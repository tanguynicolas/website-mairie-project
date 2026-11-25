(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Assiette : onglets des rubriques
  const tabs = $$('[data-dial]');
  const turn = $('.plate-turn');
  const n = tabs.length;
  const select = (i, focus) => {
    tabs.forEach((t, k) => {
      const on = k === i;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      const p = document.getElementById(t.getAttribute('aria-controls'));
      if (p) p.hidden = !on;
    });
    if (turn) turn.style.setProperty('--rot', `${-i * 360 / n}deg`);
    if (focus) tabs[i].focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(i));
    t.addEventListener('keydown', e => {
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (k) { e.preventDefault(); select((i + k + n) % n, true); }
      else if (e.key === 'Home') { e.preventDefault(); select(0, true); }
      else if (e.key === 'End') { e.preventDefault(); select(n - 1, true); }
    });
  });

  // Actualités : accordéon
  const accs = $$('.acc');
  accs.forEach(li => {
    $('.acc-tab', li).addEventListener('click', () => {
      accs.forEach(o => {
        const on = o === li;
        o.classList.toggle('is-on', on);
        $('.acc-tab', o).setAttribute('aria-expanded', on);
      });
      const link = $('.acc-body a', li);
      if (link) setTimeout(() => link.focus({ preventScroll: true }), 50);
    });
  });

  // Agenda : mois et jours
  const list = $('.cal-list');
  const clearSel = () => {
    $$('.has-ev[aria-pressed]').forEach(b => b.removeAttribute('aria-pressed'));
    $$('.cal-list li').forEach(li => li.classList.remove('is-hl'));
    list && list.classList.remove('has-sel');
  };
  $$('[data-cal-go]').forEach(b => b.addEventListener('click', () => {
    const k = b.dataset.calGo;
    const back = Number(k) < Number(b.closest('[data-cal]').dataset.cal);
    $$('[data-cal]').forEach(m => { m.hidden = m.dataset.cal !== k; });
    clearSel();
    const navs = $$(`[data-cal="${k}"] button.cal-nav`);
    (navs.find(x => (Number(x.dataset.calGo) < Number(k)) === back) || navs[0])?.focus();
  }));
  $$('.has-ev[data-day]').forEach(b => b.addEventListener('click', () => {
    const was = b.getAttribute('aria-pressed') === 'true';
    clearSel();
    if (was) return;
    b.setAttribute('aria-pressed', 'true');
    list && list.classList.add('has-sel');
    b.dataset.day.split(' ').forEach(id => document.getElementById(id)?.classList.add('is-hl'));
  }));

  // Sommaire en tiroir
  const drawer = $('#drawer');
  const opener = $('[data-drawer]');
  if (drawer && opener) {
    const close = () => {
      drawer.hidden = true;
      opener.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('drawer-open');
      opener.focus();
    };
    opener.addEventListener('click', () => {
      drawer.hidden = false;
      opener.setAttribute('aria-expanded', 'true');
      document.body.classList.add('drawer-open');
      $('[data-drawer-close]', drawer)?.focus();
    });
    $('[data-drawer-close]', drawer)?.addEventListener('click', close);
    drawer.addEventListener('click', e => { if (e.target === drawer) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !drawer.hidden) close(); });
  }
})();
