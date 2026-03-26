#!/usr/bin/env python3
"""Add resources and related sections to product .md files based on scraped data."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTS = ROOT / "products"

# Scraped data: slug -> {resources: [...], related: [...]}
# URLs are converted to full thinksrs.com URLs
BASE = "https://thinksrs.com"

DATA = {
    "perf10": {
        "resources": [
            {"label": "PRS10 Dimensional Dwg.", "url": f"{BASE}/downloads/pdfs/applicationnotes/RBoutline.pdf"},
        ],
        "related": [
            {"label": "FS725 10 MHz Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "PRS10 Rubidium Oscillator", "url": "prs10.html"},
        ],
    },
    "sr715": {
        "resources": [
            {"label": "Ext Bias for Capacitors", "url": f"{BASE}/downloads/pdfs/applicationnotes/LCR%20Bias%20Voltage.pdf"},
            {"label": "SR715 Accuracy", "url": f"{BASE}/downloads/pdfs/other%20stuff/SR715_accur_vs_Z.pdf"},
        ],
        "related": [
            {"label": "SR860 500 kHz Lock-In Amplifier", "url": "sr860.html"},
            {"label": "SR830 DSP Lock-In Amplifier", "url": "sr830.html"},
        ],
        "panels": ["images/instr/sr715720/SR700 MainPic.jpg"],  # only has main pic
    },
    "sr630": {
        "resources": [
            {"label": "Single Rack Mount Kit", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "Double Rack Mount Kit", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
            {"label": "SR630 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20SR630.pdf"},
        ],
        "related": [
            {"label": "PTC10 Programmable Temperature Controller", "url": "ptc10.html"},
        ],
    },
    "sr620": {
        "resources": [
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/SR620%20rack%20mount.pdf"},
            {"label": "SR620 Measurements", "url": f"{BASE}/downloads/pdfs/applicationnotes/SR620_details.pdf"},
            {"label": "SR620 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20SR620.pdf"},
            {"label": "High-Res Measurements", "url": f"{BASE}/downloads/pdfs/other%20stuff/SR620_High_Res_Freq_Meas.pdf"},
        ],
        "related": [
            {"label": "FS752 GPS/GNSS Disciplined Oscillator", "url": "fs752.html"},
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "SR625 Rubidium Frequency Counter", "url": "sr625.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
        ],
    },
    "sr625": {
        "resources": [
            {"label": "SR620 Measurements", "url": f"{BASE}/downloads/pdfs/applicationnotes/SR620_details.pdf"},
        ],
        "related": [
            {"label": "FS752 GPS/GNSS Disciplined Oscillator", "url": "fs752.html"},
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "SR620 Universal Time Interval Counter", "url": "sr620.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
        ],
    },
    "sr250": {
        "resources": [
            {"label": "Signal Recovery with PMTs", "url": f"{BASE}/downloads/pdfs/applicationnotes/SignalRecovery.pdf"},
            {"label": "Signal Enhancement", "url": f"{BASE}/downloads/pdfs/applicationnotes/SignalEnhancement.pdf"},
        ],
        "related": [
            {"label": "DG645 Digital Delay Generator", "url": "dg645.html"},
            {"label": "DG535 Digital Delay Generator", "url": "dg535.html"},
        ],
    },
    "sr400": {
        "resources": [
            {"label": "Signal Recovery with PMTs", "url": f"{BASE}/downloads/pdfs/applicationnotes/SignalRecovery.pdf"},
            {"label": "Signal Enhancement", "url": f"{BASE}/downloads/pdfs/applicationnotes/SignalEnhancement.pdf"},
        ],
        "related": [
            {"label": "PS300 High Voltage Power Supply", "url": "ps300.html"},
            {"label": "SR445A 350 MHz Preamplifier", "url": "sr445a.html"},
            {"label": "SR446 DC to 4 GHz Preamplifier", "url": "sr446.html"},
        ],
    },
    "sg382": {
        "resources": [
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DSG390.zip"},
            {"label": "SG382 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20SG38x.pdf"},
        ],
        "related": [
            {"label": "SG392 Vector Signal Generator", "url": "sg392.html"},
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
            {"label": "PRS10 Rubidium Oscillator", "url": "prs10.html"},
        ],
    },
    "sg392": {
        "resources": [
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DSG390.zip"},
            {"label": "SG392 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20SG39x.pdf"},
        ],
        "related": [
            {"label": "SG382 RF Signal Generator", "url": "sg382.html"},
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "FS740 GPS Time & Frequency Standard", "url": "fs740.html"},
            {"label": "PRS10 Rubidium Oscillator", "url": "prs10.html"},
        ],
    },
    "cg792": {
        "resources": [],
        "related": [
            {"label": "CG635 Synthesized Clock Generator", "url": "cg635.html"},
        ],
    },
    "ds345": {
        "resources": [
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
        ],
        "related": [
            {"label": "DS360 Ultra Low Distortion Function Generator", "url": "ds360.html"},
        ],
    },
    "ds360": {
        "resources": [
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
        ],
        "related": [
            {"label": "DS345 Synthesized Function Generator", "url": "ds345.html"},
            {"label": "SR1 Audio Analyzer", "url": "sr1.html"},
        ],
    },
    "cg635": {
        "resources": [
            {"label": "Single Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Single%20rack%20mnt.pdf"},
            {"label": "Double Rack Mount Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Double%20rack%20mnt.pdf"},
        ],
        "related": [
            {"label": "CG792 Multichannel Clock Generator", "url": "cg792.html"},
            {"label": "FS725 Rubidium Frequency Standard", "url": "fs725.html"},
            {"label": "DG645 Digital Delay Generator", "url": "dg645.html"},
        ],
    },
    "dg645": {
        "resources": [
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Lock-In%20rack%20mount.pdf"},
            {"label": "3D Step File", "url": f"{BASE}/downloads/stp/3DDG645.zip"},
            {"label": "DG645 Volatility Statement", "url": f"{BASE}/downloads/pdfs/other%20stuff/Volatility%20Statement%20DG645.pdf"},
        ],
        "related": [
            {"label": "DG535 Digital Delay/Pulse Generator", "url": "dg535.html"},
            {"label": "DB64 Digital Delay Generator", "url": "db64.html"},
        ],
    },
    "dg535": {
        "resources": [
            {"label": "Rack Mount Kit Dwg.", "url": f"{BASE}/downloads/pdfs/other%20stuff/Platform1%20rack%20mount.pdf"},
        ],
        "related": [
            {"label": "DG645 Digital Delay Generator", "url": "dg645.html"},
            {"label": "DB64 Digital Delay Generator", "url": "db64.html"},
        ],
    },
    "db64": {
        "resources": [],
        "related": [
            {"label": "DG645 Digital Delay Generator", "url": "dg645.html"},
            {"label": "DG535 Digital Delay/Pulse Generator", "url": "dg535.html"},
        ],
    },
    "dc215": {
        "resources": [],
        "related": [
            {"label": "DC205 Voltage Source", "url": "dc205.html"},
            {"label": "CS580 Voltage-Controlled Current Source", "url": "cs580.html"},
        ],
    },
    "cs580": {
        "resources": [],
        "related": [
            {"label": "DC205 Voltage Source", "url": "dc205.html"},
            {"label": "DC215 Voltage/Current Source", "url": "dc215.html"},
            {"label": "SR865A 4 MHz Lock-In Amplifier", "url": "sr865a.html"},
        ],
    },
    "dc205": {
        "resources": [],
        "related": [
            {"label": "DC215 Voltage/Current Source", "url": "dc215.html"},
            {"label": "CS580 Voltage-Controlled Current Source", "url": "cs580.html"},
            {"label": "SR865A 4 MHz Lock-In Amplifier", "url": "sr865a.html"},
        ],
    },
    "ps300": {
        "resources": [],
        "related": [
            {"label": "SR400 Photon Counter", "url": "sr400.html"},
        ],
    },
    "rga120": {
        "resources": [],
        "related": [
            {"label": "RGA Residual Gas Analyzers", "url": "rga.html"},
            {"label": "UGA120 Leak Detector / Gas Analyzer", "url": "uga120.html"},
        ],
    },
    "rga": {
        "resources": [],
        "related": [
            {"label": "RGA120 High-Sensitivity RGA Systems", "url": "rga120.html"},
            {"label": "UGA120 Leak Detector / Gas Analyzer", "url": "uga120.html"},
        ],
    },
    "uga120": {
        "resources": [],
        "related": [
            {"label": "RGA Residual Gas Analyzers", "url": "rga.html"},
            {"label": "RGA120 High-Sensitivity RGA Systems", "url": "rga120.html"},
        ],
    },
}

def add_section(text, section_name, items):
    """Add a YAML section before the --- end marker."""
    if not items:
        return text
    lines = [f"\n{section_name}:"]
    for item in items:
        label = item.get("label", item.get("title", item.get("name", "")))
        url = item["url"]
        lines.append(f'  - label: "{label}"')
        lines.append(f'    url: "{url}"')
    section = "\n".join(lines)
    # Insert before the final ---
    return text.rstrip().rstrip("-").rstrip() + section + "\n---\n"


count = 0
for slug, data in DATA.items():
    md = PRODUCTS / f"{slug}.md"
    if not md.exists():
        print(f"  {slug}: file not found")
        continue
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)", text, re.DOTALL)
    if not m:
        print(f"  {slug}: no frontmatter")
        continue

    front = m.group(2)
    body = m.group(4)
    changed = False

    # Add resources if missing and we have data
    if "resources:" not in front and data.get("resources"):
        res_lines = "\n\nresources:"
        for r in data["resources"]:
            label = r.get("label", r.get("title", r.get("name", "")))
            res_lines += f'\n  - label: "{label}"\n    url: "{r["url"]}"'
        front += res_lines
        changed = True

    # Add related if missing and we have data
    if "related:" not in front and data.get("related"):
        rel_lines = "\n\nrelated:"
        for r in data["related"]:
            label = r.get("label", r.get("title", r.get("name", "")))
            rel_lines += f'\n  - label: "{label}"\n    url: "{r["url"]}"'
        front += rel_lines
        changed = True

    if changed:
        md.write_text(m.group(1) + front + m.group(3) + body, encoding="utf-8")
        count += 1
        print(f"  {slug}: updated")
    else:
        print(f"  {slug}: no changes needed")

print(f"\nUpdated {count} files")
