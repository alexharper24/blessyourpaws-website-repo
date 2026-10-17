/**
 * /api/stripe-webhook. Stripe calls this when a Checkout payment completes
 * (destination "blessyourpaws-reserve-test", event checkout.session.completed).
 *
 * 1. Verify the Stripe-Signature header: HMAC SHA-256 of "<t>.<raw body>" with
 *    STRIPE_WEBHOOK_SECRET, against any v1 value, with t no more than 5 minutes old.
 *    Anything unsigned or stale is refused before the body is read as JSON.
 * 2. Hand the puppy and the kind of payment to the editor Worker through the EDITOR
 *    service binding, which marks the puppy and commits that one change (admin/worker/payments.js).
 * 3. Tell the owners by email (notify.js).
 *
 * A 200 tells Stripe to stop retrying, so it is returned only once the change is applied or
 * there is nothing to apply. A failure returns 500 and Stripe tries again, which is safe
 * because the editor side ignores a session it has already seen.
 *
 * NO BUYER DATA. The event carries the buyer's name and email; nothing here reads, logs or
 * passes them on. Only metadata.puppy, metadata.pay, the session id and the amount are used.
 */
import { notify } from "./notify.js";
import { verify } from "./signature.js";

export async function webhook(request, env, ctx) {
  if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
  const payload = await request.text();
  if (!(await verify(request.headers.get("Stripe-Signature"), payload, env.STRIPE_WEBHOOK_SECRET))) {
    return new Response("Bad signature", { status: 400 });
  }
  const event = JSON.parse(payload);
  if (event.type !== "checkout.session.completed") return new Response("ignored", { status: 200 });
  const s = event.data.object;
  const slug = s.metadata && s.metadata.puppy;
  const pay = s.metadata && s.metadata.pay;
  // An old Payment Link session carries no puppy; there is nothing to mark.
  if (!slug || !pay) return new Response("no puppy", { status: 200 });
  if (s.payment_status !== "paid") return new Response("not paid", { status: 200 });

  const live = event.livemode === true;
  let result;
  try {
    result = await env.EDITOR.paymentCleared({ slug, pay, session: s.id, live });
  } catch (err) {
    console.error("editor binding", String(err && err.message || err));
    return new Response("retry", { status: 500 });
  }
  console.log("stripe payment", JSON.stringify({ slug, pay, live, outcome: result.outcome, commit: result.commit || null }));
  if (result.outcome !== "repeat") {
    ctx.waitUntil(notify(env, { slug, pay, live, amount: s.amount_total, paymentIntent: s.payment_intent, result })
      .catch((err) => console.error("notify", String(err && err.message || err))));
  }
  return new Response("ok", { status: 200 });
}
