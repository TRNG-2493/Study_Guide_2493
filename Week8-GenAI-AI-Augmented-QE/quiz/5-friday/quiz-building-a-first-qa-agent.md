# Weekly Knowledge Check: [Week8-GenAI-AI-Augmented-QE] — Friday: Building a First QA Agent

**Covers:** Building agent instructions · Creating reusable prompt templates · Implementing IO contracts · Agent output validation · Building validation scripts · Executing agents against QA requirements · Agent testing and refinement
**Questions:** 50 · **Formats:** Multiple Choice, True/False, Code Prediction, Fill-in-the-Blank

> **Context:** The TestCaseDesigner agent's files are `instructions_v1.md`, `examples.txt`, a template, `stories/*.json`, `build_prompts.py`, `check_reply.py` and `run_agent.py`. Rule IDs: **G** grounding, **B** boundaries, **M** messages, **F** format, **U** uncertainty. Checker rules: **R1–R4**, **Q1**. Human checklist: **H1–H4**.

---

## Part 1: Multiple Choice

### 1. What two things change when the draft becomes `instructions_v1.md`?
- [ ] A) The rules are rewritten and shortened
- [ ] B) Every rule gets a short ID, and the file gets a version number in its name and on line 2
- [ ] C) Examples are moved into the instructions
- [ ] D) The file is converted to JSON

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** v1 uses the same words as the draft, plus rule IDs and a version.
- **Why others are wrong:**
  - A) The wording stays the same.
  - C) Examples stay in their own file.
  - D) Instructions stay as Markdown text.
</details>

---

### 2. What do the rule-ID letters G, B, M, F and U stand for?
- [ ] A) Goal, Build, Model, File, User
- [ ] B) Grounding, Boundaries, Messages, Format, Uncertainty
- [ ] C) Green, Blue, Magenta, Fuchsia, Ultramarine
- [ ] D) Given, But, Must, For, Until

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** For example, G1 means "stick to the facts" and U1 means "say so when something is unclear".
- **Why others are wrong:**
  - A), C), D) None of these is the course's naming scheme.
</details>

---

### 3. Which question should you ask of every instruction rule?
- [ ] A) "Is it polite?"
- [ ] B) "How would we ever know it was broken?"
- [ ] C) "Is it longer than ten words?"
- [ ] D) "Did the AI suggest it?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Every rule needs a check, either by code or by a person. The rule map records which.
- **Why others are wrong:**
  - A) Tone has nothing to do with whether a rule can be checked.
  - C) Length is irrelevant.
  - D) Where a rule came from does not matter. Being checkable does.
</details>

---

### 4. In the rule map, which rules are checked by **people** rather than code?
- [ ] A) F2 and U1
- [ ] B) G1, B1, M1 (and, for now, F1)
- [ ] C) R3 and R4
- [ ] D) All of them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Code checks structure: F2 (via R3), U1 (via R4) and the four output fields. People check meaning.
- **Why others are wrong:**
  - A) Code checks these.
  - C) These are checker rules, run by code.
  - D) Several rules are code-checked.
</details>

---

### 5. Why should you never edit `instructions_v1.md` after it has run?
- [ ] A) The file is locked by the operating system
- [ ] B) The saved v1 replies would no longer match any existing instructions, so results could not be compared or reproduced
- [ ] C) The AI remembers the old version
- [ ] D) It would break the JSON Schema

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Create v1.1 instead. Each reply must be traceable to the exact instructions that produced it.
- **Why others are wrong:**
  - A) Nothing stops you editing it. The rule is a discipline, not a lock.
  - C) The AI keeps no memory between chats.
  - D) The schema is a separate file.
</details>

---

### 6. An AI review suggests three improvements to v1. What should you do?
- [ ] A) Apply them to v1 immediately
- [ ] B) Treat them as hypotheses; keep v1 unchanged and make evidence-based changes in a new version
- [ ] C) Ignore all AI suggestions
- [ ] D) Ask the AI to apply them itself

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Changes should be based on failures seen in real runs.
- **Why others are wrong:**
  - A) That breaks the v1 baseline.
  - C) The suggestions can be useful ideas to test.
  - D) That still edits v1 and skips the evidence.
</details>

---

### 7. Which three parts does `build_prompts.py` combine into each prompt, in order?
- [ ] A) Examples, instructions, story
- [ ] B) Instructions, examples, filled template (story last)
- [ ] C) Story, instructions, examples
- [ ] D) Schema, story, checker

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The story goes last, so the message ends with the task.
- **Why others are wrong:**
  - A), C) Wrong order. The story must be last.
  - D) The schema and checker are never sent.
</details>

---

### 8. Where are the v1 prompts saved, and why is the version part of the path?
- [ ] A) In the root folder, because it is easier to find
- [ ] B) In `prompts/v1/<story id>.txt`, so prompts from different versions never mix
- [ ] C) In the AI tool's history
- [ ] D) In `results_v1.md`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Replies follow the same pattern: `replies/v1/<story id>.txt`.
- **Why others are wrong:**
  - A) Mixing versions in one folder breaks traceability.
  - C) Chat history is not part of the agent's files.
  - D) That file holds results, not prompts.
</details>

---

### 9. Why does the agent use `substitute` rather than `safe_substitute`?
- [ ] A) It is faster
- [ ] B) `substitute` stops with a `KeyError` on a missing placeholder; a loud stop is better than a prompt with `$name` still in it
- [ ] C) `safe_substitute` is deprecated
- [ ] D) `substitute` encrypts values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A loud failure is better than a quiet, broken prompt.
- **Why others are wrong:**
  - A) Speed is not the reason.
  - C) Both are current methods.
  - D) Neither encrypts anything.
</details>

---

### 10. `KeyError: 'max_cases'` vs `KeyError: 'name'` when building prompts. What usually causes each?
- [ ] A) Both mean Python is not installed
- [ ] B) `max_cases`: a story file is missing that field; `name`: the template has a placeholder the script does not fill
- [ ] C) Both mean the AI returned bad JSON
- [ ] D) `max_cases` is a typo in Python

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** One error points at the data and the other at the template. Placeholder names must be exact and must never change.
- **Why others are wrong:**
  - A) A missing Python would not produce a KeyError.
  - C) Prompt building happens before any AI reply exists.
  - D) It is a legitimate placeholder name.
</details>

---

### 11. Which three habits make the one manual step (running each prompt) reliable?
- [ ] A) Use one long chat, copy only the JSON, and fix typos
- [ ] B) Use a new chat per story, copy the whole reply, and save it with the exact file name, unedited
- [ ] C) Paste all stories at once, summarise the reply, and save it anywhere
- [ ] D) Raise the temperature, retry until it passes, and keep the best one

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** New chats prevent stories leaking into each other, and unedited replies show the agent's real behaviour.
- **Why others are wrong:**
  - A) A shared chat mixes stories, and editing the reply hides problems.
  - C) This breaks the one-story-per-prompt design.
  - D) Cherry-picking hides the agent's real performance.
</details>

---

### 12. Why does adding a new story such as US-313 need no change to `build_prompts.py`?
- [ ] A) The script has US-313 hard-coded
- [ ] B) The script finds every story file in `stories/` and knows nothing about particular stories: data in files, logic in code
- [ ] C) The AI writes the code automatically
- [ ] D) New stories are not supported

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Add the JSON file and run the same command.
- **Why others are wrong:**
  - A) The script hard-codes no stories at all.
  - C) No code is generated.
  - D) This is exactly how new stories are added.
</details>

---

### 13. What does `check_reply` return?
- [ ] A) True or False
- [ ] B) A list of problems; an empty list means the reply passes every check the function makes
- [ ] C) A corrected reply
- [ ] D) A score out of 100

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A list says *what* failed, not only *whether* something failed.
- **Why others are wrong:**
  - A) A bare boolean would lose the details.
  - C) The checker never edits replies.
  - D) There is no scoring.
</details>

---

### 14. Why does the checker stop early when the JSON or a required field is missing?
- [ ] A) To save time
- [ ] B) Later checks need those parts; without fields such as `test_cases` the rules would crash
- [ ] C) To hide other problems
- [ ] D) Because the AI asked it to

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is an early stop: the reply is too broken for the later checks to run.
- **Why others are wrong:**
  - A) Saving time is not the reason. Avoiding crashes is.
  - C) The broken reply is still reported.
  - D) The checker's design is decided by people, not the AI.
</details>

---

### 15. A reply has `"test_cases": []`. Does the required-fields check fail?
- [ ] A) Yes, empty fields always fail
- [ ] B) No; the field is present but empty, which the contract allows. Only a missing field fails
- [ ] C) Only if the status is "ok"
- [ ] D) It crashes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Missing is not the same as empty. An empty list is the correct answer for `needs_clarification`.
- **Why others are wrong:**
  - A) Empty is allowed.
  - C) The required-fields check does not look at the status.
  - D) An empty list is safe to process.
</details>

---

### 16. TC-205-05 ("Lowercase save10 is accepted") uses `ac_ids: ["AC3"]`. Why does R2 not catch it?
- [ ] A) R2 is disabled
- [ ] B) AC3 exists in the story; R2 only checks that AC ids are real, not whether the case's rule is in the story
- [ ] C) Lowercase is allowed
- [ ] D) R2 only checks the first test case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Human check H1 catches it, because lowercase codes are not in the story.
- **Why others are wrong:**
  - A) R2 ran and passed.
  - C) The story never says lowercase codes are allowed.
  - D) R2 checks every test case.
</details>

---

### 17. Why does Q1 fire on "The Payment networks banner is shown"?
- [ ] A) "banner" is a vague word
- [ ] B) Q1 looks for the vague word as text, and "networks" contains "works", so it is a false alarm
- [ ] C) The result is too long
- [ ] D) It has no dollar amount

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is a false positive caused by a simple substring check. Test the checker itself.
- **Why others are wrong:**
  - A) "banner" is not on the list.
  - C) Length is not checked.
  - D) Not every expected result needs an amount.
</details>

---

### 18. You extend the checker with new rules between the v1 and v1.1 runs. What must you do to keep the comparison fair?
- [ ] A) Nothing
- [ ] B) Rerun the v1 replies with the extended checker too, so both versions are judged by the same rules
- [ ] C) Only run v1.1 with the new rules
- [ ] D) Delete the v1 results

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** In a fair comparison, only the instructions differ between versions.
- **Why others are wrong:**
  - A), C) Different checkers make the comparison unfair.
  - D) Deleting the v1 results leaves you no baseline.
</details>

---

### 19. What are the two layers of agent output validation?
- [ ] A) Unit tests and integration tests
- [ ] B) The checker script (contract: JSON, fields, R1–R4, Q1) and the human checklist (H1–H4: meaning)
- [ ] C) The AI and a second AI
- [ ] D) The schema and the template

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** PASS means well-formed, not correct.
- **Why others are wrong:**
  - A) These are software test levels, not this week's validation layers.
  - C) An AI is a second opinion at most, never the verdict.
  - D) The template is part of the input, not validation.
</details>

---

### 20. Which instruction rule does each human check protect?
- [ ] A) H1→F1, H2→F2, H3→U1, H4→G1
- [ ] B) H1→G1, H2→B1, H3→M1, H4→U1
- [ ] C) H1→R1, H2→R2, H3→R3, H4→R4
- [ ] D) They protect no rules

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Nothing invented (G1), both boundary tests (B1), exact messages (M1), the right status (U1).
- **Why others are wrong:**
  - A) This mapping does not match the rule map.
  - C) R1–R4 are checker rules, not instruction rules.
  - D) Each human check is mapped to a rule.
</details>

---

### 21. US-311 passed the checker but was still wrong. Why?
- [ ] A) The checker crashed
- [ ] B) The checker cannot tell that "2 seconds" was invented or that the story should have been refused; only a person comparing reply and story can
- [ ] C) US-311 was not in `stories/`
- [ ] D) The reply was hand-edited

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Code can point. A person decides.
- **Why others are wrong:**
  - A) The checker ran and returned PASS.
  - C) It was processed like every other story.
  - D) Replies are never hand-edited.
</details>

---

### 22. Why do you never hand-edit an agent reply to fix it?
- [ ] A) Text editors corrupt JSON
- [ ] B) It hides the agent's real behaviour, and the same mistake returns on the next story; the fix goes into the next version of the instructions
- [ ] C) It is too slow
- [ ] D) The AI would notice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Every reply gets a decision: accept, fix the instructions, or send questions to the BA.
- **Why others are wrong:**
  - A) Text editors do not corrupt JSON.
  - C) Speed is not the concern.
  - D) The AI keeps no memory between runs, so it could not notice anything.
</details>

---

### 23. TC-205-01 uses a $100.00 subtotal, which the story never mentions. Does it fail H1 (nothing invented)?
- [ ] A) Yes, $100.00 is invented
- [ ] B) No; $100.00 is test data chosen within the story's rules, and "Total is $90.00" follows from AC1
- [ ] C) Only if the status is `needs_clarification`
- [ ] D) It fails R2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** H1 is about expected behaviour. Chosen inputs may be any allowed value.
- **Why others are wrong:**
  - A) This confuses test data with expected behaviour.
  - C) The status does not decide this.
  - D) R2 is about AC ids.
</details>

---

### 24. What decision does a script PASS with `needs_clarification` get, if the human reviewer agrees?
- [ ] A) Accept the test cases
- [ ] B) Send the open questions to the BA
- [ ] C) Fix the instructions
- [ ] D) Delete the story

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The agent did its job by refusing honestly. The requirement needs an answer.
- **Why others are wrong:**
  - A) There are no test cases to accept.
  - C) The agent behaved correctly.
  - D) The story still needs testing once it is clarified.
</details>

---

### 25. What are the five parts of `run_agent.py`, and which is done by a person?
- [ ] A) Build prompts, run each prompt in the AI tool (person), check every reply, write the results table, compare versions
- [ ] B) Train, test, deploy, monitor, retire
- [ ] C) Read, write, delete, update, list
- [ ] D) All five are automated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** This week, a person pastes each prompt into a new chat and saves the reply.
- **Why others are wrong:**
  - B) This is an ML lifecycle, not the runner.
  - C) These are file operations.
  - D) Step 2 is manual this week.
</details>

---

### 26. The runner shows a story as WAITING. What does it mean, and what do you do?
- [ ] A) The AI is still thinking; wait
- [ ] B) No reply has been saved for that story and version yet; paste the prompt into a new chat and save the reply where the message says
- [ ] C) The checker is broken
- [ ] D) The story failed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** WAITING, PASS and FAIL make the results table double as a to-do list.
- **Why others are wrong:**
  - A) Nothing runs in the background. WAITING means a reply file is missing.
  - C) Nothing has been checked yet.
  - D) There is nothing to fail yet.
</details>

---

### 27. Why does the runner contain no checking rules of its own?
- [ ] A) It is unfinished
- [ ] B) So each rule lives in one place (`check_reply`); fix a rule once and every run uses the fix (DRY)
- [ ] C) Rules are in the AI's instructions
- [ ] D) Python does not allow it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The runner reuses `build_prompts` and `check_reply`. It is the test harness, not the checks.
- **Why others are wrong:**
  - A) Leaving the rules out is a deliberate design choice.
  - C) Instructions guide the AI. They do not check replies.
  - D) Python would allow it. The point is to avoid duplication.
</details>

---

### 28. Why might a tester look at US-311 (PASS) before the two FAILs?
- [ ] A) It is first alphabetically
- [ ] B) A PASS on a vague, risky story will not prompt anyone to look, and invented values are most likely there; FAILs announce themselves
- [ ] C) FAILs are always false alarms
- [ ] D) US-311 has the most test cases

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Prioritise review by risk, not only by the verdict.
- **Why others are wrong:**
  - A) Ordering by risk, not name, is the point.
  - C) FAILs are real signals.
  - D) The number of cases is not the reason.
</details>

---

### 29. Which part of the runner would change if prompts were sent to an AI service automatically through an API?
- [ ] A) All of it
- [ ] B) Only the step 2 block, where a missing reply is reported; it would send the prompt and save the reply instead
- [ ] C) The checker
- [ ] D) The story files

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Everything else stays the same, including the human review. Automation through an API is next week's topic.
- **Why others are wrong:**
  - A) The design isolates the manual step, so only that block changes.
  - C) The checking rules do not change.
  - D) The data stays the same.
</details>

---

### 30. Who owns each kind of result after triage?
- [ ] A) The AI owns everything
- [ ] B) Accepted cases and open questions: the tester (who sends questions to the BA); script failures and human-found problems: the agent maintainer
- [ ] C) The BA owns everything
- [ ] D) Whoever runs the script

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Every result gets an action and an owner. One story can need two owners.
- **Why others are wrong:**
  - A) An AI cannot be accountable.
  - C) The BA answers questions but does not own agent fixes.
  - D) Running the script does not make you the owner of every result.
</details>

---

### 31. The US-311 v1 reply invented "2 seconds". Why does triage give it two owners?
- [ ] A) It is a mistake; one owner is enough
- [ ] B) The agent failed (maintainer fixes the instructions), and the story is vague (tester asks the BA for the time limit)
- [ ] C) Two people must approve all replies
- [ ] D) The BA and the developer share it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Fixing the agent and fixing the requirement are separate actions.
- **Why others are wrong:**
  - A) Two problems need two actions.
  - C) There is no such rule.
  - D) The developer is not involved here.
</details>

---

### 32. The US-314 reply passed the script, but TC-314-01 assumes a return on day 30 is free. What did review find?
- [ ] A) Nothing wrong
- [ ] B) "Within 30 days" is ambiguous; this is an assumption stated as fact, so a question goes to the BA
- [ ] C) The ID is wrong
- [ ] D) The JSON is broken

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** It is a reasonable guess written as if the story said it.
- **Why others are wrong:**
  - A) An unconfirmed assumption is a review finding.
  - C), D) The script passed, so shape and IDs were fine.
</details>

---

### 33. You update US-311 with the BA's answer, and the old reply still shows PASS. What is wrong?
- [ ] A) Nothing
- [ ] B) The reply is stale; move it aside so the story shows WAITING, then run the new prompt in a new chat
- [ ] C) The checker cached the result
- [ ] D) The BA's answer was wrong

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A stale reply no longer matches its story.
- **Why others are wrong:**
  - A) The PASS was earned against the old story text.
  - C) The checker re-checks the saved file. The file itself is old.
  - D) Nothing suggests the BA's answer was wrong.
</details>

---

### 34. What are the five steps of the agent improvement loop?
- [ ] A) Plan, code, build, test, release
- [ ] B) Measure, analyse failures by rule, make targeted changes, save as a new version with a changelog, rerun the same stories to compare
- [ ] C) Retry, retry, retry, accept, ship
- [ ] D) Draft, review, approve, archive, forget

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Refine with evidence from both validation layers.
- **Why others are wrong:**
  - A) That is a generic delivery pipeline.
  - C) Retrying is not refining.
  - D) There is no measurement in this list.
</details>

---

### 35. The runner reported "v1: 2 PASS". Why was the real v1 score 1?
- [ ] A) The runner miscounted
- [ ] B) US-311 passed the script with an invented value; after human review, only US-313 was acceptable
- [ ] C) One reply was missing
- [ ] D) v1.1 was counted by mistake

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Error analysis must use the human review too. Invented content (H1) only shows up there.
- **Why others are wrong:**
  - A) The runner counted correctly. It just cannot judge meaning.
  - C) A missing reply would show as WAITING.
  - D) The versions are kept separate.
</details>

---

### 36. The handout made five changes in one version (v1.1). What is the drawback?
- [ ] A) None
- [ ] B) When results improve, you cannot tell which change did the work
- [ ] C) It breaks the schema
- [ ] D) It is not allowed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Bundled changes are efficient but hide cause and effect. One change per version is slower but clearer.
- **Why others are wrong:**
  - A) The drawback is real.
  - C) The instructions are separate from the schema.
  - D) It is allowed, with a known trade-off.
</details>

---

## Part 2: True / False

### 37. True or False: A script PASS means the agent's reply is correct.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** PASS means "passed these checks", that is, well-formed. Meaning is checked by the human layer.
</details>

---

### 38. True or False: The version appears in both the file name and inside the instructions file because code uses the name, and the line inside travels with the text when it is copied.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Both support traceability of results.
</details>

---

### 39. True or False: In a diff, a line beginning with `-` is only in the new file.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `-` marks a line only in the **old** file. `+` marks a line only in the **new** file.
</details>

---

### 40. True or False: One successful run of v1.1 proves the new rules work reliably.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** AI output varies between runs. You need repeated runs to show a rule works reliably.
</details>

---

### 41. True or False: Every changelog entry should include a "Reason:" tied to a failure you actually saw.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Without a reason and evidence, a change is a guess that only makes the instructions longer.
</details>

---

### 42. True or False: Good refinement sometimes removes rules as well as adding them.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Every rule costs length, and some rules over-apply.
</details>

---

### 43. True or False: In the US-313 reply, the order number "00000000" is an invented value that fails H1.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is chosen test data for "an unknown order number". The tester should still confirm it is not a real order in the test environment.
</details>

---

## Part 3: Code Prediction

### 44. What does this print?
```python
print(repr("; ".join([]) or "-"))
print(repr("; ".join(["R3: 4 cases, max 3", "Q1: vague"]) or "-"))
```
- [ ] A) `''` then `'R3: 4 cases, max 3; Q1: vague'`
- [ ] B) `'-'` then `'R3: 4 cases, max 3; Q1: vague'`
- [ ] C) `'-'` then `'-'`
- [ ] D) `None` then `'R3: 4 cases, max 3; Q1: vague'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** An empty join gives `""`, which is falsy, so `or` uses `"-"`. A non-empty join is truthy and is kept.
- **Why others are wrong:**
  - A) The `or` replaces the empty string.
  - C) Non-empty text is kept.
  - D) `join` never returns `None`.
</details>

---

### 45. You run `python run_agent.py v1 v1.1`. What is `sys.argv[1:]`?
```python
import sys
print(sys.argv[1:])
```
- [ ] A) `['run_agent.py', 'v1', 'v1.1']`
- [ ] B) `['v1', 'v1.1']`
- [ ] C) `'v1 v1.1'`
- [ ] D) `['v1.1']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['v1', 'v1.1']`

**Explanation:** `sys.argv[0]` is the script name, so `[1:]` gives every word after it.
- **Why others are wrong:**
  - A) That is the full `sys.argv`.
  - C) It is a list, not a string.
  - D) `[1:]` starts at index 1, which is `v1`.
</details>

---

### 46. What does this print?
```python
story_acs = {"AC1", "AC2", "AC3", "AC4"}
covered   = {"AC1", "AC3"}    # ACs with a test case
asked     = {"AC4"}           # ACs with an open question
reply_acs = {"AC1", "AC5"}
print(story_acs - covered - asked, reply_acs - story_acs)
```
- [ ] A) `{'AC2'} {'AC5'}`
- [ ] B) `{'AC2', 'AC4'} {'AC5'}`
- [ ] C) `{'AC2'} set()`
- [ ] D) `set() {'AC5'}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `{'AC2'} {'AC5'}`

**Explanation:** The first subtraction finds forgotten ACs (R4). The second finds invented ACs (R2). Each rule is one subtraction.
- **Why others are wrong:**
  - B) AC4 has an open question, so it counts as considered.
  - C) AC5 is not in the story.
  - D) AC2 has neither a case nor a question.
</details>

---

### 47. Q1 uses a simple substring check. Which expected results does it flag?
```python
for er in ["The Payment networks banner is shown", "Total is $45.00", "Coupon works correctly"]:
    print(er, "works" in er.lower())
```
- [ ] A) Only "Coupon works correctly"
- [ ] B) "The Payment networks banner is shown" and "Coupon works correctly"
- [ ] C) All three
- [ ] D) None

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "net**works**" contains "works", which causes a false alarm. "Coupon works correctly" is a true positive.
- **Why others are wrong:**
  - A) The substring check also matches "networks".
  - C) "Total is $45.00" does not contain "works".
  - D) Two of them match.
</details>

---

### 48. What does this print?
```python
import json
r = 'Here you go:\n```json\n{"story_id": "US-205", "status": "ok"}\n```'
print(json.loads(r[r.find("{"):r.rfind("}") + 1]))
```
- [ ] A) `JSONDecodeError`
- [ ] B) `{'story_id': 'US-205', 'status': 'ok'}`
- [ ] C) `'{"story_id": "US-205", "status": "ok"}'`
- [ ] D) `{}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Defensive parsing keeps everything from the first `{` to the last `}`, ignoring the chat text and fences.
- **Why others are wrong:**
  - A) The extracted text is valid JSON.
  - C) `json.loads` returns a dict, not a string.
  - D) The object has two keys.
</details>

---

### 49. During error analysis, failures are counted by rule. What does this print?
```python
from collections import Counter
print(Counter(["R3", "H1", "H1", "Q1", "H1"]).most_common(1))
```
- [ ] A) `[('R3', 1)]`
- [ ] B) `[('H1', 3)]`
- [ ] C) `{'H1': 3}`
- [ ] D) `('H1', 3)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[('H1', 3)]`

**Explanation:** `most_common(1)` returns a list holding the single most frequent (value, count) pair. H1 (invented content) is the top failure, and it shows up only in the human review.
- **Why others are wrong:**
  - A) R3 appears only once.
  - C) `most_common` returns a list of tuples, not a dict.
  - D) It is wrapped in a list.
</details>

---

## Part 4: Fill-in-the-Blank

### 50. `if __name__ == "_____":` makes a file's test block run only when the file is started directly, not when another script `import`s it.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__main__`

**Explanation:** `build_prompts.py` and `check_reply.py` need this so their own test blocks do not run when `run_agent.py` imports them.
</details>
