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
      document.querySelectorAll('[data-reveal]').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top > vh * 1.02) { el.classList.add('reveal-pending'); io.observe(el); }
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
})();
