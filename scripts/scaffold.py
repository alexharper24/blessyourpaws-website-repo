#!/usr/bin/env python3
"""Phase 1 scaffold for blessyourpaws-website-repo.

Run scripts/prep_images.py FIRST (it splits the parents out of the puppy
galleries and writes img/photo-counts.json), then run this.

Re-running OVERWRITES every generated page, so fold hand edits back into this
script rather than editing the HTML.

Draft mode: noindex on every page, robots.txt closed, until launch.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

V = 3
BASE = "https://alexharper24.github.io/blessyourpaws-website-repo"
PHONE_DISPLAY = "(574) 377-8023"
PHONE_HREF = "tel:5743778023"
SMS_HREF = "sms:5743778023"
EMAIL = "info@blessyourpawspuppies.com"
AREA = "Warsaw and Winona Lake, Indiana"
COUNTS = json.load(open("img/photo-counts.json"))

MUNCHKINS = [
    ("joshua",  "Joshua",  "Boy",  "Red and white parti", ""),
    ("eden",    "Eden",    "Girl", "Red with white",      ""),
    ("havilah", "Havilah", "Girl", "Blue merle phantom",  ""),
    ("jordan",  "Jordan",  "Boy",  "Blue merle parti",    "The biggest of the litter so far."),
    ("caleb",   "Caleb",   "Boy",  "Red and white parti", ""),
    ("shiloh",  "Shiloh",  "Boy",  "Blue merle phantom",  ""),
    ("jericho", "Jericho", "Boy",  "Blue merle parti",    ""),
]
DOBERMANS = [
    ("elowen",  "Elowen",  "Girl", "Black and rust", "Ready for any adventure, and working on crate and leash training."),
    ("malcolm", "Malcolm", "Boy",  "Black and rust", "Eager to please, and doing well learning to sit and stay."),
    ("griffin", "Griffin", "Boy",  "Black and rust", "An outgoing boy who makes friends with everyone."),
]
M_PRICE, D_PRICE, DEPOSIT = 2000, 2200, 500
M_BORN, M_HOME = "July 22, 2026", "September 16 to 23, 2026"
D_BORN, D_HOME = "April 14, 2026", "Ready now"

CHIP_DRAFT  = '<span class="chip chip-draft">Draft, confirm before launch</span>'
CHIP_SAMPLE = '<span class="chip chip-sample">Sample copy, waiting on their words</span>'
CHIP_PHOTO  = '<span class="chip chip-draft">Photo coming</span>'
SIZE_DRAFT  = ('<span class="chip chip-draft">Draft estimate from the 19 lb and 21 lb '
               'parents, Hope to confirm</span>')

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
/* Petrona replaces Fraunces. Fraunces draws a descending, hooked lowercase f as
   part of its design, which the WONK axis does not undo. Petrona keeps the warm
   old-style vintage feel with a normal f. */
h1,h2,h3,.display,.packet-name,.price{font-family:"Petrona",Georgia,serif;
  font-feature-settings:"liga" 0,"dlig" 0,"swsh" 0}
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
.brand img{height:84px;width:auto}
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

/* ---------- hero ---------- */
.hero{padding:3rem 0 2.5rem}
.hero-split{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(2rem,4vw,4rem);
  align-items:center}
.framed{width:100%;border-radius:6px;border:1.5px solid var(--forest);
  box-shadow:0 2px 0 var(--sage-light)}
.hero-split .framed{aspect-ratio:3/2;object-fit:cover}
/* section imagery: give photos real presence, they are the product */
.grid-2 .framed{aspect-ratio:3/2;object-fit:cover}
.grid-2.narrow-left{grid-template-columns:.8fr 1.2fr}
.grid-2.narrow-right{grid-template-columns:1.2fr .8fr}
.btn{display:inline-flex;align-items:center;text-decoration:none;border-radius:3px;
  font-weight:700;padding:.75rem 1.35rem;border:1.5px solid var(--forest);
  font-size:1rem;min-height:48px}
.btn-primary{background:var(--forest);color:var(--paper)}
.btn-primary:hover{background:var(--forest-soft)}
.btn-ghost{background:transparent;color:var(--forest)}
.btn-ghost:hover{background:var(--paper-raise)}
.btn-row{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.4rem}
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
.band-raise{background:var(--paper-raise)}

/* ---------- cards ---------- */
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:clamp(1.25rem,2vw,2rem)}
/* an exact column count so a small litter spans the full width instead of
   clustering at the left with dead space beside it */
.pgrid.cols-3{grid-template-columns:repeat(3,1fr)}
.pgrid.cols-4{grid-template-columns:repeat(4,1fr)}
.pgrid.cols-7{grid-template-columns:repeat(4,1fr)}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,3vw,3rem);
  align-items:center}
.grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:clamp(1.25rem,2vw,2rem)}
.packet{position:relative;background:#fff;border:1.5px solid var(--forest);
  border-radius:4px;padding:11px;display:flex;flex-direction:column;height:100%}
.packet::before{content:"";position:absolute;inset:5px;border:1px dashed var(--sage);
  border-radius:2px;pointer-events:none}
.packet img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:2px}
/* parent portraits are a mix of landscape and portrait originals. a 4/5 frame
   with a top-biased crop keeps every head in shot and makes the cards align. */
.packet.parent img,.door.parent img{aspect-ratio:4/5;object-position:50% 22%}
.parent-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:clamp(1.25rem,2vw,2rem);align-items:stretch}
.parent-grid .packet-body{gap:.35rem}
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
a.packet-link{text-decoration:none}
a.packet-link:hover .packet{border-color:var(--sage-deep)}

.door{display:block;text-decoration:none;border:1.5px solid var(--forest);
  border-radius:6px;overflow:hidden;background:#fff}
.door img{width:100%;aspect-ratio:3/2;object-fit:cover}
.door-body{padding:1.25rem 1.4rem 1.5rem}
.door:hover{border-color:var(--sage-deep)}

/* ---------- facts ---------- */
.facts{list-style:none;margin:0 0 1.25rem;padding:0;border-top:1px solid var(--rule)}
.facts li{display:flex;justify-content:space-between;gap:1rem;padding:.6rem 0;
  border-bottom:1px solid var(--rule);font-size:.97rem}
.facts .k{color:var(--sage-deep)}
.facts .v{text-align:right;font-weight:700}
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
.frame img{width:100%;aspect-ratio:4/3;object-fit:cover}
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
.filter-row{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:1.5rem}
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
label{font-size:.9rem;font-weight:700}
input,select,textarea{font:inherit;padding:.7rem .8rem;
  border:1.5px solid var(--sage-deep);border-radius:3px;background:#fff;width:100%;
  color:var(--forest);min-height:48px}
textarea{min-height:8rem}

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
.foot-brand{background:var(--paper);border-radius:6px;padding:1.1rem 1.35rem;
  display:inline-block}
.foot-brand img{height:132px;width:auto}
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
  .brand img{height:68px}
}
@media (max-width:900px){
  .hero{padding:2rem 0 1.5rem}
  .hero-split,.grid-2,.puppy-top,.foot-grid,.foot-top{grid-template-columns:1fr}
  .foot-top{gap:1.5rem;padding-bottom:0}
  .foot-brand img{height:104px}
  .nav-toggle{display:block}
  .nav{position:fixed;inset:0;background:var(--paper);flex-direction:column;
    justify-content:center;gap:.3rem;display:none;z-index:50;overflow-y:auto}
  .nav.open{display:flex}
  .nav a{font-size:1.25rem;padding:.7rem 1.2rem}
  .nav a.nav-cta{margin-left:0}
  .nav-close{position:absolute;top:1rem;right:1.25rem}
  .cthumbs button{width:64px;height:64px}
  .facts li{min-height:44px}
  .chat-fab{right:12px;bottom:12px}
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
      slides.forEach(function(s,k){ s.hidden = k !== i; });
      thumbs.forEach(function(t,k){ t.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      if (counter) counter.textContent = (i+1) + ' / ' + slides.length;
    }
    car.querySelector('.cprev').addEventListener('click', function(){ show(i-1); });
    car.querySelector('.cnext').addEventListener('click', function(){ show(i+1); });
    thumbs.forEach(function(t,k){ t.addEventListener('click', function(){ show(k); }); });
    car.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft') show(i-1);
      if (e.key === 'ArrowRight') show(i+1);
    });
    show(0);
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

  // ---- gallery filter
  var filters = document.querySelectorAll('.filter-row button');
  if (filters.length){
    filters.forEach(function(b){
      b.addEventListener('click', function(){
        filters.forEach(function(x){ x.classList.remove('cur'); });
        b.classList.add('cur');
        var want = b.getAttribute('data-line');
        document.querySelectorAll('.gal-grid a').forEach(function(item){
          item.style.display = (want === 'all' || item.getAttribute('data-line') === want) ? '' : 'none';
        });
      });
    });
  }

  // ---- let's chat launcher, on every page
  var fab = document.createElement('button');
  fab.className = 'chat-fab';
  fab.setAttribute('aria-expanded','false');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>Let\\u2019s Chat';
  var panel = document.createElement('div');
  panel.className = 'chat-panel';
  panel.innerHTML = '<h3>Talk puppies with us</h3>'
    + '<p>Call or text is the fastest way to reach us. We are always happy to answer questions or set up a visit or video call.</p>'
    + '<div class="row"><span class="lbl">Call/Text</span><a href="__PHONE_HREF__">__PHONE__</a></div>'
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
})();
"""
JS = (JS.replace("__PHONE_HREF__", PHONE_HREF)
        .replace("__PHONE__", PHONE_DISPLAY)
        .replace("__EMAIL__", EMAIL))

SPRIG = ('<svg class="sprig" width="72" height="25" viewBox="0 0 40 14" aria-hidden="true">'
 '<g fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round">'
 '<path d="M2 7h36"/>'
 '<path d="M14 7c0-3 2.5-4.5 5-4.5C19 5.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".55"/>'
 '<path d="M14 7c0 3 2.5 4.5 5 4.5C19 8.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".35"/>'
 '<path d="M23 7c0-2.4 2-3.6 4-3.6C27 5.8 25 7 23 7z" fill="currentColor" stroke="none" opacity=".45"/>'
 '<circle cx="34" cy="7" r="1.6" fill="currentColor" stroke="none" opacity=".6"/></g></svg>')

NAV = """<nav class="nav" aria-label="Main">
  <a href="puppies.html">Puppies</a>
  <a href="munchkin-bernedoodles.html">Bernedoodles</a>
  <a href="dobermans.html">Dobermans</a>
  <a href="our-dogs.html">Our Dogs</a>
  <a href="gallery.html">Gallery</a>
  <a href="about.html">About</a>
  <a href="process.html">How It Works</a>
  <a href="contact.html">Contact</a>
  <a class="nav-cta" href="waitlist.html">Join the Waitlist</a>
</nav>"""

def header():
    return f"""<header class="site-head"><div class="wrap head-row">
  <a class="brand" href="index.html">
    <img src="img/brand/logo-horizontal-forest.png" alt="Bless Your Paws Puppies">
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-label="Open menu">Menu</button>
  {NAV}
</div></header>"""

def footer():
    return f"""<footer class="site-foot"><div class="wrap">
  <div class="foot-top">
    <div class="foot-brand"><img src="img/brand/logo-stacked-forest.png" alt="Bless Your Paws Puppies"></div>
    <div class="foot-grid">
      <div><h3>Our puppies</h3><ul>
        <li><a href="puppies.html">All available puppies</a></li>
        <li><a href="munchkin-bernedoodles.html">Munchkin Bernedoodles</a></li>
        <li><a href="dobermans.html">Doberman Pinschers</a></li>
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
        <li>Call or text Hope<br><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></li>
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

def page(path, title, desc, body, extra_head=""):
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
<link rel="canonical" href="{BASE}/{path if path != 'index.html' else ''}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/img/og-card.png">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.ico?v={V}" sizes="any">
<link rel="icon" href="img/favicon.png?v={V}" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png?v={V}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Petrona:ital,wght@0,400..700;1,400&family=Mulish:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={V}">
{extra_head}</head>
<body>
{header()}
<main>
{body}
</main>
{footer()}
<script src="main.js?v={V}"></script>
</body>
</html>
"""
    assert "—" not in html, f"em dash slipped into {path}"
    open(path, "w", encoding="utf-8").write(html)

def img_tag(stem, folder="puppies", cls="", alt="", lazy=True, hidden=False):
    q = chr(34)
    parts = ["<img"]
    if hidden: parts.append("hidden")
    if cls: parts.append(f"class={q}{cls}{q}")
    # only reference widths that were actually generated: a narrow original has no
    # 1600px derivative, and a srcset entry pointing at a missing file is a 404.
    have = [w for w in (320, 640, 1000, 1600)
            if os.path.exists(f"img/r/{stem}-{w}.webp")]
    if have:
        parts.append("srcset=" + q + ", ".join(
            f"img/r/{stem}-{w}.webp {w}w" for w in have) + q)
    parts.append(f'sizes={q}(max-width:900px) 94vw, 45vw{q}')
    parts.append(f'src={q}img/{folder}/{stem}.jpg{q}')
    parts.append(f'alt={q}{alt}{q}')
    if lazy: parts.append(f'loading={q}lazy{q}')
    return " ".join(parts) + ">"

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

def card(slug, name, sex, colour, price, breed):
    return f"""<a class="packet-link" href="puppy-{slug}.html"><article class="packet">
  {img_tag(slug+'-01', alt=f'{name}, a {colour.lower()} {breed} puppy')}
  <div class="packet-body">
    <p class="packet-name">{name}</p>
    <p class="packet-meta">{sex} &middot; {colour}</p>
    <div class="packet-row"><span class="price">${price:,}</span>
      <span class="status">Available</span></div>
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

M_PARENTS = None  # filled in build_pages
D_PARENTS = None

def build_pages():
    global M_PARENTS, D_PARENTS
    m_cards = "\n".join(card(s, n, x, c, M_PRICE, "Munchkin Bernedoodle") for s, n, x, c, _ in MUNCHKINS)
    d_cards = "\n".join(card(s, n, x, c, D_PRICE, "Doberman Pinscher") for s, n, x, c, _ in DOBERMANS)

    M_PARENTS = (
      parent_card("troy-01", "Troy", "Mom", "Mini Multi Gen Bernedoodle",
                  [("Weight", "21 lbs"), ("Color", "Blue merle parti"),
                   ("Born", "January 21, 2024")]) +
      parent_card("cavalier-sire-01", "Our Cavalier sire", "Dad",
                  "Cavalier King Charles Spaniel, AKC",
                  [("Weight", "19 lbs"), ("Color", "Ruby"),
                   ("Genetic testing", "Clear")],
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

    hp = """<div style="position:absolute;left:-9999px" aria-hidden="true">
      <label for="{i}-hp">Leave this field empty</label>
      <input id="{i}-hp" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    """

    org_ld = json.dumps({"@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "Bless Your Paws Puppies",
        "description": "Family-raised Munchkin Bernedoodle and Doberman Pinscher puppies in Warsaw and Winona Lake, Indiana.",
        "telephone": "+1-574-377-8023", "email": EMAIL, "areaServed": AREA,
        "url": BASE + "/", "image": BASE + "/img/og-card.png"})

    page("index.html", "Bless Your Paws Puppies | Munchkin Bernedoodle and Doberman Puppies, Northern Indiana",
      "Family-raised Munchkin Bernedoodle and Doberman Pinscher puppies from two sisters in northern Indiana. Raised in the home, around kids, with early socialization.",
      f"""<section class="hero"><div class="wrap hero-split">
  <div>
    <p class="eyebrow">Family-raised in northern Indiana</p>
    <h1>Puppies raised in the middle of real family life</h1>
    <p class="lede">We are two sisters raising Munchkin Bernedoodles and Doberman
      Pinschers underfoot in our homes, around our kids, the vacuum, the doorbell,
      and everything else a family sounds like. {CHIP_SAMPLE}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="puppies.html">See available puppies</a>
      <a class="btn btn-ghost" href="waitlist.html">Join the waitlist</a>
    </div>
  </div>
  {img_tag('havilah-01', cls='framed', alt='Havilah, a blue merle phantom Munchkin Bernedoodle puppy', lazy=False)}
</div></section>

<section class="band-raise"><div class="wrap">
  <p class="eyebrow">Available now</p>
  <h2>Puppies looking for their families</h2>
  <p class="lede">Munchkin Bernedoodles going home in September, and Doberman
    Pinschers ready right now. A ${DEPOSIT} deposit holds your puppy.</p>
  <div class="pgrid" style="margin-top:2rem">
{card(*MUNCHKINS[1][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*MUNCHKINS[2][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*MUNCHKINS[6][:4], M_PRICE, "Munchkin Bernedoodle")}
{card(*DOBERMANS[0][:4], D_PRICE, "Doberman Pinscher")}
  </div>
  <div class="section-cta">
    <p>Every available puppy, both litters, in one place.</p>
    <a class="btn btn-primary" href="puppies.html">See all available puppies</a>
  </div>
</div></section>

<section><div class="wrap">
  {SPRIG}
  <h2 class="center" style="margin-top:1rem">Two breeds, one standard of raising</h2>
  <div class="grid-2" style="margin-top:2rem;align-items:stretch">
    <a class="door" href="munchkin-bernedoodles.html">
      {img_tag('eden-01', alt='Eden, a red and white Munchkin Bernedoodle puppy')}
      <div class="door-body"><h3>Munchkin Bernedoodles</h3>
      <p class="fine">A small, sweet cross of a Mini Multi Gen Bernedoodle and an
        AKC Cavalier King Charles Spaniel. Going home in September.</p></div>
    </a>
    <a class="door" href="dobermans.html">
      {img_tag('griffin-01', alt='Griffin, a Doberman Pinscher puppy')}
      <div class="door-body"><h3>Doberman Pinschers</h3>
      <p class="fine">Loyal, people-loving Dobermans from our health-tested dam
        Mira. Ready to go home now.</p></div>
    </a>
  </div>
</div></section>

<section class="band-forest"><div class="wrap grid-2">
  <div>
    <p class="eyebrow">How they are raised</p>
    <h2>Socialized before they ever leave our arms</h2>
    <p>Every puppy is raised in the home, not a kennel. They grow up with children,
      other dogs, and the everyday noise of family life: the doorbell, the TV, pots
      and pans, the vacuum. Early neurological stimulation starts in the first weeks,
      and grass potty training starts before go-home.</p>
    <p>Each puppy leaves with a vet exam, current vaccinations, a health record, a bag
      of the food they know, and a toy that smells like home.
      <a href="process.html">See how reserving works</a>.</p>
  </div>
  {img_tag('caleb-02', cls='framed', alt='Caleb, a red and white parti Munchkin Bernedoodle puppy')}
</div></section>

<section><div class="wrap">
  <p class="eyebrow">The parents</p>
  <h2>Health and temperament start here</h2>
  <p class="lede" style="max-width:70ch">Meet the moms and dads, with each dog's
    testing listed on their own card. Where a record exists, we link the record.</p>
  <div class="parent-grid" style="margin-top:2rem">
{M_PARENTS}{D_PARENTS}
  </div>
  <div class="section-cta">
    <p>Every test result we hold, linked to the original record.</p>
    <a class="btn btn-primary" href="our-dogs.html">Meet our dogs</a>
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

    page("puppies.html", "Available Puppies | Bless Your Paws Puppies",
      f"All available Munchkin Bernedoodle and Doberman Pinscher puppies. A ${DEPOSIT} deposit reserves your puppy.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Available now</p>
  <h1>Our puppies</h1>
  <p class="lede" style="max-width:70ch">Ten puppies across two litters. Every price
    includes the vet exam, vaccinations, and the go-home kit. A ${DEPOSIT} deposit
    holds your puppy.</p>

  <h2 style="margin-top:2.5rem">Munchkin Bernedoodles &middot; ${M_PRICE:,}</h2>
  <p class="fine">Born {M_BORN}. Going home {M_HOME}. {SIZE_DRAFT}</p>
  <div class="pgrid cols-4" style="margin-top:1.5rem">{m_cards}</div>

  <h2 style="margin-top:4rem">Doberman Pinschers &middot; ${D_PRICE:,}</h2>
  <p class="fine">Born {D_BORN}. <strong>Ready to go home now.</strong>
    AKC registered, tails docked, dew claws removed, microchipped.</p>
  <div class="pgrid cols-3" style="margin-top:1.5rem">{d_cards}</div>
</div></section>""")

    page("munchkin-bernedoodles.html", "Munchkin Bernedoodle Puppies for Sale | Bless Your Paws Puppies",
      f"Munchkin Bernedoodle puppies from a Mini Multi Gen Bernedoodle dam and an AKC Cavalier sire. Born {M_BORN}, home in September. ${M_PRICE:,} with a ${DEPOSIT} deposit.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Hope's litter</p>
  <h1>Munchkin Bernedoodle puppies</h1>
  <div class="grid-2 narrow-left">
    <div>
      <p class="lede">Seven puppies from Troy, our Mini Multi Gen Bernedoodle, and
        our AKC-registered Cavalier King Charles Spaniel sire. Born {M_BORN},
        going home {M_HOME}.</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${M_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">{M_BORN}</span></li>
        <li><span class="k">Go home</span><span class="v">{M_HOME}</span></li>
        <li><span class="k">Expected adult size</span><span class="v">15 to 25 lbs</span></li>
      </ul>
      <p class="fine">{SIZE_DRAFT}</p>
      <p>New to the cross? <a href="what-is-a-munchkin-bernedoodle.html">Read our
        plain-language guide</a> to what a Munchkin Bernedoodle is and what to expect.</p>
    </div>
    {img_tag('jericho-01', cls='framed', alt='Jericho, a blue merle parti Munchkin Bernedoodle puppy', lazy=False)}
  </div>
  <div class="pgrid cols-4" style="margin-top:2.5rem">{m_cards}</div>
</div></section>

<section class="band-raise"><div class="wrap">
  <h2>Meet their parents</h2>
  <div class="parent-grid" style="margin-top:1.5rem">{M_PARENTS}</div>
  <div class="section-cta">
    <p>Every test result we hold, linked to the original record.</p>
    <a class="btn btn-primary" href="our-dogs.html">See full health details</a>
  </div>
</div></section>

<section class="band-pink"><div class="wrap center">
  <p class="lede">Hoping for a puppy from a future litter instead?</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="waitlist.html">Join the waitlist</a></div>
</div></section>""")

    page("dobermans.html", "Doberman Pinscher Puppies for Sale | Bless Your Paws Puppies",
      f"AKC Doberman Pinscher puppies, ready to go home now. From our health-tested dam Mira. ${D_PRICE:,} with a ${DEPOSIT} deposit.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Joy's litter</p>
  <h1>Doberman Pinscher puppies</h1>
  <div class="grid-2 narrow-left">
    <div>
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
    {img_tag('elowen-01', cls='framed', alt='Elowen, a black and rust Doberman Pinscher puppy', lazy=False)}
  </div>
  <div class="pgrid cols-3" style="margin-top:2.5rem">{d_cards}</div>
</div></section>

<section class="band-raise"><div class="wrap">
  <h2>Meet their parents</h2>
  <div class="parent-grid" style="margin-top:1.5rem">{D_PARENTS}</div>
  <div class="section-cta">
    <p>Every test result we hold, linked to the original record.</p>
    <a class="btn btn-primary" href="our-dogs.html">See full health details</a>
  </div>
</div></section>""")

    faq = [
      ("How big does a Munchkin Bernedoodle get?",
       "Most mature between 10 and 25 lbs. Our current litter is expected at 15 to 25 lbs full grown, based on the 21 lb mom and 19 lb dad. Size varies puppy to puppy, so ask us about the one you love."),
      ("Do Munchkin Bernedoodles shed?",
       "Coats vary by puppy. Many are wavy to curly and lower-shedding, but we will never promise a non-shedding or hypoallergenic coat. Ask us about the specific puppy and we will tell you honestly what we see."),
      ("Is a Munchkin Bernedoodle a dwarf breed?",
       "No. The small size comes from crossing in a naturally smaller parent breed, not from a short-legged gene. These are simply small, normally proportioned dogs."),
      ("What is the temperament like?",
       "The Cavalier side tends to bring a calm, affectionate, lap-loving nature, and the Bernedoodle side brings playfulness and clever, trainable energy. Every puppy is an individual, which is why we socialize them early and match carefully."),
      ("Are they good with children and other dogs?",
       "Ours are raised around both from day one. Our puppies grow up with our kids and our other dogs, so they arrive already used to busy family life."),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": q,
        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    faq_html = "\n".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)
    page("what-is-a-munchkin-bernedoodle.html", "What Is a Munchkin Bernedoodle? | Bless Your Paws Puppies",
      "A plain-language guide to the Munchkin Bernedoodle: the cross, the size, the coat, and the temperament, from a family that breeds them.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Breed guide</p>
  <h1>What is a Munchkin Bernedoodle?</h1>
  <div class="grid-2">
    <p class="lede">A Munchkin Bernedoodle is an intentionally small Bernedoodle cross.
      Ours come from a Mini Multi Gen Bernedoodle mom and an AKC Cavalier King Charles
      Spaniel dad, which brings the size down naturally and adds the Cavalier's
      famously gentle temperament.</p>
    {img_tag('shiloh-01', cls='framed', alt='Shiloh, a blue merle phantom Munchkin Bernedoodle puppy', lazy=False)}
  </div>
</div></section>

<section class="band-raise"><div class="wrap">
  <h2>Where the small size comes from</h2>
  <div class="grid-2" style="margin-top:1.5rem">
    <div>
      <p>The name confuses people, so here is the honest version. "Munchkin"
        describes small overall size, not short legs. There is no dwarf gene
        involved. A Munchkin Bernedoodle is a normally proportioned little dog that
        keeps the Bernedoodle look, usually somewhere between 10 and 25 lbs full
        grown, where a standard Bernedoodle can reach 70 lbs or more.</p>
      <p>Ours get there the natural way: a small mom at 21 lbs bred to a small dad at
        19 lbs. No trick, no trait, just two small parents.</p>
    </div>
    {img_tag('troy-01', folder='dogs', cls='framed', alt='Troy, our 21 lb Mini Multi Gen Bernedoodle dam')}
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

<section class="band-forest"><div class="wrap grid-2">
  <div>
    <h2>Honest words about the coat</h2>
    <p>Doodle coats vary by individual puppy, even within one litter. Many are wavy
      to curly and shed lightly. Some shed more. We will not promise you a
      non-shedding or hypoallergenic dog, because no honest breeder can.</p>
    <p>What we will do is tell you exactly what we see in the coat of the puppy you
      ask about, and let you feel it yourself when you visit.</p>
  </div>
  {img_tag('havilah-03', cls='framed', alt='Close view of a Munchkin Bernedoodle puppy coat')}
</div></section>

<section><div class="wrap prose">
  <h2>Common questions</h2>
  {faq_html}
  <div class="btn-row">
    <a class="btn btn-primary" href="munchkin-bernedoodles.html">See available puppies</a>
    <a class="btn btn-ghost" href="waitlist.html">Join the waitlist</a>
  </div>
</div></section>""",
      extra_head=f'<script type="application/ld+json">{faq_ld}</script>\n')

    page("our-dogs.html", "Our Dogs and Their Health | Bless Your Paws Puppies",
      "Meet the parents: Troy the Mini Multi Gen Bernedoodle, our AKC Cavalier sire, and Mira the health-tested Doberman dam, with testing listed dog by dog.",
      f"""<section style="padding-bottom:0"><div class="wrap">
  <p class="eyebrow">The parents</p>
  <h1>Our dogs, and what they are tested for</h1>
  <p class="lede" style="max-width:72ch">Health claims are easy to make and hard to
    check, so each dog's testing sits on their own card, and where a record exists we
    link the actual record for you to read yourself.</p>
</div></section>

<section class="band-raise"><div class="wrap">
  <h2>The Munchkin Bernedoodle parents</h2>
  <p class="fine">Troy and our Cavalier sire, the mom and dad behind Hope's litter.</p>
  <div class="parent-grid" style="margin-top:1.5rem">{M_PARENTS}</div>
  <div class="section-cta">
    <p>Troy's testing documentation is being compiled. {CHIP_DRAFT}</p>
    <a class="btn btn-primary" href="munchkin-bernedoodles.html">See their puppies</a>
  </div>
</div></section>

<section><div class="wrap">
  <h2>The Doberman parents</h2>
  <p class="fine">Mira and our Doberman sire, the mom and dad behind Joy's litter.</p>
  <div class="parent-grid" style="margin-top:1.5rem">{D_PARENTS}</div>
  <div class="section-cta">
    <p>Read Mira's records yourself:
      <a href="https://ofa.org/advanced-search?appnum=2720473">OFA record</a> and
      <a href="https://gensol2storageaccount.blob.core.windows.net/certificates/eb11a34d-fa1e-4a4b-ac2f-b5b5bcc6d48e/gensolresult534262.pdf">GenSol certificate</a>.</p>
    <a class="btn btn-primary" href="dobermans.html">See their puppies</a>
  </div>
</div></section>

<section class="band-pink"><div class="wrap">
  <h2>What a carrier result actually means</h2>
  <div class="grid-2 narrow-right" style="margin-top:1.5rem;align-items:center">
    <div>
      <p>Mira's genetic panel comes back clear on everything tested except one
        condition, where she is a carrier. A carrier has one copy of a variant and is
        not affected by it herself. Carriers are bred to clear partners so that no
        puppy can be affected, which is exactly how she is paired.</p>
      <p>An OFA heart exam is a cardiac screening performed by a veterinarian and
        registered with the Orthopedic Foundation for Animals. Mira has been screened
        by EKG and holter, and her eyes are tested too.
        <span class="chip chip-draft">Confirm DCM3 vs DM3</span></p>
    </div>
    {img_tag('mira-01', folder='dogs', cls='framed', alt='Mira, our health-tested Doberman dam')}
  </div>
</div></section>

<section class="band-forest" style="margin-bottom:0"><div class="wrap grid-2 narrow-left">
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
      <a class="btn btn-ghost" href="health-guarantee.html">Read the health guarantee</a>
    </div>
  </div>
  {img_tag('eden-02', cls='framed', alt='A Munchkin Bernedoodle puppy being held')}
</div></section>""")

    page("about.html", "About Hope and Joy | Bless Your Paws Puppies",
      "Two sisters raising Munchkin Bernedoodles and Doberman Pinschers in their northern Indiana homes.",
      f"""<section><div class="wrap">
  <p class="eyebrow">About us</p>
  <h1>Two sisters, one standard</h1>
  <div class="grid-2">
    <div>
      <p class="lede">We are Hope and Joy, twin sisters raising puppies in our
        northern Indiana homes. Hope raises the Munchkin Bernedoodles and Joy raises
        the Doberman Pinschers, and every litter is raised the same way: in the house,
        around our kids, in the middle of everything. {CHIP_SAMPLE}</p>
      <p>We grew up in a big family where there was always something cooking and
        someone at the door, and our puppies grow up the same way. By the time a puppy
        leaves us it has heard the vacuum, the doorbell, and a houseful of children,
        and it has been held every single day.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Say hello</a>
        <a class="btn btn-ghost" href="process.html">How reserving works</a>
      </div>
    </div>
    <div>
      <img class="framed" src="img/placeholder/hope-and-joy.svg" alt="Photo of Hope and Joy coming soon">
      <p class="fine center" style="margin-top:.75rem">A photo of Hope and Joy goes
        here. {CHIP_PHOTO}</p>
    </div>
  </div>
</div></section>

<section class="band-raise"><div class="wrap grid-2">
  {img_tag('joshua-02', cls='framed', alt='A Munchkin Bernedoodle puppy in the grass')}
  <div>
    <h2>Why we do it this way</h2>
    <p>A puppy's first eight weeks decide a lot about the dog they become. That is
      why ours are never raised apart from the household. They meet children, other
      dogs, the vacuum, and visitors before they ever meet you. {CHIP_SAMPLE}</p>
    <p>We would love for you to meet the puppies, and their parents, before you
      decide. Visits are by appointment, and video calls work well for families
      further away.</p>
  </div>
</div></section>

<section><div class="wrap center">
  {SPRIG}
  <h2 style="margin-top:1rem">Come meet them</h2>
  <p class="lede">Call or text Hope at <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a>,
    or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-primary" href="puppies.html">See the puppies</a></div>
</div></section>""")

    page("process.html", "How It Works | Bless Your Paws Puppies",
      f"From first hello to go-home day: inquire, meet the puppy, reserve with a ${DEPOSIT} deposit, and take your puppy home.",
      f"""<section><div class="wrap">
  <p class="eyebrow">How it works</p>
  <h1>From first hello to go-home day</h1>
  <div class="grid-2">
    <p class="lede">Four steps, no pressure, and a real conversation somewhere in the
      middle. We would rather talk you out of the wrong puppy than sell you one.</p>
    {img_tag('havilah-02', cls='framed', alt='Havilah, a Munchkin Bernedoodle puppy', lazy=False)}
  </div>
</div></section>

<section class="band-raise"><div class="wrap">
  <div class="grid-3">
    <article class="packet">{img_tag('jericho-02', alt='A Munchkin Bernedoodle puppy')}
      <div class="packet-body"><p class="packet-name">1. Say hello</p>
        <p class="fine">Browse the <a href="puppies.html">available puppies</a>, then
          call, text, or send the <a href="contact.html">inquiry form</a>. Tell us a
          little about your family and who caught your eye.</p></div></article>
    <article class="packet">{img_tag('malcolm-01', alt='A Doberman Pinscher puppy')}
      <div class="packet-body"><p class="packet-name">2. Meet the puppy</p>
        <p class="fine">We set up a visit or a video call so you can meet the puppy,
          the parents, and us. Ten minutes is usually enough to know.</p></div></article>
    <article class="packet">{img_tag('caleb-01', alt='A Munchkin Bernedoodle puppy')}
      <div class="packet-body"><p class="packet-name">3. Reserve</p>
        <p class="fine">A ${DEPOSIT} deposit holds your puppy while they finish growing
          up with us. The deposit applies to your balance and is transferable to
          another available puppy if plans change. {CHIP_DRAFT}</p></div></article>
    <article class="packet">{img_tag('shiloh-02', alt='A Munchkin Bernedoodle puppy')}
      <div class="packet-body"><p class="packet-name">4. Go-home day</p>
        <p class="fine">Puppies go home from 8 weeks, after their final vet check.
          Pickup is by appointment; delivery options are being finalized.
          {CHIP_DRAFT}</p></div></article>
  </div>
</div></section>

<section><div class="wrap">
  <h2 class="center">What comes home with your puppy</h2>
  <div class="grid-2" style="margin-top:2rem;align-items:start">
    <div>
      <h3>Munchkin Bernedoodles</h3>
      <ul class="checklist">{''.join(f'<li>{i}</li>' for i in M_KIT)}</ul>
    </div>
    <div>
      <h3>Doberman Pinschers</h3>
      <ul class="checklist">{''.join(f'<li>{i}</li>' for i in D_KIT)}</ul>
    </div>
  </div>
</div></section>

<section class="band-forest"><div class="wrap">
  <h2>Questions families ask us</h2>
  <div class="grid-2" style="margin-top:1.5rem;align-items:start">
    <div>
      <h3>How do payments work?</h3>
      <p>The ${DEPOSIT} deposit reserves your puppy online. The balance is due before
        or at pickup; most families pay the balance by check or bank transfer.
        {CHIP_DRAFT}</p>
      <h3>Can we visit first?</h3>
      <p>Yes, and we encourage it. Visits are by appointment, and our location is
        shared once your visit is scheduled.</p>
    </div>
    <div>
      <h3>Do the puppies come with a guarantee?</h3>
      <p>Yes. Read the <a href="health-guarantee.html">health guarantee</a> and the
        <a href="purchase-agreement.html">purchase agreement</a> so there are no
        surprises on either side.</p>
      <h3>Will my puppy shed?</h3>
      <p>It varies by puppy, even in one litter. Ask us about the puppy you love and
        we will tell you what we see. We never promise a non-shedding coat.</p>
    </div>
  </div>
</div></section>""")

    page("contact.html", "Contact | Bless Your Paws Puppies",
      "Ask about an available puppy or plan a visit. Call or text Hope, email us, or send the inquiry form.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Say hello</h1>
  <p class="lede" style="max-width:70ch">The fastest way to reach us is a call or a
    text. Tell us which puppy caught your eye and a little about your family, and we
    will get right back to you.</p>
  <div class="grid-2" style="margin-top:2rem;align-items:start">
    <div>
      <h2>How to reach us</h2>
      <ul class="facts">
        <li><span class="k">Hope, Munchkin Bernedoodles</span>
          <span class="v"><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></span></li>
        <li><span class="k">Joy, Dobermans</span>
          <span class="v">Number coming soon</span></li>
        <li><span class="k">Email</span>
          <span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        <li><span class="k">Where</span><span class="v">{AREA}</span></li>
        <li><span class="k">Visits</span><span class="v">By appointment</span></li>
      </ul>
      <p class="fine">Our exact location is shared once your visit is scheduled.
        Video calls work well for families further away.</p>
    </div>
    <div>
      <h2>Send an inquiry</h2>
      <form data-guard action="https://formspree.io/f/REPLACE_FORM_ID" method="POST" style="max-width:none">
      {hp.format(i="c")}<div><label for="name">Your name</label><input id="name" name="name" required></div>
      <div><label for="email">Email</label><input id="email" name="email" type="email" required></div>
      <div><label for="phone">Phone (optional)</label><input id="phone" name="phone"></div>
      <div><label for="message">Which puppy caught your eye, and a little about your family</label>
        <textarea id="message" name="message" required></textarea></div>
      <button class="btn btn-primary" type="submit">Send inquiry</button>
      <p class="guard-msg">The form is almost ready. For now, call or text Hope at
        <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a> and we will get right back to you.</p>
      </form>
    </div>
  </div>
</div></section>

<section class="band-raise" style="margin-bottom:0"><div class="wrap">
  <h2 class="center">Who you would be coming to meet</h2>
  <div class="grid-2" style="margin-top:2rem">
    <div>
      {img_tag('eden-01', cls='framed', alt='Eden, a red and white Munchkin Bernedoodle puppy')}
      <h3 style="margin-top:1rem">Munchkin Bernedoodles</h3>
      <p class="fine">Small, soft, and lap-sized. Going home in September.
        <a href="munchkin-bernedoodles.html">See the litter</a>.</p>
    </div>
    <div>
      {img_tag('malcolm-01', cls='framed', alt='Malcolm, a black and rust Doberman Pinscher puppy')}
      <h3 style="margin-top:1rem">Doberman Pinschers</h3>
      <p class="fine">AKC registered, loyal, and ready to go home now.
        <a href="dobermans.html">See the litter</a>.</p>
    </div>
  </div>
</div></section>""")

    page("waitlist.html", "Join the Waitlist | Bless Your Paws Puppies",
      "Hear about new litters before they are listed. Waitlist families get first pick.",
      f"""<section><div class="wrap grid-2" style="align-items:start">
  <div>
    <p class="eyebrow">The waitlist</p>
    <h1>Hear about litters first</h1>
    <p class="lede">Our litters tend to reserve quickly. One puppy from the current
      litter went home to a waitlist family before it was ever listed publicly.</p>
    <p>Joining costs nothing and commits you to nothing. When a new litter arrives,
      waitlist families hear first, in the order they joined, and get first chance to
      reserve.</p>
    {img_tag('jordan-02', cls='framed', alt='Jordan, a blue merle parti Munchkin Bernedoodle puppy')}
  </div>
  <div>
    <h2>Add your name</h2>
    <form data-guard action="https://formspree.io/f/REPLACE_WAITLIST_ID" method="POST">
    {hp.format(i="w")}<div><label for="wname">Your name</label><input id="wname" name="name" required></div>
    <div><label for="wemail">Email</label><input id="wemail" name="email" type="email" required></div>
    <div><label for="wphone">Phone (optional)</label><input id="wphone" name="phone"></div>
    <div><label for="wline">Which puppies are you hoping for?</label>
      <select id="wline" name="line">
        <option>Munchkin Bernedoodles</option>
        <option>Doberman Pinschers</option>
        <option>Either, tell me about both</option>
      </select></div>
    <div><label for="wwhen">When are you hoping to bring a puppy home?</label>
      <input id="wwhen" name="timing" placeholder="This year, next spring, whenever the right one comes"></div>
    <button class="btn btn-primary" type="submit">Join the waitlist</button>
    <p class="guard-msg">The form is almost ready. For now, text Hope at
      <a href="{SMS_HREF}">{PHONE_DISPLAY}</a> with the word WAITLIST and your name.</p>
    </form>
  </div>
</div></section>""")

    items = []
    for s, n, _, c, _ in MUNCHKINS:
        for i in range(1, COUNTS[s] + 1):
            items.append((f"{s}-{i:02d}", n, "munchkin", s))
    for s, n, _, c, _ in DOBERMANS:
        for i in range(1, COUNTS[s] + 1):
            items.append((f"{s}-{i:02d}", n, "doberman", s))
    gal = "\n".join(f'<a data-line="{line}" href="puppy-{slug}.html">'
                    f'{img_tag(stem, alt=name)}</a>' for stem, name, line, slug in items)
    page("gallery.html", "Photo Gallery | Bless Your Paws Puppies",
      "Every photo of our Munchkin Bernedoodle and Doberman Pinscher puppies.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Gallery</p>
  <h1>The photo album</h1>
  <p class="lede">Every photo of the puppies who are with us right now. Click any
    photo to meet that puppy.</p>
  <div class="filter-row" style="margin-top:1.5rem">
    <button class="cur" data-line="all">All photos</button>
    <button data-line="munchkin">Munchkin Bernedoodles</button>
    <button data-line="doberman">Dobermans</button>
  </div>
  <div class="gal-grid">{gal}</div>
</div></section>""")

    page("reviews.html", "Reviews | Bless Your Paws Puppies",
      "What families say about their Bless Your Paws puppies.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Reviews</p>
  <h1>From our families</h1>
  <p>{CHIP_SAMPLE}</p>
  <div class="grid-2" style="margin-top:2rem;align-items:start">
    <div>
      <blockquote class="lede" style="border-left:3px solid var(--sage);padding-left:1.25rem;margin:0 0 1.5rem">
        "Our puppy came home confident, snuggly, and already used to kids. You can
        tell she was raised in the middle of a family."
        <span class="fine">A waitlist family</span></blockquote>
      <p>We are collecting reviews from our puppy families now, with their permission,
        and will post them here as they come in. If you have one of our puppies, we
        would love to hear from you.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Share your story</a></div>
    </div>
    {img_tag('havilah-02', cls='framed', alt='Havilah, a blue merle phantom Munchkin Bernedoodle puppy')}
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
    <li><strong>Registration.</strong> Doberman puppies are sold with AKC
      registration. Breeding rights are available for an additional ${DEPOSIT}.</li>
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
        cnt = COUNTS[slug]
        slides = "\n".join(
            "        " + img_tag(f"{slug}-{i:02d}", alt=f"{name}, photo {i}",
                                 lazy=(i > 1), hidden=(i > 1))
            for i in range(1, cnt + 1))
        thumbs = "\n".join(
            f'        <button aria-current="{"true" if i==1 else "false"}" '
            f'aria-label="Photo {i}"><img src="img/r/{slug}-{i:02d}-320.webp" alt="" '
            f'loading="lazy"></button>' for i in range(1, cnt + 1))
        sibs = MUNCHKINS if breed.startswith("Munchkin") else DOBERMANS
        sib = " &middot; ".join(f'<a href="puppy-{s}.html">{n}</a>'
                               for s, n, *_ in sibs if s != slug)
        breed_page = 'munchkin-bernedoodles' if breed.startswith('Munchkin') else 'dobermans'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product",
            "name": f"{name}, {breed} puppy", "image": f"{BASE}/img/puppies/{slug}-01.jpg",
            "description": f"{name} is a {colour.lower()} {breed} puppy, available now.",
            "offers": {"@type": "Offer", "priceCurrency": "USD", "price": str(price),
                       "availability": "https://schema.org/InStock"}})
        page(f"puppy-{slug}.html", f"{name}, {breed} Puppy | Bless Your Paws Puppies",
          f"{name} is a {colour.lower()} {breed} puppy. ${price:,} with a ${DEPOSIT} deposit to reserve.",
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
      <div class="name-row"><h1>{name}</h1><span class="price">${price:,}</span></div>
      <p class="lede">{sex} &middot; {colour} &middot; {breed}</p>
      <ul class="facts">
        <li><span class="k">Status</span><span class="v">Available</span></li>
        <li><span class="k">Sex</span><span class="v">{sex}</span></li>
        <li><span class="k">Color</span><span class="v">{colour}</span></li>
        <li><span class="k">Born</span><span class="v">{born}</span></li>
        <li><span class="k">Go home</span><span class="v">{home}</span></li>
{extra_facts}
      </ul>
      {f'<p><strong>{note}</strong></p>' if note else ''}
      <div class="reserve">
        <h3>Reserve {name}</h3>
        <p class="fine">A ${DEPOSIT} deposit holds {him} until go-home day. Pay the
          deposit now, or the full amount if you prefer.</p>
        <div class="pay-row">
          <a class="btn btn-primary pay-link" href="https://buy.stripe.com/REPLACE_DEPOSIT">Deposit &middot; ${DEPOSIT}</a>
          <a class="btn btn-ghost pay-link" href="https://buy.stripe.com/REPLACE_FULL">Full payment</a>
          <a class="btn btn-ghost pay-link" href="https://buy.stripe.com/REPLACE_BALANCE">Balance</a>
        </div>
        <p class="guard-msg">Online payments are almost ready. To reserve {name}
          today, call or text Hope at <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a>.</p>
        <p class="fine">Prefer to talk first? <a href="contact.html">Start an
          inquiry</a>, or call or text <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a>.
          Visits and video calls are always welcome before you decide.</p>
      </div>
      <h3>About {name} {CHIP_SAMPLE}</h3>
      <p>{name} is a {colour.lower()} {sex.lower()} growing up in the house, handled
        every day, around kids and other dogs, with early neurological stimulation
        from the first weeks. Ask us anything about {him}; we are happy to send more
        photos or hop on a video call.</p>
      {share_row(name, f'puppy-{slug}.html', f'img/puppies/{slug}-01.jpg')}
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

    m_facts = '        <li><span class="k">Expected adult size</span><span class="v">15 to 25 lbs (draft)</span></li>'
    d_facts = ('        <li><span class="k">Registration</span><span class="v">AKC</span></li>\n'
               '        <li><span class="k">Breeding rights</span><span class="v">$500 extra</span></li>')
    for s, n, x, c, note in MUNCHKINS:
        puppy_page(s, n, x, c, note, M_PRICE, "Munchkin Bernedoodle", M_BORN, M_HOME,
                   M_KIT, M_PARENTS, m_facts)
    for s, n, x, c, note in DOBERMANS:
        puppy_page(s, n, x, c, note, D_PRICE, "Doberman Pinscher", D_BORN, D_HOME,
                   D_KIT, D_PARENTS, d_facts)

def build_assets():
    open("style.css", "w", encoding="utf-8").write(CSS)
    open("main.js", "w", encoding="utf-8").write(JS)
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
    pages = [p for p in sorted(os.listdir(".")) if p.endswith(".html") and p != "404.html"]
    urls = "\n".join(f"  <url><loc>{BASE}/{'' if p=='index.html' else p}</loc></url>" for p in pages)
    open("sitemap.xml", "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')

if __name__ == "__main__":
    build_assets()
    build_pages()
    build_meta()
    print(f"scaffold v{V}: {len([p for p in os.listdir('.') if p.endswith('.html')])} pages")
