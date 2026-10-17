// The Bless Your Paws owner editor, at admin.blessyourpawspuppies.com.
//
// Entirely private, and a separate Worker from the site on purpose: Cloudflare Access covers
// this whole Worker, and a mistake in here takes down an editor nobody can reach rather than
// the public site. The site Worker is untouched by anything in this folder.
//
//   admin/public/   the editor shell, from the assets binding
//   /api/*          the API (worker/api.js)
//   /uploads/*      previews of photos uploaded but not yet published
//
// Identity is checked again here and FAILS CLOSED (identity.js). Getting past Access is not
// enough: the address also has to be in the people table, and there is no sign-up.

import { getPersonByEmail } from './store.js';
import { handleApi } from './api.js';
import { identify } from './identity.js';
import { handleUpload, handlePreview } from './uploads.js';
import { HttpError, json } from './http.js';
import { WorkerEntrypoint } from 'cloudflare:workers';
import { paymentCleared } from './payments.js';

/**
 * Reachable only through a service binding (the site Worker's EDITOR binding names this
 * entrypoint). Not routed from any hostname, so Access does not apply and is not needed:
 * the site Worker verifies Stripe's signature before it calls.
 */
export class Internal extends WorkerEntrypoint {
  async paymentCleared(p) {
    return paymentCleared(this.env, p);
  }
}

function guarded(res) {
  const h = new Headers(res.headers);
  h.set('X-Content-Type-Options', 'nosniff');
  h.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  h.set('X-Frame-Options', 'DENY');
  h.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
  if (!h.has('Cache-Control')) h.set('Cache-Control', 'no-store');
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
}

/** Who is turned away, and why, in words that say what to do about it. */
function refusal(reason, wantsJson) {
  if (wantsJson) return json({ error: reason }, 403);
  return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Not signed in &middot; Bless Your Paws</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/paw.png">
<style>
  :root { color-scheme: light only }
  * { box-sizing: border-box }
  body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 2rem 1.25rem;
    background: #223d2c; color: #223d2c; font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif }
  .card { width: min(30rem, 100%); background: #fff; border-radius: 4px; overflow: hidden;
    box-shadow: 0 18px 50px rgba(0,0,0,.25) }
  .top { background: #fbe9ee; padding: 1.4rem; text-align: center }
  .top img { width: 13rem; height: auto }
  .body { padding: 1.5rem 1.6rem 1.7rem }
  h1 { margin: 0 0 .5rem; font-size: 1.2rem }
  .why { background: #f4f6f2; border-left: 3px solid #223d2c; padding: .7rem .85rem; margin: 0 0 .9rem }
  .quiet { color: #4a5a4e; font-size: .95rem }
  a.btn { display: inline-flex; align-items: center; min-height: 44px; padding: .4rem 1rem; border-radius: 4px;
    text-decoration: none; font-weight: 650; background: #223d2c; color: #fff; margin-top: .5rem }
</style></head><body><main class="card">
  <div class="top"><img src="/lockup.png" alt="Bless Your Paws Puppies" width="600" height="250"></div>
  <div class="body">
    <h1>You are not signed in to the editor</h1>
    <p class="why">${reason}</p>
    <p class="quiet">If you have more than one email address, this is usually the wrong one. Sign out and
    start again with the address Alex invited.</p>
    <a class="btn" href="/cdn-cgi/access/logout">Sign out and try again</a>
  </div>
</main></body></html>`, { status: 403, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}

// The only files served before anyone is identified: the refusal page needs its logo and
// icon. Nothing that reads the database is ever on this list.
const PUBLIC_ASSETS = new Set(['/lockup.png', '/paw.png']);

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const wantsJson = path.startsWith('/api/');
    try {
      if (PUBLIC_ASSETS.has(path)) return guarded(await env.ASSETS.fetch(request));
      const who = await identify(request, env, ctx, { getPersonByEmail });
      if (!who.ok) return guarded(refusal(who.reason, wantsJson));
      if (path === '/api/uploads') return guarded(await handleUpload(request, env, url, who));
      if (path.startsWith('/uploads/')) return guarded(await handlePreview(env, url));
      if (wantsJson) return guarded(await handleApi(request, env, url, who));
      const assetUrl = new URL(request.url);
      if (assetUrl.pathname === '/' || assetUrl.pathname === '') assetUrl.pathname = '/index.html';
      return guarded(await env.ASSETS.fetch(new Request(assetUrl, request)));
    } catch (err) {
      if (err instanceof HttpError) {
        return guarded(wantsJson ? json({ error: err.message }, err.status) : new Response(err.message, { status: err.status }));
      }
      console.error('worker error', path, err && err.stack ? err.stack : err);
      return guarded(json({ error: 'Something went wrong on our end. Nothing was changed.' }, 500));
    }
  },
};
