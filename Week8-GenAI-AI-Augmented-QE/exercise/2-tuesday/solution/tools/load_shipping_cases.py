"""load_shipping_cases.py - Stage 3: turn a format-locked Claude reply into trusted pytest data.

Same pipeline as the demo's load_cases.py:
    extract_json -> parse_reply -> validate_cases -> build_reask_message -> to_params
Rule from format-locking.md: tolerate WRAPPING (fences, chatter), reject BROKEN CONTENT.
Never "repair" a reply silently.

Usage:
    python tools/load_shipping_cases.py evidence/<reply>.txt            # check a reply
    python tools/load_shipping_cases.py evidence/<reply>.txt --reask    # also print the re-ask message

What to do: write the contract in your format-locked prompt FIRST, then make validate_cases()
enforce exactly that contract. The constants below are a suggested contract; if your prompt
uses different keys or values, change the constants to match your prompt (and say so in its header).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_KEYS = ["id", "title", "subtotal", "country", "express", "expected", "technique"]
TECHNIQUES = {"BVA", "EP", "error_guessing"}
ID_PATTERN = re.compile(r"^SC-\d{2}$")


def extract_json(text: str) -> str:
    """Tolerate harmless wrapping: code fences and chatty text around the array."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        text = text[start:end + 1]
    return text


def parse_reply(text: str) -> list:
    """Syntax check. Raises json.JSONDecodeError with line and column on broken content."""
    data = json.loads(extract_json(text))
    if not isinstance(data, list):
        raise ValueError("Top level must be a JSON array")
    return data


def validate_cases(cases: list) -> list[str]:
    """Structure check: drift that PARSES but is still wrong. Return one message per problem.

    TODO: implement. At minimum report, naming the case id in every message:
      - an element that is not an object
      - missing keys and unexpected keys
      - an id that does not match ID_PATTERN, and duplicate ids
      - subtotal that is not a number (watch out: bool is a subclass of int in Python)
      - express that is not a real JSON boolean (the string "true" is drift)
      - expected that is neither a number nor exactly the string "ValueError"
      - technique not in TECHNIQUES
      - country that is not a string (invalid codes such as "GB" ARE allowed as test input)
    """
    problems: list[str] = []
    seen_ids: set = set()
    for n, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            problems.append(f"element {n}: is not an object")
            continue
        label = case.get("id", f"element {n}")
        missing = [k for k in REQUIRED_KEYS if k not in case]
        extra = [k for k in case if k not in REQUIRED_KEYS]
        if missing:
            problems.append(f"{label}: missing key(s) {missing}")
        if extra:
            problems.append(f"{label}: unexpected key(s) {extra}")
        if "id" in case:
            if not ID_PATTERN.match(str(case["id"])):
                problems.append(f"{label}: id must look like SC-01")
            if case["id"] in seen_ids:
                problems.append(f"{label}: duplicate id")
            seen_ids.add(case["id"])
        if "subtotal" in case and (isinstance(case["subtotal"], bool)
                                   or not isinstance(case["subtotal"], (int, float))):
            problems.append(f"{label}: subtotal must be a number, got {case['subtotal']!r}")
        if "country" in case and not isinstance(case["country"], str):
            problems.append(f"{label}: country must be a string, got {case['country']!r}")
        if "express" in case and not isinstance(case["express"], bool):
            problems.append(f"{label}: express must be true or false, got {case['express']!r}")
        if "expected" in case:
            exp = case["expected"]
            if exp != "ValueError" and (isinstance(exp, bool) or not isinstance(exp, (int, float))):
                problems.append(f'{label}: expected must be a number or "ValueError", got {exp!r}')
        if "technique" in case and case["technique"] not in TECHNIQUES:
            problems.append(f"{label}: technique {case['technique']!r} not in {sorted(TECHNIQUES)}")
    return problems


def build_reask_message(problems: list[str]) -> str:
    """Re-ask ONCE with the exact errors (format-locking.md, section 7). Then stop and fail loudly."""
    lines = ["Your previous reply did not follow the output format. Problems found:"]
    lines += [f"- {p}" for p in problems]
    lines.append("Reply again with ONLY the corrected JSON array. "
                 "No code fences, no explanation, no trailing commas. Keep every other value unchanged.")
    return "\n".join(lines)


def load_cases(path: str | Path) -> list[dict]:
    """Used by tests/test_shipping_generated.py at collection time."""
    cases = parse_reply(Path(path).read_text(encoding="utf-8"))
    problems = validate_cases(cases)
    if problems:
        raise ValueError(f"{path}: reply breaks the contract:\n  " + "\n  ".join(problems))
    return cases


def to_params(cases: list[dict]):
    rows = [(c["subtotal"], c["country"], c["express"], c["expected"]) for c in cases]
    return rows, [c["id"] for c in cases]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    path, reask = argv[0], "--reask" in argv
    raw = Path(path).read_text(encoding="utf-8")
    print(f"File: {path}")
    print(f"Wrapping found (fences or chatter): {'no' if raw.strip().startswith('[') else 'yes, tolerated'}")
    try:
        cases = parse_reply(raw)
    except (json.JSONDecodeError, ValueError) as err:
        msg = f"{err.msg} (line {err.lineno}, column {err.colno})" if isinstance(err, json.JSONDecodeError) else str(err)
        print(f"SYNTAX FAIL: {msg}")
        if reask:
            print("\n--- paste this back to Claude, in the SAME chat (once) ---")
            print(build_reask_message([f"not valid JSON: {msg}"]))
        return 1
    print(f"Syntax: OK, {len(cases)} element(s)")
    problems = validate_cases(cases)
    if not problems:
        print("Structure: OK, every case matches the contract")
        print(f"Next: python -m pytest -v tests/test_shipping_generated.py --cases {path}")
        return 0
    print(f"STRUCTURE FAIL: {len(problems)} problem(s)")
    for p in problems:
        print(f"  - {p}")
    if reask:
        print("\n--- paste this back to Claude, in the SAME chat (once) ---")
        print(build_reask_message(problems))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
