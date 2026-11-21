# Human review of Claude's output (exemplar, built from the backup replies)

## Dry run on US-420
- `python design_lab.py check-output evidence/dryrun.us420.txt`: PARSE "NOT pure JSON - Output rule broken (prose or fence around it)", then S1 PASS.
- Rule catalogue applied by hand:

| Rule | Pass/Fail | Evidence (quote the reply) |
|---|---|---|
| R1 | Pass | story_id "US-420" |
| R2 | Pass | AC1, AC1, AC2, AC3, AC5 all exist |
| R3 | **Fail** | F-420-02 quote "code must be uppercase" is not in AC1 (invented requirement presented as a quote) |
| R4 | Pass | F-420-01..05, unique, story number 420 |
| R5 | Pass | 5 findings <= default 10 |
| R6 | Pass | status ok, open_questions empty |
| R7 | Pass | all categories in the default focus |
| Q1 | **Warning** | F-420-05 "2 seconds" in explanation and question: the agent proposes an answer (golden rule) |
| Q2 | Pass | no duplicate ac_id + quote |

- Our judgement: F-420-01, 03, 04 correct; F-420-02 wrong (ungrounded); F-420-05 right problem, bad question (should ask, not suggest). Missing compared with P01: shipping and tax in "order total", and spaces or dashes in the code.
- Design change caused: none to the contract. The fence confirms the Output rule needs the parse step on Friday. Q1 stays a warning, not an error, because "16 characters" is a legitimate number in the story; Friday's check must compare against the story's own numbers.

## Design critique
| # | Claude's critique (short quote) | Accept / Reject | Reason | File changed |
|---|---|---|---|---|
| 1 | "add a suggested_ac field" | Reject | Breaks "ask, never answer": a suggested rewrite is an answer the PO has not agreed | - |
| 2 | "curly versus straight quotes ... R3 fail on correct findings" | Accept | Real risk; normalise quotation marks before comparing | rules.md R3 wording (no contract change) |
| 3 | "severity not described in the schema" | Accept | Consumers read the schema; add a description | rr_output.schema.json (description only: patch-level, contract stays 1.0.0) |
| 4 | "no sample pair with instructions inside the story" | Accept as a Friday task | Valid gap; prompt injection is Week 10, but a simple pair is cheap | CHANGELOG note, pair planned |
| 5 | "maximum of 5" | Reject | 10 is the default; 20 is a ceiling a caller must choose; P06 shows the limit works | - |
| 6 | "mention that it also prioritises" | Reject | Would add an "and"; severity is part of each finding, not a second job | - |
