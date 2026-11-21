"""responsible.py - Stage 6: responsible use before and after the prompt (adapted from the demo).

    redact          replace secrets and personal data with numbered placeholders
    preflight       policy as data: may THIS text go to THIS tool? (allow-list)
    usage_record    one row for the team's AI usage log
    disclosure      the header line for AI-assisted files

Lesson: written/3-wednesday/responsible-use-of-ai-in-qe.md
        sections 3.2 (redactor), 3.3 (limits), 4 (pre-flight), 8 (disclosure), 13 (usage log).
The redaction rules are the same as in the lesson, with ONE gap for you to close:
gift card codes are bearer value (whoever has the code can spend the balance), and
none of the rules below catches them. Stage 6 TODO: add a GIFT_CARD rule and add it
to SECRET_LABELS. Put it BEFORE the CARD and PHONE rules (order matters).
"""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

RULES = [
    # TODO Stage 6: ("GIFT_CARD", re.compile(r"...")),
    ("API_KEY", re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{8,}\b")),
    ("AWS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("BEARER", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("PASSWORD", re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+")),
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("CARD", re.compile(r"\b\d(?:[ -]?\d){12,18}\b")),
    ("PHONE", re.compile(r"\(?\b\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b")),
]

APPROVED_TOOLS = {                      # example team policy, written as data
    "public-chatbot": {"public"},
    "claude": {"public", "internal"},       # the organisation-approved assistant for this course
}
SECRET_LABELS = {"API_KEY", "AWS_KEY", "BEARER", "PASSWORD"}


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for label, pattern in RULES:
        def _replace(m: re.Match, label: str = label) -> str:
            counts[label] = counts.get(label, 0) + 1
            if label == "PASSWORD":
                return f"{m.group(1)}=<{label}_{counts[label]}>"
            return f"<{label}_{counts[label]}>"
        text = pattern.sub(_replace, text)
    return text, counts


def preflight(text: str, tool: str, classification: str) -> tuple[bool, str, list[str]]:
    """(allowed, text_to_send, reasons). Unknown tools are denied (allow-list)."""
    if classification == "restricted":
        return False, "", ["Restricted data never goes into an AI tool."]
    if classification not in APPROVED_TOOLS.get(tool, set()):
        return False, "", [f"'{tool}' is not approved for {classification} data."]
    clean, found = redact(text)
    reasons = []
    secrets = SECRET_LABELS & found.keys()
    if secrets:
        reasons.append(f"Secrets were present ({', '.join(sorted(secrets))}): rotate them today.")
    if found:
        reasons.append(f"Redacted before sending: {found}")
    reasons.append("Now READ the redacted text yourself: names, addresses and ids are not caught.")
    return True, clean, reasons


USAGE_COLUMNS = ["date", "who", "tool", "purpose", "data_class", "redacted",
                 "artifact", "reviewed_by", "outcome"]


def append_usage(path: str | Path, **row: str) -> None:
    p = Path(path)
    new = not p.exists()
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=USAGE_COLUMNS)
        if new:
            w.writeheader()
        w.writerow({"date": date.today().isoformat(), **row})


def disclosure(tool: str, reviewer: str, day: str | None = None, what: str = "cases") -> str:
    return f"# AI-assisted: {tool} drafted {what}; reviewed by {reviewer} {day or date.today().isoformat()}"
