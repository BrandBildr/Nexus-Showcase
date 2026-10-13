/* Nexus Resourcing Group: concept homepage interactions */
(() => {
  // Swap this for Nick's real Cal.com booking link
  const CAL_URL = 'https://cal.com/nick-souness';

  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = !!(window.gsap && window.ScrollTrigger);
  const animate = !reduce && hasGsap;
  if (!animate) root.classList.remove('js-anim');

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const nav = $('#nav');
  const navH = () => nav.offsetHeight;

  $('#cal-link').href = CAL_URL;
  $('#yr').textContent = new Date().getFullYear();

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (animate && window.Lenis) {
    lenis = new Lenis({ duration: 1.15, easing: t => 1 - Math.pow(1 - t, 4), smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const scrollToEl = el => {
    if (lenis) lenis.scrollTo(el, { offset: el.id === 'top' ? 0 : -navH() + 1, duration: 1.4 });
    else el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  };

  $$('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      const target = id === '#top' ? $('#top') : $(id);
      if (!target) return;
      e.preventDefault();
      if (a.dataset.contactTab) setTab(a.dataset.contactTab, false);
      scrollToEl(target);
      history.replaceState(null, '', id === '#top' ? location.pathname : id);
    });
  });

  /* ---------- nav state ---------- */
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    const heroH = $('.hero').offsetHeight;
    nav.classList.toggle('is-solid', y > 40);
    nav.classList.toggle('is-hidden', y > heroH && y > lastY + 2);
    if (y < lastY - 2 || y <= heroH) nav.classList.remove('is-hidden');
    lastY = y;
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const sectionLinks = $$('.nav__links a');
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      sectionLinks.forEach(l => l.classList.toggle('is-current', l.getAttribute('href') === '#' + en.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  ['about', 'sectors', 'approach', 'nick', 'contact'].forEach(id => io.observe(document.getElementById(id)));

  /* ---------- hero: the letters converge ---------- */
  if (animate) try {
    gsap.registerPlugin(ScrollTrigger);
    const wms = $$('.wm');
    const spread = Math.min(window.innerWidth * 0.16, 220);
    const tl = gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.15 });
    tl.fromTo('.hero__img', { scale: 1.18 }, { scale: 1.04, duration: 3.2, ease: 'power2.out' }, 0)
      .fromTo(wms,
        { opacity: 0, x: i => (i - 2) * spread * 2.2, filter: 'blur(14px)' },
        { opacity: 1, x: 0, filter: 'blur(0px)', duration: 1.8, stagger: { each: 0.06, from: 'edges' } }, 0.25)
      .fromTo('.wm--x', { rotate: -90, scale: 1.4 }, { rotate: 0, scale: 1, duration: 1.6 }, 0.35)
      .fromTo('.hero__icon',
        { opacity: 0, scale: 0.55, rotate: -45, y: 20 },
        { opacity: 1, scale: 1, rotate: 0, y: 0, duration: 1.6 }, 0.9)
      .fromTo('.hero__shine', { backgroundPosition: '150% 0' }, { backgroundPosition: '-60% 0', duration: 1.6, ease: 'power2.inOut' }, 1.7)
      .to('.hero__group .rule', { scaleX: 1, duration: 1.2 }, 1.3)
      .fromTo('.hero__group-text', { opacity: 0, letterSpacing: '0.9em' }, { opacity: 1, letterSpacing: '0.42em', duration: 1.4 }, 1.3)
      .fromTo('.hero__tag', { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 1 }, 1.75)
      .fromTo('.hero__ctas > *', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 1, stagger: 0.1 }, 1.95)
      .to('.hero__scroll', { opacity: 1, duration: 1 }, 2.4);

    // Hero drifts away as you scroll
    gsap.to('.hero__media', { yPercent: 14, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero__content', { y: -90, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: '75% top', scrub: true } });

    // About headline: words rise into place, once
    const h = $('[data-split]');
    h.innerHTML = h.textContent.split(' ').map(w => `<span class="w" style="display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.08em;margin-bottom:-.08em"><span style="display:inline-block">${w}</span></span>`).join(' ');
    gsap.from($$('.w > span', h), {
      yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.04,
      scrollTrigger: { trigger: h, start: 'top 80%' }
    });

    // Approach: the line fills as you read down the steps
    const steps = $$('.step');
    gsap.to('.steps__fill', {
      scaleX: 1, ease: 'none',
      scrollTrigger: {
        trigger: '.steps-wrap', start: 'top 75%', end: 'bottom 55%', scrub: 0.6,
        onUpdate: self => steps.forEach((s, i) => s.classList.toggle('is-lit', self.progress >= i / steps.length + 0.02 || (i === 0 && self.progress > 0)))
      }
    });

    // Nick: count up to 20
    const c = $('.count');
    const obj = { v: 0 };
    gsap.to(obj, {
      v: +c.dataset.to, duration: 1.6, ease: 'power3.out',
      onUpdate: () => (c.textContent = Math.round(obj.v)),
      scrollTrigger: { trigger: c, start: 'top 85%' }
    });
    gsap.fromTo('.nick__frame img', { yPercent: -8 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.nick', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo('.nick__mark', { rotate: -20 }, { rotate: 15, ease: 'none', scrollTrigger: { trigger: '.nick', start: 'top bottom', end: 'bottom top', scrub: true } });
  } catch (e) {
    // Never leave the hero hidden if an animation fails
    console.error(e);
    root.classList.remove('js-anim');
  } else {
    $$('.step').forEach(s => s.classList.add('is-lit'));
  }

  /* ---------- sector panels ---------- */
  const panels = $$('.panel');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  let hoverTimer;
  const activate = p => {
    panels.forEach(x => {
      const on = x === p;
      x.classList.toggle('is-active', on);
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
    });
  };
  panels.forEach((p, i) => {
    p.tabIndex = i === 0 ? 0 : -1;
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

  /* ---------- contact: call or enquiry ---------- */
  const sw = $('.switch');
  const panes = $('.panes');
  function setTab(name, focus = true) {
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
    // smooth height change between panes
    const to = panes.offsetHeight;
    if (!reduce) {
      panes.style.height = from + 'px';
      requestAnimationFrame(() => {
        panes.style.height = to + 'px';
        setTimeout(() => (panes.style.height = ''), 650);
      });
    }
    if (focus) $('#tab-' + name).focus();
    if (lenis) setTimeout(() => ScrollTrigger.refresh(), 700);
  }
  sw.dataset.active = 'call';
  $$('.switch__btn').forEach(b => b.addEventListener('click', () => setTab(b.dataset.tab)));
  $$('[data-tab-jump]').forEach(b => b.addEventListener('click', () => setTab(b.dataset.tabJump)));

  /* ---------- enquiry form ---------- */
  const form = $('.form');
  const sent = $('.sent');
  const err = $('.form__error');
  const msgLabel = $('[data-msg-label]');
  const company = $('[data-client-only]');
  form.addEventListener('change', e => {
    if (e.target.name !== 'enquiry-type') return;
    const candidate = e.target.value === 'Candidate';
    company.hidden = candidate;
    msgLabel.textContent = candidate ? 'Tell us about your experience and the work you want' : 'Tell us about the project';
  });

  const validate = () => {
    let first = null;
    $$('[required]', form).forEach(f => {
      const ok = f.type === 'email' ? /^\S+@\S+\.\S+$/.test(f.value.trim()) : f.value.trim().length > 1;
      f.closest('.field').classList.toggle('is-invalid', !ok);
      if (!ok && !first) first = f;
    });
    return first;
  };
  form.addEventListener('input', e => {
    const fld = e.target.closest('.field.is-invalid');
    if (fld) fld.classList.remove('is-invalid');
    if (!form.querySelector('.is-invalid')) err.hidden = true;
  });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    err.hidden = true;
    const bad = validate();
    if (bad) {
      err.textContent = bad.type === 'email' ? 'Enter a valid email address so we can reply.' : 'Fill in the highlighted fields to send your enquiry.';
      err.hidden = false;
      bad.focus();
      return;
    }
    const btn = $('button[type="submit"]', form);
    btn.disabled = true; btn.textContent = 'Sending…';
    const body = new URLSearchParams(new FormData(form)).toString();
    let ok = false;
    try {
      const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
      ok = res.ok;
    } catch (_) { ok = false; }
    // Local previews have no form handler, so show the success state there
    if (!ok && /^(localhost|127\.|file)/.test(location.hostname || 'file')) ok = true;
    btn.disabled = false; btn.textContent = 'Send enquiry';
    if (!ok) {
      err.textContent = "Your enquiry didn't send. Try again, or email nick@nexusrg.co.uk directly.";
      err.hidden = false;
      return;
    }
    form.hidden = true; sent.hidden = false; sent.focus();
  });
  $('[data-reset-form]').addEventListener('click', () => {
    form.reset(); company.hidden = false; msgLabel.textContent = 'Tell us about the project';
    sent.hidden = true; form.hidden = false; $('#f-name').focus();
  });
})();
