# Artifacts and Reporting

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **job artifacts** are and how they differ from **cache** in purpose, lifetime, and direction.
- Configure the `artifacts` keyword: `paths`, `name`, `expire_in`, `when`, `exclude`, `untracked`, and `reports`.
- Pass artifacts between jobs with `needs` and `dependencies`, and download or browse them in the GitLab UI.
- Publish **JUnit XML** so GitLab shows the **Tests** tab and a merge request test summary.
- Produce a self-contained **pytest-html** report and publish it as an artifact.
- Measure coverage with **pytest-cov / coverage.py** and surface it with the `coverage:` regex and `reports: coverage_report`.
- Save and summarise **accessibility (axe) results** as artifacts.
- Publish HTML reports with **GitLab Pages**, and know where **Allure** fits.
- Capture screenshots, traces, and logs on failure, and read a failed job log efficiently.
- Control retention and storage cost, and design reporting that serves developers, QEs, and stakeholders.

---

## Why This Matters

This is the final piece of the Week 7 epic. During the week you built an API test suite (Monday to Wednesday), added accessibility scans (Thursday), and put both into a GitLab CI/CD pipeline (earlier today). The pipeline runs your tests automatically. But a pipeline run is **ephemeral**: the container that executed your tests is deleted seconds after the job ends. If a test failed at 2 a.m., the only evidence left is whatever you **saved on purpose**.

Imagine the alternative. A developer opens a red pipeline, sees "pytest exited with code 1", and has to re-run it and hope the failure repeats. Now imagine the same failure with a Tests tab that names the failing test, the assertion message, the HTTP request and response, and a downloadable HTML report. The first is a mystery; the second is a five-minute fix.

Reporting is also how quality becomes **visible**. Managers do not read pytest output. They want to know: is it safe to release? Are accessibility problems going down? Which tests are flaky? Artifacts and reports answer those questions. Publishing the reports from your Project 2 pipeline is the last milestone of the week, and the habits here (always save evidence, keep it small, never leak secrets) apply to every pipeline you will ever work on.

---

## The Concept

### 1. What Is an Artifact?

An **artifact** is a file or directory that a job **uploads to GitLab** when it finishes. GitLab stores it (as a zip) and attaches it to that job. From there it can be:

- **downloaded or browsed** by people from the job or pipeline page,
- **passed to later jobs** in the same pipeline,
- **parsed by GitLab** when declared under `reports:`, which powers UI features such as the Tests tab.

Typical QE artifacts:

| Artifact | Produced by | Used for |
|----------|-------------|----------|
| `junit.xml` | `pytest --junitxml` | Test summary in GitLab |
| `report.html` | `pytest-html` | Human-readable result page |
| `coverage.xml`, `htmlcov/` | `pytest-cov` | Coverage reports |
| `accessibility/*.json` | axe scans | Evidence, trends, thresholds |
| `screenshots/`, `traces/*.zip` | Playwright | Visual debugging |
| `test.log` | Python logging | The HTTP trail of a failed test |

**Why it exists:** the runner is thrown away after each job. Artifacts are the bridge between "the job ran somewhere temporary" and "a human can look at the result tomorrow".

### 2. Artifacts Versus Cache

Beginners confuse these constantly because both involve "saving files between jobs". They solve different problems.

| | **Artifacts** | **Cache** |
|---|---------------|-----------|
| **Purpose** | Keep and share **results** (reports, builds, logs) | Make pipelines **faster** by reusing downloads (pip packages, `node_modules`) |
| **Lifetime** | Kept until `expire_in` (default 30 days on GitLab.com); the latest successful ones can be kept longer | Best effort; can be evicted or missing at any time |
| **Direction** | Job **uploads to GitLab**; later jobs and people **download from GitLab** | Runner **restores before** the job and **saves after**, shared across pipelines on the same branch/key |
| **Reliability** | Dependable within a pipeline | Never rely on it; your job must work with an empty cache |
| **Who sees it** | People in the UI and later jobs | Only jobs; no UI |

A concrete example in your pipeline:

```yaml
api-regression:
  stage: test
  cache:
    key: pip-$CI_COMMIT_REF_SLUG
    paths:
      - .cache/pip
  script:
    - pip install --cache-dir .cache/pip -r requirements.txt
    - pytest --junitxml=reports/junit.xml
  artifacts:
    when: always
    paths:
      - reports/
```

Line by line:

- `cache:` starts the cache block. It only exists to save time.
- `key: pip-$CI_COMMIT_REF_SLUG` gives each branch its own cache, so branches do not overwrite each other.
- `paths: [.cache/pip]` is the folder pip downloads into. Next run, packages are already there.
- `pip install --cache-dir .cache/pip` tells pip to use that folder.
- `pytest --junitxml=reports/junit.xml` writes the results file. This is a **result**, not a speed-up.
- `artifacts:` starts the block that uploads results. `when: always` and `paths: [reports/]` mean "upload the reports folder whether tests pass or fail".

**Rule of thumb:** if a person or a later job needs the file, it is an **artifact**. If you only want installs to be faster, it is a **cache**.

### 3. The `artifacts` Keyword Step by Step

Start with the smallest useful example, then add options.

```yaml
api-regression:
  stage: test
  script:
    - mkdir -p reports
    - pytest -m regression --junitxml=reports/junit.xml
  artifacts:
    paths:
      - reports/
```

- `script` first creates the `reports` folder so the path always exists, then runs pytest and writes the XML into it.
- `artifacts: paths:` lists what to upload. Paths are relative to the project directory (`$CI_PROJECT_DIR`) and must be inside it.

This already works, but only when the job **passes**. Now the full version with every option from this lesson:

```yaml
api-regression:
  stage: test
  script:
    - mkdir -p reports logs
    - pytest -m regression --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
  artifacts:
    name: "api-regression-$CI_COMMIT_SHORT_SHA"
    when: always
    expire_in: 14 days
    paths:
      - reports/
      - logs/
    exclude:
      - reports/**/*.tmp
    reports:
      junit: reports/junit.xml
```

| Option | What it does | Notes |
|--------|--------------|-------|
| `name` | Name of the downloaded zip | Variables allowed; makes downloads identifiable, for example `api-regression-a1b2c3d.zip` |
| `when` | When to upload | `on_success` (default), `on_failure`, `always` |
| `expire_in` | How long GitLab keeps it | `1 hour`, `7 days`, `1 week`, `never` |
| `paths` | Files or folders to upload | Globs allowed, such as `reports/**/*.json` |
| `exclude` | Patterns to leave out of `paths` | Useful to skip temp files and caches |
| `untracked` | `true` uploads every file Git does not track | Convenient but risky (see below) |
| `reports` | Special artifact types GitLab understands | `junit`, `coverage_report`, and more |
| `expose_as` | Label for a link in the merge request | Needs `paths`; handy for HTML reports |

#### 3.1 `when`: the most important setting

By default artifacts upload **only if the job succeeds**. For test reports that is backwards: you need them **most when tests fail**, and a failing pytest run makes the job fail.

| Value | Uploads when | Use for |
|-------|--------------|---------|
| `on_success` (default) | Job passes | Build outputs needed by later jobs |
| `on_failure` | Job fails | Screenshots, traces, debug dumps you only want when something broke |
| `always` | Pass or fail | Test reports (JUnit, HTML, coverage, axe JSON) |

You can use two artifact strategies by splitting paths across jobs, but within one job there is only one `when`. The simple, safe habit: **test jobs use `when: always`.**

#### 3.2 `untracked`, `exclude`, and `name`

`untracked: true` uploads everything new that is not in Git, including `.venv/`, caches, and sometimes secrets files. Prefer explicit `paths`. If you do use it, combine it with `exclude`:

```yaml
artifacts:
  untracked: true
  exclude:
    - .venv/**/*
    - .cache/**/*
```

Using a `name` with `$CI_COMMIT_SHORT_SHA` or `$CI_JOB_NAME` makes a pile of downloaded zips easy to tell apart. Without it every download is called `artifacts.zip`.

#### 3.3 Passing artifacts between jobs: `needs` and `dependencies`

By default, a job downloads the artifacts of **all jobs from earlier stages**. That is convenient but wasteful. Two keywords let you be precise.

```yaml
generate-data:
  stage: build
  script:
    - python tools/make_testdata.py
  artifacts:
    paths:
      - testdata/generated/
    expire_in: 1 day

api-regression:
  stage: test
  needs:
    - job: generate-data
      artifacts: true
  script:
    - pytest -m regression

a11y-summary:
  stage: report
  dependencies:
    - a11y-scan
  script:
    - python tools/a11y_summary.py reports/accessibility
```

Line by line:

- `generate-data` runs in the `build` stage and writes data files, which it saves as an artifact for one day.
- `needs: - job: generate-data, artifacts: true` in `api-regression` means: start as soon as `generate-data` finishes (do not wait for the whole stage) **and** download its artifacts. `artifacts: false` would order the jobs but skip the download.
- `dependencies: [a11y-scan]` in `a11y-summary` limits downloading to the named job's artifacts. `dependencies: []` downloads nothing.
- Difference in one line: `needs` controls **order and speed** (and downloads artifacts by default); `dependencies` only controls **which artifacts to download** and does not change order.

Real-world scenario: your parallel API and accessibility jobs each write reports; a final `report` job lists both in `needs` so it only starts when both are done and gets both sets of files.

#### 3.4 Retention and storage cost

Artifacts consume storage, and storage is limited per project or group and often billed. Choose retention by value:

| Artifact | Suggested retention |
|----------|---------------------|
| Merge request pipeline reports | 7-14 days |
| Main branch or nightly reports | 30-90 days |
| Release evidence for audit | Keep, or copy to long-term storage |
| Videos and traces | 3-7 days |

GitLab keeps the **latest successful artifacts** per ref by default, and you can click **Keep** on a job to cancel its expiry. Never set `expire_in: never` casually.

### 4. Finding Artifacts in the GitLab UI

1. Open **Build > Pipelines** and click the pipeline.
2. Click a job. On the right side of the job page you see **Download**, **Browse**, and **Keep**.
3. **Download** gives you the zip. **Browse** lets you click through folders and open files such as `reports/report.html`. JavaScript-heavy pages can be restricted when browsed, so for rich reports download them or use GitLab Pages.
4. On the pipeline page, the **download icon** lists artifacts of every job.
5. If you set `expose_as`, the merge request shows a labelled link to the file.

For scripts and dashboards you can use the API:

```bash
curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/jobs/artifacts/main/download?job=api-regression" \
  --output artifacts.zip
```

This downloads the latest artifacts of the job `api-regression` on branch `main`. The token is a secret; storing it is the topic of the next lesson (secrets and variables).

### 5. JUnit XML and the Tests Tab

**JUnit XML** is a standard format describing test results: names, durations, pass/fail/skip, and the failure message. GitLab parses it and shows results in its own UI, so people do not have to scroll through raw logs.

#### 5.1 Producing it

```bash
pytest --junitxml=reports/junit.xml
```

A trimmed output:

```xml
<testsuites>
  <testsuite name="pytest" errors="0" failures="1" skipped="0" tests="42" time="12.3">
    <testcase classname="tests.api.test_users" name="test_create_user[missing-name]" time="0.21">
      <failure message="assert 201 == 400">...traceback...</failure>
    </testcase>
  </testsuite>
</testsuites>
```

- `<testsuite ...>` summarises the run: 42 tests, 1 failure, 12.3 seconds.
- `<testcase>` is one test, with its class, name (including the parametrize id in brackets), and duration.
- `<failure message=...>` holds the assertion message and traceback. This is why the descriptive assertion messages from Tuesday matter: they appear here.

#### 5.2 Publishing it

```yaml
artifacts:
  when: always
  reports:
    junit: reports/junit.xml
```

You can give several files or wildcards:

```yaml
artifacts:
  when: always
  reports:
    junit:
      - reports/junit-api.xml
      - reports/junit-a11y.xml
```

`reports: junit` does two things: the file is uploaded like any artifact, **and** GitLab parses it. Note that it uses the path of the file in the job, and `when: always` is again essential.

#### 5.3 What you see in GitLab

- A **Tests** tab on the pipeline page lists suites and each test with status and duration.
- Failed tests show the **failure message and stack trace** inline.
- The merge request has a **test summary widget**, for example "2 failed and 40 passed tests".
- GitLab compares against the target branch, so reviewers can see **new failures** versus failures that already existed.

Optionally name the suite in `pytest.ini`:

```ini
[pytest]
junit_family = xunit2
junit_suite_name = project2-api
```

`xunit2` is the modern, widely compatible JUnit flavour; the suite name makes the Tests tab readable when several jobs report.

### 6. HTML Reports with pytest-html

JUnit is for GitLab; a **human-readable HTML page** is for everyone else.

```bash
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

`--self-contained-html` embeds CSS and JavaScript in the single file. Without it the report references separate asset files that are missing once the file is downloaded or opened from the artifact browser, and the page looks broken.

Add useful context (environment, commit, pipeline link) in `conftest.py`:

```python
import os

def pytest_html_report_title(report):
    report.title = f"Project 2 API tests: {os.getenv('TEST_ENV', 'local')}"

def pytest_metadata(metadata):
    metadata["Environment"] = os.getenv("TEST_ENV", "local")
    metadata["Commit"] = os.getenv("CI_COMMIT_SHORT_SHA", "local")
    metadata["Pipeline"] = os.getenv("CI_PIPELINE_URL", "local")
```

- `pytest_html_report_title` is a hook that sets the page title.
- `pytest_metadata` adds rows to the "Environment" table at the top of the report.
- `os.getenv("CI_COMMIT_SHORT_SHA", "local")` reads a predefined GitLab variable and falls back to `"local"` on your laptop.
- Never put tokens or passwords in metadata; the report is a file anyone with access can open.

Publish it:

```yaml
api-regression:
  script:
    - pytest --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
  artifacts:
    when: always
    expose_as: "API HTML report"
    paths:
      - reports/report.html
      - reports/junit.xml
    reports:
      junit: reports/junit.xml
```

`expose_as` places a clickable "API HTML report" link in the merge request widget. It needs `paths` and works for merge request pipelines.

### 7. Coverage with pytest-cov and coverage.py

**Coverage** measures which lines of code ran while the tests executed. `pytest-cov` is the pytest plugin that drives **coverage.py**, the underlying tool. In a QE project, coverage most usefully measures **your framework code** (API client, helpers) rather than the application under test.

```bash
pip install pytest-cov
pytest --cov=api --cov=utils --cov-report=term --cov-report=xml:reports/coverage.xml --cov-report=html:reports/htmlcov
```

- `--cov=api --cov=utils` says which packages to measure.
- `--cov-report=term` prints a table in the log (including a `TOTAL` line).
- `--cov-report=xml:...` writes **Cobertura XML**, a format GitLab reads.
- `--cov-report=html:...` writes a browsable folder where you can click each file and see missed lines in red.

Now connect it to GitLab:

```yaml
test:framework-unit:
  stage: test
  script:
    - pytest -m "unit or mocked" --cov=api --cov=utils --cov-report=term --cov-report=xml:reports/coverage.xml --cov-report=html:reports/htmlcov
  coverage: '/TOTAL.*\s+(\d+(?:\.\d+)?)%/'
  artifacts:
    when: always
    paths:
      - reports/htmlcov/
    reports:
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml
```

Line by line:

- `-m "unit or mocked"` runs only fast tests that do not need a live API, which suits a coverage job.
- `coverage:` is a **regular expression** GitLab applies to the job log. The part in parentheses is captured as the percentage. For a log line like `TOTAL    480    48    90%` it captures `90`. This number appears on the job, in pipeline lists, and can power a coverage **badge** and trend graph.
- `reports: coverage_report` with `coverage_format: cobertura` uploads the XML so GitLab can show **line-by-line coverage in the merge request diff** (green and red gutter marks on changed lines) so reviewers see whether new code is tested.
- `paths: [reports/htmlcov/]` also keeps the human-browsable HTML.

Treat coverage as a **diagnostic, not a goal**. 100% coverage does not mean good assertions, and chasing the number invites meaningless tests. A low number simply points at code nobody tests.

### 8. Accessibility Reports

Thursday's axe scans produce one JSON file per page. Raw JSON is great evidence but hard to read, so do both: **keep the raw files** and **generate a summary**.

```python
# tools/a11y_summary.py
import json, sys
from pathlib import Path

folder = Path(sys.argv[1])
rows = []
for f in sorted(folder.glob("*.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    by_impact = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    for v in data["violations"]:
        by_impact[v.get("impact") or "minor"] += len(v["nodes"])
    rows.append((f.stem, by_impact))

html = ["<html><body><h1>Accessibility summary</h1><table border=1 cellpadding=6>",
        "<tr><th>Page</th><th>Critical</th><th>Serious</th><th>Moderate</th><th>Minor</th></tr>"]
for page, c in rows:
    html.append(f"<tr><td>{page}</td><td>{c['critical']}</td><td>{c['serious']}</td>"
                f"<td>{c['moderate']}</td><td>{c['minor']}</td></tr>")
html.append("</table></body></html>")
Path("reports").mkdir(exist_ok=True)
Path("reports/a11y-summary.html").write_text("\n".join(html), encoding="utf-8")
print("Wrote reports/a11y-summary.html")
```

Line by line:

- `folder = Path(sys.argv[1])` takes the folder of JSON files from the command line.
- The loop reads each page's axe result. axe stores problems under `violations`; each violation has an `impact` and a list of affected `nodes` (elements).
- `by_impact` counts **elements** per severity. `v.get("impact") or "minor"` avoids a crash when impact is missing.
- The next loop builds a simple HTML table, one row per page.
- The last lines make sure `reports/` exists and write the file.

The job that runs it:

```yaml
a11y-summary:
  stage: report
  needs:
    - job: a11y-scan
      artifacts: true
  when: always
  script:
    - python tools/a11y_summary.py reports/accessibility
  artifacts:
    when: always
    expose_as: "Accessibility summary"
    paths:
      - reports/a11y-summary.html
      - reports/accessibility/
    expire_in: 30 days
```

`when: always` at **job** level means "run this job even if earlier jobs failed" (otherwise a failed scan would skip the summary, the one time you need it). `needs` with `artifacts: true` downloads the scan JSON. The summary and the raw JSON are both kept. Since each page is already its own parametrized test, scan failures also appear in the Tests tab.

### 9. GitLab Pages for Publishing HTML Reports

The artifact browser is fine for quick looks, but **GitLab Pages** gives you a real, always-available URL. A special job named **`pages`** publishes the contents of a folder called **`public/`** as a static website.

```yaml
pages:
  stage: report
  needs:
    - job: api-regression
      artifacts: true
  script:
    - mkdir -p public
    - cp reports/report.html public/index.html
    - cp reports/a11y-summary.html public/a11y.html
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Line by line:

- The job name `pages` is what triggers the Pages deployment.
- `needs` pulls in the report files from the test job.
- The script collects reports into `public/`; `index.html` becomes the site home page.
- `artifacts: paths: [public]` is required; Pages publishes that folder.
- `rules` limits publishing to the default branch, so the site always shows the latest main-branch results.

Find the site URL under **Deploy > Pages**. Pages can be limited to project members, but treat anything published as visible to its whole audience: do not publish reports containing secrets or real personal data.

### 10. Allure (Awareness)

**Allure Report** (`allure-pytest`) turns result files into a rich interactive site: steps, attachments, categories of failures, and **history and trends** across runs. You run tests with `--alluredir=allure-results`, generate the site with the Allure command line tool, and publish it with Pages. It needs more setup than pytest-html and extra storage to keep history, so for this course know it exists and when to reach for it: teams that want trend charts and polished stakeholder reports. Newman (Postman's runner) can also emit JUnit with `--reporters cli,junit`, so Monday's collection can feed the same Tests tab.

### 11. Evidence on Failure: Screenshots, Traces, and Logs

Nobody can "just look at the screen" in CI. Capture evidence **automatically when a test fails**.

#### 11.1 Playwright screenshots and traces

```bash
pytest -m accessibility --screenshot only-on-failure --tracing retain-on-failure --output reports/playwright
```

- `--screenshot only-on-failure` saves an image only when a test fails.
- `--tracing retain-on-failure` records every action, network call, and DOM snapshot but **keeps** the trace zip only for failed tests.
- `--output reports/playwright` sets the folder, which you then include in `artifacts: paths`.
- Open a downloaded trace locally with `playwright show-trace trace.zip` to step through the failure like a recording.

#### 11.2 Logs

```ini
[pytest]
log_file = reports/test.log
log_file_level = DEBUG
```

This writes the full debug log (including your API client's request lines) to a file you save as an artifact.

#### 11.3 Reading a failed job log

When a job is red, read in this order:

1. **Scroll to the bottom** for the exit code and the line that failed (`ERROR: Job failed: exit code 1`).
2. Go **up** to pytest's `FAILURES` section: test name, the failing assertion, and the values compared.
3. Check the **setup** at the top: did `pip install` fail, was a variable missing, was the base URL wrong? Those are pipeline problems, not test bugs.
4. If the log is not enough, download the artifacts (HTML report, trace, JSON).
5. Distinguish **test failure** (assertion), **infrastructure failure** (runner, network, timeout), and **flaky** (passes on retry). Each has a different owner.

#### 11.4 Notifications

Failures should find people. GitLab emails the pipeline author on failure by default, and you can configure Slack or email integrations under **Settings > Integrations**. Keep notifications meaningful (failures on main, nightly runs) so they are not ignored.

### 12. Reporting for Different Audiences and Trends

| Audience | Needs | Delivered by |
|----------|-------|--------------|
| **Developer** | Which test failed, why, how to reproduce | MR test summary, failure message, logs, traces |
| **QE** | Trends, flaky tests, suite health, evidence | HTML or Allure reports, JUnit history, artifacts |
| **Manager/Product** | Pass rate, release readiness, accessibility status | One-page Pages summary, coverage badge |
| **Auditor** | Proof of what was tested for a release | Long-retention artifacts |

Good stakeholder reports are **short and trended**: pass rate this week versus last, count of critical accessibility violations by release, top flaky tests, and coverage direction. A number without a trend is hard to act on. Start simple: a Pages page regenerated every night, and a badge in the README.

### 13. Security and Storage Hygiene

- **Mask secrets** (Authorization headers, tokens, cookies) before logging or writing to reports.
- Use **synthetic test data**, never real personal data.
- Use **short expiry** for traces, videos, and logs.
- Keep artifacts **small**: capture only on failure, avoid whole-folder uploads, compress big files.
- Remember that artifacts and Pages are readable by anyone with access to the project or site.

### 14. Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Forgetting `when: always` | Failed run has no report; the one time you need it is lost | Add `when: always` to test jobs |
| Wrong path | "WARNING: No files to upload" | Check relative paths; `mkdir -p` the folder; confirm where the tool writes |
| `reports: junit` path wrong | Tests tab empty | Make sure the file exists and matches the path exactly |
| Huge artifacts | Storage quota hit, slow downloads | Short `expire_in`, failure-only capture, `exclude` |
| `untracked: true` everywhere | Uploads venvs and secrets | Use explicit `paths` |
| Parallel jobs overwrite files | Only one shard's results survive | Use `$CI_NODE_INDEX` or `$CI_JOB_NAME` in file names |
| HTML looks broken | Missing CSS/JS | `--self-contained-html` or Pages |
| Later job lacks files | Not in `needs`/`dependencies`, or artifacts expired | Declare them; check `expire_in` |
| Secrets in reports | Token visible in a log or report | Mask at the source; delete the job artifacts |

### 15. Glossary

### Artifact
A file or folder a job uploads to GitLab after it finishes.

### Cache
Runner-side storage reused across jobs to speed up installs; not guaranteed.

### `expire_in`
How long GitLab keeps an artifact before deleting it.

### `when: always`
Upload artifacts even if the job failed.

### `needs`
Declares job order and, by default, downloads artifacts from the listed jobs.

### `dependencies`
Restricts which earlier jobs' artifacts a job downloads.

### JUnit XML
Standard test result format that GitLab turns into the Tests tab.

### Cobertura
XML coverage format GitLab reads for diff coverage.

### Coverage regex
The `coverage:` pattern GitLab applies to the job log to extract a percentage.

### GitLab Pages
Static site hosting from a `pages` job that publishes `public/`.

### Trace
Playwright's recording of a test (actions, network, snapshots) as a zip.

### Allure
A rich reporting framework with history and trends.

### 16. Practice Exercises

#### Exercise 1: Make failures visible
Add JUnit output and artifacts to an API job, force one test to fail, and find the failure in the pipeline's Tests tab.

**Solution:**

```yaml
api-regression:
  stage: test
  script:
    - mkdir -p reports
    - pytest -m regression --junitxml=reports/junit.xml
  artifacts:
    when: always
    paths:
      - reports/
    reports:
      junit: reports/junit.xml
```

Change one expected status code in a test so it fails, push, open the pipeline, and click **Tests**. The failing test appears with its message. Without `when: always` the Tests tab would be empty because the job failed.

#### Exercise 2: Artifact or cache?
For each item say whether it should be an artifact or a cache: (a) `.cache/pip`, (b) `reports/junit.xml`, (c) `testdata/generated/`, consumed by the next stage, (d) `node_modules` for a Playwright helper.

**Solution:** (a) cache, speed-up only. (b) artifact, a result people need. (c) artifact, a later job depends on it, so it must be reliable. (d) cache, it can be re-downloaded if missing.

#### Exercise 3: Pass data and limit downloads
Write two jobs: `seed` produces `data/users.json` for one day; `regression` starts right after `seed` and receives the file. A third job `report` should download only the artifacts of `regression`.

**Solution:**

```yaml
seed:
  stage: build
  script:
    - mkdir -p data
    - python tools/seed.py > data/users.json
  artifacts:
    paths: [data/]
    expire_in: 1 day

regression:
  stage: test
  needs:
    - job: seed
      artifacts: true
  script:
    - pytest -m regression --junitxml=reports/junit.xml
  artifacts:
    when: always
    paths: [reports/]

report:
  stage: report
  when: always
  dependencies:
    - regression
  script:
    - python tools/summarise.py
```

`needs` gives order plus download; `dependencies` limits downloads for `report`.

#### Exercise 4: Publish an HTML report with coverage
Produce a self-contained pytest-html report, a coverage percentage on the job, and publish the report on Pages for the default branch.

**Solution:**

```yaml
test:framework-unit:
  stage: test
  script:
    - mkdir -p reports
    - pytest -m unit --cov=api --cov-report=term --cov-report=xml:reports/coverage.xml --html=reports/report.html --self-contained-html
  coverage: '/TOTAL.*\s+(\d+(?:\.\d+)?)%/'
  artifacts:
    when: always
    paths: [reports/]
    reports:
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml

pages:
  stage: report
  needs:
    - job: test:framework-unit
      artifacts: true
  script:
    - mkdir -p public
    - cp reports/report.html public/index.html
  artifacts:
    paths: [public]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Check the coverage percentage on the job page and open the Pages URL under **Deploy > Pages**.

### 17. Quiz

**Q1.** Your tests fail and the job is red, but there are no artifacts. What is the most likely cause?
**Q2.** Which one is guaranteed to be available to a later job in the same pipeline: artifact or cache?
**Q3.** What does the `coverage:` keyword do?
**Q4.** What must a job be named, and which folder must it publish, to deploy GitLab Pages?
**Q5.** Name two ways to keep a Playwright trace from filling storage.

**Answers:**

1. The artifacts block lacks `when: always` (or `on_failure`), so artifacts upload only on success.
2. Artifact. Cache is best effort.
3. It gives GitLab a regular expression to extract the coverage percentage from the job log, shown on the job, badge, and trends.
4. The job is named `pages` and publishes the `public/` folder as an artifact.
5. Use `--tracing retain-on-failure` so only failures are kept, and set a short `expire_in` (also `exclude` unneeded files).

---

## Summary

- **Artifacts** are results uploaded to GitLab for people and later jobs; **cache** is a best-effort speed-up that downloads and restores on the runner.
- Configure `paths`, `name`, `expire_in`, `exclude`, and above all `when: always` so failed runs keep their evidence. Use `needs` and `dependencies` to pass only what each job requires.
- `reports: junit` produces the Tests tab and MR summary; `coverage:` and `coverage_report` show percentages and diff coverage.
- pytest-html (self-contained), axe summaries, and Pages make results readable; Allure adds history when needed.
- Capture screenshots, traces, and logs on failure, read logs from the bottom up, and keep retention short and artifacts small.
- Report for your audience with trends, and never leak secrets. How to store tokens and variables safely is the next lesson.

## Additional Resources

- GitLab Docs, *Job artifacts*: https://docs.gitlab.com/ci/jobs/job_artifacts/
- GitLab Docs, *Unit test reports*: https://docs.gitlab.com/ci/testing/unit_test_reports/
- GitLab Docs, *Code coverage*: https://docs.gitlab.com/ci/testing/code_coverage/
- GitLab Docs, *GitLab Pages*: https://docs.gitlab.com/user/project/pages/
- pytest-html documentation: https://pytest-html.readthedocs.io/
- coverage.py documentation: https://coverage.readthedocs.io/
- Allure Report documentation: https://allurereport.org/docs/
