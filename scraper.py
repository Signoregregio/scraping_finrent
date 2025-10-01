import json
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, quote

def esegui_scraping():
    """
    Esegue lo scraping delle offerte di auto dal sito Finrent
    e restituisce i dati come una lista di dizionari.
    """
    # --- Configurazione Iniziale ---
    BASE = "https://www.finrent.it/"
    HEADERS = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/139.0.0.0 Safari/537.36")
    }

    # Disabilita gli avvisi SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    s = requests.Session()

    # --- Funzioni Helper (invariate) ---
    def get_safe_img_src(tag):
        if not tag: return None
        src = None
        for attr in ("src", "data-src", "data-lazy", "data-original"):
            val = tag.get(attr)
            if val and val.strip():
                src = val.strip()
                break
        if not src:
            srcset = tag.get("srcset")
            if srcset:
                src = srcset.split(",")[0].strip().split()[0]
        if not src: return None
        parsed_url = urlparse(src)
        safe_path = quote(parsed_url.path)
        return urlunparse(parsed_url._replace(path=safe_path))

    def get_all_image_urls(sd, detail_url):
        image_urls, seen_urls = [], set()
        all_imgs = sd.select("div.auto-slider-container img")
        for img in all_imgs:
            if 'timbro' in img.get('class', []) or img.find_parent(class_='etichetta') or img.find_parent(class_='slick-cloned'):
                continue
            src = get_safe_img_src(img)
            if src:
                absolute_url = urljoin(detail_url, src)
                if absolute_url not in seen_urls:
                    image_urls.append(absolute_url)
                    seen_urls.add(absolute_url)
        return image_urls

    # --- Logica Principale dello Scraper ---
    try:
        r = s.get(BASE, headers=HEADERS, timeout=20, verify=False)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
    except requests.RequestException as e:
        print(f"Errore nel caricare la pagina principale: {e}")
        return [] # Restituisce una lista vuota in caso di errore

    first_section = soup.find("section", class_="fascia-gallery-auto")
    boxes = first_section.select(".box-gallery-auto") if first_section else []

    items = []
    for box in boxes:
        a_tag = box.select_one("a[href]")
        if not a_tag: continue
        detail_url = urljoin(BASE, a_tag.get("href", ""))

        try:
            rd = s.get(detail_url, headers=HEADERS, timeout=20, verify=False)
            rd.raise_for_status()
            sd = BeautifulSoup(rd.text, "html.parser")

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
            
            timbro_img = sd.select_one("div.auto-slider-container img.timbro")
            timbro_src = get_safe_img_src(timbro_img)
            timbro_url = urljoin(detail_url, timbro_src) if timbro_src else None
            
            etichetta = None
            for etichetta_div in sd.select("div.auto-slider-container div.etichetta"):
                label_span = etichetta_div.find("span")
                if label_span and label_span.get_text(strip=True):
                    icon_img = etichetta_div.find("img")
                    icon_src = get_safe_img_src(icon_img)
                    if icon_src:
                        etichetta = {
                            "label": label_span.get_text(strip=True),
                            "icon": urljoin(detail_url, icon_src)
                        }
                        break

            image_urls = get_all_image_urls(sd, detail_url)
            def get_field(field_id):
                el = sd.find(id=field_id)
                return el.get_text(strip=True) if el else None

            items.append({
                "nomeMacchina": nome_macchina,
                "motore": motore,
                "potenzaCambio": potenza_cambio,
                "imageUrls": image_urls,
                "timbroUrl": timbro_url,
                "etichetta": etichetta,
                "prezzo": get_field("qprice"),
                "prezzoIva": get_field("qpriceiva"),
                "mesi": get_field("qmesi"),
                "kmTotali": get_field("qkmTotali"),
                "anticipo": get_field("qanticipo"),
            })
        except requests.RequestException as e:
            print(f"Errore durante l'elaborazione di {detail_url}: {e}")
            continue

    # La modifica chiave: restituisci la lista di items
    return items

# Opzionale: per testare lo script da solo
if __name__ == '__main__':
    dati_auto = esegui_scraping()
    print(json.dumps(dati_auto, indent=2, ensure_ascii=False))

