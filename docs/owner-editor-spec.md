---
doc: owner-editor-spec
site: blessyourpaws-website-repo
written: 2026-10-01
status: spec, awaiting Alex's decisions D1 to D6 before Phase 0
model: teapup-website-repo/admin (single-breeder editor, D1 + R2 + Access + publish-to-commit)
skill: breeder-site-backend
phases:
  - {id: P0, name: "Data out of the generator", status: not-started}
  - {id: P1, name: "Schema, seed and round-trip gate", status: not-started}
  - {id: P2, name: "Editor Worker, sign-in and screens", status: not-started}
  - {id: P3, name: "Publish pipeline and CI build", status: not-started}
  - {id: P4, name: "Sign-in page across the Cloudflare account", status: not-started}
  - {id: P5, name: "Handover to Hope and Joy", status: not-started}
decisions:
  - {id: D1, blocked_on: alex, item: "Editor host. Recommended admin.blessyourpawspuppies.com as its own Worker, over the /admin route already reserved on the site Worker"}
  - {id: D2, blocked_on: alex, item: "Sign-in page. Recommended instant auth (Google only) on every Access app, with a neutral Harper Studio page as the shared fallback"}
  - {id: D3, blocked_on: alex, item: "Who signs in, and with which Google account. Hope, Joy, or both"}
  - {id: D4, blocked_on: alex, item: "Stripe. Recommended pasted Payment Links on the Settings screen, over the auto-reserve webhook the original part two described"}
  - {id: D5, blocked_on: alex, item: "Adults screen scope. Recommended own dogs and outside studs on one screen, with health records as uploaded PDFs"}
  - {id: D6, blocked_on: alex, item: "Can a puppy be deleted. Recommended no, only retired with its litter"}
excluded:
  - "Creating or editing breeds. The breed is fixed to Munchkin Bernedoodle and SHOW_DOBERMANS stays a generator flag"
  - "Buyer data of any kind, meaning who reserved or adopted a puppy, contact details or payments"
  - "Legal pages. The health guarantee and purchase agreement stay verbatim in the generator"
  - "The hand-written guide pages, which stay in scaffold.py"
  - "The Team screen and the two-business switcher from the Teapup editor"
---

# Bless Your Paws owner editor, build spec

Hope and Joy get a signed-in editor where they manage puppies, litters, the parents, reviews and
the prices themselves, and pressing Publish updates blessyourpawspuppies.com in about a minute.
It is the Teapup and Sweet Puppy Paws editor trimmed to one business, with breed creation
left out. The architecture is the one in the `breeder-site-backend` skill and is not
redesigned here.

## Where Bless Your Paws differs from Teapup

Teapup's generator already read its content from `data/*.json`, because that content came out
of a Wix export. Bless Your Paws does not have that layer. Every puppy, the litter dates, the
price, the parents and the review are Python literals in `scripts/scaffold.py`, and much of it
assumes there is exactly one litter. That is why Phase 0 exists and why it is the largest phase.

| Hardcoded today | Where it goes |
|---|---|
| `MUNCHKINS` tuples (slug, name, sex, color, note) | `data/puppies.json`, each with a `litter` id |
| `ADOPTED`, `RESERVED` sets | a `status` field on each puppy, as available, reserved or adopted |
| `M_BORN`, `M_HOME`, `M_SIZE` (single litter) | `data/litters.json`, per litter |
| `M_PRICE`, `M_PRICE_CASH`, `DEPOSIT`, `IN_TAX_RATE` | `data/settings.json`, with the litter able to override the price |
| The three `buy.stripe.com` links, shared by every puppy | `data/settings.json` |
| `PRIMARY`, `PAGE_FROM`, `img/photo-counts.json` | photo order on each puppy, with a card photo and a page cover |
| Troy and Bip Finch in prose (29 mentions of Troy) | `data/adults.json`, and litter pages naming the dam and sire from it |
| The one review on `reviews.html` | `data/reviews.json` |
| `DOBERMANS`, `SHOW_DOBERMANS` | stays in the generator, untouched |

## Phase 0, data out of the generator

There's no editor in this phase. Move the table above into `data/*.json` and make `scaffold.py` read it.

- The gate is byte-identical output. Build every page before and after, and require the diff of
  all generated HTML, `sitemap.xml` and `style.css` to be empty.
- Generalize to more than one litter. Each litter gets its own section on `puppies.html` and
  names its own dam and sire, `M_TOTAL` and `M_AVAILABLE` become per-litter derivations,
  and the "Available now" eyebrow derives across all litters. Prove it with a second test
  litter that is built locally and never committed.
- A litter whose puppies are all adopted retires. Its puppy pages 301 to `/puppies` through
  `_redirects`, its pages and sitemap entries come out, and its photographs stay in the gallery.
  This closes the `breeder-puppy-301` item in `_claude-state.md`.
- Guide pages stop pointing at puppy photographs. Ten `img_tag` calls on the guide and
  reviews pages name a puppy's photo directly, and a puppy photo the editor later
  reorders or retires would drop out from under them and fail CI on an owner's publish. They
  move to copies under `img/guides/`, listed in a manifest the exporter does not own, which
  is the Teapup `guide-photos.json` pattern.
- Photos get the Teapup encoder. `prep_images.py` works from `source-photos/`, which is
  gitignored and so absent in CI. Port `make_images.py`, which carries built outputs forward
  and encodes only new files from `uploads/`.

## Phase 1, schema, seed and round-trip gate

Fork `teapup-website-repo/admin/` into `blessyourpaws-website-repo/admin/` and trim it.

- The tables are `people`, `adults`, `litters`, `puppies`, `reviews`, `settings`, `uploads`,
  `audit` and `publishes`. Drop `breeds`, `team`, `dogs` (folded into `adults` for a single
  breeder) and every `businesses.mjs` branch.
- The schema is written from the Phase 0 files, not from the domain, so the export reproduces
  them byte for byte, including key order and absent-versus-empty keys.
- There's no buyer data. A puppy is available, reserved or adopted, and who reserved it is
  not stored.
- Every editable row carries `version`, because two owners can have the same puppy open.
- `node admin/roundtrip.mjs` seeds a local database from the files, exports it and diffs it
  against them. It has to pass before anything is deployed.
- A new D1 database `blessyourpaws` and a new R2 bucket. Nothing is shared with the Teapup
  database, because these are separate clients.

## Phase 2, editor Worker, sign-in and screens

The editor is a separate Worker. Under D1 it would be `admin.blessyourpawspuppies.com`, a custom domain on the
zone the site already uses. It gets its own Cloudflare Access application, with a policy naming
Hope's and Joy's addresses, plus the `people` table invitation, and both checks must pass. Identity
fails closed, the cookie is verified against `ACCESS_TEAM_DOMAIN` and `ACCESS_AUD`, and there's
no sign-up.

| Screen | What Hope and Joy do there |
|---|---|
| Puppies | Tap a puppy to change its status, edit its name, sex, color and note, add, reorder and remove photos, and pick the card photo and the page cover |
| Litters | Add a litter, set its dam, sire, birth date, go-home date, expected size and optional price, and add puppies to it |
| Adults | Add and edit the parents, both their own dogs and outside studs such as Bip Finch, with weight, color, birth date, registration, photos and health-record PDFs |
| Reviews | Add a review word for word with the family's first name and the puppy, and reorder or hide reviews |
| Prices | Set the card price, the cash price and the deposit, and paste the three Stripe links. The tax and the cash discount are derived and are shown but can't be edited |
| Publish | See what changed since the last publish, then publish it |
| History | See every publish and who made it |
| People | Alex invites and removes people. Hope and Joy don't see this screen |

What Hope and Joy can't do is just as deliberate as what they can.

- They can't create breeds or edit the breed guides, the legal pages, the contact details or
  the delivery section, because all of those stay in the generator.
- Health facts on an adult are entered by the owner and shown as entered. Nothing in the
  editor states a result without a document, which follows the repo rule after the Bip Finch
  CDDY retraction.
- Every field is 16px on a phone, the drawer is sized with `100dvh`, and photo writes hand the
  new `version` back to the open form. Those are the three Teapup bugs the skill records, and
  each is fixed in the fork before the first deploy.

## Phase 3, publish pipeline and CI build

- Publish commits `data/*.json` plus any new photographs under `uploads/` to `main` as one
  commit, through a fine-grained GitHub token scoped to this repo alone.
- The Workers Builds build command changes from empty to `bash scripts/ci-build.sh`, which
  installs Pillow, runs the image encoder and runs `scaffold.py`. Without it a publish reaches
  GitHub and never reaches the site, which is exactly how Teapup's first publish failed on
  2026-09-12.
- `site-checks` runs on the publish commit as it does on every push.
- From the first publish the database owns the files in `data/`. Changes Alex makes from then on
  go through the editor or `admin/migrations/`, and a migration is finished only when a
  `SELECT` against the remote D1 shows it.

## Phase 4, the sign-in page across the Cloudflare account

**Why another app shows Teapup branding.** Alex's private apps, the Teapup editor and this editor
all sit behind Cloudflare Access in the same Zero Trust organization (`shy-truth-7b36`). The
login page's logo, background, header text and message are set once for the whole
organization, and Cloudflare's documentation says a change applies "for all of your Access
applications". There is no per-application login page. The only part that differs per app is
the heading, "Log in to <application name>". So when the page was branded with the Teapup and
Sweet Puppy Paws lockup on 2026-09-12, every other app picked it up too, and so would this
editor.

The fix, recommended under D2, has two parts.

- **Instant auth on every Access application.** When an application allows exactly one login
  method, Cloudflare can skip its own page and send the user straight to Google. Set Google as
  the only method and turn instant auth on for every application, including the Teapup editor and the Bless
  Your Paws editor. Nobody then sees the shared page in normal use. Google's account picker
  names `shy-truth-7b36.cloudflareaccess.com`, which is neutral, and each editor shows its own
  brand once signed in.
- **A neutral shared page as the fallback.** Anyone who reaches the shared page, through a
  second login method or a direct link, sees a Harper Studio logo and a neutral message rather than
  one client's brand. Each application is named for its business, so the heading still reads
  "Log in to administer Bless Your Paws" on this one.

The dashboard needs checking before this is built. Confirm which login methods each of the three
applications allows today, because instant auth only applies when there is exactly one.
Moving each client to its own Cloudflare account would also give each one its own page, and
it's the cleaner answer if a client ever takes ownership of their account, but that's more
than this problem needs.

## Phase 5, handover

- Invite Hope and Joy in both places, the Access policy and `node admin/invite.mjs add`.
- Write a one-page guide around the daily jobs, which are marking a puppy reserved or adopted, adding
  photos, and starting a new litter.
- Hope makes the first real publish herself while Alex watches the live site change.

## Decisions for Alex

- **D1, editor host.** The site Worker already reserves `/admin` and `/api/*`, and because this
  site is on a real zone a path-scoped Access app would work there. A separate Worker on
  `admin.blessyourpawspuppies.com` is still recommended, because a mistake in the editor then
  can't take the public site down and the Teapup code ports unchanged.
- **D2, sign-in page.** Instant auth plus a neutral fallback, as above, or keep a branded shared
  page and accept that every app shows it.
- **D3, who signs in.** Hope, Joy or both, and which Google account each uses. Instant auth
  needs each of them to sign in with Google.
- **D4, Stripe.** Payment Links have a fixed amount, so a price change in the editor needs new
  links made in Stripe and pasted in. The Prices screen refuses to publish a changed price
  until the matching link has changed too. The original part-two proposal described a puppy
  reserving itself when a deposit clears, which needs a Stripe webhook and a restricted key.
  It's left out of this spec unless you want it back.
- **D5, adults.** Own dogs and outside studs on one screen, with health records as PDFs, or own
  dogs only with studs kept in the generator.
- **D6, deleting puppies.** Recommended no. A puppy stays until its litter retires, so the
  litter always reads as a whole.
