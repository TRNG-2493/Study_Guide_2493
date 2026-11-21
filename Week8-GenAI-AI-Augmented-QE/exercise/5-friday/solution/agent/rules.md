# RequirementReviewer: Rule Catalogue (contract 1.0.0)

Every rule lives in exactly ONE layer. Cheapest and most certain first.
Friday's validation script implements every "Code" row.

| Rule | Description | Layer | Severity |
|---|---|---|---|
| S2 | Input matches `schemas/rr_input.schema.json` | Input schema | Error (no model call) |
| S1 | Output matches `schemas/rr_output.schema.json` | Output schema | Error |
| R1 | Output `story_id` equals input `story_id` | Code | Error |
| R2 | Every finding's `ac_id` is the id of an input acceptance criterion | Code | Error |
| R3 | Every finding's `quote` appears in the text of the AC named by its `ac_id` (case-insensitive, whitespace collapsed, curly quotes normalised to straight quotes) | Code | Error |
| R4 | Finding ids are unique, use the story number (US-420 -> F-420-NN) and run 01, 02, ... without gaps | Code | Error |
| R5 | Number of findings <= `max_findings` (default 10) | Code | Error |
| R6 | `needs_clarification` => `findings` empty and at least one open question; `ok` => `open_questions` empty | Code | Error |
| R7 | Every finding's `category` is in `focus` (default: all five) | Code | Error |
| Q1 | A question or explanation contains a number with a unit (seconds, %, characters, $...) that does not appear in the story: the agent may be proposing an answer | Code | Warning |
| Q2 | Two findings share the same `ac_id` and the same `quote` (possible duplicate) | Code | Warning |
| Q3 | Findings are relevant, correctly categorised and complete compared with the tester's own review | Human review | Error at review |

Order of layers: S2 -> model call -> parse -> S1 -> R1..R7 (only if S1 passed) -> Q1..Q2 warnings -> human (Q3, Wednesday checklist).
R6 could be written in the schema with if/then; we keep it in code so that every cross-field rule is in one place.
