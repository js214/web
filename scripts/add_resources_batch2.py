#!/usr/bin/env python3
"""Add resources and related sections to remaining product .md files."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTS = ROOT / "products"
BASE = "https://thinksrs.com"

DATA = {
    "qms100": {
        "resources": [
            {"label": "RGA Basics", "url": f"{BASE}/downloads/pdfs/applicationnotes/Residual%20Gas%20Analysis%20Basics.pdf"},
        ],
        "related": [
            {"label": "UGA120 Leak Detector / Gas Analyzer", "url": "uga120.html"},
            {"label": "RGA Residual Gas Analyzers", "url": "rga.html"},
        ],
    },
    "ugapm": {
        "resources": [],
        "related": [
            {"label": "UGA120 Leak Detector / Gas Analyzer", "url": "uga120.html"},
            {"label": "RGA Residual Gas Analyzers", "url": "rga.html"},
        ],
    },
    "cis100": {
        "resources": [],
        "related": [
            {"label": "RGA Residual Gas Analyzers", "url": "rga.html"},
            {"label": "RGA120 High-Sensitivity RGA Systems", "url": "rga120.html"},
        ],
    },
    "qcm200": {
        "resources": [],
        "related": [
            {"label": "EC301 Electrochemical Potentiostat", "url": "ec301.html"},
        ],
    },
    "ec301": {
        "resources": [],
        "related": [
            {"label": "QCM200 Quartz Crystal Microbalance", "url": "qcm200.html"},
        ],
    },
    "nl100": {
        "resources": [],
        "related": [],
    },
    "mpa100": {
        "resources": [],
        "related": [
            {"label": "MPA160 Visual Melting Point Apparatus", "url": "mpa160.html"},
        ],
    },
    "mpa160": {
        "resources": [],
        "related": [
            {"label": "MPA100 OptiMelt Automated Melting Point", "url": "mpa100.html"},
        ],
    },
    "ctc100": {
        "resources": [
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/LDC_CTC_IGC%20rack%20mount.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DCTC100.zip"},
        ],
        "related": [
            {"label": "PTC10 Programmable Temperature Controller", "url": "ptc10.html"},
            {"label": "SIM921 AC Resistance Bridge", "url": "sim921.html"},
            {"label": "SIM922 Diode Temperature Monitor", "url": "sim922.html"},
        ],
    },
    "ptc10": {
        "resources": [],
        "related": [
            {"label": "CTC100 Cryogenic Temperature Controller", "url": "ctc100.html"},
            {"label": "SIM921 AC Resistance Bridge", "url": "sim921.html"},
            {"label": "SIM922 Diode Temperature Monitor", "url": "sim922.html"},
        ],
    },
    "ldc501": {
        "resources": [
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/LDC_CTC_IGC%20rack%20mount.pdf"},
        ],
        "related": [],
    },
    "sim900": {
        "resources": [
            {"label": "Programming Examples", "url": f"{BASE}/downloads/pdfs/applicationnotes/ComSIMs.pdf"},
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Lock-In%20rack%20mount.pdf"},
            {"label": "SIM900 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20SIM900.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DSIM900.zip"},
        ],
        "related": [],
    },
    "sim910": {"resources": [], "related": []},
    "sim918": {"resources": [], "related": []},
    "sim921": {
        "resources": [],
        "related": [
            {"label": "CTC100 Cryogenic Temperature Controller", "url": "ctc100.html"},
            {"label": "PTC10 Programmable Temperature Controller", "url": "ptc10.html"},
        ],
    },
    "sim922": {
        "resources": [],
        "related": [
            {"label": "CTC100 Cryogenic Temperature Controller", "url": "ctc100.html"},
        ],
    },
    "sim928": {"resources": [], "related": []},
    "sim940": {"resources": [], "related": []},
    "sim960": {"resources": [], "related": []},
    "sim985": {"resources": [], "related": []},
    "sim964": {"resources": [], "related": []},
    "sim970": {"resources": [], "related": []},
    "fs725": {
        "resources": [
            {"label": "FS725 Software", "url": f"{BASE}/downloads/programs/RbMon10.exe"},
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DFS725.zip"},
            {"label": "FS725 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20FS725.pdf"},
        ],
        "related": [
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
            {"label": "PRS10 Rubidium Oscillator", "url": "prs10.html"},
            {"label": "FS730 Distribution Amplifier", "url": "fs730.html"},
            {"label": "SG382 RF Signal Generator", "url": "sg382.html"},
        ],
    },
    "prs10": {
        "resources": [
            {"label": "PRS10 Dimensional Dwg.", "url": f"{BASE}/downloads/pdfs/applicationnotes/RBoutline.pdf"},
        ],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
        ],
    },
    "fs740": {
        "resources": [
            {"label": "FS740 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20FS740.pdf"},
        ],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS752 GPS/GNSS Disciplined Oscillator", "url": "fs752.html"},
            {"label": "PRS10 Rubidium Oscillator", "url": "prs10.html"},
        ],
    },
    "fs752": {
        "resources": [],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
        ],
    },
    "sc10": {
        "resources": [],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
        ],
    },
    "fs730": {
        "resources": [],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS710 10 MHz Distribution Amplifier", "url": "fs710.html"},
        ],
    },
    "fs710": {
        "resources": [],
        "related": [
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS730 Frequency Distribution Amplifier", "url": "fs730.html"},
        ],
    },
    "sr540": {
        "resources": [],
        "related": [
            {"label": "SR542 Precision Optical Chopper", "url": "sr542.html"},
            {"label": "SR865A 4 MHz Lock-In Amplifier", "url": "sr865a.html"},
        ],
    },
    "sr542": {
        "resources": [],
        "related": [
            {"label": "SR540 Optical Chopper", "url": "sr540.html"},
            {"label": "SR865A 4 MHz Lock-In Amplifier", "url": "sr865a.html"},
        ],
    },
    "sr470": {
        "resources": [],
        "related": [
            {"label": "SR540 Optical Chopper", "url": "sr540.html"},
            {"label": "SR542 Precision Optical Chopper", "url": "sr542.html"},
        ],
    },
}

count = 0
for slug, data in DATA.items():
    md = PRODUCTS / f"{slug}.md"
    if not md.exists():
        continue
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)", text, re.DOTALL)
    if not m:
        continue

    front = m.group(2)
    body = m.group(4)
    changed = False

    if "resources:" not in front and data.get("resources"):
        res_lines = "\n\nresources:"
        for r in data["resources"]:
            res_lines += f'\n  - label: "{r["label"]}"\n    url: "{r["url"]}"'
        front += res_lines
        changed = True

    if "related:" not in front and data.get("related"):
        rel_lines = "\n\nrelated:"
        for r in data["related"]:
            rel_lines += f'\n  - label: "{r["label"]}"\n    url: "{r["url"]}"'
        front += rel_lines
        changed = True

    if changed:
        md.write_text(m.group(1) + front + m.group(3) + body, encoding="utf-8")
        count += 1
        print(f"  {slug}: updated")
    else:
        print(f"  {slug}: no changes")

print(f"\nUpdated {count} files")
