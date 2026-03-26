#!/usr/bin/env python3
"""
Scrape product data from thinksrs.com legacy pages and update local .md files.
"""

import urllib.request
import urllib.error
import re
import time
import sys
from pathlib import Path
from html.parser import HTMLParser

# ── configuration ──────────────────────────────────────────────────────────────
PRODUCTS_DIR = Path(r"C:\Users\Jkastelic\Documents\projects\web\products")
SKIP_SLUGS = {"sr865a", "sr830", "rga"}  # already complete

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# ── tiny HTML → text helpers ───────────────────────────────────────────────────

def fetch(url, timeout=20):
    """Fetch URL, return bytes or None on error."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:
        print(f"  FETCH ERROR {url}: {e}")
        return None


def strip_tags(html_frag):
    """Remove HTML tags, collapse whitespace, decode common entities."""
    # remove sup tags but keep their content with superscript unicode
    sup_map = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵',
               '6':'⁶','7':'⁷','8':'⁸','9':'⁹','-':'⁻','+':'⁺',
               'n':'ⁿ','a':'ᵃ','b':'ᵇ','c':'ᶜ','d':'ᵈ','e':'ᵉ',
               'f':'ᶠ','g':'ᵍ','h':'ʰ','i':'ⁱ','j':'ʲ','k':'ᵏ',
               'l':'ˡ','m':'ᵐ','o':'ᵒ','p':'ᵖ','r':'ʳ','s':'ˢ',
               't':'ᵗ','u':'ᵘ','v':'ᵛ','w':'ʷ','x':'ˣ','y':'ʸ','z':'ᶻ'}
    def convert_sup(m):
        inner = strip_tags(m.group(1))
        return ''.join(sup_map.get(c, c) for c in inner)
    html_frag = re.sub(r'<sup[^>]*>(.*?)</sup>', convert_sup, html_frag,
                       flags=re.IGNORECASE | re.DOTALL)
    # remove all remaining tags
    text = re.sub(r'<[^>]+>', '', html_frag)
    # decode entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&') \
               .replace('&lt;', '<').replace('&gt;', '>') \
               .replace('&le;', '≤').replace('&ge;', '≥') \
               .replace('&plusmn;', '±').replace('&times;', '×') \
               .replace('&deg;', '°').replace('&mu;', 'μ') \
               .replace('&#956;', 'μ').replace('&#8486;', 'Ω') \
               .replace('&Omega;', 'Ω').replace('&omega;', 'ω') \
               .replace('&#960;', 'π').replace('&pi;', 'π') \
               .replace('&#176;', '°').replace('&#177;', '±') \
               .replace('&#215;', '×').replace('&#247;', '÷') \
               .replace('&alpha;', 'α').replace('&beta;', 'β') \
               .replace('&gamma;', 'γ').replace('&Delta;', 'Δ') \
               .replace('&delta;', 'δ').replace('&sigma;', 'σ') \
               .replace('&tau;', 'τ').replace('&lambda;', 'λ') \
               .replace('&#8211;', '–').replace('&#8212;', '—') \
               .replace('&#8722;', '−').replace('&minus;', '−') \
               .replace('&#8730;', '√').replace('&radic;', '√') \
               .replace('&frac12;', '½').replace('&frac14;', '¼') \
               .replace('&#8486;', 'Ω').replace('&hellip;', '…') \
               .replace('&#8201;', ' ').replace('&#8202;', ' ') \
               .replace('&#160;', ' ').replace('&thinsp;', ' ') \
               .replace('&#xb5;', 'μ').replace('&#xB5;', 'μ') \
               .replace('&lsquo;', "'").replace('&rsquo;', "'") \
               .replace('&ldquo;', '"').replace('&rdquo;', '"') \
               .replace('&#8220;', '"').replace('&#8221;', '"') \
               .replace('&#8216;', "'").replace('&#8217;', "'") \
               .replace('&ndash;', '–').replace('&mdash;', '—') \
               .replace('&copy;', '©').replace('&reg;', '®')
    # numeric hex entities
    text = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), text)
    # numeric decimal entities
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    return re.sub(r'\s+', ' ', text).strip()


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


# ── YAML helpers ───────────────────────────────────────────────────────────────

def yaml_str(s):
    """Quote a string for YAML if needed."""
    s = str(s)
    if not s:
        return '""'
    need_quote = any(c in s for c in ':{}[]|>&*!,%@`\'\"') or \
                 s.startswith('-') or s.startswith('#') or \
                 s != s.strip() or '\n' in s
    if need_quote:
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return s


def render_quick_specs(specs):
    lines = ["quick_specs:"]
    for sp in specs:
        lines.append(f"  - label: {yaml_str(sp['label'])}")
        lines.append(f"    value: {yaml_str(sp['value'])}")
    return "\n".join(lines)


def render_description(title, bullets):
    lines = [f"description_title: {yaml_str(title)}", "description_bullets:"]
    for b in bullets:
        lines.append(f"  - {yaml_str(b)}")
    return "\n".join(lines)


def render_spec_groups(groups):
    lines = ["spec_groups:"]
    for g in groups:
        lines.append(f"  - name: {yaml_str(g['name'])}")
        lines.append("    rows:")
        for row in g["rows"]:
            lbl = yaml_str(row[0])
            val = yaml_str(row[1])
            lines.append(f"      - [{lbl}, {val}]")
    return "\n".join(lines)


def render_related(related):
    if not related:
        return ""
    lines = ["related:"]
    for r in related:
        lines.append(f"  - label: {yaml_str(r['label'])}")
        lines.append(f"    url: {yaml_str(r['url'])}")
    return "\n".join(lines)


# ── HTML parsing helpers ───────────────────────────────────────────────────────

def find_price(html):
    """Extract first price-like string from page."""
    # Look for price in dollar amounts
    prices = re.findall(r'\$[\d,]+(?:\.\d+)?', html)
    if prices:
        # Return the most plausible price (skip very small amounts like $1 or $0)
        for p in prices:
            val = int(re.sub(r'[^\d]', '', p))
            if val >= 100:
                return p
    return None


def find_price_in_tables(html):
    """Look for pricing tables on the page."""
    # Find tables that have price-like content
    price_pattern = re.compile(r'<tr[^>]*>.*?\$[\d,]+.*?</tr>', re.DOTALL | re.IGNORECASE)
    rows = price_pattern.findall(html)
    if rows:
        # Get first cell with dollar sign
        for row in rows:
            m = re.search(r'\$([\d,]+)', row)
            if m:
                val = int(m.group(1).replace(',', ''))
                if val >= 100:
                    return f"${m.group(1)}"
    return None


def extract_spec_tables(html):
    """Extract all spec tables from the page."""
    groups = []

    # Find all tables
    table_pattern = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    tables = table_pattern.findall(html)

    for table_html in tables:
        rows = []
        row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
        cell_pattern = re.compile(r'<t[dh][^>]*>(.*?)</t[dh]>', re.DOTALL | re.IGNORECASE)

        for row_html in row_pattern.findall(table_html):
            cells = [strip_tags(c) for c in cell_pattern.findall(row_html)]
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                rows.append(cells)

        if rows:
            # Check if this looks like a spec table (not navigation or price)
            # Spec tables typically have 2 columns: label, value
            two_col_rows = [r for r in rows if len(r) == 2]
            if len(two_col_rows) >= 3:
                groups.append({"rows": rows, "name": ""})

    return groups


def extract_features_list(html):
    """Extract bullet points / features from the page."""
    bullets = []

    # Look for <ul> lists near "features" or "highlights" headings
    # Or just main feature bullets
    ul_pattern = re.compile(r'<ul[^>]*>(.*?)</ul>', re.DOTALL | re.IGNORECASE)
    li_pattern = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)

    for ul_html in ul_pattern.findall(html):
        items = [strip_tags(li) for li in li_pattern.findall(ul_html)]
        items = [i for i in items if i and len(i) > 5 and len(i) < 200]
        if len(items) >= 3:
            bullets.extend(items)
            if len(bullets) >= 12:
                break

    return bullets[:12]


def get_section_heading(html, position):
    """Find the nearest heading before position in HTML."""
    # Look backwards for h2, h3, h4 tags
    chunk = html[:position]
    headings = list(re.finditer(r'<h[2-4][^>]*>(.*?)</h[2-4]>', chunk, re.DOTALL | re.IGNORECASE))
    if headings:
        return strip_tags(headings[-1].group(1))
    return ""


# ── Main page parser ───────────────────────────────────────────────────────────

def parse_thinksrs_page(html_bytes, slug):
    """Parse a thinksrs.com product page and extract structured data."""
    try:
        html = html_bytes.decode('utf-8', errors='replace')
    except Exception:
        html = str(html_bytes)

    result = {
        "price": None,
        "quick_specs": [],
        "description_title": "",
        "description_bullets": [],
        "spec_groups": [],
        "related": [],
        "body_text": "",
    }

    # ── Price ──────────────────────────────────────────────────────────────────
    # Try pricing table first
    price = find_price_in_tables(html)
    if not price:
        price = find_price(html)
    result["price"] = price

    # ── Description bullets ────────────────────────────────────────────────────
    bullets = []

    # Strategy 1: Look for a "Features" or "Highlights" section
    features_pattern = re.compile(
        r'(?:features|highlights|overview|key features)[^<]*</(?:h[1-6]|strong|b|p)[^>]*>\s*<ul[^>]*>(.*?)</ul>',
        re.DOTALL | re.IGNORECASE
    )
    m = features_pattern.search(html)
    if m:
        li_pat = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)
        bullets = [strip_tags(li) for li in li_pat.findall(m.group(1))]
        bullets = [b for b in bullets if b and 5 < len(b) < 250]

    # Strategy 2: Find the largest <ul> with meaningful items
    if not bullets:
        ul_pat = re.compile(r'<ul[^>]*>(.*?)</ul>', re.DOTALL | re.IGNORECASE)
        li_pat = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)
        best_ul = []
        for ul_m in ul_pat.finditer(html):
            items = [strip_tags(li) for li in li_pat.findall(ul_m.group(1))]
            items = [i for i in items if i and 10 < len(i) < 250
                     and not i.lower().startswith('home')
                     and not i.lower().startswith('product')
                     and '$' not in i]
            if len(items) > len(best_ul):
                best_ul = items
        bullets = best_ul[:12]

    result["description_bullets"] = bullets

    # ── Description title ──────────────────────────────────────────────────────
    # Look for h1, h2 that seems like product description title
    h_pat = re.compile(r'<h[12][^>]*>(.*?)</h[12]>', re.DOTALL | re.IGNORECASE)
    for m in h_pat.finditer(html):
        t = strip_tags(m.group(1))
        if t and len(t) > 5 and slug.upper() not in t.upper() and 'SRS' not in t:
            # Skip navigation-like headings
            if not any(nav in t.lower() for nav in ['home', 'product', 'contact', 'support']):
                result["description_title"] = t[:100]
                break

    if not result["description_title"] and bullets:
        result["description_title"] = f"Key Features"

    # ── Spec tables ────────────────────────────────────────────────────────────
    # Find all tables - look for spec-like tables
    # Try to find tables preceded by headings
    spec_groups = []

    # Pattern: heading then table
    section_pat = re.compile(
        r'<(?:h[2-5]|strong|b)[^>]*>(.*?)</(?:h[2-5]|strong|b)>\s*(?:<[^>]+>\s*)*<table[^>]*>(.*?)</table>',
        re.DOTALL | re.IGNORECASE
    )

    for sm in section_pat.finditer(html):
        heading = strip_tags(sm.group(1))
        table_html = sm.group(2)

        # Skip navigation/price tables
        if any(skip in heading.lower() for skip in ['order', 'price', 'accessory', 'nav', 'related']):
            continue

        rows = []
        row_pat = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
        cell_pat = re.compile(r'<t[dh][^>]*>(.*?)</t[dh]>', re.DOTALL | re.IGNORECASE)

        for row_html in row_pat.findall(table_html):
            cells = [strip_tags(c) for c in cell_pat.findall(row_html)]
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                rows.append([cells[0], cells[1]])

        if rows and len(rows) >= 2:
            spec_groups.append({"name": heading[:80], "rows": rows})

    # Fallback: find all tables with 2+ rows and 2 columns
    if not spec_groups:
        table_pat = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
        row_pat = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
        cell_pat = re.compile(r'<t[dh][^>]*>(.*?)</t[dh]>', re.DOTALL | re.IGNORECASE)

        for tm in table_pat.finditer(html):
            table_html = tm.group(1)
            rows = []
            for row_html in row_pat.findall(table_html):
                cells = [strip_tags(c) for c in cell_pat.findall(row_html)]
                cells = [c for c in cells if c]
                if len(cells) >= 2:
                    rows.append([cells[0], cells[1]])

            if len(rows) >= 3:
                # Check it's spec-like: not all rows have dollar signs
                dollar_rows = sum(1 for r in rows if '$' in r[1])
                if dollar_rows < len(rows) // 2:
                    # Find heading before this table
                    pos = tm.start()
                    heading = get_section_heading(html, pos) or "Specifications"
                    spec_groups.append({"name": heading[:80], "rows": rows})

    result["spec_groups"] = spec_groups

    # ── Quick specs (derive from spec groups or parse dedicated section) ───────
    # Look for a quick specs / key specs section
    quick = []

    # Strategy: look for definition lists or small tables near top of page
    dl_pat = re.compile(r'<dl[^>]*>(.*?)</dl>', re.DOTALL | re.IGNORECASE)
    dt_pat = re.compile(r'<dt[^>]*>(.*?)</dt>', re.DOTALL | re.IGNORECASE)
    dd_pat = re.compile(r'<dd[^>]*>(.*?)</dd>', re.DOTALL | re.IGNORECASE)

    for dl_m in dl_pat.finditer(html):
        dl_html = dl_m.group(1)
        dts = [strip_tags(t) for t in dt_pat.findall(dl_html)]
        dds = [strip_tags(d) for d in dd_pat.findall(dl_html)]
        if dts and dds and len(dts) == len(dds):
            for dt, dd in zip(dts, dds):
                if dt and dd:
                    quick.append({"label": dt, "value": dd})
            if quick:
                break

    # If no DL, derive quick specs from first spec group
    if not quick and spec_groups:
        rows = spec_groups[0]["rows"]
        for row in rows[:8]:
            if len(row) >= 2 and row[0] and row[1]:
                quick.append({"label": row[0], "value": row[1]})

    # If still nothing, derive from bullets
    if not quick and bullets:
        for b in bullets[:6]:
            # Try to split "Label: value" or "Label — value"
            for sep in [':', '—', '-', '–']:
                if sep in b:
                    parts = b.split(sep, 1)
                    if len(parts[0]) < 40 and len(parts[1].strip()) > 0:
                        quick.append({"label": parts[0].strip(), "value": parts[1].strip()})
                        break

    result["quick_specs"] = quick[:8]

    # ── Related products ───────────────────────────────────────────────────────
    related = []
    # Look for "related" / "see also" sections with links
    related_pat = re.compile(
        r'(?:related|see also|accessories)[^<]*</[^>]+>\s*(.*?)</(?:div|section|ul)',
        re.DOTALL | re.IGNORECASE
    )
    link_pat = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)

    for rm in related_pat.finditer(html):
        for lm in link_pat.finditer(rm.group(1)):
            url = lm.group(1)
            label = strip_tags(lm.group(2))
            if label and 'thinksrs.com' in url or url.startswith('/products'):
                related.append({"label": label, "url": url})
        if related:
            break

    result["related"] = related[:6]

    # ── Body text ──────────────────────────────────────────────────────────────
    # Extract first meaningful paragraph(s)
    para_pat = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
    paras = []
    for pm in para_pat.finditer(html):
        text = strip_tags(pm.group(1))
        if len(text) > 80 and len(text) < 1000:
            # Skip navigation/copyright paragraphs
            if not any(skip in text.lower() for skip in
                       ['copyright', 'all rights', 'privacy', 'contact us', 'sunnyvale']):
                paras.append(text)
        if len(paras) >= 2:
            break

    result["body_text"] = "\n\n".join(paras)

    return result


# ── File update ────────────────────────────────────────────────────────────────

def read_md(path):
    """Read .md file, return (frontmatter_str, body_str)."""
    content = path.read_text(encoding='utf-8')
    # Split on ---
    parts = content.split('---')
    if len(parts) >= 3:
        # parts[0] is empty, parts[1] is frontmatter, parts[2+] is body
        fm = parts[1]
        body = '---'.join(parts[2:])
        return fm, body
    return content, ""


def get_frontmatter_value(fm, key):
    """Get a simple scalar value from frontmatter."""
    m = re.search(rf'^{key}:\s*(.+)$', fm, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def update_md(path, data, slug):
    """Update a .md file with scraped data."""
    fm, body = read_md(path)

    # Build new fields
    new_fields = []

    # Price
    if data.get("price"):
        price_str = data["price"]
        new_fields.append(f'price: "{price_str}"')
        new_fields.append('price_note: "FOB Sunnyvale, CA"')

    # Quick specs
    if data.get("quick_specs"):
        new_fields.append(render_quick_specs(data["quick_specs"]))

    # Description
    if data.get("description_title") or data.get("description_bullets"):
        title = data.get("description_title") or f"{slug.upper()} Features"
        bullets = data.get("description_bullets") or []
        if bullets:
            new_fields.append(render_description(title, bullets))

    # Spec groups
    if data.get("spec_groups"):
        new_fields.append(render_spec_groups(data["spec_groups"]))

    # Related
    if data.get("related"):
        new_fields.append(render_related(data["related"]))

    if not new_fields:
        print(f"  SKIP (no data extracted): {slug}")
        return False

    # Append new fields to frontmatter
    fm_stripped = fm.rstrip()
    new_fm = fm_stripped + "\n\n" + "\n".join(new_fields) + "\n"

    # Body text
    body_stripped = body.strip()
    if not body_stripped and data.get("body_text"):
        new_body = "\n\n" + data["body_text"] + "\n"
    else:
        new_body = "\n" + body_stripped + "\n" if body_stripped else "\n"

    new_content = "---" + new_fm + "---" + new_body
    path.write_text(new_content, encoding='utf-8')
    return True


# ── Per-product URL resolution ─────────────────────────────────────────────────

SLUG_URL_OVERRIDES = {
    # Some products use a shared page
    "sg392": "https://thinksrs.com/products/sg380.html",
    "rga120": "https://thinksrs.com/products/rga.html",
    "uga120": "https://thinksrs.com/products/uga.html",
    "ugapm": "https://thinksrs.com/products/uga.html",
    "mpa100": "https://thinksrs.com/products/mpa.html",
    "mpa160": "https://thinksrs.com/products/mpa.html",
    "sim910": "https://thinksrs.com/products/sim900.html",
    "sim918": "https://thinksrs.com/products/sim900.html",
    "sim921": "https://thinksrs.com/products/sim900.html",
    "sim922": "https://thinksrs.com/products/sim900.html",
    "sim928": "https://thinksrs.com/products/sim900.html",
    "sim940": "https://thinksrs.com/products/sim900.html",
    "sim960": "https://thinksrs.com/products/sim900.html",
    "sim964": "https://thinksrs.com/products/sim900.html",
    "sim970": "https://thinksrs.com/products/sim900.html",
    "sim985": "https://thinksrs.com/products/sim900.html",
    "sr10": "https://thinksrs.com/products/sr10.html",
    "sr2124": "https://thinksrs.com/products/sr2124.html",
    "sr250": "https://thinksrs.com/products/sr250.html",
    "db64": "https://thinksrs.com/products/db64.html",
    "perf10": "https://thinksrs.com/products/perf10.html",
    "cis100": "https://thinksrs.com/products/cis100.html",
    "nl100": "https://thinksrs.com/products/nl100.html",
    "ec301": "https://thinksrs.com/products/ec301.html",
    "fs710": "https://thinksrs.com/products/fs710.html",
    "fs725": "https://thinksrs.com/products/fs725.html",
    "fs730": "https://thinksrs.com/products/fs730.html",
    "fs740": "https://thinksrs.com/products/fs740.html",
    "fs752": "https://thinksrs.com/products/fs752.html",
    "sc10": "https://thinksrs.com/products/sc10.html",
    "prs10": "https://thinksrs.com/products/prs10.html",
    "ptc10": "https://thinksrs.com/products/ptc10.html",
    "qcm200": "https://thinksrs.com/products/qcm200.html",
    "qms100": "https://thinksrs.com/products/qms100.html",
}


def get_legacy_url(slug, fm):
    """Determine the legacy thinksrs.com URL for a product."""
    # Check overrides first
    if slug in SLUG_URL_OVERRIDES:
        return SLUG_URL_OVERRIDES[slug]

    # Check frontmatter href
    href = get_frontmatter_value(fm, "href")
    if href and href.startswith("http"):
        return href

    # Default pattern
    return f"https://thinksrs.com/products/{slug}.html"


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    md_files = sorted(PRODUCTS_DIR.glob("*.md"))

    todo = []
    for path in md_files:
        slug = path.stem
        if slug in SKIP_SLUGS:
            continue
        content = path.read_text(encoding='utf-8')
        if 'quick_specs' in content:
            print(f"  DONE (already has quick_specs): {slug}")
            continue
        todo.append(path)

    print(f"\nFiles to process: {len(todo)}\n")

    # Track already-fetched URLs to avoid re-fetching shared pages
    fetched_cache = {}

    for path in todo:
        slug = path.stem
        fm, body = read_md(path)
        url = get_legacy_url(slug, fm)

        print(f"Processing: {slug} -> {url}")

        # Fetch (use cache for shared pages)
        if url in fetched_cache:
            html_bytes = fetched_cache[url]
        else:
            html_bytes = fetch(url)
            fetched_cache[url] = html_bytes
            time.sleep(0.5)  # be polite

        if not html_bytes:
            print(f"  SKIP (fetch failed): {slug}")
            continue

        # Parse
        try:
            data = parse_thinksrs_page(html_bytes, slug)
        except Exception as e:
            print(f"  SKIP (parse error): {slug} — {e}")
            import traceback
            traceback.print_exc()
            continue

        # Check we got something useful
        has_data = (data.get("quick_specs") or data.get("spec_groups") or
                    data.get("description_bullets"))
        if not has_data:
            print(f"  SKIP (no useful data): {slug}")
            continue

        # Update file
        try:
            updated = update_md(path, data, slug)
            if updated:
                print(f"  Updated: {slug}")
            else:
                print(f"  SKIP (no fields written): {slug}")
        except Exception as e:
            print(f"  ERROR updating {slug}: {e}")
            import traceback
            traceback.print_exc()

    print("\nDone.")


if __name__ == "__main__":
    main()
