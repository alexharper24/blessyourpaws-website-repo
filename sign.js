// Bless Your Paws Puppies - health guarantee signing and PDF
(function(){
  var dataEl = document.getElementById('gdata');
  if (!dataEl) return;
  var G = JSON.parse(dataEl.textContent);
  function track(name, params){
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }
  function nowIndiana(){
    try {
      return new Date().toLocaleString('en-US', { timeZone: 'America/Indiana/Indianapolis',
        month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit',
        timeZoneName: 'short' });
    } catch (e) { return new Date().toString(); }
  }

  // ---- the PDF, built in the browser so nothing is stored anywhere but the family's device
  var libPromise = null;
  function loadLib(){
    if (libPromise) return libPromise;
    libPromise = new Promise(function(res, rej){
      var sc = document.createElement('script');
      sc.src = G.jspdf;
      sc.onload = function(){ res(window.jspdf.jsPDF); };
      sc.onerror = function(){ libPromise = null; rej(new Error('pdf library')); };
      document.head.appendChild(sc);
    });
    return libPromise;
  }
  function loadLogo(){
    return new Promise(function(res){
      var im = new Image();
      im.onload = function(){
        var w = 700, h = Math.round(im.naturalHeight * w / im.naturalWidth);
        var c = document.createElement('canvas'); c.width = w; c.height = h;
        var x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, w, h);
        x.drawImage(im, 0, 0, w, h);
        res({ src: c.toDataURL('image/jpeg', 0.9), w: w, h: h });
      };
      im.onerror = function(){ res(null); };
      im.src = G.logo;
    });
  }
  // the PDF's built-in fonts are Latin-1, so curly quotes go straight
  function latin(t){ return String(t || '').replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"'); }

  function makePdf(info){
    return Promise.all([loadLib(), loadLogo()]).then(function(r){
      var JsPDF = r[0], logo = r[1];
      var doc = new JsPDF({ unit: 'pt', format: 'letter' });
      var W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight();
      var M = 56, y = M;
      doc.setTextColor(34, 61, 44); doc.setDrawColor(34, 61, 44);
      function room(h){ if (y + h > H - M){ doc.addPage(); y = M + 10; } }
      function rich(runs, x0, width, size, lh){
        doc.setFontSize(size);
        var words = [];
        runs.forEach(function(run){
          latin(run[1]).split(/(\s+)/).forEach(function(w){ if (w) words.push([run[0], w]); });
        });
        // Lay the words out into lines first, then draw each line as whole strings of one
        // weight. Drawing word by word dropped spaces ("Yourpuppy") in the text layer.
        function measure(bold, t){ doc.setFont('helvetica', bold ? 'bold' : 'normal'); return doc.getTextWidth(t); }
        var lines = [[]], used = 0;
        words.forEach(function(w){
          var line = lines[lines.length - 1];
          if (/^\s+$/.test(w[1])){ if (line.length) { line.push([w[0], ' ']); used += measure(w[0], ' '); } return; }
          var tw = measure(w[0], w[1]);
          if (used + tw > width && line.length){
            while (line.length && line[line.length - 1][1] === ' ') line.pop();
            line = []; lines.push(line); used = 0;
          }
          line.push(w); used += tw;
        });
        lines.forEach(function(line){
          room(lh);
          var x = x0, seg = '', bold = null;
          function flush(){
            if (!seg) return;
            doc.setFont('helvetica', bold ? 'bold' : 'normal');
            doc.text(seg, x, y); x += doc.getTextWidth(seg); seg = '';
          }
          line.forEach(function(w){
            if (w[0] !== bold){ flush(); bold = w[0]; }
            seg += w[1];
          });
          flush();
          y += lh;
        });
      }
      if (logo){
        var lw = 190, lh = lw * logo.h / logo.w;
        doc.addImage(logo.src, 'JPEG', (W - lw) / 2, y, lw, lh); y += lh + 18;
      }
      doc.setFont('helvetica', 'bold'); doc.setFontSize(18);
      var pup = info && info.puppy;
      doc.text(pup ? 'Health guarantee for ' + pup.name : 'Health guarantee', W / 2, y, { align: 'center' });
      y += 16;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(9);
      doc.text(latin(G.contact), W / 2, y, { align: 'center' });
      y += 26;

      G.blocks.forEach(function(b){
        if (b[0] === 'h'){
          y += 6; room(40);
          doc.setFont('helvetica', 'bold'); doc.setFontSize(12);
          doc.text(latin(b[1][0][1]), M, y); y += 16;
        } else if (b[0] === 'li'){
          room(14); doc.circle(M + 4, y - 3.2, 1.6, 'F');
          rich(b[1], M + 14, W - 2 * M - 14, 10, 13.5); y += 3;
        } else {
          rich(b[1], M, W - 2 * M, 10, 13.5); y += 6;
        }
      });

      // ---- the signature block. Blank lines on a print copy, the family's entries on theirs.
      y += 8; room(250);
      doc.setLineWidth(0.6); doc.line(M, y, W - M, y); y += 22;
      doc.setFont('helvetica', 'bold'); doc.setFontSize(12);
      doc.text('Signed', M, y); y += 18;
      rich([[0, G.agree]], M, W - 2 * M, 10, 13.5); y += 8;
      function row(label, value){
        room(24);
        doc.setFont('helvetica', 'bold'); doc.setFontSize(9.5);
        doc.text(label, M, y);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
        if (value){
          var lines = doc.splitTextToSize(latin(value), W - 2 * M - 150);
          doc.text(lines, M + 150, y); y += 15 * lines.length + 5;
        } else {
          doc.setLineWidth(0.4); doc.line(M + 150, y + 2, W - M, y + 2); y += 24;
        }
      }
      var addr = info ? [info.street, [info.city, info.state].filter(Boolean).join(', ') + ' ' + (info.zip || '')].join('\n') : '';
      row('Puppy', pup ? pup.name + ' (' + pup.sex.toLowerCase() + ', ' + pup.color.toLowerCase() + ')' : '');
      row('Buyer name', info ? info.name : '');
      row('Address', addr);
      if (!info) row('', '');
      row('Phone', info ? info.phone : '');
      row('Email', info ? info.email : '');
      row('Told to me before purchase', info ? (info.disclosed || 'Nothing entered') : '');
      if (!info) row('', '');
      y += 10; room(60);
      doc.setFont('helvetica', 'bold'); doc.setFontSize(9.5);
      doc.text('Buyer signature', M, y);
      if (info){
        doc.setFont('times', 'italic'); doc.setFontSize(20);
        doc.text(latin(info.signature), M + 150, y);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(9);
        y += 14;
        doc.text('Signed electronically on ' + latin(info.when), M + 150, y);
        y += 26;
      } else {
        doc.setLineWidth(0.4); doc.line(M + 150, y + 2, W - M - 140, y + 2);
        doc.text('Date', W - M - 128, y); doc.line(W - M - 100, y + 2, W - M, y + 2);
        y += 34;
      }
      room(30);
      doc.setFont('helvetica', 'bold'); doc.setFontSize(9.5);
      doc.text('Breeder signature', M, y);
      doc.setLineWidth(0.4); doc.line(M + 150, y + 2, W - M - 140, y + 2);
      doc.text('Date', W - M - 128, y); doc.line(W - M - 100, y + 2, W - M, y + 2);

      // a footer on every page, so the signature page is plainly part of the same document
      var total = doc.getNumberOfPages();
      for (var pg = 1; pg <= total; pg++){
        doc.setPage(pg);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5);
        doc.text('Bless Your Paws Puppies health guarantee' + (pup ? ' for ' + pup.name : '')
          + ', page ' + pg + ' of ' + total, W / 2, H - 30, { align: 'center' });
      }

      var name = 'Bless Your Paws health guarantee'
        + (pup ? ' - ' + pup.name : ' - blank')
        + (info && info.name ? ' - ' + info.name : '') + '.pdf';
      doc.save(name.replace(/[\\/:*?"<>|]/g, ''));
    });
  }
  function pdfButton(btn, getInfo){
    btn.addEventListener('click', function(){
      var said = btn.textContent;
      btn.disabled = true; btn.textContent = 'Preparing the PDF...';
      makePdf(getInfo()).then(function(){
        btn.disabled = false; btn.textContent = said;
      }).catch(function(){
        btn.disabled = false;
        btn.textContent = 'That did not work. Please try again.';
        setTimeout(function(){ btn.textContent = said; }, 3000);
      });
    });
  }
  document.querySelectorAll('[data-blank-pdf]').forEach(function(b){
    pdfButton(b, function(){ return null; });
  });

  // ---- the signing page
  var form = document.querySelector('form[data-sign]');
  if (form){
    var sel = form.querySelector('#gpup');
    var want = '';
    try { want = (new URLSearchParams(location.search).get('puppy') || '').toLowerCase(); } catch (e) {}
    if (want && G.puppies[want]) sel.value = want;
    var title = document.getElementById('gtitle');
    function showPup(){
      var slug = sel.value;
      document.querySelectorAll('[data-pupcard]').forEach(function(c){
        c.hidden = c.getAttribute('data-pupcard') !== slug;
        // the cards start hidden and lazy, so only the one shown downloads, and it eagerly
        var im = c.querySelector('img');
        if (!c.hidden && im) im.loading = 'eager';
      });
      title.textContent = G.puppies[slug] ? 'Health guarantee for ' + G.puppies[slug].name
        : 'Sign your health guarantee';
    }
    sel.addEventListener('change', showPup);
    showPup();

    var msg = form.querySelector('.guard-msg');
    var signed = null;
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      var said = btn.textContent;
      var fd = new FormData(form);
      var slug = sel.value, pup = G.puppies[slug];
      var when = nowIndiana();
      fd.set('puppy', pup ? pup.name : slug);
      fd.append('Signed (Indiana time)', when);
      fd.append('_subject', 'Signed health guarantee: ' + (pup ? pup.name : '') + ', ' + fd.get('name'));
      fd.append('guarantee_text', G.plain);
      btn.disabled = true; btn.textContent = 'Signing...';
      msg.classList.remove('show', 'is-error');
      fetch(form.action, { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
        .then(function(r){
          if (!r.ok) throw new Error('send');
          track('guarantee_signed', { puppy: slug });
          signed = { puppy: pup, name: fd.get('name'), email: fd.get('email'),
            phone: fd.get('phone'), street: fd.get('address_street'),
            city: fd.get('address_city'), state: fd.get('address_state'),
            zip: fd.get('address_zip'), disclosed: (fd.get('disclosed') || '').trim(),
            signature: fd.get('signature'), when: when };
          form.hidden = true;
          var done = document.getElementById('gdone');
          done.hidden = false;
          done.focus();
          done.scrollIntoView({ block: 'start' });
        })
        .catch(function(){
          btn.disabled = false; btn.textContent = said;
          msg.textContent = 'That did not go through. Please try again, or call or text Hope at '
            + G.phone + '.';
          msg.classList.add('show', 'is-error');
        });
    });
    pdfButton(document.getElementById('gdownload'), function(){ return signed; });
  }

  // ---- Hope's link page: copy a family's link
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click', function(){
      var text = b.getAttribute('data-copy'), said = b.textContent;
      function ok(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = said; }, 1800); }
      function fallback(){
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'absolute';
        ta.style.left = '-9999px'; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); ok(); } catch (e) {}
        ta.remove();
      }
      if (navigator.clipboard && navigator.clipboard.writeText)
        navigator.clipboard.writeText(text).then(ok, fallback);
      else fallback();
    });
  });
})();
