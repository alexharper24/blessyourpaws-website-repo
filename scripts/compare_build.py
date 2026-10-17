#!/usr/bin/env python3
"""Compare the generated site against a saved baseline, file by file.

    python scripts/compare_build.py <baseline-dir>

The gate for every change to how scaffold.py reads its data: the output has to be the
same bytes as before. A file whose bytes differ but whose visible text is identical is
reported separately as TEXT-SAME, because an entity written as a character (&rsquo;
against a right quote) or a re-wrapped line is not a change anyone can see, while a
changed word is. Anything in DIFF is a real change and fails the gate.
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def text_of(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"<[^>]+>", " ", t)
    return " ".join(html.unescape(t).replace("\xa0", " ").split())

def main(base):
    same, textsame, diff, missing, new = [], [], [], [], []
    names = sorted(os.listdir(base))
    for n in names:
        live = os.path.join(ROOT, "img", n) if n.endswith(".png") else os.path.join(ROOT, n)
        if not os.path.exists(live):
            missing.append(n); continue
        a, b = open(os.path.join(base, n), "rb").read(), open(live, "rb").read()
        if a == b:
            same.append(n)
        elif n.endswith(".html") and text_of(a) == text_of(b):
            textsame.append(n)
        else:
            diff.append(n)
    for n in sorted(os.listdir(ROOT)):
        if n.endswith(".html") and n not in names:
            new.append(n)
    print(f"same {len(same)}  text-same {len(textsame)}  diff {len(diff)}  missing {len(missing)}  new {len(new)}")
    for label, xs in (("TEXT-SAME", textsame), ("DIFF", diff), ("MISSING", missing), ("NEW", new)):
        for x in xs:
            print(f"  {label:<9} {x}")
    return 1 if (diff or missing or new) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
