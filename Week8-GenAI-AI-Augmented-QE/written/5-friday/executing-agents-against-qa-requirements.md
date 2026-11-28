# Executing Agents against QA Requirements

## Learning Objectives

By the end of this lesson you will be able to:

- **Run** the agent end to end on a new requirement: add the story, build its prompt, run it, save the reply, check it and review it.
- **Triage** every result, giving it an action and an owner: the tester, the business analyst (BA) or the agent maintainer.
- **Explain** why a new story needs no new code.
- **Apply** the human checklist to a reply that passes the script, and spot an assumption the story does not support.
- **Explain** why a tester still reviews test cases the agent produced and the checks accepted.

---

## Why This Matters

So far the agent has worked on stories chosen to teach: a boundary, a vague requirement, a whole-number limit. Real backlogs are not chosen to teach. A new story arrives, and nobody knows in advance whether it is clear, vague or subtly ambiguous. The agent has to handle it, and **you** have to decide what happens next.

That second part is the one people forget. Running an agent produces a reply, a check result and a review. None of those is the goal. The goal is that a tester gets useful test cases, that a BA gets the questions they need to answer, and that the agent itself improves where it failed.

Each of those is an **action** for a specific **person**. A result nobody acts on is wasted, and a result acted on by the wrong person causes confusion: test cases sent to the BA, questions sent to the tester, or a failure nobody owns.

This lesson runs the agent on a new story, US-313, end to end, and then on a second story with a numeric limit, to show a subtler kind of problem. Both pass the checker. Only one of them is ready to use.

> **Using this with the handout:** this lesson goes deeper into **Handout 10, Topic 3**. It uses the same US-313 story, the same run, the same sample reply, the same triage table and the same exercises.

---

## The Concept

### 1. What Does "Executing the Agent" Mean?

**Executing the agent** means running it on **real requirements** from the backlog, end to end:

1. add the story;
2. build its prompt;
3. run it in the AI tool;
4. save the reply;
5. check it with the script **and** the human checklist;
6. **act** on the result.

Every outcome needs an **action** and an **owner**: an accepted reply goes to a tester, unclear stories go to the BA, and failures go back to whoever maintains the agent's instructions. Running the agent is not the end of the job; **deciding what happens next is**.

### 2. The Run, Step by Step

```text
add story file ─► run_agent.py (WAITING) ─► paste prompt, save reply
     ─► run_agent.py (PASS/FAIL) ─► human checklist ─► decision + owner
```

Notice that `run_agent.py` appears **twice**. The first run builds the new prompt and tells you the story is WAITING. The second run, after you save the reply, checks it. In between is the manual step from *Creating Reusable Prompt Templates*. Nothing new is needed: the same command, the same folders, the same checker.

### 3. Triage: Every Result Gets an Action and an Owner

**Triage** means deciding, for each result, what happens next and who does it. The word comes from emergency medicine, where it means sorting patients by what they need. For the agent:

| Result | Action | Owner |
|---|---|---|
| Script PASS + human OK | Review and use the test cases | Tester |
| `needs_clarification` + human OK | Send the open questions | Tester → BA |
| Script FAIL | Fix the instructions, or rerun | Agent maintainer (you) |
| Script PASS + human problem | Fix the instructions; add a human-check note | Agent maintainer (you) |

Three owners, three different jobs:

- **The tester** uses accepted test cases: reviews them once more, adds any missing details, and puts them into the team's test management.
- **The BA** answers questions about the requirement. The BA owns what the requirement **means**, as you learned on Wednesday in *AI-Assisted Requirements Analysis*.
- **The agent maintainer** improves the agent: instructions, examples and checks. This week, that is you.

A single story can need **two** owners. US-311's v1 reply invented "2 seconds": that is a failure of the agent, so the maintainer fixes the instructions. But the reason the agent was tempted is that the story **is** vague. A good tester also sends the question "What is the maximum time, in seconds, for search results to appear?" to the BA straight away, without waiting for the agent to ask it. Fixing the agent and fixing the requirement are separate actions, with separate owners.

### 4. New Stories Need No New Code

The third key idea: **add a JSON file to `stories/` and run the same command.** You saw this in *Creating Reusable Prompt Templates*; this lesson relies on it. The code does not know US-313 exists until it finds the file. Then it builds the prompt, reports WAITING, and checks the reply, exactly as for every other story.

This is what makes the agent usable on a real backlog. Adding thirty stories means writing thirty small JSON files, not touching any code.

### 5. Always a New Chat per Story

The fourth key idea is one you have heard all week, and it matters most on a busy run: **always use a new chat per story**. When you have six stories to paste, it is tempting to stay in one chat. But the AI then sees the earlier stories and replies, and may let them influence the next answer, or answer the wrong story altogether. A new chat per story keeps every reply independent, which is what the checker and the comparisons assume.

A typical sign of a reused chat, **illustrative**, is a US-312 reply whose test case IDs start `TC-205-`, or whose open questions mention coupons. R1 would catch a copied `story_id`, but not a copied ID prefix or a stray question, so prevention is better than detection here.

### 6. Worked Example: Run the Agent on a New Story, US-313

#### Step 1 (Editor): Add the story

If you did not create it on Thursday, create `stories/US-313.json`:

```json
{
  "story_id": "US-313",
  "title": "Track an order",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Guests can track an order by entering its order number."},
    {"id": "AC2", "text": "An unknown order number shows \"Order not found\"."}
  ],
  "max_cases": 3
}
```

Before running anything, read the story as a tester. It has no numeric limit, one exact message (`"Order not found"`) and two clear criteria. Predict what a good reply contains: a positive case for AC1, a negative case for AC2 with the exact message, and no questions needed. Writing your prediction first is the same habit as working out expected values before reading an AI's answer, from Wednesday.

#### Step 2 (Terminal): Run the agent

```bash
python run_agent.py v1
```

US-313 shows **WAITING**, and the message says exactly what to do next:

```text
| US-313 | WAITING | paste prompts/v1/US-313.txt into your AI tool, save the reply as replies/v1/US-313.txt |
```

#### Step 3 (AI tool and Editor): Do the manual step

1. Open `prompts/v1/US-313.txt`, select everything and copy it.
2. Open a **new chat**, paste it and send.
3. Save the AI's **whole reply** as `replies/v1/US-313.txt`.

If your AI tool is not working, save this sample reply from the handout as `replies/v1/US-313.txt`:

```text
{"story_id": "US-313", "status": "ok", "test_cases": [
 {"id": "TC-313-01", "title": "Guest tracks an order with a valid order number", "ac_ids": ["AC1"], "type": "positive",
  "steps": ["Open the order tracking page as a guest", "Enter a valid order number", "Click Track"],
  "expected_result": "The order's tracking details are displayed"},
 {"id": "TC-313-02", "title": "Unknown order number", "ac_ids": ["AC2"], "type": "negative",
  "steps": ["Open the order tracking page as a guest", "Enter order number 00000000", "Click Track"],
  "expected_result": "\"Order not found\" is shown"}
], "open_questions": []}
```

#### Step 4 (Terminal): Run it again

```bash
python run_agent.py v1
```

With the sample reply, the US-313 row now reads:

```text
| US-313 | PASS | - |
```

#### Step 5 (Paper): Human checklist and triage

Apply H1 to H4 to the US-313 reply, then use the triage table to decide the action and owner. Add a row for US-313 to your `review_v1.md`.

**Answer (sample reply):**

| Check | Result | Why |
|---|---|---|
| H1 nothing invented | ✓ | "A valid order number" is not a made-up value; 00000000 is chosen test data for "an unknown order number" |
| H2 boundaries | - | No numeric limit in this story |
| H3 exact messages | ✓ | `"Order not found"` copied exactly |
| H4 right status | ✓ | The story is testable, so `"ok"` is right |

**Decision: accept; send to the tester** for review.

Compare the reply with your prediction from Step 1. It matches: one positive case, one negative case with the exact message, no questions. When a reply matches a prediction you wrote **before** reading it, you can be more confident the agent did the job, not just that it produced something plausible.

### 7. What the Tester Does with Accepted Test Cases

"Accept" does not mean "finished". It means the test cases are good enough to hand to a tester, who then does their own short review before using them. For US-313, a tester might note:

- **TC-313-01 needs real test data.** "Enter a valid order number" is fine for the agent, which cannot know the test environment's orders. But a tester needs an actual order number that exists in the test environment, and should write it into the test case.
- **TC-313-02's "00000000" should be confirmed** as not being a real order in the test environment.
- **"The order's tracking details are displayed"** is less exact than it could be. AC1 says only that guests "can track an order"; it does not say which details appear. That is not the agent's fault: the story does not say. If the team wants a more precise expected result, that is a question for the BA, perhaps for a later story.

The handout's exercise 3 asks why the tester still reviews accepted replies. These three notes are the answer. The checks confirm the reply follows the contract and the story. Only a person who knows the **test environment**, the **product** and the **team's needs** can turn the cases into tests that will actually run.

### 8. A Second New Story: a Subtler Problem

The handout's exercise 2 asks you to write a story of your own with at least one numeric limit. Here is one, **illustrative**, to show what can happen. Add it as `stories/US-314.json`:

```json
{
  "story_id": "US-314",
  "title": "Free returns",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Items can be returned free of charge within 30 days of delivery."},
    {"id": "AC2", "text": "After 30 days, the Return button is replaced by \"Return window closed\"."}
  ],
  "max_cases": 4
}
```

Running `python run_agent.py v1` adds a WAITING row, as expected:

```text
| US-314 | WAITING | paste prompts/v1/US-314.txt into your AI tool, save the reply as replies/v1/US-314.txt |
```

Suppose the AI replies like this, **illustrative**:

```text
{"story_id": "US-314", "status": "ok", "test_cases": [
 {"id": "TC-314-01", "title": "Return on day 30 after delivery", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Open an order delivered 30 days ago", "Click Return"], "expected_result": "The return is accepted with a $0.00 return fee"},
 {"id": "TC-314-02", "title": "Return on day 29 after delivery", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Open an order delivered 29 days ago", "Click Return"], "expected_result": "The return is accepted with a $0.00 return fee"},
 {"id": "TC-314-03", "title": "Day 31 after delivery", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Open an order delivered 31 days ago"], "expected_result": "\"Return window closed\" is shown instead of the Return button"}
], "open_questions": []}
```

We ran it through `check_reply`. The result: **PASS**. The ID matches, both ACs are covered, three cases are within the limit of four, and no vague words appear. It even tests both sides of the limit, and copies the AC2 message exactly.

Now the human checklist. Look closely at TC-314-01: it expects a return on **day 30** to be accepted. Does the story say that? "Within 30 days" could include day 30, or it could mean "before day 30". And AC2 says "after 30 days", which suggests day 30 is still inside the window, but that is an inference, not a statement. Even "day 30" itself is unclear: counted from the delivery date, or the day after?

| Check | Result | Why |
|---|---|---|
| H1 nothing invented | **Partly** | TC-314-01 **assumes** day 30 is included; the story does not say so clearly |
| H2 boundaries | ✓ | 29, 30 and 31 are all tested |
| H3 exact messages | ✓ | "Return window closed" copied exactly |
| H4 right status | **Questionable** | An ambiguous boundary deserves a question, even if most criteria are testable |

The reply is not wrong in an obvious way. It is a **reasonable assumption, stated as fact**, which is exactly how the lowercase-coupon rule started on Wednesday. The right triage is **two actions**: send the question "AC1: Is a return on day 30 after delivery still free, and is day 1 the delivery date or the day after?" to the BA, and note for the agent maintainer that boundaries with words like "within" or "after" should trigger a question.

Notice also what B1 asked for: "test the limit and just below it". Here the reply tested the limit (30), just below (29) **and** just above (31). For a rule that changes **after** a limit, just above is where the behaviour changes, so 31 is the most important test of all. B1 is a minimum, not a full boundary analysis. A good tester, and a good reply, may need more than the rule requires.

This kind of finding is easy to miss precisely because the reply looks **better** than most: it tests three days, not two, and copies the message exactly. Thoroughness in one place can make a reviewer relax in another. The checklist is there so that a good-looking reply gets the same four questions as a poor one.

### 9. Sending Questions to the BA

When a result goes to the BA, how you send it matters as much as what you send. Wednesday's rules for good questions apply: name the requirement, keep the question open, make it answerable with a fact. A short message, **illustrative**, for the two questions from this lesson:

```text
Hi <BA name>, two questions from test design, before we finalise test cases:

US-311 AC1 ("Search results should appear fast"):
  What is the maximum time, in seconds, for search results to appear, and on which network?

US-314 AC1 ("within 30 days of delivery"):
  Is a return on day 30 after delivery still free? Is day 1 the delivery date or the day after?

Until we hear back, tests for these criteria are on hold. Thanks!
```

Then record both questions in your question log, with the date. When the answers arrive, **update the story files**, not just your notes, and rerun the agent: the updated stories will produce new prompts automatically, and the agent's replies should no longer need to guess.

This last step closes a loop that runs through the whole week. The agent's questions improve the **requirements**; better requirements improve the agent's **replies**; and the checks confirm it.

### 10. When the BA Answers: Changing a Story

Suppose the BA replies, **illustrative**: *"US-311: results must appear within 2 seconds on the test network."* You update `stories/US-311.json`:

```json
{
  "story_id": "US-311",
  "title": "Fast search",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Search results appear within 2 seconds on the test network."}
  ],
  "max_cases": 3
}
```

Run `python run_agent.py v1`, and the prompt is rebuilt automatically: `prompts/v1/US-311.txt` now ends with the new AC1. So far, so good.

But look at the results table. We tried it, and the US-311 row still says:

```text
| US-311 | PASS | - |
```

The runner found the **old** reply in `replies/v1/US-311.txt`, the one written for "should appear fast", and checked it against the **new** story. It passes, because the old reply happens to mention 2 seconds. That PASS means nothing: the reply was never an answer to the new requirement. This is a **stale reply**: a saved result that no longer matches its input.

The runner cannot detect it, because it has no record of which story text a reply was written for. So the fix is a habit: **when a story changes, its old replies are no longer valid.** Move them out of the way (rename them to `.old`, for example), run the agent so the story shows WAITING, and do the manual step again with the new prompt.

There is a second question: should a changed story run under the **same** version? For checking one story, yes. But if you are about to compare v1 with v1.1, both versions should see the **same** story text, or the comparison is not fair. Change stories **between** comparisons, not during one. The same principle as *Building Agent Instructions*: change one thing at a time, and know exactly what changed.

### 11. Working Through a Batch

On a real team, stories rarely arrive one at a time. When several arrive together, a little planning keeps the work orderly:

1. **Add all the story files first**, and read each one as a tester before running anything. Note any story that already looks vague: it may be quicker to ask the BA now than to wait for the agent to ask.
2. **Run once** to build every prompt. The WAITING rows are your to-do list.
3. **Do all the manual steps**, one new chat per story.
4. **Run again**, then do the human checklist for every PASS.
5. **Triage the whole batch together.** Questions for the BA can go in **one** message; problems for the maintainer can be grouped by rule.

Step 5 is where batching pays off. Five stories reviewed one by one produce five separate interruptions for the BA. Reviewed together, they produce one clear message, and the maintainer sees patterns ("three stories broke M1") that a single story would not show. That pattern-finding is the start of *Agent Testing and Refinement*.

### 12. The Full Triage for the v1 Backlog

Putting the day's results together, here is the triage for every v1 sample reply, including the two new stories:

| Story | Script | Human | Action | Owner |
|---|---|---|---|---|
| US-205 | FAIL (R3, R4) | H1 ✗ (lowercase codes) | Fix the instructions | Agent maintainer |
| US-311 | PASS | H1 ✗, H4 ✗ ("2 seconds") | Fix the instructions; **also** ask the BA for the time limit | Agent maintainer; tester → BA |
| US-312 | FAIL (Q1) | H3 ✗ (AC2 message) | Fix the instructions | Agent maintainer |
| US-313 | PASS | ✓ | Accept: review and use | Tester |
| US-314 | PASS | Partly (day 30 assumed) | Ask the BA; note for the maintainer | Tester → BA; agent maintainer |

Five stories, three owners, and only **one** reply ready to use as it is. Notice that two of the five rows send something to the BA. An agent that asks good questions is improving the **requirements**, not just producing test cases, which is a real benefit even when its replies need work. That is a realistic picture of a first version. It is also good news: every problem in the table has a rule ID and an owner, which is exactly the input *Agent Testing and Refinement* needs next.

### 13. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| US-313 does not appear in the results | The story file is not in `stories/` or does not end in `.json` | Check the folder and the file name |
| The AI answered about US-205 instead | You pasted into an old chat | Always use a **new chat** per story |
| `KeyError: 'max_cases'` | The story file has no `max_cases` | Add it, as in Step 1 |
| Test case IDs from another story appear in a reply | The chat was reused, or an example leaked | Use a new chat per story; check IDs against the story number |
| A PASS was sent straight to the tester | The human checklist was skipped | Every PASS gets the human checklist before triage |
| A changed story still shows PASS | An old reply, written for the old story text, is still saved | Move old replies aside when a story changes, and rerun |
| A question went to the maintainer, not the BA | The problem was in the requirement, not the agent | Ask: is the agent wrong, or is the story unclear? Often both |

---

## Practice Exercises

1. **Compare with the sample (AI tool, 10 min).** Compare your AI's US-313 reply with the sample. Did your AI invent anything, such as an order number format or a time limit? Apply H1 to H4 and triage it.

2. **Your own story (editor, terminal and AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** write a story of your own, from Project 2 or invented, with at least one numeric limit. Add it to `stories/`, run the agent, and do the manual step.
   - **Review:** apply the script and the human checklist. Look especially for assumptions about the boundary, as in section 8.
   - **Run:** rerun `python run_agent.py v1` and record the result.
   - **Record:** add a row to `review_v1.md`, with the action and the owner.

3. **Why review accepted replies? (paper, 10 min).** For your own story, would you trust the test cases without reading them? Explain why the tester still reviews accepted replies, using section 7.

4. **Write the BA message (paper, 10 min).** For any question your agent raised, or any assumption you found, write a short message to the BA using section 9 as a model. Check it against Wednesday's rules for good questions.

5. **A stale reply (editor and terminal, 10 min).** Make a copy of `stories/US-311.json`, then change AC1 to *"Search results appear within 2 seconds on the test network."* Run `python run_agent.py v1`. What does the US-311 row say, and why is it misleading? Restore the original story afterwards, and rerun.

---

## Knowledge Check

1. What are the steps of executing the agent end to end?

<details><summary>Answer</summary>

Add the story, run `run_agent.py` (WAITING), paste the prompt into a new chat and save the reply, run `run_agent.py` again (PASS or FAIL), apply the human checklist, and decide the action and owner.

</details>

2. Who owns each kind of result?

<details><summary>Answer</summary>

Accepted test cases: the tester. Open questions: the tester, who sends them to the BA. Script failures and human-found problems: the agent maintainer.

</details>

3. Why does adding US-313 need no new code?

<details><summary>Answer</summary>

The code finds every story file in `stories/`. Adding a JSON file is enough; the same command builds, reports and checks it.

</details>

4. In the US-313 reply, is "00000000" an invented value?

<details><summary>Answer</summary>

No. It is chosen test data for "an unknown order number". A tester should still confirm it is not a real order in the test environment.

</details>

5. The US-311 v1 reply invented "2 seconds". Why does the triage give it two owners?

<details><summary>Answer</summary>

The agent failed, so the maintainer fixes the instructions. The story is also vague, so the tester asks the BA for the time limit. Fixing the agent and fixing the requirement are separate actions.

</details>

6. The US-314 reply passed the script. What did the human review find?

<details><summary>Answer</summary>

TC-314-01 assumes a return on day 30 is free, but "within 30 days" is ambiguous. It is a reasonable assumption stated as fact, so a question should go to the BA.

</details>

7. Why is the day-31 test the most important one for US-314?

<details><summary>Answer</summary>

The behaviour changes after the limit, so just above it is where the Return button should be replaced. B1 asks for the limit and just below; a full boundary analysis needs more.

</details>

8. Why does a tester still review test cases the agent produced and the checks accepted?

<details><summary>Answer</summary>

Only a person who knows the test environment, product and team can add real test data, confirm assumptions and turn the cases into tests that will actually run.

</details>

9. You update US-311 with the BA's answer, and the old reply still shows PASS. What is wrong, and what do you do?

<details><summary>Answer</summary>

The reply is stale: it was written for the old story text. Move it aside so the story shows WAITING, then run the new prompt in a new chat and save the new reply.

</details>

---

## Glossary

- **Executing the agent:** running it end to end on real requirements and acting on the results.
- **Triage:** deciding the action and owner for each result.
- **Owner:** the person responsible for the next action on a result.
- **Prediction (before review):** writing down what a good reply should contain before reading the agent's reply, so the review is not anchored by it.
- **Agent maintainer:** the person who improves the agent's instructions, examples and checks.
- **Backlog:** the list of stories waiting to be worked on.
- **Assumption stated as fact:** a reasonable guess written as if the story said it, such as "day 30 is included".
- **Question log:** a record of questions sent to the BA, with dates and answers.
- **Stale reply:** a saved reply that no longer matches its story, because the story has changed since.
- **Batch:** several stories worked on together, from adding the files to triage.
- **Full boundary analysis:** testing just below, on and just above a limit, as needed by the rule.

---

## Summary

- **Executing the agent** means running it end to end and **deciding what happens next**.
- **Triage** gives every result an **action and an owner**: tester, BA or agent maintainer. One story can need two.
- **New stories need no code**: add a JSON file and run the same command. Always use a **new chat** per story.
- US-313 passed both layers and went to the tester. US-314 **passed the script** but **assumed** a boundary the story does not state clearly, so a question goes to the BA.
- **Accepted is not finished**: a tester still reviews the cases, adds real test data and confirms assumptions.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (boundary value analysis and the test process): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- OpenAI, *A practical guide to building agents* (PDF; human intervention): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Agile Alliance, *INVEST* glossary entry (testable stories): https://agilealliance.org/glossary/invest
