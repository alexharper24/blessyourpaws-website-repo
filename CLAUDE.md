# CLAUDE.md — Bless Your Paws

Repo-specific conventions. Read alongside the root `C:\Git_Repos\CLAUDE.md` and
`.claude/guides/static-sites.md`.

## What this is

Static website for **Bless Your Paws**, the dog-breeding business of **Joy Williams
and Hope Williams** (twin sisters, sisters-in-law to Alex via Mary). Two breed lines
at launch:

- **Munchkin Bernedoodles** (Hope) — Bernedoodle × Cavalier King Charles Spaniel
- **Doberman Pinschers** (Joy) — co-owned with Amber

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

**The logo ink is navy `#00183c`, not forest `#223d2c`.** The supplied swatches and
the supplied logo are two different brand directions, and mixing navy ink with green
ink on one site reads as a mistake. **This is Hope's decision, not ours.** Three
workable resolutions:

1. **Recolor the navy to `--forest`** so the logo agrees with the swatches. The mono
   version recolors cleanly; on the full-colour lockups replace the navy RGB and keep
   alpha (never re-trace). The illustrated puppy's fur stays as-is — it is realistic
   colour, not brand colour.
2. **Keep navy as the ink** and demote the greens to supporting tones. Navy is a fine
   ink at 15.16:1 on white. But Hope explicitly asked for greens, so do not choose
   this for her.
3. **Navy ink plus sage as the secondary accent.** Works, and keeps both.

Until she decides, do not build the header.

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
python -m http.server 8155 --directory blessyourpaws-website-repo
```

Or `preview_start({name: "blessyourpaws"})` from the root launch.json.

Before committing: `python check_site.py blessyourpaws-website-repo` from the
`site-checks` repo.
