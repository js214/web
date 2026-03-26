import urllib.request, re, yaml
from pathlib import Path

PRODUCTS_DIR = Path("products")
HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE = "https://thinksrs.com/products/"
SKIP = {"sr865a", "sr830", "rga", "cis100", "fs730"}  # no legacy page found

URL_OVERRIDES = {
    "qms100": "qms.html",
    "sim910": "sim910911.html",
    "sim922": "sim922923.html",
    "sr10":   "sr101112.html",
    "sr470":  "sr470474.html",
    "sr715":  "sr715720.html",
    "uga120": "uga.html",
    "sg382":  "sg380.html",
    "sg392":  "sg390.html",
}

ENTITIES = [
    ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " "), ("&#160;", " "),
    ("&Omega;", "Ω"), ("&radic;", "√"), ("&plusmn;", "±"), ("&deg;", "°"),
    ("&mdash;", "—"), ("&ndash;", "–"), ("&micro;", "μ"), ("&mu;", "μ"),
    ("&times;", "×"), ("&ge;", "≥"), ("&le;", "≤"), ("&Alpha;", "A"),
]

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def strip(s):
    s = re.sub(r"<[^>]+>", " ", s)
    for e, r in ENTITIES:
        s = s.replace(e, r)
    s = re.sub(r"&[a-zA-Z]+;", "", s)
    s = re.sub(r"&#[0-9]+;", "", s)
    return " ".join(s.split()).strip()

def extract(html):
    result = {}
    # Price
    pm = re.search(r'<span class=["\']Price2021["\']>\s*\$([\d,]+)', html)
    if pm:
        result["price"] = "$" + pm.group(1)
    # Bullets (large view only)
    bullets = re.findall(r'<li class=["\']Bullets2021["\']>(.*?)</li>', html, re.DOTALL)
    result["description_bullets"] = [strip(b) for b in bullets if len(strip(b)) > 2]
    # Body text from Features tab
    feat = html.find('id="Features"')
    if feat < 0:
        feat = 0
    texts = re.findall(r'class=["\']Text2021["\']>(.*?)</(?:span|p)>', html[feat:feat+8000], re.DOTALL)
    result["body_texts"] = [strip(t) for t in texts if len(strip(t)) > 40][:2]
    # Spec groups from Specifications tab
    si = html.find('id="Specifications"')
    if si < 0:
        si = max(0, html.find("Specs2021") - 3000)
    spec_html = html[si:si+25000] if si >= 0 else ""
    groups = []
    for part in re.split(r"TextTITLESb2021", spec_html)[1:]:
        gm = re.search(r">(.*?)<", part)
        if not gm:
            continue
        gname = strip(gm.group(1))
        if not gname:
            continue
        end = part.find("TextTITLESb2021")
        section = part[:end] if end >= 0 else part
        rows = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", section, re.DOTALL):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)
            if len(cells) >= 2 and 'colspan="2"' not in cells[0] and "colspan='2'" not in cells[0]:
                k, v = strip(cells[0]), strip(cells[1])
                if k and v and len(k) > 1:
                    rows.append([k, v])
        if rows:
            groups.append({"name": gname, "rows": rows})
    # Fallback: flat table (no TextTITLESb2021 headers) — put everything in one group
    if not groups and "Specs2021" in spec_html:
        rows = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", spec_html, re.DOTALL):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)
            if len(cells) >= 2 and 'colspan="2"' not in cells[0] and "colspan='2'" not in cells[0]:
                k, v = strip(cells[0]), strip(cells[1])
                if k and v and len(k) > 1 and k != v:
                    rows.append([k, v])
        if rows:
            groups.append({"name": "Specifications", "rows": rows})
    result["spec_groups"] = groups
    return result

def needs_scraping(f):
    return "quick_specs:" not in f.read_text(encoding="utf-8")

def update_md(md_file, data, body_text):
    text = md_file.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return False
    additions = {}
    if data.get("price"):
        additions["price"] = data["price"]
        additions["price_note"] = "FOB Sunnyvale, CA"
    if data.get("description_bullets"):
        additions["description_bullets"] = data["description_bullets"]
    if data.get("spec_groups"):
        qs = []
        for grp in data["spec_groups"][:3]:
            for row in grp["rows"]:
                if len(qs) < 6:
                    qs.append({"label": row[0], "value": row[1]})
        additions["quick_specs"] = qs
        additions["spec_groups"] = data["spec_groups"]
    if not additions:
        return False
    insert = "\n" + yaml.dump(additions, default_flow_style=False, allow_unicode=True).rstrip()
    end = m.end()
    new_fm = text[:end - 3] + insert + "\n---"
    body = text[end:]
    if not body.strip() and body_text:
        body = "\n\n" + body_text + "\n"
    md_file.write_text(new_fm + body, encoding="utf-8")
    return True

files = [f for f in sorted(PRODUCTS_DIR.glob("*.md")) if f.stem not in SKIP and needs_scraping(f)]
print(f"Scraping {len(files)} products...")
for md_file in files:
    slug = md_file.stem
    url = BASE + URL_OVERRIDES.get(slug, slug + ".html")
    try:
        html = fetch(url)
        data = extract(html)
        body_text = data["body_texts"][0] if data.get("body_texts") else ""
        if update_md(md_file, data, body_text):
            ng = len(data.get("spec_groups") or [])
            print(f"  OK: {slug} ({ng} groups, price={data.get('price', '?')})")
        else:
            print(f"  no data: {slug}")
    except Exception as e:
        print(f"  ERR: {slug}: {e}")
print("Done.")
