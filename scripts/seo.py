#!/usr/bin/env python3
"""Schreibt die aktuellen Fundtiere als normalen HTML-Text in index.html
(fuer Suchmaschinen) und erzeugt sitemap.xml.
Laeuft nur beim Veroeffentlichen; index.html im Repo bleibt unveraendert.
Bei einem Fehler bleibt die Seite einfach wie bisher."""
import json, html, re, datetime
from zoneinfo import ZoneInfo

KIND = {"k": "Katze", "h": "Hund", "v": "Vogel", "n": "Kleintier", "r": "Reptil"}
SEX = {"m": "männlich", "w": "weiblich", "u": "Geschlecht unbekannt"}
BEZ = ["", "Innere Stadt", "Leopoldstadt", "Landstraße", "Wieden", "Margareten", "Mariahilf",
       "Neubau", "Josefstadt", "Alsergrund", "Favoriten", "Simmering", "Meidling", "Hietzing",
       "Penzing", "Rudolfsheim-Fünfhaus", "Ottakring", "Hernals", "Währing", "Döbling",
       "Brigittenau", "Floridsdorf", "Donaustadt", "Liesing"]
MON = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
       "September", "Oktober", "November", "Dezember"]
e = lambda x: html.escape(str(x or ""), quote=True)


def datum(iso):
    try:
        y, m, d = map(int, iso.split("-"))
        return f"{d}. {MON[m-1]} {y}"
    except Exception:
        return e(iso)


def card(a):
    o = a.get("org") or {}
    kind = KIND.get(a.get("kind"), "Tier")
    try:
        bez = int(a.get("bez") or 0)
    except ValueError:
        bez = 0
    ort = f"{bez}. Bezirk, {BEZ[bez]}" if 0 < bez < len(BEZ) else "Wien"
    facts = [SEX.get(a.get("sex"), "")]
    if a.get("born"):
        facts.append("Geburtsjahr " + str(a["born"]))
    if a.get("mix"):
        facts.append("Mischling")
    url = a.get("img") or a.get("photoUrl") or ""
    farbe = a.get("color") or kind
    photo = (f'<figure class="photo"><img src="{e(url)}" alt="Foto: {e(a.get("title"))}, {e(farbe)}, gefunden in {e(ort)}" loading="lazy"></figure>'
             if url else '<figure class="photo none"><span class="fb"><span>Kein Foto vorhanden</span></span></figure>')
    org = re.sub(r"\s+", " ", o.get("name") or "Fundservice der Stadt Wien")
    tel = o.get("tel") or "+43 1 4000-8060"
    telh = o.get("telHref") or "+43140008060"
    return (f'<article class="card" id="f-{e(a.get("id"))}"><span class="tag" title="Fund-ID">{e(a.get("id"))}</span>{photo}'
            f'<span class="kindline">{kind}</span><h2>{e(a.get("title"))}</h2>'
            f'<div class="colors"><span>{e(a.get("color") or "Farbe nicht angegeben")}</span></div>'
            f'<div class="facts">{"".join(f"<span class=fact>{e(x)}</span>" for x in facts if x)}</div>'
            f'<dl><dt>Gefunden</dt><dd>{datum(a.get("date"))}</dd>'
            f'<dt>Fundort</dt><dd>{e(a.get("street"))}<br>{e(ort)}</dd></dl>'
            f'<div class="contact"><div class="org">{e(org)}</div><div><a href="tel:{e(telh)}">{e(tel)}</a></div></div></article>')


def main():
    d = json.load(open("data.json", encoding="utf-8"))
    animals = sorted(d.get("animals") or [], key=lambda a: str(a.get("date")), reverse=True)
    s = open("index.html", encoding="utf-8").read()
    if "<!--SSR-->" not in s:
        print("Kein SSR-Platzhalter in index.html, nichts zu tun.")
    else:
        s = re.sub(r"<!--SSR-->.*?<!--/SSR-->",
                   lambda m: "<!--SSR-->" + "".join(card(a) for a in animals) + "<!--/SSR-->", s, flags=re.S)
        try:
            up = datetime.datetime.fromisoformat(d["updated"]).astimezone(ZoneInfo("Europe/Vienna"))
            stand = f"{len(animals)} Fundtiere, Stand {datum(up.date().isoformat())}."
            s = s.replace('<strong id="stand">Daten werden geladen …</strong>', f'<strong id="stand">{stand}</strong>')
        except Exception:
            pass
        open("index.html", "w", encoding="utf-8").write(s)
        print(f"{len(animals)} Tiere in index.html geschrieben.")
    day = str(d.get("updated", ""))[:10] or datetime.date.today().isoformat()
    urls = [("https://tiergefunden.at/", day, "hourly", "1.0"),
            ("https://tiergefunden.at/impressum.html", None, "yearly", "0.2"),
            ("https://tiergefunden.at/datenschutz.html", None, "yearly", "0.2")]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lm, cf, pr in urls:
        xml.append(f"  <url><loc>{loc}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") +
                   f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
    xml.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(xml) + "\n")
    print("sitemap.xml geschrieben.")


if __name__ == "__main__":
    main()
