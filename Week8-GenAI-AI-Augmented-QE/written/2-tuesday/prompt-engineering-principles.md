# Prompt Engineering Principles

## Learning Objectives

By the end of this lesson you will be able to:

- Define a **prompt** and explain what **prompt engineering** means in day-to-day QE work.
- Explain how a Large Language Model (LLM) "reads" a prompt, using Monday's ideas of **tokens**, the **context window**, **next-token prediction** and **temperature**.
- Name and recognise the seven **building blocks of a prompt**: role, task, context, input data, constraints, output format and examples.
- Describe the difference between **system**, **user** and **assistant** messages and build a provider-neutral **message list** in Python.
- Apply the **core principles** of good prompting: be clear and direct, give context, use delimiters and structure, break complex tasks into steps, ask for a plan before the answer, say what to do (not only what to avoid), and specify audience and length.
- Define **zero-shot prompting**.
- Run the **draft → run → evaluate → refine** loop and treat it as a testing activity, with prompts stored as **versioned artifacts** in Git.

---

## Why This Matters

Yesterday you saw that Generative AI can help with almost every stage of the testing life cycle. You also saw that its output can be wrong while looking right. Today's question is practical: **how do you ask an AI tool for something so that you reliably get useful, checkable output?** The answer is prompt engineering.

Think of an LLM as a very fast, very well-read new team member who joined this morning. They know a lot about software testing in general, but they know nothing about *your* application, *your* business rules or *your* team's conventions, and they will not ask clarifying questions unless you invite them to. If you say "write some tests for coupons", they will produce something generic. If you brief them the way you would brief a human colleague (who the work is for, what the rules are, what "done" looks like), the quality of the result changes dramatically.

This matters for the **Weekly Epic**. By Friday you will build your first QA agent: a program that sends prompts to an LLM and processes the results automatically. Every agent is built on prompts. A weak prompt inside an agent produces weak output *at scale*, every time the agent runs. The habits you build today (structure, clarity, explicit output formats, measurable acceptance criteria) are the same habits you will use on Thursday and Friday.

It also matters for **Project 2 – Test Automation Framework**. Today's exercise asks you to build a **prompt library** for test design and debugging tasks in your framework. A prompt library is only valuable if each prompt is well designed, tested and versioned, which is exactly what this lesson teaches.

Finally, prompt engineering is a skill that quality engineers are well placed to master. Writing a good prompt is very similar to writing a good requirement or a good bug report: precise, unambiguous, complete and testable. You already practised those skills in Week 3.

---

## The Concept

### 1. What Is a Prompt? What Is Prompt Engineering?

A **prompt** is the input text you give to a Generative AI model to get it to produce an output. It can be a single question typed into a chat window, or a long, carefully structured document containing instructions, business rules, code and examples.

**Prompt engineering** is the practice of designing, testing and improving prompts so that a model produces outputs that are **useful, accurate, consistent and in the form you need**. The word "engineering" is deliberate. It is not about finding magic words. It is a disciplined, repeatable process:

1. Decide what a good output looks like (acceptance criteria).
2. Write a prompt that gives the model everything it needs to produce that output.
3. Run it and compare the result to your criteria.
4. Change one thing at a time and run it again.

If that sounds like testing, it is. You will see in Section 7 that the prompt-refinement loop is essentially a small test cycle.

**A quick illustration.** Compare these two prompts for the same job:

> **Prompt A:** Write tests for the coupon feature.

> **Prompt B:** You are a senior QA engineer on an e-commerce web app. Using boundary value analysis and equivalence partitioning, list test ideas for the function `apply_coupon(total, code)`. Rules: coupon SAVE10 gives 10% off orders of $50.00 or more; orders under $50.00 get no discount; unknown codes raise `ValueError`. Include at least two boundary values around $50.00 and at least one negative test. Answer as a numbered list, one idea per line, in the form `input -> expected result`.

Prompt A leaves the model to guess the rules, the technique, the level of detail and the format. Prompt B removes the guessing. Neither prompt guarantees a correct answer, because LLMs can still make mistakes, but Prompt B makes a correct and *checkable* answer far more likely.

### 2. How an LLM "Reads" a Prompt

To write good prompts, it helps to remember what happens to a prompt inside the model. You learned each of these ideas on Monday; here we connect them to prompting.

#### 2.1 Tokens

The model does not see words or characters directly. Your prompt is first split into **tokens**: small chunks of text such as whole words, word pieces or punctuation. `apply_coupon` might become several tokens such as `apply`, `_`, `coupon`.

*Why it matters for prompting:* everything you send costs tokens (and often money), and every model has a limit on how many tokens it can handle. Unnecessary text is not free.

#### 2.2 The context window

The **context window** is the maximum number of tokens the model can consider at once: your instructions, any pasted material, the conversation so far *and* the response it is generating. Anything outside the window is invisible to the model.

*Why it matters for prompting:*

- The model has **no memory outside the context window**. If a business rule is not in the prompt (or earlier in the same conversation), the model does not know it.
- Each conversation starts from a blank slate. The model has no idea what you told it yesterday in a different chat.
- Long prompts are allowed, but more text is not automatically better; burying the key instruction inside pages of irrelevant logs makes it easier for the model to miss. How to choose *the right* context is the subject of today's lesson **Specificity and Context**.

#### 2.3 Next-token prediction

An LLM generates its answer one token at a time, each time predicting a likely next token given everything before it (your prompt plus what it has generated so far).

*Why it matters for prompting:*

- The model continues the pattern your prompt sets up. A formal, structured prompt tends to produce a formal, structured answer. A sloppy prompt tends to produce a loose answer.
- The model is optimised to produce *plausible* text, not *verified* text. That is why it can hallucinate a function that does not exist or a business rule you never mentioned. Good prompts reduce this by supplying facts and by asking the model to stick to them, but they cannot remove it. Systematic checking of AI output is covered on **Wednesday** (human validation) and **Friday** (validation scripts).
- Because the answer is produced left to right, asking the model to *first* outline its reasoning or plan and *then* give the final answer can improve quality on multi-step tasks (Section 5.5).

#### 2.4 Non-determinism and temperature

On Monday you saw that the model samples its next token from a probability distribution, and that **temperature** (and **top-p**) control how adventurous that sampling is. With a non-zero temperature, the same prompt can give different answers on different runs.

*Why it matters for prompting:*

- **Never judge a prompt by a single run.** A prompt that worked once may fail the next time. When you evaluate a prompt, run it several times.
- For tasks that need consistency (such as generating test data in a fixed format), a lower temperature usually helps; for brainstorming test ideas, a slightly higher temperature can give more variety. Many chat tools do not expose this setting; APIs usually do.
- The clearer and more constrained your prompt, the less room there is for random variation to change the meaning of the answer.

**Summary table**

| Monday concept | What it means for the prompts you write |
|----------------|------------------------------------------|
| Tokens | Every word costs; be concise but complete. |
| Context window | The model knows only what is in the window; supply the facts it needs. |
| Next-token prediction | The model follows the pattern you set; it produces plausible, not verified, text. |
| Temperature / top-p | Outputs vary between runs; test prompts more than once. |

### 3. The Anatomy of a Good Prompt

Most effective prompts are assembled from a small set of building blocks. Not every prompt needs all of them; a quick question might use just one. But knowing the blocks lets you check a prompt systematically, the way you might check a bug report for steps, expected result and actual result.

| # | Building block | Question it answers | QE example |
|---|----------------|---------------------|------------|
| 1 | **Role / persona** | Who should the model act as? | "You are a senior QA engineer on an e-commerce web app." |
| 2 | **Task / instruction** | What exactly should it do? | "List test ideas for `apply_coupon(total, code)`." |
| 3 | **Context** | What background does it need? | "Coupon SAVE10 gives 10% off orders of $50.00 or more." |
| 4 | **Input data** | What material should it work on? | The function's source code, a user story, an error log. |
| 5 | **Constraints** | What rules or limits apply? | "Use only the rules given. Include at least one negative test." |
| 6 | **Output format** | What shape should the answer take? | "Numbered list: `input -> expected result`." |
| 7 | **Examples** | What does a good answer look like? | "Example: `total=60.00, code=SAVE10 -> 54.00`." |

Let us look at each block more closely.

**1. Role / persona.** Assigning a role ("You are a senior QA engineer…", "You are a Python reviewer who focuses on test readability") sets the vocabulary, level of expertise and point of view the model should adopt. A role on its own does not make the model know your system, but it nudges answers towards the right professional style. Keep roles relevant: "You are a world-class genius" adds nothing; "You are a QA engineer reviewing tests for boundary coverage" tells the model what to pay attention to.

**2. Task / instruction.** The single most important block. Use a clear action verb: *list*, *generate*, *explain*, *review*, *classify*, *rewrite*, *summarise*. One prompt should usually have one main task. If you need several things, number them (Section 5.4).

**3. Context.** The facts the model cannot know on its own: business rules, the tech stack ("pytest 8 with Playwright for Python"), the purpose of the work ("these ideas will become automated regression tests"), who will read the output. Context is the block beginners most often forget, and today's lesson **Specificity and Context** is devoted to it.

**4. Input data.** The concrete material to work on: a user story, a function, a stack trace, an API response. Input data should be clearly separated from instructions using delimiters (Section 5.3) so the model knows what is *instruction* and what is *material*.

**5. Constraints.** Boundaries on the answer: what to include, what to exclude, what not to assume, limits on length or scope. "Do not invent rules that are not in the context" is a valuable constraint in QE because it directly targets hallucinated requirements.

**6. Output format.** How the answer should be laid out: a numbered list, a Markdown table, Gherkin scenarios, a pytest file, JSON. In automation, format is critical because a program, not a person, may read the result. Making the format strict and reliable is the subject of today's lesson **Format Locking**.

**7. Examples.** One or more samples of the desired output. Examples are one of the most powerful tools you have, and today's lesson **Few-Shot Prompting** covers how to choose and use them.

#### 3.1 An annotated QE prompt

Here is a full prompt for the running example, with each block labelled. Notice how it reads like a good task ticket.

```text
### Role
You are a senior QA engineer testing an e-commerce web app.        <- 1. Role

### Task
List test ideas for the apply_coupon(total, code) function.        <- 2. Task

### Context
Coupon SAVE10 gives 10% off orders of $50.00 or more.              <- 3. Context
Orders under $50.00 get no discount.
Unknown coupon codes raise ValueError.

### Input
<function>                                                         <- 4. Input data
def apply_coupon(total, code): ...
</function>

### Constraints
- Include at least two boundary values around $50.00.              <- 5. Constraints
- Include at least one negative test.
- Do not invent rules that are not in the context.

### Output format
A numbered list. One test idea per line: input -> expected result. <- 6. Output format

### Example
1. total=60.00, code=SAVE10 -> 54.00                               <- 7. Example
```

(The arrows and labels on the right are annotations for you; they would not be part of the real prompt.)

#### 3.2 Building a prompt from parts in Python

When you write prompts inside code (as you will for agents later this week), it helps to assemble them from named parts. That makes each block visible, reusable and easy to change one at a time.

```python
# build_prompt.py
def build_prompt(role, task, context, constraints, output_format):
    """Assemble a prompt from its named parts, one labelled section each."""
    sections = [
        f"### Role\n{role}",
        f"### Task\n{task}",
        f"### Context\n{context}",
        "### Constraints\n" + "\n".join(f"- {c}" for c in constraints),
        f"### Output format\n{output_format}",
    ]
    return "\n\n".join(sections)


prompt = build_prompt(
    role="You are a senior QA engineer testing an e-commerce web app.",
    task="List test ideas for the apply_coupon(total, code) function.",
    context=(
        "Coupon SAVE10 gives 10% off orders of $50.00 or more. "
        "Orders under $50.00 get no discount. "
        "Unknown coupon codes raise ValueError."
    ),
    constraints=[
        "Include at least two boundary values around $50.00.",
        "Include at least one negative test.",
        "Do not invent rules that are not in the context.",
    ],
    output_format="A numbered list. One test idea per line: input -> expected result.",
)

print(prompt)
print("---")
print("Characters:", len(prompt))
```

Output:

```text
### Role
You are a senior QA engineer testing an e-commerce web app.

### Task
List test ideas for the apply_coupon(total, code) function.

### Context
Coupon SAVE10 gives 10% off orders of $50.00 or more. Orders under $50.00 get no discount. Unknown coupon codes raise ValueError.

### Constraints
- Include at least two boundary values around $50.00.
- Include at least one negative test.
- Do not invent rules that are not in the context.

### Output format
A numbered list. One test idea per line: input -> expected result.
---
Characters: 527
```

**How the code works, line by line:**

- `def build_prompt(role, task, context, constraints, output_format):` defines a function with one parameter per building block. `constraints` is expected to be a **list** of strings because there are usually several.
- `sections = [ ... ]` builds a Python list where each item is one labelled section of the prompt.
- `f"### Role\n{role}"` is an **f-string** (Week 1). The text `### Role` is a heading, `\n` is a newline, and `{role}` inserts the value of the `role` parameter.
- `"\n".join(f"- {c}" for c in constraints)` turns the list of constraints into bullet lines. The part inside `join(...)` is a **generator expression**: for each constraint `c`, it produces the string `"- " + c`. `"\n".join(...)` glues those strings together with a newline between each.
- `return "\n\n".join(sections)` joins the sections with a blank line between them, producing one prompt string.
- The call to `build_prompt(...)` uses **keyword arguments** (`role=...`, `task=...`) so it is obvious which value fills which block.
- The `context` value is written as several string literals inside parentheses. Python automatically concatenates adjacent string literals, which keeps long text readable in code.
- `len(prompt)` counts characters. Characters are not tokens, but this simple count reminds you that prompts have a size.

This function is deliberately simple. It shows the *idea* of building prompts from parts. Turning prompts into reusable, parameterised **templates** for agents is covered on **Thursday** and **Friday**.

### 4. System, User and Assistant Messages

Chat-based LLM tools and APIs do not usually take one big string. They take a **list of messages**, and each message has a **role** saying who "said" it. Although each AI provider has its own exact syntax, almost all of them use the same three roles:

| Role | Who writes it | Purpose | Example |
|------|---------------|---------|---------|
| **system** | The developer or tool configuring the model | Standing instructions for the whole conversation: persona, rules, tone, safety boundaries. | "You are a senior QA engineer. Only use the rules you are given. Be concise." |
| **user** | The person (or program) making a request | The specific request for this turn, plus any input data. | "Give 3 test ideas for `apply_coupon`…" |
| **assistant** | The model | The model's previous replies. Sending them back keeps the conversation history. | "1. total=50.00, code=SAVE10 -> 45.00 …" |

Key points for beginners:

- **The system message sets the frame; the user message carries the job.** Put things that are true for every request (role, house rules, "do not invent rules") in the system message. Put the specific task and its input data in the user message.
- **The model is stateless.** Between API calls the model remembers nothing. A "conversation" works because the application sends the *entire* message history (system, then alternating user and assistant messages) every time. That history counts against the context window.
- **Some providers use slightly different names.** For example, some call the system message "instructions" or pass it as a separate parameter, and some call the assistant role "model". The concept is the same.
- **In chat tools such as ChatGPT, Claude or Gemini web apps,** you usually only type user messages. The tool's own system message is hidden, and some tools let you add "custom instructions" or "project instructions" that act like a system message.

#### 4.1 Building a message list in Python, with a stand-in model

The following code builds a provider-neutral message list and sends it to `fake_llm`, a tiny function that **pretends** to be an LLM. It is a deterministic stand-in for teaching only: it does not understand language, it simply returns a canned answer depending on whether the prompt asked for a numbered list. We use it so that you can run the code without an API key and get the same output every time.

```python
# messages_demo.py
def build_messages(system_text, user_text, history=None):
    """Return a provider-neutral list of chat messages."""
    messages = [{"role": "system", "content": system_text}]
    for turn in history or []:          # earlier turns, if any
        messages.append(turn)
    messages.append({"role": "user", "content": user_text})
    return messages


def fake_llm(messages):
    """A deterministic STAND-IN for a real LLM, used only for teaching.

    It does not understand anything. It just returns a canned reply that
    depends on whether the last user message asked for a specific format.
    """
    last_user = messages[-1]["content"]
    if "numbered list" in last_user.lower():
        return ("1. total=50.00, code=SAVE10 -> 45.00\n"
                "2. total=49.99, code=SAVE10 -> 49.99\n"
                "3. total=80.00, code=BOGUS -> ValueError")
    return ("There are many things you could test for a coupon feature, "
            "such as valid codes, invalid codes, and perhaps performance.")


system_text = ("You are a senior QA engineer for an e-commerce web app. "
               "Only use the rules you are given. Be concise.")

vague = build_messages(system_text, "Give me some tests for coupons.")
specific = build_messages(
    system_text,
    "Rules: SAVE10 gives 10% off orders of $50.00 or more; unknown codes "
    "raise ValueError.\nTask: give 3 test ideas for apply_coupon(total, code) "
    "as a numbered list, one per line: input -> expected result.",
)

for name, msgs in [("vague", vague), ("specific", specific)]:
    reply = fake_llm(msgs)
    msgs.append({"role": "assistant", "content": reply})   # keep the history
    print(f"== {name}: {len(msgs)} messages, roles = {[m['role'] for m in msgs]}")
    print(reply)
    print()
```

Output:

```text
== vague: 3 messages, roles = ['system', 'user', 'assistant']
There are many things you could test for a coupon feature, such as valid codes, invalid codes, and perhaps performance.

== specific: 3 messages, roles = ['system', 'user', 'assistant']
1. total=50.00, code=SAVE10 -> 45.00
2. total=49.99, code=SAVE10 -> 49.99
3. total=80.00, code=BOGUS -> ValueError
```

**How the code works:**

- Each message is a **dictionary** with two keys: `"role"` and `"content"`. This is the most common shape across providers.
- `build_messages` always starts with the system message, then adds any earlier turns from `history`, then adds the new user message at the end.
- `history or []` means "use `history` if it was given, otherwise use an empty list". This avoids an error when no history is passed, and avoids the classic Python mistake of using a mutable default argument such as `history=[]`.
- `fake_llm` looks only at `messages[-1]["content"]`, the last message (index `-1` means "last item"). `.lower()` makes the check case-insensitive.
- In the loop, `msgs.append({"role": "assistant", "content": reply})` adds the model's reply to the history. If we sent a follow-up question, we would send all three messages plus the new user message, which is exactly how real chat applications keep "memory".
- `[m['role'] for m in msgs]` is a **list comprehension** that collects the role of every message so we can see the structure.

**What to notice:** the vague request produced a generic answer that you cannot turn into tests. The specific request produced three concrete, checkable ideas covering both sides of the $50.00 boundary and a negative case. A real LLM is far more capable than `fake_llm`, but the pattern you just saw is real: the more precisely you ask, the more usable the answer.

> **Check the stand-in's "answer" yourself.** Is `total=50.00, code=SAVE10 -> 45.00` correct? Yes: 10% of 50.00 is 5.00, so 45.00. Is `49.99 -> 49.99` correct? Yes: under $50.00 there is no discount. This habit of verifying every expected result is essential, and Wednesday's lesson on human validation makes it formal.

In a real project, you would replace `fake_llm` with a call to your provider's SDK. The message list would be passed almost unchanged. Because we are not using live APIs in today's reading, we leave the provider-specific details to your instructor's demo.

### 5. Core Principles of Good Prompting

The major AI providers (Anthropic, OpenAI, Google) publish prompting guides, and they agree on a common set of principles. Here they are, with QE examples for each.

#### 5.1 Be clear and direct

Write instructions as you would for a capable colleague who has **no background** on your task. A useful test from Anthropic's guide: if you showed your prompt to a colleague with minimal context, would they be confused? If yes, the model probably will be too.

- Use explicit action verbs.
- State the goal and what success looks like.
- Avoid hints and hedging ("maybe you could possibly look at…").

| Weak | Better |
|------|--------|
| "Can you look at this test?" | "Review this pytest test and list any assertions that would still pass if `apply_coupon` returned the wrong total." |
| "Help with login testing." | "List negative test ideas for the login form: email field, password field and the Sign In button." |

#### 5.2 Give context, including the *why*

Tell the model the facts it needs (business rules, technology, environment) and, where useful, *why* you want something. Explaining the reason helps the model make good decisions in situations your instructions did not cover.

- "Use only Playwright's built-in locators such as `get_by_role`, **because our team avoids CSS selectors that break when styling changes**."
- "Keep each test independent, **because they run in parallel in our CI pipeline**."

The reason gives the model a principle to apply, not just a rule to follow. Deciding *how much* context to give, and which kinds, is covered in depth in **Specificity and Context**.

#### 5.3 Use delimiters and structure

When a prompt mixes instructions with material (code, logs, requirements), the model can confuse the two. **Delimiters** are markers that separate sections clearly. Common choices:

- Markdown headings: `### Instructions`, `### Input`
- XML-style tags: `<requirements> ... </requirements>`, `<code> ... </code>`, `<log> ... </log>`
- Triple quotes or triple backticks around a block of text or code

Example:

```text
Review the test below against the requirement. List any requirement rules the test does not check.

<requirement>
Coupon SAVE10 gives 10% off orders of $50.00 or more. Unknown codes raise ValueError.
</requirement>

<test>
def test_save10():
    assert apply_coupon(100.00, "SAVE10") == 90.00
</test>
```

Benefits:

- The model knows exactly where the requirement ends and the test begins.
- You can refer to sections by name ("compare the `<test>` to the `<requirement>`").
- It becomes easy to swap the input in code while keeping the instructions the same.
- It reduces the chance that text inside your input (for example, a log line that happens to say "ignore this") is mistaken for an instruction. Security aspects of this are covered later: responsible use on **Wednesday** and prompt injection in **Week 10**.

There is no single "correct" delimiter. Pick one style and use it consistently across your prompt library.

#### 5.4 Break complex tasks into steps

LLMs perform better when a big task is split into smaller, explicit steps, much like a test procedure. There are two ways to do this:

**Within one prompt**, with numbered steps:

```text
1. Read the user story in <story>.
2. List the business rules it states, one per line.
3. For each rule, propose one positive and one negative test idea.
4. Present the result as a table with columns: Rule | Positive test | Negative test.
```

**Across several prompts**, where you send one prompt, check the result, then use it in the next prompt (for example, first ask for the list of rules, review it, then ask for tests based on the corrected list). This gives you a checkpoint between steps where a human (you) can catch errors early. Automating such sequences, where one agent's output feeds the next, is the subject of agent chains in **Week 9**.

Why splitting helps: each step is simpler, so the model is less likely to skip something, and when something does go wrong you can see *which step* failed, just as small, focused tests make failures easier to diagnose than one giant end-to-end test.

#### 5.5 Ask for a plan or reasoning before the answer (where useful)

For tasks that involve multi-step reasoning (working out expected values, analysing why a test fails, deciding which boundaries matter), you can ask the model to think through the problem *before* giving its final answer:

```text
First, list the boundaries and partitions you can identify from the rules, and explain each briefly.
Then, based on that analysis, list the test ideas.
```

Because the model generates text left to right (Section 2.3), the reasoning it writes first becomes part of the context for the final answer. This often improves accuracy, and it also gives **you** something to review: if the reasoning says "the boundary is $500", you can spot the error immediately.

Use this selectively:

- **Helpful** for analysis, calculations, debugging and design decisions.
- **Unnecessary** for simple lookups or formatting tasks, where it only adds length and cost.
- Some modern models have built-in "reasoning" or "thinking" modes that do this automatically. Even then, asking for a short visible plan is useful when you want to review the approach.

If a program needs to read the final answer, keep the reasoning and the answer clearly separated (for example, reasoning in `<analysis>` tags and the answer in `<answer>` tags). Reliable output structure is covered in **Format Locking**.

#### 5.6 Say what to do, not only what not to do

Models follow positive instructions more reliably than prohibitions. "Don't" instructions also leave the model guessing about what you *do* want.

| Negative only | Positive and specific |
|---------------|-----------------------|
| "Don't write long answers." | "Answer in at most 5 bullet points." |
| "Don't use bad locators." | "Use `page.get_by_role(...)` or `page.get_by_test_id(...)` locators." |
| "Don't make things up." | "Use only the rules listed in `<context>`. If a rule needed for a test is missing, write `QUESTION:` followed by what you need to know." |

The last example is particularly valuable in QE. It gives the model a **legitimate way out** when information is missing, instead of pushing it to guess. A model that returns `QUESTION: What happens for exactly $50.00?` has just found an ambiguity in your requirement, which is useful testing work in itself.

Negative instructions are still fine as **additional** guard rails ("Do not invent rules"), as long as the positive instruction is also there.

#### 5.7 Specify audience, length and tone

The same content looks very different for different readers. Tell the model who the output is for and how long it should be.

- "Summarise this test run for a **product manager** in **three sentences**, without technical jargon."
- "Explain this stack trace to a **junior tester** in **under 150 words**."
- "Write the bug report in the **team's Jira style**: Title, Steps to Reproduce, Expected, Actual, Severity."

Length constraints are best expressed in countable units: number of bullet points, sentences, test ideas or words. "Short" and "detailed" mean different things to different people, and to models.

#### 5.8 Principles at a glance

| Principle | One-line reminder | QE example |
|-----------|-------------------|------------|
| Clear and direct | Write for a smart colleague with no background. | "List negative tests for the email field." |
| Give context and the why | Supply facts the model cannot know; explain reasons. | "Tests run in parallel, so keep them independent." |
| Delimiters and structure | Separate instructions from material. | `<log> ... </log>` |
| Break into steps | Number the steps or split into several prompts. | Rules → tests → table. |
| Plan before answer | Ask for analysis first on multi-step tasks. | "List boundaries, then tests." |
| Positive framing | Say what to do; give a way out. | "If unsure, write QUESTION: …" |
| Audience and length | Who reads it, how long, in what style. | "3 sentences for a PM." |

### 6. Zero-Shot Prompting

A **zero-shot prompt** asks the model to perform a task **without giving it any examples** of the desired output. Every prompt in this lesson so far, apart from the annotated example in Section 3.1, is zero-shot. The model relies entirely on your instructions and its general training.

Zero-shot prompting works well when:

- The task is common and well understood (summarise this log, explain this error).
- The output format is simple and fully described in words.

It struggles when:

- You need a very particular style or structure (your team's exact test-case template).
- The task involves a classification scheme the model has never seen (your team's defect categories).

In those cases you add one or more examples to the prompt. That technique is called **few-shot prompting** and has its own lesson today, **Few-Shot Prompting**, which covers how many examples to use and how to choose them.

### 7. The Prompt-Refinement Loop: Prompting as Testing

You will rarely write the perfect prompt first time. Professional prompt engineering follows a loop:

```text
   +---------+     +-------+     +----------+     +--------+
   |  Draft  | --> |  Run  | --> | Evaluate | --> | Refine |
   +---------+     +-------+     +----------+     +--------+
        ^                                              |
        +----------------------------------------------+
```

1. **Draft.** Write the prompt using the building blocks in Section 3. Before running it, write down your **acceptance criteria**: what must a good answer contain? For our coupon prompt: mentions the $50.00 boundary, mentions $49.99, includes a negative test, is a numbered list.
2. **Run.** Send the prompt. Because outputs vary (Section 2.4), run it several times, ideally on more than one input.
3. **Evaluate.** Compare each output to your acceptance criteria. Note which criteria failed and *how* (missing, wrong, wrong format).
4. **Refine.** Change the prompt to address the failure, **one change at a time**, so you know which change helped. Then run again.

Notice how closely this mirrors the testing you already know:

| Prompt refinement | Software testing |
|-------------------|------------------|
| Acceptance criteria for the output | Expected results |
| Running the prompt several times | Executing test cases, including repeat runs for flaky behaviour |
| Comparing output to criteria | Pass/fail evaluation |
| Changing one thing at a time | Isolating a defect |
| Re-running after a change | Regression testing |

#### 7.1 A small, automated version of the loop

The following script keeps three versions of a prompt, runs each through our stand-in model, and evaluates the reply against four explicit checks. Again, `fake_llm` is a deterministic stand-in written so that better prompts get better replies; a real model would vary.

```python
# refine_loop.py
PROMPT_VERSIONS = {
    "v1": "Give me some tests for coupons.",
    "v2": ("Give test ideas for apply_coupon(total, code). SAVE10 gives 10% "
           "off orders of $50.00 or more."),
    "v3": ("Give test ideas for apply_coupon(total, code). SAVE10 gives 10% "
           "off orders of $50.00 or more; unknown codes raise ValueError. "
           "Include boundary values and one negative test. Answer as a "
           "numbered list: input -> expected result."),
}


def fake_llm(prompt):
    """Deterministic STAND-IN for an LLM. Replies get better as prompts do."""
    if "numbered list" in prompt:
        return ("1. total=50.00, code=SAVE10 -> 45.00\n"
                "2. total=49.99, code=SAVE10 -> 49.99\n"
                "3. total=80.00, code=BOGUS -> ValueError")
    if "SAVE10" in prompt:
        return "Try SAVE10 on orders of $100.00 and $50.00 and check the discount."
    return "Test valid coupons, invalid coupons and expired coupons."


def evaluate(reply):
    """Simple, explicit checks: our acceptance criteria for the reply."""
    return {
        "mentions 50.00 boundary": "50.00" in reply,
        "mentions 49.99 boundary": "49.99" in reply,
        "has negative test": "ValueError" in reply,
        "is numbered list": reply.lstrip().startswith("1."),
    }


for version, prompt in PROMPT_VERSIONS.items():
    checks = evaluate(fake_llm(prompt))
    passed = sum(checks.values())
    print(f"{version}: {passed}/{len(checks)} checks passed")
    for name, ok in checks.items():
        if not ok:
            print(f"    FAIL: {name}")
```

Output:

```text
v1: 0/4 checks passed
    FAIL: mentions 50.00 boundary
    FAIL: mentions 49.99 boundary
    FAIL: has negative test
    FAIL: is numbered list
v2: 1/4 checks passed
    FAIL: mentions 49.99 boundary
    FAIL: has negative test
    FAIL: is numbered list
v3: 4/4 checks passed
```

**How the code works:**

- `PROMPT_VERSIONS` is a dictionary mapping a version label to the prompt text. Keeping old versions lets you compare them and roll back.
- `evaluate(reply)` returns a dictionary of named checks. Each value is `True` or `False`. These are simple substring checks using the `in` operator: `"50.00" in reply` is `True` if the text `50.00` appears anywhere in the reply.
- `reply.lstrip().startswith("1.")` removes leading whitespace, then checks whether the reply starts with `1.`, a cheap way to detect a numbered list.
- `sum(checks.values())` works because in Python `True` counts as `1` and `False` as `0`, so the sum is the number of passed checks.
- The inner loop prints only the failing checks, just like a test runner highlights failures.

**What to notice:**

- Each version adds one kind of information: v2 adds the rule, v3 adds the negative-case rule, the constraints and the format. The score rises as the prompt improves.
- The checks here are deliberately crude. A reply could contain "50.00" and still be wrong. Simple checks are a useful *first filter*, not proof of correctness. Formal output contracts (**Thursday**), validation scripts (**Friday**) and semantic evaluation of LLM output (**Week 10**) build on this idea properly.

### 8. Prompts Are Artifacts: Version Them

If a prompt is used more than once, especially inside a test framework or an agent, treat it like code:

- **Store it in Git** (Week 1). Keep prompts in files, for example a `prompts/` folder in your Project 2 repository, rather than only in chat history.
- **Give it a version** and a short description: what it is for, which model it was tested with, and its acceptance criteria.
- **Commit changes with meaningful messages**, such as `prompts: add negative-test constraint to coupon test-ideas prompt (v3)`. When a prompt's behaviour changes, `git log` and `git diff` tell you what changed and why.
- **Record evidence.** Note the date, model and a sample of outputs when you accept a version. Models are updated by their providers, and a prompt that worked on one model version may behave differently on the next. Re-running your evaluation after a model change is regression testing for prompts.
- **Review prompts** in pull requests the same way you review test code.

A simple file layout for today's exercise might look like this:

```text
prompts/
  README.md                      # what each prompt is for, how to use it
  test-design/
    coupon-test-ideas.v3.md
    login-negative-tests.v1.md
  debugging/
    explain-stack-trace.v2.md
```

Each prompt file can include a short header:

```text
Purpose: Generate boundary and negative test ideas for a pricing rule.
Version: 3
Tested with: <model name>, 5 runs, YYYY-MM-DD
Acceptance criteria: boundaries on both sides; >= 1 negative test; numbered list.
Changes from v2: added "unknown codes raise ValueError" rule and output format.
```

This is the foundation of the prompt library you will build in today's exercise. Turning these into parameterised, reusable templates for agents comes on **Thursday** and **Friday**.

### 9. Putting It Together: A Prompt Checklist

Before you send an important prompt, run through this checklist:

1. **Task:** Is there one clear main task with an action verb?
2. **Role:** Is a relevant role or perspective set?
3. **Context:** Does the model have every business rule and technical fact it needs?
4. **Input:** Is the input material clearly delimited from the instructions?
5. **Constraints:** Have I said what to include, what to avoid, and what to do if information is missing?
6. **Format:** Have I described exactly how the answer should look?
7. **Examples:** Would an example of a good answer help?
8. **Steps / reasoning:** Is the task complex enough to break into steps or ask for a plan first?
9. **Audience and length:** Have I said who it is for and how long it should be?
10. **Acceptance criteria:** Do I know how I will judge whether the answer is good, and have I planned to run it more than once?

The remaining lessons today go deeper on several of these items: **Specificity and Context** (items 3 and 4), **Format Locking** (item 6), **Few-Shot Prompting** (item 7), **Common Prompt Failure Modes** (what goes wrong and how to fix it), and two applied lessons, **AI-Assisted Test Design** and **AI-Assisted Coding and Debugging**.

---

## Practice Exercises

1. **Label the blocks.** Take this prompt and label each part with its building block (role, task, context, input, constraints, output format, examples). Then name one block that is missing.
   > "As an API tester, write pytest tests for GET /products/{id}. The endpoint returns 200 with product JSON for existing IDs and 404 for unknown IDs. Use the requests library. Return only the Python code."

2. **Rewrite a vague prompt.** Rewrite "Test the search box" into a structured prompt for the Project 2 e-commerce site using at least five building blocks. Write three acceptance criteria for the answer.

3. **System vs user.** Split the following into a system message and a user message, and explain your choice: "You are a QA reviewer who always answers in a Markdown table and never invents requirements. Review this test for missing negative cases: `def test_login(): ...`"

4. **Positive framing.** Rewrite each instruction positively: (a) "Don't be vague." (b) "Don't use time.sleep in tests." (c) "Don't guess expected results."

5. **Extend the code.** Modify `build_prompt` to accept an optional `examples` list and an optional `input_data` string. If `input_data` is provided, wrap it in `<input>` and `</input>` tags. Test your function with and without the new arguments.

6. **Extend the evaluator.** Add a fifth check to `evaluate()` in `refine_loop.py` that fails if the reply contains the word "performance" (off-topic for this prompt). Run the script and confirm which versions are affected.

7. **Version a prompt.** Create a `prompts/` folder in a practice Git repository, add your prompt from Exercise 2 as `search-test-ideas.v1.md` with a header (purpose, version, acceptance criteria), commit it, improve it to v2, and commit again with a meaningful message. Use `git diff` to view the change.

---

## Knowledge Check

1. What is the difference between a prompt and prompt engineering?
2. Why does the context window matter when you write a prompt about your own application's business rules?
3. Why should you run a prompt more than once before deciding it works?
4. Name the seven building blocks of a prompt.
5. What belongs in a system message, and what belongs in a user message?
6. Why do the message lists sent to chat APIs include previous assistant messages?
7. Give two benefits of using delimiters such as `<requirement>` tags.
8. Rewrite "Don't make up rules" as a positive instruction that also gives the model a way out.
9. What is zero-shot prompting, and when might it not be enough?
10. List the four steps of the prompt-refinement loop and map two of them to familiar testing activities.

<details>
<summary>Answers</summary>

1. A prompt is the input given to a GenAI model. Prompt engineering is the disciplined practice of designing, testing and refining prompts so the model's output is useful, accurate, consistent and in the required format.
2. The model only knows what is inside the context window (plus its general training). Your business rules are not in its training, so if they are not in the prompt or conversation, the model will guess.
3. Because with non-zero temperature the model samples tokens, so the same prompt can give different outputs on different runs. One good result does not prove the prompt is reliable.
4. Role/persona, task/instruction, context, input data, constraints, output format, examples.
5. System: standing instructions for the whole conversation (role, rules, tone, boundaries). User: the specific request for this turn and its input data.
6. Because the model is stateless between calls. The application keeps the conversation going by resending the whole history, including the model's earlier replies (assistant messages).
7. Any two of: they separate instructions from material; you can refer to sections by name; inputs can be swapped in code easily; text inside the input is less likely to be mistaken for instructions.
8. For example: "Use only the rules listed in `<context>`. If a rule you need is missing, write `QUESTION:` followed by what you need to know."
9. A prompt with no examples of the desired output. It may not be enough when you need a very specific style, structure or an unfamiliar classification scheme; then few-shot prompting helps.
10. Draft → Run → Evaluate → Refine. Running maps to executing tests; evaluating maps to comparing actual with expected results; refining one change at a time maps to isolating a defect; re-running after a change maps to regression testing.

</details>

---

## Glossary

- **Prompt:** The input text given to a Generative AI model to produce an output.
- **Prompt engineering:** Designing, testing and refining prompts to get useful, accurate, consistent and well-formatted output.
- **Token:** A chunk of text (word, word piece or symbol) that the model processes.
- **Context window:** The maximum number of tokens a model can consider at once, including the prompt, history and response.
- **Role / persona:** The perspective or expertise the prompt asks the model to adopt.
- **Context:** Background facts the model needs but cannot know on its own.
- **Constraint:** A rule or limit on what the answer may contain.
- **Delimiter:** A marker (heading, XML-style tag, triple quotes) that separates sections of a prompt.
- **System message:** Standing instructions that frame the whole conversation.
- **User message:** The specific request for the current turn.
- **Assistant message:** A previous reply from the model, resent to preserve conversation history.
- **Stateless:** Remembering nothing between calls; history must be sent each time.
- **Zero-shot prompting:** Asking a model to do a task without giving examples.
- **Few-shot prompting:** Including one or more examples of the desired output in the prompt (today's separate lesson).
- **Acceptance criteria (for a prompt):** The conditions a model's answer must meet to be considered good.
- **Prompt-refinement loop:** The cycle of draft, run, evaluate and refine.
- **Prompt library:** A versioned collection of tested, documented prompts for repeated tasks.

---

## Summary

- A **prompt** is the input to a GenAI model; **prompt engineering** is the disciplined, testable process of designing and improving prompts.
- The model sees **tokens**, knows only what is in its **context window**, generates **plausible** text one token at a time, and can vary between runs. Supply the facts, structure your request and test more than once.
- Good prompts are built from **role, task, context, input data, constraints, output format and examples**. Use them as a checklist.
- Chat models take **message lists** with **system**, **user** and **assistant** roles. The model is stateless; history is resent each time.
- Core principles: **be clear and direct**, **give context and the why**, **use delimiters**, **break tasks into steps**, **ask for a plan first** when reasoning is needed, **frame instructions positively** with a way out, and **specify audience and length**.
- **Zero-shot** prompts use no examples; few-shot prompting adds them.
- Improve prompts with the **draft → run → evaluate → refine** loop, which is a small testing cycle with acceptance criteria.
- Treat reusable prompts as **versioned artifacts in Git**, the basis of today's Project 2 prompt library.

---

## Additional Resources

- Anthropic, *Prompting best practices* (Claude Platform Docs; includes "Be clear and direct", XML tags, giving context and the why): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct
- Google AI for Developers, *Prompt design strategies* (Gemini API documentation; clear instructions, constraints, response format, breaking down prompts): https://ai.google.dev/gemini-api/docs/prompting-strategies
- Prompt Engineering Guide (DAIR.AI), *Elements of a Prompt*: https://www.promptingguide.ai/introduction/elements
