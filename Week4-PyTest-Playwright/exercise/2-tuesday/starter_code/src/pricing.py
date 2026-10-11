"""Code under test: uses 'from exchange import get_rate' (so WHERE you patch matters)."""
import requests

from exchange import get_rate


def price_in(price_usd, target):
    """Convert a USD price into another currency (rounded to 2 decimals).

    USD -> USD needs no rate lookup (no network call is made).
    """
    if price_usd < 0:
        raise ValueError("price must not be negative")
    if target == "USD":
        return price_usd
    rate = get_rate("USD", target)
    return round(price_usd * rate, 2)


def price_label(price_usd, target):
    """Human readable label, e.g. '18.50 EUR'. Degrades gracefully if the rate API is down."""
    try:
        value = price_in(price_usd, target)
    except requests.RequestException:
        return "Price unavailable"
    return f"{value:.2f} {target}"
