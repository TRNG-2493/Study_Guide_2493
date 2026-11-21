"""giftcard.py - ShopFront gift card redemption (correct version).

Implements US-420 as the product owner clarified it (see materials/po-answers.md).
This is the APPLICATION. It is never the oracle for its own tests.
"""
import re

MSG_NOT_RECOGNISED = "Gift card code not recognised"
MSG_NO_BALANCE = "This gift card has no balance"


def apply_gift_card(order_total: float, code: str, balance: float) -> dict:
    """Return how much the gift card pays, what remains to pay by card, and any message."""
    normalised = code.upper()
    if not re.fullmatch(r"[A-Z0-9]{16}", normalised):
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NOT_RECOGNISED}
    if balance <= 0:
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NO_BALANCE}
    pays = round(min(balance, order_total), 2)
    return {"gift_card_pays": pays, "remainder": round(order_total - pays, 2), "message": None}
