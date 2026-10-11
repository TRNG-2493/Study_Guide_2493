"""check_exercise.py - self-check for Week 2 Monday (Project 1: qe-foundations kickoff).

Run it from the ROOT of your qe-foundations repository, with your venv ACTIVE:

    PowerShell:  python check_exercise.py
    bash:        python check_exercise.py

Options:
    --root PATH   check a repository somewhere else (default: current folder)
    --submit      ALSO require the Git submission checks (clean tree, remote, pushed)

Every check prints PASS, FAIL or WARN. FAIL lines show a HINT. Exit code is 0
only when no required check failed. This script only READS your project (it
runs `git` read-only commands and imports your package); it changes nothing.
Uses only the standard library, so it runs in any Python 3.9+.
"""

import argparse
import contextlib
import importlib
import importlib.metadata as metadata
import io
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

UTILS_MODULES = ["strings", "numbers", "dates", "data_gen"]
PUBLIC_API = [
    "slugify", "normalize_whitespace", "is_valid_email", "mask_email",
    "is_positive_int", "clamp", "percent",
    "add_days", "days_between", "is_weekend", "timestamp_for_filename",
    "make_users",
]

RESULTS = []  # (status, required, label)


def record(status, label, hint="", required=True):
    RESULTS.append((status, required, label))
    print(f"  [{status}] {label}")
    if status != "PASS" and hint:
        print(f"         HINT: {hint}")


def check(ok, label, hint="", required=True):
    record("PASS" if ok else ("FAIL" if required else "WARN"), label, hint, required)
    return ok


def section(title):
    print(f"\n== {title}")


def run_git(root, *args):
    try:
        done = subprocess.run(["git", *args], cwd=root, capture_output=True,
                              text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return done


def read_bytes(path):
    try:
        return path.read_bytes()
    except OSError:
        return None


# ------------------------------------------------------------------ A
def check_environment(root):
    section("A. Environment (virtual environment + Python)")
    check(sys.version_info >= (3, 9), f"Python >= 3.9 (found {sys.version.split()[0]})",
          "Install a current Python 3 and recreate the venv with it.")
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    check(in_venv, "this check is running INSIDE a virtual environment",
          "Activate it first. PowerShell: .venv\\Scripts\\Activate.ps1   bash: source .venv/bin/activate")
    check((root / ".venv").is_dir(), ".venv folder exists in the repo root",
          "Create it from the repo root: python -m venv .venv")
    if in_venv:
        inside = Path(sys.prefix).resolve() == (root / ".venv").resolve()
        check(inside, "the active venv is THIS repo's .venv",
              "You activated a different environment. Deactivate, then activate .venv of this repo.",
              required=False)


# ------------------------------------------------------------------ B
def check_structure(root):
    section("B. Repository structure (Project 1 milestone)")
    for name in ["README.md", ".gitignore", "requirements.txt", "requirements-dev.txt"]:
        check((root / name).is_file(), f"{name} exists", f"Create {name} in the repo root.")
    check((root / "qe_foundations" / "__init__.py").is_file(), "qe_foundations/__init__.py exists",
          "The package folder needs an __init__.py (src-less layout: qe_foundations/ sits in the repo root).")
    check((root / "qe_foundations" / "utils" / "__init__.py").is_file(),
          "qe_foundations/utils/__init__.py exists", "utils is a sub-package: it needs its own __init__.py.")
    for mod in UTILS_MODULES:
        check((root / "qe_foundations" / "utils" / f"{mod}.py").is_file(),
              f"qe_foundations/utils/{mod}.py exists", f"Create utils/{mod}.py (see README Part 2).")
    for folder in ["tests", "data", "docs"]:
        d = root / folder
        has_file = d.is_dir() and any(p.is_file() for p in d.iterdir())
        check(has_file, f"{folder}/ exists and holds a placeholder file",
              f"Git does not store empty folders. Create {folder}/.gitkeep (empty file).")
    check(not (root / "legacy_helpers.py").exists(), "legacy_helpers.py has been removed from the repo root",
          "After moving the functions into utils/, delete legacy_helpers.py (git rm legacy_helpers.py).")

    gi = read_bytes(root / ".gitignore")
    text = gi.decode("utf-8", "replace") if gi else ""
    lines = {ln.strip().rstrip("/") for ln in text.splitlines() if ln.strip() and not ln.startswith("#")}
    check(".venv" in lines, ".gitignore ignores .venv/", "Add a line:  .venv/")
    check("__pycache__" in lines, ".gitignore ignores __pycache__/", "Add a line:  __pycache__/")
    check(bool({"*.pyc", "*.py[cod]", "*.py[co]"} & lines), ".gitignore ignores *.pyc", "Add a line:  *.pyc",
          required=False)

    readme = (read_bytes(root / "README.md") or b"").decode("utf-8", "replace")
    low = readme.lower()
    check("qe-foundations" in low or "qe foundations" in low, "README names the project (QE Foundations)",
          "Start the README with the project name and one sentence of purpose.")
    check("python -m venv" in readme, "README documents creating a venv (python -m venv)",
          "Add a Setup section with the venv creation command.")
    check("activate.ps1" in low and "source .venv/bin/activate" in low,
          "README shows activation for PowerShell AND bash",
          "Add both: .venv\\Scripts\\Activate.ps1  and  source .venv/bin/activate")
    check("pip install -r requirements.txt" in readme, "README documents pip install -r requirements.txt",
          "Add the install command (use python -m pip install -r requirements.txt).")
    check("project 1" in low and "monday" in low, "README states the Project 1 milestone (Monday)",
          "Add a short 'Project 1 milestone' section: what exists after Monday.", required=False)


# ------------------------------------------------------------------ C
def parse_requirements(path):
    """Return (names, lines, problem). names = lowercase project names."""
    raw = read_bytes(path)
    if raw is None:
        return [], [], "file is missing"
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")) or b"\x00" in raw:
        return [], [], "file is UTF-16 (PowerShell '>' redirection does this)"
    if raw.startswith(b"\xef\xbb\xbf"):
        return [], [], "file starts with a UTF-8 BOM"
    lines = [ln.strip() for ln in raw.decode("utf-8", "replace").splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    names = []
    for ln in lines:
        if ln.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", ln)
        if m:
            names.append(m.group(1).lower().replace("_", "-"))
    return names, lines, ""


def check_requirements(root):
    section("C. Dependencies (requirements files)")
    enc_hint = ("Write it as plain text. PowerShell: python -m pip freeze | Set-Content -Encoding ascii <file>"
                "  (or just type the lines in VS Code, saved as UTF-8).")
    names, lines, problem = parse_requirements(root / "requirements.txt")
    check(not problem, "requirements.txt is plain UTF-8 text" + (f" ({problem})" if problem else ""), enc_hint)
    check("requests" in names, "requirements.txt lists requests", "Add a line such as:  requests>=2.31,<3")
    req_line = next((ln for ln in lines if ln.lower().startswith("requests")), "")
    check(bool(re.search(r"(==|>=|~=|<=|<)", req_line)), "requests has a version specifier",
          "Pin or bound the version, e.g. requests>=2.31,<3 (bare 'requests' is not reproducible).")
    check("pytest" not in names, "requirements.txt contains runtime deps only (no pytest)",
          "pytest is a development tool: move it to requirements-dev.txt.")

    dnames, dlines, dproblem = parse_requirements(root / "requirements-dev.txt")
    check(not dproblem, "requirements-dev.txt is plain UTF-8 text" + (f" ({dproblem})" if dproblem else ""),
          enc_hint)
    check(any(re.match(r"^-r\s+requirements\.txt$", ln) for ln in dlines),
          "requirements-dev.txt includes '-r requirements.txt'",
          "First line should be:  -r requirements.txt")
    check("pytest" in dnames, "requirements-dev.txt lists pytest", "Add a line such as:  pytest>=8,<9")

    try:
        version = metadata.version("requests")
        check(True, f"requests is installed in this environment (version {version})")
    except metadata.PackageNotFoundError:
        check(False, "requests is installed in this environment",
              "With the venv active run:  python -m pip install -r requirements.txt")


# ------------------------------------------------------------------ D
def check_package(root):
    section("D. The qe_foundations package and the utils library")
    sys.path.insert(0, str(root))
    for name in [m for m in sys.modules if m == "qe_foundations" or m.startswith("qe_foundations.")]:
        del sys.modules[name]

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            pkg = importlib.import_module("qe_foundations")
        ok = True
    except Exception as exc:  # report any problem, whatever the type
        pkg, ok = None, False
        err = f"{type(exc).__name__}: {exc}"
    check(ok, "import qe_foundations works" + ("" if ok else f" ({err})"),
          "Run Python from the repo root and make sure qe_foundations/__init__.py exists.")
    if not ok:
        return
    check(not buf.getvalue(), "importing qe_foundations prints nothing",
          "Remove print() calls from module top level (use `if __name__ == \"__main__\":`).")
    check(isinstance(getattr(pkg, "__version__", None), str), "qe_foundations.__version__ is defined",
          'Add  __version__ = "0.1.0"  to qe_foundations/__init__.py.')

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            utils = importlib.import_module("qe_foundations.utils")
        ok = True
    except Exception as exc:
        utils, ok = None, False
        err = f"{type(exc).__name__}: {exc}"
    check(ok, "import qe_foundations.utils works" + ("" if ok else f" ({err})"),
          "Create qe_foundations/utils/__init__.py and make every import inside it resolve.")
    if not ok:
        return
    check(not buf.getvalue(), "importing qe_foundations.utils prints nothing",
          "A library must be silent on import: delete the leftover print() calls / demo code.")

    submods = {}
    for mod in UTILS_MODULES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                submods[mod] = importlib.import_module(f"qe_foundations.utils.{mod}")
            check(True, f"import qe_foundations.utils.{mod} works")
        except Exception as exc:
            check(False, f"import qe_foundations.utils.{mod} works ({type(exc).__name__}: {exc})",
                  f"Create utils/{mod}.py with the right functions (README Part 2/3).")

    missing = [n for n in PUBLIC_API if not callable(getattr(utils, n, None))]
    check(not missing, "utils re-exports the full public API from __init__.py"
          + (f" (missing: {', '.join(missing)})" if missing else ""),
          "In utils/__init__.py: from qe_foundations.utils.strings import slugify, ... for every name.")
    declared = getattr(utils, "__all__", None)
    check(isinstance(declared, (list, tuple)) and not [n for n in PUBLIC_API if n not in declared],
          "utils/__init__.py defines __all__ with every public name", "Add an __all__ list.", required=False)
    if missing:
        print("         (behaviour checks skipped: fix the missing names first)")
        return

    u = utils
    cases = [
        ("slugify", lambda: u.slugify("  Login Page: Happy Path ") == "login-page-happy-path"),
        ("normalize_whitespace", lambda: u.normalize_whitespace("  a   b \t c\n") == "a b c"),
        ("is_valid_email", lambda: u.is_valid_email("qa@example.com") is True
                                   and u.is_valid_email("qa@@example.com") is False
                                   and u.is_valid_email("qa@example") is False),
        ("mask_email (valid)", lambda: u.mask_email("tester@example.com") == "t***@example.com"),
        ("mask_email (invalid is returned unchanged)", lambda: u.mask_email("not-an-email") == "not-an-email"),
        ("is_positive_int", lambda: u.is_positive_int(5) and not u.is_positive_int(0)
                                    and not u.is_positive_int(True) and not u.is_positive_int("5")),
        ("clamp", lambda: u.clamp(150, 0, 100) == 100 and u.clamp(-5, 0, 100) == 0 and u.clamp(7, 0, 100) == 7),
        ("percent", lambda: u.percent(1, 3) == 33.3 and u.percent(5, 0) == 0.0),
        ("add_days", lambda: u.add_days(date(2025, 1, 31), 1) == date(2025, 2, 1)
                             and u.add_days(date(2025, 3, 1), -1) == date(2025, 2, 28)),
        ("days_between", lambda: u.days_between(date(2025, 1, 1), date(2025, 1, 31)) == 30
                                 and u.days_between(date(2025, 1, 31), date(2025, 1, 1)) == -30),
        ("is_weekend", lambda: u.is_weekend(date(2025, 1, 4)) and not u.is_weekend(date(2025, 1, 6))),
        ("timestamp_for_filename", lambda: u.timestamp_for_filename(datetime(2025, 1, 31, 9, 30, 0)) == "20250131_093000"),
        ("make_users (same seed -> same data)", lambda: u.make_users(3, seed=7) == u.make_users(3, seed=7)
                                                        and len(u.make_users(3, seed=7)) == 3),
        ("make_users (different seeds differ)", lambda: u.make_users(5, seed=1) != u.make_users(5, seed=2)),
        ("make_users (record shape)", lambda: sorted(u.make_users(1, seed=1)[0]) == ["age", "email", "id", "name", "role"]),
    ]
    for label, fn in cases:
        try:
            ok = bool(fn())
        except Exception as exc:
            ok = False
            label += f" (raised {type(exc).__name__}: {exc})"
        check(ok, f"behaviour: {label}", "Re-read the docstring / README spec for this function.")

    smoke = root / "smoke_utils.py"
    if smoke.is_file():
        done = subprocess.run([sys.executable, "smoke_utils.py"], cwd=root, capture_output=True, text=True)
        check(done.returncode == 0, "python smoke_utils.py exits with code 0",
              "Run it yourself and read the FAIL lines:  python smoke_utils.py\n" + done.stdout[-300:] + done.stderr[-300:])
    else:
        check(False, "smoke_utils.py is present in the repo root", "Copy smoke_utils.py from starter_code/.")


# ------------------------------------------------------------------ E
def check_git(root, submit):
    section("E. Git" + ("" if submit else "  (informational; add --submit to make these required)"))
    req = submit
    probe = run_git(root, "rev-parse", "--is-inside-work-tree")
    if probe is None:
        check(False, "git is installed", "Install Git and reopen the terminal.", required=req)
        return
    is_repo = probe.returncode == 0 and (root / ".git").exists()
    check(is_repo, "the repo root is a Git repository", "Run:  git init", required=req)
    if not is_repo:
        return
    count = run_git(root, "rev-list", "--count", "HEAD")
    n = int(count.stdout.strip()) if count and count.returncode == 0 and count.stdout.strip().isdigit() else 0
    check(n >= 3, f"at least 3 commits (found {n})", "Commit in small steps: structure, utils, requirements/README.",
          required=req)
    tracked = (run_git(root, "ls-files").stdout or "").splitlines()
    bad = [t for t in tracked if t.startswith(".venv/") or "__pycache__/" in t or t.endswith(".pyc")]
    check(not bad, "no .venv/ or __pycache__ files are tracked",
          "Run: git rm -r --cached .venv   (and fix .gitignore), then commit.", required=req)
    for needed in ["requirements.txt", "qe_foundations/__init__.py", "qe_foundations/utils/__init__.py"]:
        check(needed in tracked, f"{needed} is committed", f"git add {needed} && git commit", required=req)
    status = run_git(root, "status", "--porcelain")
    check(status is not None and not status.stdout.strip(), "working tree is clean (everything committed)",
          "Run git status, then git add / git commit.", required=req)
    remote = run_git(root, "remote", "get-url", "origin")
    has_remote = bool(remote and remote.returncode == 0)
    check(has_remote, "remote 'origin' is configured",
          "git remote add origin <url-of-your-empty-remote-repo>", required=req)
    if has_remote:
        ahead = run_git(root, "rev-list", "--count", "@{u}..HEAD")
        pushed = bool(ahead and ahead.returncode == 0 and ahead.stdout.strip() == "0")
        check(pushed, "all commits are pushed to origin",
              "First push:  git push -u origin main   (later: git push)", required=req)


# ------------------------------------------------------------------ main
def main():
    parser = argparse.ArgumentParser(description="Self-check for Week 2 Monday (qe-foundations kickoff)")
    parser.add_argument("--root", default=".", help="repository root (default: current folder)")
    parser.add_argument("--submit", action="store_true", help="require the Git submission checks too")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    print("Week 2 / Monday self-check - Project 1: qe-foundations kickoff")
    print(f"Repository root: {root}")
    check_environment(root)
    check_structure(root)
    check_requirements(root)
    check_package(root)
    check_git(root, args.submit)

    required = [r for r in RESULTS if r[1]]
    failed = [r for r in required if r[0] == "FAIL"]
    warns = [r for r in RESULTS if r[0] == "WARN"]
    passed = len(required) - len(failed)
    print(f"\nRESULT: {passed}/{len(required)} required checks passed, {len(warns)} warning(s).")
    if failed:
        print("Not done yet. Fix the FAIL items above (start from the top) and run the check again.")
        return 1
    print("All required checks passed." + ("" if args.submit else " Run again with --submit before you hand in."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
