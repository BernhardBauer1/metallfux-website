/* METALLFUX – Navigation, Slideshow, Scroll-Animation, Lightbox, Anfrageformular */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobilmenü */
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  /* Untermenüs per Klick (Touch, Tastatur) */
  document.querySelectorAll('.nav-item > button.nav-link').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = !item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function (o) {
        if (o !== item) { o.classList.remove('open'); o.querySelector('.nav-link').setAttribute('aria-expanded', 'false'); }
      });
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item')) {
      document.querySelectorAll('.nav-item.open').forEach(function (o) {
        o.classList.remove('open'); o.querySelector('.nav-link').setAttribute('aria-expanded', 'false');
      });
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.nav-item.open').forEach(function (o) { o.classList.remove('open'); });
    }
  });

  /* Slideshow Startseite */
  var slides = document.querySelectorAll('.hero-slide');
  var dots = document.querySelectorAll('.hero-dot');
  var caption = document.querySelector('.hero-caption');
  if (slides.length > 1) {
    var cur = 0, timer = null;
    var show = function (i) {
      slides[cur].classList.remove('is-active');
      dots[cur] && dots[cur].setAttribute('aria-current', 'false');
      cur = (i + slides.length) % slides.length;
      slides[cur].classList.add('is-active');
      dots[cur] && dots[cur].setAttribute('aria-current', 'true');
      if (caption) caption.textContent = slides[cur].getAttribute('data-caption') || '';
    };
    var start = function () { if (!reduce) { stop(); timer = setInterval(function () { show(cur + 1); }, 7000); } };
    var stop = function () { if (timer) clearInterval(timer); timer = null; };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); start(); }); });
    var hero = document.querySelector('.hero');
    hero.addEventListener('mouseenter', stop);
    hero.addEventListener('mouseleave', start);
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    start();
  }

  /* Scroll-Animation: Inhalte bleiben sichtbar, bis zum ersten Scrollen.
     Danach werden nur Elemente unterhalb des Sichtbereichs kurz ausgeblendet und beim Hineinscrollen eingeblendet. */
  if (!reduce && 'IntersectionObserver' in window) {
    var armed = false;
    var arm = function () {
      if (armed) return; armed = true;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add('reveal-in');
            en.target.classList.remove('reveal-pending');
            io.unobserve(en.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      var vh = window.innerHeight;
      document.querySelectorAll('[data-reveal], .section-head').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top > vh * 1.02) {
          /* Nebeneinander liegende Karten kurz nacheinander einblenden */
          var prev = el.previousElementSibling, n = 0;
          while (prev && prev.classList.contains('reveal-pending') && n < 4) { n++; prev = prev.previousElementSibling; }
          if (n) el.style.setProperty('--d', (n * 0.12) + 's');
          el.classList.add('reveal-pending'); io.observe(el);
        }
      });
    };
    window.addEventListener('scroll', arm, { passive: true, once: true });
  }

  /* Lightbox für Galerien */
  var groups = {};
  document.querySelectorAll('a[data-lightbox]').forEach(function (a) {
    var g = a.getAttribute('data-lightbox');
    (groups[g] = groups[g] || []).push(a);
    a.addEventListener('click', function (e) { e.preventDefault(); openLb(g, groups[g].indexOf(a)); });
  });
  var lb = null, lbImg, lbCount, lbGroup, lbIdx, lastFocus;
  function icon(d) { return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + d + '"></path></svg>'; }
  function build() {
    lb = document.createElement('div');
    lb.className = 'lightbox'; lb.hidden = true;
    lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Bildansicht');
    lb.innerHTML = '<img alt=""><button class="lb-btn lb-close" type="button" aria-label="Schließen">' + icon('M6 6l12 12M18 6 6 18') + '</button>' +
      '<button class="lb-btn lb-prev" type="button" aria-label="Vorheriges Bild">' + icon('M15 6l-6 6 6 6') + '</button>' +
      '<button class="lb-btn lb-next" type="button" aria-label="Nächstes Bild">' + icon('M9 6l6 6-6 6') + '</button><div class="lb-count"></div>';
    document.body.appendChild(lb);
    lbImg = lb.querySelector('img'); lbCount = lb.querySelector('.lb-count');
    lb.querySelector('.lb-close').addEventListener('click', closeLb);
    lb.querySelector('.lb-prev').addEventListener('click', function () { step(-1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { step(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); sx = null; });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') closeLb();
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }
  function render() {
    var a = groups[lbGroup][lbIdx];
    lbImg.src = a.getAttribute('href');
    var im = a.querySelector('img');
    lbImg.alt = im ? im.alt : '';
    lbCount.textContent = (lbIdx + 1) + ' / ' + groups[lbGroup].length;
  }
  function openLb(g, i) {
    if (!lb) build();
    lastFocus = document.activeElement;
    lbGroup = g; lbIdx = i; render();
    lb.hidden = false; document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-close').focus();
  }
  function closeLb() { lb.hidden = true; document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
  function step(d) { var n = groups[lbGroup].length; lbIdx = (lbIdx + d + n) % n; render(); }

  /* Anfrageformular: sendet an anfrage.php (funktioniert am Webserver) */
  var form = document.getElementById('anfrage-form');
  if (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      status.hidden = true;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      btn.disabled = true; btn.textContent = 'Wird gesendet …';
      fetch(form.getAttribute('action'), { method: 'POST', body: new FormData(form) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) {
            status.className = 'form-status ok';
            status.textContent = 'Danke! Ihre Anfrage ist bei uns angekommen. Wir melden uns in der Regel innerhalb von zwei Werktagen.';
            form.reset();
          } else {
            throw new Error(res && res.error ? res.error : 'fail');
          }
        })
        .catch(function (err) {
          status.className = 'form-status err';
          status.textContent = (err && err.message && err.message !== 'fail' && err.message.indexOf('Failed') === -1 ? err.message + ' ' : '') +
            'Die Anfrage konnte gerade nicht gesendet werden. Bitte rufen Sie uns an (0664 9917 1224) oder schreiben Sie an office@metallfux-wien.at.';
        })
        .finally(function () { status.hidden = false; btn.disabled = false; btn.textContent = 'Anfrage absenden'; });
    });
  }
  // ---------- Beratungstermin ----------
  var app = document.getElementById('termin-app');
  if (app) {
    var daysEl = app.querySelector('.termin-days');
    var slotStep = app.querySelector('.termin-slots').parentNode;
    var slotsEl = app.querySelector('.termin-slots');
    var tform = document.getElementById('termin-form');
    var wahlEl = tform.querySelector('.termin-wahl');
    var tstatus = tform.querySelector('.form-status');
    var WT = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
    var WTL = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    var MON = ['Jänner', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
    var echteSeite = /metallfux-wien\.at$/.test(location.hostname);
    var daten = {}, tag = null;

    function d(iso) { var p = iso.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function demo() {
      var out = {}, t = new Date(); t.setHours(0, 0, 0, 0);
      for (var i = 1, n = 0; n < 18 && i < 40; i++) {
        var x = new Date(t.getTime() + i * 864e5), w = x.getDay();
        if (w === 0 || w === 6) continue;
        var iso = x.getFullYear() + '-' + ('0' + (x.getMonth() + 1)).slice(-2) + '-' + ('0' + x.getDate()).slice(-2);
        out[iso] = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'].filter(function (s, k) { return (k * 7 + i * 3) % 5 > 1; });
        n++;
      }
      return out;
    }
    function zeigeTage() {
      var keys = Object.keys(daten).filter(function (k) { return daten[k].length; });
      if (!keys.length) { daysEl.innerHTML = '<p class="hint">Derzeit sind keine freien Termine online verfügbar. Bitte rufen Sie uns an.</p>'; return; }
      daysEl.innerHTML = '';
      keys.forEach(function (k) {
        var x = d(k), b = document.createElement('button');
        b.type = 'button'; b.className = 'termin-day'; b.setAttribute('role', 'option'); b.dataset.tag = k;
        b.innerHTML = '<small>' + WT[x.getDay()] + '</small><b>' + x.getDate() + '.' + (x.getMonth() + 1) + '.</b><small>' + daten[k].length + ' frei</small>';
        b.addEventListener('click', function () { waehleTag(k); });
        daysEl.appendChild(b);
      });
    }
    function waehleTag(k) {
      tag = k;
      daysEl.querySelectorAll('.termin-day').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tag === k ? 'true' : 'false'); });
      slotsEl.innerHTML = '';
      daten[k].forEach(function (z) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'termin-slot'; b.setAttribute('role', 'option'); b.textContent = z + ' Uhr'; b.dataset.zeit = z;
        b.addEventListener('click', function () { waehleZeit(z); });
        slotsEl.appendChild(b);
      });
      slotStep.hidden = false; tform.hidden = true;
      slotStep.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    function waehleZeit(z) {
      slotsEl.querySelectorAll('.termin-slot').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.zeit === z ? 'true' : 'false'); });
      var x = d(tag);
      tform.elements.termin.value = tag + ' ' + z;
      wahlEl.innerHTML = 'Ihr Wunschtermin: <b>' + WTL[x.getDay()] + ', ' + x.getDate() + '. ' + MON[x.getMonth()] + ' um ' + z + ' Uhr</b>';
      tform.hidden = false; tstatus.hidden = true;
      tform.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function laden() {
      fetch(app.dataset.api + '?slots=1', { cache: 'no-store' })
        .then(function (r) { return r.json(); })
        .then(function (res) { if (!res || !res.ok) throw new Error(res && res.error || 'fail'); daten = res.slots || {}; zeigeTage(); })
        .catch(function () {
          if (!echteSeite) { app.querySelector('.termin-demo').hidden = false; daten = demo(); zeigeTage(); return; }
          daysEl.innerHTML = '<p class="hint">Die freien Termine können gerade nicht geladen werden. Bitte rufen Sie uns an (0664 9917 1224) oder schicken Sie eine <a href="anfrage.html">Anfrage</a>.</p>';
        });
    }
    laden();
    tform.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = tform.querySelector('button[type=submit]');
      if (!tform.checkValidity()) { tform.reportValidity(); return; }
      btn.disabled = true; btn.textContent = 'Wird gesendet …';
      fetch(tform.getAttribute('action'), { method: 'POST', body: new FormData(tform) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) {
            tstatus.className = 'form-status ok';
            tstatus.textContent = 'Danke! Ihre Terminanfrage ist bei uns angekommen. Sie bekommen innerhalb von 12 Stunden eine Bestätigung.';
            tform.querySelectorAll('.field, .fields, .consent, button[type=submit]').forEach(function (el) { el.hidden = true; });
          } else {
            if (res && res.vergeben) { daten[tag] = daten[tag].filter(function (z) { return z !== tform.elements.termin.value.slice(11); }); zeigeTage(); waehleTag(tag); }
            throw new Error(res && res.error ? res.error : 'fail');
          }
        })
        .catch(function (err) {
          tstatus.className = 'form-status err';
          tstatus.textContent = (err && err.message && err.message !== 'fail' && err.message.indexOf('Failed') === -1 ? err.message + ' ' : '') +
            (echteSeite ? 'Falls es nicht klappt: 0664 9917 1224 oder office@metallfux-wien.at.' : 'In der Vorschau wird nichts verschickt.');
        })
        .finally(function () { tstatus.hidden = false; btn.disabled = false; btn.textContent = 'Termin unverbindlich anfragen'; });
    });
  }
})();

/* Scroll-Effekte: Fortschrittsbalken, Kopfzeile, Titelbild-Parallax, Projekt-Band */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bar = document.querySelector('.scroll-progress');
  var header = document.querySelector('.site-header.is-home');
  var nav = document.getElementById('nav');
  var hero = document.querySelector('.hero');
  var heroSlides = hero && hero.querySelector('.hero-slides');
  var heroInner = hero && hero.querySelector('.hero-inner');
  var rows = [].slice.call(document.querySelectorAll('.band-row'));
  var band = document.querySelector('.band-rows');
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset, vh = window.innerHeight;
    var max = document.documentElement.scrollHeight - vh;
    if (bar && !reduce) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    if (header) header.classList.toggle('solid', y > 40 || (nav && nav.classList.contains('open')));
    if (reduce) return;
    if (hero && y < hero.offsetHeight) {
      var h = hero.offsetHeight;
      heroSlides.style.transform = 'translate3d(0,' + (y * 0.35) + 'px,0)';
      heroInner.style.transform = 'translate3d(0,' + (y * 0.12) + 'px,0)';
      heroInner.style.opacity = Math.max(0, 1 - y / (h * 0.65));
    }
    if (band) {
      var r = band.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) {
        var p = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
        rows.forEach(function (row) {
          var shift = Math.max(0, row.scrollWidth - window.innerWidth);
          var x = row.getAttribute('data-dir') === '1' ? -(1 - p) * shift : -p * shift;
          row.style.transform = 'translate3d(' + x + 'px,0,0)';
        });
      }
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  var burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', function () { setTimeout(update, 0); });
  update();
})();

/* Startseite: Produkte nach Innen / Außen filtern */
(function () {
  var btns = document.querySelectorAll('.pf-btn');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.pf-tile').forEach(function (t) {
        t.hidden = f !== 'alle' && t.getAttribute('data-area') !== f;
        t.classList.remove('reveal-pending'); t.classList.add('reveal-in');
      });
    });
  });
})();
