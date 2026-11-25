import re, glob, os, json, html, shutil, datetime
from bs4 import BeautifulSoup, NavigableString, Comment

SRC = "pages"
OUT = "site"
ORIGIN = "https://www.ville-meteren.fr"

LOGO = "https://static.neopse.com/medias/p/1297/site/cc/fc/99/ccfc999b506d1617832c9f2e2923d479e750db24.png"
HERO = "https://static.neopse.com/medias/p/1297/site/58/77/63/587763ecbed68ebcb8a5b7bd7007d52539e86058.jpg?v=v1"

# ---------------------------------------------------------------- navigation
P = {
    "presentation": "/fr/rb/427130/presentation-46",
    "conseil": "/fr/tb/731980/conseil-municipal-112",
    "commissions": "/fr/rb/1522913/commissions-81",
    "cr": "/fr/rp/731512/comptes-rendus-655",
    "services": "/fr/rb/427260/services-municipaux-45",
    "interco": "/fr/rb/427156/intercommunalite-68",
    "syndicats": "/fr/rb/1014405/syndicats-intercommunaux-6",
    "journal": "/fr/pb/731902/journal-municipal",
    "presse": "/fr/pr/731551/espace-presse-114",
    "formalites": "/fr/rb/982191/formalites-administratives-5",
    "urbanisme": "/fr/rb/427312/habitat-et-urbanisme-1",
    "salles": "/fr/rb/1014366/salles-municipales-60",
    "guide": "/fr/pg/731122/guide-des-demarches-270",
    "poste": "/fr/rb/982100/agence-postale-33",
    "faq": "/fr/rb/1116767/faq-2",
    "portail": "/fr/rb/982542/inscriptions-et-facturation-aux-services",
    "enfance": "/fr/rb/427338/enfance-et-jeunesse-6",
    "cantine": "/fr/rb/982490/menus-cantine-6",
    "seniors": "/fr/rb/427351/seniors-19",
    "social": "/fr/rb/982282/actions-sociales-2",
    "sante": "/fr/rb/1058865/sante-prevention-et-informations",
    "pros_sante": "/fr/he/731356/professionnels-de-sante-2",
    "cadre": "/fr/rb/427429/cadre-de-vie-3",
    "transports": "/fr/rb/982256/transports-108",
    "citoyen": "/fr/rb/1022790/participation-citoyenne-6",
    "paroisse": "/fr/rb/982230/paroisse-et-lieux-de-culte-1",
    "numeros": "/fr/rb/1017486/numeros-utiles-175",
    "assos": "/fr/as/731395/associations-22",
    "equipements": "/fr/rb/427390/equipements-8",
    "mediatheque": "/fr/rb/894779/mediatheque-49",
    "tourisme": "/fr/rb/1061972/tourisme-10",
    "sentiers": "/fr/rb/427650/sentiers-de-randonnee",
    "agenda": "/fr/ev/730303/fetes-et-ceremonies",
    "photos": "/fr/pc/730888/galeries-de-photos-265",
    "videos": "/fr/vd/730849/galerie-de-videos-256",
    "artisans": "/fr/rb/1056525/artisans-50",
    "commercants": "/fr/rb/982022/commercants-2",
    "entreprises": "/fr/rb/982035/entreprises-43",
    "agricoles": "/fr/rb/1056330/exploitations-agricoles-2",
    "marche": "/fr/rb/1056317/marche-13",
    "actus": "/fr/nw/730264/actualites-561",
    "contact": "/fr/ct/730186/contacts-535",
    "mentions": "/fr/li/730225/mentions-legales-590",
    "confidentialite": "/fr/730225/politique-confidentialite",
    "accessibilite": "/fr/accessibilite",
}

NAV = [
    ("mairie", "Mairie", "account_balance", "Votre commune, vos élus et la vie municipale.", [
        ("La commune", ["presentation"]),
        ("Vie municipale", ["conseil", "commissions", "cr", "services"]),
        ("Intercommunalité", ["interco", "syndicats"]),
        ("Publications", ["journal", "presse"]),
    ]),
    ("demarches", "Démarches", "description", "Formalités, urbanisme, location de salles et services en ligne.", [
        ("Formalités", ["formalites", "guide", "faq"]),
        ("Logement & locations", ["urbanisme", "salles"]),
        ("Services", ["portail", "poste"]),
    ]),
    ("vivre", "Vivre à Méteren", "home", "Famille, solidarité, santé et cadre de vie au quotidien.", [
        ("Famille & solidarité", ["enfance", "cantine", "seniors", "social"]),
        ("Santé", ["sante", "pros_sante"]),
        ("Cadre de vie", ["cadre", "transports", "citoyen", "paroisse", "numeros"]),
    ]),
    ("loisirs", "Loisirs & découverte", "park", "Associations, équipements, tourisme et patrimoine.", [
        ("Sortir", ["agenda", "assos", "equipements", "mediatheque"]),
        ("Découvrir", ["tourisme", "sentiers"]),
        ("En images", ["photos", "videos"]),
    ]),
    ("economie", "Économie", "storefront", "Commerces, artisans, entreprises et marché.", [
        ("Acteurs économiques", ["commercants", "artisans", "entreprises", "agricoles", "marche"]),
    ]),
    ("actualites", "Actualités", "campaign", "Informations, arrêtés et agenda de la commune.", [
        ("Actualités", ["actus", "agenda"]),
    ]),
]
# rubrique -> owning section (first occurrence wins, "agenda" belongs to actualites)
OWNER = {}
for sid, _, _, _, groups in NAV:
    for _, keys in groups:
        for k in keys:
            OWNER.setdefault(P[k], sid)
OWNER[P["agenda"]] = "actualites"
OWNER[P["portail"]] = "vivre"

SHORT = {"pros_sante": "Professionnels de santé", "portail": "Portail Famille", "agenda": "Agenda",
         "guide": "Guide des démarches", "sante": "Santé : prévention et informations",
         "actus": "Toutes les actualités", "cr": "Comptes rendus du conseil"}

# ---------------------------------------------------------------- load pages
def fn(p):
    return re.sub(r"[^a-zA-Z0-9]+", "_", p).strip("_")

paths = {"/fr/"}
raw = {}
for f in glob.glob(f"{SRC}/*.html"):
    raw[os.path.basename(f)[:-5]] = open(f).read()
for h in raw.values():
    for u in re.findall(r'href="((?:https?://(?:www\.)?ville-meteren\.(?:neopse-site\.)?fr)?/fr/[^"#?]*)"', h):
        paths.add(re.sub(r"^https?://[^/]+", "", u))
for k in ["/fr/rb/1253943/gite-rural-de-nachtegaal",
          "/fr/pr/731551/11624/meteren-le-grand-chantier-de-rehabilitation-de-la-mairie-debutera-en-septembre"]:
    paths.add(k)
for b, n in [(P["assos"], 2), (P["assos"], 3)] + [(P["cr"], i) for i in range(1, 6)]:
    paths.add(f"{b}/{n}")
fmap = {fn(p): p.rstrip("/") for p in paths}

docs = {}
extra_pages = {}  # base list path -> [soups]
for key, h in raw.items():
    path = fmap.get(key)
    if path is None or path in ("/fr",):
        continue
    m = re.match(r"(/fr/[a-z]+/\d+/[^/]+)/(\d+)$", path)
    if m and m.group(1) in (P["assos"], P["cr"]):
        extra_pages.setdefault(m.group(1), []).append(BeautifulSoup(h, "html.parser"))
        continue
    docs[path] = {"path": path, "soup": BeautifulSoup(h, "html.parser")}

home_soup = BeautifulSoup(raw["fr"], "html.parser")

for d in docs.values():
    s = d["soup"]
    h1 = s.select_one("header.breadcrumb h1")
    d["title"] = re.sub(r"\s+", " ", h1.get_text()).strip() if h1 else ""
    d["crumbs"] = [(re.sub(r"\s+", " ", a.get_text()).strip(), a.get("href")) for a in s.select("nav.ariane a")]
    seg = d["path"].strip("/").split("/")
    d["kind"] = seg[1] if len(seg) > 2 else "static"
    d["is_list"] = d["kind"] != "rb" and len(seg) == 4
    side = s.select_one(".sous-rubriques")
    d["children"] = []
    if d["kind"] == "rb" and side and side.find("h1") and side.find("h1").get_text(strip=True) == d["title"]:
        d["children"] = [a["href"].rstrip("/") for a in side.select("a[href]")]
    cat = s.select_one(".main-content .categories")
    d["cat"] = cat.get_text(" ", strip=True) if cat else ""
    main = s.select_one(".main-content")
    txt = main.get_text(" ", strip=True) if main else ""
    dm = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", txt)
    d["date"] = dm.group(1) if dm else ""
    img = None
    if main:
        for i in main.select("img"):
            if "rdc-logo" not in (i.get("src") or ""):
                img = i.get("src"); break
    d["img"] = img
    real = [h for t, h in d["crumbs"][1:] if h and h.rstrip("/") not in ("", "/fr")]
    real = [h.rstrip("/") for h in real]
    d["root"] = real[0] if real else d["path"]
    d["parent"] = real[-2] if len(real) >= 2 and real[-1] == d["path"] else None

# fix titles from home for legal pages etc.
for p in (P["mentions"], P["confidentialite"], P["accessibilite"]):
    if p in docs and not docs[p]["title"]:
        docs[p]["title"] = {P["mentions"]: "Mentions légales", P["confidentialite"]: "Politique de confidentialité",
                            P["accessibilite"]: "Accessibilité"}[p]

if P["agenda"] in docs:
    docs[P["agenda"]]["title"] = "Agenda"

# ---------------------------------------------------------------- slugs
SPECIAL = {P["actus"]: "actualites", P["agenda"]: "agenda", P["contact"]: "contact", P["assos"]: "associations",
           P["conseil"]: "conseil-municipal", P["cr"]: "comptes-rendus", P["journal"]: "journal-municipal",
           P["presse"]: "espace-presse", P["pros_sante"]: "professionnels-de-sante", P["photos"]: "galeries-photos",
           P["videos"]: "videos", P["guide"]: "guide-des-demarches", P["faq"]: "faq",
           P["mentions"]: "mentions-legales", P["confidentialite"]: "confidentialite", P["accessibilite"]: "accessibilite"}
used = {"index", "plan-du-site", "recherche"} | {s[0] for s in NAV}
for p in sorted(docs, key=lambda x: (len(x), x)):
    if p in SPECIAL:
        s = SPECIAL[p]
    else:
        last = p.rstrip("/").split("/")[-1]
        s = re.sub(r"-\d+$", "", last)
        if s in used:
            s = last
        if s in used:
            s = p.split("/")[-2] + "-" + last
    used.add(s)
    docs[p]["slug"] = s

def url_for(path):
    path = path.rstrip("/")
    if path in docs:
        return docs[path]["slug"] + ".html"
    m = re.match(r"(/fr/[a-z]+/\d+/[^/]+)/\d+$", path)
    if m and m.group(1) in docs:
        return docs[m.group(1)]["slug"] + ".html"
    if path in ("", "/fr"):
        return "index.html"
    return None

def section_of(d):
    return OWNER.get(d["root"]) or OWNER.get(d["path"]) or None

# children tree from breadcrumbs (fallback when no sidebar)
for d in docs.values():
    if d["parent"] and d["parent"] in docs and d["kind"] == "rb":
        par = docs[d["parent"]]
        if d["path"] not in par["children"]:
            par["children"].append(d["path"])

# ---------------------------------------------------------------- content cleaning
KEEP_ATTR = {"a": ["href"], "img": ["src", "alt"], "iframe": ["src", "title", "allowfullscreen"],
             "td": ["colspan", "rowspan"], "th": ["colspan", "rowspan"], "span": ["class"], "div": ["class"],
             "ol": ["start"]}
URL_RE = re.compile(r"(https?://[^\s<>\"]+)")

def fix_href(href):
    if not href:
        return None
    href = href.strip()
    if href.startswith("//"):
        href = "https:" + href
    m = re.match(r"https?://(?:www\.)?ville-meteren\.(?:neopse-site\.)?fr(/.*)?$", href)
    if m:
        href = m.group(1) or "/"
    if href.startswith("/fr") or href == "/":
        u = url_for(href.split("#")[0].split("?")[0])
        return u or ORIGIN + href
    if href.startswith("/"):
        return ORIGIN + href
    return href

def clean(node, soup):
    for sel in ["script", "style", "form", ".modal", "button", "input", "select", "textarea", ".sous-rubriques",
                "nav", "header", ".pagination", ".categories", "noscript", "svg", "hr"]:
        for e in node.select(sel):
            e.decompose()
    for c in node.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for a in node.select('a[data-toggle="modal"]'):
        p = a.find_parent("p")
        (p or a).decompose()
    # youtube
    for y in node.select(".youtube_player[videoid]"):
        ifr = soup.new_tag("iframe", src=f"https://www.youtube-nocookie.com/embed/{y['videoid']}",
                           title=y.get("title", "Vidéo"), allowfullscreen="")
        wrap = soup.new_tag("div", attrs={"class": "video"})
        wrap.append(ifr)
        (y.find_parent(class_="embed-responsive") or y).replace_with(wrap)
    # galleries
    for g in node.select(".splide"):
        wrap = soup.new_tag("div", attrs={"class": "gallery"})
        for im in g.select("img"):
            a = soup.new_tag("a", href=im.get("src"))
            a["data-lightbox"] = "1"
            im2 = soup.new_tag("img", src=im.get("src"), alt=im.get("alt", ""))
            a.append(im2)
            wrap.append(a)
        (g.find_parent(class_="bloc-diapo") or g).replace_with(wrap)
    # icons
    for i in node.select("i.material-icons, i.material-icons-outlined"):
        name = i.get_text(strip=True)
        if name in ("keyboard_arrow_right", "remove_red_eye"):
            i.decompose(); continue
        sp = soup.new_tag("span", attrs={"class": "ms", "aria-hidden": "true"})
        sp.string = name
        i.replace_with(sp)
    # empty coordinates ("-")
    for blk in node.select(".col-md-4"):
        inf = blk.select_one(".info")
        if inf and inf.get_text(strip=True) == "-":
            blk.decompose()
    # association roles -> dl
    for box in node.select(".event-coordonnees .d-flex > .d-flex"):
        cols = box.find_all("div", recursive=False)
        if len(cols) == 2:
            labels = [p.get_text(" ", strip=True) for p in cols[0].find_all("p")]
            vals = [p.get_text(" ", strip=True) for p in cols[1].find_all("p")]
            dl = soup.new_tag("dl", attrs={"class": "roles"})
            for l, v in zip(labels, vals):
                if v and v != "-":
                    dt = soup.new_tag("dt"); dt.string = l.rstrip(":")
                    dd = soup.new_tag("dd"); dd.string = v
                    dl.append(dt); dl.append(dd)
            outer = box.find_parent(class_="d-flex")
            if len(dl.contents):
                outer.replace_with(dl)
            else:
                outer.decompose()
    # grids
    for r in node.select(".row"):
        cols = [c for c in r.find_all("div", recursive=False) if any("col" in x for x in c.get("class", []))]
        if len(cols) >= 2:
            r["class"] = ["grid"]
    for e in node.select(".info-background, .event-infos#lieu, #lieu"):
        e["class"] = ["box"]
    for e in node.select(".ckeditor_info, .photo-panel, .text-right"):
        pass
    for e in node.select("p.text-right"):
        if re.fullmatch(r"\s*\d{2}/\d{2}/\d{4}\s*", e.get_text()):
            e.decompose()
    for e in node.select(".event-thumbnail-wrapper > img, .col-12.col-md-4 > img.card-img-top"):
        e["class"] = ["aside-img"]
    # attributes
    for t in node.find_all(True):
        if t.name in ("font", "u", "center"):
            t.unwrap(); continue
        if t.name == "span" and "ms" not in (t.get("class") or []):
            t.unwrap(); continue
        cls = [c for c in (t.get("class") or []) if c in ("grid", "box", "gallery", "video", "ms", "roles", "aside-img")]
        allowed = KEEP_ATTR.get(t.name, [])
        for a in list(t.attrs):
            if a in ("data-lightbox", "aria-hidden"):
                continue
            if a == "class":
                continue
            if a not in allowed:
                del t[a]
        if cls:
            t["class"] = cls
        elif "class" in t.attrs:
            del t["class"]
        if t.name == "a":
            h = fix_href(t.get("href"))
            if h:
                t["href"] = h
                if h.startswith("http") and not h.startswith(ORIGIN):
                    t["target"] = "_blank"; t["rel"] = "noopener"
                if re.search(r"/files/download/|\.(pdf|docx?|xlsx?)$", h, re.I):
                    t["class"] = (t.get("class") or []) + ["file"]
            elif "href" in t.attrs:
                del t["href"]
        if t.name == "img":
            src = t.get("src") or ""
            if src.startswith("//"):
                t["src"] = "https:" + src
            elif src.startswith("/"):
                t["src"] = ORIGIN + src
            t["loading"] = "lazy"
        if t.name in ("h1",):
            t.name = "h2"
    # autolink bare URLs
    for tn in list(node.find_all(string=URL_RE)):
        if tn.find_parent("a"):
            continue
        parts = URL_RE.split(str(tn))
        new = []
        for i, part in enumerate(parts):
            if i % 2:
                a = soup.new_tag("a", href=part, target="_blank", rel="noopener")
                a.string = part
                new.append(a)
            elif part:
                new.append(NavigableString(part))
        for n in new:
            tn.insert_before(n)
        tn.extract()
    # empty info fields ("-") and label-only blocks
    for t in node.find_all(["p", "span", "div"]):
        if t.get_text(strip=True) == "-":
            t.decompose()
    for t in node.find_all("div"):
        kids = [c for c in t.find_all(True, recursive=False)]
        if kids and all(c.name in ("h3", "h4") or "ms" in (c.get("class") or []) for c in kids) \
                and not t.find(["img", "iframe", "a"]) \
                and not "".join(c for c in t.children if isinstance(c, NavigableString)).strip():
            t.decompose()
    for a in node.select('a[href^="#"]'):
        if not node.find(id=a["href"][1:]):
            a.unwrap()
    # prune empties
    changed = True
    while changed:
        changed = False
        for t in node.find_all(["p", "div", "h2", "h3", "h4", "h5", "li", "ul", "strong", "em", "b", "a"]):
            if t.find(["img", "iframe", "br"]) and t.get_text(strip=True) == "" and t.find(["img", "iframe"]):
                continue
            if t.get_text(strip=True) == "" and not t.find(["img", "iframe"]):
                t.decompose(); changed = True
    # unwrap meaningless divs
    for t in node.find_all("div"):
        if not t.get("class") and len([c for c in t.children if not (isinstance(c, NavigableString) and not c.strip())]) == 1 \
                and t.find(True, recursive=False) is not None and t.find(True, recursive=False).name in ("div", "p", "a", "img", "table", "ul"):
            t.unwrap()
    out = node.decode_contents()
    out = re.sub(r"(<br/>\s*){3,}", "<br/><br/>", out)
    out = re.sub(r"\n\s*\n+", "\n", out)
    return out.strip()

def content_of(d):
    s = d["soup"]
    main = s.select_one(".main-content")
    if not main:
        main = s.select_one("section.wrapper")
    if not main:
        return ""
    import copy
    return clean(copy.copy(main), s)

def text_of(htmlfrag):
    return re.sub(r"\s+", " ", BeautifulSoup(htmlfrag, "html.parser").get_text(" ")).strip()

for d in docs.values():
    d["html"] = content_of(d)
    d["text"] = text_of(d["html"])

# ---------------------------------------------------------------- layout
def esc(s):
    return html.escape(s or "", quote=True)

def ms(name):
    return f'<span class="ms" aria-hidden="true">{name}</span>'

def label(k):
    p = P[k]
    return SHORT.get(k) or (docs[p]["title"] if p in docs else k)

def header(active):
    items = []
    for sid, name, icon, desc, groups in NAV:
        cols = []
        for gname, keys in groups:
            links = "".join(f'<li><a href="{url_for(P[k])}">{esc(label(k))}</a></li>' for k in keys if url_for(P[k]))
            cols.append(f'<div class="mega-col"><p class="mega-title">{esc(gname)}</p><ul>{links}</ul></div>')
        cls = " is-active" if sid == active else ""
        items.append(f'''<li class="nav-item{cls}">
  <button class="nav-btn" aria-expanded="false" aria-controls="mega-{sid}">{esc(name)}<span class="ms chev" aria-hidden="true">expand_more</span></button>
  <div class="mega" id="mega-{sid}"><div class="mega-inner">
    <a class="mega-intro" href="{sid}.html">{ms(icon)}<strong>{esc(name)}</strong><span>{esc(desc)}</span><em>Tout voir {ms("arrow_forward")}</em></a>
    {''.join(cols)}
  </div></div>
</li>''')
    return f'''<a class="skip" href="#contenu">Aller au contenu</a>
<div class="topbar"><div class="wrap">
  <span>{ms("location_on")} Place César Herreman, 59270 Méteren</span>
  <span class="hide-sm">{ms("schedule")} Mairie ouverte du lundi au samedi, 8h30–12h</span>
  <a href="tel:+33328490408">{ms("call")} 03 28 49 04 08</a>
</div></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html"><img src="{LOGO}" alt="Logo de Méteren"><span><strong>Méteren</strong><small>Commune des Flandres</small></span></a>
    <nav class="main-nav" aria-label="Navigation principale"><ul>{''.join(items)}</ul></nav>
    <div class="header-actions">
      <button class="icon-btn" data-open-search aria-label="Rechercher">{ms("search")}</button>
      <a class="btn btn-primary hide-sm" href="contact.html">{ms("mail")} Contact</a>
      <button class="icon-btn burger" aria-label="Menu" aria-expanded="false">{ms("menu")}</button>
    </div>
  </div>
</header>
<div class="search-overlay" hidden>
  <div class="search-panel" role="dialog" aria-label="Recherche">
    <div class="search-field">{ms("search")}<input type="search" placeholder="Rechercher une démarche, un service, une association…" aria-label="Rechercher"><button class="icon-btn" data-close-search aria-label="Fermer">{ms("close")}</button></div>
    <ul class="search-results"></ul>
  </div>
</div>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-light" href="index.html"><img src="{LOGO}" alt=""><span><strong>Commune de Méteren</strong></span></a>
      <p>Place César Herreman<br>59270 Méteren – France</p>
      <p><a href="tel:+33328490408">{ms("call")} +33 3 28 49 04 08</a><br><a href="mailto:contact@ville-meteren.fr">{ms("mail")} contact@ville-meteren.fr</a></p>
      <p><a class="btn btn-light" href="contact.html">Nous écrire</a> <a class="btn btn-ghost" href="https://www.facebook.com/Commune-de-M%C3%A9teren-110030343958746" target="_blank" rel="noopener">Facebook</a></p>
    </div>
    <div>
      <h2>Horaires d'ouverture</h2>
      <p><strong>La mairie</strong><br>Du lundi au samedi de 8h30 à 12h<br>Le mercredi de 8h30 à 12h et de 14h à 17h<br><small>(sauf durant les vacances scolaires, fermé le mercredi après-midi)</small></p>
      <p><strong>Agence postale</strong><br>Du lundi au vendredi de 8h30 à 11h45<br>Samedi de 9h à 11h45</p>
    </div>
    <div>
      <h2>Liens</h2>
      <ul class="plain">
        <li><a href="https://cc-flandreinterieure.fr/fr/" target="_blank" rel="noopener">Cœur de Flandre Agglo</a></li>
        <li><a href="https://www.hautsdefrance.fr/" target="_blank" rel="noopener">Conseil régional Hauts-de-France</a></li>
        <li><a href="https://lenord.fr/jcms/j_6/accueil" target="_blank" rel="noopener">Département du Nord</a></li>
        <li><a href="https://www.nord.gouv.fr/" target="_blank" rel="noopener">Préfecture du Nord</a></li>
      </ul>
    </div>
    <div>
      <h2>Labels</h2>
      <ul class="labels">
        <li>{ms("local_florist")} Villes et villages fleuris</li>
        <li>{ms("military_tech")} Mission Centenaire 14-18</li>
        <li>{ms("visibility")} Voisins vigilants et solidaires</li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© Commune de Méteren</span>
    <nav aria-label="Liens légaux"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Politique de confidentialité</a><a href="accessibilite.html">Accessibilité</a><a href="plan-du-site.html">Plan du site</a><a href="faq.html">FAQ</a></nav>
  </div>
</footer>
<div class="lightbox" hidden><button class="icon-btn" aria-label="Fermer">{ms("close")}</button><img alt=""></div>'''

def page(title, body, active=None, desc="", cls=""):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}{" – " if title != "Méteren" else ""}{"Commune de Méteren" if title != "Méteren" else " – Site officiel de la commune"}</title>
<meta name="description" content="{esc(desc or "Site officiel de la commune de Méteren (Nord) : démarches, vie municipale, actualités, associations et loisirs.")}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL@20..48,400,0..1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="{LOGO}">
</head>
<body class="{cls}">
{header(active)}
<main id="contenu">
{body}
</main>
{footer()}
<script src="assets/search-index.js"></script>
<script src="assets/main.js"></script>
</body>
</html>'''

def crumbs_html(items):
    parts = ['<a href="index.html">Accueil</a>']
    for t, u in items:
        parts.append(f'<a href="{u}">{esc(t)}</a>' if u else f'<span aria-current="page">{esc(t)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + f'{ms("chevron_right")}'.join(parts) + "</nav>"

def sec_meta(sid):
    for n in NAV:
        if n[0] == sid:
            return n
    return None

def page_head(title, crumbs, meta="", lead=""):
    return f'''<section class="page-head"><div class="wrap">
{crumbs_html(crumbs)}
<h1>{esc(title)}</h1>{f'<div class="page-meta">{meta}</div>' if meta else ''}{f'<p class="lead">{lead}</p>' if lead else ''}
</div></section>'''

def sidebar(sid, current_path):
    meta = sec_meta(sid)
    if not meta:
        return ""
    cur = docs.get(current_path)
    chain = set()
    p = current_path
    while p in docs:
        chain.add(p)
        p = docs[p]["parent"]
    out = [f'<aside class="side"><p class="side-title">{ms(meta[2])} {esc(meta[1])}</p>']
    for gname, keys in meta[4]:
        out.append(f'<p class="side-group">{esc(gname)}</p><ul>')
        for k in keys:
            path = P[k]
            u = url_for(path)
            if not u:
                continue
            act = " class=\"active\"" if path == current_path else (" class=\"open\"" if path in chain else "")
            out.append(f'<li><a href="{u}"{act}>{esc(label(k))}</a>')
            if path in chain and path in docs and docs[path]["kind"] == "rb":
                out.append(sub_tree(path, chain, current_path))
            out.append("</li>")
        out.append("</ul>")
    out.append("</aside>")
    return "".join(out)

def sub_tree(path, chain, current):
    ch = [c for c in docs[path]["children"] if c in docs]
    if not ch:
        return ""
    s = "<ul>"
    for c in ch:
        act = ' class="active"' if c == current else ""
        s += f'<li><a href="{url_for(c)}"{act}>{esc(docs[c]["title"])}</a>'
        if c in chain:
            s += sub_tree(c, chain, current)
        s += "</li>"
    return s + "</ul>"

def breadcrumb_for(d):
    sid = section_of(d)
    items = []
    meta = sec_meta(sid)
    if meta:
        items.append((meta[1], f"{sid}.html"))
    chain = []
    p = d["parent"]
    while p and p in docs:
        chain.insert(0, p)
        p = docs[p]["parent"]
    if d["kind"] != "rb" and not d["is_list"]:
        lst = "/".join(d["path"].split("/")[:5])
        if lst in docs and lst not in chain:
            chain = [lst]
    for c in chain:
        items.append((docs[c]["title"], url_for(c)))
    items.append((d["title"], None))
    return items

def card(href, title, img=None, meta="", text="", icon=None, extra_cls=""):
    media = f'<div class="card-media"><img src="{esc(img)}" alt="" loading="lazy"></div>' if img else (
        f'<div class="card-icon">{ms(icon)}</div>' if icon else "")
    return f'''<a class="card {extra_cls}" href="{esc(href)}">{media}<div class="card-body">{f'<p class="card-meta">{meta}</p>' if meta else ''}<h3>{esc(title)}</h3>{f'<p>{esc(text)}</p>' if text else ''}</div></a>'''

def excerpt(t, n=150):
    t = t or ""
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"

def write(name, content):
    content = re.sub(r'<span[^>]*class="ms"[^>]*>\s*file_download\s*</span>\s*', '', content)
    content = content.replace("file_download ", "")
    content = re.sub(r'(<a class="file"[^>]*>)\s*(?:<span class="ms"[^>]*>\s*file_download\s*</span>|file_download)\s*', r'\1', content)
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)

# ---------------------------------------------------------------- list builders
MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
def dkey(d):
    try:
        return datetime.datetime.strptime(d, "%d/%m/%Y")
    except Exception:
        return datetime.datetime(1900, 1, 1)

def details_of(listpath):
    pre = listpath.rsplit("/", 1)[0] + "/"
    return [d for d in docs.values() if d["path"].startswith(pre) and not d["is_list"] and d["path"] != listpath]

def list_cards_from(soup, listpath):
    """subtitle text from cards in listing pages (home + list)"""
    out = {}
    pre = listpath.rsplit("/", 1)[0] + "/"
    for a in soup.select(f'a[href^="{pre}"]'):
        h = a["href"].rstrip("/")
        h3 = a.find(["h3", "h2", "h4"])
        if not h3:
            continue
        t = h3.get_text(" ", strip=True)
        rest = [x for x in a.stripped_strings if x not in (t, "!")]
        out[h] = " ".join(rest)
    return out

def build_actus(d):
    subs = list_cards_from(d["soup"], d["path"])
    subs.update({k: v for k, v in list_cards_from(home_soup, d["path"]).items() if v})
    items = sorted(details_of(d["path"]), key=lambda x: dkey(x["date"]), reverse=True)
    for it in items:
        it["subtitle"] = subs.get(it["path"], "")
    cards = "".join(card(url_for(i["path"]), i["title"], i["img"], f'{ms("event")} {i["date"]}', i["subtitle"]) for i in items)
    return f'<div class="cards cards-3">{cards}</div>'

def ev_date(it):
    m = re.search(r"date_range\s*</span>\s*([^<]+)", it["html"])
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

def build_agenda(d):
    subs = list_cards_from(d["soup"], d["path"])
    subs.update({k: v for k, v in list_cards_from(home_soup, d["path"]).items() if v})
    items = details_of(d["path"])
    rows = []
    for it in items:
        it["subtitle"] = re.sub(r"^\d+\s+\S+\s*(\d{1,2}:\d{2} à \d{1,2}:\d{2})?\s*", "", subs.get(it["path"], ""))
        it["when"] = ev_date(it)
    for it in items:
        m = re.match(r"(\d{1,2})", it["when"])
        mo = next((i for i, x in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]) if x in it["when"].lower()), 0)
        day = m.group(1) if m else ""
        it["sort"] = (int(re.search(r"(\d{4})", it["when"]).group(1)) if re.search(r"(\d{4})", it["when"]) else 0, mo, int(day or 0))
        it["badge"] = (day.zfill(2), MONTHS[mo])
    items.sort(key=lambda x: x["sort"])
    for it in items:
        rows.append(f'''<a class="event" href="{url_for(it['path'])}">
<div class="event-date"><strong>{it['badge'][0]}</strong><span>{it['badge'][1]}</span></div>
{f'<img src="{esc(it["img"])}" alt="" loading="lazy">' if it['img'] else ''}
<div><p class="card-meta">{esc(it['cat'])} · {esc(it['when'])}</p><h3>{esc(it['title'])}</h3><p>{esc(excerpt(it['subtitle'], 160))}</p></div></a>''')
    return f'<div class="events">{"".join(rows)}</div>', items

def build_conseil(d):
    out = []
    for g in d["soup"].select(".main-content .contenu > .mb-3"):
        h = g.find("h2")
        cards = []
        for a in g.select("a[href]"):
            img = a.find("img")
            name = a.find("h3").get_text(" ", strip=True) if a.find("h3") else ""
            role = a.find("p").get_text(" ", strip=True) if a.find("p") else ""
            cards.append(f'''<a class="person" href="{url_for(a['href'])}"><img src="{esc(img['src'] if img else '')}" alt="" loading="lazy"><div><h3>{esc(name)}</h3><p>{esc(role)}</p></div></a>''')
        out.append(f'<h2>{esc(h.get_text(strip=True) if h else "")}</h2><div class="people">{"".join(cards)}</div>')
    return "".join(out)

def attachments(it):
    s = BeautifulSoup(it["html"], "html.parser")
    return [(a.get_text(" ", strip=True), a["href"]) for a in s.select("a.file")]

def build_cr(d):
    items = sorted(details_of(d["path"]), key=lambda x: dkey(x["date"]), reverse=True)
    by = {}
    for it in items:
        by.setdefault(it["date"][-4:] or "Autres", []).append(it)
    years = sorted(by, reverse=True)
    chips = "".join(f'<a class="chip" href="#y{y}">{y}</a>' for y in years)
    blocks = []
    for y in years:
        rows = []
        for it in by[y]:
            files = "".join(f'<a class="file" href="{esc(h)}" target="_blank" rel="noopener">{esc(t)}</a>' for t, h in attachments(it))
            rows.append(f'<tr><td class="nowrap">{it["date"]}</td><td><a href="{url_for(it["path"])}">{esc(it["title"])}</a></td><td>{files or "—"}</td></tr>')
        blocks.append(f'<h2 id="y{y}">{y}</h2><div class="table-wrap"><table><thead><tr><th>Date</th><th>Séance</th><th>Documents</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    return f'<div class="chips">{chips}</div>' + "".join(blocks)

JOURNAL_IMGS = {}
def build_journal(d):
    imgs = JOURNAL_IMGS
    for a in home_soup.select('a[href^="/fr/pb/731902/"]') + d["soup"].select('a[href^="/fr/pb/731902/"]'):
        i = a.find("img")
        if i:
            imgs[a["href"].rstrip("/")] = i["src"]
    items = details_of(d["path"])
    def num(x):
        m = re.search(r"(\d+)", x["title"]); return int(m.group(1)) if m else 0
    items.sort(key=num, reverse=True)
    cards = []
    for it in items:
        files = attachments(it)
        cards.append(f'''<div class="issue"><a href="{url_for(it['path'])}" class="issue-cover">{f'<img src="{esc(imgs.get(it["path"]) or it["img"] or "")}" alt="Couverture {esc(it["title"])}" loading="lazy">' if (imgs.get(it["path"]) or it["img"]) else ms("menu_book")}</a>
<h3>{esc(it['title'])}</h3><p class="card-meta">{it['date']}</p>{f'<a class="btn btn-small" href="{esc(files[0][1])}" target="_blank" rel="noopener">{ms("download")} Télécharger</a>' if files else ''}</div>''')
    return f'<div class="issues">{"".join(cards)}</div>'

def build_presse(d):
    items = sorted(details_of(d["path"]), key=lambda x: dkey(x["date"]), reverse=True)
    rows = []
    for it in items:
        src = BeautifulSoup(it["html"], "html.parser").find("p")
        rows.append(card(url_for(it["path"]), it["title"], None, f'{ms("newspaper")} {it["date"]}', src.get_text(" ", strip=True) if src else "", None, "card-row"))
    return f'<div class="list">{"".join(rows)}</div>'

def contact_bits(it):
    s = BeautifulSoup(it["html"], "html.parser")
    tel = s.select_one('a[href^="tel:"]')
    addr = None
    for sp in s.select("span.ms"):
        if sp.get_text() == "location_on":
            par = sp.parent
            addr = re.sub(r"\s+", " ", par.get_text(" ", strip=True).replace("location_on", "")).strip()
            break
    return (tel.get_text(strip=True) if tel else ""), addr or ""

def build_directory(d, with_filter=True):
    items = details_of(d["path"])
    items.sort(key=lambda x: x["title"].lower())
    cats = sorted({i["cat"] for i in items if i["cat"]})
    out = []
    if with_filter:
        out.append('<div class="filters"><div class="search-field small">' + ms("search") +
                   '<input type="search" placeholder="Filtrer par nom…" data-filter-input aria-label="Filtrer"></div>'
                   '<div class="chips"><button class="chip is-on" data-cat="">Toutes</button>' +
                   "".join(f'<button class="chip" data-cat="{esc(c)}">{esc(c)}</button>' for c in cats) + "</div></div>")
    cards = []
    for it in items:
        tel, addr = contact_bits(it)
        meta = esc(it["cat"])
        txt = " · ".join(x for x in [addr, tel] if x)
        c = card(url_for(it["path"]), it["title"], it["img"], meta, txt, None, "card-row")
        cards.append(c.replace('<a class="card', f'<a data-cat="{esc(it["cat"])}" data-name="{esc(it["title"].lower())}" class="card', 1))
    out.append(f'<div class="cards cards-2" data-filter-list>{"".join(cards)}</div>')
    return "".join(out)

def build_photos(d):
    items = sorted(details_of(d["path"]), key=lambda x: dkey(x["date"]), reverse=True)
    # cover images from list sidebar
    covers = {}
    for a in d["soup"].select("a[href]"):
        dv = a.find(style=re.compile("background-image"))
        if dv:
            m = re.search(r"url\(([^)]+)\)", dv["style"])
            covers[a["href"].rstrip("/")] = m.group(1).strip() if m else None
    return '<div class="cards cards-3">' + "".join(
        card(url_for(i["path"]), i["title"], covers.get(i["path"]) or i["img"], f'{ms("photo_library")} {i["date"]}') for i in items) + "</div>"

def build_videos(d):
    items = sorted(details_of(d["path"]), key=lambda x: dkey(x["date"]), reverse=True)
    out = []
    for i in items:
        m = re.search(r"embed/([\w-]+)", i["html"])
        img = f"https://img.youtube.com/vi/{m.group(1)}/hqdefault.jpg" if m else None
        out.append(card(url_for(i["path"]), i["title"], img, f'{ms("play_circle")} Vidéo', "", None, "card-video"))
    return '<div class="cards cards-3">' + "".join(out) + "</div>"

def build_guide(d):
    return '''<p>Retrouvez toutes les informations officielles et à jour sur vos droits et démarches, fournies par Service-Public.fr.</p>
<div class="cards cards-3">''' + \
        card("https://www.service-public.fr/particuliers/vosdroits", "Particuliers", None, "Service-Public.fr", "Retrouvez dans cet espace tous vos droits et démarches", "person") + \
        card("https://entreprendre.service-public.fr/", "Professionnels", None, "Service-Public.fr", "Retrouvez dans cet espace tous vos droits et démarches concernant votre entreprise", "work") + \
        card("https://www.service-public.fr/associations", "Associations", None, "Service-Public.fr", "Retrouvez dans cet espace tous vos droits et démarches concernant votre association", "groups") + \
        "</div>"

def build_contact(d):
    return f'''<div class="contact-grid">
<div class="box">
  <h2>Commune de Méteren</h2>
  <p>{ms("location_on")} Place César Herreman<br>59270 Méteren – France</p>
  <p>{ms("call")} <a href="tel:+33328490408">+33 3 28 49 04 08</a></p>
  <p>{ms("mail")} <a href="mailto:contact@ville-meteren.fr">contact@ville-meteren.fr</a></p>
  <h2>Horaires d'ouverture</h2>
  <p><strong>La mairie :</strong><br>Du lundi au samedi de 8h30 à 12h<br>Le mercredi de 8h30 à 12h et de 14h à 17h (sauf durant les vacances scolaires, fermé le mercredi après-midi)</p>
  <p><strong>Agence postale :</strong><br>Du lundi au vendredi de 8h30 à 11h45 et samedi de 9h à 11h45</p>
</div>
<form class="box form" data-mailto="contact@ville-meteren.fr">
  <h2>Contact par formulaire</h2>
  <label>Nom et prénom<input name="nom" required></label>
  <label>Adresse e-mail<input type="email" name="email" required></label>
  <label>Objet<input name="objet" required></label>
  <label>Message<textarea name="message" rows="6" required></textarea></label>
  <button class="btn btn-primary" type="submit">{ms("send")} Envoyer</button>
  <p class="hint">Prototype : l'envoi ouvre votre messagerie.</p>
</form>
</div>
<div class="map"><iframe title="Plan d'accès à la mairie de Méteren" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=2.6830%2C50.7360%2C2.7030%2C50.7450&amp;layer=mapnik&amp;marker=50.7406%2C2.6930"></iframe></div>'''

# ---------------------------------------------------------------- render pages
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + "/assets")
for f in ("style.css", "main.js"):
    shutil.copy(f"assets/{f}", f"{OUT}/assets/{f}")

agenda_items = []
for d in docs.values():
    sid = section_of(d)
    meta = ""
    body = ""
    lead = ""
    p = d["path"]
    if p == P["actus"]:
        body = build_actus(d)
    elif p == P["agenda"]:
        body, agenda_items = build_agenda(d)
    elif p == P["conseil"]:
        body = build_conseil(d)
    elif p == P["cr"]:
        body = build_cr(d)
    elif p == P["journal"]:
        lead = "Retrouvez tous les numéros de « Contact », le journal municipal de Méteren."
        body = build_journal(d)
    elif p == P["presse"]:
        body = build_presse(d)
    elif p == P["assos"]:
        body = build_directory(d)
    elif p == P["pros_sante"]:
        body = build_directory(d)
    elif p == P["photos"]:
        body = build_photos(d)
    elif p == P["videos"]:
        body = build_videos(d)
    elif p == P["guide"]:
        body = build_guide(d)
    elif p == P["contact"]:
        body = build_contact(d)
    else:
        body = f'<div class="prose">{d["html"]}</div>'
        if d["kind"] in ("nw", "pr", "pb", "rp", "pc") and d["date"]:
            meta = f'{ms("event")} {d["date"]}'
        if d["cat"]:
            meta = f'<span class="tag">{esc(d["cat"])}</span>' + (f" {meta}" if meta else "")
        kids = [c for c in d["children"] if c in docs]
        linked = set(re.findall(r'href="([^"]+)"', d["html"]))
        missing = [c for c in kids if url_for(c) not in linked]
        if missing:
            body += '<div class="cards cards-3 subpages">' + "".join(
                card(url_for(c), docs[c]["title"], docs[c]["img"], "", excerpt(docs[c]["text"], 110), None if docs[c]["img"] else "arrow_forward") for c in kids) + "</div>"
    d["list_html"] = body
    side = sidebar(sid, p) if sid else ""
    layout = f'<div class="wrap layout{" no-side" if not side else ""}">{side}<article class="content">{body}</article></div>'
    write(d["slug"] + ".html", page(d["title"], page_head(d["title"], breadcrumb_for(d), meta, lead) + layout, sid,
                                    excerpt(d["text"], 155)))

# ---------------------------------------------------------------- section landing pages
for sid, name, icon, desc, groups in NAV:
    blocks = []
    for gname, keys in groups:
        cs = []
        for k in keys:
            pth = P[k]
            if pth not in docs:
                continue
            dd = docs[pth]
            cs.append(card(url_for(pth), label(k), None, "", excerpt(dd["text"], 120), {
                "presentation": "info", "conseil": "groups", "cr": "gavel", "services": "badge", "interco": "hub",
                "syndicats": "handshake", "journal": "menu_book", "presse": "newspaper", "formalites": "assignment",
                "guide": "travel_explore", "faq": "help", "urbanisme": "architecture", "salles": "meeting_room",
                "portail": "family_restroom", "poste": "local_post_office", "enfance": "child_care", "cantine": "restaurant",
                "seniors": "elderly", "social": "volunteer_activism", "sante": "health_and_safety", "pros_sante": "medical_services",
                "cadre": "nature", "transports": "directions_bus", "citoyen": "diversity_3", "paroisse": "church",
                "numeros": "contact_phone", "agenda": "event", "assos": "groups_2", "equipements": "sports_soccer",
                "mediatheque": "local_library", "tourisme": "explore", "sentiers": "hiking", "photos": "photo_library",
                "videos": "smart_display", "artisans": "construction", "commercants": "storefront", "entreprises": "business",
                "agricoles": "agriculture", "marche": "shopping_basket", "actus": "campaign"}.get(k, "arrow_forward")))
        blocks.append(f'<h2>{esc(gname)}</h2><div class="cards cards-3">{"".join(cs)}</div>')
    write(f"{sid}.html", page(name, page_head(name, [(name, None)], "", esc(desc)) +
                              f'<div class="wrap section-page">{"".join(blocks)}</div>', sid, desc))

# ---------------------------------------------------------------- site map
sm = []
for sid, name, icon, desc, groups in NAV:
    def tree(pth):
        if pth not in docs:
            return ""
        kids = [c for c in docs[pth]["children"] if c in docs] if docs[pth]["kind"] == "rb" else []
        return f'<li><a href="{url_for(pth)}">{esc(docs[pth]["title"])}</a>' + (
            "<ul>" + "".join(tree(c) for c in kids) + "</ul>" if kids else "") + "</li>"
    sm.append(f'<div class="box"><h2><a href="{sid}.html">{esc(name)}</a></h2><ul>' +
              "".join(tree(P[k]) for _, ks in groups for k in ks) + "</ul></div>")
sm.append('<div class="box"><h2>Informations</h2><ul><li><a href="contact.html">Contact</a></li><li><a href="mentions-legales.html">Mentions légales</a></li><li><a href="confidentialite.html">Politique de confidentialité</a></li><li><a href="accessibilite.html">Accessibilité</a></li></ul></div>')
write("plan-du-site.html", page("Plan du site", page_head("Plan du site", [("Plan du site", None)]) +
                                f'<div class="wrap sitemap">{"".join(sm)}</div>'))

# ---------------------------------------------------------------- home
actus = sorted(details_of(P["actus"]), key=lambda x: dkey(x["date"]), reverse=True)
journal = docs[P["journal"]]
jitems = sorted(details_of(P["journal"]), key=lambda x: int(re.search(r"(\d+)", x["title"]).group(1)), reverse=True)
jimgs = {**JOURNAL_IMGS, **{a["href"].rstrip("/"): a.find("img")["src"] for a in home_soup.select('a[href^="/fr/pb/731902/"]') if a.find("img")}}
quick = [("contact_phone", "Numéros utiles", "numeros"), ("family_restroom", "Portail Famille", "portail"),
         ("restaurant", "Menus cantine", "cantine"), ("architecture", "Urbanisme", "urbanisme"),
         ("assignment", "Formalités", "formalites"), ("event", "Agenda", "agenda"),
         ("groups_2", "Associations", "assos"), ("meeting_room", "Salles municipales", "salles")]
quick_html = "".join(f'<a class="quick" href="{url_for(P[k])}">{ms(i)}<span>{t}</span></a>' for i, t, k in quick)
news_html = "".join(card(url_for(i["path"]), i["title"], i["img"], f'{ms("event")} {i["date"]}', excerpt(i.get("subtitle", ""), 110)) for i in actus[:3])
news_more = "".join(f'<li><a href="{url_for(i["path"])}"><span class="card-meta">{i["date"]}</span>{esc(i["title"])}</a></li>' for i in actus[3:7])
ev_html = "".join(f'''<a class="event compact" href="{url_for(it['path'])}"><div class="event-date"><strong>{it['badge'][0]}</strong><span>{it['badge'][1]}</span></div><div><h3>{esc(it['title'])}</h3><p>{esc(excerpt(it['subtitle'], 80))}</p></div></a>''' for it in agenda_items[:3])
discover = [("presentation", "Découvrir Méteren", "Histoire, patrimoine et chiffres clés de la commune."),
            ("tourisme", "Tourisme", "Gîtes, chambres d'hôtes et étang des 4 fils Aymon."),
            ("sentiers", "Sentiers de randonnée", "Partez à la découverte des Monts de Flandre."),
            ("equipements", "Équipements", "Salle de sport, terrain synthétique, city stade…")]
disc_html = "".join(card(url_for(P[k]), t, docs[P[k]]["img"], "", x) for k, t, x in discover)
latest = jitems[0]
latest_files = attachments(latest)
home = f'''<section class="hero" style="--hero:url('{HERO}')">
  <div class="wrap hero-inner">
    <p class="hero-kicker">Bienvenue à</p>
    <h1>Méteren</h1>
    <p class="hero-lead">Petite bourgade tranquille des Flandres intérieures, au cœur des Monts.</p>
    <button class="hero-search" data-open-search>{ms("search")}<span>Que recherchez-vous ? Démarche, service, association…</span></button>
  </div>
</section>
<section class="wrap quick-grid" aria-label="Accès rapides">{quick_html}</section>

<section class="wrap home-split">
  <div>
    <div class="section-title"><h2>Actualités</h2><a href="actualites.html">Toutes les actualités {ms("arrow_forward")}</a></div>
    <div class="cards cards-3">{news_html}</div>
    <ul class="news-list">{news_more}</ul>
  </div>
  <aside>
    <div class="section-title"><h2>Agenda</h2><a href="agenda.html">Tout l'agenda {ms("arrow_forward")}</a></div>
    <div class="events">{ev_html}</div>
  </aside>
</section>

<section class="band">
  <div class="wrap journal-band">
    <a class="journal-cover" href="{url_for(latest['path'])}"><img src="{esc(jimgs.get(latest['path']) or latest['img'] or '')}" alt="Couverture du {esc(latest['title'])}"></a>
    <div>
      <p class="kicker">Journal municipal</p>
      <h2>« Contact », le journal de Méteren</h2>
      <p>Le dernier numéro ({esc(latest['title'])}) est disponible. Retrouvez toutes les informations de la vie communale.</p>
      <p>{f'<a class="btn btn-primary" href="{esc(latest_files[0][1])}" target="_blank" rel="noopener">{ms("download")} Lire le dernier numéro</a>' if latest_files else ''} <a class="btn btn-ghost-dark" href="journal-municipal.html">Tous les numéros</a></p>
    </div>
  </div>
</section>

<section class="wrap">
  <div class="section-title"><h2>Découvrir Méteren</h2></div>
  <div class="cards cards-4">{disc_html}</div>
</section>

<section class="wrap infos">
  <div class="box">
    <h2>{ms("account_balance")} Mairie de Méteren</h2>
    <p>Place César Herreman<br>59270 Méteren</p>
    <p><a href="tel:+33328490408">{ms("call")} 03 28 49 04 08</a><br><a href="mailto:contact@ville-meteren.fr">{ms("mail")} contact@ville-meteren.fr</a></p>
    <h3>Horaires de la mairie</h3>
    <p>Du lundi au samedi de 8h30 à 12h<br>Le mercredi de 8h30 à 12h et de 14h à 17h<br><small>(sauf vacances scolaires : fermé le mercredi après-midi)</small></p>
    <h3>Agence postale</h3>
    <p>Du lundi au vendredi de 8h30 à 11h45<br>Samedi de 9h à 11h45</p>
    <a class="btn btn-primary" href="contact.html">Nous contacter</a>
  </div>
  <div class="map"><iframe title="Plan d'accès à la mairie de Méteren" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=2.6830%2C50.7360%2C2.7030%2C50.7450&amp;layer=mapnik&amp;marker=50.7406%2C2.6930"></iframe></div>
</section>'''
write("index.html", page("Méteren", home, None, "", "home"))

# ---------------------------------------------------------------- search index
idx = []
for d in docs.values():
    sid = section_of(d)
    meta = sec_meta(sid)
    idx.append({"t": d["title"], "u": url_for(d["path"]), "s": meta[1] if meta else "",
                "x": (text_of(d["list_html"]) if d["is_list"] else d["text"])[:1500]})
for sid, name, *_ in NAV:
    idx.append({"t": name, "u": f"{sid}.html", "s": "Rubrique", "x": ""})
with open(f"{OUT}/assets/search-index.js", "w") as f:
    f.write(("window.SEARCH_INDEX=" + json.dumps(idx, ensure_ascii=False) + ";").replace("file_download ", ""))

print("pages:", len(docs) + len(NAV) + 2)
