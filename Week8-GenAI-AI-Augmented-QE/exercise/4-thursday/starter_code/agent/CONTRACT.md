# RequirementReviewer contract, in plain English (write this BEFORE any JSON Schema)

See `written/4-thursday/input-output-contracts.md`, section 7, for the shape of this table.

## Input contract (what the agent accepts)

| Field | Required? | Type and rule | Default (applied in code) | Why |
|---|---|---|---|---|
| story_id | | TODO | | |
| title | | TODO | | |
| acceptance_criteria | | TODO | | |
| TODO (per-call options, e.g. a limit on findings) | | | | |

Rejected before any model call when: TODO

## Output contract (what the agent returns)

| Field | Required? | Type and rule | Why |
|---|---|---|---|
| contract_version | | TODO | |
| story_id | | TODO | |
| status | | TODO (include an honest "I can't" value) | |
| TODO (the findings list, and the fields of ONE finding) | | | |
| open_questions | | TODO | |

## How "I can't" works
TODO: which status, which field carries the questions, and when each is used.

## What the schema cannot check (goes to the rule catalogue in rules.md)
- TODO
