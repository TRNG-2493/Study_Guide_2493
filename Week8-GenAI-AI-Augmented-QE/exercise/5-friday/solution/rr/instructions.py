# rr/instructions.py
"""Load a versioned instruction file and check it before the agent uses it.

Lesson: written/5-friday/building-agent-instructions.md, section 12.
"""
import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SECTIONS = [
    "Role and Goal", "Scope", "Inputs", "Process", "Rules", "Output",
    "Uncertainty and Escalation", "Boundaries", "Style",
]
HEADER = re.compile(
    r"^Version: (?P<version>\d+\.\d+\.\d+) \| "
    r"Output contract: (?P<contract>\d+\.\d+\.\d+) \| Owner: (?P<owner>.+)$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Instructions:
    path: str
    version: str
    contract_version: str
    owner: str
    text: str
    sections: dict          # heading -> body text


def split_sections(text: str) -> dict:
    """Return {heading: body} for every '## Heading' in the file."""
    parts = re.split(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    # parts = [preamble, heading1, body1, heading2, body2, ...]
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}


def load_instructions(path: str, expected_contract: str) -> Instructions:
    """Read the file, parse its header, and refuse to load a broken or mismatched file."""
    text = Path(path).read_text(encoding="utf-8")
    header = HEADER.search(text)
    if header is None:
        raise ValueError(f"{path}: header line 'Version: x.y.z | Output contract: x.y.z | Owner: ...' not found")
    sections = split_sections(text)
    missing = [s for s in REQUIRED_SECTIONS if not sections.get(s)]
    if missing:
        raise ValueError(f"{path}: missing or empty sections: {missing}")
    if header["contract"] != expected_contract:
        raise ValueError(
            f"{path}: written for output contract {header['contract']}, "
            f"but the agent uses contract {expected_contract}"
        )
    return Instructions(str(path), header["version"], header["contract"],
                        header["owner"].strip(), text, sections)


if __name__ == "__main__":
    ins = load_instructions("instructions/rr_instructions_v1.0.0.md", expected_contract="1.0.0")
    print(f"loaded {ins.path}")
    print(f"version {ins.version}, contract {ins.contract_version}, owner {ins.owner}")
    for name, body in ins.sections.items():
        print(f"  {name:<28} {len(body.splitlines()):>2} lines")
