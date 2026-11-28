# Agent Architecture

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** an AI agent, and explain how it differs from a one-off prompt.
- **Name** the six parts of our agent, TestCaseDesigner, and say what each part is for.
- **Describe** how the agent runs this week: which steps code does and which step you do in your AI tool.
- **Match** common problems with one-off prompts to the agent part that fixes each one.
- **Design** the six parts for a different one-job QE agent.

---

## Why This Matters

On Monday to Wednesday you used AI one prompt at a time. You typed a request, read the reply, checked it, and moved on. That works well for a single task. It works badly when the same task comes up again and again, which is how most testing work looks: a new user story arrives every few days, and each one needs test cases.

Try the same prompt twice and you have already seen the problem. On Tuesday, in *Common Prompt Failure Modes*, two runs of one prompt gave different numbers of test cases, in different formats, with different assumptions. If you cannot predict the shape of the answer, you cannot check it with code, and you cannot compare this week's results with last week's.

An **agent** is the fix. Instead of writing a fresh prompt each time, you build a **package** once: fixed instructions, a fixed input shape, a fixed output format, examples and checks. Then you reuse it for every story.

Agents are one of the fastest-growing areas of AI, and the word is used loosely.

OpenAI's guide for teams building agents defines them as **systems that independently accomplish tasks on your behalf**, and says every agent has three core parts: a **model**, **tools** and **instructions** ([OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)). Anthropic, which builds the Claude models, draws a useful line between **workflows**, where models and tools follow **predefined code paths**, and **agents**, which direct their own steps ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents)). 

By Anthropic's definition, what we build this week is closer to a workflow: our code decides every step. In this course we use "agent" in the broader everyday sense: **an AI model set up to do one job the same way every time.** Both guides also warn against adding complexity you do not need, and suggest that a simpler, more predictable approach is often enough. That is exactly where we start.

> **Using this with the handout:** this lesson goes deeper into **Handout 07, Topic 1**. It uses the same one-off prompt for US-205, the same six parts, the same "how our agent runs" diagram, the same Step 3 answer key and the same folder plan.

---

## The Concept

### 1. What Is an AI Agent?

An **AI agent**, in this course, is an AI model set up to do **one specific job, the same way every time**. It is a package of:

- fixed **instructions**,
- an **input template** that you fill with new data each time,
- a fixed **output format**,
- a few **examples** of good answers,
- and **checks** that test every answer.

Our agent is called **TestCaseDesigner**. It has one job: **turn one user story into test cases in a fixed JSON format.**

Notice what the definition does **not** include. An agent is not a different, smarter AI model. It uses the same ChatGPT, Copilot or Claude you have used all week. What changes is everything **around** the model: what you send it, what you expect back, and how you check the result. Building an agent is mostly **careful writing and checking**, not heavy programming. Today's lessons contain no code you need to run.

### 2. One-Off Prompt vs Agent

The handout's comparison:

| | One-off prompt | Agent |
|---|---|---|
| Written | Fresh each time | Once, then reused |
| Instructions | Whatever you remember to type | The same tested instructions every run |
| Answer format | Different every time | Fixed (JSON), so code can read it |
| Checked? | By eye, if at all | Every answer, by a script and a person |

Read the last row as a tester. The real gain of an agent is not that it writes better test cases. It is that its answers are **checkable**. A fixed format means code can check every answer in the same way. Fixed instructions mean a mistake can be traced to a specific rule and fixed once, for every future story.

An analogy helps. A one-off prompt is like asking a colleague for help in a corridor: useful, but they will answer differently each time, and nobody writes down what was agreed. An agent is like a **standard operating procedure** with a form to fill in: the same steps, the same form, the same review, every time. You trade a little flexibility for a lot of predictability.

### 3. The Six Parts of Our Agent

TestCaseDesigner has six parts. Each one is a file, or part of a file, in your `agent` folder:

| Part | What it does | File in your `agent` folder | Built on |
|---|---|---|---|
| **Role and goal** | Tells the AI who it is and its one job | Top of the instructions | Thursday |
| **Instructions (rules)** | What it must always or never do | `instructions_draft.md`, later `instructions_v1.md` | Thursday, Friday |
| **Input template** | The fixed shape every story is sent in | `input_template.txt` | Thursday |
| **Output format** | The exact JSON it must reply with | Part of the instructions, defined in `contract.md` | Thursday |
| **Examples** | Good answers to copy the pattern from | `examples.txt` | Thursday |
| **Checks** | Code and human review of every answer | `check_reply.py` plus a checklist | Friday |

Each part answers a question the AI would otherwise have to guess:

| Part | The question it answers for the AI |
|---|---|
| Role and goal | Who am I, and what is my one job? |
| Instructions | What must I always do, and never do? |
| Input template | Where in this message is the story, and what are its parts? |
| Output format | What exactly should my answer look like? |
| Examples | What does a good answer look like in practice? |
| Checks | (Not for the AI.) How will people know whether this answer is good? |

The last row is different from the others. Checks are not sent to the AI at all. They are for **you**: they turn "it looks fine" into "it passed these rules". You have done this kind of checking all week, with `review_cases.py` and `check_users.py` on Wednesday. Tomorrow you will write a checker for the agent's replies.

Four of the six parts are about **reducing guessing**. Every time the AI has to guess, it might guess differently, or wrongly. The rest of today's lessons are about removing guesses, one part at a time.

### 4. How Our Agent Runs This Week

In a fully automated agent, code sends each prompt to an AI model and collects the reply. This week we keep one step **manual**: **you** talk to the AI, in your normal chat tool. Code does everything else:

```text
stories/*.json ──► [CODE] build one prompt per story ──► prompts/v1/US-205.txt
                                                               │
                                 🤖 YOU paste it into your AI tool (new chat)
                                                               │
                   replies/v1/US-205.txt ◄── 📝 YOU save the AI's reply
                             │
            [CODE] check every reply ──► [CODE] write a results table ──► 👀 YOU review
```

Follow one story through the diagram:

1. **A story file** (`stories/US-205.json`) holds the story as data. You will write these files in *Input/Output Contracts*.
2. **Code builds the prompt**: it combines the instructions, the examples and the story into one text file, ready to paste. You will build this tomorrow.
3. **You paste** that prompt into a **new chat** in your AI tool.
4. **You save** the AI's reply into a text file.
5. **Code checks the reply** against the rules in your contract, and **writes a results table**.
6. **You review** the results, including the things only a person can check.

Why keep the AI step manual? Three reasons. Everyone can follow along with whichever AI tool they have, with no accounts or keys to set up. You **see** every prompt and reply, which is the best way to learn what the agent actually does. And it keeps a person in the loop at the riskiest step, which is a habit from Wednesday's *Human Validation of AI Output*. Next week, one small piece of code can replace the two "YOU" steps, and the agent will run on its own.

### 5. One Agent, One Job

The handout's rule is short: **one agent, one job.** "Design test cases for one story" is a good job. "Do all our testing" is not.

| Job | Good agent job? | Why |
|---|---|---|
| Turn one user story into test cases | ✅ Yes | Clear input, clear output, easy to check |
| Turn one bug description into a structured bug report | ✅ Yes | Same reasons |
| Review one story and list questions for the BA | ✅ Yes | You did this by hand on Wednesday |
| "Improve our test coverage" | ❌ No | No clear input; no clear way to check the result |
| "Test the checkout" | ❌ No | Many jobs in one; impossible to check as a whole |

A small job has three advantages, and they are the same ones that make a small test case better than a large one:

- **Easy to check.** You can write rules for "test cases for one story". You cannot write rules for "improve coverage".
- **Easy to improve.** When a reply is wrong, there are only a few places the mistake can come from.
- **Easy to combine.** Several small agents can be chained later, each one checkable on its own.

### 6. Worked Example: From a One-Off Prompt to an Agent

The stories for this part of the week, from the handout:

| Story | Title | Acceptance criteria | Why it is useful |
|---|---|---|---|
| **US-205** | Apply coupon at checkout | AC1: SAVE10 gives 10% off a subtotal of $50.00 or more. AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10". AC3: Unknown codes show "Coupon code not recognised". AC4: Only one coupon per order. | Our running example: a boundary, exact messages, and an incomplete AC (AC4) |
| **US-311** | Fast search | AC1: Search results should appear fast. | Too vague to test: "fast" has no number |
| **US-312** | Free gift wrap | AC1: Orders of 10 or more items get free gift wrap. AC2: Orders under 10 items show "Add 10 items for free gift wrap". | A boundary with whole numbers (10 vs 9) |

#### Step 1 (AI tool): Try a one-off prompt

Open a **new chat** and paste:

```text
Write test cases for this user story.

US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

Read the reply. Note **how many** test cases it gave and **what format** it used: a list, a table, paragraphs?

#### Step 2 (AI tool): Run it again

Open **another new chat** and paste exactly the same text. Compare the two replies.

The handout's checkpoint describes what most students see: different numbers of test cases (often 6 to 15), different formats, and at least one run that **assumes** something about AC4, for example "the second coupon replaces the first". That assumption is an invented rule, exactly like the lowercase-coupon rule you traced through the lifecycle on Wednesday.

None of this means the AI is broken. A one-off prompt simply leaves too much open: how many cases, in what shape, what to do with gaps. Each reply fills those gaps differently. That is the problem an agent solves.

#### Step 3 (Paper): Match the problems to the agent parts

For each problem from Steps 1 and 2, write which agent part from section 3 would fix it. Then compare with the answer key:

| Problem in Steps 1–2 | Fixed by |
|---|---|
| Different format each time | **Output format** (a fixed JSON shape) |
| Different number of test cases | **Instructions** (a rule like "at most 5") and the **input template** (states the maximum) |
| Invented behaviour for AC4 | **Instructions** ("don't guess; ask a question") and **examples** showing how to ask |
| No way to know if the answer is good | **Checks** (a script plus a human checklist) |

Notice that some problems need **two** parts working together. A rule saying "never return more than the maximum" only works if the input says what the maximum is. A rule saying "ask instead of guessing" works much better when an example **shows** a question being asked. The parts are designed to support each other.

#### Step 4 (Editor): Plan your agent folder

Your `agent` folder will grow over Thursday and Friday. Copy this plan into a file called `README.txt` in the folder, so you always know what goes where:

```text
agent/
├── instructions_draft.md   (Thursday)  first version of the instructions
├── input_template.txt      (Thursday)  the shape every story is sent in
├── contract.md             (Thursday)  what goes in and what must come out
├── examples.txt            (Thursday)  two good example answers
├── stories/                (Thursday)  the stories, one JSON file each
├── instructions_v1.md      (Friday)    the finished instructions
├── build_prompts.py        (Friday)    code: builds one prompt per story
├── check_reply.py          (Friday)    code: checks one AI reply
├── prompts/  replies/      (Friday)    prompts to paste / replies you save
├── run_agent.py            (Friday)    code: runs everything and records results
├── results_v1.md           (Friday)    results table written by run_agent.py
└── instructions_v1.1.md    (Friday)    improved instructions, plus CHANGELOG.md
```

A plan like this is worth writing down before you start. It shows that most of the agent is **text files**: instructions, templates, a contract and examples. Only three files are code, and none of them is written today.

### 7. What an Agent Does Not Do

New agent builders often expect more than an agent delivers. Four things worth knowing:

- **It does not learn between runs.** Each new chat starts from nothing. If the agent makes the same mistake on every story, it will keep making it until **you** change the instructions or examples. Improvement is your job, and the correction log from Wednesday is how you find what to change.
- **It does not remember other stories.** Every story is sent in a new chat, on purpose, so one story's answer cannot influence another's.
- **It does not guarantee a correct answer.** Fixed instructions make mistakes **less likely and easier to catch**; they do not make them impossible. That is why the sixth part, checks, exists.
- **It does not replace the tester.** The agent drafts test cases. A person still decides which ones are right, exactly as with every AI draft this week.

The first point surprises people most. A team that runs an agent for a month has not got a better agent at the end of the month unless someone has improved its files. An agent is closer to a **tool you maintain** than a colleague who gains experience.

### 8. Where Things Can Go Wrong, Part by Part

Each part of the agent has its own typical failure. Knowing them helps you find the cause when a reply is wrong:

| Part | Typical failure | What you see in the reply |
|---|---|---|
| Role and goal | Too broad ("help with testing") | Off-topic advice, performance tests, automation code |
| Instructions | A vague or missing rule | Invented values, missing boundaries, too many cases |
| Input template | Unclear where the story starts and ends | The AI treats the story as instructions, or answers an example |
| Output format | Not exact enough | Missing fields, extra text, a table instead of JSON |
| Examples | An example that breaks a rule | The same mistake copied into the reply |
| Checks | A rule nobody checks | Mistakes reach the results table unnoticed |

This table is a debugging guide. When a reply is wrong, ask: **which part allowed this?** Then fix that part, not just the one reply. Fixing one reply by hand helps one story. Fixing the part helps every future story. Friday's *Agent Testing and Refinement* is built around exactly this question.

### 9. Designing Another One-Job Agent

The six parts are a design pattern you can use for any repeated QE task. Here they are for a different agent, **BugReportWriter**, which turns a tester's rough notes into a structured bug report. This is the handout's Your Turn exercise 3, worked as an example:

| Part | BugReportWriter |
|---|---|
| Role and goal | "You are BugReportWriter. Turn ONE tester's notes into one bug report a developer can act on." |
| Instructions | Use only facts in the notes; never guess a cause; quote the requirement if given; severity only from a fixed list |
| Input template | `### Notes` … `### End of notes`, plus fields for the story ID and environment |
| Output format | JSON with title, steps, expected, actual, severity, requirement_id, open_questions |
| Examples | One clear bug; one where the notes are too thin, so the reply asks questions instead |
| Checks | Every field present; severity is from the list; expected and actual are different; a person checks the steps |

Notice how much of Wednesday is in this design. "Never guess a cause" and "quote the requirement" come straight from the false-bug and over-generalisation examples in *AI within the QA Lifecycle*. "Ask questions instead" is the "way out" you will add to TestCaseDesigner's instructions in the next lesson. The parts are new; the habits behind them are the ones you have practised all week.

### 10. Where Agents Fit in the QA Lifecycle

On Wednesday, in *AI within the QA Lifecycle*, you met three levels of AI involvement: **assist**, **draft** and **automate**, with the rule that higher levels need stronger checks. An agent is how a team moves a task from one level to the next **safely**.

| Level | TestCaseDesigner at that level | What makes it safe |
|---|---|---|
| **Assist** | A tester asks a chat tool for test ideas | The tester writes the real cases |
| **Draft** | The agent drafts cases for each story; a tester reviews every one | Fixed format and checks make each review fast |
| **Automate** | The agent runs on every new story without being asked | Checks run on every reply; a person reviews the results table |

This week we build the agent at the **draft** level: you see every prompt and every reply. That is deliberate. Nobody should automate a task before they have watched it work at the draft level and know which mistakes it tends to make. The correction log from *Human Validation of AI Output* is how you find out: if the agent's replies keep passing review with few edits, you have evidence for moving up a level. If they keep needing the same correction, you know which part to fix first.

The agent also changes **where** in the lifecycle the checks happen. With a one-off prompt, checking happens at the end, by eye. With an agent, a script checks every reply as soon as it is saved, at the hand-over between test design and everything after it. That is the "check at every hand-over" idea from Wednesday, built into the tool.

### 11. When a One-Off Prompt Is Good Enough

Building an agent takes effort: instructions, a template, a contract, examples and a checker. That effort is worth it only when the job **repeats**. A simple way to decide:

| Situation | Better choice | Why |
|---|---|---|
| A one-time question ("explain this error message") | One-off prompt | Nothing to reuse |
| A task you do a few times, differently each time | One-off prompt, saved in `prompts.txt` | A saved prompt is enough |
| The same task on many inputs, needing the same output shape | **Agent** | Consistency and checks pay back the setup time |
| Results that other people or code depend on | **Agent** | A fixed contract protects everyone downstream |

This matches the advice in both agent guides: do not add complexity you do not need. Your `prompts.txt` file from this week is the first step on that path: a saved, reusable prompt is halfway to an agent. TestCaseDesigner is the next step: the same idea, with a fixed format and automatic checks, for a job that comes up with every new story.

### 12. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Both runs in Step 2 look identical | You used the same chat, so the AI remembered the first answer | Always use a **new chat** for a fair comparison |
| The AI asks "What platform is this for?" | It is missing context | That is fine; note it. Agents remove this by giving context in the instructions |
| The agent's job keeps growing | "While it's at it, it could also..." | Keep one job per agent. Start a second agent instead |
| You expect the agent to improve by itself | It does not learn between runs | Improve its files using what the checks and your reviews find |

---

## Practice Exercises

1. **Compare tools (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** run the Step 1 prompt in your AI tool.
   - **Review:** count the test cases, note the format, and check for any invented AC4 behaviour.
   - **Run:** compare with a classmate who used a **different** AI tool, or run it yourself in a second tool.
   - **Record:** in `prompts.txt`, list two differences between the replies, and which agent part would remove each one.

2. **Explain the run (paper, 10 min).** Using section 4, explain in your own words which steps **code** will do and which steps **you** will do this week, and why the AI step is manual for now.

3. **Design your own agent (paper, 15 min).** Think of another one-job agent that would help a tester, for example "turn a failing test log into a short failure summary". Fill in the six parts for it, one line each, using section 9 as a model. Then answer: what is the one thing a person must still check?

4. **Spot the bad job (paper, 5 min).** For each job, say whether it is a good single job for an agent and why: (a) "Write release notes for this sprint"; (b) "Turn one acceptance criterion into Given/When/Then form"; (c) "Make our tests better"; (d) "List the ACs in one story that have no test case".

---

## Knowledge Check

1. What is an AI agent, as defined in this course?

<details><summary>Answer</summary>

An AI model set up to do one specific job the same way every time, with fixed instructions, an input template, a fixed output format, examples and checks.

</details>

2. Name the six parts of our agent.

<details><summary>Answer</summary>

Role and goal, instructions (rules), input template, output format, examples and checks.

</details>

3. Which part of the agent is never sent to the AI, and why does it exist?

<details><summary>Answer</summary>

The checks. They are for people: a script and a human checklist that decide whether each reply is good.

</details>

4. In this week's agent, which steps do you do, and which does code do?

<details><summary>Answer</summary>

You paste each prompt into a new chat in your AI tool and save the reply. Code builds the prompts, checks the replies and writes a results table, which you then review.

</details>

5. Two runs of the same one-off prompt gave 7 and 12 test cases. Which agent parts fix this?

<details><summary>Answer</summary>

The instructions (a rule limiting the number of cases) and the input template (which states the maximum for each story).

</details>

6. Your agent makes the same mistake on every story for a week. Will it improve by itself? What should you do?

<details><summary>Answer</summary>

No. An agent does not learn between runs. Find which part allows the mistake, such as a vague rule or a bad example, and change that file.

</details>

7. By Anthropic's definitions, is TestCaseDesigner closer to a workflow or an agent? Why?

<details><summary>Answer</summary>

Closer to a workflow, because our code decides every step in a fixed order. The course uses "agent" in a broader sense: a model set up to do one job the same way every time.

</details>

8. When is a saved one-off prompt good enough, and when is it worth building an agent?

<details><summary>Answer</summary>

A saved prompt is enough for occasional tasks that vary. An agent is worth building when the same job repeats on many inputs, needs the same output shape, or feeds results that other people or code depend on.

</details>

---

## Glossary

- **AI agent (in this course):** an AI model set up to do one job the same way every time, with fixed instructions, format, examples and checks.
- **One-off prompt:** a prompt typed fresh for a single answer.
- **TestCaseDesigner:** the agent built this week; it turns one user story into test cases in a fixed JSON format.
- **Role and goal:** the part of the instructions that says who the AI is and what its one job is.
- **Input template:** the fixed shape every story is sent in, with placeholders for the data.
- **Output format:** the exact shape every reply must have.
- **Examples:** sample answers the AI copies the pattern from.
- **Checks:** code and human review applied to every reply.
- **Workflow (Anthropic's sense):** a system where models and tools follow predefined code paths.
- **Agent (Anthropic's sense):** a system where the model directs its own steps and tool use.
- **One agent, one job:** the design rule that each agent should have a single, checkable job.

---

## Summary

- An **agent** is a reusable package for **one job**: instructions, input template, output format, examples and checks.
- Its main benefit is **checkable answers**: the same shape every time, so code and people can review every reply the same way.
- This week, **code** builds prompts, checks replies and records results; **you** run each prompt in a new chat and save the reply.
- Most problems with one-off prompts map to a specific agent part. When a reply is wrong, ask **which part allowed it**, and fix that part.
- An agent **does not learn by itself**. You improve it by changing its files.

---

## Additional Resources

- Anthropic, *Building effective agents*: https://www.anthropic.com/engineering/building-effective-agents
- OpenAI, *A practical guide to building agents* (PDF): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- OpenAI Developers, *Building agents* learning track: https://developers.openai.com/tracks/building-agents
