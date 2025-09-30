import json
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.finrent.it/"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/139.0.0.0 Safari/537.36")
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.Session()

def get_all_image_urls(sd, detail_url):
    """
    Estrae tutti gli URL delle immagini valide dal container,
    filtrando cloni, timbri ed eliminando duplicati.
    """
    image_urls = []
    seen_urls = set()

    # Seleziona tutti gli <img> dentro il contenitore specificato
    all_imgs = sd.select("div.auto-slider-container img")

    def get_img_src(tag):
        # Prova vari attributi per il lazy loading
        for attr in ("src", "data-src", "data-lazy", "data-original"):
            val = tag.get(attr)
            if val and val.strip():
                return val.strip()
        srcset = tag.get("srcset")
        if srcset:
            return srcset.split(",")[0].strip().split()[0]
        return None

    for img in all_imgs:
        # Ignora le immagini decorative (timbri, etichette)
        if 'timbro' in img.get('class', []) or img.find_parent(class_='etichetta'):
            continue
        
        # Ignora le immagini dentro i cloni dello slider
        if img.find_parent(class_='slick-cloned'):
            continue

        src = get_img_src(img)
        if src:
            absolute_url = urljoin(detail_url, src)
            # Aggiungi l'URL solo se non è già presente per evitare duplicati
            if absolute_url not in seen_urls:
                 image_urls.append(absolute_url)
                 seen_urls.add(absolute_url)

    # Fallback se non si trovano immagini
    if not image_urls:
        og = sd.select_one("meta[property='og:image'][content]")
        if og and og.get("content"):
            image_urls.append(urljoin(detail_url, og["content"].strip()))

    return image_urls

# --- Logica principale dello scraper (invariata) ---

r = s.get(BASE, headers=HEADERS, timeout=20, verify=False)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

first_section = soup.find("section", class_="fascia-gallery-auto")
boxes = []
if first_section:
    boxes = first_section.select(".box-gallery-auto")

items = []
for box in boxes:
    a_tag = box.select_one("a[href]")
    if not a_tag:
        continue
    detail_url = urljoin(BASE, a_tag.get("href", ""))

    try:
        rd = s.get(detail_url, headers=HEADERS, timeout=20, verify=False)
        rd.raise_for_status()
        sd = BeautifulSoup(rd.text, "html.parser")

        # Estrazione altri dati
        title_span = sd.select_one("h1 span.heading.heading__3")
        nome_macchina = title_span.get_text(strip=True) if title_span else None

        small_span = sd.select_one("h1 span.small")
        motore, potenza_cambio = None, None
        if small_span:
            strong = small_span.find("strong")
            if strong:
                potenza_cambio = strong.get_text(strip=True)
                full_text = small_span.get_text(" ", strip=True)
                motore = full_text.replace(potenza_cambio, "").strip(" -–—")
            else:
                parts = list(small_span.stripped_strings)
                motore = parts[0] if parts else None
                potenza_cambio = parts[1] if len(parts) > 1 else None

        # Array con tutte le immagini trovate
        image_urls = get_all_image_urls(sd, detail_url)

        def get_field(field_id):
            el = sd.find(id=field_id)
            return el.get_text(strip=True) if el else None

        items.append({
            "nomeMacchina": nome_macchina,
            "motore": motore,
            "potenzaCambio": potenza_cambio,
            "imageUrls": image_urls,
            "prezzo": get_field("qprice"),
            "prezzoIva": get_field("qpriceiva"),
            "mesi": get_field("qmesi"),
            "kmTotali": get_field("qkmTotali"),
            "anticipo": get_field("anticipo"),
        })

    except requests.RequestException as e:
        print(f"Errore durante l'elaborazione di {detail_url}: {e}")
        continue

print(json.dumps(items, ensure_ascii=False, indent=2))
