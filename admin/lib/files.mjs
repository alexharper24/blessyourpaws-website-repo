// The four files the editor owns, and the only code that turns rows into them and back.
//
// data/*.json is read by scripts/scaffold.py. The export has to reproduce each file to the
// byte, because every publish writes the whole file and a stray difference is a change to
// the site nobody asked for. scaffold.py writes nothing here; Python's
// json.dump(obj, indent=2, ensure_ascii=False) and JSON.stringify(obj, null, 2) produce the
// same bytes for this data, which roundtrip.mjs checks rather than assumes. Every file ends
// with one newline.
//
// The same module runs in the Worker and on a laptop, so what the round-trip gate tests is
// what ships.

export const FILES = {
  puppies: 'data/puppies.json',
  litters: 'data/litters.json',
  adults: 'data/adults.json',
  reviews: 'data/reviews.json',
};

/** The key a record is stored under. Reviews have no slug, so they carry an id. */
export function keyOf(file, rec, i) {
  if (file === 'reviews') return rec.id || `review-${String(i + 1).padStart(2, '0')}`;
  return rec.slug;
}

/**
 * Reviews in the file have no id, and the site does not need one. The database needs a
 * stable key, so it is kept beside the record rather than in it: the stored doc never has
 * an `id`, and the export never writes one.
 */
export function stripKey(file, rec) {
  if (file !== 'reviews' || !('id' in rec)) return rec;
  const { id, ...rest } = rec;
  return rest;
}

export function dump(list) {
  return `${JSON.stringify(list, null, 2)}\n`;
}

/** Rows of one file, in site order. */
export async function listOf(db, file) {
  const rows = await db.all(
    'SELECT key, doc, version FROM records WHERE file = ? ORDER BY sort_order, key', [file]);
  return rows.map((r) => ({ key: r.key, version: r.version, doc: JSON.parse(r.doc) }));
}

/** Every file the editor owns, as it should be in the repository. */
export async function exportAll(db) {
  const out = {};
  for (const [file, path] of Object.entries(FILES)) {
    out[path] = dump((await listOf(db, file)).map((r) => r.doc));
  }
  return out;
}

/** data/*.json into an empty database. INSERT OR REPLACE, no transaction (remote D1 rejects BEGIN). */
export async function seedAll(db, read, actor = 'seed') {
  const counts = {};
  const now = new Date().toISOString();
  for (const [file, path] of Object.entries(FILES)) {
    const list = JSON.parse(read(path));
    let i = 0;
    for (const rec of list) {
      await db.run(
        `INSERT OR REPLACE INTO records (file, key, doc, sort_order, version, updated_at, updated_by)
         VALUES (?, ?, ?, ?, 1, ?, ?)`,
        [file, keyOf(file, rec, i), JSON.stringify(stripKey(file, rec)), i, now, actor]);
      i += 1;
    }
    counts[file] = list.length;
  }
  return counts;
}
