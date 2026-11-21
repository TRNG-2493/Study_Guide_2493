# Prompt: shipping test ideas (v5)

Purpose: Design test ideas for the ShopFront shipping rule, ready to automate with pytest parametrize.
Version: 5
Tested with: <Claude model name shown in the interface>, 3 runs, <YYYY-MM-DD>
Technique: equivalence partitioning, boundary value analysis
Acceptance criteria: the 12 criteria in tools/score_reply.py (on-feature; 74.99/75.00/75.01; express on a free order = 10.00; CA 12.00; unsupported country and negative subtotal raise ValueError; exact values; table 5+ rows; no invented rules; assumptions listed)
Check with: python tools/score_reply.py evidence/shipping-test-ideas.v5.run<k>.txt, then read every row against the six requirement sentences
Changes from previous: added done-criteria and an instruction to list assumptions before the table. Expected to fix: assumptions listed; express on a free order covered on every run
Evidence: evidence/shipping-test-ideas.v5.run1.txt, run2.txt, run3.txt (12/12 on all three runs)
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
Design 8 to 10 test ideas for the function below using equivalence
partitioning and boundary value analysis. Money uses cent precision (0.01).

Audience: QA engineers who will automate these with pytest parametrize.

<requirement>
shipping_cost(subtotal, country, express=False) returns the shipping charge in dollars.
1. US orders ("US") with a subtotal of $75.00 or more ship free.
2. US orders under $75.00 pay a flat $5.99.
3. Canadian orders ("CA") pay a flat $12.00, whatever the subtotal.
4. Express delivery adds $10.00 to the charge, including free-shipping orders.
5. Any other country code raises ValueError.
6. A negative subtotal raises ValueError.
</requirement>

Constraints:
- Only US and CA are supported; do not invent other countries, limits or address rules.
- Expected results must be exact dollar amounts with two decimals, or "raises ValueError".

Output: a Markdown table with columns ID, Subtotal, Country, Express, Expected, Technique.

Done when: every requirement sentence 1 to 6 has at least one test, the values
74.99, 75.00 and 75.01 are covered, and express is tested on a free-shipping order.

Before the table, list any assumptions you had to make because the requirement
is silent (for example letter case of country codes or a zero subtotal).
Do not resolve them silently.
```

## Review notes

Human review beyond the scorer: recomputed every expected value by calling shipping_cost; all matched. Assumptions to send to the product owner: lower-case "us" (code rejects it), $0.00 subtotal. Possible model limitation to keep checking: arithmetic on express plus a flat rate (5.99 + 10.00, 12.00 + 10.00). No prompt change guarantees it; recomputing with the real function catches it.
