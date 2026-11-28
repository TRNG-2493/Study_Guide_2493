# Artificial Intelligence, Machine Learning and Deep Learning

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what Artificial Intelligence (AI), Machine Learning (ML), Deep Learning (DL) and Generative AI (GenAI) are, and how they fit inside one another.
- **Compare** a rule written by a person with a rule learned from examples, using a flaky-test example.
- **Use** the core ML vocabulary correctly: feature, label, training, model, prediction, training data and test data.
- **Check** an AI's claim about its own rule by counting the results yourself, and explain why a rule must be tested on data it has never seen.
- **Classify** tools you meet in testing as rule-based AI, ML, DL or GenAI, and say why.

---

## Why This Matters

For seven weeks you have built a Quality Engineering toolkit: Python and Git, test design, pytest, Playwright, Selenium with BDD, API and accessibility testing, and CI/CD. This week adds **AI** to that kit.

Start with a problem every automation team knows. A test fails in the pipeline. Is it a **real defect** (the code is broken) or a **flaky test** (it fails at random, and the code is fine)? Someone has to investigate, and that takes time.

At scale, this is expensive. In 2016, Google's testing team reported that about **1.5% of all its test runs** gave a flaky result, and that almost **16% of its tests** showed some flakiness. They also noted that data from flaky runs showed patterns that could help identify a flaky result **without re-running the test** ([Google Testing Blog](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)). Finding a pattern in past data and using it on new data is exactly what machine learning does.

By Friday you will build your **first QA agent**. To use AI well, and to question it well, you need a clear picture of what AI is. Without it, people either **over-trust** AI and ship tests that check the wrong thing, or **under-use** it and miss real help. Every other lesson today builds on this picture.

> **Using this with the handout:** this lesson goes deeper into **Handout 01, Topic 1**. It uses the same flaky-test data (rows 1–16), the same prompts and the same demo script.

---

## The Concept

### 1. The Big Picture: Four Nested Circles

The most useful picture to keep in your head is a set of nested circles:

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

Read it from the outside in:

- **Every ML system is AI**, but not all AI is ML. A rule written by a person is AI, but nothing was learned.
- **Every DL system is ML**, but not all ML is deep learning.
- **Generative AI** is the part of deep learning that **creates new content**. ChatGPT, Copilot and Claude are GenAI tools, and they are the focus of this week.

**An everyday analogy:** *vehicle → car → electric car*. Every electric car is a car, and every car is a vehicle, but a bicycle is a vehicle that is not a car. In the same way, a chess program written entirely by hand is AI, but not machine learning.

When a vendor says their testing tool "uses AI", ask: **which circle?** Each circle fails in different ways, so you test each differently.

Testing examples that belong to each circle, but **not** to the smaller circles inside it:

| Circle | Testing example |
|---|---|
| **AI (rule-based)**: people write all the rules | A script that runs only the checkout tests when files in `/checkout` change |
| **Machine Learning**: learns from labelled data | Predicting which failed tests are flaky (this lesson's example) |
| **Deep Learning**: handles images, sound, free text | Sorting thousands of crash screenshots by the kind of error shown |
| **Generative AI**: creates content | Drafting test cases from a user story |

### 2. What Is Artificial Intelligence?

**Artificial Intelligence** is the broad field of making computers do things we would call "intelligent" if a person did them: deciding, recognising, predicting, planning. The term dates from a 1956 workshop at Dartmouth College, often called the start of AI research.

Notice what the definition does **not** say: nothing about *how* the intelligence is achieved. AI is defined by **behaviour**, not technique. That is why hand-written rules count as AI.

#### 2.1 Rule-based AI: a person writes the rules

Early AI systems, called **expert systems**, were built from rules that experts wrote down. Testers write this kind of logic too. Many teams start flaky-test triage with one rule:

> **"If the test passed on retry, it's flaky. Otherwise it's a real defect."**

Rule-based systems are **transparent**, **predictable** and **easy to debug**. Their weakness is that **someone must think of every rule**, including combinations such as "fails only in the Firefox job when the database is busy". Rule lists grow, contradict each other and become hard to maintain. Machine learning tries to solve this.

You may also hear **narrow AI**: AI that is good at a specific task or family of tasks. Every AI product today is narrow AI, including ChatGPT, Copilot and Claude. They have specific limits, and testers are good at finding limits.

### 3. What Is Machine Learning?

**Machine Learning** is the part of AI where the computer **learns the rules from examples** instead of a person writing every rule. The examples come with correct answers, and the computer looks for a pattern that explains them.

Put simply, following Tom Mitchell's well-known 1997 definition: a program **learns** if its performance at a task improves with experience. For flaky tests:

- **Task:** decide whether a failed test is flaky or a real defect.
- **Experience:** past failures that a tester already investigated and labelled.
- **Performance:** how many new failures it labels correctly.

#### 3.1 Traditional programming vs machine learning

This comparison is the heart of the lesson:

| | Traditional programming | Machine learning |
|---|---|---|
| You give the computer | Rules + data | Data + correct answers |
| The computer gives you | Answers | **Rules** (a "model") |
| Good when | Rules are clear and stable | Rules are fuzzy or hard to write down |

The learned rules are stored in a **model**. For simple models, like the decision tree in section 4.5, you can read the rules. For large models, the rules are millions or billions of numbers that nobody can read.

> **Tester's analogy:** a trained model is like a function under test whose code you did not write and cannot read. You judge it by its **behaviour on inputs**. That is black-box testing, which you met in Week 3.

#### 3.2 ML vocabulary you will hear all week

| Word | Plain meaning | Testing example |
|---|---|---|
| **Feature** | One piece of information about an example | "Did the test pass on retry?" |
| **Label** | The correct answer for an example | "Flaky" or "Real defect" |
| **Training data** | Labelled examples the model learns from | 12 past failures a tester investigated |
| **Training** | Learning a rule from the training data | Studying those 12 failures |
| **Model** | The rule that was learned | "If the code didn't change and the timing varies…" |
| **Prediction** | Using the rule on new data | "Failure 13 is probably flaky" |
| **Test data** | Labelled examples kept back to check the model | 4 newer failures the model never saw |

One warning: in ML, **"test data"** means examples kept back to check a model, not the test data you create for your automated tests.

### 4. Worked Example: Flaky Test or Real Defect?

We will solve one problem three ways: a person's rule, an AI assistant, and a classic ML model.

We have 12 past failures that a tester already investigated (the **training data**), and 4 new ones to predict (the **test data**).

**Training data:**

| # | Passed on retry? | Code changed just before? | Timing spread (s) | Label |
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

**Test data** (answers in section 4.4):

| # | Passed on retry? | Code changed just before? | Timing spread (s) |
|---|---|---|---|
| 13 | Yes | No | 0.8 |
| 14 | No | Yes | 1.5 |
| 15 | No | No | 5.5 |
| 16 | Yes | Yes | 1.0 |

*Timing spread* is how much the test's run time varies between runs; a big spread often points to timing problems. Each column is a **feature**, and the last training column is the **label**. A person chose these three features.

#### 4.1 Approach 1: Be the rule-writer

Apply the team's rule to rows 1–12: *"If it passed on retry, it's flaky."*

| Rows | Passed on retry? | Rule says | Label | Right? |
|---|---|---|---|---|
| 1, 2, 3 | Yes | Flaky | Flaky | ✅ |
| 4, 5, 6 | No | Real defect | Flaky | ❌ |
| 7, 12 | Yes | Flaky | Real defect | ❌ |
| 8, 9, 10, 11 | No | Real defect | Real defect | ✅ |

The rule gets **7 of 12** right. Rows 4–6 are flaky even though they did **not** pass on retry; their timing spread (5.0, 4.5 and 6.0 seconds) is far higher than the rest. The rule-writer never looked at timing, so the rule cannot use it.

#### 4.2 Approach 2: Ask an AI assistant to find a rule

Now give the same examples to ChatGPT, Copilot Chat or Claude. Open a **new chat** and paste:

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

What each part does:

- **The 12 rows** are labelled examples: ML in miniature, **examples in, rule out**.
- **"Columns:"** tells the AI what each value means.
- **"At most 2 conditions"** stops it writing a long rule that memorises every row.
- **"Say how many rows it gets right"** makes it state a claim you can check.

Here is the kind of reply you might get. It is **illustrative**, written for this lesson to show a typical mistake, not copied from a real model:

```text
Rule: A failure is Flaky if its timing spread is greater than 1.2 seconds;
otherwise it is a Real defect.
This rule correctly classifies all 12 rows.
```

**Do not believe it yet.**

#### 4.3 Check the AI's claim yourself

AI assistants often **state** a result without really checking it. So you check it, row by row on paper, or with a few lines of Python:

```python
# check_rule.py
# The 12 labelled failures: (passed_on_retry, code_changed, timing_spread_s, label)
TRAINING = [
    ("Yes", "No", 1.0, "Flaky"), ("Yes", "No", 1.5, "Flaky"), ("Yes", "No", 2.0, "Flaky"),
    ("No", "No", 5.0, "Flaky"), ("No", "Yes", 4.5, "Flaky"), ("No", "No", 6.0, "Flaky"),
    ("Yes", "Yes", 0.5, "Real defect"), ("No", "Yes", 0.5, "Real defect"),
    ("No", "Yes", 1.0, "Real defect"), ("No", "No", 0.5, "Real defect"),
    ("No", "Yes", 2.0, "Real defect"), ("Yes", "Yes", 2.0, "Real defect"),
]

def human_rule(retry, changed, spread):
    return "Flaky" if retry == "Yes" else "Real defect"

def ai_rule(retry, changed, spread):          # the rule from the illustrative AI reply
    return "Flaky" if spread > 1.2 else "Real defect"

def check(rule):
    wrong = [n for n, (r, c, s, label) in enumerate(TRAINING, start=1)
             if rule(r, c, s) != label]
    print(f"{rule.__name__}: {12 - len(wrong)} of 12 correct, wrong rows {wrong}")

check(human_rule)
check(ai_rule)
```

Run it with `python check_rule.py`. Output:

```text
human_rule: 7 of 12 correct, wrong rows [4, 5, 6, 7, 12]
ai_rule: 9 of 12 correct, wrong rows [1, 11, 12]
```

What to notice:

- `TRAINING` is the same table you gave the AI, so you check against exactly that data.
- Each rule is a small function written by a person. This is **traditional programming**.
- `enumerate(..., start=1)` numbers rows from 1, so the wrong-row numbers match the table.
- `check` never trusts a claim. It counts.

The AI claimed **12 of 12**. The real count is **9 of 12**: row 1 (flaky, small spread) and rows 11 and 12 (real defects with a 2.0 s spread) are wrong. You have caught your first AI mistake of the week.

Your own AI may give a different rule, and it may be correct. Several correct rules exist, for example: *"Flaky if the code did not change and the spread is more than 0.75 s, or if the spread is more than 3.25 s."* The point is not that AI is always wrong. It is that **you only know after you check**.

#### 4.4 Predict new data: the real test

A rule can look perfect on the examples it learned from and still fail on new ones. The honest test uses data the rule has **never seen**. In the same chat, paste:

```text
Now use your rule to predict these 4 NEW failures. Answer with only the row number and Flaky or Real defect.
13. Yes, No, 0.8
14. No, Yes, 1.5
15. No, No, 5.5
16. Yes, Yes, 1.0
```

The answer key, from the tester who later investigated these failures:

| Row | Correct label | Human rule | Illustrative AI rule |
|---|---|---|---|
| 13 | Flaky | Flaky ✅ | Real defect ❌ |
| 14 | Real defect | Real defect ✅ | Flaky ❌ |
| 15 | Flaky | Real defect ❌ | Flaky ✅ |
| 16 | Real defect | Flaky ❌ | Real defect ✅ |

Both rules get **2 of 4**. Neither is good enough to trust.

Keeping labelled data back for checking is called a **train/test split**. It protects you from two classic problems:

- **Overfitting:** the rule fits the training rows, noise included, but fails on new data. It is like a student who memorised last year's exam answers and cannot answer a new question. You spot it when results are very good on training data and much worse on test data.
- **Underfitting:** the rule is too simple to capture the real pattern, like a student who only learned "the answer is usually C". It does poorly on both. The human rule underfits: it ignores two of the three features.

Asking for **at most 2 conditions** was a guard against overfitting. As a tester, ask this about every accuracy claim: **"Accuracy measured on what data?"** If the answer is "the data it learned from", the number tells you very little.

> **Save your prompt.** The handout has you save this two-part prompt, with its data, in `prompts.txt` in your `week08` folder under `=== Learn a rule - v1 ===`, so you can rerun it exactly. On Tuesday you grow this file into a prompt library.

#### 4.5 Approach 3: A real ML model does the same thing

Your AI assistant found a rule by **reasoning about the examples in your prompt**. A classic ML model **trains** on the data and stores the rule it learned, so it gives the same answer every time.

The demo trains a **decision tree**, a model that learns a flowchart of yes/no questions. It needs scikit-learn, a widely used Python ML library: `python -m pip install scikit-learn`.

```python
# learn_a_rule.py
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

Output:

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

What to look for:

- `X_train` is the same table, with **1 = Yes** and **0 = No**; `y_train` holds the labels.
- `max_depth=2` allows at most two questions per path: the same guard as "at most 2 conditions" in the prompt.
- `model.fit(...)` is **training**; `model.predict(...)` is **prediction** on rows 13–16.
- `export_text` prints the learned rule. Decision trees are one of the few models whose rules you can read.

**Read the tree like a tester:** "If the code didn't change and the timing varies, it's flaky. If the code **did** change, it's a real defect, unless the timing is very unstable." It got all four new failures right.

Notice that the model **did not use "passed on retry" at all**, the feature the team's rule relied on. Different rules can fit the same examples. And four test rows is far too few to trust any rule: a lucky rule and a good rule look the same. Real teams train on thousands of failures and check on hundreds.

So all three approaches need the same habit: **check the result against real data**.

### 5. What Is Deep Learning?

**Deep Learning** is the part of machine learning that uses **neural networks with many layers**; "deep" simply means many layers. It is very good with **messy data** such as text, images and speech, where nobody could write down the useful features by hand.

You will see how a neural network works later today, in *Neural Network Fundamentals*. For now, the big idea is enough: a network is made of many small units called **neurons**, arranged in **layers**. Early layers pick up simple patterns, and later layers combine them into complex ones. In an image model, early layers might detect edges and later layers whole objects, such as a button.

#### 5.1 It learns its own features

In our example, a **person** chose the features: retry, code change and timing spread. Deep learning can **learn useful features by itself from raw data**, such as the pixels of a screenshot or the characters of a log file.

| | Classic machine learning | Deep learning |
|---|---|---|
| Typical input | Tables of numbers and categories | Images, text, audio (tables too) |
| Features | Mostly chosen by people | Mostly learned automatically |
| Data and compute | Can work with thousands of examples on a laptop | Usually needs far more data and specialised hardware |
| Can you read the rules? | Often (for example, a decision tree) | Usually not: millions of numbers |

The last row is a real trade-off: when a deep-learning model is wrong, you cannot point to the rule that caused it. You can only test its behaviour.

#### 5.2 Why deep learning took off when it did

Neural networks are decades old, but only took over in the 2010s, when three things arrived together: **huge amounts of data** from the internet, **GPUs** (graphics processors that suit the maths), and **better training methods**. Three milestones:

- **2012:** a deep network called **AlexNet** won a major image-recognition competition by a large margin.
- **2017:** Google researchers introduced the **Transformer**, the design behind today's large language models.
- **Late 2022:** ChatGPT brought Generative AI to the general public.

### 6. Generative AI: The Focus of This Week

**Generative AI** is the part of deep learning that **creates new content**, such as text, code, test cases and images, instead of only predicting a label or a number. Everything in the worked example was **predictive** ML: the answer came from a fixed set.

| | Predictive ML (the worked example) | Generative AI (ChatGPT, Copilot, Claude) |
|---|---|---|
| What it produces | A label or a number: "Flaky" | New content: a paragraph, a test case, code |
| How you use it | Give it features, get a prediction | Write a request in plain language, called a **prompt** |
| Trained on | Labelled examples for **one** task | Huge amounts of text and code, for **many** tasks |
| How you check it | Compare with the correct label | Read it against the requirement; often no single right answer |

A GenAI tool is built on a **Large Language Model (LLM)**: a very large deep-learning model that writes its answer a small piece at a time, predicting what is most likely to come next. You will study how this works later today, in *Generative AI Concepts*.

**The catch:** GenAI writes text that **sounds** right, but does not check facts. It can confidently invent a rule, a number or a function. This is called a **hallucination**. You saw the pattern in section 4.3: a confident "12 of 12" that was really 9 of 12. The habit you practised there, **ask the AI, then check its answer**, runs through the whole week.

### 7. AI and ML in Real Testing Work

These ideas are already used in real testing pipelines.

**Predictive test selection at Facebook (real).** Running every test on every code change was too slow and costly for Facebook's huge codebase. Their engineers trained an ML model on test results from past code changes, to predict which tests were likely to fail on a new change. In their 2018 paper, they reported that it halved the cost of testing code changes while still catching more than 99.9% of faulty changes ([Machalica et al., *Predictive Test Selection*](https://arxiv.org/abs/1810.05286)). That is classic ML: labelled history in, a rule out.

**A model that goes stale (illustrative scenario).** Imagine a team trains a flaky-test model on last year's CI history, and it works well. Then the team moves its UI tests from Selenium to Playwright, and timing patterns change. The model keeps labelling real timeouts as "flaky", and genuine defects are ignored for weeks. This slow loss of accuracy, as real data moves away from the training data, is called **drift**. Models need monitoring and retraining, just as tests need maintenance.

### 8. Common Misconceptions

| Misconception | Reality |
|---|---|
| "AI and ML are the same thing." | ML is one way of building AI. Rule-based systems are AI too. |
| "More data always fixes the model." | More **bad** data makes it worse: "garbage in, garbage out". |
| "Deep learning is always better." | For small tables like ours, a simple model is often as good, cheaper and easier to explain. |
| "Once trained, a model stays correct." | The world changes. Models **drift** and need monitoring. |

---

## Practice Exercises

1. **Which circle? (paper, 10 min)** Classify each system as rule-based AI, ML, DL or GenAI, with a one-sentence reason:
   - (a) A CI job that skips the payment tests when only the `docs/` folder changed.
   - (b) A model trained on two years of CI history that predicts whether a pull request will break the build.
   - (c) A tool that recognises a "Submit" button in a screenshot whatever its colour or position.
   - (d) An assistant that turns a plain-English bug report into numbered reproduction steps.

   *Hint:* ask "was anything learned from data?", then "is the data messy?", then "does it create new content?"

2. **Catch the claim (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** in a new chat, paste the prompt from section 4.2, but change row 5's label to **Real defect**.
   - **Review:** write down the AI's rule and the count it claims.
   - **Run:** add the AI's rule to `check_rule.py` as a new function, change row 5 in `TRAINING`, and run it. Does the real count match the claim?
   - **Record:** note whether the AI was right, and how one changed label changed its rule.

3. **Spot the problem and choose features (paper, 15 min).** A teammate says: *"Our flaky-test model is 99% accurate on its training data and 70% on test data."* Is this overfitting or underfitting? Explain with the exam analogy. Then list three new features you could collect from your Project 2 runs (pytest output, Playwright traces or CI logs) that might help the model.

---

## Knowledge Check

1. Order these from the outermost circle to the innermost: Deep Learning, AI, Generative AI, Machine Learning.

<details><summary>Answer</summary>

AI → Machine Learning → Deep Learning → Generative AI. Each sits inside the one before it.

</details>

2. What is the key difference between traditional programming and machine learning?

<details><summary>Answer</summary>

In traditional programming, a person writes the rules and the computer produces answers. In machine learning, you give the computer data plus correct answers, and it produces the rules (the model).

</details>

3. Is a script that pages the on-call engineer when "ERROR" appears 5 times in a minute machine learning?

<details><summary>Answer</summary>

No. It is rule-based AI: a person wrote the rule, and nothing was learned from data.

</details>

4. An AI assistant says its rule "correctly classifies all 12 rows". What should you do before using it?

<details><summary>Answer</summary>

Check the claim yourself by applying the rule to every row and counting, on paper or with a short script. Then test the rule on new rows it has never seen.

</details>

5. Why must a model be tested on data it did not learn from?

<details><summary>Answer</summary>

A rule can fit its training examples by memorising them (overfitting) and still fail on new data. Only unseen data gives an honest picture of how it will perform.

</details>

---

## Glossary

- **Artificial Intelligence (AI):** making a computer do things we would call intelligent, such as deciding or predicting.
- **Rule-based AI / expert system:** AI in which people write all the rules; nothing is learned.
- **Machine Learning (ML):** the part of AI where the computer learns rules from labelled examples.
- **Deep Learning (DL):** the part of ML that uses neural networks with many layers.
- **Generative AI (GenAI):** the part of DL that creates new content.
- **Large Language Model (LLM):** a very large deep-learning model trained on text and code; the engine inside GenAI chat tools.
- **Feature:** one piece of information about an example.
- **Label:** the correct answer for an example.
- **Training data / test data:** labelled examples used to learn a model / kept back to check it.
- **Model:** the rule that was learned.
- **Prediction:** using a model on new data.
- **Decision tree:** a model that learns a readable flowchart of yes/no questions.
- **Overfitting / underfitting:** fitting training data too closely / too loosely to work on new data.
- **Hallucination:** confident but false output from a GenAI tool.
- **Drift:** a model's slow loss of accuracy as real-world data changes.

---

## Summary

- **AI ⊃ ML ⊃ DL ⊃ GenAI.** A rule-based script is AI but not ML: hand-written rules only contain the patterns a person thought of.
- **ML learns rules from data plus correct answers**, using features, labels, training, a model and predictions.
- **Always test on data the rule has never seen**, and ask "accuracy measured on what data?"
- **Deep learning** learns its own features from messy data, at the cost of more data, more compute and unreadable rules.
- **Generative AI creates content and can be confidently wrong**, so this week's habit is **ask the AI, then check its answer**.

---

## Additional Resources

- IBM, *AI vs. machine learning vs. deep learning vs. neural networks: What's the difference?*: https://www.ibm.com/think/topics/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks
- Google for Developers, *Machine Learning Crash Course* (free and interactive; start with the ML Models modules): https://developers.google.com/machine-learning/crash-course
- scikit-learn, *Decision Trees* (the model used in section 4.5): https://scikit-learn.org/stable/modules/tree.html
