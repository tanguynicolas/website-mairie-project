(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // Menus déroulants
  const closeAll = (except) => $$('[data-dd-item].open').forEach(li => {
    if (li !== except) { li.classList.remove('open'); const b = $('[data-dd]', li); if (b) b.setAttribute('aria-expanded', 'false'); }
  });
  $$('[data-dd]').forEach(btn => {
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', e => {
      e.preventDefault();
      const li = btn.closest('[data-dd-item]');
      const open = !li.classList.contains('open');
      closeAll(li);
      li.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', e => { if (!e.target.closest('[data-dd-item]')) closeAll(); });

  // Burger / menu plein écran
  $$('[data-burger]').forEach(b => b.addEventListener('click', () => {
    const o = document.body.classList.toggle('nav-open');
    b.setAttribute('aria-expanded', String(o));
  }));
  $$('[data-overlay-open]').forEach(b => b.addEventListener('click', () => document.body.classList.add('overlay-open')));
  $$('[data-overlay-close]').forEach(b => b.addEventListener('click', () => document.body.classList.remove('overlay-open')));

  // Recherche
  const norm = s => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const sx = document.createElement('div');
  sx.className = 'sx';
  sx.innerHTML = '<div class="sx-box" role="dialog" aria-modal="true" aria-label="Rechercher">' +
    '<div class="sx-head"><span class="ms">search</span><input type="search" placeholder="Rechercher une page, une démarche, une association…" aria-label="Rechercher"><button type="button" class="sx-close" aria-label="Fermer">Échap</button></div>' +
    '<div class="sx-res"></div></div>';
  document.body.appendChild(sx);
  const inp = $('input', sx), res = $('.sx-res', sx);
  const render = q => {
    const idx = window.SEARCH_INDEX || [];
    const n = norm(q).trim();
    if (n.length < 2) { res.innerHTML = '<p class="sx-hint">Saisissez au moins 2 lettres.</p>'; return; }
    const words = n.split(/\s+/);
    const out = [];
    for (const it of idx) {
      const t = norm(it.t), x = norm((it.s || '') + ' ' + (it.x || ''));
      if (words.every(w => t.includes(w) || x.includes(w))) out.push([words.every(w => t.includes(w)) ? 0 : 1, it]);
    }
    out.sort((a, b) => a[0] - b[0]);
    res.innerHTML = out.length ? out.slice(0, 12).map(([, it]) =>
      `<a href="../site/${esc(it.u)}"><strong>${esc(it.t)}</strong><span>${esc(it.s || '')}</span></a>`).join('')
      : '<p class="sx-hint">Aucun résultat.</p>';
  };
  const openSx = (q = '') => { sx.classList.add('on'); inp.value = q; render(q); setTimeout(() => inp.focus(), 30); };
  const closeSx = () => sx.classList.remove('on');
  inp.addEventListener('input', () => render(inp.value));
  $('.sx-close', sx).addEventListener('click', closeSx);
  sx.addEventListener('click', e => { if (e.target === sx) closeSx(); });
  $$('[data-search]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openSx(); }));
  $$('form[data-search-form]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault(); const i = $('input', f); openSx(i ? i.value : '');
  }));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeSx(); closeAll(); document.body.classList.remove('overlay-open', 'nav-open'); }
    const typing = /INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName);
    if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || (e.key === '/' && !typing)) { e.preventDefault(); openSx(); }
  });

  // Statut d'ouverture de la mairie (hors vacances scolaires)
  const now = new Date(), d = now.getDay(), m = now.getHours() * 60 + now.getMinutes();
  const open = (d >= 1 && d <= 6 && m >= 510 && m < 720) || (d === 3 && m >= 840 && m < 1020);
  $$('[data-open-status]').forEach(el => {
    el.classList.toggle('is-open', open);
    el.innerHTML = '<i class="dot"></i>' + (open ? 'Mairie ouverte actuellement' : 'Mairie fermée actuellement');
  });
  $$('[data-today]').forEach(el => {
    const s = now.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    el.textContent = s.charAt(0).toUpperCase() + s.slice(1);
  });
})();
