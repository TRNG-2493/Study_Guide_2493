"""score_reply.py - Stage 1: YOUR acceptance criteria for a shipping test-ideas reply, as code.

Write the criteria BEFORE you send any prompt (prompt-engineering-principles.md, section 7).
Each criterion is one small, crude check: a first filter, not proof. Human review still decides.
The demo's `prompt_lab.py score` shows the style: substring, number and regex checks.

Usage:
    python tools/score_reply.py evidence/calibration/reply_good.txt   # must score full marks
    python tools/score_reply.py evidence/calibration/reply_bad.txt    # must score 2 or less
    python tools/score_reply.py evidence/shipping-test-ideas.v1.run1.txt

What to do:
1. Read shopfront/shipping.py (the six numbered requirement sentences).
2. Replace the TODO in criteria() with AT LEAST 8 criteria. Cover, at minimum:
   - it is about OUR feature
   - the 74.99 / 75.00 / 75.01 boundary values
   - express on a free-shipping order (expected 10.00)
   - Canada and an unsupported country
   - a negative test (ValueError)
   - exact expected values
   - an automatable table with 5+ rows
   - no invented rules (list the words that would signal one in INVENTED_RULES)
   - assumptions listed
3. Calibrate: good reply = full marks, bad reply = 2 or less. Fix the CHECK, not the reply.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Words that signal a rule nobody gave the model. Add your own after reading shipping.py.
# Example entry: "case-insensitive country": r"case[- ]insensitive"
INVENTED_RULES: dict[str, str] = {
    "case-insensitive country": r"case[- ]insensitive",
    "once per customer / limits": r"once per|per customer|per month",
    "PO boxes / address rules": r"po box|p\.o\. box",
    "delivery speed promises": r"\bfaster\b|business days|next[- ]day",
}


def numbers_in(text: str) -> set[float]:
    return {float(n) for n in re.findall(r"(?<![\d.])\d+\.\d+|\b\d+\b", text)}


def table_rows(text: str) -> int:
    """Markdown table rows, not counting the header and the |---| separator."""
    rows = [line for line in text.splitlines() if line.strip().startswith("|")]
    return max(0, len(rows) - 2)


def invented_rules(text: str) -> list[str]:
    return [name for name, pattern in INVENTED_RULES.items() if re.search(pattern, text, re.IGNORECASE)]


def criteria(reply: str) -> dict[str, bool]:
    """Return {criterion name: passed?}. One line per criterion keeps it readable."""
    nums = numbers_in(reply)
    low = reply.lower()
    return {
        "about OUR feature (US and CA, $75.00)": bool(re.search(r"\bUS\b", reply) and re.search(r"\bCA\b", reply)) and 75.0 in nums,
        "boundary 74.99": 74.99 in nums,
        "boundary 75.00": "75.00" in reply,
        "boundary 75.01": 75.01 in nums,
        "express on a free order costs 10.00": "10.00" in reply and "express" in low,
        "Canada flat rate 12.00": "12.00" in reply,
        "unsupported country raises ValueError": "valueerror" in low and re.search(r"\b(GB|UK|DE|FR|MX|XX)\b", reply) is not None,
        "negative subtotal raises ValueError": re.search(r"-\d+\.\d{2}", reply) is not None,
        "exact expected values (5.99 present)": 5.99 in nums,
        "automatable table (5+ rows)": table_rows(reply) >= 5,
        "no invented rules": not invented_rules(reply),
        "assumptions listed": re.search(r"assum|question", low) is not None,
    }


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__)
        return 2
    for path in paths:
        reply = Path(path).read_text(encoding="utf-8")
        results = criteria(reply)
        passed = sum(results.values())
        print(f"{path}: {passed}/{len(results)} acceptance criteria met")
        for name, ok in results.items():
            if not ok:
                print(f"    FAIL  {name}")
        found = invented_rules(reply)
        if found:
            print(f"    INVENTED: {', '.join(found)}")
        if len(results) < 8:
            print(f"    CHECK  only {len(results)} criteria defined; the exercise asks for at least 8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
