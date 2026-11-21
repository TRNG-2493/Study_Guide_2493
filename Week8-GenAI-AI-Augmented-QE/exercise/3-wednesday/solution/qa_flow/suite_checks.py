"""suite_checks.py - Stage 3: AI-generated test cases and review aids (adapted from the demo).

    build_tc_prompt   test case prompt; carries YOUR PO answers and open questions forward
    parse_suite       defensive parse of Claude's reply
    check_fields      C6 Executable / C7 Traceable
    trace_matrix      C2 Complete / C7 Traceable: forward (AC -> cases) and backward
    check_messages    C3 Grounded / C5 Consistent: messages word for word
    check_expected    C1 Correct: recompute every expected result from YOUR oracle
    find_duplicates   C9 Non-duplicated
    boundary_values_present   C2: the code-length boundaries 15 / 16 / 17

Code POINTS. The human DECIDES. Nothing here approves anything. Do not edit.
"""
from __future__ import annotations

import json
from collections import Counter

from qa_flow.reqs_review import extract_json
from qa_flow.stories import (OPEN_QUESTIONS, PO_ANSWERS, STORIES, allowed_messages,
                             oracle_us420, parse_acs)

FIELDS = ["id", "title", "ac", "type", "priority", "preconditions", "steps", "test_data",
          "expected_gift_card_pays", "expected_remainder", "expected_message"]
TYPES = {"positive", "negative", "boundary"}
PRIORITIES = {"High", "Medium", "Low"}
VAGUE = ["works correctly", "as expected", "should work", "verify it works", "is correct",
         "successfully", "properly"]


def build_tc_prompt(story_id: str = "US-420", max_cases: int = 10) -> str:
    story = STORIES[story_id]
    answers = "\n".join(f"- {ac}: {a}" for ac, a in PO_ANSWERS.get(story_id, [])) or "- none"
    open_q = "\n".join(f"- {q}" for q in OPEN_QUESTIONS.get(story_id, [])) or "- none"
    return f"""You are a senior QA engineer writing manual test cases for an e-commerce
web app (login, search, cart and checkout).

Write test cases for the user story between the <story> tags.

<story>
{story}
</story>

<po_answers>
{answers}
</po_answers>

<open_questions>
{open_q}
</open_questions>

Rules:
1. Every test case traces to exactly one acceptance criterion (AC1, AC2, ...).
2. Cover every acceptance criterion at least once.
3. Include positive, negative and boundary cases. Money has a precision of $0.01.
4. expected_gift_card_pays and expected_remainder are exact amounts as numbers with two
   decimals. expected_message is the exact message text from the story or the PO answers,
   or null. Never write "works correctly".
5. Do NOT write tests for anything in <open_questions> and do NOT invent behaviour the
   story does not state. Put new doubts in "open_questions".
6. At most {max_cases} test cases.

Return ONLY a JSON object, no prose and no Markdown fences, with two keys:
"test_cases": a list of objects with exactly the keys
  {", ".join(FIELDS)}
  ("steps" is a list of strings, "test_data" is an object with "order_total" and "balance"
   (strings, two decimals) and "code" (string), "type" is positive/negative/boundary,
   "priority" is High/Medium/Low)
"open_questions": a list of strings."""


def parse_suite(raw: str) -> dict:
    data = json.loads(extract_json(raw))
    if isinstance(data, list):
        data = {"test_cases": data, "open_questions": []}
    if "test_cases" not in data:
        raise ValueError("Reply has no 'test_cases' key")
    return data


def check_fields(cases: list[dict], story_id: str) -> dict[str, list[str]]:
    acs = parse_acs(STORIES[story_id])
    out: dict[str, list[str]] = {}
    for c in cases:
        p = []
        missing = [f for f in FIELDS if f not in c]
        if missing:
            p.append(f"C6 missing fields: {', '.join(missing)}")
        if not c.get("ac"):
            p.append("C7 no acceptance criterion")
        elif c["ac"] not in acs:
            p.append(f"C7 traces to {c['ac']}, which does not exist")
        if c.get("type") not in TYPES:
            p.append(f"C6 type {c.get('type')!r} not positive/negative/boundary")
        if c.get("priority") not in PRIORITIES:
            p.append(f"C6 priority {c.get('priority')!r} not High/Medium/Low")
        if c.get("expected_gift_card_pays") is None and c.get("expected_remainder") is None \
                and not c.get("expected_message"):
            p.append("C6 no expected result: it cannot pass or fail")
        text = (str(c.get("expected_message") or "") + " " + str(c.get("title") or "")).lower()
        if any(v in text for v in VAGUE):
            p.append("C6 vague expected result")
        out[c.get("id", "?")] = p
    return out


def trace_matrix(cases: list[dict], story_id: str) -> tuple[dict[str, list[str]], list[str]]:
    acs = parse_acs(STORIES[story_id])
    forward = {ac: [c["id"] for c in cases if c.get("ac") == ac] for ac in acs}
    orphans = [c.get("id", "?") for c in cases if c.get("ac") not in acs]
    return forward, orphans


def check_messages(cases: list[dict], story_id: str) -> dict[str, list[str]]:
    allowed = allowed_messages(story_id)
    out: dict[str, list[str]] = {}
    for c in cases:
        msg = c.get("expected_message")
        if msg and msg not in allowed:
            out[c["id"]] = [f"C5/C3 message {msg!r} is not word for word in the story or PO answers"]
    return out


def _money(v) -> float | None:
    try:
        return round(float(v), 2)
    except (TypeError, ValueError):
        return None


def check_expected(cases: list[dict]) -> dict[str, list[str]]:
    """C1: recompute from YOUR oracle (stories.oracle_us420)."""
    out: dict[str, list[str]] = {}
    for c in cases:
        td = c.get("test_data") or {}
        total, balance = _money(td.get("order_total")), _money(td.get("balance"))
        if total is None or balance is None:
            continue
        code = str(td.get("code", ""))
        want = oracle_us420(total, code, balance)
        p = []
        if want is None:
            p.append(f"C3 the story and PO answers do not decide code {code!r}: open question, park it")
        else:
            got_pays, got_rem = _money(c.get("expected_gift_card_pays")), _money(c.get("expected_remainder"))
            if got_pays is not None and got_pays != want["gift_card_pays"]:
                p.append(f"C1 expected_gift_card_pays {got_pays:.2f} but your oracle gives {want['gift_card_pays']:.2f}")
            if got_rem is not None and got_rem != want["remainder"]:
                p.append(f"C1 expected_remainder {got_rem:.2f} but your oracle gives {want['remainder']:.2f}")
            if (c.get("expected_message") or None) != want["message"]:
                p.append(f"C1 expected_message {c.get('expected_message')!r} but your oracle gives {want['message']!r}")
        if p:
            out[c["id"]] = p
    return out


def find_duplicates(cases: list[dict]) -> dict[str, list[str]]:
    seen: dict[tuple, str] = {}
    out: dict[str, list[str]] = {}
    for c in cases:
        td = c.get("test_data") or {}
        key = (str(td.get("order_total")), str(td.get("code")), str(td.get("balance")))
        if key in seen:
            out[c["id"]] = [f"C9 same inputs as {seen[key]}"]
        else:
            seen[key] = c["id"]
    return out


def suite_mix(cases: list[dict]) -> Counter:
    return Counter(c.get("type") for c in cases)


def boundary_values_present(cases: list[dict]) -> dict[str, bool]:
    lengths = {len(str((c.get("test_data") or {}).get("code", ""))) for c in cases}
    return {f"code length {n}": n in lengths for n in (15, 16, 17)}


def review_pointers(cases: list[dict], story_id: str = "US-420") -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {c.get("id", "?"): [] for c in cases}
    for part in (check_expected(cases), check_fields(cases, story_id),
                 check_messages(cases, story_id), find_duplicates(cases)):
        for cid, ps in part.items():
            merged.setdefault(cid, []).extend(ps)
    order = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
    return {cid: sorted(set(ps), key=lambda s: order.index(s[:2]) if s[:2] in order else 99)
            for cid, ps in merged.items()}
