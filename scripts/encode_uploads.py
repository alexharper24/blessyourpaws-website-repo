#!/usr/bin/env python3
"""Encode photographs the owner editor published into the sizes the site serves.

The editor commits each new photograph as it was uploaded, under
uploads/puppies/<stem>.<ext> or uploads/dogs/<stem>.<ext>, together with the data/*.json
that names <stem>. It cannot run Python, so this runs in the Workers Builds build
(scripts/ci-build.sh) before scaffold.py, and writes

    img/<folder>/<stem>.jpg          the full-size fallback, at most 2000px wide
    img/r/<stem>-<w>.webp            320, 640, 1000, 1600 and 2000 where the original allows

with the same settings scripts/prep_images.py used for every photograph already on the
site, so a new photo and an old one are indistinguishable.

Safe to run on every build. A stem whose outputs already exist is skipped, so the photos
committed before the editor existed are never touched, and source-photos/ (gitignored,
absent in CI) is never needed.
"""
import os, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_W, WIDTHS = 2000, [320, 640, 1000, 1600, 2000]
EXTS = (".jpg", ".jpeg", ".png", ".webp")

def derive(src, stem, folder):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    os.makedirs(f"img/{folder}", exist_ok=True)
    os.makedirs("img/r", exist_ok=True)
    m = im.resize((MAIN_W, round(h * MAIN_W / w)), Image.LANCZOS) if w > MAIN_W else im
    m.save(f"img/{folder}/{stem}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    made = 0
    for tw in WIDTHS:
        if tw > w:
            continue
        im.resize((tw, round(h * tw / w)), Image.LANCZOS).save(
            f"img/r/{stem}-{tw}.webp", "WEBP", quality=82, method=5)
        made += 1
    if made == 0:
        # an original narrower than 320px still needs the 320 the cards and thumbnails ask for
        im.save(f"img/r/{stem}-320.webp", "WEBP", quality=82, method=5)

def main():
    os.chdir(ROOT)
    done = skipped = 0
    for folder in ("puppies", "dogs"):
        base = os.path.join("uploads", folder)
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            stem, ext = os.path.splitext(f)
            if ext.lower() not in EXTS:
                continue
            if os.path.exists(f"img/{folder}/{stem}.jpg") and os.path.exists(f"img/r/{stem}-320.webp"):
                skipped += 1
                continue
            derive(os.path.join(base, f), stem, folder)
            done += 1
            print(f"  encoded {folder}/{stem}")
    print(f"encode_uploads: {done} encoded, {skipped} already built")
    return 0

if __name__ == "__main__":
    sys.exit(main())
