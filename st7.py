from st_lib import *

COLORS = ["#2f5fd0", "#e2583e", "#24936a", "#7a5bd1", "#d9921f", "#1b93a8"]

PROFILES = [
    ("home", "Habitant", "Vos démarches et votre cadre de vie au quotidien.",
     ["Formalités administratives", "Guide des démarches", "Habitat et urbanisme", "Salles municipales",
      "Cadre de vie", "Transports", "Participation citoyenne", "Numéros utiles"]),
    ("family_restroom", "Parent", "École, cantine, loisirs : tout pour vos enfants.",
     ["Portail Famille", "Enfance et jeunesse", "Menus cantine", "Santé : prévention et informations",
      "Associations", "Médiathèque"]),
    ("elderly", "Senior", "Accompagnement, santé et services de proximité.",
     ["Seniors", "Actions sociales", "Professionnels de santé", "Agence postale", "Transports",
      "Paroisse et lieux de culte"]),
    ("hiking", "Visiteur", "Balades, patrimoine et sorties dans les Monts de Flandre.",
     ["Tourisme", "Sentiers de randonnée", "Agenda", "Galeries de photos", "Equipements", "Marché"]),
    ("storefront", "Professionnel", "Commerces, artisans, entreprises et exploitations.",
     ["Commerçants", "Artisans", "Entreprises", "Exploitations agricoles", "Habitat et urbanisme", "Espace presse"]),
]

# Paysage illustré des Monts de Flandre.
LANDSCAPE = """<svg class="land" viewBox="0 0 1440 520" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6f5"/><stop offset="1" stop-color="#fbf3e4"/></linearGradient></defs>
<rect width="1440" height="520" fill="url(#sky)"/>
<circle class="sun" cx="1130" cy="120" r="58" fill="#ffd36b"/>
<g class="clouds" fill="#fff">
 <g class="cl c1"><ellipse cx="220" cy="110" rx="70" ry="22"/><ellipse cx="260" cy="96" rx="44" ry="26"/><ellipse cx="190" cy="100" rx="34" ry="20"/></g>
 <g class="cl c2"><ellipse cx="820" cy="70" rx="60" ry="18"/><ellipse cx="850" cy="58" rx="36" ry="22"/></g>
 <g class="cl c3"><ellipse cx="1300" cy="200" rx="54" ry="16"/><ellipse cx="1320" cy="190" rx="30" ry="18"/></g>
</g>
<path d="M0 330 C180 250 330 240 480 300 C620 355 720 250 900 230 C1080 210 1240 290 1440 260 L1440 520 L0 520Z" fill="#a9cf9a"/>
<g class="antenna" transform="translate(820 255)">
 <title>Antenne du Mont des Cats</title>
 <g fill="none" stroke="#5b6b7d" stroke-width=".8" opacity=".35">
  <path d="M0 -153 L-91 19 M0 -153 L94 -9 M0 -111 L-72 13 M0 -111 L75 -6 M0 -64 L-48 8 M0 -64 L51 -3"/>
 </g>
 <rect x="-3.5" y="-171" width="7" height="171" rx="1.5" fill="#f4ead6" stroke="#847566" stroke-width=".7"/>
 <path d="M-3.5 -154 H3.5 V-134 H-3.5Z M-3.5 -113 H3.5 V-93 H-3.5Z M-3.5 -73 H3.5 V-53 H-3.5Z M-3.5 -33 H3.5 V-13 H-3.5Z" fill="#b5523b"/>
 <rect x="-2" y="-192" width="4" height="21" rx=".8" fill="#b5523b"/>
 <path d="M0 -192 V-197" stroke="#5b4636" stroke-width="1.2"/>
 <g fill="#bba994" stroke="#847566" stroke-width=".6">
  <path d="M-7 -156 H7 V-153 L3.5 -150 H-3.5 L-7 -153Z"/>
  <path d="M-7 -116 H7 V-113 L3.5 -110 H-3.5 L-7 -113Z"/>
  <path d="M-8 -76 H8 V-73 L3.5 -70 H-3.5 L-8 -73Z"/>
  <path d="M-8 -36 H8 V-33 L3.5 -30 H-3.5 L-8 -33Z"/>
 </g>
 <g fill="none" stroke="#847566" stroke-width=".65">
  <path d="M-7 -156 V-160 H7 V-156 M-7 -116 V-120 H7 V-116 M-8 -76 V-80 H8 V-76 M-8 -36 V-40 H8 V-36"/>
 </g>
 <g fill="#e6ddcb" stroke="#847566" stroke-width=".6">
  <ellipse cx="5" cy="-42" rx="3.5" ry="4"/>
  <ellipse cx="-4" cy="-23" rx="2.8" ry="3.2"/>
 </g>
 <rect x="-5" y="-2" width="10" height="3" rx="1" fill="#847566"/>
 <g class="beacon"><circle cy="-197" r="5" fill="#e2583e" opacity=".2"/><circle cy="-197" r="1.8" fill="#e2583e"/></g>
 <g class="beacon beacon-low"><circle cx="-7" cy="-116" r="4" fill="#e2583e" opacity=".2"/><circle cx="-7" cy="-116" r="1.5" fill="#e2583e"/><circle cx="7" cy="-76" r="4" fill="#e2583e" opacity=".2"/><circle cx="7" cy="-76" r="1.5" fill="#e2583e"/></g>
</g>
<g class="hop-field" transform="translate(240 265) scale(.65)">
 <title>Petite houblonnière au loin</title>
 <defs><g id="hop-vine">
  <path d="M0 30 C-3 23 3 18 0 10 C-2 5 2 3 0 0" fill="none" stroke="#5f8053" stroke-width="1"/>
  <g fill="#6e995c"><ellipse cx="-2" cy="5" rx="3" ry="1.7" transform="rotate(30 -2 5)"/><ellipse cx="2" cy="10" rx="3" ry="1.7" transform="rotate(-30 2 10)"/><ellipse cx="-2" cy="16" rx="3" ry="1.7" transform="rotate(30 -2 16)"/><ellipse cx="2" cy="22" rx="3" ry="1.7" transform="rotate(-30 2 22)"/></g>
 </g></defs>
 <path d="M-18 35 L59 20 L72 28 L-9 43Z" fill="#a1b57a"/>
 <g fill="none" stroke="#947955" stroke-linecap="round">
  <path d="M-14 35 V3 M4 32 V0 M22 29 V-3 M40 25 V-6 M58 22 V-9" stroke-width="1.4"/>
  <path d="M-14 3 L58 -9 M-7 10 L65 -2 M-14 3 L-7 10 M58 -9 L65 -2" stroke-width=".8"/>
 </g>
 <use href="#hop-vine" x="-10" y="3"/><use href="#hop-vine" x="0" y="1"/><use href="#hop-vine" x="10" y="-1"/><use href="#hop-vine" x="20" y="-3"/><use href="#hop-vine" x="30" y="-5"/><use href="#hop-vine" x="40" y="-7"/><use href="#hop-vine" x="50" y="-9"/>
 <g opacity=".7"><use href="#hop-vine" x="-3" y="10"/><use href="#hop-vine" x="7" y="8"/><use href="#hop-vine" x="17" y="6"/><use href="#hop-vine" x="27" y="4"/><use href="#hop-vine" x="37" y="2"/><use href="#hop-vine" x="47" y="0"/><use href="#hop-vine" x="57" y="-2"/></g>
</g>
<path d="M0 380 C220 320 420 350 600 390 C780 430 960 330 1160 340 C1300 348 1380 380 1440 370 L1440 520 L0 520Z" fill="#7fb37a"/>
<g class="mill" transform="translate(1010 222)">
 <path d="M-14 0 L14 0 L20 70 L-20 70Z" fill="#f4ead6" stroke="#5b4636" stroke-width="2"/>
 <path d="M-16 0 L0 -18 L16 0Z" fill="#b5523b"/>
 <g class="blades" stroke="#5b4636" stroke-width="3"><line x1="0" y1="-8" x2="0" y2="-62"/><line x1="0" y1="-8" x2="0" y2="46"/><line x1="0" y1="-8" x2="-54" y2="-8"/><line x1="0" y1="-8" x2="54" y2="-8"/></g>
</g>
<g transform="translate(1290 238)"><rect x="-12" y="0" width="24" height="70" fill="#e9dcc4" stroke="#5b4636" stroke-width="2"/><path d="M-12 0 L0 -46 L12 0Z" fill="#5b6b7d"/><rect x="-26" y="34" width="52" height="36" fill="#e9dcc4" stroke="#5b4636" stroke-width="2"/><path d="M-30 34 L0 14 L30 34Z" fill="#b5523b"/></g>
<g fill="#4f8f52"><circle cx="880" cy="262" r="20"/><circle cx="906" cy="270" r="14"/><circle cx="1380" cy="300" r="18"/><circle cx="1210" cy="330" r="24"/><circle cx="1240" cy="340" r="15"/></g>
<path d="M0 440 C260 400 520 420 760 450 C1000 480 1220 420 1440 430 L1440 520 L0 520Z" fill="#5f9a5f"/>
<path d="M0 492 C300 470 600 480 900 500 C1100 512 1300 490 1440 488 L1440 520 L0 520Z" fill="#fbf8f3"/>
</svg>"""


def render(d):
    links = {}
    for it in d["nav"]:
        for c in it["cols"]:
            for t, h in c["links"]:
                links.setdefault(t, h)

    def panel(it):
        return (f'<div class="dd-card"><div class="dd-head">{ms(it["icon"])}<div><p class="dd-h">{E(it["label"])}</p>'
                f'<p>{E(it["desc"])}</p>{a(it["href"], "Explorer la rubrique " + ms("arrow_forward"), "dd-more")}</div></div>'
                f'<div class="dd-cols">{mega_cols(it)}</div></div>')

    btn = lambda it: f'<span class="dot"></span>{E(it["label"])}{ms("expand_more", "ms chev")}'
    header = f"""
<header class="hdr"><div class="wrap hdr-in">
  <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><b>Méteren</b><small>Ma commune</small></span></a>
  <nav class="mainnav" aria-label="Menu principal"><ul class="nav">{nav_items(d, panel, btn)}</ul></nav>
  <button type="button" class="sbtn" data-search aria-label="Rechercher">{ms("search")}</button>
  <button class="burger" type="button" data-burger aria-label="Menu">{ms("menu")}</button>
</div></header>"""

    chips = "".join(f'<li>{a(x["href"], ms(x["icon"]) + E(x["label"]))}</li>' for x in d["quick"])
    hero = f"""
<section class="hero">{LANDSCAPE}
  <div class="wrap hero-in">
    <p class="hello"><span class="wave">👋</span> Bonjour et bienvenue à</p>
    <h1>Méteren<span>.</span></h1>
    <p class="lead">{E(LEAD)}</p>
    <form class="big-search" data-search-form role="search"><label class="sr-only" for="q7">Rechercher</label>
      {ms("search")}<input id="q7" type="search" placeholder="Je cherche… une démarche, la cantine, une salle…"><button type="submit">Chercher</button></form>
    <div class="most"><p>Les plus demandés</p><ul>{chips}</ul></div>
  </div>
  <aside class="mairie-badge"><p class="status" data-open-status></p><a href="tel:0328490408">{ms("call")} {E(TEL)}</a></aside>
</section>"""

    tick = "".join(f'<li>{a(b["href"], f"<b>{E(b["date"])}</b>{E(b["title"])}")}</li>' for b in d["briefs"])
    ticker = f'<section class="ticker" aria-label="En bref"><p class="tk-l">{ms("bolt")} En bref</p><div class="tk-v"><ul>{tick}</ul><ul aria-hidden="true">{tick}</ul></div></section>'

    tabs, panes = [], []
    for i, (ic, name, txt, items) in enumerate(PROFILES):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button role="tab" id="pt{i}" aria-controls="pp{i}" aria-selected="{sel}" data-tab>{ms(ic)}<span>{E(name)}</span></button>')
        li = "".join(f'<li>{a(links[t], E(t) + ms("arrow_forward"))}</li>' for t in items if t in links)
        panes.append(f'<div role="tabpanel" id="pp{i}" aria-labelledby="pt{i}" class="pane"{"" if i == 0 else " hidden"}>'
                     f'<p class="pane-t">{ms(ic)} {E(txt)}</p><ul>{li}</ul></div>')
    profiles = f"""
<section class="sec prof reveal"><div class="wrap">
  <h2 class="ttl">Vous êtes<span>…</span></h2>
  <div class="prof-box"><div class="tabs" role="tablist" aria-label="Profils">{''.join(tabs)}</div>{''.join(panes)}</div>
</div></section>"""

    news = "".join(
        f'<li class="nc">{a(n["href"], f"<span class=ni><img src=\"{E(n["img"])}\" alt=\"\" loading=lazy></span><span class=nt><em>{E(n["date"])}</em><h3>{E(n["title"])}</h3><p>{E(n["desc"])}</p><b>Lire {ms("arrow_forward")}</b></span>")}</li>'
        for n in d["news"])
    events = "".join(
        f'<li class="tkt">{a(e["href"], f"<span class=td><b>{E(e["day"])}</b>{E(e["month"])}</span><span class=tb><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p></span>")}</li>'
        for e in d["events"])
    live = f"""
<section class="sec live"><div class="wrap">
  <div class="sec-h reveal"><h2 class="ttl">Ça bouge<span>!</span></h2>
    <div class="car-nav"><button type="button" data-car="-1" aria-label="Précédent">{ms("arrow_back")}</button><button type="button" data-car="1" aria-label="Suivant">{ms("arrow_forward")}</button>{a(U_NEWS, "Toutes les actualités", "lnk")}</div></div>
  <ul class="car reveal" data-carousel>{news}</ul>
  <div class="agenda reveal"><h3 class="sub">{ms("confirmation_number")} À l'agenda</h3><ul class="tkts">{events}</ul>{a(U_AGENDA, "Tout l'agenda " + ms("arrow_forward"), "lnk")}</div>
</div></section>"""

    tiles = "".join(
        f'<li style="--c:{COLORS[i]}">{a(it["href"], f"<span class=ti>{ms(it["icon"])}</span><h3>{E(it["label"])}</h3><p>{E(it["desc"])}</p>{ms("arrow_outward", "ms go")}")}</li>'
        for i, it in enumerate(d["nav"]))
    explore = f'<section class="sec expl reveal"><div class="wrap"><h2 class="ttl">Explorer la commune</h2><ul class="tiles">{tiles}</ul></div></section>'

    j = d["journal"]
    journal = f"""
<section class="sec jr reveal"><div class="wrap jr-in">
  <div class="mag">{a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">')}</div>
  <div><p class="kick">Journal municipal</p><h2>« Contact », le journal de Méteren</h2><p>{E(j["text"])}</p>
    <p class="btns">{a(j["pdf"], ms("download") + " Lire le n° actuel", "btn")}{a(U_JOURNAL, "Tous les numéros", "btn ghost")}</p></div>
</div></section>"""

    cards = "".join(
        f'<li style="--r:{r}deg">{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>")}</li>'
        for c, r in zip(d["discover"], (-3, 2, -1.5, 3)))
    discover = f'<section class="sec pc reveal"><div class="wrap"><h2 class="ttl">Cartes postales de Méteren</h2><ul class="cards">{cards}</ul></div></section>'

    f = footer_links(d)
    visit = f"""
<section class="sec vis reveal"><div class="wrap vis-in">
  <div class="vis-card"><p class="kick">{ms("location_on")} Passer nous voir</p><h2>Mairie de Méteren</h2>
    <p class="status big" data-open-status></p>
    <p>{E(ADDR)}<br><a href="tel:0328490408">{E(TEL)}</a> · <a href="mailto:{MAIL}">{E(MAIL)}</a></p>
    <div class="hrs"><div><h3>Mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
      <div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div></div>
    {a(U_CONTACT, "Nous écrire " + ms("arrow_forward"), "btn")}</div>
  <div class="vis-map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></div>
</div></section>"""

    footer = f"""
<footer class="ftr"><svg class="ftr-wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50 C240 0 480 0 720 40 C960 80 1200 70 1440 30 L1440 80 L0 80Z"/></svg>
<div class="ftr-bg"><div class="wrap">
  <div class="ftr-top">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><b>Méteren</b><small>{E(LEAD)}</small></span></a>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3>{a(d["facebook"], ms("thumb_up") + " Facebook", "btn")}</div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></div></footer>"""

    body = header + hero + ticker + f'<main id="main">{profiles}{live}{explore}{journal}{discover}{visit}</main>' + footer
    return page(7, "Bricolage+Grotesque:opsz,wght@12..96,500..800&family=DM+Sans:wght@400;500;700", body, js="style-7.js")
