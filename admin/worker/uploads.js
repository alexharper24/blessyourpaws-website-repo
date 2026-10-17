// Photographs, from a phone into the repository.
//
// The browser resizes before it sends (public/admin.js), so what arrives is a JPEG of at
// most 2400px. It is held in R2 (FILES) and copied into the repository by the next publish,
// in the
// same commit as the data that names it, so the site can never ship a page pointing at a
// photo nobody committed.
//
// The name chosen here is the stem data/*.json uses: a puppy's next free <slug>-NN. The file
// goes to uploads/puppies/<stem>.jpg (or uploads/dogs/ for a parent), and the site build's
// scripts/encode_uploads.py turns it into img/puppies/<stem>.jpg and the webp sizes. Nothing
// is ever overwritten: every upload is a new number.

import { audit, db, getRecord, NOW } from './store.js';
import { HttpError, json } from './http.js';

const MAX_BYTES = 12 * 1024 * 1024;
const FOLDER = { puppies: 'puppies', adults: 'dogs' };

function stemPrefix(file, rec) {
  if (file === 'puppies') return rec.slug;
  return rec.slug;
}

/** The next free number for this record, across its photos and anything uploaded for it. */
async function nextStem(env, file, rec) {
  const prefix = stemPrefix(file, rec);
  const used = new Set([...(rec.photos || []), rec.photo].filter(Boolean));
  for (const r of await db(env).all('SELECT stem FROM uploads WHERE stem LIKE ?', [`${prefix}-%`])) used.add(r.stem);
  let max = 0;
  const re = new RegExp(`^${prefix.replace(/[-]/g, '\\-')}-(\\d{2,3})$`);
  for (const s of used) {
    const m = re.exec(s);
    if (m) max = Math.max(max, Number(m[1]));
  }
  return `${prefix}-${String(max + 1).padStart(2, '0')}`;
}

export async function handleUpload(request, env, url, who) {
  if (request.method !== 'POST') throw new HttpError(405, 'Use POST to upload.');
  const file = url.searchParams.get('file');
  const key = url.searchParams.get('key') || '';
  if (!FOLDER[file]) throw new HttpError(400, 'Photos attach to a puppy or a parent.');
  const type = (request.headers.get('Content-Type') || '').split(';')[0].trim();
  if (type !== 'image/jpeg') throw new HttpError(415, 'The editor sends photos as JPEG. Reload and try again.');
  const bytes = await request.arrayBuffer();
  if (!bytes.byteLength) throw new HttpError(400, 'That photo arrived empty.');
  if (bytes.byteLength > MAX_BYTES) throw new HttpError(413, 'That photo is too large even after resizing. Try a different photo.');

  const rec = await getRecord(env, file, key);
  const stem = await nextStem(env, file, rec.doc);
  const repoPath = `uploads/${FOLDER[file]}/${stem}.jpg`;
  const r2Key = `pending/${FOLDER[file]}/${stem}.jpg`;
  await env.FILES.put(r2Key, bytes, { httpMetadata: { contentType: 'image/jpeg' } });
  await db(env).run(
    `INSERT INTO uploads (key, repo_path, stem, owner_file, owner_key, bytes, committed, created_at, created_by)
     VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)`,
    [r2Key, repoPath, stem, file, key, bytes.byteLength, NOW(), who.email]);
  await audit(env, { file, key, action: 'upload', detail: stem, actor: who.email });
  return json({ stem, preview: `/uploads/${FOLDER[file]}/${stem}.jpg` });
}

/** An uploaded photo, shown back to the editor before it is on the site. Behind Access. */
export async function handlePreview(env, url) {
  const p = url.pathname.replace(/^\/uploads\//, '');
  if (!/^(puppies|dogs)\/[a-z0-9-]+\.jpg$/.test(p)) throw new HttpError(400, 'Not a photo path.');
  const obj = await env.FILES.get(`pending/${p}`);
  if (!obj) throw new HttpError(404, 'That photo is not here any more.');
  return new Response(obj.body, {
    headers: { 'Content-Type': 'image/jpeg', 'Cache-Control': 'private, max-age=86400' },
  });
}

/** Stem to a URL the editor can show: the uploaded copy until it is built, then the site's. */
export async function photoUrls(env) {
  const rows = await db(env).all('SELECT stem, repo_path, committed FROM uploads');
  const map = {};
  for (const r of rows) map[r.stem] = { pending: `/${r.repo_path}`, committed: !!r.committed };
  return map;
}
