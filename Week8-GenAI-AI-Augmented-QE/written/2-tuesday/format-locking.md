# Format Locking

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what format locking is, and why AI output that feeds code needs a fixed shape.
- **Choose** a suitable format (table, JSON or a fixed single line) for where the answer is going.
- **Write** a format-locked prompt that names every field, gives an example, sets an exact count and forbids extra text.
- **Recognise** common kinds of format drift, and read an AI reply safely in Python with defensive parsing.
- **Check** both the shape of a reply and the values inside it, and explain why a correct shape is not a correct answer.

---

## Why This Matters

In *Prompt Engineering Principles*, fixing the output format turned a loose answer into a table that a script could check. This lesson goes further: from answers that **people** read to answers that **code** reads.

That step matters for the rest of the week. On Wednesday you will turn AI drafts into test cases and test data. On Friday, your QA agent's reply is read by a validation script, not by a person. If the reply's shape changes from run to run, the script breaks, or, worse, it reads the wrong value without noticing.

AI providers know this is a problem. OpenAI introduced a feature called **Structured Outputs**, which constrains a model's reply to follow a JSON Schema supplied by the developer. Even so, its own documentation says that applications still need to handle refusals, incomplete responses and errors, and must still check business rules that the schema does not express ([OpenAI docs](https://developers.openai.com/api/docs/guides/structured-outputs)). In other words: even when the shape is guaranteed, the **content** still needs checking. That is the core idea of this lesson.

You will meet JSON Schema properly on Thursday. Today you lock the format with words in the prompt, and check it with a few lines of Python.

> **Using this with the handout:** this lesson goes deeper into **Handout 03, Topic 3**. It uses the same boundary-test prompt, the same drifted reply and the same `parse_reply.py`.

---

## The Concept

### 1. What Is Format Locking?

**Format locking** means telling the AI **exactly** what shape the answer must have, so the answer can be **read by code**, not just by people. A locked format names every field, fixes the order or count, and forbids anything extra.

Compare two replies to the same request:

```text
Free text:
Sure! For the SAVE10 rule I'd check $50.00, which should come out at $45.00, then
$49.99, which stays the same, and maybe $50.01 too, which would be about $45.01.
```

```json
[
  {"title": "Subtotal exactly 50.00 gets 10% off", "subtotal": 50.00, "expected_total": 45.00},
  {"title": "Subtotal 49.99 is unchanged", "subtotal": 49.99, "expected_total": 49.99},
  {"title": "Subtotal 50.01 gets 10% off", "subtotal": 50.01, "expected_total": 45.01}
]
```

Both contain the same test ideas. A person can read either. But only the second can be fed straight into a script, a spreadsheet or a pytest test. Notice also the word "about" in the free-text version: free text invites vagueness, while a field called `expected_total` demands a number.

**An everyday analogy: a form instead of a letter.** A bank does not ask you to "write a letter about yourself". It gives you a form with labelled boxes, so every application can be processed the same way. Format locking turns the AI's reply into a form.

### 2. Choosing the Right Format

Pick the format based on **where the answer is going**:

| Format | Best for | Example use | Watch out for |
|---|---|---|---|
| **Markdown table** | People reading or pasting into a document | Test-case drafts for review | Hard to read in code if columns vary |
| **JSON** | Code: scripts, tests, agents | Test data that drives a pytest test | Strict syntax: double quotes, no trailing commas |
| **Fixed single line** | Quick yes/no or label checks | `VERDICT: PASS` | The model adding explanation after it |
| **CSV** | Spreadsheets | Exporting 50 test records | Commas inside values |

**JSON** (JavaScript Object Notation) is the most common choice when code reads the answer. You met it in Week 7 when testing APIs. As a quick reminder:

- `[ ... ]` is a **list** (Python: `list`).
- `{ "key": value }` is an **object** (Python: `dict`).
- Strings use **double quotes** only. Numbers have no quotes.
- No comma after the last item.

**Work it by hand.** Here is how one item from the handout's reply maps to Python after `json.loads`:

| JSON text | Python value | Python type |
|---|---|---|
| `"Subtotal 49.99 is unchanged"` | `'Subtotal 49.99 is unchanged'` | `str` |
| `49.99` | `49.99` | `float` |
| `45` | `45` | `int` |
| `"45.00"` | `'45.00'` | `str` (not a number!) |
| `true` / `false` / `null` | `True` / `False` / `None` | `bool` / `bool` / `NoneType` |
| `{"title": ...}` | `{'title': ...}` | `dict` |
| `[ ... ]` | `[ ... ]` | `list` |

Look at the fourth row. `"45.00"` in quotes is **text**, not a number. If a model writes the expected total as a string, a check such as `apply_coupon(...) == case["expected_total"]` compares a number with text, and always fails. That is why the prompt states each field's **type**, not just its name.

### 3. Format-Locking Techniques

The handout's prompt uses every technique in this section:

```text
Give exactly 3 boundary test cases for: "SAVE10 gives 10% off a subtotal of $50.00 or more."
Reply ONLY with a JSON list. Each item has exactly these keys:
"title" (string), "subtotal" (number), "expected_total" (number).
Example item: {"title": "Subtotal 100.00 gets 10% off", "subtotal": 100.00, "expected_total": 90.00}
No text before or after the JSON.
```

Taken apart, line by line:

| Technique | In the prompt | Why it helps |
|---|---|---|
| **Name the container** | "Reply ONLY with a JSON list" | The reply starts with `[` and ends with `]` |
| **Name every field, with its type** | `"title" (string), "subtotal" (number), …` | No renamed or extra fields; numbers stay numbers |
| **Show one example** | `Example item: {...}` | The model copies the exact shape, spelling and number style |
| **Give an exact count** | "exactly 3" | A count you can check; "a few" cannot be checked |
| **Forbid extra text** | "No text before or after the JSON" | Reduces "Sure! Here are…" |

Two further tips:

- **Use the example carefully.** The model copies it closely. If the example's title says "gets 10% off", every title may follow that pattern, which is fine here. If the example contained a wrong value, the model might copy that too.
- **Do not make the example one of the answers.** The example uses $100.00, which is not a boundary. That stops the model from simply repeating the example as one of the three cases.

### 4. Format Drift: How Locked Output Still Goes Wrong

Even with a clear format instruction, models sometimes **drift** from it. Remember from *Generative AI Concepts* that the model predicts likely text. Chat assistants have been trained on countless friendly replies that begin "Sure! Here are…", so that opening is very likely, even when you asked for none.

Common kinds of drift:

| Drift | Example | Effect on code |
|---|---|---|
| **Chatty wrapper** | "Sure! Here are the tests:" before the JSON | `json.loads` fails on the first word |
| **Markdown fences** | The JSON wrapped in ```` ```json ```` and ```` ``` ```` | `json.loads` fails on the backticks |
| **Renamed field** | `"expected"` instead of `"expected_total"` | `KeyError` later, or a silent wrong read |
| **Wrong count** | 4 items instead of 3 | Extra or missing test cases |
| **Wrong type** | `"45.00"` (a string) instead of `45.00` | Comparisons fail, or compare text instead of numbers |
| **Single quotes** | `{'title': ...}` | Not valid JSON |
| **Truncation** | The list cut off half-way | Parsing fails; may hit the max-tokens limit from Monday |

Drift is **normal**, not a sign that something is broken. The right response is not to hope it goes away, but to **lock the format in the prompt and check the format in code**.

### 5. Worked Example: Read an AI Reply Safely

The handout sends the prompt from section 3. Even so, the reply comes back with drift around it. Here is the handout's `parse_reply.py`, which handles it in five steps:

````python
import json

# Step 1: a reply copied from an AI assistant (format drift included!)
reply = """Sure! Here are the boundary tests you asked for:
```json
[
  {"title": "Subtotal exactly 50.00 gets 10% off", "subtotal": 50.00, "expected_total": 45.00},
  {"title": "Subtotal 49.99 is unchanged", "subtotal": 49.99, "expected_total": 49.99},
  {"title": "Subtotal 50.01 gets 10% off", "subtotal": 50.01, "expected_total": 45.01}
]
```
Let me know if you need more!"""

# Step 2: try to read it as JSON directly
try:
    data = json.loads(reply)
except json.JSONDecodeError as err:
    print("Direct parse failed:", err.msg)

# Step 3: defensive parsing - keep only the part between [ and ]
def extract_json_list(text):
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list found in the reply")
    return json.loads(text[start:end + 1])

data = extract_json_list(reply)
print("Parsed", len(data), "test cases")

# Step 4: check the format we asked for
REQUIRED_KEYS = {"title", "subtotal", "expected_total"}
assert isinstance(data, list), "Reply must be a JSON list"
assert len(data) == 3, f"Asked for 3 cases, got {len(data)}"
for i, case in enumerate(data, start=1):
    missing = REQUIRED_KEYS - case.keys()
    assert not missing, f"Case {i} is missing {missing}"
print("Format OK")

# Step 5: now the data is safe to use
for case in data:
    print(f"{case['subtotal']:>6.2f} -> {case['expected_total']:>6.2f}  {case['title']}")
````

Run it with `python parse_reply.py`. Output:

```text
Direct parse failed: Expecting value
Parsed 3 test cases
Format OK
 50.00 ->  45.00  Subtotal exactly 50.00 gets 10% off
 49.99 ->  49.99  Subtotal 49.99 is unchanged
 50.01 ->  45.01  Subtotal 50.01 gets 10% off
```

The reply contains **three** kinds of drift at once: a sentence before, Markdown fences around the JSON, and a sentence after. (This lesson's code block uses four backticks on the outside, because the reply itself contains three.)

#### 5.1 Step by step

- **Step 1: the reply.** `reply` holds the AI's answer as one string. Triple quotes (`"""`) allow it to span several lines.
- **Step 2: the direct parse fails.** `json.loads` turns JSON text into Python lists and dictionaries, but only if the text is **pure** JSON. It stops at "Sure!" with the message `Expecting value`. The `try/except` catches the error, so the program carries on and prints the reason.
- **Step 3: defensive parsing.** `text.find("[")` finds the position of the **first** `[`, and `text.rfind("]")` the **last** `]`. Everything between them is the list, so the chatty sentences and the fences are cut away. If either bracket is missing, `find` returns `-1`, and the function raises an error with a **clear message**. `text[start:end + 1]` includes the final `]`.
- **Step 4: check the format you asked for.** Parsing only proves the text is valid JSON. These checks prove it is the JSON **you asked for**: a list, exactly 3 items, and every required key present. `REQUIRED_KEYS - case.keys()` is a **set difference**: the required keys missing from this item. An empty set means nothing is missing.
- **Step 5: use the data.** Only now is the data used. `:>6.2f` means right-aligned, 6 characters wide, 2 decimal places.

#### 5.2 What the checks catch

Rename `"expected_total"` to `"expected"` in the second item and run again. The script stops at Step 4 with:

```text
AssertionError: Case 2 is missing {'expected_total'}
```

That message tells a teammate exactly what is wrong and where. Compare it with what would happen **without** Step 4: the script would crash later, in Step 5, with `KeyError: 'expected_total'`, which says less about the cause. Checking early, with clear messages, is the same principle as a good test assertion.

#### 5.3 Limits of the bracket trick

The `[`…`]` trick works for this reply, but it is not perfect:

- If the chatty sentence before the JSON contained a `[`, such as "Here are the tests [as requested]:", `find` would start in the wrong place, and parsing would fail.
- If the model returned a JSON **object** (`{...}`) instead of a list, there may be no `[` at all.

In both cases the function fails **loudly**, with an error, rather than silently returning wrong data. That is the most important property of defensive parsing: **when it cannot be sure, it stops.** A parser that guesses would be worse than none.

### 6. Shape Is Not Meaning: Check the Values Too

`parse_reply.py` confirms the reply has the right **shape**. It does not confirm the values are **right**. Suppose the model had written `"expected_total": 45.00` for the $50.01 case. Every format check would still pass.

That is why, in *Prompt Engineering Principles*, you added a value check that recalculates each expected total from the rule. The same check fits here, after Step 4:

```python
def ac1_total(subtotal):                      # written by a person, from AC1
    return round(subtotal * 0.9, 2) if subtotal >= 50 else subtotal

for case in data:
    correct = ac1_total(case["subtotal"])
    assert case["expected_total"] == correct, f"{case['title']}: expected {correct}"
print("Values OK")
```

Added to `parse_reply.py`, it prints `Values OK` for this reply. Change 45.01 to 45.00 in the reply and it stops with `AssertionError: Subtotal 50.01 gets 10% off: expected 45.01`.

There are now **two layers of checking**, and you will meet them again on Thursday and Friday:

| Layer | Question | Example check |
|---|---|---|
| **Shape** | Is it the structure we asked for? | A list of 3 items, each with the 3 keys |
| **Meaning** | Are the values correct? | Each expected total matches the rule in AC1 |

Even OpenAI's Structured Outputs, which guarantees the shape, leaves the second layer to you.

### 7. When the Format Breaks: Re-Ask Once

If the defensive parser cannot find valid JSON at all, a common next step is to **re-ask once**, giving the model the error message:

```text
Your previous reply could not be read as JSON. The error was:
"Expecting property name enclosed in double quotes".
Reply again with ONLY the JSON list, using double quotes, and no other text.
```

Telling the model the exact problem usually fixes it in one try. If it does not, stop and look at the reply yourself, rather than re-asking again and again. Building automatic retries into a pipeline, with limits and logging, is a topic of its own, which you will meet in Week 9.

### 8. From Locked Output to a Test

Once a reply is parsed and checked, the data can drive a test directly. You learned `pytest.mark.parametrize` in Week 4. Here, each AI-drafted case becomes one run of the same test:

```python
import pytest
from cart import apply_coupon
from parse_reply import data      # the checked list from parse_reply.py

@pytest.mark.parametrize("case", data, ids=[c["title"] for c in data])
def test_boundary_cases(case):
    assert apply_coupon(case["subtotal"], "SAVE10") == case["expected_total"]
```

Put `cart.py`, `parse_reply.py` and this file (saved as `test_boundaries.py`) in one folder, then run `python -m pytest -q test_boundaries.py`. Output:

```text
...                                                                      [100%]
3 passed in 0.01s
```

(`parse_reply.py` also prints its own lines when it is imported; pytest hides them unless a test fails.) This reuses Monday's `cart.py`. The `ids=` argument names each run after the case's title, so a failure report says which boundary failed. You will take this further in tomorrow's lessons. The order matters: **parse, check shape, check meaning, then test.** Feeding unchecked AI output straight into a test means a wrong expected total becomes a test that fails on correct code, or passes on broken code.

### 9. Format Locking Beyond JSON

The same techniques work for any format:

- **A fixed single line,** for quick verdicts:

  ```text
  Is BUG-104 a duplicate of BUG-101? Reply with exactly one line:
  DUPLICATE: YES or DUPLICATE: NO
  ```

  Code can then check the reply against those two allowed lines, and treat anything else as drift. A defensive version:

  ```python
  # read_verdict.py
  ALLOWED = {"DUPLICATE: YES", "DUPLICATE: NO"}

  def read_verdict(reply):
      lines = [line.strip() for line in reply.strip().splitlines() if line.strip()]
      if len(lines) != 1:
          return None, f"expected 1 line, got {len(lines)}"
      if lines[0] not in ALLOWED:
          return None, f"unexpected verdict: {lines[0]!r}"
      return lines[0] == "DUPLICATE: YES", "ok"

  for reply in ["DUPLICATE: YES", "  DUPLICATE: NO \n", "Duplicate: yes",
                "DUPLICATE: YES\nBoth bugs mention coupons."]:
      print(repr(reply), "->", read_verdict(reply))
  ```

  Output:

  ```text
  'DUPLICATE: YES' -> (True, 'ok')
  '  DUPLICATE: NO \n' -> (False, 'ok')
  'Duplicate: yes' -> (None, "unexpected verdict: 'Duplicate: yes'")
  'DUPLICATE: YES\nBoth bugs mention coupons.' -> (None, 'expected 1 line, got 2')
  ```

  Notice the choices. Extra spaces and blank lines are forgiven, because they do not change the meaning. A different spelling ("Duplicate: yes") and an extra explanation line are **not** forgiven: the function returns `None` and a reason, instead of guessing. You could decide to accept lower-case answers too; what matters is that the rule is **written down in code**, not left to chance. Returning a reason alongside the result also makes the re-ask in section 7 easy: the reason is the error message you send back.

- **A fixed table,** as in *Prompt Engineering Principles*: name the columns, give the ID pattern (TC-01, TC-02…) and forbid text around the table.

- **Labelled sections,** for longer answers that a person reads:

  ```text
  Reply with exactly these headings, in this order:
  Summary:
  Likely cause:
  Suggested fix:
  ```

Whatever the format, the pattern is the same: **lock it in the prompt, then check it before you trust it.**

### 10. Designing a Good Format

Locking a format only helps if the format itself is well designed. A few principles make AI replies easier to check, both for people and for code:

- **One record per item.** Each test case is one object in a list. Do not mix several cases into one long text field.
- **Clear, consistent field names.** Use one naming style, such as `snake_case` (`expected_total`), and keep it the same in every prompt. Renaming fields between prompts invites drift.
- **Put units in the name or the instructions.** `expected_total` in dollars, or `timeout_seconds`, removes guessing about "45" meaning dollars, cents or seconds.
- **Fixed sets of values for categories.** If a field can only be `"High"`, `"Medium"` or `"Low"`, say so in the prompt: "priority must be one of High, Medium, Low". A fixed set is easy to check in code with a single `in` test.
- **Numbers as numbers, text as text.** State each field's type, and check it.
- **Keep nesting shallow.** A flat list of objects is easier to read and check than objects inside objects inside lists.
- **Leave room for "I don't know".** A field such as `"notes"` or a value such as `"NOT SPECIFIED"` gives the model a place to put uncertainty, instead of inventing a value to fill a required field.

These principles are the first step towards a **contract**: a written agreement about exactly what an AI's input and output must contain. On Thursday you will write one properly, using JSON Schema, for the QA agent you build on Friday.

### 11. A Format-Locking Checklist

Before relying on a format-locked prompt, check:

- [ ] **Container:** does the prompt say "a JSON list" (or table, or single line)?
- [ ] **Fields:** is every field named, with its type?
- [ ] **Example:** is there one example item, which is not one of the answers?
- [ ] **Count:** is there an exact number?
- [ ] **No extras:** does it say "no text before or after"?
- [ ] **Parsing:** does your code extract, parse and fail loudly with a clear message?
- [ ] **Shape checks:** container type, count, keys and types?
- [ ] **Meaning checks:** values recalculated or compared against the requirement?

### 12. Common Errors When Parsing AI Replies

| Error you see | Why it happens | Fix |
|---|---|---|
| `JSONDecodeError: Expecting value` | Text before the JSON, or fences | Use defensive parsing (Step 3) |
| `JSONDecodeError: Expecting property name enclosed in double quotes` | Single quotes, as in `'title'` | Add "use double quotes" to the prompt |
| `JSONDecodeError` about a trailing comma | A comma after the last item. (Python 3.13 says `Illegal trailing comma before end of array`; older versions may say `Expecting ',' delimiter` or similar.) | Add "valid JSON, no trailing commas" to the prompt |
| `SyntaxError` on the `reply = """...` line | The reply itself contains `"""` | Use `'''...'''` around the reply instead |
| `KeyError: 'expected_total'` | A field is missing or renamed | Run the shape checks (Step 4) before using the data |

---

## Practice Exercises

1. **Lock a format (paper, 10 min).** Write a format-locked prompt that asks for exactly 4 test cases for AC3 (*Unknown codes show "Coupon code not recognised"*). Each item must have `code` (string), `expected_message` (string) and `reason` (string). Include an example item that is **not** one of the answers.

2. **Spot the drift (paper, 10 min).** For each reply, name the kind of drift, and say which line of `parse_reply.py` would catch it:
   - (a) `[{'title': 'Exactly 50', 'subtotal': 50.0, 'expected_total': 45.0}]`
   - (b) A valid list of 3 items, where one item has `"expected_total": "45.00"`.
   - (c) A valid list of 2 items.

   *Hint:* one of these passes every check in `parse_reply.py` as written. Which one, and what check would you add?

3. **Your AI, your drift (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** send the handout's boundary-test prompt to your AI assistant in a new chat.
   - **Review:** did it drift? Note each kind of drift from section 4 that you see.
   - **Run:** paste its real reply into `reply = """..."""`, add the value check from section 6, and run `parse_reply.py`.
   - **Record:** write down whether the shape passed, whether the values passed, and one change to the prompt that might reduce the drift.

4. **A single-line format (paper, 10 min).** Write a format-locked prompt that asks whether a failure is flaky or a real defect (Monday's example), and replies with exactly one of two lines. Then write the one-line Python check that accepts only those two answers.

---

## Knowledge Check

1. What is format locking, and why does it matter when code reads the answer?

<details><summary>Answer</summary>

Telling the AI exactly what shape the answer must have, so the answer can be read reliably by code. If the shape varies, the code breaks or reads the wrong values.

</details>

2. Name four techniques for locking a format in a prompt.

<details><summary>Answer</summary>

Any four of: name the container (for example "a JSON list"), name every field with its type, show one example item, give an exact count, and forbid text before or after.

</details>

3. Why does `json.loads(reply)` fail on the handout's reply?

<details><summary>Answer</summary>

The reply is not pure JSON. It starts with "Sure!", has Markdown fences around the list, and ends with another sentence.

</details>

4. What does `text[text.find("["):text.rfind("]") + 1]` do, and when can it fail?

<details><summary>Answer</summary>

It keeps everything from the first `[` to the last `]`, cutting away text around the list. It can fail if there is a `[` in the text before the list, or if the reply has no list at all; in those cases it should raise a clear error.

</details>

5. All format checks pass, but one `expected_total` is wrong. Why did the checks not catch it?

<details><summary>Answer</summary>

Format checks only test the shape (type, count, keys). Checking values needs a separate check against the rule, such as recalculating the expected total from AC1.

</details>

6. A model writes `"expected_total": "45.00"`. Why is that a problem, and how do you prevent it?

<details><summary>Answer</summary>

In quotes, 45.00 is a string, not a number, so comparing it with a calculated total fails. State the type in the prompt ("expected_total (number)") and add a type check in code, such as `isinstance(case["expected_total"], (int, float))`.

</details>

7. Why re-ask only once when the format breaks?

<details><summary>Answer</summary>

One re-ask with the exact error usually fixes the problem. If it does not, repeating the request wastes time and can hide a deeper problem, so a person should look at the reply.

</details>

---

## Glossary

- **Format locking:** fixing the exact shape of an AI's answer so code can read it.
- **JSON:** a text format for data made of lists `[...]` and objects `{...}`; strings use double quotes.
- **JSON list / object:** `[...]`, read in Python as a list / `{...}`, read in Python as a dict.
- **`json.loads`:** a Python function that turns JSON text into Python data.
- **`JSONDecodeError`:** the error `json.loads` raises when text is not valid JSON.
- **Format drift:** when a reply moves away from the requested format.
- **Markdown fences:** the ```` ``` ```` lines that wrap code blocks in Markdown.
- **Defensive parsing:** reading a reply without assuming it is clean, and failing with a clear message when it is wrong.
- **Set difference:** `a - b`, the items in set `a` that are not in set `b`.
- **Shape check:** checking structure: types, counts and keys.
- **Meaning check:** checking values against the rule.
- **Structured Outputs:** a provider feature that constrains a reply to a JSON Schema.
- **Re-ask:** sending the model its error and asking for a corrected reply.
- **Fixed set of values:** a field that may only take listed values, such as High, Medium or Low.
- **Contract:** a written agreement about exactly what an AI's input and output must contain (covered on Thursday).
- **`snake_case`:** a naming style using lower-case words joined by underscores, such as `expected_total`.

---

## Summary

- **Lock the format whenever code will read the answer.** Pick a table for people, JSON for code, or a fixed line for quick verdicts.
- **Lock it with precise words:** name the container and every field with its type, show one example, give an exact count, and forbid extra text.
- **Drift is normal:** chatty wrappers, fences, renamed fields, wrong counts and wrong types.
- **Parse defensively:** extract what you need, parse it, check it, and fail loudly with a clear message.
- **Check meaning as well as shape.** A reply can have perfect structure and a wrong value.
- **Re-ask once with the exact error**; if that fails, look at the reply yourself.

---

## Additional Resources

- Python documentation, *json — JSON encoder and decoder*: https://docs.python.org/3/library/json.html
- OpenAI, *Structured model outputs* guide: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API* (including showing the output format with examples): https://help.openai.com/en/articles/6654000
