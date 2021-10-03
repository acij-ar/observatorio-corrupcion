#!/bin/bash
set -e

function fail {
  echo $1 >&2
  exit 1
}

function retry {
  local n=1
  local max=5
  local delay=15
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        ((n++))
        echo "Command failed. Attempt $n/$max:"
        sleep $delay;
      else
        fail "The command has failed after $n attempts."
      fi
    }
  done
}

# Output data
mkdir -p data/cij

# Run the scraper
retry docker-compose run --rm scraper node index.js
# Run the pipeline process
retry docker-compose run --rm pipeline python 01_download_external_data.py
retry docker-compose run --rm pipeline python 02_data_normalization.py
retry docker-compose run --rm pipeline python 03_download_resolution_pdfs.py
retry docker-compose run --rm pipeline python 04_create_arango_nodes.py
retry docker-compose run --rm pipeline python 05_create_arango_edges.py
retry docker-compose run --rm pipeline python 06_update_arango.py
retry docker-compose run --rm pipeline python 07_send_notify_emails.py

zip -r cij.zip data/cij/* data/db/*
