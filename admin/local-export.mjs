#!/usr/bin/env node
// What a publish from the LOCAL editor would commit, written into a folder of your choice.
//
//     node admin/local-export.mjs <out-dir>
//
// Reads the wrangler dev database (the byp-editor launch entry's --persist-to), runs the same
// exportAll the Worker publishes with, and writes data/*.json plus every uploaded photo under
// uploads/. Point it at a scratch copy of the repo, never this one: the files it writes are what
// the next publish would replace, and a copy lets the real build and site-checks run on them.

import { DatabaseSync } from 'node:sqlite';
import { readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { nodeDb } from './lib/db.mjs';
import { exportAll } from './lib/files.mjs';

const out = process.argv[2];
if (!out) { console.error('usage: node admin/local-export.mjs <out-dir>'); process.exit(2); }
const D = 'C:/Git_Repos/.wrangler-state/blessyourpaws/v3/d1/miniflare-D1DatabaseObject';
const file = readdirSync(D).find((f) => f.endsWith('.sqlite') && f !== 'metadata.sqlite');
const sqlite = new DatabaseSync(join(D, file), { readOnly: true });
const db = nodeDb(sqlite);
for (const [path, text] of Object.entries(await exportAll(db))) {
  mkdirSync(dirname(join(out, path)), { recursive: true });
  writeFileSync(join(out, path), text);
  console.log('wrote', path);
}
for (const u of sqlite.prepare('SELECT repo_path, data FROM uploads').all()) {
  mkdirSync(dirname(join(out, u.repo_path)), { recursive: true });
  writeFileSync(join(out, u.repo_path), Buffer.from(u.data));
  console.log('wrote', u.repo_path);
}
