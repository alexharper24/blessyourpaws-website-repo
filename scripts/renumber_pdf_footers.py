# -*- coding: utf-8 -*-
"""Renumber the published Wisdom Panel PDF's footer from "page 4 of 14" to "page 1 of 11".

The report was trimmed from 14 pages to 11 by copying the wanted range into a fresh
document, which renumbers nothing: every page still carries the footer it was printed
with, so the file opened on "page 4 of 14" and ended on "page 14 of 14". That reads as
a document with pages missing, which is the opposite of what a health record should
look like.

Two details that matter:

* The footer is REDACTED, not covered with a white box. A white box leaves the old
  string in the text layer, so copy-paste, ctrl-F and a screen reader would all still
  report "page 4 of 14" while the eye saw "page 1 of 11". Nothing else lives in that
  corner (no drawings, no images, the left-hand footer ends at x=146), so the redaction
  can only take the number.
* The replacement is set in the report's OWN font, extracted from the file. It is an
  Identity-H subset of UntitledSans-Regular, and it happens to retain all ten digits.
  Confirmation that it is the right font: it measures "page 4 of 14" at 44.52pt against
  the 44.53pt the original span actually occupies.
"""
import pymupdf, os, sys

os.chdir(r"C:\Git_Repos\blessyourpaws-website-repo")
SRC = "records/troy-wisdom-panel-2026-02-21.pdf"
SP  = os.path.dirname(os.path.abspath(__file__))   # the extracted font lands here
TTF = os.path.join(SP, "_extracted-untitledsans.ttf")

doc = pymupdf.open(SRC)
n = doc.page_count

# the footer's own font, pulled out of the file rather than approximated
name, ext, typ, buf = doc.extract_font(14)
assert "UntitledSans-Regular" in name, name
open(TTF, "wb").write(buf)
font = pymupdf.Font(fontfile=TTF)

SIZE  = 7.995
GREY  = (0x8C / 255.0,) * 3      # colour 9211020 == #8c8c8c, read off the original span
RIGHT = 562.2409                 # every page's footer is right-aligned to this edge
BASE  = 829.5                    # and sits on this baseline

done = []
for i, page in enumerate(doc):
    span = None
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].startswith("page ") and " of " in s["text"]:
                    span = s
    if span is None:
        sys.exit("no page-number footer found on page %d" % (i + 1))

    old = span["text"]
    new = "page %d of %d" % (i + 1, n)

    # generous rect: the numbers are the widest thing here at 47.6pt, and the nearest
    # other ink is 368pt to the left
    page.add_redact_annot(pymupdf.Rect(505, 817.5, 567, 834))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)

    x = RIGHT - font.text_length(new, SIZE)
    page.insert_text((x, BASE), new, fontsize=SIZE, fontfile=TTF,
                     fontname="UntSans", color=GREY, render_mode=0)
    done.append((old, new))

# written beside the source and moved into place only after it verifies, so a bad run
# cannot leave a broken health record in the repo
TMP = os.path.join(SP, "renumbered.pdf")
before = os.path.getsize(SRC)
doc.save(TMP, garbage=4, deflate=True)
doc.close()

chk = pymupdf.open(TMP)
assert chk.page_count == n, chk.page_count
seen = []
for i, page in enumerate(chk):
    t = page.get_text()
    want = "page %d of %d" % (i + 1, n)
    assert want in t, "page %d does not read %r" % (i + 1, want)
    assert " of 14" not in t, "page %d still says 'of 14'" % (i + 1)
    seen.append(want)
chk.close()
print("verified in the saved file: " + ", ".join(seen))

os.replace(TMP, SRC)

for old, new in done:
    print("  %-14s -> %s" % (old, new))
print("%d pages renumbered. %d bytes -> %d" % (len(done), before, os.path.getsize(SRC)))
