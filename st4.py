from st_lib import *


def render(d):
    q = d["quick"]
    navlinks = "".join(f"<li>{a(it['href'], E(it['label']))}</li>" for it in d["nav"])
    overlay_cols = "".join(
        f'<div class="ov-col"><p class="ov-h">{a(it["href"], E(it["label"]))}</p><p class="ov-d">{E(it["desc"])}</p>{mega_cols(it)}</div>'
        for it in d["nav"])
    header = f"""
<header class="hdr">
  <div class="wrap strip">
    <p><span data-today></span><span class="sep">·</span><span data-open-status></span></p>
    <p class="strip-r">{a(U_CONTACT, "Contact")}<span class="sep">·</span><a href="tel:0328490408">{E(TEL)}</a><span class="sep">·</span>{a(d["facebook"], "Facebook")}</p>
  </div>
  <div class="wrap mast">
    <a href="#" class="mast-logo"><img src="{E(d["logo"])}" alt=""></a>
    <div class="mast-t"><p class="mast-k">Commune de</p><a href="#" class="mast-n">Méteren</a><p class="mast-s">{E(LEAD)}</p></div>
    <button type="button" class="mast-search" data-search>{ms("search")}<span>Rechercher</span></button>
  </div>
  <nav class="wrap mainnav" aria-label="Menu principal">
    <ul>{navlinks}</ul>
    <button type="button" class="all" data-overlay-open>{ms("menu")} Tout le site</button>
  </nav>
</header>
<div class="ov" role="dialog" aria-modal="true" aria-label="Plan du site">
  <div class="wrap ov-head"><span class="ov-t">Méteren — tout le site</span>
    <button type="button" data-search class="ov-s">{ms("search")} Rechercher</button>
    <button type="button" data-overlay-close class="ov-x">{ms("close")} Fermer</button></div>
  <div class="wrap ov-grid">{overlay_cols}</div>
</div>"""

    n0, rest = d["news"][0], d["news"][1:]
    lead = a(n0["href"], f'<img src="{E(n0["img"])}" alt=""><span class="cat">Actualité · {E(n0["date"])}</span><h3>{E(n0["title"])}</h3><p>{E(n0["desc"])}</p>', "lead-story")
    seconds = "".join(a(c["href"], f'<img src="{E(c["img"])}" alt="" loading="lazy"><span class="cat">{E(c["date"])}</span><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p>', "sec-story") for c in rest)
    briefs = "".join(f'<li>{a(b["href"], f"<span class=cat>{E(b["date"])}</span>{E(b["title"])}")}</li>' for b in d["briefs"])
    idx = "".join(f'<li>{a(x["href"], f"<span class=num>{i:02d}</span><span>{E(x["label"])}</span>{ms("arrow_forward")}")}</li>' for i, x in enumerate(q, 1))
    events = "".join(f'<li>{a(e["href"], f"<span class=big>{E(e["day"])}</span><span class=cat>{E(e["month"])}</span><h3>{E(e["title"])}</h3><p>{E(e["desc"])}</p>")}</li>' for e in d["events"])
    disc = "".join(f'<li>{a(c["href"], f"<img src=\"{E(c["img"])}\" alt=\"\" loading=lazy><h3>{E(c["title"])}</h3><p>{E(c["desc"])}</p>")}</li>' for c in d["discover"])
    j = d["journal"]
    f = footer_links(d)

    main = f"""
<main id="main" class="wrap">
  <section class="une">
    <h2 class="rub">À la une {a(U_NEWS, "Toutes les actualités →")}</h2>
    <div class="une-grid">{lead}<div class="seconds">{seconds}</div></div>
  </section>

  <section class="bref"><h2 class="rub">En bref</h2><ul>{briefs}</ul></section>

  <section class="prat">
    <figure><img src="{E(d["hero"])}" alt="L'étang de Méteren au coucher du soleil"><figcaption>Bienvenue à Méteren — {E(LEAD)}</figcaption></figure>
    <div><h2 class="rub">Accès rapides</h2><ol class="idx">{idx}</ol></div>
  </section>

  <section class="agenda"><h2 class="rub">Agenda {a(U_AGENDA, "Tout l'agenda →")}</h2><ul>{events}</ul></section>
</main>

<section class="jband"><div class="wrap jgrid">
  {a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}">', "jc")}
  <div><p class="cat">Journal municipal</p><h2>« Contact », le journal de Méteren</h2><p class="jt">{E(j["text"])}</p>
    <p class="jl">{a(j["pdf"], ms("download") + " Lire le dernier numéro", "btn")}{a(U_JOURNAL, "Tous les numéros →", "lnk")}</p></div>
</div></section>

<div class="wrap">
  <section class="disc"><h2 class="rub">Découvrir Méteren</h2><ul>{disc}</ul></section>
  <section class="infos"><h2 class="rub">Mairie de Méteren</h2>
    <div class="info-grid">
      <div><h3>Nous trouver</h3><p>{E(ADDR)}</p><p><a href="tel:0328490408">{E(TEL)}</a><br><a href="mailto:{MAIL}">{E(MAIL)}</a></p><p>{a(U_CONTACT, "Nous contacter →", "lnk")}</p></div>
      <div><h3>Horaires de la mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
      <div><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div>
    </div>
    <div class="map"><iframe title="Plan d'accès à la mairie" src="{MAP}" loading="lazy"></iframe></div>
  </section>
</div>

<footer class="ftr"><div class="wrap">
  <div class="ftr-top">
    <p class="ftr-n">Méteren</p>
    <div><h3>Liens utiles</h3><ul>{f["ext"]}</ul></div>
    <div><h3>Labels</h3><ul class="labels">{f["labels"]}</ul></div>
    <div><h3>Suivez-nous</h3><ul><li>{a(d["facebook"], "Facebook")}</li></ul></div>
  </div>
  <div class="ftr-bot"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</div></footer>"""
    return page(4, "Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&family=Inter:wght@400;500;600", header + main, "Outlined")
