// Reads, writes and the rules that keep an owner's edit from breaking the site.
//
// Every write goes through here. Each one checks the record's version, so when Hope and Joy
// have the same puppy open the second save is refused rather than silently overwriting the
// first, and each one leaves an audit row.
//
// Every edit is a merge into the stored record: a key that exists keeps its place, so the
// export keeps the file's key order without a shape table.

import { d1Db } from '../lib/db.mjs';
import { FILES, listOf } from '../lib/files.mjs';
import { HttpError } from './http.js';

export const NOW = () => new Date().toISOString();
export const db = (env) => d1Db(env.DB);

export const STATUSES = ['available', 'reserved', 'adopted'];
export const SEXES = ['Boy', 'Girl'];
// Slugs the site already uses for something else, so a new puppy can never take one.
const RESERVED_SLUGS = new Set(['elowen', 'malcolm', 'griffin', 'mira', 'troy', 'bip-finch',
  'index', 'puppies', 'parents', 'gallery', 'contact', 'apply', 'waitlist', 'sign']);

export async function getPersonByEmail(env, email) {
  if (!email) return null;
  const rows = await db(env).all('SELECT * FROM people WHERE email = ? COLLATE NOCASE', [email]);
  return rows[0] || null;
}

export async function audit(env, { file = null, key = null, action, detail = '', actor }) {
  await db(env).run(
    'INSERT INTO audit (file, key, action, detail, actor, created_at) VALUES (?, ?, ?, ?, ?, ?)',
    [file, key, action, String(detail).slice(0, 500), actor, NOW()]);
}

export async function all(env, file) {
  return listOf(db(env), file);
}

export async function getRecord(env, file, key) {
  const rows = await db(env).all(
    'SELECT key, doc, version, sort_order FROM records WHERE file = ? AND key = ?', [file, key]);
  if (!rows.length) throw new HttpError(404, 'That is not here any more. Reload and try again.');
  return { key: rows[0].key, version: rows[0].version, sort: rows[0].sort_order, doc: JSON.parse(rows[0].doc) };
}

/** Save a whole record, refusing if someone else saved it since it was opened. */
async function save(env, file, key, doc, version, actor, action, detail) {
  const res = await db(env).run(
    `UPDATE records SET doc = ?, version = version + 1, updated_at = ?, updated_by = ?
      WHERE file = ? AND key = ? AND version = ?`,
    [JSON.stringify(doc), NOW(), actor, file, key, version]);
  const changed = res && res.meta ? res.meta.changes : (res && res.changes);
  if (!changed) {
    throw new HttpError(409, 'Someone else saved this a moment ago. Reload to see their change, then make yours.');
  }
  await audit(env, { file, key, action, detail, actor });
  return getRecord(env, file, key);
}

async function insert(env, file, key, doc, actor, action, detail) {
  const [{ n }] = await db(env).all('SELECT coalesce(max(sort_order), -1) + 1 AS n FROM records WHERE file = ?', [file]);
  await db(env).run(
    `INSERT INTO records (file, key, doc, sort_order, version, updated_at, updated_by)
     VALUES (?, ?, ?, ?, 1, ?, ?)`, [file, key, JSON.stringify(doc), n, NOW(), actor]);
  await audit(env, { file, key, action, detail, actor });
  return getRecord(env, file, key);
}

// ---- small validators ------------------------------------------------------------------

function text(v, label, max, { required = false } = {}) {
  if (v === undefined || v === null) v = '';
  if (typeof v !== 'string') throw new HttpError(400, `${label} should be text.`);
  const t = v.replace(/\s+/g, ' ').trim();
  if (required && !t) throw new HttpError(400, `${label} cannot be empty.`);
  if (t.length > max) throw new HttpError(400, `${label} is longer than ${max} characters.`);
  return t;
}

function longText(v, label, max) {
  if (typeof v !== 'string') throw new HttpError(400, `${label} should be text.`);
  const t = v.replace(/\r\n/g, '\n').replace(/[ \t]+/g, ' ').replace(/\n+/g, ' ').trim();
  if (!t) throw new HttpError(400, `${label} cannot be empty.`);
  if (t.length > max) throw new HttpError(400, `${label} is longer than ${max} characters.`);
  return t;
}

function isoDate(v, label) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(v) || Number.isNaN(Date.parse(v))) {
    throw new HttpError(400, `${label} should be a date.`);
  }
  return v;
}

/** Whole dollars in a sensible range. The site shows them as $2,060, so no cents. */
function dollars(v, label, min, max) {
  const n = typeof v === 'string' ? Number(v.replace(/[$,\s]/g, '')) : v;
  if (!Number.isInteger(n)) throw new HttpError(400, `${label} should be whole dollars, like 2060.`);
  if (n < min || n > max) throw new HttpError(400, `${label} should be between $${min.toLocaleString('en-US')} and $${max.toLocaleString('en-US')}.`);
  return n;
}

/** The three amounts on a litter, checked against each other. */
function money(body, cur = {}) {
  const price = 'price' in body ? dollars(body.price, 'Price', 300, 20000) : cur.price;
  const cash = 'cash_price' in body ? dollars(body.cash_price, 'Cash price', 300, 20000) : cur.cash_price;
  const deposit = 'deposit' in body ? dollars(body.deposit, 'Deposit', 50, 5000) : cur.deposit;
  if (price === undefined || cash === undefined || deposit === undefined) throw new HttpError(400, 'A litter needs a price, a cash price and a deposit.');
  if (cash > price) throw new HttpError(400, 'The cash price should not be more than the price.');
  if (deposit >= cash) throw new HttpError(400, 'The deposit should be less than the cash price.');
  return { price, cash_price: cash, deposit };
}

function slugify(name) {
  return name.toLowerCase().normalize('NFKD').replace(/[^\w\s-]/g, '').replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-').replace(/^-|-$/g, '');
}

/** Merge `changes` into `doc`: existing keys keep their place, so the file keeps its key order. */
function merge(doc, changes) {
  const out = { ...doc };
  for (const [k, v] of Object.entries(changes)) out[k] = v;
  return out;
}

// ---- puppies -----------------------------------------------------------------------------

/** Stems a puppy may name: photos it already has, and photos uploaded for it. */
async function ownedStems(env, file, key, doc) {
  const rows = await db(env).all('SELECT stem FROM uploads WHERE owner_file = ? AND owner_key = ?', [file, key]);
  return new Set([...(doc.photos || []), ...rows.map((r) => r.stem)]);
}

export async function updatePuppy(env, slug, body, actor) {
  const cur = await getRecord(env, 'puppies', slug);
  const ch = {};
  const notes = [];
  if ('name' in body) ch.name = text(body.name, 'Name', 40, { required: true });
  if ('sex' in body) {
    if (!SEXES.includes(body.sex)) throw new HttpError(400, 'Sex should be Boy or Girl.');
    ch.sex = body.sex;
  }
  if ('color' in body) ch.color = text(body.color, 'Color', 60, { required: true });
  if ('note' in body) ch.note = text(body.note, 'Note', 200);
  if ('status' in body) {
    if (!STATUSES.includes(body.status)) throw new HttpError(400, 'That is not a status.');
    if (body.status !== cur.doc.status) notes.push(`status ${cur.doc.status} to ${body.status}`);
    ch.status = body.status;
  }
  if ('photos' in body || 'page_photos' in body) {
    const owned = await ownedStems(env, 'puppies', slug, cur.doc);
    const photos = 'photos' in body ? body.photos : cur.doc.photos;
    const page = 'page_photos' in body ? body.page_photos : cur.doc.page_photos;
    if (!Array.isArray(photos) || !Array.isArray(page)) throw new HttpError(400, 'Photos should be a list.');
    if (photos.some((p) => !owned.has(p))) throw new HttpError(400, 'A photo there does not belong to this puppy.');
    if (new Set(photos).size !== photos.length) throw new HttpError(400, 'A photo is listed twice.');
    // Nothing is ever removed: every photo the puppy had stays in its gallery list.
    for (const p of cur.doc.photos) if (!photos.includes(p)) throw new HttpError(400, 'Photos cannot be removed, only hidden from the puppy page.');
    if (page.some((p) => !photos.includes(p))) throw new HttpError(400, 'The page can only show this puppy\'s own photos.');
    if (new Set(page).size !== page.length) throw new HttpError(400, 'A photo is shown twice.');
    if (photos.length && !page.length) throw new HttpError(400, 'Keep at least one photo on the puppy page.');
    ch.photos = photos;
    ch.page_photos = page;
    notes.push('photos');
  }
  if (!Object.keys(ch).length) return cur;
  const detail = notes.length ? notes.join(', ') : Object.keys(ch).join(', ');
  return save(env, 'puppies', slug, merge(cur.doc, ch), Number(body.version), actor,
    'status' in ch && ch.status !== cur.doc.status ? 'status' : 'save', detail);
}

export async function createPuppy(env, body, actor) {
  const litter = await getRecord(env, 'litters', text(body.litter, 'Litter', 80, { required: true }));
  if (litter.doc.status !== 'current') throw new HttpError(400, 'New puppies go in a current litter.');
  const name = text(body.name, 'Name', 40, { required: true });
  if (!SEXES.includes(body.sex)) throw new HttpError(400, 'Sex should be Boy or Girl.');
  const color = text(body.color, 'Color', 60, { required: true });
  const base = slugify(name);
  if (!base) throw new HttpError(400, 'That name needs at least one letter.');
  const taken = new Set((await db(env).all("SELECT key FROM records WHERE file = 'puppies'")).map((r) => r.key));
  let slug = base;
  for (let n = 2; taken.has(slug) || RESERVED_SLUGS.has(slug); n += 1) slug = `${base}-${n}`;
  const doc = { slug, litter: litter.key, name, sex: body.sex, color, note: '', status: 'available', photos: [], page_photos: [] };
  return insert(env, 'puppies', slug, doc, actor, 'add-puppy', `${name} in ${litter.key}`);
}

// ---- litters -----------------------------------------------------------------------------

export async function updateLitter(env, slug, body, actor) {
  const cur = await getRecord(env, 'litters', slug);
  const ch = {};
  if ('born' in body) ch.born = isoDate(body.born, 'Born');
  if ('home' in body) ch.home = isoDate(body.home, 'Can go home');
  if ('size' in body) ch.size = text(body.size, 'Expected adult size', 40, { required: true });
  if ('parents_phrase' in body) ch.parents_phrase = text(body.parents_phrase, 'Parents sentence', 200, { required: true });
  if ('parents_short' in body) ch.parents_short = text(body.parents_short, 'Short parents line', 120, { required: true });
  if ('price' in body || 'cash_price' in body || 'deposit' in body) {
    const m = money(body, cur.doc);
    for (const k of Object.keys(m)) if (m[k] !== cur.doc[k]) ch[k] = m[k];
  }
  if ('status' in body) {
    if (!['current', 'past'].includes(body.status)) throw new HttpError(400, 'That is not a litter status.');
    if (body.status === 'past' && cur.doc.status !== 'past') {
      const pups = (await all(env, 'puppies')).filter((p) => p.doc.litter === slug);
      const left = pups.filter((p) => p.doc.status !== 'adopted');
      if (left.length) {
        throw new HttpError(400, `Every puppy needs to be adopted first. Still to go: ${left.map((p) => p.doc.name).join(', ')}.`);
      }
    }
    ch.status = body.status;
  }
  const born = ch.born || cur.doc.born;
  const home = ch.home || cur.doc.home;
  if (home < born) throw new HttpError(400, 'Can go home should be after Born.');
  if (!Object.keys(ch).length) return cur;
  return save(env, 'litters', slug, merge(cur.doc, ch), Number(body.version), actor,
    'status' in ch && ch.status !== cur.doc.status ? (ch.status === 'past' ? 'retire' : 'unretire') : 'save',
    Object.keys(ch).join(', '));
}

export async function createLitter(env, body, actor) {
  const adults = Object.fromEntries((await all(env, 'adults')).map((a) => [a.key, a.doc]));
  const dam = adults[body.dam];
  const sire = adults[body.sire];
  if (!dam || dam.role !== 'Mom') throw new HttpError(400, 'Choose the mom from the parents on the site.');
  if (!sire || sire.role !== 'Dad') throw new HttpError(400, 'Choose the dad from the parents on the site.');
  const born = isoDate(body.born, 'Born');
  const home = isoDate(body.home, 'Can go home');
  if (home < born) throw new HttpError(400, 'Can go home should be after Born.');
  const size = text(body.size, 'Expected adult size', 40, { required: true });
  // A new litter starts at the newest litter's prices unless the form says otherwise.
  const prev = (await all(env, 'litters')).map((l) => l.doc).pop() || {};
  const m = money(body, prev);
  const taken = new Set((await db(env).all("SELECT key FROM records WHERE file = 'litters'")).map((r) => r.key));
  const base = `${body.dam}-${body.sire}-${born.slice(0, 7)}`;
  let slug = base;
  for (let n = 2; taken.has(slug); n += 1) slug = `${base}-${n}`;
  const doc = {
    slug,
    breed: 'Munchkin Bernedoodle',
    dam: body.dam,
    sire: body.sire,
    born,
    home,
    size,
    parents_phrase: text(body.parents_phrase || `${dam.name}, our ${dam.breed}, and ${sire.name}, our ${sire.breed}`,
      'Parents sentence', 200, { required: true }),
    parents_short: text(body.parents_short || `a ${dam.breed} mom and a ${sire.breed} dad`,
      'Short parents line', 120, { required: true }),
    photo: 'litter-01',
    status: 'current',
    ...m,
  };
  return insert(env, 'litters', slug, doc, actor, 'add-litter', slug);
}

// ---- parents -----------------------------------------------------------------------------

export async function updateAdult(env, slug, body, actor) {
  const cur = await getRecord(env, 'adults', slug);
  const ch = {};
  if ('story' in body) ch.story = longText(body.story, 'Story', 1200);
  if ('facts' in body) {
    if (!Array.isArray(body.facts) || body.facts.length !== cur.doc.facts.length) throw new HttpError(400, 'The card facts keep their labels.');
    ch.facts = cur.doc.facts.map(([k], i) => [k, text(body.facts[i], k, 80, { required: true })]);
  }
  if ('health' in body) {
    if (!Array.isArray(body.health) || body.health.length !== cur.doc.health.length) throw new HttpError(400, 'The health lines keep their labels.');
    ch.health = cur.doc.health.map(([k], i) => [k, longText(body.health[i], k, 400)]);
  }
  if ('photo' in body) {
    const owned = await db(env).all('SELECT stem FROM uploads WHERE owner_file = ? AND owner_key = ?', ['adults', slug]);
    const ok = new Set([cur.doc.photo, ...(cur.doc.photo_history || []), ...owned.map((r) => r.stem)]);
    if (!ok.has(body.photo)) throw new HttpError(400, 'That photo does not belong to this parent.');
    ch.photo = body.photo;
  }
  if (!Object.keys(ch).length) return cur;
  return save(env, 'adults', slug, merge(cur.doc, ch), Number(body.version), actor, 'save', Object.keys(ch).join(', '));
}

// ---- reviews -----------------------------------------------------------------------------

function reviewFields(body) {
  return {
    title: text(body.title, 'Title', 80),
    quote: longText(body.quote, 'Review', 1500),
    attribution: text(body.attribution, 'Who it is from', 120, { required: true }),
  };
}

export async function updateReview(env, key, body, actor) {
  const cur = await getRecord(env, 'reviews', key);
  const ch = {};
  if ('quote' in body || 'title' in body || 'attribution' in body) Object.assign(ch, reviewFields({ ...cur.doc, ...body }));
  if ('hidden' in body) ch.hidden = !!body.hidden;
  if (!Object.keys(ch).length) return cur;
  return save(env, 'reviews', key, merge(cur.doc, ch), Number(body.version), actor,
    'hidden' in ch && ch.hidden !== cur.doc.hidden ? (ch.hidden ? 'hide' : 'show') : 'save', Object.keys(ch).join(', '));
}

export async function createReview(env, body, actor) {
  const f = reviewFields(body);
  const key = `review-${Date.now().toString(36)}`;
  return insert(env, 'reviews', key, { ...f, hidden: false }, actor, 'add-review', f.attribution);
}

/** Move one record up or down within its file. Order is site order. */
export async function move(env, file, key, dir, actor) {
  const rows = await db(env).all('SELECT key, sort_order FROM records WHERE file = ? ORDER BY sort_order, key', [file]);
  const i = rows.findIndex((r) => r.key === key);
  const j = dir === 'up' ? i - 1 : i + 1;
  if (i < 0) throw new HttpError(404, 'That is not here any more.');
  if (j < 0 || j >= rows.length) return;
  const order = rows.map((r) => r.key);
  [order[i], order[j]] = [order[j], order[i]];
  for (let n = 0; n < order.length; n += 1) {
    await db(env).run('UPDATE records SET sort_order = ? WHERE file = ? AND key = ?', [n, file, order[n]]);
  }
  await audit(env, { file, key, action: 'move', detail: dir, actor });
}

export { FILES };
