# check_rule_map.py
"""Check that every instruction rule is mapped to a check, and that the map still matches the file.

Lesson: written/5-friday/building-agent-instructions.md, section 13.
Usage:  python check_rule_map.py INSTRUCTIONS.md RULE_MAP.json      (exit 0 = no problems, 1 = problems)
"""
import json
import sys
from pathlib import Path

from rr.instructions import split_sections

KNOWN_CHECKS = {"S1", "S2", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "Q1", "Q2", "Q3", "HUMAN"}
BULLET_SECTIONS = ["Rules", "Output", "Uncertainty and Escalation", "Boundaries"]   # every bullet here needs an entry


def bullets(body: str) -> list[str]:
    """Split a section body into bullets; a bullet's continuation lines are joined to it."""
    items = []
    for line in body.splitlines():
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif items and line.strip():
            items[-1] += " " + line.strip()
    return items


def flat(text: str) -> str:
    """Collapse all runs of whitespace (including line breaks) to one space."""
    return " ".join(text.split())


def check(instructions_path: str, map_path: str) -> int:
    text = Path(instructions_path).read_text(encoding="utf-8")
    sections = split_sections(text)
    entries = json.loads(Path(map_path).read_text(encoding="utf-8"))["entries"]
    problems = 0

    for e in entries:                                       # 1. map -> file
        body = flat(sections.get(e["section"], ""))
        if flat(e["phrase"]) not in body:
            print(f"DRIFT     [{e['section']}] phrase not found: \"{flat(e['phrase'])}\"")
            problems += 1
        unknown = set(e["checks"]) - KNOWN_CHECKS
        if unknown:
            print(f"BAD ID    [{e['section']}] unknown check IDs {sorted(unknown)}")
            problems += 1
        if not e["checks"]:
            print(f"NO CHECK  [{e['section']}] \"{flat(e['phrase'])}\" is verified by nothing")
            problems += 1

    for name in BULLET_SECTIONS:                            # 2. file -> map
        for b in bullets(sections.get(name, "")):
            if not any(e["section"] == name and flat(e["phrase"]) in b for e in entries):
                print(f"UNMAPPED  [{name}] \"{b[:60]}...\"")
                problems += 1

    print(f"{len(entries)} map entries, {problems} problem(s)")
    return problems


if __name__ == "__main__":
    sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
