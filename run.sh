#!/bin/bash
set -e

# Output data
mkdir -p data/cij

# Run the scraper
docker-compose run --rm scraper

# Run the pipeline process
docker-compose run --rm pipeline python 01_download_external_data.py
docker-compose run --rm pipeline python 02_data_normalization.py
docker-compose run --rm pipeline python 03_download_resolution_pdfs.py
docker-compose run --rm pipeline python 04_create_arango_nodes.py
docker-compose run --rm pipeline python 05_create_arango_edges.py
docker-compose run --rm pipeline python 06_update_arango.py

zip -r cij.zip data/cij/*
