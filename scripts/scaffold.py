#!/usr/bin/env python3
"""Phase 1 scaffold for blessyourpaws-website-repo.

Run scripts/prep_images.py FIRST (it splits the parents out of the puppy
galleries and writes img/photo-counts.json), then run this.

Re-running OVERWRITES every generated page, so fold hand edits back into this
script rather than editing the HTML.

Draft mode: noindex on every page, robots.txt closed, until launch.
"""
import functools, hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

V = 55
BASE = "https://alexharper24.github.io/blessyourpaws-website-repo"
BRAND = "Bless Your Paws"        # title-tag suffix; the full name is "Bless Your Paws Puppies"
PHONE_DISPLAY = "(574) 377-8023"          # Hope, Munchkin Bernedoodles
PHONE_HREF = "tel:5743778023"
JOY_PHONE_DISPLAY = "(574) 265-1060"      # Joy, Dobermans. Confirmed by Alex 2026-08-23
JOY_PHONE_HREF = "tel:5742651060"
SMS_HREF = "sms:5743778023"
EMAIL = "info@blessyourpawspuppies.com"
AREA = "Warsaw and Winona Lake, Indiana"
COUNTS = json.load(open("img/photo-counts.json"))
# a puppy whose best head-on shot is not the first file in the gallery
PRIMARY = {"malcolm": 2}

def lead(slug):
    """Gallery stem to use as the card and hero image for a puppy."""
    return "%s-%02d" % (slug, PRIMARY.get(slug, 1))

MUNCHKINS = [
    ("joshua",  "Joshua",  "Boy",  "Red and white parti", ""),
    ("eden",    "Eden",    "Girl", "Red with white",      ""),
    ("havilah", "Havilah", "Girl", "Blue merle phantom",  ""),
    ("jordan",  "Jordan",  "Boy",  "Blue merle parti",    "The biggest of the litter so far."),
    ("caleb",   "Caleb",   "Boy",  "Red and white parti", ""),
    ("shiloh",  "Shiloh",  "Boy",  "Blue merle phantom",  ""),
    ("jericho", "Jericho", "Boy",  "Blue merle parti",    ""),
    ("tirzah",  "Tirzah",  "Girl", "Black phantom",       ""),
]
# Puppies that are spoken for. ADOPTED means reserved by a family, NOT already gone: they
# go home on the same date as their littermates. They stay on the site so the litter reads
# as a whole rather than looking like one went missing, and they are never offered for sale.
ADOPTED = {"tirzah"}

def n_word(n):
    return {1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",
            9:"Nine",10:"Ten",11:"Eleven",12:"Twelve"}.get(n, str(n))

M_TOTAL     = len(MUNCHKINS)
M_AVAILABLE = len([m for m in MUNCHKINS if m[0] not in ADOPTED])
DOBERMANS = [
    ("elowen",  "Elowen",  "Girl", "Black and rust", "Ready for any adventure, and working on crate and leash training."),
    ("malcolm", "Malcolm", "Boy",  "Black and rust", "Eager to please, and doing well learning to sit and stay."),
    ("griffin", "Griffin", "Boy",  "Black and rust", "An outgoing boy who makes friends with everyone."),
]
# ---------------------------------------------------------------------------
# Doberman line: OFF since 2026-08-23 (Alex, conflict of interest). Nothing is
# deleted. Flip this to True and re-run to restore the whole line: the breed page,
# the three puppy pages, the nav and footer links, the litter section on
# puppies.html, Mira and the sire on our-dogs, the gallery filter, and the prose
# that names the breed. Photos and data stay in the repo either way.
SHOW_DOBERMANS = False
D_LIST = list(DOBERMANS) if SHOW_DOBERMANS else []
def dob(html):
    """Emit this markup only while the Doberman line is on."""
    return html if SHOW_DOBERMANS else ""

M_PRICE, D_PRICE, DEPOSIT = 2000, 2200, 500
M_BORN, M_HOME = "July 22, 2026", "September 16, 2026"
D_BORN, D_HOME = "April 14, 2026", "Ready now"

CHIP_DRAFT  = '<span class="chip chip-draft">Draft, confirm before launch</span>'
CHIP_SAMPLE = '<span class="chip chip-sample">Sample copy, waiting on their words</span>'
CHIP_PHOTO  = '<span class="chip chip-draft">Photo coming</span>'
M_SIZE = "15 to 20 lbs"
# The provenance changed with the figure: 15 to 20 is narrower than anything the parents'
# weights alone imply, so the chip no longer claims to be derived from them. It still
# flags the number for confirmation before launch.
SIZE_DRAFT  = ('<span class="chip chip-draft">Expected size, confirm before launch</span>')

M_KIT = ["Vaccination and health record", "Examination by our vet",
         "Small bag of the food they know", "Collar and leash", "A toy"]
D_KIT = ["AKC registration", "One year genetic health guarantee",
         "Vaccination and health record", "Vet exam and report", "Microchipped",
         "Tail docked", "Dew claws removed", "Small bag of food", "A toy", "A blanket"]

CSS = """/* Bless Your Paws Puppies - v2
   Character: a pressed-flower garden album. Blush paper, forest ink, sage stems,
   seed-packet cards. Wide gallery-first layout: the puppies are the product, so
   photography gets the room. Deliberately NOT Kingdom Family Companions'
   cream/espresso ledger. */

@font-face{font-family:"Lora";font-style:normal;font-weight:400 700;
  font-display:swap;src:url("fonts/lora-variable.woff2") format("woff2")}
@font-face{font-family:"Lora";font-style:italic;font-weight:400 600;
  font-display:swap;src:url("fonts/lora-italic.woff2") format("woff2")}
@font-face{font-family:"Mulish";font-style:normal;font-weight:400 700;
  font-display:swap;src:url("fonts/mulish-variable.woff2") format("woff2")}

:root{
  --forest:#223d2c; --forest-soft:#34523f;
  --sage:#7f8e79; --sage-deep:#6d7a68; --sage-light:#a8b89e;
  --rose:#feb5bc; --pink-pale:#fbc4db;
  --paper:#fdf9f9; --paper-raise:#faf2f1; --rule:#e4d7d6;
  --draft:#8a5512; --draft-bg:#f8ecd9;
  --maxw:1560px;
  color-scheme: light only;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--forest);
  font-family:"Mulish",system-ui,sans-serif;font-size:17px;line-height:1.65}
/* light-mode lock: iOS Safari inverts unlocked pages into dark-on-dark */
@media (prefers-color-scheme: dark){
  :root{--paper:#fdf9f9;--forest:#223d2c}
  body{background:var(--paper);color:var(--forest)}
}
img{max-width:100%;height:auto;display:block}
/* img{display:block} above outranks the UA stylesheet's [hidden]{display:none},
   which silently un-hides carousel slides and stacks every photo. restore it. */
[hidden]{display:none !important}

/* Fraunces ships wonky f/g/y by default. WONK 0 turns the swashes off, which is
   the fix for the odd-looking f. SOFT rounds the terminals a little. */
/* Third display face. Fraunces draws a hooked descending f; Petrona has an
   unconventional J. Lora is a transitional serif with entirely normal f, g, j, y
   and J, which is what this client needs. Ligatures and swashes off as well. */
h1,h2,h3,.display,.packet-name,.price,.q-btn{font-family:"Lora",Georgia,serif;
  font-feature-settings:"liga" 0,"dlig" 0,"swsh" 0,"calt" 0}
h1,h2,h3{font-weight:600;line-height:1.14;margin:0 0 .5rem;text-wrap:balance;
  letter-spacing:-.01em}
h1{font-size:clamp(2rem,3.6vw,3.1rem)}
h2{font-size:clamp(1.55rem,2.3vw,2.2rem)}
h3{font-size:1.2rem}
p{margin:0 0 1rem}
a{color:var(--forest)}
.wrap{width:min(94%,var(--maxw));margin-inline:auto}
/* grid children default to min-width:auto, so a wide child can push a track past
   the viewport. this stops the sideways scroll. */
.pgrid>*,.grid-2>*,.grid-3>*,.foot-grid>*,.puppy-top>*{min-width:0}
.eyebrow{font-size:.74rem;letter-spacing:.17em;text-transform:uppercase;
  color:var(--sage-deep);margin:0 0 .5rem;font-weight:700}
.lede{font-size:clamp(1.05rem,1.25vw,1.22rem);color:var(--forest-soft)}
.fine{font-size:.88rem;color:var(--sage-deep)}
.center{text-align:center}
.prose{max-width:70ch}

.chip{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.05em;
  padding:.2rem .55rem;border-radius:3px;vertical-align:.12em;margin-left:.35rem}
.chip-draft{background:var(--draft-bg);color:var(--draft);border:1px dashed var(--draft)}
.chip-sample{background:var(--pink-pale);color:var(--forest);border:1px dashed var(--sage)}

/* ---------- header ---------- */
.site-head{background:var(--paper);border-bottom:1px solid var(--rule);
  position:sticky;top:0;z-index:40}
.head-row{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  min-height:82px}
.brand{display:flex;align-items:center;text-decoration:none;flex:none}
/* the primary lockup is 1596x474, so ~3.4:1. At 76px it stood 6px shy of the 82px
   bar and read as though it were bursting out of it. 56px leaves 13px of air above
   and below, and the two smaller breakpoints hold that same 13px. */
.brand img{height:56px;width:auto;display:block}
.nav{display:flex;align-items:center;gap:.1rem;flex-wrap:wrap;justify-content:flex-end}
.nav a{text-decoration:none;padding:.5rem .6rem;border-radius:3px;font-size:.94rem;
  white-space:nowrap}
.nav a:hover{background:var(--paper-raise)}
.nav a.nav-cta{background:var(--forest);color:var(--paper);margin-left:.4rem;
  padding:.6rem 1rem}
.nav a.nav-cta:hover{background:var(--forest-soft)}
.nav-toggle{display:none;background:none;border:1.5px solid var(--forest);
  border-radius:3px;padding:.5rem .7rem;font:inherit;font-weight:700;
  color:var(--forest);cursor:pointer;min-height:44px}

/* ---------- hero: photo drifts behind the copy ----------
   The image is oversized and anchored right, then its left edge is dissolved with
   a mask so it fades into the paper underneath the headline instead of stopping at
   a hard edge. Copy sits above it, over plain paper, so contrast is never at risk. */
.hero{padding:0;position:relative;overflow:hidden;isolation:isolate}
/* the source is 3:2. at 1026x634 the frame was wider than that, so cover was
   trimming the puppy top and bottom. a taller frame lands nearer 3:2 and keeps him
   whole. */
.hero-drift{position:relative;display:grid;align-items:center;
  min-height:clamp(24rem,34vw,32rem)}
/* every direct child shares the one cell. the grid child here is the .wrap, NOT
   .hero-copy, so targeting .hero-copy left the .wrap auto-placed into row 2 and
   stacked the copy underneath the photo. */
.hero-drift>*{grid-area:1/1}
/* width stays proportional so the photo always reaches back behind the copy. a
   fixed rem cap broke the drift at wide viewports: the photo pinned right while the
   copy stayed in the centred wrap, and the two separated. 160vh at 3:2 keeps the
   height near a viewport so it cannot run away vertically either. */
/* 16:9 rather than the source 3:2, which buys a hero roughly a sixth shorter at the
   same width with the fade intact. The height it loses is blanket and background, not
   the puppy.
   object-position is pinned to 0% deliberately, and it is the only value that should
   be used here. havilah-01 is 1731x1154 and the top of his head is 5.4% down the
   frame, so the source itself carries very little headroom. Cover shows 84.4% of the
   source height, so every percent of object-position eats 0.19% of that headroom:
   at 22% the crown sat 2.3% below the top edge and read as though he were about to
   hit his head, and by 34% it was clipped outright. At 0% the crown sits 6.4% down,
   which is the most this photograph can give. More air than that needs a different
   photograph, not a different crop. */
.hero-photo{justify-self:end;align-self:center;
  width:min(74%,178vh);aspect-ratio:16/9;z-index:0;pointer-events:none}
.hero-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 0%;
  -webkit-mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.25) 14%,
    #000 42%,#000 100%);
  mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.25) 14%,
    #000 42%,#000 100%)}
/* a narrower measure: the headline was setting two very long lines */
.hero-drift>.wrap{z-index:1;align-self:center}
.hero-copy{position:relative;width:min(33rem,46%);
  padding:clamp(2.25rem,4vw,3.5rem) 0}
.hero-copy .lede{max-width:30rem}
.hero-copy h1{text-shadow:0 1px 0 var(--paper)}
/* older engines without mask-image get a plain right-hand photo rather than a
   full-bleed image with copy on top of it */
@supports not ((mask-image:linear-gradient(#000,#000)) or (-webkit-mask-image:linear-gradient(#000,#000))){
  .hero-photo{width:54%}
}

.hero-split{display:grid;grid-template-columns:.68fr 1.32fr;gap:clamp(2rem,4vw,4rem);
  align-items:center}
/* desktop_only_img wraps its <img> in a <picture> so a phone never downloads a photo it
   hides. The PICTURE therefore has to BE the layout box and carry the layout classes,
   because every placement rule here is a child combinator: .hic>.hic-photo, .grid-2>*,
   .pgrid>*. display:contents was tried first and is wrong for exactly that reason. It
   makes the <img> the grid ITEM while those selectors still see it as a grandchild, so
   .hic>.hic-photo matched nothing, the photo was auto-placed into the heading's row, and
   that row grew to the height of the picture: the heading pinned to the top and the copy
   pushed 650px below it. The layout looked broken in a way that measuring widths did not
   catch, because the widths were all correct.
   overflow:hidden so .framed's border-radius clips the photo, and the <img> simply fills
   whatever box the classes on the picture produce. */
picture{display:block;overflow:hidden}
picture>img{display:block;width:100%;height:100%;object-fit:cover}
.framed{width:100%;max-width:100%;border-radius:6px;border:1.5px solid var(--forest);
  box-shadow:0 2px 0 var(--sage-light)}
.hero-split .framed{aspect-ratio:3/2;object-fit:cover}
/* section imagery: give photos real presence, they are the product */
.grid-2 .framed{aspect-ratio:3/2;object-fit:cover}
/* a portrait original keeps a portrait frame. cropping a 3:4 photo of people to
   3:2 cuts off either their heads or their torsos. */
/* a 16:9 original keeps a 16:9 frame, so none of the subject is cropped away */
.framed.wide16{aspect-ratio:1672/941;object-fit:cover}
/* .78/1.22 puts a feature photo near 780px in a 1339 wrap. .62/1.38 gave 894px,
   which overwhelmed the paragraph beside it. */
/* 1.30fr rather than 1.22fr: the photographs sit in this column and were asked to be
   larger. Both variants move together so the About photo and the one below it stay the
   same size as each other. */
.grid-2.narrow-left{grid-template-columns:.70fr 1.30fr}
/* a softer lean than narrow-left/right, for a photo that should lead without dominating */
.grid-2.lean-left{grid-template-columns:1.15fr .85fr}
.grid-2.lean-right{grid-template-columns:.85fr 1.15fr}
/* narrow-RIGHT means the right column is the narrow one, so the photo-left rows
   get the wide half. It had been left identical to narrow-left, which is why the
   inverted rows put their photo in the small column. */
.grid-2.narrow-right{grid-template-columns:1.30fr .70fr}
.btn{display:inline-flex;align-items:center;text-decoration:none;border-radius:3px;
  font-weight:700;padding:.75rem 1.35rem;border:1.5px solid var(--forest);
  font-size:1rem;min-height:48px}
.btn-primary{background:var(--forest);color:var(--paper)}
.btn-primary:hover{background:var(--forest-soft)}
/* forest on rose measures 7.08:1. White on rose is 1.67:1 and is forbidden here, so a
   pink button keeps a forest label. */
.btn-pink{background:var(--rose);color:var(--forest);border-color:var(--rose)}
.btn-pink:hover{background:var(--pink-pale);border-color:var(--pink-pale)}
.btn-ghost{background:transparent;color:var(--forest)}
.btn-ghost:hover{background:var(--paper-raise)}
.btn-row{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.4rem}
.btn-row>.btn{text-align:center}
/* a page title living inside the left column of a feature row, so the headline sits
   beside the photo rather than stacked above the whole row */
.col-title{margin-bottom:1.25rem}
.col-title h1,.col-title h2{margin-bottom:.35rem}
.col-title .eyebrow{margin-bottom:.4rem}

/* heading on the left, action on the right, on one baseline. for sections where a
   closing button under the grid read as parked rather than placed. */
.section-head{display:flex;align-items:flex-end;justify-content:space-between;
  gap:1.5rem;flex-wrap:wrap;margin-bottom:1.75rem}
.section-head>div{min-width:0}
.section-head h2{margin-bottom:.25rem}
.section-head .btn{flex:none}

/* a section-closing action, tied to the block above it by a rule rather than
   floating loose underneath */
.section-cta{display:flex;justify-content:center;align-items:center;gap:1rem;
  margin-top:clamp(1.75rem,3vw,2.75rem);padding-top:clamp(1.5rem,2.5vw,2rem);
  border-top:1px solid var(--rule);flex-wrap:wrap}
.section-cta p{margin:0;color:var(--sage-deep);font-size:.95rem}
.band-forest .section-cta{border-top-color:rgba(253,249,249,.28)}
.band-pink .section-cta,.band-raise .section-cta{border-top-color:var(--sage-light)}

.sprig{display:block;margin:0 auto;color:var(--sage)}

section{padding:clamp(2.5rem,4vw,4rem) 0}
.band-forest{background:var(--forest);color:var(--paper)}
.band-forest h2,.band-forest h3{color:var(--paper)}
.band-forest .eyebrow{color:var(--rose)}
.band-forest p,.band-forest li{color:#e9ded9}
.band-forest a{color:var(--pink-pale)}
.band-pink{background:var(--pink-pale)}
/* a coloured band whose height is set by a tall photo reads as a big slab. this
   trims the vertical padding so the colour hugs the content. */
section.band-tight{padding-top:clamp(1.5rem,2.5vw,2.25rem);
  padding-bottom:clamp(1.5rem,2.5vw,2.25rem)}
.band-tight .grid-2{align-items:center}
.band-raise{background:var(--paper-raise)}

/* ---------- cards ---------- */
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:clamp(1.25rem,2vw,2rem)}
/* an exact column count so a small litter spans the full width instead of
   clustering at the left with dead space beside it. these MUST be unwound on
   narrow screens: pinned at 4 columns on a phone they force a horizontal scroll. */
@media (min-width:1100px){
  .pgrid.cols-3{grid-template-columns:repeat(3,1fr)}
  .pgrid.cols-4,.pgrid.cols-7{grid-template-columns:repeat(4,1fr)}
}
@media (min-width:700px) and (max-width:1099px){
  .pgrid.cols-3,.pgrid.cols-4,.pgrid.cols-7{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:699px){
  .pgrid,.pgrid.cols-3,.pgrid.cols-4,.pgrid.cols-7{grid-template-columns:1fr}
}
.grid-2>*{min-width:0}
/* ---- heading, photo, copy -------------------------------------------------
   A section stacked on a phone should read heading, then the photo, then the copy.
   Left to auto-placement it reads either heading-copy-photo or photo-heading-copy
   depending on which column comes first in the source, and both are wrong: the first
   buries the photo under a wall of text, the second opens with a photo of nothing in
   particular before you know what you are looking at.

   So the source order IS heading, photo, copy, and mobile needs no rules at all. The
   two-column desktop arrangement is scoped with min-width rather than set
   unconditionally and undone below 900px. That is deliberate and it is the third time
   this bit: an undo rule like `.hic>*` loses on specificity to `.hic>.hic-head`, and a
   surviving `grid-column:2` then creates an implicit second track that eats the whole
   row. Scope desktop-only placement to desktop and there is nothing to override.

   Add `hic-flip` when the photo belongs in the first column instead of the second. */
/* `.grid-2` sets align-items:center and is declared after this block, so a bare
   `.hic` at (0,1,0) loses and every item was vertically centred in its row, which is
   what pushed a heading away from its own paragraph. Compound selector to win. */
.grid-2.hic{align-items:start}
/* the copy blocks sit at the top of their own content-sized rows; the photo centres
   itself across the full span, which is what matters when the TEXT is the taller side
   and the spacer rows have collapsed to zero */
.hic>.hic-head,.hic>.hic-copy{align-self:start}
/* the heading and the copy are separate rows here, so the grid's row-gap lands between
   them and stacks with the heading's bottom margin and the paragraph's top margin. Zero
   the row-gap and let the margins alone set the distance. */
.grid-2.hic{row-gap:0}
.hic>.hic-head{margin-bottom:.9rem}
.hic>.hic-head.col-title{margin-bottom:.9rem}
.hic>.hic-copy>:first-child{margin-top:0}
.hic>.hic-photo{align-self:center}
@media (min-width:901px){
  /* Four rows: a flexible spacer, the heading, the copy, another flexible spacer. The
     two 1fr rows split the leftover height of the spanning photo evenly, which centres
     the heading and copy as a GROUP while leaving them adjacent to each other.
     `auto 1fr` was wrong in the other direction: it put all the slack in the copy's row
     and pinned the text to the top of the picture. Plain `auto auto` is wrong too, since
     the slack then lands between the heading and its own paragraph. */
  .hic{grid-template-rows:1fr auto auto 1fr}
  .hic>.hic-head{grid-column:1;grid-row:2}
  .hic>.hic-copy{grid-column:1;grid-row:3}
  .hic>.hic-photo{grid-column:2;grid-row:1 / -1}
  .hic-flip>.hic-head{grid-column:2;grid-row:2}
  .hic-flip>.hic-copy{grid-column:2;grid-row:3}
  .hic-flip>.hic-photo{grid-column:1;grid-row:1 / -1}
}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,3vw,3rem);
  align-items:center}
.grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:clamp(1.25rem,2vw,2rem)}
.packet{position:relative;background:#fff;border:1.5px solid var(--forest);
  border-radius:4px;padding:11px;display:flex;flex-direction:column;height:100%}
.packet::before{content:"";position:absolute;inset:5px;border:1px dashed var(--sage);
  border-radius:2px;pointer-events:none}
.packet img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:2px}
/* parent originals run from 0.75 to 1.42 aspect. a square frame crops both
   orientations gently, where a 4/5 frame gutted the landscape ones. */
.packet.parent img{aspect-ratio:1/1;object-position:50% 30%}
.parent-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:clamp(1.25rem,2vw,2rem);align-items:stretch}
.parent-grid.row-4{grid-template-columns:repeat(4,1fr)}
.parent-grid .packet-body{gap:.2rem;flex:1;display:flex;flex-direction:column;
  padding:.9rem .7rem .55rem}
/* the facts table fills, the note sits on the floor of the card, so a card with
   three rows and a card with five still line their notes up */
.parent-grid .facts{margin:.5rem 0 0}
.parent-grid .facts li{padding:.3rem 0;font-size:.9rem}
.parent-grid .facts li:last-child{border-bottom:none}
.parent-grid .packet-name{margin-bottom:.1rem}
.parent-grid .packet-meta{margin-bottom:.15rem}
.parent-grid .dogmeta{margin-bottom:.2rem}
.parent-grid .pnote{margin-top:auto;padding-top:.6rem;font-size:.83rem;
  line-height:1.45;color:var(--sage-deep);border-top:1px solid var(--rule)}
.parent-grid .pnote:empty{display:none}
.dogmeta{font-size:.86rem;letter-spacing:.09em;text-transform:uppercase;
  color:var(--sage-deep);font-weight:700;margin:0 0 .35rem}
.packet-body{padding:1rem .6rem .5rem;display:flex;flex-direction:column;gap:.2rem;
  flex:1}
.packet-name{font-size:1.35rem;font-weight:700;margin:0}
.packet-meta{font-size:.9rem;color:var(--sage-deep);margin:0}
.packet-row{display:flex;justify-content:space-between;align-items:baseline;
  gap:.5rem;margin-top:auto;padding-top:.6rem}
.price{font-size:1.2rem;font-weight:700}
.status{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--forest);background:var(--sage-light);padding:.2rem .55rem;border-radius:3px}
/* forest on rose is 7.08:1. An adopted card has no price, so the badge sits alone and
   carries the row on its own. */
.status-adopted{background:var(--rose)}
.packet-row:has(> .status-adopted:only-child){justify-content:flex-start}
.packet-link.is-adopted .packet{border-style:solid}
.packet-link.is-adopted img{filter:saturate(.92)}
a.packet-link{text-decoration:none}
a.packet-link:hover .packet{border-color:var(--sage-deep)}

/* flex column so the body fills the card and the two cards close on the same line even
   if one caption wraps at a width the other does not */
.door{display:flex;flex-direction:column;text-decoration:none;
  border:1.5px solid var(--forest);border-radius:6px;overflow:hidden;background:#fff}
.door-body{flex:1}
.door img{width:100%;aspect-ratio:3/2;object-fit:cover}
/* The dead band under the last line was the paragraph's own bottom margin sitting on
   top of the padding, not the padding alone. Padding on the parent stops the margin
   collapsing out, so it has to be removed explicitly. */
.door-body{padding:1.15rem 1.4rem 1.25rem}
.door-body>:last-child{margin-bottom:0}
.door:hover{border-color:var(--sage-deep)}

/* ---------- facts ---------- */
.facts{list-style:none;margin:0 0 1.25rem;padding:0;border-top:1px solid var(--rule)}
.facts li{display:flex;justify-content:space-between;gap:1rem;padding:.6rem 0;
  border-bottom:1px solid var(--rule);font-size:.97rem}
a[href^="mailto:"]{overflow-wrap:anywhere}
.foot-grid>*,.foot-top>*{min-width:0}

/* flex and grid children default to min-width:auto, so an unbreakable value with no
   break opportunity in it sets the min-content width of whatever column it sits in.
   The email address did exactly that and pushed the contact page 48px wider than a
   320px screen, dragging the photo beside it out with the column. */
.facts li{min-width:0}
.facts .k{color:var(--sage-deep)}
.facts .v{text-align:right;font-weight:700;min-width:0;overflow-wrap:anywhere}
.checklist{list-style:none;margin:0;padding:0}
.checklist li{padding:.4rem 0 .4rem 1.7rem;position:relative;font-size:.97rem}
.checklist li::before{content:"";position:absolute;left:0;top:.8em;width:11px;
  height:6px;border-left:2px solid var(--sage);border-bottom:2px solid var(--sage);
  transform:rotate(-45deg)}

/* ---------- puppy page carousel ---------- */
.puppy-top{display:grid;grid-template-columns:1.45fr 1fr;
  gap:clamp(1.5rem,3vw,3rem);align-items:stretch}
.puppy-info{display:flex;flex-direction:column}
.name-row{display:flex;align-items:baseline;justify-content:space-between;
  gap:1rem;flex-wrap:wrap}
.name-row h1{margin:0}
.name-row .price{font-size:clamp(1.6rem,2.4vw,2.1rem);white-space:nowrap}
.puppy-info .facts{margin-bottom:1rem}
.puppy-info .facts li{padding:.42rem 0;font-size:.94rem}
.puppy-info .reserve{margin:1rem 0}
.puppy-info .share-row{margin-top:auto;padding-top:1.25rem}
.carousel{position:relative}
.frame{position:relative;border:1.5px solid var(--forest);border-radius:6px;
  overflow:hidden;background:#fff}
.frame img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
/* stacked slides, crossfaded. the first keeps position:relative so the frame still
   derives its height from a real image rather than collapsing. */
.frame img{position:absolute;inset:0;height:100%;opacity:0;
  transition:opacity .7s ease-in-out}
.frame img:first-of-type{position:relative}
.frame img.is-on{opacity:1;z-index:1}
@media (prefers-reduced-motion: reduce){
  .frame img{transition:none}
}
.carousel{display:flex;flex-direction:column}
.cnav{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;
  border-radius:50%;border:1.5px solid var(--forest);background:rgba(253,249,249,.92);
  cursor:pointer;font-size:1.3rem;line-height:1;color:var(--forest);z-index:2}
.cprev{left:12px} .cnext{right:12px}
.cnav:hover{background:var(--forest);color:var(--paper)}
.count{position:absolute;bottom:12px;right:12px;background:rgba(34,61,44,.85);
  color:var(--paper);font-size:.8rem;padding:.25rem .6rem;border-radius:3px;z-index:2}
.cthumbs{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.7rem}
.cthumbs button{padding:0;border:1.5px solid var(--rule);border-radius:3px;
  background:none;cursor:pointer;width:84px;height:84px;overflow:hidden}
.cthumbs button[aria-current="true"]{border-color:var(--forest);border-width:2.5px}
.cthumbs img{width:100%;height:100%;object-fit:cover}

/* ---------- gallery ---------- */
.gal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
  gap:1.25rem}
.gal-grid a{display:block;border:1.5px solid var(--rule);border-radius:4px;
  overflow:hidden}
.gal-grid a:hover{border-color:var(--forest)}
.gal-grid img{aspect-ratio:1/1;object-fit:cover}
.filter-row{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.25rem;
  align-items:stretch}
/* the select is styled to match the buttons beside it exactly, so the row reads as
   one control group rather than a dropdown bolted on */
.filter-select{position:relative;display:inline-flex}
.filter-select select{font:inherit;font-size:.94rem;padding:.5rem 2.4rem .5rem 1.1rem;
  border:1.5px solid var(--forest);background:none;border-radius:3px;
  color:var(--forest);min-height:44px;cursor:pointer;appearance:none;
  -webkit-appearance:none}
.filter-select::after{content:"";position:absolute;right:1rem;top:50%;
  width:8px;height:8px;margin-top:-6px;pointer-events:none;
  border-right:2px solid var(--forest);border-bottom:2px solid var(--forest);
  transform:rotate(45deg)}
.filter-select select:focus-visible{outline:3px solid var(--sage);outline-offset:2px}
.filter-select.on select{background:var(--forest);color:var(--paper)}
.filter-select.on::after{border-color:var(--paper)}
.visually-hidden{position:absolute;width:1px;height:1px;overflow:hidden;
  clip-path:inset(50%);white-space:nowrap}
.filter-row button{font:inherit;font-size:.94rem;padding:.5rem 1.1rem;cursor:pointer;
  border:1.5px solid var(--forest);background:none;border-radius:3px;
  color:var(--forest);min-height:44px}
.filter-row button.cur{background:var(--forest);color:var(--paper)}

/* ---------- reserve ---------- */
.reserve{background:var(--paper-raise);border:1px dashed var(--sage);border-radius:4px;
  padding:1.4rem;margin:1.5rem 0}
.pay-row{display:flex;gap:.6rem;flex-wrap:wrap;margin:.85rem 0 .5rem}
.guard-msg{display:none;background:var(--pink-pale);border-radius:3px;
  padding:.8rem 1rem;font-size:.92rem;margin-top:.6rem}
.guard-msg.show{display:block}

/* ---------- share row ---------- */
.share-row{display:flex;gap:.8rem;margin-top:1.75rem;align-items:center;flex-wrap:wrap}
.share-lbl{font-size:.76rem;font-weight:700;letter-spacing:.17em;
  text-transform:uppercase;color:var(--sage-deep)}
.share-row a{color:var(--sage-deep);display:inline-flex;width:44px;height:44px;
  align-items:center;justify-content:center;border:1.5px solid var(--rule);
  border-radius:3px}
.share-row a:hover{color:var(--paper);background:var(--forest);border-color:var(--forest)}

/* ---------- let's chat launcher ---------- */
.chat-fab{position:fixed;right:18px;bottom:18px;z-index:60;display:inline-flex;
  align-items:center;gap:.5rem;background:var(--forest);color:var(--paper);
  border:none;border-radius:999px;padding:.8rem 1.25rem;font:inherit;font-weight:700;
  cursor:pointer;box-shadow:0 6px 18px rgba(34,61,44,.28);min-height:48px}
.chat-fab:hover{background:var(--forest-soft)}
.chat-fab svg{width:18px;height:18px}
.chat-panel{position:fixed;right:18px;bottom:82px;z-index:60;display:none;
  width:min(92vw,22rem);background:#fff;border:1.5px solid var(--forest);
  border-radius:6px;padding:1.35rem;box-shadow:0 12px 32px rgba(34,61,44,.22)}
.chat-panel.open{display:block}
.chat-panel h3{font-size:1.25rem;margin-bottom:.3em}
.chat-panel p{font-size:.92rem;color:var(--forest-soft);margin-bottom:1rem}
.chat-panel .row{display:flex;gap:.8rem;align-items:baseline;padding:.55rem 0;
  border-top:1px solid var(--rule)}
.chat-panel .row .lbl{font-size:.72rem;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--sage-deep);min-width:4.6rem}
.chat-panel .row a{font-weight:700;overflow-wrap:anywhere}

/* ---------- forms ---------- */
form{display:flex;flex-direction:column;gap:1rem;max-width:36rem}
/* a bordered card keeps the form visually anchored beside a facts column instead
   of floating as loose fields */
.formcard{background:var(--card,#fff);border:1.5px solid var(--rule);border-radius:5px;
  padding:clamp(1.25rem,2vw,1.75rem)}
.formcard form{max-width:none;gap:.9rem}
.formcard .field{display:flex;flex-direction:column;gap:.3rem}
.formcard .facts{margin-bottom:.75rem}
/* a column that stacks a card above a photo needs its own rhythm */
.grid-2>div>.formcard+.framed,.grid-2>div>.formcard+picture,
.contact-grid>div>.formcard+.framed,.contact-grid>div>.formcard+picture{margin-top:1.25rem}

/* contact: two explicit rows so the right column starts level with the lede rather
   than with the page title above it */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;
  gap:0 clamp(1.5rem,3vw,3rem);align-items:start}
.cg-head{grid-column:1;grid-row:1;margin-bottom:1.25rem}
.cg-gap{grid-column:2;grid-row:1}
.contact-grid>div:nth-of-type(3){grid-column:1;grid-row:2}
.contact-grid>div:nth-of-type(4){grid-column:2;grid-row:2}
@media (max-width:900px){
  .contact-grid{grid-template-columns:1fr;gap:0}
  .cg-gap{display:none}
  .contact-grid>div:nth-of-type(3),.contact-grid>div:nth-of-type(4){
    grid-column:1;grid-row:auto}
  .contact-grid>div:nth-of-type(4){margin-top:1.5rem}
}
.formcard .facts li:last-child{border-bottom:none}
.formcard button{margin-top:.4rem;justify-content:center}
label{font-size:.9rem;font-weight:700}
input,select,textarea{font:inherit;padding:.7rem .8rem;
  border:1.5px solid var(--sage-deep);border-radius:3px;background:#fff;width:100%;
  color:var(--forest);min-height:48px}
textarea{min-height:8rem}

/* ---------- process steps: five across, photo over caption ---------- */
.steps-row{display:grid;grid-template-columns:repeat(5,1fr);
  gap:clamp(1rem,1.6vw,1.75rem);align-items:start}
.step{display:flex;flex-direction:column;gap:.75rem}
.step-media img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:6px;
  border:1.5px solid var(--forest);box-shadow:0 2px 0 var(--sage-light)}
.step-num{display:inline-flex;align-items:center;justify-content:center;
  width:2.1rem;height:2.1rem;border-radius:50%;background:var(--forest);
  color:var(--paper);font-family:"Lora",Georgia,serif;font-size:1rem;
  font-weight:600;flex:none}
.step-head{display:flex;align-items:center;gap:.6rem}
.step h3{font-size:1.02rem;margin:0;line-height:1.25}
.step p{margin:0 0 .45rem;font-size:.9rem}
.step .fine{font-size:.82rem}
@media (max-width:1100px){.steps-row{grid-template-columns:repeat(3,1fr)}}
@media (max-width:760px){.steps-row{grid-template-columns:repeat(2,1fr)}}
@media (max-width:460px){.steps-row{grid-template-columns:1fr}}

/* ---------- dog cards: two per row, photo over the detail ---------- */
.dogpair{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,3vw,2.75rem);
  align-items:start;margin-bottom:clamp(2rem,3.5vw,3rem)}
.dogpair:last-of-type{margin-bottom:0}
.dogrow{display:flex;flex-direction:column;gap:1rem}
.dogrow .dog-photo{width:100%;border-radius:6px;border:1.5px solid var(--forest);
  box-shadow:0 2px 0 var(--sage-light);aspect-ratio:4/3;object-fit:cover;
  object-position:50% 30%}
@media (max-width:860px){.dogpair{grid-template-columns:1fr}}
.dog-kicker{font-size:.76rem;font-weight:700;letter-spacing:.19em;
  text-transform:uppercase;color:var(--sage-deep);margin:0 0 .35rem}
.dogrow h3{font-size:clamp(1.5rem,2.2vw,2rem);margin-bottom:.15rem}
/* set apart from the body copy without shouting: a rule down the side, the display face,
   and the same sage the rest of the page uses for secondary text */
/* forest, not sage-deep. sage-deep measures 4.34:1 against --paper, which is under the
   4.5 floor for normal text: it is fine for the fine print it was chosen for, and not for
   a paragraph meant to be read. The rule and the display face set this apart, not colour. */
.faith-note{border-left:3px solid var(--sage-light);padding:.15rem 0 .15rem 1.1rem;
  margin-top:1.5rem;font-family:var(--display);font-size:1.02rem;line-height:1.6;
  color:var(--forest)}
.faith-note a{color:var(--forest)}

.reg-name{font-family:"Lora",Georgia,serif;font-style:italic;color:var(--sage-deep);
  margin:0 0 1rem}
.health{border-left:3px solid var(--sage);padding:.2rem 0 .2rem 1.15rem;
  margin:1.25rem 0 0;display:grid;grid-template-columns:1fr auto;
  gap:1.5rem;align-items:start}
.health p{margin:0 0 .45rem;font-size:.95rem}
.health .btn{margin-top:.55rem;padding:.55rem 1.1rem;font-size:.88rem;min-height:44px}
/* stretch rather than flex-start so both record links take the width of the wider one.
   Two links of different widths stacked on top of each other read as an accident. */
.health-btns{display:flex;flex-wrap:wrap;gap:.6rem}
.health-btns .btn{flex:1 1 auto;justify-content:center}
.health-qr{margin:0;text-align:center;flex:none;width:132px}
.health-qr img{width:132px;height:132px;border:1px solid var(--rule);
  border-radius:4px;background:#fff}
.health-qr figcaption{font-size:.68rem;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:var(--sage-deep);margin-top:.4rem;line-height:1.35}
.health.no-qr{grid-template-columns:1fr}

/* ---------- three-column centred list ---------- */
/* A centred wrapping row rather than three fixed columns. It was named for a count and
   then held two, which left a hole on the right. Flex centres whatever is actually there.
   */
.tri{display:flex;flex-wrap:wrap;justify-content:center;
  gap:clamp(1.25rem,2.5vw,2.5rem);max-width:64rem;margin:0 auto}
.tri>div{background:var(--card,#fff);border:1px solid var(--rule);border-radius:5px;
  padding:1.35rem 1.5rem;flex:1 1 16rem;max-width:22rem}
/* When there is only one card it sits alone in a wide band and reads as an afterthought.
   Given the room, it takes it: wider panel, list in two columns, heading across the top. */
.tri.one>div{flex:1 1 auto;max-width:44rem;padding:1.75rem 2rem;width:100%}
.tri.one h3{text-align:center;margin-bottom:1.1rem}
.tri.one .checklist{columns:2;column-gap:2.5rem}
.tri.one .checklist li{break-inside:avoid}
@media (max-width:620px){.tri.one .checklist{columns:1}}
.tri h3{margin:0 0 .75rem;font-size:1.05rem}
.tri .checklist li{font-size:.93rem}
@media (max-width:900px){.tri{max-width:34rem}.tri>div{flex:1 1 100%;max-width:none}}

/* ---------- closing call to action ---------- */
.closing{background:var(--paper-raise);border-top:1px solid var(--rule);
  border-bottom:1px solid var(--rule)}
.closing .inner{max-width:44rem;margin:0 auto;text-align:center;
  display:flex;flex-direction:column;align-items:center;gap:.85rem}
.closing h2{margin:0}
.closing .contact-line{font-size:1.02rem;color:var(--forest-soft);margin:0;
  max-width:44ch}
/* A wrapping centred row, not a grid. It held two tiles when it was written and now
   holds three, and `repeat(2,auto)` stranded the third on its own row against the left
   edge of an otherwise centred block. Flex-wrap centres whatever ends up on each line,
   however many tiles there are. */
.contact-pair{display:flex;flex-wrap:wrap;justify-content:center;gap:.85rem;
  margin:.35rem 0 .25rem}
.contact-pair>.contact-tile{flex:0 1 auto;min-width:0}
.contact-tile{display:flex;flex-direction:column;gap:.2rem;text-decoration:none;
  background:var(--paper);border:1.5px solid var(--rule);border-radius:5px;
  padding:.9rem 1.1rem;text-align:left;min-height:44px}
.contact-tile:hover{border-color:var(--forest)}
/* letter-spacing adds a trailing gap after the final character. the negative
   margin removes it so the label sits flush with the value below it. */
.ct-label{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--sage-deep);font-weight:700;margin-right:-.14em}
.ct-value{font-family:"Lora",Georgia,serif;font-size:1.02rem;font-weight:600;
  overflow-wrap:anywhere}
@media (max-width:620px){
  .contact-pair{flex-direction:column;align-items:stretch}
}
.closing .btn-row{margin:.35rem 0 0;justify-content:center}

/* ---------- FAQ accordion ---------- */
.faq{max-width:60rem;margin:0 auto;border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule)}
.faq summary{list-style:none;cursor:pointer;padding:1.1rem 3rem 1.1rem 0;
  position:relative;font-family:"Lora",Georgia,serif;font-size:1.08rem;
  font-weight:600;min-height:48px;display:flex;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"";position:absolute;right:.9rem;top:1.5rem;width:11px;
  height:11px;border-right:2px solid var(--sage-deep);
  border-bottom:2px solid var(--sage-deep);transform:rotate(45deg);
  transition:transform .18s ease}
.faq details[open] summary::after{transform:rotate(-135deg)}
.faq summary:hover{color:var(--forest-soft)}
.faq .ans{padding:0 3rem 1.2rem 0;color:var(--forest-soft)}
.faq .ans p{margin:0 0 .7rem}
.faq .ans p:last-child{margin:0}
@media (prefers-reduced-motion: reduce){.faq summary::after{transition:none}}

.draft-banner{background:var(--draft-bg);border:1.5px dashed var(--draft);
  color:var(--draft);border-radius:4px;padding:1.1rem 1.35rem;font-weight:700;
  margin:0 0 1.75rem}

/* ---------- footer ---------- */
/* no margin: a coloured final section must butt straight against the footer,
   otherwise a strip of page background shows through between them */
.site-foot{background:var(--forest);color:#e9ded9}
.site-foot a{color:var(--pink-pale)}
.foot-top{display:grid;grid-template-columns:auto 1fr;gap:2.5rem;align-items:start;
  padding:3rem 0 1rem}
/* a cream panel around a colour logo reads as a sticker on the footer. instead:
   the pink paw mark, which already sits well on green, with the name typeset. */
.foot-brand{display:flex;align-items:center;gap:.9rem}
.foot-brand img{height:56px;width:auto}
.foot-brand .fb-name{font-family:"Lora",Georgia,serif;font-size:1.35rem;
  font-weight:600;color:var(--paper);line-height:1.15;display:block}
.foot-brand .fb-sub{font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;
  color:var(--rose);display:block;margin-top:.15rem}
.foot-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}
.foot-grid h3{color:var(--paper);font-size:1rem}
.foot-grid ul{list-style:none;margin:0;padding:0}
.foot-grid li{margin-bottom:.5rem;font-size:.93rem}
.foot-legal{border-top:1px solid rgba(253,249,249,.25);padding:1.35rem 0;
  font-size:.85rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}

@media print{
  .site-head,.site-foot,.btn,.nav,.cthumbs,.filter-row,.chat-fab,.chat-panel,
  .cnav,.share-row{display:none}
  body{background:#fff;color:#000}
}

/* ---------- mobile ---------- */
@media (max-width:1180px){
  .nav a{font-size:.86rem;padding:.5rem .42rem}
  .brand img{height:48px}
}
@media (max-width:900px){
  .dogpair{grid-template-columns:1fr}
  /* stack the hero: the drift only works when there is width to fade across.
     The photo was sitting flush against the sticky header with a zero gap, which read
     as the puppy bumping the top edge of the page. */
  .hero-drift>*{grid-area:auto}
  /* Option B, but only the caption goes on the photograph.
     The mock this was chosen from had a one-line lede. Production has six lines plus a
     chip, so overlaying the whole copy block put text over 72% of the picture starting
     28% down: structurally correct, and a wall of green over the puppy. The eyebrow,
     headline and buttons stay on the image as a compact block at its foot; the lede
     moves below the photograph onto paper, where it is easier to read anyway.

     Mechanically: .wrap and .hero-copy become display:contents so their children are
     grid items of .hero-drift directly, which is what lets one of them sit outside the
     photo's rows. Row 1 is the breathing space above the caption, rows 2 to 4 are the
     caption over the foot of the photo, row 5 is below it. */
  .hero-drift{position:relative;padding-top:0;display:grid;
    grid-template-columns:minmax(0,1fr);
    grid-template-rows:1fr auto auto auto auto}
  .hero-drift>.wrap,.hero-copy{display:contents}
  .hero-photo{width:auto;justify-self:auto;margin:0;position:relative;
    aspect-ratio:auto;min-height:min(158vw,39rem);
    grid-column:1;grid-row:1 / 5;align-self:stretch}
  .hero-photo img{position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:50% 50%;border:0;border-radius:0;background:none}
  .hero-photo::after{content:"";position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to top,rgba(34,61,44,.92) 0%,rgba(34,61,44,.72) 30%,
      rgba(34,61,44,.22) 58%,transparent 78%)}
  /* display:contents drops the wrap, so each item carries the gutter itself */
  .hero-copy>*{grid-column:1;padding-inline:1.25rem}
  /* "Family-raised in Warsaw and Winona Lake" is 39 characters, and at the site's
     .16em tracking it wrapped to two lines, spending caption height on nothing. Tighter
     tracking and a hair smaller holds it to one line at 320px and up. */
  .hero-copy>.eyebrow{grid-row:2;z-index:2;color:var(--rose);margin:0 0 .25rem;
    font-size:.68rem;letter-spacing:.1em}
  .hero-copy>h1{grid-row:3;z-index:2;color:#fff;
    text-shadow:0 1px 14px rgba(0,0,0,.45);
    font-size:clamp(1.5rem,7vw,1.9rem);margin:0 0 .1rem}
  .hero-copy>.btn-row{grid-row:4;z-index:2;margin:.85rem 0 0;
    padding-bottom:1.5rem}
  /* Inverted for the scrim. The site's buttons are forest on paper; over a forest scrim
     that is 1.05:1 for the filled one's background and 1.05:1 for the ghost one's text
     and border, so the ghost button was simply not there. Paper on forest is 11.85:1. */
  .hero-copy .btn-primary{background:var(--paper);color:var(--forest);
    border-color:var(--paper)}
  .hero-copy .btn-ghost{background:transparent;color:var(--paper);
    border-color:rgba(253,249,249,.8)}
  /* on paper now, so it goes back to body colour and needs its own breathing room */
  .hero-copy>.lede{grid-row:5;color:var(--sage-deep);font-size:1rem;
    margin:1.5rem 0 0}
  .hero-photo img{-webkit-mask-image:none;mask-image:none}
  .dogrow{grid-template-columns:1fr;gap:1.25rem}
  .health{grid-template-columns:1fr}
  .health-qr{width:110px}
  .health-qr img{width:110px;height:110px}
  .hero-split,.grid-2,.puppy-top,.foot-grid,.foot-top{grid-template-columns:1fr}
  .foot-top{gap:1.5rem;padding-bottom:0}
  .foot-brand img{height:48px}
  .nav-toggle{display:block}
  .nav{position:fixed;inset:0;background:var(--paper);flex-direction:column;
    justify-content:center;gap:.3rem;display:none;z-index:50;overflow-y:auto}
  .nav.open{display:flex}
  .nav a{font-size:1.25rem;padding:.7rem 1.2rem}
  .nav a.nav-cta{margin-left:0}
  .nav-close{position:absolute;top:1rem;right:1.25rem}
  .section-head{flex-direction:column;align-items:flex-start;gap:1rem}
  .cthumbs button{width:64px;height:64px}
  .facts li{min-height:44px}

  /* ---- the compound-selector trap. `.grid-2` above is specificity (0,1,0) while
     `.grid-2.narrow-left` is (0,2,0), so the two narrow variants kept their desktop
     columns on a phone and squeezed the copy into a third of the screen on eight
     pages. Any new .grid-2 modifier has to be named here too. */
  .grid-2.narrow-left,.grid-2.narrow-right,
  .grid-2.lean-left,.grid-2.lean-right{grid-template-columns:1fr}
  /* a photo that earns its place beside a fact list on desktop, but which the grid
     directly below repeats once everything is stacked */
  .hide-mobile{display:none}
  .parent-grid.row-4{grid-template-columns:1fr}

  /* ---- call to action rows. flex-grow on a wrapping row does both halves of the
     rule: buttons that fit sit side by side, a button that wraps fills its line. */
  .btn-row,.pay-row{gap:.6rem}
  .btn-row>.btn,.pay-row>.btn{flex:1 1 auto;justify-content:center}
  /* section-cta turns to a column, so growth would go vertical. stretch instead. */
  .section-cta{flex-direction:column;align-items:stretch;text-align:center;gap:.85rem}
  .section-cta>.btn{justify-content:center}

  /* ---- share row: five icons plus a label wrapped to two lines and left the last
     icon orphaned. Label on its own row, icons in five equal columns, fits at 390. */
  .share-row{display:grid;grid-template-columns:repeat(5,1fr);gap:.5rem;
    align-items:center}
  .share-lbl{grid-column:1 / -1;margin-bottom:.1rem}
  .share-row a{width:auto;min-width:0}

  /* ---- the chat launcher measured 147px, 38% of the screen, and sat on top of
     real content including a form field on the waitlist page. Icon only here. */
  .chat-fab{right:12px;bottom:12px;padding:0;width:54px;height:54px;
    border-radius:50%;justify-content:center;gap:0}
  .chat-fab .fab-label{display:none}
  /* z-index 60 put it above the z-index 50 nav overlay, so it floated over the
     open menu */
  body.nav-open .chat-fab{display:none}
  /* and it must not come to rest on the last line of a page */
  main{padding-bottom:4.5rem}

  /* ---- a trailing link reads as a stranded fragment when it wraps onto the tail of
     a sentence, so on a phone it takes its own line */
  .own-line{display:block;margin-top:.3rem}

  /* ---- a single word alone on the last line. Narrow columns produce these constantly,
     and `pretty` exists for exactly this: it pulls a word back from the last line by
     re-breaking the ones above it. `balance` evens out short headings. Browsers without
     support simply ignore both and break as they do now. */
  p,li,figcaption,blockquote,.v,.k{text-wrap:pretty}
  h1,h2,h3,.eyebrow,.dog-kicker{text-wrap:balance}

  /* ---- these two labels are long enough to wrap to two lines in a ghost button,
     which looks broken next to a single-line heading */
  .breed-link{white-space:nowrap;font-size:.92rem;padding-left:1rem;padding-right:1rem}

  /* ---- a slimmer bar gives a phone back some screen */
  .head-row{min-height:68px}
  .brand img{height:42px}
}
/* No stacking breakpoint here on purpose. Stacking the key above its value doubles the
   height of every fact list, which on a puppy page is six rows of pure scrolling. The
   pair stays side by side at every width; `min-width:0` plus `overflow-wrap` on the
   value is what stops a long one forcing the row wider than the screen. */
@media (max-width:900px){
  .hero{overflow:visible}
}
"""

JS = """// Bless Your Paws Puppies - v2
(function(){
  // ---- mobile nav overlay: fixed at every width so it never becomes a flex item
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && nav){
    var close = document.createElement('button');
    close.className = 'nav-toggle nav-close';
    close.textContent = 'Close';
    close.setAttribute('aria-label','Close menu');
    nav.appendChild(close);
    function setOpen(open){
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
      document.body.classList.toggle('nav-open', open);
    }
    toggle.addEventListener('click', function(){ setOpen(!nav.classList.contains('open')); });
    close.addEventListener('click', function(){ setOpen(false); });
    nav.addEventListener('click', function(e){ if (e.target.tagName === 'A') setOpen(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') setOpen(false); });
  }

  // ---- puppy photo carousel: prev/next, thumbs, arrow keys
  document.querySelectorAll('.carousel').forEach(function(car){
    var slides = [].slice.call(car.querySelectorAll('.frame img'));
    var thumbs = [].slice.call(car.querySelectorAll('.cthumbs button'));
    var counter = car.querySelector('.count');
    if (slides.length < 2){
      car.querySelectorAll('.cnav').forEach(function(b){ b.remove(); });
      if (counter) counter.remove();
      return;
    }
    var i = 0;
    function show(n){
      i = (n + slides.length) % slides.length;
      slides.forEach(function(s,k){
        s.hidden = false;                       // stacked, so fade rather than pop
        s.classList.toggle('is-on', k === i);
        s.setAttribute('aria-hidden', k === i ? 'false' : 'true');
      });
      thumbs.forEach(function(t,k){ t.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      if (counter) counter.textContent = (i+1) + ' / ' + slides.length;
    }
    // ---- autoplay with a crossfade, so a visitor sees the whole set without
    // clicking. Pauses on hover, focus, and when the tab or page is out of view,
    // and does not run at all for anyone who asked for reduced motion.
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var DWELL = 4000;
    var timer = null, paused = false, inView = true;
    function stop(){ if (timer){ clearInterval(timer); timer = null; } }
    function canPlay(){
      return !reduce.matches && !paused && inView && !document.hidden;
    }
    function start(){
      if (timer || !canPlay()) return;
      timer = setInterval(function(){ show(i+1); }, DWELL);
    }
    // one place decides, so every signal (hover, focus, tab switch, scrolling the
    // carousel out of view) is re-evaluated the same way instead of racing
    function sync(){ canPlay() ? start() : stop(); }
    function restart(){ stop(); start(); }

    car.querySelector('.cprev').addEventListener('click', function(){ show(i-1); restart(); });
    car.querySelector('.cnext').addEventListener('click', function(){ show(i+1); restart(); });
    thumbs.forEach(function(t,k){
      t.addEventListener('click', function(){ show(k); restart(); }); });
    car.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft'){ show(i-1); restart(); }
      if (e.key === 'ArrowRight'){ show(i+1); restart(); }
    });
    ['mouseenter','focusin'].forEach(function(ev){
      car.addEventListener(ev, function(){ paused = true; sync(); }); });
    ['mouseleave','focusout'].forEach(function(ev){
      car.addEventListener(ev, function(){ paused = false; sync(); }); });
    document.addEventListener('visibilitychange', sync);
    reduce.addEventListener('change', sync);

    show(0);
    // only cycle while the carousel is actually on screen
    if ('IntersectionObserver' in window){
      new IntersectionObserver(function(entries){
        inView = entries[0].isIntersecting;
        sync();
      }, { threshold: 0.35 }).observe(car);
    }
    sync();
  });

  // ---- guard: payment links stay friendly until the real Stripe links exist
  document.querySelectorAll('a.pay-link').forEach(function(a){
    if (a.href.indexOf('REPLACE') !== -1){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var msg = a.closest('.reserve').querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // ---- guard: forms stay friendly until the Formspree id exists
  document.querySelectorAll('form[data-guard]').forEach(function(f){
    if (f.action.indexOf('REPLACE') !== -1){
      f.addEventListener('submit', function(e){
        e.preventDefault();
        var msg = f.querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // ---- gallery: two independent filters, by litter and by puppy
  var galGrid = document.querySelector('.gal-grid');
  if (galGrid){
    var fstate = { line: 'all', pup: 'all' };
    var countEl = document.getElementById('gal-count');
    function applyFilters(){
      var shown = 0;
      galGrid.querySelectorAll('a').forEach(function(it){
        var okLine = fstate.line === 'all' || it.getAttribute('data-line') === fstate.line;
        var okPup  = fstate.pup  === 'all' || it.getAttribute('data-pup')  === fstate.pup;
        var vis = okLine && okPup;
        it.style.display = vis ? '' : 'none';
        if (vis) shown++;
      });
      if (countEl) countEl.textContent =
        shown === 1 ? 'Showing 1 photo' : 'Showing ' + shown + ' photos';
    }
    function reset(sel, attr){
      document.querySelectorAll(sel).forEach(function(x){
        x.classList.toggle('cur', x.getAttribute(attr) === 'all');
      });
    }
    var pupSel = document.getElementById('pup-select');
    document.querySelectorAll('.filter-row button').forEach(function(b){
      b.addEventListener('click', function(){
        document.querySelectorAll('.filter-row button').forEach(function(x){
          x.classList.remove('cur'); });
        b.classList.add('cur');
        fstate.line = b.getAttribute('data-line');
        // a litter choice clears the puppy dropdown, so the two never fight
        if (pupSel){ pupSel.value = 'all'; pupSel.parentElement.classList.remove('on'); }
        fstate.pup = 'all';
        applyFilters();
      });
    });
    if (pupSel){
      pupSel.addEventListener('change', function(){
        fstate.pup = pupSel.value;
        pupSel.parentElement.classList.toggle('on', pupSel.value !== 'all');
        // and a puppy choice clears the litter buttons back to All
        if (pupSel.value !== 'all'){
          fstate.line = 'all';
          reset('.filter-row button', 'data-line');
        }
        applyFilters();
      });
    }
    applyFilters();
  }

  // ---- let's chat launcher, on every page
  /* a page that already carries the inquiry form does not need a launcher for it,
     and on a phone the fixed button lands squarely on top of a form field. */
  if (!document.querySelector('form[data-guard]')) {
  var fab = document.createElement('button');
  fab.className = 'chat-fab';
  fab.setAttribute('aria-expanded','false');
  fab.setAttribute('aria-label', 'Chat with us');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span class="fab-label">Let\\u2019s Chat</span>';
  var panel = document.createElement('div');
  panel.className = 'chat-panel';
  panel.innerHTML = '<h3>Talk puppies with us</h3>'
    + '<p>Call or text is the fastest way to reach us. __WHO__</p>'
    + '<div class="row"><span class="lbl">Hope</span><a href="__PHONE_HREF__">__PHONE__</a></div>'
    + '<div class="row"><span class="lbl">Joy</span><a href="__JOY_HREF__">__JOY_PHONE__</a></div>'
    + '<div class="row"><span class="lbl">Email</span><a href="mailto:__EMAIL__">__EMAIL__</a></div>'
    + '<div class="row"><span class="lbl">Inquiry</span><a href="contact.html">Start an inquiry</a></div>'
    + '<div class="row"><span class="lbl">Waitlist</span><a href="waitlist.html">Join the waitlist</a></div>';
  document.body.appendChild(panel);
  document.body.appendChild(fab);
  fab.addEventListener('click', function(){
    var open = !panel.classList.contains('open');
    panel.classList.toggle('open', open);
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){ panel.classList.remove('open'); fab.setAttribute('aria-expanded','false'); }
  });
  }
})();

// ---- warming the next page, after this one is completely finished
// Nearly everyone who lands on the home page opens the puppies page next, and that page's
// photographs are the slowest thing on it. Fetching them while the visitor is still
// reading makes the click feel instant instead of costing another few hundred KB in front
// of them. Two rules keep this honest. It only ever requests URLs the next page would
// request anyway, so a visit that continues does not pay any extra: the bytes move
// earlier, they do not multiply. And it never competes with the page in front of the
// visitor: nothing starts before the load event, everything waits for an idle main
// thread, and every request goes out at low priority.
(function(){
  var c = navigator.connection || {};
  // do not spend somebody else's data plan on a guess
  if (c.saveData === true) return;
  if (/(^|-)2g$/.test(c.effectiveType || '')) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-data: reduce)').matches) return;

  var seen = {}, held = [], budget = 0;
  // a phone shows one card per row, so its card images are near full width and cost real
  // money. A desktop's are about 289px. Same photographs, very different bet.
  var CAP = (window.innerWidth || 1024) < 700 ? 4 : 10;

  // anything this page has already loaded is already in the cache, so it must not eat
  // into the cap. Keyed on srcset AND sizes: the same srcset with a different hint
  // resolves to a different file, which is the whole point of the hint.
  document.querySelectorAll('img[srcset],source[srcset]').forEach(function(n){
    seen[n.getAttribute('srcset') + '|' + (n.getAttribute('sizes') || '')] = 1;
  });

  function doc(href){
    if (!href || seen['d:' + href]) return;
    seen['d:' + href] = 1;
    var l = document.createElement('link');
    l.rel = 'prefetch';
    l.as = 'document';
    l.href = href;
    document.head.appendChild(l);
  }

  function pic(srcset, sizes, media){
    if (!srcset) return;
    if (media && window.matchMedia && !matchMedia(media).matches) return;
    var k = srcset + '|' + (sizes || '');
    if (seen[k] || budget >= CAP) return;
    seen[k] = 1;
    budget++;
    var i = new Image();
    i.fetchPriority = 'low';   // ignored where unsupported, which is harmless
    i.decoding = 'async';
    if (sizes) i.sizes = sizes;   // sizes BEFORE srcset: the candidate is chosen the
    i.srcset = srcset;            // moment srcset is set, and it chooses using sizes
    held.push(i);   // a detached Image can be collected mid-flight. Hold the reference.
  }

  function idle(fn){
    if (window.requestIdleCallback) requestIdleCallback(fn, {timeout: 3000});
    else setTimeout(fn, 1500);
  }

  function manifest(){
    var el = document.getElementById('warm');
    if (!el) return;
    var m;
    try { m = JSON.parse(el.textContent); } catch (e) { return; }
    (m.doc || []).forEach(doc);
    (m.img || []).forEach(function(a){ pic(a[0], a[1], a[2]); });
  }

  // whatever link the pointer, finger or keyboard is actually on beats any guess baked in
  // at build time, and costs one document. On a card it also warms the large version of
  // the photograph already showing in the card: same srcset, the puppy page's own hint.
  function intent(e){
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a || a.origin !== location.origin) return;
    if (a.pathname === location.pathname) return;
    if (/[.](pdf|zip)$/i.test(a.pathname)) return;   // a download, not a navigation
    // A character class, not a backslash-escaped dot: this JS lives inside a plain
    // Python string, where that escape is invalid and warns on every build.
    doc(a.href);
    var hint = a.getAttribute('data-warm-sizes');
    if (hint){
      var im = a.querySelector('img[srcset]');
      if (im) pic(im.getAttribute('srcset'), hint);
    }
  }

  function start(){
    idle(manifest);
    ['pointerover', 'touchstart', 'focusin'].forEach(function(t){
      document.addEventListener(t, intent, {passive: true});
    });
  }
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);
})();
"""
JS = (JS.replace("__WHO__", "Hope raises the Munchkin Bernedoodles and Joy raises the Dobermans."
                 if SHOW_DOBERMANS else "Hope and Joy raise the puppies between them.")
        .replace("__PHONE_HREF__", PHONE_HREF)
        .replace("__PHONE__", PHONE_DISPLAY)
        .replace("__JOY_HREF__", JOY_PHONE_HREF)
        .replace("__JOY_PHONE__", JOY_PHONE_DISPLAY)
        .replace("__EMAIL__", EMAIL))

SPRIG = ('<svg class="sprig" width="72" height="25" viewBox="0 0 40 14" aria-hidden="true">'
 '<g fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round">'
 '<path d="M2 7h36"/>'
 '<path d="M14 7c0-3 2.5-4.5 5-4.5C19 5.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".55"/>'
 '<path d="M14 7c0 3 2.5 4.5 5 4.5C19 8.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".35"/>'
 '<path d="M23 7c0-2.4 2-3.6 4-3.6C27 5.8 25 7 23 7z" fill="currentColor" stroke="none" opacity=".45"/>'
 '<circle cx="34" cy="7" r="1.6" fill="currentColor" stroke="none" opacity=".6"/></g></svg>')

NAV = f"""<nav class="nav" aria-label="Main">
  <a href="puppies.html">Puppies</a>
  <a href="{'munchkin-bernedoodles.html' if SHOW_DOBERMANS else 'what-is-a-munchkin-bernedoodle.html'}">{'Bernedoodles' if SHOW_DOBERMANS else 'Breed Guide'}</a>
{dob('  <a href="dobermans.html">Dobermans</a>')}
  <a href="our-dogs.html">Our Dogs</a>
  <a href="gallery.html">Gallery</a>
  <a href="about.html">About</a>
  <a href="process.html">How It Works</a>
  <a href="contact.html">Contact</a>
  <a class="nav-cta" href="waitlist.html">Join the Waitlist</a>
</nav>"""

def header():
    return f"""<header class="site-head"><div class="wrap head-row">
  <a class="brand" href="index.html" aria-label="Bless Your Paws Puppies, home">
    <img src="img/brand/logo-primary.png?v={V}"
      srcset="img/brand/logo-primary-60.png{asset_v('img/brand/logo-primary-60.png')} 202w, img/brand/logo-primary-84.png{asset_v('img/brand/logo-primary-84.png')} 283w, img/brand/logo-primary-120.png{asset_v('img/brand/logo-primary-120.png')} 404w, img/brand/logo-primary-168.png{asset_v('img/brand/logo-primary-168.png')} 566w"
      sizes="(max-width:900px) 145px, 190px"
      alt="Bless Your Paws Puppies" width="1596" height="474" decoding="async">
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-label="Open menu">Menu</button>
  {NAV}
</div></header>"""

def footer():
    return f"""<footer class="site-foot"><div class="wrap">
  <div class="foot-top">
    <div class="foot-brand">
      <img src="img/brand/mark-paw-heart.png{asset_v('img/brand/mark-paw-heart.png')}" alt="">
      <span><span class="fb-name">Bless Your Paws</span>
        <span class="fb-sub">Puppies</span></span>
    </div>
    <div class="foot-grid">
      <div><h3>Our puppies</h3><ul>
        <li><a href="puppies.html">All available puppies</a></li>
        <li><a href="{'munchkin-bernedoodles.html' if SHOW_DOBERMANS else 'puppies.html'}">Munchkin Bernedoodles</a></li>
{dob('        <li><a href="dobermans.html">Doberman Pinschers</a></li>')}
        <li><a href="what-is-a-munchkin-bernedoodle.html">What is a Munchkin Bernedoodle?</a></li>
        <li><a href="gallery.html">Photo gallery</a></li>
        <li><a href="reviews.html">Reviews</a></li>
      </ul></div>
      <div><h3>Before you visit</h3><ul>
        <li><a href="process.html">How it works</a></li>
        <li><a href="our-dogs.html">Our dogs and their health</a></li>
        <li><a href="about.html">About Hope and Joy</a></li>
        <li><a href="waitlist.html">Join the waitlist</a></li>
        <li><a href="health-guarantee.html">Health guarantee</a></li>
        <li><a href="purchase-agreement.html">Purchase agreement</a></li>
      </ul></div>
      <div><h3>Get in touch</h3><ul>
        <li>{'Hope, Munchkin Bernedoodles' if SHOW_DOBERMANS else 'Hope'}<br><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></li>
        <li>{'Joy, Dobermans' if SHOW_DOBERMANS else 'Joy'}<br><a href="{JOY_PHONE_HREF}">{JOY_PHONE_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{AREA}</li>
        <li class="fine">Visits by appointment. Our location is shared once your
          visit is scheduled.</li>
      </ul></div>
    </div>
  </div>
  <div class="foot-legal">
    <span>&copy; 2026 Bless Your Paws Puppies. Site by <a href="https://harperstudio.co/">Harper Studio</a>.</span>
    <span><a href="privacy-policy.html">Privacy</a></span>
  </div>
</div></footer>"""

# Every path page() writes, in the order it wrote them. The sitemap is built from this
# rather than from a directory listing, because a glob picks up hand-written files too.
GENERATED = []

def pretty_path(path):
    """"puppies.html" -> "puppies", and "index.html" -> "" (the site root)."""
    return "" if path == "index.html" else path[:-5] if path.endswith(".html") else path

def prettify_links(text):
    """Rewrite bare .html hrefs to the extensionless form Cloudflare Pages serves.

    Applied to finished output rather than threaded through every template, because the
    links are spread across dozens of f-strings, the nav, the footer, the Doberman-flag
    blocks and main.js. One pass over the result cannot miss one.

    Only BARE filenames match, so `records/troy-...pdf`, `img/...`, `fonts/...` and any
    absolute URL are untouched: the pattern allows no slash and no dot inside the name.
    """
    text = text.replace('href="index.html"', 'href="/"')
    return re.sub(r'href="([a-z0-9-]+)\.html"', r'href="\1"', text)

def page(path, title, desc, body, extra_head=""):
    # a JSON island rather than inline script, so there is nothing to escape and no
    # execution here at all: main.js reads it if it is present and does nothing if not
    warm = warm_for(path)
    warm_tag = ("" if not warm else '<script type="application/json" id="warm">'
                + json.dumps(warm, separators=(",", ":")) + "</script>\n")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}/{pretty_path(path)}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/img/og-card.png">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.ico?v={V}" sizes="any">
<link rel="icon" href="img/favicon.png?v={V}" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png?v={V}">
<link rel="preload" href="fonts/lora-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/mulish-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css?v={V}">
{extra_head}</head>
<body>
{header()}
<main>
{body}
</main>
{footer()}
{warm_tag}<script src="main.js?v={V}" defer></script>
</body>
</html>
"""
    assert "—" not in html, f"em dash slipped into {path}"
    open(path, "w", encoding="utf-8").write(prettify_links(html))
    GENERATED.append(path)

@functools.lru_cache(maxsize=None)
def asset_v(path):
    """?v= for one asset, from its own bytes. Empty string if the file is missing."""
    try:
        with open(path, "rb") as fh:
            return "?v=" + hashlib.md5(fh.read()).hexdigest()[:8]
    except OSError:
        return ""

def srcset_for(stem):
    """The srcset string for one stem, or "" if it has no derivatives.

    Split out of img_tag because the cache-warming manifest has to name exactly the same
    candidate URLs the next page will ask for. Two spellings of the same srcset would
    warm one URL and then request another, which looks like it works and does nothing.
    """
    # only reference widths that were actually generated: a narrow original has no
    # 1600px derivative, and a srcset entry pointing at a missing file is a 404.
    have = [w for w in (320, 640, 1000, 1600)
            if os.path.exists(f"img/r/{stem}-{w}.webp")]
    return ", ".join(f"img/r/{stem}-{w}.webp{asset_v(f'img/r/{stem}-{w}.webp')} {w}w"
                     for w in have)

def img_tag(stem, folder="puppies", cls="", alt="", lazy=True, hidden=False,
            sizes="(max-width:900px) 94vw, 58vw", priority=False):
    q = chr(34)
    parts = ["<img"]
    if hidden: parts.append("hidden")
    if cls: parts.append(f"class={q}{cls}{q}")
    ss = srcset_for(stem)
    if ss:
        parts.append("srcset=" + q + ss + q)
    parts.append(f'sizes={q}{sizes}{q}')
    parts.append(f'src={q}img/{folder}/{stem}.jpg'
                 f'{asset_v(f"img/{folder}/{stem}.jpg")}{q}')
    parts.append(f'alt={q}{alt}{q}')
    if priority:
        # the largest-contentful candidate: eager, and flagged so the browser fetches it
        # ahead of the other images competing for the same connection
        parts.append(f'fetchpriority={q}high{q}')
        parts.append(f'decoding={q}sync{q}')
    if lazy and not priority: parts.append(f'loading={q}lazy{q}')
    return " ".join(parts) + ">"

def desktop_only_img(stem, folder="puppies", cls="", alt="",
                     sizes="(max-width:900px) 94vw, 58vw"):
    """A photo that CSS hides below 901px, emitted so a phone never downloads it.

    `display:none` does NOT prevent a fetch. The browser runs image selection whatever
    the element's rendering, so puppies.html was pulling a 52KB hero at
    fetchpriority=high on a 390px screen and then hiding it. Measured, not assumed.

    Inside a <picture> the rules are different. The two <source>s hold every candidate
    and are gated on the same 901px the CSS uses, and the <img> deliberately carries no
    src and no srcset, so below that width there is nothing to select and nothing is
    requested. Above it a source matches and the image loads eagerly, which it must,
    because on a desktop this is the largest-contentful element.

    The jpg keeps its own source rather than being dropped, so a desktop browser with no
    webp support still gets the picture, exactly as it did from img_tag.

    The media query and the `.hide-mobile` breakpoint have to stay in step. If one moves,
    move the other, or the photo becomes either invisible or un-downloadable.
    """
    q = chr(34)
    ss = srcset_for(stem)
    jpg = f"img/{folder}/{stem}.jpg{asset_v(f'img/{folder}/{stem}.jpg')}"
    # The EXACT complement of the .hide-mobile query, not "(min-width:901px)". Those
    # two leave a sliver between 900px and 901px, reachable by zoom or display scaling,
    # where the CSS shows the image and no source matches it: visible and unloadable at
    # the same time. "not all and (max-width:900px)" is true precisely when the CSS rule
    # is false, so the two cannot disagree. If the breakpoint moves, move both.
    mq = "not all and (max-width:900px)"
    out = [f"<picture class={q}{cls}{q}>"]
    if ss:
        out.append(f'<source media={q}{mq}{q} srcset={q}{ss}{q} '
                   f'sizes={q}{sizes}{q} type={q}image/webp{q}>')
    out.append(f'<source media={q}{mq}{q} srcset={q}{jpg}{q}>')
    out.append(f'<img alt={q}{alt}{q} '
               f'fetchpriority={q}high{q} decoding={q}sync{q}>')
    out.append("</picture>")
    return "".join(out)

def dob_carrier_section_html():
    """Reading-a-genetic-panel section. Entirely about Mira's panel and illustrated with
    a Doberman puppy, so it goes when the Doberman line goes. This is where Troy's
    Wisdom Panel belongs once Hope has decided how she wants it presented."""
    return dob('<section class="band-pink band-tight"><div class="wrap">'
      '<div class="grid-2 narrow-right hic hic-flip">'
      '<div class="col-title hic-head"><p class="eyebrow">Reading a genetic panel</p>'
      '<h2>What a carrier result actually means</h2></div>'
      + img_tag('griffin-01', cls='framed hic-photo',
                alt='Griffin, a black and rust Doberman Pinscher puppy')
      + '<div class="hic-copy">'
        "<p>Mira's panel comes back clear on everything tested except one condition, "
        'where she is a carrier. A carrier has one copy of a variant and is not affected '
        'by it herself. Carriers are bred to clear partners so that no puppy can be '
        'affected, which is exactly how she is paired.</p>'
        '<p>An OFA heart exam is a cardiac screening performed by a veterinarian and '
        'registered with the Orthopedic Foundation for Animals. Mira has been screened '
        'by EKG and holter, and her eyes are tested too.</p>'
        '<p class="fine">Do not take our word for any of it. Scan the QR beside her, or '
        'follow the links, and read the records yourself.</p>'
        '</div></div></div></section>')

def dob_meet_card_html():
    return dob('<div>'
      + img_tag('malcolm-02', cls='framed',
                alt='Malcolm, a black and rust Doberman Pinscher puppy')
      + '<h3 style="margin-top:1rem">Doberman Pinschers</h3>'
        '<p class="fine">AKC registered, loyal, and ready to go home now.'
        '<span class="own-line"><a href="dobermans.html">See the litter</a>.</span></p>'
        '</div>')

def dog_row(stem, name, breed, reg, story, health, links, qr=None, qr_num=None,
            first=False):
    """Full-width dog row: big photo, story, a testing block with the real records
    linked, and a QR to the OFA page. Mirrors the Kingdom Family Companions pattern."""
    hp = "".join("<p><strong>%s</strong> %s</p>" % (k, v) for k, v in health)
    btns = "".join(
      '<a class="btn btn-ghost" href="%s%s" target="_blank" rel="noopener">%s</a>'
      % (u, asset_v(u) if not u.startswith("http") else "", t)
      for t, u in links)
    if qr:
        qrfig = ('<figure class="health-qr">'
                 '<img src="img/%s" alt="QR code linking to %s\u2019s OFA record %s" '
                 'width="132" height="132" loading="lazy">'
                 '<figcaption>Scan for OFA<br>%s</figcaption></figure>' % (qr, name, qr_num, qr_num))
        hcls = "health"
    else:
        qrfig, hcls = "", "health no-qr"
    reg_html = '<p class="reg-name">%s</p>' % reg if reg else ""
    return ('<article class="dogrow">'
      + img_tag(stem, folder="dogs", cls="dog-photo",
                lazy=not first, priority=first,
                alt="%s, our %s" % (name, breed),
                sizes="(max-width:900px) 94vw, 56vw")
      + '<div>'
        '<p class="dog-kicker">' + breed + '</p>'
        '<h3>' + name + '</h3>' + reg_html
      + '<p>' + story + '</p>'
      + '<div class="' + hcls + '"><div class="health-copy">' + hp
      + '<div class="health-btns">' + btns + '</div></div>' + qrfig + '</div>'
      '</div></article>')

def parent_card(stem, name, role, breed, facts, note=""):
    """Parent card with a labelled role, breed line, and facts table. Replaces the
    run-on sentence that read badly under the photos."""
    rows = "".join('<li><span class="k">%s</span><span class="v">%s</span></li>' % (k, v)
                   for k, v in facts)
    if stem.endswith(".svg"):
        img = '<img src="img/placeholder/%s" alt="Photo of %s coming soon">' % (stem, name)
    else:
        img = img_tag(stem, folder="dogs", alt="%s, our %s" % (name, breed))
    note_html = '<p class="fine" style="margin:.6rem 0 0">%s</p>' % note if note else ""
    return ('<article class="packet parent">' + img +
      '<div class="packet-body">'
      '<p class="dogmeta">' + role + '</p>'
      '<p class="packet-name">' + name + '</p>'
      '<p class="packet-meta">' + breed + '</p>'
      '<ul class="facts" style="margin-top:.6rem;margin-bottom:0">' + rows + '</ul>'
      + note_html + '</div></article>')

# measured against the real .pgrid tracks rather than guessed: 289px at 1440, 321 in the
# gallery, so the old "45vw" was more than double the truth
# measured, per column ratio, at 1440
PHOTO_WIDE   = "(max-width:900px) 94vw, 58vw"   # narrow-left: photo in the 1.30fr column
PHOTO_LEAN   = "(max-width:900px) 94vw, 46vw"   # lean-left
PHOTO_NARROW = "(max-width:900px) 94vw, 29vw"   # narrow-right + flip: copy takes the width

CARD_SIZES = ("(max-width:460px) 92vw, (max-width:760px) 46vw, "
              "(max-width:1100px) 30vw, 22vw")
# the first carousel slide on a puppy page. Named because the cache warmer has to request
# the candidate that page will pick, and a different hint picks a different file.
PUPPY_HERO_SIZES = "(max-width:900px) 94vw, 52vw"

def warm_for(path):
    """URLs worth fetching quietly once `path` has finished loading, or None.

    Read this as a bet on where the visitor goes next, and keep the bet small. Documents
    are nearly free, a few KB of HTML each. Photographs are not, so only two pages warm
    any: the home page, because almost everyone opens the puppies page from it, and it is
    the one page where we know the next step. Everywhere else the pointer tells us more
    than a guess can, and main.js warms whatever link it is actually on.

    Entries are [srcset, sizes] or [srcset, sizes, media]. The media condition exists
    because puppies.html only downloads its hero above 901px now, and warming it on a
    phone would put back exactly the wasted 52KB that desktop_only_img just removed.

    The sizes hint must be the one the DESTINATION page uses, not this one's. A different
    hint picks a different file off the same srcset, and then the warm request and the
    real request are two different URLs: the visit pays twice and feels no faster.
    """
    if path == "index.html":
        cards = [[srcset_for(lead(sl)), CARD_SIZES] for sl, *_ in list(MUNCHKINS) + D_LIST]
        return {"doc": [pretty_path("puppies.html") or "/"],
                # the puppies page's largest-contentful element, desktop only
                "img": [[srcset_for("jericho-01"), PHOTO_WIDE, "(min-width:901px)"]]
                       + [c for c in cards if c[0]]}
    if path == "puppies.html":
        return {"doc": ["what-is-a-munchkin-bernedoodle", "contact"]}
    if path.startswith("puppy-"):
        # whoever reads a whole puppy page is deciding, and both next steps are forms
        return {"doc": ["contact", "waitlist"]}
    if path == "what-is-a-munchkin-bernedoodle.html":
        return {"doc": ["puppies"]}
    return None

def card(slug, name, sex, colour, price, breed, first=False):
    # an adopted puppy shows no price: she is not for sale, and a price beside "Adopted!"
    # invites the question of whether she still is
    adopted = slug in ADOPTED
    left = "" if adopted else f'<span class="price">${price:,}</span>'
    badge = ('<span class="status status-adopted">Adopted!</span>' if adopted
             else '<span class="status">Available</span>')
    return f"""<a class="packet-link{' is-adopted' if adopted else ''}" href="puppy-{slug}.html" data-warm-sizes="{PUPPY_HERO_SIZES}"><article class="packet">
  {img_tag(lead(slug), alt=f'{name}, a {colour.lower()} {breed} puppy', sizes=CARD_SIZES,
           lazy=not first, priority=first)}
  <div class="packet-body">
    <p class="packet-name">{name}</p>
    <p class="packet-meta">{sex} &middot; {colour}</p>
    <div class="packet-row">{left}{badge}</div>
  </div>
</article></a>"""

def share_row(name, path, img):
    u = f"{BASE}/{path}"
    t = f"{name}%20at%20Bless%20Your%20Paws%20Puppies"
    ic = lambda d: (f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
                    f'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                    f'stroke-linejoin="round" aria-hidden="true">{d}</svg>')
    return f"""<div class="share-row"><span class="share-lbl">Share {name}</span>
  <a href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener" aria-label="Share {name} on Facebook">{ic('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>')}</a>
  <a href="https://pinterest.com/pin/create/button/?url={u}&amp;media={BASE}/{img}&amp;description={t}" target="_blank" rel="noopener" aria-label="Share {name} on Pinterest">{ic('<circle cx="12" cy="12" r="10"/><path d="M9 21c1-4 1.5-6 2-8.5"/><path d="M11.5 12.5a3.5 3.5 0 1 1 3 1.4c-1.2 0-2-.6-2.3-1.4"/>')}</a>
  <a href="https://wa.me/?text={t}%20{u}" target="_blank" rel="noopener" aria-label="Share {name} on WhatsApp">{ic('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/><path d="M9 10a4 4 0 0 0 5 5"/>')}</a>
  <a href="sms:?&amp;body={t}%20{u}" aria-label="Share {name} by text">{ic('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>')}</a>
  <a href="mailto:?subject={t}&amp;body={u}" aria-label="Share {name} by email">{ic('<path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/>')}</a>
</div>"""

# One phrase for every title, description, OG tag and JSON-LD block, so the breed
# list is stated once instead of in nine places that can drift apart.
BREEDS_PHRASE = ("Munchkin Bernedoodle and Doberman Pinscher" if SHOW_DOBERMANS
                 else "Munchkin Bernedoodle")
BREEDS_SHORT  = ("Munchkin Bernedoodle and Doberman" if SHOW_DOBERMANS
                 else "Munchkin Bernedoodle")

dob_reg_clause = dob('<li><strong>Registration.</strong> Doberman puppies are sold '
                     'with AKC registration. Breeding rights are available for an '
                     'additional $' + str(DEPOSIT) + '.</li>')

# The breed chooser that sat on the home page. It only means anything with two
# breeds to choose between, so it is emitted through dob(). Kept verbatim rather
# than deleted, so restoring the flag restores the section.
BREED_DOORS_HTML = '<section><div class="wrap">\n  {SPRIG}\n  <h2 class="center" style="margin-top:1rem">{\'Two breeds, one standard of raising\' if SHOW_DOBERMANS else \'One breed, one standard of raising\'}</h2>\n  <div class="grid-2" style="margin-top:2rem;align-items:stretch">\n    <a class="door" href="{\'munchkin-bernedoodles.html\' if SHOW_DOBERMANS else \'puppies.html\'}">\n      {img_tag(\'eden-01\', alt=\'Eden, a red and white Munchkin Bernedoodle puppy\')}\n      <div class="door-body"><h3>Munchkin Bernedoodles</h3>\n      <p class="fine">A small, sweet Bernedoodle and Cavalier cross. Going home in\n        September.</p></div>\n    </a>\n    {dob(\'\'\'<a class="door" href="dobermans.html">\n      IMGDOB\n      <div class="door-body"><h3>Doberman Pinschers</h3>\n      <p class="fine">Loyal Dobermans from our health-tested dam Mira. Ready to go\n        home now.</p></div>\n    </a>\'\'\').replace(\'IMGDOB\', img_tag(\'griffin-01\', alt=\'Griffin, a Doberman Pinscher puppy\'))}\n  </div>\n</div></section>'

M_PARENTS = None  # filled in build_pages
D_PARENTS = None

def build_pages():
    global M_PARENTS, D_PARENTS
    m_cards = "\n".join(card(s, n, x, c, M_PRICE, "Munchkin Bernedoodle", first=(k == 0))
                        for k, (s, n, x, c, _) in enumerate(MUNCHKINS))
    d_cards = "\n".join(card(s, n, x, c, D_PRICE, "Doberman Pinscher") for s, n, x, c, _ in D_LIST)
    # built here rather than inline in the template: an f-string cannot hold a
    # conditional multi-line block without nesting quotes of the same kind
    dob_litter_block = dob(f'''<div class="section-head" style="margin-top:4rem">
    <div>
      <h2 style="margin:0">Doberman Pinschers &middot; ${D_PRICE:,}</h2>
      <p class="fine" style="margin:.35rem 0 0">Born {D_BORN}.
        <strong>Ready to go home now.</strong> AKC registered, tails docked, dew claws
        removed, microchipped.</p>
    </div>
    <a class="btn btn-ghost breed-link" href="dobermans.html">About Doberman Pinschers</a>
  </div>
  <div class="pgrid cols-3" style="margin-top:1.5rem">{d_cards}</div>''')

    M_PARENTS = (
      parent_card("troy-01", "Troy", "Mom", "Mini Multi Gen Bernedoodle",
                  [("Weight", "22 lbs"), ("Color", "Blue merle parti"),
                   ("Born", "January 21, 2024")]) +
      parent_card("cavalier-sire-01", "Our Cavalier sire", "Dad",
                  "Cavalier King Charles Spaniel, AKC",
                  [("Weight", "19 lbs"), ("Color", "Ruby"),
                   # "Clear" was retracted from his detail row and his FAQ answer for want
                   # of a document. It survived here, on ten pages, saying the opposite.
                   ("Genetic testing", "Panel being gathered")],
                  "His registered name is being added. " + CHIP_DRAFT))
    D_PARENTS = (
      parent_card("mira-01", "Mira", "Mom", "Doberman Pinscher",
                  [("Registered", "Kingdom's Miraculous Grace"),
                   ("Weight", "70 lbs"), ("Color", "Black and rust"),
                   ("Genetic panel", "Clear, DCM3 carrier"),
                   ("OFA", "Heart and eyes")]) +
      parent_card("doberman-sire-01", "Our Doberman sire", "Dad", "Doberman Pinscher",
                  [("Weight", "100 lbs"), ("Color", "Red and rust"),
                   ("Genetic testing", "Clear")],
                  "His registered name is being added. " + CHIP_DRAFT))

    # With two litters this page is an index across both. With one it IS the litter
    # page, so it absorbs what the retired breed page carried: the parent lede, the
    # facts list, the hero photo and the parents block. Nothing is dropped, and the
    # keyword-bearing title moves onto the surviving URL.
    if SHOW_DOBERMANS:
        PUPPIES_TITLE = "Available Puppies | Bless Your Paws Puppies"
        PUPPIES_DESC  = (f"All available {BREEDS_PHRASE} puppies. A ${DEPOSIT} deposit "
                         f"reserves your puppy.")
        PUPPIES_INTRO = f'''  <p class="eyebrow">Available now</p>
  <h1>Our puppies</h1>
  <p class="lede" style="max-width:70ch">{n_word(M_TOTAL + len(DOBERMANS))} puppies across two litters. Every price
    includes the vet exam, vaccinations, and the go-home kit. A ${DEPOSIT} deposit
    holds your puppy.</p>

  <div class="section-head" style="margin-top:2.5rem">
    <div>
      <h2 style="margin:0">Munchkin Bernedoodles &middot; ${M_PRICE:,}</h2>
      <p class="fine" style="margin:.35rem 0 0">Born {M_BORN}. Going home {M_HOME}.
        {SIZE_DRAFT}</p>
    </div>
    <a class="btn btn-pink breed-link" href="what-is-a-munchkin-bernedoodle.html">What is a Munchkin Bernedoodle?</a>
  </div>
  <div class="pgrid cols-4" style="margin-top:1.5rem">{m_cards}</div>

{dob_litter_block}'''
        PUPPIES_TAIL = ""
    else:
        PUPPIES_TITLE = f"Munchkin Bernedoodle Puppies for Sale | {BRAND}"
        PUPPIES_DESC  = (f"Munchkin Bernedoodle puppies from a Mini Multi Gen Bernedoodle "
                         f"dam and an AKC Cavalier sire. Born {M_BORN}, home in September. "
                         f"${M_PRICE:,} with a ${DEPOSIT} deposit.")
        PUPPIES_INTRO = f'''  <div class="grid-2 narrow-left hic">
    <div class="col-title hic-head">
      <p class="eyebrow">{'Hope&rsquo;s litter' if SHOW_DOBERMANS else 'Available now'}</p>
      <h1>Munchkin Bernedoodle puppies</h1>
    </div>
    {desktop_only_img('jericho-01', cls='framed hic-photo hide-mobile', alt='Jericho, a blue merle parti Munchkin Bernedoodle puppy', sizes=PHOTO_WIDE)}
    <div class="hic-copy">
      <p class="lede">{n_word(M_TOTAL)} puppies from <a href="our-dogs.html">Troy</a>, our Mini Multi Gen
        Bernedoodle, and our AKC-registered Cavalier King Charles Spaniel sire. Born
        {M_BORN}, going home {M_HOME}.{f' {n_word(M_AVAILABLE)} are still looking for their families.' if M_AVAILABLE != M_TOTAL else ''}</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${M_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">{M_BORN}</span></li>
        <li><span class="k">Go home</span><span class="v">{M_HOME}</span></li>
        <li><span class="k">Expected adult size</span><span class="v">{M_SIZE}</span></li>
      </ul>
      <p class="fine">{SIZE_DRAFT}</p>
      <div class="btn-row" style="margin-top:1rem">
        <a class="btn btn-pink breed-link" href="what-is-a-munchkin-bernedoodle.html">What is a Munchkin Bernedoodle?</a>
      </div>
    </div>
  </div>
  <div class="pgrid cols-4" style="margin-top:clamp(2.75rem,4.5vw,4rem)">{m_cards}</div>'''
        PUPPIES_TAIL = f'''
<section class="band-raise"><div class="wrap">
  <div class="section-head">
    <div><h2 style="margin:0">Meet their parents</h2></div>
    <a class="btn btn-primary" href="our-dogs.html">Full health details</a>
  </div>
  <div class="parent-grid">{M_PARENTS}</div>
</div></section>'''
    # a breed chooser needs at least two breeds to choose between
    breed_doors_section = dob(BREED_DOORS_HTML)

    PUPPIES_BODY = ('<section><div class="wrap">\n' + PUPPIES_INTRO
                    + '\n</div></section>' + PUPPIES_TAIL)


    hp = """<div style="position:absolute;left:-9999px" aria-hidden="true">
      <label for="{i}-hp">Leave this field empty</label>
      <input id="{i}-hp" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    """

    # No "address" and no "geo", deliberately and permanently: this is a home-based
    # business and the standard advice to publish a street address does not apply. See the
    # departures section of .claude/guides/local-seo-aeo.md. areaServed carries the
    # geography instead, as structured Places rather than the sentence it used to be, so a
    # machine can read where they operate without anyone reading where they live.
    # "sameAs" is deliberately absent rather than empty: it belongs there the day Hope and
    # Joy hand over their social profiles, and an empty array asserts they have none.
    org_ld = json.dumps({"@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "Bless Your Paws Puppies",
        "description": f"Family-raised {BREEDS_PHRASE} puppies in Warsaw and Winona Lake, Indiana.",
        "telephone": "+1-574-377-8023", "email": EMAIL,
        "areaServed": [
            {"@type": "City",  "name": "Warsaw",       "addressRegion": "IN",
             "addressCountry": "US"},
            {"@type": "City",  "name": "Winona Lake",  "addressRegion": "IN",
             "addressCountry": "US"},
            {"@type": "State", "name": "Indiana",      "addressCountry": "US"}],
        "priceRange": f"${M_PRICE:,}",
        "logo": BASE + "/img/brand/logo-horizontal-forest.png",
        "url": BASE + "/", "image": BASE + "/img/og-card.png"})

    page("index.html", f"{BREEDS_SHORT} Puppies in Indiana | {BRAND}",
      f"Family-raised {BREEDS_PHRASE} puppies from two sisters in northern Indiana. Raised in the home, around kids, with early socialization.",
      f"""<section class="hero">
  <div class="hero-drift">
    <div class="hero-photo">
      {img_tag('havilah-01', alt='Havilah, a blue merle phantom Munchkin Bernedoodle puppy', lazy=False, priority=True, sizes='(max-width:900px) 96vw, 74vw')}
    </div>
    <div class="wrap">
      <div class="hero-copy">
        <p class="eyebrow">Family-raised in Warsaw and Winona Lake</p>
        <h1>{BREEDS_SHORT} puppies raised in the middle of real family life</h1>
        <p class="lede">We are two sisters raising {'Munchkin Bernedoodles and Doberman Pinschers' if SHOW_DOBERMANS else '<a href="what-is-a-munchkin-bernedoodle.html">Munchkin Bernedoodles</a>'} underfoot in our homes, around our kids, the vacuum, the doorbell,
          and everything else a family sounds like. {CHIP_SAMPLE}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="puppies.html">See available puppies</a>
          <a class="btn btn-ghost" href="waitlist.html">Join the waitlist</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band-raise"><div class="wrap">
  <p class="eyebrow">Available now</p>
  <h2>Puppies looking for their families</h2>
  <p class="lede">{'Munchkin Bernedoodles going home in September, and Doberman Pinschers ready right now.' if SHOW_DOBERMANS else 'Munchkin Bernedoodles going home in September.'} A ${DEPOSIT} deposit holds your puppy.</p>
  <div class="pgrid" style="margin-top:2rem">
{card(*MUNCHKINS[1][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*MUNCHKINS[2][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*MUNCHKINS[6][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*DOBERMANS[0][:4], D_PRICE, "Doberman Pinscher") if SHOW_DOBERMANS else card(*MUNCHKINS[3][:4], M_PRICE, "Munchkin Bernedoodle")}
  </div>
  <div class="section-cta">
    <p>{'Every available puppy, both litters, in one place.' if SHOW_DOBERMANS else 'Every available puppy in one place.'}</p>
    <a class="btn btn-primary" href="puppies.html">See all available puppies</a>
  </div>
</div></section>

{breed_doors_section}

<section class="band-forest"><div class="wrap grid-2 hic">
  <div class="hic-head">
    <p class="eyebrow">How they are raised</p>
    <h2>Socialized before they ever leave our arms</h2>
  </div>
  {img_tag('caleb-02', cls='framed hic-photo', alt='Caleb, a red and white parti Munchkin Bernedoodle puppy', sizes='(max-width:900px) 94vw, 44vw')}
  <div class="hic-copy">
    <p>Every puppy is raised in the home, not a kennel. They grow up with children,
      other dogs, and the everyday noise of family life: the doorbell, the TV, pots
      and pans, the vacuum. Early neurological stimulation starts in the first weeks,
      and grass potty training starts before go-home.</p>
    <p>Each puppy leaves with a vet exam, current vaccinations, a health record, a bag
      of the food they know, and a toy that smells like home.
      <a href="process.html">See how reserving works</a>.</p>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <div>
      <p class="eyebrow">The parents</p>
      <h2>Health and temperament start here</h2>
      <p class="lede" style="max-width:62ch;margin:0">Each dog's testing listed on
        their own card. Where a record exists, we link the record.</p>
    </div>
    <a class="btn btn-primary" href="our-dogs.html">Meet our dogs</a>
  </div>
  <div class="parent-grid">
{M_PARENTS}{D_PARENTS if SHOW_DOBERMANS else ''}
  </div>
</div></section>

<section class="band-pink" style="margin-bottom:0"><div class="wrap center">
  <h2>Litters reserve quickly</h2>
  <p class="lede">One puppy from this litter went home to a waitlist family before it
    was ever listed. Join the waitlist and you hear about the next litter first.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-primary" href="waitlist.html">Join the waitlist</a></div>
</div></section>""",
      extra_head=f'<script type="application/ld+json">{org_ld}</script>\n')

    page("puppies.html", PUPPIES_TITLE, PUPPIES_DESC, PUPPIES_BODY)

    if SHOW_DOBERMANS:
      page("munchkin-bernedoodles.html", "Munchkin Bernedoodle Puppies for Sale | Bless Your Paws Puppies",
      f"Munchkin Bernedoodle puppies from a Mini Multi Gen Bernedoodle dam and an AKC Cavalier sire. Born {M_BORN}, home in September. ${M_PRICE:,} with a ${DEPOSIT} deposit.",
      f"""<section><div class="wrap">
  <div class="grid-2 narrow-left">
    <div>
      <div class="col-title">
        <p class="eyebrow">Hope's litter</p>
        <h1>Munchkin Bernedoodle puppies</h1>
      </div>
      <p class="lede">{n_word(M_TOTAL)} puppies from Troy, our Mini Multi Gen
        Bernedoodle, and our AKC-registered Cavalier King Charles Spaniel sire. Born
        {M_BORN}, going home {M_HOME}.{f' {n_word(M_AVAILABLE)} are still looking for their families.' if M_AVAILABLE != M_TOTAL else ''}</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${M_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">{M_BORN}</span></li>
        <li><span class="k">Go home</span><span class="v">{M_HOME}</span></li>
        <li><span class="k">Expected adult size</span><span class="v">{M_SIZE}</span></li>
      </ul>
      <p class="fine">{SIZE_DRAFT}</p>
      <p>New to the cross? <a href="what-is-a-munchkin-bernedoodle.html">Read our
        plain-language guide</a> to what a Munchkin Bernedoodle is and what to expect.</p>
    </div>
    {desktop_only_img('jericho-01', cls='framed hide-mobile', alt='Jericho, a blue merle parti Munchkin Bernedoodle puppy', sizes=PHOTO_WIDE)}
  </div>
  <div class="pgrid cols-4" style="margin-top:2.5rem">{m_cards}</div>
</div></section>

<section class="band-raise"><div class="wrap">
  <div class="section-head">
    <div><h2 style="margin:0">Meet their parents</h2></div>
    <a class="btn btn-primary" href="our-dogs.html">Full health details</a>
  </div>
  <div class="parent-grid">{M_PARENTS}</div>
</div></section>

<section class="band-pink"><div class="wrap center">
  <p class="lede">Hoping for a puppy from a future litter instead?</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="waitlist.html">Join the waitlist</a></div>
</div></section>""")

    if SHOW_DOBERMANS:
      page("dobermans.html", "Doberman Pinscher Puppies for Sale | Bless Your Paws Puppies",
      f"AKC Doberman Pinscher puppies, ready to go home now. From our health-tested dam Mira. ${D_PRICE:,} with a ${DEPOSIT} deposit.",
      f"""<section><div class="wrap">
  <div class="grid-2 narrow-left">
    <div>
      <div class="col-title">
        <p class="eyebrow">Joy's litter</p>
        <h1>Doberman Pinscher puppies</h1>
      </div>
      <p class="lede">Three AKC-registered puppies from Mira, our health-tested
        Doberman dam. Born {D_BORN}, and <strong>ready to go home now</strong>.</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${D_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">{D_BORN}</span></li>
        <li><span class="k">Status</span><span class="v">Ready now</span></li>
        <li><span class="k">Registration</span><span class="v">AKC</span></li>
        <li><span class="k">Breeding rights</span><span class="v">${DEPOSIT} extra</span></li>
      </ul>
      <p>Mira's genetic and heart testing is real and linked:
        <a href="our-dogs.html">see the records</a>.</p>
    </div>
    {desktop_only_img('elowen-01', cls='framed hide-mobile', alt='Elowen, a black and rust Doberman Pinscher puppy', sizes=PHOTO_WIDE)}
  </div>
  <div class="pgrid cols-3" style="margin-top:2.5rem">{d_cards}</div>
</div></section>

<section class="band-raise"><div class="wrap">
  <div class="section-head">
    <div><h2 style="margin:0">Meet their parents</h2></div>
    <a class="btn btn-primary" href="our-dogs.html">Full health details</a>
  </div>
  {dob('<div class="parent-grid">' + str(D_PARENTS) + '</div>')}
</div></section>""")

    faq = [
      ("How big does a Munchkin Bernedoodle get?",
       f"Most mature between 10 and 25 lbs and stand roughly 12 to 15 inches at the shoulder. Our current litter is expected at {M_SIZE} full grown. Size varies puppy to puppy, so ask us about the one you love."),
      ("How does a Munchkin Bernedoodle end up so small?",
       "By breeding down through generations and crossing in a naturally smaller parent breed. Ours come from a 22 lb Mini Multi Gen Bernedoodle mother and a 19 lb Cavalier father. " + CHIP_DRAFT),
      ("How is this different from a Mini or Micro Bernedoodle?",
       "A Mini or Micro Bernedoodle usually gets small by crossing to a smaller Poodle. A Munchkin adds Cavalier King Charles Spaniel, which brings the size down and brings the Cavalier's calm, affectionate temperament with it."),
      ("Do they shed? Are they hypoallergenic?",
       "No dog is truly hypoallergenic, and we will never tell you otherwise. Coats vary by puppy even inside one litter. Many are wavy to curly and shed lightly, and curlier coats generally shed least. Ask us what we see in the coat of the puppy you are considering."),
      ("How much grooming do they need?",
       "Plan on brushing a few times a week and a professional groom every six to eight weeks. Ask your groomer whether they are comfortable with doodle coats, because it is a different clip. Puppy coats often change texture between six and twelve months, so grooming needs go up for a while during that change."),
      ("How long do they live?",
       "Small doodles commonly live twelve to fifteen years, and smaller dogs generally live longer than large ones. Good care, healthy weight and regular vet visits matter more than size."),
      ("What is their temperament like?",
       "The Cavalier side tends to bring a calm, affectionate, lap-loving nature. The Bernedoodle side brings playfulness and clever, trainable energy. Every puppy is an individual, which is why we socialise them early and match carefully rather than first come first served."),
      ("Are they good with children and other dogs?",
       "Ours are raised around both from day one, with our own kids and our own dogs. We still ask families with very young children to supervise, mostly to protect the puppy."),
      ("Will one be happy in an apartment?",
       "Usually yes. At this size they fit most weight limits, and thirty to sixty minutes of activity a day plus company is enough. What they do not do well is long stretches alone; this is a breed that wants to be with people."),
      ("How much exercise do they need?",
       "Thirty to sixty minutes a day of walks, play, or training games. They are smart, so mental work tires them out as much as running does."),
      ("Are they easy to train?",
       "Both sides of the cross are bright and eager to please, which makes training genuinely enjoyable. Keep sessions short and positive. Ours start on crate and potty training before they leave us."),
      ("Do they bark a lot?",
       "Not usually. They are social rather than guardy, so they tend to greet rather than warn. Any dog will bark if it is bored or left alone too long."),
      ("Are they good for a first-time owner?",
       "Yes, if you can give them company and a routine. They are affectionate, moderate energy, and highly trainable, which is a forgiving combination for a first dog."),
      ("What health testing do the parents have?",
       "<a href=\"our-dogs.html\">Troy</a> has a full Wisdom Panel and we publish it in full, including the one variant she carries. Our Cavalier sire is AKC registered and we are gathering his panel to publish the same way. " + CHIP_DRAFT
       + (" On the Doberman side, Mira has a full genetic panel plus OFA heart and eye screening, and we link her actual records." if SHOW_DOBERMANS else "")),
      ("What comes home with the puppy?",
       "A vaccination and health record, our vet's exam, a small bag of the food they are already eating, a collar and leash, and a toy."
       + (" Doberman puppies also come with AKC registration, a one year genetic health guarantee, microchipping, tail docked and dew claws removed." if SHOW_DOBERMANS else "")),
      ("How do I reserve one, and is the deposit refundable?",
       "A $500 deposit reserves your puppy. It applies to your balance and is transferable to another available puppy if your plans change. Our refund terms are being finalised, so ask us before you put a deposit down and we will tell you plainly."),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": q,
        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    faq_html = "\n".join(
      f'  <details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>'
      for q, a in faq)
    page("what-is-a-munchkin-bernedoodle.html", f"What Is a Munchkin Bernedoodle? | {BRAND}",
      "A plain-language guide to the Munchkin Bernedoodle: the cross, the size, the coat, and the temperament, from a family that breeds them.",
      f"""<section><div class="wrap">
  <div class="grid-2 narrow-left hic">
    <div class="col-title hic-head">
      <p class="eyebrow">Breed guide</p>
      <h1>What is a Munchkin Bernedoodle?</h1>
    </div>
    {img_tag('shiloh-01', cls='framed hic-photo', alt='Shiloh, a blue merle phantom Munchkin Bernedoodle puppy', lazy=False, priority=True, sizes=PHOTO_NARROW)}
    <div class="hic-copy">
      <p class="lede">A Munchkin Bernedoodle is an intentionally small Bernedoodle cross.
      Ours come from a Mini Multi Gen Bernedoodle mom and an AKC Cavalier King Charles
      Spaniel dad, which brings the size down naturally and adds the Cavalier's
      famously gentle temperament.</p>
    </div>
  </div>
</div></section>

<section class="band-raise"><div class="wrap">
  <div class="grid-2 narrow-right hic hic-flip">
    <div class="col-title hic-head"><h2>Where the small size comes from</h2></div>
    {img_tag('troy-01', folder='dogs', cls='framed hic-photo', alt='Troy, our 22 lb Mini Multi Gen Bernedoodle dam', sizes=PHOTO_NARROW)}
    <div class="hic-copy">
      <p>The name confuses people, so here is the honest version. "Munchkin"
        describes small overall size. A Munchkin Bernedoodle is a little dog that keeps
        the Bernedoodle look, usually somewhere between 10 and 25 lbs full grown, where
        a standard Bernedoodle can reach 70 lbs or more.</p>
      <p>Ours come from a small mom at 22 lbs bred to a small dad at 19 lbs. We publish
        each parent's testing on the <a href="our-dogs.html">our dogs</a> page so you can
        read it for yourself rather than take our word for it. {CHIP_DRAFT}</p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <h2 class="center">The three breeds behind the cross</h2>
  <div class="grid-3" style="margin-top:2rem">
    <article class="packet">{img_tag('troy-01', folder='dogs', alt='A Mini Multi Gen Bernedoodle')}
      <div class="packet-body"><p class="packet-name">Bernese and Poodle</p>
        <p class="fine">The Bernedoodle side. From the Bernese come the merle and
          parti coats and an easygoing sweetness. From the Poodle come brains and
          the wavy, often lower-shedding coat.</p></div></article>
    <article class="packet">{img_tag('cavalier-sire-01', folder='dogs', alt='A ruby Cavalier King Charles Spaniel')}
      <div class="packet-body"><p class="packet-name">Cavalier King Charles</p>
        <p class="fine">The small frame, and the calm, cuddly, devoted nature the
          breed is famous for. This is the side that makes them lap dogs.</p></div></article>
    <article class="packet">{img_tag('jordan-01', alt='Jordan, a Munchkin Bernedoodle puppy')}
      <div class="packet-body"><p class="packet-name">The result</p>
        <p class="fine">A small, sturdy, affectionate companion with doodle looks and
          a Cavalier heart. Usually 10 to 25 lbs full grown.</p></div></article>
  </div>
</div></section>

<section class="band-forest"><div class="wrap grid-2 narrow-left hic">
  <div class="hic-head"><h2>Honest words about the coat</h2></div>
  {img_tag('havilah-03', cls='framed hic-photo', alt='Close view of a Munchkin Bernedoodle puppy coat', sizes=PHOTO_NARROW)}
  <div class="hic-copy">
    <p>Doodle coats vary by individual puppy, even within one litter. Many are wavy
      to curly and shed lightly. Some shed more. We will not promise you a
      non-shedding or hypoallergenic dog, because no honest breeder can.</p>
    <p>What we will do is tell you exactly what we see in the coat of the puppy you
      ask about, and let you feel it yourself when you visit.</p>
  </div>
</div></section>

<section style="margin-bottom:0"><div class="wrap">
  <p class="eyebrow center">Common questions</p>
  <h2 class="center">Everything families ask us</h2>
  <p class="lede center" style="max-width:62ch;margin:0 auto 2rem">Tap any question.
    If yours is not here, call or text and ask; we would rather answer twice than
    have you guess.</p>
  <div class="faq">
{faq_html}
  </div>
  <div class="section-cta">
    <p>Still deciding? Meet them on a visit or a video call first.</p>
    <a class="btn btn-primary" href="{'munchkin-bernedoodles.html' if SHOW_DOBERMANS else 'puppies.html'}">See available puppies</a>
    <a class="btn btn-ghost" href="waitlist.html">Join the waitlist</a>
  </div>
</div></section>""",
      extra_head=f'<script type="application/ld+json">{faq_ld}</script>\n')

    M_DOGS = (
      dog_row("troy-01", "Troy", "Mini Multi Gen Bernedoodle", "Agatha Troy",
        "Troy is the mother of our <a href=\"what-is-a-munchkin-bernedoodle.html\">"
        "Munchkin Bernedoodle</a> litter. At 22 lbs she is a "
        "small, easygoing girl with a blue merle parti coat, and she passes on both the "
        "size and the temperament we breed for. " + CHIP_SAMPLE,
        [("Weight:", "22 lbs, blue merle parti, born January 21, 2024."),
         ("Genetic testing:", "Wisdom Panel, tested February 21, 2026. "
          "<strong>Clear on 29 conditions.</strong> Carries one copy of the "
          "chondrodystrophy variant, CDDY. It takes only one copy to matter, so it can "
          "pass to a puppy. The panel explains it on "
          # The published PDF's footers now read 1-11 rather than 4-14, so the CDDY
          # summary and the detail page are pages 1 and 2. Re-check this if the report is
          # ever re-trimmed: a citation pointing at a page that says something else is
          # worse than no citation at all.
          "pages 1 and 2."),
         ("Eyes:", "OFA eye examination, August 14, 2026: <strong>normal</strong>, free "
          "of observable inherited eye disease. Certificate HY-EYE13395/30F-VPI, valid "
          "one year from the exam."),
         ],
        [("Wisdom Panel report (PDF)",
          "records/troy-wisdom-panel-2026-02-21.pdf"),
         ("OFA eye certificate (PDF)",
          "records/troy-ofa-eyes-2026-08-14.pdf")], first=True) +
      dog_row("cavalier-sire-01", "Our Cavalier sire", "Cavalier King Charles Spaniel",
        None,
        "Our sire is an AKC-registered ruby Cavalier, 19 lbs, and the reason these "
        "puppies are as small and as calm as they are. The Cavalier side is where the "
        "lap-dog nature comes from. " + CHIP_SAMPLE,
        [("Registration:", "AKC registered."),
         ("Weight:", "19 lbs, ruby, born December 24, 2024."),
         ("Genetic testing:", "we are gathering his panel and will link it here in full, "
          "the same way we have for Troy. Until it is in our hands we are not going to "
          "characterise his results. " + CHIP_DRAFT)],
        []))
    D_DOGS = (
      dog_row("mira-01", "Mira", "Doberman Pinscher", "Kingdom&rsquo;s Miraculous Grace",
        "Mira is an amazing girl. We love her sweet disposition, her love of guarding "
        "the property, her desire to be a lapdog, and her inquisitive, intelligent "
        "expression. She gets along beautifully with other dogs and with children, and "
        "she makes us feel safe.",
        [("AKC number:", "WS85545303. 70 lbs, black and rust."),
         ("Genetic testing:", "tested through GenSol. Clear, carrier only for DCM3. "
          + '<span class="chip chip-draft">Confirm DCM3 vs DM3</span>'),
         ("OFA:", "certified for heart, by EKG and holter, and for eyes.")],
        [("View Mira\u2019s GenSol Results (PDF)",
          "https://gensol2storageaccount.blob.core.windows.net/certificates/eb11a34d-fa1e-4a4b-ac2f-b5b5bcc6d48e/gensolresult534262.pdf"),
         ("View Mira\u2019s OFA Record", "https://ofa.org/advanced-search?appnum=2720473")],
        ) +
      dog_row("doberman-sire-01", "Our Doberman sire", "Doberman Pinscher", None,
        "Our sire is a big, striking red and rust boy at 100 lbs, and an easy dog to "
        "live with. He is where the Doberman puppies get their size and their steady "
        "confidence. " + CHIP_SAMPLE,
        [("Weight:", "100 lbs, red and rust."),
         ("Genetic testing:", "tested clear."),
         ("Registration:", "name and AKC number being added. " + CHIP_DRAFT)],
        []))

    page("our-dogs.html", "Our Dogs and Their Health | Bless Your Paws Puppies",
      ("Meet the parents: Troy the Mini Multi Gen Bernedoodle, our AKC Cavalier sire, "
       "Mira the health-tested Doberman dam, and our Doberman sire, with testing and "
       "records for each." if SHOW_DOBERMANS else
       "Meet the parents: Troy the Mini Multi Gen Bernedoodle and our AKC Cavalier "
       "sire, with testing and records for each."),
      f"""<section style="padding-bottom:0"><div class="wrap">
  <p class="eyebrow">The parents</p>
  <h1>Our dogs, and what they are tested for</h1>
  <p class="lede" style="max-width:74ch">Health claims are easy to make and hard to
    check. So each dog gets their own testing listed here, and where a record exists we
    link the record itself and put a QR beside it. Scan it with your phone and read the
    original.</p>
</div></section>

<section><div class="wrap">
  <div class="dogpair">{M_DOGS}</div>
  {dob('<div class="dogpair">' + D_DOGS + '</div>')}
</div></section>

{dob_carrier_section_html()}


<section class="band-raise" style="margin-bottom:0"><div class="wrap grid-2 narrow-left">
  <div>
    <p class="eyebrow">Every puppy, before go-home</p>
    <h2>What happens before a puppy leaves us</h2>
    <ul class="checklist">
      <li>Examination by a licensed veterinarian</li>
      <li>Age-appropriate vaccinations and deworming, records in the go-home folder</li>
      <li>Microchipped</li>
      <li>Early neurological stimulation from the first weeks</li>
      <li>A written health guarantee</li>
    </ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="health-guarantee.html">Read the health guarantee</a>
    </div>
  </div>
  {img_tag('eden-02', cls='framed', alt='A Munchkin Bernedoodle puppy being held')}
</div></section>""")

    page("about.html", "About Hope and Joy | Bless Your Paws Puppies",
      f"Two sisters raising {BREEDS_PHRASE}s in their northern Indiana homes.",
      f"""<section><div class="wrap">
  <div class="grid-2 narrow-left hic">
    <div class="col-title hic-head">
      <p class="eyebrow">About us</p>
      <h1>Two sisters, one standard</h1>
    </div>
    <div class="hic-photo">
      <img class="framed wide16" fetchpriority="high" decoding="sync"
        src="img/hope-and-joy.jpg?v={V}"
        srcset="img/r/hope-and-joy-640.webp?v={V} 640w, img/r/hope-and-joy-1000.webp?v={V} 1000w, img/r/hope-and-joy-1400.webp?v={V} 1400w, img/r/hope-and-joy-1672.webp?v={V} 1672w"
        sizes="(max-width:900px) 94vw, 56vw"
        alt="Hope and Joy, the twin sisters behind Bless Your Paws Puppies"
        width="1672" height="941" decoding="async">
    </div>
    <div class="hic-copy">
      <p class="lede">We are Hope and Joy, twin sisters raising puppies in our
        northern Indiana homes. {'Hope raises the Munchkin Bernedoodles and Joy raises the Doberman Pinschers, and every litter' if SHOW_DOBERMANS else 'Every litter'} is raised the same way: in the house,
        around our kids, in the middle of everything. {CHIP_SAMPLE}</p>
      <p>We grew up in a big family where there was always something cooking and
        someone at the door, and our puppies grow up the same way. By the time a puppy
        leaves us it has heard the vacuum, the doorbell, and a houseful of children,
        and it has been held every single day.</p>
      <p class="faith-note">We are Christians, and everything we do here we hope brings
        glory to God. If you have never heard the good news about Jesus, we would love
        for you to <a href="https://www.youtube.com/watch?v=mIeRU12STNw&amp;t=200s"
        target="_blank" rel="noopener">watch this short film</a>.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Say hello</a>
        <a class="btn btn-ghost" href="process.html">How reserving works</a>
      </div>
    </div>
  </div>
</div></section>

<section class="band-raise"><div class="wrap grid-2 lean-left hic hic-flip">
  <div class="hic-head"><h2>Why we do it this way</h2></div>
  {img_tag('joshua-02', cls='framed hic-photo', alt='A Munchkin Bernedoodle puppy in the grass', sizes='(max-width:900px) 94vw, 56vw')}
  <div class="hic-copy">
    <p>A puppy's first eight weeks decide a lot about the dog they become. That is
      why ours are never raised apart from the household. They meet children, other
      dogs, the vacuum, and visitors before they ever meet you. {CHIP_SAMPLE}</p>
    <p>We would love for you to meet the puppies, and <a href="our-dogs.html">their
      parents</a>, before you decide. Visits are by appointment, and video calls work well for families
      further away.</p>
  </div>
</div></section>

<section class="closing" style="margin-bottom:0"><div class="wrap">
  <div class="inner">
    <h2>Come and meet them</h2>
    <p class="contact-line">Visits are by appointment, and video calls work well if
      you are further away.</p>
    <div class="contact-pair">
      <a class="contact-tile" href="{PHONE_HREF}">
        <span class="ct-label">{'Hope, Munchkins' if SHOW_DOBERMANS else 'Hope'}</span>
        <span class="ct-value">{PHONE_DISPLAY}</span>
      </a>
      <a class="contact-tile" href="{JOY_PHONE_HREF}">
        <span class="ct-label">{'Joy, Dobermans' if SHOW_DOBERMANS else 'Joy'}</span>
        <span class="ct-value">{JOY_PHONE_DISPLAY}</span>
      </a>
      <a class="contact-tile" href="mailto:{EMAIL}">
        <span class="ct-label">Email us</span>
        <span class="ct-value">{EMAIL}</span>
      </a>
    </div>
    <div class="btn-row">
      <a class="btn btn-primary" href="puppies.html">See available puppies</a>
      <a class="btn btn-ghost" href="contact.html">Send an inquiry</a>
    </div>
  </div>
</div></section>""")

    SHARED_KIT = [k for k in M_KIT if k in D_KIT]
    M_ONLY_KIT = [k for k in M_KIT if k not in D_KIT]
    D_ONLY_KIT = [k for k in D_KIT if k not in M_KIT]
    dob_kit_col = dob('<div><h3>Doberman Pinschers</h3><ul class="checklist">'
                      + ''.join(f'<li>{i}</li>' for i in D_ONLY_KIT) + '</ul></div>')
    # With two litters the useful split is shared versus breed-specific. With one there is
    # nothing to contrast, so it is a single list rather than two cards saying the same
    # thing in two halves.
    if SHOW_DOBERMANS:
        kit_cards = ('<div><h3>Every puppy</h3><ul class="checklist">'
                     + ''.join(f'<li>{i}</li>' for i in SHARED_KIT) + '</ul></div>'
                     '<div><h3>Munchkin Bernedoodles</h3><ul class="checklist">'
                     + (''.join(f'<li>{i}</li>' for i in M_ONLY_KIT)
                        or '<li>The shared list above</li>') + '</ul></div>'
                     + dob_kit_col)
    else:
        kit_cards = ('<div><h3>Every puppy goes home with</h3><ul class="checklist">'
                     + ''.join(f'<li>{i}</li>' for i in M_KIT) + '</ul></div>')

    steps = [
      ("Say hello", "havilah-02",
       "Browse the <a href=\"puppies.html\">available puppies</a>, then call, text, or "
       "send the inquiry form. Tell us "
       "a little about your family and who caught your eye. There is no application fee "
       "and no pressure.",
       'Most families text a photo of the puppy they like and go from there. '
       '<a href="puppies.html">See who is available</a>.'),
      ("Meet the puppy", "malcolm-02" if SHOW_DOBERMANS else "jordan-02",
       "We set up a visit or a video call so you can meet the puppy, meet the parents, "
       "and meet us. Ten minutes is usually enough to know. We would rather talk you out "
       "of the wrong puppy than sell you one.",
       "Visits are by appointment. Our exact location is shared once your visit is booked."),
      ("Reserve with a deposit", "caleb-01",
       f"A ${DEPOSIT} deposit holds your puppy while they finish growing up with us. It "
       "applies to your balance, and it is transferable to another available puppy if "
       "your plans change.",
       f'Refund terms are being finalised. {CHIP_DRAFT}'),
      ("Watch them grow", "jericho-02",
       "We send photos and updates right up to go-home day, and you can ask for more "
       "any time. Plenty of families end up on a first-name basis with us before they "
       "ever pick the puppy up.",
       "Ask us anything in between. We would rather over-communicate."),
      ("Go-home day", "shiloh-02",
       "Puppies go home from eight weeks, after their final vet check. You leave with the "
       "health records, the paperwork, and a puppy who already knows what a family sounds "
       "like.",
       f'Pickup is by appointment. Delivery options are being finalised. {CHIP_DRAFT}'),
    ]
    steps_html = "\n".join(
      f'''    <article class="step">
      <div class="step-media">{img_tag(stem, alt=title, sizes="(max-width:460px) 92vw, (max-width:760px) 46vw, (max-width:1100px) 30vw, 19vw", lazy=(i > 1), priority=(i == 1))}</div>
      <div class="step-head"><span class="step-num">{i}</span><h3>{title}</h3></div>
      <p>{body}</p>
      <p class="fine">{note}</p>
    </article>'''
      for i, (title, stem, body, note) in enumerate(steps, 1))

    page("process.html", "How It Works | Bless Your Paws Puppies",
      f"From first hello to go-home day: inquire, meet the puppy, reserve with a ${DEPOSIT} deposit, watch them grow, and take your puppy home.",
      f"""<section style="padding-bottom:0"><div class="wrap">
  <p class="eyebrow">How it works</p>
  <h1>From first hello to go-home day</h1>
  <p class="lede" style="max-width:68ch">Five steps, no pressure, and a real
    conversation somewhere in the middle. Here is exactly what happens, so nothing
    about buying a puppy from us is a surprise.</p>
</div></section>

<section><div class="wrap">
  <div class="steps-row">
{steps_html}
  </div>
</div></section>

<section class="band-raise"><div class="wrap">
  <p class="eyebrow center">In the go-home bag</p>
  <h2 class="center">What comes home with your puppy</h2>
  <p class="lede center" style="max-width:56ch;margin:.5rem auto 2rem">{'Both litters leave' if SHOW_DOBERMANS else 'Every puppy leaves'}
    with their paperwork, their food, and something that smells like home.</p>
  <div class="tri{'' if SHOW_DOBERMANS else ' one'}">
    {kit_cards}
  </div>
  <div class="section-cta">
    <p>{'Both litters come with a' if SHOW_DOBERMANS else 'Every puppy comes with a'} <a href="health-guarantee.html">written health guarantee</a>.</p>
    <a class="btn btn-primary" href="health-guarantee.html">Read the guarantee</a>
  </div>
</div></section>

<section class="band-pink" style="margin-bottom:0"><div class="wrap grid-2 narrow-left hic">
  <div class="hic-head">
    <p class="eyebrow">Before you ask</p>
    <h2>The questions we get most</h2>
  </div>
  {img_tag('eden-03', cls='framed hic-photo', alt='A Munchkin Bernedoodle puppy')}
  <div class="hic-copy">
    <p><strong>How do payments work?</strong> The ${DEPOSIT} deposit reserves your puppy
      online. The balance is due before or at pickup, and most families pay it by check
      or bank transfer. {CHIP_DRAFT}</p>
    <p><strong>Can we visit first?</strong> Yes, and we encourage it. Video calls work
      well for families further away.</p>
    <p><strong>Will my puppy shed?</strong> It varies by puppy, even in one litter. We
      never promise a non-shedding coat.
      <a href="what-is-a-munchkin-bernedoodle.html">More on coats</a>.</p>
  </div>
</div></section>""")

    page("contact.html", "Contact | Bless Your Paws Puppies",
      "Ask about an available puppy or plan a visit. Call or text Hope, email us, or send the inquiry form.",
      f"""<section><div class="wrap">
  <div class="contact-grid">
    <div class="cg-head">
      <p class="eyebrow">Contact</p>
      <h1 style="margin-bottom:0">Say hello</h1>
    </div>
    <div class="cg-gap" aria-hidden="true"></div>
    <div>
      <p class="lede" style="margin:0 0 1.25rem">The fastest way to reach us is a call
        or a text. Tell us which puppy caught your eye and a little about your family,
        and we will get right back to you.</p>
      <div class="formcard">
        <h2 style="margin-top:0">Send an inquiry</h2>
        <form data-guard action="https://formspree.io/f/REPLACE_FORM_ID" method="POST">
        {hp.format(i="c")}<div class="field"><label for="name">Your name</label><input id="name" name="name" required></div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
        <div class="field"><label for="phone">Phone (optional)</label><input id="phone" name="phone"></div>
        <div class="field"><label for="message">Which puppy caught your eye, and a little about your family</label>
          <textarea id="message" name="message" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send inquiry</button>
        <p class="guard-msg">The form is almost ready. For now, call or text Hope at
          <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a> and we will get right back to you.</p>
        </form>
      </div>
    </div>
    <div>
      <div class="formcard">
        <h2 style="margin-top:0">How to reach us</h2>
        <ul class="facts">
          <li><span class="k">Hope, Munchkin Bernedoodles</span>
            <span class="v"><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></span></li>
          <li><span class="k">{'Joy, Dobermans' if SHOW_DOBERMANS else 'Joy'}</span>
            <span class="v"><a href="{JOY_PHONE_HREF}">{JOY_PHONE_DISPLAY}</a></span></li>
          <li><span class="k">Email</span>
            <span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
          <li><span class="k">Where</span><span class="v">{AREA}</span></li>
          <li><span class="k">Visits</span><span class="v">By appointment</span></li>
        </ul>
        <p class="fine" style="margin-bottom:0">Our exact location is shared once your
          visit is scheduled. Video calls work well for families further away.</p>
      </div>
      {img_tag('jordan-01', cls='framed', alt='Jordan, a blue merle parti Munchkin Bernedoodle puppy', sizes='(max-width:900px) 94vw, 44vw', lazy=False, priority=True)}
    </div>
  </div>
</div></section>

""")

    page("waitlist.html", "Join the Waitlist | Bless Your Paws Puppies",
      "Hear about new litters before they are listed. Waitlist families get first pick.",
      f"""<section><div class="wrap">
  <p class="eyebrow">The waitlist</p>
  <h1>Hear about litters first</h1>
  <div class="grid-2" style="align-items:start;margin-top:1.25rem">
  <div>
    <p class="lede">Our litters tend to reserve quickly. One puppy from the current
      litter went home to a waitlist family before it was ever listed publicly.</p>
    <p>Joining costs nothing and commits you to nothing. When a new litter arrives,
      waitlist families hear first, in the order they joined, and get first chance to
      reserve.</p>
    {img_tag('jordan-02', cls='framed', alt='Jordan, a blue merle parti Munchkin Bernedoodle puppy', lazy=False, priority=True)}
  </div>
  <div class="formcard">
    <h2 style="margin-top:0">Add your name</h2>
    <form data-guard action="https://formspree.io/f/REPLACE_WAITLIST_ID" method="POST">
    {hp.format(i="w")}<div class="field"><label for="wname">Your name</label><input id="wname" name="name" required></div>
    <div class="field"><label for="wemail">Email</label><input id="wemail" name="email" type="email" required></div>
    <div class="field"><label for="wphone">Phone (optional)</label><input id="wphone" name="phone"></div>
    <div class="field"><label for="wline">Which puppies are you hoping for?</label>
      <select id="wline" name="line">
        <option>Munchkin Bernedoodles</option>
{dob('        <option>Doberman Pinschers</option>')}
        <option>Either, tell me about both</option>
      </select></div>
    <div class="field"><label for="wwhen">When are you hoping to bring a puppy home?</label>
      <input id="wwhen" name="timing" placeholder="This year, next spring, whenever the right one comes"></div>
    <button class="btn btn-primary" type="submit">Join the waitlist</button>
    <p class="guard-msg">The form is almost ready. For now, text Hope at
      <a href="{SMS_HREF}">{PHONE_DISPLAY}</a> with the word WAITLIST and your name.</p>
    </form>
  </div>
  </div>
</div></section>""")

    items = []
    for s, n, _, c, _ in MUNCHKINS:
        for i in range(1, COUNTS[s] + 1):
            items.append((f"{s}-{i:02d}", n, "munchkin", s))
    for s, n, _, c, _ in D_LIST:
        for i in range(1, COUNTS[s] + 1):
            items.append((f"{s}-{i:02d}", n, "doberman", s))
    # tiles sit in their own grid, not the section column, so they need their own hint
    GAL_SIZES = ("(max-width:460px) 46vw, (max-width:760px) 31vw, "
                 "(max-width:1100px) 24vw, 22vw")
    gal = "\n".join(f'<a data-line="{line}" data-pup="{slug}" href="puppy-{slug}.html">'
                    f'{img_tag(stem, alt=name, sizes=GAL_SIZES, lazy=(k>0), priority=(k==0))}</a>'
                    for k, (stem, name, line, slug) in enumerate(items))
    pup_opts = "\n".join(f'        <option value="{sl}">{nm}</option>'
                         for sl, nm, *_ in list(MUNCHKINS) + D_LIST)
    page("gallery.html", "Photo Gallery | Bless Your Paws Puppies",
      "Every photo of our Munchkin Bernedoodle puppies." if not SHOW_DOBERMANS
      else "Every photo of our Munchkin Bernedoodle and Doberman Pinscher puppies.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Gallery</p>
  <h1>The photo album</h1>
  <p class="lede">Every photo of the puppies who are with us right now. Click any
    photo to meet that puppy.</p>
  <div class="filter-row" style="margin-top:1.5rem">
    <button class="cur" data-line="all">All photos</button>
    <button data-line="munchkin">Munchkin Bernedoodles</button>
{dob('    <button data-line="doberman">Dobermans</button>')}
    <label class="filter-select">
      <span class="visually-hidden">Filter by puppy</span>
      <select id="pup-select">
        <option value="all">By puppy</option>
{pup_opts}
      </select>
    </label>
  </div>
  <p class="fine" id="gal-count" aria-live="polite" style="margin:.25rem 0 1.25rem"></p>
  <div class="gal-grid">{gal}</div>
</div></section>""")

    page("reviews.html", "Reviews | Bless Your Paws Puppies",
      "What families say about their Bless Your Paws puppies.",
      f"""<section><div class="wrap">
  <div class="grid-2 narrow-left hic">
    <div class="col-title hic-head">
      <p class="eyebrow">Reviews</p>
      <h1>From our families</h1>
      <p class="fine" style="margin:0">{CHIP_SAMPLE}</p>
    </div>
    {img_tag('havilah-02', cls='framed hic-photo', alt='Havilah, a blue merle phantom Munchkin Bernedoodle puppy', lazy=False, priority=True)}
    <div class="hic-copy">
      <blockquote class="lede" style="border-left:3px solid var(--sage);padding-left:1.25rem;margin:0 0 1.5rem">
        "Our puppy came home confident, snuggly, and already used to kids. You can
        tell she was raised in the middle of a family."
        <span class="fine">A waitlist family</span></blockquote>
      <p>We are collecting reviews from our puppy families now, with their permission,
        and will post them here as they come in. If you have one of our puppies, we
        would love to hear from you.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Share your story</a></div>
    </div>
  </div>
</div></section>""")

    page("health-guarantee.html", "Health Guarantee | Bless Your Paws Puppies",
      "Our written health guarantee for every puppy.",
      f"""<section><div class="wrap prose">
  <div class="draft-banner">DRAFT. This guarantee is a working draft prepared for
    Hope and Joy to review, reword, and approve. It is not in effect as written.</div>
  <p class="eyebrow">Health guarantee</p>
  <h1>Our health guarantee</h1>
  <h3>What we promise</h3>
  <ul>
    <li>Your puppy goes home current on age-appropriate vaccinations and deworming,
      with the records to show it.</li>
    <li>Your puppy is examined by a licensed veterinarian before go-home.</li>
    <li>For one year from birth, we guarantee your puppy against life-threatening
      congenital or hereditary conditions diagnosed by a licensed veterinarian.</li>
  </ul>
  <h3>What we ask of you</h3>
  <ul>
    <li>Have your own veterinarian examine the puppy within 72 hours of go-home. If a
      significant pre-existing condition is found, contact us immediately.</li>
    <li>Keep up routine veterinary care, vaccinations, and a safe environment.</li>
    <li>Send us the diagnosis in writing from your veterinarian before any claim.</li>
  </ul>
  <h3>The remedy</h3>
  <p>If a covered condition is confirmed, we will offer a replacement puppy from an
    upcoming litter or a refund of the purchase price, at our option. This guarantee
    does not cover veterinary bills, and it does not cover conditions caused by
    injury, neglect, or parasites after go-home. Adult size, coat, and color are not
    guaranteed.</p>
  <p class="fine">Questions about the guarantee? Ask before you reserve; we would
    rather explain it twice than surprise anyone once.</p>
</div></section>""")

    page("purchase-agreement.html", "Purchase Agreement | Bless Your Paws Puppies",
      "The purchase agreement every family signs at reservation.",
      f"""<section><div class="wrap prose">
  <div class="draft-banner">DRAFT. This agreement is a working draft prepared for
    Hope and Joy to review, reword, and approve. It is not in effect as written.</div>
  <p class="eyebrow">Purchase agreement</p>
  <h1>Purchase agreement</h1>
  <p>This agreement is between Bless Your Paws Puppies and the buyer named at
    reservation, for the puppy identified by name and litter.</p>
  <ul>
    <li><strong>Price and deposit.</strong> The purchase price is the listed price of
      the puppy. A ${DEPOSIT} deposit reserves the puppy and is applied to the
      balance. The balance is due before or at pickup.</li>
    <li><strong>Deposit terms.</strong> The deposit is transferable to another
      available puppy if plans change. Refund terms to be confirmed. {CHIP_DRAFT}</li>
    <li><strong>Go-home.</strong> Puppies go home no earlier than 8 weeks of age,
      after a final veterinary check.</li>
    {dob_reg_clause}
    <li><strong>Health.</strong> The puppy is sold with the
      <a href="health-guarantee.html">written health guarantee</a>, which is part of
      this agreement.</li>
    <li><strong>Care.</strong> The buyer agrees to provide routine veterinary care and
      a safe home.</li>
    <li><strong>Return first.</strong> If at any point the buyer can no longer keep
      the dog, we are contacted first and given the option to take the dog back before
      it is rehomed or surrendered.</li>
  </ul>
  <p class="fine">A signed copy goes home in the go-home folder with the health
    records.</p>
</div></section>""")

    page("privacy-policy.html", "Privacy Policy | Bless Your Paws Puppies",
      "How this website handles your information.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">Privacy</p>
  <h1>Privacy policy</h1>
  <p>{CHIP_DRAFT}</p>
  <p>This is a small family website. We collect only what you send us: your name and
    contact details when you use the inquiry or waitlist forms, or when you call or
    text. We use that information to reply to you and to manage reservations, and we
    do not sell it or share it with anyone for marketing.</p>
  <p>Forms are processed by our form provider, and card payments are processed by
    Stripe on Stripe's own secure pages; card details never touch this website. This
    site does not use advertising or analytics cookies.</p>
  <p>To have your information removed, call or text {PHONE_DISPLAY} or email
    <a href="mailto:{EMAIL}">{EMAIL}</a> and we will delete it.</p>
</div></section>""")

    page("404.html", "Page Not Found | Bless Your Paws Puppies",
      "That page wandered off.",
      f"""<section><div class="wrap center">
  <p class="eyebrow">404</p>
  <h1>This page wandered off</h1>
  <p class="lede">Probably chasing something. Try the puppies instead.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-primary" href="puppies.html">Available puppies</a>
    <a class="btn btn-ghost" href="index.html">Home</a>
  </div>
</div></section>""")

    # ---- per-puppy pages
    def puppy_page(slug, name, sex, colour, note, price, breed, born, home, kit,
                   parents_html, extra_facts):
        him = "him" if sex == "Boy" else "her"
        # Hope raises the Munchkin Bernedoodles, Joy the Dobermans. A buyer asking
        # about one of Joy's puppies was being told to call Hope.
        is_munchkin = breed.startswith('Munchkin')
        owner = "Hope" if is_munchkin else "Joy"
        owner_href = PHONE_HREF if is_munchkin else JOY_PHONE_HREF
        owner_phone = PHONE_DISPLAY if is_munchkin else JOY_PHONE_DISPLAY
        # Spoken for, but still here: she goes home with her littermates. Nothing on the
        # page invites a deposit, and nothing claims she has already left.
        if slug in ADOPTED:
            her = "her" if sex == "Girl" else "his"
            reserve_block = (
              '<div class="reserve is-adopted">'
              f'<h3>{name} is adopted</h3>'
              f'<p class="fine">{name} has found {her} family and goes home on {home}, '
              'the same day as the rest of the litter. She is on the site so you can see '
              'the whole litter, not because she is available.</p>'
              '<p class="fine">Hoping for one like her? '
              '<a href="puppies.html">See who is available</a> or '
              '<a href="waitlist.html">join the waitlist</a> for a future litter.</p>'
              '</div>')
        else:
            reserve_block = f'''<div class="reserve">
        <h3>Reserve {name}</h3>
        <p class="fine">A ${DEPOSIT} deposit holds {him} until go-home day. Pay the
          deposit now, or the full amount if you prefer.</p>
        <div class="pay-row">
          <a class="btn btn-primary pay-link" href="https://buy.stripe.com/REPLACE_DEPOSIT">Deposit &middot; ${DEPOSIT}</a>
          <a class="btn btn-ghost pay-link" href="https://buy.stripe.com/REPLACE_FULL">Full payment</a>
          <a class="btn btn-ghost pay-link" href="https://buy.stripe.com/REPLACE_BALANCE">Balance</a>
        </div>
        <p class="guard-msg">Online payments are almost ready. To reserve {name}
          today, call or text {owner} at <a href="{owner_href}">{owner_phone}</a>.</p>
        <p class="fine">Prefer to talk first? <a href="contact.html">Start an
          inquiry</a>, or call or text <a href="{owner_href}">{owner_phone}</a>.
          Visits and video calls are always welcome before you decide.</p>
      </div>'''
        cnt = COUNTS[slug]
        first = PRIMARY.get(slug, 1)
        order = [first] + [i for i in range(1, cnt + 1) if i != first]
        slides = "\n".join(
            "        " + img_tag(f"{slug}-{i:02d}", alt=f"{name}, photo {k+1}",
                                 lazy=(k > 0), hidden=(k > 0), priority=(k == 0),
                                 sizes=PUPPY_HERO_SIZES)
            for k, i in enumerate(order))
        thumbs = "\n".join(
            f'        <button aria-current="{"true" if k==0 else "false"}" '
            f'aria-label="Photo {k+1}"><img src="img/r/{slug}-{i:02d}-320.webp'
            f'{asset_v(f"img/r/{slug}-{i:02d}-320.webp")}" alt="" '
            f'loading="lazy"></button>' for k, i in enumerate(order))
        sibs = MUNCHKINS if breed.startswith("Munchkin") else DOBERMANS
        sib = " &middot; ".join(f'<a href="puppy-{s}.html">{n}</a>'
                               for s, n, *_ in sibs if s != slug)
        # with one breed the litter page is puppies.html, so the crumb points there
        breed_page = ('munchkin-bernedoodles' if (is_munchkin and SHOW_DOBERMANS)
                      else 'puppies' if is_munchkin else 'dobermans')
        # The structured data is the machine-readable copy of the same claim, and it was
        # still saying InStock, "available now" and $2,000 for an adopted puppy long after
        # the visible page stopped. Google reads this for rich results, so it is the one
        # that would have kept offering her for sale in search.
        adopted = slug in ADOPTED
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product",
            "name": f"{name}, {breed} puppy", "image": f"{BASE}/img/puppies/{lead(slug)}.jpg",
            "description": (f"{name} is a {colour.lower()} {breed} puppy from our litter, "
                            f"already adopted." if adopted else
                            f"{name} is a {colour.lower()} {breed} puppy, available now."),
            "offers": {"@type": "Offer", "priceCurrency": "USD", "price": str(price),
                       "availability": ("https://schema.org/SoldOut" if adopted
                                        else "https://schema.org/InStock")}})
        page(f"puppy-{slug}.html", f"{name}, {breed} Puppy | {BRAND}",
          # an adopted puppy's description must not advertise a price or a deposit: that
          # is the line search engines and link previews show, so it is the one place a
          # sold puppy most easily looks available
          (f"{name} is a {colour.lower()} {breed} puppy from our litter, already adopted "
           f"and going home {home}."
           if slug in ADOPTED else
           f"{name} is a {colour.lower()} {breed} puppy. ${price:,} with a ${DEPOSIT} deposit to reserve."),
          f"""<section><div class="wrap">
  <p class="eyebrow"><a href="puppies.html">Available puppies</a> /
    <a href="{breed_page}.html">{breed}s</a></p>
  <div class="puppy-top">
    <div class="carousel" tabindex="0">
      <div class="frame">
        <button class="cnav cprev" aria-label="Previous photo">&#8249;</button>
        <button class="cnav cnext" aria-label="Next photo">&#8250;</button>
        <span class="count">1 / {cnt}</span>
{slides}
      </div>
      <div class="cthumbs">
{thumbs}
      </div>
    </div>
    <div class="puppy-info">
      <div class="name-row"><h1>{name}</h1>{'<span class="status status-adopted">Adopted!</span>' if slug in ADOPTED else f'<span class="price">${price:,}</span>'}</div>
      <p class="lede">{sex} &middot; {colour} &middot; {breed}</p>
      <ul class="facts">
        <li><span class="k">Status</span><span class="v">{'Adopted!' if slug in ADOPTED else 'Available'}</span></li>
        <li><span class="k">Sex</span><span class="v">{sex}</span></li>
        <li><span class="k">Color</span><span class="v">{colour}</span></li>
        <li><span class="k">Born</span><span class="v">{born}</span></li>
        <li><span class="k">Go home</span><span class="v">{home}</span></li>
{extra_facts}
      </ul>
      {f'<p><strong>{note}</strong></p>' if note else ''}
      {reserve_block}
      <h3>About {name} {CHIP_SAMPLE}</h3>
      <p>{name} is a {colour.lower()} {sex.lower()} growing up in the house, handled
        every day, around kids and other dogs, with early neurological stimulation
        from the first weeks. Ask us anything about {him}; we are happy to send more
        photos or hop on a video call.</p>
      {share_row(name, f'puppy-{slug}.html', f'img/puppies/{lead(slug)}.jpg')}
    </div>
  </div>
</div></section>

<section class="band-raise"><div class="wrap">
  <h2>{name}'s parents</h2>
  <div class="parent-grid" style="margin-top:1.5rem">{parents_html}</div>
  <div class="btn-row"><a class="btn btn-ghost" href="our-dogs.html">Full health details</a></div>
</div></section>

<section><div class="wrap">
  <div class="grid-2" style="align-items:start">
    <div>
      <h2>What comes home with {name}</h2>
      <ul class="checklist">{''.join(f'<li>{i}</li>' for i in kit)}</ul>
    </div>
    <div>
      <h2>{name}'s littermates</h2>
      <p>{sib}</p>
      <div class="btn-row"><a class="btn btn-ghost" href="puppies.html">See all puppies</a></div>
    </div>
  </div>
</div></section>""",
          extra_head=f'<script type="application/ld+json">{ld}</script>\n')

    m_facts = ('        <li><span class="k">Expected adult size</span>'
               f'<span class="v">{M_SIZE} (draft)</span></li>')
    d_facts = ('        <li><span class="k">Registration</span><span class="v">AKC</span></li>\n'
               '        <li><span class="k">Breeding rights</span><span class="v">$500 extra</span></li>')
    for s, n, x, c, note in MUNCHKINS:
        puppy_page(s, n, x, c, note, M_PRICE, "Munchkin Bernedoodle", M_BORN, M_HOME,
                   M_KIT, M_PARENTS, m_facts)
    for s, n, x, c, note in D_LIST:
        puppy_page(s, n, x, c, note, D_PRICE, "Doberman Pinscher", D_BORN, D_HOME,
                   D_KIT, D_PARENTS, d_facts)

def build_assets():
    open("style.css", "w", encoding="utf-8").write(CSS)
    open("main.js", "w", encoding="utf-8").write(prettify_links(JS))
    os.makedirs("img/placeholder", exist_ok=True)

    def ph(fname, label, sub="Photo coming soon"):
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 750">
<rect width="1000" height="750" fill="#a8b89e"/>
<rect x="26" y="26" width="948" height="698" fill="none" stroke="#fdf9f9" stroke-width="3" stroke-dasharray="12 9"/>
<g transform="translate(500 300)" fill="#fdf9f9">
 <ellipse cx="0" cy="42" rx="62" ry="55"/>
 <ellipse cx="-66" cy="-30" rx="28" ry="36"/>
 <ellipse cx="-22" cy="-56" rx="26" ry="34"/>
 <ellipse cx="22" cy="-56" rx="26" ry="34"/>
 <ellipse cx="66" cy="-30" rx="28" ry="36"/>
</g>
<text x="500" y="512" text-anchor="middle" font-family="Georgia,serif" font-size="52" fill="#223d2c">{label}</text>
<text x="500" y="570" text-anchor="middle" font-family="Georgia,serif" font-size="32" fill="#34523f">{sub}</text>
</svg>"""
        open(f"img/placeholder/{fname}", "w", encoding="utf-8").write(svg)

    ph("doberman-sire.svg", "The Doberman sire")
    ph("hope-and-joy.svg", "Hope and Joy", "A photo of the sisters goes here")

    from PIL import Image
    mark = Image.open("img/brand/mark-paw-heart.png").convert("RGBA")
    mark = mark.crop(mark.getbbox())
    side = max(mark.size); pad = int(side * 0.10)
    sq = Image.new("RGBA", (side + 2*pad, side + 2*pad), (0, 0, 0, 0))
    sq.paste(mark, ((sq.width - mark.width)//2, (sq.height - mark.height)//2), mark)
    sq.resize((48, 48), Image.LANCZOS).save("img/favicon.png")
    apple = Image.new("RGBA", sq.size, (253, 249, 249, 255))
    apple.paste(sq, (0, 0), sq)
    apple.convert("RGB").resize((180, 180), Image.LANCZOS).save("img/apple-touch-icon.png")
    sq.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    logo = Image.open("img/brand/logo-horizontal-forest.png").convert("RGBA")
    og = Image.new("RGB", (1200, 630), (253, 249, 249))
    lw = 1000; lh = round(logo.height * lw / logo.width)
    lr = logo.resize((lw, lh), Image.LANCZOS)
    og.paste(lr, ((1200 - lw)//2, (630 - lh)//2), lr)
    og.save("img/og-card.png", "PNG")

def build_meta():
    open("robots.txt", "w", encoding="utf-8").write(
        "# Draft mode: closed until launch. At launch switch to Allow: / and\n"
        "# remove the noindex meta from every page.\n"
        "User-agent: *\nDisallow: /\n")
    # Built from what page() actually generated, NOT from a directory glob. A glob picks
    # up every hand-written file in the root too, and this project creates throwaway
    # comparison pages by convention (hero-options.html, floral-preview.html,
    # floral-applied.html). Excluding them by filename suffix was tried and leaked:
    # the list covered "-preview.html" and "-options.html", so floral-applied.html was
    # submitted for indexing for as long as it existed. A page that was never generated
    # cannot be in the list, which is a rule that does not need maintaining.
    skip = ("404.html",)
    pages = [p for p in sorted(GENERATED) if p not in skip]
    urls = "\n".join(f"  <url><loc>{BASE}/{pretty_path(p)}</loc></url>" for p in pages)
    open("sitemap.xml", "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')

if __name__ == "__main__":
    build_assets()
    build_pages()
    build_meta()
    print(f"scaffold v{V}: {len([p for p in os.listdir('.') if p.endswith('.html')])} pages")
