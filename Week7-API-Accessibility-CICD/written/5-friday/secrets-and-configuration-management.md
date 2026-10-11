# Secrets and Configuration Management

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish **configuration** from **secrets**, and explain why they are handled differently.
- Explain the twelve-factor rule "store config in the environment" and apply it to a Python test framework.
- Recognise what counts as a secret (API keys, tokens, passwords, certificates) and the ways secrets leak.
- Explain why a committed secret stays compromised even after deletion, and carry out the response: **rotate first**.
- Create GitLab CI/CD variables at project, group and instance level, and choose the right type and flags (Variable vs File, Masked, Masked and hidden, Protected, Expanded vs Raw, environment scope).
- Predict which value wins when the same variable is defined in several places (precedence), and tell predefined variables from custom ones.
- Read configuration in Python with `os.environ`, `os.getenv`, `python-dotenv` and `pydantic-settings`, failing fast when something is missing.
- Keep secrets out of job logs, test reports and artifacts.
- Describe secret scanning (gitleaks, GitLab Secret Detection, pre-commit), external secret managers and short-lived OIDC credentials, least privilege and rotation.
- Set up safe test accounts and test data for API tests.

---

## Why This Matters

This week you built an API test suite, added accessibility checks, and put both into a GitLab pipeline. All of it has a quiet dependency: **values that must come from somewhere**. Which URL does the test hit? Which username and password does it log in with? Which token goes into the `Authorization` header?

On Tuesday you learned how APIs authenticate callers: API keys, bearer tokens, Basic auth, OAuth-style flows. Every one of those mechanisms depends on a credential that the client must hold and send. In Postman you pasted a token into an environment variable and clicked Send. In a pipeline, nobody is at the keyboard, so the credential has to be delivered automatically, and it has to be delivered in a way that does not expose it to everyone who can read the repository or the job log.

Your tests must run in several places with different URLs and credentials without editing code, and credentials are the most valuable thing in the project: bots scan public repositories for leaked keys within minutes, and even private repositories are read by former team members, contractors, forks and shared log pages.

**Configuration management** solves the first problem. **Secrets management** solves the second. They are the same skill seen from two sides: keep everything that varies out of the code, and keep everything sensitive out of the repository and the logs. It is also the last piece that makes your Week 7 pipeline "real": a pipeline that only works with a password hard-coded in a file is not something you can ship or share.

---

## The Concept

### 1. Configuration versus secrets

**Configuration** is any setting that can change between runs or environments without changing the logic of the program. **Secrets** are the subset of settings that grant access or prove identity.

| | Configuration | Secret |
|---|---|---|
| What it is | Settings that vary by environment or run | Values that grant access or identity |
| Examples | `BASE_URL`, `API_TIMEOUT=10`, `LOG_LEVEL=INFO`, `TEST_ENV=staging`, browser name | `API_PASSWORD`, API keys, bearer tokens, client secrets, private keys |
| Harm if exposed | Usually low | High: unauthorised access |
| In Git? | Usually yes (defaults, `.env.example`) | Never |
| Where it lives | `.gitlab-ci.yml`, config files, plain CI variables | Masked/protected CI variables or a secret manager |
| In logs? | Fine | Must never appear |

A quick test: **"Would I be comfortable pasting this value into the team chat?"** A staging URL: yes. A password: no. That second kind is a secret.

### 2. Twelve-factor: "store config in the environment"

The **Twelve-Factor App** is a widely used set of guidelines for building software that deploys cleanly. Factor III says: *store config in the environment*. The code reads **environment variables**; where those variables come from is not the code's concern.

An environment variable is a named string that the operating system gives to a process when it starts. In a shell: `export API_BASE_URL=https://test.example.com`. Any program started from that shell can read it.

Why it works: one codebase runs everywhere, no secrets in the repository, and changing a target is a variable edit, not a commit.

You already used this idea on Monday, with Postman environments (one variable name, different values per environment). A CI/CD variable is the pipeline version of the same idea.

### 3. What counts as a secret

Treat these as secrets:

- **Passwords**: for the test account, a database, a service login.
- **API keys**: static strings that identify and authorise an application (Tuesday's `X-API-Key` header).
- **Tokens**: bearer tokens, JWTs, personal access tokens, refresh tokens, GitLab project/deploy tokens. A short-lived access token is still a secret until it expires.
- **Client secrets** from OAuth-style flows.
- **Private keys and certificates**: TLS private keys, SSH keys, signing keys, `.pem`/`.key`/`.pfx` files. (A public certificate is not secret; the private key paired with it is.)
- **Connection strings** that contain credentials (`postgres://user:pass@host/db`).
- **Webhook URLs** with embedded tokens (Slack webhook URLs, for example).
- **Session cookies** captured by a browser tool or a Playwright storage-state file after login.

### 4. Why you never commit secrets, and what to do if you do

Git is designed to **remember everything**. When you commit a file, its content is stored in the repository's history. Deleting the file in a later commit hides it from the current tree but not from history; anyone who clones can run `git log -p` or check out the old commit and read it. Rewriting history (with `git filter-repo`) can remove it from your copy, but cannot remove it from clones, forks, caches, CI runners, or the machines of everyone who pulled in the meantime.

Other leak paths: job logs (`echo`, `env`, `set -x`), artifacts and reports (headers, traces), screenshots and chat, URLs with `?api_key=...`, error messages with connection strings, pipelines from forks, and shared admin accounts.

**What to do if a secret leaks: rotate first.**

1. **Revoke or rotate the secret immediately.** Generate a new one in the system that issued it and disable the old one. Assume it was copied. This is the only step that actually ends the exposure.
2. **Update the CI/CD variable** (or secret manager entry) with the new value, and re-run the pipeline to prove it works.
3. **Check usage logs** of the affected system for activity you do not recognise, from the time of the leak onward.
4. **Clean up** the repository history (`git filter-repo` or your platform's tooling), and delete affected job logs and artifacts. Do this *after* rotation, because it is cleanup, not a fix.
5. **Find the cause** and add a control so it cannot recur (scanning, a pre-commit hook, a `.gitignore` rule).
6. **Report it** under your organisation's security policy. Fast, honest reporting limits damage; hiding a leak makes it worse.

The sentence to remember: **"I deleted the commit" is not "I fixed the leak."**

### 5. GitLab CI/CD variables: where they are defined

A **CI/CD variable** is a key-value pair that GitLab injects into jobs as an environment variable. There are four places to define one:

| Where | How | Typical use |
|---|---|---|
| **Project** | Project > Settings > CI/CD > Variables | Test credentials and URLs for this project |
| **Group** | Group > Settings > CI/CD > Variables | Values shared by many projects (a shared registry token) |
| **Instance** | Admin area (self-managed GitLab only) | Organisation-wide defaults |
| **`.gitlab-ci.yml`** | `variables:` keyword at the top level or inside a job | Non-secret configuration |

The rule of thumb: **non-secret configuration may live in the YAML (reviewed, versioned); secrets live in the Settings UI** (or an external manager), never in the YAML, because the YAML is committed.

Here is a simple pipeline file that defines non-secret configuration and uses a secret supplied from Settings:

```yaml
stages:
  - test

variables:
  TEST_ENV: "test"
  API_TIMEOUT: "10"
  LOG_LEVEL: "INFO"

api-regression:
  stage: test
  script:
    - pytest -m regression
```

Here `variables:` defines global, non-secret configuration (values are quoted so YAML keeps them as strings), and `pytest -m regression` runs tests that read `API_USER` and `API_PASSWORD` from Settings, so no secret appears in the file or the log.

The anti-pattern, which you must never do:

```yaml
variables:
  API_PASSWORD: "Passw0rd!"      # BAD: now in Git history forever
```

### 6. Variable types and flags

When you add a variable in Settings you choose a **type** and several **flags**.

**Type: Variable or File**

- **Variable** (default): the value is placed in an environment variable. `$API_PASSWORD` contains the text itself.
- **File**: GitLab writes the value to a temporary file on the runner and the variable contains the **path** to that file. Use it for multi-line or file-shaped secrets: a service-account JSON key, a TLS certificate, a kubeconfig, a whole `.env`-style file. Many tools expect a path, so this fits naturally.

```yaml
cloud-tests:
  stage: test
  script:
    - export GOOGLE_APPLICATION_CREDENTIALS="$GCP_KEY_FILE"
    - pytest -m cloud
```

Here `$GCP_KEY_FILE` is a path (for example `/builds/.../GCP_KEY_FILE.tmp`), not the JSON; the Google client library expects a path, and the file exists only for the life of the job.

**Visibility flags** (the exact labels have changed between GitLab versions; check the docs for your instance):

| Flag | What it does | Use it for |
|---|---|---|
| **Visible** | Value shows in job logs and in Settings | Non-secret config such as `API_BASE_URL` |
| **Masked** | GitLab replaces the value with `[MASKED]` in job logs | Any secret |
| **Masked and hidden** | Masked in logs, and the value is **never shown again in the Settings UI** after you save (you can only replace it) | High-value secrets; reduces exposure to anyone with Settings access |

**Masking limits.** To be maskable, a value generally must be a single line, at least 8 characters, and use only a limited character set (letters, digits and a few symbols). A value that does not qualify cannot be saved as masked. More important: masking is **exact string matching** on the log output. If something prints the value Base64-encoded, URL-encoded, split across lines, or with characters inserted, the match fails and the secret appears in plain text. Masking is a **safety net**, not permission to print secrets.

**Protect variable.** A protected variable is only given to pipelines running on **protected branches or protected tags**. A feature-branch pipeline simply does not receive it.

**Expand variable reference (Expanded vs Raw).** By default GitLab expands references: if a value contains `$OTHER`, GitLab replaces it with the value of `OTHER` before the job starts. A password such as `abc$DEF123` would be silently altered. Clear the **Expand variable reference** checkbox to make the variable **raw**, so the value is used exactly as typed. In YAML the equivalent is `expand: false` on a variable declared with `value:`.

**Environment scope.** Described in the next section.

**Description.** Free text. Use it to record the purpose, owner and rotation date; future you will be grateful.

### 7. Environment-scoped variables

You can define the **same key several times**, each with a different **Environment scope**. GitLab picks the one that matches the environment of the job.

| Key | Value | Environment scope |
|---|---|---|
| `API_BASE_URL` | `https://test.example.com/api` | `test` |
| `API_BASE_URL` | `https://staging.example.com/api` | `staging` |
| `API_PASSWORD` | (generated) | `test` |
| `API_PASSWORD` | (different generated value) | `staging` |

A job selects its environment with the `environment:` keyword:

```yaml
test:test-env:
  stage: test
  environment:
    name: test
  script:
    - pytest -m regression

test:staging-env:
  stage: test
  environment:
    name: staging
  script:
    - pytest -m smoke
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

The `environment: name:` keyword selects which scoped values the job receives; the `rules:` line runs the staging job only on the default branch. Test code is identical in both jobs.

This is the pipeline version of Monday's Postman environment dropdown.

### 8. Precedence: which value wins?

If the same variable name is defined in several places, GitLab uses a fixed order. From highest to lowest priority (simplified from the GitLab documentation):

1. Variables entered when **running a pipeline manually**, passed by a **trigger**, or set on a **schedule**.
2. **Project** variables (Settings).
3. **Group** variables.
4. **Instance** variables.
5. Variables inherited from earlier jobs (for example a `dotenv` report).
6. Variables defined **inside a job** in `.gitlab-ci.yml`.
7. Variables defined **globally** in `.gitlab-ci.yml`.
8. Deployment variables.
9. **Predefined** variables.

(There are also pipeline-policy levels above these in some editions. Always check the current docs, because this list evolves.)

Two things surprise beginners:

- **Settings variables beat the YAML.** A project variable named `API_TIMEOUT` overrides `API_TIMEOUT` in `.gitlab-ci.yml`. So if a YAML default "isn't working", look in Settings.
- **Within the Settings levels, the closest wins**: project over group over instance. If two *environment scopes* both match, the more specific scope wins.

A practical use: you put `LOG_LEVEL: "INFO"` in the YAML, and when debugging you run the pipeline manually with `LOG_LEVEL=DEBUG` in the "Run pipeline" form. The manual value wins for that run only.

### 9. Predefined versus custom variables

**Predefined variables** are created by GitLab for every job. You do not set them. Useful ones:

Useful ones: `CI` (true in GitLab CI), `CI_COMMIT_BRANCH`, `CI_COMMIT_SHA`, `CI_DEFAULT_BRANCH`, `CI_PIPELINE_ID`, `CI_ENVIRONMENT_NAME`, `CI_PROJECT_DIR`, and `CI_JOB_TOKEN` (a secret).

**Custom variables** are the ones you define: `API_BASE_URL`, `API_USER`, `API_PASSWORD`, `TEST_ENV`. A good habit is to avoid names starting with `CI_` or `GITLAB_`, which are reserved.

Remember that some predefined values (like `CI_JOB_TOKEN`) are secrets too, even though you did not create them. Never print them.

### 10. Protected branches, tags and protected variables

A **protected branch** (such as `main`) has rules: who may push, who may merge, whether force-push is allowed. A **protected tag** works the same for release tags. A **protected variable** is only handed to pipelines running on a protected branch or tag.

The result is a trust boundary:

Anyone who can create a branch can edit `.gitlab-ci.yml` on it, and a careless edit such as `- env` would print every variable the pipeline received. If strong credentials are **Protected**, unprotected branch pipelines never receive them.

The trade-off: protected variables are absent on feature branches, so tests that need them fail there. The usual design is **two tiers**:

| Variable | Environment scope | Protected | Purpose |
|---|---|---|---|
| `API_USER`, `API_PASSWORD` | `test` | No | Low-privilege QA account used by every branch |
| `STAGING_API_PASSWORD` | `staging` | **Yes** | Stronger credential, only on `main` |
| `PROD_DEPLOY_TOKEN` | `production` | **Yes** | Manual deploy job on `main` |

Feature branches use the harmless test account; `main` uses the stronger ones. A common mistake is marking everything Protected and then wondering why every feature-branch pipeline fails with "Missing required environment variable".

### 11. Reading configuration in Python

You met `os.getenv` on Wednesday. Here is the full picture.

**Basic access.**

```python
import os

base_url = os.environ["API_BASE_URL"]
timeout = os.getenv("API_TIMEOUT", "10")
maybe = os.getenv("OPTIONAL_THING")
```

`os.environ["X"]` raises `KeyError` when missing (right for required values); `os.getenv("X", default)` returns a default (only for non-secrets); values are always strings, so convert with `float()`.

**Fail fast.** If a required value is missing, you want a clear message at startup, not a confusing `401 Unauthorized` thirty tests later. A hand-written settings module:

```python
# config/settings.py
import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable {name}. "
            "Set it in your shell or .env locally, or as a CI/CD variable in GitLab."
        )
    return value


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    timeout: float
    api_user: str
    api_password: str

    def __repr__(self) -> str:
        return (
            f"Settings(env={self.env!r}, base_url={self.base_url!r}, "
            f"timeout={self.timeout}, api_user={self.api_user!r}, api_password='***')"
        )


def load_settings() -> Settings:
    return Settings(
        env=os.getenv("TEST_ENV", "test"),
        base_url=_required("API_BASE_URL"),
        timeout=float(os.getenv("API_TIMEOUT", "10")),
        api_user=_required("API_USER"),
        api_password=_required("API_PASSWORD"),
    )
```

Key points: `_required` treats missing and empty as the same failure (an unset CI variable often arrives empty); the error names the variable, never its value; the custom `__repr__` masks the password so `print(settings)` is safe; secrets have no defaults, so a missing one cannot be silently replaced.

**Option: `pydantic-settings`.** If you prefer a library that handles types and validation, `pydantic-settings` reads environment variables into a typed model, and its `SecretStr` type hides values when printed.

```python
# config/settings_pydantic.py
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    test_env: str = "test"
    api_base_url: str
    api_timeout: float = 10
    api_user: str
    api_password: SecretStr


settings = Settings()
password_value = settings.api_password.get_secret_value()
```

Key points: fields fill from environment variables case-insensitively (`api_base_url` reads `API_BASE_URL`); `env_file` reads `.env` locally while real variables win; fields without defaults are required, so `Settings()` raises a validation error naming the missing field; `SecretStr` prints as `**********` and needs a deliberate `get_secret_value()`.

**Local development with `.env`.** On your laptop you do not want to `export` five variables every day. Use a `.env` file loaded by `python-dotenv`:

```
# .env  (git-ignored; real local values)
API_BASE_URL=https://test.example.com/api
API_USER=qa_tester
API_PASSWORD=local-dev-password
```

```
# .env.example  (committed; no real values)
API_BASE_URL=https://test.example.com/api
API_USER=
API_PASSWORD=
```

```python
# conftest.py (top of file)
from dotenv import load_dotenv

load_dotenv()
```

Explanation:

- `.env` holds your private local values and is in `.gitignore`, so Git never tracks it.
- `.env.example` is the **template** others copy to `.env`. It documents what variables exist with no secret values.
- `.gitignore` also excludes key files and generated reports.
- `load_dotenv()` reads `.env` into the process environment. By default it does **not override** variables already set, so in CI, where the real variables exist and `.env` does not, the pipeline values win and nothing breaks.

**Only require what a suite needs.** A mocked unit test should run with no real credentials. Load settings lazily, in a fixture that only the live API tests use, so "missing API_PASSWORD" does not break unrelated tests.

### 12. Per-environment configuration (dev, stage, prod)

The aim is: **one test codebase, many targets, selected by variables.** A common set:

| Variable | dev (local) | stage | prod (read-only smoke only) |
|---|---|---|---|
| `TEST_ENV` | `dev` | `staging` | `production` |
| `BASE_URL` | `http://localhost:8000` | `https://staging.example.com` | `https://www.example.com` |
| `API_BASE_URL` | `http://localhost:8000/api` | `https://staging.example.com/api` | `https://www.example.com/api` |
| Credentials | local `.env` | staging-scoped, protected | read-only account, protected |

In practice `.env` supplies the dev values locally and environment-scoped GitLab variables supply stage and prod. Test code reads only `settings.base_url`; avoid `if env == "staging"` branches and use a setting such as `ALLOW_WRITES=false` to skip destructive tests.

### 13. Preventing leaks in logs, reports and artifacts

Pipelines are very good at producing text: logs, JUnit XML, HTML reports, traces, screenshots. Each is a place a secret can land.

**Never print secrets.**

```yaml
script:
  - pytest -m regression
  - echo "$REGISTRY_PASSWORD" | docker login -u "$REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  # BAD examples, shown commented out:
  # - env
  # - echo "password is $API_PASSWORD"
  # - set -x
  # - curl -u "user:$API_PASSWORD" https://example.com
```

Safe: `pytest` (Python reads the variables internally) and `--password-stdin`, which keeps the password off the command line. Unsafe: `env` dumps every variable; `echo` prints the secret; `set -x` echoes expanded commands and defeats masking; `curl -u user:$PASS` exposes it in process lists and verbose output.

**A safe configuration check.** To confirm a variable is present without showing it:

```yaml
script:
  - python -c "import os; print('API_BASE_URL set:', bool(os.getenv('API_BASE_URL')))"
```

This prints only `True` or `False`.

**Mask in your own logging.** Redact headers such as `Authorization`, `X-API-Key` and `Cookie` (replace the value with `***`) before logging requests or attaching them to reports.

**Reports and artifacts.** Artifacts are downloadable by project members for weeks. Keep credentials out of JUnit properties and report metadata; do not upload Playwright traces, HAR files or storage-state files unless they come from a throwaway account; never put `.env` or key files under `artifacts: paths:`; never bake secrets into Docker images; use `expire_in: 7 days`.

**Where masking fails (summary).** Encoded or split values; values too short or with unsupported characters; secrets printed by *other* tools in changed forms; secrets in artifacts (masking applies to the job log, not to files you write).

### 14. Secret scanning: gitleaks, GitLab Secret Detection, pre-commit

Prevention by discipline is not enough; add tools that catch mistakes automatically.

Tools: **gitleaks** and **trufflehog** scan files and history for key-like patterns; **GitLab Secret Detection** is a built-in CI scanner; **pre-commit hooks** scan before each commit so the secret never enters history.

Enable GitLab's scanner:

```yaml
include:
  - template: Security/Secret-Detection.gitlab-ci.yml
```

`include:` pulls in a ready-made GitLab job that scans new commits and reports findings.

Add a local pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```

After `pip install pre-commit` and `pre-commit install`, every `git commit` runs gitleaks and blocks on secret-like strings; `rev:` pins the version so everyone runs the same one.

Scanners produce false positives and negatives; treat them as a safety net, not a replacement for habit.

### 15. External secret managers and short-lived credentials

GitLab CI/CD variables are convenient but static: the secret lives in GitLab until someone changes it. Larger organisations move to **secret managers**.

| Approach | Idea |
|---|---|
| **HashiCorp Vault** | Central store; jobs authenticate and fetch secrets at run time |
| **AWS Secrets Manager, Azure Key Vault, Google Secret Manager** | Cloud-native stores with access policies and audit logs |
| **GitLab `secrets:` keyword** | Declares which secrets a job fetches from a supported external manager |
| **OIDC / JWT ID tokens** | The job proves its identity with a signed, short-lived token; no stored password at all |
| **Dynamic secrets** | Credentials created on demand that expire automatically (for example a database user valid for one hour) |

**The OIDC idea.** Instead of storing a password, the job asks GitLab for a signed, short-lived ID token (a JWT, as on Tuesday) stating "I am job J in project P on branch `main`". Vault or a cloud provider, configured to trust GitLab, verifies it and returns temporary credentials that expire in minutes. Nothing long-lived is stored.

A simplified example with Vault:

```yaml
api-regression:
  stage: test
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    API_PASSWORD:
      vault: qa/test-env/api_password@secrets
      token: $VAULT_ID_TOKEN
  script:
    - pytest -m regression
```

Key lines: `id_tokens` asks GitLab to mint a JWT; `aud` sets the audience so the token cannot be replayed elsewhere; `secrets:` fetches `API_PASSWORD` from Vault using `path/to/secret/field@mount` and authenticates with the token. By default GitLab delivers fetched secrets as File-type variables (set `file: false` for plain values).

You will not be asked to build this today. Know that the direction of travel is **fewer long-lived secrets, shorter lifetimes, automatic rotation**.

### 16. Least privilege and rotation

**Least privilege** means every account, token and key can do only what its job requires.

- Your API test account should be able to call the endpoints the tests need and nothing more. If it is an admin, a leak is a catastrophe; if it is a limited test user in a non-production system, a leak is an annoyance.
- Create **separate credentials per environment and per purpose** (test vs staging; testing vs deploying). One leaked key then compromises one thing.
- Give tokens narrow **scopes** (for example `read_api` rather than `api`) and an **expiry date**.
- Never use your personal account or token for CI; people leave teams.

**Rotation** means replacing a secret on a schedule so an unnoticed leak has a limited lifetime. Give every secret an owner, purpose and interval (for example 90 days) in its description; rotate immediately when someone leaves or a leak is suspected; and drill it: update the CI variable, re-run the pipeline, confirm it passes.

### 17. Test accounts and test data for API tests

API tests need identities and data. Handle both deliberately.

**Test accounts**

- Use **dedicated QA accounts** that exist only in non-production environments, with obviously fake identities (`qa_tester@example.test`).
- If a test needs several roles (admin, editor, read-only), create one account per role so you can verify permissions, and keep each with least privilege.
- Never use real customer credentials or personal data in tests.
- If the system forces you to test in production (read-only smoke tests), use a dedicated read-only account, protected variables, and extra caution.

**Test data**

- Prefer data your tests create and clean up themselves; use unique values (timestamp or UUID) so parallel runs do not collide.
- No real personal data and no credentials in fixture files; a fixture with `"password": "hunter2"` is a committed secret.
- Obtain tokens by logging in at the start of the run (a session-scoped fixture) with the password from the environment, not from a pasted long-lived token.

### 18. Common mistakes

- Committing `.env` or a Postman environment export with tokens: use `.gitignore`, `.env.example`, scrub exports.
- Believing a deleted commit is safe: rotate.
- Relying on masking while still echoing values.
- Putting the secret in `.gitlab-ci.yml` `variables:`.
- Marking everything Protected, then wondering why branches fail: use two credential tiers.
- Personal/admin account for CI, or one password everywhere.
- A password with `$` altered unexpectedly: make the variable raw.
- Defaults for secrets (`os.getenv("API_PASSWORD", "admin")`).
- Uploading traces, HAR files or `.env` as artifacts; `set -x`/`env` in secret-handling jobs.
- Never rotating or auditing variables.

### 19. Practice exercises

**Exercise 1: Classify and decide.**
For each item say whether it is configuration or a secret, and where it should live: (a) `https://staging.example.com/api`, (b) the QA account password, (c) `LOG_LEVEL=DEBUG`, (d) `postgres://app:s3cret@db:5432/test`, (e) a project access token used to download artifacts.

*Solution.* (a) Configuration: environment-scoped CI variable. (b) Secret: masked and hidden project variable, scoped to the environment. (c) Configuration: global `variables:` in the YAML. (d) Secret, because it embeds a password: masked variable, or store the password separately and build the string in code. (e) Secret: masked, protected, minimum scope (`read_api`), with an expiry date.

**Exercise 2: Design variables for two environments.**
Your API tests must hit `test` from any branch, and `staging` only from `main`. Specify the CI/CD variables (key, scope, protected, masked) and a job for each.

*Solution.*

| Key | Environment scope | Protected | Masked/hidden |
|---|---|---|---|
| `API_BASE_URL` | `test` | No | No |
| `API_USER` | `test` | No | No |
| `API_PASSWORD` | `test` | No | Masked and hidden |
| `API_BASE_URL` | `staging` | Yes | No |
| `API_USER` | `staging` | Yes | No |
| `API_PASSWORD` | `staging` | Yes | Masked and hidden |

```yaml
stages:
  - test

test-on-test-env:
  stage: test
  environment:
    name: test
  script:
    - pytest -m regression

test-on-staging:
  stage: test
  environment:
    name: staging
  script:
    - pytest -m smoke
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Explanation: the `test` credentials are unprotected, low-privilege, and available everywhere. The `staging` credentials are protected, so only protected-branch pipelines get them, and the `rules:` line stops the staging job from even being created on feature branches (where it would fail on missing variables). The same test code runs in both because settings come from the environment.

**Exercise 3: Contain a leak.**
A teammate pasted `API_PASSWORD` into a debug `print()`, merged to `main`, and the job log (public to project members) now shows it unmasked because it was Base64-encoded in the output. Write the ordered response.

*Solution.*
1. **Rotate the password** in the system that owns it; disable the old one. (Containment first.)
2. Update the masked, hidden `API_PASSWORD` variable with the new value and re-run the pipeline to confirm it passes.
3. Review the system's login and access logs since the log was published for unfamiliar activity.
4. Delete the job log (and any artifacts that contain it) in GitLab; remove the `print()` in a merge request. Cleanup comes after rotation.
5. Root cause: masking only matches exact strings. Add review rules, redaction, Secret Detection and a pre-commit scan.
6. Report per the security policy, in a blameless way, noting the time window of exposure.

### 20. Quiz

**Question 1.** Which of these is configuration rather than a secret?
A) A bearer token B) `API_TIMEOUT=10` C) A private key D) A password in a connection string

**Question 2.** You deleted a commit that contained an API key, force-pushed, and the key no longer appears on the branch. What is the correct next step?
A) Nothing, it is gone B) Rotate the key, because it may already have been copied C) Mark the key as Protected D) Ask teammates to delete their clones

**Question 3.** A project variable `LOG_LEVEL=DEBUG` and a global `variables: LOG_LEVEL: "INFO"` in `.gitlab-ci.yml` both exist. Which value does the job see?
A) `INFO`, because the YAML is committed B) `DEBUG`, because project variables from Settings take precedence over YAML-defined ones C) Whichever is alphabetically first D) The job fails

**Question 4.** Why does masking not protect a secret that your script prints Base64-encoded?
A) Masking only works on weekdays B) Masking matches the exact stored string, and the encoded text is different C) Base64 is encrypted D) Masking applies only to artifacts

**Question 5.** A feature-branch pipeline fails with "Missing required environment variable STAGING_API_PASSWORD". The variable exists in Settings. What is the most likely cause?
A) The variable is Protected, and feature branches are not protected branches B) The variable is too long C) Python cannot read variables D) The variable is Masked

**Answers.**
1. **B.** A timeout varies by environment but grants no access. The others are credentials.
2. **B.** Anyone who cloned, forked or cached the repository, and any bot scanning it, may have copied the key. Rotation is the only step that ends the exposure.
3. **B.** Project, group and instance variables from Settings rank above variables defined in `.gitlab-ci.yml`. (A manual "Run pipeline" value would beat both.)
4. **B.** Masking is exact string matching on log output, so any transformation (Base64, URL encoding, splitting) escapes it. Never print secrets.
5. **A.** Protected variables are only passed to pipelines on protected branches or tags. Use a lower-privilege unprotected credential for branches, or restrict the job with `rules:`.

### 21. Glossary

### Configuration
Non-sensitive settings that vary by environment or run (URLs, timeouts, log level).

### Secret
A value that grants access or proves identity: passwords, API keys, tokens, private keys.

### CI/CD variable
A key-value pair GitLab injects into jobs as an environment variable.

### Masked
GitLab replaces an exact match of the value with `[MASKED]` in job logs.

### Masked and hidden
Masked in logs, and the value cannot be viewed again in Settings after saving.

### Protected variable
Only available to pipelines on protected branches or tags.

### Expanded / Raw
Expanded variables have `$REFERENCES` substituted; raw variables are used exactly as typed.

### Environment scope
A restriction that makes a variable apply only to jobs targeting a matching environment (`staging`, `review/*`).

### Fail fast
Detecting a missing or invalid setting at startup with a clear error.

### Secret scanning
Tools (gitleaks, trufflehog, GitLab Secret Detection) that look for credentials in code and history.

### Secret manager
A dedicated service (Vault, AWS Secrets Manager, Key Vault) that stores secrets and controls access.

### OIDC / ID token
A short-lived signed token (JWT) that proves a job's identity so it can obtain temporary credentials.

---

## Summary

- **Configuration** (non-sensitive, varies by environment) and **secrets** (credentials) are kept apart. Both reach the code through **environment variables**, following the twelve-factor rule; the code never contains the values.
- Secrets include passwords, keys, tokens, private keys and connection strings, and leak through source, history, logs, artifacts, URLs and errors.
- Git remembers everything, so a committed secret is compromised even after deletion. **Rotate first**, then clean up, investigate and report.
- GitLab CI/CD variables can be defined at project, group and instance level or in `.gitlab-ci.yml`. Put secrets in Settings, never the YAML. Choose **Variable or File** type, **Masked** or **Masked and hidden**, **Protected**, **Expanded or Raw**, and an **environment scope**.
- Precedence: pipeline-run values beat project, group and instance variables, which beat YAML-defined ones, which beat predefined ones. Protected variables only reach protected branches and tags, so use a two-tier credential design.
- In Python, use `os.environ[...]` for required values, `os.getenv` with defaults only for non-secrets, `python-dotenv` for local `.env`, and optionally `pydantic-settings` with `SecretStr`. Fail fast with messages that name the variable but never reveal it.
- Never `echo`, `env` or `set -x` secrets; redact logs and keep credentials out of artifacts.
- Add secret scanning; consider Vault, cloud managers, `secrets:` and OIDC; use least privilege and rotation.

## Additional Resources

- GitLab Docs, *CI/CD variables*: https://docs.gitlab.com/ci/variables/
- GitLab Docs, *Using external secrets in CI*: https://docs.gitlab.com/ci/secrets/
- GitLab Docs, *Secret detection*: https://docs.gitlab.com/user/application_security/secret_detection/
- OWASP, *Secrets Management Cheat Sheet*: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- The Twelve-Factor App, *III. Config*: https://12factor.net/config
- pydantic-settings documentation: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- gitleaks project: https://github.com/gitleaks/gitleaks
