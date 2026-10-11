# GitLab CI/CD Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what GitLab CI/CD is and where a pipeline definition lives in a GitLab project.
- Use the vocabulary correctly: pipeline, stage, job, script, runner, executor, image.
- Choose between shared and project runners, and between the shell and docker executors.
- Read and write basic YAML: mappings, lists, multiline scripts with `|`, and simple anchors.
- Write a first `.gitlab-ci.yml` with `image`, `stages`, `script`, `before_script`, `after_script`, and `default`.
- Use predefined CI variables such as `$CI_COMMIT_SHA` and `$CI_PROJECT_DIR`.
- Find pipelines, jobs, logs, and statuses in the GitLab UI, and explain what triggers a pipeline.
- Validate a pipeline file with the CI Lint tool.
- Build a complete pipeline that runs `pytest` on a Python project, with pip caching.
- Diagnose the four most common beginner failures and debug them methodically.

---

## Why This Matters

This week your automation grows up. On Monday through Thursday you built API tests, checked accessibility, and worked with MCP tooling. Those suites are valuable, but only if they run every time the code changes, on a machine that is not yours, with the same result every time. Today's lesson is where that starts.

In the Week 7 epic, your Project 2 test suites must run automatically in a CI/CD pipeline. A teammate pushes a change, and within minutes the team sees a green or red result without anyone typing `pytest`. No more "it works on my machine", no more forgotten test runs before a release.

Picture a real scenario. A QA engineer joins a team whose API suite lives on three laptops. Releases are delayed because nobody is sure which laptop has the latest dependencies. She moves the suite into GitLab CI. Now one file, `.gitlab-ci.yml`, describes the Python version, the install steps, and the test command. Every merge request is checked the same way. The file is reviewed like code, so the whole team can see how tests run.

Today is the foundation. The later Friday lessons cover stages and jobs in depth, artifacts and reports, and secrets and variables. Here you learn to build, run, read, and fix one working pipeline.

---

## The Concept

### 1. What Is GitLab CI/CD?

**What it is.** GitLab is a platform that hosts Git repositories and adds code review (merge requests), issue tracking, and CI/CD. **CI/CD** stands for Continuous Integration and Continuous Delivery/Deployment. It means automatically building and testing every change, and optionally delivering it.

**Why it exists.** Manual testing does not scale. People forget steps, environments drift, and bugs are found late. Automation makes the check cheap, fast, and identical every time.

**How it works.** A GitLab *project* is a repository plus its settings. If the repository contains a file named `.gitlab-ci.yml` in the **root folder**, GitLab reads it whenever certain events happen and creates a pipeline.

```text
git push
   |
   v
GitLab finds .gitlab-ci.yml in the repo root
   |
   v
A pipeline is created (stages, jobs)
   |
   v
Runners pick up jobs, run them, and send logs and status back
```

Three facts to memorise:

1. The file name is exactly `.gitlab-ci.yml`: leading dot, lowercase, `.yml` extension.
2. It sits in the repository root, next to `README.md` and `requirements.txt`.
3. It is versioned with your code. A change to the pipeline is a commit like any other, and it can go through a merge request.

**When to use it.** Any project with tests, linting, or a build. If you run a command by hand more than twice a week, consider making it a job.

### 2. Pipeline, Stage, Job: The Vocabulary

Think of a car factory. The **pipeline** is the whole assembly line for one car. **Stages** are sections of the line: body, paint, inspection. **Jobs** are tasks at stations inside a section.

| Term | Meaning | Key behaviour |
|------|---------|---------------|
| **Pipeline** | The whole automated run triggered by one event | Has an ID, a status, and a list of stages |
| **Stage** | A named phase | Stages run in order; the next starts only if the previous passed |
| **Job** | A named block of commands | Jobs in the same stage run in parallel (if enough runners exist) |
| **Script** | The shell commands inside a job | Any non-zero exit code fails the job |
| **Runner** | The program that executes a job | Picks jobs up from GitLab |
| **Image** | The Docker image a job runs in | Gives a clean, known environment |

If you do not declare stages, GitLab provides defaults in this order: `.pre`, `build`, `test`, `deploy`, `.post`. A job with no `stage:` lands in `test`. A pipeline with one job is perfectly valid.

Fine control over job ordering and fan-out (`needs`, `parallel`, `matrix`, `rules`) is the subject of the stages-and-jobs lesson later today. For now, think: stages in order, jobs inside a stage side by side.

### 3. GitLab Runners

**What they are.** A **runner** is a small program (GitLab Runner) installed on a machine. It asks GitLab "any jobs for me?", runs the job, and streams the log back. GitLab itself never runs your tests. The runner does.

**Why they are separate.** Running untrusted code, installing packages, and launching browsers is heavy and risky. Keeping it off the GitLab server keeps things scalable and safe.

#### Shared runners versus project runners

| Type | Who owns it | Typical use |
|------|-------------|-------------|
| **Shared runner** | The GitLab instance (for example, the company's GitLab or GitLab.com) | Available to many projects; zero setup; usage limits or queueing may apply |
| **Group runner** | A group of projects | Several related projects share dedicated machines |
| **Project runner** | One project | Special hardware or software, private network access, predictable capacity |

In the UI, look under **Settings > CI/CD > Runners**. You will see which runners are available and whether shared runners are enabled for your project. For this course you will usually use whatever the instructor's GitLab provides.

#### Executors

The **executor** decides *how* a runner runs your job.

| Executor | What happens | Pros | Cons |
|----------|--------------|------|------|
| **shell** | Commands run directly in a shell on the runner machine | Simple; fast; uses what is installed | Jobs share the machine, so leftovers can leak between runs; you need Python installed there |
| **docker** | A fresh container is started from your `image` for each job, then discarded | Clean every time; you choose the tools via `image` | Needs Docker; image downloads take time |

Because the docker executor reads your `image:` line, your pipeline file decides the Python version. This is why beginners almost always meet the docker executor. Other executors exist (Kubernetes, virtual machines), but you will not need them today.

**Tags.** A runner can advertise *tags* such as `docker` or `linux`. A job with `tags: [docker]` is only picked up by runners that have that tag. A tag mismatch is the number one cause of jobs that wait forever (see section 14).

### 4. YAML Syntax Recap

The pipeline is written in YAML. You have seen YAML before, so this is a quick refresher plus the parts GitLab uses heavily.

**Rules.**

1. Use **spaces** for indentation (two is the convention), never tabs.
2. A **mapping** is `key: value`, like a Python dictionary.
3. A **list** uses a dash: `- item`, like a Python list.
4. Indentation shows nesting.
5. Comments start with `#`.
6. Quote strings that contain `:` followed by a space, or start with special characters.

```yaml
# a mapping that contains a list
greeting-job:
  stage: test
  script:
    - echo "first command"
    - echo "second command"
```

Line by line:

- `greeting-job:` is a top-level key. GitLab treats any top-level key that is not a reserved word as a **job name**.
- `stage: test` is a key-value pair inside the job (indented two spaces).
- `script:` is a key whose value is a list.
- The two `- echo ...` lines are list items, indented under `script`.

Python equivalent: `{"greeting-job": {"stage": "test", "script": ["echo \"first command\"", "echo \"second command\""]}}`.

#### Multiline scripts with `|`

```yaml
report-job:
  script:
    - |
      echo "Starting tests"
      pytest -q
      echo "Finished"
```

- `- |` starts a **literal block**. The pipe tells YAML to keep the following indented lines exactly as written, with line breaks.
- The three lines below are indented further than the dash, so they belong to the one list item.
- GitLab runs the block as one multi-line shell script.

Use `|` for `if` statements, loops, or anything that spans lines. A related form, `>`, folds lines into one; avoid it in scripts.

A common trap: a plain list item containing `: ` (colon plus space) is parsed as a mapping. Write `- 'echo "result: ok"'` with outer quotes, or use a `|` block.

#### Anchors, briefly

An **anchor** (`&name`) labels a chunk of YAML, and an **alias** (`*name`) reuses it. A merge key (`<<:`) copies a mapping into another.

```yaml
.base: &base_settings
  image: python:3.12
  before_script:
    - pip install -r requirements.txt

unit-tests:
  <<: *base_settings
  script:
    - pytest tests/unit

api-tests:
  <<: *base_settings
  script:
    - pytest tests/api
```

- `.base:` begins with a dot, so GitLab treats it as a hidden job that never runs; it only holds settings.
- `&base_settings` attaches the anchor name to that mapping.
- `<<: *base_settings` in each real job merges in the image and `before_script`.
- Each job adds its own `script`.

Anchors work, but GitLab also offers `extends` and `default`, which are usually clearer. Recognise anchors when you see them; prefer `default` for shared settings.

### 5. Your First Pipeline

**Step 1.** In your repository root, create `.gitlab-ci.yml`.

**Step 2.** Add a hello-world job.

```yaml
hello-world:
  image: python:3.12
  script:
    - echo "Hello from GitLab CI"
    - python --version
```

- `hello-world:` is the job name.
- `image: python:3.12` tells a docker-executor runner to start a container from the official `python:3.12` image.
- `script:` lists the commands. Each runs in order.
- `echo` prints text to the log; `python --version` proves the right interpreter exists.

**Step 3.** Commit and push. In the left sidebar of the project, open **Build > Pipelines** (older versions: **CI/CD > Pipelines**). A new pipeline appears, with one job in the default `test` stage.

**Step 4.** Click the pipeline status, then click the `hello-world` job to read its log. You will see the runner starting, the image being pulled, your commands each prefixed with `$`, and a final line such as `Job succeeded`.

Now make the stages explicit and add setup and cleanup:

```yaml
stages:
  - build
  - test

default:
  image: python:3.12
  before_script:
    - echo "Pipeline $CI_PIPELINE_ID starting"

prepare:
  stage: build
  script:
    - echo "Preparing"

check:
  stage: test
  script:
    - echo "Checking"
  after_script:
    - echo "Cleaning up"
```

- `stages:` lists the stage names in execution order. `build` finishes before `test` begins.
- `default:` sets values that apply to every job unless a job overrides them. Here it sets the image and a `before_script` once.
- `prepare` is in `build`; `check` is in `test`. Every stage a job names must be listed in `stages`.
- `before_script` runs before `script` in the same shell. Use it for setup.
- `after_script` runs after `script`, even when the script failed, but in a **separate shell**. Variables you `export` in `script` are not visible there. Use it for cleanup and diagnostics.

Which keywords may go under `default:`? The common ones are `image`, `before_script`, `after_script`, `cache`, `tags`, `timeout`, and `retry`. A job-level setting wins over the default.

### 6. Predefined CI Variables

GitLab injects **predefined variables** into every job as environment variables. You do not define them; they are just there.

| Variable | Meaning | Example |
|----------|---------|---------|
| `CI_COMMIT_SHA` | Full commit hash | `a3f9c2e...` (40 chars) |
| `CI_COMMIT_SHORT_SHA` | First 8 characters | `a3f9c2e1` |
| `CI_COMMIT_BRANCH` | Branch name (not set in merge request pipelines) | `feature/login-tests` |
| `CI_PIPELINE_ID` | Global pipeline number | `48211` |
| `CI_PIPELINE_SOURCE` | What triggered the pipeline | `push`, `merge_request_event`, `schedule`, `web` |
| `CI_PROJECT_DIR` | Absolute path where the repo is checked out | `/builds/team/project` |
| `CI_JOB_NAME` | The running job's name | `api-smoke` |
| `CI` | Always `true` in GitLab CI | `true` |

```yaml
show-context:
  image: python:3.12
  script:
    - echo "Commit $CI_COMMIT_SHA on branch $CI_COMMIT_BRANCH"
    - echo "Pipeline $CI_PIPELINE_ID, source $CI_PIPELINE_SOURCE"
    - echo "Repo is checked out at $CI_PROJECT_DIR"
    - ls "$CI_PROJECT_DIR"
```

- Each `$NAME` is replaced by the shell with the variable's value when the command runs.
- `ls "$CI_PROJECT_DIR"` lists your repository files, a quick way to confirm the checkout worked.
- Your Python code can read them too: `os.getenv("CI") == "true"` lets a test skip browser-only steps locally.

Real-world use: stamp a report with `$CI_COMMIT_SHORT_SHA` so you know exactly which code produced it. Defining your own variables and handling secrets is covered in the secrets-and-variables lesson later today.

### 7. How Pipelines Get Triggered

A pipeline starts because of an *event*. `CI_PIPELINE_SOURCE` tells you which.

| Trigger | When it fires | `CI_PIPELINE_SOURCE` |
|---------|---------------|----------------------|
| **Push** | You push commits to a branch | `push` |
| **Merge request** | An MR is opened or updated (requires the pipeline to be configured for MRs) | `merge_request_event` |
| **Schedule** | A cron-like timer, set up under **Build > Pipeline schedules** (for example, nightly at 02:00) | `schedule` |
| **Manual** | You click **Run pipeline** in the UI, or a job is set to wait for a click | `web` (for Run pipeline) |

Two beginner notes. First, a plain file with no `rules` runs on every push, and also for merge request pipelines only when told to. Second, a **manual job** (`when: manual`) is created with a play button and waits for a human:

```yaml
deploy-demo:
  script:
    - echo "Deploying"
  when: manual
```

- `when: manual` makes the job wait. The pipeline can still pass without it, because manual jobs are optional by default.

Choosing precisely which events run which jobs uses `rules`, covered in the stages-and-jobs lesson.

### 8. Viewing Pipelines, Jobs, Logs, and Statuses

Navigation: **Build > Pipelines** lists every pipeline for the project. Click one to see a graph with a column per stage and a box per job. Click a job to open its log.

**Job statuses** (the icon colour tells the story):

| Status | Meaning |
|--------|---------|
| **created / pending** | Job exists and is waiting for a runner to pick it up |
| **running** | A runner is executing it |
| **passed** | All commands exited with 0 |
| **failed** | A command exited non-zero, or the job timed out |
| **canceled** | A person stopped it |
| **skipped** | It was not run, for example because an earlier stage failed |
| **manual** | Waiting for someone to click the play button |
| **warning** | Passed with `allow_failure` problems |

A pipeline has the status of its worst required job.

**Reading a log.** Start at the **bottom** for the last command and the failure message, then scroll up for context. Typical pieces:

```text
Running with gitlab-runner 17.x
Using Docker executor with image python:3.12 ...
$ pip install -r requirements.txt
Successfully installed pytest-8.x ...
$ pytest -v
tests/test_api.py::test_status PASSED
tests/test_api.py::test_login FAILED
ERROR: Job failed: exit code 1
```

`exit code 1` is how pytest reports "tests failed". That is how a test failure becomes a red job.

Buttons on the job page: **Retry**, **Cancel**, and, for manual jobs, **Run**. The merge request page shows the latest pipeline status near the top, so reviewers see it before approving.

### 9. The CI Lint Tool

A tiny YAML mistake can stop the entire pipeline from being created. **CI Lint** checks your file before you push.

**How to use it.**

1. Open **Build > Pipeline editor**. It has a built-in **Validate** tab and a **Visualize** tab. (Older versions: **CI/CD > Editor** and a separate **CI Lint** page.)
2. Paste or edit your YAML.
3. Run validation. If valid, you see the jobs and stages it would create. Tick the simulation option to see what would happen on the default branch.
4. If invalid, read the message. It names the problem, for example `jobs:test script can't be blank`.

Make linting a habit: whenever you edit `.gitlab-ci.yml`, validate it first. It takes ten seconds and saves a failed push. Locally, you can also check plain YAML syntax with `python -c "import yaml,sys; yaml.safe_load(open('.gitlab-ci.yml'))"`. This catches indentation and quoting, but only CI Lint knows GitLab keywords.

### 10. Caching Basics

**What.** A **cache** stores files between pipeline runs so jobs do not repeat slow work. The classic example is downloaded Python packages.

**Why.** Every job runs in a fresh container. Without a cache, `pip install` downloads everything on every run. With one, the second run reuses the downloads and finishes much faster.

**How.**

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  key:
    files:
      - requirements.txt
  paths:
    - .cache/pip
```

- `PIP_CACHE_DIR` is a variable that pip itself reads; it tells pip to keep downloads inside the project folder. The cache can only save files inside `$CI_PROJECT_DIR`, so we point pip there.
- `cache:` is the global cache setting.
- `key: files: - requirements.txt` makes the cache name depend on the hash of `requirements.txt`. Change the dependencies and a new cache is built; leave them and the old one is reused.
- `paths:` lists what to save: the `.cache/pip` folder.

Cache rules to remember: a cache is a **best-effort speed-up**, not a guarantee, so your job must still work if the cache is empty. Do not confuse it with **artifacts**, which pass results between jobs; artifacts have their own lesson later today.

### 11. A Complete Beginner Example: pytest on a Python Project

Assume this repository layout:

```text
my-api-tests/
  .gitlab-ci.yml
  requirements.txt
  tests/
    test_health.py
```

`requirements.txt` contains `pytest` and `requests`. Here is the pipeline:

```yaml
stages:
  - test

default:
  image: python:3.12

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  key:
    files:
      - requirements.txt
  paths:
    - .cache/pip

run-pytest:
  stage: test
  before_script:
    - python --version
    - pip install -r requirements.txt
  script:
    - pytest -v
  after_script:
    - echo "Finished pipeline $CI_PIPELINE_ID for commit $CI_COMMIT_SHORT_SHA"
```

Walk through it from top to bottom:

1. `stages: - test` declares one stage. Naming it is optional here, but explicit is good practice.
2. `default: image: python:3.12` gives every job Python 3.12. Pinning the minor version makes runs reproducible; `latest` can change under you.
3. `variables: PIP_CACHE_DIR` points pip's download cache inside the repo folder so GitLab can save it.
4. `cache:` saves `.cache/pip` between runs, keyed on `requirements.txt`.
5. `run-pytest:` is the job. `stage: test` places it in the stage.
6. `before_script` prints the Python version (handy when debugging), then installs dependencies. The cache makes the second and later runs faster.
7. `script: pytest -v` runs the tests with verbose output. If any test fails, pytest exits non-zero and the job turns red.
8. `after_script` prints a closing line with the pipeline ID and short commit SHA. It runs even when the tests fail.

**What you should see.** After pushing, the first run downloads packages; open the log and find `Successfully installed`. A later run, with the same `requirements.txt`, shows a line like `Successfully extracted cache` near the start and a quicker install.

### 12. Real-World Scenario: Red After a Green Day

Yesterday your pipeline passed. Today a teammate's merge request shows red. You open the job log, jump to the bottom, and see `ModuleNotFoundError: No module named 'jsonschema'`. Scrolling up, `pip install -r requirements.txt` succeeded, so the package is not listed. The new test imports it, but nobody added it to `requirements.txt`. It worked on the teammate's laptop because they had installed it by hand earlier. CI caught the gap, which is exactly its job. The fix is one line in `requirements.txt`, a push, and a green pipeline. Notice the method: bottom of the log, read the error, trace upward.

### 13. Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Tabs instead of spaces | YAML rejects tabs | Configure your editor to insert spaces |
| Misspelling the file name (`gitlab-ci.yml`, `.gitlab-ci.yaml`) | GitLab never creates a pipeline | Use exactly `.gitlab-ci.yml` in the root |
| Forgetting `script:` | Job is invalid | Every real job needs at least one command |
| Using a `stage:` not listed in `stages:` | Config error | Add the stage name, or fix the typo |
| Installing packages in one job and expecting them in another | Each job has a fresh container | Install in every job that needs them (use `before_script`/`default`) |
| Using `image: python:latest` | Unexpected upgrades break the build | Pin a version like `python:3.12` |
| Putting secrets in the YAML | Anyone with repo access can read them | Use project CI/CD variables (secrets lesson) |
| Treating cache as storage for results | Caches can be empty or evicted | Use artifacts for results |
| Not running CI Lint | Pushing broken YAML | Validate in the Pipeline editor first |

### 14. Common Errors and How to Debug Them

#### Error 1: YAML indentation problems

```text
run-pytest:
  stage: test
 script:
    - pytest
```

(Shown as text because it is deliberately broken.) `script` is indented one space, not two, so it does not line up with `stage`. GitLab reports a syntax error such as `(<unknown>): did not find expected key`. **Debug:** open the Pipeline editor, read the line number in the message, and align keys that belong to the same mapping. Run CI Lint after every fix.

#### Error 2: Job stuck in pending, no runner

The job shows "This job is stuck because the project doesn't have any runners online assigned to it" or just stays pending for a long time.

**Causes and checks:**

1. Open **Settings > CI/CD > Runners**. Is a runner listed and online (green)?
2. Are shared runners enabled for the project?
3. Does the job have `tags:` that no runner advertises? Remove the tag or use one that exists.
4. Is the runner busy? Wait, or check queue length.

#### Error 3: Image pull failure

```text
ERROR: Job failed: failed to pull image "python:3.99" ... not found
```

**Causes:** a typo in the image name or tag, a private registry that needs credentials, or a network or rate-limit problem pulling from the registry. **Debug:** compare the name against the registry page, try `docker pull python:3.12` on your machine, and pin a tag that exists.

#### Error 4: Command not found

```text
$ pytest -v
/bin/bash: line 142: pytest: command not found
ERROR: Job failed: exit code 127
```

Exit code **127** means the shell could not find the program. The image has Python, but `pytest` was never installed. **Debug:** check that `pip install -r requirements.txt` ran in this job (container state does not carry over from other jobs), and that `pytest` is listed in `requirements.txt`. The same message appears for typos like `pyest`.

#### A general debugging routine

1. Open the failed job; scroll to the bottom for the error.
2. Classify it: syntax, runner, image, install, or test failure.
3. Reproduce locally with the same image:

```bash
docker run --rm -it -v "$PWD":/work -w /work python:3.12 bash
pip install -r requirements.txt && pytest -v
```

4. Add temporary diagnostics: `pip list`, `ls -la`, `pwd`. Never print secrets.
5. Fix, commit, push, and watch the new pipeline. Use CI Lint before pushing.

### 15. Practice Exercises

#### Exercise 1: Hello pipeline

Create a job named `hello` using `python:3.12` that prints `Hello CI`, the Python version, and the current pipeline ID.

**Solution**

```yaml
hello:
  image: python:3.12
  script:
    - echo "Hello CI"
    - python --version
    - echo "Pipeline $CI_PIPELINE_ID"
```

Each command runs in order; `$CI_PIPELINE_ID` is expanded by the shell from a predefined variable. Push it and open the job log to confirm all three lines appear.

#### Exercise 2: Two stages with default settings

Write a pipeline with stages `build` and `test`, a shared `python:3.12` image set once, a build job that prints `Building`, and a test job that prints `Testing` and then cleans up with an `after_script`.

**Solution**

```yaml
stages:
  - build
  - test

default:
  image: python:3.12

build-job:
  stage: build
  script:
    - echo "Building"

test-job:
  stage: test
  script:
    - echo "Testing"
  after_script:
    - echo "Cleaning up"
```

`default` removes the repeated `image` line. The stage list guarantees `build-job` finishes before `test-job` starts.

#### Exercise 3: Pytest with pip caching

Your repo has `requirements.txt` and a `tests/` folder. Write a pipeline that installs dependencies, caches pip downloads keyed on `requirements.txt`, and runs `pytest -q`.

**Solution**

```yaml
default:
  image: python:3.12

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  key:
    files:
      - requirements.txt
  paths:
    - .cache/pip

tests:
  stage: test
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest -q
```

Pip reads `PIP_CACHE_DIR`, so its downloads land in a folder GitLab can cache. The key ties the cache to `requirements.txt`. Run the pipeline twice and compare install times.

#### Exercise 4: Debug the broken pipeline

This pipeline fails. List two problems and fix them.

```yaml
stages:
  - test

lint:
  stage: check
  image: python:3.12
  script:
    - ruff check .
```

**Solution.** Problem 1: `stage: check` is not listed in `stages`, so the config is invalid. Change it to `stage: test` (or add `check` to `stages`). Problem 2: `ruff` is not installed in the plain `python:3.12` image, so even with a valid stage the job would end with `ruff: command not found` (exit 127). Add `pip install ruff` first.

```yaml
stages:
  - test

lint:
  stage: test
  image: python:3.12
  script:
    - pip install ruff
    - ruff check .
```

### 16. Quiz

**Q1.** Where must the pipeline definition file live, and what is it called?
a) `ci/pipeline.yaml` in any folder
b) `.gitlab-ci.yml` in the repository root
c) `gitlab-ci.yml` in the `.git` folder
d) `Jenkinsfile` in the root

**Q2.** Three jobs are in the same stage, and enough runners are free. How do they run?
a) One after another in alphabetical order
b) In parallel
c) Only the first runs
d) They run after the next stage

**Q3.** A job fails with `exit code 127` and `pytest: command not found`. What is the most likely cause?
a) A failing test
b) pytest was not installed in this job's container
c) The runner is offline
d) The YAML contains tabs

**Q4.** What is the difference between `before_script` and `after_script`?
a) There is none
b) `before_script` runs before `script` in the same shell; `after_script` runs afterwards, even on failure, in a separate shell
c) `after_script` only runs on success
d) `before_script` runs on a different machine

**Q5.** Which statement about the docker executor is true?
a) Jobs share one long-lived environment
b) A fresh container from your `image` is created for each job
c) It needs no Docker
d) It ignores the `image` keyword

**Answers**

1. **b.** GitLab looks only for `.gitlab-ci.yml` in the repo root.
2. **b.** Jobs in the same stage run in parallel when runners are available.
3. **b.** Exit code 127 means the command does not exist in that container; install the dependency in the same job.
4. **b.** Remember that `after_script` is a separate shell, so exported variables do not carry over.
5. **b.** That is why each job starts clean and must install its own dependencies.

### 17. Glossary

#### Pipeline
The complete automated run for one trigger. It has an ID (`$CI_PIPELINE_ID`) and an overall status.

#### Stage
A named phase of a pipeline. Stages run in the order listed in `stages:`.

#### Job
A named unit of work with a `script`. The smallest item that passes or fails.

#### Script
The shell commands a job runs. A non-zero exit code fails the job.

#### Runner
The program that picks up and runs jobs, then reports back to GitLab.

#### Executor
How a runner runs jobs (`shell`, `docker`, and others).

#### Image
The Docker image used for the job environment, for example `python:3.12`.

#### Tag
A label on a runner. A job's `tags:` must match a runner's tags for it to be picked up.

#### Cache
Files reused between runs to save time, such as pip downloads.

#### Predefined variable
An environment variable GitLab sets for you, such as `CI_COMMIT_SHA`.

#### CI Lint
The tool in the Pipeline editor that validates a `.gitlab-ci.yml` before you push it.

#### Anchor
A YAML feature (`&name` and `*name`) for reusing part of a file.

---

## Summary

- GitLab reads `.gitlab-ci.yml` from the repository root and creates a pipeline when an event such as a push, merge request, schedule, or manual run occurs.
- A pipeline is made of stages, which run in order, and jobs, which run in parallel within a stage. A job is a `script` that fails on any non-zero exit code.
- Runners execute jobs. They may be shared or project-specific, and the docker executor gives every job a fresh container from your `image`.
- YAML relies on spaces for indentation, with mappings, lists, `|` for multiline scripts, and anchors for reuse; `default` is usually the cleaner way to share settings.
- Use `before_script` for setup and `after_script` for cleanup, and read variables like `$CI_COMMIT_SHA`, `$CI_PIPELINE_ID`, and `$CI_PROJECT_DIR` from the environment.
- Cache pip downloads with `cache: key/paths` to speed up repeated runs; remember it is not a place to keep results.
- Validate with CI Lint, read logs from the bottom, and reproduce failures locally with the same image.
- Coming up later today: stage and job control (`needs`, `parallel`, `matrix`, `rules`), artifacts and reports, and secrets and variables.

## Additional Resources

- GitLab Docs, *CI/CD YAML syntax reference*: https://docs.gitlab.com/ci/yaml/
- GitLab Docs, *Get started with GitLab CI/CD (quick start)*: https://docs.gitlab.com/ci/quick_start/
- GitLab Docs, *Runners*: https://docs.gitlab.com/runner/ and https://docs.gitlab.com/ci/runners/
- GitLab Docs, *Predefined CI/CD variables reference*: https://docs.gitlab.com/ci/variables/predefined_variables/
- GitLab Docs, *Caching in GitLab CI/CD*: https://docs.gitlab.com/ci/caching/
