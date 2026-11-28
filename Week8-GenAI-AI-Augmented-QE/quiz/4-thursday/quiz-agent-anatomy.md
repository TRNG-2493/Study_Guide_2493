# Weekly Knowledge Check: [Week8-GenAI-AI-Augmented-QE] — Thursday: Agent Anatomy

**Covers:** Agent architecture · Agent instructions · Prompt templates · Input/output contracts · JSON Schema · Required fields and validation rules · Sample input/output pairs
**Questions:** 50 · **Formats:** Multiple Choice, True/False, Code Prediction, Fill-in-the-Blank

> **Context:** This week's agent is **TestCaseDesigner**. It turns one user story (such as US-205, US-311, US-312) into test cases in a fixed JSON format with the top-level fields `story_id`, `status`, `test_cases` and `open_questions`.

---

## Part 1: Multiple Choice

### 1. How does this course define an AI agent?
- [ ] A) Any chatbot conversation
- [ ] B) An AI model set up to do one specific job the same way every time, with fixed instructions, an input template, a fixed output format, examples and checks
- [ ] C) A model that browses the web on its own
- [ ] D) A model that retrains itself after each run

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Its main benefit is checkable answers: the same shape every time, so code and people can review every reply in the same way.
- **Why others are wrong:**
  - A) A one-off chat has no fixed format or checks.
  - C) Autonomy is not part of this course's definition.
  - D) An agent does not learn between runs.
</details>

---

### 2. Which list gives the six parts of the agent?
- [ ] A) Role and goal, instructions (rules), input template, output format, examples, checks
- [ ] B) Model, GPU, API key, temperature, top-p, max tokens
- [ ] C) Story, epic, sprint, backlog, board, release
- [ ] D) Prompt, reply, retry, log, alert, dashboard

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** These six parts make up the reusable package for one job.
- **Why others are wrong:**
  - B) These are infrastructure and settings.
  - C) These are agile planning terms.
  - D) These are operational concerns, not the agent's parts.
</details>

---

### 3. Which part of the agent is **never** sent to the AI?
- [ ] A) The examples
- [ ] B) The input template
- [ ] C) The checks
- [ ] D) The instructions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The checks

**Explanation:** The checks are for people: a script and a human checklist that decide whether each reply is good.
- **Why others are wrong:**
  - A), B), D) All three are part of the full agent prompt.
</details>

---

### 4. Two runs of the same one-off prompt gave 7 and 12 test cases. Which agent parts fix this?
- [ ] A) The examples and the checks
- [ ] B) The instructions (a rule limiting the number of cases) and the input template (which states the maximum per story)
- [ ] C) The temperature and the model
- [ ] D) Nothing can fix this

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Most problems with one-off prompts map to a specific agent part. Ask which part allowed the problem.
- **Why others are wrong:**
  - A) Checks detect the problem but do not stop it happening.
  - C) These are model settings, not agent parts.
  - D) A checkable rule plus `$max_cases` fixes it.
</details>

---

### 5. Your agent makes the same mistake on every story for a week. What should you do?
- [ ] A) Wait; it will learn from its mistakes
- [ ] B) Find which part allows the mistake (such as a vague rule or bad example) and change that file
- [ ] C) Switch to a new chat each time
- [ ] D) Raise the temperature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** An agent does not learn by itself. You improve it by changing its files.
- **Why others are wrong:**
  - A) Nothing changes between runs unless you change something.
  - C) Each run already uses a new chat.
  - D) Randomness does not fix a systematic mistake.
</details>

---

### 6. By Anthropic's definitions, is TestCaseDesigner closer to a workflow or an agent?
- [ ] A) An agent, because it uses an LLM
- [ ] B) A workflow, because our code decides every step in a fixed order
- [ ] C) Neither
- [ ] D) An agent, because it outputs JSON

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A workflow

**Explanation:** In Anthropic's sense, an agent directs its own steps and tool use. The course uses "agent" more broadly.
- **Why others are wrong:**
  - A) Using an LLM does not by itself make a system an agent in Anthropic's sense.
  - C) It fits the workflow definition.
  - D) The output format is irrelevant to this distinction.
</details>

---

### 7. When is it worth building an agent rather than saving a one-off prompt?
- [ ] A) Whenever you use AI
- [ ] B) When the same job repeats on many inputs, needs the same output shape, or feeds results that people or code depend on
- [ ] C) Only for tasks under 5 minutes
- [ ] D) When the task varies a lot each time

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A saved prompt is enough for occasional tasks that vary.
- **Why others are wrong:**
  - A) Agents have a build cost that is only worth paying for repeated work.
  - C) Duration is not the criterion.
  - D) Varying tasks suit saved prompts better.
</details>

---

### 8. Which list gives the five sections of TestCaseDesigner's instructions?
- [ ] A) Role and goal, scope, rules, output, when something is unclear
- [ ] B) Intro, body, conclusion, references, appendix
- [ ] C) Input, process, output, storage, logging
- [ ] D) Given, when, then, and, but

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** These five sections are sent with every story, so their strengths and weaknesses repeat on every run.
- **Why others are wrong:**
  - B) That is essay structure.
  - C) That is a generic system diagram.
  - D) These are Gherkin keywords.
</details>

---

### 9. What makes a rule in the instructions "checkable"?
- [ ] A) It is written in capital letters
- [ ] B) You can look at a reply and say clearly whether it was followed, often because the rule has a number, exact format or example
- [ ] C) It is longer than one sentence
- [ ] D) It uses the word "must"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "At most `$max_cases` test cases" is checkable. "Be thorough" is not.
- **Why others are wrong:**
  - A), D) Emphasis does not make a rule checkable.
  - C) Length is irrelevant.
</details>

---

### 10. Why does the "When something is unclear" section reduce invented answers?
- [ ] A) It tells the AI to try harder
- [ ] B) It gives a permitted alternative to guessing: add a question to `open_questions`, starting with the AC id
- [ ] C) It lowers the temperature
- [ ] D) It removes vague stories

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Without this "way out", the AI's easiest option is to invent a value.
- **Why others are wrong:**
  - A) Effort is not the problem. Having no alternative to guessing is.
  - C) Text in the instructions does not change model settings.
  - D) Vague stories still arrive. The section tells the AI what to do with them.
</details>

---

### 11. Why does the Scope section name specific exclusions, such as performance and security tests?
- [ ] A) Those tests are illegal
- [ ] B) AIs like to be extra helpful and often add them; naming them makes replies smaller and easier to check
- [ ] C) The schema cannot store them
- [ ] D) To make the instructions longer

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** One agent, one job. A clear scope keeps the reply focused.
- **Why others are wrong:**
  - A) They are valid tests, just outside this agent's job.
  - C) This is about scope, not storage.
  - D) Length is not the goal.
</details>

---

### 12. The instructions say "Write at least 6 test cases" and the story says "Maximum test cases: 5". What is this instruction smell?
- [ ] A) Scope creep
- [ ] B) A contradiction: the AI must break one rule, and you cannot predict which, so results become inconsistent
- [ ] C) A leftover placeholder
- [ ] D) Example leakage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A contradiction

**Explanation:** Two rules that cannot both be followed lead to unpredictable behaviour.
- **Why others are wrong:**
  - A) No extra features are being added.
  - C) Both values are filled in.
  - D) No example details are being copied.
</details>

---

### 13. How can you prove that a section of the instructions is doing real work?
- [ ] A) Ask the AI whether it read it
- [ ] B) Make a controlled change: remove only that section, run the same story in a new chat, and compare replies with the checklist
- [ ] C) Make it bold
- [ ] D) Count its words

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Change one thing only, so any difference in results is caused by that change.
- **Why others are wrong:**
  - A) The AI's self-report is not evidence.
  - C) Formatting does not prove anything.
  - D) Word count does not show the section has an effect.
</details>

---

### 14. What is the difference between the instructions and the prompt template?
- [ ] A) They are the same thing
- [ ] B) The instructions never change between stories; the template carries the part that changes: the story
- [ ] C) The template holds the rules; the instructions hold the story
- [ ] D) The instructions are optional

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Fixed rules go in the instructions. Per-story data goes in template placeholders.
- **Why others are wrong:**
  - A) They have different jobs.
  - C) This is reversed.
  - D) The instructions are the agent's standing orders.
</details>

---

### 15. Why does the filled template go **last** in the full agent prompt?
- [ ] A) Alphabetical order
- [ ] B) So the AI reads the rules and examples first, and the message ends with the task right after the story; otherwise it might answer an example instead
- [ ] C) To save tokens
- [ ] D) It does not matter where it goes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The full agent prompt is instructions, then examples, then the filled template.
- **Why others are wrong:**
  - A) There is a real reason for the order.
  - C) Order does not change the token count.
  - D) Order affects which content the AI responds to.
</details>

---

### 16. Why does the template put the story between `### Story` and `### End of story`?
- [ ] A) For decoration
- [ ] B) These delimiters show exactly where the story starts and ends, so the AI does not confuse it with instructions or examples
- [ ] C) JSON requires them
- [ ] D) They encrypt the story

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** These markers are called fences. They separate data from instructions.
- **Why others are wrong:**
  - A) They have a real job.
  - C) The template is plain text, not JSON.
  - D) They do not encrypt anything.
</details>

---

### 17. You want the agent to know whether each story is for web or mobile. Where should this go?
- [ ] A) In the instructions, as a fixed rule
- [ ] B) In the template, as a new placeholder such as `$platform`, because it changes from story to story
- [ ] C) In the checks
- [ ] D) In the examples only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Anything that varies per story belongs in the template. Fixed rules belong in the instructions.
- **Why others are wrong:**
  - A) A fixed rule cannot hold a value that changes per story.
  - C) Checks are never sent to the AI.
  - D) Examples cannot carry real per-story data.
</details>

---

### 18. Why should you fill a **copy** of the template, not the template itself?
- [ ] A) Copies use fewer tokens
- [ ] B) The template is reused for every story; overwriting it removes the placeholders for the next story
- [ ] C) Templates are read-only
- [ ] D) The AI only reads copies

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The template is the reusable master. Each run fills a fresh copy.
- **Why others are wrong:**
  - A) Token count is not affected.
  - C) The file is not read-only. Keeping the master clean is a convention.
  - D) The AI sees whatever text you send it.
</details>

---

### 19. What are the two sides of an agent's input/output contract?
- [ ] A) Request and response headers
- [ ] B) The input (what a story looks like going in) and the output (what every reply must look like)
- [ ] C) The tester and the developer
- [ ] D) The schema and the validator

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The contract is the definition of "a valid answer", and every check is built from it.
- **Why others are wrong:**
  - A) HTTP headers are not part of this contract.
  - C) These are people, not contract sides.
  - D) These are tools derived from the contract.
</details>

---

### 20. For every field, which four things does the contract state?
- [ ] A) Name, kind (text, number, list, object), whether it is required, and its rule for valid values
- [ ] B) Name, author, date, version
- [ ] C) Type, colour, font, size
- [ ] D) Key, value, index, hash

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** These four facts make the contract precise enough for a schema and rules to be built from it.
- **Why others are wrong:**
  - B) That is document metadata.
  - C) Those are display properties.
  - D) These are general data-structure terms.
</details>

---

### 21. How does TestCaseDesigner say "I can't test this story"?
- [ ] A) It returns an empty reply
- [ ] B) `status: "needs_clarification"`, an empty `test_cases` list, and open questions starting with the AC id
- [ ] C) It writes "ERROR" in plain text
- [ ] D) It invents reasonable values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A defined refusal is honest and checkable, and it can be counted and reported.
- **Why others are wrong:**
  - A), C) Both break the contract.
  - D) Inventing values is exactly what the refusal exists to prevent.
</details>

---

### 22. The team adds a `priority` field to test cases. Which files must change?
- [ ] A) Only the schema
- [ ] B) The contract (and its version), the instructions' Output section, every example reply, and the checker
- [ ] C) Only the examples
- [ ] D) None; the AI will figure it out

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The contract is the source of truth, and every file built from it must stay in step.
- **Why others are wrong:**
  - A), C) Updating only one file leaves the others inconsistent.
  - D) The AI only follows what the prompt says.
</details>

---

### 23. What does the JSON Schema keyword `enum` do?
- [ ] A) Counts the items in a list
- [ ] B) Lists the only allowed values, compared exactly (so `"OK"` is not `"ok"`)
- [ ] C) Makes a field optional
- [ ] D) Gives a regex

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** For example, `"status": {"enum": ["ok", "needs_clarification"]}`.
- **Why others are wrong:**
  - A) `minItems` sets a minimum list length. `enum` does not count anything.
  - C) A field is optional when it is not listed in `required`.
  - D) `pattern` gives a regex.
</details>

---

### 24. A validator reports `test_cases/1: 'expected_result' is a required property`. Which test case is it about?
- [ ] A) The first
- [ ] B) The second
- [ ] C) The eleventh
- [ ] D) All of them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The second

**Explanation:** Paths count from 0, so item 1 is the second test case.
- **Why others are wrong:**
  - A) The first would be `test_cases/0`.
  - C) The 1 is an index, not a two-digit number.
  - D) The path points to one specific item.
</details>

---

### 25. Why did adding `"additionalProperties": false` to the test-case schema make valid test cases fail?
- [ ] A) The keyword is invalid
- [ ] B) It allows only fields listed under `properties`, and the schema only listed `id` and `type` there, so every other required field counted as extra
- [ ] C) It made every field optional
- [ ] D) It changed the IDs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** `required` and `properties` are separate lists. `additionalProperties` only checks against `properties`.
- **Why others are wrong:**
  - A) It is a standard keyword.
  - C) It made the schema stricter, not looser.
  - D) It does not modify data.
</details>

---

### 26. When an AI's schema check and a real validator disagree, which do you trust?
- [ ] A) The AI, because it explains its reasoning
- [ ] B) The validator, because it is deterministic and applies the schema exactly
- [ ] C) Whichever finds more problems
- [ ] D) Neither

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The validator

**Explanation:** The AI is useful for explaining, but it can miss problems or invent them.
- **Why others are wrong:**
  - A) An explanation is not evidence.
  - C) More findings may include invented ones.
  - D) The validator is reliable for shape.
</details>

---

### 27. A reply has `"ac_ids": ["AC9"]` for US-205, which has no AC9. Why does the schema not catch it?
- [ ] A) The schema is broken
- [ ] B) The schema only sees the reply; knowing which AC ids exist needs the story, so a validation rule must compare them
- [ ] C) AC9 matches the enum
- [ ] D) Schemas cannot check lists

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is rule R2, which checks that no ACs are invented. A schema checks shape, not meaning.
- **Why others are wrong:**
  - A) The schema works as designed.
  - C) There is no AC enum in the schema.
  - D) Schemas check lists with `items`. They just cannot see the story.
</details>

---

### 28. What is the difference between a **missing** field and an **empty** one?
- [ ] A) No difference
- [ ] B) Missing means not there at all (the reply is broken); empty means present with nothing in it, such as `[]`, which can be fine
- [ ] C) Empty is always an error; missing is fine
- [ ] D) Missing means `null`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Because every field in the contract is required, an absence always means the reply is broken.
- **Why others are wrong:**
  - A) The difference changes the verdict.
  - C) This is reversed.
  - D) A field set to `null` is present.
</details>

---

### 29. Why is rule R1 (right story ID) checked first?
- [ ] A) It is the fastest
- [ ] B) If the reply is for the wrong story, every other rule compares it with the wrong ACs and limit, so their results are meaningless
- [ ] C) Alphabetical order
- [ ] D) The schema requires it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** R1 sets the frame for R2–R4.
- **Why others are wrong:**
  - A) Speed is not the reason.
  - C) The order is deliberate.
  - D) Rules are separate from the schema.
</details>

---

### 30. What does rule R4 check, and why does an open question count?
- [ ] A) That there are at least 4 test cases
- [ ] B) That every AC has a test case or an open question starting with its id; a question shows the AC was considered, not forgotten
- [ ] C) That the reply is under 4 KB
- [ ] D) That the status is "ok"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** For an incomplete AC such as US-205 AC4, a question is the honest answer.
- **Why others are wrong:**
  - A) The count limit is R3.
  - C) Size is not checked.
  - D) `needs_clarification` is also valid.
</details>

---

### 31. Which two mistakes pass the schema **and** all five rules (R1–R4, Q1)?
- [ ] A) Wrong story ID and invented AC
- [ ] B) An invented value (such as "within 2 seconds") and a missing boundary test (such as no case at $49.99)
- [ ] C) A missing field and a wrong enum
- [ ] D) Too many test cases and vague results

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Only a person catches these. That is why the human checklist stays essential.
- **Why others are wrong:**
  - A) R1 and R2 catch these.
  - C) The schema catches these.
  - D) R3 and Q1 catch these.
</details>

---

### 32. What two jobs does a sample input/output pair do?
- [ ] A) It speeds up the model and lowers cost
- [ ] B) It documents what a good answer looks like and, in the prompt, works as a few-shot example the AI copies
- [ ] C) It replaces the schema and the rules
- [ ] D) It trains the model permanently

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Show, don't tell. One example teaches the shape, the ID format and honest refusal.
- **Why others are wrong:**
  - A) Examples add tokens to every request.
  - C) Checks are still needed.
  - D) In-context learning is not permanent.
</details>

---

### 33. Why are the examples about US-150 and US-160 rather than the real stories?
- [ ] A) Those numbers are lucky
- [ ] B) To teach the pattern without giving away answers for the real stories, and so a copied ID or answer is easy to spot
- [ ] C) The real stories are confidential
- [ ] D) The schema rejects real IDs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Different stories make example leakage visible.
- **Why others are wrong:**
  - A) The choice is deliberate, not luck.
  - C) Confidentiality is not the reason.
  - D) Any `US-` plus three digits passes the schema.
</details>

---

### 34. Example 1 says "Delivery cost is not $0.00" instead of a price such as $4.99. Why?
- [ ] A) $4.99 is too specific for JSON
- [ ] B) The story gives no delivery price, so writing one would invent a value
- [ ] C) Negative assertions are always better
- [ ] D) To save characters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Every example must pass every rule, including the human check for invented values, because the AI copies mistakes too.
- **Why others are wrong:**
  - A) JSON can hold any value.
  - C) The wording follows what the story allows, not a preference for negatives.
  - D) Length is irrelevant.
</details>

---

### 35. What is example leakage?
- [ ] A) Examples being stolen
- [ ] B) The AI copying details of an example into an unrelated reply, such as `"story_id": "US-150"` in a reply for US-205
- [ ] C) Examples being cut off by the context window
- [ ] D) Examples that fail the schema

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Another sign is a $30.00 test case copied from an example into US-205.
- **Why others are wrong:**
  - A) This is about AI behaviour, not security.
  - C) That would be a context problem.
  - D) That is a broken example, which is a different problem.
</details>

---

## Part 2: True / False

### 36. True or False: An agent improves automatically the more stories it processes.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** An agent does not learn between runs. You improve it by changing its files.
</details>

---

### 37. True or False: The sample US-311 reply had all four keys and a valid ID, so it was correct.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It invented "2 seconds". It should have returned `needs_clarification` with an AC1 question. A correct shape does not mean a correct answer.
</details>

---

### 38. True or False: `open_questions` can be left out of a reply when the agent has no questions.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is required, so it must always be present. It can be **empty** (`[]`) when there are no questions.
</details>

---

### 39. True or False: Inside a JSON string, a quote character must be written as `\"`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A plain `"` would end the string early and break the file. This is why AC2's quoted message is escaped.
</details>

---

### 40. True or False: If an AI provider enforces your schema with Structured Outputs, you no longer need validation rules or human review.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Enforcing the schema removes shape problems, but wrong amounts and invented AC ids still match the schema.
</details>

---

### 41. True or False: The three layers of checking are schema (shape), rules (reply against story) and person (meaning).
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Each layer catches what the one before it cannot.
</details>

---

### 42. True or False: Because the vague example comes last in `examples.txt`, a tester should check that a clear story such as US-312 still gets test cases and `status: "ok"`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Because of the recency effect, example order can influence replies, so the order is worth testing.
</details>

---

## Part 3: Code Prediction

### 43. What does this print?
```python
import re
p = re.compile(r"^US-[0-9]{3}$")
print([bool(p.match(s)) for s in ["US-205", "US-2050", "us-205", "US-31"]])
```
- [ ] A) `[True, True, True, False]`
- [ ] B) `[True, False, False, False]`
- [ ] C) `[True, True, False, False]`
- [ ] D) `[True, False, True, False]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[True, False, False, False]`

**Explanation:** The pattern needs uppercase `US-` followed by exactly three digits and then the end of the text.
- **Why others are wrong:**
  - A), C) "US-2050" has four digits, so `$` fails.
  - D) The regex is case-sensitive, so "us-205" fails.
</details>

---

### 44. What does this print?
```python
from string import Template
t = Template("Story: $story_id\nMax cases: $max_cases")
print(t.safe_substitute(story_id="US-205"))
```
- [ ] A) `Story: US-205` then `Max cases: ` (blank)
- [ ] B) `Story: US-205` then `Max cases: $max_cases`
- [ ] C) `KeyError: 'max_cases'`
- [ ] D) `Story: $story_id` then `Max cases: $max_cases`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** `safe_substitute` leaves unknown placeholders as they are. This is a **leftover placeholder** that would reach the AI as `$max_cases`.
- **Why others are wrong:**
  - A) It does not replace missing values with blanks.
  - C) Only `substitute()` raises a KeyError.
  - D) `story_id` was provided and filled.
</details>

---

### 45. Same template, but using `substitute`. What happens?
```python
t.substitute(story_id="US-205")
```
- [ ] A) It returns the text with `$max_cases` left in
- [ ] B) It raises `KeyError: 'max_cases'`
- [ ] C) It returns an empty string
- [ ] D) It fills `max_cases` with 0

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** `substitute` fails loudly on a missing value. That is useful because it stops a half-filled prompt from being sent.
- **Why others are wrong:**
  - A) That is how `safe_substitute` behaves.
  - C), D) Python never silently invents a value here.
</details>

---

### 46. A filled US-205 prompt still contains a leftover. What does this print?
```python
import re
filled = "Spend $50.00 to use SAVE10. Max: $max_cases"
print(re.findall(r"\$[a-z_]+", filled), len(re.findall(r"\$", filled)))
```
- [ ] A) `['$max_cases'] 2`
- [ ] B) `['$50', '$max_cases'] 2`
- [ ] C) `[] 2`
- [ ] D) `['$max_cases'] 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `['$max_cases'] 2`

**Explanation:** Searching for plain `$` also finds the dollar amount. Searching for `$` followed by letters finds only real placeholders.
- **Why others are wrong:**
  - B) `5` is a digit, so `$50` does not match `[a-z_]`.
  - C) `$max_cases` does match.
  - D) There are two `$` characters.
</details>

---

### 47. What does this print?
```python
reply = {"story_id": "US-205", "test_cases": []}
print(reply["test_cases"] == [], "open_questions" in reply)
try:
    reply["open_questions"]
except KeyError as e:
    print("KeyError", e)
```
- [ ] A) `True True`
- [ ] B) `True False` then `KeyError 'open_questions'`
- [ ] C) `False False` then `KeyError 'open_questions'`
- [ ] D) `True False` and nothing else

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** `test_cases` is present but **empty** (fine). `open_questions` is **missing** (a broken reply), so indexing it raises a KeyError.
- **Why others are wrong:**
  - A) The key is absent.
  - C) An empty list equals `[]`.
  - D) The `try` block raises the error, and the `except` prints it.
</details>

---

### 48. A validator runs the course schema against this reply. Which list of problems does it report?
```python
reply = {
  "story_id": "US-205", "status": "done",
  "test_cases": [
    {"id": "TC-1", "title": "t", "ac_ids": ["AC1"], "type": "boundary", "steps": ["s"], "expected_result": "x"},
    {"id": "TC-205-02", "title": "t", "ac_ids": ["AC1"], "type": "boundary", "steps": ["s"]}
  ],
  "open_questions": []
}
# schema: status enum ["ok","needs_clarification"]; id pattern ^TC-[0-9]{3}-[0-9]{2}$;
# each test case requires id, title, ac_ids, type, steps, expected_result
```
- [ ] A) Only `status`
- [ ] B) `status`, `test_cases/0/id`, and `test_cases/1` missing `expected_result`
- [ ] C) `test_cases/1/id` and `status`
- [ ] D) No errors

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The validator reports: `'done' is not one of ['ok', 'needs_clarification']`, `'TC-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'`, and `test_cases/1: 'expected_result' is a required property`. The missing field is the problem people miss most often.
- **Why others are wrong:**
  - A) Two problems are missed.
  - C) "TC-205-02" is valid. The bad ID is at index 0.
  - D) Three rules are broken.
</details>

---

## Part 4: Fill-in-the-Blank

### 49. The JSON Schema keyword `_____` lists the fields that must be present, and the keyword `_____` gives the rules for every item in a list.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `required`; `items`

**Explanation:** Read a schema by following its nesting: the reply object first, then each test case inside `items`.
</details>

---

### 50. Writing the contract before building the parts that produce and check the data is called `_____`-first, and the contract is treated as the `_____` of truth when files disagree.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** contract; source

**Explanation:** Contract-first design keeps the instructions, examples, schema and checker in step.
</details>
