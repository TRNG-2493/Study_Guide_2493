# Virtual Environments

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a virtual environment is, the problem it solves, and how it works under the hood.
- Create a virtual environment with the standard `venv` module.
- Activate and deactivate an environment on Windows (PowerShell and Command Prompt), macOS and Linux, and confirm which environment is active.
- Install packages into an environment and recreate that environment on another machine using `requirements.txt`.
- Decide where to keep the environment folder, and keep it out of Git with `.gitignore`.
- Recognise the main alternatives (`virtualenv`, `conda`, `pipenv`, `poetry`, `uv`) at a high level, and when you might meet them.
- Troubleshoot common problems: activation scripts blocked, the wrong interpreter running, "externally managed" errors, broken environments after moving a folder.

---

## Why This Matters

Suppose you work on two projects at the same time:

- **Project A** is an older API test suite that only works with `requests` version 2.25 and an older plugin.
- **Project B** is a new framework that needs `requests` 2.31 or newer.

Your computer has one global Python with one `site-packages` folder. Only one version of `requests` can live there at a time. Installing what Project B needs breaks Project A, and the reverse. This is called **dependency hell**, and it shows up on every QE team that has more than one project, or more than one version of a tool.

A **virtual environment** solves it by giving **each project its own private set of installed packages**. Project A gets its own environment with `requests` 2.25; Project B gets its own environment with `requests` 2.31. They never interfere.

This ties directly to today's work and to this week's epic (hardening your Python and starting the QE Foundations capstone):

- Reproducibility: with `requirements.txt` (previous lesson) plus a fresh virtual environment, any teammate or CI server can rebuild the exact environment your tests run in.
- Cleanliness: your system Python stays untouched, so you cannot break your operating system's own Python tools.
- Safety: you can experiment with new libraries and delete the environment afterwards, leaving no trace.

An analogy: a virtual environment is a **separate workshop bench per project**. Each bench has its own labelled set of tools. You can reorganise one bench without any effect on another, and you can throw a bench away and rebuild it from a tools list (`requirements.txt`) in minutes.

---

## The Concept

### 1. What Exactly Is a Virtual Environment?

A virtual environment is a **folder** that contains:

1. A link to (or copy of) a Python interpreter, "borrowed" from the Python that created it.
2. Its own, initially nearly empty, `site-packages` directory where packages for that project are installed.
3. Activation scripts and a small configuration file (`pyvenv.cfg`) that records which base Python it came from.

It is "virtual" because it does not contain a full separate copy of Python. The standard library still comes from the base installation. It is an **isolated place for third-party packages**, plus a Python launcher that knows to look there.

Typical contents (macOS/Linux; Windows uses `Scripts` instead of `bin` and `Lib` instead of `lib`):

```
.venv/
├── bin/                  <- python, pip, activate scripts (Windows: Scripts\)
│   ├── python  -> link to the base interpreter
│   ├── pip
│   └── activate
├── include/
├── lib/
│   └── python3.12/
│       └── site-packages/    <- YOUR packages are installed here
└── pyvenv.cfg            <- records the base Python and settings
```

#### How does it work?

When you run `.venv/bin/python`, Python starts, notices a `pyvenv.cfg` file next to its location, and adjusts `sys.prefix` (the "where am I" path) to the environment folder. It then builds `sys.path` so that the environment's `site-packages` is searched, and, by default, the global site-packages is **not**. That is the isolation: `import requests` can only find what is installed in *this* environment.

You can prove it from Python:

```python
import sys

print("prefix      :", sys.prefix)        # the environment folder when inside a venv
print("base_prefix :", sys.base_prefix)   # the original Python installation
print("in a venv?  :", sys.prefix != sys.base_prefix)
```

Inside an active environment `in a venv?` prints `True`; outside, `False`. Handy for a script that refuses to run unless it is inside an environment.

### 2. Creating a Virtual Environment with `venv`

The standard library ships a module named `venv`, so no extra installation is needed (on some Debian/Ubuntu systems you may first need `sudo apt install python3-venv`).

#### Step 1: Open a terminal in your project folder

```bash
mkdir qe-foundations
cd qe-foundations
```

#### Step 2: Create the environment

```bash
python -m venv .venv
```

Breaking this down:

- `python -m venv`: run the `venv` module as a program (the `-m` mechanism you met in the packages lesson).
- `.venv`: the **folder name** to create. This is a convention: the leading dot hides it on Linux/macOS and many editors recognise `.venv` automatically. You will also see `venv` or `env`. Pick one convention per team.

On macOS/Linux you may need `python3 -m venv .venv`; on Windows, `py -m venv .venv`.

Creation takes a few seconds. Afterwards the folder `.venv` exists. Nothing is "active" yet.

> **Note:** The environment is tied to the Python version that created it. If you want Python 3.12 specifically, invoke that interpreter (for example `python3.12 -m venv .venv` or `py -3.12 -m venv .venv`).

### 3. Activating and Deactivating

**Activation** is a convenience: it changes your *current terminal session* so that typing `python` or `pip` uses the ones inside `.venv`. It works by putting the environment's `bin` (or `Scripts`) folder at the front of your `PATH` variable and changing your prompt.

| Platform / shell | Activate command (run from the project folder) |
|------------------|--------------------------------------------------|
| macOS / Linux (bash, zsh) | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt (cmd) | `.venv\Scripts\activate.bat` |
| Windows Git Bash | `source .venv/Scripts/activate` |
| fish shell | `source .venv/bin/activate.fish` |

After activation your prompt shows the environment name in parentheses:

```
(.venv) $
```

To leave it:

```bash
deactivate
```

(on every platform; `deactivate` is a function the activation script defines).

**Activation is per terminal window.** A new terminal starts without any environment, and you must activate it again. Closing the terminal ends the activation, but the environment folder remains on disk.

#### Confirm which environment is active

This is a habit worth building: before installing anything, **check**.

```bash
python -c "import sys; print(sys.executable)"
```

The printed path should include your project's `.venv`. Other checks:

```bash
# macOS/Linux
which python

# Windows PowerShell
Get-Command python

# Windows cmd
where python
```

And `python -m pip --version` shows pip's location, which should also be inside `.venv`.

#### You do not strictly need to activate

Because activation merely adjusts `PATH`, you can call the environment's interpreter directly:

```bash
.venv/bin/python -m pip install requests        # macOS/Linux
.venv\Scripts\python.exe -m pip install requests   # Windows
```

This is useful in scripts, scheduled jobs and CI pipelines where "activating" is awkward. Many tools (VS Code, PyCharm) also detect `.venv` and use its interpreter automatically; you can select it manually in the editor's "Select Python Interpreter" command.

### 4. Working Inside an Environment

With the environment active, everything from the pip lesson now happens *inside* it:

```bash
(.venv) python -m pip install --upgrade pip
(.venv) python -m pip install requests pytest
(.venv) python -m pip list
```

`pip list` in a fresh environment shows only `pip` (and perhaps `setuptools`), a tiny list. After installing, the new packages appear *only here*. Switch to another environment (or none) and they are gone. That is isolation working.

Run your code the usual way: `python main.py` uses the environment's interpreter, so `import requests` finds the copy you installed in `.venv`.

### 5. The Complete Reproducible Workflow

This is the pattern every professional Python team uses. Learn it until it is automatic.

**Person 1 (creating the project):**

```bash
mkdir qe-foundations && cd qe-foundations
git init
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install requests pytest
python -m pip freeze > requirements.txt
printf ".venv/\n__pycache__/\n" > .gitignore    # or create the file in an editor
git add requirements.txt .gitignore
git commit -m "Add dependencies and gitignore"
```

(`printf ... > .gitignore` works on macOS/Linux/Git Bash. On Windows PowerShell create the file in an editor, or use `Set-Content .gitignore ".venv/","__pycache__/"`.)

**Person 2 (joining the project):**

```bash
git clone <repository-url>
cd qe-foundations
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest                     # run the tests: same environment, same results
```

Notice what **is** shared (the *recipe*: `requirements.txt`, committed to Git) and what is **not** shared (the *environment folder itself*, which is machine-specific).

### 6. Why You Never Commit the Environment Folder

- It is **large** (can be hundreds of MB).
- It contains **absolute paths** and platform-specific binaries. A Windows `.venv` does not work on macOS; even moving the folder on the same machine can break it.
- It is **reproducible** from `requirements.txt`, so there is nothing valuable to store.
- It would produce enormous noise in Git history.

Add the folder name to `.gitignore`:

```
.venv/
venv/
env/
__pycache__/
*.pyc
```

Check that Git ignores it: `git status` should not list `.venv`. (If you accidentally staged it, `git rm -r --cached .venv` untracks it without deleting the files.)

### 7. Where Should the Environment Live?

| Approach | Description | Notes |
|----------|-------------|-------|
| **Inside the project folder** (`./.venv`) | One environment per repo, next to the code | Simple; editors auto-detect it; our recommended default for this course |
| A central folder (for example `~/.virtualenvs/projectname`) | Environments stored elsewhere | Keeps projects clean; need to remember where; used by some tools like `virtualenvwrapper`, `pipenv`, `poetry` |
| One shared environment for many projects | Convenience | Brings the original problem back; avoid |

**Rule of thumb: one project = one environment.** If you have two repos, make two environments.

### 8. Deleting and Recreating

Because environments are disposable, the fix for most weirdness is to rebuild:

```bash
deactivate                      # if it is active
rm -rf .venv                    # Windows PowerShell: Remove-Item -Recurse -Force .venv
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Deleting an environment never touches your source code, since they are separate folders. This "turn it off and on again" is a powerful troubleshooting technique when a dependency state is unclear.

### 9. Useful Options

```bash
python -m venv .venv --upgrade-deps     # upgrade pip (and setuptools where included) right after creation
python -m venv .venv --system-site-packages   # allow the environment to also see global packages (rarely wanted)
python -m venv .venv --clear            # empty an existing environment folder and recreate it
python -m venv --help                   # list all options
```

### 10. Environment Variables and Secrets (a Brief Safety Note)

Test projects often need credentials (API keys, test-account passwords). **Never hard-code secrets into code or commit them.** A common pattern is to read them from environment variables (we tour `os.environ` in the built-in modules lesson) or from a local file that is listed in `.gitignore` (for example `.env`). The virtual environment itself does not manage secrets; it only manages Python packages.

### 11. Alternatives and Related Tools (Awareness Level)

You do not need these this week; recognise the names so you are not surprised on a real team.

| Tool | What it is | When you meet it |
|------|-----------|------------------|
| `venv` | Standard library module; what we use | Everywhere; the baseline |
| `virtualenv` | Third-party predecessor of `venv`; faster, more options | Older projects, tooling |
| `conda` / `mamba` | Environment and package manager for Python and non-Python software | Data science teams |
| `pipenv`, `poetry`, `pdm` | Higher-level tools that combine environment creation, dependency resolution and lock files | Teams that want lock files and publishing support |
| `uv` | A newer, very fast tool that can create environments and install packages with pip-compatible commands | Increasingly common |
| `pyenv` | Manages multiple *Python versions* (not environments, though they pair well) | When projects need different Python versions |
| `tox` / `nox` | Run tests across many environments automatically | Libraries and CI |
| Docker containers | Isolate the whole operating-system environment, not just Python | CI and deployment |

They all solve the same core problem: **isolation and reproducibility**. If you understand `venv` + `pip` + `requirements.txt`, you can learn any of them quickly.

### 12. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| PowerShell: `...Activate.ps1 cannot be loaded because running scripts is disabled on this system` | PowerShell execution policy blocks scripts | Run once: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or use Command Prompt (`activate.bat`), or skip activation and call `.venv\Scripts\python.exe` directly. On managed company laptops follow IT's guidance |
| `The virtual environment was not created successfully because ensurepip is not available` (Debian/Ubuntu) | The `venv` package is missing | `sudo apt install python3-venv` |
| Prompt shows `(.venv)` but `python` runs the wrong one | PATH quirks, or an alias | Check `which python` / `sys.executable`; recreate; call `.venv/bin/python` directly |
| `ModuleNotFoundError` for something you installed | Environment not active when installing, or not active when running | Activate, then `python -m pip list` to confirm |
| Environment stopped working after moving/renaming the folder or upgrading Python | Environments hold absolute paths and point to the original interpreter | Delete and recreate from `requirements.txt` |
| `error: externally-managed-environment` | You ran pip without an active environment on an OS-managed Python | Create and activate a venv first |
| Editor still flags unresolved imports | Editor is using a different interpreter | Select the `.venv` interpreter in the editor |
| `git status` shows thousands of files | `.venv` was not ignored | Add to `.gitignore`; `git rm -r --cached .venv` |
| `deactivate` not found | No environment is active in this terminal | Nothing to do; it only exists after activation |
| Works locally, fails in CI | CI environment differs (Python version, missing dependency in requirements) | Pin the Python version; re-generate requirements from a clean environment |

### 13. Good Habits Checklist

1. One environment per project, created inside the project folder as `.venv`.
2. Always check the active interpreter before installing.
3. Install with `python -m pip`.
4. Keep `requirements.txt` current: update it whenever you add, remove or upgrade a dependency.
5. Commit `requirements.txt`; ignore `.venv`.
6. Document setup steps in the README (copy-pasteable commands for Windows and macOS/Linux).
7. Test your own instructions by deleting the environment and recreating it from scratch, at least once before sharing.

---

## Code Examples

### Example 1: A script that reports its environment

Save as `env_info.py`:

```python
"""env_info.py - print facts about the Python environment running this script."""

import sys


def in_virtual_environment():
    """True when running inside a venv created by the standard library."""
    return sys.prefix != sys.base_prefix


def main():
    print("Python version  :", sys.version.split()[0])
    print("Executable      :", sys.executable)
    print("Environment     :", sys.prefix)
    print("Base Python     :", sys.base_prefix)
    print("Inside a venv?  :", in_virtual_environment())
    print("First sys.path entries:")
    for entry in sys.path[:4]:
        print("   ", entry)


if __name__ == "__main__":
    main()
```

**Explanation:**

- `sys.version.split()[0]` takes the first word of the long version string (for example `3.12.3`).
- `sys.executable` is the path of the interpreter running this script, which is the most reliable "which Python am I?" answer.
- `sys.prefix` vs `sys.base_prefix` differ only inside a virtual environment, so comparing them is the standard test.
- `sys.path[:4]` slices the first four entries to keep output short.

Run it twice, once with the environment deactivated and once activated, and compare. Typical activated output (paths will differ):

```
Python version  : 3.12.3
Executable      : /home/you/qe-foundations/.venv/bin/python
Environment     : /home/you/qe-foundations/.venv
Base Python     : /usr
Inside a venv?  : True
First sys.path entries:
    /home/you/qe-foundations
    /usr/lib/python312.zip
    /usr/lib/python3.12
    /usr/lib/python3.12/lib-dynload
```

### Example 2: A guard that stops a test run outside a virtual environment

Some teams add this at the top of a "run everything" script so that nobody accidentally runs tests with random global packages:

```python
import sys

if sys.prefix == sys.base_prefix:
    sys.exit("Please activate the project's virtual environment first (see README).")

print("Environment OK; starting tests...")
```

`sys.exit("message")` prints the message to standard error and exits with a non-zero status code.

### Example 3: Proving isolation (hands-on lab)

1. Create two environments:

   ```bash
   python -m venv env_a
   python -m venv env_b
   ```

2. Install different versions in each (on macOS/Linux use `env_a/bin/python`; on Windows `env_a\Scripts\python.exe`):

   ```bash
   env_a/bin/python -m pip install requests==2.31.0
   env_b/bin/python -m pip install requests==2.32.3
   ```

3. Ask each for its version:

   ```bash
   env_a/bin/python -c "import requests; print(requests.__version__)"   # 2.31.0
   env_b/bin/python -c "import requests; print(requests.__version__)"   # 2.32.3
   ```

Two projects, two versions of the same library, no conflict. (Delete the lab with `rm -rf env_a env_b` afterwards.)

### Example 4: Real-world QA scenario - onboarding a new teammate in ten minutes

README excerpt you might write for your Project 1 repository:

```markdown
## Setup

1. Clone the repository and open a terminal in its folder.
2. Create an environment:  `python -m venv .venv`
3. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Verify: `python env_info.py` should print `Inside a venv?  : True`.
```

A README that works first time, for every new person, is a mark of a professional QE project.

---

## Practice Questions and Mini-Exercises

**Q1.** In your own words, what problem do virtual environments solve? Give a QE example.

**Q2.** Is a virtual environment a full copy of Python? What does it contain and what does it borrow?

**Q3.** Write the exact commands to (a) create an environment called `.venv`, (b) activate it on your operating system, (c) confirm that it is active, (d) deactivate it.

**Q4.** Your teammate commits their `.venv` folder to Git. List three problems this causes and the fix.

**Q5.** After activating the environment, you run `pip install pytest`, but later `python -m pytest` says "No module named pytest". Give two likely explanations and how you would verify each.

**Q6.** Does a virtual environment have to be *activated* to be used? Show how to run a script using the environment without activating.

**Q7 (hands-on).** Create a folder `env_lab`. Make a venv inside it, activate it, install `requests`, run `env_info.py` (above), and save the package list to `requirements.txt`. Then delete the venv, recreate it, and restore everything from `requirements.txt`. Verify with `pip list`.

**Q8 (debug).** You moved your project folder to a new location, and now `.venv/bin/pip` fails with "bad interpreter: No such file or directory". Why? What do you do?

**Q9 (design).** You have three repositories: an API test suite, a UI test suite, and a shared QA library. How many environments do you create, and why?

**Q10 (challenge).** Write a Python function `require_venv()` that raises a `RuntimeError` with a helpful message if the code is not running inside a virtual environment, and a short snippet that calls it.

---

### Answers

**A1.** They give each project an isolated set of installed packages, so projects with conflicting version needs can coexist and an environment can be recreated reliably. QE example: the old API suite needs an older `requests`; the new framework needs a newer one; separate environments let both run on the same laptop.

**A2.** No. It contains its own `site-packages`, a link to the base interpreter, scripts and a `pyvenv.cfg`. It borrows the interpreter and standard library from the Python that created it.

**A3.** (a) `python -m venv .venv` (b) macOS/Linux: `source .venv/bin/activate`; PowerShell: `.venv\Scripts\Activate.ps1`; cmd: `.venv\Scripts\activate.bat` (c) the prompt shows `(.venv)`, and `python -c "import sys; print(sys.executable)"` prints a path inside `.venv` (d) `deactivate`.

**A4.** It is huge; it contains machine-specific absolute paths and binaries that break on other computers/OSs; it clutters history and causes conflicts and slow clones. Fix: add `.venv/` to `.gitignore`, run `git rm -r --cached .venv`, commit; share `requirements.txt` instead.

**A5.** (1) Pytest was installed into a different environment than the one now running (verify with `python -m pip list` and `sys.executable`). (2) The shell that ran `pip install` and the one that ran `python -m pytest` differed, or the environment was deactivated in between. Another possibility is that a bare `pip` belonged to a different Python (verify with `pip --version`; this is why we use `python -m pip`).

**A6.** No. Activation is only a convenience. Run `.venv/bin/python script.py` (macOS/Linux) or `.venv\Scripts\python.exe script.py` (Windows).

**A7.** Sequence (macOS/Linux):

```bash
mkdir env_lab && cd env_lab
python -m venv .venv
source .venv/bin/activate
python -m pip install requests
python env_info.py
python -m pip freeze > requirements.txt
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip list
```

**A8.** Environment scripts and `pyvenv.cfg` record absolute paths, so moving the folder breaks them. Delete the `.venv` folder and recreate it at the new location, then `pip install -r requirements.txt`.

**A9.** Three environments, one per repository, each with its own requirements file; the two test suites would install the shared library into their environments (for example with `pip install -e ../qa-library` during development). This keeps dependencies isolated, but code shared.

**A10.**

```python
import sys


def require_venv():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError(
            "Not running inside a virtual environment. "
            "Create one with 'python -m venv .venv' and activate it."
        )


require_venv()
print("Running safely inside a virtual environment.")
```

(We will look at `raise` and exceptions properly tomorrow.)

---

## Summary / Key Takeaways

- A **virtual environment** is an isolated folder with its own `site-packages` and a Python launcher that uses it; it solves version conflicts between projects and enables reproducible setups.
- Create with `python -m venv .venv`; activate with `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1` (PowerShell) / `activate.bat` (cmd); leave with `deactivate`.
- Always verify the active interpreter with `sys.executable` before installing; use `python -m pip` inside the environment.
- Share the **recipe** (`requirements.txt`), not the environment: add `.venv/` to `.gitignore`.
- Environments are disposable: if something is wrong, delete and recreate.
- One project, one environment. Other tools (conda, poetry, uv, pipenv) are variations on the same idea.
- Next lesson: a tour of **built-in Python modules** (`os`, `sys`, `datetime`, `random`) you can use without installing anything.

---

## Additional Resources

- Python Tutorial - Virtual Environments and Packages: https://docs.python.org/3/tutorial/venv.html
- `venv` module reference: https://docs.python.org/3/library/venv.html
- Python Packaging User Guide - Installing packages using pip and virtual environments: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
