"""check_milestone.py - a self-check for the Project 1 Monday milestone.

Run:  python check_milestone.py
It is only a checklist helper; your instructor still reviews your code and logs.
"""
import re
import subprocess
import sys
from pathlib import Path


def pytest_out(*args):
    p = subprocess.run([sys.executable, "-m", "pytest", *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def count(*args):
    _, out = pytest_out("--collect-only", "-q", *args)
    return len([l for l in out.splitlines() if "::" in l])


def main():
    results = []

    def check(label, ok):
        results.append(ok)
        print(("[PASS] " if ok else "[FAIL] ") + label)

    ini = Path("pytest.ini").read_text(encoding="utf-8") if Path("pytest.ini").exists() else ""
    check("pytest.ini uses --strict-markers", "--strict-markers" in ini)
    for m in ("smoke", "regression", "boundary", "slow"):
        check(f"marker '{m}' registered in pytest.ini", re.search(rf"^\s*{m}\s*:", ini, re.M) is not None)

    total = count()
    check(f"at least 25 tests collected (found {total})", total >= 25)
    for m, need in (("smoke", 6), ("regression", 10), ("boundary", 5), ("slow", 1)):
        n = count("-m", m)
        check(f"at least {need} tests marked {m} (found {n})", n >= need)
    check("a test class exists (collected ids contain '::Test')", count("-k", "TestCartTotal") >= 1)

    rc, out = pytest_out("-q", "-p", "no:cacheprovider")
    last = [l for l in out.splitlines() if re.search(r"\d+ (passed|failed|skipped|xfailed)", l)]
    summary = last[-1] if last else ""
    print("Run summary:", summary)
    check("no failures or errors in the full run", rc == 0 and not re.search(r"\b(failed|error)", summary))
    check("at least 1 skipped (skip/skipif)", "skipped" in summary)
    check("at least 1 xfailed (known bug documented)", "xfailed" in summary)
    check("SELECTION_LOG.md has no TODO left", "TODO" not in Path("SELECTION_LOG.md").read_text(encoding="utf-8"))
    print("\nALL CHECKS PASSED" if all(results) else "\nSome checks still failing - keep going.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
