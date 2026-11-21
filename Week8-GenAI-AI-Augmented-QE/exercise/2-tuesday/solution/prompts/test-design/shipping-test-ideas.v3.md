# Prompt: shipping test ideas (v3)

Purpose: Design test ideas for the ShopFront shipping rule, ready to automate with pytest parametrize.
Version: 3
Tested with: <Claude model name shown in the interface>, 1 runs, <YYYY-MM-DD>
Technique: equivalence partitioning, boundary value analysis
Acceptance criteria: the 12 criteria in tools/score_reply.py (on-feature; 74.99/75.00/75.01; express on a free order = 10.00; CA 12.00; unsupported country and negative subtotal raise ValueError; exact values; table 5+ rows; no invented rules; assumptions listed)
Check with: python tools/score_reply.py evidence/shipping-test-ideas.v3.run<k>.txt, then read every row against the six requirement sentences
Changes from previous: named the techniques, the quantity (8 to 10) and cent precision. Expected to fix: boundaries 74.99 / 75.00 / 75.01
Evidence: evidence/shipping-test-ideas.v3.run1.txt
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
Design 8 to 10 test ideas for the function below using equivalence
partitioning and boundary value analysis. Money uses cent precision (0.01).
Label each idea with the technique it comes from.

<requirement>
shipping_cost(subtotal, country, express=False) returns the shipping charge in dollars.
1. US orders ("US") with a subtotal of $75.00 or more ship free.
2. US orders under $75.00 pay a flat $5.99.
3. Canadian orders ("CA") pay a flat $12.00, whatever the subtotal.
4. Express delivery adds $10.00 to the charge, including free-shipping orders.
5. Any other country code raises ValueError.
6. A negative subtotal raises ValueError.
</requirement>
```

## Review notes

Boundaries present, technique labels present, one assumption volunteered (letter case) without being asked. Output is a numbered list, not a table.
