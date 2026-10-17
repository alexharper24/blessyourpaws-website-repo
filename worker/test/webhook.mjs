// node worker/test/webhook.mjs
// The webhook's three parts without Cloudflare or Stripe: the signature check, the email
// text, and the editor's payment handling against an in-memory database with GitHub mocked.
// Uses a made-up signing secret; no real Stripe value is involved.
import { createHmac } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { verify } from '../signature.js';
import { compose } from '../message.js';

const R = new URL('../../', import.meta.url);
const fails = [];
const check = (label, ok) => { if (!ok) fails.push(label); };

// ---- signature
const secret = 'whsec_local_test_only';
const body = '{"id":"evt_1"}';
const now = 1_800_000_000;
const sig = (t, b = body, s = secret) => `t=${t},v1=${createHmac('sha256', s).update(`${t}.${b}`).digest('hex')}`;
check('good signature', await verify(sig(now), body, secret, now));
check('second v1 accepted', await verify(`t=${now},v1=${'0'.repeat(64)},v1=${sig(now).split('v1=')[1]}`, body, secret, now));
check('tampered body refused', !(await verify(sig(now), body + ' ', secret, now)));
check('wrong secret refused', !(await verify(sig(now, body, 'whsec_other'), body, secret, now)));
check('stale refused', !(await verify(sig(now - 301), body, secret, now)));
check('missing header refused', !(await verify(null, body, secret, now)));

// ---- email
const m1 = compose({ slug: 'joshua', pay: 'deposit', live: false, amount: 50000, paymentIntent: 'pi_1', result: { outcome: 'test-dry', name: 'Joshua', was: 'available', now: 'reserved' } });
check('test subject', m1.subject === '[TEST] Deposit paid for Joshua');
check('test link', m1.body.includes('dashboard.stripe.com/test/payments/pi_1') && m1.body.includes('$500.00'));
const m2 = compose({ slug: 'eden', pay: 'deposit', live: true, amount: 50000, paymentIntent: 'pi_2', result: { outcome: 'clash', name: 'Eden', was: 'reserved' } });
check('clash subject', m2.subject === 'Check this: Deposit paid for Eden' && m2.body.includes('refund one'));
check('live link', m2.body.includes('dashboard.stripe.com/payments/pi_2'));

// ---- editor side
const sq = new DatabaseSync(':memory:');
sq.exec(readFileSync(new URL('admin/schema.sql', R), 'utf8'));
const { seedAll, dump } = await import(new URL('admin/lib/files.mjs', R));
const { nodeDb } = await import(new URL('admin/lib/db.mjs', R));
await seedAll(nodeDb(sq), (p) => readFileSync(new URL(p, R), 'utf8').replace(/\r\n/g, '\n'));
const DB = { prepare: (sql) => ({ bind: (...a) => ({
  all: async () => ({ results: sq.prepare(sql).all(...a) }),
  run: async () => { const r = sq.prepare(sql).run(...a); return { meta: { changes: r.changes } }; } }) }) };

let file = readFileSync(new URL('data/puppies.json', R), 'utf8').replace(/\r\n/g, '\n');
const puts = [];
globalThis.fetch = async (url, init = {}) => {
  if ((init.method || 'GET') === 'GET') {
    return new Response(JSON.stringify({ content: Buffer.from(file).toString('base64'), sha: `sha${puts.length}` }), { status: 200 });
  }
  const b = JSON.parse(init.body);
  const next = Buffer.from(b.content, 'base64').toString('utf8');
  puts.push({ before: file, after: next, message: b.message, branch: b.branch });
  file = next;
  return new Response(JSON.stringify({ commit: { sha: `c0ffee${puts.length}` } }), { status: 200 });
};
const { paymentCleared } = await import(new URL('admin/worker/payments.js', R));
const env = { DB, GITHUB_TOKEN: 'x', GITHUB_REPO: 'o/r', GITHUB_BRANCH: 'main', STRIPE_TEST_WRITES: 'off' };
const avail = JSON.parse(file).filter((p) => p.status === 'available').map((p) => p.slug);
const status = (slug) => JSON.parse(sq.prepare("SELECT doc FROM records WHERE file='puppies' AND key=?").get(slug).doc).status;

const dry = await paymentCleared(env, { slug: avail[0], pay: 'deposit', session: 'cs_test_1', live: false });
check('test mode is dry', dry.outcome === 'test-dry' && status(avail[0]) === 'available' && !puts.length);

env.STRIPE_TEST_WRITES = 'on';
const dep = await paymentCleared(env, { slug: avail[0], pay: 'deposit', session: 'cs_test_2', live: false });
const changedLines = (a, b) => { const x = a.split('\n'), y = b.split('\n'); return x.filter((l, i) => l !== y[i]).length + Math.abs(x.length - y.length); };
check('deposit marks reserved', dep.outcome === 'marked' && status(avail[0]) === 'reserved');
check('one commit, one line', puts.length === 1 && changedLines(puts[0].before, puts[0].after) === 1 && puts[0].after.includes('"status": "reserved"'));
check('dump format kept', dump(JSON.parse(puts[0].after)) === puts[0].after);

const rep = await paymentCleared(env, { slug: avail[0], pay: 'deposit', session: 'cs_test_2', live: false });
check('repeat ignored', rep.outcome === 'repeat' && puts.length === 1);
const clash = await paymentCleared(env, { slug: avail[0], pay: 'deposit', session: 'cs_test_3', live: false });
check('second deposit is a clash', clash.outcome === 'clash' && puts.length === 1);
const bal = await paymentCleared(env, { slug: avail[0], pay: 'balance', session: 'cs_test_4', live: false });
check('balance changes nothing', bal.outcome === 'no-change' && status(avail[0]) === 'reserved');
const full = await paymentCleared(env, { slug: avail[1], pay: 'full', session: 'cs_test_5', live: false });
check('full marks adopted', full.outcome === 'marked' && status(avail[1]) === 'adopted' && puts.length === 2);
const unk = await paymentCleared(env, { slug: 'nobody', pay: 'full', session: 'cs_test_6', live: false });
check('unknown puppy', unk.outcome === 'unknown-puppy');

// an owner's unsaved-to-site edit stays out of the commit
sq.prepare("UPDATE records SET doc = json_set(doc, '$.note', 'owner draft') WHERE file='puppies' AND key=?").run(avail[2]);
await paymentCleared(env, { slug: avail[2], pay: 'deposit', session: 'cs_test_7', live: false });
check('owner draft not committed', !puts[2].after.includes('owner draft'));

console.log(fails.length ? `FAIL: ${fails.join('; ')}` : `ok: signature 6, email 4, editor 10 checks; ${puts.length} commits, each one line`);
process.exit(fails.length ? 1 : 0);
