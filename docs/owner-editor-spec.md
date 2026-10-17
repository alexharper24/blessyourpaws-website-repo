---
doc: owner-editor-spec
site: blessyourpaws-website-repo
written: 2026-10-01
revised: 2026-10-01, with Alex's answers on sign-in, Stripe, parents and deleting
status: spec, nothing blocking. Phase 0 can start; sign-in is settled as Cloudflare Access in the Bless Your Paws account
model: teapup-website-repo/admin (single-breeder editor, D1 + R2 + publish-to-commit)
skill: breeder-site-backend
phases:
  - {id: P0, name: "Data out of the generator", status: not-started}
  - {id: P1, name: "Schema, seed and round-trip gate", status: not-started}
  - {id: P2, name: "Editor Worker, sign-in and screens", status: not-started}
  - {id: P3, name: "Publish pipeline and CI build", status: not-started}
  - {id: P4, name: "A separate sign-in for every project", status: "account and Zero Trust done 2026-10-16; the Access application, policy and branded login page come with Phase 2"}
  - {id: P5, name: "Handover to Hope and Joy", status: not-started}
decisions:
  - {id: D1, blocked_on: none, item: "Editor host. Defaulting to admin.blessyourpawspuppies.com as its own Worker, over the /admin route reserved on the site Worker, unless Alex says otherwise"}
closed:
  - {id: D2, closed: 2026-10-16, evidence: "Account per project. Bless Your Paws moved to its own Cloudflare account (fed7bd3e491a8d6dbae0f421eeb62768) on 2026-10-16 with Zero Trust Free on and team blessyourpaws (blessyourpaws.cloudflareaccess.com). See docs/account-move.md"}
  - {id: D3, closed: 2026-10-01, evidence: "Alex: Hope and Joy both sign in. Hope's address is the one already on file for the business, Joy's comes from Alex at handover"}
  - {id: D4, closed: 2026-10-01, evidence: "Alex: hold Stripe and price changes for a later rebuild where the editor and Stripe talk to each other. New puppies take the normal price"}
  - {id: D5, closed: 2026-10-01, evidence: "Alex: the parents stay as they are on the pages today, and the editor edits that information where it sits"}
  - {id: D6, closed: 2026-10-01, evidence: "Alex: no deleting puppies or photos. Owners mark a puppy adopted and the site updates the way the generator does now"}
  - {id: shared-sign-in, closed: 2026-10-01, evidence: "Alex: every project gets its own authentication and the projects stay separate, so one sign-in page shared across projects is ruled out"}
excluded:
  - "Creating or editing breeds. The breed is fixed to Munchkin Bernedoodle and SHOW_DOBERMANS stays a generator flag"
  - "Prices, the deposit and the Stripe links. They stay in the generator until a later rebuild connects the editor to Stripe"
  - "Deleting a puppy or a photo"
  - "Adding new parents or restructuring the parents page. The editor edits the parents already shown"
  - "Buyer data of any kind, meaning who reserved or adopted a puppy, contact details or payments"
  - "Legal pages. The health guarantee and purchase agreement stay verbatim in the generator"
  - "The hand-written guide pages, which stay in scaffold.py"
  - "The Team screen and the two-business switcher from the Teapup editor"
---

# Bless Your Paws owner editor, build spec

Hope and Joy get their own signed-in editor where they keep the puppies, litters, parents and
reviews current, and pressing Publish updates blessyourpawspuppies.com in about a minute. It is
the Teapup and Sweet Puppy Paws editor trimmed to one business. It leaves out breed creation,
price changes and deleting, and it has a sign-in of its own that no other project shares. The
architecture is the one in the `breeder-site-backend` skill and is not redesigned here.

## Where Bless Your Paws differs from Teapup

Teapup's generator already read its content from `data/*.json`, because that content came out
of a Wix export. Bless Your Paws does not have that layer. Every puppy, the litter dates, the
parents and the review are Python literals in `scripts/scaffold.py`, and much of it assumes
there is exactly one litter. That is why Phase 0 exists and why it is the largest phase.

| Hardcoded today | Where it goes |
|---|---|
| `MUNCHKINS` tuples (slug, name, sex, color, note) | `data/puppies.json`, each with a `litter` id |
| `ADOPTED`, `RESERVED` sets | a `status` field on each puppy, as available, reserved or adopted |
| `M_BORN`, `M_HOME`, `M_SIZE` (single litter) | `data/litters.json`, per litter |
| `PRIMARY`, `PAGE_FROM`, `img/photo-counts.json` | photo order on each puppy, with a card photo and a page cover |
| The parents' facts as they appear on the pages today | `data/adults.json`, one record per parent already shown, same fields and same layout |
| The one review on `reviews.html` | `data/reviews.json` |
| `M_PRICE`, `M_PRICE_CASH`, `DEPOSIT`, tax, the Stripe links | stays in the generator. Every puppy uses the normal price |
| `DOBERMANS`, `SHOW_DOBERMANS` | stays in the generator, untouched |

## Phase 0, data out of the generator

There's no editor in this phase. Move the table above into `data/*.json` and make `scaffold.py` read it.

- The gate is byte-identical output. Build every page before and after, and require the diff of
  all generated HTML, `sitemap.xml` and `style.css` to be empty.
- Generalize to more than one litter. Each litter gets its own section on `puppies.html` and
  names its own dam and sire from the existing parents, `M_TOTAL` and `M_AVAILABLE` become
  per-litter derivations, and the "Available now" eyebrow derives across all litters. Prove it
  with a second test litter that is built locally and never committed.
- A litter whose puppies are all adopted retires. Its puppy pages 301 to `/puppies` through
  `_redirects`, its pages and sitemap entries come out, and its photographs stay in the gallery.
  This closes the `breeder-puppy-301` item in `_claude-state.md`. Retiring is a build rule and not
  a delete, so nothing in the database is removed.
- Guide pages stop pointing at puppy photographs. Ten `img_tag` calls on the guide and
  reviews pages name a puppy's photo directly, and a puppy photo the editor later reorders or
  hides would drop out from under them and fail CI on an owner's publish. They move to copies
  under `img/guides/`, listed in a manifest the exporter does not own, which is the Teapup
  `guide-photos.json` pattern.
- Photos get the Teapup encoder. `prep_images.py` works from `source-photos/`, which is
  gitignored and so absent in CI. Port `make_images.py`, which carries built outputs forward
  and encodes only new files from `uploads/`.

## Phase 1, schema, seed and round-trip gate

Fork `teapup-website-repo/admin/` into `blessyourpaws-website-repo/admin/` and trim it.

- The tables are `people`, `adults`, `litters`, `puppies`, `reviews`, `uploads`, `audit` and
  `publishes`. Drop `breeds`, `team`, `dogs`, `settings` and every `businesses.mjs` branch.
- The schema is written from the Phase 0 files, not from the domain, so the export reproduces
  them byte for byte, including key order and absent-versus-empty keys.
- There's no buyer data. A puppy is available, reserved or adopted, and who reserved it is
  not stored.
- Nothing has a delete route. Puppies, photos and reviews can be hidden or reordered but are
  never removed, so a mistaken tap is always recoverable.
- Every editable row carries `version`, because Hope and Joy can have the same puppy open.
- `node admin/roundtrip.mjs` seeds a local database from the files, exports it and diffs it
  against them. It has to pass before anything is deployed.
- A new D1 database and R2 bucket for Bless Your Paws alone. Nothing is shared with any other
  project.

## Phase 2, editor Worker and screens

The editor is its own Worker at `admin.blessyourpawspuppies.com`, separate from the public site,
so a mistake in the editor can't take the site down. Sign-in is covered in Phase 4. Whichever way
D2 goes, the Worker also checks the `people` table, identity fails closed, and there's no sign-up.

| Screen | What Hope and Joy do there |
|---|---|
| Puppies | Tap a puppy to mark it available, reserved or adopted, edit its name, sex, color and note, add and reorder photos, and pick the card photo and the page cover |
| Litters | Add a litter, set its dam and sire from the existing parents, its birth date, go-home date and expected size, and add puppies to it at the normal price |
| Parents | Edit the details and photos of each parent already on the site, in the same fields the parents page shows today |
| Reviews | Add a review word for word with the family's first name and the puppy, and reorder or hide reviews |
| Publish | See what changed since the last publish, then publish it |
| History | See every publish and who made it |
| People | Alex invites and removes people. Hope and Joy don't see this screen |

**Send health guarantee (added 2026-10-15).** Each puppy carries a "Send health guarantee"
button once it is reserved or adopted, with the same copy, text and email actions the hidden
`guarantee-links.html` page has today. The editor holds the link only. It never records who
signed or when, because that is buyer data and this spec keeps buyer data out of the editor;
the signed copies stay in Hope's email. A per-puppy "signed" tick would change that rule and
is Alex's call when this phase starts. Once the editor ships, `guarantee-links.html` retires.

Marking a puppy adopted or reserved does exactly what the generator does today. The price comes
off the card, the badge changes, the deposit buttons go, the puppy leaves the application's list
and the available count, and the search description drops the price.

What Hope and Joy can't do is just as deliberate as what they can.

- They can't change prices or Stripe links, delete a puppy or a photo, add a parent, create a
  breed, or edit the guides, the legal pages, the contact details or the delivery section.
- Health facts on a parent are shown as entered. Nothing in the editor states a result without a
  document, which follows the repo rule after the Bip Finch CDDY retraction.
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

## Phase 4, a separate sign-in for every project

Every project gets its own sign-in, branded for that business, and no project shares a
sign-in page or an account with another (Alex, 2026-10-01). Today they can't be separate,
because Cloudflare gives one sign-in page to a whole account and every app on it shows that
page's logo. That's why Alex's private apps picked up the Teapup and Sweet Puppy Paws logo on
2026-09-12.

There are two ways to get a separate sign-in, and D2 picks one. Both offer Google sign-in and an
emailed code.

- **A Cloudflare account per project.** Bless Your Paws gets its own Cloudflare account, holding
  its domain, the site, the editor, its database and its own sign-in page. Cloudflare keeps
  running the sign-in, as it does for Teapup now. The cost is a one-time move of the domain and
  the site Worker into the new account. Teapup, Sweet Puppy Paws and the private apps each move
  to their own account too, on whatever schedule Alex chooses.
- **Each editor runs its own sign-in page.** Cloudflare Access comes off and the editor shows its
  own branded page with a Google button and an emailed code. Nothing moves between accounts. The
  cost is that the sign-in security becomes code we write and maintain, meaning sessions, code
  expiry and lockout, where today Cloudflare carries all of it.

The recommendation is the account per project. It keeps the sign-in that is already proven on
Teapup, and it separates the projects at every level rather than only at the sign-in page.

## Phase 5, handover

- Invite Hope with the address already on file for the business, and Joy with the address Alex
  supplies at handover.
- Write a one-page guide around the daily jobs, which are marking a puppy reserved or adopted,
  adding photos, and starting a new litter.
- Hope makes the first real publish herself while Alex watches the live site change.

## Later, not in this build

A rebuild where the editor and Stripe talk to each other, so a price change or a deposit is
handled in one place (Alex, 2026-10-01). Until then the prices and Stripe links stay in the
generator, and Alex changes them on request.
