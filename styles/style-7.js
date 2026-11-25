(function () {
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // Onglets « Vous êtes… »
  const tabs = $$('[data-tab]');
  const select = t => tabs.forEach(b => {
    const on = b === t;
    b.setAttribute('aria-selected', String(on));
    b.tabIndex = on ? 0 : -1;
    document.getElementById(b.getAttribute('aria-controls')).hidden = !on;
  });
  tabs.forEach((b, i) => {
    b.tabIndex = i ? -1 : 0;
    b.addEventListener('click', () => select(b));
    b.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      const n = tabs[(i + d + tabs.length) % tabs.length];
      select(n); n.focus();
    });
  });

  // Carrousel des actualités
  const car = document.querySelector('[data-carousel]');
  $$('[data-car]').forEach(b => b.addEventListener('click', () => {
    const item = car.querySelector('li');
    car.scrollBy({ left: Number(b.dataset.car) * (item ? item.offsetWidth + 24 : 300), behavior: 'smooth' });
  }));

  // Apparition au défilement
  const els = $$('.reveal');
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(e => e.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  els.forEach(e => io.observe(e));
})();
