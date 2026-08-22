#!/usr/bin/env python3
"""Split the Bernedoodle parents out of the puppy galleries, then regenerate
every derivative.

Puppy Connection repeats the same two parent photos in all seven puppy
galleries. Detected by content hash, not by eye or by index: whichever files
appear in every gallery are the parents.

  Troy (dam, Mini Multi Gen Bernedoodle, blue merle parti) -> img/dogs/troy-01.jpg
  the AKC Cavalier sire (ruby)                             -> img/dogs/cavalier-sire-01.jpg

Puppy photos are then renumbered contiguously so no gap is left behind.
"""
import hashlib, os, json, shutil, collections
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

MUNCH = ["joshua", "eden", "havilah", "jordan", "caleb", "shiloh", "jericho"]
DOBE = ["elowen", "malcolm", "griffin"]
MAIN_W, WIDTHS = 2000, [320, 640, 1000, 1600, 2000]

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def derive(src_path, stem, folder):
    """Write img/<folder>/<stem>.jpg plus the responsive webp set."""
    im = ImageOps.exif_transpose(Image.open(src_path)).convert("RGB")
    w, h = im.size
    os.makedirs(f"img/{folder}", exist_ok=True)
    m = im.resize((MAIN_W, round(h * MAIN_W / w)), Image.LANCZOS) if w > MAIN_W else im
    m.save(f"img/{folder}/{stem}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    n = 1
    for tw in WIDTHS:
        if tw > w:
            continue
        im.resize((tw, round(h * tw / w)), Image.LANCZOS).save(
            f"img/r/{stem}-{tw}.webp", "WEBP", quality=82, method=5)
        n += 1
    return n

def main():
    os.makedirs("img/r", exist_ok=True)
    # wipe previously generated derivatives so renumbering leaves nothing stale
    for d in ("img/puppies", "img/dogs"):
        if os.path.isdir(d):
            shutil.rmtree(d)
    for f in os.listdir("img/r"):
        os.remove(f"img/r/{f}")

    # ---- find the photos shared by every Munchkin gallery: those are the parents
    base = "source-photos/puppy-connection"
    by_hash = collections.defaultdict(list)
    for n in MUNCH:
        for f in sorted(os.listdir(f"{base}/{n}")):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                by_hash[md5(f"{base}/{n}/{f}")].append(f"{base}/{n}/{f}")
    shared = {h: v for h, v in by_hash.items() if len(v) == len(MUNCH)}
    print(f"parent photos detected (in all {len(MUNCH)} galleries): {len(shared)}")

    # the dam is the blue merle parti Bernedoodle, the sire is the ruby Cavalier.
    # tell them apart on mean saturation+hue rather than filename: the ruby
    # Cavalier is a warm solid coat, Troy is a desaturated grey/white parti.
    import colorsys
    ranked = []
    for h, paths in shared.items():
        im = Image.open(paths[0]).convert("RGB").resize((64, 64))
        px = list(im.getdata())
        sat = sum(colorsys.rgb_to_hsv(*[c / 255 for c in p])[1] for p in px) / len(px)
        ranked.append((sat, paths[0]))
    ranked.sort()
    troy_src = ranked[0][1]      # least saturated -> the white/grey parti dam
    sire_src = ranked[-1][1]     # most saturated  -> the ruby Cavalier
    print(f"  Troy (dam, low saturation {ranked[0][0]:.3f}):  {os.path.basename(troy_src)}")
    print(f"  Cavalier sire (ruby, {ranked[-1][0]:.3f}):      {os.path.basename(sire_src)}")

    os.makedirs("source-photos/bernedoodle-parents", exist_ok=True)
    for src, stem in ((troy_src, "troy-01"), (sire_src, "cavalier-sire-01")):
        keep = f"source-photos/bernedoodle-parents/{stem}{os.path.splitext(src)[1]}"
        shutil.copy2(src, keep)
        derive(keep, stem, "dogs")

    shared_hashes = set(shared)

    # ---- Munchkin puppies, parents removed, renumbered contiguously
    counts = {}
    for n in MUNCH:
        files = [f for f in sorted(os.listdir(f"{base}/{n}"))
                 if f.lower().endswith((".jpg", ".jpeg", ".png"))
                 and md5(f"{base}/{n}/{f}") not in shared_hashes]
        for i, f in enumerate(files, 1):
            derive(f"{base}/{n}/{f}", f"{n}-{i:02d}", "puppies")
        counts[n] = len(files)
        print(f"  {n:<9} {len(files)} puppy photos")

    # ---- Dobermans from the Kingdom repo's DELIVERED renditions, not the raw
    # Wix originals. Wix tone-corrects on delivery, so the raw files are darker
    # and softer -- that is why the Dobermans looked shaded.
    KFC = "../kingdomfamilycompanions-website-repo/img"
    kfc_puppies = {"elowen": 3, "malcolm": 4, "griffin": 6}
    for n, cnt in kfc_puppies.items():
        for i in range(1, cnt + 1):
            derive(f"{KFC}/puppy-{n}-{i}.jpg", f"{n}-{i:02d}", "puppies")
        counts[n] = cnt
        print(f"  {n:<9} {cnt} puppy photos (delivered renditions)")

    # ---- Doberman parents: Mira, and the red-and-rust sire Joy confirmed
    derive(f"{KFC}/dog-mira.jpg", "mira-01", "dogs")
    derive(f"{KFC}/adult-dog-2.jpg", "doberman-sire-01", "dogs")
    print("  Doberman parents: mira-01, doberman-sire-01 (confirmed by Joy)")

    json.dump(counts, open("img/photo-counts.json", "w"), indent=2)
    print(f"\ndone. {sum(counts.values())} puppy photos, 3 parent photos.")

if __name__ == "__main__":
    main()
