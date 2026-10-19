#!/usr/bin/env node
// Proves a publish with many photos stays under the Workers limit of 50 outside requests per
// invocation and still ends in ONE commit (2026-10-18: a 46-photo publish failed with "Too many
// subrequests"). GitHub, R2 and D1 are stand-ins; nothing leaves this machine.
//
//     node admin/publish-rounds.test.mjs [photos]

import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { seedAll } from './lib/files.mjs';
import { nodeDb } from './lib/db.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const N = Number(process.argv[2] || 46);

const sqlite = new DatabaseSync(':memory:');
sqlite.exec(readFileSync(join(HERE, 'schema.sql'), 'utf8'));
await seedAll(nodeDb(sqlite), (p) => readFileSync(join(ROOT, p), 'utf8'));

// D1-shaped binding over node:sqlite
const DB = {
  prepare(sql) {
    const st = sqlite.prepare(sql);
    let args = [];
    const api = {
      bind(...a) { args = a.map((v) => (v instanceof ArrayBuffer ? new Uint8Array(v) : v)); return api; },
      async all() { return { results: st.all(...args) }; },
      async run() { const r = st.run(...args); return { meta: { changes: Number(r.changes) } }; },
    };
    return api;
  },
};

// N new photos on Joshua, each uploaded to "R2"
const r2 = new Map();
const pup = JSON.parse(sqlite.prepare("SELECT doc FROM records WHERE file='puppies' AND key='joshua'").get().doc);
for (let i = 0; i < N; i += 1) {
  const stem = `joshua-${String(50 + i).padStart(2, '0')}`;
  const key = `pending/puppies/${stem}.jpg`;
  r2.set(key, new Uint8Array([0xff, 0xd8, i & 255, 0xff, 0xd9]));
  sqlite.prepare(`INSERT INTO uploads (key, repo_path, stem, owner_file, owner_key, bytes, committed, created_at, created_by)
    VALUES (?, ?, ?, 'puppies', 'joshua', 5, 0, 'now', 'test')`).run(key, `uploads/puppies/${stem}.jpg`, stem);
  pup.photos.push(stem);
}
sqlite.prepare("UPDATE records SET doc = ? WHERE file='puppies' AND key='joshua'").run(JSON.stringify(pup));
const FILES = { async get(k) { const b = r2.get(k); return b ? { async arrayBuffer() { return b.buffer.slice(0); } } : null; } };

// The real repository's file list, so photos already on the site count as present
const TRACKED = execFileSync('git', ['ls-files'], { cwd: ROOT, encoding: 'utf8' }).split('\n').filter(Boolean)
  .map((path) => ({ path, type: 'blob', sha: 'x' }));

// GitHub stand-in that counts outside requests per invocation and enforces the limit
let count = 0;
let commits = 0;
let lastTree = null;
globalThis.fetch = async (url, init = {}) => {
  count += 1;
  if (count > 50) throw new Error('Too many subrequests by single Worker invocation');
  const u = String(url);
  const m = init.method || 'GET';
  const ok = (body) => new Response(JSON.stringify(body), { status: 200, headers: { 'Content-Type': 'application/json' } });
  if (u.includes('/git/ref/heads/')) return ok({ object: { sha: 'headsha' } });
  if (u.includes('/git/commits/') && m === 'GET') return ok({ tree: { sha: 'treesha' } });
  if (u.includes('/git/trees/') && m === 'GET') return ok({ tree: TRACKED, truncated: false });
  if (u.endsWith('/git/blobs') && m === 'POST') return ok({ sha: `blob${count}` });
  if (u.endsWith('/git/trees') && m === 'POST') { lastTree = JSON.parse(init.body); return ok({ sha: 'newtree' }); }
  if (u.endsWith('/git/commits') && m === 'POST') { commits += 1; return ok({ sha: 'newcommit' }); }
  if (u.includes('/git/refs/heads/') && m === 'PATCH') return ok({});
  throw new Error(`unexpected ${m} ${u}`);
};

const { publish } = await import('./worker/publish.js');
const env = { DB, FILES, GITHUB_TOKEN: 'x', GITHUB_REPO: 'o/r', GITHUB_BRANCH: 'main' };
const who = { email: 'test@example.com', person: { display_name: 'Test' } };

let round = 0;
let res;
do {
  count = 0;
  round += 1;
  res = await publish(env, who);
  console.log(`round ${round}: ${count} outside requests ->`, res.partial ? `partial ${res.staged}/${res.total}` : res.ok ? `commit ${res.commit}` : res.error);
} while (res.partial && round < 10);

const photoEntries = lastTree ? lastTree.tree.filter((e) => e.path.startsWith('uploads/')).length : 0;
const allSha = lastTree ? lastTree.tree.filter((e) => e.path.startsWith('uploads/')).every((e) => e.sha) : false;
const ok = res.ok && !res.partial && commits === 1 && photoEntries === N && allSha;
console.log(`${ok ? 'PASS' : 'FAIL'}: ${commits} commit, ${photoEntries} of ${N} photos in it, every photo by staged sha: ${allSha}`);
process.exit(ok ? 0 : 1);
