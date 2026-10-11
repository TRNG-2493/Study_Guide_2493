# Interview Questions: Week 2 — Monday: Python Modules & Environment Management

**Scope:** creating and importing modules, packages, pip and package management, virtual environments, built-in modules (`os`, `sys`, `datetime`, `random`) and the collaborative Git workflow (fetch, pull, push).
**Total:** 20 questions (14 Beginner, 5 Intermediate, 1 Advanced).

---

## Beginner (Foundational)

### Q1: What is a Python module, and why do professional teams split code into modules?
**Keywords:** `.py` file, organisation, reuse, namespace, testability
<details>
<summary>Click to Reveal Answer</summary>

A module is a single Python file (ending in `.py`) containing definitions and statements such as functions, classes and variables. The module name is the file name without `.py`, so `validators.py` is the module `validators`. Splitting code into modules gives organisation, reuse (write once, import everywhere), namespace separation (two modules can both define `load()` without clashing), easier collaboration and easier unit testing.

```python
import validators
validators.is_valid_email("a@b.com")   # the dot reaches inside the module namespace
```
</details>

*Source:* `creating-and-importing-modules.md`

---

### Q2: Explain the difference between `import validators` and `from validators import is_valid_email`. Why is `from validators import *` discouraged?
**Keywords:** namespace, prefix, name clash, star import, readability
<details>
<summary>Click to Reveal Answer</summary>

`import validators` brings only the module object into your namespace, so you call `validators.is_valid_email(x)` and it is always clear where a name came from. `from validators import is_valid_email` brings just that name in directly, giving shorter calls, but the origin is less obvious and a same-named import from another module silently replaces it. `from validators import *` is discouraged because you cannot tell where names come from, it can overwrite your own variables and linters cannot warn about undefined names. `import module` is the recommended default.
</details>

*Source:* `creating-and-importing-modules.md`

---

### Q3: What does the `if __name__ == "__main__":` guard do, and why is it useful?
**Keywords:** `__name__`, `"__main__"`, import vs run, side effects
<details>
<summary>Click to Reveal Answer</summary>

Every module has a built-in `__name__` variable. When the file is run directly (`python file.py`) it is set to `"__main__"`; when the file is imported it is set to the module's own name. The guard makes the block run only when the file is executed directly, so the same file works as both a reusable library (no side effects on import) and a runnable script. This also stops test frameworks from triggering your whole workflow when they import your code.

```python
def main():
    print("Doing the real work")

if __name__ == "__main__":
    main()
```
</details>

*Source:* `creating-and-importing-modules.md`

---

### Q4: What is a Python package, and what role does `__init__.py` play?
**Keywords:** directory, modules, `__init__.py`, dotted path, runs on import
<details>
<summary>Click to Reveal Answer</summary>

A package is a directory of modules (and optionally subpackages) that you can import as a unit using dotted names such as `qa_toolkit.validators`. The `__init__.py` file marks the folder as a regular package and is executed when the package is imported. You can leave it empty, use it for documentation and `__version__`, or re-export names (with `__all__`) to give users a clean public API. Keep it light, with no slow or side-effecting code.
</details>

*Source:* `python-packages.md`

---

### Q5: Explain the difference between an absolute import and a relative import inside a package.
**Keywords:** full path, dots, current package, parent package, only inside a package
<details>
<summary>Click to Reveal Answer</summary>

An absolute import spells out the full path from the top-level package, for example `from qa_toolkit.validators import is_non_empty`. A relative import uses dots relative to the current file: `.` is the current package, `..` is the parent package, for example `from .validators import is_non_empty`. Absolute imports are the PEP 8 default because they are explicit. Relative imports work only when the file is imported as part of a package; running the file directly gives `ImportError: attempted relative import with no known parent package`, and the fix is `python -m qa_toolkit.formatters`.
</details>

*Source:* `python-packages.md`

---

### Q6: What is the difference between pip and PyPI?
**Keywords:** tool, repository, install, download
<details>
<summary>Click to Reveal Answer</summary>

pip is the standard tool that downloads and installs Python packages. PyPI (the Python Package Index at pypi.org) is the public online repository of packages that pip downloads from by default. Packages are installed into the `site-packages` folder of the active Python or virtual environment.

```bash
python -m pip install requests
```
</details>

*Source:* `pip-and-package-management.md`

---

### Q7: Why does this course use `python -m pip install x` instead of just `pip install x`?
**Keywords:** same interpreter, multiple Pythons, correct environment
<details>
<summary>Click to Reveal Answer</summary>

`python -m pip` runs the pip that belongs to the exact Python interpreter you typed, so packages land in the environment you intend. Many machines have several Pythons, and a bare `pip` might belong to a different one. That mismatch causes the classic bug "I installed it, but `import` says it is not installed". Using `python -m pip` removes that doubt.
</details>

*Source:* `pip-and-package-management.md`

---

### Q8: What is a `requirements.txt` file, and how do `pip freeze` and `pip install -r` relate to it?
**Keywords:** list of dependencies, `pip freeze`, `-r`, reproducible, version pin
<details>
<summary>Click to Reveal Answer</summary>

A `requirements.txt` is a plain text file listing the packages (and optionally version specifiers) a project needs, one per line, and it is committed to Git. `python -m pip freeze` prints every installed package pinned to its exact version, and you can redirect it into the file with `>`. `python -m pip install -r requirements.txt` reads the file and installs everything in it, so a teammate or CI server can rebuild the same environment.

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```
On older Windows PowerShell, `>` may write UTF-16 which pip cannot read; use `python -m pip freeze | Out-File -Encoding utf8 requirements.txt`.
</details>

*Source:* `pip-and-package-management.md`

---

### Q9: What is a virtual environment, and what problem does it solve?
**Keywords:** isolation, `site-packages`, per project, version conflicts, reproducibility
<details>
<summary>Click to Reveal Answer</summary>

A virtual environment is a folder with its own private `site-packages`, a Python launcher that uses it, and a `pyvenv.cfg` file recording the base Python. It gives each project its own isolated set of third-party packages, solving "dependency hell" where one project needs `requests` 2.25 and another needs 2.31 but the global Python can hold only one. It borrows the interpreter and standard library from the base Python rather than being a full copy. Combined with `requirements.txt`, it makes setups reproducible.
</details>

*Source:* `virtual-environments.md`

---

### Q10: Why should you never commit the `.venv` folder to Git, and what should you commit instead?
**Keywords:** `.gitignore`, large, absolute paths, `requirements.txt`, recipe
<details>
<summary>Click to Reveal Answer</summary>

The environment folder is large, contains absolute paths and platform-specific binaries (a Windows `.venv` does not work on macOS), and can be rebuilt from `requirements.txt`, so committing it only adds noise to history. You share the recipe (`requirements.txt`), not the environment itself, and list `.venv/` in `.gitignore`. If it was staged by mistake, `git rm -r --cached .venv` untracks it without deleting the files.

```bash
git rm -r --cached .venv
```
</details>

*Source:* `virtual-environments.md`

---

### Q11: What is the Python standard library, and how does it differ from a third-party package such as `requests`?
**Keywords:** batteries included, ships with Python, no pip install, PyPI
<details>
<summary>Click to Reveal Answer</summary>

The standard library is the large collection of modules installed with Python itself ("batteries included"), such as `os`, `sys`, `datetime` and `random`. You can import them with no `pip install`, no version to pin and no extra dependency to maintain. A third-party package such as `requests` is not part of Python; you must install it from PyPI with pip into your environment. A quick test: if `import something` works on a fresh Python with no pip installs, it is standard library.
</details>

*Source:* `built-in-python-modules.md`

---

### Q12: What does `random.seed()` do, and why does it matter for test data?
**Keywords:** pseudo-random, same seed, repeatable, reproduce failures
<details>
<summary>Click to Reveal Answer</summary>

`random` produces pseudo-random numbers from a deterministic algorithm, so starting from the same seed gives the same sequence every time. For QA this means a failing randomised test can be reproduced exactly: log the seed at the start of the run and allow passing it in to replay a failure. A private generator, `random.Random(seed)`, keeps one part of your code from disturbing another's sequence. Note `random` is not secure; use `secrets` for tokens or passwords.

```python
import random
random.seed(42)
a = random.randint(1, 100)
random.seed(42)
b = random.randint(1, 100)
print(a == b)   # True
```
</details>

*Source:* `built-in-python-modules.md`

---

### Q13: Explain the difference between `git fetch` and `git pull`.
**Keywords:** download, integrate, remote-tracking branch, working files, merge/rebase
<details>
<summary>Click to Reveal Answer</summary>

`git fetch` downloads new commits from the remote and moves the remote-tracking branches (such as `origin/main`), but does nothing to your local branches or working files, which makes it safe at any time. `git pull` is fetch plus integrate: it fetches and then merges (or rebases, with `--rebase`) `origin/<branch>` into your current branch, so it changes your files and can produce conflicts. After a fetch you can inspect what arrived before deciding how to integrate.

```bash
git fetch
git log --oneline HEAD..origin/main   # what the remote has that I lack
```
</details>

*Source:* `collaborative-git-workflow-pull-fetch-and-push.md`

---

### Q14: What is the difference between `main` and `origin/main`?
**Keywords:** local branch, remote-tracking branch, last contact, read-only, updates on fetch
<details>
<summary>Click to Reveal Answer</summary>

`main` is your own local branch, which you move by committing. `origin/main` is a remote-tracking branch: a read-only bookmark recording where the remote's `main` was the last time you fetched, pulled or pushed. You cannot commit onto it directly, and it does not update in the background, so you must `git fetch` to learn what teammates have done. `git branch -vv` and `git status -sb` show how your branch is ahead or behind it.
</details>

*Source:* `collaborative-git-workflow-pull-fetch-and-push.md`

---

## Intermediate (Application)

### Q15: A teammate added a file called `random.py` to the project folder, and now `random.randint(1, 5)` fails with `AttributeError: module 'random' has no attribute 'randint'`. What is happening and how do you fix it?
**Keywords:** shadowing, `sys.path`, script folder first, rename, `__pycache__`
**Hint:** Think about where Python looks first when it resolves `import random`.
<details>
<summary>Click to Reveal Answer</summary>

This is the shadowing trap. The folder containing the script you ran is the first entry on `sys.path`, so `import random` finds the local `random.py` before the standard library one, and that file has no `randint`. Fix it by renaming the file to something that does not clash (for example `random_helpers.py`) and deleting the stale `__pycache__` folder. As a habit, never name your own files after standard library or installed modules (`json.py`, `csv.py`, `logging.py`, `email.py` and so on).

```bash
# bash
rm -rf __pycache__
```
```powershell
# PowerShell
Remove-Item -Recurse -Force __pycache__
```
</details>

*Source:* `creating-and-importing-modules.md`

---

### Q16: Your nightly UI suite passed on Friday, but on Monday 40 tests fail even though nobody changed the tests. How could package management explain this, and what would you do to prevent it?
**Keywords:** version pinning, latest release, `requirements.txt`, `pip freeze`, reproducible, CI
**Hint:** What did CI install on Monday?
<details>
<summary>Click to Reveal Answer</summary>

If requirements were unpinned, CI installed "the latest" version of a library on Monday, and a new release (for example with a changed default) shifted behaviour underneath the tests. To prevent it, pin versions so that Monday matches Friday: use a loose range such as `requests>=2.31,<3` for your direct dependencies and keep a frozen file generated by `pip freeze` from a known-good environment for CI, so transitive dependencies are identical too. Then a failure means "the application changed", not "the tooling shifted". Review upgrades deliberately by reading changelogs.

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```
</details>

*Source:* `pip-and-package-management.md`

---

### Q17: A new teammate clones your repo, runs `python -m pip install -r requirements.txt`, then gets `ModuleNotFoundError: No module named 'pytest'`. How do you diagnose it?
**Keywords:** active environment, `sys.executable`, `pip list`, requirements, activate
**Hint:** Which Python ran the install, and which Python is running the tests?
<details>
<summary>Click to Reveal Answer</summary>

The usual cause is that the package was installed into a different Python than the one running the tests. Check that the project's virtual environment is active (prompt shows `(.venv)`) and confirm the interpreter with `sys.executable`, then run `python -m pip list` to see whether `pytest` is there. Other causes: they activated a different environment, `pytest` is not actually listed in `requirements.txt` (for example it lives only in `requirements-dev.txt`), or the install failed partway. Fix by activating the right environment and reinstalling with `python -m pip`.

```bash
# bash (macOS/Linux)
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
python -m pip list
```
```powershell
# PowerShell
.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip list
```
</details>

*Source:* `virtual-environments.md` (also `pip-and-package-management.md`)

---

### Q18: Your test script must run against `qa` on your laptop but `staging` in CI, and the CI step must fail when `BASE_URL` is missing. How would you build this with built-in modules?
**Keywords:** `os.environ.get`, default value, `sys.exit`, exit code, `stderr`
**Hint:** Combine `os` for configuration and `sys` for the exit code.
<details>
<summary>Click to Reveal Answer</summary>

Read configuration from environment variables with `os.environ.get(name, default)`, which returns the default (or `None`) instead of raising `KeyError`, so the same code runs everywhere without edits. If a required variable is missing, print the message to `sys.stderr` and return a non-zero exit code via `sys.exit(main())`; CI treats non-zero as failure and zero as success. Environment variable values are always strings, so convert numbers yourself.

```python
import os, sys

def main():
    if not os.environ.get("BASE_URL"):
        print("Missing BASE_URL", file=sys.stderr)
        return 1
    env_name = os.environ.get("TEST_ENV", "qa")
    print(f"Running against {env_name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Set the variable for one run:

```bash
# bash
TEST_ENV=staging BASE_URL=https://qa.example.com python run_tests.py
```
```powershell
# PowerShell
$env:TEST_ENV = "staging"; $env:BASE_URL = "https://qa.example.com"; python run_tests.py
```
</details>

*Source:* `built-in-python-modules.md`

---

### Q19: You commit locally and run `git push`, but get `! [rejected] main -> main (fetch first)`. What does it mean, and how do you resolve it safely?
**Keywords:** fast-forward, remote has commits, `git fetch`, `git pull --rebase`, not force
**Hint:** Consider what a teammate has pushed since you last synced.
<details>
<summary>Click to Reveal Answer</summary>

It means the remote branch contains commits you do not have, and Git only allows a push that is a fast-forward of the remote; otherwise the push would erase your teammate's work. Fetch first, review what is missing, integrate with `git pull --rebase` (or a merge, following your team's convention), run your tests, then push. Do not use `git push --force`, since it would overwrite the remote branch and delete your teammate's commits. If conflicts appear, you can back out with `git rebase --abort` (or `git merge --abort`).

```bash
git fetch
git log --oneline HEAD..origin/main
git pull --rebase
git push
```
</details>

*Source:* `collaborative-git-workflow-pull-fetch-and-push.md`

---

## Advanced (Deep Dive)

### Q20: Module `a.py` has `from b import g` at the top, and `b.py` has `from a import f` at the top. What happens under the hood when you `import a`, and how would you fix the design?
**Keywords:** circular import, partially initialised module, executes once, `sys.modules`, third module
**Hint:** Importing runs the module's top-level code, and a module in the middle of running has not defined its names yet.
<details>
<summary>Click to Reveal Answer</summary>

Importing executes a module's top-level code, and the module object is cached in `sys.modules`. When `a` starts, it is paused at its first line to import `b`; `b` then tries to take `f` from `a`, but `a` is only partially initialised and `f` has not been defined yet, so Python raises an `ImportError` ("cannot import name ... most likely due to a circular import"). The best fix is redesign: move the shared code into a third module `c.py` that both import, so dependencies flow in one direction. Short-term workarounds are a local import inside the function that needs it, or using `import module` style so attribute lookups happen at call time.

```python
# c.py  -> holds f and g
# a.py  -> from c import g
# b.py  -> from c import f
```
</details>

*Source:* `creating-and-importing-modules.md`

---

## How to use this bank

This bank is for self-quizzing, so do not read the answers first.

1. Read a question and cover the answer (keep the `<details>` block closed).
2. Say your answer aloud as if you were in an interview, in 30 to 60 seconds. Use the hint only if you are stuck.
3. Open the answer and check that every **keyword** appeared in what you said. If you missed one, repeat the question until you can include it naturally.
4. Work through Beginner first until you can answer without notes, then attempt Intermediate (talk through the scenario step by step), then the Advanced question.
5. If you struggle with a topic, re-read the lesson named in the *Source* line and try again the next day.
