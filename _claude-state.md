---
name: blessyourpaws-website-repo
description: Project state for Bless Your Paws Puppies, read first every session
kind: breeder-site
updated: 2026-09-23
gate: G5
review_url: ""
live_url: "https://blessyourpawspuppies.com"
open:
  # G2 Build, still owed by a live site
  - {id: g2-schema-depth, gate: G2, blocked_on: claude, item: "14 of 23 pages carry no structured data at all. Only index.html (LocalBusiness), the 8 puppy pages (Product, Offer, BreadcrumbList) and the breed guide (FAQPage) have any. BreadcrumbList is missing on 15 pages"}
  - {id: g2-schema-money, gate: G2, blocked_on: claude, item: "The two money pages with no schema are puppies.html and parents.html, which for a breeder are the available-puppies and parents pages. The breed guide has FAQPage but no BreadcrumbList"}
  - {id: g2-desc-long, gate: G2, blocked_on: claude, item: "Two meta descriptions over 155 characters: puppies.html at 176 and privacy-policy.html at 158"}
  - {id: g2-heading-skip, gate: G2, blocked_on: claude, item: "17 pages skip from H1 straight to H3. On a puppy page the Reserve and About blocks are H3 while later sections are H2, so the outline reads out of order"}
  # G4 Launch
  - {id: g4-www-redirect, gate: G4, blocked_on: alex, item: "www to apex redirect rule not in place on the zone. Both hostnames resolve and every page canonical points at the apex, so Google will consolidate on its own, but the rule makes it explicit"}
  - {id: g4-bing, gate: G4, blocked_on: alex, item: "Bing Webmaster Tools not set up. Google Search Console is verified with the sitemap submitted"}
  # G5 Grow
  - {id: g5-gbp-sameas, gate: G5, blocked_on: claude, item: "Google Business Profile is verified but is not linked from the homepage LocalBusiness sameAs. Needs the Knowledge Graph ID from Alex"}
  - {id: g5-gbp-complete, gate: G5, blocked_on: alex, item: "Profile completeness not confirmed since verification: address hidden, service area set to the one-hour ring, category, hours, photos without geotags"}
  - {id: g5-reviews, gate: G5, blocked_on: client, item: "No review habit established and the site has no reviews to mark up. aggregateRating must stay absent until real reviews exist"}
  - {id: g5-monthly, gate: G5, blocked_on: alex, item: "Monthly Search Console and profile check not running, and no content cluster in progress"}
  - {id: g5-ai-check, gate: G5, blocked_on: alex, item: "AI visibility check never run. Ask the buying questions in ChatGPT, Perplexity and Gemini and record who gets named"}
  # Breeder-specific, from the lifecycle business-type table
  - {id: breeder-puppy-301, gate: G5, blocked_on: alex, item: "No plan for retired puppy URLs. Eight puppy pages will go stale within about ten weeks and each needs a 301 when it does. _redirects currently holds only the our-dogs rule"}
  - {id: breeder-breed-links, gate: G5, blocked_on: claude, item: "The breed guide is the page that accumulates ranking value between litters and it has only 4 inbound body links, against 24 to puppies.html and 14 to parents.html"}
closed:
  - {id: g2-pages, closed: 2026-09-23, evidence: "Breed guide, available puppies and parents all exist as their own pages, which is the breeder money-page set"}
  - {id: g2-onpage-nap, closed: 2026-09-23, evidence: "Name, service area and phone as real text with a tel: link on all 23 pages, verified by grep"}
  - {id: g2-canonical-root, closed: 2026-09-23, evidence: "Homepage canonical is https://blessyourpawspuppies.com/ not /index.html, the trap the lifecycle names"}
  - {id: g2-house, closed: 2026-09-23, evidence: "Light-mode lock, ?v= cache-busting, lowercase relative paths, favicon, 404 page, sitemap and robots all present"}
  - {id: g2-checks, closed: 2026-09-23, evidence: "site-checks clean and audit.py reports 0 broken links, 0 missing images, 0 pages without exactly one H1"}
  - {id: g2-images, closed: 2026-09-23, evidence: "WebP with srcset and sizes throughout, source-photos gitignored, 100 decorative images correctly carry alt=\"\" and none are missing the attribute"}
  - {id: g3-noindex, closed: 2026-09-23, evidence: "n/a, site is live. noindex confirmed absent on the live puppies page"}
  - {id: g4-noindex-off, closed: 2026-09-23, evidence: "Live robots.txt returns 200 with Allow: / and the sitemap declared, and no page carries noindex"}
  - {id: g4-sitemap, closed: 2026-09-23, evidence: "Live sitemap.xml returns 200 with 22 locs against 22 real pages"}
  - {id: g4-gsc, closed: 2026-09-23, evidence: "Search Console verified as a domain property with sitemap.xml submitted and the homepage indexed"}
decisions:
  - {date: 2026-09-23, decision: "Site sits at G5 and carries its G2 gaps as open items, per the lifecycle rule that a live site still owes its earlier gates"}
  - {date: 2026-09-23, decision: "aggregateRating stays out of the schema until real reviews exist and are visible on the page"}
  - {date: 2026-09-23, decision: "No address in LocalBusiness. areaServed only, because this is a home-based business"}
---

# Bless Your Paws Puppies

**Objective.** Sell the current litter and build ranking value that survives it, for Hope
and Joy's Munchkin Bernedoodle business in northern Indiana.

**Status.** Live and complete as a build, sitting at G5. The technical foundation is
sound, so the gaps are depth rather than defects: structured data stops at the homepage
and the puppy pages, and the local-presence and measurement phases have not started.

## Open questions

- The Google Business Profile Knowledge Graph ID, so it can go in `sameAs`. Blocked on
  Alex.
- Whether the profile's address is hidden and the service area is the one-hour ring,
  which has not been confirmed since verification came through. Blocked on Alex.
- What happens to a puppy page when the puppy goes home, because eight of them expire
  together in about ten weeks. Blocked on Alex.

## Next

Close the schema depth items, since they are the largest gap, entirely within this repo
and the thing the audit rubric weighs most.

## Where things landed

- Live at https://blessyourpawspuppies.com on Cloudflare Workers
- Generated by `scripts/scaffold.py`, which is the only place to edit anything
- Pending build items live in `README.md`, and SEO state lives here
