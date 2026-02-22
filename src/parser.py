from bs4 import BeautifulSoup, Tag

STAR_MAP = {
    "one":   1,
    "two":   2,
    "three": 3,
    "four":  4,
    "five":  5,
}


def parse_books_from_page(soup: BeautifulSoup, category: str = None) -> list[dict]:
    articles = soup.select("article.product_pod")
    books = []

    for article in articles:
        book = _parse_single_book(article)
        if category:
            book["categoria"] = category
        books.append(book)

    return books


def _parse_single_book(article: Tag) -> dict:
    return {
        "titulo":       _parse_title(article),
        "precio":       _parse_price(article),
        "disponible":   _parse_availability(article),
        "calificacion": _parse_rating(article),
    }


def _parse_title(article: Tag) -> str:
    tag = article.select_one("h3 a")
    return tag["title"].strip() if tag else "Sin título"


def _parse_price(article: Tag) -> float:
    tag = article.select_one("p.price_color")
    if not tag:
        return 0.0
    raw = tag.text.strip()
    cleaned = "".join(c for c in raw if c.isdigit() or c == ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_availability(article: Tag) -> bool:
    tag = article.select_one("p.availability")
    if not tag:
        return False
    return "in stock" in tag.text.strip().lower()


def _parse_rating(article: Tag) -> int:
    tag = article.select_one("p.star-rating")
    if not tag:
        return 0
    classes = tag.get("class", [])
    for cls in classes:
        if cls.lower() in STAR_MAP:
            return STAR_MAP[cls.lower()]
    return 0


def get_category_url(soup: BeautifulSoup, category_name: str) -> str | None:
    links = soup.select("ul.nav-list ul li a")
    target = category_name.strip().lower()

    for link in links:
        if link.text.strip().lower() == target:
            href = link["href"]
            from config import BASE_URL
            return BASE_URL.rstrip("/") + "/" + href.lstrip("/")

    return None