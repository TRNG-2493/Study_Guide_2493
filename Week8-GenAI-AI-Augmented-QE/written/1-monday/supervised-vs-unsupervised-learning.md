# Supervised vs. Unsupervised Learning

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** the difference between supervised and unsupervised learning using one question: *"Do we have labels?"*
- **Compare** the two kinds of supervised task, classification and regression, and give a testing example of each.
- **Check** a supervised prediction by working out the pattern in labelled data yourself, and judge whether an AI's reasons come from the data.
- **Group** unlabelled failures by hand, and explain why a person, not the algorithm, must name the groups.
- **Calculate** precision and recall for a small example, and explain why accuracy alone can mislead.
- **Spot** three common data problems: wrong labels, class imbalance and data leakage.

---

## Why This Matters

In the previous lesson, *Artificial Intelligence, Machine Learning and Deep Learning*, you learned that machine learning finds rules in examples. Every row in that flaky-test table had a **label**, because a tester had already investigated it. That is not always the case.

In real QE work, data arrives in two very different states:

- **With answers attached.** Every past build in your CI history is already marked *passed* or *failed*. Every closed bug already has a severity.
- **Without answers.** Last night's run produced 500 failures, and nobody has had time to read them.

These two states need two different families of machine learning: **supervised** and **unsupervised**. Choosing between them is the first decision in any ML project, and it is a question a tester can ask in any meeting: *"Where do the labels come from, and who checked them?"*

This week you will use AI assistants for both kinds of job: predicting from labelled history, and finding groups in unlabelled data. Knowing which one you are doing tells you how to check the answer.

> **Using this with the handout:** this lesson goes deeper into **Handout 01, Topic 2**. It uses the same commits (A–L), the same failures (F1–F10) and the same two prompts.

---

## The Concept

### 1. The One Question That Decides: Do We Have Labels?

Recall that a **label** is the correct answer for an example. The question "do we have labels?" decides almost everything else:

| | Supervised learning | Unsupervised learning |
|---|---|---|
| Data has answers? | ✅ Yes (labels) | ❌ No |
| Goal | **Predict** the answer for new examples | **Discover** groups or unusual items |
| QE example | "Will this commit break the build?" | "Which of these 500 failures look alike?" |
| Typical methods | Classification, regression | Clustering, anomaly detection |
| How you check it | Compare predictions with known answers | Harder: a person judges whether the groups make sense |

The word **supervised** comes from the idea of a teacher. The labels act like a teacher who says "right" or "wrong" for each example. In **unsupervised** learning there is no teacher, so the algorithm explores the data on its own.

> **Tester's analogy:** supervised learning is like running tests **with expected results**. You know what correct looks like, so you can measure pass or fail. Unsupervised learning is like **exploratory testing**: you look for patterns and surprises without a script, and a person decides what they mean.

### 2. Supervised Learning

In supervised learning, the training data is a set of **(input, label)** pairs. The algorithm learns a rule that maps inputs to labels well enough to work on **new inputs it has never seen**. That ability is called **generalisation**, and it is the whole point. A model that only works on its training data is useless.

#### 2.1 Two kinds of supervised task

Supervised problems split by the *type* of label:

| Task | Label type | Question shape | QE examples |
|---|---|---|---|
| **Classification** | A category from a fixed set | "Which bucket?" | Will this build pass or fail? Is this bug Critical, Major or Minor? |
| **Regression** | A number | "How much? How long?" | How many minutes will the regression suite take? How many defects will this release have? |

A quick way to tell them apart: **if the answer has units (seconds, items, dollars), it is usually regression. If the answer is a name or category, it is classification.**

Classification has two common forms:

- **Binary:** two classes, such as pass/fail or flaky/not flaky.
- **Multi-class:** more than two classes, one per example, such as Critical/Major/Minor.

#### 2.2 Worked example: will this commit break the build?

Here are 10 past commits from the handout, with the build result for each. The `build_result` column is the **label**, so this is supervised learning, and the task is classification.

| Commit | Files changed | Tests updated? | Build result |
|---|---|---|---|
| A | 2 | Yes | Passed |
| B | 3 | Yes | Passed |
| C | 1 | No | Passed |
| D | 4 | Yes | Passed |
| E | 5 | No | Passed |
| F | 25 | No | Failed |
| G | 30 | No | Failed |
| H | 18 | No | Failed |
| I | 22 | Yes | Passed |
| J | 35 | No | Failed |

**Find the pattern by hand first.** Sort the rows in your head:

- Every **small** commit (1–5 files) passed, with or without test updates.
- Every **large** commit (18 or more files) **without** test updates failed: F, G, H and J.
- The one large commit **with** test updates, I (22 files), passed.

So one rule that fits all 10 rows is: **"A commit fails if it changes more than 10 files and does not update tests."** You have just done what a classifier does: turned labelled examples into a rule.

Now predict the two new commits from the handout:

| Commit | Files changed | Tests updated? | Prediction | Why |
|---|---|---|---|---|
| K | 2 | Yes | **Pass** | Small, with tests, like A, B and D |
| L | 32 | No | **Fail** | Large, without tests, like F, G, H and J |

Both predictions are confident because each new commit looks very like several training examples.

**Where generalisation gets hard.** Now imagine a commit **P: 9 files, no tests**. The training data has nothing between 5 and 18 files. Is 9 "small" or "large"? The rule says "more than 10", but the number 10 was **our choice**; any cut-off from 5 to 17 files fits the data equally well.

The honest answer is: *"We don't know; there are no similar examples."* A model will still give an answer, usually with no warning that it is guessing. Testers should ask: **"Does the training data contain examples like this one?"**

#### 2.3 Asking an AI to do the same job

In the lecture, you paste the commit data into an AI assistant and ask it to predict K and L. The prompt ends with:

```text
Based ONLY on this data, predict whether these two new commits will fail, and give a one-line reason for each:
K, 2, Yes
L, 32, No
```

The words **"Based ONLY on this data"** matter. An AI assistant has read a huge amount of text about software, and it may bring in outside opinions. Compare two reasons it might give for L. Both are **illustrative**, written for this lesson:

```text
Reason 1: L is large (32 files) and has no test updates, like F, G and J, which all failed.
Reason 2: Large commits are risky, and commits made late in the week often break builds.
```

**Reason 1** points to a pattern **in the data**. **Reason 2** brings in a claim about "late in the week", but the data has no column for the day. It may sound wise, but it was not learned from these examples. When you review an AI's prediction, check that **every reason can be traced to the data you gave it**. A reason you cannot trace is a hallucination risk, even when the prediction itself is right.

#### 2.4 Evaluating a classifier: false alarms and misses

To know how good a classifier is, you compare its predictions with the real answers on test data. Testers already know the vocabulary, from the results of their own test suites:

- **True positive:** predicted *fail*, really failed. A correct alarm.
- **True negative:** predicted *pass*, really passed. Correctly quiet.
- **False positive:** predicted *fail*, really passed. A **false alarm**.
- **False negative:** predicted *pass*, really failed. A **missed problem**.

A test that fails when the product is fine is a false positive. A test that passes when the product is broken is a false negative, and that is usually the worse mistake, because a defect escapes.

**Work it by hand.** A build-risk model is tried on 50 new commits. Here is what happened:

- The model warned that **10** commits would fail.
- Of those 10, **6** really failed (true positives), and **4** passed (false positives).
- In total, **8** of the 50 commits really failed. So **2** failures got no warning (false negatives).

Two numbers describe this better than one:

| Metric | Formula | Our example | Question it answers |
|---|---|---|---|
| **Precision** | true positives ÷ all warnings | 6 ÷ 10 = **0.60** | "When it warns, how often is it right?" |
| **Recall** | true positives ÷ all real failures | 6 ÷ 8 = **0.75** | "Of the real failures, how many did it catch?" |

In plain words: 4 of its 10 warnings were false alarms, and it missed 1 in 4 real failures.

Which number matters more depends on the cost of each mistake:

- If a warning only means "run the full regression suite", false alarms are cheap and misses are costly. **Favour recall.**
- If a warning blocks the merge and pages a senior engineer at night, false alarms erode trust. **Favour precision.**

That is a product decision as much as a technical one, and testers are well placed to help make it.

#### 2.5 The accuracy trap

**Accuracy** is the share of all predictions that were right. It sounds like the obvious measure, but it can badly mislead.

Suppose only **2%** of builds fail. A "model" that **always predicts pass** is right 98% of the time, so its accuracy is 98%. Yet it catches **zero** failures: its recall is 0. This is called the **accuracy paradox**, and it happens whenever one class is much rarer than the other.

So never accept "the model is 98% accurate" on its own. Ask: **"What are its precision and recall on the class we care about?"**

### 3. Unsupervised Learning

In unsupervised learning, the data has **no labels**. The algorithm's job is not to predict a known answer but to **find structure**: groups of similar items, or items that do not fit. A person then decides what the structure means.

Why is this useful in QE? Because **labelling is expensive**. Someone has to read each failure and decide what it is. Unsupervised methods give you value **before** anyone has labelled anything, and they can make labelling faster later.

#### 3.1 Clustering: finding natural groups

**Clustering** puts similar examples into groups, called **clusters**. Here are the 10 unlabelled failures from the handout:

| Failure | Duration (s) | Memory (MB) |
|---|---|---|
| F1 | 61 | 300 |
| F2 | 58 | 280 |
| F3 | 63 | 310 |
| F4 | 9 | 1,900 |
| F5 | 12 | 2,100 |
| F6 | 10 | 1,850 |
| F7 | 8 | 290 |
| F8 | 7 | 260 |
| F9 | 9 | 300 |
| F10 | 60 | 320 |

There is no "cause" column. Nobody has said what any of these failures are.

**Group them by hand.** Look at each column in turn:

- **Duration** splits the rows into slow ones (about 60 seconds: F1, F2, F3, F10) and fast ones (7–12 seconds: everything else).
- **Memory** splits the fast ones again: a few use about 2,000 MB (F4, F5, F6), and the rest use a normal 260–300 MB (F7, F8, F9).

That gives three groups:

| Group | Members | What they have in common |
|---|---|---|
| 1 | F1, F2, F3, F10 | Slow, normal memory |
| 2 | F4, F5, F6 | Fast, huge memory |
| 3 | F7, F8, F9 | Fast, normal memory |

Notice the "what they have in common" column describes the **data**, not a cause. That is all an algorithm can do.

#### 3.2 The person names the groups

The algorithm can say "these four belong together", but it cannot say **why**. Naming the groups is a person's job, and it needs testing knowledge:

- **Group 1** (slow, normal memory) looks like **timeouts**: tests waiting about a minute for something that never arrives.
- **Group 2** (fast, huge memory) looks like **memory problems**: something loads far too much data and crashes quickly.
- **Group 3** (fast, normal memory) is a **different cause**, perhaps a backend returning an error straight away.

These names are **hypotheses**, not facts. The next step is to open one failure from each group and confirm. That is why the handout's prompt tells the AI: *"Do NOT name or explain the groups."* If the AI names them, it is guessing, and its confident guess can stop you from looking.

#### 3.3 How an algorithm does it: k-means

The most common clustering algorithm is **k-means**. It works like this:

1. You choose how many groups you want, **k** (here, 3).
2. It places k centre points in the data.
3. It assigns every example to its nearest centre.
4. It moves each centre to the average of the examples assigned to it.
5. It repeats steps 3 and 4 until the centres stop moving.

The demo below runs k-means on the same 10 failures. It needs scikit-learn (`python -m pip install scikit-learn`).

```python
# group_failures.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 10 unlabelled failures: [duration_seconds, memory_mb]
ids = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]
X = [[61, 300], [58, 280], [63, 310], [9, 1900], [12, 2100],
     [10, 1850], [8, 290], [7, 260], [9, 300], [60, 320]]

X_scaled = StandardScaler().fit_transform(X)        # put both columns on the same scale
model = KMeans(n_clusters=3, n_init=10, random_state=0)
groups = model.fit_predict(X_scaled)                # no labels given: unsupervised

for g in sorted(set(groups)):
    members = [i for i, grp in zip(ids, groups) if grp == g]
    print(f"Group {g}: {', '.join(members)}")
```

Output:

```text
Group 0: F4, F5, F6
Group 1: F7, F8, F9
Group 2: F1, F2, F3, F10
```

What to notice:

- `X` has **no label column**. `fit_predict(X_scaled)` is given only the features. That is what makes it unsupervised.
- `n_clusters=3` is k. **You** chose 3; the algorithm did not discover it. With k = 2, two of the groups would be forced together.
- The output is only **numbers** (0, 1, 2), in no meaningful order. The algorithm has no idea what the groups mean.
- `StandardScaler` puts both columns on a similar scale before measuring distances.

That last line matters more than it looks. k-means groups items by **distance**, and memory values (in the thousands) are far bigger than durations (in the tens). We ran the same script **without** the scaler, and the result was: `F4, F6` in one group, `F5` alone, and **all seven others together**, mixing the slow timeouts with the fast backend errors. Memory swamped duration, so duration was ignored. When an AI tool or a library groups your data, ask: **"Were the features on comparable scales?"**

#### 3.4 Anomaly detection: finding the odd ones out

**Anomaly detection** (also called outlier detection) finds examples that look unlike the rest. It is very useful for monitoring, because you rarely have labelled examples of every possible problem in advance.

Picture last night's performance run: 10,000 API calls, most taking 180–260 ms. An anomaly detector flags a handful at 4,000 ms, which is no surprise. It may also flag a few at **40 ms**. Testers know why that matters: an API that answers suspiciously fast might be returning an error page or empty cached data. Not every anomaly is "too slow".

#### 3.5 One more unsupervised idea: simplifying many features

Real test data can have dozens of measurements per run: CPU, memory, response times, error counts and more. **Dimensionality reduction** compresses many features into a few, keeping most of the useful information. A common method is **principal component analysis (PCA)**. Its main use in QE is **visualisation**: squash 50 metrics into 2 numbers and plot them, so people can *see* groups and outliers. You do not need the details this week; just recognise the name.

### 4. Supervised vs. Unsupervised: Side by Side

| Aspect | Supervised | Unsupervised |
|---|---|---|
| Needs labels? | Yes | No |
| Main tasks | Classification, regression | Clustering, anomaly detection, dimensionality reduction |
| Output | A prediction for each new example | Groups, outlier flags, simplified features |
| How you check it | Compare with known answers: precision, recall | A person judges whether the groups make sense |
| Main cost | Collecting good labels | Interpreting the results |
| Biggest risk | Learning from wrong or biased labels | Finding patterns that look meaningful but are not |

The two are often **combined**. A common workflow:

1. Use **clustering** on 10,000 unlabelled failures and discover there are about six kinds.
2. Engineers name the six kinds and label a few hundred examples.
3. Train a **supervised classifier** on those labels to sort future failures automatically.

Unsupervised learning finds the categories; supervised learning applies them at scale.

### 5. Beyond the Two Main Families

You will hear three more terms this week. Here is enough to recognise them:

| Approach | Idea | Where you will meet it |
|---|---|---|
| **Semi-supervised learning** | Learn from a small labelled set plus a large unlabelled set | When labelling is expensive: 200 labelled bug reports, 20,000 unlabelled |
| **Self-supervised learning** | The data supplies its own labels; for example, hide the next word in a sentence and learn to predict it | How large language models are trained, which you will see later today in *Generative AI Concepts* |
| **Reinforcement learning** | Learn by trial and error from rewards and penalties | Game-playing systems, and one step in making chat assistants helpful (also later today) |

### 6. A Real Example: Sorting Firefox Bug Reports

Mozilla receives hundreds of Firefox bug reports a day, and each must reach the right team. In 2019 Mozilla described **BugBug**, a supervised ML tool that suggests the product and component for each new bug. It was trained on more than two years of past bug reports, around 100,000 bugs, using features from each bug's title, first comment, and keywords ([Mozilla Hacks, 2019](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)).

Two details in that story show a tester's thinking at work:

- **The labels already existed.** Past bugs had been assigned to components by people, so the history was ready-made training data. This is the usual way supervised learning starts in QE: your tracker and CI history already hold labels.
- **They had to "roll back" each bug.** Mozilla noted that the bug data could not be used as it was, because a bug changes after triage. The tool would never see those later changes when a new bug arrives. So each bug was rolled back to how it looked **when it was first filed**. Without that step, the model would learn from information it can never have in real use. That trap has a name, **data leakage**, covered next.

### 7. Common Pitfalls, and How a Tester Spots Them

#### 7.1 Wrong labels: garbage in, garbage out

A supervised model learns whatever the labels say, including their mistakes. Go back to the commit table and imagine a tester mislabelled **H** (18 files, no tests) as *Passed*.

Now the failed commits are only F (25), G (30) and J (35). A rule that fits all 10 rows becomes: **"Fails if more than 20 files and no tests."** A new commit with **19 files and no tests** is now predicted to **pass**, because of one wrong label. The model is not broken; it faithfully learned a wrong lesson.

**How to spot it:** sample some labels and check them by hand, and ask how the labels were produced. "Whatever the developer selected in the form" is weaker than "confirmed during triage".

#### 7.2 Class imbalance

When one class is rare, such as builds that fail 2% of the time, a model can score high accuracy by mostly ignoring it (section 2.5). **How to spot it:** ask for the class balance, and look at precision and recall for the rare class, not overall accuracy.

#### 7.3 Data leakage

**Data leakage** means the model is trained with information it will not have when making real predictions. It looks excellent in testing, then fails in real use.

A classic QE example: predicting whether a build will fail, using a feature called "number of failed tests in this build". Of course it predicts perfectly. That feature **is** the answer, and you only know it after the build runs. Mozilla's roll-back step in section 6 was a guard against the same trap.

**How to spot it:** for every feature, ask: **"Would we know this value at the moment we need the prediction?"** If not, it is leaking the answer.

#### 7.4 Groups that look meaningful but are not

Clustering always returns groups, even for random data. Ask for 3 groups and you get 3, whether or not 3 real kinds exist. **How to spot it:** open a few members of each group and check that they really share a cause. Try a different number of groups and see whether the groups stay stable.

---

## Practice Exercises

1. **Supervised or unsupervised? (paper, 10 min)** For each situation, write the approach, and for supervised ones, whether it is classification or regression:
   - (a) Estimate how long a Playwright suite will take from the number of tests and workers, using 6 months of run history.
   - (b) Find unusual login-response times in last night's load test, with no examples of "bad" runs.
   - (c) Decide whether a new bug report is a duplicate, using 5,000 past reports already marked duplicate or not.
   - (d) Discover the main themes in 800 app-store reviews nobody has read yet.

2. **Precision and recall (paper, 10 min).** A flaky-test detector checks 100 failures. It flags 20 as flaky. Of those 20, 15 really are flaky. In total, 25 of the 100 failures are flaky. Work out precision and recall. Then say which matters more if "flaky" tests are automatically skipped in the release pipeline, and why.

   *Hint:* skipping a real defect means it ships.

3. **Does the AI follow the data? (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** paste the handout's unsupervised prompt (F1–F10), but add one more row: `F11, 35, 1200`. Keep "exactly 3 groups" and "Do NOT name or explain the groups".
   - **Review:** where did the AI put F11? Did it obey "do not name the groups"? Is F11 really like the other members of its group?
   - **Run:** add `[35, 1200]` to `X` and `"F11"` to `ids` in `group_failures.py`, run it, and compare.
   - **Record:** write two sentences on what the AI did with an item that fits no group well, and whether anomaly detection would suit F11 better than clustering.

4. **Hunt the leak (paper, 10 min).** A team wants to predict, **before** a release, whether it will need a hotfix. Their features: lines of code changed, number of open bugs at release time, number of support tickets in the week after release, and test coverage. Which feature leaks the answer, and why?

---

## Knowledge Check

1. What single question decides whether a problem is supervised or unsupervised?

<details><summary>Answer</summary>

"Do we have labels?" If the examples come with the correct answers, it is supervised; if not, it is unsupervised.

</details>

2. "Predict how many minutes the regression suite will take." Is this classification or regression?

<details><summary>Answer</summary>

Regression. The answer is a number with units (minutes), not a category.

</details>

3. A clustering tool returns three groups of failures. Who decides what each group means, and why?

<details><summary>Answer</summary>

A person. The algorithm only knows that items are similar in the data; it cannot know the cause. A tester names each group as a hypothesis, then checks real examples to confirm.

</details>

4. A model warns on 10 builds; 6 of them really fail. In total, 8 builds fail. What are its precision and recall?

<details><summary>Answer</summary>

Precision = 6 ÷ 10 = 0.60. Recall = 6 ÷ 8 = 0.75.

</details>

5. Why can a model that is 98% accurate be useless?

<details><summary>Answer</summary>

If only 2% of cases are the class you care about, a model that always predicts the common class is 98% accurate but catches none of the rare cases (recall 0).

</details>

6. What is data leakage, and what question helps you spot it?

<details><summary>Answer</summary>

Training a model with information it will not have when it makes real predictions, so it looks great in testing and fails in use. Ask of every feature: "Would we know this value at the moment we need the prediction?"

</details>

---

## Glossary

- **Supervised learning:** learning from examples that come with the correct answers (labels).
- **Unsupervised learning:** finding structure in examples that have no labels.
- **Generalisation:** a model's ability to work on new examples it has not seen.
- **Classification:** supervised learning that predicts a category.
- **Regression:** supervised learning that predicts a number.
- **True / false positive:** a correct alarm / a false alarm.
- **True / false negative:** correctly quiet / a missed problem.
- **Precision:** of all the warnings, the share that were right.
- **Recall:** of all the real problems, the share that were caught.
- **Accuracy:** the share of all predictions that were right; misleading when classes are imbalanced.
- **Accuracy paradox:** a high accuracy score that hides a model's failure on a rare class.
- **Clustering:** grouping similar examples without labels.
- **Cluster:** one group found by clustering.
- **k-means:** a clustering algorithm that groups items around k centre points.
- **Scaling:** putting features on comparable ranges so no single feature dominates.
- **Anomaly detection:** finding examples that look unlike the rest.
- **Dimensionality reduction / PCA:** compressing many features into a few.
- **Semi-supervised / self-supervised / reinforcement learning:** learning from a few labels plus many unlabelled examples / from labels the data supplies itself / from rewards and penalties.
- **Class imbalance:** one class being much rarer than another.
- **Data leakage:** training with information that will not be available at prediction time.

---

## Summary

- **"Do we have labels?"** decides the approach: yes means supervised, no means unsupervised.
- **Supervised learning predicts**: categories (classification) or numbers (regression). It is only useful if it generalises to new examples, and it struggles with examples unlike anything in its training data.
- **Check every AI reason against the data.** A reason you cannot trace to the data is a guess, even when the prediction is right.
- **Measure classifiers with precision and recall**, not accuracy alone, and decide which matters more from the cost of false alarms and misses.
- **Unsupervised learning discovers**: groups and outliers. The algorithm finds the groups; **a person names them**, and scaling the features changes what it finds.
- **Watch for bad labels, class imbalance and data leakage**: three places a tester's questions save an ML project.

---

## Additional Resources

- Google for Developers, *Machine Learning Crash Course: Accuracy, recall, precision and related metrics*: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall
- scikit-learn, *Clustering* (k-means and other clustering methods): https://scikit-learn.org/stable/modules/clustering.html
- Mozilla Hacks, *Teaching machines to triage Firefox bugs* (the real example in section 6): https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/
