/** The payment email's subject and body, free of imports so node can test it. Sent by notify.js. */

const WORDS = { deposit: "Deposit", full: "Full payment", balance: "Balance" };

const money = (cents) => `$${(cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

/** Subject and body, kept apart from sending so they can be read in a test. */
export function compose({ slug, pay, live, amount, paymentIntent, result }) {
  const name = result.name || slug;
  const what = WORDS[pay] || pay;
  const site = {
    marked: `The site now shows ${name} as ${result.now}. It updates in about two minutes.`,
    "marked-not-published": `${name} is marked ${result.now} in the editor, but the site could not be updated (${result.error}). Open the editor and press Publish.`,
    "no-change": "Nothing on the site changes for a balance payment.",
    already: `${name} was already ${result.was}, so nothing on the site changed.`,
    clash: `${name} was ALREADY ${result.was} before this payment came in, so two families may have paid for the same puppy. Nothing on the site changed. Check both payments in Stripe and refund one.`,
    raced: `${name}'s status changed while this payment was being recorded, so nothing on the site changed. Check the editor.`,
    "unknown-puppy": `The payment names a puppy the editor does not have (${slug}). Check it in Stripe.`,
    "test-dry": `TEST MODE: this would have marked ${name} ${result.now}. Nothing on the site changed.`,
  }[result.outcome] || `Result: ${result.outcome}.`;
  const subject = `${live ? "" : "[TEST] "}${result.outcome === "clash" ? "Check this: " : ""}${what} paid for ${name}`;
  const link = paymentIntent ? `https://dashboard.stripe.com/${live ? "" : "test/"}payments/${paymentIntent}` : "https://dashboard.stripe.com/payments";
  const body = [
    `${what} paid for ${name}: ${money(amount || 0)}.`,
    "",
    site,
    "",
    `The payment in Stripe: ${link}`,
    "",
    "Sent by the Bless Your Paws website.",
  ].join("\r\n");
  return { subject, body };
}
