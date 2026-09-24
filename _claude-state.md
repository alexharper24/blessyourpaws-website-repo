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
  - {id: g5-indexing, gate: G5, blocked_on: alex, item: "20 of 22 pages are Discovered - currently not indexed. Diagnosed 2026-09-23 as crawl priority, NOT a technical block: every page returns 200 to Googlebot with a self-canonical, robots allows all, the sitemap reads Success with 22 URLs, and Crawl Stats shows 183 requests, 100% OK, no host problems, 93ms. But 97% of those requests were refreshes of already-known pages and 3% discovery, so Google has barely tried the 20. Levers are manual Request Indexing on the evergreen pages first (puppies, parents, process, health-guarantee, about), body links from the two indexed pages, and external links, starting with Furry Freight linking back as a partner"}
  - {id: g5-money-pages, gate: G5, blocked_on: claude, item: "Two of the three breeder money pages earn nothing. Available puppies has drawn no impressions at all and parents is among the undiscovered pages, so the breed guide is carrying all three roles on its own"}
  - {id: g5-guide-converts, gate: G5, blocked_on: claude, item: "The breed guide holds most of the site's impressions and almost none of its clicks, because it reads as a reference article rather than a place to buy a puppy. It is also the only money page that survives the litter, so it is where the buying path belongs"}
  - {id: g5-growth-data, gate: G5, blocked_on: client, item: "The size page has no growth-by-age section because no real figures exist. When this litter is weighed at intervals, or grows up, those numbers are what searchers want and what replaces the parents-based projection"}
  - {id: g5-compare-page, gate: G5, blocked_on: hope, item: "Munchkin vs Mini vs Micro Bernedoodle comparison page, the honest route to the much larger mini and micro size searches. The puppies are not Mini Bernedoodles and the site must not call them that unless Hope decides otherwise"}
  - {id: g5-http-variant, gate: G5, blocked_on: alex, item: "An http:// version of the homepage is still being served in results. Visitors are redirected so nothing is broken, but it is a URL Google should not be holding. Same root as g4-www-redirect"}
  - {id: g5-cash-tax, gate: G5, blocked_on: alex, item: "The site never says whether 7% sales tax applies to the $2,000 cash price. Process says $2,060 plus sales tax, or $2,000 in cash; the application says tax is added and the cash fee applies only when both payments are cash. A buyer paying cash cannot tell what they owe. Alex or Hope to state it, then every place gets the same wording"}
  - {id: g5-monthly, gate: G5, blocked_on: alex, item: "Monthly Search Console and profile check not running, and no content cluster in progress"}
  - {id: g5-ai-check, gate: G5, blocked_on: alex, item: "AI visibility check never run. Ask the buying questions in ChatGPT, Perplexity and Gemini and record who gets named"}
  # Breeder-specific, from the lifecycle business-type table
  - {id: breeder-puppy-301, gate: G5, blocked_on: claude, item: "Retire the litter when every puppy is adopted: 301 each puppy-<slug> to /puppies in _redirects, remove the eight pages and their sitemap entries, and leave the photographs in the gallery. Not due until the last puppy is spoken for, and the per-puppy Adopted state already works. The colors page needs no edit at retirement, since its examples come from MUNCHKINS"}
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
  - {id: g5-retarget, closed: 2026-09-23, evidence: "Live after commit 1773e08: homepage titled Munchkin Bernedoodle Breeder in Indiana, puppies titled Munchkin Bernedoodles for Sale in Indiana with H1 to match. Approved by Alex. Measured at 1440, 901, 375 and 320 with no overflow"}
  - {id: g5-cluster-colors, closed: 2026-09-23, evidence: "bernedoodle-colors live (200) and in the sitemap after commit 1773e08. Examples generated from each puppy's recorded color, so they drop away when the litter retires. Linked from puppies and the breed guide"}
  - {id: g5-cluster-size, closed: 2026-09-23, evidence: "munchkin-bernedoodle-size live (200) after commit 85ee95e, built only from published size facts, linked from ten pages through SIZE_NOTE and from the breed guide. H1 holds two lines 901 to 1920. Growth-by-age content deliberately absent until Hope supplies real figures"}
  - {id: g5-cluster-shedding, closed: 2026-09-23, evidence: "bernedoodle-shedding live (200) after commit 2e040b3. Never promises non-shedding or hypoallergenic; says nothing about this litter beyond existing site copy. Linked from the process FAQ and the breed guide coat section. Sitemap at 25"}
  - {id: g5-cluster-lifespan, closed: 2026-09-23, evidence: "bernedoodle-lifespan-temperament live (200) after commit 15a45d1. Only facts the guide already publishes, no health conditions, no shared sentences. Linked from the guide lifespan and temperament answers. Sitemap at 26"}
  - {id: g5-cluster-cost, closed: 2026-09-23, evidence: "munchkin-bernedoodle-price live (200) after commit c3a9508. Every figure from the price constants, terms in published wording as a table; does not state whether tax applies to the cash price because the site never has. Linked from the process payments answer and seven puppy reserve blocks. Sitemap at 27"}
  - {id: g5-guide-layout, closed: 2026-09-23, evidence: "Layout pass live after commit 4ce65e4 at v=178: all five guide pages rebuilt below the hero from the hand-built components (hic photo pairs, one forest band, cards and checklists, pink close). Measured 320 to 1920 with no overflow, sizes hints within 13%, contrast 5.8:1 minimum; reviewed in full-page captures at 1440"}
  - {id: g5-kids-fact, closed: 2026-09-24, evidence: "Alex: raised around nieces and nephews. The breed guide FAQ said our own kids and the lifespan page said children; both now say nieces and nephews, and no page says our own kids"}
  - {id: g5-gbp-sameas, closed: 2026-09-23, evidence: "CID 4658031195710535829 read from the Business Profile Manager and verified by loading the Maps URL, which returns this business with this site as its website. Wired as GBP_URL into the LocalBusiness sameAs"}
  - {id: g5-gbp-complete, closed: 2026-09-23, evidence: "Read in Chrome against the live Maps listing: category Dog breeder, NO address published, 19 service areas led by Goshen and Warsaw, hours set, website and phone present, women-owned attribute set. Phone matches the site character for character at (574) 377-8023. Photos split out as g5-gbp-photos, the one thing still short"}
decisions:
  - {date: 2026-09-23, decision: "Site sits at G5 and carries its G2 gaps as open items, per the lifecycle rule that a live site still owes its earlier gates"}
  - {date: 2026-09-23, decision: "aggregateRating stays out of the schema until real reviews exist and are visible on the page"}
  - {date: 2026-09-23, decision: "No address in LocalBusiness. areaServed only, because this is a home-based business"}
  - {date: 2026-09-23, decision: "SUPERSEDED the same day by Semrush research (source-files/semrush/). Search Console only showed what two indexed pages could see; the tool showed the breed term is open (top ten all without backlinks), found coat color as an unplanned spoke, and showed the size vocabulary is far larger than the breed name. The GSC-only reasoning follows for the record"}
  - {date: 2026-09-23, decision: "Keyword research is taken from Search Console rather than from a keyword tool, per the lifecycle rule that tool volumes for small markets are unreliable. Sixteen real queries have arrived on their own and every one of them is the breed term or a question about it, so the breed name is how demand reaches this business and the category and place terms are not worth chasing"}
  - {date: 2026-09-23, decision: "The munchkin dog and munchkin dog breed queries are deliberately declined rather than targeted. Ranking for them would mean writing short-leg and dwarfism language as marketing, which Troy's panel result makes a claim this business should not be making"}
  - {date: 2026-09-23, decision: "No town pages. A set of place-swapped copies is the doorway pattern the lifecycle warns about, and this business has no town-specific content to put on them"}
  - {date: 2026-09-23, decision: "One cluster, around the breed guide, built from the two questions that already rank badly for real queries. The breed guide is the only money page that outlives the litter, so it is the page authority should accumulate on"}
  - {date: 2026-09-23, decision: "Performance figures, query data and the cluster plan live in source-files, which is gitignored, because this repo is served publicly and they are a client's business numbers. Only the decisions and the open items are here"}
  - {date: 2026-09-23, decision: "sameAs carries the Google Business Profile only. The site has no social accounts of its own, and the Bless Your Paws accounts that surface in search belong to other businesses, so none of them may be claimed here"}
  - {date: 2026-09-23, decision: "Litter lifecycle (Alex): an adopted puppy stays on the site marked Adopted until every puppy in the litter is adopted, then the whole set of puppy pages comes down together to make room for the next litter. So retirement is one batched event per litter rather than a trickle, and the redirects are written once"}
---

# Bless Your Paws Puppies

**Objective.** Sell the current litter and build ranking value that survives it, for Hope
and Joy's Munchkin Bernedoodle business in northern Indiana.

**Status.** Live and complete as a build, sitting at G5. Structured data and the Google
Business Profile are both closed out and the profile reads correctly against the site, so
the constraint is no longer on-page at all. Google has discovered twenty of the twenty-two
pages and not indexed them, which means the money pages and the cluster plan are both
waiting on indexing rather than on content.

## Open questions

- Which supporting pages to build first, since the puppy pages expire together and the
  breed guide is the only page holding ranking value between litters. Blocked on Alex.
- Whether Hope wants the Lancaster Puppies listing brought into step with the site's
  pricing, since the two currently disagree in public. Blocked on Alex.

## Next

Get the pages indexed, because nothing else pays until that moves. Twenty of twenty-two
are discovered and not indexed, so the cluster work and the money-page work are both
waiting on a problem neither of them solves. Internal linking is the half this repo
controls and the breed guide is where it should point, since it already has the fewest
inbound links and the most impressions.

## Where things landed

- Live at https://blessyourpawspuppies.com on Cloudflare Workers
- Generated by `scripts/scaffold.py`, which is the only place to edit anything
- Pending build items live in `README.md`, and SEO state lives here
