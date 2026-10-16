---
doc: account-move
written: 2026-10-15
objective: "Move Bless Your Paws, the domain, the site Worker and the info@ forwarding, out of Alex's main Cloudflare account into an account of its own, before the owner editor is built"
why: "Alex, 2026-10-01: every project gets its own authentication and the projects stay separate. Cloudflare brands one sign-in page per account, and the editor needs its own"
status: "PREP DONE 2026-10-15. Inventory read and the domain confirmed eligible to move. Waiting on Alex to create the account and turn on Zero Trust"
from_account: "8deb46801616202e202899dc565f65d5 (Alex24harper@gmail.com's Account)"
to_account: "not created yet"
inventory_checked: 2026-10-15
inventory:
  zone: {name: blessyourpawspuppies.com, id: 08249f61c05a24abd778a10ba350b427, plan: Free, nameservers: [jerome.ns.cloudflare.com, marlowe.ns.cloudflare.com], dnssec: disabled, ssl: full, always_use_https: "off (the redirect rule below closes plain http)"}
  registration: {registrar: "Cloudflare Registrar, main account", registered: 2026-08-24, expires: 2029-08-24, auto_renew: "OFF", registrant_email_verified: true, status: "clientTransferProhibited (normal registrar lock)", domain_move_ineligibility_reasons: "none"}
  dns_records_to_recreate:
    - "TXT apex google-site-verification=4o43vCJnbb_M2uawIBAuXUxcKmi6Lp5Ziw2A_zxCmPk (Search Console domain property)"
    - "TXT apex v=spf1 include:_spf.mx.cloudflare.net ~all"
    - "MX route1/2/3.mx.cloudflare.net, written by Email Routing when it is enabled, not by hand"
    - "AAAA apex and www 100:: proxied, written by the Worker custom domains, not by hand"
  redirect_rule: {name: "Canonical host: www and http to https apex", expression: '(http.host eq "www.blessyourpawspuppies.com") or (not ssl)', action: '301 to concat("https://blessyourpawspuppies.com", http.request.uri.path), query string kept'}
  email_routing: {rule: "info to Hope, info@blessyourpawspuppies.com forwards to Hope's Gmail", catch_all: "drop, disabled", destination_verified_in_old_account: true}
  worker: {name: blessyourpaws, bindings: "ASSETS only", custom_domains: [blessyourpawspuppies.com, www.blessyourpawspuppies.com], workers_dev: false, preview_urls: false}
  builds: {repo: alexharper24/blessyourpaws-website-repo, branch: main, build_command: "(none)", deploy_command: "npx wrangler deploy", root: "/"}
  nothing_else: "No D1, R2, secrets or Access application yet. They arrive with the editor, in the new account"
alex_steps:
  - {id: A1, status: open, item: "Create the account from the Accounts page and name it (suggested Bless Your Paws Puppies). Account creation is yours to click"}
  - {id: A2, status: open, item: "Turn on Zero Trust Free in the new account with team name blessyourpaws, and add a payment method if it asks, since I cannot enter card details"}
  - {id: A3, status: open, item: "Approve GitHub for the new account when Workers Builds is connected, and leave the Cloudflare GitHub app on All repositories (the Teapup move narrowed it to one repo by accident)"}
  - {id: A4, status: open, item: "Get Hope ready to click one verification email from Cloudflare on the day prep starts"}
  - {id: A5, status: open, item: "Decide whether to turn on auto-renew for the domain in the new account. It is off today and the domain expires August 24, 2029"}
claude_steps:
  - {id: C1, status: done 2026-10-15, evidence: "dashboard API read of the zone, DNS, rulesets, Email Routing, registration, Worker, custom domains and build trigger, recorded above", item: "Inventory the current setup"}
  - {id: C2, status: done 2026-10-15, evidence: "registration API reports domain_move ineligibility_reasons empty, DNSSEC disabled, registrant email verified, no pending transfer or registrant change", item: "Confirm the registration can move between accounts"}
  - {id: C3, status: open, item: "Add blessyourpawspuppies.com to the new account on the Free plan. It sits pending and changes nothing live while the nameservers still point at the old zone"}
  - {id: C4, status: open, item: "Recreate the two TXT records, the redirect rule and SSL Full in the new zone, and enable Email Routing with Hope's Gmail as a destination so she can verify it ahead of the cutover. The old forwarding keeps working until then"}
  - {id: C5, status: open, item: "Pin account_id in wrangler.jsonc on a branch, ready for the cutover deploy"}
  - {id: C6, status: open, item: "CUTOVER. Start the registration move from the old account (Manage Domain, Configuration), accept it in the new one (Manage Domains, View Actions), confirm the nameservers now point at the new zone, deploy the Worker so the custom domains attach, then connect Workers Builds in the new account and disconnect it in the old one"}
  - {id: C7, status: open, item: "Verify. Every page answers 200 on the apex, www and http redirect with 301, a test email to info@ reaches Hope, Search Console still shows the domain verified, and site-checks is clean"}
  - {id: C8, status: open, item: "Update README, CLAUDE.md, the state file and memory with the new account. The old zone is marked Moved Away by Cloudflare and removed on its own"}
risks:
  - "The registration move carries no configuration (Cloudflare docs), which is why C3 and C4 build the new zone first"
  - "Expected gap of a few minutes (estimate, not measured) between the new zone going active and the Worker custom domains attaching. Run C6 at a quiet hour"
  - "Not confirmed by the docs: whether the registrar switches nameservers to the new zone automatically on acceptance. Checked on the day before anything is deployed"
  - "The domain is transfer-locked for 30 days after the move. That limits moving it to another registrar, not anything we plan"
sources:
  - https://developers.cloudflare.com/registrar/account-options/inter-account-transfer/
  - https://developers.cloudflare.com/fundamentals/manage-domains/move-domain/
---

# Moving Bless Your Paws to its own Cloudflare account

The site, its domain and Hope's email forwarding move into a new account under Alex's login that
holds nothing else, so the owner editor gets a sign-in page of its own. The order is built so
nothing live changes until the cutover step. The new zone is fully set up while it is still
pending, and Hope verifies her forwarding address ahead of time, so email keeps flowing
throughout.
