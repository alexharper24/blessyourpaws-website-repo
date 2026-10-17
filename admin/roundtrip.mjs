#!/usr/bin/env node
// The gate on the editor's database.
//
//     node admin/roundtrip.mjs
//
// Seeds a throwaway SQLite database from data/*.json, exports it straight back, and compares
// the result with the files byte for byte (line endings normalized to LF, because git stores
// LF and the Windows working copy is CRLF). Nothing is deployed until this passes.
//
// It cannot tell you a file disagrees with the LIVE database. Only exporting the live D1
// does that, which is what publish's own check does before every commit.

import { readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { nodeDb } from './lib/db.mjs';
import { seedAll, exportAll } from './lib/files.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const read = (p) => readFileSync(join(ROOT, p), 'utf8');
const dir = mkdtempSync(join(tmpdir(), 'byp-roundtrip-'));
let failures = 0;
try {
  const sqlite = new DatabaseSync(join(dir, 'rt.sqlite'));
  sqlite.exec(read('admin/schema.sql'));
  const db = nodeDb(sqlite);
  const counts = await seedAll(db, read);
  console.log('seeded:', Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(', '));
  for (const [path, produced] of Object.entries(await exportAll(db))) {
    const onDisk = read(path).replace(/\r\n/g, '\n');
    if (onDisk === produced) {
      console.log(`  ok ${path}  ${produced.length} bytes`);
    } else {
      failures += 1;
      let i = 0;
      while (i < onDisk.length && onDisk[i] === produced[i]) i += 1;
      console.log(`  XX ${path} differs at byte ${i}`);
      console.log(`     disk  : ${JSON.stringify(onDisk.slice(Math.max(0, i - 50), i + 50))}`);
      console.log(`     export: ${JSON.stringify(produced.slice(Math.max(0, i - 50), i + 50))}`);
    }
  }
  sqlite.close();
} finally {
  try { rmSync(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 50 }); } catch {}
}
console.log(failures ? `\nROUND TRIP FAILED: ${failures} file(s)` : '\nRound trip clean: every file reproduced byte for byte.');
process.exit(failures ? 1 : 0);
