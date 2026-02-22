import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from pathlib import Path

from config import BASE_URL, TARGET_CATEGORY, OUTPUT_FILE, REQUEST_DELAY
from parser import parse_books_from_page, get_category_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def fetch(url: str) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0 (books-scraper/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        log.error(f"Error al acceder a {url}: {e}")
        raise


def scrape_home(limit: int = 20) -> list[dict]:
    log.info(f"Extrayendo {limit} libros de la página principal...")
    soup = fetch(BASE_URL)
    books = parse_books_from_page(soup)
    log.info(f"  → {len(books[:limit])} libros extraídos")
    return books[:limit]


def scrape_category(category: str, limit: int = 20) -> list[dict]:
    log.info(f"Buscando categoría '{category}'...")

    soup = fetch(BASE_URL)
    category_url = get_category_url(soup, category)

    if not category_url:
        log.warning(f"'{category}' no encontrada. Categorías disponibles:")
        for a in soup.select("ul.nav-list ul li a"):
            log.info(f"    • {a.text.strip()}")
        raise ValueError(f"Categoría '{category}' no encontrada.")

    log.info(f"  → URL: {category_url}")
    time.sleep(REQUEST_DELAY)

    books = []
    current_url = category_url

    while current_url and len(books) < limit:
        soup = fetch(current_url)
        page_books = parse_books_from_page(soup, category=category)
        books.extend(page_books)
        log.info(f"  → {len(page_books)} libros en esta página (total: {len(books)})")

        next_btn = soup.select_one("li.next a")
        if next_btn:
            base = current_url.rsplit("/", 1)[0]
            current_url = f"{base}/{next_btn['href']}"
            time.sleep(REQUEST_DELAY)
        else:
            current_url = None

    return books[:limit]


def save_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"Guardado en: {path}")


def main():
    log.info("=== Iniciando scraper ===")

    home_books = scrape_home(limit=20)
    time.sleep(REQUEST_DELAY)
    category_books = scrape_category(TARGET_CATEGORY, limit=20)

    output = {
        "fuente": BASE_URL,
        "total_libros": len(home_books) + len(category_books),
        "home": {
            "descripcion": "Primeros 20 libros de la página principal",
            "cantidad": len(home_books),
            "libros": home_books,
        },
        "categoria": {
            "nombre": TARGET_CATEGORY,
            "descripcion": f"Primeros 20 libros de la categoría {TARGET_CATEGORY}",
            "cantidad": len(category_books),
            "libros": category_books,
        },
    }

    save_json(output, OUTPUT_FILE)
    log.info(f"=== Completado: {output['total_libros']} libros extraídos ===")


if __name__ == "__main__":
    main()