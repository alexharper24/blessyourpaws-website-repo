// A payment cleared in Stripe: mark the puppy, and put ONLY that change on the site.
//
// Called by the site Worker's /api/stripe-webhook through a service binding to the Internal
// entrypoint in index.js. It is not reachable from the internet, so it carries no Access
// check; the site Worker has already verified Stripe's signature before calling.
//
// A deposit marks the puppy reserved and a full payment marks it adopted. A balance changes
// nothing. The change goes into the database the way an owner's save does (version bump,
// audit row, actor "stripe"), and then into data/puppies.json at HEAD on main as a commit
// of that one field, so anything an owner has saved but not published stays unpublished.
//
// Repeat-safe: Stripe retries a webhook until it gets a 200 and may deliver one twice. A
// session already in the audit, or a puppy already at that status, changes nothing.
//
// NO BUYER DATA. Only the puppy, the kind of payment and Stripe's session id arrive here.

import { audit, db, getRecord, NOW } from './store.js';
import { gh } from './publish.js';
import { FILES, dump } from '../lib/files.mjs';

const TARGET = { deposit: 'reserved', full: 'adopted' };
const RANK = { available: 0, reserved: 1, adopted: 2 };

function b64ToText(b64) {
  const bin = atob(b64.replace(/\n/g, ''));
  return new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0)));
}
function textToB64(text) {
  const bytes = new TextEncoder().encode(text);
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

/** Commit one puppy's status to data/puppies.json at the head of the branch. */
async function commitStatus(env, slug, status, message) {
  const path = FILES.puppies;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const cur = await gh(env, `/contents/${path}?ref=${encodeURIComponent(env.GITHUB_BRANCH)}`);
    const text = b64ToText(cur.content);
    const list = JSON.parse(text);
    // Only rewrite a file this code would have written byte for byte, so the commit is one line.
    if (dump(list) !== text) throw new Error('data/puppies.json is not in the editor\'s format; not touching it');
    const rec = list.find((p) => p.slug === slug);
    if (!rec) return { commit: null, note: 'not in the published file yet' };
    if (rec.status === status) return { commit: null, note: 'already on the site' };
    rec.status = status;
    const res = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}/contents/${path}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${env.GITHUB_TOKEN}`, Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'blessyourpaws-editor', 'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, content: textToB64(dump(list)), sha: cur.sha, branch: env.GITHUB_BRANCH }),
    });
    if (res.status === 409 || res.status === 422) continue;   // the branch moved under us: read it again
    if (!res.ok) throw new Error(`GitHub PUT ${path}: ${res.status} ${(await res.text()).slice(0, 200)}`);
    return { commit: (await res.json()).commit.sha };
  }
  throw new Error('data/puppies.json kept changing; gave up after three tries');
}

/**
 * @param {{slug: string, pay: string, session: string, live: boolean}} p
 * @returns what happened, for the email and the webhook's log. Never throws for a
 *   payment it cannot apply; it says so instead, so the owner is told.
 */
export async function paymentCleared(env, { slug, pay, session, live }) {
  const target = TARGET[pay];
  let rec;
  try { rec = await getRecord(env, 'puppies', slug); } catch { return { outcome: 'unknown-puppy' }; }
  const name = rec.doc.name;
  const was = rec.doc.status;
  if (!target) return { outcome: 'no-change', name, was };

  const seen = await db(env).all("SELECT id FROM audit WHERE actor = 'stripe' AND detail LIKE ?", [`%${session}%`]);
  if (seen.length) return { outcome: 'repeat', name, was };
  if (RANK[was] >= RANK[target]) {
    // A deposit on a puppy someone else has already reserved is the case the owner must hear about.
    const clash = pay === 'deposit' || was === 'adopted';
    await audit(env, { file: 'puppies', key: slug, action: clash ? 'stripe-clash' : 'stripe-repeat', detail: `${pay} while ${was}, ${session}`, actor: 'stripe' });
    return { outcome: clash ? 'clash' : 'already', name, was };
  }

  // Test-mode payments do not change the live site unless writes are switched on for a
  // deliberate end-to-end run (wrangler.jsonc var STRIPE_TEST_WRITES). They still report
  // what they would have done.
  if (!live && env.STRIPE_TEST_WRITES !== 'on') {
    await audit(env, { file: 'puppies', key: slug, action: 'stripe-test', detail: `would mark ${target}, ${pay}, ${session}`, actor: 'stripe' });
    return { outcome: 'test-dry', name, was, now: target };
  }

  const res = await db(env).run(
    `UPDATE records SET doc = json_set(doc, '$.status', ?), version = version + 1, updated_at = ?, updated_by = 'stripe'
      WHERE file = 'puppies' AND key = ? AND json_extract(doc, '$.status') = ?`, [target, NOW(), slug, was]);
  const changed = res && res.meta ? res.meta.changes : res && res.changes;
  if (!changed) return { outcome: 'raced', name, was };
  await audit(env, { file: 'puppies', key: slug, action: 'status', detail: `status ${was} to ${target} by ${pay} payment, ${session}`, actor: 'stripe' });

  if (!env.GITHUB_TOKEN) return { outcome: 'marked-not-published', name, was, now: target, error: 'no GitHub token' };
  try {
    const c = await commitStatus(env, slug, target,
      `Mark ${name} ${target} after a Stripe ${pay === 'full' ? 'full payment' : 'deposit'}\n\nFrom the payment webhook${live ? '' : ' (TEST MODE)'}. Only this puppy's status changed.`);
    if (c.commit) await audit(env, { action: 'publish', detail: `${c.commit.slice(0, 7)}: ${name} ${target} (stripe)`, actor: 'stripe' });
    return { outcome: 'marked', name, was, now: target, commit: c.commit, note: c.note };
  } catch (err) {
    console.error('stripe commit', String(err.message || err));
    return { outcome: 'marked-not-published', name, was, now: target, error: String(err.message || err) };
  }
}
