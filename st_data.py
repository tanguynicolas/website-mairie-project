"""Extraction des données de l'accueil v1 -> dict réutilisé par les 5 maquettes."""
import re
from bs4 import BeautifulSoup, NavigableString

P = "../site/"


def fix(h):
    if not h or h.startswith(("http", "mailto:", "tel:", "#")):
        return h
    return P + h


def first_text(el):
    for c in el.children:
        if isinstance(c, NavigableString) and c.strip():
            return c.strip()
    return el.get_text(" ", strip=True)


def last_text(el):
    t = [c.strip() for c in el.strings if c.strip()]
    return t[-1] if t else ""


def load():
    s = BeautifulSoup(open("site/index.html", encoding="utf-8").read(), "html.parser")
    d = {}
    d["logo"] = s.select_one(".site-header .brand img")["src"]
    m = re.search(r"url\('([^']+)'\)", s.select_one(".hero").get("style", ""))
    d["hero"] = m.group(1) if m else ""
    nav = []
    for li in s.select(".main-nav > ul > li"):
        btn = li.select_one(".nav-btn")
        intro = li.select_one(".mega-intro")
        it = {"label": first_text(btn), "href": "", "icon": "", "desc": "", "cols": []}
        if intro:
            it["href"] = fix(intro.get("href"))
            ic = intro.select_one(".ms")
            it["icon"] = ic.get_text(strip=True) if ic else ""
            sp = intro.find_all("span", recursive=False)
            it["desc"] = sp[1].get_text(" ", strip=True) if len(sp) > 1 else ""
        for col in li.select(".mega-col"):
            t = col.select_one(".mega-title")
            it["cols"].append({
                "title": t.get_text(" ", strip=True) if t else "",
                "links": [(a.get_text(" ", strip=True), fix(a.get("href"))) for a in col.select("a")],
            })
        if not it["href"]:
            a = li.select_one("a")
            it["href"] = fix(a.get("href")) if a else "#"
        nav.append(it)
    d["nav"] = nav
    d["quick"] = []
    for q in s.select(".quick"):
        sp = q.find_all("span", recursive=False)
        d["quick"].append({
            "icon": q.select_one(".ms").get_text(strip=True),
            "label": (sp[1] if len(sp) > 1 else q).get_text(" ", strip=True),
            "href": fix(q.get("href")),
        })
    def card(c):
        img = c.select_one("img")
        a = c if c.name == "a" else c.select_one("a")
        meta = c.select_one(".card-meta")
        p = c.select_one("p:not(.card-meta)")
        return {
            "img": img["src"] if img else "",
            "date": last_text(meta) if meta else "",
            "title": c.select_one("h3").get_text(" ", strip=True),
            "desc": p.get_text(" ", strip=True) if p else "",
            "href": fix(a.get("href")) if a else "#",
        }
    d["news"] = [card(c) for c in s.select(".home-split .card")]
    d["briefs"] = [{"date": a.select_one(".card-meta").get_text(" ", strip=True) if a.select_one(".card-meta") else "",
                    "title": last_text(a), "href": fix(a.get("href"))} for a in s.select(".news-list a")]
    d["events"] = []
    for e in s.select(".events .event"):
        a = e if e.name == "a" else e.select_one("a")
        p = e.select_one("p")
        d["events"].append({
            "day": e.select_one(".event-date strong").get_text(strip=True),
            "month": e.select_one(".event-date span").get_text(strip=True),
            "title": e.select_one("h3").get_text(" ", strip=True),
            "desc": p.get_text(" ", strip=True) if p else "",
            "href": fix(a.get("href")) if a else "#",
        })
    jb = s.select_one(".journal-band")
    ji = jb.select_one("img")
    ps = jb.select("p")
    d["journal"] = {
        "img": ji["src"],
        "title": ji.get("alt", "").replace("Couverture du ", "").strip(),
        "href": fix(jb.select_one(".journal-cover").get("href")),
        "pdf": fix(jb.select_one(".btn-primary").get("href")),
        "text": ps[1].get_text(" ", strip=True) if len(ps) > 1 else (ps[0].get_text(" ", strip=True) if ps else ""),
    }
    d["discover"] = [card(c) for c in s.select(".cards-4 .card")]
    d["ext"] = [(a.get_text(" ", strip=True), a.get("href")) for a in s.select("ul.plain a")]
    d["labels"] = [(li.select_one(".ms").get_text(strip=True) if li.select_one(".ms") else "", last_text(li)) for li in s.select("ul.labels li")]
    d["legal"] = [(a.get_text(" ", strip=True), fix(a.get("href"))) for a in s.select(".footer-bottom nav a")]
    fb = s.select_one('a[href*="facebook"]')
    d["facebook"] = fb.get("href") if fb else "#"
    return d


if __name__ == "__main__":
    import json
    d = load()
    print(json.dumps({k: (v if k not in ("nav",) else [(n["label"], n["href"], n["icon"], len(n["cols"])) for n in v]) for k, v in d.items()}, ensure_ascii=False, indent=1)[:6000])
