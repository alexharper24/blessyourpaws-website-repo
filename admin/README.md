# Bless Your Paws owner editor

Hope and Joy keep the puppies, litters, parents and reviews current here, and Publish updates
blessyourpawspuppies.com about two minutes later. It runs at `https://admin.blessyourpawspuppies.com`
in the Bless Your Paws Puppies Cloudflare account, behind Cloudflare Access.

## How it fits together

| Piece | Where |
|---|---|
| Sign-in | Access application "Bless Your Paws editor", email code only, team `blessyourpaws` |
| Who may edit | Access policy "Bless Your Paws editors" AND the `people` table. Both are needed |
| Content | D1 `blessyourpaws` (`c5b7075d-e7ef-4c75-8cc6-60769532f38a`), table `records`, one row per record |
| Photos | Resized in the browser to 2400px, held in R2 `blessyourpaws-photos` until published |
| Publish | One commit to `main` with `data/*.json` and any new `uploads/` photos |
| Site build | Workers Builds on the `blessyourpaws` Worker runs `bash scripts/ci-build.sh` |

## Rules

- **The database owns `data/puppies.json`, `litters.json`, `adults.json` and `reviews.json`.** Every
  publish writes each file whole. Change content in the editor. Where there is no screen, change
  the live D1 with a SQL file and confirm it with a `SELECT`, then bring the file into step.
- **No buyer data.** A puppy is available, reserved or adopted, and nothing records who.
- **No deletes.** Photos can be hidden from a puppy's page, reviews can be hidden, litters move to
  past litters. Undo on the Publish screen puts one record back to the site's version.
- **Identity fails closed.** With no Access audience configured, every request is refused.
- **Prices, the deposit, Stripe links, the Dobermans and legal pages stay in `scripts/scaffold.py`.**

## Commands

Run from this folder. Prepend the working Node first in Git Bash:
`export PATH="/c/Program Files/nodejs:$PATH"`.

| Task | Command |
|---|---|
| Round-trip gate | `node roundtrip.mjs` |
| Local editor | `preview_start byp-editor` (root launch.json), after `node setup-db.mjs --local` |
| Simulate a publish | `node local-export.mjs <scratch copy of the repo>`, then run the build there |
| Deploy the editor | `npx -y wrangler deploy` |
| Add the publish token | `npx -y wrangler secret put GITHUB_TOKEN` (Alex only) |

WARNING: `node setup-db.mjs --remote` seeds the live database from the files. It refuses when the
live database already has records, and must never be forced once an owner has saved anything.

## Pending

- [ ] Alex adds `GITHUB_TOKEN`, a fine-grained token for this repository only, Contents read and write.
- [ ] Alex signs in once and makes a test publish.
- [x] Hope (`hpwtwin1@gmail.com`) invited 2026-10-16, in the people table and the Access policy. Not yet told.
- [ ] Invite Joy when Alex supplies her address, in the People screen and in the Access policy.
