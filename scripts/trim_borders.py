#!/usr/bin/env python3
"""
trim_borders.py — Auto-crop near-white (or near-black) borders from images.

Usage:
    python trim_borders.py images/          # all images in a directory
    python trim_borders.py images/BGA244_FP.jpg   # single file

Trims pixels within `threshold` of pure white OR pure black on all four sides.
Saves in-place. Original is backed up as <file>.bak if --no-backup not set.
"""

import sys
from pathlib import Path
from PIL import Image


THRESHOLD = 15   # how close to white/black (0-255) before we treat as border
PADDING   = 4    # pixels of border to leave around the content


def is_border_color(r, g, b):
    """True if this color is near-white or near-black."""
    near_white = r > 255 - THRESHOLD and g > 255 - THRESHOLD and b > 255 - THRESHOLD
    near_black = r < THRESHOLD and g < THRESHOLD and b < THRESHOLD
    return near_white or near_black


def trim_image(path: Path) -> bool:
    """
    Trim uniform near-white/near-black border from all sides.
    Returns True if the image was actually cropped.
    """
    img = Image.open(path).convert("RGB")
    pixels = img.load()
    w, h = img.size

    # Detect the dominant border color from the four corners
    corners = [pixels[0, 0], pixels[w-1, 0], pixels[0, h-1], pixels[w-1, h-1]]
    border_rgb = corners[0]  # use top-left corner as reference

    def matches_border(r, g, b):
        br, bg, bb = border_rgb
        return (abs(r - br) < THRESHOLD and
                abs(g - bg) < THRESHOLD and
                abs(b - bb) < THRESHOLD)

    # Scan each side inward until we hit a non-border row/column
    top = 0
    while top < h:
        if any(not matches_border(*pixels[x, top]) for x in range(w)):
            break
        top += 1

    bottom = h - 1
    while bottom > top:
        if any(not matches_border(*pixels[x, bottom]) for x in range(w)):
            break
        bottom -= 1

    left = 0
    while left < w:
        if any(not matches_border(*pixels[left, y]) for y in range(h)):
            break
        left += 1

    right = w - 1
    while right > left:
        if any(not matches_border(*pixels[right, y]) for y in range(h)):
            break
        right -= 1

    # Apply padding, clamp to image bounds
    top    = max(0,   top    - PADDING)
    bottom = min(h-1, bottom + PADDING)
    left   = max(0,   left   - PADDING)
    right  = min(w-1, right  + PADDING)

    if (top, left, bottom+1, right+1) == (0, 0, h, w):
        print(f"  no border: {path.name}")
        return False

    cropped = img.crop((left, top, right+1, bottom+1))

    # Backup original
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        path.rename(bak)
    else:
        path.unlink()

    cropped.save(path, quality=95, subsampling=0)
    orig_size = f"{bak.stat().st_size // 1024} KB"
    new_size  = f"{path.stat().st_size  // 1024} KB"
    removed   = f"removed top={top} left={left} right={w-1-right} bottom={h-1-bottom} px"
    print(f"  trimmed:  {path.name}  [{orig_size} -> {new_size}]  ({removed})")
    return True


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["images"]
    exts = {".jpg", ".jpeg", ".png"}

    paths = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            paths.extend(f for f in sorted(p.iterdir()) if f.suffix.lower() in exts)
        elif p.is_file():
            paths.append(p)
        else:
            print(f"Not found: {t}")

    trimmed = sum(trim_image(p) for p in paths)
    print(f"\nDone — {trimmed}/{len(paths)} image(s) trimmed.")


if __name__ == "__main__":
    main()
