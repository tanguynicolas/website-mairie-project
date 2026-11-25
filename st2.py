from st_lib import *


def render(d):
    def panel(it):
        intro = (f'<div class="dd-intro">{ms(it["icon"])}<p class="dd-h">{E(it["label"])}</p>'
                 f'<p>{E(it["desc"])}</p>{a(it["href"], "Accéder à la rubrique " + ms("arrow_forward"), "dd-more")}</div>')
        return f'<div class="wrap dd-grid">{intro}{mega_cols(it)}</div>'

    q = d["quick"]
    top = "".join(a(x["href"], E(x["label"])) for x in [q[0], q[1], q[5]])
    header = f"""
<header class="hdr">
  <div class="topbar"><div class="wrap">
    <p class="top-l">{ms("location_on")} {E(ADDR)}</p>
    <nav class="top-r" aria-label="Liens rapides">{top}{a(U_CONTACT, "Contact")}{a(d["facebook"], ms("thumb_up") + " Facebook")}</nav>
  </div></div>
  <div class="wrap brandrow">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><small>Commune de</small><strong>Méteren</strong><em>Nord · Flandre intérieure</em></span></a>
    <form class="hsearch" data-search-form role="search"><label class="sr-only" for="q1">Rechercher</label>
      <input id="q1" type="search" placeholder="Rechercher sur le site"><button type="submit" aria-label="Rechercher">{ms("search")}</button></form>
    <button class="burger" type="button" data-burger aria-label="Menu">{ms("menu")}<span>Menu</span></button>
  </div>
  <nav class="mainnav" aria-label="Menu principal"><div class="wrap"><ul class="nav">
    <li class="nav-home">{a("#", ms("home"), extra=' aria-label="Accueil"')}</li>
    {nav_items(d, panel)}
  </ul></div></nav>
</header>"""

    quick = "".join(f'<li>{a(x["href"], ms(x["icon"]) + "<span>" + E(x["label"]) + "</span>" + ms("arrow_forward", "ms arr"), "tile")}</li>' for x in q)

    def card(c):
        return a(c["href"], f'<div class="cimg"><img src="{E(c["img"])}" alt="" loading="lazy"></div>'
                 f'<div class="cbody"><p class="meta">{E(c["date"])}</p><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p>'
                 f'<span class="more">Lire la suite {ms("arrow_forward")}</span></div>', "card")
    news = "".join(f"<li>{card(c)}</li>" for c in d["news"])
    briefs = "".join(f'<li>{a(b["href"], f"<span>{E(b["date"])}</span>{E(b["title"])}")}</li>' for b in d["briefs"])
    events = "".join(f'<li>{a(e["href"], f"<span class=edate><strong>{E(e["day"])}</strong>{E(e["month"])}</span><span><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p></span>", "event")}</li>' for e in d["events"])
    disc = "".join(f'<li>{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>", "disc")}</li>' for c in d["discover"])
    j = d["journal"]
    f = footer_links(d)

    main = f"""
<main id="main">
  <section class="hero"><div class="wrap hero-grid">
    <div class="hero-txt">
      <p class="kicker">Bienvenue à</p><h1>Méteren</h1><p class="lead">{E(LEAD)}</p>
      <p class="status" data-open-status></p>
      <p class="status-note">Lun.–sam. 8h30–12h · mer. 14h–17h (hors vacances scolaires)</p>
      <div class="btns">{a(U_CONTACT, "Contacter la mairie", "btn btn-p")}{a(q[4]["href"], "Faire une démarche", "btn btn-s")}</div>
    </div>
    <div class="hero-img"><img src="{E(d["hero"])}" alt="L'étang de Méteren"></div>
  </div></section>

  <section class="sec"><div class="wrap">
    <h2 class="h2">Accès rapides</h2>
    <ul class="tiles">{quick}</ul>
  </div></section>

  <section class="sec sec-grey"><div class="wrap">
    <div class="sec-head"><h2 class="h2">Actualités</h2>{a(U_NEWS, "Toutes les actualités " + ms("arrow_forward"), "link")}</div>
    <div class="news-grid"><ul class="cards">{news}</ul>
      <aside class="briefs"><h3>En bref</h3><ul>{briefs}</ul></aside></div>
  </div></section>

  <section class="sec"><div class="wrap two">
    <div><div class="sec-head"><h2 class="h2">Agenda</h2>{a(U_AGENDA, "Tout l'agenda " + ms("arrow_forward"), "link")}</div>
      <ul class="events">{events}</ul></div>
    <div class="journal">
      {a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">', "jcover")}
      <div><p class="kicker">Journal municipal</p><h2>« Contact », le journal de Méteren</h2><p>{E(j["text"])}</p>
      <div class="btns">{a(j["pdf"], ms("download") + " Lire le dernier numéro", "btn btn-p")}{a(U_JOURNAL, "Tous les numéros", "btn btn-s")}</div></div>
    </div>
  </div></section>

  <section class="sec sec-grey"><div class="wrap">
    <h2 class="h2">Découvrir Méteren</h2><ul class="discs">{disc}</ul>
  </div></section>

  <section class="sec"><div class="wrap"><div class="info">
    <div class="info-card">
      <h2 class="h2">Mairie de Méteren</h2>
      <p class="addr">{ms("location_on")} {E(ADDR)}</p>
      <p>{ms("call")} <a href="tel:0328490408">{E(TEL)}</a></p>
      <p>{ms("mail")} <a href="mailto:{MAIL}">{E(MAIL)}</a></p>
      <div class="hrs"><div><h3>Horaires de la mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
      <div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div></div>
      {a(U_CONTACT, "Nous contacter", "btn btn-p")}
    </div>
    <div class="map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></div>
  </div></div></section>
</main>

<footer class="ftr"><div class="wrap">
  <div class="ftr-top">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><small>Commune de</small><strong>Méteren</strong></span></a>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3>{a(d["facebook"], ms("thumb_up") + " Facebook", "btn btn-s")}</div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></footer>"""
    return page(2, "Source+Sans+3:wght@400;600;700", header + main, "Outlined")
