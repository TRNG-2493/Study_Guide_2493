"""giftcard_buggy.py - same requirement, one defect. Used in Stage 4 (which suite catches it?).
Do not read the difference from giftcard.py until your approved suite has run against both."""
import re

MSG_NOT_RECOGNISED = "Gift card code not recognised"
MSG_NO_BALANCE = "This gift card has no balance"


def apply_gift_card(order_total: float, code: str, balance: float) -> dict:
    normalised = code.upper()
    if not re.fullmatch(r"[A-Z0-9]{15,16}", normalised):
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NOT_RECOGNISED}
    if balance <= 0:
        return {"gift_card_pays": 0.0, "remainder": round(order_total, 2), "message": MSG_NO_BALANCE}
    pays = round(min(balance, order_total), 2)
    return {"gift_card_pays": pays, "remainder": round(order_total - pays, 2), "message": None}
