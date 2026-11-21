# Handout 10 – Secrets, Tests in Pipelines & Reporting

> **How to use this handout:** all three topics use one small repo, `ci-reports-demo`, which you create in Topic 5, Step 0. Nothing from earlier handouts is needed. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- A GitLab account. After you create the project in Topic 5, check that shared runners are enabled (**Settings → CI/CD → Runners**).
- Git and Python 3 installed.

---

## Topic 5 – Secrets and Configuration Management

### Definition

**Configuration** is anything that changes between environments, such as the base URL, timeouts and feature flags. A **secret** is configuration that grants access, such as an API key, token, password or certificate. Following the twelve-factor rule *"store config in the environment,"* both come from **environment variables**, so the same code runs everywhere. Secrets need extra protection: they are never committed to Git, never printed in logs or reports, and they are **rotated immediately** if they leak. In GitLab, they live in **CI/CD variables** marked **Masked** and **Protected**.

### Key ideas

| | Configuration | Secret |
|---|---|---|
| Example | `BASE_URL`, `API_TIMEOUT` | `API_TOKEN`, `DB_PASSWORD` |
| Can be in the repo? | Defaults only | **Never** |
| GitLab variable flags | Plain | **Masked** (hidden in logs) + **Protected** (protected branches only) |
| If leaked | Change it | **Rotate first**, then clean up |

- **A committed secret stays compromised.** It remains in Git history even after you delete the file.
- **Precedence (simplified):** job `variables:` < project CI/CD variables < variables set for a manual or scheduled pipeline run. Predefined `CI_*` variables are set by GitLab.
- **Fail fast:** if a required secret is missing, stop with a clear message instead of sending requests that return `401`.
- **Scan for leaks** with GitLab Secret Detection, gitleaks, or a pre-commit hook.

### Worked example – Safe settings, locally and in CI

📁 Repo: `ci-reports-demo`. All three topics in this handout use this small repo: a tiny API client with three tests, a one-page site with an accessibility test, and the PyTest settings.

**Step 0 – Create the `ci-reports-demo` repo.** In GitLab, create a new **blank project** named `ci-reports-demo` and clone it. Add these files, so the repo looks like this:

```
ci-reports-demo/
├── api_client.py
├── site/index.html
├── tests/test_api.py
├── tests/test_a11y.py
├── pytest.ini
├── requirements.txt
└── .gitignore
```

```python
# api_client.py
import os
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


def get_post(post_id):
    return requests.get(f"{BASE_URL}/posts/{post_id}", timeout=5)
```

```python
# tests/test_api.py
import pytest
from api_client import get_post


@pytest.mark.smoke
def test_post_1_ok():
    assert get_post(1).status_code == 200


@pytest.mark.regression
def test_post_title_is_text():
    assert isinstance(get_post(1).json()["title"], str)


@pytest.mark.regression
def test_missing_post_404():
    assert get_post(9999).status_code == 404
```

```html
<!-- site/index.html -->
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Demo home</title></head>
<body>
  <main>
    <h1>Welcome</h1>
    <label for="q">Search</label> <input id="q" type="search">
    <button type="button">Go</button>
  </main>
</body>
</html>
```

```python
# tests/test_a11y.py
import json
import os
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe

SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")
OPTIONS = {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}}
OUT = Path("reports/a11y")


@pytest.mark.accessibility
def test_home_page_is_accessible(page):
    page.goto(f"{SITE_URL}/index.html")
    results = Axe().run(page, options=OPTIONS)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.json").write_text(json.dumps(results.response, indent=2))
    assert results.violations_count == 0, results.generate_report()
```

```ini
# pytest.ini
[pytest]
pythonpath = .
testpaths = tests
markers =
    smoke: quick checks
    regression: full checks
    accessibility: axe scans
addopts = -ra --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

```
# requirements.txt
requests
pytest
pytest-html
pytest-cov
pytest-xdist
python-dotenv
playwright==1.49.0
pytest-playwright
axe-playwright-python
```

```
# .gitignore
.env
.venv/
reports/
```

Install and check locally:

```bash
pip install -r requirements.txt
pytest -q -m "smoke or regression"
```

You should see `3 passed`. Then commit and push. The steps below add `settings.py` and `.gitlab-ci.yml` to this repo.

**Step 1 – Keep local secrets in a git-ignored `.env` file** in the repo root. (`.env` is already listed in `.gitignore`.)

```
# .env  (never committed)
BASE_URL=https://jsonplaceholder.typicode.com
API_TOKEN=local-dev-token
```

**Step 2 – Load the settings and fail fast.** Create `settings.py` in the repo root, next to `api_client.py`:

```
ci-reports-demo/
├── api_client.py
├── settings.py        ← new (Step 2)
├── .env               ← new (Step 1, never committed)
├── site/index.html
├── tests/
└── ...
```

`settings.py` is the **one place** where the project reads its configuration and secrets, instead of every file calling `os.getenv` itself. Locally the values come from `.env`. In GitLab there is no `.env`, so the same code reads the CI/CD variables you create in Step 4.

```python
import os
from dotenv import load_dotenv

load_dotenv()      # does nothing in CI, where there is no .env file


def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
API_TOKEN = require("API_TOKEN")
```

> **Why is `settings.py` separate from `api_client.py` here?** In a real project, the API client would import `BASE_URL` and `API_TOKEN` from `settings.py`, so every file uses the same values. This example keeps them separate on purpose. JSONPlaceholder needs no token, and if the client imported `settings`, every test would need `API_TOKEN`. The merge-request smoke job would then fail, because protected variables are not available on feature branches. Here, only the `check-config` job in Step 5 uses `settings.py`.

**Step 3 – Never print the secret itself.** Add this to `settings.py`:

```python
def masked(value):
    return value[:4] + "***" if value else "<empty>"
```

Then try it: `python -c "import settings; print(settings.masked(settings.API_TOKEN))"` prints `loca***`.

**Step 4 – Create the variables in GitLab.** Go to **Settings → CI/CD → Variables → Add variable**:

| Key | Value | Flags |
|-----|-------|-------|
| `API_TOKEN` | `ci-token-8f2a9c71d4` | ✅ Masked ✅ Protected |
| `BASE_URL` | `https://jsonplaceholder.typicode.com` | none |

**Step 5 – Use the variables in a job** without ever echoing the secret. Create `.gitlab-ci.yml`:

```yaml
stages: [test]

check-config:
  stage: test
  image: python:3.12-slim
  script:
    - pip install python-dotenv
    - python -c "import settings; print('token loaded:', settings.masked(settings.API_TOKEN))"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH   # main is protected, so the token is available
```

**Step 6 – Add GitLab's secret scanner** at the top of `.gitlab-ci.yml`.

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```

### Final code

The repo now has the files from Step 0, plus `.env` (local only), `settings.py` and `.gitlab-ci.yml`:

**.env  (local only, never committed)**

```
BASE_URL=https://jsonplaceholder.typicode.com
API_TOKEN=local-dev-token
```

**`settings.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()      # does nothing in CI, where there is no .env file


def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


def masked(value):
    return value[:4] + "***" if value else "<empty>"


BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
API_TOKEN = require("API_TOKEN")
```

**`.gitlab-ci.yml`**

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml

stages: [test]

check-config:
  stage: test
  image: python:3.12-slim
  script:
    - pip install python-dotenv
    - python -c "import settings; print('token loaded:', settings.masked(settings.API_TOKEN))"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH   # main is protected, so the token is available
```

### How to run

Locally, from the repo root:

```bash
python -c "import settings; print(settings.masked(settings.API_TOKEN))"
```

Then remove the `API_TOKEN` line from `.env` and run the same command again to see the fail-fast error. Put the line back afterwards.

Then push to GitLab (`.env` is ignored, so it is not committed):

```bash
git add settings.py .gitlab-ci.yml
git commit -m "Add settings and secret checks"
git push
```

Open **Build → Pipelines** and check the `check-config` and `secret_detection` jobs.

### Checkpoint

- Locally, deleting `API_TOKEN` from `.env` and running `python -c "import settings"` stops immediately with `RuntimeError: Missing required setting: API_TOKEN`.
- On `main`, the CI log shows `token loaded: ci-t***`. If a script ever prints the full token, GitLab shows `[MASKED]` instead of the value.
- A new `secret_detection` job appears in the `test` stage. It is green when no secrets are found.

### Your turn

1. Add `echo $API_TOKEN` to the job temporarily and push. What appears in the log? Remove it again afterwards.
2. Temporarily remove the `rules:` from `check-config` and push to a feature branch. What happens to a **Protected** variable there, and what error does your code give?
3. A teammate committed `API_TOKEN=live-123` in `settings.py` last week and removed it today. Write the response steps in the correct order.
4. Write `tests/test_settings.py` that uses `monkeypatch.delenv("API_TOKEN", raising=False)` to prove that importing `settings` raises a clear error.

### Common errors

- **The value can't be masked.** GitLab requires masked values to be at least 8 characters, with a limited character set and on a single line.
- **`.env` committed by accident.** Add it to `.gitignore` *before* creating it. If it was already committed, rotate the secret.
- **A secret saved inside test reports** (for example, in failure messages that print request headers). Mask headers before logging them.

---

## Topic 6 – Test Automation within Pipelines

### Definition

Running tests in a pipeline makes them an automatic **quality gate**: every change is tested the same way, on a clean machine, before it can be merged. A **pipeline-ready** suite is fast, deterministic and independent, and it reads its configuration from the environment. It also gives the right **exit code**, so a failing test turns the job red. Different subsets run at different times: **smoke** tests on every merge request, the full **regression** suite on main and on a nightly schedule. When a test needs a running app, the job starts it (as a background process or a **service container**) and **waits until it is healthy** before testing.

### Key ideas

| When | Run | Why |
|------|-----|-----|
| Merge request | Smoke (`-m smoke`) | Fast feedback (minutes) |
| Main branch | Full regression + accessibility | Protects the release |
| Nightly schedule | Full regression | Catches drift in real services |

- **Fail fast:** use `--maxfail=3`, so an outage doesn't produce 400 identical failures.
- **Speed:** use `pytest -n auto` (pytest-xdist) inside a job, or `parallel: N` across jobs.
- **Flaky tests:** quarantine them with a marker and a ticket. Never "fix" them with blanket retries.
- **Reproduce CI failures locally** with the same image, for example `docker run -it python:3.12-slim bash`.

### Worked example – Smoke, regression and accessibility jobs

📁 Repo: `ci-reports-demo` (the repo you created in Topic 5, Step 0).

Replace `stages:` in `.gitlab-ci.yml` with the lines below and add a shared template. Keep `include:` and `check-config`.

**Step 1 – Declare stages and a template.**

```yaml
stages: [test, report]

.python:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt
```

**Step 2 – Run smoke tests on merge requests.**

```yaml
test:smoke:
  stage: test
  extends: .python
  script:
    - pytest -q --maxfail=3 -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

**Step 3 – Run full regression on main and on schedules, in parallel.**

```yaml
test:regression:
  stage: test
  extends: .python
  script:
    - pytest -q -n auto -m regression
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

**Step 4 – Run the accessibility scan against a site that the job starts itself.**

```yaml
test:a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  variables:
    SITE_URL: "http://localhost:8000"
  script:
    - pip install -r requirements.txt
    - python -m http.server 8000 --directory site &
    - |
      for i in $(seq 1 15); do
        curl -fs "$SITE_URL/index.html" > /dev/null && break
        echo "waiting for site..."; sleep 1
      done
    - pytest -q -m accessibility
```

**Step 5 – Add a coverage quality gate** to the `script` of `test:regression`:

```yaml
    - pytest -q -n auto -m regression --cov=api_client --cov-fail-under=80
```

The job fails if test coverage of `api_client.py` drops below 80%.

### Final code

This is the complete `.gitlab-ci.yml` after Steps 1–5. The coverage gate from Step 5 is part of the `test:regression` command, so the regression tests run once.

**`.gitlab-ci.yml`**

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml

stages: [test, report]

.python:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt

check-config:
  stage: test
  image: python:3.12-slim
  script:
    - pip install python-dotenv
    - python -c "import settings; print('token loaded:', settings.masked(settings.API_TOKEN))"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test:smoke:
  stage: test
  extends: .python
  script:
    - pytest -q --maxfail=3 -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

test:regression:
  stage: test
  extends: .python
  script:
    - pytest -q -n auto -m regression --cov=api_client --cov-fail-under=80
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"

test:a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  variables:
    SITE_URL: "http://localhost:8000"
  script:
    - pip install -r requirements.txt
    - python -m http.server 8000 --directory site &
    - |
      for i in $(seq 1 15); do
        curl -fs "$SITE_URL/index.html" > /dev/null && break
        echo "waiting for site..."; sleep 1
      done
    - pytest -q -m accessibility
```

### How to run

First run the same commands locally, from the repo root:

```bash
pytest -q -m smoke
pytest -q -n auto -m regression --cov=api_client --cov-fail-under=80

# accessibility: install the browser once, then use two terminals
playwright install chromium
python -m http.server 8000 --directory site      # terminal 1
pytest -q -m accessibility                        # terminal 2
```

Then push to `main`, and open a merge request from a branch to see the smoke job:

```bash
git add .gitlab-ci.yml
git commit -m "Add smoke, regression and accessibility jobs"
git push

git checkout -b feature/try-smoke
git commit --allow-empty -m "Trigger a merge request pipeline"
git push -u origin feature/try-smoke              # then open a merge request in GitLab
```

### Checkpoint

| Pipeline triggered by | Jobs you should see in `test` |
|-----------------------|-------------------------------|
| Merge request | `test:smoke`, `test:a11y`, `secret_detection` |
| Push to `main` | `test:regression`, `test:a11y`, `check-config`, `secret_detection` |

- The `test:a11y` log shows zero or more `waiting for site...` lines, then `1 passed, 3 deselected`. The job is green.
- `test:regression` shows `2 passed, 2 deselected` and a coverage table where `api_client.py` is at `100%`.

### Your turn

1. Break the page: remove `<label for="q">Search</label>` from `site/index.html` and push. Which job fails, and what rule id does the log show?
2. Add a nightly schedule (**Build → Pipeline schedules → New schedule**, `0 2 * * *`) and describe which jobs it runs.
3. Add `timeout: 10 minutes` and `interruptible: true` to the regression job. What does each one protect against?
4. Change `playwright==1.49.0` in `requirements.txt` to `1.50.0` (the image stays at `v1.49.0`). Predict the error and fix it.

### Common errors

- **Hard-coded `localhost` URLs inside tests.** Read `SITE_URL` or `BASE_URL` from the environment, so the same test works locally, in CI and against staging.
- **`sleep 30` instead of a health-wait loop.** It is too slow when the app is ready and too short when the app is slow.
- **A mismatch between the Playwright version and the image tag** causes `Executable doesn't exist`. Keep the two versions identical.

---

## Topic 7 – Artifacts and Reporting

### Definition

**Job artifacts** are files that a job saves after it finishes, such as test reports, screenshots, logs or a built package. GitLab stores them so people can download them and later jobs can use them. A **cache** is different: it only speeds up dependency downloads and may be empty at any time. With **`artifacts:reports:junit`**, GitLab reads your JUnit XML and shows a **Tests** tab plus a summary on the merge request. Human-friendly reports, such as **pytest-html**, coverage and axe JSON, are saved as regular artifacts and can be published with **GitLab Pages**. Good reporting tells developers *what* failed, tells QE *why*, and tells stakeholders *how healthy* the product is.

### Key ideas

| | Artifact | Cache |
|---|---|---|
| Purpose | Keep job **outputs** | Speed up job **inputs** |
| Lifetime | `expire_in` (e.g. 1 week) | Best effort |
| Passed to later jobs | Yes (`needs` / `dependencies`) | No guarantee |

- **`when: always`** keeps reports even when tests fail, which is exactly when you need them most.
- **`reports: coverage_report`** and a `coverage:` regex show coverage in the merge request.
- Keep artifact sizes small and set `expire_in`, because storage costs money.

### Worked example – Publishing test, coverage and a11y reports

📁 Repo: `ci-reports-demo` (the repo you created in Topic 5, Step 0), with the pipeline from Topic 6.

**Step 1 – Check that PyTest already produces the reports.** `pytest.ini` contains:

```ini
addopts = -ra --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

**Step 2 – Save them as artifacts, even on failure.** Add this to `test:regression`.

```yaml
  artifacts:
    when: always
    expire_in: 1 week
    paths:
      - reports/
    reports:
      junit: reports/junit.xml
```

**Step 3 – Add coverage to the merge request.** In the same job, replace `script:` and the `artifacts:` block from Step 2 with:

```yaml
  script:
    - pytest -q -n auto -m regression --cov=api_client --cov-report=term --cov-report=xml:reports/coverage.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    expire_in: 1 week
    paths: [reports/]
    reports:
      junit: reports/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml
```

**Step 4 – Keep the accessibility results.** Add this to `test:a11y`. The test already writes `reports/a11y/index.json`.

```yaml
  artifacts:
    when: always
    expire_in: 2 weeks
    paths:
      - reports/a11y/
      - reports/report.html
    reports:
      junit: reports/junit.xml
```

**Step 5 – Publish the HTML report with GitLab Pages.**

```yaml
pages:
  stage: report
  needs: [test:regression]
  script:
    - mkdir -p public
    - cp reports/report.html public/index.html
  artifacts:
    paths: [public]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Final code

This is the complete `.gitlab-ci.yml` after Steps 1–5. It replaces the file from Topic 6.

**`.gitlab-ci.yml`**

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml

stages: [test, report]

.python:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt

check-config:
  stage: test
  image: python:3.12-slim
  script:
    - pip install python-dotenv
    - python -c "import settings; print('token loaded:', settings.masked(settings.API_TOKEN))"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test:smoke:
  stage: test
  extends: .python
  script:
    - pytest -q --maxfail=3 -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

test:regression:
  stage: test
  extends: .python
  script:
    - pytest -q -n auto -m regression --cov=api_client --cov-report=term --cov-report=xml:reports/coverage.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    expire_in: 1 week
    paths: [reports/]
    reports:
      junit: reports/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"

test:a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  variables:
    SITE_URL: "http://localhost:8000"
  script:
    - pip install -r requirements.txt
    - python -m http.server 8000 --directory site &
    - |
      for i in $(seq 1 15); do
        curl -fs "$SITE_URL/index.html" > /dev/null && break
        echo "waiting for site..."; sleep 1
      done
    - pytest -q -m accessibility
  artifacts:
    when: always
    expire_in: 2 weeks
    paths:
      - reports/a11y/
      - reports/report.html
    reports:
      junit: reports/junit.xml

pages:
  stage: report
  needs: [test:regression]
  script:
    - mkdir -p public
    - cp reports/report.html public/index.html
  artifacts:
    paths: [public]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### How to run

From the repo root:

```bash
git add .gitlab-ci.yml
git commit -m "Publish test, coverage and accessibility reports"
git push
```

When the pipeline on `main` finishes, check:

1. The pipeline's **Tests** tab.
2. The `test:a11y` job → **Job artifacts → Browse**.
3. **Deploy → Pages** for the published report URL. The first Pages deployment can take a few minutes.

### Checkpoint

- The pipeline page has a **Tests** tab that shows totals (for example *3 tests, 0 failures*). Clicking a suite lists each test.
- The `test:a11y` job page has a **Job artifacts → Browse** button, with `reports/a11y/index.json` and `reports/report.html` inside.
- A merge request shows a test summary and a coverage percentage.
- **Deploy → Pages** shows a URL that opens the HTML report.

### Your turn

1. Make one regression test fail and push to `main`. Where does the failure appear, and can you still download `report.html`? Why?
2. Change `expire_in` to `30 min`, wait, and try to download the artifact again. What happens?
3. In `tests/conftest.py`, write a hook that saves a Playwright screenshot to `reports/screenshots/<test>.png` when an a11y test fails, and add that folder to the artifacts. (Hint: use the `pytest_runtest_makereport` hook.)
4. Sketch a one-page weekly quality report for stakeholders. Which three numbers would you show?

### Common errors

- **Artifacts missing after a failed job.** The default is `when: on_success`, so add `when: always`.
- **Paths outside the project folder.** GitLab can only save paths inside `$CI_PROJECT_DIR`.
- **`reports: junit` pointing at the wrong path.** The Tests tab stays empty. Check the path against the `--junitxml` value.

---

## Answers

<details>
<summary><strong>Topic 5 – Secrets and Configuration Management</strong></summary>

1. The log shows `[MASKED]` in place of the value.
2. Protected variables are **not** given to unprotected branches, so `API_TOKEN` is empty there. `require()` raises `RuntimeError: Missing required setting: API_TOKEN`. Use an unprotected test-only token for feature branches, or protect the branch.
3. (1) **Rotate/revoke** `live-123` immediately. (2) Check the access logs for misuse. (3) Store the new token as a masked, protected CI/CD variable. (4) Remove it from Git history if your policy requires it (for example with `git filter-repo`). (5) Add secret detection or a pre-commit hook so it doesn't happen again.
4. ```python
   import importlib
   import sys
   import pytest

   def test_missing_token_fails_fast(monkeypatch):
       monkeypatch.delenv("API_TOKEN", raising=False)
       monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: None)   # ignore .env
       sys.modules.pop("settings", None)                                # force a fresh import
       with pytest.raises(RuntimeError, match="API_TOKEN"):
           importlib.import_module("settings")
   ```

</details>

<details>
<summary><strong>Topic 6 – Test Automation within Pipelines</strong></summary>

1. `test:a11y` fails. The log shows the axe report with the rule id **`label`** (*Ensure every form element has a label*).
2. On a `schedule` source, `test:regression` (from its rules), `test:a11y`, `check-config` and `secret_detection` run. `test:smoke` does not, because it is MR-only.
3. `timeout` kills a hung job instead of blocking the runner for an hour. `interruptible` cancels an outdated pipeline when a newer commit is pushed to the same branch.
4. `Executable doesn't exist at /ms-playwright/chromium-...`. The fix is to pin `playwright==1.49.0` (to match the image) or to change the image to `v1.50.0-jammy`.

</details>

<details>
<summary><strong>Topic 7 – Artifacts and Reporting</strong></summary>

1. The pipeline's **Tests** tab shows the failed test and its message (on a merge request, the widget shows *"1 failed test result"*). Yes, `report.html` can still be downloaded, because of `when: always`.
2. After 30 minutes the artifact has expired and been deleted. The download returns *404* or "artifacts expired" (artifacts from the latest successful pipeline may be kept, depending on the project setting).
3. ```python
   from pathlib import Path
   import pytest

   @pytest.hookimpl(hookwrapper=True)
   def pytest_runtest_makereport(item, call):
       outcome = yield
       rep = outcome.get_result()
       if rep.when == "call" and rep.failed and "page" in item.fixturenames:
           page = item.funcargs["page"]
           out = Path("reports/screenshots")
           out.mkdir(parents=True, exist_ok=True)
           page.screenshot(path=str(out / f"{item.name}.png"), full_page=True)
   ```
   Then add `- reports/screenshots/` to the a11y job's `artifacts:paths`.
4. Example: pass rate of the regression suite (trend), the number of open a11y defects by severity (trend), and coverage % (or change failure rate from DORA).

</details>
