# Project 2: Test Automation Framework

API tests (Mon-Wed), accessibility and MCP tests (Thu). This repo has NO pipeline yet: Friday's exercise adds one.

## Layout
    config/ -> clients/ -> services/ -> models/ -> data/        (framework layers)
    tests/api  tests/unit  tests/a11y  tests/mcp               (test suites)
    storefront/ storefront_fixed/                              (static pages under a11y test)
    mcp_server/                                                (small MCP server over the API)
    project2_api_server.py                                     (stand-in API, port 8000)
    reports/a11y/                                              (a11y JSON written by the tests)

## Run locally
    pip install -r requirements.txt
    python project2_api_server.py 8000 &              # the API under test
    pytest -m "not a11y"                              # API + unit + mcp
    API_MODE=mock pytest -m "mock or smoke"           # offline subset
    REQUIRE_API=1 pytest -m "live and smoke"          # API down = failure (use in CI)
    pytest -n 2 -m "not a11y and not mcp"             # parallel (xdist)
    pytest -m a11y                                    # needs Chromium (see below)
    pytest -m mcp                                     # in-memory, no browser

Reports: add `--junitxml=reports/junit.xml --html=reports/report.html --self-contained-html` (pytest-html) and `--cov=. --cov-report=xml` (pytest-cov); install `pytest-html pytest-cov` first.

## Configuration (environment variables)
BASE_URL (default http://127.0.0.1:8000), API_USER, API_PASSWORD, API_ADMIN_USER, API_ADMIN_PASSWORD, API_TIMEOUT, API_MODE (live|mock), REQUIRE_API (0|1), CHROMIUM_PATH (a11y: use a pre-installed Chromium).
