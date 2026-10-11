# Visual diff diagnosis (Task 6)

Fill this in after you trigger the deliberate visual difference. Keep it short and factual.

## Run
- Command used to trigger the diff:
- Date / Cypress version / browser:

## Which checks failed and which stayed green?
| Test / snapshot name | Threshold | Result | Mismatched pixels / fraction |
|---|---|---|---|
|  |  |  |  |

## What the diff image shows
(Open `cypress/snapshots/diff/<spec path>/<name>.png`. Describe WHAT changed and WHERE, in words a developer can act on.)

## Classification (pick one and justify in 2 sentences)
- [ ] Regression (a bug: fix the app, baseline stays)
- [ ] Intentional change (approve: regenerate that baseline, commit with an explanation)
- [ ] Noise (flake: fix determinism, do NOT raise the threshold first)

## Evidence the failure is not noise
(Which other tests stayed green? What did the diff highlight? Did a second run give the same numbers?)

## Decision and follow-up
- Action taken:
- Back to green? (command + result):
