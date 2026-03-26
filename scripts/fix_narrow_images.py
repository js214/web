#!/usr/bin/env python3
"""Find panel images that are too narrow and pad them with white background."""
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGES = ROOT / "images"
MIN_RATIO = 0.7  # width/height — below this is "too narrow"
TARGET_RATIO = 0.8  # pad to this ratio

def check_and_fix(path, dry_run=False):
    """Check image aspect ratio and pad if too narrow. Returns (was_narrow, new_path)."""
    try:
        img = Image.open(path)
    except Exception:
        return False, path

    w, h = img.size
    ratio = w / h

    if ratio >= MIN_RATIO:
        return False, path

    if dry_run:
        print(f"  NARROW: {path.relative_to(ROOT)} ({w}x{h}, ratio {ratio:.2f})")
        return True, path

    # Pad width to target ratio
    target_w = int(h * TARGET_RATIO)
    new_img = Image.new("RGB", (target_w, h), (255, 255, 255))
    x_offset = (target_w - w) // 2
    new_img.paste(img, (x_offset, 0))

    # Save as _padded version
    suffix = path.suffix
    out = path.with_name(path.stem + "_padded" + suffix)
    new_img.save(str(out), quality=92)
    print(f"  FIXED:  {path.relative_to(ROOT)} ({w}x{h} -> {target_w}x{h})")
    return True, out


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("DRY RUN — showing narrow images without fixing\n")

    narrow_count = 0
    for img_path in sorted(IMAGES.rglob("*")):
        if img_path.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif"):
            if "_padded" in img_path.name:
                continue  # skip already-padded
            was_narrow, _ = check_and_fix(img_path, dry_run=dry_run)
            if was_narrow:
                narrow_count += 1

    print(f"\n{'Found' if dry_run else 'Fixed'} {narrow_count} narrow images")
