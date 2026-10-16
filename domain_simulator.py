"""
Domain simulation logic and data models for Scenario 2: High-Altitude Cold Terrace
Ported and expanded from terraform-platform into pure Python.
Strict Zero-Instrument Protocol: all metrics in intuitive human/household units.
Grounded in NRCS and FAO low-tech field evaluation methodologies.
"""

from typing import Dict, List, Any, Optional

# --- Crops Data Model ---
SCENARIO_CROPS = [
    {
        "id": "radish",
        "name": "Quick Mountain Radish",
        "variety": "French Breakfast / Cherry Belle",
        "category": "fast-root",
        "nominalDays": 24,
        "minSoilDepth": "finger-length (~8 cm)",
        "frostTolerance": "high (withstands repeated needle frosts)",
        "optimalSunPct": "40% to 75% direct sun",
        "windThreshold": "Tolerates high wind if mulched with small pebbles",
        "tempRange": "Germinates in barely thawed soil (feels cool like cellar stone)",
        "howToGrow": [
            "Soil Prep: Rake out coarse stones from the top hand-depth. Form a shallow raised mound 1 hand-span wide.",
            "Sowing: Poke holes 1 finger-knuckle deep (~2 cm) spaced 2 finger-widths apart. Drop 1 seed per hole and press down gently with the flat palm.",
            "Watering: Use only solar-warmed stream water. Drench in early afternoon so excess moisture drains before night freeze.",
            "Harvest: Shoulders push up out of the soil thumb-thick in 35-38 cold days. Pluck immediately before roots turn woody."
        ],
        "criticalIssues": {
            "wind": "High mountain gales whip fine dry topsoil away from exposed hypocotyl crowns. Lay flat slate mulch between rows.",
            "sunlight": "Needs minimum 3.5 hours of direct sun. If shaded too early by the ridge, leaves grow long and spindly while root fails to swell.",
            "temperature": "Severe freezing nights (< -4 C) without stone cover cause root tissue freezing and glassy blackening."
        },
        "coldBufferMultiplier": 1.4,
        "whyItFits": "Fastest root crop available; top greens are edible in two spans of hands growth even if freeze cuts season short.",
        "failureRisk": "Pithy if left unharvested too long after bulbing; will split if hit with sudden warm spell followed by frost."
    },
    {
        "id": "turnip",
        "name": "Hardy Tokyo Turnip",
        "variety": "Tokyo White / Purple Top Milan",
        "category": "fast-root",
        "nominalDays": 35,
        "minSoilDepth": "hand-depth (~15-20 cm)",
        "frostTolerance": "high (frost converts starches into natural antifreeze sugars)",
        "optimalSunPct": "50% to 80% direct sun",
        "windThreshold": "Medium wind tolerance; outer leaves act as wind-dampers for the root crown",
        "tempRange": "Active root growth when midday soil feels neutral to bare hand-back",
        "howToGrow": [
            "Soil Prep: Work 2-3 bucketfuls of decomposed forest leaf duff into the top hand-depth. Add 1 handful of crushed wood ash per pace.",
            "Sowing: Furrow 1 finger-knuckle deep. Scatter seeds sparingly, thin to 1 palm-width apart once seedlings have two true leaves.",
            "Care: Harvest outer leaves continuously for salad and soup while the bulb develops.",
            "Storage: Winter clamp in a knee-deep pit on the terrace edge lined with dry pine duff, capped with slate slabs."
        ],
        "criticalIssues": {
            "wind": "Violent ridge drafts snap crisp leaf stems at the base. Erect low woven willow wattle hurdles on the windward side.",
            "sunlight": "Requires 4-5 hours of direct sun to sweeten root. In deep shadow, roots remain pencil-thin.",
            "temperature": "Can endure light frosts unharmed, but sustained frozen ground prevents bulb swelling and causes taproot forking."
        },
        "coldBufferMultiplier": 1.45,
        "whyItFits": "Dual harvest: outer leaves can be plucked for greens while root fattens in cool soil. Frost sweetens the root.",
        "failureRisk": "If soil is shallower than a hand depth, roots become stunted and deformed against bedrock."
    },
    {
        "id": "tatsoi-kale",
        "name": "Siberian Kale & Tatsoi Rosettes",
        "variety": "Red Russian Kale / Spoon Tatsoi",
        "category": "cold-greens",
        "nominalDays": 42,
        "minSoilDepth": "hand-depth (~15-20 cm)",
        "frostTolerance": "extreme (leaves survive direct snow encasement)",
        "optimalSunPct": "35% to 70% direct sun (thrives in partial ridge shadow)",
        "windThreshold": "Prostrate spoon shape hugs the earth, providing maximum resistance to mountain gales",
        "tempRange": "Photosynthesizes at low light and near-freezing ambient air",
        "howToGrow": [
            "Soil Prep: Loosen bed to flat hand depth. Blend in dark crumbly leaf duff and quenched charcoal powder.",
            "Sowing: Press seeds 1 knuckle deep into shallow circular pockets spaced 1 hand-span apart.",
            "Microclimate Shield: Surround with dark thermal slate stones that absorb midday radiation and radiate warmth at night.",
            "Harvest: Pick outer spoon leaves continuously; plants regenerate from center crown throughout the frost season."
        ],
        "criticalIssues": {
            "wind": "Dessicating winds suck moisture out of broad leaves. Keep soil mulched with gravelly duff.",
            "sunlight": "Very shade-tolerant. Can produce nutritious dense foliage on just 3 hours of direct sun.",
            "temperature": "Freezing dawn frosts freeze leaf cells, which must NOT be touched or stepped on while frozen; thaw naturally in midday sun."
        },
        "coldBufferMultiplier": 1.35,
        "whyItFits": "Survives repeated ice-needle morning frosts; converts starches to natural sugar antifreeze making leaves sweet.",
        "failureRisk": "Slugs hiding under stone edges can strip young seedlings if unmanaged."
    },
    {
        "id": "mache-spinach",
        "name": "Mountain Mâche & Winter Spinach",
        "variety": "Vit Mâche / Bloomsdale Winter",
        "category": "cold-greens",
        "nominalDays": 32,
        "minSoilDepth": "finger-length (~8 cm)",
        "frostTolerance": "extreme (natural cryo-protectant foliage)",
        "optimalSunPct": "30% to 60% direct sun",
        "windThreshold": "Ground-hugging rosettes unaffected by gales",
        "tempRange": "Germinates even when soil surface is barely thawed",
        "howToGrow": [
            "Soil Prep: Needs almost zero bed elevation. Clear large fist rocks and firm the fine grit surface with flat board or slate.",
            "Sowing: Broadcast pinch by pinch over soil surface; dust 1 finger-knuckle of fine humus or crushed leaf mould over top.",
            "Watering: Mist with solar-warmed water from brush broom.",
            "Harvest: Snip entire rosettes at soil line with knife, or harvest individual thumb-length leaves."
        ],
        "criticalIssues": {
            "wind": "Blowing grit can embed in leaf folds; plant behind a low stone ridge.",
            "sunlight": "Tolerates severe ridge shade. Avoid baking midday sun under unventilated covers.",
            "temperature": "Beds must not be watered late in afternoon to prevent root ice lensing overnight."
        },
        "coldBufferMultiplier": 1.35,
        "whyItFits": "Germinates even when soil feels barely thawed; thrives in thin gravelly pockets near stone walls.",
        "failureRisk": "Overheating under closed covers when noon sun is fierce; covers must be propped open on clear middays."
    },
    {
        "id": "dwarf-pea",
        "name": "Alpine Dwarf Pea",
        "variety": "Little Marvel / Oregon Sugar Pod",
        "category": "legume",
        "nominalDays": 58,
        "minSoilDepth": "hand-depth (~15-20 cm)",
        "frostTolerance": "high (vines withstand frost; flowers sensitive to hard freeze)",
        "optimalSunPct": "60% to 90% direct sun",
        "windThreshold": "Short stocky vine requires short twig brush prop to resist wind whipping",
        "tempRange": "Roots actively fix atmospheric nitrogen in cool, moist soil",
        "howToGrow": [
            "Soil Prep: Dig trench 1 hand-span deep along the sunny side of the stone retaining wall.",
            "Sowing: Pre-soak seeds in lukewarm sun-warmed water for 4 hours. Plant 1 knuckle deep, 1 hand-span apart.",
            "Support: Push dry birch or willow twigs into soil as mini climbing trellis.",
            "Harvest: Pick pods while sweet and flat; leaves and tender shoot tips are edible raw at any stage."
        ],
        "criticalIssues": {
            "wind": "Strong gusts topple un-trellised vines; always interlace with brushwood props.",
            "sunlight": "Demands maximum available terrace sun. Must be planted in the earliest-unshaded zone.",
            "temperature": "Blossoms drop if hit with sub-zero freezing wind during flowering; deploy willow hoop cloth at dusk."
        },
        "coldBufferMultiplier": 1.55,
        "whyItFits": "Fixes precious nitrogen into poor stony mountain terrace soil; blossoms endure light frosts without dropping.",
        "failureRisk": "Will abort flowers if night temperatures drop to hard freeze while blooming."
    },
    {
        "id": "chitted-potato",
        "name": "Chitted Early Mountain Potato",
        "variety": "Yukon Gold / Early Rose (Pre-sprouted)",
        "category": "tuber",
        "nominalDays": 75,
        "minSoilDepth": "forearm-depth (~35 cm)",
        "frostTolerance": "low to moderate (foliage blackens at 0 C; tubers rot in cold damp ground)",
        "optimalSunPct": "75% to 100% direct sun",
        "windThreshold": "Tall bushy foliage easily shredded by alpine gales",
        "tempRange": "Demands warmed soil; stops cell division completely below 7 C",
        "howToGrow": [
            "Chitting: Pre-sprout seed tubers in direct sunlight for 2 weeks until short, dark purple sprouts form.",
            "Bed Prep: Mandatory deep raised mound backed by dry stone wall. Soil must reach elbow crease depth.",
            "Planting: Bury tubers 1 hand-depth deep. As shoots grow, hill up with rotted leaf duff and soil.",
            "Risk Note: High caloric reward, but EXCLUDED if frost horizon is under 11-12 weeks."
        ],
        "criticalIssues": {
            "wind": "Mountain winds snap brittle stems and dry out hilled ridges rapidly.",
            "sunlight": "Requires 6+ continuous hours of fierce sun. Ridge-shaded terraces cause total tuber failure.",
            "temperature": "Lethal frost sensitivity: single freezing night destroys entire foliage canopy. Tubers rot into cold mush."
        },
        "coldBufferMultiplier": 1.5,
        "whyItFits": "High caloric density for mountain survival. BUT strictly requires pre-sprouting (chitting) and deep warmed mounds.",
        "failureRisk": "HIGH RISK: Will fail completely if summer is under 11-12 weeks or if foliage is blackened by early summer frost."
    }
]

# --- Zero-Instrument No-Lab Sensory Compass (NRCS & FAO Aligned) ---
NO_LAB_COMPASS = [
    {
        "title": "Thumb-Thick Wooden Walking Stick (Stick Strike Test)",
        "tool": "Dry pine or hazel branch, thumb thickness (~2 cm diam)",
        "usage": "Measuring True Soil Depth & Subsurface Bedrock Shelves (NRCS Soil Depth Class)",
        "procedure": "Drive the sharpened stick straight down using firm palm pressure at 5 points across the terrace. Measure penetration depth against your hand-span (~20 cm) or elbow crease (~40 cm).",
        "detail": "Penetration to wrist (<10 cm) = Lithic shallow (radish/mâche only). Penetration to mid-forearm (20-30 cm) = Moderate depth (turnips/kale). Penetration to elbow (35+ cm) = Deep terrace bed (potatoes/fava beans).",
        "realm": "DEPTH"
    },
    {
        "title": "Clear Glass Jar / Drinking Horn Slaking & Ribbon Test",
        "tool": "Glass jar, bottle, or horn filled with stream water + soil",
        "usage": "Soil Texture & Clay/Silt/Sand Fractionation (FAO Field Soil Texture Guidelines)",
        "procedure": "Take a handful of soil, moisten with spit or warmed water until it kneads like putty. Roll between palms into a pencil-thick rope, then flatten between thumb and forefinger into a ribbon. Also drop 2 handfuls in a glass jar, shake vigorously, and observe settling speed.",
        "detail": "If ribbon snaps before 1 knuckle length (<2 cm) = Sandy loam or stony scree (leaches nutrients). If ribbon reaches 2-3 knuckles (5 cm) without breaking = Cohesive loam/clay. In jar: sand drops in 1 breath, silt in 5 minutes, organic scum floats on top. Clear water above = zero organic humus.",
        "realm": "TEXTURE"
    },
    {
        "title": "Five White River Pebbles (Ridge Shadow Boundary Map)",
        "tool": "5 smooth white chalk or quartz stones placed on ground",
        "usage": "Measuring Daily Direct Sunlight Hours & Afternoon Ridge Occlusion",
        "procedure": "Place Stone 1 at the shadow line at 10 AM, Stone 2 at solar noon, Stone 3 at 2 PM, Stone 4 at 3 PM, and Stone 5 at 4 PM. Pace off the distance between shadow lines and count sunlit intervals.",
        "detail": "If terrace is in full ridge shade by Stone 3 (2 PM), total daily sun is under 4.5 hours. High-light crops (potatoes, barley) cannot finish; plant shade-tolerant brassicas and fast radishes only.",
        "realm": "SOLAR"
    },
    {
        "title": "Inner Wrist Splash & Soak Test",
        "tool": "Inner forearm & wrist skin veins (high thermoreceptor density)",
        "usage": "Glacial Stream Shock & Irrigation Safety (FAO Water Quality for Mountain Crops)",
        "procedure": "Dip inner wrist into irrigation water for 5 slow breaths. Observe physical sensation.",
        "detail": "If it triggers an involuntary recoil, sharp bone ache, or numbing chill, water is 1-3 C (meltwater shock). Pouring this on roots paralyzes cell absorption for 48 hours. Let sit in shallow dark slate pans until water feels soothingly neutral or lukewarm to the wrist.",
        "realm": "IRRIGATION"
    },
    {
        "title": "Bare Back of Hand Noon Touch (Thermal Readiness Gate)",
        "tool": "Dorsal skin of the hand pressed flat against soil",
        "usage": "Soil Germination Readiness & Root Dormancy Verification",
        "procedure": "Clear mulch away at solar noon and press the bare back of your hand firmly against the bare earth for 10 slow, deep breaths.",
        "detail": "If knuckles ache with bone-chill, the soil is dormant; seeds will rot in the ground. If soil feels neutral or gently comforting, soil temperature is primed for cold-hardy brassica and radish germination.",
        "realm": "THERMAL"
    },
    {
        "title": "Campfire Smoke & Mountain Pipit Altitude Watch",
        "tool": "Hearth fire smoke drift & native bird flight lines (Phenological Barometer)",
        "usage": "Forecasting 24-Hour Freezing Fronts & Autumn Killing Freeze",
        "procedure": "Observe evening campfire smoke: does it rise vertically or curl down and flatten along the ground? Watch flocks of alpine pipits or mountain finches.",
        "detail": "Smoke curling down and hugging the soil indicates high barometric pressure inversion and severe frost 8 hours away. Birds flocking rapidly downslope toward the valley signals an imminent killing blizzard.",
        "realm": "WEATHER"
    },
    {
        "title": "One Standard Bucket Sieve Test",
        "tool": "Standard household bucket (~10 liters) + thumb knuckle check",
        "usage": "Coarse Fragment Volumetric Ratio (NRCS Skeletal Soil Classification)",
        "procedure": "Scoop 1 bucket of terrace soil. Hand-sift every rock larger than your thumb knuckle into a second bucket.",
        "detail": "If the rock bucket fills more than half-way, coarse fraction exceeds 50% (skeletal stony soil). Requires removing 2 bucketfuls of stone chips per pace and working in 2-3 bucketfuls of spongy leaf duff.",
        "realm": "SKELETAL"
    },
    {
        "title": "Fist-Batter Wall Tilt & Shoulder Shove Test",
        "tool": "Closed fist + full shoulder body weight",
        "usage": "Terrace Retaining Wall Structural Stability & Seismic/Creep Safety",
        "procedure": "Stack dry-stone retaining wall leaning inward toward the hillside by 1 fist width for every chest-height of wall rise. Once backfilled with small rubble, push the top stone coping with full shoulder body weight.",
        "detail": "If the wall shifts, rattles, or flexes, it will collapse under mountain snowmelt hydro-static pressure. Tear down and restack with tighter stone interlocking before planting any bed behind it.",
        "realm": "STRUCTURAL"
    }
]

# --- 9-Step Roadmap Definition ---
NINE_STEPS_DEFINITION = [
    {
        "step": 1,
        "title": "INPUT ECHO",
        "sub": "Diagnostic Echo & Cue Grounding",
        "goal": "Faithfully restate mountain height, frost frequency, ridge shading, soil conditions, and separate confirmed facts from uncertainties."
    },
    {
        "step": 2,
        "title": "MISSING ANALYSIS",
        "sub": "Soil Archetype & Root Failure Diagnosis",
        "goal": "Diagnose Thin Stony Lithic Regosol, identify missing parameters (season length, soil depth, frost dates), and provide 4 zero-instrument tests."
    },
    {
        "step": 3,
        "title": "FIX PROTOCOL",
        "sub": "Quantified Remediation & Sequencing",
        "goal": "Rebuild dry-stone wall with inward batter, clear fist-sized stones, work 2-3 buckets of compost per pace, lay dark slate heat sinks."
    },
    {
        "step": 4,
        "title": "NEXT ACTION",
        "sub": "Empirical Readiness Gates",
        "goal": "Mandatory stop-point: verify 4 physical gates (wall push, hand plunge, midday back-of-hand warmth, staged covers) before planting."
    },
    {
        "step": 5,
        "title": "CROP SUGGESTIONS",
        "sub": "Rationalized Resilient Crop Options",
        "goal": "Reject the potato trap. Deploy fast cold roots (Radishes, Tokyo Turnips) and extreme greens (Siberian Kale, Mâche) matched to the season."
    },
    {
        "step": 6,
        "title": "TIMEFRAME",
        "sub": "Dual Timeline & Remediation Buffer",
        "goal": "Map 7-week cycle (49 days) with cold-slowed growth multiplier (+40% to +60%), establishing strict frost safety buffers."
    },
    {
        "step": 7,
        "title": "PLANTING METHOD",
        "sub": "Substrate Prep & Matched Irrigation",
        "goal": "Prepare shallow domed beds, sow at 1 knuckle depth, solar-warm stream water in dark basins, stage low brushwood hoops."
    },
    {
        "step": 8,
        "title": "ONGOING CARE",
        "sub": "Staged Cultivation & Stress Mitigation",
        "goal": "Execute daily twilight frost covering, feed diluted dung tea, dust hearth ash against slugs/flea beetles, ventilate on clear middays."
    },
    {
        "step": 9,
        "title": "HARVEST & REGEN",
        "sub": "Harvest Signs & Soil Regeneration",
        "goal": "Check sensory ripeness cues, execute emergency pre-freeze harvest, build winter compost cairns, and mulch beds against frost heave."
    }
]

# --- Calculation Helpers ---

def calculate_cold_adjusted_maturity(nominal_days: int, frost_freq: str = "every-dawn") -> Dict[str, Any]:
    multiplier = 1.4
    if frost_freq == "every-dawn":
        multiplier = 1.6
    elif frost_freq == "intermittent":
        multiplier = 1.45
    elif frost_freq == "rare-summer":
        multiplier = 1.3

    adjusted_days = round(nominal_days * multiplier)
    extra_days = adjusted_days - nominal_days
    return {
        "adjustedDays": adjusted_days,
        "bufferMultiplier": multiplier,
        "extraDays": extra_days,
        "explanation": f"In mountain thin air with chilling night frosts, root cell division slows down. Added a {round((multiplier - 1) * 100)}% cold buffer (+{extra_days} days) to packet time."
    }

def evaluate_crop_viability(crop: Dict[str, Any], obs: Dict[str, Any]) -> Dict[str, Any]:
    season_weeks = obs.get("estimatedSeasonWeeks", 7)
    frost_freq = obs.get("frostFrequency", "every-dawn")
    soil_depth = obs.get("soilDepth", "hand-deep")
    sunlight = obs.get("sunlightHours", "four-to-five-hours")

    available_days = season_weeks * 7
    maturity = calculate_cold_adjusted_maturity(crop["nominalDays"], frost_freq)
    adjusted_days = maturity["adjustedDays"]
    days_margin = available_days - adjusted_days

    # Depth Match
    min_depth = crop["minSoilDepth"]
    depth_match = True
    if "forearm" in min_depth and soil_depth != "forearm-deep":
        depth_match = False
    elif "hand-depth" in min_depth and soil_depth == "finger-deep":
        depth_match = False

    status = "recommended"
    reason = ""

    if days_margin < -7:
        status = "high-risk-fail"
        reason = f"FATAL CYCLE BREACH: Requires ~{adjusted_days} cold-slowed days, but summer window closes in {available_days} days. Will freeze in the ground as unharvestable roots."
    elif days_margin < 0:
        status = "high-risk-fail"
        reason = f"MARGINAL FAILURE: Requires ~{adjusted_days} days, exceeding the {available_days}-day frost horizon by {abs(days_margin)} days. Extreme freeze risk."
    elif days_margin <= 8:
        status = "viable-with-protection"
        reason = f"TIGHT MARGIN: Finishes in ~{adjusted_days} days with only a {days_margin}-day buffer. Demands dark stone mulch and strict nightly covers."
    else:
        status = "recommended"
        reason = f"EXCELLENT FIT: Finishes in ~{adjusted_days} days with a comfortable +{days_margin}-day safety buffer before killing freeze."

    if not depth_match and status != "high-risk-fail":
        status = "viable-with-protection"
        reason += f" NOTE: Requires {crop['minSoilDepth']}; existing terrace soil is shallow. Must build raised mounds behind the retaining wall."

    return {
        "crop": crop,
        "adjustedDays": adjusted_days,
        "availableDays": available_days,
        "daysMargin": days_margin,
        "status": status,
        "reason": reason
    }

def calculate_water_soak_slider(depth_cm: int, sunlight_pct: int, dark_stones: bool = True) -> Dict[str, Any]:
    # Baseline: 20cm at 100% sun = 2 hours
    base_hours = (depth_cm / 10.0) * (100.0 / max(20, sunlight_pct))
    if dark_stones:
        base_hours *= 0.75  # 25% faster convection

    estimated_hours = round(base_hours, 1)

    sun_movement = "Sun travels approximately 2 finger-widths across the sky"
    if estimated_hours > 3.0:
        sun_movement = "Sun travels half a hand-span across the southern ridge"
    elif estimated_hours < 1.5:
        sun_movement = "Sun travels barely 1 finger-width across the sky"

    wrist_feel = "Inner wrist feels neutral or gentle warmth with zero involuntary recoil or stinging chill"
    if estimated_hours > 3.5:
        wrist_feel = "Still carries slight needle chill; allow another candle-flicker of midday exposure"

    bed_timing = "Draw water at morning sunrise; pour in early afternoon (approx 1 PM to 2 PM) so soil drains before twilight frost"

    return {
        "estimatedHours": estimated_hours,
        "sunMovementUnits": sun_movement,
        "wristTouchFeel": wrist_feel,
        "recommendedBedTiming": bed_timing
    }
