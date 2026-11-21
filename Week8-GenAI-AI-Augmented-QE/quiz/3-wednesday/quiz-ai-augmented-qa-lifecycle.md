# Daily Knowledge Check: Week 8 Wednesday - AI-Augmented QA Lifecycle

This check covers AI within the QA lifecycle, AI-assisted requirements analysis, AI-generated test cases, AI-generated test data, AI-assisted automation development, human validation of AI output, and responsible use of AI in QE. Try each question on your own first, then open the solution to check your reasoning.

---

## Part 1: Multiple Choice

### 1. At which level of AI involvement does the AI produce a first draft of a real artifact that a human reviews and approves before use?

- [ ] A) Assist
- [ ] B) Augment
- [ ] C) Autonomous
- [ ] D) Human-out-of-the-loop

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Augment

**Explanation:** Augment = the AI drafts real artifacts (test cases, data, code) and the human reviews and approves each one. This is the human-in-the-loop (HITL) level.
- **Why others are wrong:**
  - A) Assist means the AI only suggests; the human does the work.
  - C) Autonomous means the AI produces and uses artifacts without per-item review.
  - D) No human review at all, which is rarely appropriate in QA.

</details>

### 2. Why do most QA teams work at the assist and augment levels rather than autonomous?

- [ ] A) Autonomous AI is illegal
- [ ] B) An LLM is not a test oracle, it is confidently wrong in the same style as when it is right, and accountability stays with people
- [ ] C) Autonomous AI is too slow
- [ ] D) Assist and augment are cheaper to license

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An LLM is not a test oracle, it is confidently wrong in the same style as when it is right, and accountability stays with people

**Explanation:** "The AI said it was fine" is not an acceptable answer to a manager, customer or regulator.
- **Why others are wrong:**
  - A) It is not universally illegal.
  - C) Speed is not the concern.
  - D) Licensing cost is not the reason given.

</details>

### 3. Four unreviewed AI steps are each 90% correct. Roughly what share of outputs is correct at the end?

- [ ] A) 90%
- [ ] B) 81%
- [ ] C) About 66%
- [ ] D) 36%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) About 66%

**Explanation:** 0.9 × 0.9 × 0.9 × 0.9 = 0.6561. Errors compound across hand-overs; a checkpoint after each step (raising each to 99%) gives about 96%.
- **Why others are wrong:**
  - A) That is one step.
  - B) That is two steps.
  - D) That subtracts 10% four times from 76%, which is not how probabilities combine.

</details>

### 4. What is the pattern described for defect reports and summary reports?

- [ ] A) AI writes, AI checks, human signs
- [ ] B) AI drafts, code checks the facts, human judges
- [ ] C) Human drafts, AI judges
- [ ] D) Code drafts, AI approves

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) AI drafts, code checks the facts, human judges

**Explanation:** In `defect_draft.py`, code caught the invented browser version "129"; a human still judged severity and whether it was really a defect.
- **Why others are wrong:**
  - A) AI checking AI with no human is an anti-pattern.
  - C) and D) These reverse the roles.

</details>

### 5. What does the rule "**let code count, let AI write**" mean?

- [ ] A) Let the AI count tests because it is faster
- [ ] B) Compute every number with code, give the numbers to the AI as facts, and check the numbers in its text
- [ ] C) Never use AI for reports
- [ ] D) Let code write the narrative

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Compute every number with code, give the numbers to the AI as facts, and check the numbers in its text

**Explanation:** In the summary example, the narrative claimed 6 passed and 75%, but the data said 5 passed and 62% because one test was skipped.
- **Why others are wrong:**
  - A) LLMs are poor at counting; that is the whole point.
  - C) AI can write the narrative well.
  - D) The AI writes the words; code does the numbers.

</details>

### 6. In failure triage with TF-IDF and k-means, why are test names removed before clustering?

- [ ] A) Names are too long to process
- [ ] B) So grouping depends on what went wrong, not on what the test is called
- [ ] C) k-means cannot read underscores
- [ ] D) To reduce the number of clusters to one

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) So grouping depends on what went wrong, not on what the test is called

**Explanation:** Otherwise all `test_coupon_*` tests might cluster together just because of their names.
- **Why others are wrong:**
  - A) Length is not the problem.
  - C) Tokenisation is controlled by `token_pattern`, not underscores.
  - D) The number of clusters is set by `n_clusters`.

</details>

### 7. Which statement about clustering failures is correct?

- [ ] A) k-means decides how many root causes exist
- [ ] B) A cluster is a hypothesis to investigate, not a diagnosis; clustering groups symptoms, not causes
- [ ] C) Clustering replaces human triage entirely
- [ ] D) An LLM is always better than k-means for clustering

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A cluster is a hypothesis to investigate, not a diagnosis; clustering groups symptoms, not causes

**Explanation:** Three timeouts may have three different causes. A human decides which clusters are product defects, environment problems or test problems.
- **Why others are wrong:**
  - A) You choose k.
  - C) A human still decides what each cluster means.
  - D) Classic ML is cheaper, faster and more predictable for this job.

</details>

### 8. **Backward** traceability (test → requirement) catches which AI mistake?

- [ ] A) Coverage gaps
- [ ] B) Invented requirements, such as a test tracing to a non-existent AC5
- [ ] C) Flaky tests
- [ ] D) Slow tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Invented requirements, such as a test tracing to a non-existent AC5

**Explanation:** Forward traceability (requirement → tests) catches coverage gaps such as US-205-AC4 with no test.
- **Why others are wrong:**
  - A) That is forward traceability.
  - C) and D) Traceability does not detect flakiness or speed.

</details>

### 9. Which lifecycle anti-pattern describes pasting one AI step's output straight into the next with no review?

- [ ] A) AI as oracle
- [ ] B) Copy-paste pipeline
- [ ] C) Volume over value
- [ ] D) Leaking data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Copy-paste pipeline

**Explanation:** Errors propagate and compound. Better practice: a human checkpoint at every hand-over.
- **Why others are wrong:**
  - A) That is taking expected results from the AI without checking the requirement.
  - C) That is generating many tests nobody reads.
  - D) That is pasting real data or secrets into tools.

</details>

### 10. Requirements analysis reviews a document without running code. What kind of testing is this?

- [ ] A) Dynamic testing
- [ ] B) Static testing (and the purest form of shift-left)
- [ ] C) Performance testing
- [ ] D) Regression testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Static testing (and the purest form of shift-left)

**Explanation:** You cannot get further left than the requirement itself; a misunderstanding caught here costs a five-minute conversation.
- **Why others are wrong:**
  - A) Dynamic testing runs the software.
  - C) and D) These require executing code.

</details>

### 11. US-310 AC4 says "The address form should be fast and user-friendly." Which defect categories apply?

- [ ] A) CONTRADICTION only
- [ ] B) UNMEASURABLE ("fast") and AMBIGUOUS ("user-friendly")
- [ ] C) None; it is a good criterion
- [ ] D) INCOMPLETE only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) UNMEASURABLE ("fast") and AMBIGUOUS ("user-friendly")

**Explanation:** "Fast" has no number; "user-friendly" means different things to different people; "should" may mean optional. Three weak words in one sentence.
- **Why others are wrong:**
  - A) It does not conflict with another requirement.
  - C) It has no objective pass/fail.
  - D) Incompleteness is not its main defect.

</details>

### 12. What is the **golden rule** of AI-assisted requirements analysis?

- [ ] A) Let the AI fix every vague requirement with a number
- [ ] B) The AI may find problems and ask questions; it may not answer them. Any proposed value must be confirmed by the PO
- [ ] C) Never use AI for requirements
- [ ] D) Accept all AI findings without checks

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The AI may find problems and ask questions; it may not answer them. Any proposed value must be confirmed by the PO

**Explanation:** If "the form must load within 2 seconds" slides in unchallenged, an invented requirement enters the test basis and every downstream test enforces it.
- **Why others are wrong:**
  - A) That is exactly the invented-answer danger.
  - C) AI is genuinely useful for finding gaps.
  - D) Findings must be checked (grounding, etc.).

</details>

### 13. What does the **grounding check** in `check_findings.py` verify?

- [ ] A) That the JSON is valid
- [ ] B) That the text the AI quoted actually appears in the story
- [ ] C) That the story has exactly four ACs
- [ ] D) That the PO has answered every question

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) That the text the AI quoted actually appears in the story

**Explanation:** Finding #6 quoted "must load in under 2 seconds", which is not in the story; the model invented a requirement and reported it as a quote.
- **Why others are wrong:**
  - A) JSON validity is checked by parsing.
  - C) The AC check verifies only that the named AC exists.
  - D) Answers are tracked in the question log.

</details>

### 14. Why is the potential contradiction between US-101 AC2 and AC3 important?

- [ ] A) Both ACs use the same message
- [ ] B) A "Your account is locked" message would reveal that an email is registered, undoing AC2's protection against account enumeration
- [ ] C) AC3 locks after only one attempt
- [ ] D) AC2 has no message at all

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A "Your account is locked" message would reveal that an email is registered, undoing AC2's protection against account enumeration

**Explanation:** Unknown emails never lock, so a lock message leaks account existence. The PO (and security team) must decide the message strategy, not the tester or the AI.
- **Why others are wrong:**
  - A) The problem is the *different* lock message.
  - C) AC3 says 5 consecutive failures.
  - D) AC2 specifies "Invalid email or password".

</details>

### 15. What is an **orphan** test condition, and what must you NOT do with one?

- [ ] A) A condition with two ACs; delete it
- [ ] B) A condition tracing to an AC that does not exist; you must not quietly keep a test for an unagreed rule
- [ ] C) A condition without an ID; renumber it
- [ ] D) A passing condition; skip it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A condition tracing to an AC that does not exist; you must not quietly keep a test for an unagreed rule

**Explanation:** The three honest options: delete it, turn it into a PO question, or (if the PO agrees) add a new AC so it has a real parent.
- **Why others are wrong:**
  - A), C), D) None of these defines an orphan.

</details>

### 16. Why should you review a story yourself **before** reading the AI's review?

- [ ] A) To save tokens
- [ ] B) To avoid anchoring and to have a reference for judging what the AI missed
- [ ] C) Because the AI needs your review as input
- [ ] D) It is required by INVEST

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) To avoid anchoring and to have a reference for judging what the AI missed

**Explanation:** Once you read the AI's list it is hard to think beyond it. In the example, the AI missed ZIP codes with leading zeros.
- **Why others are wrong:**
  - A) Your own review costs no tokens but that is not the reason.
  - C) The AI does not use your review.
  - D) INVEST is a story-quality checklist, not a review order.

</details>

### 17. What is the difference between a **test condition** and a **test case**?

- [ ] A) They are identical
- [ ] B) A condition is *what* to test; a test case is *how*: preconditions, data, steps and an observable expected result
- [ ] C) A condition is automated; a case is manual
- [ ] D) A case is a one-line idea; a condition is a full script

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A condition is *what* to test; a test case is *how*: preconditions, data, steps and an observable expected result

**Explanation:** Analogy: the condition is "make a cake for six"; the test case is the recipe. Two testers following the same case should reach the same verdict.
- **Why others are wrong:**
  - A) The lesson defines them carefully as different.
  - C) Either can be manual or automated.
  - D) This reverses them.

</details>

### 18. In the AI test case draft, TC-04 expected "Invalid coupon" but AC3 says "Coupon code not recognised". What flaw is this?

- [ ] A) Near-duplicate
- [ ] B) Message drift
- [ ] C) Happy-path bias
- [ ] D) Untraced case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Message drift

**Explanation:** The model paraphrases unless told to copy exactly. Every quoted message must appear word for word in the story. A UI test with the paraphrase fails on correct software.
- **Why others are wrong:**
  - A) TC-04 tests a distinct condition.
  - C) It is a negative case.
  - D) It traces to AC3.

</details>

### 19. Why should you **retire** a bad test ID rather than renumber the suite?

- [ ] A) Renumbering is slower
- [ ] B) IDs appear in bug reports, run histories and automation code; renumbering makes old references point to the wrong test
- [ ] C) Test management tools forbid renumbering
- [ ] D) Retired IDs improve coverage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) IDs appear in bug reports, run histories and automation code; renumbering makes old references point to the wrong test

**Explanation:** New cases get new numbers (e.g. TC-08 for AC4).
- **Why others are wrong:**
  - A), C), D) None of these is the reason.

</details>

### 20. Why must `oracle_total` be written by a human from the story rather than by the same AI that drafted the tests?

- [ ] A) Humans write faster code
- [ ] B) The oracle must be independent; if the same AI wrote both, a shared misunderstanding would make the check agree with itself
- [ ] C) AIs cannot use `Decimal`
- [ ] D) It is a legal requirement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The oracle must be independent; if the same AI wrote both, a shared misunderstanding would make the check agree with itself

**Explanation:** A human-written oracle based on the story is a separate source of truth.
- **Why others are wrong:**
  - A) Speed is irrelevant.
  - C) AIs can write Decimal code.
  - D) No such law is cited.

</details>

### 21. A draft suite reports 75% AC coverage (3 of 4 ACs). What does that mean?

- [ ] A) 75% of the code is tested
- [ ] B) One quarter of the requirement has no test at all, which is a serious finding
- [ ] C) The suite is good enough to release
- [ ] D) 75% of tests passed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) One quarter of the requirement has no test at all, which is a serious finding

**Explanation:** AC coverage counts links, not quality. Even 100% would not prove good testing (TC-05 counted toward AC1 while testing an invented rule).
- **Why others are wrong:**
  - A) It is requirement coverage, not code coverage.
  - C) A completely untested AC is a red flag.
  - D) Coverage says nothing about pass rates.

</details>

### 22. Which test data source is fast, contains no real people and can target any edge case, but may be wrong if the generator is wrong?

- [ ] A) Production copy
- [ ] B) Masked production data
- [ ] C) Hand-crafted data
- [ ] D) Synthetic data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Synthetic data

**Explanation:** AI-generated data and Faker data are both synthetic. Most teams mix hand-crafted boundaries, synthetic variety and (only where approved) masked production data.
- **Why others are wrong:**
  - A) Contains real personal data.
  - B) Masking can be incomplete and needs approval.
  - C) Precise but slow and limited at volume.

</details>

### 23. What is the "**one change at a time**" principle in test data design?

- [ ] A) Change every field in each row for maximum variety
- [ ] B) Start from a known-valid base row and change exactly one field per row, so a rejection can only be caused by that field
- [ ] C) Run one test per day
- [ ] D) Generate one row per category

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Start from a known-valid base row and change exactly one field per row, so a rejection can only be caused by that field

**Explanation:** Changing the ZIP and phone together would hide which rule fired.
- **Why others are wrong:**
  - A) That makes failures impossible to diagnose.
  - C) and D) Unrelated to the principle.

</details>

### 24. Complete the core rule for AI-generated test data: "The AI ___, code ___, checks ___."

- [ ] A) writes / runs / pass
- [ ] B) designs / generates / prove
- [ ] C) tests / fixes / ship
- [ ] D) counts / labels / approve

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) designs / generates / prove

**Explanation:** AI for ideas (categories, tricky values); seeded code for volume and repeatability; independent checks to prove the data is right.
- **Why others are wrong:**
  - A), C), D) Not the phrase used, and D gives AI the jobs it is worst at.

</details>

### 25. Why does `spec_expectation` use `[0-9]` instead of `\d` in its regex?

- [ ] A) `\d` is slower
- [ ] B) In Python 3, `\d` matches any Unicode digit (e.g. Arabic-Indic digits), while `[0-9]` matches only ASCII 0-9
- [ ] C) `\d` does not exist in Python
- [ ] D) `[0-9]` also matches letters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) In Python 3, `\d` matches any Unicode digit (e.g. Arabic-Indic digits), while `[0-9]` matches only ASCII 0-9

**Explanation:** This exact detail hid a real bug: `"١٢٣٤٥".isdigit()` is `True`, so the validator accepted a non-ASCII ZIP code.
- **Why others are wrong:**
  - A) Speed is not the concern.
  - C) `\d` exists.
  - D) `[0-9]` matches only digits.

</details>

### 26. Why should you never use payment card numbers invented by an AI, even if they pass the Luhn check?

- [ ] A) Luhn-valid numbers are always fake
- [ ] B) An invented number might belong to a real person's card; use the provider's official test cards (e.g. Stripe's 4242 4242 4242 4242)
- [ ] C) AI cannot produce 16-digit numbers
- [ ] D) Luhn is not used by real cards

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An invented number might belong to a real person's card; use the provider's official test cards (e.g. Stripe's 4242 4242 4242 4242)

**Explanation:** Official test cards only work in the provider's test mode.
- **Why others are wrong:**
  - A) Real cards are Luhn-valid too.
  - C) It produces them easily; the two "valid Visa" examples simply failed Luhn.
  - D) Card numbers use Luhn as a check digit.

</details>

### 27. Why is `"locked_until": "2025-06-01T10:15:00"` poor precondition data?

- [ ] A) It uses the wrong date format
- [ ] B) It is hard-coded, so the account is "locked" only on the day it was written and "expired" afterwards; the test silently changes meaning
- [ ] C) Timestamps cannot be stored in JSON
- [ ] D) It is too precise

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is hard-coded, so the account is "locked" only on the day it was written and "expired" afterwards; the test silently changes meaning

**Explanation:** Write it relative to now, e.g. `now + timedelta(minutes=15)`, with `now` passed in as a parameter.
- **Why others are wrong:**
  - A) ISO format is fine.
  - C) JSON can store strings.
  - D) Precision is not the issue.

</details>

### 28. Which three pieces of context does an AI need to write good automation code for your framework?

- [ ] A) The browser version, the OS and the IDE
- [ ] B) The reviewed test case, a trimmed DOM snippet and your team conventions
- [ ] C) The full repository, the CI logs and the production database
- [ ] D) Only the test title

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The reviewed test case, a trimmed DOM snippet and your team conventions

**Explanation:** Without the DOM, the AI guesses locators like `#username`; without the test case, it invents the oracle; without conventions, it uses whatever is most common.
- **Why others are wrong:**
  - A) Useful details, but not the three key pieces.
  - C) Far too much, and the production database is sensitive.
  - D) Far too little.

</details>

### 29. The AI draft `test_login` passed even though login never happened. What were the two reasons?

- [ ] A) The password was wrong and the browser crashed
- [ ] B) `page.click("text=Log in")` clicked the `<h1>Log in</h1>` heading, and `assert page.locator("h1").is_visible()` is true on both pages
- [ ] C) The test was skipped
- [ ] D) The page loaded too quickly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `page.click("text=Log in")` clicked the `<h1>Log in</h1>` heading, and `assert page.locator("h1").is_visible()` is true on both pages

**Explanation:** The page-level click is not strict and picked the first match. The vague assertion cannot fail on a login defect.
- **Why others are wrong:**
  - A) The password was the correct one, and nothing crashed.
  - C) It ran and passed.
  - D) The page answers after a delay; the issue is the locator and assertion.

</details>

### 30. Which is the **highest-priority** locator according to Playwright's user-facing guidance?

- [ ] A) `page.locator("xpath=//form/input[1]")`
- [ ] B) `page.get_by_test_id("total")`
- [ ] C) `page.get_by_role("button", name="Log in")`
- [ ] D) `page.locator(".css-1x2y3z")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `page.get_by_role("button", name="Log in")`

**Explanation:** Priority: role → label → other visible text → test ID → CSS/XPath as a last resort. Role locators test what users and assistive technology experience.
- **Why others are wrong:**
  - A) and D) Positional XPath and auto-generated classes are brittle last resorts.
  - B) Test IDs are stable but rank below role and label.

</details>

### 31. What is the main difference between `inner_text()` and `expect(locator).to_have_text(...)`?

- [ ] A) No difference
- [ ] B) `inner_text()` reads once immediately (possibly stale); `expect(...).to_have_text` is a web-first assertion that retries until the text matches or a timeout expires
- [ ] C) `expect` is only for Selenium
- [ ] D) `inner_text()` waits up to 5 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `inner_text()` reads once immediately (possibly stale); `expect(...).to_have_text` is a web-first assertion that retries until the text matches or a timeout expires

**Explanation:** The draft read `''` because the page answers after 300 ms. Web-first assertions handle async pages without sleeps (default timeout 5 seconds).
- **Why others are wrong:**
  - A) The behaviours differ crucially.
  - C) `expect` is from `playwright.sync_api`.
  - D) It is the `expect` assertion that waits.

</details>

### 32. Why might an AI-generated fixture with `scope="session"` break the lockout test suite?

- [ ] A) Session fixtures are slower
- [ ] B) Tests would share state, so five failed logins in one test could leave the account locked for the next, depending on test order
- [ ] C) Session fixtures cannot use Playwright
- [ ] D) pytest forbids session scope

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Tests would share state, so five failed logins in one test could leave the account locked for the next, depending on test order

**Explanation:** Keep page-level fixtures at the default function scope unless you have a clear reason.
- **Why others are wrong:**
  - A) They are usually faster, which is why AI suggests them.
  - C) and D) Both are false.

</details>

### 33. In an AI-generated data-driven test, which part can you largely trust the AI with?

- [ ] A) The expected results in each row
- [ ] B) The parametrize plumbing (decorator, parameter names, ids, function signature)
- [ ] C) The boundary values
- [ ] D) The requirement interpretation

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The parametrize plumbing (decorator, parameter names, ids, function signature)

**Explanation:** The rows (inputs and expected results) are the test oracle and must be recomputed by a human. Recomputing each value is "the most valuable minute of the review".
- **Why others are wrong:**
  - A), C), D) These are exactly the parts a human must check.

</details>

### 34. What is a **sabotage check**?

- [ ] A) Deleting flaky tests
- [ ] B) Deliberately breaking the feature (or expectation) to confirm the test fails
- [ ] C) Running tests in production
- [ ] D) A security penetration test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Deliberately breaking the feature (or expectation) to confirm the test fails

**Explanation:** On the broken login page, the draft's `h1` check still PASSED, while the reviewed check FAILED, proving only the reviewed test had teeth.
- **Why others are wrong:**
  - A) Unrelated.
  - C) Never part of this technique.
  - D) Security testing is different.

</details>

### 35. What is **automation bias**, with an error of **omission** example?

- [ ] A) Preferring manual tests; writing too many tests
- [ ] B) Favouring an automated system's suggestions and under-checking them; not noticing AC4 has no test because the AI did not mention it
- [ ] C) Bias in training data; a model preferring English names
- [ ] D) Flaky automation; a test that times out

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Favouring an automated system's suggestions and under-checking them; not noticing AC4 has no test because the AI did not mention it

**Explanation:** An error of **commission** would be copying the AI's expected total of 44.99 for a $49.99 order.
- **Why others are wrong:**
  - A) The opposite tendency.
  - C) That is data bias, a different concept.
  - D) That is flakiness.

</details>

### 36. Why must you NOT use the application's actual output as the oracle for AI expected results?

- [ ] A) The app is too slow
- [ ] B) The test would then agree with any defect in the app; the oracle must come from the requirement or its owner
- [ ] C) Apps never return values
- [ ] D) It is not allowed by pytest

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The test would then agree with any defect in the app; the oracle must come from the requirement or its owner

**Explanation:** A test whose expected result came from the code cannot detect that the code is wrong.
- **Why others are wrong:**
  - A), C), D) None is the reason.

</details>

### 37. An AI test assumes coupon codes are case-insensitive, but the requirement is silent. What should the reviewer do?

- [ ] A) Flip the test to expect case-sensitivity
- [ ] B) Remove/park the test, log it as INVENTED_REQUIREMENT and send a question to the PO
- [ ] C) Keep it because it passes
- [ ] D) Mark it as a duplicate

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Remove/park the test, log it as INVENTED_REQUIREMENT and send a question to the PO

**Explanation:** Check C3 (Grounded) fails. "Fixing by flipping" just swaps one invented rule for another.
- **Why others are wrong:**
  - A) That is the "fixing by flipping" anti-pattern.
  - C) Passing does not make a rule agreed.
  - D) It is not a duplicate.

</details>

### 38. Which three factors make up the risk-based review score?

- [ ] A) Cost, speed and size
- [ ] B) Impact, likelihood the AI is wrong, and reach
- [ ] C) Lines of code, test count and coverage
- [ ] D) Priority, severity and age

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Impact, likelihood the AI is wrong, and reach

**Explanation:** Each rated 1-3 and multiplied (1 to 27). Reach matters because a wrong shared fixture or CI-gating test affects many people.
- **Why others are wrong:**
  - A), C), D) Not the factors used.

</details>

### 39. When sampling AI output at volume, what makes the sample trustworthy?

- [ ] A) Picking the items that look most unusual
- [ ] B) Always reviewing every high-risk item, choosing the rest randomly with a fixed seed, and escalating to full review if the sample is bad
- [ ] C) Reviewing only the first ten items
- [ ] D) Letting the AI choose which items to review

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Always reviewing every high-risk item, choosing the rest randomly with a fixed seed, and escalating to full review if the sample is bad

**Explanation:** Human picking is biased; a fixed seed makes the sample reproducible and auditable. Sampling is for mature, proven prompts only.
- **Why others are wrong:**
  - A) Biased selection.
  - C) Not random.
  - D) AI grading AI is an anti-pattern.

</details>

### 40. In responsible-use terms, why should every prompt be treated as a data transfer?

- [ ] A) Because prompts are encrypted
- [ ] B) Text leaves your machine and may be stored, logged, reviewed by vendor staff, processed by sub-processors or used for training, depending on the tool
- [ ] C) Because AI tools delete all inputs immediately
- [ ] D) Because prompts are free

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Text leaves your machine and may be stored, logged, reviewed by vendor staff, processed by sub-processors or used for training, depending on the tool

**Explanation:** Habit: treat every prompt as if you were emailing that text to an outside company.
- **Why others are wrong:**
  - A) Encryption in transit does not stop storage or use.
  - C) Retention varies by tool and contract.
  - D) Cost is irrelevant to privacy.

</details>

### 41. A SAVE10 bug report is internal. A colleague pastes a customer's card number into it. What is its data class now?

- [ ] A) Public
- [ ] B) Internal
- [ ] C) Confidential
- [ ] D) Restricted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Restricted

**Explanation:** Classification follows the most sensitive item. One card number makes the whole text restricted, which never goes into any AI tool.
- **Why others are wrong:**
  - A), B), C) All understate the sensitivity of card data.

</details>

### 42. What does `preflight.py` do with an **unknown** tool name, and what is this design called?

- [ ] A) Allows it; open-list
- [ ] B) Denies it by default; an allow-list
- [ ] C) Asks the AI whether it is safe; self-assessment
- [ ] D) Redacts and sends; best-effort

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Denies it by default; an allow-list

**Explanation:** `APPROVED_TOOLS.get(tool, set())` returns an empty set, so no classification is allowed. New, unreviewed tools are blocked until approved.
- **Why others are wrong:**
  - A) The opposite of the safe design.
  - C) and D) The code does neither.

</details>

### 43. You pasted a staging API key into a public chatbot. What should you do?

- [ ] A) Delete the chat and forget about it
- [ ] B) Report it and rotate the key the same day
- [ ] C) Ask the chatbot to forget the key
- [ ] D) Nothing; staging keys do not matter

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Report it and rotate the key the same day

**Explanation:** Once a secret has left its safe place you cannot know who has it; the only safe fix is to make it useless by issuing a new one and revoking the old.
- **Why others are wrong:**
  - A) and C) Neither guarantees removal from vendor systems.
  - D) The lesson explicitly says a staging test key pasted into a public chatbot should be rotated.

</details>

### 44. What are the four functions of the NIST AI Risk Management Framework?

- [ ] A) Plan, Do, Check, Act
- [ ] B) Govern, Map, Measure, Manage
- [ ] C) Identify, Protect, Detect, Respond
- [ ] D) Draft, Run, Evaluate, Refine

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Govern, Map, Measure, Manage

**Explanation:** For a QE team: policy and owners (Govern); data classes and risks (Map); correction rates and coverage checks (Measure); blocking tools, rotating keys (Manage).
- **Why others are wrong:**
  - A) The Deming cycle.
  - C) Part of a different (cybersecurity) framework.
  - D) The prompt-refinement loop.

</details>

---

## Part 2: True/False

### 45. True or False: AI may speed up a lifecycle phase, so it is acceptable to skip that phase's exit criteria when the AI's output looks good.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** AI can speed up a phase, but it must not let you skip its exit criteria.

</details>

### 46. True or False: In the risk table example, the human's overrides were kept separate from the AI's scores to create an audit trail.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `{**ai_suggested, **human_overrides}` merges them while both versions stay visible: "AI proposes, human adjusts with reasons".

</details>

### 47. True or False: The weak-word linter can detect missing information, such as an undefined error message for an empty required field.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A word list can only flag words that are *there*; it cannot notice what is *absent*. That is where an AI review is genuinely useful.

</details>

### 48. True or False: "Shoppers may not reuse their last 3 passwords" being flagged for "may" is an example of a linter false positive.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** It is a clear prohibition, yet the linter flags "may". "Search results appear in good time" is the matching false negative.

</details>

### 49. True or False: A `<TO CONFIRM: ...>` placeholder in a Gherkin scenario is a failure that should be removed by guessing a value.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is a feature: it makes the open question impossible to miss and impossible to automate by accident. A scenario with a placeholder is not ready for automation.

</details>

### 50. True or False: Faker data generated with the same seed is guaranteed identical across every Faker version.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** "Same seed, same data" holds for the same library versions; Faker warns results can change between versions, so pin the version.

</details>

### 51. True or False: The automated data checks in `check_data.py` caught that TD-02 used the real address of the White House.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The checks caught TD-02's wrong label but not the real address. Spotting real-looking data needs human review.

</details>

### 52. True or False: Playwright codegen is an AI tool that guesses locators.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Codegen records real interactions and takes locators from the live page; it observes rather than guesses. A good combination: record with codegen, then ask AI to refactor.

</details>

### 53. True or False: The `ast` review linter found every serious problem in the AI draft, including the `text=Log in` heading click.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It had important false negatives: problems about *meaning* (the heading click, the meaningless `h1` locator) need a human comparing the test to the requirement and DOM.

</details>

### 54. True or False: A high acceptance rate for AI output is meaningful only if the reviews behind it are real, not rubber-stamped.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** If reviewers rubber-stamp, acceptance goes up while quality goes down. Pair metrics with checklist records, second reviewers and escaped-defect tracking.

</details>

### 55. True or False: When designing a redactor, false negatives (missed data) are preferable to false positives (over-redaction).

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Prefer false positives: over-redaction is a safe failure; a missed value is a leak. Err on the side of redacting.

</details>

### 56. True or False: Labelling AI-assisted work is a confession that the work is lower quality.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Transparency tells the reader what kind of review it had. Well-reviewed, clearly labelled AI-assisted work is a sign of a mature team.

</details>

### 57. True or False: You should install a Python package as soon as an AI names it in a suggestion.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Models sometimes invent plausible package names that attackers can register with malicious code. Confirm the package exists, is the expected one and is maintained.

</details>

---

## Part 3: Code Prediction

### 58. What does this print?

```python
for n in range(1, 6):
    print(n, round(0.9 ** n * 100, 1))
```

Which line is printed for `n = 3`?

- [ ] A) `3 70.0`
- [ ] B) `3 72.9`
- [ ] C) `3 81.0`
- [ ] D) `3 27.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `3 72.9`

**Explanation:** 0.9³ = 0.729 → 72.9%. The full output is 90.0, 81.0, 72.9, 65.6, 59.0.
- **Why others are wrong:**
  - A) That subtracts 10 percentage points per step.
  - C) That is n = 2.
  - D) That is 0.3 × 0.9 × 100, an unrelated calculation.

</details>

### 59. The AI suggests likelihood 2 / impact 3 for US-205 Apply coupon. The tester overrides to likelihood 4 / impact 4. What is the new risk score, and where does coupon rank against Login (L=3, I=5)?

- [ ] A) 6; last
- [ ] B) 16; first, above Login (15)
- [ ] C) 8; third
- [ ] D) 15; tied with Login

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 16; first, above Login (15)

**Explanation:** Risk = L × I = 4 × 4 = 16. The coupon code was rewritten this sprint and coupons hit revenue: context the AI did not have.
- **Why others are wrong:**
  - A) That is the AI's original score (2 × 3).
  - C) and D) Wrong arithmetic.

</details>

### 60. What does `summary_report.py` compute for the pass rate when 5 of 8 tests passed?

```python
facts = {"total": 8, "passed": 5}
print(round(100 * facts["passed"] / facts["total"]))
```

- [ ] A) `62`
- [ ] B) `63`
- [ ] C) `62.5`
- [ ] D) `75`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `62`

**Explanation:** 5/8 = 62.5. Python's `round` uses banker's rounding (exact halves go to the nearest **even** number), so it returns 62. Decide your team's rounding rule in code.
- **Why others are wrong:**
  - B) That is round-half-up, which Python's `round` does not do here.
  - C) `round` with no digits returns an integer.
  - D) That was the AI narrative's wrong number.

</details>

### 61. In the traceability check, which line is printed for US-205-AC4 (no test case lists it)?

```python
tests = [tc for tc, acs in test_cases.items() if ac in acs]
if not tests:
    print(f"{ac}: NOT COVERED")
```

- [ ] A) `US-205-AC4: TC-07 passed`
- [ ] B) `US-205-AC4: NOT COVERED`
- [ ] C) Nothing is printed
- [ ] D) `KeyError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `US-205-AC4: NOT COVERED`

**Explanation:** The forward loop walks the ACs, so an empty list of tests is reported. TC-07 traces to the non-existent AC5 and is caught by the backward loop instead.
- **Why others are wrong:**
  - A) TC-07 does not trace to AC4.
  - C) The `if not tests` branch prints.
  - D) The list comprehension never raises here.

</details>

### 62. What does the weak-word linter report for "The address form should be fast and user-friendly."?

- [ ] A) Nothing
- [ ] B) `'should'`, `'fast'` and `'user-friendly'`
- [ ] C) Only `'fast'`
- [ ] D) `'address'` and `'form'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `'should'`, `'fast'` and `'user-friendly'`

**Explanation:** One weak obligation word and two vague quality words, sorted by position in the sentence.
- **Why others are wrong:**
  - A) All three are on the lists.
  - C) Misses two words.
  - D) These are not weak words.

</details>

### 63. What is the Jaccard similarity of the title word sets {apply, save10, at, exactly, $50.00} and {apply, save10, just, under, $50.00}?

- [ ] A) 0.60
- [ ] B) 0.43
- [ ] C) 0.75
- [ ] D) 0.30

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 0.43

**Explanation:** Shared = 3 (apply, save10, $50.00); union = 7. 3 ÷ 7 ≈ 0.43, below the 0.6 threshold, which is correct: they test different boundary values.
- **Why others are wrong:**
  - A) That is 3 / 5.
  - C) That was TC-01 vs TC-06 (6 / 8).
  - D) Wrong arithmetic.

</details>

### 64. Using the Luhn algorithm, which of these numbers is valid?

- [ ] A) `4242424242424241`
- [ ] B) `4532015112830367`
- [ ] C) `79927398713`
- [ ] D) None

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `79927398713`

**Explanation:** The textbook example sums to 70, which ends in 0. The two "valid Visa" numbers the illustrative AI produced both fail.
- **Why others are wrong:**
  - A) and B) Both fail the Luhn check.
  - D) The textbook number passes.

</details>

### 65. What happens when this runs?

```python
from datetime import date
try:
    date.fromisoformat("2026-02-30")
    print("ok")
except ValueError:
    print("impossible date")
```

- [ ] A) `ok`
- [ ] B) `impossible date`
- [ ] C) `TypeError`
- [ ] D) Prints `2026-03-02`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `impossible date`

**Explanation:** 30 February does not exist; `fromisoformat` raises `ValueError`, which the check records as a problem.
- **Why others are wrong:**
  - A) The date is invalid.
  - C) The exception is `ValueError`.
  - D) Python does not roll dates over.

</details>

### 66. What does the redactor output for this input?

```python
redact("Login failed for sam.chen@example.com with password=Hunter2 (HTTP 401)")
```

- [ ] A) Unchanged text
- [ ] B) `Login failed for <EMAIL_1> with password=<PASSWORD_1> (HTTP 401)`
- [ ] C) `Login failed for <EMAIL_1> with <PASSWORD_1> (HTTP <PHONE_1>)`
- [ ] D) `<REDACTED>`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Login failed for <EMAIL_1> with password=<PASSWORD_1> (HTTP 401)`

**Explanation:** The PASSWORD rule keeps the key name and hides the value; `401` is not redacted (the negative test checks safe text like status codes passes through).
- **Why others are wrong:**
  - A) Two sensitive values are present.
  - C) The key name is kept and 401 is not a phone number.
  - D) The redactor replaces values individually.

</details>

### 67. A review aid's oracle says: unknown code → (subtotal, "Coupon code not recognised"); ≥ 50.00 → (round(subtotal × 0.9, 2), None); else (subtotal, "Spend $50.00 to use SAVE10"). What does it return for `(49.99, "SAVE10")`?

- [ ] A) `(44.99, None)`
- [ ] B) `(49.99, 'Spend $50.00 to use SAVE10')`
- [ ] C) `(49.99, None)`
- [ ] D) `(49.99, 'Coupon code not recognised')`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `(49.99, 'Spend $50.00 to use SAVE10')`

**Explanation:** The code is valid and 49.99 is below 50.00, so AC2 applies. The AI's draft said 44.99, flagged as MISMATCH.
- **Why others are wrong:**
  - A) That was the AI's wrong answer.
  - C) AC2 also requires the message.
  - D) SAVE10 is a known code.

</details>

---

## Part 4: Fill-in-the-Blank

### 68. The INVEST checklist for user stories stands for Independent, Negotiable, Valuable, Estimable, Small and ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Testable

**Explanation:** "T" is the tester's letter: can every AC be turned into a pass/fail check?

</details>

### 69. North American phone numbers in the range 555-0100 to 555-0199 are reserved for ___ use, making them safe in test data.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** fictional

**Explanation:** Films and TV use them, so they will not ring a real person if a test sends an SMS. Similarly, `example.com` is reserved for documentation and testing.

</details>

### 70. Using unapproved AI tools such as personal accounts or random browser extensions for work is called ___ AI.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** shadow

**Explanation:** Like "shadow IT", it is the most common way well-meaning people leak data.

</details>

### 71. The correction log category for an item that enforces a rule nobody specified is ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `INVENTED_REQUIREMENT`

**Explanation:** Other categories include WRONG_EXPECTED, WRONG_TRACE, DUPLICATE, MISSING_INFO and WRONG_WORDING.

</details>

### 72. Getting worse at your own job because the AI does the thinking is called ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** deskilling

**Explanation:** Defences: think first then prompt, explain it back, do "no-AI" reps, and learn from your correction log.

</details>

---

## Part 5: Matching

### 73. Match each nine-point review check (1-5) to the typical AI failure it catches (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | C1 Correct | | A | A reference to AC5 when the story has four ACs |
| 2 | C3 Grounded | | B | Two cases with the same inputs and different titles |
| 3 | C6 Executable | | C | A wrong total at a boundary |
| 4 | C7 Traceable | | D | "Codes are case-insensitive" when the requirement is silent |
| 5 | C9 Non-duplicated | | E | No expected result, so it cannot pass or fail |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-D, 3-E, 4-A, 5-B

**Explanation:** The full checklist: correct, complete, grounded, relevant, consistent, executable, traceable, safe, non-duplicated.

</details>

### 74. Match each data classification (1-4) to its typical AI rule (A-D).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Public | | A | Never into an AI tool |
| 2 | Internal | | B | Only tools approved for it (often self-hosted) |
| 3 | Confidential | | C | Any approved tool |
| 4 | Restricted | | D | Company-approved tools only |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-D, 3-B, 4-A

**Explanation:** Data is classified by what it is, not where it lives: a staging database refreshed from production may hold real customers.

</details>

### 75. Match each automation smell (1-5) to the better practice (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `time.sleep(2)` | | A | The pytest-playwright `page` fixture |
| 2 | `//form/input[2]` | | B | Web-first `expect(...)` assertions and auto-waiting |
| 3 | `print(message)` instead of assert | | C | Fixtures that read environment variables |
| 4 | `PASSWORD = "Winter2026!"` | | D | `get_by_role` / `get_by_label` / `get_by_test_id` |
| 5 | `sync_playwright()` in each test | | E | Assert every part of the expected result |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-E, 4-C, 5-A

**Explanation:** Smells 3 (missing assertion), 4 (weak assertion) and 11 (invented APIs) are the most dangerous; 1, 2 and 6 make suites slow and flaky.

</details>
