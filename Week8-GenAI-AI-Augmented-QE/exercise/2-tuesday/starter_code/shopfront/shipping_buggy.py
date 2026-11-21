"""shipping_buggy.py - same requirement as shipping.py, with one defect.

Used in Stage 5 (structured debugging prompt). Do not read the diff against
shipping.py before you have reproduced the failure and asked Claude for hypotheses.
"""


def shipping_cost(subtotal: float, country: str, express: bool = False) -> float:
    """Return the shipping charge in dollars for a ShopFront order.

    1. US orders ("US") with a subtotal of $75.00 or more ship free.
    2. US orders under $75.00 pay a flat $5.99.
    3. Canadian orders ("CA") pay a flat $12.00, whatever the subtotal.
    4. Express delivery adds $10.00 to the charge, including free-shipping orders.
    5. Any other country code raises ValueError.
    6. A negative subtotal raises ValueError.
    """
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if country not in ("US", "CA"):
        raise ValueError(f"Unsupported country: {country}")
    charge = 12.00 if country == "CA" else 5.99
    if express:
        charge += 10.00
    if country == "US" and subtotal >= 75:
        charge = 0.0
    return round(charge, 2)
