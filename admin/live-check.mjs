#!/usr/bin/env node
// Does the LIVE database export to the files in the repo? Read only.
//
//     node live-check.mjs            compare with HEAD
//     node live-check.mjs --disk     compare with the working tree
//
// Pulls every record from the remote D1 through wrangler, loads it into an in-memory SQLite,
// and runs the same exportAll a publish runs. A mismatch means an owner saved without
// publishing, or a change to the live database never reached the files (or the reverse).
// Run it before and after any SQL file against the live database.

import { DatabaseSync } from 'node:sqlite';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { nodeDb } from './lib/db.mjs';
import { exportAll } from './lib/files.mjs';

const disk = process.argv.includes('--disk');
const out = execSync(
  'npx -y wrangler d1 execute blessyourpaws --remote --json --command "SELECT file, key, doc, sort_order, version FROM records"',
  { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 64 << 20 });
const rows = JSON.parse(out)[0].results;
const sqlite = new DatabaseSync(':memory:');
sqlite.exec('CREATE TABLE records (file TEXT, key TEXT, doc TEXT, sort_order INTEGER, version INTEGER)');
const ins = sqlite.prepare('INSERT INTO records VALUES (?, ?, ?, ?, ?)');
for (const r of rows) ins.run(r.file, r.key, r.doc, r.sort_order, r.version);

let bad = 0;
for (const [path, text] of Object.entries(await exportAll(nodeDb(sqlite)))) {
  const want = disk
    ? readFileSync(`../${path}`, 'utf8').replace(/\r\n/g, '\n')
    : execSync(`git show HEAD:${path}`, { encoding: 'utf8' });
  const ok = want === text;
  if (!ok) bad += 1;
  console.log(ok ? 'same' : 'DIFF', path);
}
console.log(bad ? `LIVE DIFFERS from ${disk ? 'disk' : 'HEAD'} in ${bad} file(s)` : `live matches ${disk ? 'disk' : 'HEAD'}`);
process.exit(bad ? 1 : 0);
