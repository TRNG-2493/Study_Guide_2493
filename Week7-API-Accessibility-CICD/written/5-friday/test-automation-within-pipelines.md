# Test Automation Within Pipelines

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why** tests belong in a pipeline and what makes a test suite "pipeline-ready".
- Write GitLab jobs that run **PyTest API tests**, **MCP server tests**, and **Playwright + axe-core accessibility scans**.
- Use pytest flags (`-q`, `--maxfail`, `-m`) and stage ordering to **fail fast**.
- Choose **smoke vs regression** subsets with `rules` for merge requests, the main branch, and nightly schedules.
- Start an app, mock, or database as a **service container** and wait for it to be healthy.
- Decide between testing a **deployed environment** and an **ephemeral** one, and pass `BASE_URL` to the tests.
- Speed up suites with **pytest-xdist** and the GitLab `parallel` keyword.
- Handle **flaky tests** without masking real failures.
- Explain how **exit codes** and **timeouts** make a pipeline pass or fail, and apply **quality gates** (coverage, zero critical accessibility violations) with merge request blocking.
- **Reproduce** a CI failure on your own machine using the same Docker image.

---

## Why This Matters

This week you built an API test framework (Monday to Wednesday), accessibility scans with axe-core (Thursday), and MCP server tests. Earlier on Friday you learned what a pipeline is, how stages and jobs work, and how GitLab runs them on runners. This lesson is the Week 7 epic's payoff: **plugging your tests into the pipeline so they run on every change, without you.**

Think about the alternative. A teammate changes an endpoint on Tuesday afternoon. Nobody runs your suite. On Thursday the front end breaks in staging, and three people spend two hours finding the cause. With the suite in the pipeline, the teammate's merge request goes red within minutes, shows exactly which test failed, and cannot be merged until it is fixed. That is the difference between tests as a personal habit and tests as a **team safety net**.

A suite that only passes on your laptop is not a safety net, though. CI has no human, no GUI, a clean container every run, and a different operating system. This lesson teaches you to make tests behave well there.

> Two things are deliberately left for the next two Friday lessons: **uploading reports and artifacts** (JUnit results in the merge request, HTML reports, coverage visualisation) and **handling secrets and variables safely**. We mention them briefly here and point you forward.

---

## The Concept

### 1. What "test automation in a pipeline" means

**What:** A pipeline job whose `script` runs your test command. If the command exits with code 0 the job is green; any other code makes it red.

**Why:** Because the pipeline runs on every push or merge request, nobody has to remember to run tests. Results are visible to the whole team, in one place, on the exact commit.

**How, in one picture:**

```
push / merge request
        |
   [ build / lint ]  -->  [ smoke tests ]  -->  [ regression + a11y + mcp ]  -->  merge allowed?
     seconds              1-2 minutes              5-10 minutes
```

Cheap, fast checks run first. Expensive ones run only if the cheap ones pass. That ordering idea (fail fast) appears throughout this lesson.

### 2. Making tests pipeline-ready

Before writing any YAML, make sure the suite itself suits an unattended Linux container.

| Requirement | Why | How |
|---|---|---|
| Pinned dependencies | Container starts empty each run | `requirements.txt` with versions, `pip install -r` |
| No hard-coded URLs | Same code, many environments | Read `BASE_URL` / `TEST_ENV` from environment variables |
| No prompts | Nobody can type | Never call `input()` |
| Headless browser | No display | Playwright is headless by default |
| Isolated, self-cleaning tests | Shared environments, parallel runs | Fixtures create and remove their own data |
| Request timeouts | A hung call must not block the runner | `requests.get(url, timeout=10)` |
| Linux-safe paths | CI is Linux, laptops are often Windows | `pathlib`, forward slashes, exact file name case |

**Real-world scenario:** A student's tests pass on Windows but fail in CI with `ModuleNotFoundError: No module named 'Utils'`. The folder is called `utils`. Windows ignores letter case; Linux does not. The fix is a one-letter rename, but you only find it by running in CI (or in the same Docker image, see section 13).

### 3. Running PyTest API tests in a GitLab job

**What:** A job using a Python image that installs requirements and runs pytest.

```yaml
test:api-smoke:
  stage: test
  image: python:3.12-slim
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
    BASE_URL: "https://api.test.example.com"
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip]
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q --maxfail=3 -m smoke
```

**Line by line:**

- `test:api-smoke:` is the job name. GitLab shows it in the pipeline graph. The colon in the name is only a naming convention.
- `stage: test` places the job in the `test` stage; it starts after earlier stages succeed.
- `image: python:3.12-slim` tells the runner which Docker image to start the job in. The slim variant is smaller and pulls faster. Pin the Python version your project uses, so CI matches local.
- `variables:` defines environment variables for this job only. `PIP_CACHE_DIR` tells pip where to keep downloads (inside the project folder, because GitLab can only cache paths inside the project). `BASE_URL` is read by your framework's config.
- `cache:` with `key: files: [requirements.txt]` creates a cache keyed to the hash of that file, so the cache refreshes only when dependencies change. `paths` lists what to save. A cache is a best-effort speed-up; the job must still work if it is empty.
- `before_script:` runs before `script`. Installing dependencies here keeps `script` focused on the test command.
- `pytest -q --maxfail=3 -m smoke`:
  - `-q` (quiet) shortens output: dots and a summary instead of one line per test. Good for large suites. Use `-v` for small ones when you want every test name in the log.
  - `--maxfail=3` stops the run after three failures. If the API is down, you do not need 400 identical failures; you need to know in 20 seconds.
  - `-m smoke` selects only tests marked `@pytest.mark.smoke`.

**Smoke vs regression:**

- **Smoke** tests are a small, fast set (health, login, one read, one write) answering "is the system basically alive?". Runs in a minute or two.
- **Regression** tests are the full functional coverage answering "did we break something that used to work?". Runs in minutes to hours.

Markers must be registered, or `--strict-markers` will reject them:

```ini
[pytest]
testpaths = tests
addopts = -ra --strict-markers --tb=short
markers =
    smoke: quick health checks
    regression: full functional coverage
    mcp: tests for the MCP server
    accessibility: axe-core scans
    live: tests that call real third-party services
```

Line by line: `testpaths` tells pytest where tests live. `-ra` prints a short summary of everything not passed (skips, xfails, failures). `--strict-markers` turns a typo like `@pytest.mark.smok` into an error instead of a silently unselected test. `--tb=short` shortens tracebacks, which keeps logs readable. The `markers` block registers each marker with a description.

Reports (`--junitxml`) and uploading them are covered in the next lesson, so we leave them out of the examples here.

### 4. Running Playwright + axe-core accessibility scans in a job

**What:** A job that opens real browser pages and runs axe-core against them.

**Why a special image:** Browsers need many system libraries. Installing them on a plain Python image is slow and fragile. Microsoft publishes an image with browsers and dependencies already included.

```yaml
test:a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  variables:
    BASE_URL: "http://localhost:8000"
  script:
    - pip install -r requirements.txt
    - python -m http.server 8000 --directory demo-site &
    - |
      for i in $(seq 1 15); do
        curl -fs "$BASE_URL" > /dev/null && break
        echo "waiting for site..."; sleep 1
      done
    - pytest -q -m accessibility
```

**Line by line:**

- `image: mcr.microsoft.com/playwright/python:v1.49.0-jammy` is the official Playwright image. `v1.49.0` is the Playwright version; `jammy` is Ubuntu 22.04.
- `pip install -r requirements.txt` installs your test dependencies (pytest, axe-playwright or similar).
- `python -m http.server 8000 --directory demo-site &` starts a tiny static web server serving the `demo-site` folder. The trailing `&` runs it in the background so the next line can continue.
- The `- |` block is a multi-line shell script. `seq 1 15` counts 1 to 15. `curl -fs` fetches the page quietly (`-s`) and fails on HTTP errors (`-f`). If it succeeds, `break` leaves the loop. Otherwise we print a message and wait one second. This is a **health-wait**: poll until ready rather than guessing with one fixed `sleep`.
- `pytest -q -m accessibility` runs the scans.

**playwright install notes:**

- In the Playwright image, browsers are already installed. You do not need `playwright install`.
- **The `playwright` version in `requirements.txt` must match the image tag.** If requirements say `playwright==1.50.0` but the image is `v1.49.0`, Playwright looks for a browser build that is not there and fails with "Executable doesn't exist".
- If you must use a plain `python:3.12` image, add `playwright install --with-deps chromium` before the tests. It downloads hundreds of MB each run, so expect a slow job.
- Do not set `headless=False`; there is no display.

### 5. Running MCP server tests

**What:** Your MCP tests (Wednesday and Thursday) typically start the MCP server as a **subprocess talking over stdio** and send it requests.

**Why it is easy in CI:** Everything lives in the same container. There is nothing extra to start.

```yaml
test:mcp:
  stage: test
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q -m mcp
```

This is the same pattern as the API job, with only the marker changed. If the MCP server is remote over HTTP, pass its address as a variable (for example `MCP_SERVER_URL`) just as you do for `BASE_URL`. If the server needs Node (some MCP servers run via `npx`), use an image with both runtimes or install Node in `before_script`.

**Common issue:** the test spawns `python server.py` but the working directory differs in CI. Build paths from `Path(__file__)`, not from the current directory.

### 6. Stage ordering and fail-fast

**What:** Stages run in order; if a job in a stage fails, later stages do not start (by default).

```yaml
stages: [lint, smoke, regression]

lint:
  stage: lint
  image: python:3.12-slim
  script:
    - pip install ruff
    - ruff check .

smoke:
  stage: smoke
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q --maxfail=1 -m smoke]

regression:
  stage: regression
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m "regression and not live"]
```

**Line by line:** `stages` defines the order: lint, then smoke, then regression. `lint` catches syntax and style errors in seconds. `smoke` stops at the first failure (`--maxfail=1`) because if basics are broken, the regression run is a waste. `regression` runs only if everything before it passed. The square-bracket form `script: [pytest ...]` is YAML shorthand for a one-item list.

**Why:** Developers get the cheapest signal first, and runner minutes are not burned on a doomed run.

**When not to fail fast:** When you *want* the full list of failures (for example, nightly runs). There, drop `--maxfail` so you see everything in one go.

You can also use `needs:` to start a job as soon as specific earlier jobs finish rather than waiting for the whole stage, which you met in the earlier lessons on stages and jobs.

### 7. Running different subsets with rules

**What:** `rules` decide whether a job exists in a given pipeline.

| Trigger | What runs | Reason |
|---|---|---|
| Merge request | Lint, smoke, mocked tests, key a11y pages | Feedback in minutes |
| Push/merge to `main` | Plus full regression | Protect the main branch |
| Nightly schedule | Everything, including `live` and full-site a11y | Thorough, nobody waiting |

```yaml
smoke:
  stage: smoke
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m smoke]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"

regression:
  stage: regression
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m "regression and not live"]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      allow_failure: true
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"

live-checks:
  stage: regression
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m live]
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $SCHEDULE_TYPE == "nightly"
```

**Line by line:**

- `$CI_PIPELINE_SOURCE` is a predefined GitLab variable describing what started the pipeline: `merge_request_event`, `push`, `schedule`, `web`, and so on.
- `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` is true on the main branch.
- Rules are checked top to bottom; the first match wins. If none match, the job is not added.
- In `regression`, the first rule makes the job **manual** on merge requests (a Play button), with `allow_failure: true` so that an unrun manual job does not block the pipeline. On main and on schedule, it runs automatically. (If your team wants regression on every merge request, delete the `when: manual` rule and use a plain `if`.)
- `live-checks` runs only when a schedule sets a variable `SCHEDULE_TYPE` to `nightly`.

**Creating the nightly schedule:** in GitLab, **Build > Pipeline schedules > New schedule**. Choose a cron like `0 2 * * *` (2 a.m. daily), the branch, and add variable `SCHEDULE_TYPE=nightly`.

**Real-world scenario:** A team's regression suite takes 25 minutes. Running it on every merge request made developers wait. They ran smoke on merge requests (3 minutes), full regression on main, and everything nightly. Bugs that smoke missed were caught within hours, and merging became pleasant again.

### 8. Services: the app, a mock, or a database as a container

**What:** The `services:` keyword starts extra containers alongside your job container. They are reachable by **hostname** (derived from the image name, or set with `alias`).

**Why:** Your tests need something to talk to, and an *ephemeral* dependency is clean every run.

```yaml
test:api-with-db:
  stage: test
  image: python:3.12-slim
  services:
    - name: postgres:16
      alias: db
    - name: wiremock/wiremock:3.5.4
      alias: mock
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: tester
    POSTGRES_PASSWORD: ci-only-password
    DB_URL: "postgresql://tester:ci-only-password@db:5432/testdb"
    THIRD_PARTY_URL: "http://mock:8080"
  before_script:
    - pip install -r requirements.txt
    - apt-get update -qq && apt-get install -y -qq postgresql-client
  script:
    - |
      for i in $(seq 1 30); do
        pg_isready -h db -U tester && break
        echo "waiting for postgres..."; sleep 2
      done
    - pytest -q -m "regression and not live"
```

**Line by line:**

- `services:` is a list of containers. Each starts before `script` and is stopped afterwards.
- `name: postgres:16` is the image; `alias: db` makes it reachable at hostname `db` (not `localhost`!).
- The WireMock service is a mock HTTP server, reachable at `http://mock:8080`, standing in for a third-party API.
- `POSTGRES_*` variables configure the database container. This password is a throwaway for a container that exists for minutes; real secrets are the subject of a later lesson.
- `DB_URL` and `THIRD_PARTY_URL` are what your framework reads, pointing at the service hostnames.
- `postgresql-client` provides `pg_isready`. The loop polls up to 30 times, 2 seconds apart, until the database accepts connections. This is the **health-wait**. Services start in parallel with your job, so without waiting, your first test may hit a database that is still booting.

**Running the app itself as a service:** if your team's pipeline builds a Docker image of the app, you can list it as a service, and then set `BASE_URL: "http://app:8080"`. Wait on its `/health` endpoint exactly like the loop above.

**Common mistake:** using `localhost` to reach a service. Services are separate containers, so use the alias.

### 9. Deployed environment vs ephemeral environment

| | Deployed (staging/test) | Ephemeral (spun up per pipeline) |
|---|---|---|
| What | A long-lived shared system | Fresh containers for this run only |
| Pros | Realistic: real config, real network, real data volume | Isolated, repeatable, no cross-run interference |
| Cons | Shared state, someone else may be using it, may be down | Setup effort, may differ from production |
| Best for | Post-deploy smoke, end-to-end, accessibility scans of real pages | Merge request checks, mocked dependencies |
| `BASE_URL` | `https://staging.example.com` | `http://app:8080` or `http://localhost:8000` |

Your tests should not care which one they hit. They read `BASE_URL`:

```python
import os
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
```

Line by line: `os.environ.get("BASE_URL", ...)` reads the variable and falls back to a local default if it is missing, so the same code works on your laptop. A post-deploy job overrides the variable:

```yaml
post-deploy-smoke:
  stage: smoke
  image: python:3.12-slim
  variables:
    BASE_URL: "https://staging.example.com"
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m smoke]
```

How variables are defined, scoped, protected and masked is the topic of the lesson after next; for now, treat `BASE_URL` as a plain environment variable.

### 10. Running faster: pytest-xdist and `parallel`

**Two levels of parallelism:**

1. **Inside one job (pytest-xdist):** `pytest -n auto` starts one worker process per CPU core and spreads tests across them.
2. **Across jobs (GitLab `parallel`):** the same job runs N times at once; each copy runs a slice of the tests.

```yaml
test:regression-xdist:
  stage: regression
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -n 4 -m "regression and not live"]
```

`-n 4` uses four workers. `-n auto` picks the CPU count; on shared runners that may be fewer than you expect, so a fixed number is more predictable. `pytest-xdist` must be in `requirements.txt`.

```yaml
test:regression-split:
  stage: regression
  image: python:3.12-slim
  parallel: 4
  before_script: [pip install -r requirements.txt]
  script:
    - pytest -q -m "regression and not live" --splits $CI_NODE_TOTAL --group $CI_NODE_INDEX
```

Line by line: `parallel: 4` creates four jobs named `test:regression-split 1/4` and so on. GitLab sets `CI_NODE_TOTAL` (4) and `CI_NODE_INDEX` (1 to 4) in each. The `--splits` and `--group` options come from the **pytest-split** plugin: it divides the tests into 4 groups, and each job runs only its group.

**Rules for safe parallelism:**

- Tests must be **independent**: no shared records, no dependence on order. Unique test data (for example, a random suffix on usernames) is the usual fix.
- Session-scoped fixtures run **once per worker** under xdist, so setup that must happen exactly once needs care.
- More workers is not always faster: a runner with 2 CPUs gains nothing from `-n 16`, and many workers hammering a small staging server can create flakiness.

### 11. Flaky tests: retry, quarantine, and not masking failures

**What:** A flaky test passes and fails on the same code.

**Why it is dangerous in CI:** People learn to press "Retry" and stop trusting red. Real bugs hide among the noise.

**Handling it, in order of preference:**

1. **Fix the cause.** Typical causes: shared data, fixed `sleep` instead of waiting for a condition, order dependence, an unstable third party (mock it), too much parallelism.
2. **Narrow retry** for known transient errors only, using `pytest-rerunfailures`:

```yaml
script:
  - pytest -q -m regression --reruns 1 --only-rerun ConnectionError
```

`--reruns 1` retries a failed test once. `--only-rerun ConnectionError` restricts that to failures matching the pattern. An `AssertionError` (a wrong answer from the product) is *not* retried, so real defects stay red.

3. **GitLab job `retry`** for infrastructure failures only:

```yaml
regression:
  stage: regression
  image: python:3.12-slim
  script: [pytest -q -m regression]
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

`retry.max` is the number of retries; `when` limits them to runner problems. A test that fails assertions is not retried by GitLab.

4. **Quarantine** a test you cannot fix immediately:

```python
@pytest.mark.quarantine
def test_search_suggestions():
    ...
```

```yaml
regression:
  stage: regression
  image: python:3.12-slim
  script: [pytest -q -m "regression and not quarantine"]

quarantine:
  stage: regression
  image: python:3.12-slim
  script: [pytest -q -m quarantine]
  allow_failure: true
```

The main job excludes quarantined tests; a separate job still runs them, with `allow_failure: true` so they show a warning instead of blocking. **Always attach a ticket and an owner**, otherwise quarantine becomes a graveyard.

**How retries mask failures:** If a test fails 1 time in 10 because of a genuine race condition in the product, three blanket retries make the pipeline green 99.9% of the time, and the bug ships. Retries are for *infrastructure*, not for *product behaviour*. Always look at which tests needed a retry (the log marks them `RERUN`) and treat them as to-do items.

### 12. Exit codes, timeouts, and quality gates

**Exit codes.** Every command ends with a number. GitLab runs each `script` line in order; the first non-zero exit code fails the job and stops that script. pytest's codes:

| Code | Meaning |
|---|---|
| 0 | All tests passed |
| 1 | Some tests failed |
| 2 | Run interrupted (for example, Ctrl+C) |
| 3 | Internal error |
| 4 | Command-line usage error (bad flag) |
| 5 | No tests collected (for example, a marker typo selects nothing) |

Code 5 is a quiet trap: a wrong `-m` expression selects zero tests and the job is red, which is good, because green with zero tests would be a lie.

**Timeouts.** A hung test can block a runner for an hour (the default job timeout). Set limits at three levels:

```yaml
test:api-smoke:
  stage: smoke
  image: python:3.12-slim
  timeout: 10 minutes
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m smoke]
```

- `timeout: 10 minutes` caps the whole job; exceeding it fails the job.
- In code, always pass a timeout to HTTP calls: `requests.get(url, timeout=10)`.
- Optionally use `pytest-timeout` (`--timeout=60`) to fail any single test that hangs.

**Quality gates.** A gate is a condition that must be true for the pipeline to proceed. All of them boil down to "exit non-zero when the condition is violated".

*Coverage threshold* with `pytest-cov`:

```yaml
script:
  - pytest -q -m "regression and not live" --cov=api --cov-fail-under=80
```

`--cov=api` measures coverage of the `api` package; `--cov-fail-under=80` makes pytest exit non-zero if coverage is below 80%. How to publish coverage in the merge request is covered in the next lesson.

*Zero critical accessibility violations*: either assert in the test itself, or check scan results in a script:

```python
# tests/accessibility/test_home.py
def test_home_has_no_critical_violations(page, axe_results):
    results = axe_results(page, "/")
    critical = [v for v in results["violations"] if v["impact"] == "critical"]
    assert critical == [], f"{len(critical)} critical a11y violations: {[v['id'] for v in critical]}"
```

Line by line: the fixtures `page` and `axe_results` (from Thursday) give a browser page and the axe results. The list comprehension keeps only violations with impact `critical`. The `assert` fails the test, and so the job, if the list is not empty, and the message names the offending rules so the log is self-explanatory.

*Blocking merges:* in the project, go to **Settings > Merge requests** and enable **Pipelines must succeed**. Now a red pipeline blocks the Merge button. Combine with a protected main branch so nobody can push directly around the gate.

*`allow_failure: true`* turns a job's failure into a warning. Use it only for experiments or quarantined tests, and review them on a schedule.

### 13. Reproducing a CI failure locally

When a test fails only in CI, do not guess. Run the **same image** locally:

```bash
docker run --rm -it \
  -v "$PWD":/work -w /work \
  -e BASE_URL="https://staging.example.com" \
  mcr.microsoft.com/playwright/python:v1.49.0-jammy \
  bash -c "pip install -r requirements.txt && pytest -q -m accessibility"
```

**Line by line:**

- `docker run` starts a container. `--rm` deletes it when it exits; `-it` gives an interactive terminal.
- `-v "$PWD":/work` mounts your current folder into the container at `/work`. `-w /work` makes that the working directory.
- `-e BASE_URL=...` sets the same environment variable the job uses.
- The image name is copied from the job's `image:` line, so you get the same OS, Python, and browsers.
- `bash -c "..."` runs the same commands as the job's `script`.

If it fails the same way, you can debug at your desk. If you drop `bash -c` and use `bash` alone, you get a shell inside the container to poke around. Typical discoveries: path case mismatches, a missing environment variable, a different Python version, or a dependency not pinned.

### 14. Common mistakes

1. **`localhost` for a service.** Use the service alias (`db`, `mock`, `app`).
2. **Fixed `sleep` instead of a health-wait.** Works until the runner is slow.
3. **Playwright version in `requirements.txt` differs from the image tag.** Browser not found.
4. **Blanket reruns** (`--reruns 3`) that hide real defects.
5. **Marker typo selecting zero tests** (and no `--strict-markers` to catch it).
6. **`allow_failure: true` left on forever**, so a failure nobody reads.
7. **Parallel tests sharing data** and corrupting each other.
8. **`|| true` at the end of a test command**, which forces exit code 0 and makes every failure green. Never do this.
9. **Hard-coded environment URLs** inside tests rather than `BASE_URL`.
10. **No job `timeout`** or request timeout, so one hung call holds a runner.
11. **Skipping the merge request gate** by not enabling *Pipelines must succeed*; a pipeline nobody must obey is only a suggestion.
12. **Windows-only assumptions:** backslash paths, case-insensitive imports, CRLF line endings in shell scripts.

### 15. Glossary

### Pipeline-ready
A test suite that runs unattended in a clean Linux container, takes its configuration from environment variables, and signals results through exit codes.

### Smoke test
A small, fast subset checking that the system is basically alive.

### Regression test
A broad set verifying that existing behaviour still works.

### Fail fast
Ordering and configuring a pipeline so cheap checks run first and a run stops soon after the first clear failure.

### Service container
An extra Docker container (database, mock, app) started alongside a job via `services:` and reached by hostname or alias.

### Health-wait
A polling loop that waits until a service responds before the tests begin.

### Ephemeral environment
An environment created for one pipeline run and discarded afterwards.

### Sharding / splitting
Dividing the test list into groups so several jobs each run a portion in parallel.

### Flaky test
A test that gives different results on the same code.

### Quarantine
Removing an unstable test from the gating run (while still running and tracking it separately) until it is fixed.

### Exit code
The number a command returns; 0 means success, anything else means failure.

### Quality gate
A rule (tests pass, coverage above N, zero critical violations) that must hold for the pipeline to succeed.

### 16. Practice exercises

**Exercise 1: Smoke job.** Write a job `test:smoke` that uses `python:3.12-slim`, installs requirements, and runs only smoke tests, stopping at the first failure. Make it run on merge requests and on the main branch.

<details><summary>Solution</summary>

```yaml
test:smoke:
  stage: test
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q --maxfail=1 -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

`--maxfail=1` gives fail-fast, `-m smoke` selects the subset, and the two rules restrict when the job exists.
</details>

**Exercise 2: Accessibility job with a health-wait.** Your app is built as an image `registry.example.com/team/app:latest` and exposes `/health` on port 8080. Write a job that runs it as a service named `app`, waits up to 60 seconds, then runs the accessibility tests with Playwright.

<details><summary>Solution</summary>

```yaml
test:a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  services:
    - name: registry.example.com/team/app:latest
      alias: app
  variables:
    BASE_URL: "http://app:8080"
  script:
    - pip install -r requirements.txt
    - |
      for i in $(seq 1 30); do
        curl -fs "$BASE_URL/health" > /dev/null && break
        echo "waiting for app..."; sleep 2
      done
    - pytest -q -m accessibility
```

The alias `app` becomes the hostname; `BASE_URL` uses it. The loop tries 30 times at 2-second intervals (60 seconds). If the app never becomes healthy, the loop ends and the tests fail with a clear connection error, which is acceptable; you could add `|| exit 1` after the loop to fail explicitly.
</details>

**Exercise 3: Nightly-only live tests.** Create a rule so a job `live-checks` runs `pytest -m live` only on a nightly schedule, and describe how to create the schedule.

<details><summary>Solution</summary>

```yaml
live-checks:
  stage: test
  image: python:3.12-slim
  before_script: [pip install -r requirements.txt]
  script: [pytest -q -m live]
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $SCHEDULE_TYPE == "nightly"
```

Create the schedule under **Build > Pipeline schedules > New schedule**: cron `0 2 * * *`, target branch `main`, variable `SCHEDULE_TYPE` = `nightly`. Without that variable the rule does not match, so manual or other scheduled pipelines will not run the live tests.
</details>

**Exercise 4: Flaky test policy.** A test `test_order_total` fails about 1 run in 8 with `AssertionError: expected 59.97 got 59.96`. A colleague proposes `--reruns 3`. Respond.

<details><summary>Solution</summary>

Refuse the blanket rerun. An `AssertionError` with different numbers is a product or test-logic problem (probably rounding or float arithmetic, or shared data), not a transient infrastructure error. Reruns would hide a real defect 99% of the time. Steps: reproduce locally in a loop (`pytest --count` or a shell `for`), inspect the calculation (use `Decimal`), fix the cause. If the fix cannot happen immediately, mark the test `@pytest.mark.quarantine`, link a ticket, and let the nightly quarantine job keep running it. If failures were `ConnectionError`, `--reruns 1 --only-rerun ConnectionError` would be appropriate.
</details>

### 17. Quiz

**Q1.** What does `pytest -q --maxfail=3 -m smoke` do?
a) Runs all tests quietly and stops after 3 seconds
b) Runs only tests marked `smoke`, with short output, and stops after 3 failures
c) Runs 3 smoke tests only
d) Retries each smoke test 3 times

**Q2.** In a job using `services: - name: postgres:16 alias: db`, how should your tests connect?
a) `localhost:5432`
b) `127.0.0.1:5432`
c) `db:5432`
d) `postgres.local:5432`

**Q3.** Your job log ends with "No tests ran" and pytest exit code 5. Most likely cause?
a) The API was down
b) The marker expression selected zero tests
c) A test timed out
d) Coverage was too low

**Q4.** Which retry setup is acceptable for gating a merge request?
a) `--reruns 5` on all tests
b) `|| true` after pytest
c) `--reruns 1 --only-rerun ConnectionError` plus GitLab `retry` limited to runner failures
d) `allow_failure: true` on every test job

**Q5.** What makes a red pipeline actually stop a merge?
a) Adding `needs: []`
b) Enabling **Pipelines must succeed** in merge request settings
c) Using `parallel: 4`
d) Setting `PYTHONUNBUFFERED`

<details><summary>Answers</summary>

1. **b.** `-q` is quiet output, `--maxfail=3` stops after 3 failures, `-m smoke` selects the marker.
2. **c.** Services are separate containers reached by alias, not `localhost`.
3. **b.** Exit code 5 means no tests were collected, typically a marker typo or wrong path.
4. **c.** Narrow retries for transient infrastructure and connection errors only; the others mask real failures.
5. **b.** The setting makes the Merge button unavailable until the pipeline passes.
</details>

---

## Summary

- A pipeline job is a `script` whose exit code decides pass or fail; make your suite **pipeline-ready** (env-driven config, headless, isolated, timeouts, Linux-safe) so it behaves identically everywhere.
- Run API and MCP tests on a Python image with `pip install -r requirements.txt` and `pytest -q --maxfail=N -m <marker>`; run Playwright + axe-core scans on the official Playwright image, matching the version in `requirements.txt`.
- Order stages cheap to expensive (lint, smoke, regression), and use `rules` to run smoke on merge requests, regression on main, and everything on nightly schedules.
- Use `services:` for databases, mocks, or the app itself, reach them by alias, and **poll for health** instead of sleeping. Choose deployed environments for realism and ephemeral ones for isolation; pass `BASE_URL`.
- Speed up with `pytest -n` and `parallel` splitting, but only with independent tests.
- Treat flakiness as a defect: fix first, retry only known transient errors, quarantine with a ticket, and never blanket-rerun assertions.
- Gates (exit codes, coverage threshold, zero critical accessibility violations, **Pipelines must succeed**) turn results into decisions. Reproduce failures with `docker run` using the job's image.
- Next: publishing JUnit and other reports and artifacts, then handling secrets and variables.

## Additional Resources

- GitLab Docs, *CI/CD YAML syntax reference* (`rules`, `services`, `parallel`, `retry`, `timeout`): https://docs.gitlab.com/ci/yaml/
- GitLab Docs, *Using services in CI/CD jobs*: https://docs.gitlab.com/ci/services/
- GitLab Docs, *Merge request pipelines and "Pipelines must succeed"*: https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/
- Playwright for Python, *Continuous Integration*: https://playwright.dev/python/docs/ci
- pytest documentation, *How to invoke pytest (exit codes) and markers*: https://docs.pytest.org/en/stable/how-to/usage.html
- pytest-xdist documentation: https://pytest-xdist.readthedocs.io/en/stable/
- pytest-rerunfailures: https://github.com/pytest-dev/pytest-rerunfailures
