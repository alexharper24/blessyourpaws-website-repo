// Bless Your Paws owner editor. One list per section and ONE drawer for every edit, so the
// list never goes away and closing the drawer puts you back where you were.
(function () {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const esc = (t) => String(t == null ? '' : t).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const STATUS = [['available', 'Available'], ['reserved', 'Reserved'], ['adopted', 'Adopted']];
  let S = null;                 // the state from /api/state
  let view = 'puppies';

  // ---- talking to the Worker ---------------------------------------------------------------
  async function api(path, opts = {}) {
    const res = await fetch(path, {
      method: opts.method || 'GET',
      headers: opts.body !== undefined && !(opts.body instanceof Blob) ? { 'Content-Type': 'application/json' } : (opts.headers || {}),
      body: opts.body === undefined ? undefined : (opts.body instanceof Blob ? opts.body : JSON.stringify(opts.body)),
      credentials: 'same-origin',
    });
    let data = {};
    try { data = await res.json(); } catch {}
    if (!res.ok) throw new Error(data.error || `That did not work (${res.status}).`);
    return data;
  }
  const post = (path, body) => api(path, { method: 'POST', body });

  function toast(msg, bad) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.toggle('bad', !!bad);
    t.classList.add('show');
    clearTimeout(toast.t);
    toast.t = setTimeout(() => t.classList.remove('show'), bad ? 6000 : 2600);
  }

  async function load() {
    S = await api('/api/state');
    $('#who').textContent = S.me.name || S.me.email;
    $('#peopleLink').hidden = !S.me.admin;
    $('#siteLink').href = S.site;
    const avail = S.puppies.filter((p) => p.doc.status === 'available' && isCurrent(p)).length;
    $('#nPuppies').textContent = avail ? `${avail} available` : '';
    $('#nLitters').textContent = String(S.litters.filter((l) => l.doc.status === 'current').length || '');
    $('#nReviews').textContent = String(S.reviews.filter((r) => !r.doc.hidden).length || '');
  }

  const litterOf = (p) => S.litters.find((l) => l.key === p.doc.litter);
  const isCurrent = (p) => { const l = litterOf(p); return l && l.doc.status === 'current'; };
  const adult = (slug) => (S.adults.find((a) => a.key === slug) || {}).doc || { name: slug };
  const fmt = (iso) => { const [y, m, d] = iso.split('-').map(Number); return new Date(y, m - 1, d).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }); };

  /** A stem as a picture: the uploaded copy until the site has built it. */
  function photo(stem, folder = 'puppies') {
    const u = S.uploads[stem];
    if (u && !u.committed) return u.pending;
    return `${S.site}/img/r/${stem}-320.webp`;
  }
  function imgTag(stem, cls, folder) {
    if (!stem) return `<div class="${cls}" aria-hidden="true"></div>`;
    const u = S.uploads[stem];
    const fb = u ? u.pending : '';
    return `<img class="${cls}" src="${esc(photo(stem, folder))}" alt="" loading="lazy"${fb ? ` onerror="this.onerror=null;this.src='${esc(fb)}'"` : ''}>`;
  }

  // ---- drawer --------------------------------------------------------------------------------
  function openDrawer(title, html, bind) {
    $('#drawerTitle').textContent = title;
    $('#drawerBody').innerHTML = html;
    $('#drawer').classList.add('open');
    $('#drawer').setAttribute('aria-hidden', 'false');
    $('#scrim').classList.add('show');
    if (bind) bind($('#drawerBody'));
    const first = $('#drawerBody input, #drawerBody textarea, #drawerBody select');
    if (first && window.matchMedia('(min-width: 861px)').matches) first.focus();
  }
  function closeDrawer() {
    $('#drawer').classList.remove('open');
    $('#drawer').setAttribute('aria-hidden', 'true');
    $('#scrim').classList.remove('show');
    $('#rail').classList.remove('open');
  }
  $('#drawerClose').addEventListener('click', closeDrawer);
  $('#scrim').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDrawer(); });
  $('#menu').addEventListener('click', () => {
    const open = !$('#rail').classList.contains('open');
    $('#rail').classList.toggle('open', open);
    $('#scrim').classList.toggle('show', open);
    $('#menu').setAttribute('aria-expanded', String(open));
  });

  /** Wire a form in the drawer to a save. `collect` turns the form into the request body. */
  function bindForm(el, path, collect, after) {
    const f = $('form', el);
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = $('button[type=submit]', f);
      btn.disabled = true;
      try {
        await post(path, collect(f));
        await load();
        closeDrawer();
        render();
        toast(after || 'Saved. Publish when you are ready for it to show on the site.');
      } catch (err) {
        toast(err.message, true);
      } finally {
        btn.disabled = false;
      }
    });
  }
  const val = (f, n) => f.elements[n].value;

  // ---- photos ------------------------------------------------------------------------------
  /** Phone photos are 4 to 8 MB. Resize to 2400px JPEG in the browser; the site uses 2000 at most. */
  async function shrink(file) {
    const bmp = await createImageBitmap(file, { imageOrientation: 'from-image' });
    for (const [max, q] of [[2400, 0.88], [2000, 0.82], [1600, 0.78]]) {
      const s = Math.min(1, max / Math.max(bmp.width, bmp.height));
      const c = document.createElement('canvas');
      c.width = Math.round(bmp.width * s);
      c.height = Math.round(bmp.height * s);
      c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height);
      const blob = await new Promise((r) => c.toBlob(r, 'image/jpeg', q));
      if (blob && blob.size < 11 * 1024 * 1024) return blob;
    }
    throw new Error('That photo is too large to send. Try another one.');
  }
  async function uploadAll(files, file, key) {
    const stems = [];
    for (const f of files) {
      const blob = await shrink(f);
      const r = await api(`/api/uploads?file=${file}&key=${encodeURIComponent(key)}`, { method: 'POST', body: blob, headers: { 'Content-Type': 'image/jpeg' } });
      stems.push(r.stem);
    }
    return stems;
  }

  // ---- Puppies -----------------------------------------------------------------------------
  function puppyRow(p) {
    const d = p.doc;
    const cover = (d.page_photos[0] || d.photos[0]);
    const waiting = !d.photos.length ? '<span class="tag">Not on the site until it has a photo</span>' : '';
    const seg = isCurrent(p) ? `<div class="seg" role="group" aria-label="${esc(d.name)} status">${STATUS.map(([s, l]) =>
      `<button type="button" data-s="${s}" data-k="${esc(p.key)}" aria-pressed="${d.status === s}">${l}</button>`).join('')}</div>` : `<span class="tag past">${esc(STATUS.find((x) => x[0] === d.status)[1])}</span>`;
    return `<div class="item">${imgTag(cover, 'thumb')}
      <div><button class="nm" data-edit="${esc(p.key)}">${esc(d.name)}</button>${waiting}
        <div class="meta">${esc(d.sex)} &middot; ${esc(d.color)}${d.note ? ` &middot; ${esc(d.note)}` : ''}</div></div>
      <div class="acts">${seg}</div></div>`;
  }

  function renderPuppies(w) {
    const cur = S.litters.filter((l) => l.doc.status === 'current').slice().reverse();
    const past = S.litters.filter((l) => l.doc.status !== 'current').slice().reverse();
    let html = `<div class="head"><div><h1>Puppies</h1><p class="muted">Tap a status to change it. Tap a name to edit
      details and photos. Changes reach the site when you publish.</p></div></div>`;
    if (!cur.length) html += '<p class="empty">No current litter. Start one under Litters.</p>';
    for (const l of cur) {
      const pups = S.puppies.filter((p) => p.doc.litter === l.key);
      html += `<section class="group"><h2>${esc(adult(l.doc.dam).name)} and ${esc(adult(l.doc.sire).name)}
        <small>born ${fmt(l.doc.born)}, going home ${fmt(l.doc.home)}</small></h2>
        <div class="list">${pups.map(puppyRow).join('') || '<p class="empty">No puppies yet.</p>'}</div>
        <div class="btn-row"><button class="btn btn-small" data-add="${esc(l.key)}">Add a puppy to this litter</button></div></section>`;
    }
    if (past.length) {
      html += '<section class="group"><h2>Past litters <small>their pages now point to the puppies page, and their photos stay in the gallery</small></h2>';
      for (const l of past) {
        html += `<h3 style="margin-top:1rem">${esc(adult(l.doc.dam).name)} and ${esc(adult(l.doc.sire).name)}, born ${fmt(l.doc.born)}</h3>
          <div class="list">${S.puppies.filter((p) => p.doc.litter === l.key).map(puppyRow).join('')}</div>`;
      }
      html += '</section>';
    }
    w.innerHTML = html;
    w.querySelectorAll('.seg button').forEach((b) => b.addEventListener('click', () => setStatus(b.dataset.k, b.dataset.s)));
    w.querySelectorAll('[data-edit]').forEach((b) => b.addEventListener('click', () => editPuppy(b.dataset.edit)));
    w.querySelectorAll('[data-add]').forEach((b) => b.addEventListener('click', () => addPuppy(b.dataset.add)));
  }

  async function setStatus(key, status) {
    const p = S.puppies.find((x) => x.key === key);
    if (!p || p.doc.status === status) return;
    try {
      await post(`/api/puppies/${encodeURIComponent(key)}`, { status, version: p.version });
      await load();
      render();
      toast(`${p.doc.name} is now ${status}. Publish to show it on the site.`);
    } catch (err) {
      toast(err.message, true);
      await load(); render();
    }
  }

  function addPuppy(litter) {
    openDrawer('Add a puppy', `<form>
      <label class="f">Name<input name="name" required maxlength="40" autocomplete="off"></label>
      <div class="row2"><label class="f">Boy or girl<select name="sex"><option>Boy</option><option>Girl</option></select></label>
      <label class="f">Color<input name="color" required maxlength="60" placeholder="Blue merle parti"></label></div>
      <p class="fine">The puppy appears on the site once you add a photo and publish.</p>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Add the puppy</button></div></form>`,
    (el) => bindForm(el, '/api/puppies', (f) => ({ litter, name: val(f, 'name'), sex: val(f, 'sex'), color: val(f, 'color') }), 'Puppy added. Open it to add photos.'));
  }

  function photoStrip(d) {
    return d.photos.slice().sort((a, b) => {
      const ia = d.page_photos.indexOf(a); const ib = d.page_photos.indexOf(b);
      return (ia < 0 ? 1e6 + d.photos.indexOf(a) : ia) - (ib < 0 ? 1e6 + d.photos.indexOf(b) : ib);
    }).map((stem) => {
      const i = d.page_photos.indexOf(stem);
      const on = i >= 0;
      return `<div class="ph${on ? '' : ' off'}${i === 0 ? ' cover' : ''}" data-stem="${esc(stem)}">
        ${i === 0 ? '<span class="badge">Cover</span>' : ''}${imgTag(stem, '')}
        <div class="pa"><button type="button" data-a="left" ${on && i > 0 ? '' : 'disabled'} aria-label="Move earlier">&#8592;</button>
        <button type="button" data-a="toggle" aria-label="${on ? 'Hide from the page' : 'Show on the page'}">${on ? 'Hide' : 'Show'}</button>
        <button type="button" data-a="right" ${on && i < d.page_photos.length - 1 ? '' : 'disabled'} aria-label="Move later">&#8594;</button></div></div>`;
    }).join('');
  }

  function editPuppy(key) {
    const p = S.puppies.find((x) => x.key === key);
    const d = p.doc;
    const work = { photos: d.photos.slice(), page_photos: d.page_photos.slice() };
    openDrawer(d.name, `<form>
      <label class="f">Name<input name="name" required maxlength="40" value="${esc(d.name)}"></label>
      <div class="row2"><label class="f">Boy or girl<select name="sex">${['Boy', 'Girl'].map((x) => `<option${x === d.sex ? ' selected' : ''}>${x}</option>`).join('')}</select></label>
      <label class="f">Color<input name="color" required maxlength="60" value="${esc(d.color)}"></label></div>
      <label class="f">Short note<span class="hint">Optional. Shown in bold on the puppy's page.</span><input name="note" maxlength="200" value="${esc(d.note)}"></label>
      <h3>Price</h3>
      <p class="fine">Leave both blank to use the litter's prices (${usd(litterOf(p).doc.price)}, or ${usd(litterOf(p).doc.cash_price)} cash). Fill in both to price this puppy on its own. The deposit is always the litter's.</p>
      <div class="row2"><label class="f">Price for this puppy<input name="price" type="number" inputmode="numeric" min="300" max="20000" step="1" placeholder="${esc(litterOf(p).doc.price ?? '')}" value="${esc(d.price ?? '')}"></label>
      <label class="f">Cash price for this puppy<input name="cash_price" type="number" inputmode="numeric" min="300" max="20000" step="1" placeholder="${esc(litterOf(p).doc.cash_price ?? '')}" value="${esc(d.cash_price ?? '')}"></label></div>
      <h3>Photos</h3>
      <p class="fine">The first photo is the cover on the cards and the puppy's page. Hidden photos stay in the gallery but leave the puppy's page. Photos are never deleted.</p>
      <div class="strip" id="strip">${photoStrip(work)}</div>
      <label class="btn btn-small upload">Add photos<input type="file" accept="image/*" multiple id="addPhotos"></label>
      <p class="fine" id="upMsg"></p>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Save</button></div></form>`, (el) => {
      const strip = $('#strip', el);
      const redraw = () => { strip.innerHTML = photoStrip(work); };
      strip.addEventListener('click', (e) => {
        const b = e.target.closest('button[data-a]'); if (!b) return;
        const stem = b.closest('.ph').dataset.stem;
        const pg = work.page_photos;
        const i = pg.indexOf(stem);
        if (b.dataset.a === 'toggle') {
          if (i >= 0) { if (pg.length === 1) { toast('Keep at least one photo on the page.', true); return; } pg.splice(i, 1); } else pg.push(stem);
        } else if (i >= 0) {
          const j = b.dataset.a === 'left' ? i - 1 : i + 1;
          if (j >= 0 && j < pg.length) [pg[i], pg[j]] = [pg[j], pg[i]];
        }
        redraw();
      });
      $('#addPhotos', el).addEventListener('change', async (e) => {
        const files = [...e.target.files];
        if (!files.length) return;
        $('#upMsg', el).textContent = `Sending ${files.length} photo${files.length === 1 ? '' : 's'}…`;
        try {
          const stems = await uploadAll(files, 'puppies', key);
          await load();
          for (const s of stems) { work.photos.push(s); work.page_photos.push(s); }
          redraw();
          $('#upMsg', el).textContent = `${stems.length} added. Save, then publish.`;
        } catch (err) { $('#upMsg', el).textContent = ''; toast(err.message, true); }
        e.target.value = '';
      });
      bindForm(el, `/api/puppies/${encodeURIComponent(key)}`, (f) => ({
        name: val(f, 'name'), sex: val(f, 'sex'), color: val(f, 'color'), note: val(f, 'note'),
        price: val(f, 'price') === '' ? '' : num(f, 'price'), cash_price: val(f, 'cash_price') === '' ? '' : num(f, 'cash_price'),
        photos: work.photos, page_photos: work.page_photos, version: S.puppies.find((x) => x.key === key).version,
      }));
    });
  }

  // ---- Litters -----------------------------------------------------------------------------
  function renderLitters(w) {
    const rows = S.litters.slice().reverse().map((l) => {
      const d = l.doc;
      const pups = S.puppies.filter((p) => p.doc.litter === l.key);
      const left = pups.filter((p) => p.doc.status !== 'adopted').length;
      return `<div class="card"><h3>${esc(adult(d.dam).name)} and ${esc(adult(d.sire).name)}${d.status === 'current' ? '' : ' <span class="tag past">Past litter</span>'}</h3>
        <p class="fine" style="margin:.2rem 0 .6rem">Born ${fmt(d.born)} &middot; can go home ${fmt(d.home)} &middot; ${esc(d.size)}<br>
        ${usd(d.price)} &middot; ${usd(d.cash_price)} cash &middot; ${usd(d.deposit)} deposit<br>
        ${pups.length} puppies, ${left ? `${left} not yet adopted` : 'every one adopted'}</p>
        <button class="btn btn-small" data-edit="${esc(l.key)}">Edit</button></div>`;
    }).join('');
    w.innerHTML = `<div class="head"><div><h1>Litters</h1><p class="muted">Dates, size and prices show on the puppies page and every puppy's page.</p></div>
      <button class="btn btn-primary" id="newLitter">Start a new litter</button></div><div class="cards">${rows}</div>`;
    w.querySelectorAll('[data-edit]').forEach((b) => b.addEventListener('click', () => editLitter(b.dataset.edit)));
    $('#newLitter', w).addEventListener('click', newLitter);
  }

  const usd = (n) => (Number.isFinite(n) ? `$${n.toLocaleString('en-US')}` : '');
  const num = (f, n) => Number(val(f, n));

  function litterFields(d) {
    return `<div class="row2"><label class="f">Born<input type="date" name="born" required value="${esc(d.born || '')}"></label>
      <label class="f">Can go home<input type="date" name="home" required value="${esc(d.home || '')}"></label></div>
      <label class="f">Expected adult size<input name="size" required maxlength="40" value="${esc(d.size || '')}" placeholder="15 to 24 lbs"></label>
      <label class="f">Parents sentence<span class="hint">Read as "Eight puppies from …" at the top of the puppies page.</span>
        <input name="parents_phrase" required maxlength="200" value="${esc(d.parents_phrase || '')}"></label>
      <label class="f">Short parents line<span class="hint">Read as "from …" in search results.</span>
        <input name="parents_short" required maxlength="120" value="${esc(d.parents_short || '')}"></label>
      <h3>Prices</h3>
      <p class="fine">Whole dollars, before sales tax. Every puppy in the litter shows them, and online payments charge them. Sales tax is added at checkout.</p>
      <div class="row3"><label class="f">Price<input name="price" type="number" inputmode="numeric" required min="300" max="20000" step="1" value="${esc(d.price ?? '')}"></label>
      <label class="f">Cash price<input name="cash_price" type="number" inputmode="numeric" required min="300" max="20000" step="1" value="${esc(d.cash_price ?? '')}"></label>
      <label class="f">Deposit<input name="deposit" type="number" inputmode="numeric" required min="50" max="5000" step="1" value="${esc(d.deposit ?? '')}"></label></div>`;
  }

  function editLitter(key) {
    const l = S.litters.find((x) => x.key === key);
    const d = l.doc;
    const pups = S.puppies.filter((p) => p.doc.litter === key);
    const allAdopted = pups.length && pups.every((p) => p.doc.status === 'adopted');
    const statusBlock = d.status === 'current'
      ? `<h3>When the litter is done</h3><p class="fine">Moving it to past litters takes its puppy pages off the site (old links go to the puppies page) and keeps its photos in the gallery. ${allAdopted ? '' : 'It becomes available once every puppy is adopted.'}</p>
         <button type="button" class="btn btn-small" id="retire" ${allAdopted ? '' : 'disabled'}>Move to past litters</button>`
      : '<h3>Past litter</h3><p class="fine">Bring it back if it was moved by mistake.</p><button type="button" class="btn btn-small" id="unretire">Make it current again</button>';
    let newPhoto = null;
    openDrawer(`Litter born ${fmt(d.born)}`, `<form>${litterFields(d)}
      <h3>Litter photo</h3><p class="fine">Shown at the top of the puppies page. A wide photo of the whole litter works best.</p>
      <div style="max-width:20rem" id="litPhoto">${imgTag(d.photo, '', 'puppies')}</div>
      <label class="btn btn-small upload" style="margin-top:.5rem">Replace the photo<input type="file" accept="image/*" id="litUp"></label>
      <label class="f">Describe the photo<span class="hint">Read aloud to visitors who cannot see it, such as "The litter asleep in a row on a blanket".</span>
        <input name="photo_alt" maxlength="140" value="${esc(d.photo_alt || '')}" placeholder="Our Munchkin Bernedoodle litter asleep side by side"></label>
      <p class="fine" id="litMsg">The old photo is kept, never deleted.</p>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Save</button></div></form>
      <div style="margin-top:2rem">${statusBlock}</div>`, (el) => {
      $('#litUp', el).addEventListener('change', async (e) => {
        if (!e.target.files[0]) return;
        $('#litMsg', el).textContent = 'Sending…';
        try {
          [newPhoto] = await uploadAll([e.target.files[0]], 'litters', key);
          await load();
          $('#litPhoto', el).innerHTML = imgTag(newPhoto, '', 'puppies');
          const alt = $('form', el).elements.photo_alt; alt.value = ''; alt.required = true; alt.focus();
          $('#litMsg', el).textContent = 'New photo ready. Describe it, save, then publish.';
        } catch (err) { $('#litMsg', el).textContent = ''; toast(err.message, true); }
      });
      bindForm(el, `/api/litters/${encodeURIComponent(key)}`, (f) => {
        const b = { born: val(f, 'born'), home: val(f, 'home'), size: val(f, 'size'), parents_phrase: val(f, 'parents_phrase'),
          parents_short: val(f, 'parents_short'), price: num(f, 'price'), cash_price: num(f, 'cash_price'), deposit: num(f, 'deposit'),
          version: S.litters.find((x) => x.key === key).version };
        if (newPhoto) b.photo = newPhoto;
        if (newPhoto || val(f, 'photo_alt')) b.photo_alt = val(f, 'photo_alt');
        return b;
      });
      const st = async (status) => {
        try { await post(`/api/litters/${encodeURIComponent(key)}`, { status, version: S.litters.find((x) => x.key === key).version });
          await load(); closeDrawer(); render(); toast(status === 'past' ? 'Moved to past litters. Publish to update the site.' : 'The litter is current again.'); }
        catch (err) { toast(err.message, true); }
      };
      const r = $('#retire', el); if (r) r.addEventListener('click', () => { if (confirm('Move this litter to past litters? Its puppy pages leave the site when you publish.')) st('past'); });
      const u = $('#unretire', el); if (u) u.addEventListener('click', () => st('current'));
    });
  }

  function newLitter() {
    const moms = S.adults.filter((a) => a.doc.role === 'Mom');
    const dads = S.adults.filter((a) => a.doc.role === 'Dad');
    const opt = (list) => list.map((a) => `<option value="${esc(a.key)}">${esc(a.doc.name)}</option>`).join('');
    openDrawer('Start a new litter', `<form>
      <div class="row2"><label class="f">Mom<select name="dam">${opt(moms)}</select></label><label class="f">Dad<select name="sire">${opt(dads)}</select></label></div>
      ${litterFields((({ size = '', price, cash_price, deposit } = {}) => ({ size, price, cash_price, deposit }))(S.litters.length ? S.litters[S.litters.length - 1].doc : {}))}
      <p class="fine">Leave the two sentences blank to have them written from the parents' names. Puppies are added after, from the Puppies screen.</p>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Start the litter</button></div></form>`, (el) => {
      const f = $('form', el);
      f.elements.parents_phrase.required = false; f.elements.parents_short.required = false;
      f.elements.born.addEventListener('change', () => {
        if (f.elements.home.value) return;
        const t = new Date(`${f.elements.born.value}T12:00:00`); t.setDate(t.getDate() + 56);
        f.elements.home.value = t.toISOString().slice(0, 10);
      });
      bindForm(el, '/api/litters', (ff) => ({ dam: val(ff, 'dam'), sire: val(ff, 'sire'), born: val(ff, 'born'), home: val(ff, 'home'),
        size: val(ff, 'size'), parents_phrase: val(ff, 'parents_phrase'), parents_short: val(ff, 'parents_short'),
        price: num(ff, 'price'), cash_price: num(ff, 'cash_price'), deposit: num(ff, 'deposit') }), 'Litter started. Add its puppies under Puppies.');
    });
  }

  // ---- Parents -----------------------------------------------------------------------------
  function renderParents(w) {
    w.innerHTML = `<div class="head"><div><h1>Parents</h1><p class="muted">What the parents page and each litter's parent cards say.</p></div></div>
      <div class="cards">${S.adults.map((a) => `<div class="card">${imgTag(a.doc.photo, 'thumb', 'dogs').replace('class="thumb"', 'class="thumb" style="width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:4px;margin-bottom:.6rem"')}
        <h3>${esc(a.doc.name)} <small class="muted">${esc(a.doc.role)}</small></h3><p class="fine">${esc(a.doc.breed)}</p>
        <button class="btn btn-small" data-edit="${esc(a.key)}">Edit</button></div>`).join('')}</div>`;
    w.querySelectorAll('[data-edit]').forEach((b) => b.addEventListener('click', () => editAdult(b.dataset.edit)));
  }

  function editAdult(key) {
    const a = S.adults.find((x) => x.key === key);
    const d = a.doc;
    let newPhoto = null;
    openDrawer(d.name, `<form>
      <label class="f">Story<span class="hint">The paragraph on the parents page.</span><textarea name="story" required maxlength="1200">${esc(d.story)}</textarea></label>
      <h3>Card facts</h3>${d.facts.map(([k, v], i) => `<label class="f">${esc(k)}<input name="fact${i}" required maxlength="80" value="${esc(v)}"></label>`).join('')}
      <h3>Health details</h3><p class="note fine">Only state a result there is a document for. A health claim without one is a claim that may have to come back off the site.</p>
      ${d.health.map(([k, v], i) => `<label class="f">${esc(k.replace(/:$/, ''))}<textarea name="health${i}" required maxlength="400" style="min-height:4.5rem">${esc(v)}</textarea></label>`).join('')}
      <h3>Photo</h3><div style="max-width:14rem" id="adultPhoto">${imgTag(d.photo, '', 'dogs')}</div>
      <label class="btn btn-small upload" style="margin-top:.5rem">Replace the photo<input type="file" accept="image/*" id="adultUp"></label>
      <p class="fine" id="upMsg">The old photo is kept, never deleted.</p>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Save</button></div></form>`, (el) => {
      $('#adultUp', el).addEventListener('change', async (e) => {
        if (!e.target.files[0]) return;
        $('#upMsg', el).textContent = 'Sending…';
        try {
          [newPhoto] = await uploadAll([e.target.files[0]], 'adults', key);
          await load();
          $('#adultPhoto', el).innerHTML = imgTag(newPhoto, '', 'dogs');
          $('#upMsg', el).textContent = 'New photo ready. Save, then publish.';
        } catch (err) { $('#upMsg', el).textContent = ''; toast(err.message, true); }
      });
      bindForm(el, `/api/adults/${encodeURIComponent(key)}`, (f) => {
        const b = { story: val(f, 'story'), facts: d.facts.map((_, i) => val(f, `fact${i}`)),
          health: d.health.map((_, i) => val(f, `health${i}`)), version: S.adults.find((x) => x.key === key).version };
        if (newPhoto) b.photo = newPhoto;
        return b;
      });
    });
  }

  // ---- Reviews -----------------------------------------------------------------------------
  function renderReviews(w) {
    w.innerHTML = `<div class="head"><div><h1>Reviews</h1><p class="muted">Posted word for word as families send them.</p></div>
      <button class="btn btn-primary" id="addReview">Add a review</button></div>
      <div class="list">${S.reviews.map((r, i) => `<div class="item" style="grid-template-columns:minmax(0,1fr) auto">
        <div><button class="nm" data-edit="${esc(r.key)}">${esc(r.doc.title || r.doc.attribution)}</button>${r.doc.hidden ? '<span class="tag past">Hidden</span>' : ''}
        <div class="meta">&ldquo;${esc(r.doc.quote.slice(0, 140))}${r.doc.quote.length > 140 ? '…' : ''}&rdquo; &middot; ${esc(r.doc.attribution)}</div></div>
        <div class="acts"><button class="btn btn-small" data-mv="up" data-k="${esc(r.key)}" ${i ? '' : 'disabled'} aria-label="Move up">&#8593;</button>
        <button class="btn btn-small" data-mv="down" data-k="${esc(r.key)}" ${i < S.reviews.length - 1 ? '' : 'disabled'} aria-label="Move down">&#8595;</button></div></div>`).join('') || '<p class="empty">No reviews yet.</p>'}</div>`;
    $('#addReview', w).addEventListener('click', () => editReview(null));
    w.querySelectorAll('[data-edit]').forEach((b) => b.addEventListener('click', () => editReview(b.dataset.edit)));
    w.querySelectorAll('[data-mv]').forEach((b) => b.addEventListener('click', async () => {
      try { await post('/api/move', { file: 'reviews', key: b.dataset.k, dir: b.dataset.mv }); await load(); render(); } catch (err) { toast(err.message, true); }
    }));
  }

  function editReview(key) {
    const r = key ? S.reviews.find((x) => x.key === key) : null;
    const d = r ? r.doc : { title: '', quote: '', attribution: '', hidden: false };
    openDrawer(r ? 'Edit review' : 'Add a review', `<form>
      <label class="f">Title<span class="hint">Optional, a few words in bold above the review.</span><input name="title" maxlength="80" value="${esc(d.title)}"></label>
      <label class="f">Review<span class="hint">Word for word, as the family wrote it.</span><textarea name="quote" required maxlength="1500">${esc(d.quote)}</textarea></label>
      <label class="f">Who it is from<span class="hint">First name and the puppy, for example "Brenda, who reserved Tirzah".</span><input name="attribution" required maxlength="120" value="${esc(d.attribution)}"></label>
      ${r ? `<label class="f" style="display:flex;gap:.5rem;align-items:center;font-weight:500"><input type="checkbox" name="hidden" style="width:auto;margin:0" ${d.hidden ? 'checked' : ''}> Hide this review from the site</label>` : ''}
      <div class="btn-row"><button class="btn btn-primary" type="submit">${r ? 'Save' : 'Add the review'}</button></div></form>`,
    (el) => bindForm(el, r ? `/api/reviews/${encodeURIComponent(key)}` : '/api/reviews', (f) => {
      const b = { title: val(f, 'title'), quote: val(f, 'quote'), attribution: val(f, 'attribution') };
      if (r) { b.hidden = f.elements.hidden.checked; b.version = S.reviews.find((x) => x.key === key).version; }
      return b;
    }));
  }

  // ---- Publish -----------------------------------------------------------------------------
  async function renderPublish(w) {
    w.innerHTML = '<div class="head"><div><h1>Publish</h1><p class="muted">Checking what has changed since the site was last updated…</p></div></div>';
    let r;
    try { r = await api('/api/publish'); } catch (err) { w.innerHTML += `<p class="err">${esc(err.message)}</p>`; return; }
    if (r.notSetUp) { w.innerHTML = `<div class="head"><div><h1>Publish</h1></div></div><p class="warn">${esc(r.error)}</p>`; return; }
    const last = r.last ? `Last published ${new Date(r.last.finished_at).toLocaleString()} by ${esc(r.last.actor)}.` : 'Nothing has been published from the editor yet.';
    const list = r.changes.length
      ? `<ul class="changes">${r.changes.map((c) => `<li><span>${esc(c.what)}</span><button class="btn btn-small" data-undo="${esc(c.file)}|${esc(c.key)}">Undo</button></li>`).join('')}</ul>`
      : '<p class="empty">Everything here is already on the site.</p>';
    const missing = r.missing.length ? `<p class="err">These photos are named but cannot be found, so publishing is blocked: ${esc(r.missing.join(', '))}. Tell Alex.</p>` : '';
    w.innerHTML = `<div class="head"><div><h1>Publish</h1><p class="muted">${last}</p></div></div>${missing}
      <h2>Waiting to go on the site</h2>${list}
      ${r.photos ? `<p class="fine">${r.photos} new photo${r.photos === 1 ? '' : 's'} will go with it.</p>` : ''}
      <div class="btn-row"><button class="btn btn-primary" id="go" ${r.changes.length && !r.missing.length ? '' : 'disabled'}>Publish to the site</button></div>
      <p class="fine" id="pubMsg">The site updates about two minutes after you publish.</p>`;
    w.querySelectorAll('[data-undo]').forEach((b) => b.addEventListener('click', async () => {
      const [file, key] = b.dataset.undo.split('|');
      if (!confirm('Put this back to how it is on the site?')) return;
      try { await post('/api/undo', { file, key }); await load(); toast('Put back.'); renderPublish(w); } catch (err) { toast(err.message, true); }
    }));
    $('#go', w).addEventListener('click', async (e) => {
      e.target.disabled = true;
      $('#pubMsg', w).textContent = 'Publishing…';
      try {
        // A big batch of photos goes up in rounds of 30, each its own request, and the last
        // round makes the single commit. Keep calling until it does.
        let res = await post('/api/publish', {});
        while (res.partial) {
          $('#pubMsg', w).textContent = `Sending photos, ${res.staged} of ${res.total}…`;
          res = await post('/api/publish', {});
        }
        if (res.nothing) { toast(res.message); renderPublish(w); return; }
        await load();
        w.innerHTML = `<div class="head"><div><h1>Published</h1></div></div><p class="note">Sent to the site. It updates in about two minutes, and you can
          <a href="${esc(S.site)}" target="_blank" rel="noopener">check it here</a>.</p>`;
      } catch (err) { $('#pubMsg', w).textContent = ''; toast(err.message, true); e.target.disabled = false; }
    });
  }

  // ---- History and People ------------------------------------------------------------------
  const WORDS = { status: 'changed a status', save: 'edited', upload: 'uploaded a photo', 'add-puppy': 'added a puppy', 'add-litter': 'started a litter',
    'add-review': 'added a review', retire: 'moved a litter to past', unretire: 'made a litter current', hide: 'hid a review', show: 'showed a review',
    move: 'reordered', undo: 'undid a change', publish: 'published', 'stripe-test': 'test payment, nothing changed, for', 'stripe-clash': 'took a payment for a puppy already spoken for:', 'stripe-repeat': 'took a second payment for', 'people-add': 'invited', 'people-remove': 'removed access for' };
  async function renderHistory(w) {
    const h = await api('/api/history');
    w.innerHTML = `<div class="head"><div><h1>History</h1></div></div>
      <h2>Publishes</h2>${h.publishes.length ? `<table class="hist"><tr><th>When</th><th>Who</th><th>Result</th></tr>${h.publishes.map((p) =>
        `<tr><td>${esc(new Date(p.started_at).toLocaleString())}</td><td>${esc(p.actor)}</td><td>${p.outcome === 'ok' ? `Published ${esc((p.commit_sha || '').slice(0, 7))}` : esc(p.outcome || 'running')}</td></tr>`).join('')}</table>` : '<p class="empty">None yet.</p>'}
      <h2 style="margin-top:1.5rem">Recent edits</h2>${h.recent.length ? `<table class="hist"><tr><th>When</th><th>Who</th><th>What</th></tr>${h.recent.map((a) =>
        `<tr><td>${esc(new Date(a.created_at).toLocaleString())}</td><td>${esc(a.actor)}</td><td>${esc(WORDS[a.action] || a.action)} ${esc(a.key || '')} ${a.detail ? `<span class="muted">(${esc(a.detail)})</span>` : ''}</td></tr>`).join('')}</table>` : '<p class="empty">None yet.</p>'}`;
  }

  async function renderPeople(w) {
    const r = await api('/api/people');
    w.innerHTML = `<div class="head"><div><h1>People</h1><p class="muted">Who can sign in. They also need to be in the Cloudflare Access policy.</p></div></div>
      <div class="list">${r.people.map((p) => `<div class="item" style="grid-template-columns:minmax(0,1fr) auto"><div><strong>${esc(p.display_name)}</strong>${p.is_admin ? ' <span class="tag past">Admin</span>' : ''}<div class="meta">${esc(p.email)}</div></div>
        <div class="acts">${p.email.toLowerCase() === S.me.email.toLowerCase() ? '' : `<button class="btn btn-small" data-rm="${esc(p.email)}">Remove</button>`}</div></div>`).join('')}</div>
      <form class="card" style="margin-top:1rem;max-width:30rem"><h2>Invite someone</h2>
        <label class="f">Name<input name="name" required maxlength="60"></label>
        <label class="f">Email<input name="email" type="email" required></label>
        <div class="btn-row"><button class="btn btn-primary" type="submit">Invite</button></div></form>`;
    w.querySelectorAll('[data-rm]').forEach((b) => b.addEventListener('click', async () => {
      if (!confirm(`Remove ${b.dataset.rm}?`)) return;
      try { await post('/api/people', { email: b.dataset.rm, remove: true }); renderPeople(w); } catch (err) { toast(err.message, true); }
    }));
    $('form', w).addEventListener('submit', async (e) => {
      e.preventDefault();
      try { await post('/api/people', { name: val(e.target, 'name'), email: val(e.target, 'email') }); toast('Invited. Add them to the Access policy too.'); renderPeople(w); } catch (err) { toast(err.message, true); }
    });
  }

  // ---- routing -----------------------------------------------------------------------------
  const VIEWS = { puppies: renderPuppies, litters: renderLitters, parents: renderParents, reviews: renderReviews,
    publish: renderPublish, history: renderHistory, people: renderPeople };
  async function render() {
    const w = $('#work');
    document.querySelectorAll('.rail a[data-view]').forEach((a) => a.classList.toggle('cur', a.dataset.view === view));
    try { await VIEWS[view](w); } catch (err) { w.innerHTML = `<p class="err">${esc(err.message)}</p>`; }
  }
  function route() {
    const v = (location.hash || '#puppies').slice(1);
    view = VIEWS[v] ? v : 'puppies';
    closeDrawer();
    render();
    $('#work').focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', route);

  load().then(route).catch((err) => { $('#work').innerHTML = `<p class="err">${esc(err.message)}</p>`; });
})();
