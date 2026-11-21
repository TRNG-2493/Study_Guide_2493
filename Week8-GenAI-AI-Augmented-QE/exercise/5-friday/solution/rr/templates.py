# rr/templates.py
"""Render the pinned user-message template. Same rules as Thursday's design_parts.render:
fill ONCE with substitute(); lists become text in code; missing values fail loudly.
Defaults are NOT applied here: the input gate (rr/contract.py) applies them once.
Provided complete. Lesson: written/5-friday/creating-reusable-prompt-templates.md.
"""
import re
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
LEFTOVER = re.compile(r"\$[A-Za-z_]\w*|\$\{[A-Za-z_]\w*\}")


def template_path(name: str, version: str) -> Path:
    path = ROOT / "agent" / "templates" / f"{name}_v{version}.txt"
    if not path.exists():
        raise KeyError(f"{name}@{version}")
    return path


def placeholders(text: str) -> list:
    names = []
    for m in Template.pattern.finditer(text):
        name = m.group("named") or m.group("braced")
        if name and name not in names:
            names.append(name)
    return names


def format_value(value) -> str:
    if isinstance(value, list):
        if value and all(isinstance(v, dict) and {"id", "text"} <= set(v) for v in value):
            return "\n".join(f"- {v['id']}: {str(v['text']).strip()}" for v in value)
        return ", ".join(str(v) for v in value)
    return str(value).strip()


def render(name: str, version: str, story: dict) -> str:
    """Strict in both directions: every placeholder needs a value; no leftovers allowed."""
    text = template_path(name, version).read_text(encoding="utf-8")
    values = {n: format_value(story[n]) for n in placeholders(text) if n in story}
    rendered = Template(text).substitute(values)          # KeyError on a missing value
    return rendered
