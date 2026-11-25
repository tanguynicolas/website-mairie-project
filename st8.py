import calendar
import re

from st_lib import *

MONTHS = {"JANV": 1, "FÉVR": 2, "FEVR": 2, "MARS": 3, "AVR": 4, "MAI": 5, "JUIN": 6, "JUIL": 7,
          "AOÛT": 8, "AOUT": 8, "SEPT": 9, "OCT": 10, "NOV": 11, "DÉC": 12, "DEC": 12}
MONTH_NAMES = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
               "septembre", "octobre", "novembre", "décembre"]
ROMAN = ["I", "II", "III", "IV", "V", "VI"]

# Moulin de Flandre peint « en camaïeu bleu » au centre de l'assiette.
MILL = """<g class="plate-mill" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
 <path d="M-58 62 C-30 50 30 50 58 62" />
 <path d="M-70 70 C-35 60 35 60 70 70" stroke-width="1.2" opacity=".6"/>
 <path d="M-14 56 L-9 -6 L9 -6 L14 56 Z" class="pf"/>
 <path d="M-12 -6 L0 -20 L12 -6 Z" class="pf"/>
 <path d="M-4 56 V42 H4 V56" />
 <path d="M-11 30 H11 M-10 12 H10" stroke-width="1" opacity=".7"/>
 <path d="M-46 64 V40 M-52 40 Q-46 26 -40 40 Z" stroke-width="1.4"/>
 <path d="M44 64 V46 M38 46 Q44 32 50 46 Z" stroke-width="1.4"/>
 <path d="M-40 -64 q8 -6 16 0 q8 -6 16 0" stroke-width="1.3" opacity=".7"/>
 <path d="M26 -54 q6 -5 12 0 q6 -5 12 0" stroke-width="1.3" opacity=".7"/>
 <g class="plate-sails">
  <path d="M0 -14 L-8 -66 L4 -68 Z M0 -14 L52 -22 L54 -10 Z M0 -14 L8 38 L-4 40 Z M0 -14 L-52 -6 L-54 -18 Z" class="pf"/>
  <path d="M-3 -40 L3 -41 M-5 -54 L3 -55 M26 -16 L27 -10 M40 -18 L41 -12 M3 12 L-3 13 M5 26 L-3 27 M-26 -12 L-27 -18 M-40 -10 L-41 -16" stroke-width="1"/>
  <circle cy="-14" r="3.2" fill="currentColor"/>
 </g>
</g>"""


def plate_rim():
    """Bordure de l'assiette : feuillages et petits points alternés."""
    out = []
    for i in range(24):
        ang = i * 15
        if i % 2:
            out.append(f'<circle r="3.2" cy="-142" transform="rotate({ang})"/>')
        else:
            out.append(f'<path d="M0 -153 C-9 -146 -9 -136 0 -130 C9 -136 9 -146 0 -153Z" transform="rotate({ang})"/>')
    return "".join(out)


def tile_motif():
    """Motif de carreau de Delft : coins en fleur de lys et rosace centrale."""
    corner = '<path d="M0 0 Q14 2 16 16 Q2 14 0 0Z M0 0 Q9 -2 11 -9 M0 0 Q-2 9 -9 11"/>'
    return f"""<svg width="0" height="0" class="defs" aria-hidden="true"><defs>
<pattern id="delft" width="96" height="96" patternUnits="userSpaceOnUse">
 <rect class="t-line" width="96" height="96"/>
 <g class="t-ink">
  <g transform="translate(0 0)">{corner}</g><g transform="translate(96 0) rotate(90)">{corner}</g>
  <g transform="translate(96 96) rotate(180)">{corner}</g><g transform="translate(0 96) rotate(270)">{corner}</g>
  <circle cx="48" cy="48" r="7"/>
  <path d="M48 32 Q53 41 48 41 Q43 41 48 32Z M48 64 Q53 55 48 55 Q43 55 48 64Z M32 48 Q41 43 41 48 Q41 53 32 48Z M64 48 Q55 43 55 48 Q55 53 64 48Z"/>
 </g>
</pattern></defs></svg>"""


def frieze(cls="frieze"):
    return f'<svg class="{cls}" aria-hidden="true" preserveAspectRatio="none"><rect width="100%" height="100%" fill="url(#delft)"/></svg>'


def calendars(d):
    """Mois contenant les événements de l'agenda, rendus en grilles HTML."""
    years = [int(m.group(1)) for x in d["news"] + d["briefs"]
             for m in [re.search(r"(\d{4})", x.get("date", ""))] if m]
    year = max(years) if years else 2026
    ev_by_month = {}
    last_month = 0
    for i, e in enumerate(d["events"]):
        key = re.sub(r"[^A-ZÉÈÛÔ]", "", e["month"].upper())
        mo = MONTHS.get(key, 1)
        y = year + (1 if mo < last_month else 0)
        last_month = mo
        e = dict(e, idx=i, y=y, m=mo, d=int(e["day"]))
        ev_by_month.setdefault((y, mo), []).append(e)
    cal = calendar.Calendar(firstweekday=0)
    heads = "".join(f"<th scope=col abbr='{n}'>{n[0].upper()}</th>"
                    for n in ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"])
    months = []
    keys = sorted(ev_by_month)
    for k, (y, mo) in enumerate(keys):
        evs = ev_by_month[(y, mo)]
        days = {}
        for e in evs:
            days.setdefault(e["d"], []).append(e)
        rows = []
        for week in cal.monthdayscalendar(y, mo):
            cells = []
            for day in week:
                if not day:
                    cells.append("<td></td>")
                elif day in days:
                    ids = " ".join(f"ev{e['idx']}" for e in days[day])
                    n = len(days[day])
                    label = f"{day} {MONTH_NAMES[mo]} : {n} rendez-vous"
                    cells.append(f'<td><button type="button" class="has-ev" data-day="{ids}" aria-label="{E(label)}">'
                                 f'{day}<i aria-hidden="true">{"•" * n}</i></button></td>')
                else:
                    cells.append(f"<td><span>{day}</span></td>")
            rows.append("<tr>" + "".join(cells) + "</tr>")
        prev_btn = (f'<button type="button" class="cal-nav" data-cal-go="{k - 1}" aria-label="Mois précédent">{ms("chevron_left")}</button>'
                    if k > 0 else '<span class="cal-nav"></span>')
        next_btn = (f'<button type="button" class="cal-nav" data-cal-go="{k + 1}" aria-label="Mois suivant">{ms("chevron_right")}</button>'
                    if k < len(keys) - 1 else '<span class="cal-nav"></span>')
        months.append(f'<div class="cal-month" data-cal="{k}"{"" if k == 0 else " hidden"}>'
                      f'<div class="cal-head">{prev_btn}<p class="cal-title">{MONTH_NAMES[mo].capitalize()} {y}</p>{next_btn}</div>'
                      f'<table class="cal-grid"><caption class="sr-only">{MONTH_NAMES[mo].capitalize()} {y}</caption>'
                      f'<thead><tr>{heads}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    items = "".join(
        f'<li id="ev{i}">{a(e["href"], f"<time>{E(e["day"])} {E(e["month"].rstrip(".").lower())}</time>"
                                     f"<strong>{E(e["title"])}</strong><span>{E(e["desc"])}</span>")}</li>'
        for i, e in enumerate(d["events"]))
    return "".join(months), items


def render(d):
    q = {x["label"]: x for x in d["quick"]}

    def ql(label, text=None):
        x = q.get(label)
        return a(x["href"], E(text or label.lower())) if x else E(text or label)

    # Accès rapides rédigés comme une phrase.
    prose = (f"Souvent demandé : {ql('Menus cantine', 'les menus de la cantine')}, "
             f"{ql('Portail Famille', 'le portail famille')}, {ql('Numéros utiles', 'les numéros utiles')}, "
             f"{ql('Formalités', 'une formalité administrative')}, {ql('Urbanisme', 'l’urbanisme')}, "
             f"{ql('Salles municipales', 'la location d’une salle')}, {ql('Associations', 'les associations')} "
             f"ou {ql('Agenda', 'l’agenda')}.")

    # Sommaire (tiroir latéral, natif via <details>).
    drawer_items = []
    for it in d["nav"]:
        cols = "".join(
            (f'<p class="dr-sub">{E(c["title"])}</p>' if c["title"] and len(it["cols"]) > 1 else "")
            + "<ul>" + "".join(f"<li>{a(h, E(t))}</li>" for t, h in c["links"]) + "</ul>"
            for c in it["cols"])
        drawer_items.append(f'<details><summary>{ms(it["icon"])}<span>{E(it["label"])}</span>{ms("add", "ms plus")}</summary>'
                            f'<div class="dr-body">{cols}{a(it["href"], "Toute la rubrique " + ms("arrow_forward"), "dr-all")}</div></details>')

    # Assiette de navigation.
    n = len(d["nav"])
    dial_btns = "".join(
        f'<li style="--a:{i * 360 / n}deg"><button type="button" role="tab" id="dial-t{i}" aria-controls="dial-p{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-dial="{i}">'
        f'<span class="num">{ROMAN[i] if i < len(ROMAN) else i + 1}</span><span class="lbl">{E(it["label"])}</span></button></li>'
        for i, it in enumerate(d["nav"]))
    dial_panels = []
    for i, it in enumerate(d["nav"]):
        cols = "".join(
            '<div class="dp-col">' + (f'<p class="dp-sub">{E(c["title"])}</p>' if c["title"] and len(it["cols"]) > 1 else "")
            + "<ul>" + "".join(f"<li>{a(h, E(t))}</li>" for t, h in c["links"]) + "</ul></div>"
            for c in it["cols"])
        dial_panels.append(
            f'<div class="dial-panel" role="tabpanel" id="dial-p{i}" aria-labelledby="dial-t{i}"{"" if i == 0 else " hidden"}>'
            f'<p class="dp-kicker">Rubrique {ROMAN[i] if i < len(ROMAN) else i + 1}</p>'
            f'<h3>{E(it["label"])}</h3><p class="dp-desc">{E(it["desc"])}</p>'
            f'<div class="dp-cols">{cols}</div>{a(it["href"], "Ouvrir la rubrique " + ms("arrow_forward"), "dp-more")}</div>')

    briefs = "".join(
        f'<li>{a(b["href"], f"<time>{E(b["date"])}</time><span>{E(b["title"])}</span>")}</li>' for b in d["briefs"])

    news = "".join(
        f'<li class="acc{" is-on" if i == 0 else ""}" style="--img:url(\'{E(x["img"])}\')">'
        f'<button type="button" class="acc-tab" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="acc{i}">'
        f'<span class="acc-n">0{i + 1}</span><span class="acc-t">{E(x["title"].capitalize() if x["title"].isupper() else x["title"])}</span></button>'
        f'<div class="acc-body" id="acc{i}"><img src="{E(x["img"])}" alt="" loading="lazy">'
        f'<div class="acc-txt"><time>{E(x["date"])}</time><h3>{E(x["title"].capitalize() if x["title"].isupper() else x["title"])}</h3>'
        f'<p>{E(x["desc"])}</p>{a(x["href"], "Lire l’article " + ms("arrow_forward"), "link-u")}</div></div></li>'
        for i, x in enumerate(d["news"]))

    cal_months, cal_items = calendars(d)

    medals = "".join(
        f'<li>{a(x["href"], f"<span class=\"medal\"><img src=\"{E(x["img"])}\" alt=\"\" loading=\"lazy\"></span>"
                             f"<strong>{E(x["title"])}</strong><span class=\"md\">{E(x["desc"])}</span>")}</li>'
        for x in d["discover"])

    j = d["journal"]
    f = footer_links(d)
    nav_inline = "".join(f"<li>{a(it['href'], E(it['label']))}</li>" for it in d["nav"])

    body = f"""{tile_motif()}
<header class="hdr">
  <div class="hdr-top wrap"><p data-today></p><p data-open-status></p></div>
  <div class="hdr-main wrap">
    <a class="brand" href="#" aria-label="Méteren, accueil"><img src="{E(d["logo"])}" alt=""><span><strong>Méteren</strong><em>Flandre intérieure</em></span></a>
    <nav class="hdr-nav" aria-label="Rubriques"><ul>{nav_inline}</ul></nav>
    <div class="hdr-actions">
      <button type="button" class="ico-btn" data-search aria-label="Rechercher">{ms("search")}</button>
      <button type="button" class="som-btn" data-drawer aria-expanded="false" aria-controls="drawer">{ms("menu")}<span>Sommaire</span></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" aria-label="Sommaire du site" hidden>
  <div class="drawer-box" role="dialog" aria-modal="true" aria-labelledby="drawer-h">
    <div class="drawer-head"><p id="drawer-h">Sommaire</p><button type="button" class="ico-btn" data-drawer-close aria-label="Fermer le sommaire">{ms("close")}</button></div>
    <div class="drawer-list">{"".join(drawer_items)}</div>
    <div class="drawer-foot"><p><strong>Mairie de Méteren</strong><br>{E(ADDR)}</p><p>{a("tel:" + TEL.replace(" ", ""), E(TEL))} · {a("mailto:" + MAIL, E(MAIL))}</p></div>
  </div>
</div>

<main id="main">
  <section class="hero">
    {frieze("frieze top")}
    <div class="wrap hero-grid">
      <div class="hero-txt">
        <p class="kicker">Commune de Méteren · Nord</p>
        <form class="site-search" data-search-form role="search">
          <label for="q8">Que recherchez-vous&nbsp;?</label>
          <span class="search-field"><span class="ms" aria-hidden="true">search</span><input id="q8" type="search" placeholder="Ex. : horaires, cantine, urbanisme" autocomplete="off"><button type="submit" aria-label="Rechercher"><span>Rechercher</span>{ms("arrow_forward")}</button></span>
        </form>
        <p class="prose">{prose}</p>
      </div>
      <aside class="avis" aria-labelledby="avis-h">
        <span class="avis-corner tl" aria-hidden="true"></span><span class="avis-corner tr" aria-hidden="true"></span>
        <span class="avis-corner bl" aria-hidden="true"></span><span class="avis-corner br" aria-hidden="true"></span>
        <h2 id="avis-h">Avis à la population</h2>
        <ol>{briefs}</ol>
        {a(U_NEWS, "Tous les avis " + ms("arrow_forward"), "link-u")}
      </aside>
    </div>
  </section>

  <section class="explore" aria-labelledby="ex-h">
    <div class="wrap">
      <header class="sec-h"><p class="kicker">Explorer</p><h2 id="ex-h">Tournez l’assiette, trouvez votre rubrique</h2></header>
      <div class="dial-wrap">
        <div class="dial" style="--n:{n}">
          <svg class="plate" viewBox="-170 -170 340 340" aria-hidden="true">
            <circle r="166" class="plate-edge"/>
            <circle r="158" class="plate-bg"/>
            <g class="plate-turn">
              <circle r="150" class="plate-ring"/>
              <g class="plate-rim">{plate_rim()}</g>
              <circle r="122" class="plate-ring thin"/>
              <path class="plate-pointer" d="M0 -126 L-8 -112 L8 -112Z"/>
            </g>
            <circle r="104" class="plate-well"/>
            {MILL}
          </svg>
          <ul class="dial-btns" role="tablist" aria-label="Rubriques du site">{dial_btns}</ul>
        </div>
        <div class="dial-panels">{"".join(dial_panels)}</div>
      </div>
    </div>
  </section>

  <section class="now" aria-labelledby="now-h">
    <div class="wrap">
      <header class="sec-h"><p class="kicker">Ça se passe à Méteren</p><h2 id="now-h">Actualités &amp; rendez-vous</h2></header>
      <div class="now-grid">
        <div>
          <ul class="accordion">{news}</ul>
          <p class="more">{a(U_NEWS, "Toutes les actualités " + ms("arrow_forward"), "link-u")}</p>
        </div>
        <div class="agenda">
          <div class="cal">{cal_months}</div>
          <ol class="cal-list">{cal_items}</ol>
          <p class="more">{a(U_AGENDA, "Tout l’agenda " + ms("arrow_forward"), "link-u")}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="journal" aria-labelledby="jr-h">
    <div class="wrap jr-grid">
      {a(j["href"], f'<img src="{E(j["img"])}" alt="Couverture du {E(j["title"])}" loading="lazy">', "jr-cover")}
      <div class="jr-txt">
        <p class="kicker">Le journal municipal</p>
        <h2 id="jr-h">« Contact », {E(j["title"].replace("Contact ", "").strip() or j["title"])}</h2>
        <p>{E(j["text"])}</p>
        <p class="jr-act">{a(j["pdf"], ms("download") + " Lire le numéro", "btn")}{a(U_JOURNAL, "Les numéros précédents", "link-u")}</p>
      </div>
    </div>
  </section>

  <section class="discover" aria-labelledby="dc-h">
    <div class="wrap">
      <header class="sec-h"><p class="kicker">Découvrir</p><h2 id="dc-h">Méteren, entre Monts et bocage</h2></header>
      <ul class="medals">{medals}</ul>
    </div>
  </section>

  <section class="visit" aria-labelledby="vi-h">
    <div class="wrap visit-grid">
      <div class="arch"><iframe title="Plan d’accès à la mairie de Méteren" src="{MAP}" loading="lazy"></iframe></div>
      <div class="visit-txt">
        <p class="kicker">Nous rendre visite</p>
        <h2 id="vi-h">La mairie</h2>
        <p class="status" data-open-status></p>
        <address>{E(ADDR)}<br>{a("tel:" + TEL.replace(" ", ""), E(TEL))} · {a("mailto:" + MAIL, E(MAIL))}</address>
        <div class="hours"><h3>Mairie</h3><dl>{hours_dl(HOURS)}</dl><p class="note">{E(HOURS_NOTE)}</p></div>
        <div class="hours"><h3>Agence postale</h3><dl>{hours_dl(POSTE)}</dl></div>
        <p>{a(U_CONTACT, "Écrire à la mairie " + ms("arrow_forward"), "btn")}</p>
      </div>
    </div>
  </section>
</main>

<footer class="ftr">
  {frieze("frieze")}
  <div class="wrap ftr-grid">
    <div><p class="ftr-brand">Méteren</p><p>{E(LEAD)}</p><p>{a(d["facebook"], ms("thumb_up") + " Suivre la commune sur Facebook")}</p></div>
    <div><h2>Liens utiles</h2><ul>{f["ext"]}</ul></div>
    <div><h2>Labels</h2><ul class="labels">{f["labels"]}</ul></div>
  </div>
  <div class="wrap ftr-legal"><nav aria-label="Informations légales">{f["legal"]}</nav><p>© Commune de Méteren</p></div>
</footer>
"""
    return page(8, "Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Figtree:wght@400;500;600",
                body, ms_variant="Sharp", js="style-8.js")
