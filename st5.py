from st_lib import *


def render(d):
    def panel(it):
        intro = (f'<div class="dd-intro"><span class="dd-ic">{ms(it["icon"])}</span><p class="dd-h">{E(it["label"])}</p>'
                 f'<p>{E(it["desc"])}</p>{a(it["href"], "Voir la rubrique " + ms("arrow_forward"), "dd-more")}</div>')
        return f'<div class="wrap"><div class="dd-box">{intro}<div class="dd-cols">{mega_cols(it)}</div></div></div>'

    q = d["quick"]
    header = f"""
<header class="hdr">
  <div class="wrap hdr-top">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><strong>Méteren</strong><small>Site officiel de la commune</small></span></a>
    <div class="hdr-act">
      <a class="hk" href="tel:0328490408">{ms("call")}<span>{E(TEL)}</span></a>
      {a(U_CONTACT, ms("mail") + "<span>Contact</span>", "hk")}
      <button type="button" class="sbtn" data-search>{ms("search")}<span>Rechercher</span><kbd>/</kbd></button>
      <button class="burger" type="button" data-burger aria-label="Menu">{ms("menu")}</button>
    </div>
  </div>
  <nav class="mainnav" aria-label="Menu principal"><div class="wrap"><ul class="nav">
    {nav_items(d, panel, lambda it: ms(it["icon"], "ms ni") + E(it["label"]) + ms("expand_more", "ms chev"))}
  </ul></div></nav>
</header>"""

    quick = "".join(f'<li>{a(x["href"], f"<span class=qi>{ms(x["icon"])}</span><span>{E(x["label"])}</span>", "q q" + str(i % 2))}</li>' for i, x in enumerate(q))
    news = "".join(f'<li>{a(c["href"], f"<span class=ci><img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><em>{E(c["date"])}</em></span><span class=cb><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>", "card")}</li>' for c in d["news"])
    briefs = "".join(f'<li>{a(b["href"], f"<span>{E(b["date"])}</span>{E(b["title"])}")}</li>' for b in d["briefs"])
    events = "".join(f'<li>{a(e["href"], f"<span class=ed><b>{E(e["day"])}</b>{E(e["month"])}</span><span class=et><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p></span>{ms("chevron_right")}", "ev")}</li>' for e in d["events"])
    disc = "".join(f'<li>{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>", "dc")}</li>' for c in d["discover"])
    j = d["journal"]
    f = footer_links(d)

    main = f"""
<main id="main">
  <section class="wrap"><div class="hero" style="--img:url('{E(d["hero"])}')">
    <div class="hero-in">
      <p class="kicker">Bienvenue à</p><h1>Méteren</h1><p class="lead">{E(LEAD)}</p>
      <form class="hsearch" data-search-form role="search"><label class="sr-only" for="q4">Rechercher</label>
        {ms("search")}<input id="q4" type="search" placeholder="Que recherchez-vous ? Démarche, service, association…"><button type="submit">Rechercher</button></form>
      <p class="chip" data-open-status></p>
    </div>
  </div></section>

  <section class="wrap sec"><h2 class="h2">Accès rapides</h2><ul class="qs">{quick}</ul></section>

  <section class="wrap sec">
    <div class="sh"><h2 class="h2">Actualités</h2>{a(U_NEWS, "Toutes les actualités " + ms("arrow_forward"), "more")}</div>
    <div class="news-grid"><ul class="cards">{news}</ul><aside class="briefs"><h3>{ms("bolt")} En bref</h3><ul>{briefs}</ul></aside></div>
  </section>

  <section class="wrap sec"><div class="agenda">
    <div class="sh"><h2 class="h2">Agenda</h2>{a(U_AGENDA, "Tout l'agenda " + ms("arrow_forward"), "more")}</div>
    <ul class="evs">{events}</ul>
  </div></section>

  <section class="jband"><div class="wrap jgrid">
    {a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">', "jc")}
    <div><p class="kicker">Journal municipal</p><h2>« Contact », le journal de Méteren</h2><p>{E(j["text"])}</p>
      <div class="btns">{a(j["pdf"], ms("download") + " Lire le dernier numéro", "btn")}{a(U_JOURNAL, "Tous les numéros", "btn btn-w")}</div></div>
  </div></section>

  <section class="wrap sec"><h2 class="h2">Découvrir Méteren</h2><ul class="discs">{disc}</ul></section>

  <section class="wrap sec"><div class="info">
    <div class="ic">
      <h2 class="h2">{ms("account_balance")} Mairie de Méteren</h2>
      <p>{ms("location_on")} {E(ADDR)}</p><p>{ms("call")} <a href="tel:0328490408">{E(TEL)}</a></p><p>{ms("mail")} <a href="mailto:{MAIL}">{E(MAIL)}</a></p>
      <div class="hrs"><div><h3>Horaires de la mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
        <div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div></div>
      {a(U_CONTACT, "Nous contacter", "btn")}
    </div>
    <div class="map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></div>
  </div></section>
</main>

<footer class="ftr"><div class="wrap">
  <div class="ftr-top">
    <div><a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span><strong>Méteren</strong><small>{E(ADDR)}</small></span></a></div>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3>{a(d["facebook"], ms("thumb_up") + " Facebook", "btn btn-w")}</div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></footer>"""
    return page(5, "Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800", header + main)
