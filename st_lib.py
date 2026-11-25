"""Utilitaires partagés par les 5 maquettes d'accueil."""
from html import escape as E
from hashlib import sha256
from pathlib import Path

NAMES = {2: "Institutionnel", 3: "Terroir flamand", 4: "Éditorial", 5: "Continuité", 6: "Bento",
         7: "Dynamique et illustré", 8: "Bleu de Flandre"}
DEFAULT_NAME = "Classique contemporain"
MAP = "https://www.openstreetmap.org/export/embed.html?bbox=2.6830%2C50.7360%2C2.7030%2C50.7450&layer=mapnik&marker=50.7406%2C2.6930"
AERIAL = "https://static.neopse.com/medias/p/1297/site/25/b7/93/25b793ab66c8be55d2f536a4b8b7cc27e727af6e.jpg?v=v1"
ADDR = "Place César Herreman, 59270 Méteren"
TEL = "03 28 49 04 08"
MAIL = "contact@ville-meteren.fr"
HOURS = [("Lundi – samedi", "8h30 – 12h00"), ("Mercredi", "+ 14h00 – 17h00")]
HOURS_NOTE = "Fermé le mercredi après-midi pendant les vacances scolaires."
POSTE = [("Lundi – vendredi", "8h30 – 11h45"), ("Samedi", "9h00 – 11h45")]
SITE = "../site/"

def asset_url(name):
    version = sha256((Path("styles_src") / name).read_bytes()).hexdigest()[:12]
    return f"{name}?v={version}"


def ms(name, cls="ms"):
    return f'<span class="{cls}" aria-hidden="true">{E(name)}</span>'


def a(href, text, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    ext = ' target="_blank" rel="noopener"' if href and href.startswith("http") else ""
    return f'<a href="{E(href)}"{c}{ext}{extra}>{text}</a>'


def proto_bar(n, style_prefix=""):
    default_href = "index.html" if n == 1 else SITE + "index.html"
    name = DEFAULT_NAME if n == 1 else NAMES[n]
    items = f'<a href="{default_href}" title="Style 1 · {E(DEFAULT_NAME)} — style par défaut"{" class=on aria-current=page" if n == 1 else ""}>1</a>'
    items += "".join(f'<a href="{style_prefix}style-{i}.html" title="Style {i} · {E(NAMES[i])}"{" class=on aria-current=page" if i == n else ""}>{i}</a>' for i in sorted(NAMES))
    return (f'<nav class="proto-bar" aria-label="Maquettes"><span>Style {n} · {E(name)}</span>{items}'
            f'<a href="{style_prefix}index.html" title="Tous les styles">☰</a></nav>')


def page(n, fonts, body, ms_variant="Rounded", js=None):
    fam = f"family={fonts}&family=Material+Symbols+{ms_variant}:opsz,wght,FILL@20..48,400,0..1"
    extra_js = f'\n<script src="{asset_url(js)}" defer></script>' if js else ""
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Méteren — Style {n} : {E(NAMES[n])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">
<link rel="stylesheet" href="{asset_url("common.css")}">
<link rel="stylesheet" href="{asset_url(f"style-{n}.css")}">
<style>:root{{--ms-font:'Material Symbols {ms_variant}'}}</style>
</head>
<body class="s{n}">
<a class="skip" href="#main">Aller au contenu</a>
{body}
{proto_bar(n)}
<script src="{SITE}assets/search-index.js" defer></script>
<script src="{asset_url("common.js")}" defer></script>{extra_js}
</body>
</html>
"""


def mega_cols(item, title_tag="p", title_cls="dd-title"):
    out = []
    for c in item["cols"]:
        links = "".join(f"<li>{a(h, E(t))}</li>" for t, h in c["links"])
        t = f'<{title_tag} class="{title_cls}">{E(c["title"])}</{title_tag}>' if c["title"] else ""
        out.append(f'<div class="dd-col">{t}<ul>{links}</ul></div>')
    return "".join(out)


def nav_items(d, render_panel, btn_inner=None, li_cls="nav-item"):
    """Génère <li data-dd-item> pour chaque rubrique ; render_panel(item) renvoie le contenu du panneau."""
    out = []
    for i, it in enumerate(d["nav"]):
        inner = btn_inner(it) if btn_inner else E(it["label"]) + ms("expand_more", "ms chev")
        out.append(f'<li class="{li_cls}" data-dd-item><button type="button" class="nav-btn" data-dd aria-controls="dd{i}">{inner}</button>'
                   f'<div class="dd" id="dd{i}">{render_panel(it)}</div></li>')
    return "".join(out)


def footer_links(d):
    return {
        "ext": "".join(f"<li>{a(h, E(t))}</li>" for t, h in d["ext"]),
        "labels": "".join(f"<li>{ms(i)}{E(t)}</li>" for i, t in d["labels"]),
        "legal": "".join(a(h, E(t)) for t, h in d["legal"]),
    }


def hours_dl(rows):
    return "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in rows)

LEAD = "Petite bourgade tranquille des Flandres intérieures, au cœur des Monts."
U_NEWS = SITE + "actualites.html"
U_AGENDA = SITE + "agenda.html"
U_JOURNAL = SITE + "journal-municipal.html"
U_CONTACT = SITE + "contact.html"
U_HOME = "#"
