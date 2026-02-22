from pathlib import Path

BASE_URL = "http://books.toscrape.com/"
TARGET_CATEGORY = "Mystery"
OUTPUT_FILE = Path(__file__).parent.parent / "output" / "libros_extraidos.json"
REQUEST_DELAY = 0.5