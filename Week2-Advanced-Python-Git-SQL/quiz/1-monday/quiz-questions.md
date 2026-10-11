# Daily Knowledge Check: Week2-Advanced-Python-Git-SQL — Monday: Python Modules & Environment Management

Try each question before opening the solution. Every question names the written lesson it comes from, so you can go back and re-read.

---

## Part 1: Multiple Choice

### 1. When Python executes `import validators`, in which order does it look for the module?
- [ ] A) Each folder in `sys.path`, then the `sys.modules` cache, then built-in modules
- [ ] B) Built-in modules, then each folder in `sys.path`, then the `sys.modules` cache
- [ ] C) The `sys.modules` cache, then built-in modules, then each folder in `sys.path`
- [ ] D) Only the folders listed in `PYTHONPATH`, then the folder of the running script

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The `sys.modules` cache, then built-in modules, then each folder in `sys.path`

**Explanation:** Python first checks `sys.modules` (modules already imported in this run), then modules compiled into the interpreter, and finally walks the entries of `sys.path` in order.
- **Why others are wrong:**
  - A) The cache is checked first, not after searching the folders.
  - B) The `sys.modules` cache is the first stop, not the last.
  - D) `PYTHONPATH` is only one source of `sys.path` entries, and the script's own folder is the first `sys.path` entry, not a fallback.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 2. A teammate creates a file called `random.py` in the project folder. Now `import random; random.randint(1, 5)` fails with `AttributeError: module 'random' has no attribute 'randint'`. Why?
- [ ] A) The script's own folder is first on `sys.path`, so `import random` loads the local file instead of the standard library module
- [ ] B) Python deletes the standard library `random` module when a file with the same name exists
- [ ] C) `randint` was removed from Python 3 and only exists in third-party packages
- [ ] D) Files named after standard modules are only allowed inside a package folder

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The script's own folder is first on `sys.path`, so `import random` loads the local file instead of the standard library module

**Explanation:** This is the "shadowing trap". The local `random.py` is found before the standard library one, and it has no `randint`. The fix is to rename the file (for example `random_helpers.py`) and delete the stale `__pycache__` folder.
- **Why others are wrong:**
  - B) Nothing is deleted; the standard module is simply never reached.
  - C) `randint` is part of the standard library `random` module.
  - D) There is no such rule; the name clash causes the problem anywhere on the search path.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 3. You run `python qa_toolkit/formatters.py`, and the file contains `from .validators import is_non_empty`. Python reports `ImportError: attempted relative import with no known parent package`. What is the cause and the correct fix?
- [ ] A) Relative imports were removed in Python 3, so you must rewrite every import as absolute
- [ ] B) The file must be renamed to `formatters_main.py` before it can be run
- [ ] C) The package's `__init__.py` is empty, so Python cannot see the package until you add code to it
- [ ] D) Run directly, the file's `__name__` is `"__main__"`, so Python does not know it belongs to a package; run `python -m qa_toolkit.formatters` from the folder that contains `qa_toolkit`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Run directly, the file's `__name__` is `"__main__"`, so Python does not know it belongs to a package; run `python -m qa_toolkit.formatters` from the folder that contains `qa_toolkit`

**Explanation:** Relative imports only work when the file is imported as part of its package. The `-m` flag imports it properly as `qa_toolkit.formatters`, so the dot has a parent package to resolve against.
- **Why others are wrong:**
  - A) Relative imports are still valid inside packages (PEP 8 accepts them for complex layouts).
  - B) The file name is irrelevant to the error.
  - C) An empty `__init__.py` is perfectly valid and still marks the folder as a package.

**Source:** `python-packages.md`
</details>

---

### 4. A `pyproject.toml` declares `name = "qa-toolkit"`, while the package folder is `qa_toolkit/`. Which statement is correct?
- [ ] A) The two names must be identical, including the hyphen, or the installation fails
- [ ] B) `qa-toolkit` is the distribution name that pip installs; `qa_toolkit` is the import name and must be a valid Python identifier, so it uses an underscore
- [ ] C) `import qa-toolkit` is valid because import names may contain hyphens
- [ ] D) The import name is chosen randomly by pip at install time

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `qa-toolkit` is the distribution name that pip installs; `qa_toolkit` is the import name and must be a valid Python identifier, so it uses an underscore

**Explanation:** The distribution (what you `pip install`) and the import package (what you `import`) are different things and need not match. Hyphens are allowed in distribution names but not in import names.
- **Why others are wrong:**
  - A) The lesson explicitly says the names can differ.
  - C) A hyphen is not valid in an identifier; `import qa-toolkit` is a syntax error.
  - D) The import name is simply the package folder name you wrote.

**Source:** `python-packages.md`
</details>

---

### 5. Your teammate runs `python -m pip install requests>=2.31` and finds a new file named `=2.31` in the folder. Which command installs the package the way they intended?
- [ ] A) `python -m pip install "requests>=2.31"`
- [ ] B) `python -m pip install requests => 2.31`
- [ ] C) `python -m pip install requests --version >=2.31`
- [ ] D) `python -m pip install requests==>2.31`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `python -m pip install "requests>=2.31"`

**Explanation:** The shell treats an unquoted `>` as output redirection, so the output went into a file named `=2.31`. Quoting the specifier keeps `>=` as part of the argument passed to pip.
- **Why others are wrong:**
  - B) `=>` is not a valid specifier, and the unquoted `>` is still a problem.
  - C) `--version` is not an install option for choosing a package version.
  - D) `==>` is not valid specifier syntax.

**Source:** `pip-and-package-management.md`
</details>

---

### 6. Which versions satisfy the requirement `requests~=2.31.0` (the "compatible release" operator)?
- [ ] A) Only exactly `2.31.0`
- [ ] B) Any `2.x` release from `2.31.0` upward, including `2.40`
- [ ] C) `2.31.0` and `2.31.5`, but not `2.32.0`
- [ ] D) Every version except `2.31.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `2.31.0` and `2.31.5`, but not `2.32.0`

**Explanation:** `~=2.31.0` means `>=2.31.0` and `==2.31.*`, so only patch releases within 2.31 are allowed.
- **Why others are wrong:**
  - A) That describes `==2.31.0`.
  - B) That describes the two-segment form `~=2.31` (`>=2.31, ==2.*`).
  - D) That describes `!=2.31.0`.

**Source:** `pip-and-package-management.md`
</details>

---

### 7. Which statement best describes what a virtual environment folder created by `python -m venv .venv` contains?
- [ ] A) A full, separate copy of Python including the whole standard library and its own compiler
- [ ] B) Only a `pyvenv.cfg` file; packages are still installed into the global `site-packages`
- [ ] C) A copy of every package currently installed in the global Python
- [ ] D) Its own `site-packages`, activation scripts, a `pyvenv.cfg` file and a link to the base interpreter, which also supplies the standard library

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Its own `site-packages`, activation scripts, a `pyvenv.cfg` file and a link to the base interpreter, which also supplies the standard library

**Explanation:** A venv is an isolated place for third-party packages plus a launcher that knows to look there. It borrows the interpreter and standard library from the Python that created it.
- **Why others are wrong:**
  - A) It is "virtual" precisely because it is not a full copy of Python.
  - B) The environment has its own `site-packages`; that is what gives isolation.
  - C) A new environment starts nearly empty (usually just pip).

**Source:** `virtual-environments.md`
</details>

---

### 8. Why should `.venv/` be listed in `.gitignore`, and what should you commit instead so teammates can rebuild the environment?
- [ ] A) Git cannot store folders whose names start with a dot; commit a zip of the folder instead
- [ ] B) It is large and contains machine-specific absolute paths and binaries, and it can be rebuilt from `requirements.txt`, which you commit
- [ ] C) Python refuses to start if a virtual environment is tracked by Git
- [ ] D) `requirements.txt` is only valid when the `.venv` folder is committed next to it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is large and contains machine-specific absolute paths and binaries, and it can be rebuilt from `requirements.txt`, which you commit

**Explanation:** Share the recipe (`requirements.txt`), not the environment. Each teammate creates their own `.venv` and runs `python -m pip install -r requirements.txt`.
- **Why others are wrong:**
  - A) Git handles dot-folders fine (`.gitignore` itself starts with a dot).
  - C) Python does not care about Git at all.
  - D) `requirements.txt` is plain text and works on its own.

**Source:** `virtual-environments.md`
</details>

---

### 9. Which keyword argument is NOT supported by `datetime.timedelta`?
- [ ] A) `weeks`
- [ ] B) `milliseconds`
- [ ] C) `months`
- [ ] D) `hours`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `months`

**Explanation:** `timedelta` supports `days`, `seconds`, `microseconds`, `milliseconds`, `minutes`, `hours` and `weeks`, but not months or years, because those have varying lengths.
- **Why others are wrong:**
  - A) `weeks` is supported.
  - B) `milliseconds` is supported.
  - D) `hours` is supported.

**Source:** `built-in-python-modules.md`
</details>

---

### 10. What does `git pull` do?
- [ ] A) It runs `git fetch` and then integrates `origin/<branch>` into your current branch (a merge by default, or a rebase if requested)
- [ ] B) It only downloads new commits and moves `origin/main`, leaving your files untouched
- [ ] C) It uploads your local commits to the remote and then downloads the remote's commits
- [ ] D) It creates a brand-new local copy of the remote repository in a new folder

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It runs `git fetch` and then integrates `origin/<branch>` into your current branch (a merge by default, or a rebase if requested)

**Explanation:** `git pull = git fetch + integrate`. Because it changes your current branch and working files, it can stop or conflict, unlike a plain fetch.
- **Why others are wrong:**
  - B) That describes `git fetch`.
  - C) Uploading is `git push`; pull never uploads.
  - D) That describes `git clone`.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

### 11. A module defines `__all__ = ["is_valid_email"]` and also has a helper function `_strip` and a function `is_positive_int`. What does `from validators import *` bring into the importing file?
- [ ] A) `is_valid_email` and `is_positive_int`, because only underscore names are hidden
- [ ] B) Only `is_valid_email`
- [ ] C) `is_valid_email` and `_strip`, because `__all__` only hides names from `dir()`
- [ ] D) Nothing, because star-imports are disabled once `__all__` exists

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Only `is_valid_email`

**Explanation:** When `__all__` is defined, a star-import brings in exactly the names listed in it. (`validators._strip(...)` still works if you use the module prefix, because `__all__` only affects star-imports and signals intent.)
- **Why others are wrong:**
  - A) With `__all__` present, the list decides, not the underscore rule; `is_positive_int` is not listed.
  - C) `__all__` has nothing to do with `dir()`; it controls star-imports, and `_strip` is not listed.
  - D) Star-imports are not disabled; `__all__` is exactly the list they use.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 12. Importing `a` raises `ImportError: cannot import name 'func_a' from partially initialized module 'a' (most likely due to a circular import)`. Module `b` imports from `a`, and `a` imports from `b`. What is the best long-term fix?
- [ ] A) Wrap the import in `try/except ImportError` and ignore the failure
- [ ] B) Rename both files so their names no longer clash
- [ ] C) Call `importlib.reload(a)` at the top of `b`
- [ ] D) Move the code both modules need into a third module `c` that both import, so dependencies flow in one direction

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Move the code both modules need into a third module `c` that both import, so dependencies flow in one direction

**Explanation:** A circular import happens when module A and module B each need the other before either has finished loading. Extracting the shared piece (A -> C <- B) removes the cycle instead of hiding it.
- **Why others are wrong:**
  - A) This hides the symptom; the name is still missing when the code later needs it.
  - B) The names do not clash; the problem is the mutual dependency, which renaming does not change.
  - C) `reload` re-executes a module that is already loaded; it does not fix the order problem of a half-initialised module.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 13. Which arrangement of imports at the top of a file follows the PEP 8 conventions described in the lesson?
- [ ] A) Standard library imports first, then third-party libraries (installed with pip), then your own project's modules, with a blank line between the groups
- [ ] B) Your own modules first, then third-party libraries, then the standard library
- [ ] C) All imports sorted purely alphabetically with no grouping
- [ ] D) Imports placed just before the first line that uses them, scattered through the file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Standard library imports first, then third-party libraries (installed with pip), then your own project's modules, with a blank line between the groups

**Explanation:** PEP 8 asks for imports at the top of the file (after the module docstring), one per line, grouped as standard library, third-party, then local project modules.
- **Why others are wrong:**
  - B) The conventional order starts with the standard library and ends with your own modules.
  - C) Alphabetical order is not the rule; grouping by origin is.
  - D) PEP 8 puts imports at the top of the file; scattering them hides the file's dependencies.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 14. A package's `__init__.py` contains `from qa_toolkit.validators import is_valid_email`. What is the effect of `import qa_toolkit` in another file?
- [ ] A) Nothing runs until you call a function from the package
- [ ] B) `__init__.py` is ignored once the folder contains other `.py` files
- [ ] C) Python runs `__init__.py` once, so `is_valid_email` becomes available as `qa_toolkit.is_valid_email`
- [ ] D) The import fails, because `__init__.py` is not allowed to import its own submodules

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Python runs `__init__.py` once, so `is_valid_email` becomes available as `qa_toolkit.is_valid_email`

**Explanation:** Importing a package executes its `__init__.py`, and the names defined there become attributes of the package. This is how libraries expose a friendly public API.
- **Why others are wrong:**
  - A) Importing a package executes `__init__.py` immediately, just as importing a module executes its top-level code.
  - B) `__init__.py` is always executed when the package is imported; it is what marks and initialises the package.
  - D) It is allowed, and re-exporting names this way is the pattern the lesson recommends.

**Source:** `python-packages.md`
</details>

---

### 15. Inside `qa_toolkit/api/checks.py`, which line is a valid RELATIVE import of `is_valid_email` from `qa_toolkit/validators.py`?
- [ ] A) `from ..validators import is_valid_email`
- [ ] B) `from .validators import is_valid_email`
- [ ] C) `from ...validators import is_valid_email`
- [ ] D) `from qa_toolkit.api.validators import is_valid_email`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `from ..validators import is_valid_email`

**Explanation:** One dot means the current package (`qa_toolkit.api`) and two dots mean its parent (`qa_toolkit`), so `..validators` reaches `qa_toolkit/validators.py`.
- **Why others are wrong:**
  - B) One dot means the same folder (`qa_toolkit/api/`), so Python would look for `qa_toolkit/api/validators.py`.
  - C) Three dots go to the grandparent, which is above the `qa_toolkit` package.
  - D) This is an absolute import, and it names a module that does not exist in the `api` subpackage.

**Source:** `python-packages.md`
</details>

---

### 16. Why do many professional projects use the "src layout" (`src/qa_toolkit/...`) instead of putting `qa_toolkit/` at the repository root?
- [ ] A) Python refuses to import a package that sits directly at the repository root
- [ ] B) Imports from a `src/` folder run faster than imports from the root
- [ ] C) `pip install -e .` only works when the code is inside a folder named `src`
- [ ] D) The package cannot be imported by accident from the working directory without installing it, so tests exercise the same code that users will install

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The package cannot be imported by accident from the working directory without installing it, so tests exercise the same code that users will install

**Explanation:** Because the package is not on the path by default, packaging mistakes (such as a missing file) show up early, and tests run against the installed package.
- **Why others are wrong:**
  - A) A root-level (flat) layout works fine and is used for small learning projects.
  - B) The layout has no effect on import speed.
  - C) Editable installs work with any layout; `where = ["src"]` in `pyproject.toml` simply tells setuptools where to look.

**Source:** `python-packages.md`
</details>

---

### 17. You run `python -m pip install requests` and pip reports that it installed five packages. What are the other four?
- [ ] A) Older versions of `requests`, kept as a backup in case the newest one fails
- [ ] B) Optional extras that every user must enable with square brackets
- [ ] C) Development tools that are bundled into every pip installation
- [ ] D) Transitive dependencies: packages that `requests` itself needs, such as `urllib3`, `idna`, `certifi` and `charset-normalizer`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Transitive dependencies: packages that `requests` itself needs, such as `urllib3`, `idna`, `certifi` and `charset-normalizer`

**Explanation:** pip reads the package's metadata, resolves a compatible set of versions and installs the dependencies of your dependency along with it.
- **Why others are wrong:**
  - A) pip does not keep backup copies of the package it installs.
  - B) Extras such as `requests[socks]` are only installed when you ask for them.
  - C) pip does not add unrelated tools; the extra packages are what `requests` depends on.

**Source:** `pip-and-package-management.md`
</details>

---

### 18. Which command shows installed packages that have newer versions available, without changing anything?
- [ ] A) `python -m pip check`
- [ ] B) `python -m pip list --outdated`
- [ ] C) `python -m pip freeze`
- [ ] D) `python -m pip install --upgrade requests`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `python -m pip list --outdated`

**Explanation:** `pip list --outdated` only reports; it never upgrades. You then decide deliberately (and read the changelog) before upgrading.
- **Why others are wrong:**
  - A) `check` verifies that installed packages' dependency rules are satisfied; it does not look for newer versions.
  - C) `freeze` prints every installed package pinned to its current exact version, with no information about newer releases.
  - D) This performs an upgrade of one package instead of just reporting.

**Source:** `pip-and-package-management.md`
</details>

---

### 19. Which line in `requirements.txt` installs `colorama` only when the platform is Windows?
- [ ] A) `colorama[win32]`
- [ ] B) `colorama==win32`
- [ ] C) `colorama; sys_platform == "win32"`
- [ ] D) `-r colorama`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `colorama; sys_platform == "win32"`

**Explanation:** The part after the semicolon is an environment marker. pip evaluates it and installs the package only when the condition is true, which helps teams that mix Windows, macOS and Linux.
- **Why others are wrong:**
  - A) Square brackets request an extra (optional feature set), not a platform condition.
  - B) `==` expects a version number, not a platform name.
  - D) `-r` includes another requirements file; it is not a platform filter.

**Source:** `pip-and-package-management.md`
</details>

---

### 20. In Windows PowerShell, which command run from the project folder activates the environment `.venv`?
- [ ] A) `.venv\Scripts\Activate.ps1`
- [ ] B) `source .venv/bin/activate`
- [ ] C) `.venv\Scripts\activate.bat`
- [ ] D) `python -m venv activate`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `.venv\Scripts\Activate.ps1`

**Explanation:** On Windows the environment's scripts live in `Scripts` rather than `bin`, and PowerShell uses the `.ps1` script. After activation, the prompt shows `(.venv)`.
- **Why others are wrong:**
  - B) That is the macOS/Linux (bash, zsh) form; there is no `bin` folder in a Windows environment.
  - C) `activate.bat` is for Command Prompt (cmd), not PowerShell.
  - D) That would create a new environment folder named `activate`; it activates nothing.

**Source:** `virtual-environments.md`
</details>

---

### 21. After you move your project folder to a new location, `.venv/bin/pip` fails with `bad interpreter: No such file or directory`. What is the best fix?
- [ ] A) Copy the contents of `.venv/lib/.../site-packages` into the global Python's `site-packages`
- [ ] B) Commit `.venv` to Git so that the paths are stored safely
- [ ] C) Delete the `.venv` folder, create a new one in the new location and reinstall with `python -m pip install -r requirements.txt`
- [ ] D) Rename `.venv` to `venv`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Delete the `.venv` folder, create a new one in the new location and reinstall with `python -m pip install -r requirements.txt`

**Explanation:** Environments contain absolute paths and point to the original interpreter, so moving them breaks them. Because they are disposable and rebuildable from `requirements.txt`, recreating is the quickest cure.
- **Why others are wrong:**
  - A) This pollutes the global Python and removes the isolation the environment exists to provide.
  - B) The paths inside would still be wrong, and committing an environment folder is a mistake in the first place.
  - D) A different name does not change the broken absolute paths stored inside.

**Source:** `virtual-environments.md`
</details>

---

### 22. A script must refuse to run outside a virtual environment. Which test do the lesson's examples use to detect that it is inside one?
- [ ] A) `sys.executable == sys.base_prefix`
- [ ] B) `sys.prefix != sys.base_prefix`
- [ ] C) `sys.path[0] == ""`
- [ ] D) `sys.platform == "venv"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `sys.prefix != sys.base_prefix`

**Explanation:** Inside a venv, `sys.prefix` points to the environment folder while `sys.base_prefix` still points to the original Python installation, so they differ. Outside a venv they are equal.
- **Why others are wrong:**
  - A) `sys.executable` is the path of the interpreter file, which is never equal to a prefix folder.
  - C) The first `sys.path` entry describes where the script lives, not whether an environment is active.
  - D) `sys.platform` holds values such as `win32`, `linux` or `darwin`; it says nothing about environments.

**Source:** `virtual-environments.md`
</details>

---

### 23. Which call makes sure the folder `output/reports` exists (creating `output` as well if needed) and does NOT raise an error if the folder is already there?
- [ ] A) `os.mkdir("output/reports")`
- [ ] B) `os.makedirs("output/reports")`
- [ ] C) `os.path.exists("output/reports")`
- [ ] D) `os.makedirs("output/reports", exist_ok=True)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `os.makedirs("output/reports", exist_ok=True)`

**Explanation:** `makedirs` creates every missing level of the path, and `exist_ok=True` suppresses the `FileExistsError`. It is the standard "make sure this folder exists" idiom.
- **Why others are wrong:**
  - A) `mkdir` creates only the last level, so it fails if `output` does not exist, and it raises `FileExistsError` if the folder already exists.
  - B) Without `exist_ok=True` it raises `FileExistsError` when the folder already exists.
  - C) This only checks and returns `True` or `False`; it creates nothing.

**Source:** `built-in-python-modules.md`
</details>

---

### 24. A script is started with `python check.py staging 5`. What does `sys.argv` contain?
- [ ] A) `['check.py', 'staging', '5']`: a list of strings, with the script name at index 0
- [ ] B) `['staging', '5']`
- [ ] C) `['check.py', 'staging', 5]`
- [ ] D) `('python', 'check.py', 'staging', '5')`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `['check.py', 'staging', '5']`: a list of strings, with the script name at index 0

**Explanation:** `sys.argv` is a list of strings: the script name followed by each argument. The `5` is still text, so convert it with `int(sys.argv[2])` before using it as a number.
- **Why others are wrong:**
  - B) The script name is always included as `sys.argv[0]`; real arguments start at index 1.
  - C) Every element is a string; Python never converts command-line arguments to numbers for you.
  - D) `sys.argv` is a list and does not include the `python` command itself.

**Source:** `built-in-python-modules.md`
</details>

---

### 25. Which is the right way to check in a test that `0.1 + 0.2` equals `0.3`?
- [ ] A) `0.1 + 0.2 == 0.3`
- [ ] B) `0.1 + 0.2 is 0.3`
- [ ] C) `math.isclose(0.1 + 0.2, 0.3)`
- [ ] D) `math.floor(0.1 + 0.2) == math.floor(0.3)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `math.isclose(0.1 + 0.2, 0.3)`

**Explanation:** Floating-point rounding makes `0.1 + 0.2 == 0.3` evaluate to `False`, so floats should be compared with a tolerance. `math.isclose` does exactly that.
- **Why others are wrong:**
  - A) This is `False` because of floating-point rounding, which is the very trap the lesson warns about.
  - B) `is` tests object identity, not numeric closeness, and it is not a reliable way to compare numbers.
  - D) Both values floor to 0, so it "passes" for almost any pair of small numbers and proves nothing.

**Source:** `built-in-python-modules.md`
</details>

---

### 26. `git branch -vv` shows `[origin/main: ahead 2, behind 3]` next to `main`. What does this mean?
- [ ] A) You have 3 local commits to push and the remote has 2 that you lack
- [ ] B) You have 2 local commits the remote does not have, and the remote has 3 commits you do not have, so the histories have diverged
- [ ] C) 2 files are modified and 3 files are untracked in your working folder
- [ ] D) Your branch is 5 commits away from the commit you cloned

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) You have 2 local commits the remote does not have, and the remote has 3 commits you do not have, so the histories have diverged

**Explanation:** Ahead means commits to push, behind means commits to fetch or pull. When both are non-zero you must integrate the remote's work (for example `git pull --rebase`) before your push can succeed.
- **Why others are wrong:**
  - A) The numbers are reversed in this reading; "ahead" is what you have and the remote lacks.
  - C) The counts are about commits compared with the upstream branch, not files in the working folder.
  - D) The counts are measured against `origin/main`, and "ahead" and "behind" are separate numbers.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

### 27. Your history has diverged from `origin/main`, and you run `git pull --ff-only`. What happens?
- [ ] A) Git creates a merge commit automatically
- [ ] B) Git silently rebases your commits on top of the remote's
- [ ] C) Git overwrites the remote branch with your version
- [ ] D) Git stops with "Not possible to fast-forward, aborting." and leaves your branch and files untouched

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Git stops with "Not possible to fast-forward, aborting." and leaves your branch and files untouched

**Explanation:** `--ff-only` integrates only when a fast-forward is possible. On diverged history it refuses, which is why it is a good beginner habit: you then choose between merge and rebase consciously.
- **Why others are wrong:**
  - A) That is what a default `git pull` (merge) or `--no-rebase` does, not `--ff-only`.
  - B) Rebasing is requested with `--rebase`; `--ff-only` never rewrites commits.
  - C) `pull` never uploads anything, and overwriting a remote branch is what a force push does.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

## Part 2: True / False

### 28. True or False: If two files in the same program both run `import noisy`, and `noisy.py` has a `print()` at the top level, the message is printed twice.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The first import executes the module and stores it in `sys.modules`. Later `import noisy` statements anywhere in the program fetch the cached module, so the top-level code runs only once.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 29. True or False: Running `python -m pip uninstall requests` does not automatically uninstall the dependencies (such as `urllib3` and `idna`) that were installed along with it.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** pip does not track "who asked for whom" well enough to be sure those transitive dependencies are unneeded, so it removes only the package you named.

**Source:** `pip-and-package-management.md`
</details>

---

### 30. True or False: A virtual environment must be activated before you can use its Python interpreter to run a script.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Activation is only a convenience that puts the environment's `bin` (or `Scripts`) folder at the front of `PATH`. You can run `.venv/bin/python script.py` (or `.venv\Scripts\python.exe` on Windows) directly, which is handy in CI pipelines and scheduled jobs.

**Source:** `virtual-environments.md`
</details>

---

### 31. True or False: The `random` module is the right tool for generating passwords and security tokens, since its output is random.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `random` is pseudo-random and not secure; an attacker could predict it. It is perfect for test data, but passwords and tokens should come from the separate `secrets` module.

**Source:** `built-in-python-modules.md`
</details>

---

### 32. True or False: `git fetch` merges the remote's new commits into your current branch and updates the files in your working folder.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `git fetch` only downloads commits and moves remote-tracking branches such as `origin/main`. Your local branches and working files are not touched, which is why it is safe to run at any time. Integrating the changes is what `git pull` (or `git merge origin/main`) adds.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

### 33. True or False: When a module does not define `__all__`, `from module import *` skips names that begin with an underscore.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Names starting with a single underscore are a convention for "internal helper", and a star-import leaves them out. They can still be reached with the module prefix, for example `module._helper`.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 34. True or False: A name that is not listed in a package's `__all__` cannot be imported with `from qa_toolkit.validators import that_name`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `__all__` only defines what `from package import *` exports and signals the public API. An explicit import of an unlisted name still works.

**Source:** `python-packages.md`
</details>

---

### 35. True or False: Running `python -m pip freeze > requirements.txt` preserves loose ranges such as `requests>=2.31,<3` that you used when installing.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `pip freeze` prints every installed package, including transitive dependencies, pinned to its exact installed version (for example `requests==2.31.0`). Ranges are only kept in a file you write by hand.

**Source:** `pip-and-package-management.md`
</details>

---

### 36. True or False: Activation applies to one terminal window, so a newly opened terminal starts without any environment and you must activate again.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Activation changes only the current terminal session (its `PATH` and prompt). Closing the terminal ends the activation, but the `.venv` folder stays on disk.

**Source:** `virtual-environments.md`
</details>

---

### 37. True or False: `random.randint(1, 6)` can return 6, whereas `random.randrange(1, 6)` can never return 6.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `randint(a, b)` includes both ends, while `randrange(a, b)` behaves like `range` and excludes the end value. It is an easy off-by-one mistake when generating test data.

**Source:** `built-in-python-modules.md`
</details>

---

### 38. True or False: `b = a.replace(hour=0)` changes the hour of the existing datetime object `a`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `datetime` objects are immutable. `replace` (like arithmetic with `timedelta`) returns a new object and leaves `a` unchanged.

**Source:** `built-in-python-modules.md`
</details>

---

### 39. True or False: After running `git fetch`, the command `git log --oneline HEAD..origin/main` lists the remote commits that you do not have yet.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `A..B` means "commits reachable from B but not from A", so `HEAD..origin/main` shows what is on the remote that you lack. It works because `fetch` has already updated the `origin/main` bookmark.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

## Part 3: Code Prediction

All outputs below were produced by running the code with Python 3 as a script (`python3 file.py`).

### 40. What does this script print?
```python
import math as m
import math

print(m is math)
print(__name__)
```
- [ ] A) `False` then `__main__`
- [ ] B) `True` then `__main__`
- [ ] C) `True` then `math`
- [ ] D) `ImportError`, because `math` is imported twice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `True` then `__main__`

**Explanation:** Both names refer to the same cached module object from `sys.modules`, so `m is math` is `True`. Because the file is run directly, its own `__name__` is `"__main__"`.
- **Why others are wrong:**
  - A) An alias does not create a second copy of the module; it is the same object.
  - C) `__name__` here is the name of *this* file's module, not `math`.
  - D) Importing the same module twice is harmless; the second import uses the cache.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 41. What does this script print (one value per line, shown here separated by commas)?
```python
import xml
import xml.etree.ElementTree as ET

print(ET.__name__)
print(ET.__package__)
print(hasattr(xml, "__path__"))
print(hasattr(ET, "__path__"))
```
- [ ] A) `ElementTree`, `xml`, `True`, `True`
- [ ] B) `xml.etree.ElementTree`, `xml`, `False`, `True`
- [ ] C) `xml.etree.ElementTree`, `xml.etree`, `True`, `False`
- [ ] D) `xml.etree`, `xml.etree.ElementTree`, `True`, `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `xml.etree.ElementTree`, `xml.etree`, `True`, `False`

**Explanation:** A module inside a package has a dotted `__name__` mirroring the folder structure, and its `__package__` is the package that contains it. Only packages have a `__path__` attribute, so `xml` has one and the plain module `ElementTree` does not.
- **Why others are wrong:**
  - A) `__name__` is the full dotted path, and a plain module has no `__path__`.
  - B) The containing package is `xml.etree`, and `xml` (a package) does have `__path__`.
  - D) The `__name__` and `__package__` values are swapped.

**Source:** `python-packages.md`
</details>

---

### 42. What does this script print? (It mimics how a preflight script reads pinned requirements.)
```python
lines = ["# deps", "", "requests>=2.31,<3", "pytest==8.1.1"]
pins = {}
for line in lines:
    line = line.strip()
    if not line or line.startswith("#") or "==" not in line:
        continue
    name, version = line.split("==", 1)
    pins[name] = version
print(pins)
```
- [ ] A) `{}`
- [ ] B) `{'requests': '>=2.31,<3', 'pytest': '8.1.1'}`
- [ ] C) `{'requests': '2.31', 'pytest': '8.1.1'}`
- [ ] D) `{'pytest': '8.1.1'}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `{'pytest': '8.1.1'}`

**Explanation:** The comment line, the blank line and the `requests>=2.31,<3` line (which has no `==`, so it is not an exact pin) are all skipped by `continue`. Only `pytest==8.1.1` is split at the first `==` into name and version.
- **Why others are wrong:**
  - A) The `pytest==8.1.1` line is an exact pin and is recorded.
  - B) The `requests` line is skipped because `"=="` is not in it.
  - C) No code ever extracts `2.31` from a `>=` range.

**Source:** `pip-and-package-management.md`
</details>

---

### 43. What does this script print?
```python
import datetime as dt

t = dt.datetime(2025, 1, 31, 23, 59, 0)
print(t.strftime("report_%Y%m%d_%H%M%S.html"))
print(t + dt.timedelta(minutes=90))
print(t.weekday())
```
- [ ] A) `report_20250131_235900.html`, then `2025-02-01 01:29:00`, then `4`
- [ ] B) `report_20250131_235900.html`, then `2025-01-31 01:29:00`, then `4`
- [ ] C) `report_20250131_235900.html`, then `2025-02-01 01:29:00`, then `5`
- [ ] D) `report_2025-01-31_23:59:00.html`, then `2025-02-01 01:29:00`, then `4`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `report_20250131_235900.html`, then `2025-02-01 01:29:00`, then `4`

**Explanation:** `%Y%m%d_%H%M%S` produces `20250131_235900`. Adding 90 minutes to 23:59 on 31 January rolls over to 01:29 on 1 February. 31 January 2025 is a Friday, and `weekday()` counts Monday as 0, so Friday is 4.
- **Why others are wrong:**
  - B) `timedelta` carries over into the next day; the date does not stay on 31 January.
  - C) 5 would be Saturday; Monday = 0 makes Friday 4.
  - D) The format codes contain no dashes or colons, so the text is exactly `20250131_235900`.

**Source:** `built-in-python-modules.md`
</details>

---

### 44. What does this script print (one value per line, shown here separated by commas)?
```python
import random

items = [3, 1, 2]
result = random.shuffle(items)
print(result)
print(len(items))
rng1 = random.Random(5)
rng2 = random.Random(5)
print(rng1.randint(1, 100) == rng2.randint(1, 100))
```
- [ ] A) `[1, 2, 3]`, `3`, `True`
- [ ] B) `None`, `3`, `True`
- [ ] C) `None`, `3`, `False`
- [ ] D) `None`, `0`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `None`, `3`, `True`

**Explanation:** `random.shuffle` rearranges the list in place and returns `None`, so `result` is `None` while `items` still has 3 elements. Two generators created with the same seed produce the same sequence, so the comparison is `True`.
- **Why others are wrong:**
  - A) `shuffle` does not return a list (and its order would be random anyway); `sample` is the function that returns a new list.
  - C) The same seed gives the same values, so the comparison is `True`.
  - D) Shuffling keeps all elements; the list is not emptied.

**Source:** `built-in-python-modules.md`
</details>

---

### 45. What does this script print?
```python
from math import sqrt
from cmath import sqrt

print(sqrt(16))
```
- [ ] A) `(4+0j)`
- [ ] B) `4.0`
- [ ] C) `4`
- [ ] D) `ImportError: name 'sqrt' is already imported`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `(4+0j)`

**Explanation:** With `from module import name`, a second import of the same name silently replaces the first. The name `sqrt` now refers to `cmath.sqrt`, which works with complex numbers and returns `(4+0j)`.
- **Why others are wrong:**
  - B) That is what `math.sqrt` would return, but its binding was replaced by the second import.
  - C) Neither square-root function returns an `int`; `math.sqrt` gives a float and `cmath.sqrt` a complex number.
  - D) Python allows rebinding a name; no error is raised, which is exactly the danger of this import style.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 46. What does this script print (one value per line, shown here separated by commas)?
```python
import string
import string as s2

s2.custom = "shared"
print(string.custom)
print(string is s2)
print(len(string.digits))
```
- [ ] A) `AttributeError`
- [ ] B) `shared`, `False`, `10`
- [ ] C) `shared`, `True`, `10`
- [ ] D) `None`, `True`, `10`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `shared`, `True`, `10`

**Explanation:** Both names point to the single module object cached in `sys.modules`, so an attribute set through one name is visible through the other. This is why module-level state is shared by every file that imports a module.
- **Why others are wrong:**
  - A) `s2` is not a copy; it is the same module object, so `custom` exists under both names.
  - B) An alias does not create a second module, so `string is s2` is `True`.
  - D) The attribute was set to `"shared"`, not `None`.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 47. This function mimics how Python resolves the dots of a relative import written inside the package `qa_toolkit.api`. What does the script print?
```python
def resolve(current_package, dots, name):
    parts = current_package.split(".")
    base = parts[: len(parts) - (dots - 1)]
    return ".".join(base + [name])

print(resolve("qa_toolkit.api", 1, "checks"))
print(resolve("qa_toolkit.api", 2, "validators"))
```
- [ ] A) `qa_toolkit.api.checks`, then `qa_toolkit.api.validators`
- [ ] B) `qa_toolkit.checks`, then `qa_toolkit.validators`
- [ ] C) `api.checks`, then `validators`
- [ ] D) `qa_toolkit.api.checks`, then `qa_toolkit.validators`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `qa_toolkit.api.checks`, then `qa_toolkit.validators`

**Explanation:** One dot stays in the current package (`qa_toolkit.api`), and each extra dot climbs one level, so two dots land in `qa_toolkit`. This matches `from .checks import ...` and `from ..validators import ...`.
- **Why others are wrong:**
  - A) The second call has two dots, which climbs from `qa_toolkit.api` up to `qa_toolkit`.
  - B) A single dot does not climb; it keeps the current package.
  - C) Climbing removes whole trailing levels only; the top-level package name `qa_toolkit` stays in the path.

**Source:** `python-packages.md`
</details>

---

### 48. This function emulates the "compatible release" rule `~=2.31.0` (`>=2.31.0` and `==2.31.*`). What does the script print (one value per line, shown here separated by commas)?
```python
def compatible(version, base):
    v = tuple(int(x) for x in version.split("."))
    b = tuple(int(x) for x in base.split("."))
    return v >= b and v[:2] == b[:2]

print(compatible("2.31.5", "2.31.0"))
print(compatible("2.32.0", "2.31.0"))
print(compatible("2.30.9", "2.31.0"))
```
- [ ] A) `True`, `True`, `False`
- [ ] B) `True`, `False`, `False`
- [ ] C) `True`, `False`, `True`
- [ ] D) `False`, `False`, `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `True`, `False`, `False`

**Explanation:** `2.31.5` is at least `2.31.0` and stays in the 2.31 series, so it matches. `2.32.0` is a different minor version, and `2.30.9` is older than the base, so both fail.
- **Why others are wrong:**
  - A) `2.32.0` fails the `v[:2] == b[:2]` test; `~=2.31.0` allows only patch releases of 2.31.
  - C) `2.30.9` is smaller than `2.31.0`, so `v >= b` is `False`.
  - D) `2.31.5` is a patch release within 2.31 and newer than the base, so the first result is `True`.

**Source:** `pip-and-package-management.md`
</details>

---

### 49. This script simulates the venv test with made-up prefix values. What does it print (one value per line, shown here separated by commas)?
```python
def in_venv(prefix, base_prefix):
    return prefix != base_prefix

checks = [("/home/you/qe/.venv", "/usr"), ("/usr", "/usr")]
for prefix, base in checks:
    print(prefix, in_venv(prefix, base))
print(sum(in_venv(p, b) for p, b in checks))
```
- [ ] A) `/home/you/qe/.venv True`, `/usr False`, `1`
- [ ] B) `/home/you/qe/.venv False`, `/usr True`, `1`
- [ ] C) `/home/you/qe/.venv True`, `/usr True`, `2`
- [ ] D) `/home/you/qe/.venv True`, `/usr False`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `/home/you/qe/.venv True`, `/usr False`, `1`

**Explanation:** Inside an environment the two prefixes differ, so the first check is `True`; for the plain installation they are equal, so it is `False`. `sum` adds up the booleans (`True` counts as 1), giving the integer `1`.
- **Why others are wrong:**
  - B) The results are reversed; differing prefixes mean "inside a venv".
  - C) Identical prefixes compare equal, so `!=` gives `False` for `/usr`.
  - D) `sum` of booleans returns an integer count (`1`), not a boolean.

**Source:** `virtual-environments.md`
</details>

---

### 50. What does this script print (one value per line, shown here separated by commas)?
```python
import datetime as dt

a = dt.datetime(2025, 3, 14, 9, 0)
b = a.replace(hour=17)
print(a)
print(b - a)
print((b - a).total_seconds())
print(dt.datetime.strptime("14/03/2025", "%d/%m/%Y").strftime("%b %d, %y"))
```
- [ ] A) `2025-03-14 17:00:00`, `8:00:00`, `28800.0`, `Mar 14, 25`
- [ ] B) `2025-03-14 09:00:00`, `8:00:00`, `28800`, `Mar 14, 25`
- [ ] C) `2025-03-14 09:00:00`, `8:00:00`, `28800.0`, `Mar 14, 25`
- [ ] D) `2025-03-14 09:00:00`, `8:00:00`, `28800.0`, `Mar 14, 2025`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `2025-03-14 09:00:00`, `8:00:00`, `28800.0`, `Mar 14, 25`

**Explanation:** `replace` returns a new object, so `a` is still 09:00. The difference is an 8-hour `timedelta`, `total_seconds()` returns a float (8 x 3600), and `%b %d, %y` gives the short month name and a two-digit year.
- **Why others are wrong:**
  - A) `replace` does not modify `a`; datetimes are immutable.
  - B) `total_seconds()` always returns a float, so it prints `28800.0`.
  - D) `%y` is the two-digit year (`25`); the four-digit form would be `%Y`.

**Source:** `built-in-python-modules.md`
</details>

---

### 51. What does this script print (one value per line, shown here separated by commas)?
```python
import os

p = "/projects/qe/data/report.final.html"
print(os.path.basename(p))
print(os.path.splitext(p)[1])
print(os.path.dirname(p))
print(os.path.splitext(os.path.basename(p))[0])
```
- [ ] A) `report.final.html`, `.final.html`, `/projects/qe/data`, `report`
- [ ] B) `/projects/qe/data/report.final.html`, `.html`, `/projects/qe/data`, `report.final`
- [ ] C) `report.final.html`, `.html`, `/projects/qe/data/`, `report.final`
- [ ] D) `report.final.html`, `.html`, `/projects/qe/data`, `report.final`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `report.final.html`, `.html`, `/projects/qe/data`, `report.final`

**Explanation:** `basename` returns only the file name, `splitext` splits at the last dot (so the extension is `.html`), `dirname` returns the folder without a trailing slash, and the stem of `report.final.html` is `report.final`.
- **Why others are wrong:**
  - A) `splitext` splits at the last dot, not the first.
  - B) `basename` strips the folder part and returns just `report.final.html`.
  - C) `dirname` does not add a trailing slash.

**Source:** `built-in-python-modules.md`
</details>

---

### 52. This script mimics how Git compares two histories (`origin/main..HEAD` and `HEAD..origin/main`). What does it print (one value per line, shown here separated by commas)?
```python
local = ["A", "B", "X"]
remote = ["A", "B", "C", "D"]
ahead = [c for c in local if c not in remote]
behind = [c for c in remote if c not in local]
print(ahead, behind)
print(f"ahead {len(ahead)}, behind {len(behind)}")
print(bool(ahead) and bool(behind))
```
- [ ] A) `['C', 'D'] ['X']`, `ahead 2, behind 1`, `True`
- [ ] B) `['X'] ['C', 'D']`, `ahead 1, behind 2`, `True`
- [ ] C) `['X'] ['C', 'D']`, `ahead 1, behind 2`, `False`
- [ ] D) `['A', 'B', 'X'] ['A', 'B', 'C', 'D']`, `ahead 3, behind 4`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['X'] ['C', 'D']`, `ahead 1, behind 2`, `True`

**Explanation:** Only commit `X` exists locally and only `C` and `D` exist remotely, so you are ahead 1 and behind 2. Because both lists are non-empty, the histories have diverged and you must integrate before pushing.
- **Why others are wrong:**
  - A) The two lists are swapped; "ahead" counts commits that only you have.
  - C) Both lists are non-empty, so `bool(ahead) and bool(behind)` is `True` (a diverged history).
  - D) Commits `A` and `B` exist on both sides, so they are shared history and are not counted.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

## Part 4: Fill-in-the-Blank

### 53. Python keeps the list of folders it searches when resolving an import in `sys.________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `path` (that is, `sys.path`)

**Explanation:** `sys.path` is a plain Python list of strings. The script's own folder is the first entry, followed by the standard library, `site-packages` and any `PYTHONPATH` folders.

**Source:** `creating-and-importing-modules.md`
</details>

---

### 54. To make `python -m qa_toolkit` run a package directly, the package folder needs a file named `________.py`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__main__` (the file `__main__.py`)

**Explanation:** If a package contains `__main__.py`, then `python -m package_name` runs it. This gives a package a command-line entry point.

**Source:** `python-packages.md`
</details>

---

### 55. After finishing work in an active virtual environment, you leave it by typing the command `________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `deactivate`

**Explanation:** `deactivate` is a function defined by the activation script, so it works on every platform, but only after an environment has been activated in that terminal. The environment folder itself stays on disk.

**Source:** `virtual-environments.md`
</details>

---

### 56. The first time you push a new branch, use `git push ____ origin feature/login-tests` so the branch is published and its upstream is recorded.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-u` (short for `--set-upstream`)

**Explanation:** `-u` pushes the branch and records that your local branch tracks `origin/feature/login-tests`, so later plain `git push` and `git pull` know where to go. Without it, a new branch's plain `git push` fails with "no upstream branch".

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

### 57. To install the project in the current folder in editable (development) mode, run `python -m pip install ____ .`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-e` (short for `--editable`)

**Explanation:** `-e` makes pip link to your source folder instead of copying it, so code changes are visible immediately without reinstalling. The `.` means "the project in the current directory".

**Source:** `python-packages.md`
</details>

---

### 58. The command `python -m pip ________` prints `No broken requirements found.` when the installed packages' dependency rules are all satisfied.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `check`

**Explanation:** `pip check` audits the environment for conflicting or missing dependencies. Run it whenever you suspect a conflict, for example after several separate installs.

**Source:** `pip-and-package-management.md`
</details>

---

### 59. If `.venv` was accidentally staged or committed, `git rm -r ________ .venv` untracks it without deleting the files on disk.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--cached`

**Explanation:** `--cached` removes the folder from Git's index only. Afterwards, add `.venv/` to `.gitignore` so that it stays out of the repository.

**Source:** `virtual-environments.md`
</details>

---

### 60. `git ________ --prune` downloads new commits and also removes remote-tracking branches (such as `origin/feature-x`) that were deleted on the remote.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `fetch`

**Explanation:** `git fetch --prune` tidies stale bookmarks after teammates delete merged branches on the remote. You can make it automatic with `git config fetch.prune true`.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

## Part 5: Scenario-Based

### 61. You added a new login-test helper to your team's automation repository and committed it locally. When you run `git push`, Git answers `! [rejected] main -> main (fetch first)`. What is the best next step?
- [ ] A) Run `git push --force` so your version replaces the remote branch
- [ ] B) Delete your local repository, clone it again and copy your helper in by hand
- [ ] C) Run `git fetch`, review what arrived with `git log --oneline HEAD..origin/main`, run `git pull --rebase` (or a merge, per team convention), re-run the tests, then `git push`
- [ ] D) Run the same `git push` again until it succeeds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Run `git fetch`, review what arrived with `git log --oneline HEAD..origin/main`, run `git pull --rebase` (or a merge, per team convention), re-run the tests, then `git push`

**Explanation:** The rejection means the remote contains commits you do not have. Bringing them in first makes your push a fast-forward, so it succeeds without erasing a teammate's work.
- **Why others are wrong:**
  - A) A forced push would delete your teammates' commits from the shared branch; the answer to a rejection is "pull first", not "force".
  - B) Needless and risky; Git already provides a safe way to combine the histories.
  - D) Nothing changes between attempts, so it will be rejected every time.

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

### 62. A teammate checks out your repository (package in `src/qa_toolkit`, with a `pyproject.toml`) and the tests fail with `ModuleNotFoundError: No module named 'qa_toolkit'`, although everything works on your laptop. What should they do first?
- [ ] A) Add `sys.path.append("C:/Users/you/project/src")` to every test file
- [ ] B) Create and activate their own virtual environment, run `python -m pip install -e .` from the project root, and confirm with `python -m pip list`
- [ ] C) Copy the `qa_toolkit` folder into the global Python's `site-packages` by hand
- [ ] D) Ask you to commit your `.venv` folder so they can use it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Create and activate their own virtual environment, run `python -m pip install -e .` from the project root, and confirm with `python -m pip list`

**Explanation:** With a `src` layout the package is not importable until it is installed into the active environment. Installing it in editable mode makes `import qa_toolkit` work from anywhere while that environment is active.
- **Why others are wrong:**
  - A) Hard-coding a path from your laptop breaks on every other machine; editing `sys.path` by hand is a last resort.
  - C) This bypasses pip and the environment, and the copy would never be updated with later changes.
  - D) An environment contains machine-specific paths and binaries and does not work on another computer.

**Source:** `python-packages.md`
</details>

---

### 63. Your nightly UI suite passed on Friday. On Monday 40 tests fail, although nobody changed the tests; the CI job installs "the latest" release of the browser-automation library each night. What is the best response?
- [ ] A) Record known-good versions (a pinned requirements file generated with `pip freeze` from a working environment) and have CI install from it, then upgrade deliberately after reading the changelog
- [ ] B) Delete the 40 failing tests until the library settles down
- [ ] C) Remove `requirements.txt` so that each run installs whatever is newest
- [ ] D) Run `sudo pip install --upgrade` for every package on the CI server

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Record known-good versions (a pinned requirements file generated with `pip freeze` from a working environment) and have CI install from it, then upgrade deliberately after reading the changelog

**Explanation:** Pinning makes failures meaningful: they mean the application changed, not that the tooling shifted underneath you. Comparing `pip freeze` outputs from Friday and Monday also shows which package changed.
- **Why others are wrong:**
  - B) This hides real coverage instead of fixing the cause, which is an uncontrolled version change.
  - C) That is the situation that caused the failure; unpinned installs are not reproducible.
  - D) Upgrading everything blindly adds more change, and installing into the system Python is discouraged.

**Source:** `pip-and-package-management.md`
</details>

---

### 64. On a company laptop, running `.venv\Scripts\Activate.ps1` in PowerShell fails with "running scripts is disabled on this system". Which of the following is an acceptable way forward?
- [ ] A) Install the project's packages into the global Python instead
- [ ] B) Delete `.venv` and create it again, because the environment is corrupted
- [ ] C) Run `python -m pip install --break-system-packages` to get past the error
- [ ] D) Use Command Prompt with `activate.bat`, or skip activation and call `.venv\Scripts\python.exe -m pip ...` directly (or change the policy for your user only if IT guidance allows it)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Use Command Prompt with `activate.bat`, or skip activation and call `.venv\Scripts\python.exe -m pip ...` directly (or change the policy for your user only if IT guidance allows it)

**Explanation:** The error comes from PowerShell's execution policy, not from the environment. Activation is only a convenience that adjusts `PATH`, so calling the environment's interpreter directly gives the same isolation.
- **Why others are wrong:**
  - A) This removes the isolation that virtual environments provide and invites version conflicts.
  - B) The environment is fine; recreating it does not change PowerShell's policy.
  - C) That flag relates to OS-managed Pythons and the `externally-managed-environment` error, which is a different problem, and it is discouraged as a habit.

**Source:** `virtual-environments.md`
</details>

---

### 65. You committed locally and your teammate pushed to `main` first, so your `git push` was rejected. You run `git pull` and Git answers `fatal: Need to specify how to reconcile divergent branches`. What is the right reading of this message?
- [ ] A) The local repository is corrupted, so you should delete it and clone again
- [ ] B) Your teammate's push deleted your commit from the remote
- [ ] C) Nothing is broken: the histories have diverged, and Git wants you to choose a strategy, for example `git pull --rebase` or `git pull --no-rebase` (or set `pull.rebase`)
- [ ] D) You must now run `git push --force` to settle the difference

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Nothing is broken: the histories have diverged, and Git wants you to choose a strategy, for example `git pull --rebase` or `git pull --no-rebase` (or set `pull.rebase`)

**Explanation:** Since Git 2.27 you must say how to combine diverged histories if no default is configured. After integrating, run your tests and push, which is now a fast-forward.
- **Why others are wrong:**
  - A) The message is a request for a decision, not a sign of corruption, and re-cloning would throw away your unpushed commit.
  - B) Your commit was never pushed; Git refused your push precisely to protect your teammate's work.
  - D) Forcing would delete your teammate's commits from the shared branch; the answer to a rejection is "pull first".

**Source:** `collaborative-git-workflow-pull-fetch-and-push.md`
</details>

---

## Answer Key


| Q# | Answer | Q# | Answer | Q# | Answer |
|----|--------|----|--------|----|--------|
| 1 | C | 23 | D | 45 | A |
| 2 | A | 24 | A | 46 | C |
| 3 | D | 25 | C | 47 | D |
| 4 | B | 26 | B | 48 | B |
| 5 | A | 27 | D | 49 | A |
| 6 | C | 28 | B (False) | 50 | C |
| 7 | D | 29 | A (True) | 51 | D |
| 8 | B | 30 | B (False) | 52 | B |
| 9 | C | 31 | B (False) | 53 | `path` |
| 10 | A | 32 | B (False) | 54 | `__main__` |
| 11 | B | 33 | A (True) | 55 | `deactivate` |
| 12 | D | 34 | B (False) | 56 | `-u` |
| 13 | A | 35 | B (False) | 57 | `-e` |
| 14 | C | 36 | A (True) | 58 | `check` |
| 15 | A | 37 | A (True) | 59 | `--cached` |
| 16 | D | 38 | B (False) | 60 | `fetch` |
| 17 | D | 39 | A (True) | 61 | C |
| 18 | B | 40 | B | 62 | B |
| 19 | C | 41 | C | 63 | A |
| 20 | A | 42 | D | 64 | D |
| 21 | C | 43 | A | 65 | C |
| 22 | B | 44 | B | | |
