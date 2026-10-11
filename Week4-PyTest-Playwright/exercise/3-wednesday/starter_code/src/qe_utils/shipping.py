"""Code under test: shipping-cost utility (Project 1 utility function).

SPECIFICATION (the tests are written against THIS text, not against the code):
  * weight_kg must be a number (int or float, not bool) greater than 0 and at most 30.
      - not a number          -> TypeError("weight must be a number")
      - <= 0 or > 30          -> ValueError("weight must be between 0 and 30 kg")
  * zone must be one of "local", "national", "international" (lower-case).
      - not a string          -> TypeError("zone must be a string")
      - any other string      -> ValueError("unknown zone: <zone>")
  * Light parcels (UP TO AND INCLUDING 5 kg) pay the light rate;
    heavier parcels (over 5 kg) pay the heavy rate.

        zone            light   heavy
        local            4.00    8.00
        national         6.50   12.00
        international   15.00   30.00
"""

RATES = {
    "local": (4.00, 8.00),
    "national": (6.50, 12.00),
    "international": (15.00, 30.00),
}


def shipping_cost(weight_kg, zone):
    if not isinstance(weight_kg, (int, float)) or isinstance(weight_kg, bool):
        raise TypeError("weight must be a number")
    if not isinstance(zone, str):
        raise TypeError("zone must be a string")
    if not 0 < weight_kg <= 30:
        raise ValueError("weight must be between 0 and 30 kg")
    if zone not in RATES:
        raise ValueError(f"unknown zone: {zone}")
    light, heavy = RATES[zone]
    if weight_kg < 5:          # <- a developer wrote this line; compare it with the spec above
        return light
    return heavy
