# Prompt: shipping test ideas (v1)

Purpose: Design test ideas for the ShopFront shipping rule, ready to automate with pytest parametrize.
Version: 1
Tested with: <Claude model name shown in the interface>, 1 runs, <YYYY-MM-DD>
Technique: none (baseline)
Acceptance criteria: the 12 criteria in tools/score_reply.py (on-feature; 74.99/75.00/75.01; express on a free order = 10.00; CA 12.00; unsupported country and negative subtotal raise ValueError; exact values; table 5+ rows; no invented rules; assumptions listed)
Check with: python tools/score_reply.py evidence/shipping-test-ideas.v1.run<k>.txt, then read every row against the six requirement sentences
Changes from previous: first version: deliberately vague baseline
Evidence: evidence/shipping-test-ideas.v1.run1.txt
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
Write some tests for the shipping feature.
```

## Review notes

Expected: generic shipping tests, invented rules (PO boxes, delivery speed, per-customer limits), no values. Input problem: no context.
