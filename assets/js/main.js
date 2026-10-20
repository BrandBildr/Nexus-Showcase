/* Nexus Resourcing Group: site interactions */
(() => {
  // Swap this for Nick's real Cal.com booking link
  const CAL_URL = 'https://cal.com/nick-souness';

  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = !!(window.gsap && window.ScrollTrigger);
  const animate = !reduce && hasGsap;
  if (!animate) root.classList.remove('js-anim');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  // iOS/Android address bars resize the viewport while scrolling; don't recalculate every trigger when they do
  if (hasGsap) ScrollTrigger.config({ ignoreMobileResize: true });

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const nav = $('#nav');
  const navH = () => (nav ? nav.offsetHeight : 0);
  const isLocal = /^(localhost|127\.|file)/.test(location.hostname || 'file');

  $$('[data-cal]').forEach(a => (a.href = CAL_URL));
  $$('[data-year]').forEach(el => (el.textContent = new Date().getFullYear()));

  // Run one feature without letting a failure break the rest of the page
  const safely = fn => { try { fn(); } catch (e) { console.error(e); root.classList.remove('js-anim'); } };

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (animate && window.Lenis) safely(() => {
    if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return; // phones and tablets keep native scrolling
    lenis = new Lenis({ lerp: 0.12, smoothWheel: true, wheelMultiplier: 1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  });
  const scrollToEl = (el, immediate = false) => {
    // sector sections get a little extra room so the sticky sector pills never touch the heading
    const offset = el.id === 'top' ? 0 : -navH() + 1 - (el.classList.contains('sector') ? 20 : 0);
    if (lenis) lenis.scrollTo(el, { offset, duration: immediate ? 0 : 1.1, immediate });
    else window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY + offset, behavior: reduce || immediate ? 'auto' : 'smooth' });
  };

  // Same-page anchors scroll smoothly
  $$('a[href*="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || !url.hash) return;
      const target = url.hash === '#top' ? $('#top') : document.getElementById(url.hash.slice(1));
      if (!target) return;
      e.preventDefault();
      if (a.dataset.contactTab && window.__setContactTab) window.__setContactTab(a.dataset.contactTab, false);
      closeMenu(false);
      scrollToEl(target);
      history.replaceState(null, '', url.hash === '#top' ? location.pathname : url.hash);
    });
  });

  /* ---------- nav: solid on scroll, hides on the way down ---------- */
  if (nav) {
    let lastY = window.scrollY, anchorY = lastY, hidden = false, solid = null, ticking = false;
    const firstSection = $('.hero, .phero, .lost');
    const update = () => {
      ticking = false;
      const y = Math.max(0, window.scrollY);
      const limit = firstSection ? firstSection.offsetHeight : 200;
      const s = y > 40;
      if (s !== solid) { solid = s; nav.classList.toggle('is-solid', s); }
      // change direction only after a real move: 24px down to hide, 12px up to show
      if ((y > lastY) !== (lastY > anchorY)) anchorY = lastY;
      let h = hidden;
      if (y <= limit) h = false;
      else if (y - anchorY > 24) h = true;
      else if (anchorY - y > 12) h = false;
      if (h !== hidden) { hidden = h; nav.classList.toggle('is-hidden', h); root.classList.toggle('nav-hidden', h); }
      lastY = y;
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    update();
  }

  /* ---------- pause looping pulses while they're off screen ---------- */
  if ('IntersectionObserver' in window) {
    const loopIo = new IntersectionObserver(entries => entries.forEach(en => en.target.classList.toggle('is-offscreen', !en.isIntersecting)));
    $$('.hero__scroll, .wmap, .hiring, .sector').forEach(el => loopIo.observe(el));
  }

  /* ---------- mobile quick-contact bar ---------- */
  const quickbar = $('.quickbar');
  if (quickbar) {
    // hide it wherever the page already offers a way to get in touch
    const blockers = $$('.hero, .phero, .contact, .register, .cta-band, .foot, .hiring');
    const inView = new Set();
    const update = () => quickbar.classList.toggle('is-visible', inView.size === 0);
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => (en.isIntersecting ? inView.add(en.target) : inView.delete(en.target)));
      update();
    }, { rootMargin: '0px 0px -10% 0px' });
    blockers.forEach(b => io.observe(b));
  }

  /* ---------- mobile menu ---------- */
  const toggle = $('.nav__toggle');
  const menu = $('#menu');
  function openMenu() {
    if (!menu) return;
    menu.hidden = false;
    requestAnimationFrame(() => menu.classList.add('is-open'));
    toggle.setAttribute('aria-expanded', 'true');
    nav.classList.add('menu-open');
    root.classList.add('menu-lock');
    if (lenis) lenis.stop();
    const first = $('a', menu);
    if (first) first.focus({ preventScroll: true });
  }
  function closeMenu(returnFocus = true) {
    if (!menu || menu.hidden) return;
    menu.classList.remove('is-open');
    menu.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('menu-open');
    root.classList.remove('menu-lock');
    if (lenis) lenis.start();
    if (returnFocus) toggle.focus();
  }
  if (toggle && menu) {
    toggle.addEventListener('click', () => (menu.hidden ? openMenu() : closeMenu()));
    document.addEventListener('keydown', e => {
      if (menu.hidden) return;
      if (e.key === 'Escape') closeMenu();
      if (e.key === 'Tab') {
        // keep focus inside the open menu (toggle + menu links)
        const items = [toggle, ...$$('a, button', menu)];
        const i = items.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
      }
    });
    matchMedia('(min-width: 981px)').addEventListener('change', e => e.matches && closeMenu(false));
  }

  /* ---------- headings that rise word by word ---------- */
  const splitWords = h => {
    h.setAttribute('aria-label', h.textContent.trim());
    h.innerHTML = h.textContent.trim().split(/\s+/).map(w =>
      `<span class="w" aria-hidden="true" style="display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.08em;margin-bottom:-.08em"><span style="display:inline-block">${w}</span></span>`
    ).join(' ');
    return $$('.w > span', h);
  };

  /* ---------- home hero: the letters converge ---------- */
  if ($('.hero') && animate) safely(() => {
    // Full sequence on the first visit in a session, a quicker one after that
    let seen = false;
    try { seen = sessionStorage.getItem('nx-intro') === '1'; sessionStorage.setItem('nx-intro', '1'); } catch (_) {}
    const k = seen ? 0.45 : 1;
    const wms = $$('.wm');
    const small = innerWidth < 700;
    const spread = Math.min(window.innerWidth * 0.16, 220);
    const tl = gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.15 * k });
    tl.fromTo('.hero__img', { scale: 1.18 }, { scale: 1.04, duration: 3.2 * k, ease: 'power2.out' }, 0)
      .fromTo(wms,
        { opacity: 0, x: i => (i - 2) * spread * 2.2, filter: small ? 'none' : 'blur(14px)' },
        { opacity: 1, x: 0, filter: small ? 'none' : 'blur(0px)', duration: 1.8 * k, stagger: { each: 0.06 * k, from: 'edges' } }, 0.25 * k)
      .fromTo('.wm--x', { rotate: -90, scale: 1.4 }, { rotate: 0, scale: 1, duration: 1.6 * k }, 0.35 * k)
      .fromTo('.hero__icon', { opacity: 0, scale: 0.55, rotate: -45, y: 20 }, { opacity: 1, scale: 1, rotate: 0, y: 0, duration: 1.6 * k }, 0.9 * k)
      .fromTo('.hero__shine', { backgroundPosition: '150% 0' }, { backgroundPosition: '-60% 0', duration: 1.6, ease: 'power2.inOut' }, 1.7 * k)
      .to('.hero__group .rule', { scaleX: 1, duration: 1.2 * k }, 1.3 * k)
      .fromTo('.hero__group-text', { opacity: 0, letterSpacing: '0.9em' }, { opacity: 1, letterSpacing: '0.42em', duration: 1.4 * k }, 1.3 * k)
      .fromTo('.hero__tag', { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 1 * k }, 1.75 * k)
      .fromTo('.hero__ctas > *', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 1 * k, stagger: 0.1 * k }, 1.95 * k)
      .to('.hero__scroll', { opacity: 1, duration: 1 }, 2.4 * k);

    gsap.to('.hero__media', { yPercent: 14, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero__content', { y: -90, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: '75% top', scrub: true } });
  });

  /* ---------- inner page hero: one orchestrated entrance ---------- */
  if ($('.phero') && animate) safely(() => {
    const h = $('.phero__title[data-split]');
    const words = h ? splitWords(h) : [];
    const tl = gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.05 });
    tl.fromTo('.phero__kicker', { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 1 }, 0);
    if (words.length) tl.from(words, { yPercent: 110, duration: 1.2, stagger: 0.05 }, 0.1);
    tl.fromTo('.phero__lede', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 1.1 }, 0.5)
      .fromTo('.phero__actions', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 1.1 }, 0.62)
      .fromTo('.phero__media', { opacity: 0, clipPath: 'inset(0 0 100% 0 round 22px)' }, { opacity: 1, clipPath: 'inset(0 0 0% 0 round 22px)', duration: 1.4, ease: 'expo.inOut' }, 0.2)
      .fromTo('.mosaic img', { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 1.2, stagger: 0.08 }, 0.25)
      .set('.mosaic', { opacity: 1 }, 0.25)
      .fromTo('.phero__mark', { rotate: -25, opacity: 0 }, { rotate: 0, opacity: 0.045, duration: 2.2 }, 0);

    if (innerWidth >= 700) gsap.to('.phero__mark', { rotate: 18, ease: 'none', scrollTrigger: { trigger: '.phero', start: 'top top', end: 'bottom top', scrub: true } });
    if ($('.phero__media img')) gsap.fromTo('.phero__media img', { yPercent: -6 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: '.phero', start: 'top top', end: 'bottom top', scrub: true } });
  });

  /* ---------- section headings (home about) ---------- */
  if (animate) safely(() => {
    $$('.about__title[data-split]').forEach(h => {
      gsap.from(splitWords(h), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.04, scrollTrigger: { trigger: h, start: 'top 80%' } });
    });
  });

  /* ---------- process steps: the line fills as you read ---------- */
  $$('.steps-wrap').forEach(wrap => {
    const steps = $$('.step', wrap);
    if (!animate) { steps.forEach(s => s.classList.add('is-lit')); return; }
    safely(() => gsap.to($('.steps__fill', wrap), {
      scaleX: 1, ease: 'none',
      scrollTrigger: {
        trigger: wrap, start: 'top 75%', end: 'bottom 55%', scrub: 0.6,
        onUpdate: self => steps.forEach((s, i) => s.classList.toggle('is-lit', self.progress >= i / steps.length + 0.02 || (i === 0 && self.progress > 0)))
      }
    }));
  });

  /* ---------- Nick: count up, drifting mark ---------- */
  if (animate) safely(() => {
    $$('.count').forEach(c => {
      const obj = { v: 0 };
      gsap.to(obj, { v: +c.dataset.to, duration: 1.6, ease: 'power3.out', onUpdate: () => (c.textContent = Math.round(obj.v)), scrollTrigger: { trigger: c, start: 'top 85%' } });
    });
    if (innerWidth >= 700) $$('.nick').forEach(sec => {
      const mark = $('.nick__mark', sec);
      if (mark) gsap.fromTo(mark, { rotate: -20 }, { rotate: 15, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    if (innerWidth >= 700) $$('.cta-band').forEach(sec => gsap.fromTo($('.cta-band__mark', sec), { rotate: -30, scale: 0.85 }, { rotate: 10, scale: 1.05, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: true } }));
  });

  /* ---------- About: the usual way gets struck through ---------- */
  if ($('.compare') && animate) safely(() => {
    const items = $$('.compare__col--old li span');
    items.forEach(s => s.style.setProperty('--strike', '0%'));
    items.forEach((s, i) => {
      const st = { v: 0 };
      gsap.to(st, {
        v: 100, ease: 'none',
        onUpdate: () => s.style.setProperty('--strike', st.v + '%'),
        scrollTrigger: { trigger: '.compare__grid', start: `top ${78 - i * 6}%`, end: `top ${58 - i * 6}%`, scrub: 0.5 }
      });
    });
  });

  /* ---------- home: sector panels ---------- */
  const panels = $$('.panel');
  if (panels.length) {
    const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
    let hoverTimer;
    const activate = p => panels.forEach(x => {
      const on = x === p;
      x.classList.toggle('is-active', on);
      x.setAttribute('aria-expanded', on);
    });
    panels.forEach((p, i) => {
      p.addEventListener('click', () => activate(p));
      if (finePointer) {
        p.addEventListener('mouseenter', () => { clearTimeout(hoverTimer); hoverTimer = setTimeout(() => activate(p), 140); });
        p.addEventListener('mouseleave', () => clearTimeout(hoverTimer));
      }
      p.addEventListener('keydown', e => {
        const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (!k) return;
        e.preventDefault();
        const next = panels[(i + k + panels.length) % panels.length];
        activate(next); next.focus();
      });
    });
  }

  /* ---------- sectors page: index follows your place ---------- */
  const index = $('.sector-index');
  if (index) {
    const links = $$('a', index);
    const ul = $('ul', index);
    const bar = document.createElement('span');
    bar.className = 'sector-index__bar';
    ul.appendChild(bar);
    const setCurrent = id => {
      links.forEach(l => {
        const on = l.hash === '#' + id;
        l.classList.toggle('is-current', on);
        if (on) {
          l.setAttribute('aria-current', 'true');
          bar.style.transform = `translateY(${l.offsetTop}px)`;
          bar.style.height = l.offsetHeight + 'px';
          // keep the active pill in view on mobile
          if (ul.scrollWidth > ul.clientWidth) ul.scrollTo({ left: l.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
        } else l.removeAttribute('aria-current');
      });
    };
    const io = new IntersectionObserver(entries => entries.forEach(en => en.isIntersecting && setCurrent(en.target.id)), { rootMargin: '-40% 0px -55% 0px' });
    $$('.sector').forEach(s => io.observe(s));
    setCurrent('marine');
  }

  /* ---------- vacancies: tap a role to open it ---------- */
  $$('.vac__pill').forEach(btn => {
    btn.addEventListener('click', () => {
      const li = btn.closest('.vac');
      const open = !li.classList.contains('is-open');
      li.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open);
      if (hasGsap) setTimeout(() => ScrollTrigger.refresh(), 600);
    });
  });

  /* ---------- world map: pins drop in, tap or hover to highlight ---------- */
  $$('[data-map]').forEach(map => {
    const pins = $$('.wmap__pin', map);
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { map.classList.add('is-in'); io.disconnect(); }
    }), { threshold: 0.25 });
    io.observe(map);
    const legend = $$('.wmap__legend button', map);
    const small = matchMedia('(max-width: 700px)');
    const activate = pin => {
      // on phones one location is always shown; on desktop all labels are visible anyway
      if (!pin && small.matches) pin = pins[0];
      pins.forEach(p => p.classList.toggle('is-active', p === pin));
      legend.forEach(b => b.setAttribute('aria-pressed', pins[+b.dataset.pin] === pin));
    };
    pins.forEach(pin => {
      const dot = $('.wmap__dot', pin);
      ['mouseenter', 'focus', 'click'].forEach(ev => dot.addEventListener(ev, () => activate(pin)));
    });
    legend.forEach(b => b.addEventListener('click', () => activate(pins[+b.dataset.pin])));
    map.addEventListener('mouseleave', () => activate(null));
    small.addEventListener('change', () => activate(null));
    activate(null);
  });

  /* ---------- candidates: arriving from a vacancy fills in the role ---------- */
  const params = new URLSearchParams(location.search);
  if (params.get('role') && $('#c-trade')) {
    $('#c-trade').value = params.get('role');
    const msg = $('#c-msg');
    if (msg && !msg.value) msg.value = `Applying for: ${params.get('role')}${params.get('loc') ? ' (' + params.get('loc') + ')' : ''}`;
  }

  /* ---------- arriving with a #hash from another page ---------- */
  if (location.hash && location.hash.length > 1) {
    const t = document.getElementById(location.hash.slice(1));
    if (t) window.addEventListener('load', () => setTimeout(() => scrollToEl(t, true), 60));
  }

  /* ---------- contact card: call or enquiry ---------- */
  const sw = $('.switch');
  if (sw) {
    const panes = $('.panes');
    const setTab = (name, focus = true) => {
      if (sw.dataset.active === name) return;
      const from = panes.offsetHeight;
      sw.dataset.active = name;
      $$('.switch__btn').forEach(b => {
        const on = b.dataset.tab === name;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-selected', on);
      });
      $$('.pane').forEach(p => {
        const on = p.id === 'pane-' + name;
        p.hidden = !on;
        p.classList.toggle('is-entering', on);
      });
      const to = panes.offsetHeight;
      if (!reduce) {
        panes.style.height = from + 'px';
        requestAnimationFrame(() => {
          panes.style.height = to + 'px';
          setTimeout(() => (panes.style.height = ''), 650);
        });
      }
      if (focus) $('#tab-' + name).focus();
      if (hasGsap) setTimeout(() => ScrollTrigger.refresh(), 700);
    };
    window.__setContactTab = setTab;
    sw.dataset.active = 'call';
    $$('.switch__btn').forEach(b => b.addEventListener('click', () => setTab(b.dataset.tab)));
    $$('[data-tab-jump]').forEach(b => b.addEventListener('click', () => setTab(b.dataset.tabJump)));

    // /contact/?sector=Marine opens the enquiry form with that sector chosen
    const sector = new URLSearchParams(location.search).get('sector');
    const sel = $('#f-sector');
    if (sector && sel && [...sel.options].some(o => o.value === sector)) {
      sel.value = sector;
      setTab('enquiry', false);
    }
  }

  /* ---------- form helpers ---------- */
  const fieldOk = f => {
    if (f.type === 'checkbox') return f.checked;
    if (f.type === 'email') return /^\S+@\S+\.\S+$/.test(f.value.trim());
    if (f.type === 'tel') return f.value.replace(/\D/g, '').length >= 10;
    return f.value.trim().length > 1;
  };
  const markField = (f, ok) => {
    const wrap = f.closest('.field, .consent');
    if (wrap) wrap.classList.toggle('is-invalid', !ok);
  };
  const messageFor = f => {
    if (f.type === 'email') return 'Enter a valid email address so we can reply.';
    if (f.type === 'tel') return 'Enter a phone number we can call you on.';
    if (f.type === 'checkbox') return 'Tick the box to agree to us storing your details.';
    return 'Fill in the highlighted fields to continue.';
  };
  const submitForm = async (form, multipart) => {
    let ok = false;
    try {
      const fd = new FormData(form);
      const res = multipart
        ? await fetch(form.getAttribute('action') || '/', { method: 'POST', body: fd })
        : await fetch(form.getAttribute('action') || '/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(fd).toString() });
      ok = res.ok;
    } catch (_) { ok = false; }
    // Local previews have no form handler, so show the success state there
    return ok || isLocal;
  };

  /* ---------- enquiry form ---------- */
  $$('form[data-form="enquiry"]').forEach(form => {
    const card = form.closest('.pane') || form.parentElement;
    const sent = $('.sent', card);
    const err = $('.form__error', form);
    const msgLabel = $('[data-msg-label]', form);
    const company = $('[data-client-only]', form);
    const note = $('[data-candidate-only]', form);
    form.addEventListener('change', e => {
      if (e.target.name !== 'enquiry-type') return;
      const candidate = e.target.value === 'Candidate';
      company.hidden = candidate;
      if (note) note.hidden = !candidate;
      msgLabel.textContent = candidate ? 'Tell us about your experience and the work you want' : 'Tell us about the project';
    });
    form.addEventListener('input', e => {
      const w = e.target.closest('.is-invalid');
      if (w) w.classList.remove('is-invalid');
      if (!$('.is-invalid', form)) err.hidden = true;
    });
    form.addEventListener('submit', async e => {
      e.preventDefault();
      err.hidden = true;
      let first = null;
      $$('[required]', form).forEach(f => { const ok = fieldOk(f); markField(f, ok); if (!ok && !first) first = f; });
      if (first) { err.textContent = messageFor(first); err.hidden = false; first.focus(); return; }
      const btn = $('button[type="submit"]', form);
      btn.disabled = true; btn.textContent = 'Sending…';
      const ok = await submitForm(form, false);
      btn.disabled = false; btn.textContent = 'Send enquiry';
      if (!ok) { err.textContent = "Your enquiry didn't send. Try again, or email nick@nexusrg.co.uk directly."; err.hidden = false; return; }
      form.hidden = true; sent.hidden = false; sent.focus();
    });
    const reset = $('[data-reset-form]', card);
    if (reset) reset.addEventListener('click', () => {
      form.reset(); company.hidden = false; if (note) note.hidden = true;
      msgLabel.textContent = 'Tell us about the project';
      sent.hidden = true; form.hidden = false; $('input[name="name"]', form).focus();
    });
  });

  /* ---------- candidate registration: three steps ---------- */
  const reg = $('form[data-form="candidate"]');
  if (reg) {
    const steps = $$('.reg__step', reg);
    const crumbs = $$('.reg-progress li');
    const bar = $('.reg-progress__bar span');
    const prev = $('[data-prev]', reg), next = $('[data-next]', reg), submit = $('[data-submit]', reg);
    const err = $('.form__error', reg);
    const card = reg.closest('.reg-card');
    let current = 0;

    const show = (i, back = false) => {
      steps.forEach((s, n) => {
        s.hidden = n !== i;
        s.classList.toggle('is-active', n === i);
        s.classList.toggle('is-entering', n === i);
        s.classList.toggle('is-back', n === i && back);
      });
      crumbs.forEach((c, n) => {
        c.classList.toggle('is-active', n === i);
        c.classList.toggle('is-done', n < i);
        if (n === i) c.setAttribute('aria-current', 'step'); else c.removeAttribute('aria-current');
      });
      bar.style.width = ((i + 1) / steps.length * 100) + '%';
      prev.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
      err.hidden = true;
      current = i;
      const firstInput = $('input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=file]), textarea', steps[i]);
      if (firstInput && i > 0) firstInput.focus({ preventScroll: true });
      if (card.getBoundingClientRect().top < navH()) scrollToEl(card);
      if (hasGsap) setTimeout(() => ScrollTrigger.refresh(), 600);
    };

    const validateStep = i => {
      let first = null;
      $$('[required]', steps[i]).forEach(f => { const ok = fieldOk(f); markField(f, ok); if (!ok && !first) first = f; });
      // Step 2 needs at least one sector
      const pick = $('.pick:not(.pick--radio)', steps[i]);
      if (pick && !$$('input:checked', pick).length) {
        pick.classList.add('is-invalid');
        if (!first) { err.textContent = 'Choose at least one sector you work in.'; err.hidden = false; $('input', pick).focus(); return false; }
      }
      if (first) { err.textContent = messageFor(first); err.hidden = false; first.focus(); return false; }
      return true;
    };

    next.addEventListener('click', () => validateStep(current) && show(current + 1));
    prev.addEventListener('click', () => show(current - 1, true));
    reg.addEventListener('input', e => {
      const w = e.target.closest('.is-invalid');
      if (w) w.classList.remove('is-invalid');
      if (!$('.is-invalid', reg)) err.hidden = true;
    });
    reg.addEventListener('change', e => {
      const w = e.target.closest('.is-invalid');
      if (w) w.classList.remove('is-invalid');
      if (!$('.is-invalid', reg)) err.hidden = true;
    });
    // Enter moves forward rather than submitting early
    reg.addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT' && current < steps.length - 1) { e.preventDefault(); next.click(); }
    });

    // CV drop zone
    const drop = $('[data-drop]', reg);
    const file = $('#c-cv');
    const zone = $('.drop__zone', drop), chosen = $('.drop__file', drop), name = $('.drop__name', drop);
    zone.addEventListener('click', () => file.click());
    const MAX = 8 * 1024 * 1024;
    const showFile = () => {
      const f = file.files[0];
      if (f && f.size > MAX) { file.value = ''; err.textContent = 'That file is over 8MB. Try a smaller PDF or Word document.'; err.hidden = false; return showFile(); }
      if (f && !/\.(pdf|docx?)$/i.test(f.name)) { file.value = ''; err.textContent = 'Upload your CV as a PDF or Word document.'; err.hidden = false; return showFile(); }
      chosen.hidden = !f; zone.hidden = !!f;
      if (f) { name.textContent = f.name; err.hidden = true; }
    };
    file.addEventListener('change', showFile);
    ['dragenter', 'dragover'].forEach(t => drop.addEventListener(t, e => { e.preventDefault(); drop.classList.add('is-over'); }));
    ['dragleave', 'drop'].forEach(t => drop.addEventListener(t, e => { e.preventDefault(); drop.classList.remove('is-over'); }));
    drop.addEventListener('drop', e => {
      if (!e.dataTransfer.files.length) return;
      const dt = new DataTransfer(); dt.items.add(e.dataTransfer.files[0]);
      file.files = dt.files; showFile();
    });
    $('.drop__remove', drop).addEventListener('click', () => { file.value = ''; showFile(); file.focus(); });

    reg.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validateStep(current)) return;
      submit.disabled = true; submit.textContent = 'Sending…';
      const ok = await submitForm(reg, true);
      submit.disabled = false; submit.textContent = 'Submit registration';
      if (!ok) { err.textContent = "Your registration didn't send. Try again, or email your CV to nick@nexusrg.co.uk."; err.hidden = false; return; }
      reg.hidden = true;
      $$('.reg-progress li').forEach(c => { c.classList.remove('is-active'); c.classList.add('is-done'); });
      const sent = $('.sent', card);
      sent.hidden = false; sent.focus();
    });

    show(0);
  }
})();
