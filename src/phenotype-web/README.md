# Phenotype Web App

This folder contains the Flask app used by Phenotype.

The current source of truth for setup, features, imports, VEP workflow, and API endpoints is the repository root [README.md](/Users/m/Documents/GitHub/Phenotype/README.md).

## Local Run

```bash
cd src/phenotype-web
../../.venv/bin/python -m flask --app phenotype.app:create_app run --host 127.0.0.1 --port 5000
```

If `5000` is already occupied, use any free local port.

The default view opens on `Findings`, sorted by highest SNPedia magnitude.

## Data Files

- `data/scrapedData.json`
- `data/yourData.json`
- `data/phenotype.sqlite`
- `data/exports/`

## Notes

- Summary counts and the first page of the default findings view are cached locally for faster refreshes.
- The sidebar carries zygosity, position, release, VEP, studies, and source links; the table stays summary-first.
