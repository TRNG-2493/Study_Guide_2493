"""check_gherkin.py - Stage 4: check a few-shot Gherkin reply for shape, content and leakage.

Same idea as `prompt_lab.py gherkin` in the demo. Shape OK is not content OK:
read the scenarios yourself after the checker passes.

Usage:
    python tools/check_gherkin.py evidence/registration-gherkin.v1.run1.txt

What to do:
1. Fill REQUIRED_VALUES with the exact values your feature MUST contain, taken from
   materials/registration-criteria.md (boundary values and the exact error messages).
2. Fill LEAK_MARKERS with distinctive values from the EXAMPLES you put in your prompt
   (from materials/features/). If any appear in the reply, the model copied your example.
"""
from __future__ import annotations

import sys
from pathlib import Path

KEYWORDS = ("Feature:", "Scenario", "Given ", "When ", "Then ")

REQUIRED_VALUES: list[str] = [
    "@registration",
    "Username must be 4-16 characters",
    "Username may use a-z, 0-9 and - and must start with a letter",
    "Use an example.com or example.org address",
    "Age must be between 16 and 99",
    "Welcome to ShopFront",
    "| 15 ", "| 16 ", "| 99 ", "| 100 ",
]

LEAK_MARKERS: list[str] = [
    "mila.ortiz", "Tulip-Garden", "Walnut Desk Lamp", "My account", "ignores letter case",
]


def check(text: str) -> int:
    problems = 0
    missing_kw = [k.strip() for k in KEYWORDS if k not in text]
    print(f"Shape:    missing keywords: {', '.join(missing_kw) or 'none'}")
    problems += bool(missing_kw)
    first = text.strip().splitlines()[0] if text.strip() else ""
    prose = not first.startswith(("Feature:", "@", "#"))
    print(f"Shape:    {'FAIL' if prose else 'OK  '}  starts with Feature (no prose before it)")
    problems += prose
    outline = "Scenario Outline:" in text and "Examples:" in text
    print(f"Shape:    {'OK  ' if outline else 'FAIL'}  Scenario Outline with Examples used")
    problems += not outline
    third_person = any(p in text for p in ("the user ", "the shopper ", "the customer "))
    print(f"Style:    {'FAIL' if third_person else 'OK  '}  first person steps (no 'the user ...')")
    problems += third_person
    for value in REQUIRED_VALUES:
        ok = value in text
        print(f"Content:  {'OK  ' if ok else 'FAIL'}  {value!r} present")
        problems += not ok
    leaked = [m for m in LEAK_MARKERS if m in text]
    print(f"Leakage:  {('copied from examples: ' + ', '.join(leaked)) if leaked else 'none'}")
    problems += bool(leaked)
    if len(REQUIRED_VALUES) < 6 or len(LEAK_MARKERS) < 3:
        print("CHECK     fill REQUIRED_VALUES (6+) and LEAK_MARKERS (3+) before trusting this result")
    print("Reminder: shape OK is not content OK. Check every rule and value yourself.")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(check(Path(sys.argv[1]).read_text(encoding="utf-8")))
