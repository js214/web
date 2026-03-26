#!/usr/bin/env python3
"""Download all thinksrs.com images referenced in product .md files and update paths to local."""

import re
import os
import yaml
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTS_DIR = ROOT / "products"
IMAGES_DIR = ROOT / "images" / "instr"

def get_all_urls():
    """Extract all thinksrs.com image URLs from .md files, plus auto-generated panel URLs."""
    urls = set()
    products = {}

    for md_file in sorted(PRODUCTS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
        if not match:
            continue
        front = yaml.safe_load(match.group(1))
        body = match.group(2)
        slug = front.get("slug", md_file.stem)
        model = front.get("model", "").split("/")[0].strip()
        products[slug] = front

        # Explicit image URLs in frontmatter
        img = front.get("image", "")
        if isinstance(img, str) and "thinksrs.com/images" in img:
            urls.add(img)

        panels = front.get("panels", [])
        if panels:
            for p in panels:
                if isinstance(p, str) and "thinksrs.com/images" in p:
                    urls.add(p)
        else:
            # Auto-generated panel URLs from template
            urls.add(f"https://thinksrs.com/images/instr/{slug}/{model}_FPlg.jpg")
            urls.add(f"https://thinksrs.com/images/instr/{slug}/{model}_RPlg.jpg")

        # Markdown body image URLs
        for m in re.finditer(r'!\[.*?\]\((https://thinksrs\.com/images/[^)]+)\)', body):
            urls.add(m.group(1))

    return urls, products


def url_to_local_path(url):
    """Convert a thinksrs.com image URL to a local path under images/instr/."""
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)  # /images/instr/sr865a/SR865A_FP.jpg
    # Strip leading /images/ to get instr/sr865a/SR865A_FP.jpg
    rel = path.replace("/images/instr/", "", 1)
    return IMAGES_DIR / rel


def download_image(url, local_path):
    """Download a single image."""
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if local_path.exists():
        print(f"  exists: {local_path.relative_to(ROOT)}")
        return True
    try:
        encoded_url = url.replace(" ", "%20")
        urllib.request.urlretrieve(encoded_url, str(local_path))
        print(f"  downloaded: {local_path.relative_to(ROOT)}")
        return True
    except Exception as e:
        print(f"  FAILED: {url} -> {e}")
        return False


def update_md_files(products):
    """Replace thinksrs.com image URLs with local paths in all .md files."""
    for md_file in sorted(PRODUCTS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        original = text

        # Replace all thinksrs.com/images/instr/ URLs with relative local paths
        def replace_url(m):
            url = m.group(0)
            parsed = urllib.parse.urlparse(url)
            path = urllib.parse.unquote(parsed.path)
            rel = path.replace("/images/", "", 1)  # instr/sr865a/SR865A_FP.jpg
            return "images/" + rel

        text = re.sub(
            r'https://thinksrs\.com/images/instr/[^\s"\')]+',
            replace_url,
            text,
        )

        if text != original:
            md_file.write_text(text, encoding="utf-8")
            print(f"  updated: {md_file.name}")


if __name__ == "__main__":
    print("Scanning for image URLs...")
    urls, products = get_all_urls()
    print(f"Found {len(urls)} unique image URLs\n")

    print("Downloading images...")
    ok = 0
    fail = 0
    for url in sorted(urls):
        local = url_to_local_path(url)
        if download_image(url, local):
            ok += 1
        else:
            fail += 1
    print(f"\nDownloaded: {ok}, Failed: {fail}\n")

    print("Updating .md files to use local paths...")
    update_md_files(products)
    print("\nDone!")
