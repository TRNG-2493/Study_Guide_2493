# Exercise: Package a Utility Library and Kick Off Project 1 (QE Foundations)

**Week 2 / Monday - Python Modules & Environment Management**
**Mode:** A - Code Lab (individual) | **Time:** 2.5 hours (budget 2-3 h) | **Platform:** Windows PowerShell (bash commands given where they differ)

> **Project 1 milestone (Monday): "Kickoff - repo + structure."**
> By the end of today you own ONE Git repository called **`qe-foundations`** containing the importable package **`qe_foundations/`**
> with its first sub-package **`qe_foundations/utils/`**, a documented virtual-environment setup, `requirements.txt` /
> `requirements-dev.txt`, and empty placeholder folders for the rest of the week. **This same repo is used all week**
> (Tue `qe_foundations/ingestion/`, Wed logging + unit tests in `tests/`, Thu `sql/` validation queries, Fri joins validation + integration).
> Keep the names exactly as written here.

---

## 1. Scenario

You joined a QE team that validates data for a client. The only shared code is `legacy_helpers.py`: one file of helpers for building and checking QA test data (slugs for test-case IDs, email checks, seeded random users, date helpers). It prints text when imported, nobody knows what depends on it, and it cannot be installed anywhere cleanly.

Your lead asks you to (1) turn it into a proper package, (2) make the project reproducible for any teammate with a virtual environment and `requirements.txt`, and (3) put it in a Git repository others can clone and run. That repository is the foundation of Project 1.

## 2. Learning objectives (what you practise)

| Skill | Lesson it comes from |
|-------|----------------------|
| Split code into modules, `import` / `from ... import`, `if __name__ == "__main__"`, silent imports | `creating-and-importing-modules.md` |
| Package + sub-package, `__init__.py`, public API re-exports, absolute imports | `python-packages.md` |
| `python -m pip`, version specifiers, `requirements.txt` | `pip-and-package-management.md` |
| `python -m venv`, activate, `.gitignore` for `.venv` | `virtual-environments.md` |
| `datetime`, `random.Random(seed)` (used inside your utils) | `built-in-python-modules.md` |
| `git init`, remotes, `push -u`, clone, `pull` | `collaborative-git-workflow-pull-fetch-and-push.md` |

Everything needed is in those lessons and in the instructor demo (`qa_toolkit`). No other topics are required.

## 3. What you receive (`starter_code/`)

| File | Purpose |
|------|---------|
| `legacy_helpers.py` | the one-file helper script to split into modules |
| `smoke_utils.py` | PASS/FAIL smoke script that imports your finished library. **Do not edit.** |
| `check_exercise.py` | self-check: validates structure, requirements, imports, behaviour and Git state |

## 4. Final repository layout (target)

```
qe-foundations/
|-- .gitignore
|-- README.md
|-- requirements.txt            <- runtime: requests
|-- requirements-dev.txt        <- "-r requirements.txt" + pytest
|-- smoke_utils.py              <- from starter_code (committed)
|-- check_exercise.py           <- from starter_code (committed)
|-- qe_foundations/
|   |-- __init__.py             <- __version__
|   `-- utils/
|       |-- __init__.py         <- re-exports the public API
|       |-- strings.py          <- normalize_whitespace, slugify, is_valid_email, mask_email (NEW)
|       |-- numbers.py          <- is_positive_int, clamp, percent
|       |-- dates.py            <- add_days, days_between (NEW), is_weekend, timestamp_for_filename
|       `-- data_gen.py         <- FIRST_NAMES, ROLES, make_users
|-- tests/.gitkeep              <- placeholder (Wed)
|-- data/.gitkeep               <- placeholder (Tue)
`-- docs/                       <- at least one file, e.g. structure.md
```
(`.venv/` exists on your machine but is **never** committed. `legacy_helpers.py` does **not** appear in the final repo.)

---

## 5. Tasks (time-boxed)

| Part | Task | Time |
|------|------|------|
| 0 | Read the brief, locate starter files | 5 min |
| 1 | Create the repo folder, venv and `.gitignore` | 20 min |
| 2 | Split `legacy_helpers.py` into the `utils` package | 40 min |
| 3 | Write two new functions + run the smoke script | 25 min |
| 4 | Dependencies: `requirements.txt` + `requirements-dev.txt` | 15 min |
| 5 | `README.md`, `docs/`, placeholders | 15 min |
| 6 | Commit, push, and prove a fresh clone works | 25 min |
| 7 | Run the self-check, fix, final push | 5 min |
| | **Total** | **150 min** |

If you are more than 10 minutes behind at the end of Part 3, use the hints and move on; Parts 4-6 are the Project 1 deliverable.

### Part 0 - Orient (5 min)

1. Read sections 1-4 above. Open the written lessons you may need next to you.
2. Decide where the repo will live **outside** the course repository, for example `C:\Users\<you>\projects\qe-foundations` (PowerShell: `$HOME\projects\qe-foundations`).

### Part 1 - Repo, venv, `.gitignore` (20 min)

1. Create the folder and enter it; copy the three starter files in:

   | | Commands (run from the folder that contains `starter_code`) |
   |---|---|
   | PowerShell | `New-Item -ItemType Directory $HOME\projects\qe-foundations -Force \| Out-Null`<br>`Copy-Item starter_code\* $HOME\projects\qe-foundations\`<br>`cd $HOME\projects\qe-foundations` |
   | bash | `mkdir -p ~/projects/qe-foundations`<br>`cp starter_code/* ~/projects/qe-foundations/`<br>`cd ~/projects/qe-foundations` |

2. **Create `.gitignore` FIRST** (before any `git add`) so it ignores at least: `.venv/`, `__pycache__/`, `*.pyc`, `.env`.
3. Initialise Git on branch `main`: `git init -b main` (older Git: `git init` then `git branch -M main`). Check identity: `git config user.name` and `git config user.email`.
4. Create the virtual environment **inside the repo folder**: `python -m venv .venv` (PowerShell alternative: `py -m venv .venv`).
5. Activate it:

   | | Command |
   |---|---|
   | PowerShell | `.venv\Scripts\Activate.ps1` |
   | bash / Git Bash | `source .venv/bin/activate` (Git Bash on Windows: `source .venv/Scripts/activate`) |

6. Prove it: `python -c "import sys; print(sys.executable)"` must print a path **inside** `.venv`; your prompt shows `(.venv)`. Run `git status` - `.venv/` must **not** be listed.
7. First commit: `git add .gitignore` then `git commit -m "Add .gitignore"`.

> PowerShell says "running scripts is disabled"? Run once: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, reopen the terminal, activate again.

### Part 2 - Split the legacy file into a package (40 min)

Create the package `qe_foundations/` with sub-package `utils/` (each folder needs an `__init__.py`). Then **move** (copy, then delete the original) the functions from `legacy_helpers.py` into modules:

| Module | Move these |
|--------|------------|
| `qe_foundations/utils/strings.py` | `normalize_whitespace`, `slugify`, `is_valid_email` |
| `qe_foundations/utils/numbers.py` | `is_positive_int`, `clamp`, `percent` |
| `qe_foundations/utils/dates.py` | `add_days`, `is_weekend`, `timestamp_for_filename` |
| `qe_foundations/utils/data_gen.py` | `FIRST_NAMES`, `ROLES`, `make_users` |

Requirements:
- Each module begins with a one-line **docstring**, and imports only what it uses (`dates.py` needs `datetime`; `data_gen.py` needs `random`).
- **Importing must be silent.** The legacy file prints at import and runs demo code at the bottom; do **not** carry that over.
- `qe_foundations/__init__.py` contains a docstring and `__version__ = "0.1.0"` (nothing else needed).
- `qe_foundations/utils/__init__.py` **re-exports** every public function so users can write `from qe_foundations.utils import slugify`. Use **absolute imports** (`from qe_foundations.utils.strings import slugify`) and define `__all__`.
- Finally `git rm legacy_helpers.py` (or delete the file and `git add -A` it) - the repo must not contain it.

Quick test (venv active, from the repo root):
```
python -c "from qe_foundations.utils import slugify; print(slugify('  Hello World  '))"
```
It must print `hello-world` and **nothing else**. Commit: `git add qe_foundations` / `git commit -m "Package utils library"`.

### Part 3 - Two new functions + smoke script (25 min)

Add these two yourself (each with a one-line docstring):

1. `mask_email(email)` in `strings.py` - hides the user part of an email for safe logging of test data.
   - `mask_email("tester@example.com")` -> `"t***@example.com"` (first character, three stars, `@`, domain)
   - If `is_valid_email(email)` is `False`, return the input **unchanged**: `mask_email("not-an-email")` -> `"not-an-email"`
2. `days_between(start, end)` in `dates.py` - number of whole days from `start` to `end` (both `datetime.date`).
   - `days_between(date(2025, 1, 1), date(2025, 1, 31))` -> `30`; swapped arguments give `-30`.

Add both to `utils/__init__.py` (imports and `__all__`). Then run:
```
python smoke_utils.py
```
Expected: `requests version: ...` (installed in Part 4 - if `requests` is missing, jump to Part 4 step 2 and come back), then 7 `PASS` lines and `7/7 checks passed`. Commit: `git commit -am "Add mask_email and days_between"` (new files need `git add` first).

### Part 4 - Dependencies (15 min)

1. Create **`requirements.txt`** (runtime): one line `requests>=2.31,<3`. Write it by hand in VS Code (UTF-8).
2. Install from it with the venv active: `python -m pip install -r requirements.txt`. Check: `python -m pip show requests`.
3. Create **`requirements-dev.txt`** (development tools): first line `-r requirements.txt`, then `pytest>=8,<9`. Install it: `python -m pip install -r requirements-dev.txt`. (pytest is used from Wednesday; today it only lives in the dev file.)
4. Re-run `python smoke_utils.py` - it should print `7/7 checks passed`.
5. Commit: `git add requirements.txt requirements-dev.txt` / `git commit -m "Add requirements files"`.

> **Windows trap:** do NOT create requirements with PowerShell `>`: `python -m pip freeze > requirements.txt` in Windows PowerShell 5.1 writes **UTF-16**, which many tools cannot read. Safe form: `python -m pip freeze | Set-Content -Encoding ascii requirements-lock.txt`.

### Part 5 - README, docs, placeholders (15 min)

1. Create `tests/.gitkeep` and `data/.gitkeep` (empty files; Git does not track empty folders).
   PowerShell: `New-Item tests\.gitkeep, data\.gitkeep -ItemType File | Out-Null` | bash: `mkdir -p tests data && touch tests/.gitkeep data/.gitkeep`
2. Create `docs/structure.md`: a short table of the folders and what each is for (and which day adds it).
3. Write `README.md` containing: project name + one-sentence purpose; a **"Project 1 milestone - Week 2, Monday"** section (what exists now, what is coming Tue-Fri); a **Setup** section with numbered steps: create venv (`python -m venv .venv`), activate (**PowerShell and bash** commands), install (`python -m pip install -r requirements.txt`), verify (`python smoke_utils.py`); a short **Usage** example.
4. Commit: `git add .` then `git status` (check nothing unexpected is staged - no `.venv`, no `__pycache__`) then `git commit -m "Add README, docs and placeholders"`.

### Part 6 - Publish and prove a teammate can use it (25 min)

1. Create an **empty** repository named `qe-foundations` on your team's Git host (GitHub: no README, no .gitignore, no licence - it must be empty). Copy its URL.
   *No access to a host? Use the fallback local "remote": `git init --bare ..\qe-foundations-remote.git` (bash: `../qe-foundations-remote.git`) and use that path as the URL below.*
2. Connect and push:
   ```
   git remote add origin <url>
   git remote -v
   git push -u origin main
   ```
3. **Fresh-clone test** (simulates a teammate or CI). In a *different* folder:

   | | Commands |
   |---|---|
   | PowerShell | `cd $HOME\projects`<br>`git clone <url> qe-foundations-verify`<br>`cd qe-foundations-verify`<br>`python -m venv .venv`<br>`.venv\Scripts\Activate.ps1`<br>`python -m pip install -r requirements.txt`<br>`python smoke_utils.py` |
   | bash | `cd ~/projects`<br>`git clone <url> qe-foundations-verify`<br>`cd qe-foundations-verify`<br>`python -m venv .venv`<br>`source .venv/bin/activate`<br>`python -m pip install -r requirements.txt`<br>`python smoke_utils.py` |

   It must end with `7/7 checks passed` using **only** your README steps. If it fails, fix the repo (not the clone), push, `git pull` in the clone, and retry. When done: `deactivate`, then delete the verify folder.
4. Back in your real repo, re-activate your `.venv`.

### Part 7 - Self-check and hand-in (5 min)

From your real repo root, venv active:
```
python check_exercise.py --submit
```
Fix every `FAIL` (each prints a `HINT`). Commit and `git push` any fixes. Run it once more; the last line must say all required checks passed.

---

## 6. Hints (open one at a time - try for 10 minutes first)

<details><summary>Hint 1 - Part 1: ".venv shows up in git status"</summary>

The `.gitignore` must exist and list `.venv/`. If you already ran `git add .` before creating it: `git rm -r --cached .venv`, fix `.gitignore`, commit. See `virtual-environments.md` section 6.
</details>

<details><summary>Hint 2 - Part 2: "ModuleNotFoundError: No module named 'qe_foundations'"</summary>

(a) Run Python from the repo root, not from inside `qe_foundations/`. (b) Both `qe_foundations/__init__.py` and `qe_foundations/utils/__init__.py` must exist. (c) Check the spelling: folder `qe_foundations` (underscore), repo `qe-foundations` (hyphen). Lesson: `python-packages.md` ("What `__init__.py` does", "How Python finds your package").
</details>

<details><summary>Hint 3 - Part 2: shape of utils/__init__.py</summary>

```python
"""qe_foundations.utils - helpers for building and checking QA test data."""

from qe_foundations.utils.strings import slugify, normalize_whitespace, is_valid_email
# ... one import line per module ...

__all__ = ["slugify", "normalize_whitespace", "is_valid_email"]  # extend with every name
```
</details>

<details><summary>Hint 4 - Part 2: something is printed on import</summary>

Search your modules for `print(`. Library modules should define things only; any demo code belongs under `if __name__ == "__main__":` or should be deleted.
</details>

<details><summary>Hint 5 - Part 3: mask_email and days_between</summary>

`mask_email`: split with `email.split("@")`, then build `f"{local[0]}***@{domain}"`. Guard with `is_valid_email` first. `days_between`: subtracting two `date` objects gives a `timedelta`; it has a `.days` attribute (see `built-in-python-modules.md` section 5.5).
</details>

<details><summary>Hint 6 - Part 4: "No module named requests" although I installed it</summary>

You installed into a different Python. Activate `.venv`, then always use `python -m pip ...`. Compare `python -c "import sys; print(sys.executable)"` with `python -m pip --version`. Lesson: `pip-and-package-management.md` ("Why `python -m pip`").
</details>

<details><summary>Hint 7 - Part 6: push rejected / auth problems</summary>

"rejected ... fetch first": the remote was not empty. Either recreate it empty, or `git pull --rebase origin main` and push again. "Authentication failed": use a personal access token or your team's SSH setup; or use the local bare-repo fallback. Lesson: `collaborative-git-workflow-pull-fetch-and-push.md`, sections 2, 6, 7.
</details>

<details><summary>Hint 8 - check_exercise.py says tests/ or data/ are missing</summary>

They exist but are empty, and Git ignores empty folders. Add an empty `.gitkeep` file in each, then `git add` it.
</details>

---

## 7. Stretch goals (optional, after Part 7)

1. **`__all__` in every module** (not only in `utils/__init__.py`) and test `from qe_foundations.utils.strings import *`.
2. **Run as a module:** add `qe_foundations/__main__.py` so `python -m qe_foundations` prints the version, the Python executable and `sys.platform` (use `sys`, `platform`, and your `__version__`).
3. **`env_info.py` in the repo root** that reports whether it runs inside a venv (`sys.prefix != sys.base_prefix`) and which `requests` version is installed.
4. **Lock file:** `python -m pip freeze | Set-Content -Encoding ascii requirements-lock.txt` (bash: `python -m pip freeze > requirements-lock.txt`). Explain in `docs/` why the hand-written `requirements.txt` and the frozen lock file serve different purposes.
5. **Feature branch + `git fetch`:** create branch `feature/docs-polish`, push it, then use `git fetch` and `git log origin/main..HEAD` to inspect it before merging.
6. **Environment-driven data:** let `make_users` default its seed from an environment variable `QE_SEED` using `os.environ` (keep the function silent and repeatable when the seed is given).

## 8. Definition of Done (checklist)

- [ ] `python check_exercise.py --submit` ends with "All required checks passed"
- [ ] Repo `qe-foundations` is on the remote; `git status` clean; `git log --oneline` shows at least 3 meaningful commits
- [ ] `.venv/` and `__pycache__/` are ignored and not tracked
- [ ] `qe_foundations/` and `qe_foundations/utils/` have `__init__.py`; four modules exist; public API re-exported
- [ ] Importing `qe_foundations.utils` prints nothing
- [ ] `legacy_helpers.py` removed from the repo
- [ ] `mask_email` and `days_between` implemented and listed in `__all__`
- [ ] `requirements.txt` (requests with a version range) and `requirements-dev.txt` (`-r requirements.txt` + pytest) are plain UTF-8
- [ ] `tests/`, `data/`, `docs/` exist with placeholder / content files
- [ ] README has the **Project 1 milestone** section and setup steps for PowerShell and bash
- [ ] A fresh clone + the README steps ends with `7/7 checks passed`

## 9. Submission

1. Everything committed on branch `main` and pushed: `git push` (first time: `git push -u origin main`).
2. Run `git status` (must say "nothing to commit, working tree clean") and `git log --oneline -n 5`.
3. Submit the repository URL to your trainer by the channel they specify, with a screenshot or paste of the final `python check_exercise.py --submit` output.
4. Do **not** delete or rename the repo: you continue in it tomorrow (Project 1, Tuesday).

## 10. Grading rubric (100 points)

| Area | Points | Full marks when |
|------|-------:|-----------------|
| Repository & Git hygiene | 20 | Repo pushed; >= 3 meaningful commits; clean tree; `.gitignore` correct; no `.venv`/`__pycache__` tracked |
| Package structure & imports | 25 | Package + sub-package with `__init__.py`; 4 modules with the right contents; silent import; absolute imports; `__all__`; legacy file removed |
| Functionality | 20 | All 12 public functions behave per spec incl. `mask_email` and `days_between`; `smoke_utils.py` 7/7 |
| Dependencies & venv | 15 | Correct two requirements files (UTF-8, version ranges, dev separated); fresh clone works from README |
| Documentation | 10 | README with Project 1 milestone, PowerShell + bash setup, usage; `docs/structure.md` |
| Code quality | 10 | Docstrings, clear names, no dead code or leftover prints |
| Stretch (bonus) | up to +10 | Per completed stretch goal, trainer's judgement |

The full rubric with scoring bands is also in `solution/RUBRIC.md` (instructor-only).
