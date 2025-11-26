# QA Engineer Case Study — Public APIs x K6 + Playwright

## Setup

Clone the repository and set up the environment:

```bash
git clone https://github.com/nihalgokmen/QA_Case_Study.git
cd qa-case-study

# Python virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
playwright install
Run tests:

bash
Copy code
# K6 tests
k6 run k6/rest/restcountries-smoke.js
k6 run k6/graphql/rickmorty-characters.js

# Playwright E2E tests
pytest playwright-python/tests/ 

```

CI / GitHub Actions
Workflows run automatically on Pull Requests

## Integration Tests
Integration Tests (K6, JS)
Tests are executed on REST and GraphQL public APIs:

REST: Rest Countries v3

GraphQL: Rick & Morty GraphQL

Include happy-path and edge cases, response time SLAs, schema validation, functional assertions, error handling, and basic load testing.

## E2E Tests
E2E Tests (Playwright, Python)
Demo site: SauceDemo

Login success/failure

Product listing and detail view

Add to cart and checkout (payment step excluded)

Optional accessibility checks

Screenshots, videos, or traces are captured on failures.


## Notes
Tests are isolated and idempotent, not dependent on mutable server state

Pytest markers (login, checkout) are registered in pytest.ini

K6 thresholds and load profiles ensure meaningful performance validation
