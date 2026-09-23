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
  - {id: g2-desc-long, gate: G2, blocked_on: claude, item: "Two meta descriptions over 155 characters: puppies.html at 176 and privacy-policy.html at 158"}
  - {id: g2-heading-skip, gate: G2, blocked_on: claude, item: "17 pages skip from H1 straight to H3. On a puppy page the Reserve and About blocks are H3 while later sections are H2, so the outline reads out of order"}
  # G4 Launch
  - {id: g4-www-redirect, gate: G4, blocked_on: alex, item: "www to apex redirect rule not in place on the zone. Both hostnames resolve and every page canonical points at the apex, so Google will consolidate on its own, but the rule makes it explicit"}
  - {id: g4-bing, gate: G4, blocked_on: alex, item: "Bing Webmaster Tools not set up. Google Search Console is verified with the sitemap submitted"}
  # G5 Grow
  - {id: g5-gbp-photos, gate: G5, blocked_on: client, item: "The profile carries ONE photo, owner-posted 29 days ago. Everything else about the profile is right, so photos are the whole remaining gap. Hope and Joy already have the puppy sets used on the site"}
  - {id: g5-name-collision, gate: G5, blocked_on: alex, item: "At least four unrelated businesses trade as Bless Your Paws: a groomer in Shelbyville TN, a pet sitter in Asheville, a Yelp pet-sitting listing in New Mexico, and a Pup Strut Society account. They crowd page one for the bare brand name. The site ranks first for the full name, so the exposure is on the short form"}
  - {id: g5-lancaster-price, gate: G5, blocked_on: alex, item: "A Lancaster Puppies breeder listing under this business name shows $1,350.00 in Google results, against $2,060 card and $2,000 cash on the site. Not ours to change and not verified as current, but a third-party listing carrying a different price for the same brand is worth Hope knowing about"}
  - {id: g5-reviews, gate: G5, blocked_on: client, item: "No review habit established and the site has no reviews to mark up. aggregateRating must stay absent until real reviews exist"}
  - {id: g5-monthly, gate: G5, blocked_on: alex, item: "Monthly Search Console and profile check not running, and no content cluster in progress"}
  - {id: g5-ai-check, gate: G5, blocked_on: alex, item: "AI visibility check never run. Ask the buying questions in ChatGPT, Perplexity and Gemini and record who gets named"}
  # Breeder-specific, from the lifecycle business-type table
  - {id: breeder-puppy-301, gate: G5, blocked_on: claude, item: "Retire the litter when every puppy is adopted: 301 each puppy-<slug> to /puppies in _redirects, remove the eight pages and their sitemap entries, and leave the photographs in the gallery. Not due until the last puppy is spoken for, and the per-puppy Adopted state already works"}
  - {id: breeder-breed-links, gate: G5, blocked_on: claude, item: "The breed guide is the page that accumulates ranking value between litters and it has only 4 inbound body links, against 24 to puppies.html and 14 to parents.html"}
closed:
  - {id: g2-pages, closed: 2026-09-23, evidence: "Breed guide, available puppies and parents all exist as their own pages, which is the breeder money-page set"}
  - {id: g2-onpage-nap, closed: 2026-09-23, evidence: "Name, service area and phone as real text with a tel: link on all 23 pages, verified by grep"}
  - {id: g2-schema-depth, closed: 2026-09-23, evidence: "page() now emits a BreadcrumbList for every page that does not bring its own, so 21 of 23 pages carry one. Only index.html (the root of the trail) and 404.html do not, by design. Every block parses"}
  - {id: g2-schema-money, closed: 2026-09-23, evidence: "puppies.html has an ItemList of the eight puppies it visibly lists, parents.html and the breed guide have BreadcrumbList, the business node has an @id and the puppy Offers name it as seller"}
  - {id: g2-canonical-root, closed: 2026-09-23, evidence: "Homepage canonical is https://blessyourpawspuppies.com/ not /index.html, the trap the lifecycle names"}
  - {id: g2-house, closed: 2026-09-23, evidence: "Light-mode lock, ?v= cache-busting, lowercase relative paths, favicon, 404 page, sitemap and robots all present"}
  - {id: g2-checks, closed: 2026-09-23, evidence: "site-checks clean and audit.py reports 0 broken links, 0 missing images, 0 pages without exactly one H1"}
  - {id: g2-images, closed: 2026-09-23, evidence: "WebP with srcset and sizes throughout, source-photos gitignored, 100 decorative images correctly carry alt=\"\" and none are missing the attribute"}
  - {id: g3-noindex, closed: 2026-09-23, evidence: "n/a, site is live. noindex confirmed absent on the live puppies page"}
  - {id: g4-noindex-off, closed: 2026-09-23, evidence: "Live robots.txt returns 200 with Allow: / and the sitemap declared, and no page carries noindex"}
  - {id: g4-sitemap, closed: 2026-09-23, evidence: "Live sitemap.xml returns 200 with 22 locs against 22 real pages"}
  - {id: g4-gsc, closed: 2026-09-23, evidence: "Search Console verified as a domain property with sitemap.xml submitted and the homepage indexed"}
  - {id: g5-gbp-sameas, closed: 2026-09-23, evidence: "CID 4658031195710535829 read from the Business Profile Manager and verified by loading the Maps URL, which returns this business with this site as its website. Wired as GBP_URL into the LocalBusiness sameAs"}
  - {id: g5-gbp-complete, closed: 2026-09-23, evidence: "Read in Chrome against the live Maps listing: category Dog breeder, NO address published, 19 service areas led by Goshen and Warsaw, hours set, website and phone present, women-owned attribute set. Phone matches the site character for character at (574) 377-8023. Photos split out as g5-gbp-photos, the one thing still short"}
decisions:
  - {date: 2026-09-23, decision: "Site sits at G5 and carries its G2 gaps as open items, per the lifecycle rule that a live site still owes its earlier gates"}
  - {date: 2026-09-23, decision: "aggregateRating stays out of the schema until real reviews exist and are visible on the page"}
  - {date: 2026-09-23, decision: "No address in LocalBusiness. areaServed only, because this is a home-based business"}
  - {date: 2026-09-23, decision: "sameAs carries the Google Business Profile only. The site has no social accounts of its own, and the Bless Your Paws accounts that surface in search belong to other businesses, so none of them may be claimed here"}
  - {date: 2026-09-23, decision: "Litter lifecycle (Alex): an adopted puppy stays on the site marked Adopted until every puppy in the litter is adopted, then the whole set of puppy pages comes down together to make room for the next litter. So retirement is one batched event per litter rather than a trickle, and the redirects are written once"}
---

# Bless Your Paws Puppies

**Objective.** Sell the current litter and build ranking value that survives it, for Hope
and Joy's Munchkin Bernedoodle business in northern Indiana.

**Status.** Live and complete as a build, sitting at G5. Structured data and the Google
Business Profile are now closed out, so what remains is the local-presence and measurement half of G5 plus two small
on-page items, and the biggest open question is no longer technical but editorial, being
what this site publishes between litters.

## Open questions

- Which supporting pages to build first, since the puppy pages expire together and the
  breed guide is the only page holding ranking value between litters. Blocked on Alex.
- Whether Hope wants the Lancaster Puppies listing brought into step with the site's
  pricing, since the two currently disagree in public. Blocked on Alex.

## Next

Work the content cluster around the breed guide, because after the litter retires it is
the only money page left standing and it currently has the fewest inbound links of the
three.

## Where things landed

- Live at https://blessyourpawspuppies.com on Cloudflare Workers
- Generated by `scripts/scaffold.py`, which is the only place to edit anything
- Pending build items live in `README.md`, and SEO state lives here
