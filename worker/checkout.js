/**
 * /api/checkout?puppy=<slug>&pay=deposit|full|balance
 *
 * Builds a Stripe Checkout Session for one puppy and sends the buyer to it (303). What it may
 * charge comes from prices.json, which scripts/scaffold.py writes on the same build that
 * deploys this Worker, so the amount always matches the page the buyer clicked from.
 *
 * - deposit and full: only for an available puppy. A deposit has no tax.
 * - balance: for a reserved puppy, or an available one (a deposit taken by phone).
 * - full and balance carry the sales tax as its own line, so the receipt shows it.
 *
 * Card only. Apple Pay and Google Pay ride on card; Link stays off because it brings back
 * pay-later methods (see the Stripe setup notes). ACH must never be enabled here, for the
 * reason written above M_PRICE_CASH in scaffold.py.
 *
 * Nothing about the buyer passes through or is kept by this Worker. Stripe collects what it
 * needs on its own page.
 */
import PRICES from "./prices.json";
import { SITE, plan, sessionForm } from "./pricing.js";

export async function checkout(request, env) {
  if (request.method !== "GET") return new Response("Method not allowed", { status: 405, headers: { Allow: "GET" } });
  // A prefetch or prerender must never create a session. The site's own warmer skips /api/,
  // and this covers browsers and link previewers that do not.
  const purpose = request.headers.get("Sec-Purpose") || request.headers.get("Purpose") || "";
  if (/prefetch|prerender/i.test(purpose)) return new Response(null, { status: 204 });

  const url = new URL(request.url);
  const slug = url.searchParams.get("puppy") || "";
  const pay = url.searchParams.get("pay") || "";
  const pl = plan(PRICES, slug, pay);
  if (pl.error === 404) return Response.redirect(`${SITE}/puppies`, 303);
  // Spoken for since the page was built: back to the puppy page, which will say so.
  if (pl.error) return Response.redirect(`${SITE}${pl.puppy.page}`, 303);
  if (!env.STRIPE_KEY) return new Response("Payments are not set up.", { status: 503 });

  const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.STRIPE_KEY}`, "Content-Type": "application/x-www-form-urlencoded" },
    body: sessionForm(slug, pay, pl),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.url) {
    // The message names the field Stripe disliked, never a key. No buyer data exists here yet.
    console.error("stripe checkout", res.status, body.error && body.error.message);
    return new Response("Online payment is not available right now. Please call or text us to reserve.", {
      status: 502, headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
  return new Response(null, { status: 303, headers: { Location: body.url, "Cache-Control": "no-store" } });
}
