# Supervised vs. Unsupervised Learning

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between **supervised** and **unsupervised** learning by asking one simple question: *"Do we have labels?"*
- Distinguish the two main supervised tasks, **classification** and **regression**, and give QE examples of each.
- Describe the three main unsupervised tasks: **clustering**, **dimensionality reduction** and **anomaly detection**.
- Evaluate a classifier with the metrics testers care about most: **confusion matrix, precision and recall**, and explain why accuracy alone can mislead.
- Build and read small Python examples of each approach with scikit-learn, using quality-engineering data.
- Recognise related approaches you will hear about (**semi-supervised**, **self-supervised** and **reinforcement learning**) and know where they appear in modern Generative AI.
- Choose the right approach for a given QE problem and avoid common pitfalls such as bad labels, class imbalance and data leakage.

---

## Why This Matters

In the previous lesson you learned that machine learning means *learning patterns from data*. But "data" comes in two very different situations:

- Sometimes your data comes **with the answers attached**. Every historical bug report already has a severity. Every past build is already marked *passed* or *failed*.
- Sometimes you have **mountains of data but no answers**. Ten thousand failure logs from last month's nightly runs, and nobody has had time to read them.

These two situations call for two different families of machine learning: **supervised** and **unsupervised** learning. Knowing which one fits a problem is the first decision any ML project makes.

For a quality engineer this is practical, not academic. When someone proposes "let's use AI to predict risky releases" or "let's use AI to make sense of our failure logs", you should immediately be able to ask the right questions: *Do we have labels? How good are they? How will we measure success?* This week's epic ends with you building a QA agent; the habit of asking "what is the expected output, and how do I check it?" starts here.

---

## The Concept

### 1. The One Question That Decides: Do We Have Labels?

Recall from the previous lesson that a **label** is the known correct answer for an example.

| | Supervised learning | Unsupervised learning |
|--|---------------------|-----------------------|
| Data | Inputs **and** correct outputs (labels) | Inputs **only** |
| Goal | Learn to **predict** the label for new inputs | **Discover structure** hidden in the data |
| Analogy | Studying with an answer key | Sorting a pile of unlabelled photos into groups that "seem to belong together" |
| Typical question | "Is this new build going to fail?" | "What kinds of failures do we have?" |
| How you check it | Compare predictions with known answers | Harder; usually human judgement plus helper metrics |

The word **supervised** comes from the idea of a teacher (the labels) supervising the learning by saying "right" or "wrong" for each example. In **unsupervised** learning there is no teacher; the algorithm explores on its own.

> **Tester's analogy:** supervised learning is like running tests **with expected results**: you know what correct looks like and can measure pass/fail. Unsupervised learning is like **exploratory testing**: you look for patterns and oddities without a predefined expected result, and a human interprets what you find.

### 2. Supervised Learning

In supervised learning, the training data is a set of pairs:

```text
(input features)                                      -> (label)
(changed_files=12, lines_changed=840, author_new=1)   -> FAILED
(changed_files=2,  lines_changed=35,  author_new=0)   -> PASSED
...
```

The algorithm learns a function that maps inputs to labels well enough that it also works on **new inputs it has never seen**. That ability is called **generalisation**, and it is the entire point.

#### 2.1 The two kinds of supervised task

Supervised problems split by the *type* of label:

| Task | Label type | Question shape | QE examples |
|------|-----------|----------------|-------------|
| **Classification** | A category (from a fixed set) | "Which bucket?" | Will this build pass or fail? Is this failure flaky or a real defect? Is this bug report Critical, Major or Minor? Is this screenshot "layout broken"? |
| **Regression** | A number (continuous value) | "How much? How long?" | How long will the regression suite take? How many defects will this release likely have? What will page load time be under 500 users? |

A quick test to tell them apart: **if the answer has units (seconds, count, dollars), it is usually regression; if the answer is a name or category, it is classification.**

Classification is further divided into:

- **Binary classification:** two classes (pass/fail, flaky/not flaky, spam/not spam).
- **Multi-class classification:** more than two classes, exactly one per example (Critical/Major/Minor/Trivial).
- **Multi-label classification:** an example can have several labels at once (a bug that is tagged both "UI" and "accessibility").

#### 2.2 Common supervised algorithms (names you will hear)

You do not need to know the maths of these today. Just recognise the names:

| Algorithm | Used for | One-line intuition |
|-----------|---------|--------------------|
| Linear regression | Regression | Fit the best straight line (or plane) through the data. |
| Logistic regression | Classification | Despite the name, a classifier: outputs the probability of a class. |
| Decision tree | Both | A learned flowchart of yes/no questions (you saw one in the previous lesson). |
| Random forest / gradient boosting | Both | Many trees voting together; very strong on tabular data. |
| k-nearest neighbours | Both | "You are probably like the examples closest to you." |
| Neural networks | Both | Layers of simple units; the foundation of deep learning (next lesson). |

#### 2.3 Example: classifying risky builds

Let us predict whether a CI build will **fail**, based on properties of the commit. This is a binary classification problem.

```bash
pip install scikit-learn numpy
```

```python
# build_risk_classifier.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(7)
n = 1000

# Features describing each commit
files_changed = rng.integers(1, 40, n)
lines_changed = rng.integers(5, 2000, n)
touches_test_code = rng.integers(0, 2, n)      # 1 if the commit also updated tests
friday_evening = rng.integers(0, 2, n)         # the classic risky time to merge

# Hidden "truth" used only to generate labels for this demo
risk = 0.06 * files_changed + 0.0012 * lines_changed - 1.0 * touches_test_code + 0.8 * friday_evening
probability_fail = 1 / (1 + np.exp(-(risk - 2.5)))
y = (rng.random(n) < probability_fail).astype(int)        # 1 = build failed

X = np.column_stack([files_changed, lines_changed, touches_test_code, friday_evening])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["passed", "failed"]))

# Probability, not just a yes/no answer:
new_commit = [[30, 1500, 0, 1]]     # big change, no test updates, Friday evening
print("Probability this build fails:", round(model.predict_proba(new_commit)[0][1], 2))
```

**Code walkthrough:**

- We create 1,000 synthetic commits with four features. The `risk` formula is hidden "truth" used only to produce realistic labels; in real life the labels come from your CI history.
- `1 / (1 + np.exp(-x))` is the **sigmoid** function. It squashes any number into a probability between 0 and 1. You will meet it again in the neural network lesson.
- `LogisticRegression` learns how much each feature pushes the probability of failure up or down.
- `predict` returns the class (0 or 1). `predict_proba` returns the probability of each class, which is often more useful: a team could decide to run the full regression suite only when the failure probability is above 0.4.
- `confusion_matrix` and `classification_report` are explained in the next section, and they are the most important part of this example for a tester.

#### 2.4 Evaluating a classifier: the tester's view

The **confusion matrix** counts every combination of *actual* answer versus *predicted* answer:

```text
                         PREDICTED
                     passed      failed
ACTUAL  passed   |    TN     |    FP     |
        failed   |    FN     |    TP     |
```

- **True Positive (TP):** predicted *failed*, actually failed. A correct alarm.
- **True Negative (TN):** predicted *passed*, actually passed. Correctly quiet.
- **False Positive (FP):** predicted *failed*, actually passed. A **false alarm**.
- **False Negative (FN):** predicted *passed*, actually failed. A **missed problem**.

Testers already know this matrix by another name. A test that fails when the product is fine is a **false positive**; a test that passes when the product is broken is a **false negative**. A false negative is usually the more dangerous one, because it hides defects.

From the matrix come three key metrics:

| Metric | Formula | Question it answers | When it matters most |
|--------|---------|---------------------|----------------------|
| **Accuracy** | (TP + TN) / all | "How often is the model right overall?" | Only when classes are roughly balanced and both errors cost the same. |
| **Precision** | TP / (TP + FP) | "When it raises an alarm, how often is the alarm real?" | When false alarms are expensive (e.g. paging an on-call engineer at 3 a.m.). |
| **Recall** | TP / (TP + FN) | "Of all the real problems, how many did it catch?" | When misses are expensive (e.g. a defect escaping to production). |

The **F1 score** combines precision and recall into one number, useful when you care about both (explained with numbers below).

#### 2.5 Working the metrics by hand

Formulas become clear once you calculate them yourself. When you run `build_risk_classifier.py`, the confusion matrix for the 250 test builds is:

```text
                         PREDICTED
                     passed      failed
ACTUAL  passed   |  TN = 95   |  FP = 42  |      (137 builds actually passed)
        failed   |  FN = 39   |  TP = 74  |      (113 builds actually failed)
```

Read it like this: of the 113 builds that **really failed**, the model caught 74 and missed 39. It also raised 42 false alarms on builds that were fine.

Now the metrics, treating **failed** as the "positive" class we care about:

```text
Accuracy  = (TP + TN) / all     = (74 + 95) / 250    = 169 / 250 = 0.676  (67.6%)
Precision = TP / (TP + FP)      = 74 / (74 + 42)     = 74 / 116  = 0.638  (63.8%)
Recall    = TP / (TP + FN)      = 74 / (74 + 39)     = 74 / 113  = 0.655  (65.5%)
```

In plain English:

- **Precision 0.64:** when the model says "this build will fail", it is right about 64% of the time. More than one in three of its alarms are false.
- **Recall 0.65:** of all the builds that actually failed, it warned about 65%. About one in three failures came with no warning.

Compare these with the `failed` row of the `classification_report` printed by the script: precision 0.64, recall 0.65. The library is doing exactly this arithmetic.

#### 2.6 F1 and the harmonic mean

Why not simply average precision and recall? Because an ordinary (arithmetic) average can hide a terrible weakness. The **F1 score** uses the **harmonic mean**:

```text
F1 = 2 * (precision * recall) / (precision + recall)
```

The harmonic mean is pulled strongly towards the **smaller** of the two numbers, so a model can only get a high F1 if **both** precision and recall are good. Compare:

| Model | Precision | Recall | Ordinary average | F1 (harmonic mean) |
|-------|-----------|--------|------------------|--------------------|
| Our build-risk model | 0.638 | 0.655 | 0.646 | **0.646** |
| "Only alarms when certain" model | 1.00 | 0.10 | 0.55 | **0.18** |
| "Alarms on everything" model | 0.45 | 1.00 | 0.73 | **0.62** |

The second model catches only 1 failure in 10, yet its ordinary average (0.55) looks almost as good as our model's. F1 (0.18) exposes it immediately. When precision and recall are close, as for our model, F1 and the ordinary average are nearly identical; F1 only differs sharply when one of them is weak, which is exactly when you want a warning.

#### 2.7 The threshold: trading precision against recall

`predict` turns a probability into a yes/no answer using a **threshold**, by default 0.5: "if the probability of failure is at least 0.5, predict failed". You can choose a different threshold yourself using `predict_proba`, and this changes the balance between precision and recall:

```python
# threshold_tradeoff.py  (add to the end of build_risk_classifier.py)
from sklearn.metrics import precision_score, recall_score

fail_probability = model.predict_proba(X_test)[:, 1]     # column 1 = probability of "failed"

for threshold in (0.3, 0.5, 0.7):
    y_pred_t = (fail_probability >= threshold).astype(int)
    print(f"threshold {threshold}: alarms={y_pred_t.sum():3d}  "
          f"precision={precision_score(y_test, y_pred_t):.2f}  "
          f"recall={recall_score(y_test, y_pred_t):.2f}")
```

Typical output:

```text
threshold 0.3: alarms=166  precision=0.56  recall=0.82
threshold 0.5: alarms=116  precision=0.64  recall=0.65
threshold 0.7: alarms= 53  precision=0.77  recall=0.36
```

**Code walkthrough:**

- `predict_proba(X_test)` returns one row per build with two columns: probability of "passed" and probability of "failed". `[:, 1]` selects every row (`:`) from column 1.
- `(fail_probability >= threshold)` produces `True`/`False` for each build; `.astype(int)` turns these into 1/0 predictions.
- `y_pred_t.sum()` counts the 1s, i.e. how many alarms were raised.

**What the output shows:** a **low threshold** raises many alarms, catching most real failures (high recall) but with more false alarms (low precision). A **high threshold** raises few alarms that are usually right (high precision) but misses most failures (low recall). You cannot maximise both at once with the same model; you choose the balance that suits the cost of each mistake:

- "Run the full regression suite when risk is high" → missing a failure is costly, running extra tests is cheap → **low threshold, favour recall.**
- "Block the merge and page a senior engineer" → false alarms annoy people and erode trust → **high threshold, favour precision.**

This is a product decision as much as a technical one, and testers are well placed to help make it.

#### 2.8 The accuracy trap

Suppose only 2% of builds fail. A "model" that **always predicts passed** is 98% accurate, yet it catches **zero** failures. Its recall is 0%. This is called the **accuracy paradox**, and it is why you should never accept "the model is 98% accurate" without asking: *"What are the precision and recall on the class we actually care about?"*

#### 2.9 Example: regression for suite duration

```python
# suite_duration_regression.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(1)
n = 300
num_tests = rng.integers(50, 800, n)
num_ui_tests = (num_tests * rng.uniform(0.1, 0.6, n)).astype(int)
parallel_workers = rng.integers(1, 9, n)

# Hidden truth: UI tests are slow; more workers help
minutes = (0.02 * num_tests + 0.25 * num_ui_tests) / parallel_workers + rng.normal(0, 1.5, n) + 3

X = np.column_stack([num_tests, num_ui_tests, parallel_workers])
X_train, X_test, y_train, y_test = train_test_split(X, minutes, test_size=0.25, random_state=0)

reg = LinearRegression().fit(X_train, y_train)
pred = reg.predict(X_test)
print(f"Mean absolute error: {mean_absolute_error(y_test, pred):.2f} minutes")
print("Predicted minutes for 600 tests, 200 UI, 4 workers:",
      round(reg.predict([[600, 200, 4]])[0], 1))
```

**Code walkthrough:**

- The label is now a **number** (minutes), so this is regression.
- **Mean absolute error (MAE)** is the average distance between prediction and reality, in the label's own units: "on average we are off by about N minutes." Regression uses error metrics such as MAE instead of a confusion matrix.
- Notice the true relationship involves *division* by workers, but `LinearRegression` can only fit straight-line relationships. Its error will be noticeably larger than the noise we added. That is a mild case of **underfitting**: the model family is too simple for the pattern. Try replacing it with `RandomForestRegressor` from `sklearn.ensemble` in the practice exercises and compare the MAE.

### 3. Unsupervised Learning

In unsupervised learning, the data has **no labels**. The algorithm's job is not to predict a known answer but to **find structure**: groups, simplifications or oddities. A human then interprets what it found.

Why is this so useful in QE? Because labelling is expensive. Someone has to read every failure and decide what it is. Unsupervised methods let you get value from data **before** anyone has labelled it, and they can even help you decide *what labels to create*.

#### 3.1 Clustering: finding natural groups

**Clustering** groups similar examples together. The most common algorithm is **k-means**:

1. Choose how many groups you want, **k**.
2. Place k "centre points" (centroids) somewhere in the data.
3. Assign every example to its nearest centre.
4. Move each centre to the average position of its assigned examples.
5. Repeat steps 3-4 until the centres stop moving.

**k-means by hand.** Before the code, let us run the algorithm on paper with six test durations (in seconds) and k = 2:

```text
Durations: 1, 2, 3, 10, 11, 12
Starting centres (chosen badly on purpose): A = 1, B = 2
```

*Round 1 – assign each point to its nearest centre:*

| Point | Distance to A (1) | Distance to B (2) | Assigned to |
|-------|-------------------|-------------------|-------------|
| 1 | 0 | 1 | A |
| 2 | 1 | 0 | B |
| 3 | 2 | 1 | B |
| 10 | 9 | 8 | B |
| 11 | 10 | 9 | B |
| 12 | 11 | 10 | B |

*Move the centres to the average of their points:* A = 1; B = (2 + 3 + 10 + 11 + 12) / 5 = **7.6**.

*Round 2 – assign again with the new centres (A = 1, B = 7.6):* 1, 2 and 3 are now closer to A (for example, 3 is 2 away from A but 4.6 away from B); 10, 11 and 12 are closer to B.

*Move the centres:* A = (1 + 2 + 3) / 3 = **2**; B = (10 + 11 + 12) / 3 = **11**.

*Round 3:* assigning again changes nothing, so the algorithm stops. It found the two natural groups, "fast tests" around 2 seconds and "slow tests" around 11 seconds, even from a poor start and without ever being told the groups existed. Real data has many features instead of one, so "distance" is measured across all of them at once, but the steps are identical.

Example: you have hundreds of failed test runs, each described by duration, memory used and the number of HTTP 5xx responses seen during the test. Nobody has labelled them. Can we discover the kinds of failure we have?

```python
# failure_clustering.py
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(3)

# Three hidden "kinds" of failure (the algorithm is NOT told this)
timeouts = np.column_stack([rng.normal(60, 5, 80),  rng.normal(300, 40, 80), rng.normal(0, 0.5, 80)])
memory   = np.column_stack([rng.normal(20, 6, 60),  rng.normal(1900, 150, 60), rng.normal(0, 0.5, 60)])
backend  = np.column_stack([rng.normal(8, 3, 70),   rng.normal(280, 50, 70), rng.normal(6, 1.5, 70)])
X = np.vstack([timeouts, memory, backend])        # columns: duration_s, memory_mb, http_5xx_count

X_scaled = StandardScaler().fit_transform(X)       # put features on the same scale

kmeans = KMeans(n_clusters=3, n_init=10, random_state=0)
cluster_ids = kmeans.fit_predict(X_scaled)

for c in range(3):
    members = X[cluster_ids == c]
    print(f"Cluster {c}: {len(members)} failures | "
          f"avg duration {members[:, 0].mean():5.1f}s | "
          f"avg memory {members[:, 1].mean():6.0f}MB | "
          f"avg 5xx {members[:, 2].mean():.1f}")
```

**Code walkthrough:**

- We never pass labels to `KMeans`. Only `X`. That is what makes it unsupervised.
- `StandardScaler` is essential here because k-means measures **distance**. Without scaling, memory (in the thousands) would completely dominate duration (in the tens).
- `n_clusters=3` is **k**, a hyperparameter you choose. `n_init=10` runs the algorithm 10 times from different starting points and keeps the best result, because k-means can get stuck in a poor solution.
- The output is just cluster **numbers** (0, 1, 2). The algorithm does not know what they *mean*. A human looks at the averages and says: *"Cluster with long duration and no 5xx = timeouts; huge memory = memory leaks; many 5xx = backend errors."* That interpretation step is always human work.

**How do you choose k?** Common aids are the **elbow method** (plot how tightly grouped the clusters are for k = 1, 2, 3, … and look for the point where adding clusters stops helping much) and the **silhouette score** (a number from -1 to 1 measuring how well separated clusters are). These are helpers, not answers. Domain knowledge decides in the end.

#### 3.2 Dimensionality reduction: simplifying many features

Real data can have hundreds of features. **Dimensionality reduction** compresses them into fewer features while keeping most of the useful information. The classic algorithm is **Principal Component Analysis (PCA)**.

Uses in QE:

- **Visualisation:** squash 50 metrics about each test run down to 2 numbers and plot them, so humans can *see* groups and outliers.
- **Speed:** fewer features mean faster training for later models.
- **Noise removal:** dropping the least informative directions can remove noise.

```python
# pca_example.py
import numpy as np
from sklearn.decomposition import PCA

rng = np.random.default_rng(0)
base = rng.normal(size=(200, 2))
# 6 correlated metrics per test run (e.g. CPU, memory, duration, network bytes, ...)
X = np.column_stack([base[:, 0], base[:, 0] * 2, base[:, 1],
                     base[:, 1] * 0.5, base[:, 0] + base[:, 1], rng.normal(0, 0.1, 200)])

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)
print("Shape before:", X.shape, "after:", X_2d.shape)
print("Share of information kept:", round(pca.explained_variance_ratio_.sum(), 3))
```

**Code walkthrough:**

- `base` holds two hidden "underlying factors" per test run (imagine *system load* and *network quality*). We then build **six** visible metrics from them: some are copies or multiples of one factor (`base[:, 0] * 2`), one mixes both, and one is pure noise. This mimics real monitoring data, where CPU, memory and duration often rise and fall together because they share a cause.
- `PCA(n_components=2)` asks PCA to find the **two directions** in the six-dimensional data along which the test runs differ the most. These new directions are called **principal components**.
- `fit_transform(X)` learns those directions and re-expresses every test run as just two numbers: its position along component 1 and along component 2. Shape goes from `(200, 6)` to `(200, 2)`.
- `explained_variance_ratio_` tells you how much of the original **variation** (spread) in the data each component captures. Here it prints about `[0.758, 0.241]`: the first component keeps about 76% of the variation, the second about 24%, together about 99.9%. Only the tiny noise column is lost.
- **Note:** the components are not any of the original metrics. They are new, combined measurements. PCA does not tell you what they mean; as with clustering, a human interprets them.

**An analogy: shadows.** Imagine a 3-D wire sculpture lit by a lamp. Its shadow on the wall is 2-D, yet if you turn the sculpture to the right angle, the shadow still shows most of its shape. PCA finds the "best angle" for casting a high-dimensional dataset onto fewer dimensions, keeping as much of the shape (variation) as possible.

**When PCA helps and when it does not:** it works best when features are **correlated** (several metrics measuring overlapping things), as in this example. If every feature were independent, there would be no shortcut, and dropping dimensions would throw away real information. Always check `explained_variance_ratio_` before trusting the compressed version.

Here six metrics compress into two numbers while keeping almost all the variation, because most of the original metrics were measuring the same underlying things. You will meet a related idea, turning text into lists of numbers called **embeddings**, in the NLP and Generative AI lessons later today.

#### 3.3 Anomaly detection: finding the odd ones out

**Anomaly (outlier) detection** finds examples that look unlike the rest. It is extremely useful for monitoring, because you rarely have labelled examples of every possible problem in advance.

```python
# response_time_anomalies.py
import numpy as np
from sklearn.ensemble import IsolationForest

rng = np.random.default_rng(5)
normal_ms = rng.normal(220, 25, 495)                 # typical API response times
spikes_ms = np.array([900, 1250, 40, 1100, 980])     # a few strange ones
response_ms = np.concatenate([normal_ms, spikes_ms]).reshape(-1, 1)

detector = IsolationForest(contamination=0.01, random_state=0)
flags = detector.fit_predict(response_ms)            # -1 = anomaly, 1 = normal

print("Anomalies found (ms):", np.sort(response_ms[flags == -1].ravel()).round(0))
```

**Code walkthrough:**

- `IsolationForest` works on a clever idea: unusual points are **easier to isolate** with random splits than normal points packed in a crowd.
- `contamination=0.01` tells it to expect roughly 1% anomalies. This is an assumption you must think about; set it wrong and you get too many or too few alerts.
- Notice it flags the suspiciously **fast** 40 ms response too. Testers know why that matters: an API that answers instantly might be returning an error page or cached empty data. Not every anomaly is "too slow". This ties back to the response validation you practised in Week 7.

### 4. Supervised vs. Unsupervised: Side by Side

| Aspect | Supervised | Unsupervised |
|--------|-----------|--------------|
| Needs labels? | Yes | No |
| Main tasks | Classification, regression | Clustering, dimensionality reduction, anomaly detection |
| Output | A prediction for each new input | Groups, compressed features, outlier flags |
| Evaluation | Clear: compare with known answers (accuracy, precision, recall, MAE) | Fuzzier: helper metrics plus human interpretation |
| Cost driver | Collecting good labels | Interpreting results |
| Typical QE use | Predict build failure, classify bug severity, estimate run time | Group failure logs, find unusual performance runs, explore a new dataset |
| Biggest risk | Learning from wrong or biased labels | Finding patterns that look meaningful but are not |

The two are often **combined**. A common real workflow:

1. Use **clustering** on 10,000 unlabelled failures to discover that there are about six kinds.
2. Have engineers name those six kinds and label a few hundred examples.
3. Train a **supervised classifier** on those labels to triage future failures automatically.

### 5. Beyond the Two Main Families

You will hear three more terms this week. Here is just enough to recognise them.

| Approach | Idea | Where you will meet it |
|----------|------|------------------------|
| **Semi-supervised learning** | Train with a small labelled set plus a large unlabelled set. | When labelling is expensive, e.g. 200 labelled bug reports and 20,000 unlabelled ones. |
| **Self-supervised learning** | The data creates its own labels. For text: hide the next word and ask the model to predict it; the real next word is the label. | This is how large language models are **pre-trained** on huge amounts of text. You will see why this matters in the Generative AI lessons later today. |
| **Reinforcement learning (RL)** | An agent learns by **trial and error**, receiving rewards or penalties for its actions. | Game-playing AI, robotics, and a technique used to tune LLMs using human feedback (RLHF), introduced in today's Generative AI concepts lesson. |

### 6. Choosing the Right Approach

Use this simple decision flow when someone proposes an ML idea:

```text
What do you want?
|
+-- To PREDICT something for new cases?
|     |
|     +-- Do you have enough trustworthy labelled examples?
|           +-- Yes --> SUPERVISED
|           |            +-- Label is a category --> CLASSIFICATION
|           |            +-- Label is a number   --> REGRESSION
|           +-- No  --> Label some data first, or start with UNSUPERVISED exploration
|
+-- To UNDERSTAND or EXPLORE data you have not labelled?
      +-- Find groups              --> CLUSTERING
      +-- Simplify / visualise     --> DIMENSIONALITY REDUCTION
      +-- Find unusual cases       --> ANOMALY DETECTION
```

### 7. Common Pitfalls (and How a Tester Spots Them)

| Pitfall | What happens | How to spot or prevent it |
|---------|-------------|---------------------------|
| **Bad labels** | Bug severities were set inconsistently by different people; the model learns the inconsistency. | Sample and review labels; measure how often two people agree. |
| **Class imbalance** | Failures are rare, so the model learns to always say "pass". | Check recall on the rare class; use stratified splits; consider class weights. |
| **Data leakage** | A feature secretly contains the answer, e.g. using `"was_rolled_back"` to predict whether a release fails. Test scores look amazing, then real use fails. | Ask of every feature: *"Would I really know this value at prediction time?"* |
| **Unscaled features** | Distance-based methods (k-means, k-NN) are dominated by large-valued features. | Scale features (`StandardScaler`) before distance-based algorithms. |
| **Over-reading clusters** | Every clustering run produces clusters, even on random noise. | Check if clusters are stable across runs and meaningful to domain experts. |

---

## Practice Exercises

1. **Classify the problem.** For each, say *supervised or unsupervised*, and if supervised, *classification or regression*:
   - (a) Predict how many minutes a Playwright suite will take on a new branch.
   - (b) Group 5,000 customer-reported bugs into themes nobody has defined yet.
   - (c) Decide whether a new bug report is a duplicate of an existing one, given 3,000 past reports marked "duplicate" or "not duplicate".
   - (d) Alert when tonight's API response times look unusual compared with the last 30 nights.
2. **Metrics reasoning.** A model that flags risky pull requests has precision 0.9 and recall 0.3. Describe in plain English what developers will experience. Is that acceptable for a "block the merge" gate? For a "suggest extra review" hint?
3. **Run and extend.** Run `suite_duration_regression.py`, then swap `LinearRegression` for `RandomForestRegressor(random_state=0)` from `sklearn.ensemble`. Compare the MAE and explain the difference using the word *underfitting*.
4. **Choose k.** In `failure_clustering.py`, try `n_clusters` values from 2 to 6 and print `silhouette_score(X_scaled, cluster_ids)` (import it from `sklearn.metrics`). Which k scores best? Does that match the number of hidden failure types?
5. **Metrics by hand.** A flaky-test detector is evaluated on 200 failures: TP = 30, FP = 10, FN = 20, TN = 140. Calculate accuracy, precision, recall and F1 by hand. Then write one sentence explaining each number to a non-technical product owner.
6. **Pick a threshold.** Run `threshold_tradeoff.py` with thresholds 0.2, 0.4 and 0.6. Which threshold would you choose for (a) automatically re-running the full suite, and (b) posting an alert in the team chat? Justify each choice using the cost of false positives and false negatives.
7. **Project 2 brainstorm.** For a generic web application under test in Project 2, list one supervised and one unsupervised idea that could help your team. For each, state where the data would come from and, for the supervised idea, where the labels would come from.

---

## Knowledge Check

1. What single question best distinguishes supervised from unsupervised learning?
2. Give one classification and one regression example from QE.
3. Why is accuracy a poor metric when only 2% of builds fail?
4. What does a k-means algorithm output, and what must a human still do with it?
5. What is self-supervised learning, and which famous kind of model is pre-trained this way?
6. If you lower a classifier's decision threshold from 0.5 to 0.3, what usually happens to precision and to recall?

<details>
<summary>Suggested answers</summary>

1. "Do we have labels (known correct answers) for the training data?"
2. Classification: flaky vs. genuine failure. Regression: predicted suite duration in minutes. (Other valid answers exist.)
3. A model that always predicts "pass" would score 98% while catching no failures; precision and recall on the failure class reveal this.
4. A cluster number for each example (and the cluster centres). A human must interpret what each cluster means and decide if it is useful.
5. Learning where labels are created from the data itself (e.g. predicting the next word). Large language models are pre-trained this way.
6. More alarms are raised: recall usually rises (fewer misses) and precision usually falls (more false alarms).

</details>

---

## Glossary

- **Supervised learning:** Learning from examples that include correct answers (labels).
- **Unsupervised learning:** Finding structure in data without labels.
- **Classification / Regression:** Predicting a category / predicting a number.
- **Confusion matrix:** Table counting true/false positives and negatives.
- **Precision:** Of the predicted positives, the fraction that were truly positive.
- **Recall:** Of the true positives, the fraction the model found.
- **F1 score:** The harmonic mean of precision and recall; high only when both are high.
- **Threshold:** The probability cut-off above which a classifier predicts the positive class.
- **Clustering:** Grouping similar examples without labels.
- **k-means:** A clustering algorithm that groups points around k centres.
- **PCA:** A dimensionality-reduction technique that compresses many features into fewer.
- **Principal component:** A new combined direction found by PCA along which the data varies most.
- **Explained variance ratio:** The share of the data's variation captured by each principal component.
- **Anomaly detection:** Finding examples that differ markedly from the rest.
- **Data leakage:** When training data contains information that would not be available at prediction time.

---

## Summary

- **Supervised learning** learns from labelled examples to **predict** answers for new inputs. It splits into **classification** (categories) and **regression** (numbers).
- **Unsupervised learning** finds **structure** in unlabelled data: **clusters**, **compressed representations** and **anomalies**. Humans interpret the results.
- Evaluate classifiers with the **confusion matrix, precision, recall and F1**, and calculate them by hand until they feel natural; never trust accuracy alone on imbalanced data.
- The **decision threshold** trades precision against recall; choose it based on the cost of false alarms versus missed problems.
- Real projects often **combine** both: cluster first to understand, then label and train a classifier.
- **Self-supervised learning** (predict the hidden next word) is how LLMs are pre-trained; you will see why that matters later today.
- Testers' instincts (question the labels, check the rare cases, look for leakage) are exactly what ML projects need.

---

## Additional Resources

- scikit-learn User Guide, *Supervised learning*: https://scikit-learn.org/stable/supervised_learning.html
- scikit-learn User Guide, *Unsupervised learning*: https://scikit-learn.org/stable/unsupervised_learning.html
- Google for Developers, *Machine Learning Crash Course* (see the classification module for precision and recall): https://developers.google.com/machine-learning/crash-course
