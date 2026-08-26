// Bless Your Paws Puppies - v2
(function(){
  // ---- mobile nav overlay: fixed at every width so it never becomes a flex item
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && nav){
    var close = document.createElement('button');
    close.className = 'nav-toggle nav-close';
    close.textContent = 'Close';
    close.setAttribute('aria-label','Close menu');
    nav.appendChild(close);
    function setOpen(open){
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
      document.body.classList.toggle('nav-open', open);
    }
    toggle.addEventListener('click', function(){ setOpen(!nav.classList.contains('open')); });
    close.addEventListener('click', function(){ setOpen(false); });
    nav.addEventListener('click', function(e){ if (e.target.tagName === 'A') setOpen(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') setOpen(false); });
  }

  // ---- puppy photo carousel: prev/next, thumbs, arrow keys
  document.querySelectorAll('.carousel').forEach(function(car){
    var slides = [].slice.call(car.querySelectorAll('.frame img'));
    var thumbs = [].slice.call(car.querySelectorAll('.cthumbs button'));
    var counter = car.querySelector('.count');
    if (slides.length < 2){
      car.querySelectorAll('.cnav').forEach(function(b){ b.remove(); });
      if (counter) counter.remove();
      return;
    }
    var i = 0;
    function show(n){
      i = (n + slides.length) % slides.length;
      slides.forEach(function(s,k){
        s.hidden = false;                       // stacked, so fade rather than pop
        s.classList.toggle('is-on', k === i);
        s.setAttribute('aria-hidden', k === i ? 'false' : 'true');
      });
      thumbs.forEach(function(t,k){ t.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      if (counter) counter.textContent = (i+1) + ' / ' + slides.length;
    }
    // ---- autoplay with a crossfade, so a visitor sees the whole set without
    // clicking. Pauses on hover, focus, and when the tab or page is out of view,
    // and does not run at all for anyone who asked for reduced motion.
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var DWELL = 4000;
    var timer = null, paused = false, inView = true;
    function stop(){ if (timer){ clearInterval(timer); timer = null; } }
    function canPlay(){
      return !reduce.matches && !paused && inView && !document.hidden;
    }
    function start(){
      if (timer || !canPlay()) return;
      timer = setInterval(function(){ show(i+1); }, DWELL);
    }
    // one place decides, so every signal (hover, focus, tab switch, scrolling the
    // carousel out of view) is re-evaluated the same way instead of racing
    function sync(){ canPlay() ? start() : stop(); }
    function restart(){ stop(); start(); }

    car.querySelector('.cprev').addEventListener('click', function(){ show(i-1); restart(); });
    car.querySelector('.cnext').addEventListener('click', function(){ show(i+1); restart(); });
    thumbs.forEach(function(t,k){
      t.addEventListener('click', function(){ show(k); restart(); }); });
    car.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft'){ show(i-1); restart(); }
      if (e.key === 'ArrowRight'){ show(i+1); restart(); }
    });
    ['mouseenter','focusin'].forEach(function(ev){
      car.addEventListener(ev, function(){ paused = true; sync(); }); });
    ['mouseleave','focusout'].forEach(function(ev){
      car.addEventListener(ev, function(){ paused = false; sync(); }); });
    document.addEventListener('visibilitychange', sync);
    reduce.addEventListener('change', sync);

    show(0);
    // only cycle while the carousel is actually on screen
    if ('IntersectionObserver' in window){
      new IntersectionObserver(function(entries){
        inView = entries[0].isIntersecting;
        sync();
      }, { threshold: 0.35 }).observe(car);
    }
    sync();
  });

  // ---- guard: payment links stay friendly until the real Stripe links exist
  document.querySelectorAll('a.pay-link').forEach(function(a){
    if (a.href.indexOf('REPLACE') !== -1){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var msg = a.closest('.reserve').querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // ---- forms: a friendly guard while there is no endpoint, otherwise submit in place
  document.querySelectorAll('form[data-guard]').forEach(function(f){
    var msg = f.querySelector('.guard-msg');

    // No endpoint yet. Never let a real inquiry vanish into a placeholder: stop the
    // submit and point them at the phone instead.
    if (f.action.indexOf('REPLACE') !== -1){
      f.addEventListener('submit', function(e){
        e.preventDefault();
        if (msg) msg.classList.add('show');
      });
      return;
    }

    // A native POST to Formspree navigates away to formspree.io. Asking Formspree for
    // JSON instead keeps the visitor on the page they were reading. The form keeps its
    // real action and method, so with JavaScript off the native POST still works: this
    // is an upgrade, not the only path.
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = f.querySelector('button[type=submit]');
      var said = btn ? btn.textContent : '';
      if (btn){ btn.disabled = true; btn.textContent = 'Sending...'; }
      function done(text, ok){
        if (msg){
          msg.textContent = text;
          msg.classList.add('show');
          msg.classList.toggle('is-error', !ok);
        }
        if (ok){ f.reset(); if (btn) btn.remove(); }
        else if (btn){ btn.disabled = false; btn.textContent = said; }
      }
      fetch(f.action, {
        method: 'POST',
        body: new FormData(f),
        headers: { Accept: 'application/json' }
      }).then(function(r){
        if (r.ok) done('Thank you. That came through, and Hope will be in touch soon.', true);
        else done('That did not go through. Please call or text Hope at (574) 377-8023 and she will get right back to you.', false);
      }).catch(function(){
        done('That did not go through. Please call or text Hope at (574) 377-8023 and she will get right back to you.', false);
      });
    });
  });

  // ---- gallery: two independent filters, by litter and by puppy
  var galGrid = document.querySelector('.gal-grid');
  if (galGrid){
    var fstate = { line: 'all', pup: 'all' };
    var countEl = document.getElementById('gal-count');
    function applyFilters(){
      var shown = 0;
      galGrid.querySelectorAll('a').forEach(function(it){
        var okLine = fstate.line === 'all' || it.getAttribute('data-line') === fstate.line;
        var okPup  = fstate.pup  === 'all' || it.getAttribute('data-pup')  === fstate.pup;
        var vis = okLine && okPup;
        it.style.display = vis ? '' : 'none';
        if (vis) shown++;
      });
      if (countEl) countEl.textContent =
        shown === 1 ? 'Showing 1 photo' : 'Showing ' + shown + ' photos';
    }
    function reset(sel, attr){
      document.querySelectorAll(sel).forEach(function(x){
        x.classList.toggle('cur', x.getAttribute(attr) === 'all');
      });
    }
    var pupSel = document.getElementById('pup-select');
    document.querySelectorAll('.filter-row button').forEach(function(b){
      b.addEventListener('click', function(){
        document.querySelectorAll('.filter-row button').forEach(function(x){
          x.classList.remove('cur'); });
        b.classList.add('cur');
        fstate.line = b.getAttribute('data-line');
        // a litter choice clears the puppy dropdown, so the two never fight
        if (pupSel){ pupSel.value = 'all'; pupSel.parentElement.classList.remove('on'); }
        fstate.pup = 'all';
        applyFilters();
      });
    });
    if (pupSel){
      pupSel.addEventListener('change', function(){
        fstate.pup = pupSel.value;
        pupSel.parentElement.classList.toggle('on', pupSel.value !== 'all');
        // and a puppy choice clears the litter buttons back to All
        if (pupSel.value !== 'all'){
          fstate.line = 'all';
          reset('.filter-row button', 'data-line');
        }
        applyFilters();
      });
    }
    applyFilters();
  }

  // ---- let's chat launcher, on every page
  /* a page that already carries the inquiry form does not need a launcher for it,
     and on a phone the fixed button lands squarely on top of a form field. */
  if (!document.querySelector('form[data-guard]')) {
  var fab = document.createElement('button');
  fab.className = 'chat-fab';
  fab.setAttribute('aria-expanded','false');
  fab.setAttribute('aria-label', 'Chat with us');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span class="fab-label">Let\u2019s Chat</span>';
  var panel = document.createElement('div');
  panel.className = 'chat-panel';
  panel.innerHTML = '<h3>Talk puppies with us</h3>'
    + '<p>Call or text is the fastest way to reach us. Hope and Joy raise the puppies between them.</p>'
    + '<div class="row"><span class="lbl">Hope</span><a href="tel:5743778023">(574) 377-8023</a></div>'
    + '<div class="row"><span class="lbl">Joy</span><a href="tel:5742651060">(574) 265-1060</a></div>'
    + '<div class="row"><span class="lbl">Email</span><a href="mailto:info@blessyourpawspuppies.com">info@blessyourpawspuppies.com</a></div>'
    + '<div class="row"><span class="lbl">Inquiry</span><a href="contact">Start an inquiry</a></div>'
    + '<div class="row"><span class="lbl">Waitlist</span><a href="waitlist">Join the waitlist</a></div>';
  document.body.appendChild(panel);
  document.body.appendChild(fab);
  fab.addEventListener('click', function(){
    var open = !panel.classList.contains('open');
    panel.classList.toggle('open', open);
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){ panel.classList.remove('open'); fab.setAttribute('aria-expanded','false'); }
  });
  }
})();

// ---- warming the next page, after this one is completely finished
// Nearly everyone who lands on the home page opens the puppies page next, and that page's
// photographs are the slowest thing on it. Fetching them while the visitor is still
// reading makes the click feel instant instead of costing another few hundred KB in front
// of them. Two rules keep this honest. It only ever requests URLs the next page would
// request anyway, so a visit that continues does not pay any extra: the bytes move
// earlier, they do not multiply. And it never competes with the page in front of the
// visitor: nothing starts before the load event, everything waits for an idle main
// thread, and every request goes out at low priority.
(function(){
  var c = navigator.connection || {};
  // do not spend somebody else's data plan on a guess
  if (c.saveData === true) return;
  if (/(^|-)2g$/.test(c.effectiveType || '')) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-data: reduce)').matches) return;

  var seen = {}, held = [], budget = 0;
  // a phone shows one card per row, so its card images are near full width and cost real
  // money. A desktop's are about 289px. Same photographs, very different bet.
  var CAP = (window.innerWidth || 1024) < 700 ? 4 : 10;

  // anything this page has already loaded is already in the cache, so it must not eat
  // into the cap. Keyed on srcset AND sizes: the same srcset with a different hint
  // resolves to a different file, which is the whole point of the hint.
  document.querySelectorAll('img[srcset],source[srcset]').forEach(function(n){
    seen[n.getAttribute('srcset') + '|' + (n.getAttribute('sizes') || '')] = 1;
  });

  function doc(href){
    if (!href || seen['d:' + href]) return;
    seen['d:' + href] = 1;
    var l = document.createElement('link');
    l.rel = 'prefetch';
    l.as = 'document';
    l.href = href;
    document.head.appendChild(l);
  }

  function pic(srcset, sizes, media){
    if (!srcset) return;
    if (media && window.matchMedia && !matchMedia(media).matches) return;
    var k = srcset + '|' + (sizes || '');
    if (seen[k] || budget >= CAP) return;
    seen[k] = 1;
    budget++;
    var i = new Image();
    i.fetchPriority = 'low';   // ignored where unsupported, which is harmless
    i.decoding = 'async';
    if (sizes) i.sizes = sizes;   // sizes BEFORE srcset: the candidate is chosen the
    i.srcset = srcset;            // moment srcset is set, and it chooses using sizes
    held.push(i);   // a detached Image can be collected mid-flight. Hold the reference.
  }

  function idle(fn){
    if (window.requestIdleCallback) requestIdleCallback(fn, {timeout: 3000});
    else setTimeout(fn, 1500);
  }

  function manifest(){
    var el = document.getElementById('warm');
    if (!el) return;
    var m;
    try { m = JSON.parse(el.textContent); } catch (e) { return; }
    (m.doc || []).forEach(doc);
    (m.img || []).forEach(function(a){ pic(a[0], a[1], a[2]); });
  }

  // whatever link the pointer, finger or keyboard is actually on beats any guess baked in
  // at build time, and costs one document. On a card it also warms the large version of
  // the photograph already showing in the card: same srcset, the puppy page's own hint.
  function intent(e){
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a || a.origin !== location.origin) return;
    if (a.pathname === location.pathname) return;
    if (/[.](pdf|zip)$/i.test(a.pathname)) return;   // a download, not a navigation
    // A character class, not a backslash-escaped dot: this JS lives inside a plain
    // Python string, where that escape is invalid and warns on every build.
    doc(a.href);
    var hint = a.getAttribute('data-warm-sizes');
    if (hint){
      var im = a.querySelector('img[srcset]');
      if (im) pic(im.getAttribute('srcset'), hint);
    }
  }

  function start(){
    idle(manifest);
    ['pointerover', 'touchstart', 'focusin'].forEach(function(t){
      document.addEventListener(t, intent, {passive: true});
    });
  }
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);
})();
