from __future__ import annotations

from pathlib import Path

from flask import Flask

from phenotype.app_jobs import _clear_snps_cache, start_background_refresh
from phenotype.app_routes import register_routes
from phenotype.paths import APP_DIR, DATA_DIR, DEFAULT_DB_PATH, DEFAULT_GENOTYPES_JSON, UPLOAD_DIR
from phenotype.providers.combined import fetch_snp_record
from phenotype.storage import PhenotypeStore


def create_app(
    database_path: str | Path = DEFAULT_DB_PATH,
    genotypes_path: str | Path = DEFAULT_GENOTYPES_JSON,
    upload_dir: str | Path = UPLOAD_DIR,
    export_dir: str | Path | None = None,
    seed_legacy: bool = True,
) -> Flask:
    app = Flask(__name__, template_folder=str(APP_DIR / "templates"))
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
    store = PhenotypeStore(database_path)
    genotypes_path = Path(genotypes_path)
    upload_dir = Path(upload_dir)
    export_dir = Path(export_dir) if export_dir is not None else (DATA_DIR / "exports" if seed_legacy else Path(database_path).parent / "exports")
    store.mark_interrupted_runs()
    if seed_legacy:
        store.seed_from_legacy_files(genotypes_path=genotypes_path)
    app.config["PHENOTYPE_STORE"] = store
    _clear_snps_cache()
    start_background_refresh(store)
    register_routes(app, store, genotypes_path, upload_dir, export_dir, fetch_snp_record)
    return app
