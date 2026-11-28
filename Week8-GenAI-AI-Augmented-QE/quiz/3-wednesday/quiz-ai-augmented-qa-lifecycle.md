# Weekly Knowledge Check: [Week8-GenAI-AI-Augmented-QE] — Wednesday: AI-Augmented QA Lifecycle

**Covers:** AI within the QA lifecycle · AI-assisted requirements analysis · AI-generated test cases · AI-generated test data · AI-assisted automation development · Human validation of AI output · Responsible use of AI in QE
**Questions:** 50 · **Formats:** Multiple Choice, True/False, Code Prediction, Fill-in-the-Blank

> **Running story (US-205, SAVE10):** AC1: subtotals of $50.00 or more get 10% off. AC2: subtotals under $50.00 are unchanged, with the message "Spend $50.00 to use SAVE10". Only the code SAVE10 is mentioned.

---

## Part 1: Multiple Choice

### 1. Why does an AI mistake made early in the STLC spread into later phases?
- [ ] A) Because AI tools share memory across phases
- [ ] B) Because each phase hands its output to the next phase, which treats it as correct
- [ ] C) Because test closure re-runs requirements analysis
- [ ] D) It does not spread; each phase starts fresh

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is error propagation. In the worked example, one invented sentence became a wrong test case, wrong data, a failing test and a false bug.
- **Why others are wrong:**
  - A) The tools do not share memory. The *documents* are what carry the mistake forward.
  - C) Phases run forward, so closure does not re-run earlier phases.
  - D) The phases depend on each other's outputs, so they do not start fresh.
</details>

---

### 2. What are the three levels of AI involvement, and what rule goes with them?
- [ ] A) Low, medium, high; use high whenever possible
- [ ] B) Assist, draft, automate; the higher the level, the stronger your checks must be
- [ ] C) Read, write, execute; only read is allowed
- [ ] D) Plan, do, check; repeat each sprint

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Choose the level deliberately, based on the cost of a mistake, how easily you can check it, and whether it can be undone.
- **Why others are wrong:**
  - A) These labels are not the course's levels, and "use high whenever possible" ignores the risk.
  - C) These are file permissions, not AI involvement levels.
  - D) That is the PDCA improvement cycle.
</details>

---

### 3. Where is the cheapest place to catch an invented rule such as "codes are case-insensitive"?
- [ ] A) Test execution
- [ ] B) Bug triage
- [ ] C) Requirements analysis, by asking "Is this statement actually in the story?"
- [ ] D) Test closure

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** Nothing has been built on the mistake yet, so fixing it there costs one question.
- **Why others are wrong:**
  - A), B), D) By then, cases, data, tests and possibly a false bug have already been built on the mistake.
</details>

---

### 4. An AI drafts a bug report saying "SAVE10 is broken for all customers", but only the $50.00 test fails. What kind of mistake is this?
- [ ] A) An invented rule
- [ ] B) An over-generalisation
- [ ] C) A false negative
- [ ] D) A flaky test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Over-generalisation

**Explanation:** It turns one failing boundary case into a broad claim. The check "Does the bug report quote the requirement it breaks?" exposes it.
- **Why others are wrong:**
  - A) No new rule was invented. The claim is just too broad.
  - C) A false negative is a missed problem, but here a problem was reported.
  - D) The failure is consistent, not intermittent.
</details>

---

### 5. `in_story.py` flagged "orders over $50 get 10% off" as NOT FOUND. What did a human notice that the script could not?
- [ ] A) The script had a typo
- [ ] B) The paraphrase changed the meaning: "over $50" excludes exactly $50.00, while the story says "$50.00 or more"
- [ ] C) The sentence was actually correct
- [ ] D) The story file was empty

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Code points, humans decide. The script only knew the words did not match. A person saw that the boundary had moved.
- **Why others are wrong:**
  - A) The script worked as designed.
  - C) The paraphrase is wrong at exactly $50.00.
  - D) The story was present, and the script compared against it.
</details>

---

### 6. An AI lists "security vulnerabilities" as a risk in the test plan for US-205. Why is that weak?
- [ ] A) Security never matters for coupons
- [ ] B) It is generic: it could apply to any project and names no feature or story
- [ ] C) Risks should not appear in test plans
- [ ] D) It should be spelled out as OWASP

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Keep risks that name something specific, such as the $50.00 boundary (AC1) or a second coupon (AC4).
- **Why others are wrong:**
  - A) The problem is vagueness, not the topic.
  - C) Test plans do list risks.
  - D) Naming a list does not make the risk specific to this story.
</details>

---

### 7. What makes a requirement testable?
- [ ] A) It is written in Gherkin
- [ ] B) You can write a test for it with a clear pass/fail result, usually thanks to a measurable value, exact message or precise condition
- [ ] C) It has been approved by a manager
- [ ] D) It is short

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "Fast" is not testable. "Under 2 seconds" is.
- **Why others are wrong:**
  - A) Format does not make a requirement testable.
  - C) Approval does not fix vague wording.
  - D) Short requirements can still be vague.
</details>

---

### 8. Which list gives the four common requirement defects?
- [ ] A) Vague word, missing value, missing behaviour, weak obligation
- [ ] B) Typo, duplicate, outdated, untranslated
- [ ] C) Hallucination, drift, overfitting, leakage
- [ ] D) Critical, high, medium, low

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** Examples: "fast" (vague word), "several" (missing value), nothing said about a second coupon (missing behaviour), "may be locked" (weak obligation).
- **Why others are wrong:**
  - B) These are editing problems, not the four defects the lesson names.
  - C) These are AI and ML failure terms.
  - D) These are severity levels.
</details>

---

### 9. Why run the deterministic word check *before* the AI review of requirements?
- [ ] A) The AI cannot read requirements
- [ ] B) The word check never invents a problem and gives a reliable baseline in milliseconds; the AI then looks deeper for meaning but can be wrong
- [ ] C) The word check finds everything the AI finds
- [ ] D) It is alphabetical order

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Use two checks in order: first a word check, then an AI review for meaning.
- **Why others are wrong:**
  - A) The AI review happens second, so it obviously can read them.
  - C) The word check missed US-205 AC4.
  - D) There is a real reason for the order.
</details>

---

### 10. Why did the word check miss US-205 AC4?
- [ ] A) AC4 contained a typo
- [ ] B) AC4 has no weak words; its problem is missing behaviour (what the user sees when trying a second coupon)
- [ ] C) The word list was empty
- [ ] D) AC4 was not in the file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Missing behaviour is a meaning problem, and a word list cannot find it. The AI review found it.
- **Why others are wrong:**
  - A) A typo was not the issue.
  - C) The word list worked on other criteria.
  - D) AC4 was present.
</details>

---

### 11. Why does the requirements review prompt say "Do not suggest answers to your own questions"?
- [ ] A) To keep the reply short
- [ ] B) Without it, the AI tends to fill gaps with invented values, such as "lock after 5 attempts", which can then be accepted as the requirement
- [ ] C) Because the AI's answers are always right
- [ ] D) To save tokens

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Turn every problem into an open question for the BA, and check for invented answers.
- **Why others are wrong:**
  - A), D) Length and cost are not the reason.
  - C) If its answers were always right, there would be no need to ban them.
</details>

---

### 12. The word check flags "Users may not apply an expired coupon" because it contains "may". What is this result?
- [ ] A) A true positive
- [ ] B) A false positive
- [ ] C) A false negative
- [ ] D) A contradiction

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A false positive

**Explanation:** "May not" is a clear prohibition here, so the requirement is not vague.
- **Why others are wrong:**
  - A) There is no real problem, so it cannot be a true positive.
  - C) A false negative would be a *missed* problem.
  - D) No two requirements conflict.
</details>

---

### 13. You must start test design before the BA answers a question about a requirement value. What should you do?
- [ ] A) Wait and do nothing
- [ ] B) Use the AI's suggested value as final
- [ ] C) Rewrite the requirement with a sensible value marked "(to confirm with the BA)", keep the question logged, and update it when answered
- [ ] D) Skip that requirement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** Temporary values must be clearly marked and traced in the question log.
- **Why others are wrong:**
  - A) Waiting blocks the work unnecessarily.
  - B) That treats an invented value as fact.
  - D) Skipping it leaves a coverage gap.
</details>

---

### 14. Which five fields make a good test case?
- [ ] A) ID, requirement (AC), title, steps, expected result
- [ ] B) Title, priority, owner, sprint, label
- [ ] C) ID, screenshot, video, log, comment
- [ ] D) Name, date, browser, OS, version

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** The requirement field gives traceability, so a reviewer can check the case against the criterion it claims to test.
- **Why others are wrong:**
  - B) These are tracker fields.
  - C) These are evidence attachments.
  - D) These describe the environment.
</details>

---

### 15. TC-05 was reported only for an empty expected result, but its title tests lowercase codes. Why would filling in the expected result be the wrong fix?
- [ ] A) It would make the invented rule pass every check
- [ ] B) Expected results are optional
- [ ] C) The structure check is broken
- [ ] D) TC-05 is a duplicate

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** The real problem is the invented rule. Remove the case and take the question to the BA.
- **Why others are wrong:**
  - B) Every case needs an exact expected result.
  - C) The structure check did its job. It just cannot judge meaning.
  - D) Duplication is not the issue.
</details>

---

### 16. Structure checks print nothing for the fixed test case draft. What does that prove?
- [ ] A) The suite is complete and correct
- [ ] B) The structure is right (fields filled, every AC covered, messages exact), but not that the expected values are correct or coverage is enough
- [ ] C) The checks did not run
- [ ] D) The AI did a perfect job

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Code checks structure, and humans check meaning. Calculate expected values by hand.
- **Why others are wrong:**
  - A) Structure is not correctness.
  - C) An empty output means the checks ran and found nothing.
  - D) The draft needed fixing, which is why it was called the *fixed* draft.
</details>

---

### 17. Why is $50.01 needed in addition to $49.99 and $50.00?
- [ ] A) It is not needed
- [ ] B) BVA tests just below, on and just above the boundary; $50.01 confirms the discount above the boundary and checks rounding ($45.01)
- [ ] C) To test the maximum order value
- [ ] D) Because the AI suggested it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** 50.01 × 0.9 = 45.009, which rounds to $45.01. This is a good rounding check.
- **Why others are wrong:**
  - A) Three-value BVA uses all three values.
  - C) $50.01 is nowhere near a maximum value.
  - D) The technique decides the values, not the AI.
</details>

---

### 18. An AI case has the step "Verify the discount" and the expected result "Discount is applied correctly". What is wrong?
- [ ] A) Nothing
- [ ] B) Neither gives a pass/fail rule; the expected result should state an exact value such as "Total is $45.00"
- [ ] C) It should be written in Gherkin
- [ ] D) It needs a screenshot

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Vague expected results are a classic AI drafting mistake.
- **Why others are wrong:**
  - A) "Correctly" cannot be checked.
  - C) Format would not fix the vagueness.
  - D) Evidence does not replace an expected result.
</details>

---

### 19. What are the three main kinds of test data for a sign-up form with ages 18 to 120?
- [ ] A) Small, medium, large
- [ ] B) Valid (age 34), invalid (age 16), boundary (17, 18, 120, 121)
- [ ] C) Old, new, archived
- [ ] D) Real, copied, masked

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Work out the data you need by purpose first, then generate it.
- **Why others are wrong:**
  - A) Size is not a purpose.
  - C) Age of records is irrelevant.
  - D) Real data should never be used.
</details>

---

### 20. Why should each invalid test data row break exactly one rule?
- [ ] A) To keep files small
- [ ] B) So when the row is rejected, you know which rule caused it
- [ ] C) Because systems only check one rule
- [ ] D) To reach 100% coverage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A row that breaks two rules cannot tell you whether each rule works.
- **Why others are wrong:**
  - A) File size is not the reason.
  - C) Systems check many rules, which is exactly why you isolate them.
  - D) This is about diagnosis, not coverage.
</details>

---

### 21. Why is "UK" a classic AI test data mistake?
- [ ] A) UK is not a real country
- [ ] B) The ISO 3166-1 alpha-2 code for the United Kingdom is GB; a system expecting ISO codes rejects "UK"
- [ ] C) Two-letter codes are not allowed
- [ ] D) UK should be lowercase

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** AI data looks realistic but breaks hidden rules such as standard codes.
- **Why others are wrong:**
  - A) The country is real. The code is wrong.
  - C) ISO alpha-2 codes are two letters.
  - D) Case is not the issue here.
</details>

---

### 22. Why is a rule-based script a better check of AI test data than asking the same AI "is this data valid?"
- [ ] A) Scripts are cheaper to write than prompts
- [ ] B) The script is independent and deterministic; the AI may miss mistakes and you cannot tell which
- [ ] C) The AI refuses validation requests
- [ ] D) There is no difference

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** In the worked example, only 1 of 5 "valid" users was actually valid.
- **Why others are wrong:**
  - A) The cost of writing it is not the main point. Independence is.
  - C) The AI will answer. Its answer just cannot be trusted as a check.
  - D) Independence is the whole difference.
</details>

---

### 23. Why should a test not ask an AI for fresh data on every run?
- [ ] A) It is too expensive
- [ ] B) The data would change each run, so failures would not be repeatable; save reviewed data or use code with a fixed seed
- [ ] C) AI cannot generate JSON
- [ ] D) It violates licences

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Repeatable data means repeatable failures.
- **Why others are wrong:**
  - A) Cost is a side issue. Repeatability is the main one.
  - C) AI can generate JSON.
  - D) Licensing is not the concern here.
</details>

---

### 24. Why is `assert result` a weak assert for `login()`?
- [ ] A) It is too slow
- [ ] B) It passes for any non-empty text, including "Invalid email or password"
- [ ] C) `assert` is deprecated
- [ ] D) It only works in Playwright

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Weak asserts create false confidence. Use an exact assert such as `assert result == "Welcome back!"`.
- **Why others are wrong:**
  - A) Speed is not the issue.
  - C) `assert` is standard pytest.
  - D) It is plain Python.
</details>

---

### 25. In mutation testing, what does it mean if a mutant "survives"?
- [ ] A) The code is correct
- [ ] B) All tests still pass on the deliberately changed code, so the tests cannot tell broken code from correct code
- [ ] C) The mutant crashed
- [ ] D) The tests were deleted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A killed mutant is one the tests detect. A surviving mutant reveals weak tests.
- **Why others are wrong:**
  - A) The mutant is broken on purpose.
  - C) A crash that made the tests fail would count as killed.
  - D) Deleting tests has nothing to do with whether a mutant survives.
</details>

---

### 26. Why prefer `page.get_by_role("button", name="Log in")` over `page.locator("#btn-23 > span")`?
- [ ] A) It runs faster
- [ ] B) It finds the button as a user sees it, so it survives ID and layout changes and checks the visible name
- [ ] C) CSS locators are not supported
- [ ] D) It avoids needing a browser

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** User-facing locators are robust. Fragile locators depend on internal details that can change at any time.
- **Why others are wrong:**
  - A) Speed is not the reason.
  - C) Playwright supports CSS locators. They are just fragile.
  - D) Both locators need a browser.
</details>

---

### 27. An AI test uses `time.sleep(3)` then `assert "Invalid" in page.content()`. What are the two problems?
- [ ] A) No problems
- [ ] B) The fixed wait is slow or flaky, and the assert is weak (it passes if "Invalid" appears anywhere in the HTML)
- [ ] C) `sleep` should be 5 seconds
- [ ] D) `page.content()` does not exist

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Use `expect(page.get_by_text("Invalid email or password")).to_be_visible()` instead.
- **Why others are wrong:**
  - A) There are clearly two issues.
  - C) A longer sleep is still a fixed wait.
  - D) `page.content()` exists. Using it like this is the weakness.
</details>

---

### 28. Which three traps make people trust AI output too much?
- [ ] A) Fluency trap, volume trap, automation bias
- [ ] B) Overfitting, underfitting, drift
- [ ] C) Recency bias, majority bias, anchoring bias
- [ ] D) Cost trap, speed trap, scale trap

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** Well-written text feels correct, a large amount of output looks thorough, and "the tool said so" feels authoritative.
- **Why others are wrong:**
  - B) These are model training problems.
  - C) Recency and majority bias affect few-shot prompts, and anchoring is related but not one of the three traps.
  - D) These are invented.
</details>

---

### 29. TC-02 says "SAVE10 on $49.99 gives $44.99". What should the reviewer do?
- [ ] A) Accept it as-is
- [ ] B) Edit it: AC2 says under $50.00 is unchanged, so the expected result is $49.99 with "Spend $50.00 to use SAVE10"
- [ ] C) Reject the whole suite
- [ ] D) Ask the AI to double-check

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Edit

**Explanation:** The AI applied AC1's discount to AC2's range. Log the edit with a reason category.
- **Why others are wrong:**
  - A) The expected result is wrong.
  - C) One wrong case does not justify rejecting everything.
  - D) The story is the oracle, not the AI.
</details>

---

### 30. You and an AI second reviewer disagree about a case. How is it decided?
- [ ] A) The AI wins, since it is more consistent
- [ ] B) Majority vote with a third AI
- [ ] C) The story decides; re-read the exact AC, and you remain the accountable reviewer
- [ ] D) Flip a coin

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** An AI can be a second reviewer, but never the accountable one.
- **Why others are wrong:**
  - A), B) An AI cannot be the source of truth.
  - D) Decisions must trace to the requirement.
</details>

---

### 31. A 1-in-5 sample of low-risk AI test cases finds one invented rule. What should you do?
- [ ] A) Fix that one and move on
- [ ] B) Widen the review to all items, since AI mistakes often share a cause
- [ ] C) Reduce the sample to 1-in-10
- [ ] D) Accept the rest

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A sample that finds problems means you review everything.
- **Why others are wrong:**
  - A), D) Similar mistakes are likely in the unsampled items.
  - C) That moves in the wrong direction.
</details>

---

### 32. What does "redact before you prompt" mean?
- [ ] A) Delete the whole log before asking the AI
- [ ] B) Replace every sensitive value with a placeholder such as `<EMAIL>` or `<API_KEY>`, keeping the structure the AI needs
- [ ] C) Encrypt the prompt
- [ ] D) Ask the AI to ignore sensitive data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Keep the time, the error and the field names so the AI can still help.
- **Why others are wrong:**
  - A) Deleting the log loses the evidence the AI needs.
  - C) The AI tool would still receive the values.
  - D) Once sent, the data has already left your control.
</details>

---

### 33. You accidentally pasted a log containing a live API key into an AI tool. What must happen to the key?
- [ ] A) Nothing, as long as you delete the chat
- [ ] B) It must be rotated, because once pasted it must be treated as leaked; also stop, delete, and tell your lead or security contact
- [ ] C) Ask the AI to forget it
- [ ] D) Change its expiry date to next year

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The incident steps are: stop, delete, tell, rotate, learn.
- **Why others are wrong:**
  - A) Deleting the chat does not undo exposure.
  - C) The AI cannot guarantee it has forgotten the key.
  - D) The old value would still work, which is the whole problem.
</details>

---

## Part 2: True / False

### 34. True or False: In the worked example, the invented rule "codes are case-insensitive" produced a real bug in the code.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It produced a **false bug**. The code correctly followed US-205, and the test was built on an invented rule.
</details>

---

### 35. True or False: Expected values for automated tests should come from the requirement or reviewed test case, never from the code under test.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The requirement is the source of truth. Copying values from the code just confirms whatever the code does, bugs included.
</details>

---

### 36. True or False: In the `if True:` bug demo, the AI's tests reported `2 passed` while the reviewed tests reported `3 failed, 1 passed`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The AI's weak tests passed on broken code. The one reviewed test that passed was the valid-login test, which is correct, because the bug lets everyone in.
</details>

---

### 37. True or False: After an AI re-ask fixes the problems you named, you can merge the new file without reviewing it again.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A re-ask can introduce new problems. Review again with the checklist, including a break-it check.
</details>

---

### 38. True or False: Using `<valid_password>` in an automation prompt, instead of the real test password, is good practice even for test accounts.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The AI does not need the real value, and pasting secrets is a bad habit.
</details>

---

### 39. True or False: If a redaction script's pre-flight check reports "safe to send", the text is guaranteed to contain no sensitive data.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It only means none of its patterns matched. In the Your Turn example, a phone number and a token slipped through. Always read the output.
</details>

---

### 40. True or False: Data in a test environment that was copied from production can be pasted into an AI tool without redaction.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A production copy is still production data. Redact it like a live customer record, and only use an approved tool.
</details>

---

### 41. True or False: Every edit or rejection in a correction log should have a reason category, so the log can be counted and turned into prompt fixes.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Counted reasons show what kinds of mistakes the AI makes. In the worked example, 50% of items were accepted as-is.
</details>

---

## Part 3: Code Prediction

### 42. What does this print?
```python
tc = {"id": "TC-05", "ac": "AC3", "title": "x", "steps": "y", "expected": ""}
print([f for f in ["id", "ac", "title", "steps", "expected", "data"] if not tc.get(f)])
```
- [ ] A) `['expected']`
- [ ] B) `['data']`
- [ ] C) `['expected', 'data']`
- [ ] D) `KeyError: 'data'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `['expected', 'data']`

**Explanation:** `get` returns `None` for the missing key "data". Both `None` and `""` are falsy, so `not` catches both.
- **Why others are wrong:**
  - A) The missing "data" key is caught too.
  - B) The empty string for "expected" is caught too.
  - D) `.get()` never raises a KeyError.
</details>

---

### 43. What does this print?
```python
cases = [{"ac": "AC1"}, {"ac": "AC1"}, {"ac": "AC2"}, {"ac": "AC3"}]
covered = {c["ac"] for c in cases}
print(sorted({"AC1", "AC2", "AC3", "AC4"} - covered), len(covered))
```
- [ ] A) `[] 4`
- [ ] B) `['AC4'] 3`
- [ ] C) `['AC4'] 4`
- [ ] D) `['AC1'] 3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['AC4'] 3`

**Explanation:** A set comprehension keeps each AC once, so the size is 3. The set difference shows AC4 is uncovered.
- **Why others are wrong:**
  - A), C) Duplicates collapse in a set, and AC4 is missing.
  - D) AC1 is covered twice.
</details>

---

### 44. What does this print?
```python
import re
line = "2026-03-01 10:02 ERROR login failed password=hunter2 user=a@b.com"
print(re.sub(r"(?<=password=)\S+", "<PASSWORD>", line))
```
- [ ] A) `2026-03-01 10:02 ERROR login failed <PASSWORD> user=a@b.com`
- [ ] B) `2026-03-01 10:02 ERROR login failed password=<PASSWORD> user=a@b.com`
- [ ] C) `2026-03-01 10:02 ERROR login failed password=<PASSWORD> user=<PASSWORD>`
- [ ] D) The line is unchanged

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The lookbehind matches text *after* `password=` without including it, so the field name stays. Note that the email is still exposed and needs its own rule.
- **Why others are wrong:**
  - A) The lookbehind keeps `password=`.
  - C) `\S+` stops at the space, so `user=` is untouched.
  - D) The pattern matches `hunter2`.
</details>

---

### 45. The rule is "age 18 to 120". What does this print?
```python
def valid_age(a): return 18 <= a <= 120
print([(a, valid_age(a)) for a in [17, 18, 120, 121]])
```
- [ ] A) `[(17, False), (18, True), (120, False), (121, False)]`
- [ ] B) `[(17, False), (18, True), (120, True), (121, False)]`
- [ ] C) `[(17, True), (18, True), (120, True), (121, True)]`
- [ ] D) `[(17, False), (18, False), (120, True), (121, False)]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** 120 is valid. In the worked example, the AI wrongly labelled age 120 as breaking the rule, which would have produced a false bug report.
- **Why others are wrong:**
  - A) That repeats the AI's mislabel of 120.
  - C) 17 and 121 are outside the range.
  - D) 18 is inside the range.
</details>

---

### 46. What does this print?
```python
ISO = {"US", "CA", "GB", "IN"}
print([c in ISO for c in ["US", "UK", "GB", "in"]])
```
- [ ] A) `[True, True, True, True]`
- [ ] B) `[True, False, True, False]`
- [ ] C) `[True, False, True, True]`
- [ ] D) `[True, True, True, False]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "UK" is not an ISO 3166-1 alpha-2 code (GB is), and set membership is case-sensitive, so "in" ≠ "IN".
- **Why others are wrong:**
  - A), D) "UK" is not in the set.
  - C) Lowercase "in" does not match.
</details>

---

### 47. What does this print?
```python
import random
random.seed(42); a = [random.randint(18, 120) for _ in range(3)]
random.seed(42); b = [random.randint(18, 120) for _ in range(3)]
print(a == b)
```
- [ ] A) `True`
- [ ] B) `False`
- [ ] C) It depends on the time of day
- [ ] D) `ValueError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `True`

**Explanation:** A fixed seed makes pseudo-random generation repeatable. That is how you get repeatable test data from code.
- **Why others are wrong:**
  - B) The same seed produces the same sequence.
  - C) Seeding removes the dependence on time.
  - D) The arguments are valid.
</details>

---

### 48. The login code has the `if True:` bug. What does this print?
```python
def login(email, pw):
    if True:
        return "Welcome back!"

print(bool(login("x", "bad")), login("x", "bad") == "Invalid email or password")
```
- [ ] A) `True True`
- [ ] B) `True False`
- [ ] C) `False False`
- [ ] D) `False True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `True False`

**Explanation:** `assert result` (truthiness) would pass, but an exact assert on the invalid-login message would fail and catch the bug.
- **Why others are wrong:**
  - A) The return value is "Welcome back!", not the error message.
  - C), D) Any non-empty string is truthy.
</details>

---

## Part 4: Fill-in-the-Blank

### 49. A `_____`-in-the-loop way of working means the AI drafts, and a named person reviews, approves and stays accountable.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** human

**Explanation:** The four checklist questions: Does it trace to an AC? Is the expected result exact? Is anything invented? Could it ever fail?
</details>

---

### 50. Use the reserved domain `_____` for test email addresses, so a test email can never reach a real person.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** example.com

**Explanation:** It is reserved for examples and testing (RFC 2606). Never use real personal data.
</details>
