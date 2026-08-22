// Bless Your Paws Puppies - v1
(function(){
  // mobile nav overlay. fixed at every width so it never becomes a flex item.
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

  // guard: payment links stay friendly until the real Stripe links exist
  document.querySelectorAll('a.pay-link').forEach(function(a){
    if (a.href.indexOf('REPLACE') !== -1){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var msg = a.closest('.reserve').querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // guard: forms stay friendly until the Formspree id exists
  document.querySelectorAll('form[data-guard]').forEach(function(f){
    if (f.action.indexOf('REPLACE') !== -1){
      f.addEventListener('submit', function(e){
        e.preventDefault();
        var msg = f.querySelector('.guard-msg');
        if (msg) msg.classList.add('show');
      });
    }
  });

  // puppy page: thumb click swaps the main photo
  var main = document.getElementById('gallery-main');
  if (main){
    document.querySelectorAll('.thumbs button').forEach(function(b){
      b.addEventListener('click', function(){
        main.src = b.getAttribute('data-src');
        main.removeAttribute('srcset');
        document.querySelectorAll('.thumbs button').forEach(function(x){ x.classList.remove('cur'); });
        b.classList.add('cur');
      });
    });
  }

  // gallery page filter
  var filters = document.querySelectorAll('.filter-row button');
  if (filters.length){
    filters.forEach(function(b){
      b.addEventListener('click', function(){
        filters.forEach(function(x){ x.classList.remove('cur'); });
        b.classList.add('cur');
        var want = b.getAttribute('data-line');
        document.querySelectorAll('.gal-grid a').forEach(function(item){
          item.style.display = (want === 'all' || item.getAttribute('data-line') === want) ? '' : 'none';
        });
      });
    });
  }
})();
