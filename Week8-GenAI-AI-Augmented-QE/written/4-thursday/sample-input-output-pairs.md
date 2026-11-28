# Sample Input/Output Pairs

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** a sample input/output pair, and explain its two jobs: documentation and few-shot example.
- **Write** two example pairs for TestCaseDesigner: one clear story and one too vague to test.
- **Check** that every example obeys every rule in the contract, because the AI copies mistakes too.
- **Compare** the agent's reply for a vague story with and without examples.
- **Recognise** example leakage and other ways examples can mislead the AI.

---

## Why This Matters

On Tuesday, in *Few-Shot Prompting*, you saw that showing an AI a couple of examples often works better than describing what you want. That idea goes back to the research that made large language models famous: the GPT-3 paper showed models performing new tasks from just a few **demonstrations** placed in the prompt, without any retraining ([Brown et al., 2020](https://arxiv.org/abs/2005.14165)).

TestCaseDesigner needs exactly that help. In *Prompt Templates*, the typical reply for US-311 had a **perfect format and an invented value**: "within 2 seconds". The instructions said "do not invent", and the contract defined how to say "I can't", but nothing **showed** the AI what saying "I can't" looks like. Rules describe; examples demonstrate.

Examples have a second, quieter job. Written down in a file, a story with its correct reply is **documentation**: the clearest possible answer to "what does a good reply look like?" A new team member can read two examples and understand the contract faster than by reading the tables.

But examples are powerful in both directions. The AI copies them closely, including their **mistakes**. An example with a vague expected result teaches vague expected results. An example with a typo in its ID may teach the typo. So the last rule of this lesson matters as much as the first: **every example must obey every rule.**

> **Using this with the handout:** this lesson goes deeper into **Handout 08, Topic 4**. It uses the same two pairs (US-150 Free delivery and US-160 Quick login), the same `examples.txt`, the same US-311 run, the same checklist and the same sample reply.

---

## The Concept

### 1. What Is a Sample Input/Output Pair?

A **sample input/output pair** is an example **story** together with a **correct reply** for it. Pairs do two jobs:

| Job | How | Who benefits |
|---|---|---|
| **Document** what a good answer looks like | Kept in `examples.txt`, read by people | Testers, reviewers, new team members |
| **Teach** the AI the pattern | Added to the prompt as **few-shot examples** | The AI |

As few-shot examples, the AI copies their pattern: the exact JSON shape, the ID format, how boundaries are tested, and how to say "I can't". Choosing pairs that show **different situations**, such as a clear story and a vague one, is what makes them useful.

### 2. Show, Don't Tell

The handout's first key idea: **one good example reply teaches the JSON shape better than a paragraph of rules.**

Compare what the AI learns from each:

| From the rules alone | From an example |
|---|---|
| "Number test cases TC-<story number>-<two digits>" | `"id": "TC-150-01"` |
| "For every numeric limit, test the limit and just below it" | One case at $30.00, one at $29.99 |
| "If no criterion can be tested: status = needs_clarification, test_cases = []" | A complete reply that does exactly that |

The rules and the examples say the same things. But a rule has to be **interpreted**, and an example only has to be **copied**. When the two agree, they reinforce each other. When they disagree, many AIs follow the example, which is why section 7 checks the examples against the rules so carefully.

### 3. Cover Different Situations

The second key idea: **cover different situations.** Our two pairs show the two kinds of reply the contract allows:

| Pair | Situation | What it shows |
|---|---|---|
| **Example 1: US-150 Free delivery** | A clear story | Normal test cases, the boundary at the limit and just below, exact expected results |
| **Example 2: US-160 Quick login** | A story too vague to test | `needs_clarification`, an empty list and a question starting with the AC id |

If only Example 1 were given, the AI would learn that every reply has test cases, which is exactly the wrong lesson for US-311. If only Example 2 were given, it might learn that refusing is normal, even for clear stories. Together, they show that **both** answers are correct, each in its own situation.

### 4. Use Different Stories from the Real Ones

The third key idea: the examples are about **free delivery (US-150)** and **login (US-160)**, not about US-205, US-311 or US-312. Why not just use the real stories, with their correct answers?

- **No giving away answers.** If Example 1 were US-205 with five perfect test cases, the agent would simply copy them for US-205, and you would learn nothing about whether the agent works. You would be testing your own example, not the agent.
- **Teaching the pattern, not the content.** A different story forces the AI to **apply** the pattern: test the limit and just below it, whatever the limit is. US-150's limit is $30.00; US-205's is $50.00; US-312's is 10 items. The pattern transfers; the numbers do not.
- **Clear separation.** Different IDs make it easy to see if the AI confuses an example with the real story (section 10).

Notice how closely the examples **mirror** the real stories without copying them. US-150 has a money boundary, like US-205. US-160 says "login should be **quick**", which is vague in exactly the way US-311's "fast" is. Good examples are close enough to teach, and different enough not to give the answer away.

### 5. Examples Must Pass Every Rule

The fourth key idea: **a broken example teaches broken habits.** An example in the prompt is the strongest signal the AI receives. If it breaks a rule, the AI receives two contradictory messages, the rule and the example, and often follows the example.

So every example is checked against R1 to R4, Q1 and the human checklist, exactly like a real reply. Section 7 does that. You would never put an unreviewed AI draft into a test suite; for the same reason, you never put an unreviewed example into an agent.

### 6. Worked Example: Write `examples.txt`

#### Step 1 (Editor): Example 1, a clear story

Create `examples.txt` in your `agent` folder:

```text
### Example 1: a clear story
Story: US-150 Free delivery. Maximum test cases: 2
AC1: Orders of $30.00 or more get free delivery.
Reply:
{"story_id": "US-150", "status": "ok", "test_cases": [
 {"id": "TC-150-01", "title": "Order of exactly $30.00 gets free delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $30.00", "Go to checkout"],
  "expected_result": "Delivery cost shows $0.00"},
 {"id": "TC-150-02", "title": "Order of $29.99 pays delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $29.99", "Go to checkout"],
  "expected_result": "Delivery cost is not $0.00"}],
 "open_questions": []}
```

**What it teaches:** the exact JSON shape, the ID format, testing **at** the limit ($30.00) and **just below** it ($29.99), and exact expected results.

Look closely at the second expected result: *"Delivery cost is not $0.00"*. Why not *"Delivery cost is $4.99"*? Because the story **does not give a delivery price**. Writing $4.99 would invent a value, the very mistake the agent must avoid. The example shows the honest version: state exactly what the story allows you to state, and nothing more. That is a subtle lesson, and an example teaches it far better than a rule could.

#### Step 2 (Editor): Example 2, a vague story

Add underneath:

```text
### Example 2: a story that is too vague to test
Story: US-160 Quick login. Maximum test cases: 2
AC1: Login should be quick.
Reply:
{"story_id": "US-160", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum login time, in seconds?"]}
```

**What it teaches:** how to say "I can't": `needs_clarification`, an empty list, and a question that starts with the AC id. "Quick" is like "fast" in US-311, so this example targets exactly the mistake from *Prompt Templates*.

Notice the question's wording: *"What is the maximum login time, in seconds?"* It is open, it asks for a number, and it states the unit. It does not suggest an answer, such as "Is 2 seconds OK?". That is the good-question style from Wednesday's *AI-Assisted Requirements Analysis*, now built into the agent's example.

#### The consolidated file

```text
### Example 1: a clear story
Story: US-150 Free delivery. Maximum test cases: 2
AC1: Orders of $30.00 or more get free delivery.
Reply:
{"story_id": "US-150", "status": "ok", "test_cases": [
 {"id": "TC-150-01", "title": "Order of exactly $30.00 gets free delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $30.00", "Go to checkout"],
  "expected_result": "Delivery cost shows $0.00"},
 {"id": "TC-150-02", "title": "Order of $29.99 pays delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $29.99", "Go to checkout"],
  "expected_result": "Delivery cost is not $0.00"}],
 "open_questions": []}

### Example 2: a story that is too vague to test
Story: US-160 Quick login. Maximum test cases: 2
AC1: Login should be quick.
Reply:
{"story_id": "US-160", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum login time, in seconds?"]}
```

### 7. Step 3 (Paper): Check the Examples Against the Rules

Run R1 to R4 and Q1 over both example replies, each against **its own** story. Do it yourself first, then compare:

| Rule | Example 1 (US-150) | Example 2 (US-160) |
|---|---|---|
| R1: `story_id` matches | ✅ US-150 | ✅ US-160 |
| R2: every AC id exists | ✅ AC1 only | ✅ no `ac_ids` used; the question uses AC1, which exists |
| R3: cases ≤ maximum | ✅ 2 ≤ 2 | ✅ 0 ≤ 2 |
| R4: every AC covered | ✅ AC1 has two cases | ✅ AC1 has a question |
| Q1: no vague words | ✅ "shows $0.00", "is not $0.00" | ✅ no expected results to check |

Both examples pass every rule. Now the human checklist:

| Human check | Example 1 | Example 2 |
|---|---|---|
| No invented rules or values | ✅ No delivery price invented | ✅ No time limit invented |
| Boundary at the limit and just below | ✅ $30.00 and $29.99 | (none to test) |
| Messages copied exactly | (no messages in the story) | (no messages in the story) |

And the schema, from *JSON Schema*: all four fields present, IDs matching `^US-[0-9]{3}$` and `^TC-[0-9]{3}-[0-9]{2}$`, every `type` allowed. Both pass.

That is the standard every example must meet: **all three layers**, the same as a real reply. Example 1's R3 row deserves a second look: 2 cases with a maximum of 2. The example sits exactly **on** its own limit, which quietly teaches the AI that using the full allowance is fine, and exceeding it is not.

### 8. Checking That the Examples Parse

There is one more check worth doing: is each example reply **valid JSON**? A missing comma in an example would teach the AI broken JSON, and might make it hard for you to see the problem by eye. This short script, `check_examples.py`, finds each `Reply:` in `examples.txt` and tries to load the JSON after it. You do not need to run it today:

```python
import json

text = open("examples.txt").read()
for block in text.split("### Example")[1:]:
    title = block.splitlines()[0].strip(" :0123456789")
    reply_text = block.split("Reply:", 1)[1]
    try:
        reply = json.loads(reply_text)
        print(f"{reply['story_id']}: valid JSON, status={reply['status']}, "
              f"{len(reply['test_cases'])} test case(s) - {title}")
    except json.JSONDecodeError as error:
        print(f"NOT valid JSON - {title}: {error}")
```

On the file above it prints:

```text
US-150: valid JSON, status=ok, 2 test case(s) - a clear story
US-160: valid JSON, status=needs_clarification, 0 test case(s) - a story that is too vague to test
```

**What this code does:** `split("### Example")` cuts the file into one piece per example, and `[1:]` skips the empty text before the first one. In each piece, everything after `Reply:` is the JSON, which `json.loads` either reads or rejects with a `JSONDecodeError`. It relies on the file's layout staying exactly as written: one `### Example` heading and one `Reply:` per example. That is one more reason to keep the layout consistent.

### 9. Step 4 (AI tool): Run US-311 Again, Now with Examples

Open a **new chat** and paste, **in this order**, as **one message**:

1. the whole of `instructions_draft.md`;
2. the whole of `examples.txt`;
3. the whole of `filled_US-311.txt` from *Prompt Templates*:

```text
### Story
ID: US-311
Title: Fast search
Maximum test cases: 3
Acceptance criteria:
AC1: Search results should appear fast.
### End of story

Now write the JSON reply for this story.
```

This is the full agent prompt from *Prompt Templates*: instructions, then examples, then the filled template, with the real story **last**.

Mark your AI's reply:

- ✅ `status` is `"needs_clarification"` and `test_cases` is `[]`
- ✅ One open question starting with `AC1:` asking for a time in seconds
- ✅ **No invented time limit**
- ✅ The JSON shape matches the examples exactly

The handout's sample reply:

```json
{"story_id": "US-311", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum time, in seconds, for search results to appear?"]}
```

Compare it with the typical reply **without** examples, from *Prompt Templates*:

| | Without examples | With examples |
|---|---|---|
| `status` | `"ok"` | `"needs_clarification"` |
| `test_cases` | One case, "within 2 seconds" | `[]` |
| `open_questions` | `[]` | One question starting `AC1:` |
| Invented value? | ❌ Yes, "2 seconds" | ✅ No |

The instructions did not change. The story did not change. Only Example 2 was added, and the reply now follows the pattern it shows, almost word for word: compare its question with Example 2's *"What is the maximum login time, in seconds?"*. With an example of a vague story, most AIs now copy the honest refusal pattern. If yours still invented a number, do not worry: Friday adds a rule aimed at exactly this mistake.

### 10. Example Leakage

Examples work because the AI copies them. That same tendency can go wrong in a specific way: the AI copies **details** of an example into a reply where they do not belong. This is called **example leakage**. Some forms, **illustrative**:

| Leak | What you see in a reply for US-205 | Why it happens |
|---|---|---|
| **Copied story ID** | `"story_id": "US-150"` | The AI confused the example with the real story |
| **Copied values** | A test case at $30.00 | The example's numbers felt "standard" |
| **Copied wording** | "Delivery cost shows $0.00" | The example's phrasing was reused without thinking |
| **Answering the example** | A reply for US-160 instead of US-205 | The real story was not clearly separated or not last |

The handout's two defences work against all of these:

- **Clearly different IDs.** US-150 and US-160 look nothing like US-205, US-311 or US-312, so a copied ID is obvious, and R1 catches it automatically.
- **The real story last, inside its fences.** The `### Story` ... `### End of story` markers and the final instruction line tell the AI which story to answer.

The checks catch the rest. A copied $30.00 value would show up in the human checklist as a boundary that does not match the story. This is why examples and checks belong together: examples make good replies more likely, and checks catch the cases where the copying went too far.

### 11. Bad Examples Teach Bad Habits

The handout's Your Turn exercise 3 tests the fourth key idea directly: change Example 1's second expected result to *"Delivery works correctly"*, and run US-312 with it.

Before you try it, predict what might happen. *"Delivery works correctly"* breaks **Q1**. If the AI follows the example's pattern, you might see expected results for US-312 like *"Gift wrap works correctly"*. That exact phrase appeared in Reply A in *Required Fields and Validation Rules*, the reply that broke four rules. A single vague example can bring back a mistake the instructions explicitly forbid.

Whatever result you get, the experiment teaches the same thing as removing the "when unclear" section did in *Agent Instructions*: it is a **controlled change**, one edit with everything else the same, so any difference in the reply comes from that edit. Run it, record the result, then **restore** the correct example. A forgotten bad example would quietly damage every future run.

### 12. How Many Examples, and in What Order?

Two examples are enough for this agent: one for each kind of reply. More examples make the prompt longer, and every example is one more thing that must pass every rule and be kept up to date.

Order can matter too. Research on few-shot prompting has found that a model's results can change noticeably with the choice and **order** of the examples, and that models tend to favour patterns that appear often or near the end of the prompt ([Zhao et al., 2021](https://arxiv.org/abs/2102.09690)). In our `examples.txt`, the **vague** example comes last, just before the real story. That helps US-311. A tester should ask the obvious follow-up question: **could it push a clear story towards "needs clarification" too?**

You can test that. Run US-312, a clear story, with the examples, and check that the reply has test cases and `status: "ok"`. If a clear story ever comes back as `needs_clarification`, the order of the examples is one of the first things to try changing. Treat this as a hypothesis to check, not a known problem.

### 13. Examples as Living Documentation

`examples.txt` will change, like the instructions and the contract. When Friday's testing finds a mistake the agent keeps making, one of the fixes to try is an example that shows the right behaviour. When the contract changes, for example a new `priority` field, every example must change with it, or it will break the contract and teach the old format.

So examples deserve the same care as test cases:

- **Reviewed** before use, against every rule.
- **Kept in step** with the contract and the instructions.
- **Changed deliberately**, with the reason recorded.

That last point connects to Friday's `CHANGELOG.md`: "Added an example of refusing a vague story, because US-311 replies invented a time limit" is exactly the kind of entry that helps the next person understand the agent.

### 14. A Recipe for Writing a New Example

When you need a new pair, for this agent or another, these steps keep it useful and safe:

1. **Name the situation it teaches.** "A story with an exact message" or "a story with two boundaries". If you cannot name it in a few words, the example probably teaches nothing new.
2. **Invent a story close to the real ones, but different.** Same kind of rule, different feature, different numbers, a clearly different ID.
3. **Write the reply by hand, not with the AI.** An AI-written example may contain the very mistakes you want to prevent. If you do use an AI to draft it, review it as strictly as any AI output.
4. **Check it against all three layers**: the schema, R1 to R4 and Q1, and the human checklist, as in section 7.
5. **Check that it parses**, by eye or with `check_examples.py`.
6. **Test its effect**: run at least one real story with and without the new example, and compare the replies with the checklist.
7. **Record why it was added**, so the next person knows what it is for.

Step 3 is worth repeating. The examples are the part of the agent the AI copies most closely, so they are the last place to accept unreviewed AI text. Exercise 4 below asks you to write a third pair by hand; this recipe is the checklist for it.

### 15. When Examples and Rules Disagree

Sometimes an example and a rule point in different directions without anyone noticing. A typical case, **illustrative**: the instructions say "Number test cases TC-<story number>-<two digits>", but an old example still uses `TC-150-1` with one digit. The AI now sees two patterns and may follow either.

The fix is always the same: **the contract decides.** Check the example against the contract, correct whichever part disagrees, and re-run a story to confirm the replies follow the corrected pattern. Disagreements like this are one reason to re-check every example whenever the instructions or the contract change, not only when an example is first written.

### 16. The Complete Text Agent

Your `agent` folder now has every **text** part of the agent:

```text
agent/
├── README.txt
├── instructions_draft.md
├── input_template.txt
├── contract.md
├── examples.txt
└── stories/
    ├── US-205.json
    ├── US-311.json
    └── US-312.json
```

Look at what is there: role and goal, rules, the input template, the output format in the contract, two examples, and the rules for checking. Five of the six agent parts from *Agent Architecture* are now written down. The sixth, the **checks** as code, arrives tomorrow, along with the code that builds the prompts and records the results.

### 17. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI also "answers" the examples | The story at the end is not clearly separated | Keep the `### Story` ... `### End of story` fences and the final instruction line |
| The AI copies an example's story ID | It confused the example with the real story | Use clearly different IDs (US-150, US-160) and keep the real story **last** |
| A reply copies an example's values | The example's numbers leaked | Check boundaries against the real story; R1 and the human checklist catch most leaks |
| A vague phrase appears that the rules forbid | An example contains it | Check every example against Q1 and the human checklist |
| An example uses an old ID format or field | It was not updated when the contract changed | Re-check every example after any contract or instruction change |
| A clear story comes back as `needs_clarification` | Possibly the order of the examples | Test a clear story with the examples; try changing the order if it happens |

---

## Practice Exercises

1. **With and without (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** run Step 4 (instructions, examples, then US-311).
   - **Review:** mark the reply with the checklist in section 9.
   - **Run:** compare it, field by field, with your US-311 reply from *Prompt Templates*.
   - **Record:** in `prompts.txt`, note what the example changed.

2. **A clear story with examples (AI tool, 15 min).** Run US-312 (`filled_US-312.txt` from *Prompt Templates*) with the instructions **and** the examples. Did it test 10 and 9 items, copy the AC2 message exactly, and return `status: "ok"`? Did anything leak from the examples?

3. **Bad examples teach bad habits (AI tool, 15 min).** In a **copy** of `examples.txt`, change Example 1's second expected result to `"Delivery works correctly"`. Run US-312 with it. Did any vague wording appear in the reply? Record the result, then delete the copy.

4. **Write a third pair (paper, 15 min).** Write a pair for a story with an **exact message**, for example *US-170 Newsletter. AC1: Subscribing shows "Thanks for subscribing".* (Maximum test cases: 1.) Check your reply against R1 to R4, Q1 and the human checklist. Would adding it to `examples.txt` help US-205 and US-312? What could leak from it?

---

## Knowledge Check

1. What is a sample input/output pair, and what two jobs does it do?

<details><summary>Answer</summary>

An example story with a correct reply. It documents what a good answer looks like, and, in the prompt, works as a few-shot example the AI copies.

</details>

2. Why do our examples include a vague story?

<details><summary>Answer</summary>

So the AI sees how to refuse honestly instead of inventing a value, the mistake from US-311.

</details>

3. Why are the examples about US-150 and US-160, not the real stories?

<details><summary>Answer</summary>

To teach the pattern without giving away answers for US-205, US-311 or US-312, and so a copied ID or answer is easy to spot.

</details>

4. Why does Example 1 say "Delivery cost is not $0.00" instead of a price such as $4.99?

<details><summary>Answer</summary>

The story gives no delivery price, so writing one would invent a value. The example states only what the story allows.

</details>

5. What happened to the US-311 reply when the examples were added?

<details><summary>Answer</summary>

It changed from `status: "ok"` with an invented "2 seconds" to `needs_clarification`, an empty list and an AC1 question, closely copying Example 2's pattern.

</details>

6. What is example leakage? Give one example.

<details><summary>Answer</summary>

The AI copying details of an example into a reply where they do not belong, such as `"story_id": "US-150"` in a reply for US-205, or a $30.00 test case for US-205.

</details>

7. Why must every example pass every rule?

<details><summary>Answer</summary>

The AI copies examples closely, including their mistakes. A broken example teaches the broken pattern, even when the instructions forbid it.

</details>

8. The vague example comes last in `examples.txt`. What should a tester check because of that?

<details><summary>Answer</summary>

Whether a clear story, such as US-312, still gets test cases and `status: "ok"`. Example order can influence replies, so it is worth testing.

</details>

---

## Glossary

- **Sample input/output pair:** an example story with a correct reply.
- **Few-shot examples:** example pairs in the prompt that the AI copies the pattern from.
- **Demonstration:** another word for an example placed in the prompt.
- **Show, don't tell:** teaching by example rather than by description.
- **Example leakage:** the AI copying details of an example, such as its ID or values, into an unrelated reply.
- **Controlled change:** changing only one thing, so any difference in results is caused by that change.
- **Recency effect (in prompts):** a tendency for patterns near the end of the prompt to have more influence.
- **Example recipe:** the steps for writing a new pair: name the situation, invent a similar story, write the reply by hand, check it, test its effect, record why.
- **Living documentation:** documentation, such as `examples.txt`, kept up to date as the system changes.

---

## Summary

- A **sample pair** is a story with a correct reply. It **documents** a good answer and, in the prompt, **teaches** the AI the pattern.
- **Show, don't tell:** one example teaches the shape, the ID format and honest refusal better than a paragraph of rules.
- Cover **different situations** (a clear story and a vague one), and use **different stories** from the real ones.
- **Every example must pass every rule**: the schema, R1 to R4, Q1 and the human checklist. The AI copies mistakes too.
- With Example 2 added, the US-311 reply changed from an **invented "2 seconds"** to an **honest question**. Watch for **leakage** and test a clear story too.

---

## Additional Resources

- Brown et al., *Language Models are Few-Shot Learners* (GPT-3, 2020): https://arxiv.org/abs/2005.14165
- Zhao et al., *Calibrate Before Use: Improving Few-Shot Performance of Language Models* (2021): https://arxiv.org/abs/2102.09690
- OpenAI, *Prompt engineering* guide (few-shot learning): https://developers.openai.com/api/docs/guides/prompt-engineering
