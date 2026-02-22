# Books Scraper

Extrae 20 libros de la página principal y 20 de una categoría específica
de [books.toscrape.com](http://books.toscrape.com/) y los guarda en `output/libros_extraidos.json`.


## Instalación y ejecución
```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/books-scraper.git
cd books-scraper

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python src/scraper.py
```

El resultado se guarda en `output/libros_extraidos.json`.