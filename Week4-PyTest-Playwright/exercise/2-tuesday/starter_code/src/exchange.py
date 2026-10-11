"""Code under test: calls an EXTERNAL HTTP API for currency rates (the thing you will mock).

The '.test' domain never resolves, so a forgotten mock fails loudly instead of hitting the net.
"""
import requests

RATES_URL = "https://rates.example-fx.test/v1/latest"


def get_rate(base, target):
    """Return the exchange rate (float) from base currency to target currency."""
    response = requests.get(RATES_URL, params={"base": base, "target": target}, timeout=5)
    response.raise_for_status()
    return response.json()["rate"]
