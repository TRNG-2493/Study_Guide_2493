"""shipping.py - ShopFront checkout rule used in Stage 5 (evidence probe).

The requirement lives in the docstring. Treat the docstring as the source of truth.
This file is synthetic course material; it is safe to paste into Claude.
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
    if country == "US":
        base = 0.0 if subtotal >= 75 else 5.99
    elif country == "CA":
        base = 12.00
    else:
        raise ValueError(f"Unsupported country: {country}")
    if express:
        base += 10.00
    return round(base, 2)
