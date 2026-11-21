# Handout 09 – CI/CD Concepts & GitLab Pipelines

> **How to use this handout:** Topics 1 and 2 are small local scripts. Topics 3 and 4 use one tiny repo, `ci-demo`, which you create in Topic 3, Step 0. Nothing from earlier handouts is needed. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- A GitLab account. After you create the project in Topic 3, check that shared runners are enabled (**Settings → CI/CD → Runners**).
- Git and Python 3 installed.

---

## Topic 1 – Continuous Integration and Deployment

### Definition

**Continuous Integration (CI)** means every developer merges small changes into the shared main branch often (at least daily). Each merge is automatically **built and tested**, so problems are found within minutes instead of in a painful "integration hell" weeks later. **Continuous Delivery** goes further: every change that passes the pipeline is *ready* to release, and a person presses the button. **Continuous Deployment** removes that button, so every passing change goes to production automatically. For QE, automated tests act as **quality gates**: if a gate fails, the change does not move forward.

### Key ideas

| DORA metric | Question it answers | Good direction |
|-------------|---------------------|----------------|
| Deployment frequency | How often do we release? | ↑ more often |
| Lead time for changes | Commit → production takes how long? | ↓ shorter |
| Change failure rate | What % of deployments cause a failure? | ↓ lower |
| Time to restore service | How fast do we recover? | ↓ faster |

- **Pipeline vocabulary (tool-neutral):** trigger → stages → jobs → gates → artifacts.
- **Shift-left:** run cheap, fast tests (lint, unit, API smoke) first and slower ones (accessibility, end-to-end) later.
- **Merge request + required checks:** code cannot be merged unless the pipeline is green.

### Worked example – Calculating DORA metrics from a deployment log

📁 Folder: `week7-demos/09-1-dora/`

**Step 1 – Save the log** as `data/deploys.csv`.

```
deployed_at,committed_at,failed,restored_at
2026-11-02 10:00,2026-11-01 15:00,no,
2026-11-04 16:00,2026-11-04 09:00,yes,2026-11-04 17:30
2026-11-06 11:00,2026-11-05 14:00,no,
2026-11-09 09:30,2026-11-08 18:00,no,
```

**Step 2 – Load the log** (`dora.py`).

```python
import csv
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"
rows = list(csv.DictReader(open("data/deploys.csv", encoding="utf-8")))
parse = lambda s: datetime.strptime(s, FMT)
```

**Step 3 – Calculate deployment frequency and lead time.**

```python
days = (parse(rows[-1]["deployed_at"]) - parse(rows[0]["deployed_at"])).days or 1
print("Deploys per week:", round(len(rows) / days * 7, 1))

leads = [(parse(r["deployed_at"]) - parse(r["committed_at"])).total_seconds() / 3600 for r in rows]
print("Avg lead time (h):", round(sum(leads) / len(leads), 1))
```

**Step 4 – Calculate the change failure rate and time to restore.**

```python
failed = [r for r in rows if r["failed"] == "yes"]
print("Change failure rate:", f"{len(failed) / len(rows):.0%}")

restore = [(parse(r["restored_at"]) - parse(r["deployed_at"])).total_seconds() / 60 for r in failed]
print("Avg time to restore (min):", round(sum(restore) / len(restore)))
```

### Final code

**`data/deploys.csv`**

```
deployed_at,committed_at,failed,restored_at
2026-11-02 10:00,2026-11-01 15:00,no,
2026-11-04 16:00,2026-11-04 09:00,yes,2026-11-04 17:30
2026-11-06 11:00,2026-11-05 14:00,no,
2026-11-09 09:30,2026-11-08 18:00,no,
```

**`dora.py`**

```python
import csv
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"
rows = list(csv.DictReader(open("data/deploys.csv", encoding="utf-8")))
parse = lambda s: datetime.strptime(s, FMT)

# Deployment frequency and lead time
days = (parse(rows[-1]["deployed_at"]) - parse(rows[0]["deployed_at"])).days or 1
print("Deploys per week:", round(len(rows) / days * 7, 1))

leads = [(parse(r["deployed_at"]) - parse(r["committed_at"])).total_seconds() / 3600 for r in rows]
print("Avg lead time (h):", round(sum(leads) / len(leads), 1))

# Change failure rate and time to restore
failed = [r for r in rows if r["failed"] == "yes"]
print("Change failure rate:", f"{len(failed) / len(rows):.0%}")

restore = [(parse(r["restored_at"]) - parse(r["deployed_at"])).total_seconds() / 60 for r in failed]
print("Avg time to restore (min):", round(sum(restore) / len(restore)))
```

### How to run

```bash
cd week7-demos/09-1-dora
python dora.py
```

### Checkpoint

```
Deploys per week: 4.7
Avg lead time (h): 15.6
Change failure rate: 25%
Avg time to restore (min): 90
```

### Your turn

1. Add two more successful deploys on 2026-11-10 and 2026-11-11 (each with a 2-hour lead time) and rerun. Which metrics improve?
2. Explain the difference between Continuous **Delivery** and Continuous **Deployment** in one sentence each, and give a reason a bank might choose Delivery.
3. Put these in fail-fast order: accessibility scan, lint, deploy to staging, API smoke tests, unit tests, full API regression.
4. A test fails randomly about 1 run in 20. Why is that dangerous for CI, beyond being annoying?

---

## Topic 2 – Build-Test-Deploy Lifecycle

### Definition

The **build-test-deploy lifecycle** is the path every change takes: **source** → **build** → **test** → **package** → **release** → **deploy** → **operate/monitor**. *Build* turns source code into something runnable, such as a Python wheel, a Node bundle or a Docker image. The rule **build once, deploy many** means that exact same, versioned artifact is promoted through dev → staging → production, so what you tested is what you ship. After each deployment, a **health check** confirms the service is really up before traffic is sent to it or the pipeline continues.

### Key ideas

| Strategy | How it works | Rollback |
|----------|--------------|----------|
| Recreate | Stop the old version, start the new one | Redeploy the old version (downtime) |
| Rolling | Replace instances a few at a time | Roll forward or back gradually |
| Blue-green | Two environments; switch traffic | Switch back instantly |
| Canary | Send a small % of traffic to the new version first | Route the % back |
| Feature flag | Deploy the code switched off; turn it on later | Turn the flag off |

- **Version every artifact** with semver plus the commit SHA, for example `1.4.2+a1b2c3d`. Never rebuild for each environment.
- **Per-environment config** comes from variables, never from different code (Handout 10).
- **QE in each phase:** reviews (source) → unit, API and a11y tests (test) → smoke and health checks (deploy) → monitoring alerts (operate).

### Worked example – A post-deploy health-check script

📁 Folder: `week7-demos/09-2-health/`

**Step 1 – Read the target from the environment** (`healthcheck.py`).

```python
import os
import sys
import time
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
HEALTH_PATH = os.getenv("HEALTH_PATH", "/posts/1")
```

**Step 2 – Write one check that never hangs.**

```python
def healthy():
    try:
        r = requests.get(BASE_URL + HEALTH_PATH, timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False
```

**Step 3 – Retry a bounded number of times with a delay.**

```python
def wait_until_healthy(attempts=5, delay=2):
    for i in range(1, attempts + 1):
        if healthy():
            print(f"healthy on attempt {i}")
            return True
        print(f"attempt {i} failed, retrying in {delay}s")
        time.sleep(delay)
    return False
```

**Step 4 – Report the result with an exit code**, because exit codes are how a pipeline decides pass or fail.

```python
if __name__ == "__main__":
    sys.exit(0 if wait_until_healthy() else 1)
```

### Final code

**`healthcheck.py`**

```python
import os
import sys
import time
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
HEALTH_PATH = os.getenv("HEALTH_PATH", "/posts/1")


def healthy():
    try:
        r = requests.get(BASE_URL + HEALTH_PATH, timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False


def wait_until_healthy(attempts=5, delay=2):
    for i in range(1, attempts + 1):
        if healthy():
            print(f"healthy on attempt {i}")
            return True
        print(f"attempt {i} failed, retrying in {delay}s")
        time.sleep(delay)
    return False


if __name__ == "__main__":
    sys.exit(0 if wait_until_healthy() else 1)
```

### How to run

```bash
cd week7-demos/09-2-health

# a healthy target
python healthcheck.py; echo "exit=$?"

# a bad path
HEALTH_PATH=/does-not-exist python healthcheck.py; echo "exit=$?"
```

In PowerShell, use `python healthcheck.py; echo "exit=$LASTEXITCODE"`, and set the bad path with `$env:HEALTH_PATH="/does-not-exist"` (clear it afterwards with `Remove-Item Env:HEALTH_PATH`).

### Checkpoint

The healthy target prints:

```
healthy on attempt 1
exit=0
```

The bad path prints five `attempt N failed` lines (about 10 seconds), then `exit=1`.

### Your turn

1. Add a `--attempts` command-line option (use `sys.argv` or `argparse`).
2. Also check that the response time is under 2 seconds. Should a slow response fail the health check? Discuss.
3. Choose a deployment strategy for each scenario: (a) an internal tool where 10 minutes of downtime is fine, (b) a payment API, (c) a new UI you want 5% of users to try.
4. Why is rebuilding the Docker image separately for staging and for production risky?

---

## Topic 3 – GitLab CI/CD Fundamentals

### Definition

**GitLab CI/CD** runs pipelines defined in a YAML file named **`.gitlab-ci.yml`** at the root of the repository. Each push or merge request triggers a **pipeline**, which is made of **stages** that contain **jobs**. A job is a list of shell commands (`script`) that runs on a **runner**, usually inside a Docker **image** you choose. GitLab provides **predefined variables** such as `$CI_COMMIT_SHA`, and the **CI Lint** tool checks the YAML before you push.

### Key ideas

| Keyword | Purpose |
|---------|---------|
| `stages:` | The ordered list of stage names |
| `image:` | The Docker image the job runs in (e.g. `python:3.12-slim`) |
| `before_script:` / `script:` / `after_script:` | Setup / main commands / always-run cleanup |
| `default:` | Settings shared by all jobs |
| `cache:` | Speeds up repeated downloads (best effort) |

- **YAML rules:** indent with spaces (never tabs), `key: value` for mappings, `- item` for lists, and `|` for multi-line scripts.
- **A job fails** when any `script` command exits with a non-zero code. That is why PyTest's exit code matters.
- **Where to look:** Build → Pipelines → (pipeline) → (job) → log.

### Worked example – Your first pipeline

📁 Repo: `ci-demo`. A pipeline needs something to test, so you first create a tiny repo with a small Python module and four tests.

**Step 0 – Create the `ci-demo` repo.** In GitLab, create a new **blank project** named `ci-demo` and clone it. Add these four files, so the repo looks like this:

```
ci-demo/
├── calc.py
├── tests/
│   └── test_calc.py
├── pytest.ini
└── requirements.txt
```

```python
# calc.py
def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("b must not be zero")
    return a / b
```

```python
# tests/test_calc.py
import pytest

from calc import add, divide


@pytest.mark.smoke
def test_add():
    assert add(2, 3) == 5


@pytest.mark.smoke
def test_divide():
    assert divide(6, 3) == 2


@pytest.mark.regression
def test_divide_by_zero():
    with pytest.raises(ValueError, match="zero"):
        divide(1, 0)


@pytest.mark.regression
def test_add_negative():
    assert add(-1, -1) == -2
```

```ini
# pytest.ini
[pytest]
pythonpath = .
markers =
    smoke: quick checks
    regression: full checks
```

```
# requirements.txt
pytest
```

Run `pytest -q` locally and check you see `4 passed`. Then commit and push.

In the steps below you build `.gitlab-ci.yml` in the repo root. Push after each step, and each push starts a new pipeline.

**Step 1 – One stage and one job.**

```yaml
stages:
  - test

hello:
  stage: test
  script:
    - echo "Pipeline for $CI_PROJECT_NAME at $CI_COMMIT_SHORT_SHA"
```

**Step 2 – Choose a Python image and install dependencies.**

```yaml
default:
  image: python:3.12-slim
  before_script:
    - python --version
    - pip install -r requirements.txt
```

**Step 3 – Replace `hello` with a real test job.**

```yaml
unit-tests:
  stage: test
  script:
    - pytest -v
```

**Step 4 – Cache pip downloads.** Add a top-level `variables:` block, and add `cache:` inside `default:`.

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

default:
  # ...image and before_script from Step 2...
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip]
```

**Step 5 – Validate before pushing.** Go to **Build → Pipeline editor → Validate** (CI Lint), then commit.

### Final code

The repo now has the four files from Step 0 plus this pipeline file:

**`.gitlab-ci.yml`**

```yaml
stages:
  - test

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

default:
  image: python:3.12-slim
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip]
  before_script:
    - python --version
    - pip install -r requirements.txt

unit-tests:
  stage: test
  script:
    - pytest -v
```

### How to run

From the root of your `ci-demo` clone:

```bash
git add .gitlab-ci.yml
git commit -m "Add first pipeline"
git push
```

Then open your project in GitLab and go to **Build → Pipelines**. Click the newest pipeline, then the `unit-tests` job, to see its log.

### Checkpoint

In **Build → Pipelines**, a pipeline with one green `unit-tests` job appears. Its log ends with `==== 4 passed in 0.05s ====` and `Job succeeded`.

### Your turn

1. Break the YAML on purpose (indent `script:` with a tab) and run CI Lint. Copy the error message.
2. Add `after_script: - echo "Job status: $CI_JOB_STATUS"` and find it in the log.
3. Make one test fail, push, and find in the log the exact line that made the job red.
4. Print three more predefined variables: the branch name, the pipeline id and the commit author.

### Common errors

- **`pytest: command not found`.** `pytest` is missing from `requirements.txt`.
- **`This job is stuck`.** No runner is available. Check **Settings → CI/CD → Runners** and enable the shared runners.
- **The job passes locally but fails in CI.** CI uses a clean image, so check Python versions, missing files (`.gitignore`) and environment variables.

---

## Topic 4 – Pipeline Stages and Jobs

### Definition

**Stages** run **in order**, and the **jobs inside a stage run in parallel**. A stage starts only when the previous stage has succeeded. The `needs:` keyword turns this into a **DAG** (directed acyclic graph), so a job starts as soon as its real prerequisites finish instead of waiting for the whole previous stage. `rules:` decide **whether** a job runs (for example, only on merge requests). `extends:` and hidden jobs (names that start with `.`) let many jobs share configuration. Together these produce a pipeline that is fast, readable, and fails early.

### Key ideas

| Keyword | Example | Use it to |
|---------|---------|-----------|
| `needs:` | `needs: [unit]` | Start early (DAG) and fetch only these jobs' artifacts |
| `rules:` | `- if: $CI_PIPELINE_SOURCE == "merge_request_event"` | Run a job conditionally |
| `parallel:matrix:` | `PY: ["3.11", "3.12"]` | Fan out one job across variants |
| `extends:` | `extends: .python` | Reuse a hidden template job |
| `allow_failure:` / `retry:` / `timeout:` | `retry: 1` | Control how a failure is handled |
| `environment:` | `name: staging` | Track deployments in GitLab |

### Worked example – A `lint → test → build → deploy` pipeline

📁 Repo: `ci-demo` (the repo you created in Topic 3, Step 0). Replace the whole `.gitlab-ci.yml` with the blocks below, in order.

**Step 1 – Declare the stages and a hidden template.**

```yaml
stages: [lint, test, build, deploy]

.python:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt
```

**Step 2 – Add lint and two test jobs in the same stage** (they run in parallel).

```yaml
lint:
  stage: lint
  extends: .python
  script:
    - pip install ruff
    - ruff check .

smoke:
  stage: test
  extends: .python
  script:
    - pytest -q -m smoke

all-tests:
  stage: test
  extends: .python
  script:
    - pytest -q
```

**Step 3 – Fan out across Python versions with a matrix.**

```yaml
regression:
  stage: test
  image: python:$PY-slim
  parallel:
    matrix:
      - PY: ["3.11", "3.12"]
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q -m regression
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

**Step 4 – Build as soon as the smoke tests pass**, using `needs` to form a DAG.

```yaml
build:
  stage: build
  needs: [lint, smoke]
  script:
    - echo "Building image ci-demo:$CI_COMMIT_SHORT_SHA"
```

**Step 5 – Add a manual deploy to staging, on the main branch only.**

```yaml
deploy-staging:
  stage: deploy
  needs: [build]
  environment:
    name: staging
  script:
    - echo "Deploying $CI_COMMIT_SHORT_SHA to staging"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

### Final code

This is the complete `.gitlab-ci.yml` after Steps 1–5. It replaces the file from Topic 3.

**`.gitlab-ci.yml`**

```yaml
stages: [lint, test, build, deploy]

.python:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt

lint:
  stage: lint
  extends: .python
  script:
    - pip install ruff
    - ruff check .

smoke:
  stage: test
  extends: .python
  script:
    - pytest -q -m smoke

all-tests:
  stage: test
  extends: .python
  script:
    - pytest -q

regression:
  stage: test
  image: python:$PY-slim
  parallel:
    matrix:
      - PY: ["3.11", "3.12"]
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q -m regression
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

build:
  stage: build
  needs: [lint, smoke]
  script:
    - echo "Building image ci-demo:$CI_COMMIT_SHORT_SHA"

deploy-staging:
  stage: deploy
  needs: [build]
  environment:
    name: staging
  script:
    - echo "Deploying $CI_COMMIT_SHORT_SHA to staging"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

### How to run

Push it twice, once on a feature branch and once on `main`, to see how `rules:` changes the pipeline:

```bash
# 1. a feature branch
git checkout -b feature/stages-demo
git add .gitlab-ci.yml
git commit -m "Add lint, test, build and deploy stages"
git push -u origin feature/stages-demo

# 2. main
git checkout main
git merge feature/stages-demo
git push
```

Open **Build → Pipelines** after each push. On the `main` pipeline, click ▶ on `deploy-staging` to run the manual job.

### Checkpoint

- **On a feature-branch push:** the pipeline graph shows `lint` → `smoke` + `all-tests` → `build`. There is no regression or deploy job.
- **On `main`:** `regression: [3.11]` and `regression: [3.12]` also appear, plus `deploy-staging` with a ▶ (play) button.
- In the **Needs** view, `build` starts right after `smoke`, without waiting for `all-tests` or the regression jobs.

### Your turn

1. Add `allow_failure: true` to `all-tests` and make a regression test fail. What colour is the job, and does the pipeline pass?
2. Add `retry: 1` to `smoke`. When is retrying acceptable, and when does it hide real bugs?
3. Add a `workflow: rules:` block so pipelines run only for merge requests and the default branch.
4. Add a `docs-check` job to the `lint` stage that runs only when `README.md` changes. (Hint: `rules: - changes: [README.md]`.)

### Common errors

- **`needs:` points to a job in a later stage**, or to a job that is skipped by `rules`. The pipeline is then invalid or stuck. Use `optional: true` when a needed job may not exist.
- **A typo in a `rules:` variable** (`$CI_COMMIT_BRANH`). It silently evaluates to false, so the job never runs.
- **Mixing `only/except` with `rules`** in the same job is not allowed. Use `rules`.

---

## Answers

<details>
<summary><strong>Topic 1 – Continuous Integration and Deployment</strong></summary>

1. The average lead time drops from 15.6 h to 11.1 h, and the change failure rate drops from 25% to 17%. Deploys per week stays at 4.7 (6 deploys over 9 days is the same rate as 4 over 6), and time to restore stays at 90 minutes because no new failures were added.
2. **Delivery:** every passing change *can* be released, and a person decides when. **Deployment:** every passing change *is* released automatically. A bank may need a manual approval for regulation, audit or timed release windows.
3. lint → unit tests → API smoke tests → full API regression → accessibility scan → deploy to staging.
4. People learn to ignore red builds and rerun them, so real failures get ignored too. This destroys trust in the quality gate.

</details>

<details>
<summary><strong>Topic 2 – Build-Test-Deploy Lifecycle</strong></summary>

1. ```python
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("--attempts", type=int, default=5)
   args = parser.parse_args()
   sys.exit(0 if wait_until_healthy(attempts=args.attempts) else 1)
   ```
2. ```python
   return r.status_code == 200 and r.elapsed.total_seconds() < 2
   ```
   Discussion: a health check answers "is it up?". Slowness is better handled by monitoring or performance tests, unless the deployment requires a performance SLO.
3. (a) Recreate, (b) blue-green (instant rollback), (c) canary or a feature flag.
4. Two builds can differ (dependency updates, a different base image), so production would run code that was never tested.

</details>

<details>
<summary><strong>Topic 3 – GitLab CI/CD Fundamentals</strong></summary>

1. A message such as *"This GitLab CI configuration is invalid: (<unknown>): found character that cannot start any token while scanning for the next token at line N column M"*.
2. ```yaml
   unit-tests:
     stage: test
     script:
       - pytest -v
     after_script:
       - echo "Job status: $CI_JOB_STATUS"
   ```
   The log shows `Job status: success` (or `failed`) in the after-script section.
3. Look for the PyTest `FAILED tests/...` line and the `AssertionError`, then `ERROR: Job failed: exit code 1`.
4. `echo "$CI_COMMIT_BRANCH $CI_PIPELINE_ID $CI_COMMIT_AUTHOR"`.

</details>

<details>
<summary><strong>Topic 4 – Pipeline Stages and Jobs</strong></summary>

1. `all-tests` shows **orange (warning)** and the pipeline still **passes** (with a warning). (On `main`, the `regression` job fails red, because it has no `allow_failure`.)
2. Retrying is acceptable for known *infrastructure* blips (runner or network). It hides bugs when the test itself is flaky or the product fails intermittently, so track retries and fix the cause.
3. ```yaml
   workflow:
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
   ```
4. ```yaml
   docs-check:
     stage: lint
     image: alpine:3.20
     script:
       - test -s README.md && echo "README is not empty"
     rules:
       - changes: [README.md]
   ```

</details>
