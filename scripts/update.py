#!/usr/bin/env python3
"""Holt die Fundtiere der Stadt Wien (Open Data, CC BY 4.0) und schreibt data.json + Fotos.

Laeuft automatisch ueber GitHub Actions. Nur Python-Standardbibliothek.
Sicherheitsnetz: Liefert der Feed nichts oder viel weniger als vorher,
bleibt die alte data.json stehen und der Lauf schlaegt fehl (GitHub schickt dann eine E-Mail).
"""
import json, os, re, sys, time, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED = "https://www.wien.gv.at/fundundvergabetiere/internet/rssfeed.xml"
BASE = "https://www.wien.gv.at"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
PHOTOS = os.path.join(ROOT, "photos")
UA = {"User-Agent": "tiervermisst-updater/1.0 (gemeinnuetzige Fundtier-Suche)"}

NS = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "vie": "http://www.wien.gv.at/vierss",
    "cal": "http://www.w3.org/2002/12/cal#",
    "vcard": "http://www.w3.org/2006/vcard/ns",
    "media": "http://search.yahoo.com/mrss/",
}

BIRDS = ("sittich", "vogel", "taube", "fink", "papagei", "huhn", "hahn", "ente", "gans", "wachtel",
         "kanarie", "kakadu", "agapornid", "amsel", "star", "zebrafink", "ara", "pfau")
REPTILES = ("schildkr", "gecko", "schlange", "echse", "leguan", "agame", "python", "natter", "chamäleon", "chamaeleon", "frosch", "kröte")


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def text(el, path):
    found = el.find(path, NS)
    return (found.text or "").strip() if found is not None and found.text else ""


def kind_of(category, title):
    t = title.lower()
    if category.startswith("01"):
        return "h"
    if category.startswith("02"):
        return "k"
    if any(w in t for w in REPTILES):
        return "r"
    if any(w in t for w in BIRDS):
        return "v"
    return "n"


def tel_href(tel):
    m = re.search(r"\+?\d[\d\s/\-]{5,}\d", tel)
    if not m:
        return ""
    digits = re.sub(r"[^\d+]", "", m.group(0))
    if digits.startswith("0"):
        digits = "+43" + digits[1:]
    return digits


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    animals = []
    for it in root.iter("item"):
        fid = text(it, "guid")
        if not fid.isdigit():
            continue
        title = text(it, "title") or "Tier"
        addr = text(it, "cal:location/vcard:street-address")
        m = re.match(r"\s*(\d{1,2})\.\s*,?\s*(.*)", addr)
        bez = int(m.group(1)) if m and 1 <= int(m.group(1)) <= 23 else 0
        street = (m.group(2) if m else addr).strip()
        thumb = it.find("media:thumbnail", NS)
        thumb_url = thumb.get("url", "") if thumb is not None else ""
        tel = text(it, "cal:organizer/vcard:tel")
        sex = text(it, "vie:geschlecht").lower()
        animals.append({
            "id": int(fid),
            "date": text(it, "dc:date"),
            "title": title,
            "kind": kind_of(text(it, "description"), title),
            "born": text(it, "vie:geburtsjahr"),
            "sex": "m" if sex.startswith("m") else "w" if sex.startswith("w") else "u",
            "color": text(it, "vie:farbe"),
            "mix": bool(text(it, "vie:mischling")),
            "bez": bez,
            "street": street,
            "org": {
                "name": text(it, "cal:organizer/vcard:fn"),
                "tel": tel,
                "telHref": tel_href(tel),
                "mail": text(it, "cal:organizer/vcard:email"),
            },
            "photoUrl": (BASE + thumb_url) if thumb_url.startswith("/") else thumb_url,
            "img": None,
        })
    return animals


def sync_photos(animals):
    os.makedirs(PHOTOS, exist_ok=True)
    keep = set()
    for a in animals:
        if not a["photoUrl"]:
            continue
        name = f"{a['id']}.jpg"
        path = os.path.join(PHOTOS, name)
        keep.add(name)
        if not os.path.exists(path):
            try:
                body, ctype = fetch(a["photoUrl"])
                if not ctype.startswith("image/") or len(body) < 500:
                    raise ValueError("kein Bild")
                with open(path, "wb") as f:
                    f.write(body)
                time.sleep(0.3)  # Server der Stadt schonen
            except Exception as e:
                print(f"Foto {a['id']} nicht geladen: {e}", file=sys.stderr)
                continue
        a["img"] = f"photos/{name}"
    for old in os.listdir(PHOTOS):
        if old.endswith(".jpg") and old not in keep:
            os.remove(os.path.join(PHOTOS, old))


def main():
    old_count = 0
    if os.path.exists(DATA):
        try:
            with open(DATA, encoding="utf-8") as f:
                old_count = len(json.load(f).get("animals", []))
        except Exception:
            pass
    body, _ = fetch(FEED)
    animals = parse(body)
    if not animals:
        sys.exit("Feed leer oder unlesbar – alte Daten bleiben bestehen.")
    if old_count >= 40 and len(animals) < old_count * 0.4:
        sys.exit(f"Verdaechtig wenige Tiere ({len(animals)} statt {old_count}) – alte Daten bleiben bestehen.")
    sync_photos(animals)
    animals.sort(key=lambda a: (a["date"], a["id"]), reverse=True)
    out = {
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "Stadt Wien – data.gv.at, Lizenz CC BY 4.0",
        "animals": animals,
    }
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(animals)} Tiere gespeichert.")


if __name__ == "__main__":
    main()
