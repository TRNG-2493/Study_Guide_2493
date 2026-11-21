# Exemplar Answers (instructors only)

A model answer for calibration, not a key. Trainees will pick different use cases, scores and wording. Grade the reasoning, the verification story and the evidence, not agreement with this file.

## Stage 2: expected tool choices for the brief's pain points

| Pain point | Expected choice | Deciding property |
|---|---|---|
| 1 Vague user stories | GenAI | language understanding; a tester checks a short list of questions |
| 2 Test design under time pressure | GenAI (with BVA review) | language plus code; pytest and the docstring make it checkable |
| 3 Repetitive data files | GenAI, checked by a rules script | rules are known, so every row can be checked by code |
| 4 Page objects | GenAI (IDE assistant) with review | code boilerplate; must run against the real page |
| 5 Nightly failures, 3-10 a day | GenAI, as a hypothesis only | language summary; verifying needs the log line; redaction needed |
| 6 Inconsistent bug reports | GenAI | rewriting text; reporter confirms steps |
| 7 Friday PO summary | GenAI, low priority | numbers must be checked; risk of reassuring omissions |
| 8 2,000 unlabelled historical failures | **Classic NLP / unsupervised ML**: TF-IDF + clustering | no labels, large volume, repeatable, offline |
| 9 Flaky tests with 6 months labelled history | **Classic supervised ML**: classification | labels exist; tabular history; repeatable scores |
| 10 Username max 16 characters | **No AI**: parametrised pytest test | deterministic rule |

Accept "GenAI to explain clusters after classic NLP groups them" for 8 if the grouping itself is classic. Do not accept GenAI as the primary tool for 9 or 10.

## Selected use cases (exemplar ranking from `rank_use_cases.py`)

### 1. Review new user stories for ambiguity before automation (26)
- **Part / STLC:** checkout stories US-101 to US-103; requirements analysis.
- **Claude produces:** a list of ambiguities with one clarifying question each.
- **Value:** gaps found before any test or code is written; faster refinement meetings.
- **Why GenAI:** needs language understanding of free text; no labelled data exists; no rule can list "what is missing".
- **Verifier and check:** the story's assigned tester reads each question against the story (about 5 minutes), keeps the relevant ones and sends them to the product owner, who answers.
- **What could go wrong:** (a) states an invented rule as fact, such as "promo codes expire after 30 days": hallucination, plausible next tokens with no fact-check; (b) misses a domain gap such as the minimum-spend rule hinted at in `bug-notes.txt`: no access to the team's context beyond the prompt; (c) a different question set on each run: non-determinism from sampling.
- **Data sensitivity:** stories only; never paste customer tickets or internal URLs.
- **Measure after a month:** share of questions kept by the tester; number of story defects found after automation started.

### 2. Draft boundary and negative tests for new business rules (26)
- **Part / STLC:** `shipping.py` unit tests; test design and automation.
- **Claude produces:** a pytest file.
- **Value:** faster first draft, broader negative cases.
- **Why GenAI:** produces code and test ideas from a written rule; a plain parametrised test would still need someone to design the cases.
- **Verifier and check:** the tester runs pytest, then reviews each test against the six docstring sentences and a BVA list (74.99, 75.00, express on a free order, unknown country, negative subtotal). About 10 minutes.
- **What could go wrong:** wrong expected result (express on a free order stays free) and invented requirement (case-insensitive country code): hallucination; missing boundaries: next-token prediction favours common examples (100, 50) over boundaries; tests that pass but prove little.
- **Data sensitivity:** business rule code only.
- **Measure:** boundary defects found per sprint; share of AI tests kept after review.

### 3. Generate synthetic registration data for data-driven tests (24)
- **Part / STLC:** `data/` CSV files for the registration tests; test data.
- **Claude produces:** a CSV with an expected-valid label per row.
- **Value:** varied data instead of `user1`, `user2`; no real personal data.
- **Why GenAI:** fast variety, including awkward-but-valid values; classic ML has nothing to learn from here.
- **Verifier and check:** a 20-line rules checker (`checks/check_registration_data.py`) flags every mislabelled row in seconds; the tester reviews names and domains for anything that looks real.
- **What could go wrong:** mislabelled boundary rows (3-character usernames marked valid): counting errors, tokens are not characters; real-looking domains such as gmail.com: plausible continuation from training data; header drift breaks the loader: non-determinism.
- **Data sensitivity:** reserved `example.com`/`example.org` domains only; invented people.
- **Measure:** mislabelled rows caught per batch; time to produce a new data file.

### Rejected candidates
- Pain point 10 (username length): No AI. A parametrised test at 16 and 17 characters is deterministic, free and exact.
- Pain point 8 (2,000 unlabelled failures): Classic NLP, TF-IDF and clustering. Cheap, repeatable and runs offline every night.
- Auto-approve releases: unverifiable and severe if wrong; GenAI assists judgement, it does not replace it.

## Typical Claude behaviours to expect in the evidence logs

| Probe | Common good output | Common faults trainees should catch |
|---|---|---|
| US-101 review | expiry definition, time zone, guest users, replacing a code, error message | stating an expiry period or minimum spend as fact; missing "used at the exact expiry moment" |
| `shipping.py` tests | flat rates, CA, unknown country | no 74.99 / 75.00 pair; express on a free order asserted as 0; case-insensitive country asserted; `== 0` on floats without thought |
| Registration CSV | mostly valid structure | 3-character usernames or underscores marked valid; gmail-style domains; extra prose around the CSV; header changed |
| CI failures | Apply button disabled, not a timeout problem | "increase the timeout"; claiming the search failure is definitely a product bug (the requirement for the message text is not in the brief, so it is a question); calling 21 vs 20 a flaky test |
| Bug notes | a tidy structured report | inventing exact amounts, browser versions or a minimum-spend value of $60 stated as fact; severity overstated; merging the two separate issues into one report |
| Source request | real ISTQB or vendor documentation pages | non-existent URLs or titles, or real pages that do not say what was claimed |
