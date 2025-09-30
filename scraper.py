import json
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.finrent.it/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.Session()

r = s.get(BASE, headers=HEADERS, timeout=20, verify=False)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

items = []
for box in soup.select(".box-gallery-auto"):
    a = box.select_one("a[href]")
    if not a:
        continue
    detail_url = urljoin(BASE, a.get("href", ""))
    try:
        rd = s.get(detail_url, headers=HEADERS, timeout=20, verify=False)
        rd.raise_for_status()
        sd = BeautifulSoup(rd.text, "html.parser")

        # nomeMacchina
        title_span = sd.select_one("h1 span.heading.heading__3")
        nome_macchina = title_span.get_text(strip=True) if title_span else None

        # motore e potenzaCambio dalla seconda riga
        small_span = sd.select_one("h1 span.small")
        motore = None
        potenza_cambio = None
        if small_span:
            strong = small_span.find("strong")
            if strong:
                potenza_cambio = strong.get_text(strip=True)
                # Testo completo della riga, poi rimuovi la parte strong
                full = small_span.get_text(" ", strip=True)
                motore = full.replace(potenza_cambio, "").strip(" -–—")
            else:
                # Se non c'è <strong>, prova a dividere i pezzi disponibili
                parts = list(small_span.stripped_strings)
                if parts:
                    motore = parts[0]
                if len(parts) > 1:
                    potenza_cambio = parts[-1]

        # campi già richiesti
        def get(id_):
            el = sd.find(id=id_)
            return el.get_text(strip=True) if el else None

        items.append({
            "nomeMacchina": nome_macchina,
            "motore": motore,
            "potenzaCambio": potenza_cambio,
            "prezzo":    get("qprice"),
            "prezzoIva": get("qpriceiva"),
            "mesi":      get("qmesi"),
            "kmTotali":  get("qkmTotali"),
            "anticipo":  get("qanticipo"),
        })

    except requests.RequestException:
        continue

print(json.dumps(items, ensure_ascii=False, indent=2))
