# QA Engineer Case Study — Public APIs x K6 + Playwright

## Setup

```bash
# Clone the repository
git clone <repo-link>
cd qa-case-study

# Python virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r playwright-python/requirements.txt
playwright install
Run tests:

bash
Copy code
# K6 tests
k6 run k6/rest/restcountries-smoke.js
k6 run k6/graphql/rickmorty-characters.js

# Playwright E2E tests
pytest playwright-python/tests/
Test Strategy
Integration Tests (K6, JS)
REST: Rest Countries v3

GraphQL: Rick & Morty GraphQL

Scenarios: happy-path & edge cases, response time SLAs, schema validation, functional assertions, error handling, basic load testing

E2E Tests (Playwright, Python)
Demo site: SauceDemo

Scenarios: login success/failure, product listing, add to cart & checkout (payment excluded), optional accessibility checks

Flakiness controls: stable selectors (data-test), explicit waits, retries

Screenshots/video/trace captured on failure

CI / GitHub Actions
Workflows run automatically on Pull Requests:

K6 tests: k6-integration.yml

Playwright tests: playwright-e2e.yml

Test artifacts (screenshots/video) available on failures

K6 performance thresholds logged in workflow

Notes
Tests are isolated and idempotent, not dependent on mutable server state

Pytest markers (login, checkout) are registered in pytest.ini

K6 thresholds and load profiles ensure meaningful performance validation