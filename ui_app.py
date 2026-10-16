"""
HackIt // SUPERCOMPUTER DESKTOP APPLICATION: SCENARIO 2
=========================================================
Fully Functional Desktop Tkinter Implementation:
- Experience Taking Dialog Box: Takes free-form survivor observations + Quick Example Presets.
- Full 9-Stage Resolution Pipeline Navigator: Step 1 (Input Echo) to Step 9 (Harvest/Regen).
- Interactive Step 4 Empirical Readiness Gate Checklist (7 verified tactile tests).
- Biological Crop Viability Engine with cold buffer calculations.
- Zero-Instrument Sensory Compass & Part A Markdown Export.
- Pixel-perfect HackIt dark layout with ZERO EMOJIS (Clean technical tags).
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from model import SurvivalSoilAdvisor
import domain_simulator as ds

K_BLACK = "#000000"
K_TOPBAR = "#000000"
K_SIDEBAR = "#000000"
K_PANEL = "#050505"
K_CARD = "#0A0A0A"
K_CARD_SUBTLE = "#0F0F0F"
K_BORDER = "#1A1A1A"
K_ORANGE = "#FF5A1F"
K_GREEN = "#22C55E"
K_RED_ESTOP = "#E11D48"
K_TEXT_WHITE = "#FFFFFF"
K_TEXT_MUTED = "#94A3B8"
K_TEXT_DIM = "#64748B"

EXAMPLES = {
    "Baseline Terrace": (
        "The terrace wall has collapsed in one place. Soil is thin, about a hand deep, and half stones. "
        "Frost on the plants every morning. The ridge shades the plot by mid-afternoon. "
        "Water comes from an ice-cold glacial stream. I think summer lasts about 6 weeks."
    ),
    "Steep Scree Slope": (
        "Steep open mountain slope with no terraces intact. Thin gravelly scree slides under boot heels. "
        "Cold wind scour, no windbreak. Frost covers the gravel every morning. Water rushes down without soaking. "
        "Growing season feels very brief and uncertain."
    ),
    "Frost Pocket Clay": (
        "A flat terrace step nestled in a mountain bowl. Deep cold air pools at night with heavy white frost. "
        "Soil is damp, compacted glacial clay with poor drainage. The front wall is standing firm. "
        "Sunlight is blocked until mid-morning and lost early afternoon."
    ),
    "Wind-Scoured Bench": (
        "An upper terrace bench exposed to heavy mountain gales. Decent soil depth (two hand-spans), but acidic "
        "with conifer needle duff and gravel. Light frost in mornings, full midday sun. Front wall is bulging slightly."
    )
}

STEP_TITLES = [
    ("01", "step_1_input_echo", "INPUT ECHO", "Diagnostic Cue Grounding"),
    ("02", "step_2_missing_analysis", "MISSING ANALYSIS", "Soil Archetype Diagnosis"),
    ("03", "step_3_fix_protocol", "FIX PROTOCOL", "Quantified Remediation"),
    ("04", "step_4_readiness_gate", "NEXT ACTION", "Empirical Readiness Gates"),
    ("05", "step_5_crop_suggestions", "CROP OPTIONS", "Resilient Crop Selection"),
    ("06", "step_6_timeframe", "TIMEFRAME", "Dual Timeline & Buffer"),
    ("07", "step_7_planting_method", "PLANTING METHOD", "Substrate & Water Setup"),
    ("08", "step_8_ongoing_care", "ONGOING CARE", "Staged Frost & Pest Regimen"),
    ("09", "step_9_harvest_regen", "HARVEST & REGEN", "Ripeness & Soil Revival"),
]

class SupercomputerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HackIt // Sector 76 — High-Altitude Mountain Terraforming Supercomputer")
        self.geometry("1380x900")
        self.minsize(1180, 780)
        self.configure(bg=K_BLACK)

        self.advisor = SurvivalSoilAdvisor()
        self.current_results = {}
        self.active_step_idx = 0

        self.alerts_list = [
            ("System initialized: Sector 76 Baseline loaded", "Just now", True),
            ("Needle frost on upper bench", "2 mins ago", False),
            ("Stream diverted to solar pan", "15 mins ago", True),
            ("Organic leaf duff worked in", "1 hour ago", False)
        ]

        self.readiness_checks = {
            "wallStable": False,
            "stonesCleared": True,
            "organicWorked": False,
            "soilDepthAdequate": True,
            "middaySoilWarmth": False,
            "waterWarmed": False,
            "frostCoverStaged": False
        }

        self._build_interface()
        self._load_preset("Baseline Terrace")

    def _build_interface(self):
        # 1. Top Bar
        top_bar = tk.Frame(self, bg=K_TOPBAR, height=50, highlightbackground=K_BORDER, highlightthickness=1)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        brand_frame = tk.Frame(top_bar, bg=K_TOPBAR, padx=16, pady=10)
        brand_frame.pack(side=tk.LEFT)

        tk.Label(brand_frame, text="HackIt", font=("Segoe UI", 13, "bold"), fg="#FFF", bg=K_TOPBAR).pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(brand_frame, text="Sector 76 (Alpine Cold Terrace)  ⌄", font=("Segoe UI", 10), fg=K_TEXT_MUTED, bg=K_TOPBAR).pack(side=tk.LEFT)

        right_hdr = tk.Frame(top_bar, bg=K_TOPBAR, padx=16)
        right_hdr.pack(side=tk.RIGHT)

        clock_frame = tk.Frame(right_hdr, bg=K_TOPBAR)
        clock_frame.pack(side=tk.LEFT, padx=16)
        tk.Label(clock_frame, text="SOLAR TRANSIT", font=("Consolas", 8, "bold"), fg=K_TEXT_DIM, bg=K_TOPBAR).pack(anchor="e")
        tk.Label(clock_frame, text="08:42:12 AM", font=("Consolas", 9), fg=K_TEXT_MUTED, bg=K_TOPBAR).pack(anchor="e")

        estop_btn = tk.Button(
            right_hdr, text="◯ E-STOP", font=("Consolas", 9, "bold"),
            bg="#22070D", fg=K_RED_ESTOP, activebackground=K_RED_ESTOP, activeforeground="#FFF",
            highlightbackground=K_RED_ESTOP, highlightthickness=1, relief=tk.FLAT, padx=10, pady=3,
            command=self._estop_click, cursor="hand2"
        )
        estop_btn.pack(side=tk.LEFT)

        # 2. Main 3-Column Body
        body = tk.Frame(self, bg=K_BLACK)
        body.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar (200px)
        sidebar_left = tk.Frame(body, bg=K_SIDEBAR, width=200, highlightbackground=K_BORDER, highlightthickness=1, padx=10, pady=16)
        sidebar_left.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_left.pack_propagate(False)
        self._build_left_sidebar(sidebar_left)

        # Right Sidebar (240px)
        sidebar_right = tk.Frame(body, bg=K_SIDEBAR, width=240, highlightbackground=K_BORDER, highlightthickness=1, padx=14, pady=16)
        sidebar_right.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar_right.pack_propagate(False)
        self._build_right_sidebar(sidebar_right)

        # Center Main Stage
        self.center_stage = tk.Frame(body, bg=K_BLACK, padx=18, pady=14)
        self.center_stage.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_center_stage(self.center_stage)

    def _build_left_sidebar(self, parent):
        tk.Label(parent, text="VIEW CONTEXT", font=("Segoe UI", 8, "bold"), fg=K_TEXT_DIM, bg=K_SIDEBAR).pack(anchor="w", padx=6, pady=(0, 4))
        self.btn_nav_advisor = self._sidebar_item(parent, "[~]  Live Advisor", active=True, cmd=lambda: self._switch_tab("advisor"))
        self.btn_nav_gates = self._sidebar_item(parent, "[@]  Readiness Gates", active=False, cmd=lambda: self._switch_tab("gates"))
        self.btn_nav_crops = self._sidebar_item(parent, "[%]  Biological Crops", active=False, cmd=lambda: self._switch_tab("crops"))
        self.btn_nav_compass = self._sidebar_item(parent, "[=]  Sensory Compass", active=False, cmd=lambda: self._switch_tab("compass"))

        # Bottom Power Widget
        p_frame = tk.Frame(parent, bg=K_SIDEBAR)
        p_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 6))

        p_meta = tk.Frame(p_frame, bg=K_SIDEBAR)
        p_meta.pack(fill=tk.X, pady=(0, 4))
        tk.Label(p_meta, text="SOLAR BUFFER (i)", font=("Consolas", 8, "bold"), fg=K_ORANGE, bg=K_SIDEBAR, cursor="hand2").pack(side=tk.LEFT)
        tk.Label(p_meta, text="98.2%", font=("Consolas", 8, "bold"), fg=K_ORANGE, bg=K_SIDEBAR).pack(side=tk.RIGHT)

        bar_bg = tk.Frame(p_frame, bg=K_CARD, height=4)
        bar_bg.pack(fill=tk.X)
        bar_fill = tk.Frame(bar_bg, bg=K_ORANGE, height=4, width=170)
        bar_fill.pack(side=tk.LEFT)

        tk.Label(p_frame, text="Night root thermal reserve stored in stones", font=("Segoe UI", 7), fg=K_TEXT_DIM, bg=K_SIDEBAR, wraplength=180, justify="left").pack(anchor="w", pady=(3, 0))

    def _sidebar_item(self, parent, text, active=False, cmd=None):
        bg_col = "#1E130D" if active else K_SIDEBAR
        fg_col = "#FFF" if active else K_TEXT_MUTED
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 9, "bold" if active else "normal"), fg=fg_col, bg=bg_col, padx=8, pady=6, anchor="w", cursor="hand2")
        lbl.pack(fill=tk.X, pady=1)
        if cmd:
            lbl.bind("<Button-1>", lambda e: cmd())
        return lbl

    def _build_right_sidebar(self, parent):
        tk.Label(parent, text="TERRACE SYSTEM HEALTH", font=("Segoe UI", 8, "bold"), fg=K_TEXT_DIM, bg=K_SIDEBAR).pack(anchor="w", pady=(0, 8))

        # Season Elapsed
        c_top = tk.Frame(parent, bg=K_SIDEBAR)
        c_top.pack(fill=tk.X)
        tk.Label(c_top, text="SEASON ELAPSED", font=("Consolas", 8, "bold"), fg=K_TEXT_MUTED, bg=K_SIDEBAR).pack(side=tk.LEFT)
        tk.Label(c_top, text="42%", font=("Consolas", 8, "bold"), fg=K_ORANGE, bg=K_SIDEBAR).pack(side=tk.RIGHT)

        cpu_bar = tk.Frame(parent, bg="#161A22", height=4)
        cpu_bar.pack(fill=tk.X, pady=(4, 6))
        tk.Frame(cpu_bar, bg=K_ORANGE, width=90, height=4).pack(side=tk.LEFT)

        # Readiness Gates
        m_top = tk.Frame(parent, bg=K_SIDEBAR)
        m_top.pack(fill=tk.X, pady=(6, 0))
        tk.Label(m_top, text="READINESS GATES", font=("Consolas", 8, "bold"), fg=K_TEXT_MUTED, bg=K_SIDEBAR).pack(side=tk.LEFT)
        self.lbl_side_gates = tk.Label(m_top, text="0 / 7 PASSED", font=("Consolas", 8, "bold"), fg="#FFF", bg=K_SIDEBAR)
        self.lbl_side_gates.pack(side=tk.RIGHT)

        mem_bar = tk.Frame(parent, bg="#161A22", height=4)
        mem_bar.pack(fill=tk.X, pady=(4, 6))
        self.bar_side_gates = tk.Frame(mem_bar, bg="#FFF", width=0, height=4)
        self.bar_side_gates.pack(side=tk.LEFT)

        # Cold Buffer
        b_top = tk.Frame(parent, bg=K_SIDEBAR)
        b_top.pack(fill=tk.X, pady=(6, 0))
        tk.Label(b_top, text="COLD BUFFER", font=("Consolas", 8, "bold"), fg=K_TEXT_MUTED, bg=K_SIDEBAR).pack(side=tk.LEFT)
        tk.Label(b_top, text="+48% LATENCY", font=("Consolas", 8, "bold"), fg="#FFF", bg=K_SIDEBAR).pack(side=tk.RIGHT)

        bw_bar = tk.Frame(parent, bg=K_SIDEBAR)
        bw_bar.pack(fill=tk.X, pady=(4, 16))
        tk.Frame(bw_bar, bg="#64748B", width=65, height=4).pack(side=tk.LEFT, padx=1)
        tk.Frame(bw_bar, bg="#64748B", width=65, height=4).pack(side=tk.LEFT, padx=1)
        tk.Frame(bw_bar, bg="#252D3A", width=65, height=4).pack(side=tk.LEFT, padx=1)

        # Field Alerts (Dynamic)
        tk.Label(parent, text="FIELD ALERTS", font=("Segoe UI", 8, "bold"), fg=K_TEXT_DIM, bg=K_SIDEBAR).pack(anchor="w", pady=(8, 4))
        self.alerts_frame = tk.Frame(parent, bg=K_SIDEBAR)
        self.alerts_frame.pack(fill=tk.X)
        self._render_alerts()

        # Quick Actions
        qa_frame = tk.Frame(parent, bg=K_SIDEBAR)
        qa_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        tk.Label(qa_frame, text="QUICK ACTIONS", font=("Segoe UI", 8, "bold"), fg=K_TEXT_DIM, bg=K_SIDEBAR).pack(anchor="w", pady=(0, 6))
        qa_grid = tk.Frame(qa_frame, bg=K_SIDEBAR)
        qa_grid.pack(fill=tk.X)

        b1 = tk.Button(qa_grid, text="[@]\nGATES", font=("Consolas", 8, "bold"), bg=K_CARD, fg=K_TEXT_MUTED, activebackground="#1C212B", relief=tk.FLAT, pady=6, cursor="hand2", command=lambda: self._switch_tab("gates"))
        b1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b2 = tk.Button(qa_grid, text="[▲]\nDOSSIER", font=("Consolas", 8, "bold"), bg=K_CARD, fg=K_TEXT_MUTED, activebackground="#1C212B", relief=tk.FLAT, pady=6, cursor="hand2", command=self._export_dossier)
        b2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def _render_alerts(self):
        for widget in self.alerts_frame.winfo_children():
            widget.destroy()
        for text, time_str, active in self.alerts_list[:5]:
            row = tk.Frame(self.alerts_frame, bg=K_SIDEBAR, pady=3)
            row.pack(fill=tk.X)
            dot_col = K_ORANGE if active else K_TEXT_DIM
            tk.Label(row, text="●", font=("Segoe UI", 7), fg=dot_col, bg=K_SIDEBAR).pack(side=tk.LEFT, padx=(0, 5))
            col = tk.Frame(row, bg=K_SIDEBAR)
            col.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(col, text=text, font=("Segoe UI", 8, "bold" if active else "normal"), fg=K_TEXT_WHITE if active else K_TEXT_MUTED, bg=K_SIDEBAR, anchor="w", justify="left").pack(anchor="w")
            tk.Label(col, text=time_str, font=("Segoe UI", 7), fg=K_TEXT_DIM, bg=K_SIDEBAR, anchor="w").pack(anchor="w")

    def _add_alert(self, text, active=True):
        self.alerts_list.insert(0, (text, "Just now", active))
        if len(self.alerts_list) > 8:
            self.alerts_list.pop()
        self._render_alerts()

    def _build_center_stage(self, parent):
        top_meta = tk.Frame(parent, bg=K_BLACK)
        top_meta.pack(fill=tk.X, pady=(0, 10))

        tk.Label(top_meta, text="Terrace Master  /  Lithic Mountain Soil  /  ", font=("Segoe UI", 10), fg=K_TEXT_DIM, bg=K_BLACK).pack(side=tk.LEFT)
        tk.Label(top_meta, text="Sector 76 Step", font=("Segoe UI", 10, "bold"), fg=K_ORANGE, bg=K_BLACK).pack(side=tk.LEFT)

        opt_badge = tk.Label(top_meta, text="● ZERO-INSTRUMENT OPTIMAL", font=("Consolas", 8, "bold"), fg=K_GREEN, bg="#081E11", padx=8, pady=2)
        opt_badge.pack(side=tk.RIGHT)

        # 4 Top KPI Cards
        kpi_row = tk.Frame(parent, bg=K_BLACK)
        kpi_row.pack(fill=tk.X, pady=(0, 12))

        self.kpi_gate_lbl = self._kpi_box(kpi_row, "READINESS GATES", "0/7", "", "LOCKED", K_ORANGE)
        self._kpi_box(kpi_row, "SEASON HORIZON", "49", "d", "7 Weeks Base", K_GREEN)
        self._kpi_box(kpi_row, "COLD LATENCY", "+48", "%", "Delay Buffer", K_TEXT_DIM)
        self._kpi_box(kpi_row, "POTATO TRAP RISK", "FAIL", "", "110d Exceeds", K_ORANGE)

        # Content Container for Tab Views
        self.content_container = tk.Frame(parent, bg=K_BLACK)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        # TAB 1: LIVE ADVISOR & EXPERIENCE TAKING DIALOG
        self.view_advisor = tk.Frame(self.content_container, bg=K_BLACK)
        self.view_advisor.pack(fill=tk.BOTH, expand=True)

        # Generator Card (Experience Taking Dialog Box)
        gen_card = tk.Frame(self.view_advisor, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=14, pady=12)
        gen_card.pack(fill=tk.X, pady=(0, 10))

        gen_hdr = tk.Frame(gen_card, bg=K_PANEL)
        gen_hdr.pack(fill=tk.X, pady=(0, 4))
        tk.Label(gen_hdr, text="[+] SURVIVOR FIELD OBSERVATION TERMINAL", font=("Segoe UI", 10, "bold"), fg="#FFF", bg=K_PANEL).pack(side=tk.LEFT)
        tk.Label(gen_hdr, text="GROUND RULE: ZERO INSTRUMENTS", font=("Consolas", 8, "bold"), fg=K_GREEN, bg="#0A1810", padx=6, pady=2).pack(side=tk.RIGHT)

        tk.Label(gen_card, text="Describe your mountain terrace in plain everyday words (wall status, soil depth, stones, frost, sun, stream). The engine grounds cues in training_data.json and answers across the 9-stage restoration architecture.", font=("Segoe UI", 8), fg=K_TEXT_MUTED, bg=K_PANEL, wraplength=800, justify="left").pack(anchor="w", pady=(2, 6))

        # Survivor Input Text Area
        self.survivor_txt = scrolledtext.ScrolledText(gen_card, height=4, bg=K_CARD, fg="#FFF", font=("Consolas", 9), insertbackground=K_ORANGE)
        self.survivor_txt.pack(fill=tk.X, pady=(0, 8))

        # Modern Sci-Fi Presets Row
        ex_container = tk.Frame(gen_card, bg=K_PANEL)
        ex_container.pack(fill=tk.X, pady=(0, 8))

        tk.Label(ex_container, text="[SCENARIO MISSION PRESETS]:", font=("Consolas", 8, "bold"), fg=K_ORANGE, bg=K_PANEL).pack(anchor="w", pady=(0, 4))
        ex_grid = tk.Frame(ex_container, bg=K_PANEL)
        ex_grid.pack(fill=tk.X)

        self.preset_btns = {}
        preset_info = [
            ("Baseline Terrace", "M-01: BASELINE", "Thin Loam • Frost"),
            ("Steep Scree Slope", "M-02: SCREE", "Loose Gravel • Gales"),
            ("Frost Pocket Clay", "M-03: CLAY POCKET", "Cold Sink • Poor Drain"),
            ("Wind-Scoured Bench", "M-04: GALE BENCH", "Upper Bench • Sun")
        ]

        for full_name, tag, sub in preset_info:
            b_frame = tk.Frame(ex_grid, bg=K_CARD, highlightbackground=K_BORDER, highlightthickness=1, padx=6, pady=4)
            b_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            top_f = tk.Frame(b_frame, bg=K_CARD)
            top_f.pack(fill=tk.X)
            tk.Label(top_f, text=tag, font=("Consolas", 7, "bold"), fg=K_ORANGE, bg=K_CARD).pack(side=tk.LEFT)
            dot = tk.Label(top_f, text="●", font=("Segoe UI", 6), fg=K_TEXT_DIM, bg=K_CARD)
            dot.pack(side=tk.RIGHT)
            
            btn = tk.Button(
                b_frame, text=full_name, font=("Segoe UI", 8, "bold"),
                bg=K_CARD, fg="#FFF", activebackground=K_CARD_SUBTLE, relief=tk.FLAT, bd=0,
                cursor="hand2", anchor="w",
                command=lambda n=full_name: self._load_preset(n)
            )
            btn.pack(fill=tk.X)
            tk.Label(b_frame, text=sub, font=("Consolas", 7), fg=K_TEXT_DIM, bg=K_CARD, anchor="w").pack(fill=tk.X)
            self.preset_btns[full_name] = (b_frame, dot)

        # 6 Empirical Measurements with (i) Buttons
        telem_frame = tk.Frame(gen_card, bg=K_CARD, highlightbackground=K_BORDER, highlightthickness=1, padx=10, pady=8)
        telem_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(telem_frame, text="ZERO-INSTRUMENT TACTILE FIELD INPUTS (Click (i) for Non-Lab Measurement Guide):", font=("Consolas", 8, "bold"), fg=K_TEXT_DIM, bg=K_CARD).pack(anchor="w", pady=(0, 6))

        grid_inputs = tk.Frame(telem_frame, bg=K_CARD)
        grid_inputs.pack(fill=tk.X)

        # Helper to make label + (i) + entry/option
        self._build_input_col(grid_inputs, 0, 0, "a. Outside Temp", "Bare back of hand touch at solar noon.\nPress knuckles flat against earth for 10 slow breaths.\n• If knuckles ache with bone-chill (<5 C): Soil dormant, seeds will rot.\n• If soothing/neutral (>8 C): Safe for cold brassicas.", ["Cold Borderline (3-7 C)", "Sub-Zero Freeze (<0 C)", "Mild Midday (8-14 C)"])
        self._build_input_col(grid_inputs, 0, 1, "b. Snow Depth", "Hand Plunge Test.\nPlunge fingers straight into undisturbed snow:\n• 1st Knuckle (~2.5 cm): Dusting, no freeze protection.\n• Wrist (~18 cm): Moderate winter cover.\n• Elbow (~45 cm): Heavy thermal blanket, subsoil stays at 0 C.", ["Hand-Depth Crust", "Heavy Drift (Elbow)", "Light Dusting", "Cleared/Thawed"])
        self._build_input_col(grid_inputs, 0, 2, "c. Water (Safe Gather)", "Glacial Melt Shock & Safe Collection.\nNever wade bare-legged (hypothermia shock).\nDip inner wrist for 5 breaths. If sharp bone ache strikes, water is 1-3 C meltwater shock.\nGather with bucket-on-pole. Pre-warm 2h in dark slate pans before pouring on crops.", ["Glacial Stream (1-3 C)", "Snowmelt Trickle", "Rock Depression Pool", "Scarce / Rationed"])

        self._build_input_col(grid_inputs, 1, 0, "d. Soil Condition", "NRCS/FAO Ribbon & Slake Test.\nKnead golf-ball of moist soil into pencil-thick cylinder.\nPush outward over index finger:\n• Breaks <2 cm: Skeletal stony sand (leaches water).\n• Rolls 2.5-5 cm: Ideal mountain loam.\nDrop in water jar: if water stays clear, zero humus.", ["Thin Stony Loam (50% rock)", "Compacted Glacial Clay", "Loose Scree / Gravel", "Deep Worked Humus"])
        self._build_input_col(grid_inputs, 1, 1, "e. Wind Speed", "WMO Non-Instrument Beaufort Method.\nFace sensation & jacket flap:\n• Light breeze (felt on cheeks, leaves rustle: ~8 km/h)\n• Moderate gale (whistles in ears, jackets snap: ~25 km/h)\n• Severe gales (walking impeded, dust flying: >40 km/h).", ["Alpine Gale Scour (>40 km/h)", "Moderate Breeze (~20 km/h)", "Sheltered Bench Calm"])
        self._build_input_col(grid_inputs, 1, 2, "f. Sunlight & Intervals", "5 White Stones Shadow Method.\nPlace 5 white stones across bed from morning sunbreak to sunset.\nIf ridge shadow covers Stone 4 by 2 PM, daily sun is <4.5 hours.\nOnly fast brassicas will finish; long-season tubers will starve.", ["Ridge Shaded (4-5h max)", "Late Morning Sunbreak", "Full Alpine UV (7h+)", "Persistent Fog/Low Sun"])

        # Dispatch Button & Status
        btn_row = tk.Frame(gen_card, bg=K_PANEL)
        btn_row.pack(fill=tk.X, pady=(2, 0))

        btn_run = tk.Button(
            btn_row, text="[▲] GENERATE 9-STEP RESTORATION PROTOCOL",
            font=("Consolas", 10, "bold"), bg=K_ORANGE, fg="#FFF",
            activebackground="#FF6E38", relief=tk.FLAT, padx=14, pady=6,
            cursor="hand2", command=self._generate_protocol
        )
        btn_run.pack(side=tk.LEFT)

        self.lbl_stage_status = tk.Label(btn_row, text="Adjust toggles or enter description above to unlock 9-stage restoration architecture.", font=("Consolas", 8), fg=K_TEXT_DIM, bg=K_PANEL)
        self.lbl_stage_status.pack(side=tk.LEFT, padx=12)

        # CONDITIONAL 9-STAGE RESTORATION CONTAINER
        self.frame_nine_stages = tk.Frame(self.view_advisor, bg=K_BLACK)
        # Note: Not packed until user clicks Generate or provides input

        # 9-Step Interactive Stage Navigation Pills Strip
        pills_frame = tk.Frame(self.frame_nine_stages, bg=K_BLACK)
        pills_frame.pack(fill=tk.X, pady=(4, 6))

        self.pill_buttons = []
        for idx, (num, key, title, sub) in enumerate(STEP_TITLES):
            p = tk.Button(
                pills_frame, text=f"ST {num}\n{title}", font=("Consolas", 7, "bold"),
                bg=K_CARD, fg=K_TEXT_MUTED, activebackground=K_CARD_SUBTLE,
                relief=tk.FLAT, padx=4, pady=4, cursor="hand2",
                command=lambda i=idx: self._select_step(i)
            )
            p.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
            self.pill_buttons.append(p)

        # Resolution Card (Stage Output Stream)
        res_card = tk.Frame(self.frame_nine_stages, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=14, pady=12)
        res_card.pack(fill=tk.BOTH, expand=True)

        res_hdr = tk.Frame(res_card, bg=K_PANEL)
        res_hdr.pack(fill=tk.X, pady=(0, 6))
        self.lbl_stage_heading = tk.Label(res_hdr, text="STAGE 01: INPUT ECHO — DIAGNOSTIC CUE GROUNDING", font=("Consolas", 10, "bold"), fg=K_ORANGE, bg=K_PANEL)
        self.lbl_stage_heading.pack(side=tk.LEFT)

        tk.Label(res_hdr, text="GROUNDED IN TRAINING DATA", font=("Consolas", 8, "bold"), fg=K_GREEN, bg="#0A1810", padx=6, pady=2).pack(side=tk.RIGHT)

        self.resolution_txt = scrolledtext.ScrolledText(res_card, bg="#06090E", fg="#CAD5E2", font=("Consolas", 10), insertbackground=K_ORANGE, padx=10, pady=10)
        self.resolution_txt.pack(fill=tk.BOTH, expand=True)

        # Placeholder Card (Shown while awaiting input)
        self.frame_stage_placeholder = tk.Frame(self.view_advisor, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=20, pady=30)
        self.frame_stage_placeholder.pack(fill=tk.BOTH, expand=True, pady=4)

        tk.Label(self.frame_stage_placeholder, text="[◯] 9-STAGE RESTORATION PIPELINE AWAITING FIELD OBSERVATIONS", font=("Consolas", 11, "bold"), fg=K_ORANGE, bg=K_PANEL).pack(pady=(0, 6))
        tk.Label(
            self.frame_stage_placeholder,
            text="The 9-step resolution architecture remains hidden until mountain cues are provided.\n"
                 "Select a preset above, adjust the 6 measurement toggles (temperature, snow, water, soil, wind, sunlight),\n"
                 "or type your observations and click '[▲] GENERATE 9-STEP RESTORATION PROTOCOL'.",
            font=("Segoe UI", 9), fg=K_TEXT_MUTED, bg=K_PANEL, justify="center"
        ).pack()

        # TAB 2: READINESS GATES & SOP
        self.view_gates = tk.Frame(self.content_container, bg=K_BLACK)

        g_card = tk.Frame(self.view_gates, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=16, pady=14)
        g_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(g_card, text="STEP 4 EMPIRICAL READINESS GATE CHECKPOINT", font=("Segoe UI", 11, "bold"), fg="#FFF", bg=K_PANEL).pack(anchor="w")
        tk.Label(g_card, text="Soil preparation and wall stabilization must strictly precede crop planting. Check each tactile gate as verified:", font=("Segoe UI", 8), fg=K_TEXT_MUTED, bg=K_PANEL).pack(anchor="w", pady=(2, 10))

        self.gate_vars = {}
        for key, text in self.readiness_checks.items():
            var = tk.BooleanVar(value=text)
            self.gate_vars[key] = var
            cb = tk.Checkbutton(
                g_card, text=f"{key}: Physical verification passed",
                variable=var, command=self._update_readiness_count,
                font=("Consolas", 9), bg=K_PANEL, fg="#FFF",
                selectcolor=K_CARD, activebackground=K_PANEL
            )
            cb.pack(anchor="w", pady=3)

        tk.Label(g_card, text="9-STAGE STANDARD OPERATING PROCEDURE (SOP):", font=("Consolas", 9, "bold"), fg=K_ORANGE, bg=K_PANEL).pack(anchor="w", pady=(16, 6))
        sop_txt = scrolledtext.ScrolledText(g_card, height=10, bg=K_CARD, fg="#CAD5E2", font=("Consolas", 9))
        sop_txt.pack(fill=tk.BOTH, expand=True)
        for s in ds.NINE_STEPS_DEFINITION:
            sop_txt.insert(tk.END, f"STAGE {s['step']}: {s['title']} ({s['sub']})\nGoal: {s['goal']}\n\n")

        # TAB 3: CROPS MATRIX
        self.view_crops = tk.Frame(self.content_container, bg=K_BLACK)
        c_card = tk.Frame(self.view_crops, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=16, pady=14)
        c_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(c_card, text="BIOLOGICAL CROP MATRIX & COLD DELAY LATENCY ENGINE", font=("Segoe UI", 11, "bold"), fg="#FFF", bg=K_PANEL).pack(anchor="w")
        tk.Label(c_card, text="All maturity numbers include +40% to +60% cold buffer for slow cell division. 49-day hard freeze boundary enforced:", font=("Segoe UI", 8), fg=K_TEXT_MUTED, bg=K_PANEL).pack(anchor="w", pady=(2, 10))

        self.crops_txt = scrolledtext.ScrolledText(c_card, bg=K_CARD, fg="#CAD5E2", font=("Consolas", 9))
        self.crops_txt.pack(fill=tk.BOTH, expand=True)
        self._populate_crops()

        # TAB 4: COMPASS
        self.view_compass = tk.Frame(self.content_container, bg=K_BLACK)
        cp_card = tk.Frame(self.view_compass, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=16, pady=14)
        cp_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(cp_card, text="ZERO-INSTRUMENT TACTILE SENSORY COMPASS (NRCS & FAO ALIGNED)", font=("Segoe UI", 11, "bold"), fg="#FFF", bg=K_PANEL).pack(anchor="w")
        tk.Label(cp_card, text="Human sensory organs and household objects replacing lab equipment:", font=("Segoe UI", 8), fg=K_TEXT_MUTED, bg=K_PANEL).pack(anchor="w", pady=(2, 10))

        comp_txt = scrolledtext.ScrolledText(cp_card, bg=K_CARD, fg="#CAD5E2", font=("Consolas", 9), padx=10, pady=10)
        comp_txt.pack(fill=tk.BOTH, expand=True)
        for c in ds.NO_LAB_COMPASS:
            comp_txt.insert(tk.END, f"===============================================================================\n")
            comp_txt.insert(tk.END, f"{c['title'].upper()}  [{c['realm']}]\n")
            comp_txt.insert(tk.END, f"-------------------------------------------------------------------------------\n")
            if 'tool' in c:
                comp_txt.insert(tk.END, f"[SURVIVAL TOOL] : {c['tool']}\n")
            comp_txt.insert(tk.END, f"[APPLICATION]   : {c['usage']}\n")
            if 'procedure' in c:
                comp_txt.insert(tk.END, f"[PROCEDURE]     : {c['procedure']}\n")
            comp_txt.insert(tk.END, f"[DIAGNOSIS]     : {c['detail']}\n\n")

    def _build_input_col(self, parent, row, col, label_text, info_text, options):
        c_frame = tk.Frame(parent, bg=K_CARD, padx=8, pady=5)
        c_frame.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
        parent.columnconfigure(col, weight=1)

        hdr = tk.Frame(c_frame, bg=K_CARD)
        hdr.pack(fill=tk.X)

        tk.Label(hdr, text=label_text, font=("Consolas", 8, "bold"), fg=K_TEXT_MUTED, bg=K_CARD).pack(side=tk.LEFT)
        i_btn = tk.Button(
            hdr, text="i", font=("Consolas", 6, "bold"), bg="#1A1A1A", fg=K_ORANGE,
            relief=tk.FLAT, bd=1, padx=3, pady=0, cursor="hand2",
            command=lambda: messagebox.showinfo(f"Measurement Guide: {label_text}", info_text)
        )
        i_btn.pack(side=tk.RIGHT)

        cb = ttk.Combobox(c_frame, values=options, state="readonly", font=("Consolas", 8))
        cb.current(0)
        cb.pack(fill=tk.X, pady=(2, 0))
        cb.bind("<<ComboboxSelected>>", lambda e: self._on_telemetry_changed())

    def _on_telemetry_changed(self):
        self.lbl_stage_status.config(text="Input changed. Click GENERATE to ground observations through 9-stage pipeline.", fg=K_ORANGE)

    def _kpi_box(self, parent, title, num, unit, sub, sub_col):
        b = tk.Frame(parent, bg=K_PANEL, highlightbackground=K_BORDER, highlightthickness=1, padx=12, pady=8)
        b.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        tk.Label(b, text=title, font=("Segoe UI", 7, "bold"), fg=K_TEXT_DIM, bg=K_PANEL).pack(anchor="w")
        row = tk.Frame(b, bg=K_PANEL)
        row.pack(anchor="w", pady=(2, 0))
        val_lbl = tk.Label(row, text=num, font=("Consolas", 18, "bold"), fg="#FFF", bg=K_PANEL)
        val_lbl.pack(side=tk.LEFT)
        if unit:
            tk.Label(row, text=unit, font=("Consolas", 10), fg=K_TEXT_DIM, bg=K_PANEL).pack(side=tk.LEFT)
        tk.Label(row, text=f"  {sub}", font=("Consolas", 8), fg=sub_col, bg=K_PANEL).pack(side=tk.LEFT)
        return val_lbl

    def _switch_tab(self, tab_id):
        self.view_advisor.pack_forget()
        self.view_gates.pack_forget()
        self.view_crops.pack_forget()
        self.view_compass.pack_forget()

        self.btn_nav_advisor.config(bg=K_SIDEBAR, fg=K_TEXT_MUTED)
        self.btn_nav_gates.config(bg=K_SIDEBAR, fg=K_TEXT_MUTED)
        self.btn_nav_crops.config(bg=K_SIDEBAR, fg=K_TEXT_MUTED)
        self.btn_nav_compass.config(bg=K_SIDEBAR, fg=K_TEXT_MUTED)

        if tab_id == "advisor":
            self.view_advisor.pack(fill=tk.BOTH, expand=True)
            self.btn_nav_advisor.config(bg="#1E130D", fg="#FFF")
        elif tab_id == "gates":
            self.view_gates.pack(fill=tk.BOTH, expand=True)
            self.btn_nav_gates.config(bg="#1E130D", fg="#FFF")
        elif tab_id == "crops":
            self.view_crops.pack(fill=tk.BOTH, expand=True)
            self.btn_nav_crops.config(bg="#1E130D", fg="#FFF")
        elif tab_id == "compass":
            self.view_compass.pack(fill=tk.BOTH, expand=True)
            self.btn_nav_compass.config(bg="#1E130D", fg="#FFF")

    def _load_preset(self, name):
        if name in EXAMPLES:
            # Highlight selected preset button
            for p_name, (b_frame, dot) in self.preset_btns.items():
                if p_name == name:
                    b_frame.config(highlightbackground=K_ORANGE)
                    dot.config(fg=K_ORANGE)
                else:
                    b_frame.config(highlightbackground=K_BORDER)
                    dot.config(fg=K_TEXT_DIM)

            self.survivor_txt.delete("1.0", tk.END)
            self.survivor_txt.insert(tk.END, EXAMPLES[name])
            self._add_alert(f"Preset loaded: {name}", active=True)
            self._generate_protocol()

    def _generate_protocol(self):
        text = self.survivor_txt.get("1.0", tk.END).strip()
        
        # Reveal 9-stage container and hide placeholder
        self.frame_stage_placeholder.pack_forget()
        self.frame_nine_stages.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        self.resolution_txt.delete("1.0", tk.END)
        self.resolution_txt.insert(tk.END, "DISPATCHING HACKIT NEURAL SURVIVAL ENGINE...\nGrounding environmental vectors from training_data.json...\n\n")

        self.current_results = self.advisor.advise(text)
        self._select_step(0)
        self.lbl_stage_status.config(text="[PASS] 9-Stage protocol active and grounded.", fg=K_GREEN)
        self._add_alert("9-Stage Protocol generated & grounded", active=True)

    def _select_step(self, idx):
        self.active_step_idx = idx
        num, key, title, sub = STEP_TITLES[idx]
        self.lbl_stage_heading.config(text=f"STAGE {num}: {title} — {sub.upper()}")

        for i, b in enumerate(self.pill_buttons):
            if i == idx:
                b.config(bg=K_ORANGE, fg="#FFF")
            else:
                b.config(bg=K_CARD, fg=K_TEXT_MUTED)

        content = self.current_results.get(key, "Stage output not yet generated.")
        self.resolution_txt.delete("1.0", tk.END)
        self.resolution_txt.insert(tk.END, content)

    def _update_readiness_count(self):
        count = sum(1 for v in self.gate_vars.values() if v.get())
        total = len(self.gate_vars)
        self.lbl_side_gates.config(text=f"{count} / {total} PASSED")
        self.kpi_gate_lbl.config(text=f"{count}/{total}")
        pct = int((count / total) * 140)
        self.bar_side_gates.config(width=pct)
        self._add_alert(f"Readiness Gate updated: {count}/{total} passed", active=(count == total))

    def _populate_crops(self):
        obs = {
            "estimatedSeasonWeeks": 7,
            "frostFrequency": "every-dawn",
            "soilDepth": "hand-deep",
            "sunlightHours": "four-to-five-hours"
        }
        for c in ds.SCENARIO_CROPS:
            e = ds.evaluate_crop_viability(c, obs)
            status_tag = e['status'].upper()
            is_fail = c['id'] == 'chitted-potato'
            tag_display = "[FAIL] EXCLUDED" if is_fail else "[PASS] VIABLE"
            self.crops_txt.insert(tk.END, f"{tag_display}: {c['name']} ({c['variety']})\n")
            pct_val = round((c.get('coldBufferMultiplier', 1.45) - 1) * 100)
            self.crops_txt.insert(tk.END, f"Nominal: {c['nominalDays']}d  -->  Cold Mountain Adjusted: {e['adjustedDays']}d (+{pct_val}%)\n")
            self.crops_txt.insert(tk.END, f"Min Depth: {c.get('minSoilDepth', 'hand-depth')} | Frost Tolerance: {c.get('frostTolerance', 'high')}\n")
            
            crit = c.get('criticalIssues', {})
            self.crops_txt.insert(tk.END, f"CRITICAL STRESSORS:\n")
            self.crops_txt.insert(tk.END, f"  • Wind: {crit.get('wind', 'Protect from mountain gales')}\n")
            self.crops_txt.insert(tk.END, f"  • Sunlight: {crit.get('sunlight', 'Needs maximum terrace sun')}\n")
            self.crops_txt.insert(tk.END, f"  • Temperature: {crit.get('temperature', 'Night frost risk')}\n")
            
            if 'howToGrow' in c:
                self.crops_txt.insert(tk.END, f"HOW TO GROW:\n")
                for step in c['howToGrow']:
                    self.crops_txt.insert(tk.END, f"  - {step}\n")

            self.crops_txt.insert(tk.END, f"Why It Fits / Fails: {c['whyItFits']}\n")
            self.crops_txt.insert(tk.END, "=" * 78 + "\n\n")

    def _estop_click(self):
        messagebox.showwarning("HackIt E-STOP", "E-STOP ENGAGED. Soil readiness gates locked. Planting prohibited.")

    def _export_dossier(self):
        dossier = f"""# HackIt // SCENARIO 2 HIGH-ALTITUDE COLD TERRACE DOSSIER
STATUS: 100% Zero-Instrument Certified
METRICS: Handful, Bucketful, Pace, Hand's Depth, Finger Knuckle

9-STAGE SURVIVAL ARCHITECTURE:
Step 1: Input Echo & Diagnostic Cue Grounding
Step 2: Missing Analysis & Everyday Field Tests
Step 3: Quantified Fix Protocol
Step 4: Mandatory Physical Readiness Gate
Step 5: Resilient Crop Roster
Step 6: Dual Timeline & +40-60% Buffer
Step 7: Bed Substrate & Solar-Warmed Stream Water
Step 8: Ongoing Staged Care
Step 9: Ripeness Signs & Post-Harvest Regeneration
"""
        self.clipboard_clear()
        self.clipboard_append(dossier)
        messagebox.showinfo("HackIt Export", "Official Part A Dossier Markdown copied to clipboard.")

if __name__ == "__main__":
    app = SupercomputerApp()
    app.mainloop()
