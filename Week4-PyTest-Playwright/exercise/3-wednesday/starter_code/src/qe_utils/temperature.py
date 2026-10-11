"""Code under test: temperature conversion (Project 1 utility function).

SPECIFICATION:
  celsius_to_fahrenheit(c) = c * 9 / 5 + 32   (NOT rounded: a float).
      Not a number (bool excluded) -> TypeError("temperature must be a number")
      Below absolute zero (-273.15) -> ValueError("below absolute zero")
"""


def celsius_to_fahrenheit(celsius):
    if not isinstance(celsius, (int, float)) or isinstance(celsius, bool):
        raise TypeError("temperature must be a number")
    if celsius < -273.15:
        raise ValueError("below absolute zero")
    return celsius * 9 / 5 + 32
