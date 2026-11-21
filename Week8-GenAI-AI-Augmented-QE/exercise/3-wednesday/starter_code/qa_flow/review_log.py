"""review_log.py - Stage 4: human decisions, correction log, sign-off (adapted from the demo). Do not edit.

    load_decisions     read the reviewer's decision file (review_decisions.json)
    validate_review    the sign-off GATE: every AI item decided, reasons and evidence present
    apply_decisions    build the approved suite (drop rejected, patch edited, append added)
    write_correction_log  correction_log.csv, one row per human decision
    review_metrics     acceptance / edit / rejection rates and prompt feedback

The checklist IDs C1..C9 are the ones in review_checklist.md and in
written/3-wednesday/human-validation-of-ai-output.md, section 4.
Correction categories: same lesson, section 9 (plus MISSING_COVERAGE for added cases).
"""
from __future__ import annotations

import copy
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

DECISIONS = {"ACCEPTED", "EDITED", "REJECTED", "ADDED"}
CATEGORIES = {"WRONG_EXPECTED", "INVENTED_REQUIREMENT", "WRONG_TRACE", "DUPLICATE",
              "MISSING_INFO", "WRONG_WORDING", "MISSING_COVERAGE"}
CHECKS = {f"C{i}" for i in range(1, 10)}
HIGH_RISK_STORIES = {"US-420"}      # money at checkout: a second person approves

# Section 10 of the lesson: the correction log is a feedback loop into the prompt.
PROMPT_FEEDBACK = {
    "WRONG_EXPECTED": "put the worked numbers (oracle table) in the prompt and keep recomputing",
    "INVENTED_REQUIREMENT": "strengthen 'do not invent; use open_questions' and list open questions",
    "WRONG_TRACE": "repeat the AC list and 'exactly one AC per case'",
    "DUPLICATE": "ask for distinct inputs per partition, or a coverage table first",
    "MISSING_INFO": "name every required field and forbid null expected results",
    "WRONG_WORDING": "paste the exact messages inside delimiters and say 'word for word'",
    "MISSING_COVERAGE": "'cover every AC' was ignored: check the trace matrix every run",
}


class ReviewError(ValueError):
    """The review is not complete enough to sign off."""


def load_decisions(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_review(draft_cases: list[dict], review: dict) -> list[str]:
    """Return every reason the review cannot be signed off (empty list = OK)."""
    errors = []
    draft_ids = [c["id"] for c in draft_cases]
    entries = review.get("decisions", [])
    by_id = Counter(e.get("item_id") for e in entries)

    if not str(review.get("reviewer", "")).strip():
        errors.append("no reviewer named")
    if review.get("story") in HIGH_RISK_STORIES:
        approver = str(review.get("approver", "")).strip()
        if not approver:
            errors.append("high-risk story: a second person must approve (approver is empty)")
        elif approver == review.get("reviewer"):
            errors.append("high-risk story: approver must be a different person from the reviewer")

    for cid in draft_ids:
        if by_id[cid] == 0:
            errors.append(f"{cid}: no human decision (an AI item cannot pass review silently)")
        elif by_id[cid] > 1:
            errors.append(f"{cid}: decided {by_id[cid]} times")

    for e in entries:
        cid, d = e.get("item_id", "?"), e.get("decision")
        failed = e.get("failed", [])
        if d not in DECISIONS:
            errors.append(f"{cid}: decision is {d!r}; use one of {sorted(DECISIONS)}")
            continue
        if any(f not in CHECKS for f in failed):
            errors.append(f"{cid}: unknown checklist ids {failed}")
        if d == "ACCEPTED":
            if failed:
                errors.append(f"{cid}: ACCEPTED but checks failed {failed}")
            continue
        if e.get("category") not in CATEGORIES:
            errors.append(f"{cid}: {d} needs a category from {sorted(CATEGORIES)}")
        if not str(e.get("source", "")).strip():
            errors.append(f"{cid}: {d} needs evidence (an AC, a PO answer, a spec section)")
        if d == "EDITED" and not e.get("patch"):
            errors.append(f"{cid}: EDITED needs a patch with the corrected fields")
        if d == "ADDED":
            if cid in draft_ids:
                errors.append(f"{cid}: ADDED cases need a NEW id (never reuse an AI id)")
            if not e.get("patch", {}).get("title"):
                errors.append(f"{cid}: ADDED needs the full case in 'patch'")
        if d in ("EDITED", "REJECTED") and cid not in draft_ids:
            errors.append(f"{cid}: not in the AI draft")
    return errors


def apply_decisions(draft_cases: list[dict], review: dict) -> list[dict]:
    decided = {e["item_id"]: e for e in review["decisions"]}
    approved = []
    for c in draft_cases:
        e = decided[c["id"]]
        if e["decision"] == "REJECTED":
            continue
        case = copy.deepcopy(c)
        if e["decision"] == "EDITED":
            case.update(e["patch"])
        case["review"] = e["decision"]
        approved.append(case)
    for e in review["decisions"]:
        if e["decision"] == "ADDED":
            approved.append({"id": e["item_id"], **e["patch"], "review": "ADDED"})
    return approved


def write_correction_log(draft_cases: list[dict], review: dict, path: str | Path) -> None:
    draft = {c["id"]: c for c in draft_cases}
    cols = ["item_id", "decision", "failed_checks", "category", "ai_said", "fixed_to",
            "source", "reason", "reviewer"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for e in review["decisions"]:
            c = draft.get(e["item_id"], {})
            td = c.get("test_data", {}) if c else {}
            ai_said = "" if not c else (f"{c.get('ac')} total={td.get('order_total')} code={td.get('code')} "
                                        f"balance={td.get('balance')} -> pays {c.get('expected_gift_card_pays')}, "
                                        f"remainder {c.get('expected_remainder')}, msg {c.get('expected_message')}")
            w.writerow({"item_id": e["item_id"], "decision": e["decision"],
                        "failed_checks": ";".join(e.get("failed", [])),
                        "category": e.get("category", ""), "ai_said": ai_said,
                        "fixed_to": json.dumps(e.get("patch", {})) if e.get("patch") else "",
                        "source": e.get("source", ""), "reason": e.get("reason", ""),
                        "reviewer": review["reviewer"]})


def review_metrics(review: dict) -> list[str]:
    ai_items = [e for e in review["decisions"] if e["decision"] != "ADDED"]
    n = len(ai_items) or 1
    d = Counter(e["decision"] for e in ai_items)
    cats = Counter(e["category"] for e in review["decisions"] if e.get("category"))
    fails = Counter(f for e in review["decisions"] for f in e.get("failed", []))
    lines = [f"AI items reviewed : {len(ai_items)}"]
    for k in ("ACCEPTED", "EDITED", "REJECTED"):
        lines.append(f"{k:<18}: {d[k]}  ({d[k] / n:.0%})")
    lines += [f"Usable as-is      : {d['ACCEPTED'] / n:.0%}",
              f"Usable at all     : {(d['ACCEPTED'] + d['EDITED']) / n:.0%}",
              f"Added by human    : {sum(1 for e in review['decisions'] if e['decision'] == 'ADDED')}",
              "Checks failed     : " + ", ".join(f"{k} x{v}" for k, v in sorted(fails.items())),
              "Prompt feedback   :"]
    for cat, _ in cats.most_common(3):
        lines.append(f"  {cat}: {PROMPT_FEEDBACK[cat]}")
    return lines


def decisions_template(draft_cases: list[dict], story: str = "US-420") -> dict:
    """A blank decision file: one TODO entry per AI item. You fill it in; nothing is pre-decided."""
    return {"story": story, "reviewer": "", "approver": "", "date": "",
            "decisions": [{"item_id": c.get("id", "?"), "decision": "TODO", "failed": [], "category": "",
                           "reason": "", "source": "", "patch": {}} for c in draft_cases]}


def signoff(draft_cases: list[dict], review: dict, out_dir: str | Path = ".") -> list[str]:
    errors = validate_review(draft_cases, review)
    if errors:
        raise ReviewError("\n".join(errors))
    out = Path(out_dir)
    approved = apply_decisions(draft_cases, review)
    write_correction_log(draft_cases, review, out / "correction_log.csv")
    suite = {"story": review["story"], "status": "APPROVED",
             "source": "AI-assisted, human-reviewed",
             "reviewed_by": review["reviewer"], "approved_by": review.get("approver", ""),
             "date": review.get("date") or date.today().isoformat(),
             "test_cases": approved}
    (out / "approved_suite.json").write_text(json.dumps(suite, indent=2), encoding="utf-8")
    return review_metrics(review)
