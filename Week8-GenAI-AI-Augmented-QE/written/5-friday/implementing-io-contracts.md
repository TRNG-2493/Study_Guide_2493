# Implementing IO Contracts

## Learning Objectives

By the end of this lesson you will be able to:

- **Write** `check_reply.py`, which checks any AI reply against the contract and the rules R1 to R4 and Q1.
- **Explain** defensive parsing: finding the JSON inside a reply that contains extra text, and handling broken JSON safely.
- **Explain** how three Python sets make rules R2 and R4 short and exact.
- **Test** the checker on replies with known problems, and confirm it agrees with your hand checks.
- **Identify** which parts of the contract the checker does and does not implement.

---

## Why This Matters

On Thursday, in *Required Fields and Validation Rules*, you checked Reply A and Reply B by hand. It took several minutes per reply, and you had to be careful: the R4 trap caught many people, and the "US-031" typo in Reply B was easy to miss.

A checker does the same work in a fraction of a second, and it never gets tired, never skips a rule and never falls into the R4 trap. More importantly for what comes later today, it is **completely predictable**: the same reply always gets the same result. That is exactly what you need to compare two versions of the agent fairly. If the judge changed its mind between runs, you could not tell whether the agent improved or the judge did.

This lesson writes `check_reply.py`, about 45 lines of standard Python. Then it does what testers do with any new tool: **tests it**, on replies whose problems you already know, and on some tricky ones. That testing finds a few things the checker cannot see, which is just as useful to know as what it can.

> **Using this with the handout:** this lesson goes deeper into **Handout 09, Topic 3**. It uses the same `check_reply.py`, built in the same four steps, the same flow diagram, the same sample-reply results and the same exercises.

---

## The Concept

### 1. What Does "Implementing the Contract" Mean?

**Implementing the IO contract** means turning the contract and rules from Thursday into **code that checks every AI reply**. Our checker:

1. finds the JSON in the reply;
2. checks the **required fields**;
3. checks rules **R1 to R4** against the story;
4. checks the quality rule **Q1**;
5. returns a **list of problems**. An **empty list** means the reply passes.

Returning a list, rather than just "pass" or "fail", is a deliberate choice. A list says **what** is wrong, which is what you need to fix it. It is the same principle as Thursday's check records: every failure carries its evidence.

### 2. The Order of the Checks

The handout's first key idea: **the checker runs the checks in order, and stops early when a reply is too broken to continue.**

```text
reply text ─► find the JSON ─► required fields ─► rules R1–R4 ─► quality Q1 ─► list of problems
                  │                  │
              stop if none     stop if any missing
```

The two early stops are not shortcuts; they are necessary. If there is no JSON, there are no fields to check. If `test_cases` is missing, rules R2, R3 and R4, which all count or read test cases, would crash trying. So the checker reports the deepest problem it can reach, and stops there.

After the early stops, the checker does **not** stop at the first broken rule. Reply A broke four rules, and the checker should report all four, so all four can be fixed at once. That matches the hand-checking advice from Thursday.

### 3. Defensive Parsing

The second key idea: **defensive parsing**, which you met on Tuesday in *Format Locking*. AI replies often add "Here you go!" or put the JSON inside ```` ```json ```` fences, even when told not to. A checker that demanded pure JSON would fail replies whose content was fine.

So the checker keeps only the part from the **first `{`** to the **last `}`**, and reads that. The US-205 sample reply begins *"Here are the test cases for US-205:"* and wraps the JSON in a fence; the checker ignores both.

Defensive parsing is generous about **wrapping**, not about **content**. If the JSON itself is broken, the checker says so, instead of guessing what the AI meant. Being generous about the wrapper and strict about the content is the right balance for checking AI output.

### 4. One Function, Reused

The third key idea: `check_reply(story, reply_text)` is **one function**, and later today the runner will reuse it for every story and every version. So the function takes its inputs as **arguments** (a story and some reply text) and **returns** its result, rather than opening files or printing by itself. The few lines that open files and print are kept at the bottom, inside `if __name__ == "__main__":`, exactly like `build_prompts.py`.

The benefit is that every rule lives in **one place**. Fix a rule once, and every future run uses the fix. You will see this in action in *Building Validation Scripts*.

### 5. Code Checks the Contract; People Check the Meaning

The fourth key idea, which you have met all week: **a reply can pass every rule and still contain an invented value.** The checker is the first layer of validation, not the last. *Agent Output Validation*, later today, adds the human layer.

### 6. Worked Example: `check_reply.py`

Create `check_reply.py` in your `agent` folder and build it step by step.

#### Step 1 (Editor): Find and read the JSON

```python
import json

REQUIRED = ["story_id", "status", "test_cases", "open_questions"]
VAGUE_WORDS = ["works", "correctly", "properly", "as expected", "successfully"]

def check_reply(story, reply_text):
    # Step 1: find the JSON object in the reply and read it
    start, end = reply_text.find("{"), reply_text.rfind("}")
    if start == -1 or end == -1:
        return ["Not JSON: no { ... } found in the reply"]
    try:
        reply = json.loads(reply_text[start:end + 1])
    except json.JSONDecodeError as err:
        return [f"Not valid JSON: {err.msg}"]
```

**What this code does:**

- `REQUIRED` and `VAGUE_WORDS` are lists taken straight from `contract.md`. Keeping them at the top, in capitals, marks them as **constants**: values the code uses but never changes. To change a rule's word list, you change one line here.
- `find("{")` is the position of the **first** `{`, and `rfind("}")` ("find from the right") is the position of the **last** `}`. Everything between them is the JSON. Any chat text or fences around it are ignored.
- If there is no `{` or `}`, `find` returns `-1`, so the function returns one clear problem straight away.
- `json.loads` turns the JSON text into a Python dictionary. If the JSON is broken, `try/except` catches the error and returns it as a problem instead of crashing.

#### Step 2 (Editor): Required fields

Add inside the function:

```python
    # Step 2: required fields
    missing = [field for field in REQUIRED if field not in reply]
    if missing:
        return [f"Missing field: {field}" for field in missing]
```

**What this code does:** lists every required field that is **missing**. If any are missing, it stops here, because the rules below need those fields.

An **empty** list such as `"test_cases": []` is **not** missing: the key is present, so `field not in reply` is false. That is exactly the "missing is not empty" rule from Thursday, in one line of code. US-311's honest refusal, with `"test_cases": []`, passes this check, as the contract says it should.

#### Step 3 (Editor): Rules R1 to R4

Add:

```python
    # Step 3: rules that compare the reply with the story
    problems = []
    if reply["story_id"] != story["story_id"]:
        problems.append("R1: story_id does not match the story")
    story_acs = {ac["id"] for ac in story["acceptance_criteria"]}
    covered = {ac for tc in reply["test_cases"] for ac in tc.get("ac_ids", [])}
    asked = {q.split(":")[0].strip() for q in reply["open_questions"]}
    for ac in sorted(covered - story_acs):
        problems.append(f"R2: {ac} is not in the story (invented)")
    if len(reply["test_cases"]) > story["max_cases"]:
        problems.append(f"R3: {len(reply['test_cases'])} test cases, maximum is {story['max_cases']}")
    for ac in sorted(story_acs - covered - asked):
        problems.append(f"R4: {ac} has no test case and no open question")
```

**What this code does, rule by rule:**

- **R1** compares the two story IDs, exactly. "US-031" is not "US-311", and neither is "us-205" the same as "US-205".
- Three **sets** (collections without duplicates) make the other rules easy:
  - `story_acs`: the AC ids in the story, for example {AC1, AC2, AC3, AC4};
  - `covered`: the AC ids used in the test cases;
  - `asked`: the AC ids that open questions start with. `"AC4: What...".split(":")[0]` gives `"AC4"`.
- **R2**: `covered - story_acs` is the AC ids in the reply that are not in the story, that is, **invented**.
- **R3** counts the test cases and compares with `max_cases`.
- **R4**: `story_acs - covered - asked` is the ACs with **no** test case **and** no question, that is, **forgotten**.
- `sorted(...)` keeps the order the same every time, so the output is predictable.

`tc.get("ac_ids", [])` deserves a note. If a test case has no `ac_ids` field, `get` returns an empty list instead of crashing. The test case then covers nothing, which is the honest interpretation.

#### Step 4 (Editor): Quality rule Q1, and return the result

Add:

```python
    # Step 4: a quality rule - expected results must be exact
    for tc in reply["test_cases"]:
        if any(word in tc.get("expected_result", "").lower() for word in VAGUE_WORDS):
            problems.append(f"Q1: {tc.get('id', '?')} has a vague expected result")
    return problems
```

**What this code does:** for each test case, checks whether the expected result contains any vague word. `.lower()` makes "Works" and "works" the same. `tc.get(..., "")` avoids a crash if a field is missing, and `tc.get('id', '?')` prints `?` if the test case has no ID. Finally, the function returns the list of problems.

#### Step 5 (Editor, then Terminal): Try it on one reply

Add at the bottom, **not** indented:

```python
if __name__ == "__main__":
    with open("stories/US-205.json", encoding="utf-8") as f:
        story = json.load(f)
    with open("replies/v1/US-205.txt", encoding="utf-8") as f:
        reply_text = f.read()
    problems = check_reply(story, reply_text)
    print("PASS" if not problems else "FAIL")
    for problem in problems:
        print(" -", problem)
```

Then run:

```bash
python check_reply.py
```

With the US-205 sample reply from *Creating Reusable Prompt Templates*, it prints:

```text
FAIL
 - R3: 6 test cases, maximum is 5
 - R4: AC4 has no test case and no open question
```

Notice the checker **ignored** the "Here are the test cases" line and the ```` ```json ```` fence: defensive parsing at work.

With your own AI's reply, you will see `PASS` or a different list of problems. Either is fine. **Check one problem by hand** to make sure you agree with the checker. A checker you have not checked is just another source you are trusting blindly.

The consolidated file is Steps 1 to 5 together: about 45 lines, as the handout promises.

### 7. The Sets, Worked by Hand

Sets can feel abstract, so here are the three sets for the US-205 sample reply, worked out by hand. The reply's test cases use `ac_ids` AC1, AC1, AC2, AC3, AC3 and AC1, and it has no open questions.

| Set | Contents | How |
|---|---|---|
| `story_acs` | {AC1, AC2, AC3, AC4} | The story's four ACs |
| `covered` | {AC1, AC2, AC3} | Every AC id in every test case; duplicates disappear |
| `asked` | {} (empty) | No open questions |
| `covered - story_acs` (R2) | {} | Every covered AC is in the story: nothing invented |
| `story_acs - covered - asked` (R4) | **{AC4}** | AC4 is neither covered nor asked about |

We printed the real sets from the reply, and they match the table. R4 reports AC4, as the checkpoint shows.

Now the same calculation for the improved v1.1 reply you will meet later today, which adds the question *"AC4: What happens, and what message is shown, when a second coupon is entered?"*:

| Set | Contents |
|---|---|
| `covered` | {AC1, AC2, AC3} |
| `asked` | **{AC4}** |
| `story_acs - covered - asked` (R4) | {} |

One question moves AC4 into `asked`, and R4 is satisfied. That is the "a question counts as coverage" rule from Thursday, done by one subtraction.

Notice also what the sets **cannot** see. TC-205-05, "Lowercase save10 is accepted", uses `ac_ids: ["AC3"]`. AC3 exists, so R2 is happy. The test case is invented, but it points at a real AC, and the sets only see the ID. That one is for the human layer.

### 8. Results for the Other Sample Replies

The handout's exercise 1 asks you to change both `US-205` file names in the bottom block to `US-312`, then to `US-311`, and run the checker again. We did:

| Story | Result |
|---|---|
| US-312 | `FAIL`: Q1: TC-312-02 has a vague expected result |
| US-311 | `PASS` |

Look hard at the US-311 `PASS`. The reply invents "within 2 seconds" and sets `status` to `"ok"` for a story that cannot be tested. Every rule the checker knows is satisfied: the ID matches, AC1 exists and is covered, one case is within the limit of three, and "Results are displayed within 2 seconds" contains no vague word. The checker is right by its rules, and the reply is still wrong. You will come back to it in *Agent Output Validation*.

### 9. Testing the Checker

A tester does not trust a new tool because it gives sensible output on three examples. So we tested `check_reply` on replies whose problems we knew in advance, including some designed to be awkward. Every result below is real output from the checker as written in the handout:

| Test reply | Expected | Checker result | Agrees? |
|---|---|---|---|
| Thursday's Reply A (US-312) | R2, R3, R4, Q1 | R2 (AC3), R3 (4 vs 3), R4 (AC2), Q1 (TC-312-02) | ✅ |
| "Sorry, I can't help with that." | Not JSON | `Not JSON: no { ... } found in the reply` | ✅ |
| JSON cut off half-way | Not valid JSON | `Not valid JSON: Expecting ',' delimiter` | ✅ |
| `open_questions` missing | Missing field | `Missing field: open_questions` | ✅ |
| `"story_id": "us-205"` | R1 | `R1: story_id does not match the story` | ✅ |
| Valid JSON, then *"Let me know if you want more {details}."* | Should pass | `Not valid JSON: Extra data` | ⚠️ |
| Question starts *"Question about AC4: ..."* | AC4 is asked about | `R4: AC4 has no test case and no open question` | ⚠️ |
| Expected result *"The Payment networks banner is shown"* | Not vague | `Q1: ... has a vague expected result` | ⚠️ |
| `"status": "done"` | Not allowed | **PASS** | ❌ |
| A test case with only `id` and `ac_ids` | Missing fields | **PASS** | ❌ |

The first five rows show the checker doing exactly its job. The rest are worth understanding one by one.

- **Extra data.** The AI added a sentence **with braces** after the JSON. `rfind("}")` found the last `}`, which belonged to `{details}`, so the text passed to `json.loads` was the JSON plus some chat, and it failed. Defensive parsing assumes the last `}` closes the JSON; usually true, not always. The reply's content was fine, so this is a **false alarm**, but a safe one: it fails loudly and a person looks.
- **Question prefix.** The contract says questions **start** with the AC id. "Question about AC4: ..." does not, so the checker does not count it. That is the checker being **strict**, as the contract asks, the same strictness as the R4 trap on Thursday. The fix is in the reply, not the checker.
- **"networks".** "networks" contains "works", so Q1 fires on a perfectly exact result. Q1 checks for the word as **text inside** the expected result, not as a whole word. This is the same word-list limit as Wednesday's `word_check.py`.
- **Status "done".** The checker never looks at `status`. The schema in *JSON Schema* would reject `"done"`; our checker accepts it.
- **Missing test case fields.** The checker checks the four **top-level** fields, but not the six fields **inside** each test case. A test case with no `expected_result` passes.

None of these make the checker useless. They show what it **is**: an implementation of **part** of the contract.

### 10. What the Checker Implements

Put the contract from Thursday next to the checker:

| Contract item | In `check_reply.py`? |
|---|---|
| Reply is one JSON object | ✅ Step 1 (defensively) |
| Four top-level fields required | ✅ Step 2 |
| `status` is "ok" or "needs_clarification" | ❌ Not checked |
| Six fields in every test case | ❌ Not checked |
| `id` follows TC-<story>-<two digits> | ❌ Not checked (rule F1 is a human check) |
| R1 to R4 | ✅ Step 3 |
| Q1 | ✅ Step 4 (as text inside the result) |
| Human checklist (invented values, boundaries, messages) | ❌ By design: people check these |

Some gaps are deliberate. The human checklist is for people, as the rule map in *Building Agent Instructions* shows. Others are simply not built yet. The handout keeps the checker short so beginners can read every line; that is a sensible trade-off, as long as you **know** where the gaps are. A gap you know about is a risk you can manage. A gap you do not know about is a surprise waiting to happen.

### 11. An Optional Extension: Two More Checks

If you want to close the two clearest gaps, six extra lines do it. Add two constants under `VAGUE_WORDS`:

```python
STATUSES = ["ok", "needs_clarification"]
TC_FIELDS = ["id", "title", "ac_ids", "type", "steps", "expected_result"]
```

and, in Step 3, straight after `problems = []`:

```python
    if reply["status"] not in STATUSES:
        problems.append(f"S1: status {reply['status']!r} is not allowed")
    for tc in reply["test_cases"]:
        for field in TC_FIELDS:
            if field not in tc:
                problems.append(f"S2: {tc.get('id', '?')} is missing {field}")
```

We ran the extended checker on the same tests. The two ❌ rows now fail correctly:

```text
status done: ["S1: status 'done' is not allowed"]
tc missing fields: ['S2: TC-205-01 is missing title', 'S2: TC-205-01 is missing type', 'S2: TC-205-01 is missing steps', 'S2: TC-205-01 is missing expected_result']
```

And, just as important, **nothing else changed**: every sample reply in the handout gets exactly the same result as before. When you extend a checker, that second test is the one that matters most. A new check that also changes old results is a new bug.

The `S` stands for **schema**: these are the checks the schema from Thursday makes, written in plain Python. If you add them, add `S1` and `S2` to the rule map and to `contract.md`, so the code and the documents still agree. The worked examples later today use the handout's checker, so their outputs stay the same either way.

### 12. Acting on the Checker's Output

Every message the checker prints points to a likely cause and a next step. Reading them this way turns a FAIL into a to-do list:

| Message | Most likely cause | What to do next |
|---|---|---|
| `Not JSON: ...` | The reply was saved without its JSON, or the AI refused | Re-save the whole reply; if the AI refused, note it |
| `Not valid JSON: ...` | The reply was cut off, or the AI broke the JSON | Check the end of the reply; a broken JSON is an agent failure |
| `Missing field: ...` | The AI ignored part of the Output section | Note it; strengthen the Output section or an example |
| `R1: ...` | The wrong reply was saved, or the AI typed the ID wrongly | Check the file name first, then the reply |
| `R2: ...` | The AI invented a criterion | Strengthen G1; check the reply for an invented requirement |
| `R3: ...` | Too many test cases | Strengthen F2 |
| `R4: ...` | A criterion was forgotten, or a question did not start with the AC id | Read the reply's questions; strengthen U1 |
| `Q1: ...` | A vague expected result, or a false alarm like "networks" | Read the expected result before deciding |

Two rows start with "check the file" rather than "blame the AI". When a check fails, the cause is sometimes the **process** (a reply saved under the wrong name, or saved incomplete), not the agent. Rule that out first: it is quick, and it stops you "fixing" instructions that were never the problem.

Several rows end with "strengthen" a rule. That is the improvement loop you will run in *Agent Testing and Refinement*: the checker's output, grouped by rule, tells you which instruction to change.

### 13. Why the Checker Must Never Change Its Mind

The definition in the handout calls the checker **completely predictable**, and that property is worth protecting. Run `python check_reply.py` on the same reply ten times and you get the same output ten times. There is nothing random in the code, and it does not depend on the time, the computer or anything outside its two inputs.

Compare that with asking an AI to check the reply, as you did on Thursday in *JSON Schema*. The AI might report different problems on different runs, and sometimes problems that are not there. That makes it useful for a second opinion, and useless as the **judge** in a comparison.

Later today, you will compare v1 with v1.1. If v1.1 passes more stories, you want to be sure the **agent** improved, not that the judge became more lenient. So two rules follow:

- **Do not change the checker between the two runs you are comparing.** If you extend it, as in section 11, rerun the **old** version's replies with the new checker too, so both versions are judged the same way.
- **Do not use an AI as the checker.** Use it to explain, to suggest and to review, as the human layer does. Keep the verdict deterministic.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: replies/v1/US-205.txt` | The reply was not saved, or was saved with a different name | Save it as exactly `replies/v1/US-205.txt` |
| `Not JSON: no { ... } found in the reply` | You saved only the AI's intro sentence, not the JSON | Copy the AI's **whole** reply |
| `Not valid JSON: ...` | The reply was cut off, or the AI made a JSON mistake | Check the reply ends with `}`. If the AI broke the JSON, that is a real agent failure: note it |
| `Not valid JSON: Extra data` | The AI added text containing `}` after the JSON | Look at the end of the reply; note it as a format problem |
| `IndentationError` | A step was added at the wrong indentation | Steps 2 to 4 are **inside** the function (4 spaces); Step 5 is **not** indented |

---

## Practice Exercises

1. **The other stories (code, 5 min).** In the `if __name__ == "__main__":` block, change **both** `US-205` file names to `US-312` and run it again. Then do the same for `US-311`. Write down the results, and compare them with section 8.

2. **Reply A (code, 10 min).** Paste Reply A from *Required Fields and Validation Rules* into a file `replies/v1/test-A.txt`, point the bottom block at it (with `stories/US-312.json`), and run the checker. Does it find the same four problems you found by hand on Thursday?

3. **A new vague word (code, 10 min).** Add `"seamlessly"` to `VAGUE_WORDS`. Create a reply that uses it in an expected result, and check that Q1 fires. Then predict: would "The network error is shown" trigger the original Q1 check? Would "Frameworks page is shown"? Test both.

4. **Explain the sets (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** ask your AI *"Explain this Python function line by line for a beginner"* and paste `check_reply`.
   - **Review:** is its explanation of the three **sets** correct? Compare with section 7.
   - **Run:** work out the three sets by hand for the US-312 sample reply, then print them to check.
   - **Record:** note in `prompts.txt` anything the AI explained wrongly.

5. **Extend the checker (code, 15 min, optional).** Add S1 and S2 from section 11. Run the checker on all three sample replies and confirm the results do not change. Then write a reply that breaks S2 only.

---

## Knowledge Check

1. What does `check_reply` return, and what does an empty result mean?

<details><summary>Answer</summary>

A list of problems. An empty list means the reply passes every check the function makes.

</details>

2. Why does the checker stop early when the JSON is missing or a required field is missing?

<details><summary>Answer</summary>

The later checks need those parts. Without JSON there is nothing to check, and without fields such as `test_cases` the rules would crash.

</details>

3. How does defensive parsing find the JSON in a reply with extra text?

<details><summary>Answer</summary>

It keeps everything from the first `{` to the last `}` and reads that with `json.loads`, ignoring chat text and fences around it.

</details>

4. A reply has `"test_cases": []`. Does the required-fields check fail? Why?

<details><summary>Answer</summary>

No. The field is present but empty, which the contract allows. Only a missing field fails.

</details>

5. What does `story_acs - covered - asked` find, and which rule uses it?

<details><summary>Answer</summary>

ACs with no test case and no open question, that is, forgotten ACs. It is rule R4.

</details>

6. TC-205-05 ("Lowercase save10 is accepted") uses `ac_ids: ["AC3"]`. Why does R2 not catch it?

<details><summary>Answer</summary>

AC3 exists in the story. R2 only checks that AC ids are real, not whether the test case's rule is in the story. A person must catch the invented rule.

</details>

7. Name two parts of the contract that the handout's checker does not check.

<details><summary>Answer</summary>

Any two of: the allowed `status` values, the six fields inside each test case, and the test case ID format. The human checklist items are also left to people by design.

</details>

8. Why does Q1 fire on "The Payment networks banner is shown"?

<details><summary>Answer</summary>

Q1 looks for the vague word as text inside the expected result, and "networks" contains "works". It is a false alarm caused by the simple word check.

</details>

9. You extend the checker with S1 and S2 between the v1 and v1.1 runs. What must you do to keep the comparison fair?

<details><summary>Answer</summary>

Rerun the v1 replies with the extended checker too, so both versions are judged by exactly the same rules.

</details>

---

## Glossary

- **Implementing the contract:** turning the contract's rules into code that checks every reply.
- **`check_reply.py`:** the script that checks one AI reply against the contract and rules.
- **Defensive parsing:** keeping only the JSON part of a reply and handling broken JSON safely.
- **`find` / `rfind`:** the position of the first / last occurrence of some text.
- **Constant:** a value the code uses but never changes, written in capitals, such as `REQUIRED`.
- **Set:** a Python collection without duplicates; `a - b` gives the items in `a` but not in `b`.
- **Early stop:** returning straight away when a reply is too broken for later checks.
- **False alarm (false positive):** a check reporting a problem that is not there.
- **Strict check:** a check that follows the contract exactly, even when the intent seems clear.
- **Deterministic check:** a check that always gives the same result for the same input.
- **Checker coverage:** which parts of the contract the checker actually tests.

---

## Summary

- **`check_reply.py`** finds the JSON, checks the required fields, then R1 to R4 and Q1, and returns a **list of problems**.
- **Defensive parsing** is generous about wrapping (chat text, fences) and strict about content (broken JSON).
- **Three sets** make R2 (invented ACs) and R4 (forgotten ACs) one subtraction each.
- **Test the checker.** It matched every hand check, but it also has false alarms ("networks", trailing braces) and gaps (status values, test case fields).
- **Know what the checker covers.** A script PASS means "passed these checks", not "correct". The human layer comes next.

---

## Additional Resources

- Python documentation, *json — JSON encoder and decoder*: https://docs.python.org/3/library/json.html
- Python documentation, *Data Structures: sets*: https://docs.python.org/3/tutorial/datastructures.html#sets
- Python documentation, *Built-in Types: `str.find` and `str.rfind`*: https://docs.python.org/3/library/stdtypes.html#str.find
