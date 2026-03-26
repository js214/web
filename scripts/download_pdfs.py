#!/usr/bin/env python3
"""Download all datasheets and manuals from thinksrs.com and update paths to local."""
import re
import urllib.request
import urllib.parse
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTS = ROOT / "products"

def download(url, dest):
    """Download URL to dest, return True on success."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return True
    try:
        encoded = url.replace(" ", "%20")
        urllib.request.urlretrieve(encoded, str(dest))
        time.sleep(0.5)  # be gentle on legacy server
        return True
    except Exception as e:
        print(f"  FAILED: {url} -> {e}")
        return False

def main():
    ok = 0
    fail = 0

    for md in sorted(PRODUCTS.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)", text, re.DOTALL)
        if not m:
            continue

        front = m.group(2)
        changed = False

        # Process datasheet
        ds_m = re.search(r'^datasheet:\s*"?(https://thinksrs\.com/\S+)"?', front, re.MULTILINE)
        if ds_m:
            url = ds_m.group(1).strip('"')
            filename = urllib.parse.unquote(url.split("/")[-1])
            local = ROOT / "datasheets" / filename
            if download(url, local):
                ok += 1
                new_path = f"datasheets/{filename}"
                front = front.replace(ds_m.group(0), f'datasheet: "{new_path}"')
                changed = True
                print(f"  {md.stem}: datasheet -> {new_path}")
            else:
                fail += 1

        # Process manual
        mn_m = re.search(r'^manual:\s*"?(https://thinksrs\.com/\S+)"?', front, re.MULTILINE)
        if mn_m:
            url = mn_m.group(1).strip('"')
            # Some manuals are multi-page HTML, not PDFs
            if url.endswith('.pdf'):
                filename = urllib.parse.unquote(url.split("/")[-1])
                local = ROOT / "manuals" / filename
                if download(url, local):
                    ok += 1
                    new_path = f"manuals/{filename}"
                    front = front.replace(mn_m.group(0), f'manual: "{new_path}"')
                    changed = True
                    print(f"  {md.stem}: manual -> {new_path}")
                else:
                    fail += 1
            else:
                print(f"  {md.stem}: manual is HTML ({url}), keeping external link")

        if changed:
            md.write_text(m.group(1) + front + m.group(3) + m.group(4), encoding="utf-8")

    print(f"\nDownloaded: {ok}, Failed: {fail}")

if __name__ == "__main__":
    main()
