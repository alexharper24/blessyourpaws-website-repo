#!/usr/bin/env python3
"""One-shot Phase 1 scaffold for blessyourpaws-website-repo.

Generates every page, style.css, main.js, placeholders, favicons, og-card,
robots.txt and sitemap.xml from the data below. Running it again OVERWRITES
all generated files, so after hand-editing pages either fold the edit back
into this script or stop running it.

Draft mode: every page ships noindex + closed robots.txt until launch.
"""
import json, os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

V = 1                                    # cache-bust version, bump with any css/js change
BASE = "https://alexharper24.github.io/blessyourpaws-website-repo"   # swap at domain purchase
PHONE_DISPLAY = "(574) 377-8023"
PHONE_HREF = "tel:5743778023"
SMS_HREF = "sms:5743778023"

# ---------------------------------------------------------------- data
MUNCHKINS = [
    # slug, name, sex, colour, photos, note
    ("joshua",  "Joshua",  "Boy",  "Red and white parti", 10, ""),
    ("eden",    "Eden",    "Girl", "Red with white",      11, ""),
    ("havilah", "Havilah", "Girl", "Blue merle phantom",  13, ""),
    ("jordan",  "Jordan",  "Boy",  "Blue merle parti",    10, "Biggest of the litter so far."),
    ("caleb",   "Caleb",   "Boy",  "Red and white parti",  9, ""),
    ("shiloh",  "Shiloh",  "Boy",  "Blue merle phantom",  11, ""),
    ("jericho", "Jericho", "Boy",  "Blue merle parti",    14, ""),
]
DOBERMANS = [
    ("elowen",  "Elowen",  "Girl", "Black and rust", 3, ""),
    ("malcolm", "Malcolm", "Boy",  "Black and rust", 4, ""),
    ("griffin", "Griffin", "Boy",  "Black and rust", 6, ""),
]
M_PRICE, D_PRICE, DEPOSIT = 2000, 2200, 500

CHIP_DRAFT  = '<span class="chip chip-draft">Draft, confirm before launch</span>'
CHIP_SAMPLE = '<span class="chip chip-sample">Sample copy, waiting on their words</span>'

# ---------------------------------------------------------------- css
CSS = """/* Bless Your Paws Puppies - v1
   Character: a pressed-flower garden album. Blush paper, forest ink, sage stems,
   seed-packet cards with arch-top photos. Deliberately NOT Kingdom Family
   Companions' cream/espresso ledger. */

:root{
  --forest:#223d2c; --forest-soft:#34523f;
  --sage:#7f8e79; --sage-deep:#6d7a68; --sage-light:#a8b89e;
  --rose:#feb5bc; --pink-pale:#fbc4db;
  --paper:#fdf9f9; --paper-raise:#faf2f1; --rule:#e4d7d6;
  --draft:#8a5512; --draft-bg:#f8ecd9;
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
img{max-width:100%;height:auto}
h1,h2,h3{font-family:"Fraunces",Georgia,serif;font-weight:600;line-height:1.15;
  margin:0 0 .5rem;text-wrap:balance;letter-spacing:-.01em}
h1{font-size:2.4rem} h2{font-size:1.7rem} h3{font-size:1.15rem}
p{margin:0 0 1rem}
a{color:var(--forest)}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem}
.eyebrow{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--sage-deep);margin:0 0 .5rem;font-weight:700}
.lede{font-size:1.12rem;color:var(--forest-soft)}
.fine{font-size:.85rem;color:var(--sage-deep)}
.center{text-align:center}

/* chips for draft and sample content */
.chip{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;
  padding:.2rem .55rem;border-radius:3px;vertical-align:.12em;margin-left:.4rem}
.chip-draft{background:var(--draft-bg);color:var(--draft);border:1px dashed var(--draft)}
.chip-sample{background:var(--pink-pale);color:var(--forest);border:1px dashed var(--sage)}

/* header */
.site-head{background:var(--paper);border-bottom:1px solid var(--rule)}
.head-row{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  padding:.8rem 0}
.brand{display:flex;align-items:center;gap:.6rem;text-decoration:none}
.brand-mark{width:34px;height:34px;object-fit:contain}
.brand-name{font-family:"Fraunces",Georgia,serif;font-size:1.15rem;font-weight:700}
.brand-name em{font-style:normal;color:var(--sage-deep);font-weight:400}
.nav{display:flex;align-items:center;gap:.25rem}
.nav a{text-decoration:none;padding:.5rem .65rem;border-radius:3px;font-size:.95rem}
.nav a:hover{background:var(--paper-raise)}
.nav a.nav-cta{background:var(--forest);color:var(--paper);margin-left:.35rem;
  padding:.5rem .9rem}
.nav a.nav-cta:hover{background:var(--forest-soft)}
.nav-toggle{display:none;background:none;border:1.5px solid var(--forest);
  border-radius:3px;padding:.4rem .6rem;font:inherit;color:var(--forest);cursor:pointer}

/* hero */
.hero{padding:3rem 0 2.5rem}
.hero-split{display:grid;grid-template-columns:1.1fr .9fr;gap:2.5rem;align-items:center}
.arch{border-radius:50% 50% 6px 6px / 34% 34% 6px 6px;width:100%;
  aspect-ratio:4/5;object-fit:cover;border:1.5px solid var(--forest);
  box-shadow:0 0 0 6px var(--paper),0 0 0 7.5px var(--sage-light)}
.btn{display:inline-block;text-decoration:none;border-radius:3px;font-weight:700;
  padding:.7rem 1.25rem;border:1.5px solid var(--forest);font-size:.98rem}
.btn-primary{background:var(--forest);color:var(--paper)}
.btn-primary:hover{background:var(--forest-soft)}
.btn-ghost{background:transparent;color:var(--forest)}
.btn-ghost:hover{background:var(--paper-raise)}
.btn-row{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.25rem}

/* sprig divider */
.sprig{display:block;margin:0 auto;color:var(--sage)}

/* sections */
section{padding:2.5rem 0}
.band-forest{background:var(--forest);color:var(--paper)}
.band-forest h2,.band-forest h3{color:var(--paper)}
.band-forest .eyebrow{color:var(--rose)}
.band-forest p{color:#e9ded9}
.band-forest a{color:var(--pink-pale)}
.band-pink{background:var(--pink-pale)}
.band-raise{background:var(--paper-raise)}

/* seed-packet cards */
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
.packet{position:relative;background:#fff;border:1.5px solid var(--forest);
  border-radius:4px;padding:10px;display:flex;flex-direction:column}
.packet::before{content:"";position:absolute;inset:5px;border:1px dashed var(--sage);
  border-radius:2px;pointer-events:none}
.packet img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:2px}
.packet-body{padding:.9rem .6rem .5rem;display:flex;flex-direction:column;gap:.15rem}
.packet-name{font-family:"Fraunces",Georgia,serif;font-size:1.2rem;font-weight:700;
  margin:0}
.packet-meta{font-size:.85rem;color:var(--sage-deep);margin:0}
.packet-row{display:flex;justify-content:space-between;align-items:baseline;
  gap:.5rem;margin-top:.35rem}
.price{font-family:"Fraunces",Georgia,serif;font-size:1.1rem;font-weight:700}
.status{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--forest);background:var(--sage-light);padding:.15rem .5rem;border-radius:3px}
a.packet-link{text-decoration:none}
a.packet-link:hover .packet{border-color:var(--sage-deep)}

/* breed doors */
.door{display:block;text-decoration:none;position:relative;border:1.5px solid var(--forest);
  border-radius:6px;overflow:hidden;background:#fff}
.door img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.door-body{padding:1.1rem 1.25rem 1.25rem}
.door:hover{border-color:var(--sage-deep)}

/* facts list on puppy pages */
.facts{list-style:none;margin:0 0 1.25rem;padding:0;border-top:1px solid var(--rule)}
.facts li{display:flex;justify-content:space-between;gap:1rem;padding:.5rem 0;
  border-bottom:1px solid var(--rule);font-size:.95rem}
.facts .k{color:var(--sage-deep)}
.facts .v{text-align:right;font-weight:700}

/* gallery thumbs */
.thumbs{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.6rem}
.thumbs button{padding:0;border:1.5px solid var(--rule);border-radius:3px;
  background:none;cursor:pointer;width:64px;height:64px;overflow:hidden}
.thumbs button.cur{border-color:var(--forest)}
.thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.gal-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.gal-grid img{aspect-ratio:1/1;object-fit:cover;border-radius:3px;
  border:1px solid var(--rule)}
.filter-row{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.25rem}
.filter-row button{font:inherit;font-size:.9rem;padding:.4rem .9rem;cursor:pointer;
  border:1.5px solid var(--forest);background:none;border-radius:3px;color:var(--forest)}
.filter-row button.cur{background:var(--forest);color:var(--paper)}

/* reserve block */
.reserve{background:var(--paper-raise);border:1px dashed var(--sage);border-radius:4px;
  padding:1.25rem;margin:1.5rem 0}
.pay-row{display:flex;gap:.6rem;flex-wrap:wrap;margin:.75rem 0 .5rem}
.guard-msg{display:none;background:var(--pink-pale);border-radius:3px;
  padding:.75rem 1rem;font-size:.9rem;margin-top:.5rem}
.guard-msg.show{display:block}

/* forms */
form{display:flex;flex-direction:column;gap:.9rem;max-width:34rem}
label{font-size:.88rem;font-weight:700}
input,select,textarea{font:inherit;padding:.6rem .7rem;border:1.5px solid var(--sage-deep);
  border-radius:3px;background:#fff;width:100%;color:var(--forest)}
textarea{min-height:7rem}

/* draft banner for legal pages */
.draft-banner{background:var(--draft-bg);border:1.5px dashed var(--draft);
  color:var(--draft);border-radius:4px;padding:1rem 1.25rem;font-weight:700;
  margin:0 0 1.5rem}

/* tables */
.tbl{width:100%;border-collapse:collapse;font-size:.93rem}
.tbl th,.tbl td{text-align:left;padding:.5rem .6rem .5rem 0;
  border-bottom:1px solid var(--rule)}
.tbl th{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--sage-deep)}

/* prose column */
.prose{max-width:46rem}
.prose ul{padding-left:1.2rem}
.prose li{margin-bottom:.4rem}

/* footer */
.site-foot{background:var(--forest);color:#e9ded9;margin-top:3rem}
.site-foot a{color:var(--pink-pale)}
.foot-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;padding:2.5rem 0}
.foot-grid h3{color:var(--paper);font-size:1rem}
.foot-grid ul{list-style:none;margin:0;padding:0}
.foot-grid li{margin-bottom:.45rem;font-size:.92rem}
.foot-legal{border-top:1px solid rgba(253,249,249,.25);padding:1.25rem 0;
  font-size:.83rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}

@media print{
  .site-head,.site-foot,.btn,.nav,.thumbs,.filter-row{display:none}
  body{background:#fff;color:#000}
}

/* mobile */
@media (max-width:760px){
  h1{font-size:1.85rem}
  .hero{padding:2rem 0 1.5rem}
  .hero-split,.pgrid,.grid-2,.foot-grid{grid-template-columns:1fr}
  .gal-grid{grid-template-columns:repeat(2,1fr)}
  .nav-toggle{display:block}
  .nav{position:fixed;inset:0;background:var(--paper);flex-direction:column;
    justify-content:center;gap:.5rem;display:none;z-index:50}
  .nav.open{display:flex}
  .nav a{font-size:1.3rem;padding:.7rem 1.2rem}
  .nav a.nav-cta{margin-left:0}
  .nav-close{position:absolute;top:1rem;right:1.25rem}
  .facts li,.btn{min-height:44px}
}
"""

# ---------------------------------------------------------------- js
JS = """// Bless Your Paws Puppies - v1
(function(){
  // mobile nav overlay. fixed at every width so it never becomes a flex item.
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

  // guard: payment links stay friendly until the real Stripe links exist
  document.querySelectorAll('a.pay-link').forEach(function(a){
    if (a.href.indexOf('REPLACE') !== -1){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var msg = a.closest('.reserve').querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // guard: forms stay friendly until the Formspree id exists
  document.querySelectorAll('form[data-guard]').forEach(function(f){
    if (f.action.indexOf('REPLACE') !== -1){
      f.addEventListener('submit', function(e){
        e.preventDefault();
        var msg = f.querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // puppy page: thumb click swaps the main photo
  var main = document.getElementById('gallery-main');
  if (main){
    document.querySelectorAll('.thumbs button').forEach(function(b){
      b.addEventListener('click', function(){
        main.src = b.getAttribute('data-src');
        main.removeAttribute('srcset');
        document.querySelectorAll('.thumbs button').forEach(function(x){ x.classList.remove('cur'); });
        b.classList.add('cur');
      });
    });
  }

  // gallery page filter
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
})();
"""

# ---------------------------------------------------------------- html chrome
SPRIG = ('<svg class="sprig" width="64" height="22" viewBox="0 0 40 14" aria-hidden="true">'
 '<g fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round">'
 '<path d="M2 7h36"/>'
 '<path d="M14 7c0-3 2.5-4.5 5-4.5C19 5.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".55"/>'
 '<path d="M14 7c0 3 2.5 4.5 5 4.5C19 8.5 16.5 7 14 7z" fill="currentColor" stroke="none" opacity=".35"/>'
 '<path d="M23 7c0-2.4 2-3.6 4-3.6C27 5.8 25 7 23 7z" fill="currentColor" stroke="none" opacity=".45"/>'
 '<circle cx="34" cy="7" r="1.6" fill="currentColor" stroke="none" opacity=".6"/></g></svg>')

NAV = """<nav class="nav" aria-label="Main">
  <a href="puppies.html">Puppies</a>
  <a href="our-dogs.html">Our Dogs</a>
  <a href="health-testing.html">Health</a>
  <a href="about.html">About</a>
  <a href="process.html">How It Works</a>
  <a href="contact.html">Contact</a>
  <a class="nav-cta" href="waitlist.html">Join the Waitlist</a>
</nav>"""

def header():
    return f"""<header class="site-head"><div class="wrap head-row">
  <a class="brand" href="index.html">
    <img class="brand-mark" src="img/brand/mark-paw-heart.png" alt="">
    <span class="brand-name">Bless Your Paws <em>Puppies</em></span>
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-label="Open menu">Menu</button>
  {NAV}
</div></header>"""

def footer():
    return f"""<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div><h3>Explore</h3><ul>
      <li><a href="puppies.html">Available Puppies</a></li>
      <li><a href="munchkin-bernedoodles.html">Munchkin Bernedoodles</a></li>
      <li><a href="dobermans.html">Doberman Pinschers</a></li>
      <li><a href="what-is-a-munchkin-bernedoodle.html">What is a Munchkin Bernedoodle?</a></li>
      <li><a href="gallery.html">Photo Gallery</a></li>
      <li><a href="reviews.html">Reviews</a></li>
    </ul></div>
    <div><h3>Plan your visit</h3><ul>
      <li><a href="process.html">How It Works</a></li>
      <li><a href="health-testing.html">Health &amp; Testing</a></li>
      <li><a href="our-dogs.html">Our Dogs</a></li>
      <li><a href="about.html">About Us</a></li>
      <li><a href="waitlist.html">Join the Waitlist</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul></div>
    <div><h3>Get in touch</h3><ul>
      <li>Call or text Hope: <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></li>
      <li>Email: coming soon</li>
      <li>Northern Indiana <span class="chip chip-draft">Confirm area</span></li>
      <li>Visits by appointment. Our location is shared once your visit is scheduled.</li>
    </ul></div>
  </div>
  <div class="foot-legal">
    <span>&copy; 2026 Bless Your Paws Puppies. Site by <a href="https://harperstudio.co/">Harper Studio</a>.</span>
    <span><a href="privacy-policy.html">Privacy</a> &middot;
      <a href="health-guarantee.html">Health Guarantee</a> &middot;
      <a href="purchase-agreement.html">Purchase Agreement</a></span>
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..700&family=Mulish:wght@400;700&display=swap" rel="stylesheet">
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

def srcset(stem, folder="puppies"):
    return (f'srcset="img/r/{stem}-240.webp 240w, img/r/{stem}-600.webp 600w, '
            f'img/r/{stem}-1100.webp 1100w" sizes="(max-width:760px) 92vw, 340px" '
            f'src="img/{folder}/{stem}.jpg"')

def puppy_card(slug, name, sex, colour, price, breed_label):
    return f"""<a class="packet-link" href="puppy-{slug}.html"><article class="packet">
  <img {srcset(slug + '-01')} alt="{name}, a {colour.lower()} {breed_label} puppy" loading="lazy">
  <div class="packet-body">
    <p class="packet-name">{name}</p>
    <p class="packet-meta">{sex} &middot; {colour}</p>
    <div class="packet-row"><span class="price">${price:,}</span>
      <span class="status">Available</span></div>
  </div>
</article></a>"""

SIZE_DRAFT = ('Expected adult size: 15 to 25 lbs '
              '<span class="chip chip-draft">Draft estimate from the 19 lb and 21 lb parents</span>')

# ---------------------------------------------------------------- pages
def build_pages():
    m_cards = "\n".join(puppy_card(s, n, x, c, M_PRICE, "Munchkin Bernedoodle") for s, n, x, c, _, _ in MUNCHKINS)
    d_cards = "\n".join(puppy_card(s, n, x, c, D_PRICE, "Doberman Pinscher") for s, n, x, c, _, _ in DOBERMANS)

    org_ld = json.dumps({
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "Bless Your Paws Puppies",
        "description": "Family-raised Munchkin Bernedoodle and Doberman Pinscher puppies in northern Indiana.",
        "telephone": "+1-574-377-8023", "areaServed": "Northern Indiana",
        "url": BASE + "/", "image": BASE + "/img/og-card.png"}, indent=1)

    # ---- home
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
  <img class="arch" {srcset('havilah-01')} alt="Havilah, a blue merle phantom Munchkin Bernedoodle puppy">
</div></section>

<section class="band-raise"><div class="wrap">
  <p class="eyebrow">Ready to reserve now</p>
  <h2>This litter goes home September 16 to 23</h2>
  <p class="lede">Seven Munchkin Bernedoodles born July 22, and three Doberman
    Pinscher puppies. A $500 deposit holds your puppy until go-home day.</p>
  <div class="pgrid" style="margin-top:1.5rem">
{puppy_card(*[x for x in MUNCHKINS[1][:4]], M_PRICE, "Munchkin Bernedoodle")}
{puppy_card(*[x for x in MUNCHKINS[2][:4]], M_PRICE, "Munchkin Bernedoodle")}
{puppy_card(*[x for x in DOBERMANS[0][:4]], D_PRICE, "Doberman Pinscher")}
  </div>
  <div class="btn-row"><a class="btn btn-ghost" href="puppies.html">See all ten puppies</a></div>
</div></section>

<section><div class="wrap">
  {SPRIG}
  <h2 class="center">Two breeds, one standard of raising</h2>
  <div class="grid-2" style="margin-top:1.5rem">
    <a class="door" href="munchkin-bernedoodles.html">
      <img {srcset('eden-01')} alt="Eden, a red and white Munchkin Bernedoodle puppy" loading="lazy">
      <div class="door-body"><h3>Munchkin Bernedoodles</h3>
      <p class="fine">A small, sweet cross of a Mini Multi Gen Bernedoodle and an
        AKC Cavalier King Charles Spaniel. Seven available now.</p></div>
    </a>
    <a class="door" href="dobermans.html">
      <img {srcset('griffin-01')} alt="Griffin, a Doberman Pinscher puppy" loading="lazy">
      <div class="door-body"><h3>Doberman Pinschers</h3>
      <p class="fine">Loyal, people-loving Dobermans from our health-tested dam,
        Mira. Three available now.</p></div>
    </a>
  </div>
</div></section>

<section class="band-forest"><div class="wrap">
  <p class="eyebrow">How they are raised</p>
  <h2>Socialized before they ever leave our arms</h2>
  <div class="grid-2">
    <p>Every puppy is raised in the home, not a kennel. They grow up with children,
      other dogs, and the everyday noise of family life: the doorbell, the TV, pots
      and pans, the vacuum. Early neurological stimulation starts in the first weeks,
      and grass potty training starts before go-home.</p>
    <p>Each puppy leaves with a vet exam, current vaccinations and deworming, a
      health record, a bag of the food they know, a collar and leash, and a toy that
      smells like home. <a href="process.html">See how reserving works</a>.</p>
  </div>
</div></section>

<section><div class="wrap grid-2">
  <div>
    <p class="eyebrow">The parents</p>
    <h2>Meet the moms and dads</h2>
    <p>Temperament starts with the parents, so ours live the same family life the
      puppies are born into. Meet Troy, Mira, and the rest on the parents page,
      with health testing listed dog by dog.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="our-dogs.html">Meet our dogs</a></div>
  </div>
  <div>
    <p class="eyebrow">New to the breed?</p>
    <h2>What is a Munchkin Bernedoodle?</h2>
    <p>A deliberately small Bernedoodle cross, usually 10 to 25 lbs full grown.
      We wrote a plain-language guide to the cross, the coat, and what to expect.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="what-is-a-munchkin-bernedoodle.html">Read the guide</a></div>
  </div>
</div></section>

<section class="band-pink"><div class="wrap center">
  <h2>Litters reserve quickly</h2>
  <p class="lede">One puppy from this litter went home to a waitlist family before it
    was ever listed. Join the waitlist and you hear about the next litter first.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-primary" href="waitlist.html">Join the waitlist</a></div>
</div></section>""",
      extra_head=f'<script type="application/ld+json">{org_ld}</script>\n')

    # ---- puppies index
    page("puppies.html", "Available Puppies | Bless Your Paws Puppies",
      "All available Munchkin Bernedoodle and Doberman Pinscher puppies. A $500 deposit reserves your puppy.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Available now</p>
  <h1>Our puppies</h1>
  <p class="lede">Ten puppies across two litters. Every price includes the vet exam,
    vaccinations, deworming, and the go-home kit. A $500 deposit holds your puppy.</p>

  <h2 style="margin-top:2rem">Munchkin Bernedoodles &middot; ${M_PRICE:,}</h2>
  <p class="fine">Born July 22, 2026. Go home September 16 to 23. {SIZE_DRAFT}</p>
  <div class="pgrid" style="margin-top:1rem">{m_cards}</div>

  <h2 style="margin-top:3rem">Doberman Pinschers &middot; ${D_PRICE:,}</h2>
  <p class="fine">Ready now. Date of birth to be posted. {CHIP_DRAFT}</p>
  <div class="pgrid" style="margin-top:1rem">{d_cards}</div>
</div></section>""")

    # ---- breed pages
    page("munchkin-bernedoodles.html", "Munchkin Bernedoodle Puppies for Sale | Bless Your Paws Puppies",
      "Munchkin Bernedoodle puppies from a Mini Multi Gen Bernedoodle dam and an AKC Cavalier sire. Born July 22, ready mid September. $2,000 with a $500 deposit.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Hope's litter</p>
  <h1>Munchkin Bernedoodle puppies</h1>
  <div class="grid-2">
    <div>
      <p class="lede">Seven puppies from Troy, our Mini Multi Gen Bernedoodle, and
        our AKC-registered Cavalier King Charles Spaniel sire. Born July 22, 2026.
        Going home September 16 to 23.</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${M_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">July 22, 2026</span></li>
        <li><span class="k">Go home</span><span class="v">September 16 to 23, 2026</span></li>
        <li><span class="k">Expected adult size</span><span class="v">15 to 25 lbs</span></li>
      </ul>
      <p class="fine">{SIZE_DRAFT}</p>
      <p>New to the cross? <a href="what-is-a-munchkin-bernedoodle.html">Read our
        plain-language guide</a> to what a Munchkin Bernedoodle is and what to expect.</p>
    </div>
    <img class="arch" {srcset('jericho-01')} alt="Jericho, a blue merle parti Munchkin Bernedoodle puppy">
  </div>
  <div class="pgrid" style="margin-top:2rem">{m_cards}</div>
</div></section>
<section class="band-pink"><div class="wrap center">
  <p class="lede">Want a puppy from a future litter instead?</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="waitlist.html">Join the waitlist</a></div>
</div></section>""")

    page("dobermans.html", "Doberman Pinscher Puppies for Sale | Bless Your Paws Puppies",
      "Doberman Pinscher puppies from our health-tested dam Mira. GenSol tested and OFA cardiac normal, with records linked. $2,200 with a $500 deposit.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Joy's litter</p>
  <h1>Doberman Pinscher puppies</h1>
  <div class="grid-2">
    <div>
      <p class="lede">Three puppies from Mira, our health-tested Doberman dam.
        Dobermans are loyal, smart, people-focused dogs, and ours grow up in the
        middle of family life.</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${D_PRICE:,}</span></li>
        <li><span class="k">Deposit to reserve</span><span class="v">${DEPOSIT}</span></li>
        <li><span class="k">Born</span><span class="v">To be posted</span></li>
        <li><span class="k">Dam</span><span class="v">Mira (Kingdom's Miraculous Grace)</span></li>
      </ul>
      <p class="fine">Date of birth and go-home date to be posted. {CHIP_DRAFT}</p>
      <p>Mira's genetic and heart testing is real and linked:
        <a href="health-testing.html">see the records</a>.</p>
    </div>
    <img class="arch" src="img/dogs/mira-01.jpg" alt="Mira, our Doberman Pinscher dam, standing in the yard">
  </div>
  <div class="pgrid" style="margin-top:2rem">{d_cards}</div>
</div></section>""")

    # ---- explainer
    faq = [
      ("How big does a Munchkin Bernedoodle get?",
       "Most mature between 10 and 25 lbs. Our current litter is expected at 15 to 25 lbs full grown, based on the 21 lb mom and 19 lb dad. Size varies puppy to puppy, so ask us about the one you love."),
      ("Do Munchkin Bernedoodles shed?",
       "Coats vary by puppy. Many are wavy to curly and lower-shedding, but we will never promise a non-shedding or hypoallergenic coat. Ask us about the specific puppy and we will tell you honestly what we see."),
      ("Is a Munchkin Bernedoodle a dwarf breed?",
       "No. The small size comes from crossing in a naturally smaller parent breed, not from a short-legged gene. These are simply small, normally proportioned dogs."),
      ("What is the temperament like?",
       "The Cavalier side tends to bring a calm, affectionate, lap-loving nature, and the Bernedoodle side brings playfulness and clever, trainable energy. Every puppy is an individual, which is why we socialize them early and match carefully."),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": q,
        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    faq_html = "\n".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)
    page("what-is-a-munchkin-bernedoodle.html", "What Is a Munchkin Bernedoodle? | Bless Your Paws Puppies",
      "A plain-language guide to the Munchkin Bernedoodle: the cross, the size, the coat, and the temperament, from a family that breeds them.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">Breed guide</p>
  <h1>What is a Munchkin Bernedoodle?</h1>
  <p class="lede">A Munchkin Bernedoodle is an intentionally small Bernedoodle cross.
    Ours come from a Mini Multi Gen Bernedoodle mom and an AKC Cavalier King Charles
    Spaniel dad, which brings the size down naturally and adds the Cavalier's famously
    gentle temperament.</p>
  <p>The name can be confusing, so here is the honest version. "Munchkin" describes
    small overall size, not short legs. There is no dwarf gene involved. A Munchkin
    Bernedoodle is a normally proportioned little dog that keeps the Bernedoodle look,
    usually somewhere between 10 and 25 lbs full grown, where a standard Bernedoodle
    can reach 70 lbs or more.</p>
  <h2>The three breeds behind the cross</h2>
  <p>Behind our litter sit three breeds: the Bernese Mountain Dog and Poodle that make
    the Bernedoodle side, and the Cavalier King Charles Spaniel. From the Bernese come
    the tricolor and merle-influenced coats and the easygoing sweetness. From the
    Poodle come brains and the wavy, often lower-shedding coat. From the Cavalier come
    the small frame and a calm, cuddly, devoted nature.</p>
  <h2>Honest words about the coat</h2>
  <p>Doodle coats vary by individual puppy, even within one litter. Many are wavy to
    curly and shed lightly. Some shed more. We will not promise you a non-shedding or
    hypoallergenic dog, because no honest breeder can. What we will do is tell you
    exactly what we see in the coat of the puppy you ask about.</p>
  <h2>Common questions</h2>
  {faq_html}
  <div class="btn-row">
    <a class="btn btn-primary" href="munchkin-bernedoodles.html">See available puppies</a>
    <a class="btn btn-ghost" href="waitlist.html">Join the waitlist</a>
  </div>
</div></section>""",
      extra_head=f'<script type="application/ld+json">{faq_ld}</script>\n')

    # ---- our dogs
    page("our-dogs.html", "Our Dogs | Bless Your Paws Puppies",
      "Meet the parents: Troy the Mini Multi Gen Bernedoodle, our AKC Cavalier sire, and Mira the health-tested Doberman dam.",
      f"""<section><div class="wrap">
  <p class="eyebrow">The parents</p>
  <h1>Our dogs</h1>
  <p class="lede">Temperament and health start here. These are the moms and dads
    behind every litter, living the same family life the puppies are born into.</p>

  <h2 style="margin-top:2rem">The Munchkin Bernedoodle parents</h2>
  <div class="grid-2" style="margin-top:1rem">
    <article class="packet">
      <img src="img/placeholder/troy.svg" alt="Photo of Troy coming soon">
      <div class="packet-body">
        <p class="packet-name">Troy <span class="chip chip-draft">Photo coming from Hope</span></p>
        <p class="packet-meta">Dam &middot; Mini Multi Gen Bernedoodle</p>
        <ul class="facts" style="margin-top:.75rem">
          <li><span class="k">Weight</span><span class="v">21 lbs</span></li>
          <li><span class="k">Color</span><span class="v">Blue merle parti</span></li>
          <li><span class="k">Born</span><span class="v">January 21, 2024</span></li>
        </ul>
        <p class="fine">Health testing information is being compiled. {CHIP_DRAFT}</p>
      </div>
    </article>
    <article class="packet">
      <img src="img/placeholder/cavalier-sire.svg" alt="Photo of our Cavalier sire coming soon">
      <div class="packet-body">
        <p class="packet-name">Our Cavalier sire <span class="chip chip-draft">Name and photo coming</span></p>
        <p class="packet-meta">Sire &middot; Cavalier King Charles Spaniel, AKC registered</p>
        <ul class="facts" style="margin-top:.75rem">
          <li><span class="k">Weight</span><span class="v">19 lbs</span></li>
          <li><span class="k">Color</span><span class="v">Ruby</span></li>
          <li><span class="k">Born</span><span class="v">December 24, 2024</span></li>
        </ul>
        <p class="fine">Genetic testing documentation is being added. {CHIP_DRAFT}</p>
      </div>
    </article>
  </div>

  <h2 style="margin-top:3rem">The Doberman parents</h2>
  <div class="grid-2" style="margin-top:1rem">
    <article class="packet">
      <img src="img/dogs/mira-01.jpg" alt="Mira, our Doberman Pinscher dam">
      <div class="packet-body">
        <p class="packet-name">Mira</p>
        <p class="packet-meta">Dam &middot; Doberman Pinscher &middot; Kingdom's Miraculous Grace</p>
        <ul class="facts" style="margin-top:.75rem">
          <li><span class="k">AKC number</span><span class="v">WS85545303</span></li>
          <li><span class="k">Born</span><span class="v">October 21, 2024</span></li>
          <li><span class="k">Genetic panel</span><span class="v">GenSol: clear, DCM3 carrier</span></li>
          <li><span class="k">Heart</span><span class="v">OFA Advanced Cardiac: normal</span></li>
        </ul>
        <p class="fine">See her records on the <a href="health-testing.html">health page</a>.</p>
      </div>
    </article>
    <article class="packet">
      <img src="img/placeholder/doberman-sire.svg" alt="Photo of the Doberman sire coming soon">
      <div class="packet-body">
        <p class="packet-name">The sire <span class="chip chip-draft">Details coming from Joy</span></p>
        <p class="packet-meta">Sire &middot; Doberman Pinscher</p>
        <p class="fine" style="margin-top:.75rem">Name, registration, and health
          testing to be added.</p>
      </div>
    </article>
  </div>
</div></section>""")

    # ---- health
    page("health-testing.html", "Health and Testing | Bless Your Paws Puppies",
      "What our parent dogs are tested for, with links to the actual records. Every puppy is vet examined, vaccinated, and dewormed before go-home.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">Health &amp; testing</p>
  <h1>Health, in the open</h1>
  <p class="lede">Health claims are easy to make and hard to check. So where a record
    exists, we link the actual record and let you read it yourself.</p>

  <h2>Mira, Doberman dam</h2>
  <ul>
    <li>GenSol genetic panel: clear on all tested conditions, carrier for DCM3.
      Carrier status does not affect Mira's own health.
      <a href="https://gensol2storageaccount.blob.core.windows.net/certificates/eb11a34d-fa1e-4a4b-ac2f-b5b5bcc6d48e/gensolresult534262.pdf">Read the certificate</a>.</li>
    <li>OFA Advanced Cardiac: normal.
      <a href="https://ofa.org/advanced-search?appnum=2720473">See her OFA record</a>.</li>
  </ul>

  <h2>The Munchkin Bernedoodle parents</h2>
  <p>Our Cavalier sire is AKC registered and genetically tested; the panel
    documentation is being added to this page. Troy's health information is being
    compiled. {CHIP_DRAFT}</p>

  <h2>Every puppy, before go-home</h2>
  <ul>
    <li>Examination by a licensed veterinarian</li>
    <li>Age-appropriate vaccinations and deworming, with records in the go-home folder</li>
    <li>Early neurological stimulation from the first weeks</li>
    <li>A written health guarantee: <a href="health-guarantee.html">read the draft</a></li>
  </ul>

  <h2>What the tests mean</h2>
  <p>A genetic panel screens a parent for known inherited conditions in their breeds.
    "Clear" means the dog does not carry the tested mutation. "Carrier" means the dog
    carries one copy but is not affected; carriers are bred responsibly to clear
    partners so puppies cannot be affected. An OFA cardiac exam is a heart screening
    performed by a veterinarian and registered with the Orthopedic Foundation for
    Animals.</p>
</div></section>""")

    # ---- about
    page("about.html", "About Us | Bless Your Paws Puppies",
      "Two sisters raising Munchkin Bernedoodles and Doberman Pinschers in their northern Indiana homes.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">About us</p>
  <h1>Two sisters, one standard</h1>
  <p>{CHIP_SAMPLE}</p>
  <p class="lede">We are Hope and Joy, twin sisters raising puppies in our northern
    Indiana homes. Hope raises the Munchkin Bernedoodles and Joy raises the Doberman
    Pinschers, and every litter is raised the same way: in the house, around our
    kids, in the middle of everything.</p>
  <p>We grew up in a big family where there was always something cooking and someone
    at the door, and our puppies grow up the same way. By the time a puppy leaves us
    it has heard the vacuum, the doorbell, and a houseful of children, and it has
    been held every single day.</p>
  <p>We would love for you to meet the puppies, and their parents, before you decide.
    Visits are by appointment, and video calls work great for families further away.</p>
  <div class="btn-row">
    <a class="btn btn-primary" href="contact.html">Say hello</a>
    <a class="btn btn-ghost" href="process.html">How reserving works</a>
  </div>
</div></section>""")

    # ---- process
    page("process.html", "How It Works | Bless Your Paws Puppies",
      "From first hello to go-home day: inquire, meet the puppy on a visit or video call, reserve with a $500 deposit, and take your puppy home at 8 weeks.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">How it works</p>
  <h1>From first hello to go-home day</h1>
  <h3>1. Say hello</h3>
  <p>Browse the <a href="puppies.html">available puppies</a>, then call, text, or
    send the <a href="contact.html">inquiry form</a>. Tell us a little about your
    family and who caught your eye.</p>
  <h3>2. Meet the puppy</h3>
  <p>We will set up a visit or a video call so you can meet the puppy, the parents,
    and us. Ten minutes is usually enough to know.</p>
  <h3>3. Reserve with a deposit</h3>
  <p>A ${DEPOSIT} deposit holds your puppy while they finish growing up with us.
    Deposit terms: the deposit is applied to your balance and is transferable to
    another available puppy if plans change. {CHIP_DRAFT}</p>
  <h3>4. Watch them grow</h3>
  <p>We send updates and photos until go-home day. Ask for as many as you like.</p>
  <h3>5. Go-home day</h3>
  <p>Puppies go home from 8 weeks, after their final vet check. Every puppy leaves
    with a vaccination and health record, the vet exam paperwork, a bag of the food
    they are eating, a collar and leash, and a toy. Pickup is by appointment;
    delivery options are being finalized. {CHIP_DRAFT}</p>
  {SPRIG}
  <h2>Questions families ask us</h2>
  <h3>How do payments work?</h3>
  <p>The ${DEPOSIT} deposit reserves your puppy online. The balance is due before or
    at pickup; most families pay the balance by check or bank transfer. {CHIP_DRAFT}</p>
  <h3>Can we visit first?</h3>
  <p>Yes, and we encourage it. Visits are by appointment, and our location is shared
    once your visit is scheduled.</p>
  <h3>Do the puppies come with a guarantee?</h3>
  <p>Yes. <a href="health-guarantee.html">Read the health guarantee</a>, and the
    <a href="purchase-agreement.html">purchase agreement</a>, so there are no
    surprises on either side.</p>
  <h3>Will my puppy shed?</h3>
  <p>Honest answer: it varies by puppy, even in one litter. Ask us about the puppy
    you love and we will tell you what we see. We never promise a non-shedding or
    hypoallergenic coat.</p>
</div></section>""")

    # ---- contact
    form_guard = """<form data-guard action="https://formspree.io/f/REPLACE_FORM_ID" method="POST">
<div style="position:absolute;left:-9999px" aria-hidden="true">
      <label for="c-hp">Leave this field empty</label>
      <input id="c-hp" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    <div><label for="name">Your name</label><input id="name" name="name" required></div>
    <div><label for="email">Email</label><input id="email" name="email" type="email" required></div>
    <div><label for="phone">Phone (optional)</label><input id="phone" name="phone"></div>
    <div><label for="message">Which puppy caught your eye, and a little about your family</label>
      <textarea id="message" name="message" required></textarea></div>
    <button class="btn btn-primary" type="submit">Send inquiry</button>
    <p class="guard-msg">The form is almost ready. For now, call or text Hope at
      <a href="{PH}">{PD}</a> and we will get right back to you.</p>
  </form>""".replace("{PH}", PHONE_HREF).replace("{PD}", PHONE_DISPLAY)

    page("contact.html", "Contact | Bless Your Paws Puppies",
      "Ask about an available puppy or plan a visit. Call or text Hope, or send the inquiry form.",
      f"""<section><div class="wrap grid-2">
  <div>
    <p class="eyebrow">Contact</p>
    <h1>Say hello</h1>
    <p class="lede">The fastest way to reach us is a call or a text.</p>
    <ul class="facts">
      <li><span class="k">Hope (Munchkin Bernedoodles)</span>
        <span class="v"><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></span></li>
      <li><span class="k">Joy (Dobermans)</span>
        <span class="v">Number coming soon</span></li>
      <li><span class="k">Email</span><span class="v">Coming soon</span></li>
      <li><span class="k">Where</span><span class="v">Northern Indiana</span></li>
    </ul>
    <p class="fine">Visits are by appointment. Our location is shared once your
      visit is scheduled. {CHIP_DRAFT}</p>
  </div>
  <div>
    <h2>Send an inquiry</h2>
    {form_guard}
  </div>
</div></section>""")

    # ---- waitlist
    wait_form = """<form data-guard action="https://formspree.io/f/REPLACE_WAITLIST_ID" method="POST">
<div style="position:absolute;left:-9999px" aria-hidden="true">
      <label for="w-hp">Leave this field empty</label>
      <input id="w-hp" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    <div><label for="wname">Your name</label><input id="wname" name="name" required></div>
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
      <a href="{PH}">{PD}</a> with the word WAITLIST and your name.</p>
  </form>""".replace("{PH}", SMS_HREF).replace("{PD}", PHONE_DISPLAY)

    page("waitlist.html", "Join the Waitlist | Bless Your Paws Puppies",
      "Hear about new litters before they are listed. Waitlist families get first pick.",
      f"""<section><div class="wrap grid-2">
  <div>
    <p class="eyebrow">The waitlist</p>
    <h1>Hear about litters first</h1>
    <p class="lede">Our litters tend to reserve quickly. One puppy from the current
      litter went home to a waitlist family before it was ever listed publicly.</p>
    <p>Joining the waitlist costs nothing and commits you to nothing. When a new
      litter arrives, waitlist families hear first, in the order they joined, and
      get first chance to reserve.</p>
  </div>
  <div>
    <h2>Add your name</h2>
    {wait_form}
  </div>
</div></section>""")

    # ---- gallery
    picks = []
    for s, n, _, _, count, _ in MUNCHKINS:
        for i in (1, 2):
            picks.append((f"{s}-{i:02d}", n, "munchkin"))
    for s, n, _, _, count, _ in DOBERMANS:
        for i in range(1, min(count, 2) + 1):
            picks.append((f"{s}-{i:02d}", n, "doberman"))
    gal_items = "\n".join(
        f'<a data-line="{line}" href="puppy-{stem.rsplit("-",1)[0]}.html">'
        f'<img {srcset(stem)} alt="{name}" loading="lazy"></a>' for stem, name, line in picks)
    page("gallery.html", "Photo Gallery | Bless Your Paws Puppies",
      "Photos of our Munchkin Bernedoodle and Doberman Pinscher puppies.",
      f"""<section><div class="wrap">
  <p class="eyebrow">Gallery</p>
  <h1>The photo album</h1>
  <div class="filter-row">
    <button class="cur" data-line="all">All</button>
    <button data-line="munchkin">Munchkin Bernedoodles</button>
    <button data-line="doberman">Dobermans</button>
  </div>
  <div class="gal-grid">{gal_items}</div>
</div></section>""")

    # ---- reviews
    page("reviews.html", "Reviews | Bless Your Paws Puppies",
      "What families say about their Bless Your Paws puppies.",
      f"""<section><div class="wrap prose">
  <p class="eyebrow">Reviews</p>
  <h1>From our families</h1>
  <p>{CHIP_SAMPLE}</p>
  <blockquote class="lede" style="border-left:3px solid var(--sage);padding-left:1rem">
    "Our puppy came home confident, snuggly, and already used to kids. You can tell
    she was raised in the middle of a family." <span class="fine">A waitlist family
    (sample review, real ones are being gathered with permission)</span></blockquote>
  <p>We are collecting reviews from our puppy families now, with their permission,
    and will post them here as they come in. If you have one of our puppies, we
    would love to hear from you.</p>
  <div class="btn-row"><a class="btn btn-primary" href="contact.html">Share your story</a></div>
</div></section>""")

    # ---- legal drafts
    page("health-guarantee.html", "Health Guarantee | Bless Your Paws Puppies",
      "Our written health guarantee for every puppy.",
      f"""<section><div class="wrap prose">
  <div class="draft-banner">DRAFT. This guarantee is a working draft prepared for
    the family to review, reword, and approve. It is not in effect as written.</div>
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
    <li>Have your own veterinarian examine the puppy within 72 hours of go-home.
      If a significant pre-existing condition is found, contact us immediately.</li>
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
    the family to review, reword, and approve. It is not in effect as written.</div>
  <p class="eyebrow">Purchase agreement</p>
  <h1>Purchase agreement</h1>
  <p>This agreement is between Bless Your Paws Puppies (the breeder) and the buyer
    named at reservation, for the puppy identified by name and litter.</p>
  <ul>
    <li><strong>Price and deposit.</strong> The purchase price is the listed price of
      the puppy. A ${DEPOSIT} deposit reserves the puppy and is applied to the
      balance. The balance is due before or at pickup.</li>
    <li><strong>Deposit terms.</strong> The deposit is transferable to another
      available puppy if plans change. Refund terms to be confirmed by the family.
      {CHIP_DRAFT}</li>
    <li><strong>Go-home.</strong> Puppies go home no earlier than 8 weeks of age,
      after a final veterinary check.</li>
    <li><strong>Health.</strong> The puppy is sold with the
      <a href="health-guarantee.html">written health guarantee</a>, which is part of
      this agreement.</li>
    <li><strong>Care.</strong> The buyer agrees to provide routine veterinary care
      and a safe home.</li>
    <li><strong>Return first.</strong> If at any point the buyer can no longer keep
      the dog, the breeder is contacted first and given the option to take the dog
      back before it is rehomed or surrendered.</li>
  </ul>
  <p class="fine">A signed copy goes home in the go-home folder with the health
    records.</p>
</div></section>""")

    # ---- privacy, 404
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
  <p>To have your information removed, call or text {PHONE_DISPLAY} and we will
    delete it.</p>
</div></section>""")

    page("404.html", "Page Not Found | Bless Your Paws Puppies",
      "That page wandered off.",
      f"""<section><div class="wrap center prose" style="margin:0 auto">
  <p class="eyebrow">404</p>
  <h1>This page wandered off</h1>
  <p class="lede">Probably chasing something. Try the puppies instead.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-primary" href="puppies.html">Available puppies</a>
    <a class="btn btn-ghost" href="index.html">Home</a>
  </div>
</div></section>""")

    # ---- per-puppy pages
    def puppy_page(slug, name, sex, colour, photos, note, price, breed, litter_line, extra_facts):
        pron = "she" if sex == "Girl" else "he"
        thumbs = "\n".join(
            f'<button data-src="img/puppies/{slug}-{i:02d}.jpg" class="{"cur" if i==1 else ""}">'
            f'<img src="img/r/{slug}-{i:02d}-240.webp" alt="" loading="lazy"></button>'
            for i in range(1, photos + 1))
        sibs = MUNCHKINS if breed.startswith("Munchkin") else DOBERMANS
        sib_links = " &middot; ".join(
            f'<a href="puppy-{s}.html">{n}</a>' for s, n, *_ in sibs if s != slug)
        note_html = f"<p><strong>{note}</strong></p>" if note else ""
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product",
            "name": f"{name}, {breed} puppy", "image": f"{BASE}/img/puppies/{slug}-01.jpg",
            "description": f"{name} is a {colour.lower()} {breed} puppy, available now.",
            "offers": {"@type": "Offer", "priceCurrency": "USD", "price": str(price),
                       "availability": "https://schema.org/InStock"}})
        page(f"puppy-{slug}.html", f"{name}, {breed} Puppy | Bless Your Paws Puppies",
          f"{name} is a {colour.lower()} {breed} puppy. ${price:,} with a ${DEPOSIT} deposit to reserve.",
          f"""<section><div class="wrap">
  <p class="eyebrow"><a href="puppies.html">Available puppies</a> / {breed}</p>
  <div class="grid-2">
    <div>
      <img id="gallery-main" src="img/puppies/{slug}-01.jpg"
        alt="{name}, a {colour.lower()} {breed} puppy" style="border-radius:4px;border:1.5px solid var(--forest)">
      <div class="thumbs">{thumbs}</div>
    </div>
    <div>
      <h1>{name}</h1>
      <p class="lede">{sex} &middot; {colour} &middot; {breed}</p>
      <ul class="facts">
        <li><span class="k">Price</span><span class="v">${price:,}</span></li>
        <li><span class="k">Status</span><span class="v">Available</span></li>
        <li><span class="k">Sex</span><span class="v">{sex}</span></li>
        <li><span class="k">Color</span><span class="v">{colour}</span></li>
{extra_facts}
      </ul>
      {note_html}
      <div class="reserve">
        <h3>Reserve {name}</h3>
        <p class="fine">A ${DEPOSIT} deposit holds {pron.replace('he','him') if sex=='Boy' else 'her'} until go-home day. Pay the deposit now,
          or the full amount if you prefer.</p>
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
      <p>{name} is a {colour.lower()} {sex.lower()} from {litter_line} {pron.capitalize()} is
        growing up in the house, handled every day, around kids and other dogs, with
        early neurological stimulation from the first weeks. Ask us anything about
        {pron.replace('he','him') if sex=='Boy' else 'her'}; we are happy to send more photos or hop on a video call.</p>
      <p class="fine">Littermates: {sib_links}</p>
    </div>
  </div>
</div></section>""",
          extra_head=f'<script type="application/ld+json">{ld}</script>\n')

    m_facts = f"""        <li><span class="k">Born</span><span class="v">July 22, 2026</span></li>
        <li><span class="k">Go home</span><span class="v">September 16 to 23, 2026</span></li>
        <li><span class="k">Expected adult size</span><span class="v">15 to 25 lbs (draft)</span></li>"""
    d_facts = """        <li><span class="k">Born</span><span class="v">To be posted</span></li>
        <li><span class="k">Dam</span><span class="v">Mira, health tested</span></li>"""
    for s, n, x, c, ph, note in MUNCHKINS:
        puppy_page(s, n, x, c, ph, note, M_PRICE, "Munchkin Bernedoodle",
                   "Troy's litter of eight, born July 22, 2026.", m_facts)
    for s, n, x, c, ph, note in DOBERMANS:
        puppy_page(s, n, x, c, ph, note, D_PRICE, "Doberman Pinscher",
                   "Mira's litter.", d_facts)

# ---------------------------------------------------------------- assets
def build_assets():
    open("style.css", "w", encoding="utf-8").write(CSS)
    open("main.js", "w", encoding="utf-8").write(JS)

    os.makedirs("img/placeholder", exist_ok=True)
    def placeholder(fname, label):
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
<rect width="800" height="800" fill="#a8b89e"/>
<rect x="24" y="24" width="752" height="752" fill="none" stroke="#fdf9f9" stroke-width="3" stroke-dasharray="10 8"/>
<g transform="translate(400 330)" fill="#fdf9f9">
 <ellipse cx="0" cy="40" rx="58" ry="52"/>
 <ellipse cx="-62" cy="-28" rx="26" ry="34"/>
 <ellipse cx="-21" cy="-52" rx="24" ry="32"/>
 <ellipse cx="21" cy="-52" rx="24" ry="32"/>
 <ellipse cx="62" cy="-28" rx="26" ry="34"/>
</g>
<text x="400" y="520" text-anchor="middle" font-family="Georgia,serif" font-size="42" fill="#223d2c">{label}</text>
<text x="400" y="572" text-anchor="middle" font-family="Georgia,serif" font-size="30" fill="#34523f">Photo coming soon</text>
</svg>"""
        open(f"img/placeholder/{fname}", "w", encoding="utf-8").write(svg)
    placeholder("troy.svg", "Troy")
    placeholder("cavalier-sire.svg", "Our Cavalier sire")
    placeholder("doberman-sire.svg", "The Doberman sire")

    # favicons + og card from the brand assets
    from PIL import Image
    mark = Image.open("img/brand/mark-paw-heart.png").convert("RGBA")
    bbox = mark.getbbox(); mark = mark.crop(bbox)
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
    lw = 980; lh = round(logo.height * lw / logo.width)
    logo_r = logo.resize((lw, lh), Image.LANCZOS)
    og.paste(logo_r, ((1200 - lw)//2, (630 - lh)//2), logo_r)
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
    n = len([p for p in os.listdir(".") if p.endswith(".html")])
    print(f"scaffold complete: {n} pages, style.css, main.js, placeholders, favicons, og-card, robots, sitemap")
