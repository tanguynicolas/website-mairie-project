# Projet de site pour la mairie de Méteren

Prototype statique de refonte du site de la commune de Méteren. Il comprend une proposition complète et six variantes de page d'accueil et de menu.

## Consulter les propositions

Depuis la racine du dépôt, démarrer un serveur local :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Ouvrir ensuite [la sélection des styles](http://localhost:8000/styles/index.html). Le style 1 donne accès au site complet ; les liens des styles 2 à 7 pointent vers ses pages.

## Organisation

- `site/` : site statique complet du style 1.
- `styles/` : sélection des styles et pages d'accueil des styles 2 à 7.
- `styles_src/`, `st2.py` à `st7.py`, `st_data.py`, `st_lib.py` et `gen_styles.py` : sources des variantes.
- `pages/`, `assets/` et `build.py` : données et sources utilisées pour générer le site complet. Les pages sources sont une copie du contenu public, sans les scripts tiers du site d'origine.

## Régénérer les pages

La génération nécessite Python 3.12 ou plus récent et Beautiful Soup :

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Pour régénérer les variantes et la sélection :

```sh
.venv/bin/python gen_styles.py
```

Pour reconstruire aussi le site complet à partir des données de `pages/` :

```sh
.venv/bin/python build.py
.venv/bin/python gen_styles.py
```

**Attention :** `build.py` supprime puis reconstruit le dossier `site/`. Sauvegarder au préalable toute modification manuelle de ce dossier. `gen_styles.py` réinstalle ensuite le sélecteur de styles sur les pages du site complet.

Les contenus correspondent à une capture du site existant et peuvent être datés. Les images et documents municipaux restent principalement hébergés sur les services d'origine ; les polices et la carte utilisent également des services externes. Le formulaire de contact du prototype ouvre la messagerie de l'utilisateur : il n'envoie pas de message depuis un serveur.
