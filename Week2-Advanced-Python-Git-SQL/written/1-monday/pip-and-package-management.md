# pip and Package Management

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what pip is, what PyPI is, and how installing a third-party package works.
- Use `python -m pip` to install, upgrade, inspect, list and uninstall packages.
- Read and write version specifiers (`==`, `>=`, `~=`, `<`, and combinations) and explain why version pinning matters for repeatable test runs.
- Create and use a `requirements.txt` file with `pip freeze` and `pip install -r`.
- Understand direct vs transitive dependencies and why dependency conflicts happen.
- Install from other sources (a local folder, a Git URL, a requirements file) and install in editable mode.
- Diagnose common pip errors (`pip: command not found`, "externally-managed-environment", permission errors, version conflicts).
- Follow safe practices when installing third-party code.

---

## Why This Matters

Python's real power for QE comes from its ecosystem: `requests` for API testing, `pytest` for test running, `selenium` or `playwright` for browser automation, `faker` for test data, and database drivers for validating data. Almost every automation framework you will ever work on begins with a list of dependencies installed through **pip**.

This week's epic is about hardening your Python skills and starting the QE Foundations capstone, and a project that cannot be installed identically on a teammate's laptop and on the CI server is not a project, it is a "works on my machine" story. Package management is what makes test suites **reproducible**: "run these tests" must mean the same thing on every machine, today and six months from now. Knowing how to pin versions, record dependencies and install them cleanly is a day-one skill for anyone joining a QE team.

An analogy: pip is like a **supermarket delivery service for code**. You write a shopping list (`requirements.txt`), pip fetches each item (and every ingredient *those* items need) from the warehouse (PyPI), and puts it on your kitchen shelf (your environment's `site-packages`). The shopping list is what lets a colleague stock an identical kitchen.

---

## The Concept

### 1. Key Vocabulary

| Term | Meaning |
|------|---------|
| **Package / distribution** | A bundle of Python code that can be installed (for example `requests`) |
| **PyPI** (Python Package Index) | The public online repository of Python packages at pypi.org; pip downloads from here by default |
| **pip** | The standard tool that downloads and installs packages ("pip installs packages") |
| **site-packages** | The folder inside a Python installation or virtual environment where installed packages live |
| **Wheel (`.whl`)** | A pre-built package file; the fast, common format pip prefers |
| **Source distribution (sdist)** | A package as source code that must be built on your machine |
| **Dependency** | A package your code needs in order to work |
| **Transitive dependency** | A dependency *of a dependency* (you did not ask for it directly) |
| **Version** | A label like `2.31.0`, typically `MAJOR.MINOR.PATCH` |
| **Requirement specifier** | A rule describing acceptable versions, such as `requests>=2.31,<3` |

You have already used the **standard library** (modules shipped with Python such as `os`, `json`). Anything *not* in the standard library must be installed; that is where pip comes in. (The next-but-one lesson tours the useful built-in modules.)

### 2. Check That pip Is Available

pip ships with modern Python installers. Check:

```bash
python -m pip --version
```

Example output:

```
pip 24.0 from /path/to/site-packages/pip (python 3.12)
```

(Your numbers will differ.) On macOS/Linux you may need `python3 -m pip --version`; on Windows, `py -m pip --version` also works.

#### Why `python -m pip` instead of just `pip`?

Both work in many setups, but `python -m pip` guarantees you are using the pip that belongs to **the exact Python interpreter** you typed. Many machines have several Pythons installed; a bare `pip` might be attached to a different one than `python`. The result is the classic confusing bug: "I installed it, but `import` says it is not installed". Using `python -m pip ...` removes that doubt, so we use it throughout this course.

You can see where a package would land:

```bash
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Both lines should point into the same Python (and, once you learn virtual environments in the next lesson, into your project's `.venv`).

> **Always install into a virtual environment.** Everything in this lesson assumes you will run it with an environment active. If you are reading this before the virtual environments lesson, read that one next, or at least create and activate one with `python -m venv .venv` first. Installing project packages into the system Python is the number one source of beginner trouble.

### 3. Installing Packages

#### Install the latest version

```bash
python -m pip install requests
```

What happens:

1. pip contacts PyPI and finds the newest release of `requests` compatible with your Python.
2. It reads the package's metadata to learn *its* dependencies (`urllib3`, `idna`, `certifi`, `charset-normalizer`).
3. It resolves a set of versions that satisfies everyone.
4. It downloads wheels (or builds sdists) and unpacks them into `site-packages`.

You will see output ending with something like `Successfully installed certifi-... charset-normalizer-... idna-... requests-... urllib3-...`. You asked for one package; pip installed five. The other four are transitive dependencies.

Check that it works:

```python
import requests
print(requests.__version__)
```

#### Install a specific version

```bash
python -m pip install requests==2.31.0
```

`==` means "exactly this version". Use it when you need a precise, known-good release.

#### Install several at once

```bash
python -m pip install requests pytest faker
```

#### Upgrade an installed package

```bash
python -m pip install --upgrade requests
# short form:
python -m pip install -U requests
```

If `requests` is already at the newest version, pip says "Requirement already satisfied".

#### Upgrade pip itself

```bash
python -m pip install --upgrade pip
```

Inside a virtual environment this is safe and often useful, since new environments sometimes ship an older pip.

#### Uninstall

```bash
python -m pip uninstall requests
```

pip asks for confirmation (`y/n`). Add `-y` to skip it. Note: uninstalling a package does **not** uninstall its dependencies automatically. pip does not track "who asked for whom" well enough to be sure they are unneeded.

### 4. Version Specifiers (Controlling *Which* Versions)

Packages release new versions constantly. A new version can fix bugs, but it can also **break your tests**. Version specifiers let you control the risk.

| Specifier | Meaning | Example matches for `X` |
|-----------|---------|--------------------------|
| `==2.31.0` | Exactly this version | only `2.31.0` |
| `>=2.31` | This or newer | `2.31`, `2.32`, `3.0` |
| `<3` | Older than this | `2.99`, but not `3.0` |
| `>=2.31,<3` | A range (comma = AND) | `2.31` through `2.x` |
| `!=2.32.0` | Anything except this | skip a known-bad release |
| `~=2.31.0` | "Compatible release": `>=2.31.0, ==2.31.*` | `2.31.0`, `2.31.5`, not `2.32.0` |
| `~=2.31` | `>=2.31, ==2.*` | `2.31`, `2.40`, not `3.0` |

On the command line, quote specifiers that contain `<`, `>` or other special characters, otherwise your shell interprets `>` as "redirect output to a file":

```bash
python -m pip install "requests>=2.31,<3"
python -m pip install "pytest~=8.0"
```

**Semantic versioning (SemVer)** is the common convention: `MAJOR.MINOR.PATCH`.

- **PATCH** (2.31.**1**): bug fixes only; safe.
- **MINOR** (2.**32**.0): new features, supposed to be backward compatible.
- **MAJOR** (**3**.0.0): may break existing code.

Many (not all!) packages follow it. A common safe range is "same major version, at least the minor you tested with", such as `>=2.31,<3`.

#### Why pinning matters for QE

Imagine your nightly UI test suite passes on Friday. On Saturday the browser-automation library publishes a new release with a changed default timeout. On Monday your CI installs "the latest" and 40 tests fail, but *nobody changed the tests*. If the version had been pinned (`selenium==4.x.y`), Monday would have matched Friday. Your goal is to make failures meaningful: they should mean "the application changed", not "the tooling shifted underneath us".

### 5. Inspecting What Is Installed

#### List everything

```bash
python -m pip list
```

Sample output:

```
Package            Version
------------------ ---------
certifi            2026.7.22
charset-normalizer 3.5.2
idna               3.20
pip                26.2.1
requests           2.31.0
urllib3            2.8.0
```

(Exact versions will vary with the date you install.)

#### Show details of one package

```bash
python -m pip show requests
```

You see its version, summary, home page, license, the **install location**, `Requires:` (what it depends on) and `Required-by:` (what installed packages depend on it). `Requires` and `Required-by` are the quickest way to understand why a package is present.

#### See which are outdated

```bash
python -m pip list --outdated
```

Shows installed packages with newer versions available. It does not change anything.

#### Check for broken dependencies

```bash
python -m pip check
```

Prints `No broken requirements found.` when all installed packages' dependency rules are satisfied. Run it whenever you suspect a conflict.

#### Search for the available versions of a package

```bash
python -m pip index versions requests
```

Lists the versions available on the index. (This command is flagged "experimental" in pip's own docs, so its output format may change; the PyPI website is a reliable alternative.)

### 6. Requirements Files: Recording and Reproducing an Environment

A **requirements file** is a plain text file (conventionally `requirements.txt`) listing packages, one per line. It is the "shopping list" from our analogy and it is committed to Git alongside your code.

#### Writing one by hand (recommended for direct dependencies)

```text
# requirements.txt - direct dependencies of the QE Foundations project
requests>=2.31,<3
pytest~=8.0
faker==24.0.0
```

- Lines starting with `#` are comments.
- Blank lines are ignored.
- Each other line is a requirement specifier.

Install everything in the file:

```bash
python -m pip install -r requirements.txt
```

`-r` means "read requirements from this file".

#### Generating one with `pip freeze`

```bash
python -m pip freeze
```

prints every installed package pinned to its exact version:

```
certifi==2026.7.22
charset-normalizer==3.5.2
idna==3.20
requests==2.31.0
urllib3==2.8.0
```

Redirect it into a file:

```bash
python -m pip freeze > requirements.txt
```

(`>` writes the command's output into the file, replacing any previous content.)

> **Windows PowerShell note:** `>` in some older PowerShell versions writes the file in UTF-16, which pip may fail to read (`ERROR: ... UnicodeDecodeError`). If that happens, use `python -m pip freeze | Out-File -Encoding utf8 requirements.txt`, or use Command Prompt or Git Bash.

#### Two styles of requirements file

| Style | How made | Pros | Cons |
|-------|----------|------|------|
| **Loose (direct dependencies, ranges)** | Written by hand: `requests>=2.31,<3` | Easy to read; you see what you chose; allows bug-fix upgrades | Two installs on different days may give different transitive versions |
| **Pinned (frozen, exact versions)** | `pip freeze` | Reproducible down to every package | Long; includes transitive dependencies you did not choose; harder to upgrade deliberately |

Many teams keep **both**: `requirements.in` or `requirements.txt` with the loose direct dependencies, and a frozen `requirements.lock.txt` (or `constraints.txt`) generated from a known-good environment, which CI uses. For Project 1 a single hand-maintained `requirements.txt` with sensible pins is fine; just be consistent, and know the trade-off.

#### Useful requirements-file features

```text
-r base.txt                  # include another requirements file
requests==2.31.0             # exact pin
pytest>=8,<9                 # range
colorama; sys_platform == "win32"    # environment marker: only on Windows
```

Environment markers (the part after `;`) install a package only on certain platforms or Python versions. They are useful when a team uses a mix of Windows, macOS and Linux machines. A common split is `requirements.txt` for runtime packages, and `requirements-dev.txt` that begins with `-r requirements.txt` and adds test-only tools.

#### A critical caution about `pip freeze`

If you run `pip freeze` in an environment cluttered with unrelated packages (for example, your global Python), your `requirements.txt` will be full of things your project does not need. This is the main reason we **use one virtual environment per project**: the freeze output then reflects only that project. You also noticed above that an editable install of your own package shows up in `freeze` as a `-e` line; for a shared requirements file you may need to remove that line.

### 7. How pip Resolves Dependencies, and Why Conflicts Happen

Suppose your project needs libraries A and B:

- Package A requires `shared>=2,<3`.
- Package B requires `shared>=3`.

No single version of `shared` can satisfy both. This is a **dependency conflict**. Modern pip has a *resolver* that tries to find a combination that works, and if there is none it stops with an error such as:

```
ERROR: Cannot install A and B because these package versions have conflicting dependencies.
```

**How to handle it:**

1. Read the message: it names the conflicting packages and the constraints.
2. Try relaxing your own pins (maybe you pinned an old version that blocks the upgrade).
3. Check whether a newer or older version of A or B changes its requirement.
4. If two tools genuinely cannot coexist, put them in **separate virtual environments**. This is one more reason environments exist.
5. As a last resort, ask: do I really need both?

pip **does not** analyse conflicts between packages you installed in *different commands* until the next install; use `python -m pip check` to audit.

### 8. Other Places to Install From

| Source | Command | When used |
|--------|---------|-----------|
| PyPI (default) | `python -m pip install requests` | Normal case |
| Requirements file | `python -m pip install -r requirements.txt` | Reproducing an environment |
| Local project folder (editable) | `python -m pip install -e .` | Developing your own package (see packages lesson) |
| Local project folder (regular) | `python -m pip install ./qa-toolkit` | Install a snapshot of a local package |
| Wheel file | `python -m pip install qa_toolkit-0.1.0-py3-none-any.whl` | Offline or internal distribution |
| Git repository | `python -m pip install "git+https://github.com/user/repo.git@v1.0"` | Internal libraries or unreleased fixes; `@v1.0` selects a tag/branch |
| Private package index | `python -m pip install --index-url https://my.company/simple pkg` | Companies hosting internal packages |

Teams often share an internal QE library through a Git URL: tag a release (`v1.0`), and every project installs `git+https://...@v1.0`. You will practise Git collaboration at the end of today's lessons.

### 9. Extras and Optional Dependencies

Some packages offer optional feature sets called **extras**, written in square brackets:

```bash
python -m pip install "requests[socks]"
```

This installs `requests` plus the additional dependencies needed for SOCKS proxy support. You will mostly meet extras in documentation instructions such as `pip install "something[all]"`. Quote them, because square brackets are special in some shells (notably zsh).

### 10. Where Are Packages Stored? Caches and Wheels

- Installed packages live in `site-packages` of the active interpreter/environment. Find it with:

  ```python
  import site
  print(site.getsitepackages())
  ```

  (In a virtual environment this prints the environment's own `site-packages`; some very old virtualenv versions lacked `getsitepackages`, which is not a concern with the standard `venv` module.)

- pip keeps a **download cache** so reinstalling is fast. Show its location with `python -m pip cache dir`. Clear it with `python -m pip cache purge`.
- Prefer wheels. If a package must be compiled from source and you lack a compiler, installation may fail with long error output. Usually there is a wheel available for common platforms; upgrading pip (`python -m pip install -U pip`) often helps pip find it.

### 11. Troubleshooting Guide

| Message / Symptom | Meaning | Fix |
|-------------------|---------|-----|
| `pip: command not found` / `'pip' is not recognized` | pip's script is not on your PATH | Use `python -m pip ...`; make sure Python is installed and on PATH |
| `No module named pip` | pip not installed for this Python | `python -m ensurepip --upgrade` |
| `ModuleNotFoundError` after a successful install | Installed into a different Python/environment than the one running your code | Use `python -m pip`; activate the correct virtual environment; verify with `sys.executable` |
| `error: externally-managed-environment` | Your OS-managed Python (common on recent Debian/Ubuntu/macOS Homebrew) blocks system-wide pip installs | Create and activate a virtual environment, then install there. Do not use `--break-system-packages` as a habit |
| `PermissionError` / `Access is denied` | Trying to write to a protected system location | Use a virtual environment; avoid `sudo pip` |
| `ERROR: Could not find a version that satisfies the requirement ...` | Typo in the name, the version does not exist, or your Python version is unsupported | Check spelling and available versions (`pip index versions name`) |
| `ERROR: No matching distribution found` | Often network/proxy issues or unsupported platform | Check connectivity; corporate proxies may require `--proxy` or configuration |
| `ERROR: Cannot install X and Y because these package versions have conflicting dependencies` | Dependency conflict | See section 7 |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Corporate network intercepting HTTPS, or outdated certificates | Ask IT for the corporate CA bundle; never disable verification as a habit |
| Wrong version imported after an upgrade | Old Python session still running | Restart the interpreter |
| `UnicodeDecodeError` reading requirements.txt | File saved in UTF-16 | Re-save as UTF-8 |

### 12. Safe Practices for Installing Third-Party Code

Installing a package means **running someone else's code on your computer**, including install scripts. Treat it with the same care as any download:

1. **Check the name carefully.** Attackers publish look-alike names (`requets`, `reqeusts`), a trick called *typosquatting*.
2. Prefer well-known, actively maintained packages. Look at the PyPI page: release history, project links, maintainers, and download popularity.
3. Pin versions in project files so you do not silently receive a compromised or broken new release.
4. Do not run `sudo pip install` or install to system Python.
5. Do not install packages you do not need: every dependency is something you must keep updated.
6. Review upgrades deliberately (read changelogs) rather than upgrading everything blindly.

Companies often add automated dependency scanning to their CI pipelines, which is one reason a clean, accurate requirements file is valuable.

### 13. A Standard Workflow for a New QE Project

Putting it all together (we will practise this in today's demo and exercise):

```bash
# 1. Create a project folder and enter it
mkdir qe-foundations && cd qe-foundations

# 2. Create and activate a virtual environment (next lesson explains this fully)
python -m venv .venv
# macOS/Linux:  source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1

# 3. Upgrade pip inside the environment
python -m pip install --upgrade pip

# 4. Install what you need
python -m pip install requests pytest

# 5. Record it
python -m pip freeze > requirements.txt

# 6. Commit requirements.txt (but NOT .venv/) to Git
```

A teammate then clones the repository, creates their *own* `.venv`, and runs `python -m pip install -r requirements.txt` to get the same environment.

---

## Code Examples

### Example 1: Using an installed package in a script

After `python -m pip install requests` inside your environment, this script builds a request *without* contacting any network (so it works offline and is safe to run in class):

```python
import requests

request = requests.Request(
    "GET",
    "https://example.com/api/users",
    params={"page": 2, "limit": 10},
    headers={"Accept": "application/json"},
)
prepared = request.prepare()

print(prepared.method)    # GET
print(prepared.url)       # https://example.com/api/users?page=2&limit=10
print(prepared.headers["Accept"])   # application/json
print(requests.__version__)
```

**Explanation:**

- `requests.Request(...)` describes a request object (method, URL, query parameters, headers) without sending it.
- `.prepare()` turns it into the exact request that *would* be sent, including URL encoding of parameters.
- Printing shows the final URL. This is useful for QE: you can check how your code constructs requests before running them against a real server.

### Example 2: Checking installed package versions from Python itself

```python
from importlib import metadata

for name in ("requests", "pip"):
    try:
        print(name, metadata.version(name))
    except metadata.PackageNotFoundError:
        print(name, "is NOT installed")
```

`importlib.metadata` is in the standard library. `metadata.version(name)` reads the installed version, and `PackageNotFoundError` is raised if the package is missing, which we catch with `try/except` (covered fully tomorrow; for now read it as "try this, and if it fails this particular way, do that instead").

### Example 3: A "preflight" script that verifies your environment against requirements

QE teams often add a small check that fails fast with a helpful message if the environment is wrong. This script reads simple `name==version` lines from `requirements.txt` and compares them to what is installed:

```python
"""check_env.py - verify installed packages match pinned requirements."""

import sys
from importlib import metadata


def read_pins(path):
    """Return {package_name: version} for lines like 'name==1.2.3'."""
    pins = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "==" not in line:
                continue
            name, version = line.split("==", 1)
            pins[name.strip()] = version.strip()
    return pins


def main(path="requirements.txt"):
    problems = 0
    for name, wanted in read_pins(path).items():
        try:
            found = metadata.version(name)
        except metadata.PackageNotFoundError:
            print(f"MISSING  {name} (wanted {wanted})")
            problems += 1
            continue
        if found != wanted:
            print(f"MISMATCH {name}: installed {found}, wanted {wanted}")
            problems += 1
        else:
            print(f"OK       {name}=={found}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

**Line-by-line notes:**

- `with open(path, encoding="utf-8") as handle:` opens the file and guarantees it is closed afterwards (files are covered in depth tomorrow).
- `line.strip()` removes surrounding whitespace and newline characters.
- `if not line or line.startswith("#") or "==" not in line: continue` skips blank lines, comments and non-pinned lines.
- `line.split("==", 1)` splits at the first `==` only, giving name and version.
- `metadata.version(name)` returns the installed version string.
- `main` returns `1` when there were problems and `0` otherwise; `sys.exit(...)` passes that as the process **exit code**. By convention exit code 0 means success; a CI system treats non-zero as failure, which is exactly what we want from a preflight check.
- `sys.argv[1:]` is the list of command-line arguments after the script name, so `python check_env.py other.txt` checks a different file. (If no argument is passed, `main()` uses its default.)
- Caveat: package-name matching is exact here; names like `Pillow`/`pillow` are case-insensitive in practice for `metadata.version`, but your file's spelling should match.

Run: `python check_env.py requirements.txt`

Sample output:

```
OK       requests==2.31.0
MISMATCH urllib3: installed 2.8.0, wanted 1.26.18
```

### Example 4: A sample project `requirements.txt` and `requirements-dev.txt`

`requirements.txt`:

```text
# Runtime libraries for the QE Foundations toolkit
requests>=2.31,<3
```

`requirements-dev.txt`:

```text
-r requirements.txt
# Tools only needed while developing/testing
pytest>=8,<9
```

Install everything for development: `python -m pip install -r requirements-dev.txt`.

---

## Practice Questions and Mini-Exercises

**Q1.** What is the difference between pip and PyPI?

**Q2.** Why do we prefer `python -m pip install x` over `pip install x`?

**Q3.** Interpret each specifier in plain English: (a) `pytest==8.1.1` (b) `requests>=2.31,<3` (c) `faker~=24.0.0` (d) `urllib3!=2.0.0`.

**Q4.** You run `python -m pip install requests` and pip installs five packages. Why? Which one did you ask for directly?

**Q5.** Your teammate cloned your repo and ran `python -m pip install -r requirements.txt`, but they get `ModuleNotFoundError: No module named 'pytest'` when running tests. Give three possible causes.

**Q6 (hands-on).** In a fresh virtual environment (use `python -m venv .venv` and activate it): (a) install `requests==2.31.0`; (b) run `pip show requests` and note the `Requires` line; (c) run `pip freeze > requirements.txt`; (d) uninstall `requests`; (e) restore everything from the file; (f) verify with `pip list`.

**Q7 (predict).** Why might the command `python -m pip install requests>=2.31` create a file named `=2.31` in your folder? How do you fix the command?

**Q8 (debug).** Output:

```
error: externally-managed-environment
```

What does it mean, and what is the right fix?

**Q9 (design).** Your suite uses `requests`. Write a loose requirement line you would be comfortable with, and explain why you would also keep a pinned (frozen) file for CI.

**Q10 (challenge).** Extend `check_env.py` so that it also reports packages in `requirements.txt` that use `>=` rather than `==` as "SKIPPED (not pinned)". Hint: look at the `read_pins` condition.

---

### Answers

**A1.** pip is the *tool* that installs packages. PyPI (Python Package Index) is the *online repository* of packages pip downloads from by default.

**A2.** `python -m pip` runs the pip belonging to exactly the Python interpreter you invoked, so packages are installed into the environment you intend. A bare `pip` might belong to a different Python.

**A3.** (a) exactly version 8.1.1. (b) version 2.31 or newer but below 3 (any 2.x from 2.31 on). (c) compatible release: `>=24.0.0` and `<24.1`, so 24.0.x only. (d) any version except 2.0.0.

**A4.** pip also installs the dependencies of `requests` (transitive dependencies: `urllib3`, `idna`, `certifi`, `charset-normalizer`). You asked directly only for `requests`.

**A5.** (1) They did not activate their virtual environment, or they activated a different one than the one they installed into. (2) `pytest` is not actually listed in `requirements.txt` (for example it was in `requirements-dev.txt` or was never added). (3) They installed with a different Python (use `python -m pip`), or the install failed partway and they missed an error message. Another possible cause: the file was saved in the wrong encoding.

**A6.** One sequence:

```bash
python -m pip install requests==2.31.0
python -m pip show requests
python -m pip freeze > requirements.txt
python -m pip uninstall -y requests
python -m pip install -r requirements.txt
python -m pip list
```

Note that uninstalling `requests` leaves its dependencies behind; the final `install -r` succeeds either way.

**A7.** The shell interprets `>` as output redirection, so the command becomes `pip install requests` with its output redirected into a file named `=2.31`. Quote the requirement: `python -m pip install "requests>=2.31"`.

**A8.** The operating system manages that Python installation and refuses system-wide package installs to avoid breaking OS tools. Create a virtual environment (`python -m venv .venv`), activate it, and install there.

**A9.** For example `requests>=2.31,<3`, which allows compatible bug-fix and feature upgrades but protects against a breaking major release. A frozen file (`pip freeze`) is kept for CI so every pipeline run uses identical versions of everything, including transitive dependencies, making failures traceable to your tests or the application and not to a changed library.

**A10.** Modify `read_pins` so that lines containing `>=` (or other specifiers) are recorded separately and reported:

```python
def read_pins(path):
    pins, skipped = {}, []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "==" in line:
                name, version = line.split("==", 1)
                pins[name.strip()] = version.strip()
            else:
                skipped.append(line)
    return pins, skipped
```

and in `main`, unpack `pins, skipped = read_pins(path)` and print `SKIPPED (not pinned)  <line>` for each item in `skipped`.

---

## Summary / Key Takeaways

- **pip** installs packages from **PyPI** into the active environment's `site-packages`. Use **`python -m pip`** so you always target the right interpreter.
- Core commands: `install`, `install -U`, `uninstall`, `list`, `show`, `freeze`, `check`, `list --outdated`.
- **Version specifiers** (`==`, `>=`, `<`, `~=`, `!=`, comma-combined) control what is acceptable; quote them in the shell. Pinning makes test runs reproducible.
- Record your environment in **`requirements.txt`** (hand-written loose ranges for direct dependencies; `pip freeze` for exact pins) and rebuild it anywhere with `pip install -r requirements.txt`.
- pip also installs transitive dependencies; conflicts are resolved by relaxing pins, or by separating environments.
- You can install from PyPI, local folders (`-e .`), wheels and Git URLs.
- Install into a **virtual environment** (next lesson), never into the system Python, and treat third-party code with caution (watch for typosquatting).

---

## Additional Resources

- pip documentation - User Guide: https://pip.pypa.io/en/stable/user_guide/
- pip documentation - Requirements File Format: https://pip.pypa.io/en/stable/reference/requirements-file-format/
- Python Packaging User Guide - Installing Packages: https://packaging.python.org/en/latest/tutorials/installing-packages/
