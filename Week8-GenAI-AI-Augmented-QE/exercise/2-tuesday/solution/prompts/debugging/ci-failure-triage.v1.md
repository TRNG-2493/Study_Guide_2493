# Prompt: CI failure triage (v1)

Purpose: First-pass triage of a nightly run, as JSON a script can check against the real log.
Version: 1
Tested with: <Claude model name shown in the interface>, 2 runs, <YYYY-MM-DD>
Technique: format locking; evidence quoting (every claim tied to a log line)
Acceptance criteria: passes tools/check_triage.py (one entry per FAILED test, allowed categories, evidence lines exist in the log); each category agreed or corrected by a human
Check with: python tools/check_triage.py <reply> materials/ci-failure-sample.txt, then review each category
Changes from previous: first version
Evidence: evidence/ci-failure-triage.v1.run1.txt (contract OK), run2.txt (backup: 3 contract problems: paraphrased evidence, mistyped test id)
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
Triage the failed tests in the CI output below. You are helping a QA engineer decide
where to look first; you are not deciding anything.

<ci_output>
<paste the full contents of materials/ci-failure-sample.txt here>
</ci_output>

OUTPUT FORMAT (follow exactly):
- Return ONLY a JSON array with exactly one object per FAILED test. No prose, no code fences.
- Each object has exactly these keys:
  "test": the full test id exactly as it appears after "FAILED " in the output
  "category": one of "product_bug", "test_bug", "needs_clarification", "environment"
  "evidence": one line copied EXACTLY, character for character, from the CI output
  "hypothesis": one sentence, the most likely cause
  "confirm_by": one sentence, how a tester confirms or rules out the hypothesis
- Use "needs_clarification" when the output does not contain enough information to tell
  a product bug from a test bug. Do not guess.
```

## Review notes

run1: agreed with all three categories. The search failure is correctly needs_clarification: nothing in the brief says which message text is the requirement.
run2 (backup): "increase the timeout" contradicts the log line "element is not enabled"; evidence paraphrased; test id mistyped. The checker caught the last two; only a human caught the first.
