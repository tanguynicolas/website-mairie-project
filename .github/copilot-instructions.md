# Contexte pour agents IA

> Fichier dupliqué dans `AGENTS.md` (Codex) et `.github/copilot-instructions.md` (GitHub Copilot). Modifier les deux à l'identique.

Tenir à jour ce fichier au fil du projet et des demandes utilisateur, uniquement dans les parties suivantes : "Carte rapide du code", "Commandes", "Pièges connus".

## Projet

Prototype **statique** de refonte du site de la commune de Méteren (Nord), actuellement https://www.ville-meteren.fr/fr/. Pas de framework, pas de backend, pas de build JS : HTML/CSS/JS générés par des scripts Python.

- **Style 1 « Classique contemporain »** : style par défaut, **site complet** (~273 pages) dans `site/`, validé par le porteur du projet.
- **Styles 2 à 7** : variantes limitées à la **page d'accueil + menu** dans `styles/style-N.html`. Leurs liens mènent aux pages du style 1 (`../site/…`).
- `styles/index.html` : récapitulatif des styles avec vignettes. Un sélecteur de styles flottant est présent sur toutes les pages (y compris `site/`).

## Attentes du porteur du projet (à respecter)

- Répondre en **français**.
- **Conserver au moins en partie le contenu** du site actuel (le fond) ; la forme, le menu et l'organisation peuvent être réorganisés tant que cela reste logique.
- Ne pas casser le style 1 : c'est la base validée.
- Illustrations (par exemple SVG du style 7) : **fidèles à la réalité** et cohérentes avec la patte graphique existante. Se documenter (photos de référence) avant de dessiner un élément réel.
- Vérifier visuellement (desktop ~1440 px et mobile ~390 px) avant d'annoncer qu'un rendu est créé, corrigé, modifié.

## Règles Git

- Tous les commits doivent utiliser l'adresse personnelle **`***********@outlook.fr`** (auteur et committer). Des hooks locaux non versionnés (`.git/hooks/pre-commit`, `pre-push`) le contrôlent ; ne jamais les contourner (`--no-verify`) ni modifier la config Git globale.
- Messages au format `type(scope): description`, ex. `feat(skip): …`, `fix(skip): …` (types : feat, fix, docs, style, refactor, perf, test, chore, revert, …) (scopes : style 1, style 5, …).
- Commit et push à chaque demande de modification, après avoir vérifié le bon fonctionnement et la non regréssion.

## Carte rapide du code

| Besoin | Où regarder |
|---|---|
| Générer tout le site du style 1 | `build.py` (lit `pages/*.html`, écrit `site/`). Menu principal : constante `NAV`. Rendu : `header()`, `footer()`, `page()`, `build_*()` par type de page. |
| CSS/JS du style 1 | **Sources** : `assets/style.css`, `assets/main.js` → copiés dans `site/assets/` par `build.py` (avec `search-index.js` généré). |
| Données sources | `pages/` : captures HTML nettoyées du site d'origine (ne pas modifier sauf mise à jour du contenu). |
| Générer styles 2-8 + récap + sélecteur | `gen_styles.py` (copie `styles_src/` → `styles/`, appelle `stN.render(d)`, écrit `styles/index.html`, injecte le sélecteur dans `site/*.html` entre `<!-- style-selector:start -->` et `<!-- style-selector:end -->`). Descriptions du récap : dict `DESC`. |
| Ajouter un style N | Créer `stN.py` (fonction `render(d)`), `styles_src/style-N.css` (+ `.js` éventuel), ajouter le nom dans `NAMES` de `st_lib.py` et la description dans `DESC`, puis une vignette `styles_src/thumbs/style-N.png`. |
| Helpers communs aux variantes | `st_lib.py` : `NAMES`, coordonnées mairie (`ADDR`, `TEL`, `HOURS`…), `page()`, `proto_bar()`, `nav_items()`, `mega_cols()`, `asset_url()` (versionnement par hash SHA-256 contre le cache). |
| Données de l'accueil pour les variantes | `st_data.py` : extrait menu, accès rapides, actus, agenda… **depuis `site/index.html`** (donc dépend du style 1 généré). |
| Style 7 | `st7.py` (SVG du paysage : moulin animé, antenne `.antenna` avec balises clignotantes, houblonnière `.hop-field`), `styles_src/style-7.css` (`@keyframes beacon-blink`…), `styles_src/style-7.js` (onglets profils, carrousel). |
| Style 8 | `st8.py` (assiette de Delft SVG `.plate-turn` + onglets `[data-dial]`, accordéon `.acc`, calendrier mensuel généré `[data-cal]`/`[data-day]`, sommaire en tiroir `#drawer`), `styles_src/style-8.css`, `styles_src/style-8.js`. |

**Toujours éditer les sources** (`assets/`, `styles_src/`, `*.py`) et régénérer, jamais directement `site/` ou `styles/` (écrasés à la génération).

## Commandes

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python ≥ 3.12, beautifulsoup4
.venv/bin/python gen_styles.py                                       # variantes + récap + sélecteur
.venv/bin/python build.py && .venv/bin/python gen_styles.py          # tout reconstruire
python3 -m http.server 8000 --bind 127.0.0.1                         # servir la RACINE du dépôt
# puis http://localhost:8000/styles/index.html
```

- ⚠️ `build.py` **supprime puis recrée `site/`** ; toujours relancer `gen_styles.py` ensuite (sinon le sélecteur disparaît du style 1).
- Servir la racine (pas `site/` ni `styles/`), sinon les liens croisés `../site/` cassent.
- Pas de suite de tests : valider par régénération, contrôle des liens locaux et vérification visuelle.

## Pièges connus

- **Vignettes du récap** (`styles_src/thumbs/default.png`, `style-N.png`) : captures d'écran faites à la main (navigateur headless), non générées par les scripts. Les refaire après toute modification visible d'un style ou renumérotation, sinon elles ne correspondent plus.
- **Cache navigateur** : les URL de CSS/JS/vignettes passent par `asset_url()` (suffixe `?v=hash`). L'utiliser pour toute nouvelle ressource.
- **Cartes OpenStreetMap (iframe)** : les contraindre dans leur conteneur (`width/height/max-width: 100%`, ratio fixé) ; un bug de carte « géante » a déjà eu lieu sur les styles 5 et 6.
- Images et documents municipaux restent hébergés chez Neopse (`static.neopse.com`) ; polices Google Fonts + Material Symbols ; formulaire de contact = `mailto:` (pas de serveur).
- Le contenu est une capture datée du site d'origine.
- **Captures mobiles** : Chrome headless impose une largeur de fenêtre minimale (~500 px) ; pour un vrai rendu à 390 px, capturer une page hôte contenant une `<iframe>` de 390 px de large.
- **`gen_styles.py` doit rester idempotent** : relancé deux fois, il ne doit modifier aucun fichier de `site/` (la regex de retrait du sélecteur consomme aussi le saut de ligne ajouté).
