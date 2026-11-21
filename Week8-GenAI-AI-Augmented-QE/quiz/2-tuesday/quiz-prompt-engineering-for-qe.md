# Daily Knowledge Check: Week 8 Tuesday - Prompt Engineering for QE

This check covers prompt engineering principles, specificity and context, format locking, few-shot prompting, common prompt failure modes, AI-assisted test design, and AI-assisted coding and debugging. Try each question on your own first, then open the solution to check your reasoning.

---

## Part 1: Multiple Choice

### 1. What best describes **prompt engineering**?

- [ ] A) Finding magic words that always make a model give the right answer
- [ ] B) A disciplined, repeatable process of designing, testing and refining prompts so output is useful, accurate, consistent and in the required form
- [ ] C) Retraining a model's weights on your team's data
- [ ] D) Writing the longest possible prompt

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A disciplined, repeatable process of designing, testing and refining prompts so output is useful, accurate, consistent and in the required form

**Explanation:** The lesson stresses that "engineering" is deliberate: decide acceptance criteria, write the prompt, run it, compare, change one thing, repeat.
- **Why others are wrong:**
  - A) The lesson explicitly says it is not about finding magic words.
  - C) Retraining weights is fine-tuning, not prompting.
  - D) More text is not automatically better; irrelevant text can hurt.

</details>

### 2. Which list contains the seven building blocks of a prompt?

- [ ] A) Role, task, context, input data, constraints, output format, examples
- [ ] B) Model, temperature, top-p, max tokens, seed, stop, stream
- [ ] C) Given, When, Then, And, But, Scenario, Feature
- [ ] D) Draft, run, evaluate, refine, commit, push, merge

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Role, task, context, input data, constraints, output format, examples

**Explanation:** These blocks can be used as a checklist, much like checking a bug report for steps, expected and actual results.
- **Why others are wrong:**
  - B) These are generation/API settings, not prompt building blocks.
  - C) These are Gherkin keywords.
  - D) The first four are the refinement loop; the rest are Git actions.

</details>

### 3. Which building block does the lesson say beginners most often forget?

- [ ] A) Role
- [ ] B) Task
- [ ] C) Context
- [ ] D) Output format

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Context

**Explanation:** Context is the facts the model cannot know on its own: business rules, tech stack, purpose of the work, who will read it.
- **Why others are wrong:**
  - A) A role is helpful but the lesson does not single it out as most forgotten.
  - B) The task is described as the single most important block, and people usually include one.
  - D) Format matters greatly in automation but is not the one named as most forgotten.

</details>

### 4. What belongs in a **system** message rather than a **user** message?

- [ ] A) The specific stack trace for this turn
- [ ] B) Standing instructions for the whole conversation, such as persona, house rules and "do not invent rules"
- [ ] C) The model's previous reply
- [ ] D) A one-off question about today's failing build

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Standing instructions for the whole conversation, such as persona, house rules and "do not invent rules"

**Explanation:** The system message sets the frame; the user message carries the specific job and its input data.
- **Why others are wrong:**
  - A) and D) Turn-specific material goes in the user message.
  - C) Previous model replies are **assistant** messages.

</details>

### 5. Why do chat APIs receive previous **assistant** messages with each request?

- [ ] A) To train the model on its own replies
- [ ] B) Because the model is stateless between calls; resending the history is how conversations keep "memory"
- [ ] C) To reduce token costs
- [ ] D) Because the system message would otherwise be ignored

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because the model is stateless between calls; resending the history is how conversations keep "memory"

**Explanation:** Between API calls the model remembers nothing. The application sends the whole message history every time, and that history counts against the context window.
- **Why others are wrong:**
  - A) No weights change during a request.
  - C) Resending history *increases* tokens.
  - D) The system message is not dependent on assistant messages.

</details>

### 6. Which rewrite of "Don't make things up" follows the "say what to do" principle best?

- [ ] A) "Never, ever make anything up."
- [ ] B) "Use only the rules listed in `<context>`. If a rule needed for a test is missing, write `QUESTION:` followed by what you need to know."
- [ ] C) "Be accurate."
- [ ] D) "Avoid hallucinations at all costs."

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "Use only the rules listed in `<context>`. If a rule needed for a test is missing, write `QUESTION:` followed by what you need to know."

**Explanation:** Positive, specific instructions are followed more reliably, and this one gives the model a legitimate way out instead of pushing it to guess.
- **Why others are wrong:**
  - A) and D) Still negative-only and give no alternative.
  - C) Too vague to act on.

</details>

### 7. When is asking the model to "list the boundaries first, then the tests" most useful?

- [ ] A) For simple formatting or lookup tasks
- [ ] B) For multi-step reasoning tasks such as analysis, calculations, debugging and design
- [ ] C) Never; it always wastes tokens
- [ ] D) Only when temperature is above 1

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) For multi-step reasoning tasks such as analysis, calculations, debugging and design

**Explanation:** Because the model writes left to right, the plan it writes first becomes context for the final answer, and it gives you something to review.
- **Why others are wrong:**
  - A) For simple tasks it only adds length and cost.
  - C) The lesson recommends it selectively, not never.
  - D) It has nothing to do with temperature.

</details>

### 8. Which dimension of specificity does the lesson call "the most overlooked, and the most powerful for QE"?

- [ ] A) Tone
- [ ] B) Length
- [ ] C) Done-criteria
- [ ] D) Task verb

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Done-criteria

**Explanation:** A done-criterion (e.g. "every equivalence class has at least one test; 49.99, 50.00 and 50.01 are all covered") gives the model a target and gives you a review checklist.
- **Why others are wrong:**
  - A) Tone matters more for bug reports and summaries.
  - B) Length limits help focus but are not singled out this way.
  - D) The verb is important but not described as the most overlooked.

</details>

### 9. In the five-iteration "vague to specific" worked example, which single change produced the **largest** improvement?

- [ ] A) Adding the output table format
- [ ] B) Adding the requirement (context)
- [ ] C) Naming the audience
- [ ] D) Asking for assumptions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Adding the requirement (context)

**Explanation:** Iteration 2 replaced invented behaviour (like "expired coupons") with tests for the real feature. Without the test basis, no wording produces the right tests.
- **Why others are wrong:**
  - A), C), D) All helped, but in later, smaller steps.

</details>

### 10. What did the *Lost in the Middle* research find?

- [ ] A) Models ignore the first sentence of every prompt
- [ ] B) Models tended to use relevant information best near the beginning or end of a long input and worse when it was buried in the middle
- [ ] C) Longer prompts are always more accurate
- [ ] D) Models cannot read XML tags

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Models tended to use relevant information best near the beginning or end of a long input and worse when it was buried in the middle

**Explanation:** Practical advice: put long reference material first and instructions at the end (or state key instructions at the start and repeat them at the end). Do not bury a critical rule mid-paste.
- **Why others are wrong:**
  - A) The beginning was one of the well-used positions.
  - C) The study points the other way: position and noise matter.
  - D) Nothing in the research is about XML tags.

</details>

### 11. Which is the best rule of thumb for how much context to include?

- [ ] A) Paste the entire repository to be safe
- [ ] B) Give the model everything it needs to do the task, and nothing it needs to ignore
- [ ] C) Never include code
- [ ] D) Include only the task verb

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Give the model everything it needs to do the task, and nothing it needs to ignore

**Explanation:** Aim for high signal and low noise. Test each block: "if I removed this, would the answer get worse?"
- **Why others are wrong:**
  - A) Irrelevant context dilutes attention, wastes the window and costs money.
  - C) Existing code and conventions are one of the six context types.
  - D) That would be context-poor and generic.

</details>

### 12. Why does the `PromptSpec` dataclass use `field(default_factory=dict)` instead of `= {}`?

- [ ] A) Because `{}` is not valid Python
- [ ] B) Dataclasses forbid shared mutable defaults; `default_factory` creates a fresh dict for each object
- [ ] C) To make the class faster
- [ ] D) Because dictionaries cannot be fields

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Dataclasses forbid shared mutable defaults; `default_factory` creates a fresh dict for each object

**Explanation:** Without it, two `PromptSpec` objects could accidentally share the same context dictionary.
- **Why others are wrong:**
  - A) `{}` is valid Python; it is just not allowed as a dataclass default.
  - C) Speed is not the reason.
  - D) Dict fields are fine when created with a factory.

</details>

### 13. What are the two halves of **format locking**?

- [ ] A) Encrypting and decrypting the output
- [ ] B) Requesting the format in the prompt, and enforcing it in code after the response arrives
- [ ] C) Writing JSON and writing CSV
- [ ] D) Lowering temperature and raising top-p

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Requesting the format in the prompt, and enforcing it in code after the response arrives

**Explanation:** Requesting makes the right structure *likely*; enforcing catches the cases where it still slips. Treat model output as untrusted input.
- **Why others are wrong:**
  - A) Encryption is unrelated.
  - C) These are formats, not the two halves.
  - D) Temperature is one technique, not a "half".

</details>

### 14. Which family of format drift is described as **more dangerous**, and why?

- [ ] A) Syntax drift, because `json.loads` fails loudly
- [ ] B) Structure drift (missing, renamed or extra keys; wrong types; out-of-range values), because it parses successfully and can silently produce wrong tests
- [ ] C) Code fences, because they cannot be removed
- [ ] D) Neither; all drift is equally harmless

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Structure drift (missing, renamed or extra keys; wrong types; out-of-range values), because it parses successfully and can silently produce wrong tests

**Explanation:** Syntax drift is noisy, so you notice it. Structure drift passes the parser and fails later, or not at all.
- **Why others are wrong:**
  - A) Loud failures are the *less* dangerous family.
  - C) Fences are easy to strip defensively.
  - D) Drift can break pipelines or corrupt results.

</details>

### 15. What does a provider's **JSON mode** guarantee compared with **structured outputs**?

- [ ] A) JSON mode guarantees correct content; structured outputs guarantee speed
- [ ] B) JSON mode guarantees syntactically valid JSON; structured outputs also guarantee the response matches a supplied schema; neither guarantees correct content
- [ ] C) Both guarantee the expected values are right
- [ ] D) JSON mode is the newer, stronger feature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) JSON mode guarantees syntactically valid JSON; structured outputs also guarantee the response matches a supplied schema; neither guarantees correct content

**Explanation:** A perfectly structured test case can still have the wrong expected value. You still parse defensively and review content.
- **Why others are wrong:**
  - A) Neither guarantees correct content.
  - C) Shape is not correctness.
  - D) The lesson notes structured outputs are described as the evolution of JSON mode.

</details>

### 16. A defensive parser should do which of the following?

- [ ] A) Silently replace single quotes with double quotes to "repair" the JSON
- [ ] B) Strip code fences and surrounding chatter, then fail clearly on real syntax errors
- [ ] C) Retry forever until the JSON parses
- [ ] D) Accept any response without checking keys

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Strip code fences and surrounding chatter, then fail clearly on real syntax errors

**Explanation:** "Tolerate wrapping; reject broken content." Fences and chatter are harmless wrapping around valid content.
- **Why others are wrong:**
  - A) Replacing quotes can corrupt values like `"Customer's cart"` and hides that the model ignored instructions.
  - C) The lesson recommends re-asking once, then failing loudly.
  - D) Parsing is not enough; you must also check structure.

</details>

### 17. Why does the "re-ask with the error" pattern stop after **one** retry?

- [ ] A) Because APIs only allow two calls
- [ ] B) To avoid wasting tokens, avoid infinite loops and make persistent failures visible for a person to investigate
- [ ] C) Because the second answer is always correct
- [ ] D) Because the first error message is lost after one retry

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) To avoid wasting tokens, avoid infinite loops and make persistent failures visible for a person to investigate

**Explanation:** "Retry once, then fail loudly." Fuller retry strategies are a Week 9 topic.
- **Why others are wrong:**
  - A) There is no such API limit.
  - C) The second answer can fail too, which is why the error surfaces.
  - D) The error is included in the correction message deliberately.

</details>

### 18. Why is JSON usually preferred over CSV when the output feeds Python code?

- [ ] A) CSV cannot be read by Python
- [ ] B) JSON carries types and supports nesting; CSV values are all text, need manual conversion and break on unquoted commas
- [ ] C) JSON is shorter than CSV
- [ ] D) CSV is not supported by spreadsheets

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) JSON carries types and supports nesting; CSV values are all text, need manual conversion and break on unquoted commas

**Explanation:** In the CSV example, `row["expected"]` was still the string `"45.00"` and needed explicit conversion.
- **Why others are wrong:**
  - A) Python's `csv` module reads CSV well.
  - C) JSON is often longer.
  - D) CSV opens directly in spreadsheets; that is one of its strengths.

</details>

### 19. What does "shot" mean in zero-shot, one-shot and few-shot prompting?

- [ ] A) An API call
- [ ] B) A worked example (input plus desired output) included in the prompt
- [ ] C) A retry attempt
- [ ] D) A temperature setting

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A worked example (input plus desired output) included in the prompt

**Explanation:** Zero-shot has no examples, one-shot has one, few-shot usually 2 to 5. Anthropic also calls it "multishot" prompting.
- **Why others are wrong:**
  - A), C), D) None of these is what "shot" refers to.

</details>

### 20. When a model follows the examples in a few-shot prompt, what has happened to its weights?

- [ ] A) They were updated by gradient descent
- [ ] B) Nothing; this is in-context learning and the examples exist only in the context window for that request
- [ ] C) They are saved for the next request
- [ ] D) They are reset to random values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Nothing; this is in-context learning and the examples exist only in the context window for that request

**Explanation:** The next request starts fresh; without the examples, the model does not remember them. Supervised training (Monday) is what changes weights.
- **Why others are wrong:**
  - A) That describes training, not prompting.
  - C) Models are stateless between requests.
  - D) Nothing is reset or changed.

</details>

### 21. If a few-shot prompt's instruction says "answer in one word" but an example answers with a full sentence, what often happens?

- [ ] A) The model always follows the instruction
- [ ] B) The model often follows the examples, so instructions and examples must be kept consistent
- [ ] C) The model refuses to answer
- [ ] D) The model averages the two styles

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The model often follows the examples, so instructions and examples must be kept consistent

**Explanation:** Examples are powerful "show, don't tell" signals and can override written rules when they disagree.
- **Why others are wrong:**
  - A) Not guaranteed; the lesson warns about this conflict.
  - C) There is no reason to refuse.
  - D) There is no such averaging behaviour described.

</details>

### 22. How many examples does Anthropic's prompting guide suggest for best few-shot results?

- [ ] A) 1
- [ ] B) 3 to 5
- [ ] C) 20 to 30
- [ ] D) As many as fit in the context window

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 3 to 5

**Explanation:** More examples bring diminishing returns and cost tokens on every request. Start with two or three and add one only to fix a specific observed mistake.
- **Why others are wrong:**
  - A) One mainly shows a format.
  - C) and D) Expensive and rarely helpful beyond a point.

</details>

### 23. Your five examples are labelled Major, Major, Major, Major, Critical. Which two biases could this introduce?

- [ ] A) Sycophancy and hallucination
- [ ] B) Majority-label bias and recency bias
- [ ] C) Overfitting and underfitting
- [ ] D) Truncation and format drift

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Majority-label bias and recency bias

**Explanation:** Most examples share "Major", pulling answers that way; the last example ("Critical") sits closest to the new input and may have extra influence. Balance labels and vary positions.
- **Why others are wrong:**
  - A) These are different failure modes.
  - C) These are training concepts from Monday.
  - D) These are output-format problems.

</details>

### 24. Every example test case uses SAVE10 and an $80 order. You ask for gift-card tests and the output mentions SAVE10. What is this risk called?

- [ ] A) Example leakage
- [ ] B) Over-copying (anchoring on surface details)
- [ ] C) Lost in the middle
- [ ] D) Over-refusal

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Over-copying (anchoring on surface details)

**Explanation:** The model copies incidental features of examples. Diversity in examples is the main defence.
- **Why others are wrong:**
  - A) Leakage is returning an example's content *instead of* a new answer (e.g. the same title as Example 2).
  - C) That concerns position in long inputs.
  - D) That is declining a legitimate request.

</details>

### 25. Why does Jaccard similarity score "Cannot sign in" and "Login fails" as completely dissimilar?

- [ ] A) Because the sentences have different lengths
- [ ] B) Because Jaccard compares exact words, and the two phrases share no words
- [ ] C) Because Jaccard ignores lowercase letters
- [ ] D) Because Jaccard only works on numbers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because Jaccard compares exact words, and the two phrases share no words

**Explanation:** Production systems use embeddings (Monday) to match meaning; TF-IDF with cosine similarity is a middle ground.
- **Why others are wrong:**
  - A) Length is not what Jaccard measures.
  - C) The code lower-cases text precisely so case does not matter.
  - D) It works on sets of words.

</details>

### 26. An AI tells you to run `pytest --retry-failed 3`. Which failure mode is this?

- [ ] A) Sycophancy
- [ ] B) Hallucination (an invented CLI flag)
- [ ] C) Over-refusal
- [ ] D) Lost in the middle

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Hallucination (an invented CLI flag)

**Explanation:** It is not a built-in pytest option. Check `pytest --help` or the docs, or simply run it and see the unrecognised-argument error.
- **Why others are wrong:**
  - A) Sycophancy is agreeing with the user's wrong premise.
  - C) Nothing was declined.
  - D) That concerns buried instructions.

</details>

### 27. You ask "I'm pretty sure this test is correct. Can you confirm?" and the model agrees with a wrong test. What is this?

- [ ] A) Format drift
- [ ] B) Sycophancy triggered by a leading question
- [ ] C) Non-determinism
- [ ] D) Outdated knowledge

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Sycophancy triggered by a leading question

**Explanation:** Models tuned on human feedback tend to agree, and your words become context that raises the probability of agreement. Ask neutral questions and supply the rule.
- **Why others are wrong:**
  - A) The format was fine.
  - C) Variation between runs is a separate issue.
  - D) No old API was involved.

</details>

### 28. Why can "Don't use `time.sleep`" lead to code that uses `time.sleep`?

- [ ] A) Because the model cannot read the word "don't"
- [ ] B) The banned tokens become part of the context and raise their probability, and the instruction gives no alternative (the "pink elephant" effect)
- [ ] C) Because `time.sleep` is the only way to wait
- [ ] D) Because temperature is too low

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The banned tokens become part of the context and raise their probability, and the instruction gives no alternative (the "pink elephant" effect)

**Explanation:** Better: "Wait for elements using WebDriverWait with expected_conditions" (or Playwright's auto-waiting).
- **Why others are wrong:**
  - A) The model reads it; the issue is how tokens influence prediction.
  - C) Explicit waits and auto-waiting are better alternatives.
  - D) Low temperature does not cause this.

</details>

### 29. An AI suggests `driver.find_element_by_id("username")`. Which failure mode is this?

- [ ] A) Outdated knowledge
- [ ] B) Over-refusal
- [ ] C) Conflicting instructions
- [ ] D) Sycophancy

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Outdated knowledge

**Explanation:** Selenium 4 removed the `find_element_by_*` helpers from the Python bindings; use `find_element(By.ID, "username")`. Old patterns are common in training data. Fix by stating versions.
- **Why others are wrong:**
  - B), C), D) None of these describes producing a removed API.

</details>

### 30. Why is it better to ask the AI for the test **inputs** and compute expected values yourself?

- [ ] A) Because the AI cannot produce numbers
- [ ] B) Models work on tokens and make plausible arithmetic slips; your code or calculation is deterministic and trustworthy
- [ ] C) Because expected values are not needed
- [ ] D) Because computing is slower than asking

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Models work on tokens and make plausible arithmetic slips; your code or calculation is deterministic and trustworthy

**Explanation:** The lesson's example: an AI table said 75.50 × 0.9 = 67.50 when the correct value is 67.95. The AI's value is suggesting interesting inputs.
- **Why others are wrong:**
  - A) It produces numbers, just not reliably correct ones.
  - C) Expected values are the heart of a test.
  - D) Speed is not the reason.

</details>

### 31. In AI-assisted test design, who or what is the **test oracle**?

- [ ] A) The LLM, because it has read many specifications
- [ ] B) The requirement, specification, product owner or reference implementation; an LLM is not an oracle
- [ ] C) Whatever the code currently returns
- [ ] D) The test framework

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The requirement, specification, product owner or reference implementation; an LLM is not an oracle

**Explanation:** An LLM predicts plausible text; its expected results are guesses. The tester owns and verifies expected results. "Let the AI widen the funnel; you narrow it."
- **Why others are wrong:**
  - A) Reading many specs does not make its guesses verified.
  - C) Current behaviour might be buggy.
  - D) The framework runs checks; it does not define correct behaviour.

</details>

### 32. Why does "cent precision (0.01)" matter in a BVA prompt for the $50.00 threshold?

- [ ] A) It makes the prompt shorter
- [ ] B) Without it, models often pick 49, 50 and 51, which cannot detect bugs like `total > 49.5`
- [ ] C) Because pytest cannot handle whole numbers
- [ ] D) It has no effect

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Without it, models often pick 49, 50 and 51, which cannot detect bugs like `total > 49.5`

**Explanation:** All three whole-number tests pass against `> 49.5`. A test at 49.99 would catch it. The correct 3-value BVA inputs are 49.99, 50.00 and 50.01.
- **Why others are wrong:**
  - A) It adds words; length is not the point.
  - C) pytest handles any numbers.
  - D) It directly prevents the most common AI BVA mistake.

</details>

### 33. Why should you ask an AI for one row per **(state, event) pair** in state transition testing?

- [ ] A) It makes the table prettier
- [ ] B) Otherwise the model typically lists only valid transitions and forgets invalid pairs, where many real defects live
- [ ] C) Because states and events are the same thing
- [ ] D) To reduce the number of tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Otherwise the model typically lists only valid transitions and forgets invalid pairs, where many real defects live

**Explanation:** For example: does a correct password in the Locked state log the user in? With 5 states and 4 events there are 20 pairs, which you can count.
- **Why others are wrong:**
  - A) Presentation is not the reason.
  - C) States and events are distinct concepts.
  - D) It increases coverage, not reduces tests.

</details>

### 34. In the pairwise example, the AI's 9-row set had every value appearing three times. Why was it still incomplete?

- [ ] A) Pairwise testing requires 27 rows
- [ ] B) Balanced value frequency does not guarantee pair coverage; the last row repeated `Card` where `PayPal` was needed, leaving two pairs untested
- [ ] C) Safari is not supported by pairwise testing
- [ ] D) Nine rows is always too few

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Balanced value frequency does not guarantee pair coverage; the last row repeated `Card` where `PayPal` was needed, leaving two pairs untested

**Explanation:** (Safari, PayPal) and (Android, PayPal) were missing. Changing the last row to `("Safari", "Android", "PayPal")` fixes both.
- **Why others are wrong:**
  - A) 27 is all combinations; pairwise needs fewer (9 can be enough).
  - C) Any value can be used.
  - D) For three parameters with three values, 9 rows can cover all pairs.

</details>

### 35. What does the instruction "mark unspecified behaviour as **ASK PO**" prevent?

- [ ] A) The model from producing tables
- [ ] B) The model from inventing requirements; gaps become visible questions for the product owner
- [ ] C) The model from using EP
- [ ] D) The product owner from changing requirements

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The model from inventing requirements; gaps become visible questions for the product owner

**Explanation:** Whether `" SAVE10 "` should be trimmed or `save10` accepted is a business decision, not something the AI or tester invents.
- **Why others are wrong:**
  - A), C), D) The instruction does none of these.

</details>

### 36. Why does Playwright's sync vs async API matter when prompting for code?

- [ ] A) Only the async API exists in Python
- [ ] B) Without saying which, you may get `await`-heavy async code that does not fit a sync-API project
- [ ] C) The sync API cannot click buttons
- [ ] D) It only matters for Selenium

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Without saying which, you may get `await`-heavy async code that does not fit a sync-API project

**Explanation:** Always state language, framework and versions, e.g. "Python 3.12, pytest 8, Playwright for Python (sync API)".
- **Why others are wrong:**
  - A) Playwright for Python has both.
  - C) The sync API is fully capable (used in Week 4).
  - D) It is a Playwright distinction.

</details>

### 37. Why ask an AI for **ranked hypotheses with a way to confirm each** rather than "fix it"?

- [ ] A) Hypotheses are shorter
- [ ] B) "Fix it" invites any change that turns the test green, often weakening the test; hypotheses keep the focus on root cause and let evidence decide
- [ ] C) Because AIs cannot write fixes
- [ ] D) Because confirmation steps are required by pytest

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "Fix it" invites any change that turns the test green, often weakening the test; hypotheses keep the focus on root cause and let evidence decide

**Explanation:** You remain the investigator; each hypothesis comes with a cheap experiment.
- **Why others are wrong:**
  - A) Length is not the reason.
  - C) AIs can write fixes; the risk is *which* fix.
  - D) pytest has no such requirement.

</details>

### 38. A test passes alone (`pytest -k name`) but fails in the full suite. What is the most likely flaky-test category?

- [ ] A) Timing and waits
- [ ] B) Shared state or test order dependence
- [ ] C) Outdated API
- [ ] D) Format drift

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Shared state or test order dependence

**Explanation:** Check whether the test relies on data or state created or modified by another test: module-level variables, session-scoped fixtures, shared test users.
- **Why others are wrong:**
  - A) Timing issues typically show as intermittent "not found/visible", often worse on slow CI.
  - C) An outdated API fails every time.
  - D) Format drift relates to AI output, not test isolation.

</details>

---

## Part 2: True/False

### 39. True or False: A prompt that worked correctly once can be considered reliable.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** With non-zero temperature, output is sampled; a wrong answer with ~20% probability often will not appear in one run. Run important prompts several times (three to five is a reasonable start).

</details>

### 40. True or False: A role such as "You are a world-class genius" gives the model useful knowledge about your system.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Roles set vocabulary and perspective but do not supply knowledge. Keep roles relevant, e.g. "a QA engineer reviewing tests for boundary coverage".

</details>

### 41. True or False: Reusable prompts should be stored in Git with a version, purpose and acceptance criteria.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Prompts are artifacts. Version them, commit changes with meaningful messages, record the model and evidence, and review them in pull requests.

</details>

### 42. True or False: Delimiters such as `<requirement>` tags are special keywords that the model must be trained on.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Tag names are not special keywords; the model simply understands the structure. Pick clear, descriptive names and use one style consistently.

</details>

### 43. True or False: Lowering temperature for a format-locked task guarantees a valid format and correct content.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Low temperature reduces random deviations in structure, but guarantees neither validity nor correctness.

</details>

### 44. True or False: In Python, `isinstance(True, int)` returns `True`, which is why the type checker adds an explicit `bool` guard.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `bool` is a subclass of `int`. Without the guard, `"input_total": true` would pass a number check.

</details>

### 45. True or False: Prefilling the assistant's response is supported identically by every LLM provider and model version.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Prefilling is provider-specific; for example, Anthropic's documentation notes it is not supported on its newer Claude models and recommends structured outputs or system-prompt instructions instead.

</details>

### 46. True or False: Zero-shot prompting can be the better choice when you want varied, creative output such as brainstorming unusual test ideas.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Examples narrow output towards their pattern, reducing creativity. Zero-shot also suits common tasks and early exploration.

</details>

### 47. True or False: At temperature 0, the model's most likely answer is always the correct answer.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Consistency is not correctness. The most likely answer can still be wrong if the prompt lacks context.

</details>

### 48. True or False: When an AI table and your real code disagree on an expected value, the AI is always the one that is wrong.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Either could be wrong. Always compare against the **requirement**; if the code does not match it, you have found a real application defect.

</details>

### 49. True or False: Using `itertools.product` to generate all decision-table rules guarantees no combination is forgotten.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The table is complete by construction; combinations are a mechanical job for code. The *action* column, however, still contains assumptions to confirm.

</details>

### 50. True or False: The passing `lowercase-code` test proves that coupon codes are required to be case-sensitive.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It documents *current* behaviour, not confirmed *required* behaviour. Case handling is an open question for the product owner.

</details>

### 51. True or False: Adding `@pytest.mark.xfail` to a failing boundary test is an acceptable fix when the requirement has not changed.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It hides the failure, which is one of the listed ways a test gets weakened. Ask: "Did the code change, or did the test change?"

</details>

### 52. True or False: Explaining unfamiliar code is one of the lower-risk uses of an AI assistant, but you should still predict first and verify at least one claim.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A wrong explanation costs less than wrong code, but explanations can be confidently wrong on subtle details.

</details>

---

## Part 3: Code Prediction

### 53. What does `refine_loop.py` print for prompt version `v2`, which mentions SAVE10 and the $50 rule but nothing about unknown codes or numbered lists? (The fake model replies: "Try SAVE10 on orders of $100.00 and $50.00 and check the discount.")

The four checks are: mentions "50.00", mentions "49.99", contains "ValueError", starts with "1.".

- [ ] A) `v2: 0/4 checks passed`
- [ ] B) `v2: 1/4 checks passed`
- [ ] C) `v2: 2/4 checks passed`
- [ ] D) `v2: 4/4 checks passed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `v2: 1/4 checks passed`

**Explanation:** The reply contains "50.00" (pass) but not "49.99", not "ValueError", and does not start with "1.". `sum(checks.values())` counts `True` as 1.
- **Why others are wrong:**
  - A) "50.00" is in the reply.
  - C) Only one substring matches.
  - D) That is v3's result.

</details>

### 54. What does this specificity linter print for the vague prompt?

```python
vague = "Write some tests for the coupon feature."
score, missing = lint(vague)    # 7 checks: task verb, technique, quantity,
print(f"score {score}/7")       # output format, audience, context block, constraints
```

- [ ] A) `score 0/7`
- [ ] B) `score 1/7`
- [ ] C) `score 3/7`
- [ ] D) `score 7/7`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `score 1/7`

**Explanation:** Only the task verb "write" matches. Technique, quantity, format, audience, context block and constraints are all missing.
- **Why others are wrong:**
  - A) "write" is in the verb pattern.
  - C) No other patterns match.
  - D) That was the specific prompt's score.

</details>

### 55. What happens when this runs?

```python
import json
text = '{"id": "TC-01", "expected": 45.0,}'
try:
    json.loads(text)
    print("OK")
except json.JSONDecodeError:
    print("FAIL")
```

- [ ] A) `OK`
- [ ] B) `FAIL`
- [ ] C) `TypeError`
- [ ] D) Prints the dictionary

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `FAIL`

**Explanation:** JSON forbids a trailing comma after the last item (Python literals allow it, which is why models slip).
- **Why others are wrong:**
  - A) The trailing comma is invalid JSON.
  - C) `json.loads` raises `JSONDecodeError`, a `ValueError` subclass, not `TypeError`.
  - D) Parsing fails before anything could be printed.

</details>

### 56. The `extract_json_block` helper strips code fences and cuts from the first `{`/`[` to the last matching bracket. What does `parse_llm_json` return for this input?

```python
'Sure! Here is the test case:\n{"id": "TC-01", "expected": 45.0}\nHope this helps.'
```

- [ ] A) `ValueError: No JSON object or array found`
- [ ] B) `{'id': 'TC-01', 'expected': 45.0}`
- [ ] C) `ValueError: JSON block is not closed`
- [ ] D) The whole string unchanged

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `{'id': 'TC-01', 'expected': 45.0}`

**Explanation:** The chatter before and after is harmless wrapping; slicing from the first `{` to the last `}` rescues the valid object.
- **Why others are wrong:**
  - A) A `{` is present.
  - C) A closing `}` is present.
  - D) The function returns parsed Python objects.

</details>

### 57. In an f-string prompt, what does this print?

```python
x = "SAVE10"
print(f'{{"code": "{x}"}}')
```

- [ ] A) `{{"code": "SAVE10"}}`
- [ ] B) `{"code": "SAVE10"}`
- [ ] C) `{"code": "{x}"}`
- [ ] D) A `SyntaxError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `{"code": "SAVE10"}`

**Explanation:** Doubled braces `{{` and `}}` print as literal single braces; `{x}` is replaced by the variable's value. Forgetting to double braces in JSON-shaped prompts is a very common bug.
- **Why others are wrong:**
  - A) Doubled braces are printed as single braces.
  - C) `{x}` is a placeholder and gets substituted.
  - D) The f-string is valid.

</details>

### 58. How many messages does `build_messages` produce for 1 system instruction, 3 few-shot examples (each as a user/assistant pair) and 1 new input?

- [ ] A) 4
- [ ] B) 5
- [ ] C) 7
- [ ] D) 8

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 8

**Explanation:** 1 system + (3 × 2) example messages + 1 real user input = 8.
- **Why others are wrong:**
  - A) That counts each example as one message and forgets pairs.
  - B) That ignores the assistant messages.
  - C) That forgets either the system or the final user message.

</details>

### 59. What Jaccard similarity does the lesson compute between "Applying coupon SAVE10 to a $45 order still gives a discount." (10 distinct words) and "Coupon SAVE10 is accepted on a $20 order." (8 distinct words), which share 4 words?

- [ ] A) 0.40
- [ ] B) 0.29
- [ ] C) 0.50
- [ ] D) 0.22

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 0.29

**Explanation:** Union = 10 + 8 − 4 = 14. Jaccard = 4 / 14 ≈ 0.29.
- **Why others are wrong:**
  - A) That is 4 / 10 (forgetting the second text).
  - C) That is 4 / 8.
  - D) That is 4 / 18 (forgetting to subtract the shared words).

</details>

### 60. What does `boundary_values("50.00", three_value=True)` return (as strings)?

```python
from decimal import Decimal
def boundary_values(threshold, step="0.01", three_value=False):
    t, s = Decimal(threshold), Decimal(step)
    return [t - s, t, t + s] if three_value else [t - s, t]
```

- [ ] A) `['49', '50', '51']`
- [ ] B) `['49.99', '50.00', '50.01']`
- [ ] C) `['49.99', '50.00']`
- [ ] D) `['49.9', '50.0', '50.1']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['49.99', '50.00', '50.01']`

**Explanation:** Decimal keeps exact cent values; 3-value BVA is below, on and above the boundary.
- **Why others are wrong:**
  - A) That uses a step of 1, the classic AI mistake.
  - C) That is the 2-value result.
  - D) That uses a step of 0.1.

</details>

### 61. In `ep_coverage.py`, the AI's inputs are `[20.00, 35.50, 50.00, 75.00, 120.00]` and the partitions are "negative", "0 to 49.99" and "50+". Which partition is reported MISSING?

- [ ] A) 0 to 49.99
- [ ] B) 50+
- [ ] C) Negative total
- [ ] D) None

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Negative total

**Explanation:** No input is below zero. Note that the finding is "ask the PO what should happen", not "add a test expecting ValueError", because negative totals are unspecified.
- **Why others are wrong:**
  - A) 20.00 and 35.50 cover it.
  - B) 50.00, 75.00 and 120.00 cover it.
  - D) One partition is uncovered.

</details>

### 62. What does `check_label_balance` (with `max_share=0.5`) return for three examples all labelled `Major`?

- [ ] A) `[]`
- [ ] B) `["'Major' is 100% of the examples"]`
- [ ] C) `["'Major' is 50% of the examples"]`
- [ ] D) `{'Major': 3}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `["'Major' is 100% of the examples"]`

**Explanation:** 3 / 3 = 1.0, which exceeds 0.5, so a warning is returned, formatted with `:.0%`.
- **Why others are wrong:**
  - A) An empty list means balanced.
  - C) The share is 100%, not 50%.
  - D) The counts are printed, but the function returns the warnings list.

</details>

### 63. A mutation check replaces `total >= MINIMUM_ORDER` with `total > MINIMUM_ORDER`. The only tests are `assert result is not None` (for $80) and `assert result > 0` (for $50). What is the verdict?

- [ ] A) KILLED
- [ ] B) SURVIVED
- [ ] C) The script crashes
- [ ] D) The tests are skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) SURVIVED

**Explanation:** Both weak assertions still pass with the bug (50.0 is still > 0). Strict BVA assertions such as `apply_coupon(50.00, "SAVE10") == 45.00` would kill it.
- **Why others are wrong:**
  - A) No test fails, so the mutant is not killed.
  - C) The script restores the file in `finally` and runs normally.
  - D) Nothing is skipped.

</details>

### 64. What does the API existence check print for `("pytest", "mark.parameterize")` (note the misspelling)?

- [ ] A) `NOT FOUND`
- [ ] B) `ok`
- [ ] C) `ModuleNotFoundError`
- [ ] D) `AttributeError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `ok`

**Explanation:** `pytest.mark` creates marks dynamically for any name, so `hasattr` returns True. Only running the test reveals "Unknown 'parameterize' mark, did you mean 'parametrize'?". Running the code is the real check.
- **Why others are wrong:**
  - A) That is what you would hope for, but not what happens.
  - C) The module `pytest` exists.
  - D) `hasattr` never raises; it returns a boolean.

</details>

### 65. A "fix" changes the test to `assert result in (45.00, 50.00)` against the buggy `>` code. What does `pytest` report?

- [ ] A) 1 failed
- [ ] B) 1 passed, with the bug still present
- [ ] C) 1 error
- [ ] D) 1 skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 1 passed, with the bug still present

**Explanation:** The buggy result (50.0) is now accepted. The test was weakened and can no longer detect the bug; a customer with a $50.00 cart is still overcharged.
- **Why others are wrong:**
  - A) The loosened assertion passes.
  - C) There is no error in the code.
  - D) Nothing marks it skipped.

</details>

---

## Part 4: Fill-in-the-Blank

### 66. The four steps of the prompt-refinement loop are Draft → Run → ___ → Refine.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Evaluate

**Explanation:** Evaluating compares output with acceptance criteria, like comparing actual and expected results in testing.

</details>

### 67. A decision table with four binary conditions has ___ rules.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 16

**Explanation:** 2⁴ = 16. Generate them with `itertools.product` rather than trusting an AI's list.

</details>

### 68. When parsing, `json.loads` raises `json.___` for invalid JSON, which has `msg`, `lineno` and `colno` attributes.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `JSONDecodeError`

**Explanation:** It is a subclass of `ValueError`. Never write code that depends on the exact message text, which differs between Python versions.

</details>

### 69. The regex `r"\bfind_elements?_by_\w+"` is used to detect ___ Selenium calls in AI-generated code.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** outdated (deprecated / removed)

**Explanation:** It matches `find_element_by_id` and `find_elements_by_css_selector` but not the modern `find_element(By.ID, ...)`.

</details>

### 70. Exploratory test charters commonly follow the template "Explore ___ with ___ to discover ___", and the prompt should say "do not include ___".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** target / resources (or approach) / information; steps

**Explanation:** A charter is a mission, not a script. Without "do not include steps", models drift into scripted test cases.

</details>

### 71. In mutation testing, a mutant that makes at least one test fail is said to be ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** killed

**Explanation:** A mutant that no test catches has **survived**, revealing a gap in the tests.

</details>

---

## Part 5: Matching

### 72. Match each prompt failure mode (1-5) to the best detection method (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Format drift | | A | Ask the same question with the opposite framing and compare |
| 2 | Counting error | | B | Parse it with `json.loads` or check column count |
| 3 | Sycophancy | | C | Run the prompt several times and compare answers |
| 4 | Non-determinism | | D | `len()` on the returned list |
| 5 | Hallucinated function | | E | `importlib` + `hasattr`, or simply run the code |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-A, 4-C, 5-E

**Explanation:** If a failure can be detected by code, detect it by code. Sycophancy needs judgement, and flipping the framing is the practical test.

</details>

### 73. Match each format (1-5) to its best consumer (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | JSON | | A | Quick brainstorming and checklists for people |
| 2 | Markdown table | | B | BDD frameworks and product owners |
| 3 | CSV | | C | Python code, APIs and CI steps |
| 4 | Gherkin | | D | Human review in chat, Jira or pull requests |
| 5 | Numbered list | | E | Spreadsheets and flat data-driven tests |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-D, 3-E, 4-B, 5-A

**Explanation:** Choose the format by consumer: code → JSON (or CSV for flat data); people → tables or lists; tools with their own syntax → that syntax.

</details>

### 74. Match each test design prompt pattern (1-5) to why it helps (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Analysis before tests | | A | Surfaces gaps the model would not volunteer |
| 2 | Technique labelling | | B | Builds on existing tests and keeps output short |
| 3 | "What did you not cover?" | | C | Makes reasoning reviewable and tests more consistent |
| 4 | Critique-and-extend | | D | Prevents 49/50/51 boundary mistakes |
| 5 | Precision statement | | E | Shows coverage, exposes padding, enables traceability |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-A, 4-B, 5-D

**Explanation:** These patterns form the core of a test design prompt library for Project 2.

</details>

### 75. Match each pytest debugging option (1-5) to what it does (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `-x` | | A | Re-run only the tests that failed last time |
| 2 | `-l` | | B | Drop into the Python debugger at the failure |
| 3 | `--lf` | | C | Stop at the first failure |
| 4 | `--pdb` | | D | Run only tests whose names match an expression |
| 5 | `-k "exact_minimum"` | | E | Show local variable values in tracebacks |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-A, 4-B, 5-D

**Explanation:** These options improve the information you read yourself and paste into a debugging request.

</details>
