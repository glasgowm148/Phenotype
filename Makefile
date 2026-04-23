.PHONY: install run test lint format scrape-demo

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e ".[dev]"

run:
	cd src/phenotype-web && ../../.venv/bin/python -m flask --app phenotype.app:create_app run --host 127.0.0.1 --port 5000

test:
	.venv/bin/python -m pytest

lint:
	.venv/bin/python -m ruff check src/phenotype-web/phenotype tests

format:
	.venv/bin/python -m ruff format src/phenotype-web/phenotype tests

scrape-demo:
	cd src/phenotype-web && ../../.venv/bin/python DataScraper.py -f data/example2.txt
