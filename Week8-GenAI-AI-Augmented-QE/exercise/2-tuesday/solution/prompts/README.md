# ShopFront Prompt Library

Prompts the ShopFront QE team uses with Claude for test design and debugging.
Every prompt is a versioned file. Use the latest version unless its notes say otherwise.

## How to use a prompt
1. Open the latest version and copy the text inside its `## Prompt` block.
2. Paste it into a **fresh** Claude chat with any material it asks for. Synthetic or approved material only.
3. Save the reply in `evidence/` and run the "Check with" command from the header.
4. Review the reply yourself. A passing check is a first filter, not approval.

## Index

| ID | File (latest) | Area | Technique | Output | How the output is checked |
|---|---|---|---|---|---|
| TD-1 | `test-design/shipping-test-ideas.v5.md` | test design | EP, BVA, done-criteria, assumptions | Markdown table + assumptions | `tools/score_reply.py` (12 criteria), then recompute every expected value with `shipping_cost` |
| TD-2 | `test-design/shipping-cases-json.v1.md` | test design | format locking, EP, BVA | JSON array | `tools/load_shipping_cases.py`, then pytest `--cases`, then case-by-case review |
| TD-3 | `test-design/registration-gherkin-fewshot.v1.md` | test design | few-shot, BVA | Gherkin feature | `tools/check_gherkin.py`, then read boundaries and rules |
| DB-1 | `debugging/structured-failure-analysis.v1.md` | debugging | structured request, hypotheses first | ranked hypotheses + fix | run the confirmation command yourself; `git diff --stat` shows no test change |
| DB-2 | `debugging/ci-failure-triage.v1.md` | debugging | format locking, evidence quoting | JSON array | `tools/check_triage.py` against the log, then a human judges each category |

## Rules for this library
- One change per new version. Keep old versions; never edit a version that has evidence.
- Commit message format: `prompts: <what changed> (<ID> v<N>)`.
- Never paste real customer data, credentials, tokens, cookies or internal URLs. Redact real logs first.
- Never accept a reply that changes a test's expected value, adds skip/xfail or loosens an assertion unless the requirement changed.
- Any quoted log line, method, flag or option in a reply is checked against the source before anyone acts on it.
- A model or Claude version change means re-running every prompt's evidence before relying on it.
- "Make this failing test pass" is deliberately NOT in this library: it optimises for green, not for correct (see evidence/make-it-pass.weakening-trap.txt).
