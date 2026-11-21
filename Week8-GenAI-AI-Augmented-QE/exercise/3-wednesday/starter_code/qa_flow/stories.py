"""stories.py - the test basis for Wednesday's exercise, and YOUR oracle.

Nothing in this file may be produced by Claude. You write:
  - REFERENCE_ISSUES   your own manual review of US-420, BEFORE any prompt (Stage 1)
  - PO_ANSWERS and OPEN_QUESTIONS   only what the product owner decided (Stage 1)
  - oracle_us420       your expected results from the ACs and PO answers (Stage 2)
Same structure as the Wednesday demo's stories.py.
"""
from __future__ import annotations

import re

US_420 = """US-420 Pay with a gift card at checkout
As a shopper I want to pay with a gift card so that I can use my balance.
AC1: A gift card code is 16 characters: letters A-Z and digits only.
AC2: The gift card pays as much of the order total as its balance allows; any remainder is paid by card.
AC3: A gift card with a zero balance shows "This gift card has no balance".
AC4: An unknown or badly formed code shows "Gift card code not recognised".
AC5: The gift card should be applied quickly."""

STORIES = {"US-420": US_420}

# ---------------------------------------------------------------------------
# Stage 1, BEFORE you prompt Claude: your own manual review of US-420.
# Each item: (short name, keywords). A Claude finding "covers" the item if any
# keyword appears in it. Write at least 4. (Demo: reqs_review.REFERENCE_ISSUES)
# ---------------------------------------------------------------------------
REFERENCE_ISSUES: dict[str, list[tuple[str, list[str]]]] = {
    "US-420": [
        # TODO e.g. ("AC5 'quickly' has no number", ["quickly"]),
    ],
}

# ---------------------------------------------------------------------------
# Stage 1, AFTER the product owner has answered your question log.
# Only answered questions go into PO_ANSWERS. Everything else stays open.
# Format: ("AC2", "the answer, with any exact message in double quotes")
# ---------------------------------------------------------------------------
PO_ANSWERS: dict[str, list[tuple[str, str]]] = {"US-420": []}      # TODO
OPEN_QUESTIONS: dict[str, list[str]] = {"US-420": []}             # TODO


def parse_acs(story: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r"^(AC\d+):\s*(.+)$", story, re.MULTILINE)}


def allowed_messages(story_id: str) -> set[str]:
    """Every quoted message in the story or a PO answer. Tests may expect only these."""
    text = STORIES[story_id] + "\n" + "\n".join(a for _, a in PO_ANSWERS.get(story_id, []))
    return set(re.findall(r'"([^"]+)"', text))


# ---------------------------------------------------------------------------
# Stage 2: YOUR oracle, written from AC1 to AC4 plus the PO answers.
# Do NOT import shopfront: the application is never the oracle for its own tests.
# ---------------------------------------------------------------------------
MSG_NO_BALANCE = "This gift card has no balance"
MSG_NOT_RECOGNISED = "Gift card code not recognised"


def oracle_us420(order_total: float, code: str, balance: float) -> dict | None:
    """Expected {"gift_card_pays", "remainder", "message"} for one redemption.

    Return None when the story and the PO answers do not decide the case:
    that is an OPEN question, not something to guess.
    Amounts are rounded to cents.
    """
    raise NotImplementedError("Stage 2: write your oracle before you read any AI test case")
