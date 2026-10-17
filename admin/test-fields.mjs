#!/usr/bin/env node
// node test-fields.mjs  -- the litter price, per-puppy price and litter photo rules in
// worker/store.js, against an in-memory database seeded from data/*.json. Prints one line.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { nodeDb } from './lib/db.mjs';
import { seedAll, exportAll } from './lib/files.mjs';
import * as S from './worker/store.js';

const R = new URL('../', import.meta.url);
const sq = new DatabaseSync(':memory:');
sq.exec(readFileSync(new URL('admin/schema.sql', R), 'utf8'));
await seedAll(nodeDb(sq), (p) => readFileSync(new URL(p, R), 'utf8').replace(/\r\n/g, '\n'));
const DB = { prepare: (sql) => ({ bind: (...a) => ({
  all: async () => ({ results: sq.prepare(sql).all(...a) }),
  run: async () => { const r = sq.prepare(sql).run(...a); return { meta: { changes: r.changes } }; } }) }) };
const env = { DB };
const fails = [];
const check = (label, ok) => { if (!ok) fails.push(label); };
const status = async (label, fn) => { try { await fn(); return 'ok'; } catch (e) { return e.status || String(e); } };
const ver = async (f, k) => (await S.getRecord(env, f, k)).version;
const pup = JSON.parse(readFileSync(new URL('data/puppies.json', R), 'utf8')).find((p) => p.status === 'available').slug;
const lit = JSON.parse(readFileSync(new URL('data/litters.json', R), 'utf8'))[0].slug;
const file = async (n) => (await exportAll(nodeDb(sq)))[`data/${n}.json`];
const orig = await file('puppies');

// per-puppy price
check('one of two refused', await status('', async () => S.updatePuppy(env, pup, { price: 2200, cash_price: '', version: await ver('puppies', pup) }, 't')) === 400);
check('cash above price refused', await status('', async () => S.updatePuppy(env, pup, { price: 2100, cash_price: 2200, version: await ver('puppies', pup) }, 't')) === 400);
check('cash at or below deposit refused', await status('', async () => S.updatePuppy(env, pup, { price: 600, cash_price: 500, version: await ver('puppies', pup) }, 't')) === 400);
check('blank on a puppy with no price is no change', await status('', async () => S.updatePuppy(env, pup, { price: '', cash_price: '', version: await ver('puppies', pup) }, 't')) === 'ok' && await file('puppies') === orig);
await S.updatePuppy(env, pup, { price: 2200, cash_price: 2140, version: await ver('puppies', pup) }, 't');
const d1 = (await S.getRecord(env, 'puppies', pup)).doc;
check('override saved at the end of the record', d1.price === 2200 && d1.cash_price === 2140 && Object.keys(d1).slice(-2).join() === 'price,cash_price');
await S.updatePuppy(env, pup, { price: '', cash_price: '', version: await ver('puppies', pup) }, 't');
check('clearing restores the file exactly', await file('puppies') === orig);

// litter photo
const v = await ver('litters', lit);
check('photo not owned refused', await status('', async () => S.updateLitter(env, lit, { photo: 'jordan-01', photo_alt: 'x', version: v }, 't')) === 400);
sq.prepare("INSERT INTO uploads (key, repo_path, stem, owner_file, owner_key, bytes, created_at, created_by) VALUES ('k', 'uploads/puppies/t.jpg', ?, 'litters', ?, 1, 'now', 't')").run(`${lit}-01`, lit);
check('new photo needs a description', await status('', async () => S.updateLitter(env, lit, { photo: `${lit}-01`, photo_alt: '', version: v }, 't')) === 400);
await S.updateLitter(env, lit, { photo: `${lit}-01`, photo_alt: 'The litter on a blanket', version: v }, 't');
const L = (await S.getRecord(env, 'litters', lit)).doc;
check('photo and description saved', L.photo === `${lit}-01` && L.photo_alt === 'The litter on a blanket');
const litFile = await file('litters');
await S.updateLitter(env, lit, { size: L.size, version: await ver('litters', lit) }, 't');
check('unrelated save leaves the photo alone', await file('litters') === litFile);

console.log(fails.length ? `FAIL: ${fails.join('; ')}` : 'ok: per-puppy price 6 checks, litter photo 4 checks');
process.exit(fails.length ? 1 : 0);
