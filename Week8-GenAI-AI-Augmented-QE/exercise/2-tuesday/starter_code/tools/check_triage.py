"""check_triage.py - Stage 5: validate a format-locked CI-triage reply against the real log.

The contract your ci-failure-triage prompt must ask for (copy it into the prompt):
  A JSON array with exactly one object per FAILED test in the log. Each object has exactly:
    "test":        the full test id as it appears after "FAILED " in the log
    "category":    one of "product_bug", "test_bug", "needs_clarification", "environment"
    "evidence":    one line copied EXACTLY from the log that supports the category
    "hypothesis":  one sentence: the most likely cause
    "confirm_by":  one sentence: how a tester confirms or rules out the hypothesis

This script checks the parts a program CAN check: shape, allowed values, one entry per
failure, and that every quoted evidence line really exists in the log (quotes are where
hallucination hides). It cannot tell whether the hypothesis or the category is RIGHT.
That is your review.

Usage:
    python tools/check_triage.py evidence/ci-failure-triage.v1.run1.txt materials/ci-failure-sample.txt
Do not edit.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KEYS = ["test", "category", "evidence", "hypothesis", "confirm_by"]
CATEGORIES = {"product_bug", "test_bug", "needs_clarification", "environment"}


def extract_json(text: str) -> str:
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    start, end = text.find("["), text.rfind("]")
    return text[start:end + 1] if start != -1 and end > start else text


def failed_tests(log: str) -> list[str]:
    return re.findall(r"^FAILED (\S+)", log, re.MULTILINE)


def check(reply: str, log: str) -> list[str]:
    try:
        items = json.loads(extract_json(reply))
    except json.JSONDecodeError as err:
        return [f"not valid JSON: {err.msg} (line {err.lineno}, column {err.colno})"]
    if not isinstance(items, list):
        return ["top level must be a JSON array"]
    problems = []
    log_lines = [line.strip() for line in log.splitlines() if line.strip()]
    seen = []
    for n, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            problems.append(f"element {n}: not an object")
            continue
        label = item.get("test", f"element {n}")
        if sorted(item) != sorted(KEYS):
            problems.append(f"{label}: keys must be exactly {KEYS}, got {list(item)}")
        if item.get("category") not in CATEGORIES:
            problems.append(f"{label}: category {item.get('category')!r} not in {sorted(CATEGORIES)}")
        evidence = str(item.get("evidence", "")).strip()
        if not evidence or not any(evidence in line for line in log_lines):
            problems.append(f"{label}: evidence is not a line from the log: {evidence!r}")
        for key in ("hypothesis", "confirm_by"):
            if not str(item.get(key, "")).strip():
                problems.append(f"{label}: {key} is empty")
        seen.append(item.get("test"))
    expected = failed_tests(log)
    for test in expected:
        if seen.count(test) != 1:
            problems.append(f"{test}: must appear exactly once, appears {seen.count(test)} time(s)")
    for test in seen:
        if test not in expected:
            problems.append(f"{test}: not a FAILED test in the log (invented or mistyped)")
    return problems


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    reply_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    log_text = Path(sys.argv[2]).read_text(encoding="utf-8")
    found = check(reply_text, log_text)
    for p in found:
        print(f"FAIL  {p}")
    print("Contract: OK" if not found else f"Contract: {len(found)} problem(s)")
    print("Reminder: a valid triage is not a correct triage. Review each category and hypothesis.")
    sys.exit(1 if found else 0)
