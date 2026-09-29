#!/usr/bin/env python3
"""Resize and compress photos before committing them.

Shrinks images so the long edge is at most --max pixels (default 2000),
applies EXIF rotation, strips metadata, and re-encodes JPEGs as progressive
with --quality (default 82). Files are overwritten in place, and only when
the result is smaller or the image had to be resized.

Usage:
    python scripts/resize_images.py                  # everything in content/images
    python scripts/resize_images.py path/to/photo.jpg some/folder
    python scripts/resize_images.py --dry-run --max 1600
"""

import argparse
import io
import sys
from pathlib import Path

from PIL import Image, ImageOps

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_DIR = Path(__file__).resolve().parent.parent / "content" / "images"


def iter_images(paths):
    for path in paths:
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*") if p.suffix.lower() in EXTENSIONS)
        elif path.suffix.lower() in EXTENSIONS:
            yield path


def encode(img, fmt, quality):
    buf = io.BytesIO()
    if fmt == "JPEG":
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    elif fmt == "WEBP":
        img.save(buf, "WEBP", quality=quality, method=6)
    else:
        img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def process(path, max_edge, quality, dry_run):
    before = path.stat().st_size
    with Image.open(path) as original:
        fmt = original.format
        img = ImageOps.exif_transpose(original)
        resized = max(img.size) > max_edge
        if resized:
            img.thumbnail((max_edge, max_edge), Image.LANCZOS)
        data = encode(img, fmt, quality)

    after = len(data)
    if not resized and after >= before:
        print(f"  skip   {path}  (already optimised)")
        return 0

    size = f"{img.size[0]}x{img.size[1]}"
    print(f"  {'would ' if dry_run else ''}write {path}  {before / 1024:.0f} KB -> {after / 1024:.0f} KB  ({size})")
    if not dry_run:
        path.write_bytes(data)
    return before - after


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, default=[DEFAULT_DIR], help="files or folders (default: content/images)")
    parser.add_argument("--max", type=int, default=2000, help="max long-edge size in px (default 2000)")
    parser.add_argument("--quality", type=int, default=82, help="JPEG/WebP quality 1-95 (default 82)")
    parser.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    args = parser.parse_args()

    saved = 0
    for path in iter_images(args.paths):
        try:
            saved += process(path, args.max, args.quality, args.dry_run)
        except OSError as exc:
            print(f"  error  {path}: {exc}", file=sys.stderr)
    print(f"Saved {saved / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
