# Weekly Knowledge Check: [Week8-GenAI-AI-Augmented-QE] — Tuesday: Prompt Engineering for QE

**Covers:** Prompt engineering principles · Specificity and context · Format locking · Few-shot prompting · Common prompt failure modes · AI-assisted test design · AI-assisted coding and debugging
**Questions:** 50 · **Formats:** Multiple Choice, True/False, Code Prediction, Fill-in-the-Blank

> **Running requirement used in several questions (AC1):** *SAVE10 gives 10% off orders of $50.00 or more. Orders under $50.00 are unchanged. Unknown coupon codes raise a ValueError.*

---

## Part 1: Multiple Choice

### 1. Why is the prompt described as "the only steering wheel" for an AI assistant?
- [ ] A) Because the AI can browse your project files on its own
- [ ] B) Because the model predicts likely text from what is in its context window and cannot see your requirements unless they are in the prompt
- [ ] C) Because prompts are compiled into the model's weights
- [ ] D) Because temperature cannot be changed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Whatever is missing from the prompt becomes invented content. The prompt is the only thing shaping the answer.
- **Why others are wrong:**
  - A) A chat assistant only sees what you give it.
  - C) Prompts never change the model's weights. They only affect the current conversation.
  - D) Temperature is a separate setting and has nothing to do with this idea.
</details>

---

### 2. Which list names the five parts of a good prompt?
- [ ] A) Role, task, context, constraints, output format
- [ ] B) Greeting, task, examples, temperature, signature
- [ ] C) Title, summary, code, tests, deadline
- [ ] D) System, user, assistant, tool, memory

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** Role, task, context, constraints and output format. Of these, context usually helps most.
- **Why others are wrong:**
  - B) Greetings and signatures add nothing, and temperature is a model setting, not part of the prompt text.
  - C) These look like ticket fields, not prompt parts.
  - D) These are chat message roles, not the parts of one prompt.
</details>

---

### 3. When refining a prompt for coupon tests, which single change usually improves the answer most?
- [ ] A) Asking the AI to "be careful"
- [ ] B) Adding the actual AC1 text as context
- [ ] C) Making the prompt twice as long
- [ ] D) Raising the temperature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Without the requirement, the model guesses rules from generic coupon features. With AC1, it works from *our* rule.
- **Why others are wrong:**
  - A) A vague instruction is not checkable and does not supply the missing facts.
  - C) Length is not specificity.
  - D) Higher temperature adds randomness, not accuracy.
</details>

---

### 4. What is the difference between a system message and a user message?
- [ ] A) System messages are written by the AI; user messages by the tester
- [ ] B) A system message holds standing instructions for the whole conversation; a user message holds a particular request
- [ ] C) There is no difference; they are merged
- [ ] D) System messages are only used for images

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The tool or a developer writes the system message, and it applies throughout. The user writes each user message.
- **Why others are wrong:**
  - A) The AI writes *assistant* messages.
  - C) They have different roles and authority.
  - D) System messages apply to any conversation, not just images.
</details>

---

### 5. Why should you change only one thing at a time when improving a prompt?
- [ ] A) Models reject prompts with many changes
- [ ] B) So you know which change caused the improvement or the problem, as when debugging a test
- [ ] C) It uses fewer tokens
- [ ] D) It resets the context window

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is the prompt-refinement loop: write, run, check, change one thing, run again.
- **Why others are wrong:**
  - A) Models accept any prompt. The issue is your ability to learn from the result.
  - C) Token savings are not the reason.
  - D) Editing a prompt does not reset the context window.
</details>

---

### 6. Why does a vague prompt tend to produce a generic answer?
- [ ] A) The model refuses vague prompts
- [ ] B) The model fills each gap with the most likely content, which is the common textbook answer
- [ ] C) Vague prompts use a smaller model
- [ ] D) The model looks up a FAQ

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "Vague in, generic out." Every gap becomes the most likely continuation, and that is where invented rules come from.
- **Why others are wrong:**
  - A) Models answer vague prompts. They just answer them generically.
  - C) The prompt does not change which model is used.
  - D) There is no FAQ lookup in next-token prediction.
</details>

---

### 7. A tester retyped user story US-205 from memory instead of pasting it. What went wrong?
- [ ] A) Nothing; the meaning was preserved
- [ ] B) Details were lost: "$50.00" became "50", the exact error message became "an error", and AC4 disappeared
- [ ] C) The AI refused to read retyped text
- [ ] D) It used more tokens

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The AI can only review what it is given. Paste the real requirement, not a summary.
- **Why others are wrong:**
  - A) Exact values and a whole criterion were lost.
  - C) Models read any text you give them.
  - D) Token count was not the problem.
</details>

---

### 8. What two jobs do delimiters such as `###` or `"""` do in a prompt?
- [ ] A) They lower the cost and speed up the reply
- [ ] B) They separate instructions from pasted data, and make it less likely that text inside the data is treated as an instruction
- [ ] C) They encrypt the data and hide secrets
- [ ] D) They force the reply into JSON

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Delimiters fence off each pasted item. They also help a little against prompt injection.
- **Why others are wrong:**
  - A) Delimiters add a few tokens. They do not reduce cost.
  - C) They do not encrypt anything. Secrets must be replaced with placeholders.
  - D) Format locking is a separate instruction.
</details>

---

### 9. Your log contains a real API key. What should you paste into the prompt?
- [ ] A) The whole log as is, since the AI will not store it
- [ ] B) Nothing from the log
- [ ] C) The same log line with the key replaced by a placeholder such as `<API_KEY>`
- [ ] D) The key in base64 so it is unreadable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** A placeholder keeps the shape of the evidence while removing the secret.
- **Why others are wrong:**
  - A) Never paste secrets or real personal data.
  - B) Dropping the log loses the evidence the AI needs.
  - D) Base64 is an encoding, not encryption. Anyone can decode it.
</details>

---

### 10. Why ask the AI to raise questions or write NOT SPECIFIED instead of guessing?
- [ ] A) It makes the answer shorter
- [ ] B) It turns hidden guesses into visible questions you can take to the business analyst, which reduces hallucinations
- [ ] C) It guarantees the answer is correct
- [ ] D) It lowers the temperature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This "way out" replaces invented requirements with labelled assumptions or questions.
- **Why others are wrong:**
  - A) The answer may get longer, and length is not the goal.
  - C) Nothing guarantees correctness. You still review the answer.
  - D) It is an instruction in the prompt, not a model setting.
</details>

---

### 11. Why does `json.loads(reply)` fail on a reply such as *"Sure! ```json [...] ``` Hope this helps!"*?
- [ ] A) JSON cannot contain numbers
- [ ] B) The reply is not pure JSON: it has chatty text and Markdown fences around the list
- [ ] C) `json.loads` only reads files
- [ ] D) The list has too many items

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Chatty wrappers and fences are common kinds of format drift. Forbid text before or after the JSON, and parse defensively.
- **Why others are wrong:**
  - A) JSON supports numbers.
  - C) `json.loads` reads a string. `json.load` reads a file.
  - D) The number of items does not affect parsing.
</details>

---

### 12. All format checks pass, but one `expected_total` is wrong. Why did the checks miss it?
- [ ] A) The JSON was invalid
- [ ] B) Format checks only test shape (type, count, keys); values need a separate meaning check against the rule
- [ ] C) Python rounds numbers incorrectly
- [ ] D) The re-ask was skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A reply can have perfect structure and a wrong value. Recalculate expected totals from AC1.
- **Why others are wrong:**
  - A) The JSON parsed, so it was valid.
  - C) The problem is the AI's arithmetic, not Python's.
  - D) A re-ask is for format errors, and none were detected.
</details>

---

### 13. When the format breaks, how many times should you re-ask the model with the exact error?
- [ ] A) Until it works, however many tries that takes
- [ ] B) Once; if that fails, a person should look at the reply
- [ ] C) Never; always fix it by hand
- [ ] D) Three times with increasing temperature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Once

**Explanation:** One re-ask usually fixes it. Repeating the request wastes time and can hide a deeper problem.
- **Why others are wrong:**
  - A) Endless retries hide real problems.
  - C) One re-ask is cheap and often enough.
  - D) Higher temperature makes the format *less* reliable.
</details>

---

### 14. What is the difference between zero-shot, one-shot and few-shot prompting?
- [ ] A) The number of times the prompt is run
- [ ] B) The number of worked examples in the prompt: none, one, or a few (usually 2–5)
- [ ] C) The number of models used
- [ ] D) The temperature setting

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A "shot" is one worked example: an input with its exact output.
- **Why others are wrong:**
  - A) Running the prompt several times is a consistency check, not shots.
  - C) All three use one model.
  - D) Temperature is unrelated to shots.
</details>

---

### 15. A few-shot prompt's examples are labelled High, High, High, Low. Which two biases might affect a new answer?
- [ ] A) Automation bias and confirmation bias
- [ ] B) Majority-label bias (towards High) and recency bias (towards Low)
- [ ] C) Overfitting and underfitting
- [ ] D) Selection bias and survivor bias

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The model leans towards the most common label and towards the last one. Balance the labels and mix the order.
- **Why others are wrong:**
  - A) Those biases affect people reviewing output, not the model's choice between example labels.
  - C) Those are training problems, and no training happens here.
  - D) Those are statistics terms that do not describe this effect.
</details>

---

### 16. When is few-shot prompting **not** enough?
- [ ] A) When the output format is hard to describe
- [ ] B) When the model lacks the facts, such as your requirements
- [ ] C) When you need a fixed set of labels
- [ ] D) When the style matters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Examples teach a pattern, not the rules. For missing facts, add context, not more examples.
- **Why others are wrong:**
  - A), C), D) Format, labels and style are exactly where few-shot works best.
</details>

---

### 17. Why do LLMs make arithmetic mistakes, and what is the fix?
- [ ] A) Their calculators are outdated; use a newer model
- [ ] B) They predict digits as text rather than calculating; check every expected value against the rule, by hand or in code
- [ ] C) They round to whole numbers; ask for decimals
- [ ] D) The temperature is too low; raise it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Let code catch the easy failures: counts, formats, maths and missing functions.
- **Why others are wrong:**
  - A) LLMs have no built-in calculator.
  - C) Asking for decimals does not make the arithmetic reliable.
  - D) More randomness does not fix maths.
</details>

---

### 18. Why might an instruction placed in the middle of a long prompt be ignored?
- [ ] A) Models skip every second paragraph
- [ ] B) Models use information at the start and end of long inputs best ("lost in the middle"); put key rules near the end
- [ ] C) The middle of a prompt is not sent
- [ ] D) Instructions must be in capital letters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "Lost in the middle" is a known effect. Place key rules last.
- **Why others are wrong:**
  - A) There is no such skipping rule.
  - C) The whole prompt is sent.
  - D) Placement matters more than capital letters.
</details>

---

### 19. `failure_checks.py` reports mismatches as "need a human decision" rather than "are wrong". Why?
- [ ] A) To be polite
- [ ] B) A mismatch only shows the AI and the code disagree; either could be wrong, and only the requirement decides
- [ ] C) Because the script cannot compare numbers
- [ ] D) Because the AI is always right

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The requirement is the oracle. Against the buggy `>` code, the AI's $50.00 → $45.00 value was actually the correct one.
- **Why others are wrong:**
  - A) Politeness is not the reason. The wording reflects what a mismatch actually proves.
  - C) The script did compare the numbers. That is how it found the mismatch.
  - D) The AI is often wrong, and sometimes the code is.
</details>

---

### 20. Which four ingredients make a technique-driven test design prompt?
- [ ] A) Name the technique, give the rule exactly, give the precision, ask for working first and gaps last
- [ ] B) Role, temperature, max tokens, top-p
- [ ] C) Paste the code, the logs, the screenshots and the diff
- [ ] D) Ask for 100 tests, in Gherkin, with emojis, sorted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** For example: "Apply BVA to '$50.00 or more', money in cents (2 dp); show working; list what is not covered."
- **Why others are wrong:**
  - B) These are model settings.
  - C) That is debugging context, not test design.
  - D) Quantity and style are not technique.
</details>

---

### 21. Why should you work out the boundaries yourself **before** reading the AI's test design answer?
- [ ] A) To save tokens
- [ ] B) To have an independent view to compare against; reading the AI first makes you more likely to accept it (automation bias)
- [ ] C) Because the AI cannot do BVA
- [ ] D) It is a company rule with no reason

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** In the worked example, the AI stepped in whole dollars and missed 49.99 and 50.01.
- **Why others are wrong:**
  - A) Your own working costs no tokens either way. Saving tokens is not the reason.
  - C) The AI can apply BVA, but it can get the precision wrong.
  - D) The rule exists to counter automation bias.
</details>

---

### 22. An AI's "not covered" list includes "lowercase save10". What should you do?
- [ ] A) Add a test that lowercase works
- [ ] B) Add a test that lowercase fails
- [ ] C) Treat it as a question and ask the business analyst
- [ ] D) Ignore the list entirely

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** It is not in the story. Let the requirement decide scope, and ask instead of assuming.
- **Why others are wrong:**
  - A), B) Either test would invent a requirement.
  - D) The list is useful for finding questions to ask.
</details>

---

### 23. Fix A changes the code; Fix B changes the test. Both make the test pass. The requirement says "$50.00 or more ships free". Which is correct?
- [ ] A) Fix B, because changing tests is safer
- [ ] B) Fix A, because it makes the code match the requirement; Fix B makes the test match the buggy code
- [ ] C) Both, since the build is green
- [ ] D) Neither; delete the test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Fix A

**Explanation:** This is the weakened-test trap. A green build after changing the test is only correct if the requirement says the test was wrong.
- **Why others are wrong:**
  - A) Changing the test here would let the bug ship.
  - C) A green build is not proof of correctness.
  - D) Deleting a test is another way of weakening it.
</details>

---

### 24. Why do AI assistants sometimes suggest changing the test instead of the code?
- [ ] A) They prefer editing short files
- [ ] B) Without the requirement, they only see a disagreement, and making the test agree with the code is a likely continuation
- [ ] C) Tests are easier to compile
- [ ] D) They are trained to never edit source code

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Include the requirement in debugging prompts so the AI can judge which side is wrong.
- **Why others are wrong:**
  - A) File length is not the reason.
  - C) Python tests are not compiled.
  - D) No such training rule exists. AI assistants edit source code all the time.
</details>

---

### 25. An AI refactor of `cart.py` passed all five reviewed tests, yet it made coupon codes case-insensitive. Why did the tests not catch it?
- [ ] A) pytest ignores string case
- [ ] B) None of the tests tried a lowercase code; tests only protect the behaviour they check
- [ ] C) Refactors cannot change behaviour
- [ ] D) The tests were skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** "Refactor" does not guarantee "same behaviour". Read the diff and pin important behaviour with characterization tests.
- **Why others are wrong:**
  - A) pytest compares strings exactly.
  - C) This refactor did change behaviour.
  - D) The tests ran and passed.
</details>

---

### 26. What does `DID NOT RAISE ValueError` mean in a pytest failure?
- [ ] A) Python could not import ValueError
- [ ] B) The test expected the code inside `pytest.raises(ValueError)` to raise that error, but it finished without raising it
- [ ] C) The code raised a different error
- [ ] D) The test file has a syntax error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is the message `pytest.raises` gives when no exception occurred.
- **Why others are wrong:**
  - A) ValueError is built in.
  - C) A different error would appear as that error's traceback.
  - D) A syntax error would stop collection with a different message.
</details>

---

### 27. Which set lists the six parts of a good debugging prompt?
- [ ] A) Code under test, failing test, full error output, expected vs actual, what you tried, what you want back
- [ ] B) Role, task, context, constraints, format, examples
- [ ] C) Screenshot, log level, browser, OS, priority, owner
- [ ] D) Title, steps, severity, label, sprint, assignee

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** Add the requirement as well, so the AI can tell whether the code or the test is wrong.
- **Why others are wrong:**
  - B) These are the general prompt parts, not the debugging-specific ones.
  - C), D) These are bug-tracker fields.
</details>

---

## Part 2: True / False

### 28. True or False: A longer prompt is always more specific.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Specificity comes from exact scope, criteria, limits, format and real context. A short prompt that pastes the AC can be far more specific than a long, general one.
</details>

---

### 29. True or False: In-context learning from few-shot examples permanently retrains the model.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It lasts only for that conversation, while the examples are in the context window.
</details>

---

### 30. True or False: If three runs of the same prompt agree on a value, the value is proven correct.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Agreement only shows the prompt is stable. All three runs could share the same mistake, so the value still needs checking against the requirement.
</details>

---

### 31. True or False: In a few-shot prompt, a wrong label in one example can become a wrong pattern in the replies.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The examples are the specification, and the model copies their mistakes too. Check the examples and the replies with the same rule.
</details>

---

### 32. True or False: Good constraints should be checkable, and should say what to do rather than only what not to do.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** "Return exactly 6 rows" can be checked. "Don't be vague" cannot.
</details>

---

### 33. True or False: Because of sampling, one good run of a fixed prompt may be luck, so you should re-run it several times and check each run.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Several runs, each checked, show whether the fix is reliable. Treat this the way you treat a flaky test.
</details>

---

### 34. True or False: Equivalence Partitioning tests the edges of each partition, and Boundary Value Analysis picks one value per partition.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is the other way round. EP picks one value per partition, and BVA tests at and just around each partition's edges.
</details>

---

### 35. True or False: In a decision table, the outcome for an invalid code combined with a low subtotal (rule R4) should be confirmed with the business analyst if the story does not say which message wins.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Any expected outcome for that combination is an interpretation. AI often misses unstated combinations.
</details>

---

### 36. True or False: A good way to check that a fixed test can still fail is to temporarily reintroduce the bug and confirm the test goes red.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is called re-breaking. Change `>=` back to `>`, run the test, see it fail, then restore the fix.
</details>

---

### 37. True or False: Each extra few-shot example is a cost paid on every request.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The examples are sent with every call. Three examples of about 80 tokens in total, across 1,000 bugs, add about 80,000 tokens.
</details>

---

### 38. True or False: Outdated knowledge is a prompt failure mode caused by the model's training cut-off.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Answers may be based on old library versions or practices. Check them against current official docs.
</details>

---

## Part 3: Code Prediction

### 39. What does this print?
```python
import json
reply = 'Sure! Here are the cases:\n```json\n[{"id": 1, "expected_total": 45.0}]\n```\nHope this helps!'
try:
    json.loads(reply)
except json.JSONDecodeError as e:
    print(type(e).__name__)
```
- [ ] A) `[{'id': 1, 'expected_total': 45.0}]`
- [ ] B) `JSONDecodeError`
- [ ] C) `KeyError`
- [ ] D) Nothing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `JSONDecodeError`

**Explanation:** The text begins with "Sure!", which is not valid JSON.
- **Why others are wrong:**
  - A) Parsing fails before any data is returned.
  - C) No dictionary key is accessed.
  - D) The `except` block prints the error name.
</details>

---

### 40. Continuing with the same `reply`, what does this print?
```python
t = reply[reply.find("["):reply.rfind("]") + 1]
print(json.loads(t))
```
- [ ] A) `[{'id': 1, 'expected_total': 45.0}]`
- [ ] B) `JSONDecodeError`
- [ ] C) `[]`
- [ ] D) `'[{"id": 1, "expected_total": 45.0}]'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A)

**Explanation:** The slice keeps everything from the first `[` to the last `]`, cutting away the chat and the fences. This is defensive parsing. It can fail if a `[` appears before the list.
- **Why others are wrong:**
  - B) The extracted text is valid JSON.
  - C) The list has one item.
  - D) `json.loads` returns Python data, not a string.
</details>

---

### 41. What does this print?
```python
required = {"id", "input", "expected_total"}
got = {"id", "expected_total", "notes"}
print(required - got, got - required)
```
- [ ] A) `{'notes'} {'input'}`
- [ ] B) `{'input'} {'notes'}`
- [ ] C) `set() set()`
- [ ] D) `{'id'} {'expected_total'}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `{'input'} {'notes'}`

**Explanation:** `required - got` gives the missing keys. `got - required` gives the unexpected keys. Both are useful shape checks.
- **Why others are wrong:**
  - A) The order of the sets is swapped.
  - C) The sets are not equal.
  - D) "id" and "expected_total" are in both sets.
</details>

---

### 42. A model returned the total in quotes. What does this print?
```python
case = {"expected_total": "45.00"}
print(isinstance(case["expected_total"], (int, float)), case["expected_total"] == 45.0)
```
- [ ] A) `True True`
- [ ] B) `False True`
- [ ] C) `False False`
- [ ] D) `True False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `False False`

**Explanation:** `"45.00"` is a string, so the type check fails and the comparison with a number fails. State the type in the prompt and check it in code.
- **Why others are wrong:**
  - A), D) A string is not an int or float.
  - B) Python does not convert a string to a number when comparing with `==`.
</details>

---

### 43. A validator checks each verdict line. Which inputs print `True`?
```python
import re
pat = re.compile(r"^Priority: (Critical|High|Medium|Low)$")
for s in ["Priority: High", "priority: High", "Priority: Urgent", "Priority: High."]:
    print(s, bool(pat.match(s)))
```
- [ ] A) All four
- [ ] B) Only `Priority: High`
- [ ] C) `Priority: High` and `Priority: High.`
- [ ] D) `Priority: High` and `priority: High`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Only `Priority: High`

**Explanation:** The pattern is case-sensitive, allows only the four listed labels, and `$` forbids trailing characters.
- **Why others are wrong:**
  - A) Three of the lines break the format.
  - C) The trailing "." fails `$`.
  - D) Lowercase "priority" does not match.
</details>

---

### 44. Using the correct AC1 rule, what does this print?
```python
def ac(total):
    return round(total * 0.9, 2) if total >= 50 else total

print([ac(t) for t in (49.99, 50.00, 50.01)])
```
- [ ] A) `[49.99, 45.0, 45.01]`
- [ ] B) `[44.99, 45.0, 45.01]`
- [ ] C) `[49.99, 50.0, 45.01]`
- [ ] D) `[49.99, 45.0, 50.01]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `[49.99, 45.0, 45.01]`

**Explanation:** These are the three-value BVA cases at cent precision. 50.01 × 0.9 = 45.009, which rounds to 45.01.
- **Why others are wrong:**
  - B) 49.99 is under $50, so it is unchanged.
  - C) 50.00 qualifies under `>=`.
  - D) 50.01 qualifies too.
</details>

---

### 45. The code has the `>` bug. Which AI-suggested whole-dollar case detects it?
```python
def ac_bug(total):
    return round(total * 0.9, 2) if total > 50 else total

for t, expected in [(49.0, 49.0), (50.0, 45.0), (51.0, 45.9)]:
    print(t, ac_bug(t) == expected)
```
- [ ] A) Only 49.0 prints `False`
- [ ] B) Only 50.0 prints `False`
- [ ] C) All three print `False`
- [ ] D) None print `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Only 50.0 prints `False`

**Explanation:** 49.00 and 51.00 behave the same with `>` and `>=`. Only a value exactly on the boundary reveals the bug.
- **Why others are wrong:**
  - A) 49.0 is unchanged either way.
  - C) 49.0 and 51.0 still match.
  - D) 50.0 returns 50.0, not 45.0.
</details>

---

### 46. What does this print?
```python
tokens_per_example = 80 / 3
bugs = 1000
print(round(tokens_per_example * 3 * bugs))
```
- [ ] A) `80`
- [ ] B) `240`
- [ ] C) `80000`
- [ ] D) `240000`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `80000`

**Explanation:** Three examples total about 80 tokens per request. Sent with all 1,000 requests, that is about 80,000 tokens.
- **Why others are wrong:**
  - A) That is the cost of a single request.
  - B) That multiplies 80 by 3 again, but 80 is already the total for all three examples.
  - D) Same double count, multiplied by 1,000.
</details>

---

## Part 4: Fill-in-the-Blank

### 47. A `_____` test is a test changed so that it no longer checks what the requirement demands, for example by editing the expected value to match buggy code.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** weakened

**Explanation:** Other examples include deleting the assertion, loosening the check, skipping the test, or catching errors too broadly.
</details>

---

### 48. A `_____` test pins down what code does today, before a refactor, so behaviour changes become visible.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** characterization

**Explanation:** Combine characterization tests with reading the diff and asking the AI for a list of changes.
</details>

---

### 49. Put only reviewed values into tests, using pytest's `@pytest.mark._____` decorator to run one test per row.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** parametrize

**Explanation:** `@pytest.mark.parametrize("total, expected", [(49.99, 49.99), (50.00, 45.00), (50.01, 45.01)])` runs the test once per reviewed row.
</details>

---

### 50. A shape check tests types, counts and keys; a `_____` check tests the values against the rule.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** meaning

**Explanation:** You need both. A reply can have perfect structure and a wrong value.
</details>
