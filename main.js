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

  // ---- guard: forms stay friendly until the Formspree id exists
  document.querySelectorAll('form[data-guard]').forEach(function(f){
    if (f.action.indexOf('REPLACE') !== -1){
      f.addEventListener('submit', function(e){
        e.preventDefault();
        var msg = f.querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
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
  var fab = document.createElement('button');
  fab.className = 'chat-fab';
  fab.setAttribute('aria-expanded','false');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>Let\u2019s Chat';
  var panel = document.createElement('div');
  panel.className = 'chat-panel';
  panel.innerHTML = '<h3>Talk puppies with us</h3>'
    + '<p>Call or text is the fastest way to reach us. We are always happy to answer questions or set up a visit or video call.</p>'
    + '<div class="row"><span class="lbl">Call/Text</span><a href="tel:5743778023">(574) 377-8023</a></div>'
    + '<div class="row"><span class="lbl">Email</span><a href="mailto:info@blessyourpawspuppies.com">info@blessyourpawspuppies.com</a></div>'
    + '<div class="row"><span class="lbl">Inquiry</span><a href="contact.html">Start an inquiry</a></div>'
    + '<div class="row"><span class="lbl">Waitlist</span><a href="waitlist.html">Join the waitlist</a></div>';
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
})();
