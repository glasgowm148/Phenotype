from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"
TEMPLATE_DIR = APP_DIR / "templates"
DEFAULT_DB_PATH = DATA_DIR / "phenotype.sqlite"
DEFAULT_SCRAPED_JSON = DATA_DIR / "scrapedData.json"
DEFAULT_GENOTYPES_JSON = DATA_DIR / "yourData.json"
UPLOAD_DIR = DATA_DIR / "uploads"

