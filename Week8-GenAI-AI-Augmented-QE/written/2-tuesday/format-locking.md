# Format Locking

## Learning Objectives

By the end of this lesson you will be able to:

- Define **format locking** and explain why it is essential whenever an LLM's output is read by **code** rather than only by a person.
- Choose an appropriate output format (JSON, Markdown table, CSV, Gherkin, code-only block, numbered list) for a given QE task.
- Apply the main **format-locking techniques**: explicit format instructions, "only X, no prose" rules, skeletons, exact field names with types and allowed values, delimiters, a single shape example, low temperature, response prefilling and provider structured-output features.
- Recognise the most common kinds of **format drift** (code fences, chatty preambles, single quotes, trailing commas, missing or extra keys, wrong types, truncation) and explain why each one breaks a parser.
- Write **defensive parsing** code in Python that strips fences, extracts the JSON block, parses safely, and checks required keys, types and allowed values.
- Implement a simple **"re-ask once with the error"** pattern.
- Build an end-to-end example that turns a format-locked LLM response into a **pytest parametrized test** for the `apply_coupon` function.

---

## Why This Matters

Yesterday you saw many ways Generative AI can support quality engineering. In almost every one of them, there is a moment where the AI's answer stops being something you **read** and becomes something your tools **consume**:

- A list of test cases that should become rows in `@pytest.mark.parametrize`.
- A set of test data records that should be loaded into a database or posted to an API (Week 7).
- A bug summary that should be pushed into a Jira ticket's fields (Week 3).
- A Gherkin feature that should be saved as a `.feature` file and run by a BDD framework (Week 6).
- A list of risks that a CI pipeline step should count and compare against a threshold.

A human reader is forgiving. If the model writes "Sure! Here are your test cases:" before the list, you skip the greeting without thinking. A JSON parser is not forgiving. One friendly sentence, one stray comma or one missing field, and `json.loads` raises an exception, your pipeline step fails and nobody gets the test cases.

**Format locking** is the discipline of telling the model *exactly* what shape its answer must take, and then **checking** that it did. It is the bridge between "an AI said something useful" and "an automated QE workflow used it reliably."

This connects directly to the Weekly Epic. By Friday you will build your first QA agent, and an agent is only as reliable as the structure of what it produces. On **Thursday** you will formalise output structures as input/output contracts using **JSON Schema**, and on **Friday** you will write **validation scripts** that enforce them. Today you learn the foundation those days build on: how to ask for a structure in a prompt, what goes wrong, and how to parse the result safely with plain Python.

For **Project 2 (Test Automation Framework)**, imagine you want an assistant to propose test cases for the e-commerce checkout. If the answer comes back as a predictable JSON array, you can turn it into runnable pytest tests in a few lines of code, as you will do at the end of this lesson.

---

## The Concept

### 1. What Is Format Locking?

**Format locking** means constraining a language model's response to an **exact, predictable structure** so that it can be processed by a program without manual clean-up.

Recall from Monday that an LLM generates text **one token at a time**, choosing each next token based on probabilities. Nothing in that mechanism *guarantees* a particular structure. The model has learned that JSON usually looks a certain way, so when you ask for JSON it usually produces it, but "usually" is not "always." Format locking is about pushing that probability as close to "always" as you can, and then catching the cases where it still slips.

A helpful analogy is a **paper form versus a blank sheet of paper**. If you ask a customer to "write down your delivery details" on a blank sheet, you will get many layouts: some put the postcode first, some forget the phone number, some add a note about the dog. If you hand them a form with labelled boxes ("Name", "Street", "Postcode", "Phone"), the answers come back in the same place every time, and a clerk (or a scanner) can process them quickly. Format locking turns a blank sheet into a form.

There are two halves to format locking, and you need both:

| Half | Where it happens | Purpose |
|------|------------------|---------|
| **Requesting** the format | In the prompt (and sometimes in API settings) | Make the correct structure the most likely output |
| **Enforcing** the format | In your code, after the response arrives | Detect and handle responses that still do not match |

A common beginner mistake is to do only the first half: write "return JSON" in the prompt and then call `json.loads` directly on the reply. That works in a demo and fails in a pipeline at 2 a.m. A good QE engineer treats the model's output like any other **untrusted input** to a system: you validate it before you rely on it. That is exactly the mindset you used in Week 7 when you validated API responses instead of assuming the server returned what the documentation promised.

### 2. Free Text Versus Locked Output: A First Example

Suppose you ask an assistant, with no format instructions:

> Give me some test cases for a coupon function where SAVE10 gives 10% off orders of $50 or more.

A typical answer might look like this:

```text
Great question! Here are some test cases you might consider:

1. Test with an order of exactly $50 - the discount should apply, giving $45.
2. Try $49.99 - no discount expected.
3. You could also test invalid codes, which should probably raise an error.

Let me know if you'd like me to write these as pytest tests!
```

For a person, this is fine. For code, it is a problem:

- Where does each test case start and end? (By number? By line?)
- Which part is the input total and which is the expected result? ("an order of exactly $50" must be turned into `50`.)
- Case 3 has no specific input at all.
- There are greetings and offers to help mixed in with the data.

Now compare a locked version of the same answer:

```json
[
  {"id": "TC-01", "title": "Total exactly at $50 threshold", "input_total": 50.0, "code": "SAVE10", "expected": 45.0, "technique": "BVA"},
  {"id": "TC-02", "title": "Total one cent below threshold", "input_total": 49.99, "code": "SAVE10", "expected": 49.99, "technique": "BVA"},
  {"id": "TC-03", "title": "Unknown coupon code is rejected", "input_total": 80.0, "code": "BOGUS", "expected": "ValueError", "technique": "error_guessing"}
]
```

Every case has the same fields, every value has a clear type, and there is nothing else in the response. One call to `json.loads` turns this into a Python list of dictionaries. That is the goal.

### 3. Choosing the Right Format

There is no single "best" format. Choose the one that matches **who or what will consume the output**.

| Format | Best for | Consumed by | Strengths | Watch out for |
|--------|----------|-------------|-----------|---------------|
| **JSON** (object or array) | Test cases, test data, bug fields, any nested structure | Python code, APIs, CI steps | Typed values (numbers, strings, booleans, lists), nesting, universal parser support | Very strict syntax: one stray comma breaks it |
| **Markdown table** | Test case lists for human review, coverage matrices | People (in chat, Jira, Confluence, pull requests) | Easy to read, renders nicely | Hard to parse reliably; pipes (`|`) inside cell text break columns |
| **CSV** | Flat tabular test data, data-driven tests (Week 7 CSV parametrization) | Spreadsheets, `csv` module, data loaders | Compact, opens in Excel, simple | No types (everything is text), commas inside values need quoting, no nesting |
| **Gherkin** | Acceptance scenarios (Week 6) | BDD frameworks (Cucumber, pytest-bdd), product owners | Business-readable and executable | Keywords must be exact (`Given`, `When`, `Then`, `Scenario Outline`, `Examples`) |
| **Code-only block** | A pytest test, a Playwright snippet, a helper function | A Python file, the test runner | Can be saved and executed directly | Model may add explanations or multiple files; code still needs review and running |
| **Numbered list** | Quick brainstorming, checklists | People, simple line-based scripts | Very low effort for the model to follow | Weak structure: each line is still free text |

A practical rule of thumb:

- If **code** reads it, prefer **JSON** (or CSV for simple flat data).
- If a **person** reads it, prefer a **Markdown table** or **numbered list**.
- If a **tool with its own syntax** reads it (BDD runner, test runner), lock to **that tool's syntax** (Gherkin, Python code).

You can also combine them. A common pattern is to ask for JSON (for your code) and then generate the Markdown table yourself from the parsed JSON (for people). That way the model only has to get one strict format right, and the human-friendly view is produced deterministically by your code.

### 4. Format-Locking Techniques

The following techniques stack: each one makes the correct format more likely, and in practice you will combine several in a single prompt.

#### 4.1 Give an explicit format instruction

State the format by name and early in the prompt, not as an afterthought at the end of a long paragraph.

Weak:

> ...and it would be nice if you could maybe put it in JSON.

Strong:

> OUTPUT FORMAT: Return a JSON array of objects.

Words like "maybe" and "it would be nice" signal that the format is optional. A heading such as `OUTPUT FORMAT` signals that it is a requirement. Some teams write the format section in capitals or as a separate block so it stands out from the task description.

#### 4.2 Forbid everything else: "only X, no prose"

Chat-tuned models are trained to be friendly, so they like to add an introduction ("Here are your test cases") and an outro ("Let me know if you need more!"). You must explicitly forbid this:

> Return ONLY the JSON array. Do not add any text before or after it. Do not wrap it in Markdown code fences.

Notice that the instruction names the specific unwanted behaviours (text before, text after, code fences). Naming the exact behaviour you do not want is more effective than a vague "be concise."

#### 4.3 Provide a skeleton or template to fill

A **skeleton** is the empty shape of the answer. It works like the paper form from the analogy:

```text
Fill in this template exactly. Replace each <...> with a value. Keep the labels.

ID: <TC-NN>
Title: <short title>
Input total: <number>
Code: <coupon code>
Expected: <number or ValueError>
```

Skeletons are especially useful for **semi-structured** text such as bug reports, where you want fixed headings ("Steps to reproduce", "Expected result", "Actual result") but free text inside each one.

#### 4.4 Name the exact fields, their types and their allowed values

The model cannot read your mind about field names. If you say "include the input and expected output," you might get `input`, `inputTotal`, `total`, `order_total` or `amount` on different runs. Your code expects exactly one of them. So spell it out, in plain words:

```text
Each object has exactly these keys:
  "id": string, "TC-" followed by two digits, e.g. "TC-01"
  "input_total": number (not a string), e.g. 49.99
  "expected": number for a returned total, OR the string "ValueError" if the call must raise
  "technique": one of "BVA", "EP", "error_guessing"
```

Three details matter here:

1. **Exact key names**, in quotes, with consistent naming style (all `snake_case` in this example).
2. **Types**, including the common trap: "number (not a string)". Without that, models often write `"49.99"` (a string) instead of `49.99` (a number).
3. **Allowed values** for fields that act like categories (an **enumeration**, or "enum"). If you allow free text, you will get "boundary value analysis", "Boundary", "BVA", "boundary testing" and so on, and your code cannot group them.

This plain-language field list is the informal ancestor of a JSON Schema. On **Thursday** you will learn to express the same rules formally with JSON Schema as part of an agent's input/output contract.

#### 4.5 Use delimiters around inputs and outputs

**Delimiters** are markers that show where one piece of content starts and ends. Common choices are XML-style tags (`<function> ... </function>`), triple quotes (`"""`), or headings.

Delimiters help in two directions:

- **Around the input** you paste in (a requirement, a function, a log), so the model does not confuse your material with your instructions. You will see `<function>` tags in the full example in Section 8.
- **Around the output**, so your code can find the answer even if the model adds chatter. For example: "Put the JSON between `<result>` and `</result>` tags." Your code then extracts only what is between the tags.

The second use is a useful fallback: even if you cannot stop a model from adding a sentence before its answer, you can make the answer easy to cut out.

#### 4.6 Show one example of the output shape

A single, concrete example of one element is often clearer than a paragraph of description:

```text
Shape of one element (values are placeholders, do not copy them):
{"id": "TC-00", "title": "...", "input_total": 0.0, "code": "...", "expected": 0.0, "technique": "EP"}
```

Two cautions:

- Label it clearly as a **shape** example and use obvious placeholder values ("TC-00", "...", `0.0`). Otherwise the model may copy your example values into its real answer.
- Showing several worked examples to teach a style or a decision rule is a technique of its own, called **few-shot prompting**. It has its own lesson today; here we only use one example to pin down the *shape*.

#### 4.7 Lower the temperature

On Monday you learned that **temperature** controls how random the next-token choice is. Higher temperature means more variety; lower temperature means the model sticks more closely to the most probable tokens.

For format-locked tasks, you usually want **low temperature** (for example 0 to 0.3), because creativity in *structure* is never helpful. Low temperature does not guarantee a valid format, and it does not make the content correct, but it reduces random deviations such as a renamed key or a surprise extra sentence. If you need *varied content* (for example many different test data names) you can still ask for variety in the instructions while keeping the temperature low enough that the structure stays stable.

#### 4.8 Start the response for the model (prefilling)

Some LLM APIs let you supply the **beginning of the assistant's reply**, and the model continues from there. This is called **prefilling** the response. If you prefill with `[` or `{`, the model is strongly steered to continue with JSON rather than with "Sure! Here are...".

This is a **provider-specific feature**, and support changes between providers and model versions. For example, Anthropic's documentation notes that prefilling is not supported on its newer Claude models and recommends structured outputs or system-prompt instructions instead. Treat prefilling as a tool you check for in your provider's current documentation, not something you can assume.

#### 4.9 Use the provider's JSON mode or structured outputs

Most major LLM APIs now offer a setting that constrains output at the **generation** level rather than only through the wording of the prompt:

- **JSON mode** (offered by several providers) ensures the response is **syntactically valid JSON**, but does not promise which keys it contains.
- **Structured outputs** go further: you supply a description of the required structure (a schema), and the service constrains generation so the response **matches that structure**. OpenAI's documentation describes structured outputs as the evolution of JSON mode, and Anthropic offers a similar structured outputs feature.

These features are powerful and you should use them when your provider supports them. But they do **not** replace the rest of this lesson:

- They make the **shape** reliable, not the **content**. A perfectly structured test case can still have the wrong expected value.
- Not every tool you use (chat interfaces, IDE assistants, some local models) exposes them.
- Your code should still parse defensively, because network errors, truncation and configuration mistakes still happen.

The schemas these features use are written in **JSON Schema**, which you will study on **Thursday**. For today, it is enough to know the features exist and what they guarantee.

#### 4.10 Putting the techniques together

Here is a quick checklist you can apply to any format-locked prompt:

| Technique | Question to ask yourself |
|-----------|--------------------------|
| Explicit format | Did I name the format clearly and early? |
| Only X | Did I forbid preambles, outros and code fences? |
| Skeleton | Would a fill-in template make this clearer? |
| Fields | Did I list every key with its type and allowed values? |
| Delimiters | Are my inputs (and optionally outputs) clearly marked? |
| Shape example | Did I show one placeholder element? |
| Temperature | Is the temperature low for this structural task? |
| Provider features | Can I use JSON mode, structured outputs or prefilling here? |
| Enforcement | Does my code validate the response before using it? |

### 5. Format Drift: How Locked Output Still Goes Wrong

**Format drift** is any deviation of the model's output from the format you requested. Even with good prompts it happens, especially over long responses, with higher temperatures, with smaller models, or when the prompt is long and the format instruction is buried.

Here are the most common forms, each with an example and why it breaks a parser.

| Drift type | Example output | Why it breaks |
|------------|----------------|---------------|
| **Code fences** | ` ```json\n{"id": "TC-01"}\n``` ` | The backticks are not JSON. The parser fails on the first character. |
| **Chatty preamble/outro** | `Sure! Here it is:\n{"id": "TC-01"}\nHope this helps.` | Text before the `{` is not JSON. |
| **Single quotes** | `{'id': 'TC-01'}` | JSON requires double quotes. This looks like a Python dict, not JSON. |
| **Trailing comma** | `{"id": "TC-01", "expected": 45.0,}` | JSON forbids a comma after the last item (Python allows it, which is why models slip). |
| **Missing key** | `{"id": "TC-01", "title": "..."}` (no `expected`) | Parses fine, but your code crashes later with `KeyError`. |
| **Extra key** | `..., "priority": "high"}` | Parses fine, but may indicate the model ignored your field list; can confuse downstream tools. |
| **Renamed key** | `"inputTotal"` instead of `"input_total"` | Parses fine, but your code cannot find the field. |
| **Wrong type** | `"input_total": "50"` instead of `50` | Parses fine, but `"50" >= 50` raises `TypeError` in Python, and `"50" == 50` is `False`. |
| **Out-of-range value** | `"technique": "boundary"` instead of `"BVA"` | Parses fine, but breaks grouping and reporting. |
| **Truncation** | `{"id": "TC-01", "expec` | The response hit the model's maximum output length and was cut off mid-token. |

Notice the two families:

1. **Syntax drift** (fences, chatter, quotes, commas, truncation) makes `json.loads` fail immediately. This is noisy, so you will notice it.
2. **Structure drift** (missing, extra, renamed keys; wrong types; values outside the allowed list) **parses successfully** and fails later, or worse, does not fail at all and silently produces wrong tests. This is the more dangerous family, and it is why you must check more than "did it parse?"

Truncation deserves a special note. On Monday you learned about the **context window** and output token limits. If you ask for 200 test cases in one response, the model may simply run out of output tokens and stop mid-object. The fix is usually to ask for fewer items per request (for example batches of 10 to 20) rather than to fight the parser.

#### Seeing syntax drift in Python

Let's prove that `json.loads` rejects these variants. Save this as `drift.py`:

```python
import json

responses = {
    "clean": '{"id": "TC-01", "expected": 45.0}',
    "fenced": '```json\n{"id": "TC-01", "expected": 45.0}\n```',
    "chatty": 'Sure! Here is the test case:\n{"id": "TC-01", "expected": 45.0}\nLet me know if you need more.',
    "single_quotes": "{'id': 'TC-01', 'expected': 45.0}",
    "trailing_comma": '{"id": "TC-01", "expected": 45.0,}',
    "truncated": '{"id": "TC-01", "expec',
}

for name, text in responses.items():
    try:
        data = json.loads(text)
        print(f"{name:15} OK    -> {data}")
    except json.JSONDecodeError as err:
        print(f"{name:15} FAIL  -> {err.msg}")
```

Output (Python 3.13):

```text
clean           OK    -> {'id': 'TC-01', 'expected': 45.0}
fenced          FAIL  -> Expecting value
chatty          FAIL  -> Expecting value
single_quotes   FAIL  -> Expecting property name enclosed in double quotes
trailing_comma  FAIL  -> Illegal trailing comma before end of object
truncated       FAIL  -> Unterminated string starting at
```

How the code works:

- `responses` is a dictionary mapping a **label** to a **simulated model reply**. Each reply is a Python string containing what the model might return.
- `json.loads(text)` ("load string") parses a JSON string into Python objects: JSON objects become `dict`, arrays become `list`, numbers become `int` or `float`, and so on.
- When the text is not valid JSON, `json.loads` raises `json.JSONDecodeError`. This exception class is a subclass of `ValueError` and carries useful attributes: `msg` (the reason), `lineno` and `colno` (where it failed).
- `f"{name:15}"` pads the label to 15 characters so the output lines up in columns.

Only the clean version parses. Note that the exact wording of error messages can differ between Python versions (older versions report the trailing comma as "Expecting property name enclosed in double quotes"), so never write code that depends on the precise message text.

### 6. Defensive Parsing in Python

Since drift will happen, your code should be **defensive**: tolerate harmless wrapping (fences, chatter) and fail **clearly** on real problems.

A sensible order of operations is:

1. **Strip** surrounding whitespace.
2. **Remove code fences** if present.
3. **Extract** the JSON block: from the first `{` or `[` to the last matching `}` or `]`.
4. **Parse** with `json.loads` inside `try/except`.
5. **Check structure**: required keys, types and allowed values.
6. If anything fails, **report a readable error** (and optionally re-ask the model, Section 7).

What you should **not** do is "repair" real syntax errors silently, for example by regex-replacing single quotes with double quotes. That can corrupt text such as `"title": "Customer's cart"` and hides the fact that the model is not following instructions. Tolerate *wrapping*; reject *broken content*.

#### 6.1 Extracting and parsing the JSON block

Save as `parser.py`:

```python
import json
import re

def extract_json_block(text):
    """Return the most likely JSON substring from an LLM response."""
    text = text.strip()

    # 1. If the model wrapped the answer in a ``` code fence, keep only the inside.
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    # 2. Find the first opening bracket and the last matching closing bracket.
    starts = [i for i in (text.find("{"), text.find("[")) if i != -1]
    if not starts:
        raise ValueError("No JSON object or array found in the response")
    start = min(starts)
    closer = "}" if text[start] == "{" else "]"
    end = text.rfind(closer)
    if end == -1:
        raise ValueError("JSON block is not closed (response may be truncated)")
    return text[start:end + 1]

def parse_llm_json(text):
    """Extract and parse JSON; raise ValueError with a readable message on failure."""
    block = extract_json_block(text)
    try:
        return json.loads(block)
    except json.JSONDecodeError as err:
        raise ValueError(f"Invalid JSON at line {err.lineno}, column {err.colno}: {err.msg}") from err

samples = [
    '```json\n{"id": "TC-01", "expected": 45.0}\n```',
    'Sure! Here is the test case:\n{"id": "TC-01", "expected": 45.0}\nHope this helps.',
    '{"id": "TC-01", "expected": 45.0,}',
    '{"id": "TC-01", "expec',
]
for s in samples:
    try:
        print("parsed:", parse_llm_json(s))
    except ValueError as err:
        print("error: ", err)
```

Output:

```text
parsed: {'id': 'TC-01', 'expected': 45.0}
parsed: {'id': 'TC-01', 'expected': 45.0}
error:  Invalid JSON at line 1, column 33: Illegal trailing comma before end of object
error:  JSON block is not closed (response may be truncated)
```

Line by line:

- `import re` brings in Python's **regular expression** module (from Week 1-2 string handling). We use it only to find code fences.
- `re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)` looks for three backticks, optionally followed by the word `json`, then any whitespace, then captures everything (`(.*?)`) up to the next three backticks.
  - `(?:json)?` is a **non-capturing optional group**: "the word json may or may not be here."
  - `.*?` is a **lazy** match: it stops at the *first* closing fence rather than the last.
  - `re.DOTALL` lets `.` match newline characters, which is necessary because the JSON spans several lines.
  - `fence.group(1)` returns the captured inside of the fence.
- `text.find("{")` and `text.find("[")` return the index of the first `{` and `[`, or `-1` if not found. The list comprehension keeps only the ones that were found, and `min(starts)` picks whichever comes first. That decides whether we are extracting an **object** or an **array**.
- `text.rfind(closer)` searches from the **right** for the last `}` or `]`. Slicing `text[start:end + 1]` returns everything between them, inclusive. Chatter before and after is dropped.
- If there is an opening bracket but no closing one, the response was almost certainly **truncated**, so we raise a clear `ValueError` saying so.
- In `parse_llm_json`, `json.loads(block)` is wrapped in `try/except json.JSONDecodeError`. We convert the low-level error into a `ValueError` with a human-readable message including line and column. `raise ... from err` keeps the original exception attached, which helps debugging.

Results: the fenced and chatty responses are **rescued** (harmless wrapping), while the trailing comma and truncation are **reported clearly** (real problems). This is the balance you want.

This extractor is deliberately simple. It assumes the response contains one JSON block. It is good enough for learning and for many practical scripts; on **Friday** you will build more complete validation scripts around agent output.

#### 6.2 Checking required keys, types and allowed values

Parsing proves the text is JSON. It does not prove the JSON has the **structure** you asked for. Save as `checks.py`:

```python
REQUIRED_FIELDS = {
    "id": str,
    "title": str,
    "input_total": (int, float),
    "code": str,
    "expected": (int, float, str),
    "technique": str,
}
ALLOWED_TECHNIQUES = {"BVA", "EP", "error_guessing"}

def check_test_case(case):
    """Return a list of problems found in one test-case dictionary (empty list = OK)."""
    problems = []
    if not isinstance(case, dict):
        return [f"expected an object, got {type(case).__name__}"]

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in case:
            problems.append(f"missing field '{field}'")
        elif isinstance(case[field], bool) or not isinstance(case[field], expected_type):
            problems.append(f"field '{field}' has wrong type {type(case[field]).__name__}")

    extra = set(case) - set(REQUIRED_FIELDS)
    if extra:
        problems.append(f"unexpected field(s): {sorted(extra)}")

    if case.get("technique") not in ALLOWED_TECHNIQUES:
        problems.append(f"technique '{case.get('technique')}' not in {sorted(ALLOWED_TECHNIQUES)}")
    return problems

good = {"id": "TC-01", "title": "Exactly 50", "input_total": 50,
        "code": "SAVE10", "expected": 45.0, "technique": "BVA"}
bad = {"id": "TC-02", "title": "Just below", "input_total": "49.99",
       "code": "SAVE10", "technique": "boundary", "priority": "high"}

print("good:", check_test_case(good))
print("bad: ")
for p in check_test_case(bad):
    print("  -", p)
```

Output:

```text
good: []
bad: 
  - field 'input_total' has wrong type str
  - missing field 'expected'
  - unexpected field(s): ['priority']
  - technique 'boundary' not in ['BVA', 'EP', 'error_guessing']
```

How it works:

- `REQUIRED_FIELDS` is a dictionary from **field name** to **allowed Python type(s)**. A tuple such as `(int, float)` means "either of these." JSON numbers like `50` become `int` and `49.99` becomes `float`, so we accept both.
- `isinstance(value, expected_type)` checks a value's type. It accepts a single type or a tuple of types.
- `isinstance(case[field], bool)` is a subtle guard: in Python, `bool` is a subclass of `int`, so `isinstance(True, int)` is `True`. Without this check, a model that wrote `"input_total": true` would pass the number check.
- `set(case) - set(REQUIRED_FIELDS)` uses **set difference** to find keys the model added that we did not ask for.
- `case.get("technique")` returns `None` instead of raising `KeyError` if the key is missing, so the allowed-values check is safe even on incomplete objects.
- The function **collects all problems** into a list instead of stopping at the first. When you show this list to a person (or feed it back to the model), they can fix everything in one pass.

You are writing these rules by hand today, in plain Python, so that you understand exactly what is being checked. On **Thursday** you will see how JSON Schema lets you declare the same kinds of rules (required fields, types, allowed values) in a standard, reusable way.

#### 6.3 Parsing CSV output

If you lock the format to CSV instead, use Python's built-in `csv` module rather than splitting on commas yourself. Save as `csvparse.py`:

```python
import csv
import io

llm_output = """id,title,input_total,code,expected
TC-01,Exactly at threshold,50.00,SAVE10,45.00
TC-02,"Below threshold, no discount",49.99,SAVE10,49.99
TC-03,Unknown code,80.00,BOGUS,ValueError
"""

reader = csv.DictReader(io.StringIO(llm_output))
expected_header = ["id", "title", "input_total", "code", "expected"]
if reader.fieldnames != expected_header:
    raise ValueError(f"Unexpected header: {reader.fieldnames}")

for row in reader:
    total = float(row["input_total"])
    print(row["id"], "|", row["title"], "|", total, "|", row["code"], "|", row["expected"])
```

Output:

```text
TC-01 | Exactly at threshold | 50.0 | SAVE10 | 45.00
TC-02 | Below threshold, no discount | 49.99 | SAVE10 | 49.99
TC-03 | Unknown code | 80.0 | BOGUS | ValueError
```

Key points:

- `io.StringIO(llm_output)` wraps a string so it behaves like a file. `csv` readers expect a file-like object.
- `csv.DictReader` uses the first line as the **header** and returns each following row as a dictionary keyed by column name.
- Checking `reader.fieldnames` against the expected header catches **renamed or reordered columns** before you process any rows.
- Row TC-02's title contains a comma. Because the model wrapped it in double quotes, `csv` handles it correctly. A naive `line.split(",")` would have produced six columns and misaligned everything. If you lock to CSV, include "wrap any value containing a comma in double quotes" in your format instructions.
- Every CSV value is a **string**. `float(row["input_total"])` converts explicitly. Notice `row["expected"]` is still the string `"45.00"`; your code must decide how to convert it (number or the literal `ValueError`). This lack of types is the main reason JSON is usually preferred for anything feeding code.

### 7. Re-Asking Once with the Error Message

Sometimes the best fix for a malformed response is to **show the model its mistake** and ask again. Models are usually good at correcting a specific, clearly described error, for example "trailing comma at line 1, column 33."

The simple pattern is:

1. Send the prompt.
2. Try to parse the reply.
3. If parsing fails, send a follow-up message containing the **original reply** and the **exact error**, and ask for only the corrected output.
4. Try once more. If it fails again, **stop** and surface the error.

In the code below, `fake_llm` is a **stand-in** for a real LLM API call. It returns fixed responses so the example is repeatable and needs no API key. A real call would send the same `messages` list to a provider's API. Save as `reask.py`:

```python
import json

def fake_llm(messages):
    """Stand-in for a real LLM API call. Deterministic so the example is repeatable.
    First call: returns chatty, fenced output with a trailing comma.
    Any call that contains a correction message: returns clean JSON."""
    last = messages[-1]["content"]
    if "could not be parsed" in last:
        return '{"id": "TC-01", "title": "Exactly 50", "expected": 45.0}'
    return 'Here you go!\n```json\n{"id": "TC-01", "title": "Exactly 50", "expected": 45.0,}\n```'

def parse_json_strict(text):
    return json.loads(text.strip())

def ask_for_json(prompt):
    messages = [{"role": "user", "content": prompt}]
    reply = fake_llm(messages)
    try:
        return parse_json_strict(reply)
    except json.JSONDecodeError as err:
        print(f"Attempt 1 failed: {err.msg} (line {err.lineno}, column {err.colno})")
        # Re-ask ONCE: show the model its own reply and the exact error.
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": (
            f"Your previous reply could not be parsed as JSON: {err.msg} "
            f"at line {err.lineno}, column {err.colno}. "
            "Reply again with ONLY the corrected JSON object. "
            "No code fences, no explanation, no trailing commas."
        )})
        reply = fake_llm(messages)
        result = parse_json_strict(reply)   # if this fails too, let the error surface
        print("Attempt 2 succeeded")
        return result

prompt = ("Return ONE test case for apply_coupon as a JSON object with keys "
          "id, title, expected. Return only the JSON object.")
print(ask_for_json(prompt))
```

Output:

```text
Attempt 1 failed: Expecting value (line 1, column 1)
Attempt 2 succeeded
{'id': 'TC-01', 'title': 'Exactly 50', 'expected': 45.0}
```

What is happening:

- `messages` is a list of dictionaries, each with a `role` (`"user"` or `"assistant"`) and `content`. This is the conversation format most chat-based LLM APIs use. The prompt engineering principles lesson today explains message roles in more detail.
- On the first attempt the strict parser fails at line 1, column 1, because the reply starts with "Here you go!" rather than `{`.
- We append the model's **own bad reply** as an `assistant` message, then a `user` message containing the **exact error** and a short restatement of the rules. Including the bad reply matters: the model can see what it produced and what to change.
- The second attempt is parsed with no `try/except`. If it fails again, the exception propagates to the caller. This is deliberate: **retry once, then fail loudly**. Endless retries waste tokens, hide problems, and can loop forever.

This example uses the *strict* parser to make the re-ask visible. In practice you would combine the two ideas: first try the defensive parser from Section 6.1 (which would have rescued the fenced reply without any re-ask), and only re-ask for errors that the defensive parser cannot handle, such as the trailing comma, a missing key or a wrong type. The problem list from `check_test_case` makes an excellent correction message.

Re-asking once is a simple, practical pattern. Production systems need more careful handling (how many attempts, back-off between them, what to do after the last failure, logging). Those **retry strategies and agent error handling** are covered in **Week 9**.

### 8. End to End: From a Format-Locked Prompt to a pytest Parametrized Test

Now let's put everything together for the Project 2 running example. The function under test:

```python
# coupon.py
def apply_coupon(total, code):
    """Apply a coupon to an order total. SAVE10 = 10% off orders of $50 or more."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon code: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total
```

#### 8.1 The format-locked prompt

Save as `build_prompt.py`:

```python
FUNCTION_UNDER_TEST = '''def apply_coupon(total, code):
    """SAVE10 gives 10% off orders of $50 or more. Unknown codes raise ValueError."""'''

PROMPT = f"""You are a QA engineer designing unit tests.

Design 5 test cases for the Python function below.

<function>
{FUNCTION_UNDER_TEST}
</function>

OUTPUT FORMAT (follow exactly):
- Return ONLY a JSON array. No prose before or after it. No Markdown code fences.
- Each element is an object with exactly these 6 keys, in this order:
  "id": string, pattern "TC-" followed by two digits, e.g. "TC-01"
  "title": string, under 60 characters
  "input_total": number (not a string), e.g. 49.99
  "code": string, the coupon code passed to the function
  "expected": number for a returned total, OR the string "ValueError" if the call must raise
  "technique": one of "BVA", "EP", "error_guessing"
- Use double quotes. No trailing commas. No comments.

Shape of one element (values are placeholders, do not copy them):
{{"id": "TC-00", "title": "...", "input_total": 0.0, "code": "...", "expected": 0.0, "technique": "EP"}}
"""

if __name__ == "__main__":
    print(PROMPT)
```

Running it prints the prompt you would send:

```text
You are a QA engineer designing unit tests.

Design 5 test cases for the Python function below.

<function>
def apply_coupon(total, code):
    """SAVE10 gives 10% off orders of $50 or more. Unknown codes raise ValueError."""
</function>

OUTPUT FORMAT (follow exactly):
- Return ONLY a JSON array. No prose before or after it. No Markdown code fences.
- Each element is an object with exactly these 6 keys, in this order:
  "id": string, pattern "TC-" followed by two digits, e.g. "TC-01"
  "title": string, under 60 characters
  "input_total": number (not a string), e.g. 49.99
  "code": string, the coupon code passed to the function
  "expected": number for a returned total, OR the string "ValueError" if the call must raise
  "technique": one of "BVA", "EP", "error_guessing"
- Use double quotes. No trailing commas. No comments.

Shape of one element (values are placeholders, do not copy them):
{"id": "TC-00", "title": "...", "input_total": 0.0, "code": "...", "expected": 0.0, "technique": "EP"}
```

Map each part to a technique from Section 4:

| Prompt part | Technique |
|-------------|-----------|
| `OUTPUT FORMAT (follow exactly):` | Explicit format instruction (4.1) |
| `Return ONLY a JSON array. No prose... No Markdown code fences.` | Only X, no prose (4.2) |
| The six key lines | Exact fields, types, allowed values (4.4) |
| `<function> ... </function>` | Delimiters around input (4.5) |
| `Shape of one element...` | One shape example with placeholders (4.6) |

Two Python details:

- The prompt is an **f-string** (`f"""..."""`) so `{FUNCTION_UNDER_TEST}` is replaced by the function text. Because f-strings treat `{` and `}` as placeholders, the literal braces in the JSON shape example are **doubled** (`{{` and `}}`). Python prints them as single braces. Forgetting this is a very common bug when building JSON-format prompts with f-strings.
- The `"expected"` field has a **union** type: a number, or the special string `"ValueError"`. This is how we represent "this call should raise" in a data format that has no concept of exceptions.

#### 8.2 The model's response

Imagine the model replied with the following (saved as `fake_llm_response.txt`). This is a **stand-in** response written for the lesson; note that it **still** wrapped the answer in a code fence despite being told not to, which is realistic:

````text
```json
[
  {"id": "TC-01", "title": "Total exactly at $50 threshold", "input_total": 50.00, "code": "SAVE10", "expected": 45.0, "technique": "BVA"},
  {"id": "TC-02", "title": "Total one cent below threshold", "input_total": 49.99, "code": "SAVE10", "expected": 49.99, "technique": "BVA"},
  {"id": "TC-03", "title": "Total one cent above threshold", "input_total": 50.01, "code": "SAVE10", "expected": 45.01, "technique": "BVA"},
  {"id": "TC-04", "title": "Typical large order", "input_total": 120.00, "code": "SAVE10", "expected": 108.0, "technique": "EP"},
  {"id": "TC-05", "title": "Unknown coupon code is rejected", "input_total": 80.00, "code": "BOGUS", "expected": "ValueError", "technique": "error_guessing"}
]
```
````

#### 8.3 Loading and checking the cases

Save as `load_cases.py`:

```python
import json
import re
from pathlib import Path

REQUIRED = ["id", "title", "input_total", "code", "expected", "technique"]
TECHNIQUES = {"BVA", "EP", "error_guessing"}

def load_cases(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    cases = json.loads(text)
    if not isinstance(cases, list):
        raise ValueError("Top level must be a JSON array")
    for case in cases:
        missing = [k for k in REQUIRED if k not in case]
        if missing:
            raise ValueError(f"{case.get('id', '?')}: missing {missing}")
        if not isinstance(case["input_total"], (int, float)):
            raise ValueError(f"{case['id']}: input_total must be a number")
        if case["technique"] not in TECHNIQUES:
            raise ValueError(f"{case['id']}: bad technique {case['technique']!r}")
    return cases

def to_params(cases):
    """Convert dicts into the tuple list pytest.mark.parametrize expects."""
    return [(c["input_total"], c["code"], c["expected"]) for c in cases], [c["id"] for c in cases]
```

- `Path(path).read_text(encoding="utf-8")` reads the whole file as a string (from `pathlib`, Week 1-2).
- The fence-stripping is the same technique as Section 6.1. Because of it, the fenced response from 8.2 still loads.
- After `json.loads`, we check the **top-level type** (must be a list) and then each case's required keys, number type and allowed technique, failing fast with a message naming the case `id`.
- `to_params` returns **two lists**: the parameter tuples `(total, code, expected)` and the matching `ids`. pytest uses the ids to label each generated test, which makes reports readable.

#### 8.4 The parametrized test

Recall `@pytest.mark.parametrize` from Week 4: it runs the same test function once per row of data. Save as `test_coupon_generated.py`:

```python
import pytest
from coupon import apply_coupon
from load_cases import load_cases, to_params

CASES = load_cases("fake_llm_response.txt")
PARAMS, IDS = to_params(CASES)

@pytest.mark.parametrize("total, code, expected", PARAMS, ids=IDS)
def test_apply_coupon(total, code, expected):
    if expected == "ValueError":
        with pytest.raises(ValueError):
            apply_coupon(total, code)
    else:
        assert apply_coupon(total, code) == pytest.approx(expected)
```

Run it with `python -m pytest -v`:

```text
test_coupon_generated.py::test_apply_coupon[TC-01] PASSED                [ 20%]
test_coupon_generated.py::test_apply_coupon[TC-02] PASSED                [ 40%]
test_coupon_generated.py::test_apply_coupon[TC-03] PASSED                [ 60%]
test_coupon_generated.py::test_apply_coupon[TC-04] PASSED                [ 80%]
test_coupon_generated.py::test_apply_coupon[TC-05] PASSED                [100%]

============================== 5 passed in 0.02s ===============================
```

- `CASES = load_cases(...)` runs at **import time** (when pytest collects the file). If the AI output is malformed, collection fails immediately with your clear `ValueError` message, before any test runs. That is the behaviour you want: bad data should never silently become "0 tests ran."
- The test checks the special value `"ValueError"` and uses `pytest.raises` (Week 4 exception testing) for that case; otherwise it compares totals.
- `pytest.approx(expected)` compares floating-point numbers with a small tolerance, avoiding failures from tiny rounding differences such as `45.00000000000001`.
- The test ids `TC-01` to `TC-05` come straight from the AI output, so a failing case in a CI report points back to the exact generated row.

#### 8.5 What format locking did and did not give you

Format locking turned the AI's answer into **runnable tests with almost no manual work**. That is a big win. But remember what it does **not** guarantee:

- **Correctness of content.** If the model had written `"expected": 50.0` for TC-01, the format would still be perfect and the test would fail (or, worse, if the code were also wrong, pass). The structure check cannot know the business rule.
- **Coverage.** Five well-formatted cases might all test the same partition. Whether the *set* of tests is good is a test design question, covered in today's lesson on AI-assisted test design.
- **Trust.** A green test run proves the tests and the code agree, not that either matches the requirement.

Reviewing AI-generated test cases and validating AI output with a human checklist are covered in depth on **Wednesday**. Format locking makes that review faster, because every case has the same fields in the same place, but it does not replace it.

### 9. Format Locking Beyond JSON

The same ideas apply to other formats. Two short examples:

**Gherkin (Week 6).** Lock the keywords and structure:

```text
OUTPUT FORMAT:
- Return ONLY a valid Gherkin feature file. No explanations, no code fences.
- Start with "Feature: Coupon codes at checkout".
- Use exactly one "Scenario Outline:" with an "Examples:" table.
- Use only the keywords Given, When, Then, And.
- Examples table columns, in this order: | total | code | result |
```

Your code can then check simple things before saving the `.feature` file: the first line starts with `Feature:`, the text contains `Scenario Outline:` and `Examples:`, and every line of the table has the same number of `|` characters.

**Code-only output.** When asking for test code:

```text
Return ONLY the contents of a single Python file named test_login.py.
No explanation before or after. No Markdown code fences.
Use pytest. Do not import any module other than pytest and app.auth.
```

The restrictions on imports are a form of format locking for code: they constrain the *shape* of the file so it fits your project. You will look at AI-generated code in more depth in today's lesson on AI-assisted coding and debugging.

---

## Practice Exercises

1. **Spot the drift.** For each response below, name the drift type and say whether `json.loads` would fail or whether the problem would only appear later:
   - a) `{"id": "TC-07", "input_total": "75", "code": "SAVE10", "expected": 67.5}`
   - b) `Here is the JSON you asked for: [{"id": "TC-08"}]`
   - c) `{"ID": "TC-09", "inputTotal": 75}`
   - d) `[{"id": "TC-10", "technique": "Boundary Value Analysis"}]`
2. **Lock a format.** Rewrite this vague prompt into a format-locked prompt that asks for **search** test cases for the Project 2 web app as a JSON array: *"Give me some tests for the product search box."* Decide on 5 fields, their types and at least one field with allowed values.
3. **Extend the checker.** Add two rules to `check_test_case` from Section 6.2: `id` must match the pattern `TC-` plus two digits (hint: `re.fullmatch(r"TC-\d{2}", value)`), and `title` must be under 60 characters. Test it with a good case and a bad case.
4. **CSV to JSON.** Take the CSV output from Section 6.3 and write code that converts it into the same list-of-dictionaries format used in Section 8, converting `input_total` to `float` and `expected` to `float` unless it is the literal `ValueError`.
5. **Re-ask with structure problems.** Modify `ask_for_json` from Section 7 so that, after a successful parse, it also runs `check_test_case` and, if there are problems, re-asks once with the list of problems in the correction message. Update `fake_llm` so you can see both paths.
6. **Project 2 connection.** Pick one feature of your Project 2 application (login, search, cart or checkout). Choose the most appropriate output format from Section 3 for (a) a list of test ideas you will review with your team and (b) data that will drive a parametrized test. Justify each choice in two sentences.

---

## Knowledge Check

1. What are the two halves of format locking, and why is doing only the first half risky?
2. Why is JSON usually preferred over CSV when the output feeds Python code?
3. Name three kinds of **syntax drift** and two kinds of **structure drift**. Which family is more dangerous, and why?
4. In an f-string prompt, why do the braces in a JSON shape example need to be doubled?
5. What does a provider's JSON mode guarantee, what do structured outputs add, and what does neither guarantee?
6. Why should a defensive parser strip code fences but **not** automatically replace single quotes with double quotes?
7. Why does the re-ask pattern in Section 7 stop after one retry?
8. Your format-locked test cases parse perfectly and all pass in pytest. Name two reasons this still does not prove the tests are good.

<details>
<summary>Answers</summary>

1. **Requesting** the format in the prompt (and API settings) and **enforcing** it in code after the response arrives. Requesting only makes the right format *likely*, not certain; without enforcement, a single malformed response crashes or silently corrupts the pipeline.
2. JSON carries **types** (numbers, strings, booleans, lists) and supports **nesting**, and Python's `json` module parses it directly into native objects. CSV values are all text, need manual conversion, have no nesting, and break easily on commas inside values.
3. Syntax drift: code fences, chatty preamble/outro, single quotes, trailing commas, truncation. Structure drift: missing keys, extra keys, renamed keys, wrong types (e.g. `"50"`), values outside the allowed list. **Structure drift** is more dangerous because the JSON parses successfully, so the problem surfaces later or not at all, possibly producing wrong tests silently.
4. In an f-string, `{` and `}` mark placeholders for Python expressions. To output a literal brace you write `{{` or `}}`; otherwise Python tries to evaluate the JSON text as an expression and raises an error.
5. JSON mode guarantees **syntactically valid JSON**. Structured outputs additionally guarantee the response **matches a supplied structure (schema)**. Neither guarantees the **content is correct** (for example, the right expected value).
6. Code fences are harmless **wrapping** around otherwise valid content, so removing them is safe. Replacing quotes changes the **content** itself and can corrupt values (for example apostrophes inside strings), while also hiding the fact that the model ignored instructions.
7. To avoid wasting tokens and time, avoid infinite loops, and make persistent failures **visible** so a person can investigate the prompt or the model. Fuller retry strategies are a Week 9 topic.
8. Any two of: the expected values might be wrong (format checks cannot know business rules); the tests and code might share the same mistake; the set of cases may miss important partitions or boundaries (coverage); the cases may not trace back to the actual requirement.

</details>

---

## Glossary

- **Format locking:** Constraining an LLM's response to an exact, predictable structure so a program can process it reliably.
- **Format drift:** Any deviation of the model's output from the requested format.
- **Syntax drift:** Drift that makes the output fail to parse (fences, chatter, quotes, trailing commas, truncation).
- **Structure drift:** Drift that parses successfully but has the wrong keys, types or values.
- **Delimiter:** A marker (such as `<function>...</function>` or triple quotes) that shows where a piece of content starts and ends.
- **Skeleton / template:** The empty shape of a desired answer, given to the model to fill in.
- **Enumeration (enum):** A fixed list of allowed values for a field, such as `"BVA"`, `"EP"`, `"error_guessing"`.
- **Defensive parsing:** Parsing code that tolerates harmless wrapping and fails clearly on real problems.
- **Prefilling:** Supplying the beginning of the assistant's reply so the model continues from it (provider-specific).
- **JSON mode:** A provider setting that ensures syntactically valid JSON output.
- **Structured outputs:** A provider feature that constrains output to match a supplied schema.
- **Truncation:** Output cut off because it reached the model's maximum output length.
- **`json.JSONDecodeError`:** The exception Python's `json` module raises for invalid JSON; it has `msg`, `lineno` and `colno` attributes.

---

## Summary

- **Format locking** turns an LLM's answer from something a person reads into something code can consume. It has two halves: **request** the format in the prompt, and **enforce** it in code.
- Choose the format by consumer: **JSON** for code, **Markdown tables or lists** for people, **Gherkin or code-only** for tools with their own syntax, **CSV** for simple flat data.
- Stack techniques: explicit format heading, "only X, no prose", skeletons, exact fields with types and allowed values, delimiters, one placeholder shape example, low temperature, and provider features (prefilling, JSON mode, structured outputs) where available.
- Expect **format drift**. Syntax drift fails loudly; structure drift parses and fails quietly, so always check keys, types and allowed values, not only "did it parse?"
- Parse defensively: strip fences, extract the JSON block, `json.loads` inside `try/except`, then check structure. Tolerate wrapping, reject broken content.
- **Re-ask once** with the exact error, then fail loudly.
- A locked format makes AI output **usable and reviewable**, not **correct**. Content review is still required.
- Coming up: **JSON Schema** and input/output contracts on **Thursday**, **validation scripts** on **Friday**, and **retry strategies** in **Week 9**.

---

## Additional Resources

- Anthropic, *Increase output consistency* (format specification, prefilling caveats, examples and structured outputs): https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency
- OpenAI, *Structured model outputs* (how structured outputs differ from JSON mode): https://developers.openai.com/api/docs/guides/structured-outputs
- Python documentation, *json — JSON encoder and decoder* (`json.loads`, `JSONDecodeError` attributes): https://docs.python.org/3/library/json.html
