# Week 08 · Lecture 01: What Is AI?

**Topics:**

1. [AI, Machine Learning and Deep Learning](#topic-1)
2. [Supervised vs. Unsupervised Learning](#topic-2)
3. [Neural Network Fundamentals](#topic-3)

---

## Before Class

> **Setup checklist (5 minutes, do this before the lecture starts)**
>
> 1. Open your AI assistant in a browser tab: **ChatGPT, Copilot Chat or Claude**. Any of them works. Copilot users in VS Code: use the **chat panel**, not inline suggestions.
> 2. Have a pen and paper (or a blank text file) ready. Some activities ask you to work something out **before** you ask the AI.
> 3. Optional: check Python is installed with `python --version` (on Windows you can also try `py --version`). Topic 3 has one tiny optional script that uses standard Python only.
>
> **Optional:** to run the demo script in Topic 1 yourself, install scikit-learn: `python -m pip install scikit-learn`.

---

## How to Use This Handout

Today you **don't write ML code**. You use your AI assistant as a **lab partner** to see how machines learn, and then you **check its work** against an answer key. Checking AI output is the most important skill of this whole week, so we start on day one.

Each topic has the same parts:

| Part | What you do |
|---|---|
| **Definition** | Read it. This is the one thing to remember. |
| **Key ideas** | The 3–4 points the lecture is built around. |
| **Worked example** | Follow the numbered steps. Most steps give you a **prompt** to paste into your AI assistant, or something to work out yourself. |
| **Checkpoint** | An **answer key** and a checklist to mark your AI's answer. |
| **Your turn** | Exercise 1 is done **in class** (about 3 minutes). The rest are for **after class**. |
| **Common problems** | Read these if something goes wrong. |

> **About AI answers:** ChatGPT, Copilot and Claude each answer differently, and even the same tool gives a different answer each time. Don't expect to match a classmate word for word. Check that your AI's answer contains the right **things**, using the checklist.
>
> **If your AI tool isn't working,** each checkpoint includes a **sample AI answer** you can mark instead.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Explain the difference between **AI, Machine Learning (ML) and Deep Learning (DL)** using the "nested circles" picture.
- Explain how a **hand-written rule** differs from a rule **learned from examples**, and why we test a learned rule on **new** data.
- Explain what **Generative AI** is, how it differs from the **predictive** ML in today's examples, and why every GenAI answer needs checking.
- Tell **supervised** learning (we have the answers) apart from **unsupervised** learning (we don't).
- Work out what a single **neuron** does, and explain in plain words how a network **learns**.

---

<a id="topic-1"></a>

# Topic 1: AI, Machine Learning and Deep Learning

## Definition

**Artificial Intelligence (AI)** is any technique that makes a computer do something we'd call "intelligent", such as deciding, recognising or predicting. **Machine Learning (ML)** is a part of AI where the computer **learns the rules from examples** instead of a person writing every rule by hand. **Deep Learning (DL)** is a part of ML that uses **neural networks with many layers**, and it is very good with messy data like text, images and speech. **Generative AI (GenAI)** is a part of deep learning that **creates new content**, such as text, code, test cases and images, instead of only predicting a label or a number. ChatGPT, Copilot and Claude are Generative AI tools, and they are the **main focus of this week**.

## Key Ideas

1. **Three nested circles.** Every DL system is ML, and every ML system is AI. The reverse is not true.

   ```text
   +-----------------------------------------------------+
   |  ARTIFICIAL INTELLIGENCE  (any "smart" behaviour)   |
   |   +---------------------------------------------+   |
   |   |  MACHINE LEARNING  (learns from examples)   |   |
   |   |   +-------------------------------------+   |   |
   |   |   |  DEEP LEARNING  (many-layered NNs)  |   |   |
   |   |   |   +-----------------------------+   |   |   |
   |   |   |   |  GENERATIVE AI (e.g. LLMs)  |   |   |   |
   |   |   |   +-----------------------------+   |   |   |
   |   |   +-------------------------------------+   |   |
   |   +---------------------------------------------+   |
   +-----------------------------------------------------+
   ```

   **Use cases at each level.** Each row shows things that belong to that circle but **not** to the smaller circles inside it:

   | Level | What makes it this level | Everyday use cases | Testing (QE) use cases |
   |---|---|---|---|
   | **AI (rule-based, no learning)** | People write all the rules; nothing is learned from data | A classic chess program that searches through possible moves · A bank rule that blocks any card payment over $5,000 made abroad | A script that runs only the checkout tests when files in `/checkout` change · A log alert that pages the on-call engineer if "ERROR" appears 5 times in a minute |
   | **Machine Learning** | Learns patterns from labelled data, usually tables of numbers and categories | Fraud scores learned from millions of past transactions · "Customers who bought this also bought…" recommendations | Predicting which failed tests are flaky (today's worked example) · Ordering a regression suite so the tests most likely to fail run first, learned from past runs |
   | **Deep Learning** | ML with many-layered neural networks; handles messy data such as images, sound and free text | Face unlock on a phone · Speech-to-text in voice assistants | Reading the total from a screenshot of a receipt (OCR) to check it · Sorting thousands of crash screenshots by the kind of error shown |
   | **Generative AI** | Deep learning that **creates** new content | ChatGPT, Copilot or Claude drafting an email · Generating an image from a text description | Drafting test cases from a user story · Explaining a long failing stack trace in plain English |

   > Remember the circles: the fraud-score model is ML **and** AI; a face-unlock model is DL **and** ML **and** AI. A rule-based script is AI, but **not** ML, because nothing was learned from data.

2. **Rules vs. learning.** In normal programming, **a person writes the rules**. In ML, **the computer finds the rules** by looking at examples that come with the correct answers.

   | | Traditional programming | Machine learning |
   |---|---|---|
   | You give the computer | Rules + data | Data + correct answers |
   | The computer gives you | Answers | **Rules** (a "model") |
   | Good when | Rules are clear and stable | Rules are fuzzy or hard to write down |

3. **ML vocabulary you'll hear all week:**

   | Word | Plain meaning | Testing example |
   |---|---|---|
   | **Feature** | One piece of information about an example | "Did the test pass on retry?" |
   | **Label** | The correct answer for an example | "Flaky" or "Real defect" |
   | **Training** | Learning a rule from labelled examples | Studying 12 past failures |
   | **Model** | The rule that was learned | "If the code didn't change and…" |
   | **Prediction** | Using the rule on new data | "Failure 13 is probably flaky" |

4. **Always test on new data.** A rule can look perfect on the examples it learned from and still fail on new ones. Testers ask: *"Accuracy measured on what data?"*

5. **Generative AI: the focus of this week.** Most of today's examples are **predictive** ML: the model picks an answer from a fixed set (flaky or real defect, pass or fail). Generative AI **writes something new**.

   | | Predictive ML (today's worked example) | Generative AI (ChatGPT, Copilot, Claude) |
   |---|---|---|
   | What it produces | A label or a number: "Flaky" | New content: a paragraph, a test case, code, an image |
   | How you use it | Give it features, get a prediction | Write a request in plain language (a **prompt**) |
   | Trained on | Labelled examples for **one** task | Huge amounts of text and code, so it can do **many** tasks |
   | How you check it | Compare with the correct label | Read it against the requirement. There's no single "correct" answer |

   **How it works, in one sentence:** a GenAI tool is built on a **Large Language Model (LLM)**, a very large deep-learning model that writes its answer one word at a time by predicting the most likely next word. You'll see this happen in Lecture 02.

   **What it can do for testers:**

   - Read a user story and point out vague or missing requirements
   - Draft test cases, test data and bug reports in seconds
   - Write and explain automation code, and help debug failures
   - Summarise long logs and test results

   **The catch:** GenAI writes text that **sounds** right, but it doesn't check facts. It can be confidently wrong: inventing a rule, a number or a function that doesn't exist. This is called a **hallucination**. That's why the habit you start in this lecture (**ask the AI, then check its answer**) runs through the whole week, until you build your own AI agent that checks its output automatically.

## Worked Example: Flaky Test or Real Defect?

**The problem:** a test failed. Was it **flaky** (random, the code is fine) or a **real defect** (the code is broken)? We have 12 past failures that a tester already investigated (the **training data**), and 4 new ones that we want to predict (the **test data**).

**Training data** (12 past failures, with labels):

| # | Passed on retry? | Code changed just before? | Timing spread (seconds) | Label |
|---|---|---|---|---|
| 1 | Yes | No | 1.0 | Flaky |
| 2 | Yes | No | 1.5 | Flaky |
| 3 | Yes | No | 2.0 | Flaky |
| 4 | No | No | 5.0 | Flaky |
| 5 | No | Yes | 4.5 | Flaky |
| 6 | No | No | 6.0 | Flaky |
| 7 | Yes | Yes | 0.5 | Real defect |
| 8 | No | Yes | 0.5 | Real defect |
| 9 | No | Yes | 1.0 | Real defect |
| 10 | No | No | 0.5 | Real defect |
| 11 | No | Yes | 2.0 | Real defect |
| 12 | Yes | Yes | 2.0 | Real defect |

**Test data** (4 new failures, **no labels**; the answers are in the Checkpoint):

| # | Passed on retry? | Code changed just before? | Timing spread (seconds) |
|---|---|---|---|
| 13 | Yes | No | 0.8 |
| 14 | No | Yes | 1.5 |
| 15 | No | No | 5.5 |
| 16 | Yes | Yes | 1.0 |

*Timing spread* = how much the test's run time varies between runs. A big spread often means timing problems.

### Step 1: Be the rule-writer (traditional programming)

Many teams start with this simple rule: **"If it passed on retry, it's flaky. Otherwise it's a real defect."**

Apply it to rows 1–12 on paper. For each row, write your prediction and tick it if it matches the label. **How many of the 12 does the rule get right?**

**What to notice:** a rule written by a person is quick, but it can miss patterns hidden in the data. Look at rows 4–6: they're flaky even though they **didn't** pass on retry.

### Step 2: Let the AI find a rule (learning from examples)

Paste this into a **new chat** in your AI assistant:

```text
Here are 12 past test failures that a tester investigated.
Columns: passed_on_retry, code_changed, timing_spread_seconds, label

1. Yes, No, 1.0, Flaky
2. Yes, No, 1.5, Flaky
3. Yes, No, 2.0, Flaky
4. No, No, 5.0, Flaky
5. No, Yes, 4.5, Flaky
6. No, No, 6.0, Flaky
7. Yes, Yes, 0.5, Real defect
8. No, Yes, 0.5, Real defect
9. No, Yes, 1.0, Real defect
10. No, No, 0.5, Real defect
11. No, Yes, 2.0, Real defect
12. Yes, Yes, 2.0, Real defect

Find ONE simple rule (at most 2 conditions) that separates Flaky from Real defect.
Write the rule in one sentence. Then say how many of the 12 rows your rule gets right.
```

**What this does:** the 12 rows are **labelled examples**: features plus the correct answer. The AI looks for a pattern that explains the labels. That's the core idea of ML: **examples in, rule out**.

### Step 3: Check the AI's claim yourself

The AI told you how many rows its rule gets right. **Don't believe it yet.** Apply its rule to rows 1–12 on paper and count for yourself.

**What to notice:** chat AIs often **state** a result without really checking it. If its count was wrong, you've just caught your first AI mistake of the week.

### Step 4: Predict new data (the real test)

In the **same chat**, paste:

```text
Now use your rule to predict these 4 NEW failures. Answer with only the row number and Flaky or Real defect.
13. Yes, No, 0.8
14. No, Yes, 1.5
15. No, No, 5.5
16. Yes, Yes, 1.0
```

Mark the AI's answers with the answer key in the Checkpoint. Do the same for your Step 1 human rule.

**Why this matters:** getting the training rows right proves very little, because the rule was **made** from them. The honest test is data the rule has **never seen**. This is called a **train/test split**, and you'll meet it again when we test our own AI agent at the end of the week.

### Step 5: See a real ML model do the same thing (demo)

Your AI assistant found a rule by **reasoning about the examples in your prompt**. A classic ML model does something different: it **trains** on the data and stores the rule it learned. Here is a short script that does this. To try it, save it as `learn_a_rule.py` and run `python learn_a_rule.py` (it needs scikit-learn: see Before Class). You don't need to understand every line.

```python
from sklearn.tree import DecisionTreeClassifier, export_text

# 12 past failures: [passed_on_retry, code_changed, timing_spread_s]  (1 = yes, 0 = no)
X_train = [[1, 0, 1.0], [1, 0, 1.5], [1, 0, 2.0], [0, 0, 5.0], [0, 1, 4.5], [0, 0, 6.0],
           [1, 1, 0.5], [0, 1, 0.5], [0, 1, 1.0], [0, 0, 0.5], [0, 1, 2.0], [1, 1, 2.0]]
y_train = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # 1 = flaky, 0 = real defect

model = DecisionTreeClassifier(max_depth=2, random_state=0)
model.fit(X_train, y_train)                              # training: learn a rule
print(export_text(model, feature_names=["passed_on_retry", "code_changed", "timing_spread_s"]))

X_test = [[1, 0, 0.8], [0, 1, 1.5], [0, 0, 5.5], [1, 1, 1.0]]   # rows 13-16, never seen
y_test = [1, 0, 1, 0]
predictions = [int(p) for p in model.predict(X_test)]    # prediction on new data
print("Predicted:", predictions, "Actual:", y_test)
print("Correct on new data:", sum(p == t for p, t in zip(predictions, y_test)), "of 4")
```

**What to look for (not every line):**

- `X_train` is the same table as Step 2, with **1 = Yes** and **0 = No**. `y_train` holds the labels.
- `model.fit(...)` is **training**. `model.predict(...)` is **prediction** on rows 13–16.
- `export_text` prints the rule the model learned as a set of yes/no questions.

The demo prints:

```text
|--- code_changed <= 0.50
|   |--- timing_spread_s <= 0.75
|   |   |--- class: 0
|   |--- timing_spread_s >  0.75
|   |   |--- class: 1
|--- code_changed >  0.50
|   |--- timing_spread_s <= 3.25
|   |   |--- class: 0
|   |--- timing_spread_s >  3.25
|   |   |--- class: 1

Predicted: [1, 0, 1, 0] Actual: [1, 0, 1, 0]
Correct on new data: 4 of 4
```

**Read the tree like a tester:** "If the code didn't change and the timing varies, it's flaky. If the code **did** change, it's a real defect, unless the timing is very unstable." Notice that the model **didn't use "passed on retry" at all**. Different rules can fit the same 12 examples, which is exactly why we test on new data.

### Consolidated Prompt

Steps 2 and 4 together are your **"learn a rule, then predict"** prompt. Create a text file called `prompts.txt` in your `week08` folder and save it there **with its data**, so you can rerun it exactly as it is. Use this format for every prompt you save this week:

```text
=== Learn a rule - v1 ===
Use: find a rule from labelled examples, then test it on new data.
Source: Handout 01, Topic 1

--- Part 1: find the rule (new chat) ---
Here are 12 past test failures that a tester investigated.
Columns: passed_on_retry, code_changed, timing_spread_seconds, label

1. Yes, No, 1.0, Flaky
2. Yes, No, 1.5, Flaky
3. Yes, No, 2.0, Flaky
4. No, No, 5.0, Flaky
5. No, Yes, 4.5, Flaky
6. No, No, 6.0, Flaky
7. Yes, Yes, 0.5, Real defect
8. No, Yes, 0.5, Real defect
9. No, Yes, 1.0, Real defect
10. No, No, 0.5, Real defect
11. No, Yes, 2.0, Real defect
12. Yes, Yes, 2.0, Real defect

Find ONE simple rule (at most 2 conditions) that separates Flaky from Real defect.
Write the rule in one sentence. Then say how many of the 12 rows your rule gets right.

--- Part 2: predict new data (same chat) ---
Now use your rule to predict these 4 NEW failures. Answer with only the row number and Flaky or Real defect.
13. Yes, No, 0.8
14. No, Yes, 1.5
15. No, No, 5.5
16. Yes, Yes, 1.0
```

The heading, the **Use** line and the **new chat / same chat** markers let you find and rerun a prompt weeks later without re-reading the handout. You'll grow this file into a full prompt library in Lecture 03.

## Checkpoint

**Answer key:**

| | Answer |
|---|---|
| Step 1: the human rule on rows 1–12 | **7 of 12** correct (it gets rows 4, 5, 6, 7 and 12 wrong) |
| Row 13 | **Flaky** |
| Row 14 | **Real defect** |
| Row 15 | **Flaky** |
| Row 16 | **Real defect** |
| The human rule on rows 13–16 | 2 of 4 (it gets 15 and 16 wrong) |

**A rule that gets all 12 training rows right** (one of several possible):
*"Flaky if the code did **not** change and the timing spread is more than 0.75 s, or if the timing spread is more than 3.25 s."*

**Mark your AI's answer:**

- ✅ It gave **one** rule with at most 2 conditions, in one sentence
- ✅ The count it **claimed** for rows 1–12 matches **your own** count from Step 3
- ✅ Its predictions for rows 13–16 match the answer key
- ✅ It **didn't** quietly change the data or invent new columns

**Sample AI answer** (if your tool isn't working, mark this one):

> *Rule: "A failure is Flaky if the code was not changed and the timing spread is above 0.75 seconds, or the timing spread is above 4 seconds; otherwise it is a Real defect." This rule correctly classifies all 12 rows.*
> *Predictions: 13 Flaky, 14 Real defect, 15 Flaky, 16 Real defect.*

(Check its claim! Does "above 4 seconds" still get row 5, with a spread of 4.5, right?)

## Your Turn

1. **(In class, 3 min)** Compare your AI's rule from Step 2 with the person next to you. Did your two AIs find the **same** rule? Do both rules get rows 13–16 right?
2. **(After class)** Improve the Step 1 human rule so it also looks at "code changed". How many of rows 1–12 does it get right now? And rows 13–16?
3. **(After class)** Ask your AI: *"Is what you just did the same as training a machine learning model? Explain the difference in 3 sentences."* Compare its answer with Step 5.
4. **(After class)** Sort these into **Rule-based AI**, **Machine Learning** or **Deep Learning**. Then ask your AI the same question and compare:
   - (a) A spam filter that learned from millions of emails users marked as spam
   - (b) A script that fails a build if code coverage drops below 80%
   - (c) A tool that compares page screenshots using a neural network
   - (d) ChatGPT, Copilot or Claude writing a test case

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI's rule uses 4 or 5 conditions | It's trying to fit every row perfectly | Re-ask: "Use at most 2 conditions" |
| The AI says "100% correct" but you count fewer | It stated a result without checking it | Trust your own count, and note it as an AI mistake |
| The AI asks what the columns mean | Your paste lost the header line | Paste the whole prompt, including the "Columns:" line |

---

<a id="topic-2"></a>

# Topic 2: Supervised vs. Unsupervised Learning

## Definition

**Supervised learning** means the computer learns from examples that **come with the correct answer** (labels), so it can predict the answer for new examples. Topic 1 was supervised, because a tester had labelled every row. **Unsupervised learning** means the computer gets examples **without any answers** and finds structure by itself, usually by **grouping similar things together** (called *clustering*). The single question that decides which one to use is: **"Do we have labels?"**

## Key Ideas

1. **Do we have labels?** Yes → supervised. No → unsupervised.

   | | Supervised | Unsupervised |
   |---|---|---|
   | Data has answers? | ✅ Yes (labels) | ❌ No |
   | Goal | **Predict** an answer | **Discover** groups or unusual items |
   | QE example | "Will this commit break the build?" | "Which of these 500 failures look alike?" |
   | Typical method | Classification, regression | Clustering, anomaly detection |

2. **Two kinds of supervised learning:** **classification** predicts a *category* (pass/fail, flaky/defect). **Regression** predicts a *number* (how many minutes the test suite will take).
3. **Unsupervised groups have no names.** The computer says "these 4 failures belong together", and **a human** decides what the group means (for example, "these are timeouts").
4. **Garbage in, garbage out.** If the labels are wrong, a supervised model learns the wrong lesson. Spotting bad data is a tester's skill.

## Worked Example: Both Kinds of Learning, with Your AI

### Step 1: Supervised: labelled past commits

Paste into a **new chat**:

```text
Here are 10 past commits and whether the build failed.
Columns: commit, files_changed, tests_updated, build_result

A, 2, Yes, Passed
B, 3, Yes, Passed
C, 1, No, Passed
D, 4, Yes, Passed
E, 5, No, Passed
F, 25, No, Failed
G, 30, No, Failed
H, 18, No, Failed
I, 22, Yes, Passed
J, 35, No, Failed

Based ONLY on this data, predict whether these two new commits will fail, and give a one-line reason for each:
K, 2, Yes
L, 32, No
```

**What this does:** the `build_result` column holds the **labels**, so this is **supervised**. The AI uses the labelled history to **predict** an answer for new commits.

### Step 2: Check the AI's reasoning

Read the AI's reasons. A good answer is based on a **pattern in the data**, such as "big commits without test updates failed". A weak answer brings in outside opinions that aren't in the data, such as "commits on Fridays are risky". Did your AI stick to the data, as the prompt asked?

### Step 3: Unsupervised: unlabelled test failures

Now paste this into the **same chat**:

```text
Here are 10 test failures with NO labels.
Columns: failure, duration_seconds, memory_mb

F1, 61, 300
F2, 58, 280
F3, 63, 310
F4, 9, 1900
F5, 12, 2100
F6, 10, 1850
F7, 8, 290
F8, 7, 260
F9, 9, 300
F10, 60, 320

Put these failures into exactly 3 groups of similar failures.
List the failure IDs in each group. Do NOT name or explain the groups.
```

**What this does:** there is **no label column**, so this is **unsupervised**. We ask for groups **without names** on purpose, because naming them is the human's job.

### Step 4: You name the groups

Look at the AI's groups and name each one yourself. For example: what do slow tests with normal memory use usually mean? What about fast tests that use a **lot** of memory?

### Consolidated Prompts

Add both prompts to `prompts.txt`, with their data:

```text
=== Supervised - predict - v1 ===
Use: predict an answer for new items from labelled history.
Source: Handout 01, Topic 2

--- Prompt (new chat) ---
Here are 10 past commits and whether the build failed.
Columns: commit, files_changed, tests_updated, build_result

A, 2, Yes, Passed
B, 3, Yes, Passed
C, 1, No, Passed
D, 4, Yes, Passed
E, 5, No, Passed
F, 25, No, Failed
G, 30, No, Failed
H, 18, No, Failed
I, 22, Yes, Passed
J, 35, No, Failed

Based ONLY on this data, predict whether these two new commits will fail, and give a one-line reason for each:
K, 2, Yes
L, 32, No
```

```text
=== Unsupervised - group - v1 ===
Use: group unlabelled items; a human names the groups.
Source: Handout 01, Topic 2

--- Prompt (new chat) ---
Here are 10 test failures with NO labels.
Columns: failure, duration_seconds, memory_mb

F1, 61, 300
F2, 58, 280
F3, 63, 310
F4, 9, 1900
F5, 12, 2100
F6, 10, 1850
F7, 8, 290
F8, 7, 260
F9, 9, 300
F10, 60, 320

Put these failures into exactly 3 groups of similar failures.
List the failure IDs in each group. Do NOT name or explain the groups.
```

## Checkpoint

**Answer key:**

| Question | Expected answer |
|---|---|
| Commit K (2 files, tests updated) | **Pass**: small, with tests updated, like A, B and D |
| Commit L (32 files, no tests) | **Fail**: large, without tests, like F, G, H and J |
| Group 1 | **F1, F2, F3, F10**: slow (about 60 s), normal memory → probably **timeouts** |
| Group 2 | **F4, F5, F6**: fast, huge memory (about 2,000 MB) → probably **memory problems** |
| Group 3 | **F7, F8, F9**: fast, normal memory → a **different cause**, such as a backend error |

**Mark your AI's answer:**

- ✅ Predictions for K and L match the key
- ✅ Its reasons point to patterns **in the data**, not outside opinions
- ✅ The 3 groups contain the same failures as the key (the group **order** doesn't matter)
- ✅ It did **not** name the groups (if it did, it ignored an instruction, which counts as a mistake)

**Sample AI answer:** *K: Likely passes (small change with tests updated, like A, B, D). L: Likely fails (large change, no tests, like F, G, J). Groups: {F1, F2, F3, F10}, {F4, F5, F6}, {F7, F8, F9}.*

## Your Turn

1. **(In class, 3 min)** Ask your AI about a third commit: `M, 15, Yes`. Is the answer as confident as for K and L? Why might this one be harder? (Hint: is there a similar commit in the data?)
2. **(After class)** Ask the AI to put the 10 failures into **2** groups instead of 3. Which groups get merged? What does this tell you about choosing the number of groups?
3. **(After class)** For each situation, write **supervised** or **unsupervised** and a one-line reason:
   - (a) Predict "High" or "Low" priority for bug reports, using 2,000 past reports that already have priorities
   - (b) Find unusual API response times in last night's performance run
   - (c) Predict how many minutes the regression suite will take
   - (d) Group 800 customer complaints into themes
4. **(After class)** Change commit I's result to `Failed` in the Step 1 prompt (a **wrong label**) and ask again about a new commit `N, 20, Yes`. Does the bad label change the AI's answer? That's "garbage in, garbage out".

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI names or explains the groups anyway | It's trying to be helpful and ignored the instruction | Note it as an ignored instruction (you'll study these in Lecture 04) |
| The AI uses outside knowledge ("Friday deploys are risky") | The prompt didn't keep it to the data | Re-ask with "based ONLY on this data" in capitals |
| Different group numbering from a classmate | Group order doesn't matter | Compare **which failures are together**, not the group numbers |

---

<a id="topic-3"></a>

# Topic 3: Neural Network Fundamentals

## Definition

A **neural network** is a model built from many small units called **neurons**, arranged in **layers**. Each neuron does something very simple: it **multiplies each input by a weight, adds them up, adds a bias**, and passes the result through an **activation function** that decides the output. One neuron on its own is a tiny decision-maker; billions of them in layers make up **deep learning**, the technology inside ChatGPT, Copilot and Claude. The network **learns** by adjusting its weights a little at a time, so its answers get closer to the correct ones.

## Key Ideas

1. **One neuron = a weighted vote.**

   ```text
   input 1 ──(× weight 1)──┐
   input 2 ──(× weight 2)──┼──► sum + bias = z ──► activation ──► output
   input 3 ──(× weight 3)──┘
   ```

   - **Weights** say how much each input matters.
   - **Bias** is a starting nudge that makes the neuron harder or easier to "switch on".
2. **Activation:** the simplest one, a **step**, says "output 1 if z is above 0, otherwise 0".
3. **Layers:** the outputs of one layer become the inputs of the next. "Deep" just means **many layers**.
4. **Learning = adjusting weights.** Make a guess, see how wrong it is, nudge the weights, repeat. Computers do this millions of times. You'll do it once, by hand.

## Worked Example: A Neuron That Decides "Does This Failure Need Attention Now?"

**The problem:** one neuron decides whether a test failure needs **attention right now** (1) or **can wait** (0). Each failure has three inputs:

- `is_smoke_test`: 1 if it's a critical smoke test, 0 if not
- `times_failed_this_week`: how many times it failed this week
- `failed_in_production_env`: 1 if it failed in the production-like environment, 0 if not

**Weights:** smoke test = **2.0**, each failure this week = **0.5**, production-like environment = **1.5**. **Bias** = **−3.0**.

### Step 1: Work out the neuron by hand

**The correct answers (labels).** The QA lead has already decided what the right answer is for each failure, using the team's rule: *"A failing smoke test always needs attention now, because smoke tests cover the most critical features. A normal test that failed once in dev can wait."* These labels are what the neuron **should** output, just like the labels in Topics 1 and 2.

For each failure, multiply each input by its weight, add them up, add the bias to get **z**, then apply the step: **1 if z > 0, otherwise 0**. Fill in the table on paper, then compare the neuron's output with the correct answer:

| Failure | Inputs | Weighted sum | + bias | z | Neuron output | Correct answer (label) | Match? |
|---|---|---|---|---|---|---|---|
| A: smoke test, failed 3×, in production-like env | [1, 3, 1] | 2.0 + 1.5 + 1.5 = ? | −3.0 | ? | ? | **1** (smoke test) | ? |
| B: normal test, failed once, in dev | [0, 1, 0] | 0 + 0.5 + 0 = ? | −3.0 | ? | ? | **0** (normal test, once, in dev) | ? |
| C: smoke test, failed once this week, in dev | [1, 1, 0] | ? | −3.0 | ? | ? | **1** (smoke test) | ? |

### Step 2: Check the AI's arithmetic

Paste into your AI assistant:

```text
A neuron has weights [2.0, 0.5, 1.5] and bias -3.0, with a step activation (1 if z > 0, else 0).
For each input, show the weighted sum, z and the output:
A: [1, 3, 1]
B: [0, 1, 0]
C: [1, 1, 0]
Then explain in 2 sentences what the bias does.
```

Compare its numbers with **your** table. LLMs are usually right on small sums like these, but they predict text rather than calculate, so **always check numbers**.

### Step 3: Learn by hand

Look at failure **C**. Its label is **1**: it's a **smoke test**, and the team's rule says a failing smoke test always needs attention now. But the neuron says **0**, because one failure in dev didn't push z above 0. **The neuron's output doesn't match the label, so it made a mistake.** Finding and fixing these mismatches is exactly what training does.

**Fix it by nudging one value.** Try either:

- changing the **bias** from −3.0 to **−1.5**, or
- changing the **smoke-test weight** from 2.0 to **3.5**.

Recalculate A, B and C with your change. Is C now correct? Are A and B **still** correct?

**What to notice:** you just did what training does: you saw an error, adjusted a weight or the bias, and checked that you didn't break the other examples. A real network repeats this automatically, millions of times, over millions of weights.

### Step 4 (optional): Confirm with code

If you'd like to see it in Python, save this as `neuron.py` and run `python neuron.py`. It needs no installs.

```python
def neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias   # weighted sum + bias
    return z, (1 if z > 0 else 0)                              # step activation

weights, bias = [2.0, 0.5, 1.5], -3.0
for failure in ([1, 3, 1], [0, 1, 0], [1, 1, 0]):
    z, output = neuron(failure, weights, bias)
    print(f"{failure} -> z = {z:+.1f} -> output {output}")
```

**What it does:** `neuron` multiplies each input by its weight (`zip` pairs them up), adds the bias, and applies the step. The loop runs failures A, B and C. Change `-3.0` to `-1.5` to check your Step 3 fix.

### Consolidated Result

Your completed table from Steps 1 and 3 **is** the result: a neuron worked out by hand and corrected by one "learning" step. `neuron.py` is the optional code version.

## Checkpoint

**Answer key, Step 1 (bias −3.0):**

| Failure | Weighted sum | z | Neuron output | Correct answer (label) | Match? |
|---|---|---|---|---|---|
| A [1, 3, 1] | 2.0 + 1.5 + 1.5 = 5.0 | **+2.0** | **1** | 1 | ✅ |
| B [0, 1, 0] | 0 + 0.5 + 0 = 0.5 | **−2.5** | **0** | 0 | ✅ |
| C [1, 1, 0] | 2.0 + 0.5 + 0 = 2.5 | **−0.5** | **0** | 1 (failing smoke test) | ❌ The neuron is wrong |

**Answer key, Step 3 (bias changed to −1.5):** A: z = +3.5 → 1 ✅ · B: z = −1.0 → 0 ✅ · C: z = +1.0 → 1 ✅

(Changing the smoke weight to 3.5 also works: A +3.5 → 1, B −2.5 → 0, C +1.0 → 1.)

**If you ran `neuron.py`** with the original bias:

```text
[1, 3, 1] -> z = +2.0 -> output 1
[0, 1, 0] -> z = -2.5 -> output 0
[1, 1, 0] -> z = -0.5 -> output 0
```

**Mark your AI's answer to Step 2:** ✅ the z values match the key · ✅ the outputs match · ✅ the bias explanation says something like "it shifts how easily the neuron switches on".

## Your Turn

1. **(In class, 3 min)** With your Step 3 fix in place, work out failure **D**: a normal test that failed 4 times in the production-like environment, `[0, 4, 1]`. Does it need attention? Does that seem right to you as a tester?
2. **(After class)** Change the bias to **0.0** and recalculate A, B and C. What goes wrong? Why is a bias that's too high a problem?
3. **(After class)** Ask your AI: *"Explain how a neural network learns, for a software tester with no maths background, in 5 sentences, using an everyday analogy."* Compare it with Key Idea 4. Is anything confusing or wrong?
4. **(After class)** Ask your AI: *"Roughly how many weights does a large language model have?"* Then ask: *"How sure are you about that number?"* What does its second answer tell you about trusting AI facts?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Your z doesn't match the key | A sign mistake with the bias (−3.0 is subtracted) | Write each step: sum first, then add the bias |
| The AI's numbers differ from yours | Either of you may have slipped | Recalculate. If the AI is wrong, that's a real example of an AI maths mistake |
| `python` is not recognised (optional script) | Python isn't on the PATH | On Windows try `py neuron.py`, or skip the optional step |

---

## Lecture Wrap-Up: Quick Check

1. Which statement is true? (a) All AI is machine learning. (b) All deep learning is machine learning. (c) All machine learning is deep learning.
2. In ML, what is a **label**?
3. Why do we test a learned rule on **new** data (rows 13–16) and not just the training rows?
4. A clustering tool puts 50 failures into "Group 2". Who decides what Group 2 **means**?
5. In one sentence: how does a neural network learn?
6. What's the main difference between the predictive ML in today's worked example and Generative AI?

<details>
<summary>Answers</summary>

1. **(b)** Deep learning sits inside machine learning, which sits inside AI.
2. The **correct answer** for an example (for example "flaky" or "real defect").
3. The rule was **made from** the training rows, so of course it fits them. Only new data shows whether it really works.
4. **A human.** The algorithm only groups. People give the groups meaning.
5. It makes a guess, measures how wrong it was, and **nudges its weights**, repeating this many times.
6. Predictive ML picks an answer from a fixed set (a label or a number); Generative AI **creates new content** (text, code, test cases) from a prompt, so its output has to be **reviewed**, not just compared with one correct label.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Artificial Intelligence (AI)** | Any technique that makes computers behave "intelligently" |
| **Machine Learning (ML)** | AI that learns rules from examples |
| **Deep Learning (DL)** | ML using neural networks with many layers |
| **Generative AI (GenAI)** | Deep learning that creates new content (text, code, images) from a prompt |
| **Large Language Model (LLM)** | The deep-learning model behind GenAI chat tools; it writes text by predicting the next word |
| **Prompt** | The request you write to a GenAI tool |
| **Hallucination** | Confident, fluent GenAI output that is wrong or invented |
| **Feature** | One piece of input information about an example |
| **Label** | The known correct answer for an example |
| **Training data / test data** | Examples used to learn a rule / new examples used to check it |
| **Train/test split** | Keeping some examples aside to test the rule on data it hasn't seen |
| **Model** | The rule (or set of rules) learned from data |
| **Prediction** | Using a learned rule on new data |
| **Supervised learning** | Learning from examples **with** labels |
| **Unsupervised learning** | Finding structure in examples **without** labels |
| **Classification / regression** | Predicting a category / a number |
| **Clustering** | Grouping similar examples together |
| **Neuron** | A unit that computes a weighted sum + bias and applies an activation |
| **Weight / bias** | How much an input matters / a neuron's starting nudge |
| **Activation function** | Turns the neuron's raw score into its output (for example a step) |

## Summary

- **AI ⊃ ML ⊃ DL ⊃ Generative AI.** The tools you'll use this week sit in the smallest circle.
- **Generative AI creates new content from a prompt.** It's fast and versatile, but it can **hallucinate**, so every answer is a draft that a tester checks.
- In ML, **the computer learns rules from labelled examples**. A learned rule must be tested on **new** data before you trust it.
- **Labels decide the approach:** with answers → supervised (predict); without → unsupervised (discover groups, which a human then names).
- A **neuron** is a weighted sum + bias + activation, and **learning** means nudging weights to fix errors.
- Today you also started the week's key habit: **ask the AI, then check its answer**, including the numbers it claims.
