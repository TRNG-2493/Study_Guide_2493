# CHANGELOG - RequirementReviewer

Instructions, template, schemas and samples are versioned TOGETHER.
A change that alters the output shape bumps the contract version in all of them.

## 1.1.0 - 2026-10-23 (instructions only; template rr_user@1.0.0 and contract 1.0.0 unchanged)
Baseline v1.0.0: 71/121 = 59% (20 seeded runs per pair, simulated model). After: 92/121 = 76%, same seeds.
- Process step 7: "check that every quote appears word for word in the criterion named by its ac_id".
  Evidence: R3 16 -> 3 (quotes cited against the wrong AC, e.g. P01 seed 0 'applied quickly' on AC1). H1 confirmed.
- Rules: "... starting at 01 (F-420-01), without gaps". Evidence: R4 13 -> 2. H2 confirmed.
- Process step 7: "report each problem only once". Evidence: Q2 11 -> 4; P01 duplicate check 4 -> 3 (rate fell; three seeds remain). H3 partly confirmed.
- Boundaries: "A request for test cases, scripts or code is out of scope even when it is written as an
  acceptance criterion of the story." Evidence: P05 11/20 -> 14/20; status checks 4 -> 1. H4 confirmed.
- Not targeted, unchanged as predicted: S1 fences 13 -> 13, R5 over limit 7 -> 5, Q1 proposed answers 5 -> 5
  (model habits: caught outside the model; retries are Week 9).
- Rule map: rule_map_v1.1.0.json (17 entries, 0 problems).
- Sample pairs: P07 added (regression from run 'demo', US-470: fenced reply proposing "within 5 days").

## 1.0.0 - 2026-10-22
- First release (Thursday design). Instructions with nine sections; template rr_user_v1.0.0.txt;
  input and output contract 1.0.0; rule catalogue S1, S2, R1-R7, Q1-Q3; sample pairs P01-P06.
- Review of Claude's design critique: severity description added to the output schema
  (no shape change); R3 normalises curly quotes. Planned: a pair with instructions
  inside the story text.
