// The database back into the website, as one commit.
//
// Publish writes data/*.json and every photo those files name that has been uploaded but
// never committed, in a single commit on main. Workers Builds then runs scripts/ci-build.sh
// (encode_uploads.py, then scaffold.py) and deploys. Adapted from the Teapup editor, which
// has published this way since 2026-09-12.
//
// It refuses rather than guesses: with no token it says publishing is not set up, with
// nothing changed it says so, with another publish running it waits, and if any photo the
// data names exists neither on the site nor in the uploads it stops before committing,
// because that build would fail.

import { exportAll, FILES } from '../lib/files.mjs';
import { audit, db, NOW } from './store.js';

const API = 'https://api.github.com';

function headers(env) {
  return {
    Authorization: `Bearer ${env.GITHUB_TOKEN}`,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'blessyourpaws-editor',
    'Content-Type': 'application/json',
  };
}

async function gh(env, path, init = {}) {
  const res = await fetch(`${API}/repos/${env.GITHUB_REPO}${path}`, { ...init, headers: headers(env) });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`GitHub ${init.method || 'GET'} ${path}: ${res.status} ${body.slice(0, 300)}`);
  }
  return res.json();
}

function toBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i += 0x8000) binary += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(binary);
}

/** The sha git gives this content, so unchanged files drop out without asking GitHub. */
async function gitBlobSha(bytes) {
  const header = new TextEncoder().encode(`blob ${bytes.byteLength}\0`);
  const joined = new Uint8Array(header.length + bytes.byteLength);
  joined.set(header, 0);
  joined.set(new Uint8Array(bytes), header.length);
  const digest = await crypto.subtle.digest('SHA-1', joined);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

async function tree(env, commitSha) {
  const commit = await gh(env, `/git/commits/${commitSha}`);
  const t = await gh(env, `/git/trees/${commit.tree.sha}?recursive=1`);
  const paths = new Map();
  for (const e of t.tree || []) if (e.type === 'blob') paths.set(e.path, e.sha);
  return { treeSha: commit.tree.sha, paths, truncated: !!t.truncated };
}

async function blobText(env, sha) {
  const blob = await gh(env, `/git/blobs/${sha}`);
  const raw = atob((blob.content || '').replace(/\n/g, ''));
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i += 1) bytes[i] = raw.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

/** Every photo stem the data names, with the folder it lives in. */
function stemsIn(files) {
  const out = [];
  for (const p of JSON.parse(files[FILES.puppies])) for (const s of p.photos) out.push(['puppies', s]);
  for (const a of JSON.parse(files[FILES.adults])) out.push(['dogs', a.photo]);
  return out;
}

/** The site as it is now, and what a publish would change. Shared by preview and publish. */
async function plan(env) {
  const files = await exportAll(db(env));
  const head = await gh(env, `/git/ref/heads/${env.GITHUB_BRANCH}`);
  const parent = head.object.sha;
  const { treeSha, paths, truncated } = await tree(env, parent);
  if (truncated) throw new Error('The repository listing came back truncated, so what changed cannot be known.');

  const uploads = await db(env).all('SELECT key, repo_path, stem, committed FROM uploads');
  const byStem = Object.fromEntries(uploads.map((u) => [u.stem, u]));
  const enc = new TextEncoder();
  const changed = [];
  const missing = [];
  const photos = [];
  for (const [folder, stem] of stemsIn(files)) {
    if (paths.has(`img/${folder}/${stem}.jpg`) || paths.has(`uploads/${folder}/${stem}.jpg`)) continue;
    const u = byStem[stem];
    if (!u) { missing.push(stem); continue; }
    photos.push(u);
  }
  for (const [path, text] of Object.entries(files)) {
    const bytes = enc.encode(text);
    if (paths.get(path) !== await gitBlobSha(bytes)) changed.push({ path, bytes, binary: false });
  }
  for (const u of photos) {
    const [row] = await db(env).all('SELECT data FROM uploads WHERE key = ?', [u.key]);
    if (!row || !row.data) { missing.push(u.stem); continue; }
    const bytes = row.data instanceof ArrayBuffer ? row.data : new Uint8Array(row.data).buffer;
    changed.push({ path: u.repo_path, bytes, binary: true, key: u.key });
  }
  return { files, parent, treeSha, paths, changed, missing };
}

const LABEL = {
  name: 'name', sex: 'boy or girl', color: 'color', note: 'note', status: 'status',
  photos: 'photos', page_photos: 'photos on the page', born: 'born date', home: 'go-home date',
  size: 'expected size', parents_phrase: 'parents sentence', parents_short: 'parents line',
  story: 'story', facts: 'card facts', health: 'health details', photo: 'photo', title: 'title',
  quote: 'review wording', attribution: 'who it is from', hidden: 'shown or hidden',
};

function nameOf(file, rec) {
  if (file === 'reviews') return `Review from ${rec.attribution}`;
  if (file === 'litters') return `Litter born ${rec.born}`;
  return rec.name;
}

/** Record-level differences between the site's copy of a file and the editor's. */
export function diffFile(file, was, now, nowKeys = []) {
  // Puppies, litters and parents match on slug. Reviews have no slug in the file, so they
  // match on who the review is from, and each change carries the review's database key
  // (nowKeys, in export order) so Undo can find it.
  const out = [];
  const ident = (r) => (file === 'reviews' ? r.attribution : r.slug);
  const a = new Map((was || []).map((r) => [ident(r), r]));
  const seen = new Set();
  (now || []).forEach((rec, i) => {
    const id = ident(rec);
    seen.add(id);
    const key = file === 'reviews' ? (nowKeys[i] || id) : rec.slug;
    const old = a.get(id);
    if (!old) { out.push({ file, key, what: `${nameOf(file, rec)} added` }); return; }
    const fields = Object.keys(rec).filter((f) => JSON.stringify(rec[f]) !== JSON.stringify(old[f]));
    if (!fields.length) return;
    const bits = fields.map((f) => (f === 'status'
      ? `${old.status} to ${rec.status}`
      : (f === 'photos' && rec.photos.length > old.photos.length)
        ? `${rec.photos.length - old.photos.length} new photo${rec.photos.length - old.photos.length === 1 ? '' : 's'}`
        : `${LABEL[f] || f} changed`));
    out.push({ file, key, what: `${nameOf(file, rec)}: ${[...new Set(bits)].join(', ')}` });
  });
  if (file !== 'reviews') for (const [id, rec] of a) if (!seen.has(id)) out.push({ file, key: id, what: `${nameOf(file, rec)} is not in the editor` });
  return out;
}

export async function pending(env) {
  if (!env.GITHUB_TOKEN) return { ok: false, notSetUp: true, error: 'Publishing is not set up yet. Alex needs to add the repository token.' };
  const p = await plan(env);
  const list = [];
  for (const [file, path] of Object.entries(FILES)) {
    const now = JSON.parse(p.files[path]);
    const sha = p.paths.get(path);
    const was = sha ? JSON.parse(await blobText(env, sha)) : [];
    if (JSON.stringify(was) === JSON.stringify(now)) continue;
    const keys = file === 'reviews' ? (await db(env).all("SELECT key FROM records WHERE file = 'reviews' ORDER BY sort_order, key")).map((r) => r.key) : [];
    list.push(...diffFile(file, was, now, keys));
  }
  const [last] = await db(env).all("SELECT actor, finished_at FROM publishes WHERE outcome = 'ok' ORDER BY id DESC LIMIT 1");
  return { ok: true, changes: list, photos: p.changed.filter((c) => c.binary).length, missing: p.missing, last: last || null };
}

export async function publish(env, who) {
  if (!env.GITHUB_TOKEN) return { ok: false, code: 503, error: 'Publishing is not set up yet. Alex needs to add the repository token.' };
  const running = await db(env).all(
    "SELECT id FROM publishes WHERE finished_at IS NULL AND started_at > datetime('now', '-5 minutes')");
  if (running.length) return { ok: false, code: 409, error: 'A publish is already running. Give it a moment.' };

  const p = await plan(env);
  if (p.missing.length) {
    return { ok: false, code: 409, error: `These photos are named but missing, so the site would not build: ${p.missing.join(', ')}. Nothing was published.` };
  }
  const summary = { files: p.changed.map((c) => c.path), photos: p.changed.filter((c) => c.binary).length };
  if (!p.changed.length) return { ok: true, nothing: true, message: 'Everything here is already on the site.' };

  const [{ id }] = await db(env).all(
    'INSERT INTO publishes (actor, summary_json, started_at) VALUES (?, ?, ?) RETURNING id',
    [who.email, JSON.stringify(summary), NOW()]);
  try {
    const entries = [];
    for (const c of p.changed) {
      const blob = await gh(env, '/git/blobs', {
        method: 'POST',
        body: JSON.stringify(c.binary
          ? { content: toBase64(c.bytes), encoding: 'base64' }
          : { content: new TextDecoder().decode(c.bytes), encoding: 'utf-8' }),
      });
      entries.push({ path: c.path, mode: '100644', type: 'blob', sha: blob.sha });
    }
    const newTree = await gh(env, '/git/trees', { method: 'POST', body: JSON.stringify({ base_tree: p.treeSha, tree: entries }) });
    const n = summary.photos;
    const commit = await gh(env, '/git/commits', {
      method: 'POST',
      body: JSON.stringify({
        message: `Update from the editor\n\nPublished by ${who.person.display_name || who.email} from the Bless Your Paws editor.\n`
          + `${p.changed.length - n} data file${p.changed.length - n === 1 ? '' : 's'}${n ? `, ${n} photo${n === 1 ? '' : 's'}` : ''}.`,
        tree: newTree.sha,
        parents: [p.parent],
      }),
    });
    await gh(env, `/git/refs/heads/${env.GITHUB_BRANCH}`, { method: 'PATCH', body: JSON.stringify({ sha: commit.sha, force: false }) });
    for (const c of p.changed) if (c.key) await db(env).run('UPDATE uploads SET committed = 1 WHERE key = ?', [c.key]);
    await db(env).run("UPDATE publishes SET commit_sha = ?, finished_at = ?, outcome = 'ok' WHERE id = ?", [commit.sha, NOW(), id]);
    await audit(env, { action: 'publish', detail: `${commit.sha.slice(0, 7)}: ${p.changed.length} files`, actor: who.email });
    return { ok: true, commit: commit.sha, summary };
  } catch (err) {
    await db(env).run("UPDATE publishes SET finished_at = ?, outcome = 'failed', summary_json = ? WHERE id = ?",
      [NOW(), JSON.stringify({ ...summary, error: String(err.message || err) }), id]);
    return { ok: false, code: 502, error: `The site was not updated: ${err.message || err}` };
  }
}

/** Put one record back to the version on the site, or take away one the site never had. */
export async function undo(env, file, key, actor) {
  if (!env.GITHUB_TOKEN) return { ok: false, code: 503, error: 'Publishing is not set up yet.' };
  if (!FILES[file]) return { ok: false, code: 400, error: 'Nothing to undo there.' };
  const head = await gh(env, `/git/ref/heads/${env.GITHUB_BRANCH}`);
  const { paths } = await tree(env, head.object.sha);
  const sha = paths.get(FILES[file]);
  const list = sha ? JSON.parse(await blobText(env, sha)) : [];
  const rows = await db(env).all('SELECT key, doc FROM records WHERE file = ?', [file]);
  let published = null;
  if (file === 'reviews') {
    const row = rows.find((r) => r.key === key);
    const doc = row && JSON.parse(row.doc);
    published = doc ? list.find((r) => r.attribution === doc.attribution) || null : null;
  } else {
    published = list.find((r) => r.slug === key) || null;
  }
  if (!published && file === 'reviews' && /^review-\d+$/.test(key)) {
    // A review that came from the site but whose name was edited cannot be matched back to
    // its published copy, and taking it away would lose a real review. Refuse instead.
    return { ok: false, code: 409, error: 'That review cannot be put back automatically. Edit it back by hand.' };
  }
  if (!published) {
    await db(env).run('DELETE FROM records WHERE file = ? AND key = ?', [file, key]);
    await audit(env, { file, key, action: 'undo', detail: 'not on the site, so taken away', actor });
    return { ok: true, removed: true };
  }
  await db(env).run(
    'UPDATE records SET doc = ?, version = version + 1, updated_at = ?, updated_by = ? WHERE file = ? AND key = ?',
    [JSON.stringify(published), NOW(), actor, file, key]);
  await audit(env, { file, key, action: 'undo', detail: 'put back to the site version', actor });
  return { ok: true, restored: true };
}

export async function history(env) {
  const publishes = await db(env).all(
    'SELECT id, actor, commit_sha, summary_json, started_at, finished_at, outcome FROM publishes ORDER BY id DESC LIMIT 15');
  const recent = await db(env).all('SELECT file, key, action, detail, actor, created_at FROM audit ORDER BY id DESC LIMIT 60');
  return { publishes, recent };
}
