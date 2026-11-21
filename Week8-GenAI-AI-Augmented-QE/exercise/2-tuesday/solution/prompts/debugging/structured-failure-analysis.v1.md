# Prompt: structured failure analysis (v1)

Purpose: Get ranked, checkable hypotheses for a failing pytest test without letting the model change the test.
Version: 1
Tested with: <Claude model name shown in the interface>, 1 run, <YYYY-MM-DD>
Technique: structured debugging request (reproduce, read, minimise, ask for hypotheses before a fix)
Acceptance criteria: 3 ranked hypotheses, each with a confirmation step; no change to the test proposed; a fix only after the hypotheses; the top hypothesis is confirmed by a command the tester runs
Check with: read the reply; run the confirmation command yourself; after the fix, git diff --stat shows no change under tests/
Changes from previous: first version
Evidence: evidence/structured-failure-analysis.v1.run1.txt
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
## Instructions
You are a senior Python test engineer. Environment: Python 3.10+, pytest.
Do not rewrite or weaken the test assertions. The requirement in the docstring is the source of truth.

I have a failing pytest test and need help finding the cause.

## Code under test (shopfront/shipping_buggy.py)
<paste the whole file, copied from the file, not retyped>

## Test file (tests/test_shipping_buggy.py)
<paste the whole file>

## Full pytest output
<paste the complete output of: python -m pytest -q tests/test_shipping_buggy.py>

## Expected vs actual
Requirement sentence 4: express delivery adds $10.00, including free-shipping orders.
For a US order of $80.00 with express I expect 10.00; I get 0.0.

## What I already tried
Re-ran 3 times: fails every time (not flaky). Express on a $40.00 US order (15.99) and on CA (22.00) pass.

## What I want from you
1. List the 3 most likely causes, ranked from most to least likely.
2. For each cause, give one quick way I can confirm or rule it out.
3. Only after that, propose the smallest code change that fixes the root cause. Do not change the test.
```

## Review notes

Top hypothesis in the backup reply: the free-shipping assignment (charge = 0.0) runs after the express surcharge and overwrites it. Confirmed with:
python -c "from shopfront.shipping_buggy import shipping_cost as s; print(s(80,'US',True), s(74.99,'US',True))"  ->  0.0 15.99
Fix: move the express block below the free-shipping rule. git diff --stat lists only shopfront/shipping_buggy.py. Suite: 5 passed.
