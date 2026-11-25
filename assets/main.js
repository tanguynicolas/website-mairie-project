(function(){
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const desktop=()=>window.matchMedia('(min-width:961px)').matches;
  // mega menu
  $$('.nav-item').forEach(item=>{
    const btn=$('.nav-btn',item);
    const set=o=>{item.classList.toggle('open',o);btn.setAttribute('aria-expanded',o)};
    btn.addEventListener('click',()=>{const o=!item.classList.contains('open');$$('.nav-item.open').forEach(i=>i!==item&&i.classList.remove('open'));set(o)});
    let t;
    item.addEventListener('mouseenter',()=>{if(!desktop())return;clearTimeout(t);$$('.nav-item.open').forEach(i=>i!==item&&i.classList.remove('open'));set(true)});
    item.addEventListener('mouseleave',()=>{if(!desktop())return;t=setTimeout(()=>set(false),120)});
  });
  document.addEventListener('click',e=>{if(desktop()&&!e.target.closest('.nav-item'))$$('.nav-item.open').forEach(i=>i.classList.remove('open'))});
  const burger=$('.burger');
  burger&&burger.addEventListener('click',()=>{const o=document.body.classList.toggle('nav-open');burger.setAttribute('aria-expanded',o);$('.ms',burger).textContent=o?'close':'menu'});

  // search
  const ov=$('.search-overlay'), input=$('.search-overlay input'), res=$('.search-results');
  const norm=s=>(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const idx=(window.SEARCH_INDEX||[]).map(d=>({...d,nt:norm(d.t),nx:norm(d.x)}));
  const open=()=>{ov.hidden=false;input.focus();render()}, close=()=>{ov.hidden=true};
  $$('[data-open-search]').forEach(b=>b.addEventListener('click',open));
  $('[data-close-search]').addEventListener('click',close);
  ov.addEventListener('click',e=>{if(e.target===ov)close()});
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){close();$('.lightbox').hidden=true}
    if((e.key==='k'&&(e.metaKey||e.ctrlKey))||(e.key==='/'&&!/input|textarea/i.test(document.activeElement.tagName))){e.preventDefault();open()}
  });
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function render(){
    const q=norm(input.value.trim());
    if(q.length<2){res.innerHTML='<li class="empty">Saisissez au moins 2 caractères. Astuce : « cantine », « salle », « permis »…</li>';return}
    const terms=q.split(/\s+/);
    const hits=idx.map(d=>{let s=0;for(const t of terms){if(d.nt.includes(t))s+=10;else if(d.nx.includes(t))s+=1;else return null}return{d,s}}).filter(Boolean).sort((a,b)=>b.s-a.s).slice(0,12);
    if(!hits.length){res.innerHTML='<li class="empty">Aucun résultat.</li>';return}
    res.innerHTML=hits.map(({d})=>{
      let snip='';const i=d.nx.indexOf(terms[0]);
      if(i>=0){snip=d.x.substr(Math.max(0,i-50),140);snip=(i>50?'…':'')+esc(snip)+'…'}
      return `<li><a href="${d.u}"><strong>${esc(d.t)}</strong><small>${esc(d.s)}${snip?' · '+snip:''}</small></a></li>`}).join('');
  }
  input.addEventListener('input',render);

  // directory filter
  const list=$('[data-filter-list]');
  if(list){
    let cat='';const fi=$('[data-filter-input]');
    const apply=()=>{const q=norm(fi.value);$$('.card',list).forEach(c=>{c.style.display=(!cat||c.dataset.cat===cat)&&norm(c.dataset.name).includes(q)?'':'none'})};
    fi.addEventListener('input',apply);
    $$('.chip[data-cat]').forEach(ch=>ch.addEventListener('click',()=>{cat=ch.dataset.cat;$$('.chip[data-cat]').forEach(c=>c.classList.toggle('is-on',c===ch));apply()}));
  }
  // lightbox
  const lb=$('.lightbox');
  $$('a[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();$('img',lb).src=a.href;lb.hidden=false}));
  lb.addEventListener('click',()=>lb.hidden=true);
  // contact form (prototype: mailto)
  $$('form[data-mailto]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);
    location.href=`mailto:${f.dataset.mailto}?subject=${encodeURIComponent(d.get('objet'))}&body=${encodeURIComponent(d.get('message')+'\n\n'+d.get('nom')+' – '+d.get('email'))}`}));
})();
