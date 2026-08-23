"""Clean and derive the floral motif assets.

The five source files came out of an image generator with its background removed,
which left two artifacts on every one of them:

  1. Isolated faint flecks floating in the transparent areas, mean alpha around 0.10
     to 0.20. Invisible at thumbnail size, clearly visible as dirt at hero size.
  2. Saturated yellow, red and neon-green fringe hugging the alpha edges, worst on
     the swag and the wreath.

A caution on judging this by eye: most image viewers, including the one used to
inspect these, render transparency as BLACK, which is the worst possible backdrop for
a light halo and makes the fringe look far worse than it is. Composite onto the actual
--paper #fdf9f9 and onto --forest #223d2c before concluding anything is wrong.

Neither can be cleaned with a hue filter alone. The palette's own gold stamens sit at
the same hue and saturation as the yellow fringe, so a global hue test removes the
flower centres. Both artifacts are instead identified by WHERE they sit:

  - a fleck has a sparse neighbourhood, real content sits inside a dense mass
  - fringe is within a couple of pixels of transparent AND far more saturated than
    the muted sage the palette actually uses

Run:  python scripts/prep_florals.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(HERE, "img", "brand")

# source file -> output stem. The two corner pieces are named for the corner they
# actually occupy: one masses its blooms upper-left, the other upper-right. The
# sources arrived with generator filenames and were renamed to match these stems.
SOURCES = [
    ("floral-corner-left-source.png",  "floral-corner-left",  (360, 520, 720)),
    ("floral-corner-right-source.png", "floral-corner-right", (360, 520, 720)),
    ("floral-swag-source.png",         "floral-swag",         (640, 1000, 1500)),
    ("floral-sprig-source.png",        "floral-sprig",        (240, 380, 560)),
    ("floral-wreath-source.png",       "floral-wreath",       (420, 640, 900)),
]

FLECK_DENSITY = 0.25   # local alpha mean below which a visible pixel is a fleck
FRINGE_SAT    = 0.62   # the sage in this palette never gets this saturated
EDGE_PX       = 3      # how far from transparent counts as the fringe band


def hue_sat(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = mx - mn
    sat = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0.0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    nz = d > 1e-6
    hue = np.select(
        [nz & (mx == r), nz & (mx == g), nz & (mx == b)],
        [(60 * ((g - b) / np.maximum(d, 1e-6))) % 360,
          60 * ((b - r) / np.maximum(d, 1e-6)) + 120,
          60 * ((r - g) / np.maximum(d, 1e-6)) + 240], 0.0)
    return hue, sat


def clean(path):
    im = Image.open(path).convert("RGBA")
    arr = np.asarray(im).astype(np.float32)
    rgb, alpha = arr[..., :3] / 255.0, arr[..., 3] / 255.0
    vis = alpha > 0.02
    before = int(vis.sum())

    # --- 1. isolated flecks -------------------------------------------------
    dens = np.asarray(
        Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.BoxBlur(6))
    ).astype(np.float32) / 255.0
    fleck = vis & (dens < FLECK_DENSITY)
    alpha[fleck] = 0.0

    # --- 2. saturated fringe, but only in the band next to transparent -------
    # recompute visibility after the fleck pass so the band follows the real edge
    vis2 = alpha > 0.02
    interior = np.asarray(
        Image.fromarray((vis2 * 255).astype(np.uint8), "L")
        .filter(ImageFilter.MinFilter(EDGE_PX * 2 + 1))
    ) > 127
    band = vis2 & ~interior
    hue, sat = hue_sat(rgb)
    # out-of-palette hues: the palette is pink around 340-360 and muted sage around
    # 80-110. Neon yellow-through-green and pure red in the edge band are artifacts.
    offpalette = ((hue > 25) & (hue < 160)) | (hue > 356) | (hue < 10)
    fringe = band & offpalette & (sat > FRINGE_SAT)
    # desaturate toward the pixel's own value rather than erasing, so the silhouette
    # keeps its antialiasing instead of gaining a hard jagged edge
    if fringe.any():
        v = rgb[fringe].max(-1, keepdims=True)
        rgb[fringe] = rgb[fringe] * 0.25 + v * 0.75 * np.array([0.62, 0.66, 0.58])

    out = np.dstack([np.clip(rgb, 0, 1) * 255.0, np.clip(alpha, 0, 1) * 255.0])
    return (Image.fromarray(out.astype(np.uint8), "RGBA"),
            before, int(fleck.sum()), int(fringe.sum()))


def crop_to_content(im):
    """Trim fully transparent margins so a CSS width means the art, not the padding."""
    bbox = im.getchannel("A").point(lambda v: 255 if v > 2 else 0).getbbox()
    return im.crop(bbox) if bbox else im


def main():
    total = 0
    for src, stem, widths in SOURCES:
        path = os.path.join(BRAND, src)
        if not os.path.exists(path):
            print("  MISSING, skipped: %s" % src)
            continue
        im, vis, flecks, fringe = clean(path)
        im = crop_to_content(im)
        # no cleaned master is kept: the sources are tracked and this script is
        # deterministic, so a 1.5MB PNG per motif would be 6.5MB of duplicate
        sizes = []
        webp_kb = 0.0
        for w in widths:
            h = round(im.height * w / im.width)
            d = im.resize((w, h), Image.LANCZOS)
            # WebP carries the alpha channel and is what the photos on this site
            # already ship as. A PNG of the same divider is five to eight times the
            # weight, which is not a trade worth making for decoration.
            wp = os.path.join(BRAND, "%s-%d.webp" % (stem, w))
            d.save(wp, format="WEBP", quality=82, method=6)
            webp_kb += os.path.getsize(wp) / 1024
            sizes.append("%d:%.0fKB" % (w, os.path.getsize(wp) / 1024))
            total += 1
        # only WebP derivatives ship. A PNG set of the same widths measured five to
        # eight times the weight, which is not a trade worth making for decoration,
        # and the site's photographs already ship as WebP.
        sizes.append("[%.0fKB total]" % webp_kb)
        print("  %-20s flecks %5d, fringe %5d  ->  %s"
              % (stem, flecks, fringe, "  ".join(sizes)))
    print("\n%d derivatives written to img/brand/" % total)


if __name__ == "__main__":
    main()
