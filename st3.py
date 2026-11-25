from st_lib import *


def render(d):
    def panel(it):
        cols = mega_cols(it)
        return (f'<div class="dd-in">{cols}<p class="dd-foot">{a(it["href"], "Toute la rubrique « " + E(it["label"]) + " » " + ms("arrow_forward"))}</p></div>')

    q = d["quick"]
    header = f"""
<header class="hdr">
  <div class="hdr-line"><div class="wrap"><span data-today></span><span class="hl-r">{a(U_CONTACT, ms("mail") + " Contact")}{a("tel:0328490408", ms("call") + " " + E(TEL))}</span></div></div>
  <div class="wrap hdr-main">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span class="b-name">Méteren</span><span class="b-sub">Village des Monts de Flandre</span></a>
    <button class="burger" type="button" data-burger aria-label="Menu">{ms("menu")}</button>
  </div>
  <nav class="mainnav" aria-label="Menu principal"><div class="wrap"><ul class="nav">
    {nav_items(d, panel)}
    <li class="nav-search"><button type="button" data-search aria-label="Rechercher">{ms("search")}</button></li>
  </ul></div></nav>
</header>"""

    quick = "".join(f'<li>{a(x["href"], "<span class=qi>" + ms(x["icon"]) + "</span><span>" + E(x["label"]) + "</span>", "q")}</li>' for x in q)
    news = "".join(
        f'<li>{a(c["href"], f"<span class=nimg><img src=\"{E(c["img"])}\" alt=\"\" loading=lazy></span><span class=nb><span class=nd>{E(c["date"])}</span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>", "nc")}</li>'
        for c in d["news"])
    briefs = "".join(f'<li>{a(b["href"], f"<span>{E(b["date"])}</span>{E(b["title"])}")}</li>' for b in d["briefs"])
    events = "".join(
        f'<li>{a(e["href"], f"<span class=ed><b>{E(e["day"])}</b>{E(e["month"])}</span><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p><span class=go>En savoir plus {ms("arrow_forward")}</span>", "ev")}</li>'
        for e in d["events"])
    disc = "".join(
        f'<li class="m{i}">{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>")}</li>'
        for i, c in enumerate(d["discover"]))
    j = d["journal"]
    f = footer_links(d)
    orn = '<span class="orn" aria-hidden="true"></span>'

    main = f"""
<main id="main">
  <section class="hero" style="--img:url('{E(AERIAL)}')"><div class="wrap">
    <div class="hero-card">
      <p class="kicker">Bienvenue à</p><h1>Méteren</h1><p class="lead">{E(LEAD)}</p>
      <form class="hsearch" data-search-form role="search"><label class="sr-only" for="q2">Rechercher</label>
        {ms("search")}<input id="q2" type="search" placeholder="Une démarche, un service, une association…"><button type="submit">Rechercher</button></form>
      <p class="status" data-open-status></p>
    </div>
  </div></section>

  <section class="quick"><div class="wrap"><h2 class="sr-only">Accès rapides</h2><ul class="qs">{quick}</ul></div></section>

  <section class="sec"><div class="wrap">
    <div class="sh">{orn}<h2>Actualités</h2>{a(U_NEWS, "Toutes les actualités", "more")}</div>
    <ul class="news">{news}</ul>
    <div class="briefs"><h3>En bref</h3><ul>{briefs}</ul></div>
  </div></section>

  <section class="sec green"><div class="wrap">
    <div class="sh">{orn}<h2>Rendez-vous</h2>{a(U_AGENDA, "Tout l'agenda", "more")}</div>
    <ul class="evs">{events}</ul>
  </div></section>

  <section class="sec"><div class="wrap journal">
    {a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">', "jc")}
    <div><p class="kicker">Journal municipal</p><h2>« Contact », le journal de Méteren</h2><p>{E(j["text"])}</p>
      <div class="btns">{a(j["pdf"], ms("download") + " Lire le dernier numéro", "btn")}{a(U_JOURNAL, "Tous les numéros", "btn btn-o")}</div></div>
  </div></section>

  <section class="sec cream"><div class="wrap">
    <div class="sh">{orn}<h2>Découvrir Méteren</h2></div>
    <ul class="mosaic">{disc}</ul>
  </div></section>

  <section class="sec"><div class="wrap info">
    <div class="ic">
      <div class="sh">{orn}<h2>Mairie de Méteren</h2></div>
      <p>{ms("location_on")} {E(ADDR)}</p>
      <p>{ms("call")} <a href="tel:0328490408">{E(TEL)}</a></p>
      <p>{ms("mail")} <a href="mailto:{MAIL}">{E(MAIL)}</a></p>
      <div class="hrs"><div><h3>Horaires de la mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
        <div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div></div>
      {a(U_CONTACT, "Nous contacter", "btn")}
    </div>
    <div class="map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></div>
  </div></section>
</main>

<footer class="ftr"><div class="wrap">
  <div class="ftr-top">
    <div class="fb"><img src="{E(d["logo"])}" alt=""><p class="b-name">Méteren</p><p>{E(ADDR)}<br>{E(TEL)}</p></div>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3>{a(d["facebook"], ms("thumb_up") + " Facebook", "btn btn-l")}</div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></footer>"""
    return page(3, "Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Mulish:wght@400;600;700", header + main)
