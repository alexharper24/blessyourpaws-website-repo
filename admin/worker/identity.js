// Who is asking, and are they allowed.
//
// This Worker sits behind Cloudflare Access at the edge: the whole Worker, not a path
// inside it, which is the reason the editor is a separate Worker at all. Identity is
// still resolved here rather than assumed, and it FAILS CLOSED: if Access is not
// configured, nobody gets in. An admin tool that defaults to open the moment its guard
// goes missing is worse than no admin tool.
//
// Getting past Access is not the same as being allowed to edit Bless Your Paws. Access proves
// someone is in the Cloudflare policy; the `people` table says whether they were
// invited. Both have to be true.

const CERT_CACHE_TTL_MS = 60 * 60 * 1000;
let certCache = { domain: null, expires: 0, keys: null };

function b64urlToBytes(s) {
  const pad = s.length % 4 === 0 ? '' : '='.repeat(4 - (s.length % 4));
  const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/') + pad);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i += 1) out[i] = bin.charCodeAt(i);
  return out;
}

function decodeSegment(seg) {
  return JSON.parse(new TextDecoder().decode(b64urlToBytes(seg)));
}

async function getKeys(teamDomain) {
  const now = Date.now();
  if (certCache.keys && certCache.domain === teamDomain && certCache.expires > now) {
    return certCache.keys;
  }
  const res = await fetch(`https://${teamDomain}.cloudflareaccess.com/cdn-cgi/access/certs`, {
    cf: { cacheTtl: 3600, cacheEverything: true },
  });
  if (!res.ok) throw new Error(`Access certs fetch failed: ${res.status}`);
  const body = await res.json();
  const keys = {};
  for (const jwk of body.keys || []) {
    keys[jwk.kid] = await crypto.subtle.importKey(
      'jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify'],
    );
  }
  certCache = { domain: teamDomain, expires: now + CERT_CACHE_TTL_MS, keys };
  return keys;
}

/**
 * Verify the Access assertion on the request.
 *
 * A fallback only. Worker-level Access hands identity to ctx.access directly; this path
 * exists so the editor stays safe however its Access application is set up, for example
 * a hostname-based one, which is a dashboard change with no
 * code change.
 */
async function verifyAssertion(request, env) {
  const team = env.ACCESS_TEAM_DOMAIN;
  const aud = env.ACCESS_AUD;
  if (!team || team.startsWith('PASTE_') || !aud || aud.startsWith('PASTE_')) {
    return { ok: false, reason: 'Access is not configured yet, so nobody can sign in.' };
  }

  const token = request.headers.get('Cf-Access-Jwt-Assertion')
    || (request.headers.get('Cookie') || '').match(/CF_Authorization=([^;]+)/)?.[1];
  if (!token) return { ok: false, reason: 'No Access assertion on the request.' };

  const parts = token.split('.');
  if (parts.length !== 3) return { ok: false, reason: 'Malformed assertion.' };

  let header;
  let payload;
  try {
    header = decodeSegment(parts[0]);
    payload = decodeSegment(parts[1]);
  } catch {
    return { ok: false, reason: 'Unreadable assertion.' };
  }

  const keys = await getKeys(team);
  const key = keys[header.kid];
  if (!key) return { ok: false, reason: 'Unknown signing key.' };

  const valid = await crypto.subtle.verify(
    { name: 'RSASSA-PKCS1-v1_5' }, key, b64urlToBytes(parts[2]),
    new TextEncoder().encode(`${parts[0]}.${parts[1]}`),
  );
  if (!valid) return { ok: false, reason: 'Bad signature.' };

  const now = Math.floor(Date.now() / 1000);
  if (payload.exp && payload.exp < now) return { ok: false, reason: 'Your sign-in expired.' };
  if (payload.nbf && payload.nbf > now + 60) return { ok: false, reason: 'Assertion not yet valid.' };

  const audList = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
  if (!audList.includes(aud)) return { ok: false, reason: 'Assertion is for a different application.' };
  if (payload.iss !== `https://${team}.cloudflareaccess.com`) {
    return { ok: false, reason: 'Unexpected issuer.' };
  }

  return { ok: true, email: payload.email || null };
}

/**
 * Local development only.
 *
 * `wrangler dev` has no Access in front of it, so without this the editor cannot be run
 * locally at all. BOTH conditions must hold: the var must be set (it lives in .dev.vars,
 * which is gitignored, and setup.mjs refuses to deploy if it ever appears in
 * wrangler.jsonc) AND the request must have arrived on localhost.
 */
function devIdentity(request, env) {
  if (!env.DEV_IDENTITY) return null;
  const host = new URL(request.url).hostname;
  if (host !== 'localhost' && host !== '127.0.0.1') return null;
  return { ok: true, email: env.DEV_IDENTITY, dev: true };
}

/** Resolve the caller. { ok, email, person, dev } or { ok: false, reason, status }. */
export async function identify(request, env, ctx, { getPersonByEmail }) {
  let auth = devIdentity(request, env);

  if (!auth && ctx && ctx.access && typeof ctx.access.getIdentity === 'function') {
    const identity = await ctx.access.getIdentity();
    if (identity?.email) auth = { ok: true, email: identity.email };
  }

  if (!auth) auth = await verifyAssertion(request, env);
  if (!auth.ok) return { ok: false, reason: auth.reason, status: 403 };

  const person = await getPersonByEmail(env, auth.email);
  if (!person) {
    // There is no sign-up. An address reaches the people table because somebody put it
    // there, and until then getting past Access buys nothing.
    return {
      ok: false,
      status: 403,
      reason: `${auth.email} is signed in, but that address has not been invited to the Bless Your Paws editor.`,
    };
  }

  return { ok: true, email: auth.email, person, dev: !!auth.dev };
}
