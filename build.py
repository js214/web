#!/usr/bin/env python3
"""
build.py — Build the site into dist/.

Usage:
    python build.py              # full build
    python build.py sr865a       # rebuild one product by slug
"""

import re
import shutil
import sys
from collections import OrderedDict
from pathlib import Path
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

ROOT           = Path(__file__).parent
PRODUCTS_DIR   = ROOT / "products"
PAGES_DIR      = ROOT / "pages"
IMAGES_DIR     = ROOT / "images"
DIST           = ROOT / "dist"

TAB_ORDER = ["new", "sci", "time", "analytical", "test", "vac"]

TAB_LABELS = [
    ("new",        "New"),
    ("sci",        "Scientific"),
    ("time",       "Time &amp; Frequency"),
    ("analytical", "Analytical"),
    ("test",       "Test &amp; Measurement"),
    ("vac",        "Vacuum"),
]

GROUP_ORDER = {
    "sci": [
        "Lock-In Amplifiers",
        "Preamplifiers",
        "Temperature Controllers",
        "Voltage & Current Sources",
        "Laser Diode Controllers",
        "Optical Instruments",
        "Digital Delay & Pulse Generators",
        "High Voltage Power Supplies",
        "Boxcar Averagers & Photon Counters",
        "SIM Modular Instrument System",
    ],
    "time": [
        "Frequency Standards & Oscillators",
        "Distribution Amplifiers",
        "Frequency Counters",
    ],
    "analytical": ["Analytical Instruments"],
    "test": [
        "RF Signal Generators",
        "Function & Clock Generators",
        "FFT Spectrum Analyzers",
        "Audio Instruments",
        "LCR Meters & Monitors",
    ],
    "vac": [
        "Residual Gas Analyzers",
        "Atmospheric & Process Gas Analyzers",
    ],
}


def process_figures(html: str) -> str:
    """Convert <p><img></p> to <figure> with captions; wrap consecutive figures in fig-grid."""
    def img_to_figure(m):
        img_tag = m.group(1)
        alt_m = re.search(r'alt="([^"]*)"', img_tag)
        caption = alt_m.group(1) if alt_m else ""
        if caption:
            return f'<figure>{img_tag}<figcaption>{caption}</figcaption></figure>'
        return f'<figure>{img_tag}</figure>'

    html = re.sub(r'<p>(<img\b[^>]*>)</p>', img_to_figure, html)

    # Wrap 2+ consecutive <figure> blocks in a grid container.
    # Use negative lookahead so .*? can't backtrack across </figure> boundaries.
    html = re.sub(
        r'((?:<figure>(?:(?!</figure>).)*</figure>\s*){2,})',
        lambda m: '<div class="fig-grid">' + m.group(1).strip() + '</div>',
        html,
        flags=re.DOTALL,
    )
    return html


def parse_md(path: Path) -> dict:
    """Split YAML front matter from Markdown body, return merged dict."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"No front matter found in {path}")
    front = yaml.safe_load(match.group(1))
    body_md = match.group(2).strip()
    body_html = markdown.markdown(body_md, extensions=["extra"])
    body_html = process_figures(body_html)
    front["body_html"] = body_html
    front.setdefault("href", f"products/{front['slug']}.html")
    return front


def organize_by_tab(products: dict) -> OrderedDict:
    """Return OrderedDict: tab_id -> [(group_name, [sorted products])]"""
    buckets: dict[str, dict[str, list]] = {t: {} for t in TAB_ORDER if t != "new"}

    for p in products.values():
        # tabs can be a list (multi-tab product) or single string
        tabs = p.get("tabs") or [p.get("tab", "sci")]
        if isinstance(tabs, str):
            tabs = [tabs]

        # groups can be a dict {tab: group_name} or use the single 'group' field
        groups_map = p.get("groups") or {}
        primary_group = p.get("group", "")

        for tab in tabs:
            if tab == "new":
                continue
            group = groups_map.get(tab, primary_group) if isinstance(groups_map, dict) else primary_group
            buckets.setdefault(tab, {})
            buckets[tab].setdefault(group, [])
            buckets[tab][group].append(p)

    result = OrderedDict()

    # "New" tab: all is_new products sorted by sort field
    new_products = sorted(
        [p for p in products.values() if p.get("is_new")],
        key=lambda p: p.get("sort", 999),
    )
    result["new"] = [("New Products", new_products)]

    for tab in TAB_ORDER:
        if tab == "new":
            continue
        tab_groups = buckets.get(tab, {})
        ordered = []
        defined_order = GROUP_ORDER.get(tab, [])
        for gname in defined_order:
            if gname in tab_groups:
                prods = sorted(tab_groups[gname], key=lambda p: p.get("sort", 999))
                ordered.append((gname, prods))
        # Append any groups not explicitly listed in GROUP_ORDER
        for gname, prods in tab_groups.items():
            if gname not in defined_order:
                ordered.append((gname, sorted(prods, key=lambda p: p.get("sort", 999))))
        result[tab] = ordered

    return result


def copy_dir(src: Path, dst: Path):
    """Copy all files from src into dst (flat — no subdirectories)."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, dst / f.name)
            print(f"  copied: {dst.name}/{f.name}")


def build(slug: str | None = None):
    DIST.mkdir(exist_ok=True)

    # --- Load all product data ---
    all_products = {}
    for md_file in sorted(PRODUCTS_DIR.glob("*.md")):
        data = parse_md(md_file)
        all_products[data["slug"]] = data

    tabs_by_group = organize_by_tab(all_products)

    env = Environment(loader=FileSystemLoader(str(PAGES_DIR)), autoescape=False)

    # --- Copy CSS ---
    for f in sorted(PAGES_DIR.glob("*.css")):
        shutil.copy2(f, DIST / f.name)
        print(f"  copied: {f.name}")

    # --- Asset directories ---
    copy_dir(IMAGES_DIR, DIST / "images")

    # --- Render all *.html.j2 pages (excluding product.html.j2 template) ---
    skip = {"product.html.j2"}
    for j2 in sorted(PAGES_DIR.glob("*.html.j2")):
        if j2.name in skip:
            continue
        out_name = j2.name[:-3]
        tmpl = env.get_template(j2.name)
        html = tmpl.render(
            products=all_products,
            tabs_by_group=tabs_by_group,
            tab_labels=TAB_LABELS,
        )
        (DIST / out_name).write_text(html, encoding="utf-8")
        print(f"  built:  {out_name}")

    # --- Render product pages (all products) ---
    tmpl = env.get_template("product.html.j2")
    prod_dir = DIST / "products"
    prod_dir.mkdir(exist_ok=True)
    files = sorted(PRODUCTS_DIR.glob("*.md"))
    if slug:
        files = [f for f in files if f.stem == slug]
        if not files:
            print(f"No product found for slug: {slug}")
            sys.exit(1)

    for md_file in files:
        data = all_products[md_file.stem]
        out_name = f"{data['slug']}.html"
        html = tmpl.render(**data)
        (prod_dir / out_name).write_text(html, encoding="utf-8")
        print(f"  built:  products/{out_name}")


if __name__ == "__main__":
    slug_arg = sys.argv[1] if len(sys.argv) > 1 else None
    build(slug_arg)
