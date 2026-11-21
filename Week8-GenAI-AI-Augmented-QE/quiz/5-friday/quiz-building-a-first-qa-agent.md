# Daily Knowledge Check: Week 8 Friday - Building a First QA Agent

This check covers building agent instructions, reusable prompt templates, implementing IO contracts, agent output validation, building validation scripts, executing agents against QA requirements, and agent testing and refinement. All questions use the running project `tcd_agent/` and the agent **TestCaseDesigner** (instructions v1.0.0 → v1.1.0, contract 1.0.0). Try each question on your own first, then open the solution to check your reasoning.

---

## Part 1: Multiple Choice

### 1. Why does the lesson call building instructions an **engineering** process rather than a writing exercise?

- [ ] A) Because instructions must be written in Python
- [ ] B) Because it starts from a requirement (job card), collects evidence, makes rules testable, desk-checks, reviews, then versions and pins the result
- [ ] C) Because only engineers are allowed to write prompts
- [ ] D) Because the model writes its own instructions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because it starts from a requirement (job card), collects evidence, makes rules testable, desk-checks, reviews, then versions and pins the result

**Explanation:** The seven-step method mirrors the testing process: requirement, test basis, design, traceability, static review, baseline.
- **Why others are wrong:**
  - A) Instructions are a Markdown file sent as the system message.
  - C) Nothing restricts who writes them; the point is the process.
  - D) The team writes, reviews and versions them.

</details>

### 2. Which sentence is pitched at the **right altitude**?

- [ ] A) "For US-205, test $50.00 and $49.99."
- [ ] B) "Test the boundaries well."
- [ ] C) "For every numeric threshold, write one test at the threshold and one just below it (for example $50.00 and $49.99)."
- [ ] D) "Write thorough, high-quality test cases."

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) "For every numeric threshold, write one test at the threshold and one just below it (for example $50.00 and $49.99)."

**Explanation:** Right altitude = a general principle made concrete with an example or measurable test.
- **Why others are wrong:**
  - A) Too low: a brittle script that only works for one story.
  - B) Too high: "well" cannot be checked.
  - D) Too high: a vague wish whose meaning changes run to run.

</details>

### 3. "Minimal but sufficient" instructions means:

- [ ] A) As short as possible, even if behaviour is underspecified
- [ ] B) The smallest set of information that fully describes expected behaviour; every sentence earns its place by preventing a nameable failure
- [ ] C) No more than ten lines
- [ ] D) Only the Output section

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The smallest set of information that fully describes expected behaviour; every sentence earns its place by preventing a nameable failure

**Explanation:** Minimal does not mean short. If you cannot say which failure a rule prevents, it is a candidate for deletion.
- **Why others are wrong:**
  - A) "Sufficient" rules out underspecification.
  - C) There is no line limit.
  - D) All nine sections are still required.

</details>

### 4. What is a **job card**, and who is it for?

- [ ] A) The system message, written for the model
- [ ] B) A short human-facing description of the agent's one job, consumer, inputs, outputs, done criteria and out-of-scope work, written before any instruction text
- [ ] C) A Jira ticket assigning the agent to a tester
- [ ] D) The `agent.json` configuration file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A short human-facing description of the agent's one job, consumer, inputs, outputs, done criteria and out-of-scope work, written before any instruction text

**Explanation:** It stops scope creep and gives every later decision a reference point ("does this rule serve the job?").
- **Why others are wrong:**
  - A) The job card is for humans, not the model.
  - C) It describes the agent's job, not a work ticket.
  - D) `agent.json` pins files and settings; it does not describe the job.

</details>

### 5. The tip in the job-card section says: "If you cannot write 'One job' in one sentence…"

- [ ] A) …make the sentence longer
- [ ] B) …you probably have two agents; split the job before writing instructions
- [ ] C) …skip the job card
- [ ] D) …let the model decide the job

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) …you probably have two agents; split the job before writing instructions

**Explanation:** This is Thursday's single-responsibility idea applied at design time.
- **Why others are wrong:**
  - A) A longer sentence hides two jobs rather than fixing the design.
  - C) The job card is step 1 of the method.
  - D) Scope is a team decision, not a model one.

</details>

### 6. Which is **not** one of the four sources of raw material for TestCaseDesigner's instructions?

- [ ] A) The IO contract
- [ ] B) The sample pairs P01–P05
- [ ] C) The correction log and known model habits
- [ ] D) The model's own suggestions about what rules it needs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The model's own suggestions about what rules it needs

**Explanation:** The four sources are A: contract, B: sample pairs, C: correction log (Wednesday), D: known model habits (Tuesday). "Do not write instructions from imagination."
- **Why others are wrong:**
  - A) Source A.
  - B) Source B.
  - C) Sources C and D.

</details>

### 7. In what **writing order** does the lesson recommend drafting the nine sections?

- [ ] A) Role and Goal first, then top to bottom
- [ ] B) Output and Inputs first, then Process, Rules, Uncertainty, Boundaries, and finally Scope, Style and Role and Goal
- [ ] C) Alphabetical order
- [ ] D) Style first, because tone matters most

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Output and Inputs first, then Process, Rules, Uncertainty, Boundaries, and finally Scope, Style and Role and Goal

**Explanation:** The contract fixes Output and Inputs, so they are easiest to get exactly right; writing the role last avoids a grand opening that over-promises. The **file** order stays Thursday's reading order.
- **Why others are wrong:**
  - A) That is reading order, not writing order.
  - C) Order follows dependencies, not the alphabet.
  - D) Style is written near the end.

</details>

### 8. Where does "Return at most 6 test cases" belong?

- [ ] A) In the instructions, because it is a rule
- [ ] B) In the user-message template, because it depends on this call's `max_cases`
- [ ] C) In the output schema
- [ ] D) Nowhere; the model chooses

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) In the user-message template, because it depends on this call's `max_cases`

**Explanation:** If a sentence is true for every story it goes in the instructions; if it mentions this story or a per-call option it goes in the template.
- **Why others are wrong:**
  - A) It is not true for every call.
  - C) The schema cannot know the per-call limit; R5 checks it in code.
  - D) The limit is a caller choice enforced by R5.

</details>

### 9. Rewrite 1 changed "Use boundary value analysis where appropriate." What kind of improvement was it mainly?

- [ ] A) Make it concrete: a findable trigger ("every numeric threshold"), an action and an example with real numbers
- [ ] B) Give it a reason
- [ ] C) Delete it
- [ ] D) Move it to the template

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Make it concrete: a findable trigger ("every numeric threshold"), an action and an example with real numbers

**Explanation:** "Where appropriate" is a weak word; the example pins "just below" for money as one cent ($49.99), not $49.00.
- **Why others are wrong:**
  - B) Rewrite 2 (grounding) is the one that added a reason.
  - C) Boundary testing is required behaviour (M3).
  - D) It is true for every story, so it stays in the instructions.

</details>

### 10. Why was "If something is unclear, ask the user." a weak rule?

- [ ] A) It is too long
- [ ] B) There is no user in a pipeline run, "something" is undefined, and "ask" does not say where the question goes
- [ ] C) Models cannot ask questions
- [ ] D) It contradicts the job card

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) There is no user in a pipeline run, "something" is undefined, and "ask" does not say where the question goes

**Explanation:** The improved rule names three conditions (ambiguous, contradictory, untestable), routes the question into `open_questions`, and requires the criterion ID, which makes it checkable by R3.
- **Why others are wrong:**
  - A) Length is not the problem.
  - C) Models can write questions; the issue is where they go.
  - D) It does not contradict the job card; it is just untestable.

</details>

### 11. Which are the four questions to ask of every rule?

- [ ] A) Who, what, when, where?
- [ ] B) Can the model find the trigger? Does it name a concrete action or source? Does it say why? Could a script or reviewer tell whether it was followed?
- [ ] C) Is it short, polite, numbered and bold?
- [ ] D) Is it in the template, schema, code or log?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Can the model find the trigger? Does it name a concrete action or source? Does it say why? Could a script or reviewer tell whether it was followed?

**Explanation:** Trigger, concrete action, reason, checkable. If any answer is "no", rewrite.
- **Why others are wrong:**
  - A) Generic journalism questions.
  - C) Formatting is not the test.
  - D) Those are locations, not quality questions.

</details>

### 12. In the first rule-to-check map, the Boundaries rule "Never put real customer data…" had no check. How was this resolved for v1.0.0?

- [ ] A) The rule was deleted
- [ ] B) An automated email detector was added immediately
- [ ] C) It was consciously assigned to human review and added to the reviewer's checklist (`"checks": ["HUMAN"]`)
- [ ] D) It was left with an empty list

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It was consciously assigned to human review and added to the reviewer's checklist (`"checks": ["HUMAN"]`)

**Explanation:** A rule no check verifies is a smell. An automated check for real-looking emails or card numbers is noted as a later improvement (desk-check finding F-04).
- **Why others are wrong:**
  - A) It is a good rule; only its verification was missing.
  - B) That was deferred, not done.
  - D) An empty list triggers the `NO CHECK` problem in `check_rule_map.py`.

</details>

### 13. In the desk-check, finding F-02 (P03 status) was a **conflict**. What should the team do during the desk-check?

- [ ] A) Silently edit the instructions to match the pair
- [ ] B) Silently edit the pair to match the instructions
- [ ] C) Record it with an owner and get a team decision; do not edit either document during the desk-check
- [ ] D) Ignore it, because the model will probably do something sensible

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Record it with an owner and get a team decision; do not edit either document during the desk-check

**Explanation:** Neither document is automatically right. The QE lead later decided the pair was right, and v1.1.0 closed F-02.
- **Why others are wrong:**
  - A/B) Silent edits destroy the record of the decision.
  - D) That is exactly how gaps stay invisible until behaviour changes.

</details>

### 14. Why did P04 (malformed input) need **no** instruction line in the desk-check?

- [ ] A) Because the model handles malformed input well
- [ ] B) Because the input gate rejects it before the model is called; a rule would duplicate the gate and waste tokens
- [ ] C) Because P04 was deleted
- [ ] D) Because P04 is out of scope like P05

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because the input gate rejects it before the model is called; a rule would duplicate the gate and waste tokens

**Explanation:** "Not the instructions' job" is one of the three kinds of desk-check finding.
- **Why others are wrong:**
  - A) The model never sees it.
  - C) P04 is still a sample pair.
  - D) P05 reaches the model and is handled by Boundaries; P04 never does.

</details>

### 15. What does `load_instructions` check, in order?

- [ ] A) Weak words, length, spelling
- [ ] B) The header exists; all nine sections exist and are non-empty; the header's contract version matches `expected_contract`
- [ ] C) That the model accepts the file
- [ ] D) That the rules are good

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The header exists; all nine sections exist and are non-empty; the header's contract version matches `expected_contract`

**Explanation:** Cheapest first; any failure raises `ValueError` naming the file and the problem.
- **Why others are wrong:**
  - A) Weak words are `check_instructions.py`'s job.
  - C) No model is called when loading.
  - D) The loader does not judge rule quality; review, desk-check and the rule map do.

</details>

### 16. Why does `check_rule_map.py` identify each rule by a **phrase** rather than a line number?

- [ ] A) Phrases are shorter
- [ ] B) Line numbers change whenever a line is added above; a phrase survives harmless edits but disappears when the rule itself is reworded, which is exactly when a human should look again
- [ ] C) JSON cannot store numbers
- [ ] D) The model reads phrases, not lines

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Line numbers change whenever a line is added above; a phrase survives harmless edits but disappears when the rule itself is reworded, which is exactly when a human should look again

**Explanation:** Reworded rules show up as `DRIFT`; added bullets show up as `UNMAPPED`.
- **Why others are wrong:**
  - A) Length is irrelevant.
  - C) JSON stores numbers fine.
  - D) The map is for the team, not the model.

</details>

### 17. What problem does a **template library** solve?

- [ ] A) Slow model responses
- [ ] B) Copy-paste **drift**: copies of shared wording changing independently until they disagree
- [ ] C) Missing API keys
- [ ] D) JSON Schema validation

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Copy-paste **drift**: copies of shared wording changing independently until they disagree

**Explanation:** Shared wording is written once as a partial, named, versioned and referred to everywhere, like extracting a duplicated function.
- **Why others are wrong:**
  - A/C) Unrelated to templates.
  - D) That is the contract layer.

</details>

### 18. Which of these is a **partial** in the library?

- [ ] A) `tcd_user@1.0.1`
- [ ] B) `req_review_user@1.0.0`
- [ ] C) `output_reminder@1.0.0`
- [ ] D) `tcd_user_fewshot@1.0.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `output_reminder@1.0.0`

**Explanation:** The three partials are `story_block`, `output_reminder` and `example`; they are only ever included in other templates.
- **Why others are wrong:**
  - A, B, D) These are `prompt` kind: complete user messages sent to a model.

</details>

### 19. In `manifest.json`, what is the `includes` field for?

- [ ] A) Listing Python modules to import
- [ ] B) Listing the partials a template embeds, pinned as `name@version`, so a new partial version never sneaks in
- [ ] C) Listing the agents that use the template
- [ ] D) Listing the template's placeholders

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Listing the partials a template embeds, pinned as `name@version`, so a new partial version never sneaks in

**Explanation:** Partials are pinned too; moving to a new partial version requires a new template version.
- **Why others are wrong:**
  - A) Not related to Python imports.
  - C) Agents pin templates in `agent.json`, not the reverse.
  - D) That is the `variables` field.

</details>

### 20. Which values must a caller supply to render `tcd_user@1.0.1`?

- [ ] A) `story_block`, `techniques`, `max_cases`, `output_reminder`
- [ ] B) `story_id`, `title`, `acceptance_criteria`, `techniques`, `max_cases`, `agent_name`, `contract_version`
- [ ] C) Only `story_id`
- [ ] D) `examples` and `story_block`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `story_id`, `title`, `acceptance_criteria`, `techniques`, `max_cases`, `agent_name`, `contract_version`

**Explanation:** Seven values: `story_block` and `output_reminder` are filled by the library from partials, which need the story values plus `agent_name` and `contract_version`.
- **Why others are wrong:**
  - A) Two of those are filled by the library, and the partials' own values are missing.
  - C) Far too few.
  - D) `examples` belongs to the few-shot template.

</details>

### 21. Why does `TemplateLibrary.render()` reject an **unexpected** value, not just a missing one?

- [ ] A) To save memory
- [ ] B) An unexpected value usually means the caller has the wrong template version in mind (e.g. a renamed `$max_cases`), and ignoring it would silently drop that information from the prompt
- [ ] C) Because `string.Template` cannot accept extra keys
- [ ] D) Because partials cannot have variables

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An unexpected value usually means the caller has the wrong template version in mind (e.g. a renamed `$max_cases`), and ignoring it would silently drop that information from the prompt

**Explanation:** The library is strict in both directions: missing values fail, unexpected values fail.
- **Why others are wrong:**
  - A) Memory is irrelevant.
  - C) `substitute()` ignores extra keys; the library adds this check itself.
  - D) Partials do have variables.

</details>

### 22. Rendering `tcd_user@1.0.0` and `tcd_user@1.0.1` with the same story gives identical text (699 vs 699 characters). What version bump does that justify?

- [ ] A) MAJOR
- [ ] B) MINOR
- [ ] C) PATCH
- [ ] D) None; no new file is needed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) PATCH

**Explanation:** The model receives exactly the same prompt, so behaviour cannot have changed; only internal structure changed.
- **Why others are wrong:**
  - A) Nothing broke for consumers.
  - B) No new behaviour; a wording change would need measuring and at least MINOR.
  - D) A refactor of a released template still gets a new versioned file.

</details>

### 23. Why does the few-shot template say "Copy its format, never its content, IDs or numbers"?

- [ ] A) To make the prompt longer
- [ ] B) Models copy patterns from examples, including details like `TC-101-01` or "5 failed attempts"; the line discourages this and R4 catches it when it still happens
- [ ] C) Because the example is in a different language
- [ ] D) Because copying format is forbidden

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Models copy patterns from examples, including details like `TC-101-01` or "5 failed attempts"; the line discourages this and R4 catches it when it still happens

**Explanation:** Instruction plus validation: neither alone is enough.
- **Why others are wrong:**
  - A) Length is a cost, not the goal.
  - C) The example is in the same language.
  - D) Copying the format is exactly the point.

</details>

### 24. Why was pair **P02**, not P01, used as the few-shot example for a US-205 prompt?

- [ ] A) P02 is shorter only
- [ ] B) The example must be a **different** story; with US-205's own answer the model could simply copy it
- [ ] C) P01 is invalid
- [ ] D) P02 has more test cases

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The example must be a **different** story; with US-205's own answer the model could simply copy it

**Explanation:** P02 also helps by being short (one AC, one case), since examples cost tokens on every call.
- **Why others are wrong:**
  - A) Shortness helps but is not the main reason.
  - C) P01 is the happy-path pair.
  - D) P02 has exactly one test case.

</details>

### 25. The parametrized template test suite reports **21 passed**. Where does 21 come from?

- [ ] A) 7 templates × 3 tests
- [ ] B) 7 (no leftovers) + 5 (every AC once) + 7 (unknown value rejected) + 1 (refactor equality) + 1 (format lock)
- [ ] C) 21 acceptance criteria
- [ ] D) 3 partials × 7 agents

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 7 (no leftovers) + 5 (every AC once) + 7 (unknown value rejected) + 1 (refactor equality) + 1 (format lock)

**Explanation:** Only five templates contain acceptance criteria, so the "every AC once" test runs five times.
- **Why others are wrong:**
  - A) The AC test does not run for all seven, and two tests are not parametrized.
  - C/D) Not how the count is built.

</details>

### 26. A teammate fixes a typo in `tcd_user_v1.0.1.txt`, which has been in use for two weeks. What is the right move?

- [ ] A) Edit in place; typos do not matter
- [ ] B) Create a new version (e.g. 1.0.2), register and test it, and deliberately update the pin in `agent.json`
- [ ] C) Delete 1.0.1
- [ ] D) Edit in place and mark it deprecated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Create a new version (e.g. 1.0.2), register and test it, and deliberately update the pin in `agent.json`

**Explanation:** Never edit a released file: one name and version would refer to two different prompts, and logs would become misleading.
- **Why others are wrong:**
  - A) That breaks hygiene rule 1.
  - C) Deprecate first, delete only when no agent pins it.
  - D) Still an in-place edit of a released file.

</details>

### 27. What are the four **enforcement points** in the implemented contract, in order?

- [ ] A) Instructions, template, model, log
- [ ] B) (A) input gate, (B) parse, (C) output schema gate, (D) typed objects for consumers
- [ ] C) Parse, input gate, typed objects, schema
- [ ] D) Schema, code, human, CI

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) (A) input gate, (B) parse, (C) output schema gate, (D) typed objects for consumers

**Explanation:** Every check sits at a boundary; every rightward arrow in the diagram is a rejection, never a silent fix.
- **Why others are wrong:**
  - A) Those are agent parts, not enforcement points.
  - C) Wrong order: input is checked before the model call.
  - D) Those are validation layers, not the four contract points.

</details>

### 28. Why does `contract.py` build schema paths from `ROOT = Path(__file__).resolve().parent.parent`?

- [ ] A) To make paths shorter
- [ ] B) A relative path depends on the current working directory, which differs between terminal, IDE, pytest and CI; `ROOT` finds the schemas wherever the code runs
- [ ] C) Because `pathlib` requires it
- [ ] D) To hide the schema location

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A relative path depends on the current working directory, which differs between terminal, IDE, pytest and CI; `ROOT` finds the schemas wherever the code runs

**Explanation:** `contract.py` → `tcd/` → project folder.
- **Why others are wrong:**
  - A) Absolute paths are longer.
  - C) `pathlib` accepts relative paths.
  - D) Nothing is hidden.

</details>

### 29. What does `Draft202012Validator.check_schema(schema)` do at import time?

- [ ] A) Validates a story against the schema
- [ ] B) Validates the **schema itself** against the JSON Schema meta-schema, so a broken schema (e.g. `"minItems": "one"`) stops the agent at start-up
- [ ] C) Downloads the schema
- [ ] D) Converts the schema to Python classes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Validates the **schema itself** against the JSON Schema meta-schema, so a broken schema (e.g. `"minItems": "one"`) stops the agent at start-up

**Explanation:** Fail fast: the cheapest moment to find a broken contract is before the first story. The error is `SchemaError: 'one' is not of type 'integer'`.
- **Why others are wrong:**
  - A) That is `iter_errors` on data.
  - C) Nothing is downloaded.
  - D) Dataclasses are written by hand.

</details>

### 30. What two attributes does `ContractError` carry?

- [ ] A) `code` and `line`
- [ ] B) `stage` (`"input"`, `"parse"` or `"output"`) and `errors` (a list of messages, one per problem)
- [ ] C) `rule` and `severity`
- [ ] D) `story_id` and `verdict`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `stage` (`"input"`, `"parse"` or `"output"`) and `errors` (a list of messages, one per problem)

**Explanation:** The stage tells callers whose problem it is; the list supports "collect all errors".
- **Why others are wrong:**
  - A) Not its attributes.
  - C) Those belong to `Finding`.
  - D) Those belong to `ValidationReport`.

</details>

### 31. Why are defaults applied **once**, inside `check_input`?

- [ ] A) Because the schema cannot hold defaults
- [ ] B) Because the default for `techniques` lived in two places (instructions said EP and BVA; Thursday's renderer said "choose the techniques that fit") and they drifted; one fact, one place
- [ ] C) Because the model applies defaults badly
- [ ] D) To make the caller's dictionary smaller

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because the default for `techniques` lived in two places (instructions said EP and BVA; Thursday's renderer said "choose the techniques that fit") and they drifted; one fact, one place

**Explanation:** Every later step (template, model, validator R5/Q1) now sees the same gated story.
- **Why others are wrong:**
  - A) The schema documents a default; the point is applying it once.
  - C) The model is not the issue.
  - D) It returns a **new**, larger dict; the caller's dict is untouched.

</details>

### 32. Why is `parse_reply` deliberately **strict** about Markdown fences?

- [ ] A) Because fences break `json.loads` in all cases
- [ ] B) The contract forbids them, strictness lets you measure format failures, and repair/re-ask is a separate decision (retry strategies, Week 9)
- [ ] C) Because Tuesday's defensive parser was wrong
- [ ] D) To save tokens

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The contract forbids them, strictness lets you measure format failures, and repair/re-ask is a separate decision (retry strategies, Week 9)

**Explanation:** A forgiving parser would enforce a different contract from the written one and hide how often the model breaks format.
- **Why others are wrong:**
  - A) Not the reasoning; fences get their own explicit message.
  - C) The defensive parser is fine at the keyboard, just not in the contract layer.
  - D) Parsing does not affect tokens.

</details>

### 33. Why is it safe to write `TestCase(**tc)` in `DesignResult.from_dict`?

- [ ] A) Because dataclasses accept any keys
- [ ] B) Because it is only called after the closed output schema has guaranteed exactly the allowed keys, with all required ones present
- [ ] C) Because the model never adds fields
- [ ] D) Because `**` ignores unknown keys

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because it is only called after the closed output schema has guaranteed exactly the allowed keys, with all required ones present

**Explanation:** On unvalidated data an extra key raises `TypeError` (unexpected keyword) and a missing one raises `TypeError` (missing argument).
- **Why others are wrong:**
  - A/D) Unknown keys raise `TypeError`.
  - C) Models do add fields (e.g. `confidence`); the schema rejects them.

</details>

### 34. Which is the **dangerous** case that motivates semantic validation?

- [ ] A) A reply wrapped in fences
- [ ] B) An empty reply
- [ ] C) Schema-valid but wrong: e.g. a test that traces to a non-existent AC5, which looks perfect and is accepted downstream
- [ ] D) A reply with a `<script>` tag

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Schema-valid but wrong: e.g. a test that traces to a non-existent AC5, which looks perfect and is accepted downstream

**Explanation:** Shape errors are loud (parser/schema stop them); errors that keep the shape are quiet and surface weeks later.
- **Why others are wrong:**
  - A/B) These are loud and caught at parse.
  - D) Real, but handled by encoding downstream and flagged by B1.

</details>

### 35. Which OWASP Top 10 for LLM Applications entry does the lesson cite for treating model output as untrusted?

- [ ] A) LLM01 Prompt Injection
- [ ] B) LLM05:2025 Improper Output Handling
- [ ] C) LLM10 Model Theft
- [ ] D) LLM03 Training Data Poisoning

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) LLM05:2025 Improper Output Handling

**Explanation:** Output must be **validated**, and **encoded** where it is displayed, before it reaches downstream systems.
- **Why others are wrong:**
  - A) Prompt injection is Week 10 and about input.
  - C/D) Not cited in this lesson.

</details>

### 36. In `validate_reply`, why do parse and schema failures **stop** validation while R1–R6 failures are all collected?

- [ ] A) To save time only
- [ ] B) After a shape failure the code rules cannot trust that `story_id` or `ac_ids` exist (they would crash or produce follow-on noise); once the shape is valid, every rule runs so the reviewer sees all problems
- [ ] C) Because R-rule errors are warnings
- [ ] D) Because the schema already checks R1–R6

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) After a shape failure the code rules cannot trust that `story_id` or `ac_ids` exist (they would crash or produce follow-on noise); once the shape is valid, every rule runs so the reviewer sees all problems

**Explanation:** Fail fast on shape; collect all on meaning. `stopped_at` records where it stopped.
- **Why others are wrong:**
  - A) Correctness, not speed, is the reason.
  - C) R1–R6 are errors.
  - D) R1–R6 compare output with input, which a schema cannot do.

</details>

### 37. Q1, Q2 and the new B1 are **warnings**, not errors. Why?

- [ ] A) They are less important rules
- [ ] B) Their automated checks have known false positives (e.g. "applied successfully and the total is $45.00", or a legitimate `<b>` tag), so they flag for a human instead of blocking
- [ ] C) Because warnings are faster to compute
- [ ] D) Because the schema handles them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Their automated checks have known false positives (e.g. "applied successfully and the total is $45.00", or a legitimate `<b>` tag), so they flag for a human instead of blocking

**Explanation:** A rule you know is sometimes wrong should never block on its own.
- **Why others are wrong:**
  - A) Importance is not the criterion; reliability of the check is.
  - C) Speed is irrelevant.
  - D) They are code-layer rules.

</details>

### 38. In the `validate_output.py` exit-code contract, what does exit code **2** mean?

- [ ] A) Two replies failed
- [ ] B) The check could not run (missing file, broken story, bad arguments, or nothing to check)
- [ ] C) Warnings only
- [ ] D) All replies passed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The check could not run (missing file, broken story, bad arguments, or nothing to check)

**Explanation:** `0` = all valid, `1` = at least one reply bad, `2` = unusable. Separating 1 and 2 sends the right person to the right fix.
- **Why others are wrong:**
  - A) The count of failures is not encoded in the exit code.
  - C) Warnings exit 0 unless `--strict`.
  - D) That is 0.

</details>

### 39. In `run_requirements.py`, what does the **prompt fingerprint** tell you that the version fields do not?

- [ ] A) How much the call cost
- [ ] B) What was **actually sent**, byte for byte; versions say what was meant to be sent, so a changed fingerprint with unchanged versions reveals an unversioned edit or changed story text
- [ ] C) The model's name
- [ ] D) Whether the reply was valid

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) What was **actually sent**, byte for byte; versions say what was meant to be sent, so a changed fingerprint with unchanged versions reveals an unversioned edit or changed story text

**Explanation:** It is the first 12 hex characters of a SHA-256 hash over every `role:content` message.
- **Why others are wrong:**
  - A) Cost is not recorded by the fingerprint.
  - C) The model name is not part of the messages.
  - D) That is the outcome/verdict.

</details>

### 40. In the evaluation suite, why is the simulated model seeded with `f"{seed}-{story_id}"`?

- [ ] A) To make it faster
- [ ] B) Same seed gives the same draws, so results are reproducible, and v1.0.0 and v1.1.0 get exactly the same random draws (a **paired comparison**), so differences come from the instruction change, not luck
- [ ] C) To hide the story ID
- [ ] D) Because Python requires a seed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Same seed gives the same draws, so results are reproducible, and v1.0.0 and v1.1.0 get exactly the same random draws (a **paired comparison**), so differences come from the instruction change, not luck

**Explanation:** Also called "common random numbers". With a real model you cannot control the dice, which is one more reason to use enough runs.
- **Why others are wrong:**
  - A) Seeding does not change speed.
  - C) The story ID is part of the seed, not hidden.
  - D) `random` works without an explicit seed.

</details>

---

## Part 2: True/False

### 41. True or False: The job card is written for the model and is sent as part of the system message.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The job card is for humans. Its lines become instruction sections later (One job → Role and Goal, Not this job → Scope, Done when → Process and Rules).

</details>

### 42. True or False: In the desk-check, not every decision needs a rule; for P02 the pair's MAY list allows either boundary, so the gap was accepted.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Finding F-01 was an **accepted gap**: a rule would add length without improving the agent ("minimal but sufficient" in practice).

</details>

### 43. True or False: The author of an instruction file is the best person to review it, because they know what they meant.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The author reads what they meant, not what they wrote, for the same reason a developer is the worst tester of their own code. A teammate reviews with the job card, rule map and desk-check findings.

</details>

### 44. True or False: `agent.json` pins the instructions, template, contract version and model settings, so a behaviour change always shows up as a reviewed change to this file or a file it names.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Pinning exact files is like pinning library versions in `requirements.txt`: today's run and next week's run use the same text.

</details>

### 45. True or False: Inside `string.Template`, a value such as `$50.00` inserted into a template can become a new placeholder on a second pass.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `string.Template` scans only the template file's own text; values are inserted as plain text and never rescanned. (`$50` would not match a name anyway, because names cannot start with a digit.)

</details>

### 46. True or False: The template library's pytest suite proves that the model's answers are good.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It proves the **prompt text** is assembled correctly. Checking answers is the job of output validation, validation scripts and agent testing.

</details>

### 47. True or False: LangChain's documentation warns against rendering Jinja2 templates from untrusted sources because they can lead to arbitrary code execution.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Engines with logic can execute more than you expect; templates should come only from your reviewed repository, never from user input or model output.

</details>

### 48. True or False: Model-side "structured outputs" make your own contract code unnecessary.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Providers support only a subset of JSON Schema (e.g. `minLength`, `minimum` unsupported in Claude's structured outputs), refusals or `max_tokens` cut-offs can still break the schema, and no API feature checks R1–R6. Keep the gates in your own code.

</details>

### 49. True or False: A **PASS** verdict means the test cases are approved and can go straight into the Project 2 pytest suite.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** PASS means "no automated rule found a problem". Validation is not approval: the "Total is $40.00" example passes every rule and is wrong (Q3 needs a human).

</details>

### 50. True or False: A validator that finds no files and reports "0 checked, 0 failed" with exit code 0 is a **silent pass**, so the script exits 2 instead.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `if not results:` prints "cannot validate: no replies found" to stderr and returns `EXIT_UNUSABLE`. "Nothing checked" must never look like success.

</details>

### 51. True or False: CI should call the live model on every pull request so the agent is always tested.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Live calls cost money, are slow, need a secret key in the pipeline and vary between runs. CI checks deterministic things: validator tests, schemas, templates, committed replies.

</details>

### 52. True or False: In the run over the Project 2 backlog, 6 stories cost only 5 model calls because the input gate rejected US-52 before the model was called.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** US-52 failed `'^US-[0-9]{3}$'`, so its outcome is `rejected_input` and its fingerprint is `None`. On a real provider that is a call you did not pay for.

</details>

### 53. True or False: When US-412's output failed R2 for an invented case-insensitive search rule, the right action was to add that rule to the requirement because it is a good idea.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Reject the output, never hand-patch it, and never let an agent quietly rewrite a requirement. If the idea seems valuable, raise it with the product owner as a question.

</details>

---

## Part 3: Code Prediction

### 54. Using `split_sections` from `tcd/instructions.py`, what does this print?

```python
import re
text = "# T\nintro\n## A\none\n## B\ntwo\nthree\n"
parts = re.split(r"^##\s+(.+)$", text, flags=re.MULTILINE)
d = {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}
print(len(d), repr(d["B"]))
```

- [ ] A) `3 'two'`
- [ ] B) `2 'two\nthree'`
- [ ] C) `2 'two three'`
- [ ] D) `1 '\ntwo\nthree\n'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2 'two\nthree'`

**Explanation:** The capturing group keeps headings in the result: `['# T\nintro\n', 'A', '\none\n', 'B', '\ntwo\nthree\n']`. Odd positions are headings, the next item is the body, and `.strip()` removes outer newlines only. The preamble is skipped.
- **Why others are wrong:**
  - A) The preamble is not a section; B's body keeps both lines.
  - C) `strip()` does not touch the inner newline.
  - D) Two headings give two entries, and the body is stripped.

</details>

### 55. What does `flat` from `check_rule_map.py` return?

```python
def flat(text: str) -> str:
    return " ".join(text.split())

print(repr(flat("a  b\n   c")))
```

- [ ] A) `'a  b\n   c'`
- [ ] B) `'a b c'`
- [ ] C) `'abc'`
- [ ] D) `'a b\nc'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `'a b c'`

**Explanation:** `split()` with no argument splits on any run of whitespace, giving `['a', 'b', 'c']`. Comparing flattened text lets a phrase match even after a harmless re-wrap.
- **Why others are wrong:**
  - A) The whitespace is collapsed.
  - C) `join` uses a single space.
  - D) The newline is also whitespace.

</details>

### 56. What does this print?

```python
INPUT_DEFAULTS = {"techniques": ["EP", "BVA"], "max_cases": 10}
story = {"story_id": "US-205", "max_cases": 6}
print({**INPUT_DEFAULTS, **story}["max_cases"], {**story, **INPUT_DEFAULTS}["max_cases"])
```

- [ ] A) `6 6`
- [ ] B) `10 10`
- [ ] C) `6 10`
- [ ] D) `10 6`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `6 10`

**Explanation:** When unpacked dictionaries share a key, the **later** one wins. The correct `check_input` order puts `story` last; the swapped order silently forces every caller's `max_cases` back to 10, which `test_caller_value_wins_over_default` would catch.
- **Why others are wrong:**
  - A/B) The two orders give different results.
  - D) Reversed.

</details>

### 57. What does `_messages` produce for these two error paths?

```python
for path in (["test_cases", 0, "priority"], []):
    print("/".join(str(p) for p in path) or "(root)")
```

- [ ] A) `test_cases/0/priority` then an empty line
- [ ] B) `test_cases/0/priority` then `(root)`
- [ ] C) `TypeError` because 0 is an int
- [ ] D) `test_cases.0.priority` then `(root)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `test_cases/0/priority` then `(root)`

**Explanation:** `str(p)` converts the integer index. An empty path joins to `''`, which is falsy, so `or` substitutes the readable `(root)`.
- **Why others are wrong:**
  - A) `or` replaces the empty string.
  - C) `str(p)` prevents the error.
  - D) The separator is `/`.

</details>

### 58. What happens with each reply passed to `check_output_schema(parse_reply(reply))`?

```python
replies = {
    "fenced": '```json\n{"story_id": "US-205"}\n```',
    "list":   '[{"id": "TC-205-01"}]',
    "wrong object": '{"story_id": "US-205", "tests": []}',
}
```

- [ ] A) All three fail at stage `output`
- [ ] B) `fenced` → stage `parse`; `list` → stage `parse`; `wrong object` → stage `output` with five errors
- [ ] C) `fenced` passes after the fences are stripped
- [ ] D) `list` → stage `output`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `fenced` → stage `parse`; `list` → stage `parse`; `wrong object` → stage `output` with five errors

**Explanation:** Fences and non-objects never reach the schema. The wrong object is missing four required properties and has the unexpected `tests` field (`additionalProperties: false`).
- **Why others are wrong:**
  - A) You cannot schema-check text that is not a JSON object.
  - C) The strict parser rejects fences.
  - D) "reply must be a JSON object, got list" is a parse error.

</details>

### 59. Given the `ValidationReport.verdict` property, what is printed?

```python
findings = [Finding("Q1", "warning", "test_cases", "..."),
            Finding("Q2", "warning", "test_cases[0].expected_result", "...")]
report = ValidationReport(story_id="US-205", findings=findings)
print(report.verdict)
```

- [ ] A) `PASS`
- [ ] B) `PASS_WITH_WARNINGS`
- [ ] C) `FAIL`
- [ ] D) `WARNING`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `PASS_WITH_WARNINGS`

**Explanation:** Any error → FAIL; otherwise any warning → PASS_WITH_WARNINGS; otherwise PASS. There are no errors here.
- **Why others are wrong:**
  - A) There are warnings.
  - C) No error findings.
  - D) Not a valid verdict.

</details>

### 60. What does this print, and which rule depends on it?

```python
import re
print(bool(re.search(r"\bAC1\b", "AC10: is this final?")),
      bool(re.search(r"\bAC1\b", "AC1: is this final?")))
```

- [ ] A) `True True`, rule R2
- [ ] B) `False True`, rule R3
- [ ] C) `True False`, rule R3
- [ ] D) `False False`, rule R6

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `False True`, rule R3

**Explanation:** `\b` is a word boundary, so `AC1` does not match inside `AC10`. R3 uses this so a question naming `AC12` does not count as mentioning `AC1`. (`trace_matrix.py`'s plain `in` check has exactly this bug.)
- **Why others are wrong:**
  - A) That is the result without `\b`.
  - C) Reversed.
  - D) The second string does contain the whole word `AC1`.

</details>

### 61. In `validate_output.py`, what is `failed` after this loop?

```python
failed = 0
for verdict in ["PASS", "FAIL", "FAIL (strict)", "PASS_WITH_WARNINGS"]:
    failed += verdict.startswith("FAIL")
print(failed)
```

- [ ] A) `1`
- [ ] B) `2`
- [ ] C) `3`
- [ ] D) `TypeError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2`

**Explanation:** `startswith` returns a bool, and `True` counts as 1 when added. Both `"FAIL"` and `"FAIL (strict)"` count; `PASS_WITH_WARNINGS` does not (without `--strict` it was never relabelled).
- **Why others are wrong:**
  - A) Misses the strict failure.
  - C) `PASS_WITH_WARNINGS` does not start with "FAIL".
  - D) Adding bools to ints is valid Python.

</details>

### 62. What does this grouping (the core of `load_backlog`) print?

```python
from collections import OrderedDict
rows = [("US-101", "AC1"), ("US-101", "AC2"), ("US-205", "AC1"), ("US-101", "AC3")]
stories = OrderedDict()
for sid, ac in rows:
    stories.setdefault(sid, {"acs": []})["acs"].append(ac)
print(len(stories), [len(v["acs"]) for v in stories.values()])
```

- [ ] A) `4 [1, 1, 1, 1]`
- [ ] B) `2 [3, 1]`
- [ ] C) `3 [2, 1, 1]`
- [ ] D) `2 [2, 1]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2 [3, 1]`

**Explanation:** `setdefault` returns the existing object for a known key, so every US-101 row (even the later one) appends to the same story. Order follows first appearance.
- **Why others are wrong:**
  - A) Rows are grouped, not kept separate.
  - C) The fourth row joins the existing US-101.
  - D) US-101 ends up with three ACs.

</details>

### 63. What does this print in `check_versions.py`?

```python
print("https://example.com/schemas/tcd/output/1.0.0".rsplit("/", 1)[1])
```

- [ ] A) `https:`
- [ ] B) `output/1.0.0`
- [ ] C) `1.0.0`
- [ ] D) `['https://example.com/schemas/tcd/output', '1.0.0']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1.0.0`

**Explanation:** `rsplit("/", 1)` splits once from the right, and `[1]` takes the last part: the version in the schema's `$id`.
- **Why others are wrong:**
  - A) That would be `split` and `[0]`.
  - B) Only one split happens, at the last `/`.
  - D) `[1]` selects the second element, not the whole list.

</details>

### 64. What does this print (the evaluation's rule counters)?

```python
from collections import Counter
rule_failures = Counter()
rule_failures.update(["R3", "R6"])
rule_failures.update(["R3"])
print(rule_failures["R3"], rule_failures["R2"])
```

- [ ] A) `2 0`
- [ ] B) `1 0`
- [ ] C) `2` then `KeyError`
- [ ] D) `3 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `2 0`

**Explanation:** `update` adds 1 per item; a missing key in a `Counter` returns 0 instead of raising.
- **Why others are wrong:**
  - B) R3 was added twice.
  - C) `Counter` never raises `KeyError` on lookup.
  - D) Only two R3s were added.

</details>

### 65. What does this print?

```python
from string import Template
print(Template("Total $amount").substitute(amount="$50.00"))
```

- [ ] A) `Total $amount`
- [ ] B) `Total $50.00`
- [ ] C) `KeyError: '50'`
- [ ] D) `ValueError: Invalid placeholder`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Total $50.00`

**Explanation:** Only the template text is scanned for placeholders; the value is inserted as-is. That is why stories containing dollar amounts are safe in the library.
- **Why others are wrong:**
  - A) `amount` is supplied.
  - C/D) The value is never re-parsed.

</details>

### 66. What does this print?

```python
values = {"story_id", "title", "max_cases", "techniques"}
uses = {"story_id", "title", "acceptance_criteria"}       # story_block@1.0.0
print(sorted(values - uses))
```

- [ ] A) `['acceptance_criteria']`
- [ ] B) `['max_cases', 'techniques']`
- [ ] C) `[]`
- [ ] D) `['story_id', 'title']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['max_cases', 'techniques']`

**Explanation:** Set difference keeps what the caller passed but the template does not use. In `render()` this produces `KeyError: "story_block@1.0.0 does not use: ['max_cases', 'techniques']"`.
- **Why others are wrong:**
  - A) That is `uses - values` (a missing value).
  - C) Two keys are unexpected.
  - D) Those are used by the partial.

</details>

---

## Part 4: Fill-in-the-Blank

### 67. `@dataclass(___=True)` makes instances read-only, so `ins.version = "9.9.9"` raises an error.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `frozen`

**Explanation:** Used for `Instructions`, `TestCase` and `DesignResult`: loaded instructions and agent output are evidence that nothing should quietly change.

</details>

### 68. In a dataclass, an optional list field is written `preconditions: list = field(___=list)` rather than `= []`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `default_factory`

**Explanation:** It creates a new empty list per instance; a plain `[]` would be shared by every instance, so dataclasses reject it. Defaulted fields must also come last.

</details>

### 69. argparse's `add_mutually_exclusive_group(___=True)` makes exactly one of `--story` or `--run` mandatory.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `required`

**Explanation:** Without it, neither option could be given. The usage line shows it as `(--story STORY | --run RUN)`.

</details>

### 70. The run log `run.jsonl` uses the ___ format: one complete JSON object per line.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** JSON Lines

**Explanation:** You can append a line at a time, read it line by line and search it with ordinary tools (`grep US-412 runs/demo/run.jsonl`).

</details>

### 71. The first measurement of the current version, used as the reference for every later comparison, is called the ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** baseline

**Explanation:** v1.0.0 scored 47/81 = 58%; v1.1.0 scored 69/81 = 85% on the same suite and seeds. Without a baseline, "it looks better" is only a feeling.

</details>

---

## Part 5: Matching

### 72. Match each `check_rule_map.py` problem (1-4) to its meaning (A-D).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | DRIFT | | A | A bullet in Rules, Output or Uncertainty has no map entry |
| 2 | BAD ID | | B | A map phrase is no longer found in its section (rule reworded or deleted) |
| 3 | NO CHECK | | C | A map entry has an empty `checks` list |
| 4 | UNMAPPED | | D | A check ID is not in `KNOWN_CHECKS` (e.g. a typo such as `R7`) |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-C, 4-A

**Explanation:** Part 1 checks map → file (DRIFT, BAD ID, NO CHECK); part 2 checks file → map (UNMAPPED). It checks that rules are mapped, not that the mapped check really catches violations.

</details>

### 73. Match each validation rule (1-6) to what it catches (A-F).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | R1 | | A | Status `ok` with no test cases, or `needs_clarification` with no questions |
| 2 | R2 | | B | An input AC neither covered by a test case nor named in an open question |
| 3 | R3 | | C | Output `story_id` differs from the input's |
| 4 | R4 | | D | Duplicate test case IDs, or IDs not using the story number |
| 5 | R5 | | E | An `ac_ids` entry that does not exist in the input |
| 6 | R6 | | F | More test cases than `max_cases` |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-B, 4-D, 5-F, 6-A

**Explanation:** All six compare the output with the input or check cross-field consistency, which a schema alone cannot do. Replacing AC1 with AC9 fires both R2 and R3: one defect, two consequences.

</details>

### 74. Match each run outcome (1-5) to its action and owner (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `rejected_input` | | A | Normal human review; reviewer (tester) |
| 2 | `FAIL` (S1) | | B | Fix the story in the backlog and re-run; backlog owner (BA / PO) |
| 3 | `FAIL` (R1–R6) | | C | Human review starting with the warnings; reviewer |
| 4 | `PASS_WITH_WARNINGS` | | D | Reject, log for refinement, never hand-patch; agent owner (QE) |
| 5 | `PASS` + `ok` | | E | Reject; reply unusable as data; count it (retries: Week 9); agent owner (QE) |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-E, 3-D, 4-C, 5-A

**Explanation:** Every outcome gets an action and an owner. A hand-patched output would look like agent output but is not, so the evidence would lie.

</details>

### 75. Match each v1.1.0 instruction change (1-4) to the evidence or decision behind it (A-D).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Process: coverage self-check before replying | | A | 11 R2 errors (invented AC5 test cases) |
| 2 | Rules: use only input AC IDs; never create AC5 | | B | Desk-check finding F-02, decided by the QE lead |
| 3 | Style: expected_result names an exact total, message, page or state | | C | 18 R3 and 11 R6 errors from dropped open questions |
| 4 | Uncertainty: `needs_clarification` whenever any AC needs clarification | | D | 9 Q2 warnings ("works correctly") |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-A, 3-D, 4-B

**Explanation:** Each change is recorded in the changelog with its evidence. S1 (5) and R5 (7) were not targeted and stay behind the validation gate until Week 9. This is a MINOR bump: new guaranteed behaviour, same contract 1.0.0.

</details>
