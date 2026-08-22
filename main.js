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
      slides.forEach(function(s,k){ s.hidden = k !== i; });
      thumbs.forEach(function(t,k){ t.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      if (counter) counter.textContent = (i+1) + ' / ' + slides.length;
    }
    car.querySelector('.cprev').addEventListener('click', function(){ show(i-1); });
    car.querySelector('.cnext').addEventListener('click', function(){ show(i+1); });
    thumbs.forEach(function(t,k){ t.addEventListener('click', function(){ show(k); }); });
    car.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft') show(i-1);
      if (e.key === 'ArrowRight') show(i+1);
    });
    show(0);
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
    document.querySelectorAll('.filter-row').forEach(function(row){
      var isPup = row.hasAttribute('data-pupfilter');
      row.querySelectorAll('button').forEach(function(b){
        b.addEventListener('click', function(){
          row.querySelectorAll('button').forEach(function(x){ x.classList.remove('cur'); });
          b.classList.add('cur');
          if (isPup){
            fstate.pup = b.getAttribute('data-pup');
            // choosing one puppy clears the litter narrowing, so the pick always resolves
            if (fstate.pup !== 'all'){
              fstate.line = 'all';
              reset('.filter-row:not([data-pupfilter]) button', 'data-line');
            }
          } else {
            fstate.line = b.getAttribute('data-line');
            if (fstate.line !== 'all'){
              fstate.pup = 'all';
              reset('.filter-row[data-pupfilter] button', 'data-pup');
            }
          }
          applyFilters();
        });
      });
    });
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
