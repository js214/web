#!/usr/bin/env python3
"""
Fetch product images from thinksrs.com, resize to max 1000px wide,
save as JPEG, and update product .md frontmatter.
"""

import urllib.request
import urllib.error
import re
import os
import sys
from html.parser import HTMLParser
from PIL import Image
import io

IMAGES_DIR = r"C:\Users\Jkastelic\Documents\projects\web\images"
PRODUCTS_DIR = r"C:\Users\Jkastelic\Documents\projects\web\products"

PRODUCTS = [
    ("cis100",  "https://thinksrs.com/products/cis.html"),
    ("db64",    "https://thinksrs.com/products/db64.html"),
    ("ec301",   "https://thinksrs.com/products/ec301.html"),
    ("fs710",   "https://thinksrs.com/products/time/fs710.html"),
    ("fs725",   "https://thinksrs.com/products/time/fs725.html"),
    ("fs730",   "https://thinksrs.com/products/time/fs730-1.html"),
    ("fs740",   "https://thinksrs.com/products/time/fs740.html"),
    ("fs752",   "https://thinksrs.com/products/time/fs752.html"),
    ("mpa100",  "https://thinksrs.com/products/mpa100.html"),
    ("mpa160",  "https://thinksrs.com/products/mpa160.html"),
    ("nl100",   "https://thinksrs.com/products/nl100.html"),
    ("prs10",   "https://thinksrs.com/products/time/prs10.html"),
    ("qcm200",  "https://thinksrs.com/products/qcm200.html"),
    ("qms100",  "https://thinksrs.com/products/qms.html"),
    ("sc10",    "https://thinksrs.com/products/time/sc10.html"),
    ("sim900",  "https://thinksrs.com/products/sim900.html"),
    ("sim910",  "https://thinksrs.com/products/sim910911.html"),
    ("sim918",  "https://thinksrs.com/products/sim918.html"),
    ("sim921",  "https://thinksrs.com/products/sim921.html"),
    ("sim922",  "https://thinksrs.com/products/sim922923.html"),
    ("sim928",  "https://thinksrs.com/products/sim928.html"),
    ("sim940",  "https://thinksrs.com/products/sim940.html"),
    ("sim960",  "https://thinksrs.com/products/sim960.html"),
    ("sim964",  "https://thinksrs.com/products/sim965.html"),
    ("sim970",  "https://thinksrs.com/products/sim970.html"),
    ("sr250",   "https://thinksrs.com/products/sr250.html"),
    ("sr620",   "https://thinksrs.com/products/time/sr620.html"),
    ("sr625",   "https://thinksrs.com/products/time/sr625.html"),
    ("uga120",  "https://thinksrs.com/products/uga.html"),
    ("ugapm",   "https://thinksrs.com/products/ugapm.html"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}


class ImgParser(HTMLParser):
    """Parse HTML and collect image src attributes."""
    def __init__(self):
        super().__init__()
        self.images = []  # list of (src, attrs_dict)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src", "")
            if src:
                self.images.append((src, attrs_dict))


def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_bytes(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def normalize_url(url):
    """Normalize URL: resolve .. segments and percent-encode spaces."""
    # Parse and normalize the path
    parsed = urllib.parse.urlparse(url)
    # Normalize path segments (resolve ..)
    path_parts = parsed.path.split("/")
    resolved = []
    for part in path_parts:
        if part == "..":
            if resolved:
                resolved.pop()
        elif part != ".":
            resolved.append(part)
    normalized_path = "/".join(resolved)
    # Percent-encode spaces (and other chars that need encoding) but keep slashes
    normalized_path = urllib.parse.quote(normalized_path, safe="/:@!$&'()*+,;=")
    return urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, normalized_path,
        parsed.params, parsed.query, parsed.fragment
    ))


def score_image(src, attrs):
    """Score image candidates; higher = better."""
    score = 0
    src_lower = src.lower()
    filename = os.path.basename(src_lower).replace("%20", " ")

    # Must be from thinksrs image server or relative
    if "thinksrs.com" in src_lower and "/images/" not in src_lower and not src.startswith("/"):
        return -1

    # Priority patterns in filename
    for pattern in ["wide", "main", "hero", "product", "instr"]:
        if pattern in src_lower:
            score += 10

    # Images under /images/instr/ are instrument photos
    if "/images/instr/" in src_lower:
        score += 20

    # Prefer larger apparent images by checking width/height attrs
    try:
        w = int(attrs.get("width", 0))
        h = int(attrs.get("height", 0))
        score += (w * h) // 10000
    except (ValueError, TypeError):
        pass

    # Avoid icons, logos, banners, nav images
    for bad in ["logo", "icon", "banner", "nav", "arrow", "bullet", "btn",
                "spacer", "pixel", "clear", "trans", "dot", "star", "check",
                "pdf", "sprite", "bg", "background"]:
        if bad in src_lower:
            score -= 50

    # JPEG/PNG preferred
    if any(src_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
        score += 5

    return score


def find_best_image(html, page_url):
    """Return the absolute URL of the best product image found in page HTML."""
    # Derive base URL
    parts = page_url.split("/")
    base = "/".join(parts[:3])  # e.g. https://thinksrs.com
    path_base = "/".join(parts[:-1]) + "/"

    parser = ImgParser()
    parser.feed(html)

    candidates = []
    for src, attrs in parser.images:
        # Make absolute
        if src.startswith("//"):
            abs_src = "https:" + src
        elif src.startswith("/"):
            abs_src = base + src
        elif src.startswith("http"):
            abs_src = src
        else:
            abs_src = path_base + src

        s = score_image(abs_src, attrs)
        if s > 0:
            candidates.append((s, abs_src, attrs))

    if not candidates:
        # Fallback: try any /images/ URL
        for src, attrs in parser.images:
            if src.startswith("//"):
                abs_src = "https:" + src
            elif src.startswith("/"):
                abs_src = base + src
            elif src.startswith("http"):
                abs_src = src
            else:
                abs_src = path_base + src
            if "/images/" in abs_src.lower() and abs_src.lower().endswith((".jpg",".jpeg",".png")):
                candidates.append((1, abs_src, attrs))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def resize_and_save(img_bytes, out_path, max_width=1000):
    img = Image.open(io.BytesIO(img_bytes))
    # Convert to RGB (handles PNG with alpha, etc.)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    w, h = img.size
    if w > max_width:
        new_h = int(h * max_width / w)
        img = img.resize((max_width, new_h), Image.LANCZOS)
    img.save(out_path, "JPEG", quality=85)
    return img.size


def update_md_frontmatter(md_path, slug):
    """Add/replace image field in YAML frontmatter of .md file."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    image_value = f'images/{slug}_web.jpg'
    image_line = f'image: "{image_value}"'

    # Check if frontmatter exists (starts with ---)
    if not content.startswith("---"):
        print(f"  [WARN] {md_path} has no frontmatter")
        return

    # If image field already exists, replace it
    if re.search(r'^image:\s*', content, re.MULTILINE):
        new_content = re.sub(r'^image:.*$', image_line, content, flags=re.MULTILINE)
    else:
        # Insert after 'sort:' line
        if re.search(r'^sort:\s*', content, re.MULTILINE):
            new_content = re.sub(
                r'^(sort:.*)$',
                r'\1\n' + image_line,
                content,
                flags=re.MULTILINE
            )
        else:
            # Insert before closing ---
            # Find second --- and insert before it
            idx = content.find("---", 3)
            if idx != -1:
                new_content = content[:idx] + image_line + "\n" + content[idx:]
            else:
                new_content = content + "\n" + image_line + "\n"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def process_product(slug, url):
    print(f"\n{'='*60}")
    print(f"Processing: {slug} -> {url}")

    # 1. Fetch page
    try:
        html = fetch_url(url)
    except Exception as e:
        print(f"  [FAIL] Could not fetch page: {e}")
        return False, "page fetch failed"

    # 2. Find best image
    img_url = find_best_image(html, url)
    if not img_url:
        print(f"  [SKIP] No usable image found")
        return False, "no image found"

    img_url = normalize_url(img_url)
    print(f"  Image URL (normalized): {img_url}")

    # 3. Download image
    try:
        img_bytes = fetch_bytes(img_url)
    except Exception as e:
        print(f"  [FAIL] Could not download image: {e}")
        return False, f"image download failed: {e}"

    # 4. Resize and save
    out_path = os.path.join(IMAGES_DIR, f"{slug}_web.jpg")
    try:
        final_size = resize_and_save(img_bytes, out_path)
        print(f"  Saved: {out_path} ({final_size[0]}x{final_size[1]})")
    except Exception as e:
        print(f"  [FAIL] Could not process image: {e}")
        return False, f"image processing failed: {e}"

    # 5. Update .md file
    md_path = os.path.join(PRODUCTS_DIR, f"{slug}.md")
    if os.path.exists(md_path):
        try:
            update_md_frontmatter(md_path, slug)
            print(f"  Updated: {md_path}")
        except Exception as e:
            print(f"  [WARN] Could not update .md: {e}")
    else:
        print(f"  [WARN] .md file not found: {md_path}")

    return True, img_url


def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)

    results = []
    for slug, url in PRODUCTS:
        ok, detail = process_product(slug, url)
        results.append((slug, ok, detail))

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    succeeded = [(s, d) for s, ok, d in results if ok]
    failed = [(s, d) for s, ok, d in results if not ok]

    print(f"\nSucceeded ({len(succeeded)}):")
    for s, d in succeeded:
        print(f"  {s}")

    print(f"\nFailed/Skipped ({len(failed)}):")
    for s, d in failed:
        print(f"  {s}: {d}")


if __name__ == "__main__":
    main()
