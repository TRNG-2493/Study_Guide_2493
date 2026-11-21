# rr/validation.py
"""Output validation: parse -> schema (S1) -> rules R1-R7 -> warnings Q1-Q2 -> verdict.

Lesson: written/5-friday/agent-output-validation.md, section 5.
Rule catalogue: agent/rules.md (Thursday). Every Code rule there is one function here.
Design decisions: stop after a shape failure (R rules need a valid shape); after that,
run every rule and collect every finding; warnings never fail a reply on their own.
"""
import re
from dataclasses import dataclass, field

from rr.contract import ContractError, check_output_schema, parse_reply

ERROR, WARNING = "error", "warning"
NUMBER_WITH_UNIT = re.compile(
    r"\$\d+(?:\.\d+)?|\b\d+(?:\.\d+)?\s*(?:seconds?|secs?|ms|minutes?|hours?|days?|weeks?|%|percent|characters?|digits?)\b",
    re.IGNORECASE)


@dataclass
class Finding:
    rule: str
    severity: str
    where: str
    message: str


@dataclass
class ValidationReport:
    story_id: str
    findings: list = field(default_factory=list)
    stopped_at: str = ""                     # "parse" or "output" when validation could not go deeper

    @property
    def errors(self) -> list:
        return [f for f in self.findings if f.severity == ERROR]

    @property
    def warnings(self) -> list:
        return [f for f in self.findings if f.severity == WARNING]

    @property
    def verdict(self) -> str:
        if self.errors:
            return "FAIL"
        return "PASS_WITH_WARNINGS" if self.warnings else "PASS"


def norm(text: str) -> str:
    """Case-insensitive, whitespace collapsed, curly quotes made straight (catalogue R3)."""
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return " ".join(text.lower().split())


def check_r1(story: dict, out: dict) -> list:
    if out["story_id"] != story["story_id"]:
        return [Finding("R1", ERROR, "story_id", f"expected '{story['story_id']}' (from input), got '{out['story_id']}'")]
    return []


def check_r2(story: dict, out: dict) -> list:
    known = [ac["id"] for ac in story["acceptance_criteria"]]
    return [Finding("R2", ERROR, f"findings[{i}].ac_id",
                    f"'{f['ac_id']}' is not an acceptance criterion of {story['story_id']} (expected one of {known})")
            for i, f in enumerate(out["findings"]) if f["ac_id"] not in known]


def check_r3(story: dict, out: dict) -> list:
    texts = {ac["id"]: norm(ac["text"]) for ac in story["acceptance_criteria"]}
    found = []
    for i, f in enumerate(out["findings"]):
        if f["ac_id"] in texts and norm(f["quote"]) not in texts[f["ac_id"]]:
            elsewhere = [a for a, t in texts.items() if norm(f["quote"]) in t]
            hint = f" (it is in {elsewhere[0]})" if elsewhere else " (it is not in the story at all)"
            found.append(Finding("R3", ERROR, f"findings[{i}].quote",
                                 f"quote '{f['quote']}' is not in the text of {f['ac_id']}{hint}"))
    return found


def check_r4(story: dict, out: dict) -> list:
    number = story["story_id"].split("-")[1]
    found, seen = [], set()
    for i, f in enumerate(out["findings"]):
        expected = f"F-{number}-{i + 1:02d}"
        if f["id"] in seen:
            found.append(Finding("R4", ERROR, f"findings[{i}].id", f"'{f['id']}' is used more than once"))
        elif f["id"].split("-")[1] != number:
            found.append(Finding("R4", ERROR, f"findings[{i}].id",
                                 f"'{f['id']}' should start with 'F-{number}-' because the story is {story['story_id']}"))
        elif f["id"] != expected:
            found.append(Finding("R4", ERROR, f"findings[{i}].id", f"'{f['id']}' breaks the sequence; expected '{expected}'"))
        seen.add(f["id"])
    return found


def check_r5(story: dict, out: dict) -> list:
    limit, count = story.get("max_findings", 10), len(out["findings"])
    if count > limit:
        return [Finding("R5", ERROR, "findings", f"{count} findings returned, max_findings is {limit}")]
    return []


def check_r6(story: dict, out: dict) -> list:
    if out["status"] == "needs_clarification":
        found = []
        if out["findings"]:
            found.append(Finding("R6", ERROR, "findings", "status is 'needs_clarification' but findings is not empty"))
        if not out["open_questions"]:
            found.append(Finding("R6", ERROR, "open_questions", "status is 'needs_clarification' but open_questions is empty"))
        return found
    if out["open_questions"]:
        return [Finding("R6", ERROR, "open_questions", "status is 'ok' but open_questions is not empty")]
    return []


def check_r7(story: dict, out: dict) -> list:
    focus = story.get("focus", [])
    return [Finding("R7", ERROR, f"findings[{i}].category", f"category '{f['category']}' is not in focus {focus}")
            for i, f in enumerate(out["findings"]) if f["category"] not in focus]


def check_q1(story: dict, out: dict) -> list:
    story_text = norm(" ".join(ac["text"] for ac in story["acceptance_criteria"]) + " " + story["title"])
    found = []
    for i, f in enumerate(out["findings"]):
        for m in NUMBER_WITH_UNIT.finditer(f["question"] + " " + f["explanation"]):
            if norm(m.group(0)) not in story_text:
                found.append(Finding("Q1", WARNING, f"findings[{i}]",
                                     f"'{m.group(0)}' is not in the story: is the agent proposing an answer?"))
                break
    return found


def check_q2(story: dict, out: dict) -> list:
    found, seen = [], {}
    for i, f in enumerate(out["findings"]):
        key = (f["ac_id"], norm(f["quote"]))
        if key in seen:
            found.append(Finding("Q2", WARNING, f"findings[{i}]", f"same ac_id and quote as findings[{seen[key]}]: duplicate?"))
        else:
            seen[key] = i
    return found


RULES = [check_r1, check_r2, check_r3, check_r4, check_r5, check_r6, check_r7, check_q1, check_q2]


def validate_reply(story: dict, reply: str) -> ValidationReport:
    """Validate one raw reply against one GATED input story (defaults already applied)."""
    report = ValidationReport(story_id=story["story_id"])
    try:
        out = check_output_schema(parse_reply(reply))
    except ContractError as exc:
        for msg in exc.errors:
            where = "(reply)" if exc.stage == "parse" else msg.split(":")[0]
            report.findings.append(Finding("S1", ERROR, where, msg))
        report.stopped_at = exc.stage
        return report
    for rule in RULES:
        report.findings.extend(rule(story, out))
    return report
