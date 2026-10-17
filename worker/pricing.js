/** The money rules for /api/checkout, kept free of imports so node can test them
 * (worker/test/amounts.mjs). See checkout.js for the route. */

export const SITE = "https://blessyourpawspuppies.com";
export const PAYS = ["deposit", "full", "balance"];

/** What to charge, or a reason to refuse. Pure, so the amounts can be tested. */
export function plan(prices, slug, pay) {
  const p = prices.puppies[slug];
  if (!p || !PAYS.includes(pay)) return { error: 404 };
  if (p.status === "adopted") return { error: 409, puppy: p };
  if ((pay === "deposit" || pay === "full") && p.status !== "available") return { error: 409, puppy: p };
  const lines = [];
  if (pay === "deposit") {
    lines.push([`Deposit for ${p.name}, ${p.breed}`, p.deposit]);
  } else if (pay === "full") {
    lines.push([`${p.name}, ${p.breed}`, p.price]);
    lines.push([prices.tax_label, p.tax]);
  } else {
    lines.push([`Balance for ${p.name}, ${p.breed}, after the ${dollars(p.deposit)} deposit`, p.price - p.deposit]);
    lines.push([prices.tax_label, p.tax]);
  }
  return { puppy: p, lines, total: lines.reduce((t, l) => t + l[1], 0) };
}

const dollars = (c) => `$${(c / 100).toLocaleString("en-US", { minimumFractionDigits: c % 100 ? 2 : 0 })}`;

/** The form body Stripe's REST API takes. */
export function sessionForm(slug, pay, pl) {
  const f = new URLSearchParams();
  f.set("mode", "payment");
  f.append("payment_method_types[]", "card");
  pl.lines.forEach(([name, cents], i) => {
    f.set(`line_items[${i}][quantity]`, "1");
    f.set(`line_items[${i}][price_data][currency]`, "usd");
    f.set(`line_items[${i}][price_data][unit_amount]`, String(cents));
    f.set(`line_items[${i}][price_data][product_data][name]`, name);
  });
  for (const k of ["metadata", "payment_intent_data[metadata]"]) {
    f.set(`${k}[puppy]`, slug);
    f.set(`${k}[pay]`, pay);
  }
  f.set("success_url", `${SITE}/thanks?pay=${pay}`);
  f.set("cancel_url", `${SITE}${pl.puppy.page}`);
  return f;
}
