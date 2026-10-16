"""
SurvivalSoilAdvisor – AI Model for High-Altitude Cold Terrace Agriculture
==========================================================================
Trained exclusively on training_data.json.
Uses TF-IDF vectorisation + cosine-similarity retrieval combined with
rule-based reasoning to walk the survivor through the 9-step protocol.

Key design principles:
  • All advice uses everyday measurements (handful, bucketful, pace, hand's depth)
  • No scientific instruments or lab readings
  • Handles the full range of mountain terrace conditions
  • Accuracy-focused: matches input signals to the closest knowledge entries
"""

import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flatten_text(obj: Any, depth: int = 0) -> str:
    """Recursively flatten a JSON object into searchable text."""
    if depth > 8:
        return ""
    if isinstance(obj, str):
        return obj + " "
    if isinstance(obj, (int, float)):
        return str(obj) + " "
    if isinstance(obj, list):
        return " ".join(_flatten_text(item, depth + 1) for item in obj)
    if isinstance(obj, dict):
        return " ".join(_flatten_text(v, depth + 1) for v in obj.values())
    return ""


def _normalise(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


# ---------------------------------------------------------------------------
# Knowledge-base document wrapper
# ---------------------------------------------------------------------------

class KnowledgeDoc:
    """One retrievable knowledge chunk."""

    def __init__(self, category: str, entry: dict):
        self.category = category
        self.entry = entry
        self.doc_id = entry.get("id", "unknown")
        self.name = entry.get("name", entry.get("method_name",
                    entry.get("technique", entry.get("practice",
                    entry.get("check_name", entry.get("condition",
                    entry.get("scenario", entry.get("method", self.doc_id))))))))
        self.text = _normalise(_flatten_text(entry))


# ---------------------------------------------------------------------------
# Main model class
# ---------------------------------------------------------------------------

class SurvivalSoilAdvisor:
    """
    AI model trained on the structured JSON knowledge base.
    Provides survival agriculture advice for high-altitude cold terraces.
    """

    # Mapping from category to the protocol step(s) it contributes to
    CATEGORY_STEP_MAP = {
        "soil_archetypes":      [1, 2, 3],
        "terrain_conditions":   [1, 2, 3],
        "frost_protection":     [3, 7, 8],
        "crops":                [5, 6, 7, 8, 9],
        "water_management":     [3, 7, 8],
        "pest_management":      [8],
        "soil_regeneration":    [9],
        "readiness_gates":      [4],
        "season_reasoning":     [2, 5, 6],
        "sunlight_assessment":  [2],
    }

    def __init__(self, data_path: str | None = None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "training_data.json")
        self.data_path = data_path
        self.raw_data: dict = {}
        self.docs: list[KnowledgeDoc] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.tfidf_matrix = None
        self._load_and_train()

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def _load_and_train(self):
        """Load JSON, build document list, fit TF-IDF vectoriser."""
        with open(self.data_path, "r", encoding="utf-8") as fh:
            self.raw_data = json.load(fh)

        # Build flat document list
        self.docs = []
        for category, entries in self.raw_data.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                self.docs.append(KnowledgeDoc(category, entry))

        corpus = [doc.text for doc in self.docs]

        # Fit TF-IDF with bigrams for better phrase matching
        self.vectorizer = TfidfVectorizer(
            max_features=6000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    # ------------------------------------------------------------------
    # Retrieval engine
    # ------------------------------------------------------------------

    def _retrieve(self, query: str, top_k: int = 5,
                  category_filter: str | None = None) -> list[tuple[KnowledgeDoc, float]]:
        """Return top-k most relevant docs for a query."""
        q_vec = self.vectorizer.transform([_normalise(query)])
        sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()

        indices = np.argsort(sims)[::-1]
        results = []
        for idx in indices:
            doc = self.docs[idx]
            score = float(sims[idx])
            if category_filter and doc.category != category_filter:
                continue
            if score < 0.01:
                break
            results.append((doc, score))
            if len(results) >= top_k:
                break
        return results

    def _retrieve_multi(self, query: str, categories: list[str],
                        per_cat: int = 3) -> dict[str, list[tuple[KnowledgeDoc, float]]]:
        """Retrieve top docs across multiple categories."""
        result = {}
        for cat in categories:
            result[cat] = self._retrieve(query, top_k=per_cat, category_filter=cat)
        return result

    # ------------------------------------------------------------------
    # Signal extraction from user input
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_signals(text: str, telemetry: dict | None = None) -> dict:
        """Parse user description and telemetry controls for environmental cues."""
        t = text.lower()
        telem = telemetry or {}
        
        # Merge telemetry strings into text for broad semantic matching
        snow_days = telem.get("snow_days", "none")
        snow_time = telem.get("snow_time", "irregular")
        sun_intensity = telem.get("sun_intensity", "moderate")
        moisture_dryness = telem.get("moisture_dryness", "moderate")
        soil_cracks = telem.get("soil_cracks", "none")
        seabody = telem.get("seabody", "none")
        alone_setting = telem.get("is_alone", None)

        signals = {
            "mentions_frost": any(w in t for w in ["frost", "freeze", "frozen", "ice", "cold night"]) or snow_days in ["frequent_snow", "daily_flurries", "heavy_blizzard"],
            "mentions_slope": any(w in t for w in ["slope", "steep", "incline", "angle"]),
            "mentions_terrace": any(w in t for w in ["terrace", "step", "flat step", "level", "bench"]),
            "mentions_wall": any(w in t for w in ["wall", "retaining", "stone wall", "dry stone"]),
            "wall_damaged": any(w in t for w in ["damaged", "broken", "collapsed", "fallen", "bulging", "crumbled"]),
            "mentions_stones": any(w in t for w in ["stone", "stony", "rocky", "gravel", "shale", "rock"]),
            "mentions_thin_soil": any(w in t for w in ["thin soil", "shallow", "barely any soil", "not much earth"]),
            "mentions_wind": any(w in t for w in ["wind", "gale", "breeze", "gust"]) or seabody != "none",
            "mentions_shade": any(w in t for w in ["shade", "shadow", "ridge", "blocked sun", "short sun"]) or sun_intensity in ["weak_shaded", "short_morning_only", "short_afternoon_only"],
            "mentions_stream": any(w in t for w in ["stream", "creek", "water source", "brook", "spring", "runoff"]),
            "mentions_short_season": any(w in t for w in ["short season", "brief summer", "not long", "few weeks"]) or snow_days in ["frequent_snow", "daily_flurries"],
            "mentions_erosion": any(w in t for w in ["erosion", "wash", "runoff", "sliding", "washed away"]),
            "mentions_organic_matter": any(w in t for w in ["compost", "leaf", "dung", "manure", "organic", "humus"]),
            "mentions_sun": any(w in t for w in ["sun", "sunlight", "bright", "warm afternoon"]) or sun_intensity in ["scorching_midday", "strong_unfiltered"],
            "mentions_alone": (alone_setting is True) or any(w in t for w in ["alone", "isolated", "solitary", "nobody", "no one", "abandoned", "no locals", "stranded"]),
            
            # Specific telemetry signals
            "snow_days": snow_days,
            "snow_time": snow_time,
            "sun_intensity": sun_intensity,
            "moisture_dryness": moisture_dryness,
            "soil_cracks": soil_cracks,
            "seabody": seabody,
            
            "soil_type_clues": [],
        }
        
        # Soil type clue detection
        if any(w in t for w in ["loam", "gritty", "crumbly"]):
            signals["soil_type_clues"].append("loam")
        if any(w in t for w in ["gravel", "scree", "rattl"]):
            signals["soil_type_clues"].append("gravel")
        if any(w in t for w in ["clay", "sticky", "heavy"]) or soil_cracks in ["deep_fissures", "surface_cracks"]:
            signals["soil_type_clues"].append("clay")
        if any(w in t for w in ["sand", "coarse", "grit"]):
            signals["soil_type_clues"].append("sand")
        if any(w in t for w in ["peat", "bog", "wet", "spongy"]) or moisture_dryness in ["waterlogged", "marshy"]:
            signals["soil_type_clues"].append("peat")
        if any(w in t for w in ["acid", "pine", "needl"]):
            signals["soil_type_clues"].append("acidic")

        return signals

    # ------------------------------------------------------------------
    # Season fitness logic
    # ------------------------------------------------------------------

    def _evaluate_season_fit(self, season_desc: str, telemetry: dict | None = None) -> dict:
        """Reason about which crops can fit the described season."""
        t = season_desc.lower()
        telem = telemetry or {}
        snow_days = telem.get("snow_days", "none")
        sun_intensity = telem.get("sun_intensity", "moderate")

        # Estimate available days heuristically
        if snow_days in ["frequent_snow", "daily_flurries"] or any(w in t for w in ["very short", "barely", "few weeks", "under two", "hyper short"]):
            est_days = 45 if snow_days == "daily_flurries" else 55
            label = "very_short"
        elif any(w in t for w in ["moderate", "reasonable", "decent", "two to three", "standard"]):
            est_days = 85
            label = "moderate"
        elif any(w in t for w in ["long", "extended", "generous", "three to four"]):
            est_days = 110
            label = "extended"
        else:
            est_days = 70  # conservative unknown
            label = "unknown"

        # Shading penalty
        if sun_intensity in ["weak_shaded", "short_morning_only", "short_afternoon_only"]:
            est_days = max(40, est_days - 10)

        viable = []
        marginal = []
        too_slow = []

        for crop_entry in self.raw_data.get("crops", []):
            drange = crop_entry.get("days_to_harvest_range", [60, 90])
            buffer = crop_entry.get("cold_buffer_days", 10)
            total_needed = drange[1] + buffer  # worst case + buffer
            best_case = drange[0]

            if best_case + buffer <= est_days:
                viable.append(crop_entry)
            elif best_case <= est_days:
                marginal.append(crop_entry)
            else:
                too_slow.append(crop_entry)

        return {
            "estimated_days": est_days,
            "season_label": label,
            "viable_crops": viable,
            "marginal_crops": marginal,
            "too_slow_crops": too_slow,
        }

    # ------------------------------------------------------------------
    # Core advisory engine — produces the full 9-step response
    # ------------------------------------------------------------------

    def advise(self, user_input: str, telemetry: dict | None = None) -> dict:
        """
        Generate a complete 9-step advisory response based on user input & telemetry.

        Returns a dict with keys step_1 through step_9, each containing
        structured advice text.
        """
        signals = self._extract_signals(user_input, telemetry)
        
        # Build expanded query incorporating telemetry details
        expanded_query = user_input + " "
        if signals["snow_days"] != "none":
            expanded_query += f" snow {signals['snow_days']} {signals['snow_time']}"
        if signals["soil_cracks"] != "none":
            expanded_query += f" soil cracks {signals['soil_cracks']}"
        if signals["moisture_dryness"] != "moderate":
            expanded_query += f" moisture {signals['moisture_dryness']}"
        if signals["seabody"] != "none":
            expanded_query += f" sea coast marine air salt spray {signals['seabody']}"
        if signals["sun_intensity"] != "moderate":
            expanded_query += f" sunlight intensity {signals['sun_intensity']}"
        
        multi = self._retrieve_multi(expanded_query, list(self.raw_data.keys()), per_cat=3)

        # ---- STEP 1: INPUT ECHO ----
        step1 = self._build_step1(user_input, signals, telemetry)

        # ---- STEP 2: MISSING ANALYSIS ----
        step2 = self._build_step2(signals, multi)

        # ---- STEP 3: FIX PROTOCOL ----
        step3 = self._build_step3(signals, multi)

        # ---- STEP 4: NEXT ACTION / READINESS GATE ----
        step4 = self._build_step4(signals, multi)

        # ---- STEP 5: CROP SUGGESTIONS ----
        season_fit = self._evaluate_season_fit(user_input, telemetry)
        step5 = self._build_step5(signals, multi, season_fit)

        # ---- STEP 6: TIMEFRAME ----
        step6 = self._build_step6(season_fit)

        # ---- STEP 7: PLANTING METHOD ----
        step7 = self._build_step7(signals, multi, season_fit)

        # ---- STEP 8: ONGOING CARE ----
        step8 = self._build_step8(signals, multi, season_fit)

        # ---- STEP 9: HARVEST & REGEN ----
        step9 = self._build_step9(signals, multi, season_fit)

        return {
            "step_1_input_echo": step1,
            "step_2_missing_analysis": step2,
            "step_3_fix_protocol": step3,
            "step_4_readiness_gate": step4,
            "step_5_crop_suggestions": step5,
            "step_6_timeframe": step6,
            "step_7_planting_method": step7,
            "step_8_ongoing_care": step8,
            "step_9_harvest_regen": step9,
            "_signals": signals,
            "_season_fit": {
                "estimated_days": season_fit["estimated_days"],
                "season_label": season_fit["season_label"],
                "viable_count": len(season_fit["viable_crops"]),
                "marginal_count": len(season_fit["marginal_crops"]),
            },
        }

    # ------------------------------------------------------------------
    # Step builders
    # ------------------------------------------------------------------

    def _build_step1(self, user_input: str, signals: dict, telemetry: dict | None = None) -> str:
        """INPUT ECHO — restate description faithfully, flag unknowns."""
        lines = ["STEP 1 — INPUT ECHO (Diagnostic Echo & Cue Grounding)", ""]
        lines.append("Based on your description and telemetry settings, here is what I understand:")
        lines.append("")

        # Echo observed conditions
        observed = []
        uncertain = []

        # Telemetry echoes
        if signals.get("snow_days") and signals["snow_days"] != "none":
            s_days = signals["snow_days"].replace("_", " ")
            s_time = signals.get("snow_time", "irregular").replace("_", " ")
            observed.append(f"Snow pattern: {s_days} occurring primarily {s_time}.")
        if signals.get("sun_intensity") and signals["sun_intensity"] != "moderate":
            s_sun = signals["sun_intensity"].replace("_", " ")
            observed.append(f"Sunlight intensity: {s_sun}.")
        if signals.get("moisture_dryness") and signals["moisture_dryness"] != "moderate":
            s_m = signals["moisture_dryness"].replace("_", " ")
            observed.append(f"Moisture status: {s_m}.")
        if signals.get("soil_cracks") and signals["soil_cracks"] != "none":
            s_c = signals["soil_cracks"].replace("_", " ")
            observed.append(f"Soil cracking: {s_c} observed across the surface.")
        if signals.get("seabody") and signals["seabody"] != "none":
            s_sea = signals["seabody"].replace("_", " ")
            observed.append(f"Proximity to sea / marine body: {s_sea} (maritime winds / salt risk present).")

        if signals["mentions_alone"]:
            observed.append("Survivor isolation: Completely alone with no local folk or settlement nearby.")
        if signals["mentions_terrace"]:
            observed.append("The plot is on a flat step or terrace on a mountain slope.")
        if signals["mentions_slope"]:
            observed.append("The terrain has a noticeable slope or incline.")
        if signals["mentions_frost"]:
            observed.append("Frost is present — cold nights with freezing risk.")
        if signals["mentions_wind"]:
            observed.append("Wind exposure is a concern — cold mountain gusts.")
        if signals["mentions_shade"]:
            observed.append("Sunlight is limited — a ridge or slope blocks the sun before evening.")
        if signals["mentions_stones"]:
            observed.append("The soil is stony — filled with rocks and gravel fragments.")
        if signals["mentions_thin_soil"]:
            observed.append("Soil is thin and shallow, possibly hitting rock not far down.")
        if signals["mentions_stream"]:
            observed.append("A water source (stream or spring) is nearby.")
        if signals["mentions_wall"]:
            if signals["wall_damaged"]:
                observed.append("A terrace retaining wall exists but appears damaged or collapsed.")
            else:
                observed.append("A stone retaining wall is present on the terrace.")
        if signals["mentions_erosion"]:
            observed.append("Signs of erosion or soil wash are visible.")

        # Things that are uncertain
        if signals.get("snow_days") in ["frequent_snow", "daily_flurries"]:
            observed.append("Growing season length: Confirmed critically compressed by recurring snow.")
        else:
            uncertain.append("Exact length of the frost-free growing season — UNKNOWN, needs observation.")
        
        uncertain.append("Precise frost arrival and departure dates — UNKNOWN, needs local signs.")
        uncertain.append("Exact soil depth across the full plot — UNKNOWN, needs probing.")
        
        if signals.get("sun_intensity") in ["short_morning_only", "short_afternoon_only"]:
            observed.append("Daily direct sun window: Restricted to half-day exposure.")
        else:
            uncertain.append("Daily hours of direct sunlight — UNKNOWN, needs shadow tracking.")

        if not signals["mentions_stream"] and signals.get("seabody") in ["none", None]:
            uncertain.append("Freshwater irrigation source location and reliability — NOT MENTIONED.")
        if not signals["mentions_wall"]:
            uncertain.append("Presence or condition of retaining walls — NOT MENTIONED.")

        for obs in observed:
            lines.append(f"  ✓ OBSERVED: {obs}")
        lines.append("")
        for unc in uncertain:
            lines.append(f"  ⚠ UNCERTAIN: {unc}")

        if not observed:
            lines.append("  (No specific terrain features were mentioned — please describe what you see: slope, rocks, walls, shade, frost signs, water.)")

        return "\n".join(lines)

    def _build_step2(self, signals: dict, multi: dict) -> str:
        """MISSING ANALYSIS — soil archetype + what's missing + how to find out."""
        lines = ["STEP 2 — MISSING ANALYSIS (Soil Archetype & Root Failure Diagnosis)", ""]

        # Best-match soil archetype
        soil_hits = multi.get("soil_archetypes", [])
        if soil_hits:
            best_soil = soil_hits[0][0]
            lines.append(f"SOIL ARCHETYPE IDENTIFIED: {best_soil.name}")
            lines.append(f"  {best_soil.entry.get('description', '')}")
            lines.append("")

            # Dominant failures
            failures = best_soil.entry.get("dominant_failures", [])
            if failures:
                lines.append("ROOT FAILURE FACTORS:")
                for f in failures:
                    lines.append(f"  ✗ {f}")
                lines.append("")
        else:
            lines.append("SOIL ARCHETYPE: Cannot be determined from description alone.")
            lines.append("  → Perform the hand tests below to identify your soil.")
            lines.append("")

        # What is missing and how to find out
        lines.append("WHAT IS MISSING — and how to find out with your hands:")
        lines.append("")

        # Always include key missing items
        season_method = (
            "Since you are completely alone with no local folk to ask, rely strictly on natural indicators: "
            "Track alpine phenology — watch for the first wild mountain flowers (like alpine gentians or buttercups) blooming to mark the spring thaw. "
            "Track the snow line on surrounding peaks: as it retreats upward, your window opens. "
            "Count days between the last dawn frost that freezes dew on grass blades and the first autumn freeze. "
            "Watch high-altitude bird migrations: when mountain pipits or thrushes begin flocking downslope, killing frost is 2 to 3 weeks away."
            if signals.get("mentions_alone") else
            "Ask any local folk when snow stays and leaves. If no one is near, watch for the first wild mountain flowers blooming to mark the thaw. "
            "Count the days between the last hard frost you feel on your face at dawn and the first autumn morning that freezes the dew on grass blades."
        )

        missing_items = [
            ("Season Length", season_method),
            ("Frost Dates", "Each morning at first light, check the ground: if dew glistens on leaf tips, it stayed above freezing; if blades crunch like thin glass underfoot, frost struck. Mark a stone each frost morning to build a pattern."),
            ("Soil Depth", "Push a straight stick (thick as your thumb) straight down with steady palm pressure. Where it stops, that's your root limit. Test in at least five spots across the plot — soil depth can change within a few paces on a terrace."),
            ("Sunlight Hours", "Place a line of small pale stones along the shadow edge at the same time each day for five days. If the shadow line moves inward (less sun), note it. Count the span from when the sun first warms your face in the morning to when the ridge steals it."),
        ]

        if signals["mentions_wall"] and signals["wall_damaged"]:
            missing_items.append(("Wall Integrity",
                "Lean your full shoulder weight against the wall at several points. If it shifts or stones rattle loose, it needs rebuilding before the bed behind it can hold soil through a rainstorm."))

        # Sunlight assessment methods from KB
        sun_hits = multi.get("sunlight_assessment", [])
        if sun_hits:
            best_sun = sun_hits[0][0]
            missing_items.append(("Sun Exposure Detail",
                f"{best_sun.entry.get('procedure', 'Track the shadow line with stones daily.')}"))

        for title, method in missing_items:
            lines.append(f"   {title}:")
            lines.append(f"     {method}")
            lines.append("")

        # Include hand tests from best-match soil
        if soil_hits:
            tests = soil_hits[0][0].entry.get("hand_tests", [])
            if tests:
                lines.append("DIAGNOSTIC HAND TESTS TO CONFIRM SOIL TYPE:")
                for t in tests:
                    lines.append(f"   {t['test_name']}:")
                    lines.append(f"     How: {t['procedure']}")
                    lines.append(f"     Reading: {t['interpretation']}")
                    lines.append("")

        return "\n".join(lines)

    def _build_step3(self, signals: dict, multi: dict) -> str:
        """FIX PROTOCOL — step-by-step remediation with everyday amounts."""
        lines = ["STEP 3 — FIX PROTOCOL (Quantified Remediation & Sequencing)", ""]
        lines.append("Complete these fixes IN ORDER before any planting:")
        lines.append("")

        fix_number = 1

        # A) Wall repair if needed
        if signals["mentions_wall"] and signals["wall_damaged"]:
            terrain_hits = multi.get("terrain_conditions", [])
            wall_entry = None
            for doc, _ in terrain_hits:
                if "wall" in doc.doc_id or "wall" in doc.name.lower():
                    wall_entry = doc.entry
                    break
            if wall_entry:
                fixes = wall_entry.get("fixes", [])
                lines.append(f"  FIX {fix_number}: WALL REPAIR (Critical — do first)")
                for f in fixes:
                    lines.append(f"    → {f.get('action', '')}: {f.get('method', '')}")
                    if f.get('everyday_amount'):
                        lines.append(f"      Amount: {f['everyday_amount']}")
                lines.append("")
                fix_number += 1
            else:
                lines.append(f"  FIX {fix_number}: WALL REPAIR")
                lines.append("    → Clear fallen stones. Rebuild from the bottom up, largest flattest stones at the base.")
                lines.append("    → Tilt the wall slightly into the hillside (lean it back about a fist-width per arm's height).")
                lines.append("    → Pack angular rubble behind the face stones. Never use round river stones or mud.")
                lines.append("    → Cap with heavy flat stones to lock the courses together.")
                lines.append("")
                fix_number += 1

        # B) Soil cracks remediation if detected
        if signals.get("soil_cracks") in ["deep_fissures", "surface_cracks"]:
            lines.append(f"  FIX {fix_number}: SOIL CRACK SEALING & STRUCTURE REPAIR")
            lines.append("    → Surface cracks indicate severe clay shrinkage or organic desiccation.")
            lines.append("    → Pack cracks with three double-handfuls of weathered leaf mould and coarse sand per pace.")
            lines.append("    → Do NOT leave open cracks: dry mountain winds penetrate deep fissures and freeze lower roots.")
            lines.append("    → Lightly scratch the top two finger-widths to break crust capillaries and stop water evaporation.")
            lines.append("")
            fix_number += 1

        # C) Marine / Salt air remediation if near sea
        if signals.get("seabody") in ["coastal_cliff", "sea_in_view", "fjord_bay"]:
            lines.append(f"  FIX {fix_number}: COASTAL SALT SPRAY & MARITIME WIND DEFENSE")
            lines.append("    → Coastal mountain air carries caustic salt aerosol that burns tender seedlings.")
            lines.append("    → Erect a dense wattle hurdle of conifer boughs and driftwood along the seaward edge.")
            lines.append("    → Dust planting beds with two handfuls of crushed campfire charcoal to bind marine sodium.")
            lines.append("    → Avoid watering with brackish littoral pools — rely strictly on upland freshwater runoff.")
            lines.append("")
            fix_number += 1

        # D) Soil remediation from best-match archetype
        soil_hits = multi.get("soil_archetypes", [])
        if soil_hits:
            best_soil = soil_hits[0][0]
            rem_steps = best_soil.entry.get("remediation_steps", [])
            for rs in rem_steps:
                lines.append(f"  FIX {fix_number}: {rs.get('action', 'Soil Amendment')}")
                lines.append(f"    Materials: {rs.get('materials', 'Local organic matter')}")
                lines.append(f"    Amount: {rs.get('amount', 'A generous helping per pace of bed')}")
                lines.append(f"    Purpose: {rs.get('purpose', '')}")
                lines.append("")
                fix_number += 1

        # E) Water management setup
        water_hits = multi.get("water_management", [])
        if water_hits:
            best_water = water_hits[0][0]
            lines.append(f"  FIX {fix_number}: WATER SETUP — {best_water.name}")
            lines.append(f"    {best_water.entry.get('procedure', '')}")
            if best_water.entry.get("warnings"):
                lines.append(f"    ⚠ Warning: {best_water.entry['warnings']}")
            lines.append("")
            fix_number += 1

        # F) Frost / Snow protection prep
        frost_hits = multi.get("frost_protection", [])
        if frost_hits:
            best_frost = frost_hits[0][0]
            lines.append(f"  FIX {fix_number}: FROST & SNOW PROTECTION PREP — {best_frost.name}")
            if signals.get("snow_days") in ["frequent_snow", "daily_flurries", "heavy_blizzard"]:
                lines.append("    → A-FRAME STOOKING: Build peaked wooden ridge sticks over beds to shed heavy snow weight.")
                lines.append("    → Flat covers will collapse under wet mountain snow and crush young crops.")
            proc = best_frost.entry.get("procedure", "")
            if isinstance(proc, list):
                for p in proc:
                    if isinstance(p, dict):
                        lines.append(f"    → Step {p.get('step','-')}: {p.get('action','')}")
                    else:
                        lines.append(f"    → {p}")
            else:
                lines.append(f"    {proc}")
            lines.append("")

        return "\n".join(lines)

    def _build_step4(self, signals: dict, multi: dict) -> str:
        """READINESS GATE — pass/fail checks before planting."""
        lines = ["STEP 4 — NEXT ACTION (Empirical Readiness Gate)", ""]
        lines.append("DO NOT PLANT until every gate below shows PASS:")
        lines.append("")

        gate_hits = multi.get("readiness_gates", [])
        gates = [doc.entry for doc, _ in gate_hits]

        if not gates:
            gates = self.raw_data.get("readiness_gates", [])[:5]

        # Extra dynamic gates based on telemetry
        if signals.get("soil_cracks") in ["deep_fissures", "surface_cracks"]:
            lines.append("  ☐ Soil Crack Closure Gate:")
            lines.append("     Test: Inspect the bed surface at three paces distance in bright light.")
            lines.append("     PASS if: No fissures wider than a straw remain open; leaf duff mulch completely caps fissures.")
            lines.append("     If FAIL: Pack more sand/leaf duff into gaps before any sowing.")
            lines.append("")

        if signals.get("snow_days") in ["frequent_snow", "daily_flurries"]:
            lines.append("  ☐ Snow Load Ridge-Frame Gate:")
            lines.append("     Test: Press both hands firmly down on the apex of your wooden A-frame cover.")
            lines.append("     PASS if: Frame bears heavy palm weight without bowing or collapsing.")
            lines.append("     If FAIL: Add center prop sticks every two paces.")
            lines.append("")

        for g in gates:
            lines.append(f"  ☐ {g.get('check_name', 'Check')}:")
            lines.append(f"     Test: {g.get('procedure', '')}")
            lines.append(f"     PASS if: {g.get('pass_criteria', '')}")
            lines.append(f"     If FAIL: {g.get('fail_action', 'Repeat the relevant fix step.')}")
            lines.append("")

        return "\n".join(lines)

    def _build_step5(self, signals: dict, multi: dict,
                     season_fit: dict) -> str:
        """CROP SUGGESTIONS — rationalized against site signals."""
        lines = ["STEP 5 — CROP SUGGESTIONS (Rationalized Resilient Crop Options)", ""]

        if season_fit["viable_crops"]:
            lines.append("VIABLE CROPS (can complete their full cycle in your estimated season):")
            lines.append("")
            for crop in season_fit["viable_crops"]:
                dr = crop["days_to_harvest_range"]
                lines.append(f"   {crop['name']}")
                lines.append(f"     Days to harvest: {dr[0]}–{dr[1]} days + {crop.get('cold_buffer_days',0)} cold-buffer days")
                lines.append(f"     Frost tolerance: {crop.get('frost_tolerance','moderate_frost').replace('_',' ').title()}")
                lines.append(f"     Soil needs: {crop.get('soil_needs','')}")
                lines.append(f"     Why it fits: {crop.get('season_fit_logic','')}")
                lines.append("")

        if season_fit["marginal_crops"]:
            lines.append("MARGINAL CROPS (might finish — only if season turns out longer than expected):")
            lines.append("")
            for crop in season_fit["marginal_crops"]:
                dr = crop["days_to_harvest_range"]
                lines.append(f"  ⚠ {crop['name']}")
                lines.append(f"     Days: {dr[0]}–{dr[1]} + {crop.get('cold_buffer_days',0)} buffer")
                lines.append(f"     Risk: may not mature before hard frost.")
                lines.append("")

        if season_fit["too_slow_crops"]:
            lines.append("TOO SLOW FOR THIS SEASON:")
            for crop in season_fit["too_slow_crops"]:
                lines.append(f"  ✗ {crop['name']} — needs {crop['days_to_harvest_range'][0]}–{crop['days_to_harvest_range'][1]} days minimum, will NOT finish.")
            lines.append("")

        if not season_fit["viable_crops"] and not season_fit["marginal_crops"]:
            lines.append("⚠ WARNING: No crops in the knowledge base can reliably finish in your estimated season.")
            lines.append("  Consider building soil now and planting only when you can confirm a longer window.")
            lines.append("")

        return "\n".join(lines)

    def _build_step6(self, season_fit: dict) -> str:
        """TIMEFRAME — dual timeline with remediation buffer."""
        lines = ["STEP 6 — TIMEFRAME (Dual Timeline & Remediation Buffer)", ""]

        lines.append(f"ESTIMATED SEASON: ~{season_fit['estimated_days']} days ({season_fit['season_label'].replace('_',' ').title()})")
        lines.append("")
        lines.append("REMEDIATION PHASE (before any seed touches the soil):")
        lines.append("  Wall repair + soil fixes + frost prep: 7–14 days depending on damage")
        lines.append("  Readiness gate testing: 1–2 days")
        lines.append("")
        lines.append("CROP MATURITY (under cold-stress conditions):")
        lines.append("")

        for crop in season_fit["viable_crops"]:
            dr = crop["days_to_harvest_range"]
            buf = crop.get("cold_buffer_days", 0)
            total_min = dr[0] + buf
            total_max = dr[1] + buf
            lines.append(f"  {crop['name']}: {dr[0]}–{dr[1]} days + {buf} cold-buffer = {total_min}–{total_max} total")
            rem_days = season_fit["estimated_days"] - total_max
            if rem_days > 0:
                lines.append(f"    → Fits with ~{rem_days} days to spare ✓")
            elif rem_days == 0:
                lines.append(f"    → Tight fit — no margin for delay ⚠")
            else:
                lines.append(f"    → May overshoot by ~{abs(rem_days)} days ⚠ (marginal)")
            lines.append("")

        lines.append("NOTE: Cold mountain soil slows growth. These estimates include a cold-buffer,")
        lines.append("but if your plot loses sun early due to ridge shadow, add extra days.")
        lines.append("If a crop plainly will not finish, do NOT plant it — focus on the fastest options.")

        return "\n".join(lines)

    def _build_step7(self, signals: dict, multi: dict,
                     season_fit: dict) -> str:
        """PLANTING METHOD — bed prep, sowing, frost protection, water warming."""
        lines = ["STEP 7 — PLANTING METHOD (Substrate Prep & Matched Irrigation)", ""]

        lines.append("BED PREPARATION:")
        lines.append("  1. Clear stones larger than a fist from the planting row.")
        lines.append("  2. Loosen the top one hand's depth with a digging stick or forked branch.")
        lines.append("  3. Mix in two double-handfuls of composted leaf mould per pace of bed.")
        lines.append("  4. Shape the bed slightly higher in the centre (a gentle dome, not flat) so cold")
        lines.append("     water drains to the edges rather than pooling on seedling roots.")
        lines.append("")

        # Crop-specific planting info
        lines.append("SOWING GUIDANCE (for your viable crops):")
        lines.append("")
        for crop in season_fit["viable_crops"][:6]:
            lines.append(f"   {crop['name']}:")
            lines.append(f"     Planting depth: {crop.get('planting_depth', 'one finger knuckle deep')}")
            lines.append(f"     Spacing: {crop.get('spacing', 'one hand span apart')}")
            # Get first growth stage
            stages = crop.get("growth_stages", [])
            if stages:
                first = stages[0]
                lines.append(f"     First stage ({first.get('stage_name','seedling')}): {first.get('care_notes','Keep moist and sheltered.')}")
                if first.get("frost_handling"):
                    lines.append(f"     Frost handling: {first['frost_handling']}")
            lines.append("")

        # Water warming
        lines.append("WATER WARMING (critical — cold stream water shocks roots):")
        water_hits = multi.get("water_management", [])
        if water_hits:
            for doc, _ in water_hits[:2]:
                lines.append(f"   {doc.name}:")
                lines.append(f"     {doc.entry.get('procedure', '')}")
                lines.append("")
        else:
            lines.append("  Fill buckets or hollowed logs from the stream in the morning.")
            lines.append("  Let them sit in full sun all day. Water plants in the late afternoon")
            lines.append("  with this sun-warmed water — never pour icy stream water directly on roots.")
            lines.append("")

        # Frost protection during planting
        lines.append("SEEDLING FROST PROTECTION:")
        frost_hits = multi.get("frost_protection", [])
        if frost_hits:
            for doc, _ in frost_hits[:2]:
                lines.append(f"  ❄ {doc.name}:")
                proc = doc.entry.get("procedure", "")
                if isinstance(proc, list):
                    for p in proc[:3]:
                        if isinstance(p, dict):
                            lines.append(f"    → {p.get('action','')}")
                        else:
                            lines.append(f"    → {p}")
                else:
                    lines.append(f"    {proc[:300]}")
                lines.append("")

        return "\n".join(lines)

    def _build_step8(self, signals: dict, multi: dict,
                     season_fit: dict) -> str:
        """ONGOING CARE — staged cultivation, pest watch, stress mitigation."""
        lines = ["STEP 8 — ONGOING CARE (Staged Cultivation & Stress Mitigation)", ""]

        # Growth stage journey for top viable crops
        lines.append("CROP JOURNEY BY GROWTH STAGE:")
        lines.append("")
        for crop in season_fit["viable_crops"][:4]:
            lines.append(f"  ── {crop['name']} ──")
            stages = crop.get("growth_stages", [])
            for s in stages:
                lines.append(f"    Stage: {s.get('stage_name', '?')}")
                lines.append(f"      Duration: {s.get('duration_description', '?')}")
                lines.append(f"      Care: {s.get('care_notes', '')}")
                if s.get("frost_handling"):
                    lines.append(f"      Frost night: {s['frost_handling']}")
            lines.append("")

        # Frost-night protocol
        lines.append("FROST-NIGHT EMERGENCY PROTOCOL:")
        lines.append("  1. Before sunset: cover all beds with conifer boughs, straw, or cloth draped over sticks.")
        lines.append("  2. Weigh down edges with heavy stones so wind cannot lift covers.")
        lines.append("  3. If you have water containers, place them inside the cover — they release heat as they cool.")
        lines.append("  4. At first light: check for frost damage (blackened, limp leaves). Remove covers once sun warms.")
        lines.append("")

        # Pest and disease watch
        lines.append("PEST & DISEASE WATCH (cool damp mountain conditions):")
        lines.append("")
        pest_hits = multi.get("pest_management", [])
        if pest_hits:
            for doc, _ in pest_hits[:4]:
                entry = doc.entry
                lines.append(f"   {entry.get('pest_name', doc.name)}:")
                lines.append(f"     Signs: {entry.get('signs_to_watch', '')}")
                lines.append(f"     Favoured by: {entry.get('conditions_that_favor', '')}")
                controls = entry.get("bio_controls", [])
                if controls:
                    for ctrl in controls[:2]:
                        if isinstance(ctrl, dict):
                            lines.append(f"     Bio-control: {ctrl.get('method', ctrl.get('ingredients',''))}")
                            if ctrl.get("procedure"):
                                lines.append(f"       How: {ctrl['procedure']}")
                        else:
                            lines.append(f"     Bio-control: {ctrl}")
                companions = entry.get("companion_planting_deterrents", "")
                if companions:
                    lines.append(f"     Companion deterrent: {companions}")
                lines.append("")

        # Fertiliser for cold soil
        lines.append("COLD-SOIL FERTILITY BOOST:")
        lines.append("  Every two weeks, water beds with diluted dung tea (a handful of aged animal")
        lines.append("  dung stirred into a bucketful of sun-warmed water, strained through cloth).")
        lines.append("  This feeds both the plants and the soil microbes that are sluggish in the cold.")
        lines.append("")

        return "\n".join(lines)

    def _build_step9(self, signals: dict, multi: dict, season_fit: dict) -> str:
        """HARVEST & REGEN — ripeness signs, harvest, storage, soil regeneration."""
        lines = ["STEP 9 — HARVEST & REGEN (Harvest Signs & Soil Regeneration)", ""]

        # Ripeness signs for viable crops
        lines.append("RIPENESS SIGNS (harvest by sight and touch — no instruments):")
        lines.append("")
        for crop in season_fit["viable_crops"][:6]:
            signs = crop.get("ripeness_signs", [])
            lines.append(f"   {crop['name']}:")
            for sign in signs:
                lines.append(f"     • {sign}")
            if crop.get("harvest_method"):
                lines.append(f"     Harvest: {crop['harvest_method']}")
            if crop.get("storage_notes"):
                lines.append(f"     Storage: {crop['storage_notes']}")
            lines.append("")

        lines.append("⚠ HARVEST BEFORE HARD FREEZE:")
        lines.append("  When you see the warning signs (ground frozen hard at dawn two mornings running,")
        lines.append("  mountain birds flocking downslope, first dusting of snow on the ridge above),")
        lines.append("  harvest EVERYTHING — even slightly unripe. A frozen crop in the ground feeds nobody.")
        lines.append("")

        # Soil regeneration
        lines.append("POST-HARVEST SOIL REGENERATION:")
        lines.append("")
        regen_hits = multi.get("soil_regeneration", [])
        if regen_hits:
            for doc, _ in regen_hits[:4]:
                entry = doc.entry
                lines.append(f"   {entry.get('practice', doc.name)}:")
                lines.append(f"     When: {entry.get('when_to_do', 'After final harvest')}")
                lines.append(f"     How: {entry.get('procedure', '')}")
                lines.append(f"     Benefit: {entry.get('benefit', '')}")
                lines.append("")
        else:
            lines.append("  1. Chop all crop stalks and leaves and spread them across the bed as mulch.")
            lines.append("  2. Scatter a handful of wood ash per pace to return minerals.")
            lines.append("  3. If possible, sow a quick cover of cereal rye or hardy vetch to hold the soil over winter.")
            lines.append("  4. Repair any wall stones loosened during the season.")
            lines.append("")

        lines.append("WALL UPKEEP:")
        lines.append("  Before winter storms: walk the full wall, push-test each section,")
        lines.append("  re-pack any loose hearting stones, and replace any coping stones")
        lines.append("  dislodged by freeze-thaw cycles.")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Quick query — answer a specific question
    # ------------------------------------------------------------------

    def query(self, question: str, top_k: int = 5) -> str:
        """Answer a specific question by retrieving the most relevant knowledge."""
        results = self._retrieve(question, top_k=top_k)
        if not results:
            return "I don't have enough information in my knowledge base to answer that. Please describe your terrain, soil, and conditions in more detail."

        lines = [f"Based on my training data, here is what I know about: \"{question}\"", ""]
        for doc, score in results:
            lines.append(f"[{doc.category} / {doc.name}] (relevance: {score:.2f})")
            # Summarise the entry
            entry = doc.entry
            if "description" in entry:
                lines.append(f"  {entry['description'][:200]}")
            if "procedure" in entry:
                proc = entry["procedure"]
                if isinstance(proc, str):
                    lines.append(f"  Procedure: {proc[:200]}")
            if "remediation_steps" in entry:
                for rs in entry["remediation_steps"][:3]:
                    lines.append(f"  → {rs.get('action','')}: {rs.get('amount','')}")
            if "pass_criteria" in entry:
                lines.append(f"  Pass criteria: {entry['pass_criteria']}")
            lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    advisor = SurvivalSoilAdvisor()
    print(f"Model loaded: {len(advisor.docs)} knowledge documents")
    print(f"TF-IDF vocabulary size: {len(advisor.vectorizer.vocabulary_)}")
    print()

    test_input = (
        "I woke up on a mountain slope, on a flat step that was once a terrace. "
        "The mornings bring frost, the afternoon sun is strong but a ridge blocks it by mid-afternoon. "
        "The soil is thin, stony, full of gravel and shale fragments. "
        "There is a damaged stone wall at the front of the terrace. "
        "A stream runs below. I don't know how long summer will last. "
        "The wind is cold and constant."
    )

    result = advisor.advise(test_input)
    for key, value in result.items():
        if key.startswith("_"):
            continue
        print("=" * 70)
        print(value)
        print()
