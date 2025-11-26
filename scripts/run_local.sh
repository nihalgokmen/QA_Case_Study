#!/usr/bin/env bash
set -e

echo "Running K6 REST test..."
k6 run k6/rest/restcountries.js

echo "Running K6 GraphQL test..."
k6 run k6/graphql/rickmorty-characters.js

echo "Running Python Playwright E2E tests..."
cd playwright-python
# ensure venv activated outside — we assume you've activated it; otherwise use system python
pytest tests/ -q
cd ..
