# RequirementReviewer contract, in plain English (written BEFORE any JSON Schema)

## Input contract (what the agent accepts)

| Field | Required? | Type and rule | Default (applied in code) | Why |
|---|---|---|---|---|
| story_id | yes | string, `US-` and three digits | - | Traceability; finding ids reuse the number |
| title | yes | string, 5 to 120 characters | - | Context for the reviewer; one line |
| acceptance_criteria | yes | list, at least 1 item; each item has `id` (`AC` + digits) and `text` (at least 5 characters) | - | Nothing to review without ACs |
| max_findings | no | whole number 1 to 20 | 10 | Keeps the review short enough for a human to read |
| focus | no | list of distinct defect categories (AMBIGUOUS, UNMEASURABLE, INCOMPLETE, CONTRADICTION, UNTESTABLE) | all five | Lets a caller ask for, say, only UNMEASURABLE |

Rejected before any model call when: a required field is missing, a pattern or range is broken, `acceptance_criteria` is empty, or an unknown field is present.

## Output contract (what the agent returns)

| Field | Required? | Type and rule | Why |
|---|---|---|---|
| contract_version | yes | exactly "1.0.0" | Consumers know which contract they hold |
| story_id | yes | same pattern as the input | Traceability (equality with the input is rule R1, in code) |
| status | yes | "ok" or "needs_clarification" | The honest "I can't" path |
| findings | yes | list (may be empty) of finding objects | An empty list is a legal answer for a clear story |
| finding.id | yes | `F-` + three digits + `-` + two digits, e.g. F-420-01 | Stable reference in the question log |
| finding.ac_id | yes | `AC` + digits | Every finding points at exactly one AC |
| finding.category | yes | one of the five defect categories | Same vocabulary as Wednesday's review |
| finding.quote | yes | string, 3 to 200 characters | The exact words that cause the problem (grounding) |
| finding.explanation | yes | string, 10 to 300 characters | Why it is a problem |
| finding.question | yes | string ending with "?" | One clarifying question for the product owner |
| finding.severity | yes | high, medium or low | Helps the PO answer the important ones first |
| open_questions | yes | list of strings (may be empty) | Questions about the INPUT itself when the story cannot be reviewed |

## How "I can't" works
- `status: "ok"`: the story was reviewed. `findings` holds every problem found (possibly none); `open_questions` is empty.
- `status: "needs_clarification"`: the story could not be reviewed (placeholders instead of criteria, or the request is not a requirements review). `findings` is empty and `open_questions` says what input is needed.

## What the schema cannot check (goes to the rule catalogue)
- Output `story_id` equals the input (R1); `ac_id` exists in the input (R2); the quote is really in that AC (R3); ids are unique and match the story (R4); no more than `max_findings` (R5); status and lists agree (R6); categories respect `focus` (R7).
- Whether a finding proposes an answer or a number the story does not contain (Q1), duplicates (Q2), and whether the findings are relevant and complete (human, Q3).
