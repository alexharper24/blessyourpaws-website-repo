/**
 * Bless Your Paws Puppies.
 *
 * The site itself is static and is served straight from the edge by the ASSETS binding;
 * this Worker only runs for the paths named in `run_worker_first`: /admin (a 404, the editor
 * is its own Worker at admin.blessyourpawspuppies.com) and /api/*, which is Stripe checkout.
 *
 * It is here now rather than later because the hosting shape is expensive to change once
 * a domain is pointed at it, and cheap to put in place while nothing depends on it.
 *
 * When the admin arrives it goes behind Cloudflare Access, not behind a password this
 * code checks: Access handles sign-in, and the Worker verifies the signed assertion as a
 * second line of defence. roanoke-baptist/worker/access.js is the working example.
 *
 * Anything served from in here needs its headers set in code. `_headers` applies to
 * assets, not to responses a Worker generates.
 */
import { checkout } from "./checkout.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Stripe Checkout per puppy (docs/checkout-build.md).
    if (url.pathname === "/api/checkout") return checkout(request, env);

    // Not built yet. A 404 rather than a placeholder page, so nothing suggests there is
    // something here to find.
    if (url.pathname === "/admin" || url.pathname.startsWith("/admin/") ||
        url.pathname.startsWith("/api/")) {
      return new Response("Not found", {
        status: 404,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    // Unreachable while run_worker_first lists only the routes above, but correct if that
    // list ever widens.
    return env.ASSETS.fetch(request);
  },
};
