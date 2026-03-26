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
CATALOG_ORDER  = ROOT / "pages" / "catalog_order.yaml"

TAB_LABELS = [
    ("new",         "New"),
    ("detect",      "Detect"),
    ("generate",    "Generate"),
    ("analyze",     "Analyze"),
    ("control",     "Control"),
    ("synchronize", "Synchronize"),
]


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


def validate_hero_density(data: dict):
    """Raise if hero text is too sparse or too dense to align price/buy with panel thumbnails."""
    bullets = data.get("description_bullets") or []
    desc = data.get("tile_desc") or ""
    bullet_lines = len(bullets)
    desc_lines = max(1, len(desc) // 60 + (1 if len(desc) % 60 else 0)) if desc else 0
    total_lines = bullet_lines + desc_lines
    slug = data.get("slug", "?")
    if total_lines < 3:
        raise ValueError(
            f"{slug}: hero text too sparse ({total_lines} estimated lines) — "
            f"add more bullets or a longer tile_desc so the layout doesn't collapse."
        )
    if total_lines > 18:
        raise ValueError(
            f"{slug}: hero text too dense ({total_lines} estimated lines) — "
            f"reduce bullets or shorten tile_desc so the main image isn't squeezed out."
        )


def organize_by_tab(products: dict, catalog_order: dict) -> OrderedDict:
    """Return OrderedDict: tab_id -> [(group_name, [products])] using catalog_order.yaml."""
    result = OrderedDict()
    seen_slugs = set()

    for tab_id, groups in catalog_order.items():
        tab_groups = []
        for group_name, slugs in groups.items():
            prods = []
            for slug in slugs:
                if slug in products:
                    prods.append(products[slug])
                    seen_slugs.add(slug)
                else:
                    print(f"  warning: {slug} in catalog_order.yaml but no .md file found")
            if prods:
                tab_groups.append((group_name, prods))
        result[tab_id] = tab_groups

    # Warn about products not in catalog_order
    for slug in products:
        if slug not in seen_slugs:
            print(f"  warning: {slug}.md exists but is not listed in catalog_order.yaml")

    return result


def copy_dir(src: Path, dst: Path):
    """Copy all files from src into dst (flat — no subdirectories)."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file() and f.suffix != '.bak':
            shutil.copy2(f, dst / f.name)
            print(f"  copied: {dst.name}/{f.name}")


def build(slug: str | None = None):
    DIST.mkdir(exist_ok=True)

    # --- Load all product data ---
    all_products = {}
    for md_file in sorted(PRODUCTS_DIR.glob("*.md")):
        data = parse_md(md_file)
        all_products[data["slug"]] = data

    catalog_order = yaml.safe_load(CATALOG_ORDER.read_text(encoding="utf-8"))
    tabs_by_group = organize_by_tab(all_products, catalog_order)

    # Build slug -> (primary_tab, group_name) from catalog_order (skip "new" tab)
    slug_placement = {}
    for tab_id, groups in catalog_order.items():
        if tab_id == "new":
            continue
        for group_name, slugs in groups.items():
            for s in slugs:
                if s not in slug_placement:
                    slug_placement[s] = (tab_id, group_name)

    def slugify(s):
        s = s.lower()
        s = re.sub(r'[^a-z0-9]+', '-', s)
        return s.strip('-')

    env = Environment(loader=FileSystemLoader(str(PAGES_DIR)), autoescape=False)
    env.filters['slugify'] = slugify

    # --- Copy CSS ---
    for f in sorted(PAGES_DIR.glob("*.css")):
        shutil.copy2(f, DIST / f.name)
        print(f"  copied: {f.name}")

    # --- Asset directories ---
    copy_dir(IMAGES_DIR, DIST / "images")

    # --- Instrument images (recursive) ---
    instr_src = IMAGES_DIR / "instr"
    if instr_src.exists():
        instr_dst = DIST / "images" / "instr"
        for f in instr_src.rglob("*"):
            if f.is_file() and f.suffix != '.bak':
                rel = f.relative_to(instr_src)
                dest = instr_dst / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                print(f"  copied: images/instr/{rel}")

    # --- PDFs (datasheets, manuals, app_notes) ---
    for dirname in ("datasheets", "manuals", "app_notes"):
        src = ROOT / dirname
        if src.exists():
            dst = DIST / dirname
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(src)
                    dest = dst / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest)
                    print(f"  copied: {dirname}/{rel}")

    # --- Render all *.html.j2 pages (excluding product.html.j2 template) ---
    skip = {"product.html.j2"}
    for j2 in sorted(PAGES_DIR.glob("*.html.j2")):
        if j2.name in skip:
            continue
        out_name = j2.name[:-3]
        tmpl = env.get_template(j2.name)
        # Collect new and discontinued slugs
        new_slugs = set()
        for group_slugs in catalog_order.get("new", {}).values():
            new_slugs.update(group_slugs)
        discontinued_slugs = {s for s, p in all_products.items() if p.get("discontinued")}
        html = tmpl.render(
            products=all_products,
            tabs_by_group=tabs_by_group,
            tab_labels=TAB_LABELS,
            new_slugs=new_slugs,
            discontinued_slugs=discontinued_slugs,
            slug_placement=slug_placement,
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
        validate_hero_density(data)
        # Inject tab/group from catalog_order (overrides any .md fields)
        placement = slug_placement.get(data["slug"])
        if placement:
            data["primary_tab"] = placement[0]
            data["group_display"] = placement[1]
        data["tab_labels"] = TAB_LABELS
        out_name = f"{data['slug']}.html"
        html = tmpl.render(**data)
        (prod_dir / out_name).write_text(html, encoding="utf-8")
        print(f"  built:  products/{out_name}")


if __name__ == "__main__":
    slug_arg = sys.argv[1] if len(sys.argv) > 1 else None
    build(slug_arg)
