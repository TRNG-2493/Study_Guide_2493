"""design_parts.py - generic helpers to check an agent DESIGN (no model calls).

Adapted from the Thursday demo's agent_parts.py so it works on YOUR agent folder:
    agent/instructions.md            nine sections + version header
    agent/templates/<one file>.txt   the user-message template ($placeholders)
    agent/schemas/*input*.schema.json and *output*.schema.json   (Draft 2020-12)
    agent/rules.md                   rule catalogue
    agent/samples/*.json             sample input/output pairs
    agent/manifest.json              anatomy manifest + 12 design questions
    agent/CHANGELOG.md
Do not edit. If a check is wrong for your design, explain it in RETRO.md.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from string import Template

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit('jsonschema is too old or missing. Fix: pip install "jsonschema>=4.18"')

HERE = Path(__file__).parent
AGENT = HERE / "agent"
INSTRUCTIONS = AGENT / "instructions.md"
MANIFEST = AGENT / "manifest.json"
RULES = AGENT / "rules.md"
SAMPLES = AGENT / "samples"
CHANGELOG = AGENT / "CHANGELOG.md"

REQUIRED_SECTIONS = ["Role and Goal", "Scope", "Inputs", "Process", "Rules", "Output",
                     "Uncertainty and Escalation", "Boundaries", "Style"]
WEAK_WORDS = ["good", "nice", "appropriate", "reasonable", "important", "thorough", "properly",
              "user-friendly", "fast", "etc", "as needed", "some"]
DANGER = ["make reasonable assumptions", "assume", "use your best judgement", "fill in any gaps"]
REQUIRED_CATEGORIES = ["happy_path", "edge", "clarification", "invalid_input", "out_of_scope"]
LEFTOVER = re.compile(r"\$[A-Za-z_]\w*|\$\{[A-Za-z_]\w*\}")


def read(path) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_json(path):
    return json.loads(read(path))


def one(pattern: str, folder: Path) -> Path:
    hits = sorted(folder.glob(pattern))
    if len(hits) != 1:
        raise FileNotFoundError(f"expected exactly one {folder.name}/{pattern}, found {[h.name for h in hits]}")
    return hits[0]


def template_path() -> Path:
    return one("*.txt", AGENT / "templates")


def input_schema_path() -> Path:
    return one("*input*.schema.json", AGENT / "schemas")


def output_schema_path() -> Path:
    return one("*output*.schema.json", AGENT / "schemas")


# ------------------------------------------------------------ instructions
def headings(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", text, re.MULTILINE)]


def weak_words(text: str) -> list[tuple[int, str]]:
    return [(n, w) for n, line in enumerate(text.splitlines(), 1) for w in WEAK_WORDS
            if re.search(rf"\b{re.escape(w)}\b", line, re.IGNORECASE)]


def danger_lines(text: str) -> list[tuple[int, str]]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for phrase in DANGER:
            if re.search(rf"\b{re.escape(phrase)}\b", line, re.IGNORECASE):
                out.append((n, phrase))
                break
    return out


def instruction_header(text: str) -> dict:
    m = re.search(r"Version:\s*([\d.]+)\s*\|\s*Output contract:\s*([\d.]+)\s*\|\s*Owner:\s*(.+)", text)
    return {"version": m.group(1), "contract": m.group(2), "owner": m.group(3).strip()} if m else {}


def todo_markers(folder: Path = AGENT) -> list[str]:
    hits = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".txt", ".json"):
            for n, line in enumerate(read(p).splitlines(), 1):
                if "TODO" in line:
                    hits.append(f"{p.relative_to(HERE).as_posix()}:{n}")
    return hits


# ------------------------------------------------------------- template
def placeholders(text: str) -> list[str]:
    names = []
    for m in Template.pattern.finditer(text):
        name = m.group("named") or m.group("braced")
        if name and name not in names:
            names.append(name)
    return names


def format_value(value) -> str:
    """Lists of {id, text} become bullet lines; lists of strings a comma list. Logic lives in code."""
    if isinstance(value, list):
        if value and all(isinstance(v, dict) and {"id", "text"} <= set(v) for v in value):
            return "\n".join(f"- {v['id']}: {str(v['text']).strip()}" for v in value)
        return ", ".join(str(v) for v in value) if value else "none"
    return str(value).strip()


def render(story: dict) -> str:
    """Fill the template ONCE. Missing values use the input schema 'default'; else fail loudly."""
    text = read(template_path())
    props = load_json(input_schema_path()).get("properties", {})
    values = {}
    for name in placeholders(text):
        if name in story:
            values[name] = format_value(story[name])
        elif "default" in props.get(name, {}):
            values[name] = format_value(props[name]["default"])
    return Template(text).substitute(values)


def messages(story: dict, instructions: Path = INSTRUCTIONS) -> list[dict]:
    return [{"role": "system", "content": read(instructions)}, {"role": "user", "content": render(story)}]


# ------------------------------------------------------------- contracts
def validator(schema_path: Path) -> Draft202012Validator:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def where(error) -> str:
    return "/".join(str(p) for p in error.absolute_path) or "(root)"


def errors(schema_path: Path, instance) -> list:
    key = lambda e: [(0, p) if isinstance(p, int) else (1, str(p)) for p in e.absolute_path]
    return sorted(validator(schema_path).iter_errors(instance), key=key)


def check_input(obj) -> list:
    return errors(input_schema_path(), obj)


def check_output(obj) -> list:
    return errors(output_schema_path(), obj)


def output_contract_facts() -> dict:
    """What the design rules expect of every output contract (input-output-contracts.md, section 8)."""
    s = load_json(output_schema_path())
    props = s.get("properties", {})
    return {
        "contract_version const": "const" in props.get("contract_version", {}),
        "status enum has needs_clarification": "needs_clarification" in props.get("status", {}).get("enum", []),
        "open_questions required": "open_questions" in s.get("required", []),
        "additionalProperties false at root": s.get("additionalProperties") is False,
        "$id ends with a version": bool(re.search(r"/\d+\.\d+\.\d+$", s.get("$id", ""))),
    }


def parse_reply(text: str):
    try:
        return json.loads(text), "pure JSON (Output rule kept)"
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else (text[text.index("{"): text.rindex("}") + 1]
                                                if "{" in text and "}" in text else None)
    if candidate is not None:
        try:
            return json.loads(candidate), "NOT pure JSON - Output rule broken (prose or fence around it)"
        except json.JSONDecodeError:
            pass
    return None, "PARSE FAIL - no JSON object could be read"


# --------------------------------------------------------------- versions
def version_rows() -> list[tuple[str, str]]:
    out_schema = load_json(output_schema_path())
    rows = [("manifest agent.contract_version", load_json(MANIFEST)["agent"].get("contract_version", "NONE"))]
    rows.append(("instructions.md 'Output contract:'", instruction_header(read(INSTRUCTIONS)).get("contract", "NONE")))
    tpl = template_path()
    m = re.search(r'contract_version "([\d.]+)"', read(tpl))
    rows.append(("template reminder contract_version", m.group(1) if m else "NONE"))
    m = re.search(r"_v([\d.]+)\.txt$", tpl.name)
    rows.append(("template file name", m.group(1) if m else "NONE"))
    for label, path in (("input schema $id", input_schema_path()), ("output schema $id", output_schema_path())):
        rows.append((label, load_json(path).get("$id", "").rsplit("/", 1)[-1] or "NONE"))
    rows.append(("output schema contract_version const",
                 str(out_schema.get("properties", {}).get("contract_version", {}).get("const", "NONE"))))
    for p in sorted(SAMPLES.glob("*.json")):
        rows.append((f"samples/{p.name}", load_json(p).get("contract_version", "NONE")))
    m = re.search(r"^## ([\d.]+)", read(CHANGELOG), re.MULTILINE)
    rows.append(("CHANGELOG latest entry", m.group(1) if m else "NONE"))
    return rows
