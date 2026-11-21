# rr/validation.py
"""Output validation: parse -> schema (S1) -> rules R1-R7 -> warnings Q1-Q2 -> verdict.

Stage 3: implement every check_* function from agent/rules.md. validate_reply(), the report and
the verdict are provided: read them first, they decide when your rules run.

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
    """R1: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r2(story: dict, out: dict) -> list:
    """R2: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r3(story: dict, out: dict) -> list:
    """R3: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r4(story: dict, out: dict) -> list:
    """R4: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r5(story: dict, out: dict) -> list:
    """R5: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r6(story: dict, out: dict) -> list:
    """R6: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_r7(story: dict, out: dict) -> list:
    """R7: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_q1(story: dict, out: dict) -> list:
    """Q1: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


def check_q2(story: dict, out: dict) -> list:
    """Q2: see agent/rules.md. Return a list of Finding (empty list = rule passes)."""
    return []   # TODO Stage 3


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
