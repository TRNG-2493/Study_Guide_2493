# Build-Test-Deploy Lifecycle

## Learning Objectives

By the end of this lesson you will be able to:

- Describe each phase of the lifecycle (source, build, test, package, release, deploy, operate/monitor) and say what a QE contributes in each.
- Explain what "build" means for Python, Node, and Docker applications.
- Explain "build once, deploy many" and why artifacts must be immutable and versioned (semver and commit SHA).
- Layer tests (unit, API, accessibility, smoke) and order them to fail fast.
- Describe environments (dev, staging, production), promotion, and per-environment configuration.
- Compare deployment strategies (recreate, rolling, blue-green, canary, feature flags) and explain rollback.
- Explain manual approval gates, post-deploy health checks, and how to handle pipeline failures.
- Write a simple Python health-check script and trace a small API service end to end.

---

## Why This Matters

This week you built API tests (Monday to Wednesday), accessibility scans with axe (Thursday), and on Friday you met the idea of CI/CD in the earlier concepts lesson. The week's epic is: **turn the tests you wrote into an automated quality gate that protects every release.**

A pipeline is just the lifecycle written down as automation. If you do not understand the lifecycle, you cannot decide *which check belongs where*. Put a 30-minute browser suite first and developers wait half an hour to learn they forgot a semicolon. Put your API tests after the production deploy and customers find the bugs for you. Rebuild the software separately for each environment and you may ship something nobody tested.

Think of a restaurant kitchen. Ingredients arrive (source), get prepared (build), the chef tastes the dish (test), it is plated (package), the head chef approves it (release), a waiter carries it to the table (deploy), and someone watches whether the customer enjoys it (operate/monitor). A tasting spoon before plating is cheap; a complaint at the table is expensive. The lifecycle is the same idea for software, and the QE is the person who decides where the tasting spoons go.

The next Friday lessons turn this into real pipeline files. Today is about thinking: what happens, in what order, and why.

---

## The Concept

### 1. The Lifecycle at a Glance

```
 Source -> Build -> Test -> Package -> Release -> Deploy -> Operate/Monitor
 (commit)  (deps,   (unit,   (image,    (version,  (dev,     (health, logs,
           lint,    API,     archive)   approve)   staging,   alerts)
           compile) a11y,                           prod)
                    smoke)
   ^                                                              |
   +------------------- feedback to the team <--------------------+
```

Each arrow is a **gate**: the work only moves forward if the previous phase succeeded. Each phase answers one question:

| Phase | Question it answers |
|-------|--------------------|
| Source | What exact change are we looking at? |
| Build | Can this code be turned into something runnable? |
| Test | Does it behave correctly and accessibly? |
| Package | Can we produce one deployable, versioned thing? |
| Release | Is this specific version approved to go out? |
| Deploy | Is it running in the target environment? |
| Operate/Monitor | Is it still healthy now that real traffic is using it? |

The most important idea: **cost of a defect rises the later you find it**. A failing lint check costs seconds. A failing API test costs minutes. A bug in production costs customers, money, and an incident meeting. Good lifecycle design pushes detection as early (left) as possible.

### 2. Phase 1: Source

Everything starts with a commit in version control. A **trigger** is the event that starts the lifecycle: a push, a merge request being opened, a merge to `main`, a schedule (nightly), a tag such as `v1.4.0`, or a manual click.

What belongs in the repository:

- application code,
- **test code** and test data (yes, your API and axe tests live with the project),
- the pipeline definition,
- configuration templates (never real secrets),
- documentation.

What does not belong: passwords, API tokens, virtual environments, generated reports, `node_modules`. Use `.gitignore`.

QE contribution: insist on merge requests for `main`, so every change passes through the pipeline before it lands.

### 3. Phase 2: Build

**Build** turns source into something runnable and checks it is structurally sound. The word means different things for different technologies, so let us look at three.

**Python.** Python is interpreted, so there is no compile step, but a build still has real work:

1. Create a clean environment (a virtual environment or container).
2. **Install dependencies** from a pinned file: `pip install -r requirements.txt`.
3. **Lint and static checks**: `ruff check .` or `flake8`, optionally `mypy` for types.
4. **Check the code imports**: `python -m compileall src` or `pytest --collect-only -q`.
5. Optionally build a wheel (`python -m build`).

**Node.** Similar, with different tools:

1. `npm ci` (clean install exactly from `package-lock.json`; prefer it over `npm install` in pipelines).
2. `npm run lint`.
3. `npm run build` (this may transpile TypeScript or bundle front-end code).

**Docker.** For containerised apps the build produces an image:

1. Write a `Dockerfile` that describes the base image, copies the code, installs dependencies, and defines the start command.
2. `docker build -t myapi:1.4.0 .`.
3. Optionally scan the image for known vulnerabilities.

Here is a small Dockerfile for a Python API, explained line by line:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV APP_VERSION=unset
CMD ["python", "-m", "src.main"]
```

- `FROM python:3.12-slim` picks a small base image with Python already installed. Pin the version; never rely on an untagged "latest".
- `WORKDIR /app` sets the folder inside the image where later commands run.
- `COPY requirements.txt .` copies only the dependency list first. Docker caches each step, so when only your code changes, the slow dependency install is reused.
- `RUN pip install ...` installs dependencies while building the image. `--no-cache-dir` keeps the image smaller.
- `COPY src/ ./src/` copies the application code after the dependencies, for the caching reason above.
- `ENV APP_VERSION=unset` declares a variable that the build or deploy will set, so the running service can report its own version.
- `CMD [...]` is the command that starts the service when a container runs.

A good build has three properties:

- **Reproducible**: same inputs give the same output. Pin dependency versions.
- **Automated**: no one types commands by hand.
- **Fast**: it runs on every change, so seconds matter.

Build also includes **versioning** the result (covered in section 5).

QE contribution: your test project also gets built. Installing its dependencies, linting, and running `pytest --collect-only` catches import errors and typos in seconds, before any test hits an API.

### 4. Phase 3: Test (Layering and Fail-Fast Ordering)

Tests run in **layers**. The test pyramid says: many fast, cheap tests at the bottom; few slow, expensive ones at the top. In this week's work the layers look like this:

| Layer | What it checks | Typical speed | Runs |
|-------|---------------|---------------|------|
| Static checks | Lint, imports, formatting | seconds | every push |
| **Unit** | One function or class, dependencies mocked | seconds | every push |
| **API** | Endpoints: status codes, JSON schema, auth, errors | 1-10 min | every merge request |
| **Accessibility** | axe scans of rendered pages, WCAG rules | 2-10 min | merge request and main |
| **Smoke** | A tiny set of critical checks on a running deployment | under 2 min | after every deploy |

Smoke is slightly different from the others: it is not a layer of the pyramid but a **purpose**. A smoke test can be an API test or a UI test; what makes it smoke is that it is small, critical, and answers "is this deployment alive and sane?".

**Fail-fast ordering.** Order jobs so that the cheapest, fastest, most informative run first. If lint fails in 10 seconds, there is no reason to start a 20-minute regression. A typical order:

1. lint and static checks,
2. unit tests,
3. build the artifact,
4. API tests (against a started copy of the service),
5. accessibility scans,
6. deploy to a shared environment,
7. smoke tests there.

Within a stage, tests that do not depend on each other can run in **parallel** (for example API tests and axe scans at the same time) so you get faster feedback without removing any coverage.

Real-world scenario: a developer renames the response field `total` to `totalAmount`. Lint passes. Unit tests pass because they mock the data layer. The **API schema test** fails ninety seconds later, the merge request is blocked, and the developer fixes it before anyone else is affected. Without that layer the front end would show "NaN" for every order total in production.

QE contribution: you own the content and ordering of the test layers. Ask of every test: "what is the cheapest place this could run and still catch the bug?"

### 5. Phase 4: Package, Immutable Artifacts, and Versioning

**Packaging** creates the deployable **artifact**: a Docker image, a wheel, a ZIP, or a compiled binary. Three rules matter.

**Build once, deploy many.** Build the artifact one time. Then deploy that same artifact to dev, then staging, then production. Do not rebuild for each environment. Why? A rebuild pulls in fresh dependencies, a different compiler state, or a different base image. You would be testing one thing and shipping another. Differences between environments should come only from **configuration**, never from different builds.

**Immutable artifacts.** Once published, an artifact is never changed. If you find a bug, you build a new version. This means "version 1.4.0" always means exactly the same bytes, which makes debugging, auditing, and rollback reliable. If someone could quietly overwrite `myapi:1.4.0`, nobody could say what was running last Tuesday.

**Versioning.** Two complementary labels are common:

- **Semantic versioning (semver)**: `MAJOR.MINOR.PATCH`, for example `2.4.1`.
  - MAJOR: breaking changes (clients must change). `1.x` to `2.0.0`.
  - MINOR: new backwards-compatible features. `2.3.0` to `2.4.0`.
  - PATCH: backwards-compatible bug fixes. `2.4.0` to `2.4.1`.
- **Commit SHA tag**: the first characters of the Git commit hash, for example `myapi:3f2a9c1`. It traces any running service back to the exact source code.

Many teams use both: every build gets a SHA tag automatically; a release additionally gets a semver tag pointing at the same image.

```
# pseudo-commands (conceptual)
build image from commit 3f2a9c1       -> myapi:3f2a9c1
tests pass on myapi:3f2a9c1
release decision: this is version 2.4.1 -> add label myapi:2.4.1 to the SAME image
deploy myapi:2.4.1 (same bytes as 3f2a9c1) to staging, then production
```

Artifacts are **stored** in a registry or package repository, not on someone's laptop. Test **reports** (JUnit XML, axe results) are also artifacts of a different kind: evidence rather than deployables. A later Friday lesson covers pipeline artifacts in detail.

QE contribution: record the version under test in your reports. "Test run passed" is useless; "tests passed on `myapi:3f2a9c1`" is evidence.

### 6. Phase 5: Release

**Release** means declaring a specific, already-tested version eligible for production. It typically includes assigning the semver number, writing release notes or a changelog, checking that required tests passed, and an approval. Release is a decision about a version; deploy is the act of putting it somewhere.

### 7. Phase 6: Environments, Promotion, and Configuration

An **environment** is a place where the software runs. Each successive environment looks more like production.

| Environment | Purpose | Data | Who uses it | QE activity |
|-------------|---------|------|-------------|-------------|
| **Dev** | Integration of the team's latest work, experiments | Fake/synthetic | Developers | Fast API tests, early exploratory testing |
| **Staging** | Rehearsal for production: same setup, scale, and settings as far as practical | Synthetic or anonymised | QE, product, stakeholders | Full regression, accessibility, smoke, exploratory |
| **Production** | Real users | Real | Customers | Read-only smoke, monitoring |

Many organisations also have a "test" or "QA" environment between dev and staging, and the pipeline itself often creates a short-lived temporary environment for each merge request. The principle is the same: the further along, the more production-like and the more careful you must be.

**Promotion** means moving the *same artifact* from one environment to the next after it passes the checks for the current one. Promotion is not rebuilding; it is "take the image that passed in dev and deploy it to staging".

```
myapi:3f2a9c1 --passes--> dev --promote--> staging --approval--> production
```

**Configuration per environment.** Because the artifact is identical, anything that differs by environment must live outside it: base URLs, database addresses, feature switches, credentials. Common mechanisms are environment variables or configuration files injected at deploy time. Credentials are secrets and must come from a secrets store, not the repository (a later Friday lesson covers this).

Your tests follow the same rule. The base URL and credentials come from variables you set in Tuesday and Wednesday's work, so the same suite runs everywhere:

```bash
# pseudo-usage: only configuration changes between environments
API_BASE_URL=https://dev.example.test      pytest -m api
API_BASE_URL=https://staging.example.test  pytest -m "api or accessibility"
API_BASE_URL=https://www.example.test      pytest -m "smoke and not destructive"
```

QE contribution: guard the boundary. Staging must be realistic enough that a pass there means something; production tests must be safe by design.

### 8. Phase 6 (continued): Deployment Strategies

How you replace the old version with the new one has a big effect on risk and downtime. Five common approaches:

**Recreate.** Stop the old version completely, then start the new one.
- Simple. There is a gap of downtime.
- Fine for internal tools or off-hours windows.

**Rolling.** Replace instances gradually: if there are four copies of the service, update one, check it, update the next, and so on.
- No total downtime. For a while, old and new versions run side by side, so they must be compatible with each other (for example the database must work with both).

**Blue-green.** Keep two complete environments. "Blue" is live. Deploy the new version to "green", test it there (smoke, API, axe) with no users affected, then switch traffic from blue to green in one step.
- Instant switch and an instant rollback (switch back). Costs double the infrastructure during the release.

**Canary.** Send a small share of real traffic (say 5%) to the new version, watch error rates and response times, and increase the share if all is well.
- Real-world feedback with limited blast radius. Needs good monitoring to decide.

**Feature flags.** Deploy the code switched off, then turn the feature on for chosen users or percentages with a configuration setting, independent of deployment.
- Separates "deployed" from "released". A bad feature is turned off in seconds without redeploying. The cost is flag management: old flags must be cleaned up, and tests must cover both flag states.

| Strategy | Downtime | Rollback speed | Extra cost | Good for |
|----------|----------|----------------|-----------|----------|
| Recreate | Yes, short | Redeploy old | Lowest | Internal tools |
| Rolling | None | Moderate | Low | Most services |
| Blue-green | None | Very fast | High | Critical services, big changes |
| Canary | None | Fast | Medium + monitoring | High-traffic public services |
| Feature flag | None | Instant (flip flag) | Flag management | Gradual feature exposure |

**Rollback** means returning to the last known-good version. It works well because of immutable, versioned artifacts: "redeploy `myapi:2.4.0`" is a precise instruction. Rollback has pitfalls: database changes may not be reversible, and a rollback you have never rehearsed may fail when you need it most. Teams practise rollbacks in staging.

QE contribution: know which strategy your product uses, because it decides what to test. With blue-green, run your full smoke and accessibility checks against green *before* the switch. With canary, check that your tests tolerate two versions running together. With feature flags, test both on and off.

### 9. Manual Approval Gates

Not every step should be automatic. A **manual approval gate** pauses the pipeline until a person approves. Typical places:

- before deploying to production,
- before a database migration,
- before something costly or irreversible.

**Continuous Delivery** means every passing change is *ready* to deploy and a human presses the button. **Continuous Deployment** means passing changes go to production automatically with no human gate. Which one a team uses depends on risk, regulation, and confidence in the automated tests.

A good approval gate has a named approver, a clear checklist (tests green, release notes written, no open critical defects, change window agreed), and a record of who approved and when.

Common mistake: approvals as rubber stamps. If the approver does not look at the test results, the gate adds delay but no safety. The QE's job is to make the evidence easy to read: one summary showing which tests ran, on which version, with what result.

### 10. Operate, Monitor, and Post-Deploy Checks

After deploying, verify that the new version is actually working **in that environment**. A deployment that "succeeded" only means the files were copied and the process started; it does not mean customers can use it.

Post-deploy checks, from cheapest to most thorough:

| Check | Question |
|-------|----------|
| **Health endpoint** (`GET /health`) | Is the service up and are its dependencies reachable? |
| **Version check** | Is the new version actually the one serving traffic? |
| **Smoke tests** | Do the critical journeys work (login, a read, a create)? |
| **Accessibility spot check** | Do key pages still pass axe after deployment? |
| **Monitoring** | Are error rates, latency, and logs normal over the next hours? |

The version check catches a common failure: the deploy reported success, but the old containers are still running. Here is a health-check script that a pipeline job could run after deployment. It retries, because new services need a few seconds to start.

```python
import json
import sys
import time
import urllib.request
import urllib.error


def check_health(base_url, expected_version, attempts=10, delay=3):
    """Poll /health until the service is healthy and on the expected version."""
    url = base_url.rstrip("/") + "/health"
    last_problem = "no attempt made"

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                body = json.loads(response.read().decode("utf-8"))
            if body.get("status") != "ok":
                last_problem = f"status was {body.get('status')!r}"
            elif body.get("version") != expected_version:
                last_problem = (
                    f"version was {body.get('version')!r}, "
                    f"expected {expected_version!r}"
                )
            else:
                print(f"Healthy on attempt {attempt}: {body}")
                return True
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            last_problem = f"request failed: {error}"

        print(f"Attempt {attempt}/{attempts}: {last_problem}")
        time.sleep(delay)

    print(f"UNHEALTHY after {attempts} attempts: {last_problem}")
    return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: health_check.py BASE_URL EXPECTED_VERSION")
        sys.exit(2)
    ok = check_health(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
```

Line-by-line:

- The imports use only the standard library, so the script runs anywhere Python is installed with nothing to install first.
- `check_health(...)` takes the service address, the version we expect, and how many times to try and how long to wait between tries.
- `url = base_url.rstrip("/") + "/health"` builds the endpoint address and avoids a double slash if the base URL ends with one.
- `last_problem` remembers the most recent reason for failure so the final message is useful.
- The `for` loop is the retry. Services often need a few seconds after deployment, so one failed request is not necessarily a failure.
- `urlopen(url, timeout=5)` makes the request; the timeout stops a hung service from hanging the pipeline. A non-2xx status raises `urllib.error.HTTPError` (a kind of `URLError`), which the `except` handles.
- `json.loads(...)` parses the body. If the body is not valid JSON, `ValueError` is raised and handled.
- The `if / elif / else` checks two things in order: status is `ok`, and version matches. Only when both hold do we return `True`.
- On any problem we print the attempt, wait, and try again; after all attempts we print the last reason and return `False`.
- The `__main__` block reads two command-line arguments and exits with code `0` (success) or `1` (failure). **The exit code is what the pipeline reads**: non-zero fails the job, which stops promotion or triggers rollback. Exit code `2` signals a usage error.

Usage in a deploy job would be one line: `python health_check.py https://staging.example.test 2.4.1`.

**Monitoring and operate.** After release, production keeps teaching you things pre-release tests could not. Teams watch logs, metrics (error rate, latency), alerts, and **synthetic monitoring**: your smoke tests run on a schedule against production, so a failure is noticed even when no deployment happened (an expired certificate, a downstream service outage). Monitoring is also where the lifecycle loops: production issues become new defects, new tests, and new changes.

### 11. Where QA Validates at Each Step

| Phase | QA activity |
|-------|-------------|
| Source | Review test changes in merge requests; enforce required pipelines; check requirements are testable |
| Build | Keep test project dependencies pinned; lint test code; verify tests are collected |
| Test | Own the unit-adjacent, API, and accessibility suites; decide ordering; tag tests (smoke, regression); fight flakiness |
| Package | Record which artifact version the tests ran against; check test reports are saved as evidence |
| Release | Provide the quality summary for approvers; confirm no open critical defects |
| Deploy | Verify environment configuration; run post-deploy smoke and health checks |
| Operate/Monitor | Review synthetic checks, investigate incidents, turn escapes into new automated tests |

### 12. Pipeline Failure Handling and Notifications

Pipelines will fail. What matters is how the team responds. When a job fails, **triage** by cause:

| Cause | Example | Action |
|-------|---------|--------|
| Product defect | API returns `500` for a valid request | Report to developer; block the change |
| Test defect | Locator or assertion is wrong | Fix the test; do not weaken it to pass |
| Environment | Staging database is down | Notify the owner; re-run when fixed |
| Infrastructure | Runner out of disk, registry unreachable | Platform team; retry |
| Flaky | Passes on re-run, fails randomly | Quarantine and fix; track it; do not ignore |

Good practices:

- **Fail fast and loudly**: a failure stops later stages and clearly names the job that failed.
- **Keep the evidence**: logs, reports, and screenshots saved from failed runs so nobody must reproduce it first.
- **Notify the right people**: the author of the change for merge request failures; a team channel for `main` or production-check failures; an on-call person for production alerts. Avoid sending every message to everyone, because people learn to ignore noisy alerts.
- **Fix broken `main` first**: a red main branch blocks everyone and gets priority over new work.
- **Retry carefully**: automatic retries are acceptable for infrastructure hiccups, but retrying a failing test until it passes hides real problems.
- **Failure during deploy**: if post-deploy checks fail, roll back (or switch traffic back) automatically or by quick manual action, then investigate.

### 13. End-to-End Example: A Small Orders API Service

Imagine a small service with `GET /health`, `GET /orders`, `POST /orders`, and a simple web page that lists orders. Here is its lifecycle for one change, described in generic pseudo-configuration (the real syntax is covered in the next lesson).

```
trigger: merge request opened (and on merge to main)

stage 1: build
  job lint        -> ruff check . ; npm run lint
  job install     -> pip install -r requirements.txt (pinned)
  job collect     -> pytest --collect-only -q           [fail fast: seconds]

stage 2: unit
  job unit        -> pytest -m unit                      [1 minute]

stage 3: package
  job image       -> docker build -t orders:<commit-sha>
                     docker push to registry             [artifact created ONCE]

stage 4: test (in parallel, against the image started as a temporary service)
  job api         -> pytest -m api   (status, schema, auth, error cases)
  job a11y        -> pytest -m accessibility (axe scan of the orders page)

stage 5: deploy-staging   (only on main)
  job deploy      -> deploy orders:<commit-sha> to staging
  job verify      -> python health_check.py $STAGING_URL <commit-sha>
  job smoke       -> pytest -m smoke  (against staging)

stage 6: release
  job approve     -> MANUAL gate: named approver; tag the same image as 1.5.0

stage 7: deploy-production
  job deploy      -> deploy orders:1.5.0 using canary (5% -> 50% -> 100%)
  job verify      -> python health_check.py $PROD_URL 1.5.0
  job smoke       -> pytest -m "smoke and not destructive"

on failure at any stage: stop, keep reports, notify the author (MR) or team channel (main);
                         on production failure: roll back to previous version
```

Walk through what each part protects against:

- **Stage 1** catches typos and broken imports in seconds, before spending minutes on anything else.
- **Stage 2** checks logic quickly with dependencies mocked.
- **Stage 3** builds the image **once**. Everything after this uses that same image.
- **Stage 4** runs the API tests and the axe scan in parallel. The API tests verify the contract (field names, types, status codes, authentication, error messages). The axe scan verifies that the orders page has labelled form fields, enough colour contrast, and valid structure. A missing label on a new "Add order" field fails here, before it ships.
- **Stage 5** proves the image works in a realistic environment. The health script confirms the right version is running; smoke tests check one read and one create path.
- **Stage 6** is the human decision point.
- **Stage 7** introduces the change gradually and verifies again in production using only safe tests.

### 14. Common Mistakes

| Mistake | Better practice |
|---------|-----------------|
| One giant job that does everything | Separate stages and jobs by purpose and speed |
| Slow tests before fast ones | Fail fast: lint, unit, then slower layers |
| Rebuilding per environment | Build once, promote the same artifact |
| Deploying the `latest` tag | Deploy immutable version or SHA tags |
| Unpinned dependencies | Pin versions for reproducible builds |
| Hard-coded URLs and secrets in tests | Environment variables and a secrets store |
| Destructive tests against production | Read-only, designed-for-production smoke tests only |
| No post-deploy verification | Health, version, and smoke checks after every deploy |
| No rehearsed rollback | Practise rollback in staging |
| Rubber-stamp approvals | Give approvers a clear evidence summary |
| Ignoring flaky tests or re-running until green | Quarantine, investigate, fix |
| Reports not saved from failed runs | Keep logs and reports as evidence |
| Skipping accessibility until the end | Run axe scans in the pipeline from the start |

### 15. Glossary

- **Artifact**: a file or image the pipeline produces and keeps (a deployable image, or evidence such as a test report).
- **Build**: turning source into something runnable (install, lint, compile or bundle, build an image).
- **Canary / blue-green**: strategies that expose a small traffic share, or switch between two parallel environments.
- **Fail fast**: run the quickest, most informative checks first so failures stop the pipeline early.
- **Feature flag**: a configuration switch that turns a feature on or off without redeploying.
- **Gate**: a condition (passing tests, approval) required before the next phase.
- **Immutable**: never changed after creation; a fix is a new version.
- **Promotion**: moving the same artifact to the next environment.
- **Rollback**: returning to the last known-good version.
- **Semver**: `MAJOR.MINOR.PATCH` versioning that signals the kind of change.
- **Smoke test**: a small, quick set of critical checks showing a deployment is basically working.

### 16. Practice Exercises

**Exercise 1: Place the checks.** A tiny web shop has a Python API, a lint tool, unit tests, API tests, axe scans, and smoke tests. List them in the order you would run them and say where each runs (before packaging, staging, production). Explain one ordering decision.

**Solution.** One reasonable answer:

1. Lint (build stage; seconds, catches syntax and style).
2. Unit tests (before packaging; fast, no environment needed).
3. Package the image once.
4. API tests (against the image as a temporary service; contract checks) and axe scans (rendered page) in parallel.
5. Deploy to staging, run health check, then smoke tests.
6. After approval, deploy to production, run health check and read-only smoke tests.

Ordering decision: lint before everything because it takes seconds and a failure makes every later stage pointless. Smoke tests run only after a deploy because they need a running deployment in a real environment.

**Exercise 2: Build once, deploy many.** Explain the principle and give an example of a bug it prevents.

**Solution.** The artifact is built a single time and the same one is promoted through every environment; only configuration differs. Example bug: if staging and production were built separately, a dependency released between the two builds (for example a library minor version) could change behaviour. Staging passes with the old library; production runs the new one and breaks. Building once means production runs exactly the bytes that passed in staging.

**Exercise 3: Choose a deployment strategy.** For each case pick a strategy and justify it: (a) an internal reporting tool used 9-to-5, with a quiet weekend; (b) a high-traffic public checkout service; (c) a new "dark mode" setting that product wants to show to 10% of users first.

**Solution.**
(a) Recreate. Downtime on a weekend is harmless and it is the simplest and cheapest.
(b) Canary (or blue-green). A bug would cost money immediately; a small traffic share limits damage, and monitoring decides whether to continue. Blue-green is the alternative if instant rollback matters most and doubled infrastructure is acceptable.
(c) Feature flag. The code is deployed to everyone but switched on for 10%, adjustable without redeploying. Tests should cover the flag on and off.

**Exercise 4: Read the health script.** Using the Python health-check script above, (a) what exit code does it return if the service never becomes healthy, (b) why does it check the version, (c) what would happen with `attempts=1` on a service that takes 5 seconds to start?

**Solution.** (a) Exit code `1`, which fails the pipeline job. (b) To prove the new build, not an old one, is serving traffic; a deploy may "succeed" while old instances still run. (c) The single request would probably fail (connection refused), the script would report unhealthy and return failure even though the service would be fine seconds later. Retries with a delay avoid this false alarm.

### 17. Quiz

**Q1.** Why should an artifact be built only once?
A) It saves disk space
B) So the exact thing tested is the thing shipped to every environment
C) Docker requires it
D) It makes tests faster

**Q2.** A bug fix is released and changes no public behaviour except correcting an error. Which semver change is appropriate from `2.4.0`?
A) `3.0.0`
B) `2.5.0`
C) `2.4.1`
D) `2.4.0-latest`

**Q3.** Which deployment strategy allows near-instant rollback by switching traffic back to the previous environment?
A) Recreate
B) Blue-green
C) Rolling
D) Hard-coded

**Q4.** Why does the health-check script compare the reported version to the expected version?
A) To make the script longer
B) To confirm the new build is the one actually serving traffic
C) Because `/health` always returns a version
D) To check the database

**Q5.** Which ordering best follows fail-fast?
A) Accessibility scans, smoke tests, lint, unit tests
B) Lint, unit tests, package, API tests and axe scans, deploy, smoke
C) Deploy, smoke, lint, unit tests
D) API tests, lint, package

**Answers.**
Q1: B. Rebuilding can change dependencies or base images, so you would ship something different from what you tested.
Q2: C. A backwards-compatible fix is a PATCH increment.
Q3: B. Blue-green keeps the old environment intact, so rollback is a traffic switch.
Q4: B. A "successful" deploy can leave old instances serving; the version check catches that.
Q5: B. Cheap and fast checks first, expensive and environment-dependent ones later.

---

## Summary

- The lifecycle runs source, build, test, package, release, deploy, operate/monitor, with feedback to the team and a gate between phases.
- Build means different things per technology (pip and ruff for Python, `npm ci` for Node, `docker build` for images) but is always reproducible, automated, and fast.
- Build once, deploy many: artifacts are immutable and versioned with semver and commit SHAs; environments differ only by configuration.
- Layer tests (unit, API, accessibility, smoke) and order them to fail fast; run independent jobs in parallel.
- Environments move from dev to staging to production; promotion moves the same artifact; tests must read configuration from variables and be safe in production.
- Deployment strategies (recreate, rolling, blue-green, canary, feature flags) trade cost, speed, and risk; rollback relies on versioned artifacts and should be rehearsed.
- Manual approval gates need evidence, post-deploy health and smoke checks verify reality, and failures should be triaged by cause with the right people notified.
- Next in Friday's lessons: GitLab fundamentals, stages and jobs, running tests in pipelines, artifacts, and secrets turn this lifecycle into a working pipeline.

## Additional Resources

- Martin Fowler, *Deployment Pipeline*: https://martinfowler.com/bliki/DeploymentPipeline.html
- Martin Fowler, *Test Pyramid*: https://martinfowler.com/bliki/TestPyramid.html
- Semantic Versioning specification: https://semver.org/
- Docker Docs, *Building best practices*: https://docs.docker.com/build/building/best-practices/
- GitLab Docs, *CI/CD*: https://docs.gitlab.com/ci/
