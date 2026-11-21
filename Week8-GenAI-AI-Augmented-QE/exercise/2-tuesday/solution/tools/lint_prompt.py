"""lint_prompt.py - check a prompt-library file's INPUT for the dimensions of specificity.

Same idea as the linter in written/2-tuesday/specificity-and-context.md section 9.2 and
`prompt_lab.py lint` in the demo. Keyword-based: it is a spell-checker, not a reviewer.
"do not use a table" passes the "output format" check. A high lint score means the
prompt MENTIONS the right things, not that it is good. Measure the OUTPUT with score_reply.py.

Usage:
    python tools/lint_prompt.py prompts/test-design/shipping-test-ideas.v1.md
    python tools/lint_prompt.py prompts/**/*.md        (several files)
Do not edit.
"""
import re
import sys

from prompt_file import missing_header_fields, read_prompt

LINT_CHECKS = {
    "task verb": r"\b(design|write|list|generate|review|identify|create|explain|convert|classify|analyse|analyze)\b",
    "technique": r"boundary|equivalence|decision table|state transition|error guessing|negative|hypothes",
    "quantity": r"\b\d+\s+(to\s+\d+\s+)?(test|idea|case|scenario|cause|hypothes\w*)s?\b|\b(three|five|eight|ten)\b",
    "output format": r"table|json|gherkin|bullet|csv|columns|numbered",
    "audience": r"audience|for (a|the) (junior|senior|qa|developer|manager)|qa engineers|engineers who",
    "context block": r"<\w+>|\"\"\"|###|^## ",
    "constraints": r"\bdo not\b|\bonly\b|\bavoid\b|\bmust\b",
    "done-criteria": r"done when|at least one|every .* (has|is) ",
    "gaps surfaced": r"assumption|clarifying question|open question|questions",
}


def lint(prompt: str) -> list[str]:
    return [name for name, pattern in LINT_CHECKS.items()
            if not re.search(pattern, prompt, re.IGNORECASE | re.MULTILINE)]


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__)
        return 2
    worst = 0
    for path in paths:
        try:
            prompt = read_prompt(path)
        except ValueError as err:
            print(f"ERROR {err}")
            worst = 1
            continue
        missing = lint(prompt)
        header = missing_header_fields(path)
        found = len(LINT_CHECKS) - len(missing)
        print(f"{path}: {found}/{len(LINT_CHECKS)}  missing: {', '.join(missing) or 'nothing'}")
        if header:
            print(f"    HEADER missing or empty: {', '.join(header)}")
            worst = 1
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
