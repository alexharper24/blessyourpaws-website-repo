/**
 * The email Hope (and Joy, once her address is added) gets for every Checkout payment.
 *
 * Sent through the MAIL send_email binding, which can only deliver to addresses verified in
 * the zone's Email Routing and listed in wrangler.jsonc. Plain text: the puppy, which payment,
 * the amount, what the site did about it, and the payment's page in Stripe. Who paid is on
 * that Stripe page and nowhere in this email, so no buyer details pass through our systems.
 */
import { EmailMessage } from "cloudflare:email";
import { compose } from "./message.js";

const FROM = "payments@blessyourpawspuppies.com";
function header(v) {
  return /^[\x20-\x7e]*$/.test(v) ? v : `=?UTF-8?B?${btoa(String.fromCharCode(...new TextEncoder().encode(v)))}?=`;
}

export async function notify(env, info) {
  if (!env.MAIL || !env.NOTIFY_TO) return;
  const { subject, body } = compose(info);
  for (const to of env.NOTIFY_TO.split(",").map((a) => a.trim()).filter(Boolean)) {
    const raw = [
      `From: Bless Your Paws website <${FROM}>`,
      `To: ${to}`,
      `Subject: ${header(subject)}`,
      `Message-ID: <${crypto.randomUUID()}@blessyourpawspuppies.com>`,
      `Date: ${new Date().toUTCString()}`,
      "MIME-Version: 1.0",
      "Content-Type: text/plain; charset=utf-8",
      "Content-Transfer-Encoding: 8bit",
      "",
      body,
    ].join("\r\n");
    await env.MAIL.send(new EmailMessage(FROM, to, raw));
  }
}
