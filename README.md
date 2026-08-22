# Bless Your Paws — website

Static website for **Bless Your Paws**, the dog-breeding business of Joy Williams and
Hope Williams (twin sisters). Plain HTML/CSS/JS, no build step, targets GitHub Pages.

**Status: scoped, not yet built.** This repo currently holds the brand swatches and
the working conventions. See the pending list below.

**Character:** REPLACE THIS — write the one-sentence character statement before any
CSS is written. Direction from the client is botanical / vintage-plate: flowery,
pinks, greens, vintage.

- **Palette:** forest `#223d2c` (ink, dark bands) / sage `#7f8e79` (large text only,
  `#6d7a68` derived for small) / light sage `#a8b89e` / rose `#feb5bc` / pale pink
  `#fbc4db`. All sampled from the client's swatches in `img/brand/`. Full contrast
  matrix and the two hard rules are in [`CLAUDE.md`](CLAUDE.md).
- **Type:** REPLACE THIS — must not be Newsreader + Karla (that is Kingdom Family
  Companions' identity).
- **Archetype:** REPLACE THIS — must not be the ledger-row / narrative-scroll
  archetype (also KFC's).

## Breed lines

| Line | Owner | Status |
|---|---|---|
| Munchkin Bernedoodle (Bernedoodle × Cavalier King Charles Spaniel) | Hope | Litter of 8, born ~mid-July 2026, taking reservations |
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
python -m http.server 8155 --directory blessyourpaws-website-repo
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

- [ ] **Build option not yet chosen** (A static / B data-driven / C admin + Stripe).
      Determines the architecture. See the pricing analysis.
- [ ] **Quote not yet sent or accepted.**
- [ ] Confirm the five swatches in `img/brand/` are the final brand palette and not
      just inspiration.
- [ ] Logo: does one exist? If Harper Studio is designing the wordmark and floral
      mark, that is a separate line item from the build.

### Content from Joy and Hope

- [ ] **Bernedoodle dam's name and spelling.** Transcribed as "Mura"/"Mira" — and
      **"Mira" is already the Doberman dam on the KFC site**. Either two dogs with
      similar names or a garbled transcription. Do not write either down until Hope
      confirms.
- [ ] **Doberman sire** — name, registration, health testing. No sire is listed
      anywhere on the KFC site; only dams. Two unidentified adult photos there were
      staged but never confirmed.
- [ ] Bernedoodle sire is **Troy** (Cavalier King Charles Spaniel). Need his
      registration, health testing, and adult weight.
- [x] **Dam is a Mini Multi Gen Bernedoodle** (confirmed 2026-08-22). Pawrade said
      "Mini", Puppy Connection said "Multi Gen"; she is both. Multi-gen supports a more
      consistent curl and lower shedding than an F1 — still a per-puppy prediction, never
      a promise.
- [x] **Sire is 19 lbs** (confirmed). Puppy Connection's 18 lbs is wrong.
- [ ] Per-puppy: date of birth, go-home date, sex, colour, name, price, expected
      adult size. **8 Munchkin Bernedoodles + 3 Dobermans.**
- [ ] **Prices.** Munchkin Bernedoodle market range is $3,500–$6,500; Joy's Dobermans
      list at $2,200 on KFC. Multi-site listing at varying prices is approved, so
      confirm what *this* site shows.
- [ ] **Deposit amount and refund/transfer terms.** Never guess.
- [ ] **Health guarantee terms** and the **Purchase Agreement** — their documents,
      attorney-reviewed. Harper Studio publishes, does not write.
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
- [ ] Original socialization wording. Confirmed: raised in the home, around children, around
      many people including a Fourth of July gathering. **Not confirmed and not to be
      claimed:** vet/store outings, noise and surface desensitization, crate/leash
      starts, or any named protocol (Puppy Culture, ENS, Rule of Seven).
- [ ] Reviews/testimonials — Hope has at least one on social media. Need the wording,
      the buyer's name, and **explicit permission**. Joy's are unknown. Carry none
      over from KFC.
- [ ] Their story: how each came to breeding, in their own words. Whether the twin
      angle is part of the brand.
- [ ] Whether Joy has rights to reuse the Doberman puppy photos, which came off
      Amber's Wix site during the KFC build.
- [ ] Any faith element. Do not assume either way — KFC's verse band is not a
      template.
- [x] **Photos pulled 2026-08-22.** 78 full-resolution originals for all seven Munchkin
      Bernedoodles, from the Puppy Connection listings with Hope's confirmation that the
      family owns the rights. Originals in gitignored `source-photos/puppy-connection/`;
      web JPEGs at 1400px in `img/puppies/` plus a 240/600/1100 WebP set in `img/r/`.
      Counts: joshua 10, eden 11, havilah 13, jordan 10, caleb 9, shiloh 11, jericho 14.
      Spot-verified that filing matches recorded colour.
- [ ] Doberman photos — still to source. Joy's three are on the Kingdom site but those
      are Amber's files; ask Joy for her own.
- [ ] Parent photos (sire and dam) — not yet pulled.
- [ ] Confirm both are comfortable with faces and first names on a public site.

### Technical

- [ ] Contact form backend: Formspree ID, or the shared `form-backend-worker`.
- [ ] Stripe account (Hope's). **Stripe does not require an LLC** — sole proprietors
      can open an account with an SSN. Whether she *should* form one is a liability
      and tax question for an attorney or CPA, not for this project.
- [ ] Branded email — Cloudflare Email Routing forwarding is free.
- [ ] Domain (~$12–20/yr, theirs). Set the custom domain in Pages settings *before*
      moving DNS; enable Enforce HTTPS after the cert issues.
- [ ] Publish in **draft mode** (noindex on every page + closed robots.txt) so it is
      shareable before launch.
- [ ] GitHub repo + first push.
- [ ] Google Business Profile + Search Console after launch.
- [ ] Phase 2 only: Cloudflare Worker + D1 admin, two logins, photo upload, and the
      **Stripe webhook that auto-marks a puppy reserved when a deposit clears**.
