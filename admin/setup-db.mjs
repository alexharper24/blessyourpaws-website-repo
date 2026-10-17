#!/usr/bin/env node
// Create the editor's tables and seed them from data/*.json.
//
//     node admin/setup-db.mjs --local            the wrangler dev database
//     node admin/setup-db.mjs --remote           the live D1 (run ONCE, before the first publish)
//     node admin/setup-db.mjs --remote --sql     write the SQL file and stop, to read it first
//
// WARNING: --remote seeds the live database FROM THE FILES. Once Hope or Joy have saved
// anything, the database is ahead of the files and seeding again would overwrite their work.
// The script refuses if the remote database already holds records.
//
// It writes one SQL file and hands it to `wrangler d1 execute`, because that is the only
// route that works the same locally and remotely. No transaction, since remote D1 rejects
// BEGIN TRANSACTION.

import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { FILES, keyOf, stripKey } from './lib/files.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const args = process.argv.slice(2);
const where = args.includes('--remote') ? '--remote' : '--local';
const q = (v) => `'${String(v).replace(/'/g, "''")}'`;
const now = new Date().toISOString();

// The first person in. Everyone else is invited from the People screen.
const PEOPLE = [['alex24harper@gmail.com', 'Alex', 1]];

const lines = [readFileSync(join(HERE, 'schema.sql'), 'utf8')];
for (const [file, path] of Object.entries(FILES)) {
  const list = JSON.parse(readFileSync(join(ROOT, path), 'utf8'));
  list.forEach((rec, i) => {
    lines.push(`INSERT OR REPLACE INTO records (file, key, doc, sort_order, version, updated_at, updated_by) VALUES (${q(file)}, ${q(keyOf(file, rec, i))}, ${q(JSON.stringify(stripKey(file, rec)))}, ${i}, 1, ${q(now)}, 'seed');`);
  });
}
for (const [email, name, admin] of PEOPLE) {
  lines.push(`INSERT OR IGNORE INTO people (email, display_name, is_admin, added_at, added_by) VALUES (${q(email)}, ${q(name)}, ${admin}, ${q(now)}, 'setup');`);
}
const dir = mkdtempSync(join(tmpdir(), 'byp-seed-'));
const sqlFile = join(dir, 'seed.sql');
writeFileSync(sqlFile, `${lines.join('\n')}\n`);
console.log(`seed SQL: ${sqlFile}`);
if (args.includes('--sql')) process.exit(0);

// --persist-to matches the byp-editor entry in C:\Git_Repos\.claude\launch.json, so the
// local seed lands in the database `wrangler dev` reads.
const persist = where === '--local' ? ['--persist-to', 'C:/Git_Repos/.wrangler-state/blessyourpaws'] : [];
const wrangler = (extra) => execFileSync(process.platform === 'win32' ? 'npx.cmd' : 'npx',
  ['-y', 'wrangler', 'd1', 'execute', 'blessyourpaws', where, ...persist, ...extra],
  { cwd: HERE, encoding: 'utf8', shell: process.platform === 'win32' });

if (where === '--remote') {
  let out = '';
  const probe = join(dir, 'probe.sql');
  writeFileSync(probe, 'SELECT count(*) AS n FROM records;\n');
  try { out = wrangler(['--json', '--file', probe, '--yes']); } catch { out = '[]'; }
  const m = /"n":\s*(\d+)/.exec(out);
  if (m && Number(m[1]) > 0) {
    console.error(`The live database already holds ${m[1]} records. Refusing to seed over them.`);
    process.exit(1);
  }
}
console.log(wrangler(['--file', sqlFile, '--yes']).split('\n').filter((l) => /rows|executed|Success|ERROR/i.test(l)).join('\n'));
