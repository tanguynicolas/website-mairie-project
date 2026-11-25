from st_lib import *


def render(d):
    def panel(it):
        head = (f'<div class="dd-head">{ms(it["icon"])}<div><p class="dd-h">{E(it["label"])}</p><p>{E(it["desc"])}</p></div>'
                f'{a(it["href"], "Voir tout " + ms("arrow_outward"), "dd-more")}</div>')
        return f'<div class="dd-card">{head}<div class="dd-cols">{mega_cols(it)}</div></div>'

    q = d["quick"]
    header = f"""
<header class="hdr"><div class="pill">
  <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span>Méteren</span></a>
  <nav class="mainnav" aria-label="Menu principal"><ul class="nav">{nav_items(d, panel)}</ul></nav>
  <button type="button" class="sbtn" data-search aria-label="Rechercher">{ms("search")}</button>
  <button class="burger" type="button" data-burger aria-label="Menu">{ms("menu")}</button>
</div></header>"""

    quick = "".join(f'<li class="t c3 qk">{a(x["href"], f"{ms(x["icon"])}<span>{E(x["label"])}</span>{ms("arrow_outward", "ms ar")}")}</li>' for x in q)
    n0, n1, n2 = d["news"]
    def nc(c, cls):
        return f'<li class="t {cls} nw">{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span class=nb><em>{E(c["date"])}</em><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>")}</li>'
    briefs = "".join(f'<li>{a(b["href"], f"<span>{E(b["date"])}</span>{E(b["title"])}")}</li>' for b in d["briefs"])
    events = "".join(f'<li>{a(e["href"], f"<span class=ed><b>{E(e["day"])}</b>{E(e["month"])}</span><span><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p></span>")}</li>' for e in d["events"])
    disc = "".join(f'<li class="t c3 dc">{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p></span>")}</li>' for c in d["discover"])
    j = d["journal"]
    f = footer_links(d)
    lbl = lambda t: f'<p class="lbl">{t}</p>'

    main = f"""
<main id="main" class="wrap">
  <ul class="bento">
    <li class="t c8 r2 hero" style="--img:url('{E(d["hero"])}')"><div><p class="kicker">Bienvenue à</p><h1>Méteren</h1><p>{E(LEAD)}</p></div></li>
    <li class="t c4 st">{lbl(ms("account_balance") + " Mairie")}<p class="status" data-open-status></p>
      <dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p>
      <p class="st-a"><a href="tel:0328490408">{ms("call")} {E(TEL)}</a>{a(U_CONTACT, ms("mail") + " Écrire")}</p></li>
    <li class="t c4 sr"><p class="sr-t">Que recherchez-vous ?</p>
      <form data-search-form role="search"><label class="sr-only" for="q5">Rechercher</label><input id="q5" type="search" placeholder="Démarche, service, association…"><button type="submit" aria-label="Rechercher">{ms("arrow_forward")}</button></form>
      <p class="sr-k"><kbd>/</kbd> ou <kbd>Ctrl K</kbd> depuis n'importe où</p></li>

    <li class="t c12 sh"><h2>Accès rapides</h2></li>
    {quick}

    <li class="t c12 sh"><h2>Actualités</h2>{a(U_NEWS, "Toutes les actualités " + ms("arrow_forward"))}</li>
    {nc(n0, "c6 big")}{nc(n1, "c3")}{nc(n2, "c3")}

    <li class="t c4 ag">{lbl(ms("event") + " Agenda")}<ul>{events}</ul>{a(U_AGENDA, "Tout l'agenda " + ms("arrow_forward"), "tl")}</li>
    <li class="t c4 br">{lbl(ms("bolt") + " En bref")}<ul>{briefs}</ul></li>
    <li class="t c4 jn">{lbl(ms("menu_book") + " Journal municipal")}
      <div class="jw">{a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">', "jc")}
      <div><h3>« Contact », le journal de Méteren</h3><p>{E(j["text"])}</p></div></div>
      <p class="jb">{a(j["pdf"], ms("download") + " Lire le n° actuel", "btn")}{a(U_JOURNAL, "Tous les numéros", "tl")}</p></li>

    <li class="t c12 sh"><h2>Découvrir Méteren</h2></li>
    {disc}

    <li class="t c5 inf">{lbl(ms("location_on") + " Nous trouver")}<h2>Mairie de Méteren</h2>
      <p>{E(ADDR)}</p><p><a href="tel:0328490408">{E(TEL)}</a> · <a href="mailto:{MAIL}">{E(MAIL)}</a></p>
      <div class="hrs"><div><h3>Mairie</h3><dl>{hours_dl(HOURS)}</dl></div><div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div></div>
      {a(U_CONTACT, "Nous contacter " + ms("arrow_forward"), "btn")}</li>
    <li class="t c7 map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></li>
  </ul>
</main>

<footer class="wrap ftr"><div class="ftr-in">
  <div class="ftr-top">
    <a class="brand" href="#"><img src="{E(d["logo"])}" alt=""><span>Méteren</span></a>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3>{a(d["facebook"], ms("thumb_up") + " Facebook", "btn btn-l")}</div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></footer>"""
    return page(6, "Manrope:wght@400;500;600;700;800", header + main)
