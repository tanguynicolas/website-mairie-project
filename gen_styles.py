"""Génère les maquettes d'accueil (styles 2 et suivants) et la page de choix."""
import importlib
import os
import shutil
import re
from pathlib import Path

import st_data
from st_lib import NAMES, DEFAULT_NAME, E, proto_bar, asset_url

OUT = "styles"
d = st_data.load()
shutil.copytree("styles_src", OUT, dirs_exist_ok=True)

built = []
for n in sorted(NAMES):
    mod = importlib.import_module(f"st{n}")
    open(f"{OUT}/style-{n}.html", "w", encoding="utf-8").write(mod.render(d))
    built.append(n)

DESC = {
    2: "Sobre et officiel, inspiré du Système de design de l'État : marine, rouge du blason, angles nets. Méga-menu pleine largeur ouvert au clic, recherche visible dans l'en-tête.",
    3: "Chaleureux et local : crème, brique et vert bocage, typographie à empattements. Menu centré à petits menus déroulants, recherche posée sur la photo du village.",
    4: "Esprit journal municipal : grands titres à empattements, filets noirs, mise en page « à la une ». Menu texte et bouton « Tout le site » ouvrant un menu plein écran.",
    5: "Reprend les couleurs du site actuel (vert d'eau, bleu ciel, marine) en version moderne et arrondie. Barre de menu marine avec icônes et panneaux pastel.",
    6: "Grille de tuiles « bento » sur fond grège, accent jaune : tout est visible d'un coup d'œil. En-tête flottant en pilule et méga-menu en carte.",
    7: "Rompt avec l'organisation actuelle : paysage illustré des Monts de Flandre, fil « En bref » défilant, entrée par profil (« Vous êtes… »), agenda en billets, découverte en cartes postales. Une couleur par rubrique.",
}
cards = (
    f'<a class="c" href="../site/index.html"><img src="{asset_url("thumbs/default.png")}" alt="">'
    f'<span><b>Style 1 · {E(DEFAULT_NAME)}</b><strong class="badge">Style par défaut</strong>'
    '<em>La première proposition validée : une présentation sobre et aérée, des accès rapides '
    'et une navigation claire. Ce style est déjà décliné sur le site complet ; '
    'les liens des autres propositions mènent à ses pages.</em></span></a>'
)
cards += "".join(
    f'<a class="c" href="style-{n}.html"><img src="{asset_url(f"thumbs/style-{n}.png")}" alt="">'
    f'<span><b>Style {n} · {E(NAMES[n])}</b><em>{E(DESC[n])}</em></span></a>' for n in built)
total = len(built) + 1
open(f"{OUT}/index.html", "w", encoding="utf-8").write(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Méteren — {total} styles d'accueil</title>
<style>
body{{margin:0;font:16px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif;background:#f3f3f1;color:#1b1b1b}}
main{{max-width:1240px;margin:0 auto;padding:48px 24px}}
h1{{margin:0 0 6px;font-size:32px}} p.l{{margin:0 0 30px;color:#555}} p.l a{{color:#1f3a68}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(360px,100%),1fr));gap:22px}}
.c{{display:flex;flex-direction:column;background:#fff;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 1px 3px rgba(0,0,0,.08);transition:transform .2s,box-shadow .2s}}
.c:hover{{transform:translateY(-3px);box-shadow:0 14px 34px rgba(0,0,0,.12)}}
.c img{{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;border-bottom:1px solid #eee}}
.c span{{padding:16px 18px 20px;display:flex;flex-direction:column;gap:6px}} .c em{{font-style:normal;color:#555;font-size:15px}}
.badge{{align-self:flex-start;padding:3px 10px;background:#e7efe9;color:#254b35;border-radius:999px;font-size:13px}}
</style></head><body><main>
<h1>Méteren — {total} propositions de style</h1>
<p class="l">Le <a href="../site/index.html">style 1 — {E(DEFAULT_NAME)}</a> est le style par défaut du site complet. Les styles 2 à {built[-1]} proposent uniquement une autre page d'accueil et un autre menu ; leurs liens mènent aux pages du style par défaut.</p>
<div class="g">{cards}</div></main></body></html>""")
selector_css = '<link rel="stylesheet" href="../styles/selector.css">'
selector = "<!-- style-selector:start -->" + proto_bar(1, "../styles/") + "<!-- style-selector:end -->"
for path in Path("site").glob("*.html"):
    content = path.read_text(encoding="utf-8")
    content = re.sub(r"<!-- style-selector:start -->.*?<!-- style-selector:end -->", "", content, flags=re.S)
    if selector_css not in content:
        content = content.replace("</head>", selector_css + "\n</head>")
    content = content.replace("</body>", selector + "\n</body>")
    path.write_text(content, encoding="utf-8")
print("OK", built)
