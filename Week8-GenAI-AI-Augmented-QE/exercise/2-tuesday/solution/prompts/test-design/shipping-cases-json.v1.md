# Prompt: shipping cases as JSON (v1)

Purpose: Generate shipping_cost test cases as JSON that tests/test_shipping_generated.py runs directly.
Version: 1
Tested with: <Claude model name shown in the interface>, 2 runs, <YYYY-MM-DD>
Technique: format locking; equivalence partitioning, boundary value analysis
Acceptance criteria: loads with no syntax or structure problems (tools/load_shipping_cases.py); 8+ cases; every requirement sentence covered; every expected value correct when reviewed
Check with: python tools/load_shipping_cases.py <reply> (add --reask on failure, once), then python -m pytest -v tests/test_shipping_generated.py --cases <reply>, then review every case
Changes from previous: first version (contract = REQUIRED_KEYS, TECHNIQUES, ID_PATTERN in tools/load_shipping_cases.py)
Evidence: evidence/shipping-cases-json.v1.run1.txt (clean, 9 passed), run2.txt (format OK, content wrong: 3 failed), drift-test.txt (hand-made drift: 8 problems)
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
You are a QA engineer designing unit tests.

Design 8 to 10 test cases for the Python function below using boundary value
analysis and equivalence partitioning. Money uses cent precision (0.01).

<requirement>
shipping_cost(subtotal, country, express=False) returns the shipping charge in dollars.
1. US orders ("US") with a subtotal of $75.00 or more ship free.
2. US orders under $75.00 pay a flat $5.99.
3. Canadian orders ("CA") pay a flat $12.00, whatever the subtotal.
4. Express delivery adds $10.00 to the charge, including free-shipping orders.
5. Any other country code raises ValueError.
6. A negative subtotal raises ValueError.
</requirement>

OUTPUT FORMAT (follow exactly):
- Return ONLY a JSON array. No prose before or after it. No Markdown code fences.
- Each element is an object with exactly these 7 keys, in this order:
  "id": string, "SC-" followed by two digits, e.g. "SC-01"
  "title": string, under 60 characters
  "subtotal": number (not a string), e.g. 74.99
  "country": string, the country code passed to the function (unsupported codes are allowed as test input)
  "express": JSON boolean true or false (not a string)
  "expected": number for a returned charge, OR the string "ValueError" if the call must raise
  "technique": one of "BVA", "EP", "error_guessing"
- Use double quotes. No trailing commas. No comments.

Shape of one element (values are placeholders, do not copy them):
{"id": "SC-00", "title": "...", "subtotal": 0.0, "country": "..", "express": false, "expected": 0.0, "technique": "EP"}
```

## Review notes

run1: wrapped in a code fence despite "No Markdown code fences"; tolerated by extract_json. All 9 cases correct.
run2: structure OK, 3 failures. SC-03 expects express on a free order to stay free: Claude wrong (sentence 4). SC-04 lower-case "us": invented requirement; question for the product owner, not an assertion. SC-05 zero subtotal expects 0.00: Claude wrong (sentence 2, under 75.00 pays 5.99).
