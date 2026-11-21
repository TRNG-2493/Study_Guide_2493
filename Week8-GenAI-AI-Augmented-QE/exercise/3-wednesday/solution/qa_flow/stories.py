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
        ("AC1 upper/lower case letters in the code", ["case", "lower"]),
        ("AC1 spaces or dashes typed inside the code", ["space", "dash", "hyphen", "format"]),
        ("AC2 what 'order total' includes (shipping, tax)", ["shipping", "tax", "order total"]),
        ("AC2 balance larger than the total: remainder and unused balance", ["larger", "greater", "exceeds", "more than", "unused", "remaining balance"]),
        ("AC3/AC4 expired or blocked cards", ["expire", "blocked", "inactive"]),
        ("AC5 'quickly' has no number", ["quickly"]),
    ],
}

# ---------------------------------------------------------------------------
# Stage 1, AFTER the product owner has answered your question log.
# Only answered questions go into PO_ANSWERS. Everything else stays open.
# Format: ("AC2", "the answer, with any exact message in double quotes")
# ---------------------------------------------------------------------------
PO_ANSWERS: dict[str, list[tuple[str, str]]] = {"US-420": [
    ("AC1", "Codes are not case-sensitive: lower-case letters are accepted and treated as upper case."),
    ("AC2", "Order total means the final amount the shopper pays, including shipping and tax."),
    ("AC2", "When the balance is larger than the order total, the gift card pays the whole total, "
            "the remainder is 0.00 and the unused balance stays on the card."),
    ("AC5", "Out of scope this sprint; the platform team will set a performance target later."),
]}
OPEN_QUESTIONS: dict[str, list[str]] = {"US-420": [
    "Are spaces or dashes inside a gift card code accepted (for example QATEST26-ABCD-1234)?",
]}


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
    if re.search(r"[\s-]", code):
        return None                                   # spaces/dashes: OPEN question
    if not re.fullmatch(r"[A-Z0-9]{16}", code.upper()):  # AC1 + PO answer (case-insensitive)
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NOT_RECOGNISED}
    if balance <= 0:                                  # AC3
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NO_BALANCE}
    pays = round(min(balance, order_total), 2)        # AC2 + PO answer
    return {"gift_card_pays": pays, "remainder": round(order_total - pays, 2), "message": None}
