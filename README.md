# Bless Your Paws — website

Static website for **Bless Your Paws Puppies**, the dog-breeding business of Hope and
Joy (twin sisters). Plain HTML/CSS/JS, no build step. Served by the `blessyourpaws`
Cloudflare Worker; a push to `main` deploys it.

**The site presents them by first name only. Do not add a surname anywhere in the
copy** (Alex, 2026-08-26).

---

# GO-LIVE CHECKLIST

> **LIVE since 2026-08-27** at https://blessyourpawspuppies.com (v=123). Steps 1 to 3 are
> done and verified. What is left is off-site: the two redirect rules, Search Console, and
> the Google Business Profile. See "Still to do after launch" directly below.

## Still to do after launch

- [ ] **`www` -> apex redirect rule** on the zone. Low urgency, not zero: www serves the
      same site as a custom domain and every page it serves carries a canonical pointing
      at the apex, so Google will consolidate them on its own. The rule makes it explicit.
      A Cloudflare **Redirect Rule** (Rules -> Redirect Rules) is the mechanism, matching
      `Hostname equals www.blessyourpawspuppies.com` and dynamically redirecting to
      `concat("https://blessyourpawspuppies.com", http.request.uri.path)` at 301 with
      preserve-query-string on. Keep www as a Worker custom domain either way, so the
      hostname still resolves.
- [x] **workers.dev is already off.** Disabled by the deploy that added the custom domains
      and pinned `"workers_dev": false` in `wrangler.jsonc`. Verified returning 404. There
      is nothing left to turn off.
- [x] **DROPPED 2026-08-27 (Alex): `blessyourpaws.com` is not a domain they are
      tracking.** Earlier notes said it was owned and should 301 to the canonical; it is
      not in scope. Ignore any other mention of it in this file.
- [x] **DONE 2026-08-27 (Alex): property added, `sitemap.xml` submitted, home page
      indexed.** Nothing further to do by hand. Do NOT request indexing page by page; the
      sitemap covers all 22. Worth checking that the property covers BOTH apex and www (a
      Domain property does, a URL-prefix property for the apex alone does not), and
      glancing at the Pages report in a few days for anything unexpectedly excluded.
- [x] **SET UP 2026-08-27 (Alex), with the real domain as the website.** Service area is
      20 entries, which is Google's cap. Note ~10 of them (Warsaw, Winona Lake, Mentone,
      Milford, Claypool, Leesburg, Pierceton, Silver Lake, North Webster, Syracuse) sit
      inside Kosciusko County, which is also listed, so those slots are redundant. Not
      worth rushing to change: **service areas are informational and do not widen the
      ranking radius** for a service-area business, which is still driven by the verified
      address. If the list is ever edited, spend the freed slots on larger nearby draws
      such as Elkhart, Mishawaka or Huntington.
- [ ] Still to confirm on the profile: name is exactly `Bless Your Paws Puppies` with
      nothing appended, the address is entered but NOT displayed (customers served outside
      the business location), phone reads `(574) 377-8023`, and no photo shows the house,
      the street or carries geotags.
- [ ] Bing Places and Apple Business Connect, same address rule.


**Nothing here is optional and the order matters.** Steps 1 to 3 are the switch; step 3
is irreversible in practice, because Google caches what it finds.

## Before you flip anything: these must be TRUE

- [x] **DONE 2026-08-26: the fabricated review is gone**, replaced by Brenda's real
      review, quoted word for word.
- [x] **DONE 2026-08-27: no chips remain anywhere.** `grep -c 'class="chip' *.html`
      returns nothing on any page. If you add one, add it back to this list too.
- [x] **DONE 2026-08-27: the Health Guarantee page is Hope's real guarantee**, and the
      Privacy Policy is written from what the site actually does.
- [x] **DONE 2026-08-27: Hope has signed off on the terms** (Alex), so the last draft
      banner is off `purchase-agreement.html`. **No draft banners or chips remain on any
      page.** The `.draft-banner` CSS is deliberately kept: it is the only user of
      `--draft`/`--draft-bg` and the mechanism for flagging unapproved copy next time.
- [ ] Someone qualified reads the Purchase Agreement, the Health Guarantee and the Privacy
      Policy. The guarantee is Hope's own wording; the terms and the privacy policy are
      not, and both describe real obligations.
- [ ] Both forms tested end to end, with the notification actually landing in Hope's inbox.
- [x] **RESOLVED 2026-08-26: `info@` forwards to the right Gmail.** The open question was
      whether "HPW 21", as Hope said it on the call, was the same account as
      `hpwtwin1@gmail.com`. It is: Cloudflare Email Routing only enables a rule after the
      destination address clicks its own verification link, and **Hope clicked it herself**
      at 00:02 UTC. That is the confirmation, not a second thing to go and check.
- [ ] Still worth doing: send a real test to `info@` and watch it land, so the first live
      message is not the first test.

## 0. Launching without Stripe — already works, nothing to build

Confirmed 2026-08-27. **The site is safe to launch before Stripe exists.** All 21 pay
links across the seven puppy pages still point at `buy.stripe.com/REPLACE_DEPOSIT`,
`REPLACE_BALANCE` and `REPLACE_FULL`, and `main.js` keys its guard on the literal string
`REPLACE`: any such link has its click cancelled and reveals the message beside it instead.
A visitor clicking Deposit on Caleb's page sees

> Online payments are almost ready. To reserve Caleb today, call or text Hope at
> (574) 377-8023.

So the buttons cannot take money, cannot 404, and cannot land anyone on a broken Stripe
page. Nothing needs disabling before launch.

**When the real links exist**, paste them over the three `REPLACE_*` placeholders in
`scripts/scaffold.py`, bump `V`, regenerate. The guard disarms itself, because the string
`REPLACE` is gone. No code change.

- [ ] **Do NOT enable ACH or bank debit on the link charging $2,060.** The dual pricing
      holds only while every payment at the card price is a card payment.
- [ ] Worth a look before launch, and a judgement call, not a defect: once someone submits
      an application, the gate unlocks **three** pay buttons on each puppy page, and all
      three currently show the same phone message. Three dead buttons in a row reads worse
      than one clear instruction. If Stripe is still days away at launch, consider hiding
      the pay row until the links are live and letting the "call or text Hope" line carry
      it alone. It is a few lines in the scaffold and reversible either way.

## 1. Domain

- [x] **DONE 2026-08-27.** Both declared in `wrangler.jsonc` as `custom_domain: true`
      routes rather than clicked in, so the intent lives in the repo. Pre-flight found
      both zones on Cloudflare nameservers, Email Routing MX live on the apex, and **no A
      or AAAA record on any hostname**, so nothing was serving and there was no live site
      to break.
- [x] **DONE.** Apex answered 200 over HTTPS immediately; www finished issuing a
      few minutes later and also returns 200.
- [ ] 301 `blessyourpaws.com` to `blessyourpawspuppies.com` (a redirect rule on that zone).

## 2. `BASE`

- [x] **DONE 2026-08-27.** Note the deploy that created the custom domains also
      **disabled workers.dev**, warning it does that by default when `workers_dev` is
      absent, so BASE had to move in the same push or all 23 pages would have pointed at
      a host that now 404s. `workers_dev` is pinned `false` explicitly so one hostname
      serves the site and a later deploy cannot quietly restore a second.
- [x] Order held: BASE moved only after the apex resolved, and indexing opened only
      after every canonical was confirmed returning 200 on the real domain.
- [ ] The URL shape is already correct and needs no work: links, canonicals and the
      sitemap are extensionless, which is what the Worker serves.

## 3. The switch

- [x] **DONE 2026-08-27 via `DRAFT_MODE = False`**, not by deleting the line. One
      boolean drives the noindex meta and robots.txt together, so the site can be
      closed again by flipping it back.
- [x] **DONE.** Also now carries `Sitemap: https://blessyourpawspuppies.com/sitemap.xml`.
- [x] **CONFIRMED on the live domain:** 0 noindex tags across 8 sampled pages, all
      22 sitemap URLs 200, /robots.txt and /sitemap.xml 200, an unknown path 404s
      to the real 404 page.

## 4. Get found for the brand name

- [ ] Search Console: add the property, submit `sitemap.xml`, request indexing on the home
      page. This is what turns "eventually" into days.
- [ ] **Google Business Profile.** For a branded search this is often more prominent than
      the site itself. It has the one genuinely irreversible step on the whole project:
      **enter the address to verify, then hide it, on the first save.** A published home
      address is scraped within days and hiding it afterwards does nothing about the copies.
      Full setup sheet further down this README.
- [ ] Bing Places and Apple Business Connect. Same address rule.
- [ ] Add `sameAs` to the schema once Hope gives the social profiles. For a branded query
      this is the signal that confirms the business is a real, single entity.
- [ ] Expect the marketplace listings (Puppy Connection and similar) to outrank the site
      for their own name at first. That resolves with time; link from those profiles to the
      site where you can.

## 5. After

- [ ] Watch the first real inquiry all the way through: form, Formspree archive, email.
- [ ] Diary: **Troy's OFA eye certificate expires 14 Aug 2027.** The page states the exam
      date but no longer states the one-year validity, so after that date it implies a
      currency it does not have.
- [ ] Delivery options and the balance payment method are still marked draft on
      `process.html`. Decide or remove.

---

**Status: technically complete, content-blocked.** Generated by `scripts/scaffold.py`,
which holds the puppy data and templates; it overwrites on re-run, so fold hand edits
back into the script or stop running it. Verified in-browser: zero broken images at
desktop and 390px, no horizontal scroll, nav overlay opens fixed and closes, thumb
galleries swap, pay and form guards intercept with Hope's number, Product and FAQ
schema present, site-checks clean.

**Character:** a pressed-flower garden album. Blush paper, forest ink, sage stems,
seed-packet cards with arch-top photos, unhurried vintage serifs.

- **Palette:** forest `#223d2c` (ink, dark bands) / sage `#7f8e79` (large text only,
  `#6d7a68` derived for small) / light sage `#a8b89e` / rose `#feb5bc` / pale pink
  `#fbc4db`. All sampled from the client's swatches in `img/brand/`. Full contrast
  matrix and the two hard rules are in [`CLAUDE.md`](CLAUDE.md).
- **Type:** Fraunces (display) + Mulish (body), via Google Fonts.
- **Archetype:** seed-packet card grid with breed doors and arch-top hero photos.
  Distinct from KFC's ledger rows in palette, type, and structure.

## Breed lines

| Line | Owner | Status |
|---|---|---|
| Munchkin Bernedoodle (Mini Multi Gen Bernedoodle × Cavalier King Charles Spaniel) | Hope | Born 22 Jul 2026. 8 whelped, 1 sold off the waitlist, **7 available**. Home 16 Sep 2026 |
| Doberman Pinscher | Joy (co-owned with Amber) | 3 available: Elowen, Malcolm, Griffin |
| Maltipoo | TBC | ~18 months out. **Deliberately not in the launch build** |

## Planned pages

Home · Puppies · Munchkin Bernedoodles · What is a Munchkin Bernedoodle? · Dobermans ·
The Dogs (parents) · Health & Testing · Gallery · Reviews · About · Process + FAQ ·
Contact · Purchase Agreement · Health Guarantee · per-puppy pages · Privacy · 404

The **"What is a Munchkin Bernedoodle?"** explainer is the highest-value SEO page on
the site. Every competing breeder runs one, because buyers search the term itself.

## Run locally

```bash
python -m http.server 8199 --directory blessyourpaws-website-repo
```

Or `preview_start({name: "blessyourpaws"})` from the root launch.json.

Before committing: `python check_site.py blessyourpaws-website-repo` from the
`site-checks` repo.

## Deliberate decisions (do not "fix" these back)

- **No shopping cart.** Puppies are quantity-one inventory. A cart implies stock and
  opens a double-sell race where two families pay deposits on the same puppy minutes
  apart. The flow is per-puppy "Reserve with a deposit" instead. The client asked
  "Cart?" and this is the considered answer.
- **Stripe Checkout (hosted), never a card form on the site.** Card data never touches
  our pages and PCI scope stays effectively nil.
- **Nothing carries over from Kingdom Family Companions except facts about the dogs.**
  Full boundary list in [`CLAUDE.md`](CLAUDE.md). KFC is Amber's site.
- **No home address anywhere.** Service area only.
- **Maltipoos excluded at launch** even though the client mentioned the line, because
  it is ~18 months out. The breed-page pattern makes adding it a content task.

## Pending (the project tracker — keep current)

### Blocking the build

- [x] **Quote tentatively accepted 2026-08-22. Phase 1 build started.** Phased plan:
      $1,500 site now, $1,500 admin later, $500 Maltipoo line later.
- [ ] Confirm the five swatches in `img/brand/` are the final brand palette and not
      just inspiration.
- [x] **RESOLVED: logo package supplied and in use**, navy recoloured to forest per Alex.
      Primary lockup in the header, paw-heart mark in the footer and favicon.

### Content from Joy and Hope

> **Client questionnaire issued 2026-08-22.** 27 questions covering every open item
> below, grouped into terms / parent dogs / their own words / look and feel / practical
> setup, tagged Hope / Joy / Both, with the launch blockers marked. Built outside this
> repo (it is a client document, not a site page) at
> `scratchpad/questionnaire.html` -> `BlessYourPaws-Questionnaire.pdf`. As answers come
> back, tick the items here rather than tracking them in the PDF.


- [x] **RESOLVED: the Bernedoodle dam is TROY** (female, Mini Multi Gen Bernedoodle).
      The "Mura/Mira" transcription was the Doberman, Mira, all along. The earlier
      note calling Troy the Cavalier sire was wrong.
- [x] **RESOLVED 2026-08-25: the Cavalier sire is BIP FINCH.** AKC TS65827904, 19 lbs,
      ruby, born 24 Dec 2024. Published on the parents page, every puppy page and the
      breed guide. **He is an outside stud, not one of their own dogs.** This item sat open
      in the README for two days after the fact and was repeated back as still-unknown on
      2026-08-27; if a name gets published, close the item in the same commit.
- [ ] PARKED with the Doberman line (off since 2026-08-23): Doberman sire name, registration and health testing.
- [x] Parent facts on file: dam Troy (Mini Multi Gen Bernedoodle, 21 lbs) and the
      AKC Cavalier sire (19 lbs, ruby).
- [x] **RESOLVED 2026-08-23: Troy has a full Wisdom Panel and it is now published.**
      Tested 2026-02-21, clear on 29 of 30 conditions, and **carries one copy of CDDY**
      (chondrodystrophy, FGF4 retrogene, autosomal dominant). Report committed at
      `records/troy-wisdom-panel-2026-02-21.pdf` and linked in full from her row on
      our-dogs, with a section explaining the result in plain language. Two false claims
      were removed from the site because of it, see this repo's CLAUDE.md.
- [ ] **Does the Cavalier sire's panel cover CDDY / the FGF4 retrogene?** This is now the
      most important open question on the site. CDDY needs only one copy to matter, so the
      framing of the whole pairing depends on his status, and many Cavalier panels do not
      test FGF4 at all. Until his report exists, the site says only that we are gathering
      it and deliberately does not characterise his results.
- [x] **SUPERSEDED 2026-08-25 (commit 7680122): the claim was deliberately reinstated on
      Hope's own word.** His row now reads "Genetic testing: clear, including for
      chondrodystrophy (CDDY). We are gathering his full results to publish here the same
      way we publish Troy's." There is still **no document**, because his breeder can only
      fax. This is a recorded decision, not an oversight, and the retraction note above it
      was the stale thing.
- [ ] **Residual risk, worth one decision: the site states it as fact, the commit records
      it as Hope's position.** Those are not the same claim. Troy carries one copy of CDDY
      and one copy is enough to pass on, so his status is the single most consequential
      health sentence on the site. Attributing it ("Hope's breeder reports him clear,
      including for CDDY; we are gathering the written panel") costs nothing and is
      accurate to what is actually known. **Ask Alex before rewording** — he chose the
      current phrasing knowingly.
- [ ] **Will the puppies themselves be tested for CDDY?** It is a cheap, definitive test
      for a dominant variant, and it would let Hope tell each buyer exactly where their
      puppy stands. No competitor offers that. Hope's decision.
- [x] **RESOLVED 2026-08-23: Troy is 22 lbs** (Alex). Updated in all eight places it
      appeared, and the draft chip on her weight is removed since it is confirmed. This
      also squares with the panel's predicted ideal range, which is recorded in
      `source-files/` rather than here. The puppy estimate is 15-20 lbs
      (Alex, 2026-08-23), superseding the 15-25 I had derived from the parents' weights.
- [x] **Troy's ancestry is NOT published** (Alex, 2026-08-23). It was briefly, then the
      report was trimmed to drop its breed-ancestry page and the percentages came off the
      site with it, so nothing on the page is unevidenced by the linked document. The
      figures are in `source-files/troy-panel-notes.md`, which is gitignored, and they must
      not be written back into any tracked file: **this README is publicly served too.**
      Still worth Hope knowing the minor breed fractions exist, in case a buyer runs their
      own panel.
- [x] **Dam is a Mini Multi Gen Bernedoodle** (confirmed 2026-08-22). Pawrade said
      "Mini", Puppy Connection said "Multi Gen"; she is both. Multi-gen supports a more
      consistent curl and lower shedding than an F1 — still a per-puppy prediction, never
      a promise.
- [x] **Sire is 19 lbs** (confirmed). Puppy Connection's 18 lbs is wrong.
- [x] **Per-puppy records complete for all seven Munchkin Bernedoodles** — real names
      Joshua, Eden, Havilah, Jordan, Caleb, Shiloh, Jericho, with sex and colour. Born
      22 July 2026, home 16 September 2026. Full table in the litter dossier.
- [ ] **Expected adult size is 15 to 20 lbs** (Alex, 2026-08-23). Held in one constant,
      `M_SIZE`, and shown on ten pages. Still carries a visible chip reading "Expected
      size, confirm before launch". **Open question: is 15-20 Hope's confirmed figure?**
      If so the chip comes off, the way Troy's weight chip did. The chip no longer claims
      the number is derived from the parents' weights, because 15-20 is narrower than
      anything 19 and 22 lbs alone imply, so it came from somewhere else.
- [ ] PARKED with the Doberman line (off since 2026-08-23): Doberman per-puppy detail.
- [x] **Prices set for launch (Alex, 2026-08-22): Munchkins $2,000, Dobermans $2,200.**
      The market case for raising the Munchkin price later stays in the audit docs.
- [ ] **Deposit amount and refund/transfer terms.** Never guess.
- [ ] **Health guarantee + Purchase Agreement: DRAFT pages shipped in the scaffold**
      per Alex's direction, each carrying a visible draft banner. **Must be verified,
      reworded by the family, and reviewed before launch. Not in effect as written.**
- [ ] Go-home package contents (vaccinations, deworming, vet check, microchip, food,
      blanket, contract).
- [x] **Socialisation and ENS documented** (from Pawrade's structured fields, pending
      Hope's confirmation): grass potty training; socialised with other animals, small
      dogs, large dogs, older kids and younger kids; ENS via Bio-Sensor, doorbell, loud
      music/TV, pots and pans, vacuum cleaner.
- [x] **Go-home kit:** vaccination and health record, vet examination, small bag of food,
      collar and leash, toy.
- [x] **Hope's phone number is 574-377-8023** (confirmed). Not the marketplace's
      574-221-0326.
- [x] **Joy's phone number is 574-265-1060** (Alex, 2026-08-23). Litter pages now route
      to whoever raises that litter: Doberman puppy pages carry Joy's number, Munchkin
      pages Hope's. The footer, the home page closing band and the chat panel list both,
      labelled by breed. Before this, every Doberman page told buyers to call Hope.
- [ ] **Rewrite the socialisation and puppy descriptions in Hope's own words.** The
      wording currently on both marketplaces is theirs, not hers — reusing it would put
      her site in competition with them on Google. Facts carry over; prose does not.
- [ ] Reviews/testimonials — Hope has at least one on social media. Need the wording,
      the buyer's name, and **explicit permission**. Joy's are unknown. Carry none
      over from KFC.
- [ ] Their story: how each came to breeding, in their own words. Whether the twin
      angle is part of the brand.
- [ ] PARKED with the Doberman line (off since 2026-08-23): rights to the Doberman puppy photos.
- [x] **RESOLVED 2026-08-23: faith element added** (Alex). A short note at the end of the
      About bio saying they are Christians who hope their work brings glory to God, with a
      link to a gospel film (youtube.com/watch?v=mIeRU12STNw). Set apart with a rule and
      the display face rather than by colour. Nothing doctrinal is asserted beyond that,
      and it appears on the About page only.
- [x] **RESOLVED 2026-08-23: Tirzah added as the eighth puppy**, marked Adopted!. Facts
      pulled from her Puppy Connection listing: girl, black phantom, same litter. Three of
      her four listing photos are hers; the fourth is Troy and was not carried over. Her
      description there is Puppy Connection's copy so no note was taken. Litter counts are
      now derived from the data, not written, so adding or adopting a puppy cannot leave a
      stale "Seven puppies" behind.
- [x] **RESOLVED 2026-08-23: mobile hero is option B**, full bleed with the caption over
      the foot of the photograph. Only the eyebrow, headline and buttons sit on the
      picture; the lede is below it on paper. `hero-options.html` can be deleted.
      Still open, and a business call rather than a design one: whether to keep
      havilah-01, which has only 5.4% headroom above the puppy's crown.
- [ ] **Floral motif: pick the placements.** NOTE 2026-08-25: the comparison pages
      (`floral-preview.html`, `floral-applied.html`) were deleted per the standing
      convention that previews do not ship. The decision is still open, so if Hope
      needs to see the options again, restore them from commit `e44e775` rather than
      rebuilding them:
      `git checkout e44e775 -- floral-preview.html floral-applied.html`
- [ ] Original item: Hope asked for flowers. Five assets are
      prepared and committed (`img/brand/floral-*.webp`: two corner sprays, a
      horizontal swag, a single sprig, a wreath) but **nothing is wired into the
      site**. `floral-preview.html` shows seven candidate placements against the real
      stylesheet. Recommendation on that page is options 1, 2 and 6-restrained only,
      i.e. three placements: the swag replacing the existing section divider, the
      sprig beside a heading, and low-opacity corner sprays on one dark band per page.
      `floral-applied.html` then shows those three recommendations built into real page
      sections, with a toggle for a true before and after, plus the puppy page left
      deliberately plain. Delete both preview pages once the choice is made, per the
      preview-page convention. Regenerate assets with `python scripts/prep_florals.py`.
- [x] **Photos pulled 2026-08-22.** 78 full-resolution originals for all seven Munchkin
      Bernedoodles, from the Puppy Connection listings with Hope's confirmation that the
      family owns the rights. Originals in gitignored `source-photos/puppy-connection/`;
      web JPEGs at 1400px in `img/puppies/` plus a 240/600/1100 WebP set in `img/r/`.
      Counts: joshua 10, eden 11, havilah 13, jordan 10, caleb 9, shiloh 11, jericho 14.
      Spot-verified that filing matches recorded colour.
- [x] **Doberman photos in, 2026-08-22.** Joy confirmed the Doberman photography and
      Mira are hers. Pulled from the Kingdom build's gitignored originals rather than
      re-scraping: Elowen 3, Malcolm 4, Griffin 6, plus Mira in `img/dogs/`. Most are
      6000x4000 camera originals, so far better than the 1800px web copies on that site.
      Each original was matched to its named web file by image fingerprint (MSE ≤ 0.011
      against a next-best of 0.14–1.47), not by eye. Map kept at
      `source-photos/kfc-original-map.json`.
- [ ] **Munchkin Bernedoodle parent photos** — Troy (the dam) and the Cavalier sire.
      Hope is getting photos of Troy. Branded placeholders ship meanwhile.
- [ ] PARKED with the Doberman line (off since 2026-08-23): the two unidentified adult Dobermans.
- [ ] PARKED with the Doberman line (off since 2026-08-23): the Golden Retrievers.
- [x] **Service area: Warsaw and Winona Lake, Indiana** (confirmed 2026-08-22).
- [ ] Confirm both are comfortable with faces and first names on a public site.

### Technical

- [x] **DONE 2026-08-26. Formspree, activated.** Inquiry `mnpaegkw`, waitlist `xbgrnzvq`,
      held in `FORM_INQUIRY` / `FORM_WAITLIST`. Notifications go to
      `info@blessyourpawspuppies.com`, which Email Routing forwards to Hope.
      **Chosen over the Worker deliberately:** the Worker's notification is a Cloudflare
      Email Sending call, and Email Sending requires the Workers Paid plan ($5/mo) — which
      is what the `Unauthorized [code: 2036]` was all along, not scopes and not onboarding.
      Formspree is free at 50 submissions a month, which is not a constraint for one
      litter, and unlike a pure relay it keeps its own copy of every submission, so a lead
      survives an email being spam-filtered.

      The trade, recorded so it can be revisited: a third party sees buyer names, emails,
      phone numbers and what families write about their children, and the submission
      archive lives under Formspree's retention rather than ours. Moving to the Worker
      later means Workers Paid, a Turnstile widget, and pointing the two form actions at
      it — `blessyourpaws` is already registered in the Worker's `SITES`.
- [ ] Stripe account (Hope's). **Stripe does not require an LLC** — sole proprietors
      can open an account with an SSN. Whether she *should* form one is a liability
      and tax question for an attorney or CPA, not for this project.
- [ ] Branded email — Cloudflare Email Routing forwarding is free.
- [x] **Privacy policy written 2026-08-27**, from an audit of what the site actually does
      rather than a template: no analytics, no advertising, no tracking pixels, and no
      cookies set by the site. The only client-side storage is the `sessionStorage` flag
      behind the application gate, and no third party is contacted until a visitor submits
      a form or clicks an outbound link. **If that ever stops being true — analytics, a
      Meta pixel, an embedded YouTube player rather than a link — the page has to change
      in the same commit.** It commits to updating before anything is turned on.
- [ ] Domain (~$12–20/yr, theirs). Set the custom domain in Pages settings *before*
      moving DNS; enable Enforce HTTPS after the cert issues.
- [ ] Publish in **draft mode** (noindex on every page + closed robots.txt) so it is
      shareable before launch.
- [x] **Published 2026-08-22** to
      https://github.com/alexharper24/blessyourpaws-website-repo
      Live preview: **https://alexharper24.github.io/blessyourpaws-website-repo/**
      Pages serves from `main` / root, HTTPS enforced. Still in **draft mode**
      (noindex on all 26 pages + `robots.txt` closed), so the link is shareable but
      not indexable.
- [ ] Google Business Profile + Search Console after launch. See the full GBP checklist
      below — the profile is the single highest-leverage item on this list.
- [ ] Phase 2 only: Cloudflare Worker + D1 admin, two logins, photo upload, and the
      **Stripe webhook that auto-marks a puppy reserved when a deposit clears**.

### Search, local and AEO

Method and reasoning: `.claude/guides/local-seo-aeo.md`. Read the "does NOT fit our sites"
section first — this is a **considered purchase**, not a proximity one. Families drive hours
for a specific puppy, so the breed term carries far more weight than the map pack.
**Do not build the "Core 30", per-city pages, or landmark pages here.** They are right for a
plumber and would be thin content for a breeder with one category and one product.

Free, needs nothing from Hope and Joy:

- [x] **DONE 2026-08-24.** `areaServed` is now structured `City`/`State` entries rather than
      a free-text sentence. Still no `address` and no `geo`, permanently.
- [x] **DONE 2026-08-24.** `priceRange` and `logo` added to `LocalBusiness`.
- [x] **DONE 2026-08-24.** Seven editorial links added by anchoring words ALREADY in the
      copy, so not one sentence was rewritten. Verified: exactly one word changed across all
      22 pages, and that was the intended H1. `about.html` still has no inbound body link;
      there is no natural anchor for it anywhere and inventing a sentence to create one would
      have cost more in voice than the link is worth.
- [x] **DONE 2026-08-24.** H1 is now "Munchkin Bernedoodle puppies raised in the middle of
      real family life" — the distinctive clause kept word for word, the breed on the front.
      The region was already in the eyebrow directly above, so only the breed was missing.
      Revisit only if the chosen GBP category differs from the breed name.
- [ ] Grow the FAQ from real questions — Google "People also ask" and Reddit breed threads.
      **Reword rather than copying questions verbatim**; the lift-them-exactly pattern is
      recognised now. Anything touching Hope and Joy's own practices has to be asked, not
      inferred.

Needs Hope and Joy:

- [ ] `sameAs` in schema, pointing at their real social profiles. A primary entity-alignment
      signal for Google and the AI assistants alike. Blocked on the socials.
- [ ] Review widget and `aggregateRating`/`Review` schema. Blocked on reviews plus
      permission to publish them.

## Hosting: Workers static assets, not Pages (decided 2026-08-25)

The site is served by a **Worker** (`blessyourpaws`), the same shape as
`roanoke-baptist`, because an admin surface behind auth is coming and that decision is
expensive to reverse once a domain points at the old one.

Live for testing at `https://blessyourpaws.alexharper.workers.dev`. The Pages project
(`blessyourpaws-website-repo.pages.dev`) still exists and still builds from `main`;
retire it once the domain is attached to the Worker, so there is no ambiguity about which
host is live.

**Why a Worker rather than Pages + a separate Worker.** Both work. A separate Worker never
needs to intercept a page request, which is exactly what `form-backend-worker` does for
every client site. But an admin needs the opposite: a route on the same origin, protected
by Cloudflare Access, possibly rendering a page server-side. Pages Functions could do it;
Workers static assets is what the other project already proves out, so the patterns and the
Access code are reusable rather than invented twice.

What runs where: only `/admin`, `/admin/*` and `/api/*` cost a Worker invocation
(`run_worker_first`). Every page, the stylesheet, the images and the PDFs are served
straight from the edge.

**`html_handling` is left at the default, and that is a decision.** It serves `/puppies`
directly with a 200 and 307s `/puppies.html` to it, which matches this site's extensionless
links, canonicals and sitemap. `roanoke-baptist` sets `"none"` for the opposite reason: its
links all end in `.html` and any other mode would put a 307 in front of the whole site.
**Match the mode to the links.** Verified on the deployed Worker: `/`, `/puppies`,
`/our-dogs`, `/puppy-eden` and `/contact` all return 200 with no redirect, and
`/puppies.html` returns 307 then 200.

**`.assetsignore` is the real control for the internal docs.** On Pages everything in the
output directory was served and the docs had to be redirected away, which still ships the
file. Here they are never uploaded: 523 files of the 1268 in the tree. `.git/` is listed
first, because without it wrangler reads the whole repository history as site assets and
fails on a pack file far over the 25 MiB per-asset limit. This does **not** make the repo
private; it is public on GitHub regardless, so no client confidences in tracked files.

**`_headers` does not apply to responses the Worker generates**, only to served assets.
Anything returned from `worker/index.js` sets its own headers. Verified that assets still
get `immutable` for a year and HTML still revalidates.

### Still to do for the admin

- [x] **DONE 2026-08-26. Workers Builds connected** to `alexharper24/blessyourpaws-website-repo`
      on `main`, so a push deploys. Settings, for when the next site needs this:

      | Field | Value |
      |---|---|
      | Build command | *empty* (no build step, the HTML is committed) |
      | Deploy command | `npx wrangler deploy` |
      | Path | `/` |
      | Enable Preview builds | **off** |

      **Preview builds are off deliberately.** `preview_urls` is `false` in
      `wrangler.jsonc`, so the non-production deploy command would create versions with no
      URL to open: build minutes spent on something unviewable. There is also only `main`
      in this repo, so nothing would trigger it. Revisit with the admin, together with
      whether Access can cover a preview hostname.

      **Give each project its own build token.** The dashboard offered a token named for
      another project. Reusing it couples the two: rotating or revoking it for one silently
      breaks the other's deploys, and the name stops meaning anything. This Worker needs
      exactly **Account → Workers Scripts → Edit** and nothing else, since its only binding
      is static assets, which upload as part of the script. Add D1 or R2 permissions only
      when a binding actually appears.

      **Ignore the dashboard's permissions warning if it names email_routing.** This Worker
      declares no email bindings. The warning compares the token against what a Worker
      could need, not against what yours declares, and granting email permissions to a
      static-site build token is access for no reason.
- [ ] Create the Cloudflare Access application covering `/admin` on the production
      hostname, then add `ACCESS_TEAM_DOMAIN` and `ACCESS_AUD` to `wrangler.jsonc`. The
      Zero Trust team domain already in use is `shy-truth-7b36`.
- [ ] Verify the Access JWT in the Worker as a second line of defence, not the only one.
      `roanoke-website-repo/worker/access.js` is the working example to copy.
- [ ] `preview_urls` is off deliberately: a preview hostname is not covered by an Access
      application scoped to the production hostname.

## Purchase agreement: Hope's document and the site, now aligned

Her document (`source-files/BYPP Purchase Agreement.docx`, gitignored) is a **fill-in bill
of sale**: buyer name/address/phone/email, the puppy's sex, colour, DOB, microchip number
and parents' names, the fee with 7% Indiana sales tax, the $500 deposit and balance with
dates, and both signatures. **It contains no terms at all** — no deposit clause, no health
guarantee, no return policy, no companion-only restriction. So it did not replace the terms
on `purchase-agreement.html`; it supplied the half that page was missing. The page carries
both, and **as of 2026-08-27 her .docx carries both too**. The terms stay marked draft on
the site until Hope and Joy approve them.

**If either one changes, change both.** The eight terms are duplicated between
`scripts/scaffold.py` and the .docx by hand; there is no generator linking them.

- [x] **RESOLVED 2026-08-26 (Alex): dual pricing, not a surcharge.** Her document says
      there is a 2.9% card charge for paying online. The site does not, and will not. That is surcharge language, and the site deliberately uses dual pricing
      instead: $2,060 list, $2,000 cash. The difference is not cosmetic. A cash discount is
      permitted everywhere; a card surcharge cannot lawfully be applied to debit cards, and
      a Stripe Payment Link cannot tell debit from credit before the payment goes through.
      **The website copy does not carry her wording**, because publishing both framings
      would be worse than publishing neither. Hope needs to pick one, and the agreement and
      the site then have to match.
- [x] **RESOLVED 2026-08-26 (Alex): the puppies are microchipped.** Her agreement records
      a microchip number, which is what surfaced the gap: `M_KIT` had no microchip while the
      Doberman list did. It is on the go-home list now.
- [x] **DONE 2026-08-27: Hope's document updated to match.**
      `source-files/BYPP Purchase Agreement.docx` now carries the dual pricing and the
      eight terms, and a rendered `BYPP Purchase Agreement (preview).pdf` sits beside it
      for reading without Word. Her original is kept at
      `source-files/archive/BYPP Purchase Agreement (original from Hope).docx`. What
      changed:
      - The `2.9% card charge` line is gone, replaced by "The purchase price is $2,060,
        plus 7% Indiana sales tax. Pay the balance in cash and the price is $2,000, a $60
        cash discount." **List price first, discount second.** That ordering is the whole
        legal point and must not be flipped to "$2,000 plus a card fee".
      - A `Payment method (circle one): Card $2,060 / Cash $2,000` line, so the chosen
        price is recorded on the signed document.
      - Page 2 is new: the eight terms, an acknowledgement that the buyer has read the
        agreement and the health guarantee and received a copy of both, then the
        signatures. **Signatures moved to after the terms**; on her original they sat on
        page 1 above terms that did not exist.
      - Four repairs to the form itself: the email hyperlink pointed at an empty relationship
        target and was a dead link, so it now points at the real mailto; "Puppies new family
        information" reads "Puppy's new family information"; a **puppy name** field was
        added (the form recorded sex, colour, DOB, microchip and both parents but never the
        puppy's own name); and the balance line gained an **amount** blank, having had only
        a date.
      - Verified: opens in Word, renders as 2 pages, passes OOXML schema validation
        against the original.
- [x] **APPROVED 2026-08-27: Hope has signed off on the eight terms** (Alex), and the
      draft banner is off the page. Nothing was invented beyond what the site already said:
      no rehoming fee, no spay/neuter deadline, no arbitration or venue clause, no
      late-pickup or abandonment terms. **Those gaps are deliberate** and are the things
      worth asking them about.

## Deployment runbook — Cloudflare Pages, email send and forward

Ordered, and split by what actually blocks what. **Email does not depend on moving the
site.** Onboarding the domain for sending and routing only adds mail records; the website
keeps resolving wherever it already does. Only step 5 changes where the site lives.

Canonical domain: **blessyourpawspuppies.com** (decided 2026-08-24). `blessyourpaws.com` is
also owned and should 301 to it. Both are already on Cloudflare nameservers.

### Before anything: fix the PATH on this machine

`nvm4w` is installed under the **`Admin-AlexHarper`** profile
(`NVM_HOME=C:\Users\Admin-AlexHarper\AppData\Local\nvm`) and `C:\nvm4w\nodejs` symlinks
into it. This account cannot read that directory, which breaks `npm` itself, not just
wrangler: every command dies with `EPERM lstat C:\Users\Admin-AlexHarper\AppData`.

There is a working Node at `C:\Program Files\nodejs`. Prepend it per shell session.

PowerShell (the usual shell here):

```powershell
$env:PATH = "C:\Program Files\nodejs;$env:PATH"
```

Git Bash:

```bash
export PATH="/c/Program Files/nodejs:$PATH"
```

Confirm with `npm --version` (expect 11.x) before going further. Verified 2026-08-24:
node v24.18.0, npm 11.16.0, resolving to `C:\Program Files\nodejs\node.exe`.

**Adding it to the User PATH does not work, and it looks like it should.** Both broken
entries live in the **Machine** PATH:

```
C:\Users\Admin-AlexHarper\AppData\Local\nvm
C:\nvm4w\nodejs
```

Windows resolves the Machine PATH before the User PATH, so a User entry is appended after
those two and loses. There are no nodejs entries in the User PATH at all.

Two real options. **Per session**, as above, which is what the commands in this runbook
assume. Or **persistently without admin**, by prepending it in the PowerShell profile
(`$PROFILE`, which did not exist as of 2026-08-24) — note that path is inside
OneDrive-synced Documents, so it follows the account to other machines. The actual fix is to
reorder or remove the stale `Admin-AlexHarper` nvm entries in the Machine PATH, which needs
the admin account.

### 1. Hosting — SUPERSEDED 2026-08-25, the host is a Worker

The site is served by the `blessyourpaws` Worker, not by Pages. See "Hosting:
Workers static assets" above for the reasoning and the verified behaviour. The
Pages project was deleted on 2026-08-25 so there is no ambiguity about which host
is live. What remains from this step is connecting Workers Builds so `main`
deploys automatically.

Historic detail, kept because the reasoning still applies to the next static site:

`wrangler pages deploy` can only do **direct upload**, and a direct-upload project
**cannot be converted to Git-connected later**. Doing it the quick way burns the project
name. So this step is manual, once:

Dashboard → Workers & Pages → Create → Pages → Connect to Git →
`alexharper24/blessyourpaws-website-repo`

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | *empty* |
| Build output directory | `/` |
| Root directory | *empty* |

No build step: `scripts/scaffold.py` is run locally and the HTML is committed. Cloudflare
only serves files.

- [x] **DONE 2026-08-25.** Project live at `blessyourpaws-website-repo.pages.dev`,
      automatic deployments from `main` enabled. Note the dashboard's "Create" button now
      defaults to the **Worker** flow; the Pages flow is a separate tab and is the one to
      use.
- [x] **`_headers` verified working.** Images and fonts return
      `cache-control: public, max-age=31536000, immutable`, HTML returns
      `max-age=0, must-revalidate`. That is the whole reason for moving: GitHub Pages
      forces `max-age=600` on everything and cannot be configured.
- [x] **`_redirects` fixed.** The first version used `404` as the status and was **silently
      ignored** — `/CLAUDE.md` kept returning HTTP 200 while the rules looked correct in
      the file. `_redirects` only supports 3xx, so they are 301s to `/` now. Verified
      against the live deployment, not assumed.

### 2. Email Sending (outbound, for the form)

```bash
npx wrangler email sending enable blessyourpawspuppies.com
```

- [ ] **BLOCKED 2026-08-25: `Unauthorized [code: 2036]`, and it is NOT an auth problem.**
      Re-authenticating was tried and changed nothing: `wrangler logout` then `login`, the
      fresh token still lists `email_sending (write)` in `whoami`, and the identical token
      reads and writes Email **Routing** on both zones without complaint. Scope granted,
      token valid, Routing fine, Sending 2036 on the account-level endpoint. That points at
      the Email Sending product not being enabled or entitled on the account rather than
      anything wrangler can fix. **Do not retry the CLI or another login** — look for
      Email Services / Email Sending in the dashboard and complete whatever onboarding it
      offers. Original note below, kept for the reasoning:

- [ ] Earlier reading of the same failure: Not zone-specific and not a typo
      — even the read-only `email sending list` at account level fails the same way, while
      every Email **Routing** call on the same token succeeds. So the OAuth token cannot
      reach the Email Sending API even though `wrangler whoami` lists `email_sending
      (write)` among its scopes. Email Sending is a newer product in open beta; the likely
      fixes are onboarding it once in the dashboard, or re-running `wrangler login` to
      re-consent the scope. Both need a browser, so this one is Alex's.
- [ ] Then verify with `npx wrangler email sending list` and confirm the domain is enabled.

**Nothing sends until this is resolved**, including the contact form: the Worker's
notification is an Email Sending call.

### 3. Email Routing (inbound, to Hope)

`info@blessyourpawspuppies.com` → Hope's Gmail. This is what makes the branded address
usable without anyone buying a mailbox.

- [x] **DONE 2026-08-25.** Routing enabled, status ready. MX now points at
      `route1/2/3.mx.cloudflare.net` and SPF is `v=spf1 include:_spf.mx.cloudflare.net
      ~all`. Nothing was displaced: the zone had no MX, SPF or apex record beforehand.
- [x] **Destination address created** and the verification email sent to Hope.
      **Her address is NOT recorded in this repo** — it lives only in the Cloudflare
      routing config. The Worker notifies `info@blessyourpawspuppies.com` and Routing
      decides where that lands, so her personal address never needs to be in a public file
      and must not be added to one.
- [x] **DONE 2026-08-26. Hope verified her address** (00:02 UTC) and the forwarding rule
      is live: `info@blessyourpawspuppies.com` → her Gmail, rule
      `6be02efe1e204b00a7a856705c17bca0`, enabled.
- [x] Catch-all is **disabled and set to drop**, which is what we want: only `info@`
      forwards and nothing else on the domain leaks through to her inbox.
- [ ] Send a test to `info@` and confirm it lands (worth doing before anyone relies on it).

Routing adds MX records for the zone. Note the consequence: **once MX points at Cloudflare,
all mail for the domain flows through Routing**, so any future mailbox has to be set up
through it.

### 4. Deploy the Worker and wire the forms

D1 is already created and wired: `form-submissions`,
`d46e2279-632b-45ad-959a-d3e515d47ae2`, schema applied. `blessyourpaws` is registered in
`SITES` in `form-backend-worker/src/index.js` with the notify address, the `from`, and
origins covering both GitHub Pages and the domain.

```bash
cd ../form-backend-worker
npx wrangler secret put TURNSTILE_SECRET     # paste the widget's secret key
npx wrangler deploy
```

- [ ] Create a Turnstile widget first and note both keys. The site key goes in the form
      markup, the secret goes in the command above. **If no secret is set the Worker skips
      spam verification entirely** and the honeypot is the only defence, which is not
      enough for a public form.
- [ ] Point both forms at the Worker URL and add the hidden `site` field. Today they still
      POST to `https://formspree.io/f/REPLACE_FORM_ID`, so **the forms do not work at all
      right now** — anything submitted is discarded silently.
- [ ] The Worker needs `site`, `name`, `email`. `message` is optional and any other field is
      folded into the notification, so the waitlist form's `line` and `timing` come through
      without a Worker change. That was a bug fixed 2026-08-24: it used to require
      `message` and would have rejected every waitlist submission with an error the visitor
      had no field to fix.
- [ ] Test both forms end to end and confirm a row lands in D1 as well as an email:
      `npx wrangler d1 execute form-submissions --remote --command "SELECT * FROM submissions"`

### 5. The cutover (the part that waits until the site is ready)

- [ ] Add `blessyourpawspuppies.com` and `www` as custom domains **in the Pages project
      before touching DNS**. Standing rule, learned the hard way on an earlier build.
- [ ] Let the certificate issue, then enable Enforce HTTPS.
- [ ] 301 `blessyourpaws.com` → `blessyourpawspuppies.com` (a redirect rule on that zone).
- [ ] **Decide the URL shape, and change it in the same commit as `BASE`.** Cloudflare
      Pages strips `.html` and issues a **308 to the extensionless form**: `/puppies.html`
      redirects to `/puppies`. GitHub Pages does the opposite — it serves `/puppies.html`
      and 404s `/puppies`. Right now the site has **669 internal links and 21 sitemap
      entries** ending in `.html`, so on Pages every internal click costs a redirect hop and
      every canonical points at a URL that redirects.

      **Do NOT "fix" this early.** Extensionless links 404 on GitHub Pages, which is still
      the live host, so the two hosts want opposite things and the change is only safe at
      the moment the domain moves. Everything is generated, so it is a `scaffold.py` change
      (link generation, canonicals and sitemap together), not 669 manual edits. Cheap to do
      once, actively harmful to do sooner.

- [ ] **Change `BASE` in `scripts/scaffold.py`** from the github.io URL to
      `https://blessyourpawspuppies.com`, bump `V`, regenerate, commit. Every canonical, the
      sitemap and every OG tag derive from it. Do this at cutover, not before: earlier, and
      the canonicals point at a domain that is not serving yet.
- [ ] Leave GitHub Pages live until the domain resolves correctly through Cloudflare. The
      rollback is repointing DNS.
- [ ] Update the GBP website field to the domain. No re-verification needed.

### 6. Launch, as a separate deliberate step

- [ ] Remove the `noindex` meta from every page and open `robots.txt`. Currently closed on
      purpose. This is the easiest thing in the whole list to forget, because by then
      everything looks finished.
- [ ] Submit the sitemap in Search Console.

## Google Business Profile — the setup sheet

Worked out 2026-08-24, ready to work from. Method and reasoning:
`.claude/guides/local-seo-aeo.md`.

**Get it as close to final as possible on the first save.** A burst of edits straight after
verification is a known re-review trigger.

### The address: enter it, never display it

- [ ] Google requires a real address to verify and there is no way around that. Enter it.
- [ ] Answer that **customers are served outside the business location**, which makes it a
      service-area business and lets the address be cleared from public display. Google
      keeps it on file; visitors see the service area instead of a pin.
- [ ] **Do this on the first save, not as a cleanup later.** A published address is copied
      within days by data aggregators that never re-check. Hiding it in Google afterwards
      does nothing about the places that already took it. This is the one step in the whole
      process that cannot be undone.
- [ ] **Never substitute a different address** — a relative's house, a virtual office, a
      mailbox store, a PO box. PO boxes and mailbox stores are disallowed outright, and a
      location the business does not operate from is a guideline violation. Suspensions are
      common and appeals are slow.
- [ ] Accept the cost knowingly: **no map pin, and a tighter ranking radius**, because
      proximity is still measured from the real address even while it is hidden. For a home
      with children in it that is the right trade.
- [ ] **Same rule on every other directory**: Bing Places, Apple Business Connect, Yelp,
      breeder directories. One of them carrying the home address makes it public AND breaks
      consistency with everywhere else. The consistency baseline is name and phone only:
      `Bless Your Paws Puppies` / `(574) 377-8023`.
- [ ] Expect **video verification**, and expect it to want a look at the premises. Worth
      warning Hope so it is not a surprise mid-call.
- [ ] Watch the entity filing separately: if Hope forms an LLC, Indiana records are public
      and a home address on them is permanently searchable. A registered agent service is
      the normal way around it. Raise it with whoever advises her; it is the same privacy
      problem arriving through a different door.

### Service area: pick for accuracy, not reach

**Listing a city does not make you rank there.** Google ranks a service-area business by
proximity between the searcher and the real (hidden) address. The service-area list is a
qualification and display signal for humans, not a ranking lever, and an over-broad area
invites scrutiny.

- [ ] Roughly a one-hour ring around Warsaw. Verify the drive times; these are approximate.
      Warsaw, Winona Lake, Leesburg, Pierceton, Claypool, Silver Lake, Mentone, Syracuse,
      Milford, North Webster, Columbia City, Nappanee, Goshen, Wabash, Rochester, Plymouth,
      **Fort Wayne** (~50 min), **South Bend** (~1 hr). Kosciusko County works as a single
      entry.
- [ ] **Do not list Chicago** (~2.5-3 hrs) or Indianapolis (~2 hrs). Google caps the list at
      20 areas and expects a plausible operating radius.
- [ ] Remember which channel does what: **the GBP reaches the local ring, the website
      reaches everyone else.** A family in Chicago finds them by searching the breed and
      then drives. That is `what-is-a-munchkin-bernedoodle.html` doing its job. Do not try to
      make the GBP do work the breed guide already does better.

### The fields

- [ ] **Name: `Bless Your Paws Puppies`**, exactly, nothing appended. Adding
      "Munchkin Bernedoodle Breeder Warsaw IN" is keyword stuffing and one of the most
      reliable ways to get suspended.
- [ ] **Primary category:** likely **"Dog breeder"**; "Pet breeder" may also exist. Take the
      most specific one **that is actually in the dropdown**. Models invent categories that
      are not in the list, so treat any AI suggestion, including the ones in this README, as
      unverified until seen in the interface.
- [ ] **Secondary categories:** only where genuinely true. For a single-breed breeder there
      may be none, and that is fine. Do not stuff.
- [ ] **Phone:** `(574) 377-8023`, character for character with the site.
- [ ] **Website:** the github.io URL now, swapped to the domain later. Changing it does not
      require re-verification.
- [ ] **Hours:** not 24/7. Hours they will genuinely answer, plus the appointment attribute.
- [ ] **Attributes:** "identifies as women-owned" is likely true and worth having, but that
      is Hope and Joy's claim to make, not ours to assume.
- [ ] **Products/services:** list services such as "Munchkin Bernedoodle puppies" and
      "Waitlist for future litters". Avoid transacting through Google: several Google
      surfaces restrict live-animal listings and where that line falls for GBP specifically
      is unconfirmed. Check before relying on it.

### Photos: the one place the standard advice is wrong here

- [ ] 20+ photos. They already have plenty: puppies, the dams, indoor family context.
- [ ] **No exterior shots of the house, the street, or anything that identifies it.** Every
      local-SEO guide says upload exterior photos. That defeats the entire reason the
      address is hidden.
- [ ] **Do not geotag.** The standard advice to upload weekly geotagged photos would encode
      their home coordinates into files they are handing out. (The advice is dubious anyway:
      the source recommending it admits Google strips EXIF on upload.)

### Description — 680 characters of 750, ready to paste

Written in the site's voice and consistent with what is already published:

> Bless Your Paws Puppies is a small, family-run breeder in northern Indiana. We are Hope
> and Joy, twin sisters, and we raise Munchkin Bernedoodles in our homes rather than in a
> kennel. Our puppies grow up underfoot, around children, other dogs, the vacuum and the
> doorbell, so they are used to the sound of a family before they ever leave us. Every puppy
> goes home with a vet exam, current vaccinations and a health record. Our dogs' health
> testing is published in full on our website, so you can read it for yourself before you
> decide. Visits are by appointment and video calls work well for families further away.
> Serving Warsaw, Winona Lake and families across northern Indiana.

- [ ] Confirm with Hope that the go-home items are accurate as stated, and that she is
      comfortable being named alongside Joy.
- [ ] **Deliberately omitted, do not add them back:** the address; the health guarantee,
      whose terms are still unconfirmed; and any coat or shedding claim.
- [ ] **Deliberately NOT claiming the Wisdom Panel in detail yet.** An earlier draft said
      the panel is published "in full, including the one variant she carries". Two reasons
      it is not in there. A description is a headline with no room for the context the
      website gives the finding, and a cold reader meets CDDY with none of the explanation
      around it. More importantly **the Cavalier sire's panel is not in hand**, CDDY needs
      only one copy to matter, and many Cavalier panels do not test FGF4 at all — so leading
      with genetic transparency invites the first question a knowledgeable buyer asks and
      the one that currently has no answer. The wording used instead says the testing is
      published without characterising a result. Note it does not say "health tested" on its
      own either, which unqualified reads as *tested clear*, the exact claim that came off
      the site.
- [ ] **Revisit when the sire's panel arrives.** If he is clear of FGF4 the stronger claim
      becomes available and is worth making. How a heritable at-risk finding is presented is
      Hope's decision, not ours.
- [ ] Whatever it ends up saying, **the description and the site have to keep agreeing.**
      Consistency between profile and site is exactly what Google and the AI assistants
      check.

### Deliberate departures (do not "fix" these back)

- [ ] **No Google Maps embed** on the site and **no address**, dropping two of the seven
      standard "consistency signals". There is no public pin for a hidden home address, and
      a service-area business shows its area rather than its location.

### After the profile is live

- [ ] Search Console, and citations on Bing Places and Apple Business Connect — address
      handled the same way as above.
- [ ] Local authority links worth having: the Kosciusko County chamber of commerce, and any
      sponsorship they would genuinely want to do anyway. **Do not buy links** — paying for
      links that pass PageRank is a link scheme under Google's spam policies, and the risk
      lands on the client, not the vendor.
