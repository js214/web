#!/usr/bin/env python3
"""Download all app notes and update app_notes.yaml to use local paths."""
import re
import time
import urllib.request
import urllib.parse
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
APP_NOTES_DIR = ROOT / "app_notes"
YAML_FILE = ROOT / "pages" / "app_notes.yaml"

def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return True
    try:
        encoded = url.replace(" ", "%20")
        urllib.request.urlretrieve(encoded, str(dest))
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"  FAILED: {url} -> {e}")
        return False

def main():
    notes = yaml.safe_load(YAML_FILE.read_text(encoding="utf-8"))
    ok = 0
    fail = 0

    for cat, items in notes.items():
        for item in items:
            url = item["url"]
            if not url.startswith("http"):
                continue
            filename = urllib.parse.unquote(url.split("/")[-1])
            local = APP_NOTES_DIR / filename
            if download(url, local):
                ok += 1
                item["url"] = f"app_notes/{filename}"
                print(f"  {item['label'][:40]:40s} -> app_notes/{filename}")
            else:
                fail += 1

    YAML_FILE.write_text(yaml.dump(notes, default_flow_style=False, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"\nDownloaded: {ok}, Failed: {fail}")

if __name__ == "__main__":
    main()
