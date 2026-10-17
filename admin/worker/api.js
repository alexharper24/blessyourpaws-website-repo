// The editor's API. Every route is behind Cloudflare Access and the people table (index.js).
//
//   GET  /api/state                       everything the screens show, in one call
//   POST /api/puppies                     add a puppy to a current litter
//   POST /api/puppies/<slug>              edit, change status, or reorder photos
//   POST /api/litters                     start a litter
//   POST /api/litters/<slug>              edit, or move to past litters
//   POST /api/adults/<slug>               edit a parent
//   POST /api/reviews                     add a review
//   POST /api/reviews/<key>               edit, hide or show
//   POST /api/move                        { file, key, dir } reorder within a file
//   GET  /api/publish                     what a publish would change
//   POST /api/publish                     publish
//   POST /api/undo                        { file, key } put one record back to the site's copy
//   GET  /api/history                     publishes and recent edits
//   GET|POST /api/people                  invited people (admin only)
//
// There is no delete route for content, on purpose.

import * as S from './store.js';
import { pending, publish, undo, history } from './publish.js';
import { photoUrls } from './uploads.js';
import { HttpError, json } from './http.js';

async function body(request) {
  try {
    return await request.json();
  } catch {
    throw new HttpError(400, 'That request was not readable.');
  }
}

function admin(who) {
  if (!who.person.is_admin) throw new HttpError(403, 'Only Alex can change who has access.');
}

export async function handleApi(request, env, url, who) {
  const method = request.method;
  const parts = url.pathname.replace(/^\/api\/?/, '').split('/').filter(Boolean);
  const [what, id] = parts;
  const actor = who.email;
  const send = (rec) => json({ ok: true, record: rec });

  if (what === 'state' && method === 'GET') {
    const [puppies, litters, adults, reviews] = await Promise.all(
      ['puppies', 'litters', 'adults', 'reviews'].map((f) => S.all(env, f)));
    return json({
      me: { email: who.email, name: who.person.display_name, admin: !!who.person.is_admin, dev: who.dev },
      site: env.SITE_URL,
      puppies, litters, adults, reviews,
      uploads: await photoUrls(env),
      publishReady: !!env.GITHUB_TOKEN,
    });
  }

  if (method === 'POST') {
    if (what === 'puppies') return send(id ? await S.updatePuppy(env, id, await body(request), actor) : await S.createPuppy(env, await body(request), actor));
    if (what === 'litters') return send(id ? await S.updateLitter(env, id, await body(request), actor) : await S.createLitter(env, await body(request), actor));
    if (what === 'adults' && id) return send(await S.updateAdult(env, id, await body(request), actor));
    if (what === 'reviews') return send(id ? await S.updateReview(env, id, await body(request), actor) : await S.createReview(env, await body(request), actor));
    if (what === 'move') {
      const b = await body(request);
      if (!['puppies', 'reviews', 'adults'].includes(b.file)) throw new HttpError(400, 'That list cannot be reordered.');
      await S.move(env, b.file, b.key, b.dir === 'up' ? 'up' : 'down', actor);
      return json({ ok: true });
    }
    if (what === 'publish') {
      const r = await publish(env, who);
      return json(r, r.ok ? 200 : r.code || 500);
    }
    if (what === 'undo') {
      const b = await body(request);
      const r = await undo(env, b.file, b.key, actor);
      return json(r, r.ok ? 200 : r.code || 500);
    }
    if (what === 'people') {
      admin(who);
      const b = await body(request);
      const email = String(b.email || '').trim().toLowerCase();
      if (b.remove) {
        if (email === who.email.toLowerCase()) throw new HttpError(400, 'You cannot remove yourself.');
        await S.db(env).run('DELETE FROM people WHERE email = ? COLLATE NOCASE', [email]);
        await S.audit(env, { action: 'people-remove', detail: email, actor });
        return json({ ok: true });
      }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) throw new HttpError(400, 'That is not an email address.');
      const name = String(b.name || '').trim().slice(0, 60) || email;
      await S.db(env).run(
        'INSERT OR REPLACE INTO people (email, display_name, is_admin, added_at, added_by) VALUES (?, ?, ?, ?, ?)',
        [email, name, b.admin ? 1 : 0, S.NOW(), actor]);
      await S.audit(env, { action: 'people-add', detail: email, actor });
      return json({ ok: true });
    }
  }

  if (method === 'GET') {
    if (what === 'publish') {
      const r = await pending(env);
      return json(r, r.ok || r.notSetUp ? 200 : 500);
    }
    if (what === 'history') return json(await history(env));
    if (what === 'people') {
      admin(who);
      return json({ people: await S.db(env).all('SELECT email, display_name, is_admin, added_at FROM people ORDER BY added_at') });
    }
  }

  throw new HttpError(404, 'Nothing here.');
}
