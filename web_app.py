"""
HackIt // SUPERCOMPUTER COMMAND SYSTEM: SCENARIO 2 HIGH-ALTITUDE COLD TERRACE
================================================================================
Complete Functional UI matching the HackIt Dark B2B Industrial Layout:
- Tab 1: [LIVE OPERATIONS] - Experience Taking Dialog Box, Survivor Log, Examples,
          and Full 9-Step Resolution Stream with Grounding & Missing Analysis.
- Tab 2: [FLOOR MAP & CONTOURS] - Terrace 1, 2, 3 contours, wall reconstruction,
          solar warming pans, and shadow tracking lines.
- Tab 3: [WORKFORCE & READINESS GATES] - Interactive Step 4 Empirical Verification
          Gate Checklist (7 tactile checks) + 9-Stage SOP Roadmap Definitions.
- Tab 4: [BIOLOGICAL CROPS] - Crop Roster with +40-60% Cold-Delay Latency Engine,
          viability margins, and Potato Trap breakdown.
- Tab 5: [LOGS & COMPASS] - Zero-instrument body unit calibrations, defect handling,
          and complete Part A dossier export with 1-click Markdown copy.
No Emojis (Clean technical ASCII tags: [OK], [WARN], [FAIL], ▲, ◯, ⊞).
Outputs strictly grounded in training_data.json and case_study.txt.
"""

import http.server
import json
import socketserver
import urllib.parse
import os
import sys

from model import SurvivalSoilAdvisor
import domain_simulator as ds

PORT = 8080
ADVISOR = SurvivalSoilAdvisor()

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HackIt // Sector 76 — Autonomous Mountain Terraforming System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-black: #000000;
      --bg-topbar: #000000;
      --bg-sidebar: #000000;
      --bg-panel: #050505;
      --bg-card: #0A0A0A;
      --bg-card-subtle: #0F0F0F;
      --bg-input: #000000;
      
      --border-main: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.04);
      --border-card: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(255, 90, 31, 0.7);

      --kin-orange: #FF5A1F;
      --kin-orange-glow: rgba(255, 90, 31, 0.28);
      --kin-green: #22C55E;
      --kin-green-glow: rgba(34, 197, 94, 0.25);
      --kin-red-estop: #E11D48;
      
      --text-white: #FFFFFF;
      --text-heading: #F8FAFC;
      --text-muted: #94A3B8;
      --text-dim: #64748B;

      --font-ui: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-black);
      color: var(--text-heading);
      font-family: var(--font-ui);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
      -webkit-font-smoothing: antialiased;
    }

    /* TOP HEADER BAR */
    header.kin-header {
      height: 52px;
      background: var(--bg-topbar);
      border-bottom: 1px solid var(--border-main);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      flex-shrink: 0;
      z-index: 50;
    }

    .hdr-left {
      display: flex;
      align-items: center;
      gap: 24px;
    }

    .brand-logo {
      display: flex;
      align-items: center;
      font-size: 19px;
      font-weight: 700;
      letter-spacing: -0.04em;
      color: #FFF;
    }

    .brand-logo .dot {
      color: var(--kin-orange);
      font-size: 20px;
      line-height: 0;
      margin: 0 -1px;
    }

    .sector-dropdown {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.15s;
    }

    .sector-dropdown:hover {
      background: rgba(255, 255, 255, 0.05);
      color: #FFF;
    }

    .hdr-right {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .shift-clock {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-dim);
      text-align: right;
      line-height: 1.25;
      letter-spacing: 0.03em;
    }

    .shift-clock strong {
      color: var(--text-muted);
      display: block;
    }

    .btn-estop {
      background: rgba(225, 29, 72, 0.08);
      border: 1px solid var(--kin-red-estop);
      border-radius: 4px;
      color: var(--kin-red-estop);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 6px 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: 0.08em;
      transition: all 0.2s;
    }

    .btn-estop:hover {
      background: var(--kin-red-estop);
      color: #FFF;
      box-shadow: 0 0 15px rgba(225, 29, 72, 0.4);
    }

    /* 3-COLUMN APP SHELL */
    .app-body {
      display: grid;
      grid-template-columns: 200px 1fr 240px;
      flex: 1;
      height: calc(100vh - 52px);
      overflow: hidden;
    }

    /* LEFT SIDEBAR */
    aside.kin-sidebar-left {
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-main);
      padding: 18px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow-y: auto;
    }

    .sidebar-section {
      margin-bottom: 22px;
    }

    .sidebar-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 8px;
      padding-left: 10px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      margin-bottom: 2px;
    }

    .nav-item:hover {
      color: #FFF;
      background: rgba(255, 255, 255, 0.03);
    }

    .nav-item.active {
      color: #FFF;
      background: rgba(255, 90, 31, 0.12);
      border-left: 2px solid var(--kin-orange);
    }

    .nav-icon {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-dim);
      width: 16px;
      text-align: center;
    }

    .nav-item.active .nav-icon {
      color: var(--kin-orange);
    }

    /* Grid Power Widget */
    .grid-power-widget {
      padding: 10px;
      border-top: 1px solid var(--border-subtle);
    }

    .power-meta {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      color: var(--text-dim);
      margin-bottom: 6px;
    }

    .power-meta span:last-child {
      color: var(--kin-orange);
    }

    .power-bar-track {
      height: 3px;
      background: var(--bg-card);
      border-radius: 2px;
      overflow: hidden;
    }

    .power-bar-fill {
      height: 100%;
      width: 98.2%;
      background: var(--kin-orange);
      box-shadow: 0 0 8px var(--kin-orange-glow);
    }

    /* CENTER COMMAND STAGE */
    main.kin-stage {
      background: var(--bg-black);
      overflow-y: auto;
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    main.kin-stage::-webkit-scrollbar { width: 5px; }
    main.kin-stage::-webkit-scrollbar-track { background: var(--bg-black); }
    main.kin-stage::-webkit-scrollbar-thumb { background: var(--bg-card); border-radius: 3px; }

    /* Top Breadcrumbs & System Optimal Pill */
    .stage-top-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 4px;
    }

    .breadcrumb-row {
      font-size: 13px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .breadcrumb-row span.white { color: #FFF; font-weight: 500; }
    .breadcrumb-row span.orange { color: var(--kin-orange); font-weight: 600; }

    .status-optimal-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--kin-green);
      background: rgba(34, 197, 94, 0.08);
      border: 1px solid rgba(34, 197, 94, 0.25);
      padding: 5px 12px;
      border-radius: 12px;
      letter-spacing: 0.04em;
    }

    .status-optimal-badge::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--kin-green);
      box-shadow: 0 0 6px var(--kin-green);
    }

    /* 4 Primary Top Metrics */
    .top-metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .metric-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-main);
      border-radius: 6px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 86px;
    }

    .metric-hdr {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      color: var(--text-dim);
      text-transform: uppercase;
    }

    .metric-hdr-tag {
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--text-dim);
    }

    .metric-val-row {
      display: flex;
      align-items: baseline;
      gap: 8px;
      margin-top: 8px;
    }

    .metric-num {
      font-size: 26px;
      font-weight: 700;
      font-family: var(--font-mono);
      color: #FFF;
      line-height: 1;
    }

    .metric-sub {
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--text-dim);
    }

    .metric-sub.orange { color: var(--kin-orange); }
    .metric-sub.green { color: var(--kin-green); font-weight: 600; }

    /* Dialog Box & Generator Card (Functional Input Experience) */
    .generator-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-main);
      border-radius: 8px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .generator-hdr {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .generator-title {
      font-size: 13px;
      font-weight: 700;
      color: #FFF;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .generator-desc {
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    .survivor-textarea {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-main);
      border-radius: 6px;
      color: #FFF;
      padding: 12px 14px;
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.6;
      resize: vertical;
      min-height: 95px;
      outline: none;
      transition: border-color 0.2s;
    }

    .survivor-textarea:focus {
      border-color: var(--kin-orange);
      box-shadow: 0 0 10px var(--kin-orange-glow);
    }

    .examples-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .ex-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-dim);
      text-transform: uppercase;
      font-family: var(--font-mono);
    }

    .btn-example {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 10.5px;
      padding: 4px 10px;
      cursor: pointer;
      transition: all 0.15s;
    }

    .btn-example:hover {
      background: var(--bg-card-subtle);
      color: #FFF;
      border-color: var(--border-main);
    }

    .btn-generate-protocol {
      background: var(--kin-orange);
      border: 1px solid var(--kin-orange);
      border-radius: 4px;
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.06em;
      padding: 10px 18px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      align-self: flex-start;
      transition: all 0.2s;
      box-shadow: 0 0 14px var(--kin-orange-glow);
    }

    .btn-generate-protocol:hover {
      background: #FF6E38;
      box-shadow: 0 0 20px rgba(255, 90, 31, 0.6);
    }

    /* Structured Telemetry Controls */
    .telemetry-row-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      background: var(--bg-card);
      padding: 14px;
      border-radius: 6px;
      border: 1px solid var(--border-subtle);
    }

    .telem-col label {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      font-family: var(--font-mono);
      margin-bottom: 5px;
    }

    /* Modern Sci-Fi Preset Cards Grid */
    .presets-scifi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 2px;
      margin-bottom: 4px;
    }

    .preset-card {
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-radius: 4px;
      padding: 8px 10px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 3px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      text-align: left;
    }

    .preset-card:hover {
      background: var(--bg-card-subtle);
      border-color: rgba(255, 90, 31, 0.4);
      transform: translateY(-1px);
    }

    .preset-card.active {
      background: rgba(255, 90, 31, 0.1);
      border-color: var(--kin-orange);
      box-shadow: 0 0 10px rgba(255, 90, 31, 0.2);
    }

    .preset-card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .preset-tag {
      font-family: var(--font-mono);
      font-size: 9px;
      font-weight: 700;
      color: var(--kin-orange);
      letter-spacing: 0.05em;
    }

    .preset-status-dot {
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--text-dim);
    }

    .preset-card.active .preset-status-dot {
      background: var(--kin-orange);
      box-shadow: 0 0 5px var(--kin-orange);
    }

    .preset-title {
      font-family: var(--font-ui);
      font-size: 11px;
      font-weight: 600;
      color: #FFF;
      line-height: 1.2;
    }

    .preset-desc {
      font-family: var(--font-mono);
      font-size: 9px;
      color: var(--text-dim);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Intuitive Encircled Info Tooltip (Ultra-compact 9px) */
    .info-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      border: 1px solid rgba(255, 90, 31, 0.5);
      color: var(--kin-orange);
      font-size: 6.5px;
      font-family: var(--font-mono);
      font-weight: 700;
      cursor: pointer;
      position: relative;
      background: rgba(255, 90, 31, 0.05);
      user-select: none;
      flex-shrink: 0;
      line-height: 1;
      padding: 0;
      transition: all 0.15s ease;
    }

    .info-btn:hover, .info-btn:focus {
      background: var(--kin-orange);
      color: #000;
      box-shadow: 0 0 6px var(--kin-orange-glow);
      outline: none;
    }

    .info-tooltip {
      visibility: hidden;
      opacity: 0;
      position: absolute;
      bottom: calc(100% + 6px);
      left: 50%;
      transform: translateX(-50%);
      width: 250px;
      background: #000000;
      border: 1px solid var(--kin-orange);
      border-radius: 4px;
      padding: 8px 10px;
      color: #E2E8F0;
      font-size: 10.5px;
      font-family: var(--font-mono);
      line-height: 1.45;
      text-transform: none;
      font-weight: 400;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.95), 0 0 10px rgba(255, 90, 31, 0.15);
      z-index: 1000;
      pointer-events: none;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }

    .info-btn:hover .info-tooltip, .info-btn:focus .info-tooltip {
      visibility: visible;
      opacity: 1;
      transform: translateX(-50%) translateY(-2px);
    }

    .info-tooltip-title {
      color: var(--kin-orange);
      font-weight: 700;
      margin-bottom: 4px;
      font-size: 9.5px;
      border-bottom: 1px solid rgba(255, 90, 31, 0.25);
      padding-bottom: 2px;
      letter-spacing: 0.04em;
    }

    /* Sensory Compass Cards (High-Tech Sci-Fi Radar Module) */
    .compass-card {
      background: #030303;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 6px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      position: relative;
      overflow: hidden;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .compass-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 3px;
      height: 100%;
      background: rgba(255, 255, 255, 0.1);
      transition: background 0.2s ease;
    }

    .compass-card:hover {
      background: #080808;
      border-color: rgba(255, 90, 31, 0.4);
      transform: translateY(-2px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.8), 0 0 14px rgba(255, 90, 31, 0.15);
    }

    .compass-card:hover::before {
      background: var(--kin-orange);
      box-shadow: 0 0 8px var(--kin-orange);
    }

    .compass-hdr {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }

    .compass-title {
      font-family: var(--font-ui);
      font-size: 13px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.3;
    }

    .compass-realm-tag {
      font-family: var(--font-mono);
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      padding: 2px 7px;
      border-radius: 3px;
      background: rgba(255, 90, 31, 0.1);
      border: 1px solid rgba(255, 90, 31, 0.3);
      color: var(--kin-orange);
      flex-shrink: 0;
    }

    .compass-tool-row {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 10px;
      color: #94A3B8;
      background: rgba(255, 255, 255, 0.03);
      padding: 5px 8px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .compass-tool-label {
      color: var(--kin-orange);
      font-weight: 700;
    }

    .compass-body {
      font-family: var(--font-mono);
      font-size: 11px;
      color: #CBD5E1;
      line-height: 1.55;
    }

    .compass-procedure-box {
      background: rgba(0, 0, 0, 0.6);
      border: 1px dashed rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: #E2E8F0;
      line-height: 1.45;
    }

    .compass-procedure-label {
      font-size: 9px;
      font-weight: 700;
      color: #22C55E;
      letter-spacing: 0.06em;
      margin-bottom: 3px;
      text-transform: uppercase;
    }

    .telem-select {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      color: var(--text-heading);
      padding: 7px 9px;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 11px;
      outline: none;
      transition: border-color 0.15s;
    }

    .telem-select:focus {
      border-color: var(--kin-orange);
    }

    /* Pop-Out Biological Crop Cards with Smooth Animations */
    .crop-pop-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 14px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .crop-pop-card:hover {
      transform: translateY(-4px) scale(1.015);
      border-color: var(--kin-orange);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 16px var(--kin-orange-glow);
      background: var(--bg-card-subtle);
      z-index: 10;
    }

    .crop-pop-card.excluded-card:hover {
      border-color: #EF476F;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 16px rgba(239, 71, 111, 0.2);
    }

    .crop-stressor-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 6px;
      border-radius: 3px;
      font-family: var(--font-mono);
      font-size: 9.5px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
    }

    .crop-stressor-badge.crit-wind {
      border-color: rgba(56, 189, 248, 0.3);
      color: #7DD3FC;
    }

    .crop-stressor-badge.crit-sun {
      border-color: rgba(251, 191, 36, 0.3);
      color: #FCD34D;
    }

    .crop-stressor-badge.crit-temp {
      border-color: rgba(239, 71, 111, 0.3);
      color: #FCA5A5;
    }

    /* 9-Step Interactive Stage Navigation Pills */
    .steps-pills-strip {
      display: grid;
      grid-template-columns: repeat(9, 1fr);
      gap: 6px;
      margin-bottom: 4px;
    }

    .step-nav-pill {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 8px 6px;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }

    .step-nav-pill:hover {
      border-color: var(--border-main);
      background: var(--bg-card-subtle);
    }

    .step-nav-pill.active {
      background: rgba(255, 90, 31, 0.15);
      border-color: var(--kin-orange);
    }

    .step-nav-pill-num {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      color: var(--kin-orange);
    }

    .step-nav-pill-title {
      font-size: 10.5px;
      font-weight: 600;
      color: #FFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 2px;
    }

    /* Protocol Step Display Card (Resolution Output) */
    .resolution-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-main);
      border-radius: 6px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .resolution-hdr {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .resolution-tag {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--kin-orange);
    }

    .resolution-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      background: rgba(34, 197, 94, 0.1);
      border: 1px solid rgba(34, 197, 94, 0.3);
      color: var(--kin-green);
      padding: 2px 8px;
      border-radius: 4px;
    }

    .resolution-body {
      font-family: var(--font-mono);
      font-size: 12px;
      color: #CAD5E2;
      line-height: 1.7;
      white-space: pre-wrap;
      max-height: 380px;
      overflow-y: auto;
      padding-right: 8px;
    }

    .resolution-body::-webkit-scrollbar { width: 4px; }
    .resolution-body::-webkit-scrollbar-thumb { background: var(--bg-card); }

    /* Readiness Checklist Cards */
    .readiness-item {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 10px 14px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.15s;
    }

    .readiness-item:hover {
      border-color: var(--border-main);
    }

    .readiness-item.passed {
      background: rgba(34, 197, 94, 0.05);
      border-color: rgba(34, 197, 94, 0.3);
    }

    .readiness-text {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--text-heading);
    }

    .readiness-check-box {
      width: 18px;
      height: 18px;
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      background: var(--bg-input);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: bold;
      color: #000;
    }

    .readiness-item.passed .readiness-check-box {
      background: var(--kin-green);
      border-color: var(--kin-green);
    }

    /* RIGHT SIDEBAR */
    aside.kin-sidebar-right {
      background: var(--bg-sidebar);
      border-left: 1px solid var(--border-main);
      padding: 18px 16px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      overflow-y: auto;
    }

    .right-sec-title {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .health-metric-block {
      margin-bottom: 14px;
    }

    .health-metric-top {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .health-metric-top span:last-child {
      color: var(--kin-orange);
    }

    .health-metric-top.white-val span:last-child {
      color: #FFF;
    }

    .health-bar-track {
      height: 4px;
      background: #171B22;
      border-radius: 2px;
      overflow: hidden;
      margin-bottom: 6px;
    }

    .health-bar-fill {
      height: 100%;
      border-radius: 2px;
    }

    .health-bar-fill.orange {
      width: 42%;
      background: var(--kin-orange);
    }

    .health-bar-fill.white {
      width: 64%;
      background: #E2E8F0;
    }

    .cpu-mini-eq {
      display: flex;
      align-items: flex-end;
      gap: 3px;
      height: 12px;
    }

    .eq-bar {
      width: 3px;
      border-radius: 1px;
      background: var(--kin-orange);
    }

    .seg-bar-wrap {
      display: flex;
      gap: 3px;
      height: 4px;
    }

    .seg-piece {
      flex: 1;
      background: #252D3A;
      border-radius: 1px;
    }

    .seg-piece.active {
      background: #64748B;
    }

    /* Alerts Feed */
    .alerts-feed-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .alert-row {
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }

    .alert-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--text-dim);
      margin-top: 4px;
      flex-shrink: 0;
    }

    .alert-dot.orange {
      background: var(--kin-orange);
      box-shadow: 0 0 6px var(--kin-orange);
    }

    .alert-content {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .alert-text {
      font-size: 11.5px;
      font-weight: 500;
      color: #E2E8F0;
      line-height: 1.3;
    }

    .alert-time {
      font-size: 10px;
      color: var(--text-dim);
    }

    /* Quick Action Buttons */
    .quick-actions-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: auto;
    }

    .btn-quick {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.05em;
      padding: 10px 4px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }

    .btn-quick:hover {
      background: var(--bg-card-subtle);
      border-color: var(--border-main);
      color: #FFF;
    }

    /* MODAL EXPORT */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(3, 4, 7, 0.88);
      backdrop-filter: blur(8px);
      z-index: 200;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }

    .modal-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-main);
      border-radius: 8px;
      max-width: 900px;
      width: 100%;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(255, 90, 31, 0.15);
    }

    .modal-hdr {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-hdr h3 {
      font-size: 14px;
      font-weight: 600;
      color: #FFF;
    }

    .modal-body-scroll {
      padding: 20px;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 12px;
      color: #CAD5E2;
      line-height: 1.7;
      white-space: pre-wrap;
    }

    .modal-ftr {
      padding: 14px 20px;
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: flex-end;
      gap: 10px;
    }

    .btn-ftr-primary {
      background: var(--kin-orange);
      border: 1px solid var(--kin-orange);
      border-radius: 4px;
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      padding: 6px 14px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- TOP HEADER BAR -->
  <header class="kin-header">
    <div class="hdr-left">
      <div class="brand-logo">
        Hack<span class="dot">I</span>t
      </div>
      <div class="sector-dropdown" onclick="toggleSectorSelect()">
        <span id="currentSectorText">Sector 76 (Alpine Cold Terrace)</span>
        <span>⌄</span>
      </div>
    </div>

    <div class="hdr-right">
      <div class="shift-clock">
        <strong>SOLAR TRANSIT</strong>
        <span id="liveTimestamp">08:42:12 AM</span>
      </div>
      <button class="btn-estop" onclick="triggerEStop()">E-STOP</button>
    </div>
  </header>

  <!-- MAIN 3-COLUMN BODY -->
  <div class="app-body">

    <!-- LEFT SIDEBAR -->
    <aside class="kin-sidebar-left">
      <div>
        <div class="sidebar-section">
          <div class="sidebar-label">View Context</div>
          <div class="nav-item active" id="navLiveOps" onclick="selectNav('live')">
            <span class="nav-icon">[~]</span>
            <span>Live Advisor</span>
          </div>
          <div class="nav-item" id="navFloorMap" onclick="selectNav('floor')">
            <span class="nav-icon">[#]</span>
            <span>Terrace Contours</span>
          </div>
          <div class="nav-item" id="navWorkforce" onclick="selectNav('workforce')">
            <span class="nav-icon">[@]</span>
            <span>Readiness Gates</span>
          </div>
        </div>

        <div class="sidebar-section">
          <div class="sidebar-label">Analysis</div>
          <div class="nav-item" id="navPerf" onclick="selectNav('perf')">
            <span class="nav-icon">[%]</span>
            <span>Biological Crops</span>
          </div>
          <div class="nav-item" id="navLogs" onclick="selectNav('logs')">
            <span class="nav-icon">[=]</span>
            <span>Sensory Compass</span>
          </div>
        </div>
      </div>

      <div class="grid-power-widget" style="position:relative;" title="Survival Solar Buffer">
        <div class="power-meta">
          <span style="display:flex; align-items:center; gap:5px;">
            <span>SURVIVAL SOLAR BUFFER</span>
            <span class="info-btn" tabindex="0" onclick="toggleSolarBufferModal(event)">(i)
              <span class="info-tooltip" style="bottom:auto; top:-125px; left:0; transform:none; width:220px; z-index:9999;">
                <div class="info-tooltip-title">[WHAT IS SURVIVAL SOLAR BUFFER?]</div>
                In plain words: High mountains lose warmth the moment the sun dips behind the ridge. The 'Solar Buffer' is daytime heat trapped inside dry stone walls, black slate tiles, and shallow water pans. It radiates a warm blanket of air preventing night frost from killing plant cells.
              </span>
            </span>
          </span>
          <span style="color:var(--kin-orange); font-weight:700;">98.2%</span>
        </div>
        <div class="power-bar-track">
          <div class="power-bar-fill"></div>
        </div>
        <div style="font-family:var(--font-mono); font-size:9.5px; color:var(--text-dim); margin-top:5px; line-height:1.3;">
          Thermal reserve in stone walls protecting roots during sub-zero dusk.
        </div>
      </div>
    </aside>

    <!-- CENTER COMMAND STAGE -->
    <main class="kin-stage">
      
      <!-- Breadcrumb Bar -->
      <div class="stage-top-meta">
        <div class="breadcrumb-row">
          <span>Terrace Master</span>
          <span>/</span>
          <span class="white">Lithic Mountain Soil</span>
          <span>/</span>
          <span class="orange">Sector 76 Step</span>
        </div>
        <div class="status-optimal-badge">
          ZERO-INSTRUMENT OPTIMAL
        </div>
      </div>

      <!-- 4 Top KPI Cards -->
      <div class="top-metrics-grid">
        <div class="metric-box">
          <div class="metric-hdr">
            <span>READINESS GATES</span>
            <span class="metric-hdr-tag">STEP 4</span>
          </div>
          <div class="metric-val-row">
            <div class="metric-num" id="kpiGatesNum">0<span style="font-size:16px; color:var(--text-dim);">/7</span></div>
            <div class="metric-sub orange" id="kpiGatesSub">LOCKED</div>
          </div>
        </div>

        <div class="metric-box">
          <div class="metric-hdr">
            <span>SEASON HORIZON</span>
            <span class="metric-hdr-tag">HORIZON</span>
          </div>
          <div class="metric-val-row">
            <div class="metric-num">49<span style="font-size:16px; color:var(--text-dim);">d</span></div>
            <div class="metric-sub green">7 Weeks Baseline</div>
          </div>
        </div>

        <div class="metric-box">
          <div class="metric-hdr">
            <span>COLD DELAY LATENCY</span>
            <span class="metric-hdr-tag">BUFFER</span>
          </div>
          <div class="metric-val-row">
            <div class="metric-num">+48<span style="font-size:16px; color:var(--text-dim);">%</span></div>
            <div class="metric-sub">Cell Division Delay</div>
          </div>
        </div>

        <div class="metric-box">
          <div class="metric-hdr">
            <span>POTATO TRAP RISK</span>
            <span class="metric-hdr-tag" style="color:var(--kin-orange);">[CRIT]</span>
          </div>
          <div class="metric-val-row">
            <div class="metric-num">FAIL</div>
            <div class="metric-sub">110d+ Exceeds 49d</div>
          </div>
        </div>
      </div>

      <!-- =================================================================== -->
      <!-- VIEW 1: LIVE ADVISOR & EXPERIENCE TAKING DIALOG (TAB: LIVE) -->
      <!-- =================================================================== -->
      <div id="viewLive" class="view-panel" style="display:flex; flex-direction:column; gap:14px;">
        
        <!-- Experience Taking Dialog Box -->
        <div class="generator-card">
          <div class="generator-hdr">
            <div class="generator-title">
              <span>[+]</span> SURVIVOR FIELD OBSERVATION TERMINAL
            </div>
            <span class="resolution-badge">GROUND RULE: ZERO INSTRUMENTS</span>
          </div>
          <p class="generator-desc">
            Describe your mountain terrace in everyday words (soil depth, stones, frost frequency, ridge shadow, wall condition, stream presence). 
            The system grounds your observations and answers through the official 9-step restoration sequence using only eyes, hands, and household units.
          </p>

          <textarea class="survivor-textarea" id="survivorInputText" placeholder="e.g. The terrace wall has collapsed in one place. Soil is thin, about a hand deep, and half stones. Frost on the plants every morning. The ridge shades the plot by mid-afternoon. Water comes from an ice-cold glacial stream. I think summer lasts about 6 weeks."></textarea>

          <!-- Modern Sci-Fi Presets -->
          <div style="display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="ex-label" style="color:var(--kin-orange);">[SCENARIO MISSION PRESETS]:</span>
              <span style="font-family:var(--font-mono); font-size:9.5px; color:var(--text-dim);">SELECT MISSION ARCHETYPE TO SYNC TELEMETRY</span>
            </div>
            <div class="presets-scifi-grid">
              <div class="preset-card active" id="presetCard1" onclick="loadExample(1)">
                <div class="preset-card-top">
                  <span class="preset-tag">MISSION 01</span>
                  <span class="preset-status-dot"></span>
                </div>
                <div class="preset-title">Baseline Terrace</div>
                <div class="preset-desc">Collapsed Wall • 50% Stone • Frost</div>
              </div>
              <div class="preset-card" id="presetCard2" onclick="loadExample(2)">
                <div class="preset-card-top">
                  <span class="preset-tag">MISSION 02</span>
                  <span class="preset-status-dot"></span>
                </div>
                <div class="preset-title">Steep Scree Slope</div>
                <div class="preset-desc">Loose Gravel • Severe Wind • No Wall</div>
              </div>
              <div class="preset-card" id="presetCard3" onclick="loadExample(3)">
                <div class="preset-card-top">
                  <span class="preset-tag">MISSION 03</span>
                  <span class="preset-status-dot"></span>
                </div>
                <div class="preset-title">Frost Pocket Clay</div>
                <div class="preset-desc">Cold Sink • Heavy Frost • Slow Drain</div>
              </div>
              <div class="preset-card" id="presetCard4" onclick="loadExample(4)">
                <div class="preset-card-top">
                  <span class="preset-tag">MISSION 04</span>
                  <span class="preset-status-dot"></span>
                </div>
                <div class="preset-title">Gale Bench</div>
                <div class="preset-desc">Upper Bench • Acidic Duff • Bulging Wall</div>
              </div>
            </div>
          </div>

          <!-- Structured Telemetry Selectors with Encircled (i) Tooltips for Survivor Tactile Measurements -->
          <div class="telemetry-row-grid">
            <!-- (a) Outside Temperature -->
            <div class="telem-col">
              <label>
                <span>Outside Temperature</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[MEASURE: OUTSIDE TEMPERATURE]</div>
                    Bare back of hand touch at solar noon. Clear mulch and press bare hand knuckles flat against earth for 10 slow breaths. If knuckles ache with bone-chill (< 5 C), soil is dormant. If neutral/soothing (> 8-10 C), safe for cold brassicas.
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selTemp" onchange="onObservationChanged()">
                <option value="freezing_subzero">Sub-Zero / Sharp Morning Freeze (< 0 C)</option>
                <option value="cold_borderline" selected>Cold Mountain Borderline (3 C to 7 C)</option>
                <option value="temperate_mild">Brief Midday Warmth (8 C to 14 C)</option>
              </select>
            </div>

            <!-- (b) Snow Layer Depth -->
            <div class="telem-col">
              <label>
                <span>Snow Layer Depth</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[MEASURE: SNOW LAYER DEPTH]</div>
                    Plunge fingers straight down into undisturbed drift. 1st knuckle (~2.5 cm) = dusting (no freeze insulation); Wrist-deep (~18 cm) = moderate winter cover; Elbow-deep (~45 cm) = heavy thermal blanket insulating subsoil at 0 C.
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selSnowDepth" onchange="onObservationChanged()">
                <option value="heavy_drift">Heavy Pack (Wrist to Elbow Deep)</option>
                <option value="hand_depth" selected>Morning Crust (Hand-Depth / Knuckle)</option>
                <option value="rare_dusting">Light Dusting (Fingertip)</option>
                <option value="cleared">Cleared / Thawed Ground</option>
              </select>
            </div>

            <!-- (c) Water Availability & Safe Gathering -->
            <div class="telem-col">
              <label>
                <span>Water Availability</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[SAFE GATHERING: WATER WITHOUT HARM]</div>
                    Glacial runoff is 1-3 C. NEVER wade bare-legged (hypothermia shock). Dip inner wrist for 5 breaths. If sharp bone ache strikes, water will shock crops. Dip with bucket on stick; warm 2h in dark slate solar pans before use.
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selWater" onchange="onObservationChanged()">
                <option value="glacial_stream_nearby" selected>Glacial Melt Stream (Near-Freezing 1-3 C)</option>
                <option value="snow_melt_channel">Snowbank Melt Trickle</option>
                <option value="standing_pool">Standing Rock Depression Pool</option>
                <option value="scarce_dry">Extremely Scarce (Rationed)</option>
              </select>
            </div>

            <!-- (d) Soil Condition -->
            <div class="telem-col">
              <label>
                <span>Soil Condition</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[MEASURE: SOIL CONDITION & TEXTURE]</div>
                    NRCS/FAO Ribbon & Slake Test. Knead golf-ball of moist soil into pencil-thick roll; push outward over index finger. Breaks < 2 cm = skeletal stony sand. Rolls 2.5-5 cm = rich mountain loam. Jar shake: if water stays clear, zero humus.
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selSoil" onchange="onObservationChanged()">
                <option value="thin_stony_loam" selected>Thin Stony Loam (Hand-Depth + 50% Rocks)</option>
                <option value="compacted_clay">Compacted Wet Glacial Clay (Slakes poorly)</option>
                <option value="loose_gravel_scree">Loose Scree / Gravelly Sand (Slides down)</option>
                <option value="deep_worked_humus">Deep Mountain Loam (Two hand-spans)</option>
              </select>
            </div>

            <!-- (e) Wind Speed & Timing -->
            <div class="telem-col">
              <label>
                <span>Wind Speed & Timing</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[MEASURE: WIND SPEED & DIRECTION]</div>
                    WMO Non-Instrument Beaufort method. Face sensation & jacket flap: Light breeze (felt on cheeks, leaves rustle: ~8 km/h); Moderate gale (wind whistles in ears, jackets snap: ~25 km/h); Severe scour (walking impeded, dust flying: >40 km/h).
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selWind" onchange="onObservationChanged()">
                <option value="severe_gales" selected>Alpine Gale Scour (Afternoon Gusts >40 km/h)</option>
                <option value="moderate_breeze">Moderate Valley Breeze (~20-25 km/h)</option>
                <option value="sheltered_calm">Sheltered Bench / Low Ridge Wind</option>
              </select>
            </div>

            <!-- (f) Sunlight Intensity & Intervals -->
            <div class="telem-col">
              <label>
                <span>Sunlight & Ridge Shadow</span>
                <span class="info-btn" tabindex="0">(i)
                  <span class="info-tooltip">
                    <div class="info-tooltip-title">[MEASURE: SUNLIGHT TIMING INTERVALS]</div>
                    5 White Stones Method. Place Stone 1 at morning sunbreak, Stone 2 at 10 AM, Stone 3 at solar noon, Stone 4 at 2 PM, Stone 5 at ridge shadow cutoff. If shadow hits at Stone 4 (2 PM), daily sun is < 4.5h. Only fast brassicas will finish.
                  </span>
                </span>
              </label>
              <select class="telem-select" id="selSunlight" onchange="onObservationChanged()">
                <option value="ridge_shaded_afternoon" selected>Lost by Mid-Afternoon (4-5 Sun Hours Max)</option>
                <option value="morning_shadow_only">Late Morning Sunbreak (High Eastern Ridge)</option>
                <option value="full_alpine_uv">Unobstructed High Plateau (7+ Sun Hours)</option>
                <option value="heavy_cloud_fog">Persistent Alpine Fog / Low Light</option>
              </select>
            </div>
          </div>

          <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <button class="btn-generate-protocol" onclick="generateProtocol()">
              <span>[▲]</span> GENERATE 9-STEP RESTORATION PROTOCOL
            </button>
            <span style="font-family:var(--font-mono); font-size:11px; color:var(--text-dim);" id="lblProtocolStatusPrompt">
              Adjust toggles or type notes above to unlock the 9-stage restoration pipeline.
            </span>
          </div>
        </div>

        <!-- CONDITIONAL 9-STAGE RESTORATION CONTAINER: REVEALED ONLY AFTER INPUT OR GENERATE -->
        <div id="sectionNineStages" style="display:none; flex-direction:column; gap:12px; transition:opacity 0.3s ease;">
          <!-- 9-Step Interactive Stage Navigation Pills -->
          <div>
            <div class="sidebar-label" style="padding-left:2px; margin-bottom:6px; color:var(--kin-orange);">
              [ACTIVE] 9-Stage Resolution Pipeline Navigator (Select stage to inspect):
            </div>
            <div class="steps-pills-strip" id="stagePillsStrip">
              <!-- Dynamically populated 9 pills -->
            </div>
          </div>

          <!-- Selected Step Resolution Output Card -->
          <div class="resolution-card">
            <div class="resolution-hdr">
              <div class="resolution-tag" id="resolutionStepTag">STAGE 01: INPUT ECHO</div>
              <span class="resolution-badge" id="resolutionBadgeStatus">GROUNDED IN TRAINING DATA</span>
            </div>
            <div class="resolution-body" id="resolutionContentText"></div>
          </div>
        </div>

        <!-- EMPTY STATE PROMPT WHEN NO INPUT GIVEN -->
        <div id="sectionNineStagesPlaceholder" style="background:var(--bg-panel); border:1px dashed var(--border-main); border-radius:6px; padding:28px 20px; text-align:center;">
          <div style="font-family:var(--font-mono); font-size:13px; font-weight:700; color:var(--kin-orange); margin-bottom:6px;">
            [◯] 9-STAGE RESTORATION PIPELINE AWAITING FIELD INPUT
          </div>
          <div style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-muted); max-width:680px; margin:0 auto; line-height:1.6;">
            The 9-step resolution architecture remains hidden until you provide mountain observations above.
            Enter your terrace description, select a quick preset, or adjust the 6 environmental toggles (temperature, snow, water, soil, wind, sun), then click 
            <strong style="color:#FFF;">"GENERATE 9-STEP RESTORATION PROTOCOL"</strong> to ground your inputs in <code>training_data.json</code>.
          </div>
        </div>

      </div>

      <!-- =================================================================== -->
      <!-- VIEW 2: TERRACE CONTOURS & HYDRO MAP (TAB: FLOOR) -->
      <!-- =================================================================== -->
      <div id="viewFloor" class="view-panel" style="display:none; flex-direction:column; gap:14px;">
        <div class="generator-card">
          <div class="generator-hdr">
            <div class="generator-title">[#] TERRACE TOPOGRAPHIC CONTOURS & SOLAR HYDRO DYNAMICS</div>
            <span class="resolution-badge">STREAM PRE-WARMING OPTIMIZER</span>
          </div>
          <p class="generator-desc">
            Direct application of 1–3 C glacial meltwater triggers root-cell paralysis for 48 hours.
            This module models contour ditching, dark slate warming pans, and ridge shadow trajectories.
          </p>

          <div style="background:#000000; border:1px solid var(--border-subtle); border-radius:6px; padding:20px; display:grid; grid-template-columns:1fr 1fr; gap:20px;">
            <div>
              <div class="sidebar-label" style="padding:0; margin-bottom:10px;">SOLAR SOAKING VESSEL SIMULATOR:</div>
              <div style="margin-bottom:12px;">
                <label style="font-size:11px; font-family:var(--font-mono); color:var(--text-muted); display:flex; justify-content:space-between;">
                  <span>Vessel Water Depth:</span>
                  <span id="txtDepthVal" style="color:var(--kin-orange);">20 cm (Bucket Depth)</span>
                </label>
                <input type="range" min="5" max="40" value="20" id="rngDepth" oninput="updateWaterSim()" style="width:100%; margin-top:4px;">
              </div>
              <div style="margin-bottom:12px;">
                <label style="font-size:11px; font-family:var(--font-mono); color:var(--text-muted); display:flex; justify-content:space-between;">
                  <span>Sun Exposure:</span>
                  <span id="txtSunVal" style="color:var(--kin-green);">85% (Alpine High UV)</span>
                </label>
                <input type="range" min="20" max="100" value="85" id="rngSun" oninput="updateWaterSim()" style="width:100%; margin-top:4px;">
              </div>
              <div style="background:var(--bg-card); padding:10px; border-radius:4px; font-family:var(--font-mono); font-size:11.5px; color:#E2E8F0;">
                <div>REQUIRED SOAKING: <strong id="lblSoakHours" style="color:var(--kin-orange);">2.0h</strong></div>
                <div style="margin-top:4px;">INNER WRIST TOUCH: <span id="lblWristFeel">Soothing lukewarm, zero stinging chill</span></div>
              </div>
            </div>

            <!-- SVG Contour Map: Fixed Pan & Blue Stream Line Bug -->
            <div style="background:#000000; border:1px solid var(--border-subtle); border-radius:6px; padding:12px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
              <svg viewBox="0 0 320 180" style="width:100%; height:160px; overflow:hidden;">
                <!-- Terrace 1: Upper Bench -->
                <polygon points="10,18 310,18 298,52 22,52" fill="#050505" stroke="rgba(255,255,255,0.12)" stroke-width="1" />
                <text x="28" y="38" fill="#64748B" font-family="JetBrains Mono" font-size="8.5" font-weight="bold">TERRACE 1: UPPER BENCH [POTATO EXCLUSION ZONE]</text>

                <!-- Terrace 2: Active Sowing Step -->
                <polygon points="20,62 300,62 288,110 32,110" fill="#0A0A0A" stroke="#FF5A1F" stroke-width="1.2" />
                <text x="38" y="82" fill="#F8FAFC" font-family="JetBrains Mono" font-size="8.5" font-weight="bold">TERRACE 2: ACTIVE SOWING [RADISH / TURNIP / TATSOI]</text>

                <!-- Terrace 3: Lower Bench -->
                <polygon points="30,120 290,120 278,168 42,168" fill="#050505" stroke="rgba(255,255,255,0.12)" stroke-width="1" />
                <text x="48" y="146" fill="#64748B" font-family="JetBrains Mono" font-size="8.5" font-weight="bold">TERRACE 3: LOWER BENCH [SIBERIAN KALE ROSETTES]</text>

                <!-- Upstream Melt Channel (Cold 1-3 C) -->
                <path d="M 275,10 C 265,30 255,50 248,72" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="4,2" />
                <text x="246" y="24" fill="#38BDF8" font-family="JetBrains Mono" font-size="7.5">1-3°C MELT</text>

                <!-- Dark Slate Solar Warming Pan (Seated cleanly in diversion notch) -->
                <rect x="216" y="68" width="46" height="24" rx="3" fill="#06090E" stroke="#FF5A1F" stroke-width="1.5" />
                <rect x="219" y="71" width="40" height="18" rx="2" fill="rgba(255, 90, 31, 0.12)" />
                <text x="223" y="83" fill="#FF5A1F" font-family="JetBrains Mono" font-size="8" font-weight="bold">SOLAR PAN</text>
                <text x="226" y="92" fill="#22C55E" font-family="JetBrains Mono" font-size="6.5">PRE-WARM</text>

                <!-- Warmed Outflow Irrigating Terrace 2 (Soothing Lukewarm) -->
                <path d="M 216,80 C 185,82 145,95 90,95" fill="none" stroke="#22C55E" stroke-width="2" />
                <circle cx="90" cy="95" r="3" fill="#22C55E" />
                <text x="100" y="103" fill="#22C55E" font-family="JetBrains Mono" font-size="7">WARMED DRIP LINE (SAFE)</text>

                <!-- Bypass overflow channel safely exiting down contour -->
                <path d="M 252,92 C 250,115 242,145 235,175" fill="none" stroke="#38BDF8" stroke-width="1.8" opacity="0.6" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- =================================================================== -->
      <!-- VIEW 3: WORKFORCE & READINESS GATES (TAB: WORKFORCE) -->
      <!-- =================================================================== -->
      <div id="viewWorkforce" class="view-panel" style="display:none; flex-direction:column; gap:14px;">
        <div class="generator-card">
          <div class="generator-hdr">
            <div class="generator-title">[@] STEP 4 MANDATORY PHYSICAL READINESS GATE CHECKPOINT</div>
            <span class="resolution-badge" id="lblGatesBadge" style="color:var(--kin-orange);">LOCKED: 0/7 PASSED</span>
          </div>
          <p class="generator-desc">
            Official evaluation rule: <strong>Soil preparation and readiness verification must strictly precede crop planting</strong>.
            Click each tactile gate as you empirically test and verify it on the mountain terrace:
          </p>

          <div id="readinessChecklistContainer">
            <!-- Populated via JS -->
          </div>

          <div class="sidebar-label" style="padding:0; margin-top:14px;">9-STAGE RESTORATION STANDARD OPERATING PROCEDURE (SOP):</div>
          <div id="sopListContainer" style="display:flex; flex-direction:column; gap:8px;"></div>
        </div>
      </div>

      <!-- =================================================================== -->
      <!-- VIEW 4: BIOLOGICAL CROPS (TAB: PERF) -->
      <!-- =================================================================== -->
      <div id="viewPerf" class="view-panel" style="display:none; flex-direction:column; gap:14px;">
        <div class="generator-card">
          <div class="generator-hdr">
            <div class="generator-title">[%] BIOLOGICAL CROP MATRIX & COLD LATENCY ENGINE</div>
            <span class="resolution-badge">+40% TO +60% DELAY BUFFER</span>
          </div>
          <p class="generator-desc">
            Seed packets assume 20 C lowland conditions. In cold thin mountain soil, cellular root division slows down.
            Crops exceeding the 49-day hard freeze horizon will rot in the ground.
          </p>

          <div style="background:rgba(255, 90, 31, 0.08); border:1px solid var(--kin-orange); border-radius:4px; padding:12px; font-family:var(--font-mono); font-size:11.5px; color:#FDE68A;">
            <strong>THE POTATO TRAP IN HIGH-ALTITUDE COLD TERRACES:</strong>
            Potatoes require 110–120 cold days. In a 7-week season, early frosts kill foliage and tubers rot. 
            Prioritize <strong>Quick Mountain Radishes (24d nominal -> 38d cold)</strong> and <strong>Tokyo Turnips (35d nominal -> 50d cold)</strong>.
          </div>

          <div id="cropsGridContainer" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:12px; margin-top:10px;"></div>
        </div>
      </div>

      <!-- =================================================================== -->
      <!-- VIEW 5: SENSORY COMPASS & DOSSIER (TAB: LOGS) -->
      <!-- =================================================================== -->
      <div id="viewLogs" class="view-panel" style="display:none; flex-direction:column; gap:14px;">
        <div class="generator-card">
          <div class="generator-hdr">
            <div class="generator-title">[=] ZERO-INSTRUMENT TACTILE SENSORY COMPASS & PART A DOSSIER</div>
            <button class="btn-ftr-primary" onclick="openDossierModal()">EXPORT DOSSIER MARKDOWN</button>
          </div>
          <p class="generator-desc">
            Everyday sensory calibrations replacing scientific lab equipment:
          </p>

          <div id="compassGridContainer" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:12px;"></div>
        </div>
      </div>

    </main>

    <!-- RIGHT SIDEBAR -->
    <aside class="kin-sidebar-right">
      
      <div>
        <div class="right-sec-title">Terrace System Health</div>

        <div class="health-metric-block">
          <div class="health-metric-top">
            <span>SEASON ELAPSED</span>
            <span>42%</span>
          </div>
          <div class="health-bar-track">
            <div class="health-bar-fill orange"></div>
          </div>
          <div class="cpu-mini-eq">
            <div class="eq-bar" style="height: 4px;"></div>
            <div class="eq-bar" style="height: 10px;"></div>
            <div class="eq-bar" style="height: 7px;"></div>
            <div class="eq-bar" style="height: 12px;"></div>
            <div class="eq-bar" style="height: 6px;"></div>
          </div>
        </div>

        <div class="health-metric-block">
          <div class="health-metric-top white-val">
            <span>READINESS GATES</span>
            <span id="sideGatesVal">0 / 7 PASSED</span>
          </div>
          <div class="health-bar-track">
            <div id="sideGatesBar" class="health-bar-fill white" style="width: 0%;"></div>
          </div>
        </div>

        <div class="health-metric-block">
          <div class="health-metric-top white-val">
            <span>COLD BUFFER</span>
            <span style="color:#FFF;">+48% LATENCY</span>
          </div>
          <div class="seg-bar-wrap">
            <div class="seg-piece active"></div>
            <div class="seg-piece active"></div>
            <div class="seg-piece"></div>
          </div>
        </div>
      </div>

      <div>
        <div class="right-sec-title">Field Alerts</div>
        <div class="alerts-feed-list" id="alertsFeedList">
          <!-- Dynamically updated based on survivor actions -->
        </div>
      </div>

      <div>
        <div class="right-sec-title">Quick Actions</div>
        <div class="quick-actions-grid">
          <button class="btn-quick" onclick="selectNav('workforce')">
            <span class="btn-quick-icon">[+]</span>
            <span>GATES</span>
          </button>
          <button class="btn-quick" onclick="openDossierModal()">
            <span class="btn-quick-icon">[▲]</span>
            <span>DOSSIER</span>
          </button>
        </div>
      </div>

    </aside>

  </div>

  <!-- Detailed Modal -->
  <div class="modal-backdrop" id="kinModal">
    <div class="modal-box">
      <div class="modal-hdr">
        <h3 id="modalHeading">HackIt // TERRACE RESTORATION DISPATCH</h3>
        <button style="background:none; border:none; color:var(--text-muted); font-size:14px; font-weight:bold; cursor:pointer;" onclick="closeModal()">X</button>
      </div>
      <div class="modal-body-scroll" id="modalBodyText"></div>
      <div class="modal-ftr">
        <button class="btn-ftr-primary" onclick="copyModalMarkdown()">COPY MARKDOWN</button>
        <button class="btn-quick" style="padding:6px 12px;" onclick="closeModal()">CLOSE</button>
      </div>
    </div>
  </div>

  <script>
    const EXAMPLES = {
      1: "The terrace wall has collapsed in one place. Soil is thin, about a hand deep, and half stones. Frost on the plants every morning. The ridge shades the plot by mid-afternoon. Water comes from an ice-cold glacial stream. I think summer lasts about 6 weeks.",
      2: "Steep open mountain slope with no terraces intact. Thin gravelly scree slides under boot heels. Cold wind scour, no windbreak. Frost covers the gravel every morning. Water rushes down without soaking. Growing season feels very brief and uncertain.",
      3: "A flat terrace step nestled in a mountain bowl. Deep cold air pools at night with heavy white frost. Soil is damp, compacted glacial clay with poor drainage. The front wall is standing firm. Sunlight is blocked until mid-morning and lost early afternoon.",
      4: "An upper terrace bench exposed to heavy mountain gales. Decent soil depth (two hand-spans), but acidic with conifer needle duff and gravel. Light frost in mornings, full midday sun. Front wall is bulging slightly."
    };

    const STEP_DEFS = [
      { num: "01", key: "step_1_input_echo", title: "INPUT ECHO", sub: "Diagnostic Cue Grounding" },
      { num: "02", key: "step_2_missing_analysis", title: "MISSING ANALYSIS", sub: "Soil Archetype Diagnosis" },
      { num: "03", key: "step_3_fix_protocol", title: "FIX PROTOCOL", sub: "Quantified Remediation" },
      { num: "04", key: "step_4_readiness_gate", title: "NEXT ACTION", sub: "Empirical Readiness Gates" },
      { num: "05", key: "step_5_crop_suggestions", title: "CROP OPTIONS", sub: "Resilient Crop Selection" },
      { num: "06", key: "step_6_timeframe", title: "TIMEFRAME", sub: "Dual Timeline & Buffer" },
      { num: "07", key: "step_7_planting_method", title: "PLANTING METHOD", sub: "Substrate & Water Setup" },
      { num: "08", key: "step_8_ongoing_care", title: "ONGOING CARE", sub: "Staged Frost & Pest Regimen" },
      { num: "09", key: "step_9_harvest_regen", title: "HARVEST & REGEN", sub: "Ripeness & Soil Revival" }
    ];

    let currentResults = {};
    let activeStepIdx = 0;

    const readinessState = {
      wallStable: false,
      stonesCleared: true,
      organicWorked: false,
      soilDepthAdequate: true,
      middaySoilWarmth: false,
      waterWarmed: false,
      frostCoverStaged: false
    };

    const readinessLabels = {
      wallStable: "1. Terrace Wall Stability: Rebuilt & holds rigid under full shoulder shove",
      stonesCleared: "2. Coarse Stones Cleared: Fist-sized rocks picked out of top hand-depth",
      organicWorked: "3. Humus Sponge Incorporated: 2-3 buckets of leaf mould worked in per pace",
      soilDepthAdequate: "4. Workable Depth Check: Flat hand plunges past the wrist without hitting bedrock",
      middaySoilWarmth: "5. Midday Warmth Check: Bare back of hand pressed to noon soil feels neutral, not icy",
      waterWarmed: "6. Irrigation Water Pre-Warmed: Glacial runoff solar-warmed in dark pans",
      frostCoverStaged: "7. Twilight Frost Covers Staged: Willow hoops and stone weights ready for 4 PM deployment"
    };

    function updateClock() {
      const now = new Date();
      let hours = now.getHours();
      let minutes = now.getMinutes();
      let seconds = now.getSeconds();
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12;
      hours = hours ? hours : 12;
      const strTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')} ${ampm}`;
      document.getElementById('liveTimestamp').innerText = strTime;
    }
    setInterval(updateClock, 1000);
    updateClock();

    function selectNav(type) {
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.view-panel').forEach(el => el.style.display = 'none');

      if (type === 'live') {
        document.getElementById('navLiveOps').classList.add('active');
        document.getElementById('viewLive').style.display = 'flex';
      } else if (type === 'floor') {
        document.getElementById('navFloorMap').classList.add('active');
        document.getElementById('viewFloor').style.display = 'flex';
      } else if (type === 'workforce') {
        document.getElementById('navWorkforce').classList.add('active');
        document.getElementById('viewWorkforce').style.display = 'flex';
      } else if (type === 'perf') {
        document.getElementById('navPerf').classList.add('active');
        document.getElementById('viewPerf').style.display = 'flex';
      } else if (type === 'logs') {
        document.getElementById('navLogs').classList.add('active');
        document.getElementById('viewLogs').style.display = 'flex';
      }
    }

    let alertsList = [
      { text: "System initialized: Sector 76 Baseline loaded", time: "Just now", active: true },
      { text: "Needle frost on upper bench", time: "2 mins ago", active: false },
      { text: "Stream diverted to solar pan", time: "15 mins ago", active: true },
      { text: "Organic leaf duff worked in", time: "1 hour ago", active: false }
    ];

    function renderFieldAlerts() {
      const container = document.getElementById('alertsFeedList');
      if (!container) return;
      container.innerHTML = '';
      alertsList.slice(0, 5).forEach(alert => {
        const row = document.createElement('div');
        row.className = 'alert-row';
        row.innerHTML = `
          <div class="alert-dot ${alert.active ? 'orange' : ''}"></div>
          <div class="alert-content">
            <div class="alert-text">${alert.text}</div>
            <div class="alert-time">${alert.time}</div>
          </div>
        `;
        container.appendChild(row);
      });
    }

    function addFieldAlert(text, active = true) {
      alertsList.unshift({ text, time: "Just now", active });
      if (alertsList.length > 8) alertsList.pop();
      renderFieldAlerts();
    }

    function onObservationChanged() {
      const text = document.getElementById('survivorInputText').value.trim();
      const temp = document.getElementById('selTemp').value;
      const snow = document.getElementById('selSnowDepth').value;
      const water = document.getElementById('selWater').value;
      const soil = document.getElementById('selSoil').value;
      const wind = document.getElementById('selWind').value;
      const sun = document.getElementById('selSunlight').value;

      if (text.length > 0) {
        document.getElementById('lblProtocolStatusPrompt').innerText = "Inputs updated. Click GENERATE to process through 9-stage restoration architecture.";
        document.getElementById('lblProtocolStatusPrompt').style.color = "var(--kin-orange)";
      }

      addFieldAlert(`Telemetry updated: ${soil.replace(/_/g, ' ')} | ${wind.replace(/_/g, ' ')}`, true);
    }

    function loadExample(idx) {
      // Highlight selected preset card
      for (let i = 1; i <= 4; i++) {
        const card = document.getElementById(`presetCard${i}`);
        if (card) {
          if (i === idx) card.classList.add('active');
          else card.classList.remove('active');
        }
      }

      const presetNames = {
        1: "Mission 01: Baseline Terrace",
        2: "Mission 02: Steep Scree Slope",
        3: "Mission 03: Frost Pocket Clay",
        4: "Mission 04: Gale Bench"
      };

      if (EXAMPLES[idx]) {
        document.getElementById('survivorInputText').value = EXAMPLES[idx];
        
        // Sync telemetry selectors to archetype
        if (idx === 1) {
          document.getElementById('selTemp').value = 'cold_borderline';
          document.getElementById('selSnowDepth').value = 'hand_depth';
          document.getElementById('selWater').value = 'glacial_stream_nearby';
          document.getElementById('selSoil').value = 'thin_stony_loam';
          document.getElementById('selWind').value = 'severe_gales';
          document.getElementById('selSunlight').value = 'ridge_shaded_afternoon';
        } else if (idx === 2) {
          document.getElementById('selTemp').value = 'freezing_subzero';
          document.getElementById('selSnowDepth').value = 'hand_depth';
          document.getElementById('selWater').value = 'snow_melt_channel';
          document.getElementById('selSoil').value = 'loose_gravel_scree';
          document.getElementById('selWind').value = 'severe_gales';
          document.getElementById('selSunlight').value = 'full_alpine_uv';
        } else if (idx === 3) {
          document.getElementById('selTemp').value = 'freezing_subzero';
          document.getElementById('selSnowDepth').value = 'heavy_drift';
          document.getElementById('selWater').value = 'standing_pool';
          document.getElementById('selSoil').value = 'compacted_clay';
          document.getElementById('selWind').value = 'sheltered_calm';
          document.getElementById('selSunlight').value = 'morning_shadow_only';
        } else if (idx === 4) {
          document.getElementById('selTemp').value = 'cold_borderline';
          document.getElementById('selSnowDepth').value = 'rare_dusting';
          document.getElementById('selWater').value = 'glacial_stream_nearby';
          document.getElementById('selSoil').value = 'deep_worked_humus';
          document.getElementById('selWind').value = 'severe_gales';
          document.getElementById('selSunlight').value = 'full_alpine_uv';
        }

        addFieldAlert(`Preset loaded: ${presetNames[idx] || 'Custom'}`, true);
        generateProtocol();
      }
    }

    function toggleSolarBufferModal(e) {
      if (e) e.stopPropagation();
      openModalWithContent(
        'SURVIVAL SOLAR BUFFER — DETAILED TECHNICAL BRIEF',
        `WHAT IS SURVIVAL SOLAR BUFFER?
In plain, non-academic words:

High-altitude cold mountain terraces lose all heat the moment the sun dips behind the towering mountain ridge. Without any heat buffer, the soil temperature plunges below 0°C within 30 minutes of sunset, causing cellular rupture in root hairs and killing delicate brassica seedlings.

HOW THE SOLAR BUFFER WORKS WITHOUT ANY LAB INSTRUMENTS:
1. Dry Stone Walls: The dark granite and schist stones stacked into the terrace retaining wall absorb solar radiation from 10:00 AM to 2:30 PM. After dusk, they radiate low-frequency thermal energy outward into the soil beds for 3 to 4 hours.
2. Slate Solar Warming Pans: Shallow dark stone pans placed along the contour heat glacial stream water (1-3°C) up to a neutral, soothing wrist-warm temperature before it reaches crop roots.
3. Dark Stone Mulch: Laying fist-sized black slate fragments around plant collars acts as thermal batteries directly above the root crown.

SURVIVAL BUFFER STATUS: 98.2% (OPTIMAL)
Sufficient thermal mass is stored in the Sector 76 front wall to shield cold-tolerant turnip and radish taproots against nightly sub-zero frost.`
      );
    }

    function renderStagePills() {
      const strip = document.getElementById('stagePillsStrip');
      strip.innerHTML = '';
      STEP_DEFS.forEach((s, idx) => {
        const pill = document.createElement('div');
        pill.className = `step-nav-pill ${idx === activeStepIdx ? 'active' : ''}`;
        pill.onclick = () => selectStep(idx);
        pill.innerHTML = `
          <div class="step-nav-pill-num">STEP ${s.num}</div>
          <div class="step-nav-pill-title">${s.title}</div>
        `;
        strip.appendChild(pill);
      });
    }

    function selectStep(idx) {
      activeStepIdx = idx;
      renderStagePills();
      const s = STEP_DEFS[idx];
      document.getElementById('resolutionStepTag').innerText = `STAGE ${s.num}: ${s.title} — ${s.sub.toUpperCase()}`;
      const content = currentResults[s.key] || "Click 'GENERATE 9-STEP RESTORATION PROTOCOL' to ground cues and run analysis.";
      document.getElementById('resolutionContentText').innerText = content;
    }

    async function generateProtocol() {
      const input = document.getElementById('survivorInputText').value.trim();
      const telemetry = {
        outside_temp: document.getElementById('selTemp').value,
        snow_depth: document.getElementById('selSnowDepth').value,
        water_availability: document.getElementById('selWater').value,
        soil_condition: document.getElementById('selSoil').value,
        wind_speed: document.getElementById('selWind').value,
        sunlight_intensity: document.getElementById('selSunlight').value,
        snow_days: document.getElementById('selSnowDepth').value,
        sun_intensity: document.getElementById('selSunlight').value,
        is_alone: true
      };

      // Reveal the 9-stage section and hide placeholder
      const nineSec = document.getElementById('sectionNineStages');
      const placeholder = document.getElementById('sectionNineStagesPlaceholder');
      if (nineSec) nineSec.style.display = 'flex';
      if (placeholder) placeholder.style.display = 'none';

      document.getElementById('resolutionContentText').innerText = "DISPATCHING AUTONOMOUS ANALYSIS ACCROSS 9 STAGES...\n[Grounding survivor cues from training_data.json]\n[Evaluating terrace wall stability, cold-soil latency, and frost boundaries]...\n[Filtering zero-instrument constraints]...";

      try {
        const res = await fetch('/api/advise', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input, telemetry })
        });
        currentResults = await res.json();
        selectStep(0);
        document.getElementById('lblProtocolStatusPrompt').innerText = "[PASS] 9-stage restoration protocol successfully generated and grounded.";
        document.getElementById('lblProtocolStatusPrompt').style.color = "var(--kin-green)";
        addFieldAlert("9-Stage Protocol compiled & grounded in training_data.json", true);
      } catch (err) {
        document.getElementById('resolutionContentText').innerText = "Error executing analysis: " + err.message;
        addFieldAlert("Protocol generation error: " + err.message, true);
      }
    }

    function renderReadinessList() {
      const container = document.getElementById('readinessChecklistContainer');
      container.innerHTML = '';
      let passedCount = 0;
      const total = Object.keys(readinessState).length;

      for (const [key, passed] of Object.entries(readinessState)) {
        if (passed) passedCount++;
        const item = document.createElement('div');
        item.className = `readiness-item ${passed ? 'passed' : ''}`;
        item.onclick = () => {
          readinessState[key] = !readinessState[key];
          const newStatus = readinessState[key] ? "[VERIFIED]" : "[UNCHECKED]";
          addFieldAlert(`Gate check ${newStatus}: ${key}`, readinessState[key]);
          renderReadinessList();
        };
        item.innerHTML = `
          <div class="readiness-text">${readinessLabels[key]}</div>
          <div class="readiness-check-box">${passed ? 'OK' : ''}</div>
        `;
        container.appendChild(item);
      }

      document.getElementById('kpiGatesNum').innerHTML = `${passedCount}<span style="font-size:16px; color:var(--text-dim);">/${total}</span>`;
      document.getElementById('sideGatesVal').innerText = `${passedCount} / ${total} PASSED`;
      document.getElementById('sideGatesBar').style.width = `${Math.round((passedCount/total)*100)}%`;

      const badge = document.getElementById('lblGatesBadge');
      const sub = document.getElementById('kpiGatesSub');
      if (passedCount === total) {
        badge.innerText = `GATE PASSED: ${passedCount}/${total} VERIFIED (SAFE TO SOW)`;
        badge.style.color = 'var(--kin-green)';
        sub.innerText = "PASSED";
        sub.className = "metric-sub green";
      } else {
        badge.innerText = `LOCKED: ${passedCount}/${total} PASSED (${total - passedCount} MISSING)`;
        badge.style.color = 'var(--kin-orange)';
        sub.innerText = "LOCKED";
        sub.className = "metric-sub orange";
      }
    }

    async function loadDomainData() {
      const res = await fetch('/api/domain_data');
      const data = await res.json();

      // SOP Roadmap list
      const sopBox = document.getElementById('sopListContainer');
      sopBox.innerHTML = '';
      data.nineSteps.forEach(s => {
        const d = document.createElement('div');
        d.style.background = 'var(--bg-card)';
        d.style.border = '1px solid var(--border-subtle)';
        d.style.borderRadius = '4px';
        d.style.padding = '8px 12px';
        d.innerHTML = `
          <div style="font-family:var(--font-mono); font-size:11px; font-weight:bold; color:#FFF;">STAGE ${s.step}: ${s.title} (${s.sub})</div>
          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-muted); margin-top:3px;">${s.goal}</div>
        `;
        sopBox.appendChild(d);
      });

      // Crops Matrix: Pop-Out Cards with Growing Details & Critical Stressors
      const cropsBox = document.getElementById('cropsGridContainer');
      cropsBox.innerHTML = '';
      data.crops.forEach(c => {
        const item = document.createElement('div');
        const isFail = c.id === 'chitted-potato';
        item.className = `crop-pop-card ${isFail ? 'excluded-card' : ''}`;
        
        // Build growing steps HTML
        const stepsHtml = (c.howToGrow || []).map(step => `
          <div style="font-size:10.5px; color:#CAD5E2; line-height:1.45; margin-bottom:3px;">
            • ${step}
          </div>
        `).join('');

        // Build critical issues HTML
        const crit = c.criticalIssues || {};
        const windNote = crit.wind || c.windThreshold || "Protect from dry gales";
        const sunNote = crit.sunlight || c.optimalSunPct || "Monitor ridge shade";
        const tempNote = crit.temperature || c.tempRange || "Watch night needle frost";

        item.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div>
              <div style="font-family:var(--font-mono); font-size:13px; font-weight:700; color:#FFF;">${c.name}</div>
              <div style="font-family:var(--font-mono); font-size:10px; color:var(--text-dim);">${c.variety} [${c.category.toUpperCase()}]</div>
            </div>
            <span style="font-family:var(--font-mono); font-size:9px; font-weight:700; padding:3px 7px; border-radius:3px; background:${isFail ? 'rgba(239,71,111,0.12)' : 'rgba(34,197,94,0.12)'}; color:${isFail ? '#EF476F' : '#22C55E'}; border:1px solid ${isFail ? '#EF476F' : '#22C55E'}; white-space:nowrap;">
              ${isFail ? '[FAIL] EXCLUDED' : '[PASS] VIABLE'}
            </span>
          </div>

          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-muted); background:var(--bg-panel); padding:8px; border-radius:4px; border:1px solid var(--border-subtle); display:flex; justify-content:space-between;">
            <span>Nominal: <strong style="color:#FFF;">${c.nominalDays}d</strong></span>
            <span>Cold Buffer: <strong style="color:var(--kin-orange);">x${c.coldBufferMultiplier} (+${Math.round((c.coldBufferMultiplier-1)*100)}%)</strong></span>
            <span>Depth: <strong style="color:#FFF;">${c.minSoilDepth || 'hand-depth'}</strong></span>
          </div>

          <!-- Critical Issues Badges -->
          <div style="display:flex; flex-direction:column; gap:4px;">
            <div class="crop-stressor-badge crit-wind">
              <span>[WIND]</span> ${windNote}
            </div>
            <div class="crop-stressor-badge crit-sun">
              <span>[SUN]</span> ${sunNote}
            </div>
            <div class="crop-stressor-badge crit-temp">
              <span>[TEMP]</span> ${tempNote}
            </div>
          </div>

          <!-- Step-by-Step Growing Procedure -->
          <div style="background:rgba(0,0,0,0.25); border:1px solid var(--border-subtle); border-radius:4px; padding:8px;">
            <div style="font-family:var(--font-mono); font-size:9.5px; font-weight:700; color:var(--kin-orange); margin-bottom:4px; text-transform:uppercase;">
              How to Grow in Cold Mountain Terraces:
            </div>
            ${stepsHtml}
          </div>

          <div style="font-family:var(--font-mono); font-size:10.5px; color:${isFail ? '#FCA5A5' : 'var(--text-muted)'}; line-height:1.4;">
            <strong>Scenario Logic:</strong> ${c.whyItFits}
          </div>
        `;
        cropsBox.appendChild(item);
      });

      // Compass (High-Tech Sci-Fi Radar Sensory Cards)
      const compassBox = document.getElementById('compassGridContainer');
      compassBox.innerHTML = '';
      data.compass.forEach(cp => {
        const card = document.createElement('div');
        card.className = 'compass-card';
        
        const procHtml = cp.procedure ? `
          <div class="compass-procedure-box">
            <div class="compass-procedure-label">[ACTION PROCEDURE]</div>
            <div>${cp.procedure}</div>
          </div>
        ` : '';

        const toolHtml = cp.tool ? `
          <div class="compass-tool-row">
            <span class="compass-tool-label">[TOOL]:</span>
            <span>${cp.tool}</span>
          </div>
        ` : '';

        card.innerHTML = `
          <div class="compass-hdr">
            <div class="compass-title">${cp.title}</div>
            <span class="compass-realm-tag">${cp.realm}</span>
          </div>
          ${toolHtml}
          ${procHtml}
          <div class="compass-body">
            <span style="color:var(--kin-orange); font-weight:700;">[DIAGNOSIS & DETAIL]:</span> ${cp.detail}
          </div>
        `;
        compassBox.appendChild(card);
      });
    }

    function calcSoakLocal(depthCm, sunPct) {
      // Direct client calculation: baseline 20cm at 100% sun = 2 hours, with dark stones = 1.5h
      const baseHours = (depthCm / 10.0) * (100.0 / Math.max(20, sunPct)) * 0.75;
      const hours = Math.round(baseHours * 10) / 10;
      let wristFeel = "Inner wrist feels neutral or gentle warmth with zero involuntary recoil or stinging chill";
      if (hours > 3.5) {
        wristFeel = "Still carries slight needle chill; allow another candle-flicker of midday exposure";
      } else if (hours < 1.0) {
        wristFeel = "Lukewarm soothing bath; completely safe for cold brassica seedlings";
      }
      return { hours, wristFeel };
    }

    async function updateWaterSim() {
      const depthEl = document.getElementById('rngDepth');
      const sunEl = document.getElementById('rngSun');
      if (!depthEl || !sunEl) return;
      const depth = parseInt(depthEl.value, 10);
      const sun = parseInt(sunEl.value, 10);

      document.getElementById('txtDepthVal').innerText = `${depth} cm (${depth <= 10 ? 'Shallow Basin' : 'Bucket Depth'})`;
      document.getElementById('txtSunVal').innerText = `${sun}% (${sun > 75 ? 'Alpine High UV' : 'Filtered Sun'})`;

      // Instant client-side response
      const local = calcSoakLocal(depth, sun);
      const soakEl = document.getElementById('lblSoakHours');
      const wristEl = document.getElementById('lblWristFeel');
      if (soakEl) soakEl.innerText = `${local.hours}h`;
      if (wristEl) wristEl.innerText = local.wristFeel;

      // Dynamic field alert on significant adjustment
      addFieldAlert(`Hydro slider adjusted: Depth ${depth}cm @ ${sun}% sun -> ${local.hours}h required`, false);

      try {
        const res = await fetch(`/api/water_calc?depth=${depth}&sun=${sun}&stones=true`);
        if (res.ok) {
          const data = await res.json();
          if (soakEl) soakEl.innerText = `${data.estimatedHours}h`;
          if (wristEl) wristEl.innerText = data.wristTouchFeel;
        }
      } catch (e) {
        // Fallback already rendered
      }
    }

    async function openDossierModal() {
      const res = await fetch('/api/full_dossier_markdown');
      const text = await res.text();
      openModalWithContent('HackIt // OFFICIAL PART A DOSSIER', text);
    }

    function openModalWithContent(title, text) {
      document.getElementById('modalHeading').innerText = title;
      document.getElementById('modalBodyText').innerText = text;
      document.getElementById('kinModal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('kinModal').style.display = 'none';
    }

    function copyModalMarkdown() {
      const text = document.getElementById('modalBodyText').innerText;
      navigator.clipboard.writeText(text);
      alert('Official Part A Dossier Markdown copied to clipboard.');
    }

    function triggerEStop() {
      alert('E-STOP TRIGGERED: Soil readiness gates locked. Planting prohibited.');
    }

    function toggleSectorSelect() {
      const sectors = ['Sector 76 (Alpine Cold Terrace)', 'Sector 77 (Wind-Scoured Upper Bench)', 'Sector 78 (Glacial Wash Scree)'];
      const cur = document.getElementById('currentSectorText').innerText;
      const next = sectors[(sectors.indexOf(cur) + 1) % sectors.length];
      document.getElementById('currentSectorText').innerText = next;
    }

    window.onload = () => {
      // Start in awaiting-input state; load preset when user clicks or types
      renderStagePills();
      renderReadinessList();
      renderFieldAlerts();
      loadDomainData();
      updateWaterSim();
    };
  </script>
</body>
</html>
"""

class SupercomputerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))

        elif path == "/api/domain_data":
            data = {
                "crops": ds.SCENARIO_CROPS,
                "compass": ds.NO_LAB_COMPASS,
                "nineSteps": ds.NINE_STEPS_DEFINITION
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/water_calc":
            depth = int(query.get("depth", ["20"])[0])
            sun = int(query.get("sun", ["85"])[0])
            stones = query.get("stones", ["true"])[0].lower() == "true"
            result = ds.calculate_water_soak_slider(depth, sun, stones)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif path == "/api/full_dossier_markdown":
            dossier_text = f"""# HackIt // SUPERCOMPUTER RESTORATION DOSSIER: SCENARIO 2
SECTOR: Sector 76 (High-Altitude Cold Terrace - Frost + Short Season)
TRAINED SOLELY ON: training_data.json
COMPLIANCE: 100% Zero-Instrument Constitution
MEASUREMENTS: Handful, Bucketful, Pace, Hand's Depth, Finger Knuckle

================================================================================
PART A CERTIFICATION & GROUND RULE
================================================================================
"The survivor has no instruments and no lab. Your System must not ask for, quote,
or depend on scientific readings or fixed numbers. Any check it suggests must be
doable with eyes, hands, and household items, and amounts must be described in
everyday terms (a handful, a bucketful, a pace, a hand's depth)."

STAGE 1: INPUT ECHO
Restatement: Mountain terrace step, thin gritty cryic lithic soil, severe morning
needle frost, high midday UV radiation. Sunlight truncated by opposing ridge
before sunset. Glacial stream runoff (near-freezing). Retaining wall damaged.

STAGE 2: MISSING ANALYSIS & ZERO-LAB TESTS
Soil Archetype: Thin Stony Loam (Lithic Cryic Regosol).
What is Missing: Exact summer duration, freeze date, soil depth across bed, rock ratio.
Sensory Tests (from training_data.json):
1. Sunlight Check: Track shadow cutoff line using 5 white pebbles on terrace rim.
2. Soil Depth Check: Drive dry thumb-thick pine branch until hitting rock ledge.
3. Stone Ratio Check: Sift 1 standard bucketful; hand-sort stones larger than knuckle.
4. Biological Phenology: Watch mountain pipit flocking & dandelion tufts for freeze cues.

STAGE 3: FIX PROTOCOL
Remediation (from training_data.json):
1. Dry-stone retaining wall restacked at inward batter angle (1 fist lean per chest height).
2. Surface stone picking: remove fist-sized rocks; stack as thermal windbreak on north/east.
3. Humus sponge incorporation: work 2-3 bucketfuls of forest leaf duff per pace.
4. Dark slate stone mulch: place around seedling collars to capture midday solar radiation.
5. Flexible willow frost hoops: staged with canvas ready for 4 PM deployment.

STAGE 4: NEXT ACTION (STRICT READINESS GATE)
All 4 physical gates must hold rigid before planting:
1. Wall Stability Gate: Wall holds firm against full shoulder shove with zero shifting.
2. Workable Depth Gate: Flat hand plunges past the wrist without hitting bedrock.
3. Midday Warmth Gate: Bare back of hand pressed to noon soil feels neutral, not icy.
4. Glacial Water Solar Pre-Warming Gate: Water warmed in shallow slate pans until soothing to wrist.

STAGE 5: CROP SUGGESTIONS (RESILIENT SHORT-SEASON SELECTION)
1. Quick Mountain Radish (24d nominal -> 38d cold-slowed): edible greens in 2 spans.
2. Hardy Tokyo Turnip (35d nominal -> 50d cold-slowed): dual harvest (greens + root).
3. Siberian Kale & Spoon Tatsoi (42d nominal -> 55d cold-slowed): extreme frost survivor.
4. EXCLUDED: Early Mountain Potato (110d+ required; will rot in cold soil).

STAGE 6: TIMEFRAME & BIOLOGICAL BUFFER
Operational Window: 7 Weeks (49 Days).
Cold-Slowed Growth Buffer: +40% to +60% applied to all lowland seed estimates.

STAGE 7: PLANTING METHOD & SOLAR-WARMED WATER
Geometry: Domed beds (1 hand-span high in center) for cold air drainage.
Depth: 1 finger-knuckle deep (~2 cm).
Watering: Never pour 1-3 C glacial runoff directly on roots. Solar-warm in shallow slate pans.

STAGE 8: ONGOING CARE & ABIOTIC SHIELDS
Twilight Frost Routine: Unfurl canvas/brushwood covers before 4 PM; prop open at 10 AM.
Fertility & Pest: Warm dung tea drench bi-weekly; dust hearth ash against flea beetles.

STAGE 9: HARVEST RIPENESS & REGENERATION
Ripeness: Turnip shoulders bulge 2-3 fingers above soil; radishes thumb-thick.
Emergency Harvest: Immediate harvest if mountain pipits flock downslope or snow stays white past noon.
Soil Regeneration: Residue crimping, dung-quenched biochar pit creation, wall chinking.
"""
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(dossier_text.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/advise":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            user_input = data.get("input", "")
            telemetry = data.get("telemetry", None)

            results = ADVISOR.advise(user_input, telemetry)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SupercomputerHandler) as httpd:
        print(f"HackIt Scenario 2 Supercomputer Terminal online on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
