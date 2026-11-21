# Refinement Log

## TD-1 shipping test ideas: the ladder

Acceptance criteria written before v1 (copy from score_reply.py):
1.
2.

| Version | The ONE change | Lint | Score (run 1) | Criteria that flipped | Input problem or model limitation? |
|---|---|---|---|---|---|
| v1 | first version | | | | |
| v2 | | | | | |
| v3 | | | | | |
| v4 | | | | | |

Final version, three runs:

| Run | Score | Failed criteria | What differed from the other runs |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Criteria that still fail sometimes, and the check OUTSIDE the model that catches them:

## TD-2 format-locked cases

| Reply | Syntax | Structure | Re-ask needed? | Re-ask result | pytest result |
|---|---|---|---|---|---|
| | | | | | |

Content review of every failing or suspicious case:

| Case id | Claude expected | Code returns | Who is right? (code / Claude's case / question for PO) | Requirement sentence |
|---|---|---|---|---|
| | | | | |

## TD-3 few-shot Gherkin

| Version | Change | check_gherkin result | Leakage | What I corrected by reading |
|---|---|---|---|---|
| | | | | |

## DB-1 structured debugging

- My own reading of the failure BEFORE asking Claude:
- Claude's ranked hypotheses (short):
- The command I ran to confirm the top hypothesis, and its output:
- The fix (the diff) and the test result after it:
- Weakening check: did the test file change? (`git diff --stat`):

## DB-2 CI triage

| Test | Claude category | My category | Evidence line correct? | Agree? Why / why not |
|---|---|---|---|---|
| | | | | |

## What I would tell a teammate (3 bullets)
-
