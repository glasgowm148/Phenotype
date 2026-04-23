.PHONY: install run test lint format scrape-demo

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e ".[dev]"

run:
	cd src/1-Phenotype-web && ../../.venv/bin/python -m flask --app SnpApi run --host 127.0.0.1 --port 5000

test:
	.venv/bin/python -m pytest

lint:
	.venv/bin/python -m ruff check src/1-Phenotype-web/phenotype tests

format:
	.venv/bin/python -m ruff format src/1-Phenotype-web/phenotype tests

scrape-demo:
	cd src/1-Phenotype-web && ../../.venv/bin/python DataScraper.py -f data/example2.txt
