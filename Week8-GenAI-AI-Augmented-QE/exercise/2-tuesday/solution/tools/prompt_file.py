"""prompt_file.py - read the prompt text out of a prompt-library file. Do not edit.

A prompt-library file has a header (Purpose, Version, ...) and a section
"## Prompt" followed by one ```text block. That block is what you paste into Claude.
"""
import re
import sys
from pathlib import Path

REQUIRED_HEADER_FIELDS = ["Purpose:", "Version:", "Tested with:", "Technique:",
                          "Acceptance criteria:", "Check with:", "Changes from previous:"]


def read_prompt(path: str | Path) -> str:
    text = Path(path).read_text(encoding="utf-8")
    match = re.search(r"## Prompt\s+```text\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: no '## Prompt' section with a ```text block")
    return match.group(1).strip()


def missing_header_fields(path: str | Path) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    header = text.split("## Prompt")[0]
    return [f for f in REQUIRED_HEADER_FIELDS
            if not re.search(re.escape(f) + r"[ \t]*\S", header)]


if __name__ == "__main__":
    print(read_prompt(sys.argv[1]))
