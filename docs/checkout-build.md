---
doc: checkout-build
written: 2026-10-17
alex_said: "treat it as part 2 and go ahead and build it"
billing: "Part 2 of the quote, not a separate charge"
scope_estimate: "hs-proposals/blessyourpaws/2026-10-17-checkout-scope.json (local, private)"
goal: "A price change in the owner editor carries through to Stripe, a puppy marks itself reserved when a deposit or full payment clears, and Hope and Joy get an email for each. No buyer data is stored by the site or editor"
read_first:
  - "_claude-state.md, then this file"
  - "admin/README.md and docs/editor-build.md for how the editor works"
  - "breeder-site-backend skill, and project-cloudflare-account for Stripe-side steps that are Alex's"
  - "memory blessyourpaws-stripe-setup for the Stripe account traps (Link brings back pay-later, links cannot change amount, sandbox vs live)"
design:
  prices: "Each litter gets price (card, 2060 today), cash_price (2000) and deposit (500). scaffold.py's M_PRICE, M_PRICE_CASH and DEPOSIT become the puppy's litter's values, and the newest shown litter's for hand-written pages. Byte-identical gate (scripts/compare_build.py) before anything else changes"
  tax: "7% Indiana, IN_TAX_RATE stays in the generator. Full payment = round(price x 1.07, 2). Balance = full minus deposit. Deposit has no tax. Today's amounts to reproduce exactly: deposit 500.00, full 2204.20, balance 1704.20"
  checkout: "Site Worker (worker/index.js, /api/* already runs worker-first) route /api/checkout?puppy=<slug>&pay=deposit|full|balance. Reads a public per-puppy price file the generator writes (name, status, litter price, deposit). Refuses unknown or adopted puppies; deposit and full only for available; balance for reserved or available. Creates a Checkout Session by REST: payment_method_types card only (Apple Pay and Google Pay come with card; Link stays off), one line item for the puppy and a separate tax line on full and balance, metadata puppy and pay, success_url /thanks, cancel_url the puppy page, then 303 to session.url"
  webhook: "/api/stripe-webhook verifies the Stripe-Signature header (HMAC SHA-256 of t.payload with STRIPE_WEBHOOK_SECRET, 5 minute tolerance). On checkout.session.completed with pay deposit or full: mark the puppy reserved (deposit) or adopted (full) in the editor's D1, ignoring repeats, then commit ONLY that puppy's status change to data/puppies.json at HEAD on main, so an owner's unpublished edits never ship. Audit actor stripe. Balance payments change nothing"
  webhook_db: "The webhook runs on the site Worker, so it needs a D1 binding to the editor's database (blessyourpaws, c5b7075d) and GITHUB_TOKEN as its own secret, or it calls the editor Worker through a service binding. Prefer the service binding: the editor Worker keeps all writes and the token, and exposes an internal route reachable only through the binding"
  email: "Cloudflare send_email binding to the verified Email Routing destinations (Hope verified; add Joy when Alex gives her address). Plain text: puppy, which payment, amount, link to the payment in Stripe"
  editor: "Price, cash price and deposit inputs on the litter drawer, with range checks. History shows Stripe's changes"
  secrets_alex_enters: ["STRIPE_KEY (restricted key: Checkout Sessions write only)", "STRIPE_WEBHOOK_SECRET"]
  never: ["Claude creates or enters a Stripe key or webhook secret", "buyer names, emails or phones stored anywhere of ours", "the three live Payment Links turned off before the new checkout passes a full test-mode run"]
tasks:
  - {id: c1-prices, status: open, item: "Prices on litters, generator reads them, gate byte-identical"}
  - {id: c2-editor, status: open, item: "Price fields in the editor; roundtrip clean; redeploy editor"}
  - {id: c3-checkout, status: open, item: "Checkout route and public price file; unit-test amounts 500 / 2204.20 / 1704.20"}
  - {id: c4-links, status: open, item: "Swap the buy.stripe.com links for checkout links; thanks page; analytics event; gate shows only the intended pages change"}
  - {id: c5-webhook, status: open, item: "Webhook, signature check, reserve via service binding, targeted commit, repeat-safe"}
  - {id: c6-email, status: open, item: "Reservation email"}
  - {id: c7-test, status: open, item: "Stripe sandbox key and webhook from Alex; full test-mode run locally and on a preview"}
  - {id: c8-cutover, status: open, item: "Live key and webhook from Alex; deploy; one live payment and refund; deactivate the three old Payment Links; docs"}
---

# Prices in the editor and Stripe Checkout per puppy

Finishes Part 2 of the Bless Your Paws quote. The YAML above is the plan and the task list. Update
each task's status as it lands.
