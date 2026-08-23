# CLAUDE.md — Bless Your Paws

Repo-specific conventions. Read alongside the root `C:\Git_Repos\CLAUDE.md` and
`.claude/guides/static-sites.md`.

## What this is

Static website for **Bless Your Paws**, the dog-breeding business of **Joy Williams
and Hope Williams** (twin sisters, sisters-in-law to Alex via Mary). Two breed lines
at launch:

- **Munchkin Bernedoodles** (Hope) — dam **Troy**, a Mini Multi Gen Bernedoodle
  (21 lbs, blue merle parti, born 21 Jan 2024, unregistered) × an AKC Cavalier King
  Charles Spaniel sire (19 lbs, ruby, born 24 Dec 2024, **name unknown**).
  CORRECTED 2026-08-22: Troy is the DAM, female. Earlier notes had Troy as the
  Cavalier sire; that was a transcription error. "Mira" was never a Bernedoodle,
  she is Joy's Doberman dam.
- **Doberman Pinschers** (Joy) — co-owned with Amber. Dam **Mira** (Kingdom's
  Miraculous Grace, WS85545303, GenSol clear / DCM3 carrier, OFA Advanced Cardiac
  normal, appnum 2720473). Sire unknown.

**Launch pricing (Alex, 2026-08-22): Munchkin Bernedoodles $2,000, Dobermans $2,200.**
Deposit $500. Quote tentatively accepted; Phase 1 build authorized.

**Draft-content directive (Alex, 2026-08-22):** where copy is missing, write sample
copy and mark it visibly; where images are missing, ship branded placeholders. The
health guarantee and purchase agreement get DRAFT pages flagged for review before
launch. Expected adult weight may be shown as a DRAFT estimate from the 19 lb and
21 lb parents (15–25 lbs), clearly marked to be confirmed by Hope. Faith element is
ON HOLD pending the questionnaire; do not add or rule out.

A **Maltipoo** line is roughly 18 months out and is deliberately NOT in the launch
build. Build the breed-page pattern so it drops in as content, not a redesign.

## Design tokens — sampled from the client's five swatches, not from labels

```css
:root {
  --forest:      #223d2c;  /* ink + dark bands. 11.85:1 on white */
  --sage:        #7f8e79;  /* mid accent. 3.47:1 — LARGE TEXT ONLY */
  --sage-deep:   #6d7a68;  /* derived. 4.53:1 on white — use for small text/links */
  --sage-light:  #a8b89e;  /* surface tint */
  --rose:        #feb5bc;  /* surface tint / accent */
  --pink-pale:   #fbc4db;  /* surface tint */
}
```

**Two hard contrast rules:**

1. `--sage` is **large-text-only** at 3.47:1. Any small text or link uses
   `--sage-deep`.
2. **Never white text on `--rose` or `--pink-pale`** (1.67:1 and 1.50:1). Use
   `--forest` on them — it reads at 7.08:1 and 7.91:1 respectively.

Verified-good pairings: forest on white 11.85, on pale pink 7.91, on rose 7.08, on
light sage 5.65. White on forest 11.85. Rose on forest 7.08. Pale pink on forest
7.91. The pinks work as accents *on* the dark band — a useful inversion.

Unlike `marysbakingcorner`, this palette needs **no documented WCAG departures**.
Keep it that way.

## Logo package — and the navy vs forest conflict

`img/brand/` holds a seven-file logo package. Full business name is
**Bless Your Paws Puppies**. Alpha is clean on all of them (no opaque-background
trap). Alex did not generate these; he is adapting them.

| File | What it is |
|---|---|
| `logo-horizontal-color.png` | Primary horizontal lockup, 1672x941 |
| `logo-stacked-color.png` | Stacked lockup, 1122x1402 |
| `logo-badge-color.png` | Circular badge/seal with a cream ground baked in |
| `mark-heart-puppy-color.png` | Heart + puppy mark, no text |
| `mark-paw-heart.png` | **Pink paw print with a heart. Use this for favicon and nav** |
| `logo-horizontal-navy-mono.png` | Monochrome navy line-art version |
| `logo-horizontal-navy-alt.png` | Second navy horizontal variant |

**RESOLVED 2026-08-22 (Alex): recolour the navy to forest and keep the greens.**

The supplied logo inked in navy `#00183c` while the supplied swatches are forest green
and pinks — two different brand directions. Alex chose to keep the greens, so the navy
was recoloured to `--forest`.

Recoloured files sit **alongside** the navy originals, which stay tracked (never delete
a logo variant):

| Forest version | From |
|---|---|
| `logo-horizontal-forest.png` | `logo-horizontal-color.png` |
| `logo-stacked-forest.png` | `logo-stacked-color.png` |
| `logo-badge-forest.png` | `logo-badge-color.png` |
| `logo-horizontal-forest-mono.png` | `logo-horizontal-navy-mono.png` |
| `logo-horizontal-forest-alt.png` | `logo-horizontal-navy-alt.png` |

**How it was done, so it can be repeated consistently.** Navy is HSV(216.0, 1.00,
0.235) and forest is HSV(142.2, 0.443, 0.239) — the two are within 0.004 of the same
*lightness*. So the recolour shifts hue by −73.8° and damps saturation to 0.443 while
**keeping value and alpha untouched**, which preserves every antialiased edge. No
re-tracing, per the standing rule.

The mask is deliberately narrow — hue 195–262°, saturation > 0.15, alpha > 0.02 — so it
catches the navy script and leaves alone the puppy's black and tan fur (near-neutral,
low saturation) and the pink heart and paw (opposite hue). Verified visually on the
horizontal and mono versions: fur and pinks are intact.

`mark-heart-puppy-color.png` and `mark-paw-heart.png` contain no navy and needed no
recolour.

**The script lockup will not read at nav size.** Fine script plus an illustrated
puppy disappears at 34px, and the badge has a cream ground that will not sit on a
tinted section. `mark-paw-heart.png` is the small-size answer; the full lockup is for
hero and About placements only. Favicon needs stroke dilation per the standing rule.

## Character and direction

Client brief from Hope: **flowery, pinks, greens, vintage.** Direction is botanical /
vintage-plate. Floral motif is explicitly welcomed.

**Write the one-sentence character statement into the README before any CSS**, and
log the row in the skill's `references/built-sites.md` ledger when the build ships.

## Do NOT carry anything over from Kingdom Family Companions

Hope said she liked how `kingdomfamilycompanions-website-repo` turned out. That is a
compliment about **quality and structure**, not a request for a copy. KFC is
**Amber's** site.

Reusable: the flow from litter → puppy → reserve, and the linked-health-records
credibility pattern.

**Never carried over:**

- Cream `#fdf8ef` / espresso `#513833` / gold palette
- Newsreader + Karla type
- The ledger-row / narrative-scroll archetype — this build needs a different one
- The verse band and "Kingdom" naming
- Any testimonial (two were transcribed from screenshots, one is unattributed)
- **KFC's contact details** — `(260) 306-9010`,
  `info@kingdomfamilycompanions.com`, and the Milford, Indiana location are Amber's
  business identity. **This is the easiest mistake to make while "pulling the
  Doberman info."**
- **The dog bios and puppy descriptions** — Amber's words from her Wix site.
  Duplicate content, and not Joy's to republish.
- **The Golden Retrievers** (Diamond, Scarlet) — Joy co-owns *the Doberman*. Working
  assumption is the Goldens are Amber's alone and belong nowhere on this site.

**Facts** about the dogs Joy co-owns (registrations, OFA numbers, test results) carry
over fine. Prose and identity do not.

## Breed-term rules

- **"Munchkin Bernedoodle" is an established market term** — use it prominently. It
  is what buyers search. Verified against seven competing breeder sites 2026-08-22.
- **It means small overall size, NOT short legs.** Some secondary sources (including
  Google's AI Overview) call it a Corgi-like dwarf trait. The actual breeder sources
  do not. **Never put short-leg or dwarfism language on this site.**
- **Never promise non-shedding or hypoallergenic coats.** Even the established
  breeders hedge ("may be low-shedding, depending on the individual puppy"). Publish
  only what Hope states about her own puppies.

## Never guess these

Deposit amount, refund terms, health guarantee terms, the Purchase Agreement, go-home
package contents, prices, dates of birth, and go-home dates. All client-supplied; the
legal documents should be attorney-reviewed. Mark every gap `REPLACE THIS` and track
it in the README pending list.

## No home address, ever

Home-based business. Service area only. "Location shared once your visit is
scheduled."

## Run locally

```bash
python -m http.server 8199 --directory blessyourpaws-website-repo
```

Or `preview_start({name: "blessyourpaws"})` from the root launch.json.

Before committing: `python check_site.py blessyourpaws-website-repo` from the
`site-checks` repo.

## Responsive traps this build actually hit

Two of these cost a full review round each. Check both before claiming a mobile pass
is done.

**A modifier class outranks the mobile override.** `.grid-2.narrow-left` is
specificity (0,2,0); the `@media (max-width:900px)` rule that collapses `.grid-2` is
(0,1,0) and loses. The variants held their desktop columns on a phone across eight
pages while the override looked correct in the source. Every modifier has to be named
in the mobile block explicitly. Applies equally to `.parent-grid.row-4` and to any
`.grid-2` modifier added later.

**Flex and grid children default to `min-width:auto`.** A value with no break
opportunity in it, in this case `info@blessyourpawspuppies.com`, sets the min-content
width of its column, which pushed the contact page 48px past a 320px screen and
dragged the photo in the next column out with it. `.grid-2>*{min-width:0}` and
`overflow-wrap:anywhere` on the value are the fix. The symptom is horizontal scroll on
one page at one narrow width, so it does not show up unless 320px is actually measured.

**CTA rows.** The rule is: side by side when the buttons fit, full width when one
wraps onto its own line. `flex:1 1 auto` on the buttons of a wrapping row does both,
so there is no need for a media query per button pair. Do not apply it to
`.section-cta` on mobile, which turns to a column, where flex-grow would grow the
button vertically instead; that one uses `align-items:stretch`.

**The chat launcher is not injected on a page that has `form[data-guard]`.** It is
redundant next to the inquiry form, and at 390px the fixed button landed on top of a
form field on the waitlist page.

**Stacked sections read heading, photo, copy. Use `.hic`.** Left to auto-placement a
two-column section stacks as heading-copy-photo or photo-heading-copy depending on which
column happens to come first in the source, and both are wrong on a phone: the first
buries the photo under a wall of text, the second opens with a photo of nothing in
particular before the reader knows what they are looking at. Nine sections were wrong
this way. The pattern is three children in source order, `.hic-head` / `.hic-photo` /
`.hic-copy`, on a container with `.hic`, plus `.hic-flip` when the photo belongs in the
first column on desktop. Mobile then needs no rules at all, because the source order IS
the mobile order.

**Scope desktop-only grid placement with `min-width`, never by undoing it below 900px.**
This is the same specificity trap as the modifier classes above and it bit three times in
one session. An undo rule like `.hic>*` is (0,1,0) and loses to `.hic>.hic-head` at
(0,2,0); the `grid-column:2` that survives then creates an *implicit second track*, which
takes the whole row width and leaves the text column at 0px. The failure looks like a
collapsed layout, not like a specificity problem, which is what makes it expensive.

**The hero photo's headroom is a property of the photograph, not the crop.** `havilah-01`
has the puppy's crown 5.4% down the frame. Cropping can only ever reduce that, so
`object-position` is pinned to `50% 0%` on desktop and mobile uses `aspect-ratio:3/2`,
matching the source so nothing is cropped at all. Note that 5-6% is 38px on a 593px
desktop hero but only 14px on a phone, so the same crop that reads as generous on a
laptop reads as tight on a phone. The mobile fix that actually mattered was the 20px gap
between the sticky header and the photo, which had been zero. More air than this needs a
different photograph. Run the headroom measurement in the git history before picking one.

**Clearing `aspect-ratio` is part of overriding a sized box.** The mobile hero blew the
whole document out to 967px inside a 375px page. The mobile rule set `width:auto` and a
`min-height`, but left the desktop `aspect-ratio:16/9` in place, and the ratio then
derived the width FROM the height: 544 x 16/9 = 967. Any rule that re-sizes a box which
had an aspect-ratio must set `aspect-ratio:auto` too.

**`height:100%` needs a parent with a definite height.** After that fix the hero photo
sat at its intrinsic 250px inside a 544px cell with a dark void beneath it, because the
parent's height came from `min-height` plus a grid sibling, which is indefinite, so the
percentage resolved to auto. The photo is `position:absolute;inset:0` instead. Same trap
applies to any full-bleed image in a cell sized by something other than itself.

**A grid's implicit track is `auto`, which means max-content.** An unconstrained image in
one sizes the track to the intrinsic width of the source file. Overlay heroes use
`grid-template-columns:minmax(0,1fr)`.

**`.grid-2` sets `align-items:center` and is declared AFTER `.hic`.** A bare `.hic` at
(0,1,0) loses, every item centres in its row, and a heading floats away from its own
paragraph. It is `.grid-2.hic` for that reason. Also give `.hic` `grid-template-rows:auto
1fr` on desktop: with two `auto` rows the slack from a tall spanning photo is split
BETWEEN the heading row and the copy row, which opens the same gap a different way.

**A last child's bottom margin does not collapse out through padding.** The "extra white
space before the box closes" on the door cards was the final paragraph's own margin
sitting on top of `.door-body`'s padding. `.door-body>:last-child{margin-bottom:0}`.

**Do not stack `.facts` key over value at narrow widths.** It was tried and reverted:
doubling the height of a six-row fact list is pure scrolling on the page where buyers are
reading specs. `min-width:0` plus `overflow-wrap` on the value is what prevents overflow,
not stacking.

**Single-word last lines are handled by `text-wrap:pretty` on mobile**, with `balance` on
headings. Browsers without support ignore both.

**An overlay item must be `align-self:stretch`, not inherit `center`.** `.hero-drift` sets
`align-items:center`. The mobile hero puts the photo and the copy in the SAME grid cell,
so on a device whose text runs taller than the photo's `min-height` the cell grows, a
centred photo stays at `min-height`, and the copy hangs off the bottom of the picture it
is supposed to be sitting on. This did not reproduce in Chrome at 393px, where the lede
wraps to four lines; it reproduced on an iPhone where it wraps to five. Stress-test an
overlay by forcing the type larger rather than trusting one browser's line breaking.

**`.wrap` makes its gutter with `width:min(94%,var(--maxw))` and auto margins, not
padding**, so the inset is 3% a side, about 12px on a phone. Every section except `.hero`
adds its own padding on top of that; `.hero` is `padding:0`, so overlaid hero copy sat
12px from the screen edge. The hero overlay carries `width:100%;padding-inline:1.25rem`
for a deliberate 20px, wider than body copy because type over a photograph needs more
room from the edge than type on paper.

**Bump `V` on every change to style.css, not once per session.** V sat at 18 across three
different stylesheet contents while intermediate fixes were made. Only the last was
committed so nothing broken shipped, but any device that loaded the site mid-session
would have cached a `?v=18` that no longer matched the markup.

**Measure a range, not one width.** 390px alone was clean while 320px overflowed and
768px was fine. The audit that matters runs every page at 320 / 390 / 414 checking for
horizontal overflow, uncollapsed multi-column grids, and CTA lines that do not fill
their container, then re-checks 1280 and 1920 to confirm the desktop treatment and the
asymmetric columns survived. `.parent-grid` is `auto-fit`, so 2 to 3 columns at 768px
and above is correct, not a missed collapse.
