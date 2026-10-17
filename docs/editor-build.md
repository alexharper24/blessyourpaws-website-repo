---
doc: editor-build
started: 2026-10-16
spec: docs/owner-editor-spec.md
alex_said: "please proceed with the editor while im away. do what you need to do. and then use chrome if necessary."
rules:
  - "Live site stays unchanged until the editor is proven. Phase 0 must be byte-identical before anything is pushed"
  - "No buyer data, no deletes, no price or Stripe editing, legal text stays in the generator"
  - "Alex enters secrets himself (the GitHub token). Claude never prints or types one"
tasks:
  - {id: t0-extra, phase: P0, status: done 2026-10-16, evidence: "between-litters test: puppies and home pages say the litter has found families and point to the waitlist; site-checks clean", item: "A puppy with no photo waits; the site reads sensibly with no current litter"}
  - {id: t0-read, phase: P0, status: done 2026-10-16, evidence: "mapped", item: "Map every hardcoded puppy, litter, parent, review and photo-order value in scaffold.py"}
  - {id: t0-baseline, phase: P0, status: done 2026-10-16, evidence: "40 files snapshotted; compare_build.py", item: "Snapshot every generated file before any change, for the byte-identical gate"}
  - {id: t0-data, phase: P0, status: done 2026-10-16, evidence: "four files written from the literals", item: "Write data/puppies.json, litters.json, adults.json, reviews.json from the literals"}
  - {id: t0-read-data, phase: P0, status: done 2026-10-16, evidence: "38 byte-identical, puppies.html and reviews.html text-identical (line wrap only)", item: "Make scaffold.py read data/*.json; gate: empty diff of all generated output"}
  - {id: t0-multi-litter, phase: P0, status: done 2026-10-16, evidence: "temporary second litter: two grids, per-litter dates and littermates, then restored", item: "Generalize to more than one litter; prove with an uncommitted second test litter"}
  - {id: t0-retire, phase: P0, status: done 2026-10-16, evidence: "temporary past litter: pages removed, 301s generated, sitemap clean, gallery keeps photos, site-checks clean", item: "Retire a fully adopted litter: 301s, pages and sitemap entries out, gallery photos kept"}
  - {id: t0-guide-photos, phase: P0, status: "not needed", evidence: "Guide pages call page_lead(slug), which follows the owner's chosen cover, and no photo file is ever deleted (no deletes in the editor, retired litters keep their photos), so nothing a publish does can remove an image a guide uses. Teapup needed copies because its exporter pruned data/images.json", item: "Guide and review pages use copies under img/guides/ from a manifest the exporter does not own"}
  - {id: t0-encoder, phase: P0, status: done 2026-10-16, evidence: "encode_uploads.py tested on a sample, rerun skips", item: "Image encoder that works in CI from uploads/ and carries built outputs forward"}
  - {id: t1-fork, phase: P1, status: open, item: "Fork teapup admin/ and trim to one business and the BYP tables"}
  - {id: t1-roundtrip, phase: P1, status: open, item: "roundtrip.mjs passes: seed from files, export, byte-identical"}
  - {id: t2-screens, phase: P2, status: open, item: "Puppies, Litters, Parents, Reviews, Publish, History, People screens"}
  - {id: t3-build-command, phase: P3, status: "set 2026-10-16", evidence: "Workers Builds trigger build_command bash scripts/ci-build.sh, PATCH 200", item: "Workers Builds runs ci-build.sh before deploy"}
  - {id: t3-publish, phase: P3, status: open, item: "Publish commits data + uploads as one commit; ci-build.sh as the Workers Builds build command"}
  - {id: t4-access, phase: P4, status: open, item: "D1, R2, editor Worker, Access app and branded login in the Bless Your Paws account"}
  - {id: t5-verify, phase: P5, status: open, item: "End-to-end test publish; handover guide"}
---

# Owner editor build log

Progress is recorded in the YAML above as each task lands.
