// node worker/test/amounts.mjs  -- the three amounts the site states, from the generated prices.
import { readFileSync } from 'node:fs';
import { plan, sessionForm } from '../pricing.js';
const P = JSON.parse(readFileSync(new URL('../prices.json', import.meta.url), 'utf8'));
const avail = Object.keys(P.puppies).find((s) => P.puppies[s].status === 'available');
const adopted = Object.keys(P.puppies).find((s) => P.puppies[s].status === 'adopted');
const want = { deposit: 50000, full: 220420, balance: 170420 };
const out = []; let bad = 0;
for (const [pay, cents] of Object.entries(want)) {
  const t = plan(P, avail, pay).total; if (t !== cents) bad++; out.push(`${pay} ${(t / 100).toFixed(2)}`);
}
const reserved = { ...P, puppies: { x: { ...P.puppies[avail], status: 'reserved' } } };
const refuse = [plan(P, 'nobody', 'deposit').error, plan(P, avail, 'tip').error, plan(P, adopted, 'balance').error,
  plan(reserved, 'x', 'deposit').error, plan(reserved, 'x', 'full').error, plan(reserved, 'x', 'balance').total];
if (refuse.join() !== '404,404,409,409,409,170420') bad++;
const f = sessionForm(avail, 'full', plan(P, avail, 'full'));
if (f.getAll('payment_method_types[]').join() !== 'card' || f.get('metadata[pay]') !== 'full' || f.get('line_items[1][price_data][unit_amount]') !== '14420') bad++;
console.log(`${bad ? 'FAIL' : 'ok'}: ${out.join(', ')}; refusals ${refuse.join(',')}`);
process.exit(bad ? 1 : 0);
