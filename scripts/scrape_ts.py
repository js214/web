
import urllib.request, re
from pathlib import Path

products_dir = Path("products")

PAGES = [
    ("bga244sup.html", ["bga244"]),
    ("cg635sup.html", ["cg635"]),
    ("cg792sup.html", ["cg792"]),
    ("cs580sup.html", ["cs580"]),
    ("ctc100sup.html", ["ctc100"]),
    ("dc205sup.html", ["dc205"]),
    ("dc215sup.html", ["dc215"]),
    ("dg535sup.html", ["dg535"]),
    ("dg645sup.html", ["dg645"]),
    ("ds345sup.html", ["ds345"]),
    ("ds360sup.html", ["ds360"]),
    ("fs725sup.html", ["fs725"]),
    ("fs740sup.html", ["fs740"]),
    ("ldc500sup.html", ["ldc501"]),
    ("mpasup.html", ["mpa100"]),
    ("prs10sup.html", ["prs10"]),
    ("ps300sup.html", ["ps300"]),
    ("ptc10sup.html", ["ptc10"]),
    ("qcm200sup.html", ["qcm200"]),
    ("qmssup.html", ["qms100"]),
    ("rgasup.html", ["rga"]),
    ("rga120sup.html", ["rga120"]),
    ("sg3xxsup.html", ["sg382", "sg392"]),
    ("sim900sup.html", ["sim900"]),
    ("sim921sup.html", ["sim921"]),
    ("sim928sup.html", ["sim928"]),
    ("sim960sup.html", ["sim960"]),
    ("sr1sup.html", ["sr1"]),
    ("sr1242124sup.html", ["sr2124"]),
    ("sr250sup.html", ["sr250"]),
    ("sr400sup.html", ["sr400"]),
    ("sr470474sup.html", ["sr470"]),
    ("sr510sup.html", ["sr510"]),
    ("sr542sup.html", ["sr542"]),
    ("sr560sup.html", ["sr560"]),
    ("sr570sup.html", ["sr570"]),
    ("sr620sup.html", ["sr620"]),
    ("sr630sup.html", ["sr630"]),
    ("sr715720sup.html", ["sr715"]),
    ("sr770sup.html", ["sr770"]),
    ("sr78xsup.html", ["sr780"]),
    ("sr830sup.html", ["sr830"]),
    ("sr844sup.html", ["sr844"]),
    ("sr850sup.html", ["sr850"]),
    ("sr86xsup.html", ["sr860", "sr865a"]),
    ("ugasup.html", ["uga120"]),
]

BASE = "https://www.thinksrs.com/support/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    for ent, rep in [("&amp;","&"),("&lt;","<"),("&gt;",">"),("&nbsp;"," "),("&#160;"," ")]:
        s = s.replace(ent, rep)
    s = re.sub(r"&[a-z]+;", "", s)
    s = re.sub(r"&#\d+;", "", s)
    return " ".join(s.split()).strip()

def extract_qa(html):
    idx = html.lower().find("troubleshooting guide")
    if idx < 0:
        idx = 0
    html = html[idx:]
    parts = re.split(r"<p class=.ProdPgTITLESb2021.>", html)
    pairs = []
    for part in parts[1:]:
        q_match = re.match(r"(.*?)</p>", part, re.DOTALL)
        if not q_match:
            continue
        q = strip_tags(q_match.group(1))
        q = re.sub(r"^\d+\)\s*", "", q)
        answer_parts = re.findall(r"<p class=.Text2021.>(.*?)</p>", part, re.DOTALL)
        a = " ".join(strip_tags(ap) for ap in answer_parts if strip_tags(ap))
        if len(q) > 5 and len(a) > 5:
            pairs.append((q[:300], a[:800]))
    return pairs

def yaml_escape(s):
    s = s.replace(chr(92), chr(92)+chr(92))
    s = s.replace(chr(34), chr(92)+chr(34))
    return s

def add_troubleshooting(md_file, pairs):
    text = md_file.read_text(encoding="utf-8")
    if "troubleshooting:" in text:
        return False
    m = re.match(r"^(---\n.*?\n---)", text, re.DOTALL)
    if not m:
        return False
    frontmatter = text[:m.end()]
    body = text[m.end():]
    lines = ["troubleshooting:"]
    for q, a in pairs:
        lines.append("  - q: " + chr(34) + yaml_escape(q) + chr(34))
        lines.append("    a: " + chr(34) + yaml_escape(a) + chr(34))
    insert = "\n" + "\n".join(lines)
    new_fm = frontmatter[:-3] + insert + "\n---"
    md_file.write_text(new_fm + body, encoding="utf-8")
    return True

for page, slugs in PAGES:
    url = BASE + page
    try:
        html = fetch(url)
        pairs = extract_qa(html)
        if not pairs:
            print("NO Q&A: " + page)
            continue
        for slug in slugs:
            md_file = products_dir / (slug + ".md")
            if not md_file.exists():
                print("  SKIP (no file): " + slug)
                continue
            if add_troubleshooting(md_file, pairs):
                print("  Updated: " + slug + " (" + str(len(pairs)) + " items)")
            else:
                print("  Skip (exists): " + slug)
    except Exception as e:
        print("ERROR: " + page + ": " + str(e))

print("Done.")
