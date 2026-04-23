from __future__ import annotations

from phenotype.app import create_app
from phenotype.scraper import main as scrape_main


def web() -> None:
    create_app().run()


def scrape() -> None:
    scrape_main()
