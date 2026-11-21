"""data_checks.py - Stage 5: AI-designed test data for US-420, checked independently.

    BASE_ROW           one known-good row; every test row changes ONE field
    build_data_prompt  constrained, synthetic-only data prompt
    check_rows         independent checks: counts, one change, strings, reserved test prefix,
                       and every label recomputed with YOUR oracle (stories.oracle_us420)

"Claude designs, code generates, checks prove." (ai-generated-test-data.md)
Do not edit. If check_rows disagrees with Claude, the human decides who is right.
"""
from __future__ import annotations

import json
from collections import Counter

from qa_flow.reqs_review import extract_json
from qa_flow.stories import OPEN_QUESTIONS, PO_ANSWERS, US_420, oracle_us420

FIELDS = ["order_total", "code", "balance"]
CATEGORIES = ["VALID", "INVALID", "BOUNDARY", "EDGE"]
OUTCOMES = {"applied", "no_balance", "not_recognised"}
TEST_PREFIX = "QATEST"           # team rule: every test gift card code starts with this

BASE_ROW = {"order_total": "80.00", "code": "QATEST26ABCD1234", "balance": "50.00"}


def build_data_prompt(rows_per_category: int = 3) -> str:
    answers = "\n".join(f"- {ac}: {a}" for ac, a in PO_ANSWERS.get("US-420", [])) or "- none"
    open_q = "\n".join(f"- {q}" for q in OPEN_QUESTIONS.get("US-420", [])) or "- none"
    return f"""You are a test data designer for an e-commerce checkout.

<rules>
{US_420}
</rules>

<po_answers>
{answers}
</po_answers>

<open_questions>
{open_q}
</open_questions>

<base_row>
{json.dumps(BASE_ROW)}
</base_row>

Design test data rows for gift card redemption.
1. Start every row from <base_row> and change EXACTLY ONE field, so a failure points at one
   rule. (One VALID row may be the base row unchanged.)
2. Exactly {rows_per_category} rows in each category: {", ".join(CATEGORIES)}.
3. "expected_outcome" is one of "applied", "no_balance", "not_recognised", decided ONLY from
   the rules and PO answers above. "expected_gift_card_pays" is a string with two decimals.
4. All values are strings.
5. Synthetic data only. Every gift card code must start with "{TEST_PREFIX}" so it can
   never be a real card.
6. If the rules and PO answers do not decide a value, add it to "questions", not to the rows.

Return ONLY a JSON object, no prose and no Markdown fences:
{{"rows": [{{"id": "TD-01", "category": "VALID", "changed_field": "none",
            "data": {{"order_total": "...", "code": "...", "balance": "..."}},
            "expected_outcome": "applied", "expected_gift_card_pays": "50.00", "why": "..."}}],
  "questions": ["..."]}}"""


def parse_rows(raw: str) -> tuple[list[dict], list[str]]:
    data = json.loads(extract_json(raw))
    if isinstance(data, list):
        return data, []
    return data.get("rows", []), data.get("questions", [])


def _outcome(result: dict) -> str:
    if result["message"] == "This gift card has no balance":
        return "no_balance"
    if result["message"] == "Gift card code not recognised":
        return "not_recognised"
    return "applied"


def check_rows(rows: list[dict], rows_per_category: int = 3) -> list[str]:
    problems = []
    counts = Counter(r.get("category") for r in rows)
    for cat in CATEGORIES:
        if counts[cat] != rows_per_category:
            problems.append(f"{cat}: expected {rows_per_category} rows, got {counts[cat]}")
    for r in rows:
        rid, data = r.get("id", "?"), r.get("data", {})
        if sorted(data) != sorted(FIELDS):
            problems.append(f"{rid}: data keys must be exactly {FIELDS}")
            continue
        for f in FIELDS:
            if not isinstance(data[f], str):
                problems.append(f"{rid}: {f} is {type(data[f]).__name__}, not a string")
        changed = [f for f in FIELDS if str(data[f]) != BASE_ROW[f]]
        if len(changed) > 1:
            problems.append(f"{rid}: changes {len(changed)} fields ({', '.join(changed)}); one change per row")
        if not str(data["code"]).upper().startswith(TEST_PREFIX):
            problems.append(f"{rid}: code {data['code']!r} does not start with {TEST_PREFIX}: could be a real card")
        try:
            total, balance = float(data["order_total"]), float(data["balance"])
        except ValueError:
            problems.append(f"{rid}: order_total or balance is not a number")
            continue
        want = oracle_us420(round(total, 2), str(data["code"]), round(balance, 2))
        if want is None:
            problems.append(f"{rid}: your oracle says this case is undecided: it belongs in questions, not rows")
            continue
        if r.get("expected_outcome") not in OUTCOMES:
            problems.append(f"{rid}: expected_outcome must be one of {sorted(OUTCOMES)}")
        elif r["expected_outcome"] != _outcome(want):
            problems.append(f"{rid}: Claude says {r['expected_outcome']}, your oracle says {_outcome(want)}")
        try:
            if round(float(r.get("expected_gift_card_pays")), 2) != want["gift_card_pays"]:
                problems.append(f"{rid}: Claude says pays {r.get('expected_gift_card_pays')}, "
                                f"your oracle says {want['gift_card_pays']:.2f}")
        except (TypeError, ValueError):
            problems.append(f"{rid}: expected_gift_card_pays is not a number")
    return problems
