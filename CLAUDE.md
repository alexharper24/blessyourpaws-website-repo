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
the parents' weights. SUPERSEDED 2026-08-23: it is 15–20 lbs per Alex, held in
`M_SIZE`, still chip-marked for confirmation. Faith element is
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
- **It means small overall size** as a market term. Some secondary sources (including
  Google's AI Overview) call it a Corgi-like dwarf trait; the breeder sources do not.
- **REVISED 2026-08-23 by Troy's own genetic report. The site may no longer claim there
  is no dwarfism gene involved.** Troy's Wisdom Panel (test date 2026-02-21) returns her
  **At Risk for Chondrodystrophy (CDDY) and IVDD**: one copy of the FGF4 retrogene
  insertion, autosomal dominant, plus one copy of CDPA. The report states in terms that
  her legs will likely be slightly shorter. Two claims were removed from the live site
  because of it: "There is no dwarf gene involved" and the FAQ answer "No. ... not from a
  short-legged or dwarfism gene." Do not reinstate either. What replaces them is Hope's
  decision, not ours, because CDDY is dominant and therefore inheritable by the puppies.
- Do not write short-leg or dwarfism language *as marketing*. That is different from
  denying the genetics, which is what the old rule had the site doing.
- **Never promise non-shedding or hypoallergenic coats.** Even the established
  breeders hedge ("may be low-shedding, depending on the individual puppy"). Publish
  only what Hope states about her own puppies.


## Fonts are self-hosted

`fonts/` holds three woff2 files: `lora-variable`, `lora-italic`, `mulish-variable`. Both
families are SIL Open Font License, so redistribution is fine. They are VARIABLE fonts, one
file spanning 400-700, which is why six Google faces came down as three files.

Google Fonts is gone entirely. It cost two third-party origins, a DNS and TLS handshake for
each, and a serial dependency: the browser had to fetch and parse a stylesheet from
googleapis before it could even discover the font URLs on gstatic. Self-hosted with a
`preload` on the two faces every page uses, the fonts start with the HTML. Byte count is
about the same, roughly 66KB either way; the win is the round trips, not the bytes.

`lora-italic` is declared but deliberately NOT preloaded. A browser only fetches a
`@font-face` file when a matching glyph actually renders, and the only italic on the site is
`.reg-name`, which is Mira's registered name and off with the Doberman line. Verified: the
italic file is not requested. It will start being fetched, on its own, the day that section
returns.

Do not reinstate the Google Fonts link. If a weight is needed that the variable range does
not cover, the range is what changes.

## Page weight vs repo weight

The repo is ~74MB and that is fine. 20.9MB of it is JPEGs that are the `src` fallback behind
a webp `srcset` on 211 img tags, so they are fetched only by a browser with no webp support,
which is under 1% in 2026. **That is clone and deploy weight, not page weight, and it does
not cost a visitor anything.** Real pages are 130-343KB. Do not "optimise" it by deleting
the fallbacks; if it ever matters, the lever is Cloudflare Pages build time, not visitors.

## Image sizing: the `sizes` hint must be measured, not guessed

`img_tag`'s default was `45vw` while the things using it rendered anywhere from 289px to
852px. A wrong `sizes` costs bytes in one direction and sharpness in the other, and neither
shows up in any check that only looks for broken images.

Named constants now, each measured at 1440 against the real grid track:

| constant | column | renders | hint |
|---|---|---|---|
| `CARD_SIZES` | `.pgrid` 4-up | 289px | 22vw + breakpoints |
| `GAL_SIZES` | gallery tiles | 321px | 22vw + breakpoints |
| `PHOTO_WIDE` | `narrow-left` 1.30fr | 843px | 58vw |
| `PHOTO_LEAN` | `lean-left` 1.15fr | 745px | 46vw |
| `PHOTO_NARROW` | `narrow-right` + flip, .70fr | 403px | 29vw |

The card grid alone was picking a 1000px file for a 289px slot: 372KB where 74KB does, and
the gallery 5.2MB where 979KB does. **When adding a section, pick the constant that matches
its column ratio.** The audit is analytic and cache-proof: resolve each `sizes` attribute at
a viewport width and compare to the element's real rendered width. Do NOT audit by reading
`currentSrc` — the browser keeps a larger cached candidate and will report it, which is how
I first mis-measured this.

**The LCP image must be eager and `fetchpriority="high"`.** Six pages had a lazy-loaded
largest-contentful image, which delays LCP by a whole round trip for nothing. `img_tag`
takes `priority=True`, which sets `fetchpriority` and `decoding=sync` and suppresses
`loading=lazy`. The check: the first image in the viewport wider than 200px must have
`fetchpriority` and must not be lazy, on every page, at every width.

## Adopted puppies stay on the site

`ADOPTED = {"tirzah"}` in `scripts/scaffold.py`. **ADOPTED means spoken for, NOT gone.**
An adopted puppy is still with Hope and goes home on the same date as her littermates, so
no copy may say she is home or with her family. She keeps her card and her page so the
litter reads as a whole rather than looking like puppies went missing, but nothing offers
her for sale. Add a slug to `ADOPTED` and all of this follows:

- no price on the card, and the badge replaces the price in the page's name row too
- an "Adopted!" badge on rose, forest label, 7.08:1
- the reserve block becomes "<name> is adopted", saying she has found her family and goes
  home on the litter date, and pointing at the available puppies and the waitlist
- **the meta and og description drop the price and the deposit.** That is the line search
  results and link previews show, so it is the single easiest place for a spoken-for puppy
  to still look available, and it is the one furthest from anyone's eye while editing.

**Say "Adopted!", not "sold"** (Alex, 2026-08-23). One exception left standing on purpose:
the purchase agreement says the puppy "is sold with the written health guarantee". That is
contract language on a document already flagged for review, and this repo's rule is that
legal terms are not paraphrased without asking. Raise it, do not rewrite it.

**Litter counts are derived, never written.** `M_TOTAL`, `M_AVAILABLE` and `n_word()`.
Adding Tirzah made a hardcoded "Seven puppies" wrong in two places at once, which is the
argument for computing it.

**A marketplace listing's photo set can include the parents.** Four images were attached to
Tirzah's product record and the fourth is Troy, the dam, already published elsewhere on the
site. Scoping the media list to her product was not enough; each photo still had to be
looked at. Publishing that one as "Tirzah" would have been exactly the mistake the standing
rule about not drawing conclusions from photographs is there to prevent.

**`--sage-deep` is 4.34:1 on `--paper`, not 4.53.** The 4.53 figure in the palette notes is
against pure white. On the actual page background it is under the 4.5 floor, so it is fine
for the fine print and labels it is used for and wrong for a paragraph meant to be read.
The faith note uses `--forest` at 11.34:1 for that reason.

## Doberman line is OFF (2026-08-23)

Alex: conflict of interest, temporary, expects it may come back. **Nothing is deleted.**
`SHOW_DOBERMANS = False` in `scripts/scaffold.py` gates all of it: the breed page, the
three puppy pages, nav and footer links, the litter section on puppies.html, Mira and the
sire on our-dogs, the home page doors and parent grid, the gallery filter, the waitlist
option, the purchase-agreement registration clause, the "reading a genetic panel" section
(which is entirely about Mira's panel), and every title, description and OG tag that named
the breed. Flip it to True and re-run to restore all of it.

Photos, the `DOBERMANS` data list and the per-dog facts all stay in the repo. The four
generated pages were `git rm`'d because a file left in the repo stays live on Pages
whether or not anything links to it.

Two traps found doing this. `NAV` was a plain string, not an f-string, so a `{dob(...)}`
call inside it was emitted as **literal text into every page** rather than evaluated —
check that a template is an f-string before putting an expression in it. And a Doberman
photo was being used as generic step imagery on process.html with the alt text "Meet the
puppy", so grepping for the word "Doberman" alone would have missed it; grep the slugs
(`elowen|malcolm|griffin|mira`) too.

Joy stays on the site. Her number and her name remain; only the breed attribution comes
off, so labels read "Hope" and "Joy" rather than "Hope, Munchkins" and "Joy, Dobermans".

**Images are cache-busted per file, from their own bytes.** `asset_v(path)` returns
`?v=<md5[:8]>` and `img_tag` appends it to every srcset candidate and to the src. Keyed on
content rather than the global `V`, so replacing one photograph gives that photograph a new
URL while a stylesheet bump leaves the other thousand-odd image URLs alone. The logo srcset
and the per-puppy carousel thumbnails are hand-written tags and needed it added by hand;
if another hand-written `<img>` appears, it needs `asset_v` too. The check is: every
`src`/`srcset` URL ending in webp/jpg/png carries `?v=`, and there are 1,079 of them.

**Cache-busting must be on the `srcset`, not just the `src`.** The Hope and Joy photo was
replaced in place under the same filenames, with `?v={V}` on the `src` fallback only.
Browsers choose from `srcset`, so every visitor kept being served the cached old picture
and the replacement looked like it had silently failed. Either version every srcset
candidate or give the new file a new name.

**Three sources of space made one gap.** In a `.hic` the heading and the copy are separate
grid rows, so the grid's own `row-gap` lands between them and stacks with the heading's
bottom margin and the paragraph's top margin: 63px where the intended distance was ~14.
`.grid-2.hic{row-gap:0}` and let the margins alone set it.

**An f-string interpolates at the point it is written, not where it is used.** The merged
puppies page built its parents block 22 lines before `M_PARENTS` was assigned, so
`{M_PARENTS}` picked up the module-level `None` and the live page rendered the literal word
"None" under the "Meet their parents" heading. It passed site-checks, because "None" is
valid HTML. When a template pulls in a variable filled in later by `build_pages`, build the
template after that assignment, not before.

**No per-sister attribution while one line is off.** "Hope's litter" and "Joy's litter"
only mean something when there are two. With one, the site presents Hope and Joy together;
the eyebrow reads "Available now". Both strings are on `SHOW_DOBERMANS`.

**Some sections do not need re-centring, they need removing.** Three layouts in a row broke
the same way when the Doberman line went off: `.contact-pair` sized for two tiles,
`.tri` sized for three cards, and the home page breed chooser sized for two doors. The
first two were genuinely layout bugs and got flexible containers. The third was not: a
chooser exists to offer a choice, and with one breed there is no choice, so centring the
single card would have been polish on a section with no job. Ask what the section is FOR
before fixing how it looks. Its markup is stashed verbatim in `BREED_DOORS_HTML` and
emitted through `dob()`, so the flag restores it.

**What the site says about the report must track what the report contains.** It has been
edited twice: first published whole and described as "all 14 pages, nothing left out", then
trimmed to drop the profile summary, breed ancestry and family tree. The description moved
with it each time, and it does not advertise the omission: it says the linked file carries
every health result the panel returned, which is true. Two rules fall out of that. Do not
describe a linked document as complete unless it is, since trimming it later turns accurate
copy into a false claim. And do not state a figure on the page that the linked document no
longer evidences, which is why the ancestry percentages came off when the ancestry page did.

**A trimmed PDF still carries the page numbers it was printed with.** Copying pages 4-14
into a fresh document renumbers nothing, so the published report opened on "page 4 of 14"
and ended on "page 14 of 14", which reads as a document with pages missing. The footers now
read 1-11. They are REDACTED rather than covered with a white box: a box leaves the old
string in the text layer, so ctrl-F, copy-paste and a screen reader would all still say
"page 4 of 14" while the eye read "page 1 of 11". The replacement is set in the report's own
font, extracted from the file with `extract_font` (an Identity-H subset of
UntitledSans-Regular that happens to retain all ten digits); the proof it is the right font
is that it measures the original string at 44.52pt against the 44.53pt the original span
occupies. Script: `scripts/renumber_pdf_footers.py`, which is idempotent: it reads whatever
the footers currently say and rewrites them 1-N, so re-running it after another trim is
safe.

**A page citation is coupled to the page numbers.** our-dogs.html told readers the panel
explains CDDY "on pages 4 and 5", which the renumbering made wrong. It is "pages 1 and 2"
now. Re-check it if the report is ever re-trimmed: a citation pointing at a page that says
something else is worse than no citation.

**Trimming a PDF: use `insert_pdf`, not `delete_pages`.** `delete_pages` leaves the removed
pages' embedded fonts and images in the file. Trimming 3 pages of 14 that way produced
853KB from a 572KB original. Copying the wanted range into a fresh document gives 142KB.

## Photographs: what gets downloaded, and when (2026-08-24)

**`display:none` does not prevent a download.** The browser runs image selection whatever
the element's rendering, so puppies.html was fetching a 52KB hero at `fetchpriority=high`
on a 390px screen and then hiding it with `.hide-mobile`. Measured in the browser, not
assumed. `desktop_only_img()` emits the same photo as a `<picture>` whose `<source>`s carry
every candidate and whose `<img>` deliberately has no `src` and no `srcset`: below the
breakpoint nothing matches, so nothing is requested. The jpg keeps its own `<source>` so a
desktop browser without webp is no worse off than it was.

**The source's media query must be the exact complement of the CSS query.** `.hide-mobile`
hides at `max-width:900px`; pairing it with `min-width:901px` leaves a sliver between 900
and 901px, reachable by zoom or display scaling, where the CSS shows the image and no
source matches it. Visible and unloadable at once. The query is
`not all and (max-width:900px)`, which is true precisely when the CSS rule is false. Move
one, move the other.

**The `<picture>` must BE the layout box and carry the layout classes.** Every placement
rule in this stylesheet is a child combinator: `.hic>.hic-photo`, `.grid-2>*`, `.pgrid>*`.
Wrapping an `<img>` in a `<picture>` inserts a generation between the grid and the image, so
whichever element holds the classes, one of the two goes wrong.

Both failure modes were hit in order, which is worth recording because the second is far
harder to see than the first. Leaving the classes on the `<img>` with a plain wrapper makes
the PICTURE the grid item, `.hic-photo` matches nothing, and the hero drops from 843px to
454px. Adding `picture{display:contents}` to fix that makes the `<img>` the grid ITEM while
those same selectors still see it as a grandchild: `.hic>.hic-photo` still matches nothing,
so the photo is auto-placed into the heading's row, that row grows to the photo's 655px, and
the heading pins to the top with the copy pushed 650px below it. **The widths were all
correct in that state**, which is exactly why checking `heroWidth` and `headWidth` passed it
and Alex's eye caught it instead. Check the vertical arrangement of a `.hic`, not just its
column widths: assert `.hic-copy.top - .hic-head.bottom` is about 14px.

The answer is `picture{display:block;overflow:hidden}` with the classes on the `<picture>`
and `picture>img{width:100%;height:100%;object-fit:cover}` filling it. `overflow:hidden` so
`.framed`'s border-radius clips the photo. `.grid-2 .framed` is a descendant selector and
still applies, giving the picture the 3:2 box the image then fills.

**The cache warmer.** After the load event and an idle main thread, `main.js` quietly
fetches what the next page will need. Two things keep it honest: it only ever requests URLs
the next page would request anyway, so the bytes move earlier rather than multiply, and it
never competes with the current page (nothing before `load`, everything at
`fetchPriority=low`). Skipped entirely on `saveData`, on 2g, and under
`prefers-reduced-data`.

Two mechanisms. `warm_for(path)` in `scaffold.py` emits a JSON island, `<script
type="application/json" id="warm">`, naming documents and `[srcset, sizes, media?]` triples.
And an intent handler warms whatever link the pointer, finger or keyboard actually lands on,
which beats any build-time guess; on a puppy card it also warms the large version of the
photo already in the card, via `data-warm-sizes`.

**The `sizes` hint in a manifest entry must be the DESTINATION page's hint, not the current
page's.** A different hint picks a different file off the same srcset, so the warm request
and the real request become two different URLs: the visit pays twice and feels no faster.
This is why `PUPPY_HERO_SIZES` and `srcset_for()` exist as named, shared things rather than
being spelled out twice.

**Measured cost, analytically rather than from the network panel.** Warming index.html costs
**101KB on a desktop** (14KB document, hero 51KB, four card images) and **203KB on a phone**
(14KB document, four card images at 1000w). The phone costs more because its cards are
near-full-width, so they resolve to a much larger candidate than a desktop's 289px slot. The
knob is `CAP` in the warmer, 4 on a phone and 10 on a desktop; entries already loaded by the
current page are skipped without consuming it.

**Do not measure this with `encodedBodySize`.** It reports the full body size on a cache hit,
which made a run of warmed-but-cached images look like 86KB of fresh transfer. And a
memory-cache hit may produce no Resource Timing entry at all, which makes a working warm
look like it did nothing. Resolve `sizes` against the viewport analytically and sum the files
on disk, the same cache-proof approach the `sizes` audit above uses.

## One listing page while there is one breed (2026-08-23)

`puppies.html` and `munchkin-bernedoodles.html` listed the identical seven cards. The prose
was not duplicated, zero shared sentences, but two thin URLs competing on the same query
with the same product set is the problem regardless. Measured before deciding: 117 words
against 208, same 7 cards, while `what-is-a-munchkin-bernedoodle.html` already owns the
breed keyword properly with 1,039 words.

`puppies.html` survives and absorbs what the litter page carried: the parent lede, the
facts list, the hero photo, the parents block, and the keyword-bearing title. The nav slot
that said "Bernedoodles" now says "Breed Guide" and points at the guide. All of it is on
`SHOW_DOBERMANS`, so restoring Joy's line restores the two-litter index page and the breed
page together.

Watch the per-puppy breadcrumb when toggling: `breed_page` resolves to `puppies` for
Munchkins while the flag is off, and back to `munchkin-bernedoodles` when it is on.

**`scaffold.py` never deletes. Toggling `SHOW_DOBERMANS` to test leaves live pages behind.**
Flipping it to True to verify the restore path regenerated dobermans.html,
munchkin-bernedoodles.html and the three Doberman puppy pages. Flipping back does not
remove them, so five pages the site no longer links were left in the working tree, and got
committed. A file in this repo is live on Pages whether or not anything links to it, so
that briefly republished the whole Doberman line.

site-checks caught it, via the nav-consistency check rather than anything about Dobermans:
the stale pages carried the old nav and no longer matched the rest of the site. Run
site-checks after any flag toggle, and `git rm` the pages the scaffold has stopped
generating.

## Troy's genetic report

`source-files/troy genetic report.pdf`, Wisdom Panel, test date 2026-02-21. **`source-files/`
is gitignored on purpose** — a file committed here is publicly reachable on Pages whether
or not anything links to it, and this one should not go up until Hope has seen what it
says and decided how she wants it presented.

Contains no owner name and no address, so there is no PII barrier to publishing it. What
it contains instead:

- **At Risk: CDDY / IVDD.** One copy of the FGF4 retrogene insertion, autosomal dominant.
  Also one copy of CDPA. See the breed-term rules above; this is the finding that took two
  claims off the site.
- **Clear on 29 conditions, carrier of 0.** That is a genuinely good result to publish and
  is most of the story.
- Breed mix 67% Toy/Mini Poodle, 14% Medium/Standard Poodle, 13% Bernese Mountain Dog,
  5% Bichon Frise, 1% Miniature Schnauzer. **NOT published on the site, and the published
  report no longer contains the ancestry page** (Alex, 2026-08-23). Kept here for
  reference only. Consistent with a multi-gen Bernedoodle, which is mostly Poodle by
  definition. The Bichon and Schnauzer fractions are worth mentioning
  to Hope before anyone else notices them.
- **Predicted ideal adult weight 22-40 lbs**, against the 21 lbs the site states for her.
  Worth a question; it does not change the puppies' estimate, which comes from the actual
  parent weights.

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

**Column ratios available on `.grid-2`**, so the next one does not get invented from
scratch: plain is 1fr 1fr; `lean-left` / `lean-right` are 1.15fr / .85fr, a photo that
leads without dominating; `narrow-left` / `narrow-right` are .70fr / 1.30fr, a strong
asymmetry. At 1440 the wide column comes out about 648px, 745px and 843px respectively.
Every one of them is named in the mobile collapse rule, and any new one must be too.

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

**Centring a heading-plus-copy group against a taller photo takes FOUR rows, not two.**
`.hic` is `grid-template-rows:1fr auto auto 1fr` with the photo spanning `1 / -1`. Both
wrong answers were tried first: `auto auto` puts the leftover height BETWEEN the heading
and its own paragraph, so the heading floats away from it; `auto 1fr` puts all of it under
the copy, so the whole text block pins to the top of the picture and leaves a void below.
Two flexible spacer rows split the slack evenly above and below the pair. When the text is
taller than the photo the spacers compute to 0px and there is nothing to centre, which is
correct, so verify against a section where the photo is the taller side.

**A layout named for its item count breaks when the count changes.** `.contact-pair` was
`grid-template-columns:repeat(2,auto)` and held two tiles. Adding Joy's number made three,
and the third was stranded on its own row against the left edge of an otherwise centred
block. It is a wrapping centred flex row now, which is right for any number of tiles.

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

**Buttons moved onto a dark scrim need inverting, and contrast has to be MEASURED.** The
hero CTAs kept the site palette, forest on paper, while sitting on a 92% forest scrim:
1.05:1 for the filled button's background and 1.05:1 for the ghost button's text AND
border. The ghost button was not dim, it was absent. Every geometric check passed, because
the buttons were the right size in the right place. Over the scrim they are paper on
forest, 10.8:1. When any component moves onto a new background, compute the ratio rather
than looking at it.

**An overlay hero must be designed against the REAL copy length.** Option B was chosen
from a mock whose lede was one line. Production's lede wraps to six or seven, and the
eyebrow and headline to two each, so overlaying the whole copy block put text over 72% of
the photograph starting 28% down. It measured as correct at every check I ran, because
nothing overflowed and everything sat inside the photo. It was still wrong. Only the
eyebrow, headline and buttons go on the picture; the lede sits below it on paper, which is
easier to read anyway. The caption now covers 35-56% depending on width. That band was re-measured after the H1 gained the breed name for search (47 to 68 characters, three lines at 390px): 35% at 430px, 44% at 390, 54% at 320, and 56% at 320 with type forced to 1.25x. The buttons stay inside the photo in every one of those. **Any edit to the hero H1 has to be re-measured across that range**, not just looked at once, because the overlay is sized by the copy.

The mechanism: `.hero-drift>.wrap` and `.hero-copy` are `display:contents` on mobile so
their children become grid items of the drift directly, which is what lets the lede sit in
a row outside the photo's row span. Each item then carries its own `padding-inline`, since
display:contents drops the wrap that used to provide the gutter.

**Email addresses cause horizontal overflow. Handle them once, globally.** Long, no break
opportunity. Fixed for `.facts .v` on the contact page, then it reappeared in the footer
in the 901-1000px band where the footer column is 169px and the address is 230px. It is
now `a[href^="mailto:"]{overflow-wrap:anywhere}` plus `min-width:0` on the footer grids.

**Audit the width just ABOVE a breakpoint, not just below.** 900 and 1280 were both clean
while 901 overflowed by 33px. The sweep worth running is 320/360/394/430/600/768/899/901/
940/1000/1100/1280/1600/1920 across the busiest pages, which is 112 combinations and takes
one call.

**Measure a range, not one width.** 390px alone was clean while 320px overflowed and
768px was fine. The audit that matters runs every page at 320 / 390 / 414 checking for
horizontal overflow, uncollapsed multi-column grids, and CTA lines that do not fill
their container, then re-checks 1280 and 1920 to confirm the desktop treatment and the
asymmetric columns survived. `.parent-grid` is `auto-fit`, so 2 to 3 columns at 768px
and above is correct, not a missed collapse.
