# Artificial Intelligence, Machine Learning and Deep Learning

## Learning Objectives

By the end of this lesson you will be able to:

- Define **Artificial Intelligence (AI)**, **Machine Learning (ML)** and **Deep Learning (DL)** in plain language, and explain how they nest inside one another.
- Explain the difference between **traditional (rule-based) programming** and **learning from data**, using a testing example.
- Describe the basic ML vocabulary you will hear all week: **data, features, labels, model, training, inference, parameters, loss**.
- Walk through the **ML workflow** from collecting data to evaluating a model, and recognise the role **train/test splits** play (a concept every tester should love).
- Explain why deep learning took off after 2012 and why it is the foundation for the Generative AI you will use later this week.
- Read and run a small Python example that solves the same QE problem three ways: hand-written rules, a classic ML model, and a small neural network.
- Talk about AI accurately with developers, product owners and managers, avoiding the most common misconceptions.

---

## Why This Matters

For seven weeks you have built a solid Quality Engineering toolkit: Python and Git, test design, pytest, Playwright, Selenium with BDD, API and accessibility testing, and CI/CD pipelines. This week adds a new kind of tool to that kit: **AI**.

This week's epic is ambitious. By Friday you will design and build your **first QA agent**, with input/output contracts and validation scripts. To get there, you need a strong mental model of what AI actually *is*. Without it, two bad things tend to happen:

1. **Over-trust.** People treat AI as magic and accept whatever it produces. In QE, that means shipping tests that look plausible but check the wrong thing.
2. **Under-use.** People dismiss AI as hype and miss real productivity gains, such as drafting test ideas, summarising logs or spotting patterns in thousands of failures.

A tester who understands the basics sits in the healthy middle: able to use AI confidently *and* to question it intelligently. Quality engineers are increasingly asked two different questions:

- *"Can AI help us test faster?"* (AI **for** testing, the focus of this week)
- *"How do we test the AI features in our product?"* (testing **of** AI, which you will meet in later weeks)

Both questions start with the same foundation: knowing the difference between AI, machine learning and deep learning. That is today's first topic, and every other lesson today builds on it.

---

## The Concept

### 1. The Big Picture: Three Nested Circles

The single most useful picture to keep in your head is a set of nested circles, like Russian dolls:

```text
+---------------------------------------------------------------+
|  ARTIFICIAL INTELLIGENCE                                      |
|  Any technique that makes machines behave "intelligently"     |
|                                                               |
|   +-------------------------------------------------------+   |
|   |  MACHINE LEARNING                                     |   |
|   |  AI that LEARNS patterns from data                    |   |
|   |                                                       |   |
|   |   +-----------------------------------------------+   |   |
|   |   |  DEEP LEARNING                                |   |   |
|   |   |  ML using many-layered neural networks        |   |   |
|   |   |                                               |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   |   |  GENERATIVE AI (e.g. LLMs)            |   |   |   |
|   |   |   |  DL models that CREATE new content    |   |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   +-----------------------------------------------+   |   |
|   +-------------------------------------------------------+   |
+---------------------------------------------------------------+
```

Read it from the outside in:

- **All deep learning is machine learning**, but not all machine learning is deep learning.
- **All machine learning is AI**, but not all AI is machine learning.
- **Generative AI** (the technology behind tools like ChatGPT, Claude, Gemini and GitHub Copilot) is a modern branch that, today, is built almost entirely with deep learning. You will study it in detail later today.

A helpful analogy: think of **"vehicle" → "car" → "electric car"**. Every electric car is a car, and every car is a vehicle, but a bicycle is a vehicle that is not a car. In the same way, a hand-written chess program from the 1990s is AI, but it is not machine learning.

### 2. What Is Artificial Intelligence?

**Artificial Intelligence** is the broad field of building computer systems that perform tasks we normally associate with human intelligence: recognising images, understanding language, making decisions, planning, solving problems.

The term was coined in the mid-1950s, in the proposal for the 1956 Dartmouth summer workshop, which is often called the founding event of AI research. Notice that the definition says nothing about *how* the intelligence is achieved. That is deliberate. AI is defined by **behaviour**, not by technique.

Historically, AI has used two very different approaches.

#### 2.1 Symbolic AI (rule-based AI)

In early AI, humans wrote the intelligence directly as rules. These systems were called **expert systems**. For example, a medical expert system might contain thousands of rules like:

```text
IF patient has fever AND rash AND recent travel
THEN consider diagnosis X with confidence 0.7
```

You already write rule-based logic every day as a tester. Consider this simple function that decides whether a test failure is probably *flaky* (passes sometimes, fails sometimes without any code change):

```python
def is_probably_flaky(failure_message: str, retries_passed: int) -> bool:
    """A hand-written rule: a human expert decided what 'flaky' looks like."""
    if retries_passed > 0:
        return True
    if "TimeoutError" in failure_message:
        return True
    if "element is not attached to the DOM" in failure_message:
        return True
    return False
```

This is perfectly valid AI in the broad, historical sense: it encodes expert judgement into a machine. Its strengths are that it is **transparent** (you can read every rule), **predictable** and **easy to debug**.

Its weakness is that **someone must think of every rule**. What about a new kind of failure message nobody anticipated? What about subtle combinations, such as "fails only on Tuesdays in the Firefox job when the database is under load"? Rule lists grow, conflict and become impossible to maintain. This is the problem machine learning solves.

#### 2.2 Narrow AI vs. General AI

You will often hear two more terms:

| Term | Meaning | Exists today? |
|------|---------|---------------|
| **Narrow AI** (weak AI) | A system that is good at a specific task or family of tasks: spam filtering, image recognition, translation, writing code suggestions. | **Yes.** Every AI product you use is narrow AI, including large language models, even though they cover a wide range of language tasks. |
| **Artificial General Intelligence (AGI)** | A hypothetical system with flexible, human-level ability across essentially any intellectual task. | Debated. There is no agreed definition or test, and you should treat claims in either direction with healthy scepticism. |

For QE work, the practical point is simple: **today's AI tools are powerful but have specific, testable limits.** Your job is to find and respect those limits, which is exactly what testers are good at.

### 3. What Is Machine Learning?

**Machine Learning** is a subset of AI in which the system **learns patterns from examples (data)** instead of following rules written by a human.

A widely quoted informal description (often attributed to Arthur Samuel, an ML pioneer in the 1950s) says ML gives computers "the ability to learn without being explicitly programmed." A more precise and still widely used definition comes from Tom Mitchell (1997):

> A computer program is said to learn from experience **E** with respect to some class of tasks **T** and performance measure **P**, if its performance at tasks in **T**, as measured by **P**, improves with experience **E**.

Let us translate that into a QE example:

- **Task (T):** classify a failed test as *flaky* or *genuine defect*.
- **Experience (E):** 5,000 historical failures that engineers have already triaged and labelled.
- **Performance (P):** the percentage of new failures classified correctly.

If the classifier gets better as you give it more labelled history, it is learning. That is machine learning.

#### 3.1 Traditional programming vs. machine learning

This comparison is the heart of today's lesson:

```text
TRADITIONAL PROGRAMMING
   Rules (written by a human)  +  Data   --->  [ Program ]  --->  Answers

MACHINE LEARNING (training)
   Data  +  Answers (examples)           --->  [ Learning algorithm ]  --->  Rules (a "model")

MACHINE LEARNING (using the model, called "inference")
   New data  --->  [ Model ]  --->  Predicted answers
```

In traditional programming you supply the rules. In ML you supply **examples of inputs paired with the correct outputs**, and the algorithm **discovers the rules itself**. The learned "rules" are stored in a **model**, usually as a large collection of numbers called **parameters** (or **weights**).

#### 3.2 Core ML vocabulary

You will use these words all week. Learn them now and the rest of the day becomes much easier.

| Term | Plain-language meaning | QE example |
|------|------------------------|-----------|
| **Dataset** | The collection of examples the model learns from. | 5,000 historical test failures. |
| **Example / sample / row** | One item in the dataset. | One failed test run. |
| **Feature** | A measurable input property of an example. | Test duration, number of retries, browser, "message contains Timeout". |
| **Label** | The correct answer for an example (when known). | "flaky" or "defect". |
| **Model** | The learned function that maps features to predictions. | The trained flaky-test classifier. |
| **Parameters / weights** | The numbers inside the model that training adjusts. | Thousands (or billions) of numbers you never set by hand. |
| **Training** | The process of adjusting parameters so predictions match labels. | Running `model.fit(...)` on historical data. |
| **Inference / prediction** | Using a trained model on new, unseen data. | Classifying tonight's new failures. |
| **Loss** | A number measuring how wrong the model's predictions are. Training tries to make it small. | "We mislabelled 12% of failures." |
| **Hyperparameter** | A setting chosen by a human *before* training (not learned). | How deep a decision tree may grow. |

> **Tester's analogy:** think of a model as a function under test whose code you did not write and cannot read line by line. You can only judge it by its **behaviour on inputs**. That is black-box testing, a skill you already have.

#### 3.3 The ML workflow

Almost every ML project follows the same broad loop:

1. **Define the problem.** What exactly should the model predict, and how will we measure success? (A vague goal produces a useless model, just as a vague requirement produces useless tests.)
2. **Collect data.** Gather examples. Quality matters more than quantity: mislabelled or biased data teaches the model the wrong lesson. This is summed up in the old saying **"garbage in, garbage out."**
3. **Prepare data.** Clean it, handle missing values, convert text and categories into numbers (models only understand numbers), and choose features.
4. **Split the data.** Keep some data *hidden* from training so you can test the model honestly (see the next section).
5. **Train the model.** Let the algorithm adjust its parameters.
6. **Evaluate.** Measure performance on the held-back test data.
7. **Deploy and monitor.** Use the model in real life, and watch for its performance dropping as the world changes (called **drift**).
8. **Iterate.** Improve data, features or model and repeat.

Steps 2, 4, 6 and 7 are essentially **quality engineering for models**. ML teams need people who think like testers.

#### 3.4 Train/test split: the tester's favourite ML idea

Imagine a teacher who gives students the exact exam questions as homework, then gives the same questions in the final exam. Every student scores 100%, but nobody knows if they actually learned anything.

ML has the same trap. If you evaluate a model on the same data it trained on, it can simply **memorise** the answers. So we split the data:

- **Training set** (typically 70-80%): the model learns from this.
- **Test set** (typically 20-30%): kept locked away and used only at the end to estimate real-world performance.
- Often a **validation set** too: used during development to tune hyperparameters, so the test set stays truly unseen.

Two failure patterns follow from this:

| Problem | What it means | Analogy | Sign |
|--------|---------------|---------|------|
| **Overfitting** | The model memorises training data, including its noise, and fails on new data. | A student who memorised past papers but cannot answer a new question. | Very high training score, much lower test score. |
| **Underfitting** | The model is too simple to capture the real pattern. | A student who only learned "the answer is usually C". | Low score on both training and test data. |

You will see a train/test split in code later in this lesson, and you will see it again in the next lesson on supervised learning.

### 4. What Is Deep Learning?

**Deep Learning** is a subset of machine learning that uses **artificial neural networks with many layers** (that is what "deep" means: depth = number of layers).

You will study how neural networks work in detail later today in *Neural Network Fundamentals*. For now, you only need the big idea:

- A neural network is made of many simple units ("neurons") arranged in **layers**.
- Each layer transforms its input a little and passes it to the next layer.
- Early layers learn simple patterns; later layers combine them into complex ones. In an image model, early layers might detect edges, middle layers shapes, and later layers whole objects like "button" or "checkbox".

#### 4.1 Why deep learning is different: feature learning

In classic ML, a human usually performs **feature engineering**: deciding which measurable properties to feed the model. For our flaky-test problem, a human decided that "duration" and "retries" matter.

Deep learning can **learn useful features by itself from raw data**: raw pixels of a screenshot, raw characters of a log file, raw audio. This is a big deal for messy, unstructured data like images and language, where nobody can write down all the useful features by hand.

| | Classic machine learning | Deep learning |
|--|--------------------------|---------------|
| Typical input | Structured, tabular data (rows and columns) | Unstructured data: images, text, audio, video (also works on tabular) |
| Features | Mostly designed by humans | Mostly learned automatically |
| Data needed | Can work well with hundreds to thousands of examples | Usually needs a lot more data |
| Compute needed | A laptop CPU is often enough | Often needs GPUs or specialised hardware for training |
| Interpretability | Often easier to explain (e.g. a decision tree) | Often a "black box"; harder to explain individual decisions |
| Examples | Fraud scoring, churn prediction, flaky-test classification | Image recognition, speech recognition, translation, LLMs |

#### 4.2 Why deep learning took off when it did

Neural networks were invented decades ago, so why did they suddenly dominate in the 2010s? Three things arrived together:

1. **Data.** The internet produced huge labelled and unlabelled datasets (for example, the ImageNet image collection).
2. **Compute.** Graphics processing units (GPUs), built for video games, turned out to be excellent at the maths neural networks need.
3. **Better techniques.** Improvements in training methods made deep networks practical.

A famous turning point came in **2012**, when a deep neural network called **AlexNet** won the ImageNet image-recognition competition by a large margin. In **2017**, researchers at Google introduced the **Transformer** architecture, which is the foundation of today's large language models. Late in **2022**, ChatGPT brought Generative AI to the general public. You will learn about Transformers and LLMs later today; you do not need the details yet.

### 5. Putting It Together: One Problem, Three Approaches

Let us make the nested circles concrete with code. We will solve one QE problem, **"is this failed test flaky?"**, in three ways.

You need `scikit-learn` (a popular Python ML library) and `numpy`:

```bash
pip install scikit-learn numpy
```

#### 5.1 The data

Each row describes a failed test using four numeric features:

- `retries_passed`: how many automatic retries passed after the failure (0, 1, 2).
- `duration_spread`: how much the test's run time varies across recent runs, in seconds.
- `network_calls`: how many network requests the test makes.
- `recent_code_change`: 1 if the code under test changed in the last commit, else 0.

The label is `1` for flaky and `0` for a genuine defect. In real life this data would come from your CI history (remember the pipeline artifacts from Week 7). Here we generate a small synthetic dataset so the example runs anywhere.

```python
# flaky_data.py
import numpy as np

def make_flaky_dataset(n_rows: int = 600, seed: int = 42):
    """Create a synthetic dataset of failed tests.

    Returns X (features, shape n_rows x 4) and y (labels: 1 = flaky, 0 = defect).
    """
    rng = np.random.default_rng(seed)          # seeded so results are repeatable

    retries_passed = rng.integers(0, 3, n_rows)           # 0, 1 or 2
    duration_spread = rng.uniform(0.0, 6.0, n_rows)       # seconds
    network_calls = rng.integers(0, 15, n_rows)           # count
    recent_code_change = rng.integers(0, 2, n_rows)       # 0 or 1

    # The "true" hidden pattern the model must discover (a human would not know this exactly):
    score = (
        1.4 * retries_passed
        + 0.5 * duration_spread
        + 0.15 * network_calls
        - 2.0 * recent_code_change
    )
    noise = rng.normal(0, 0.8, n_rows)          # real data is never perfectly clean
    y = (score + noise > 2.5).astype(int)

    X = np.column_stack([retries_passed, duration_spread, network_calls, recent_code_change])
    return X, y

if __name__ == "__main__":
    X, y = make_flaky_dataset()
    print("Shape of X:", X.shape)          # (600, 4)
    print("First row:", X[0], "label:", y[0])
    print("Fraction flaky:", round(y.mean(), 2))
```

**Code walkthrough:**

- `np.random.default_rng(seed)` creates a random number generator. Fixing the `seed` makes the "random" data identical every run, which is just as important in ML experiments as it is in deterministic tests.
- `rng.integers(0, 3, n_rows)` produces `n_rows` whole numbers from 0 up to (but not including) 3.
- `score` is a hidden formula we use only to *generate* labels. A real team never knows this formula, which is exactly why they need ML to approximate it from examples.
- `np.column_stack` glues the four feature arrays into a table with 600 rows and 4 columns. By convention, ML code calls this table `X` (capital, because it is a matrix) and the labels `y` (lowercase, because it is a vector).

#### 5.2 Approach 1: Rule-based AI (a human writes the rules)

```python
# approach_rules.py
import numpy as np
from flaky_data import make_flaky_dataset

def rule_based_flaky(row) -> int:
    retries_passed, duration_spread, network_calls, recent_code_change = row
    if retries_passed >= 1 and recent_code_change == 0:
        return 1
    if duration_spread > 4.0:
        return 1
    return 0

X, y = make_flaky_dataset()
predictions = np.array([rule_based_flaky(row) for row in X])
accuracy = (predictions == y).mean()
print(f"Rule-based accuracy: {accuracy:.2%}")
```

The human guessed sensible rules. They work reasonably, but they were never tuned against the data and miss interactions the human did not think of. Notice there is no training step and no train/test split: nothing was learned.

#### 5.3 Approach 2: Classic machine learning (the algorithm learns the rules)

```python
# approach_ml.py
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from flaky_data import make_flaky_dataset

X, y = make_flaky_dataset()

# 1. Hold back 25% of the data as an honest "final exam"
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y
)

# 2. Choose a model and a hyperparameter (max_depth), then train it
model = DecisionTreeClassifier(max_depth=4, random_state=0)
model.fit(X_train, y_train)                 # <-- this is "training"

# 3. Evaluate on data the model has never seen
print(f"Training accuracy: {model.score(X_train, y_train):.2%}")
print(f"Test accuracy:     {model.score(X_test, y_test):.2%}")

# 4. Inference on a brand-new failure
new_failure = [[2, 3.1, 9, 0]]              # 2 retries passed, unstable timing, no code change
print("Prediction (1 = flaky):", model.predict(new_failure)[0])

# 5. Because this is a decision tree, we can print the rules it learned
feature_names = ["retries_passed", "duration_spread", "network_calls", "recent_code_change"]
print(export_text(model, feature_names=feature_names))
```

**Code walkthrough:**

- `train_test_split(..., test_size=0.25, stratify=y)` shuffles and splits the data. `stratify=y` keeps the same flaky/defect ratio in both halves, which matters when one class is rarer.
- `DecisionTreeClassifier(max_depth=4)` is a model that learns a flowchart of yes/no questions. `max_depth` is a **hyperparameter**: we chose it; the model did not learn it. A very deep tree can memorise the training data (overfitting).
- `model.fit(X_train, y_train)` is the training step. Every scikit-learn model uses this same `fit` / `predict` / `score` pattern, which makes it easy to swap models.
- `model.score(...)` returns accuracy: the fraction of correct predictions. Comparing training accuracy with test accuracy is your first overfitting check.
- `export_text` prints the learned rules. Compare them with the human rules in Approach 1: the algorithm *discovered* thresholds from the data instead of guessing them.

#### 5.4 Approach 3: Deep(ish) learning (a neural network learns its own representation)

```python
# approach_nn.py
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from flaky_data import make_flaky_dataset

X, y = make_flaky_dataset()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y
)

# A small neural network with two hidden layers of 16 and 8 neurons.
# StandardScaler puts all features on a similar scale, which neural networks need.
nn_model = make_pipeline(
    StandardScaler(),
    MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=2000, random_state=0),
)
nn_model.fit(X_train, y_train)

print(f"Neural network test accuracy: {nn_model.score(X_test, y_test):.2%}")
print("Prediction for new failure:", nn_model.predict([[2, 3.1, 9, 0]])[0])
```

**Code walkthrough:**

- `MLPClassifier` stands for *multi-layer perceptron*, the classic neural network. `hidden_layer_sizes=(16, 8)` means two hidden layers. Production deep-learning systems use frameworks such as PyTorch or TensorFlow and have far more layers, but the idea is the same.
- `StandardScaler` rescales each feature to have an average of 0 and a similar spread. Without it, a feature measured in large numbers can dominate one measured in small numbers.
- `make_pipeline` chains the scaler and the model, so the same scaling is applied automatically during both training and prediction (a common source of bugs when done by hand).
- Notice what is **missing**: unlike the decision tree, there is no readable list of rules. The network's knowledge lives in hundreds of numeric weights. This is the interpretability trade-off from section 4.1.

When you run all three, you will typically see the learned models beat the hand-written rules on this data. On a tiny tabular problem like this one, the neural network is **not** guaranteed to beat the decision tree; deep learning shines most on large, unstructured data such as text and images. Choosing the simplest tool that works is good engineering.

### 6. Where You Already Meet AI, ML and DL in QE

| Situation | Category | Why |
|-----------|----------|-----|
| A linter rule that flags `time.sleep()` in tests | Rule-based (classic AI in the broad sense) | Human-written rule. |
| A CI dashboard that predicts which tests are likely to fail for a given change | Machine learning | Learned from historical runs. |
| A tool that groups thousands of failure logs into similar clusters | Machine learning | Pattern discovery from data (you will see this in the next lesson). |
| Visual testing that ignores harmless anti-aliasing but flags a missing button | Often deep learning | Learned image understanding. |
| A coding assistant that suggests the next lines of a Playwright test | Deep learning (Generative AI) | A large language model, covered later today. |

### 7. Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "AI understands things the way people do." | Models learn statistical patterns in data. They can be very capable and still fail in ways a human never would. Always verify. |
| "AI and ML are the same thing." | ML is one (now dominant) way of building AI. Rule-based systems are AI too. |
| "More data always fixes the model." | More *bad* or *biased* data makes it worse. Data quality beats quantity. |
| "If the accuracy is 95%, it is good enough." | It depends on the cost of the 5%. Missing 5% of genuine defects could be unacceptable. Accuracy can also mislead on imbalanced data. |
| "Deep learning is always better." | For small, structured problems, simpler models are often as good, faster, cheaper and easier to explain. |
| "A model, once trained, stays correct." | The world changes (new features, new browsers, new user behaviour). Models **drift** and need monitoring and retraining. |

---

## Practice Exercises

1. **Classify the system.** For each of the following, decide whether it is rule-based AI, classic ML or deep learning, and justify your answer in one sentence:
   - (a) A test-selection tool that runs only tests whose file paths match the changed files.
   - (b) A model trained on 2 years of CI history that predicts the probability a pull request will break the build.
   - (c) A visual-comparison tool that recognises a "Submit" button in a screenshot regardless of its colour or position.
2. **Spot the overfitting.** A teammate reports: *"Training accuracy 99.8%, test accuracy 71%."* Explain what is probably happening and suggest two things to try.
3. **Run and modify the code.** Run `approach_ml.py`. Then change `max_depth` to `1`, then to `20`. Record training and test accuracy each time. Which setting underfits? Which overfits? Explain using the student analogy from section 3.4.
4. **Feature thinking.** List five features (other than those used above) you could extract from your Project 2 test runs that might help predict flakiness. For each, say how you would obtain it (for example, from pytest output, Playwright traces or CI logs).

---

## Knowledge Check

1. Draw (or describe) the nested relationship between AI, ML, DL and Generative AI.
2. In your own words, what is the key difference between traditional programming and machine learning?
3. What is the difference between a *parameter* and a *hyperparameter*?
4. Why must the test set be kept separate from the training set?
5. Give two reasons deep learning became practical in the 2010s.

<details>
<summary>Suggested answers</summary>

1. Generative AI sits inside Deep Learning, which sits inside Machine Learning, which sits inside AI.
2. In traditional programming a human writes the rules; in ML the algorithm learns the rules (the model) from examples of inputs and correct outputs.
3. Parameters are learned by the model during training (e.g. neural network weights); hyperparameters are chosen by a human before training (e.g. `max_depth`).
4. To get an honest estimate of performance on unseen data; evaluating on training data hides overfitting.
5. Large datasets, GPU computing power and improved training techniques (any two).

</details>

---

## Glossary

- **Artificial Intelligence (AI):** The broad field of making machines perform tasks associated with human intelligence.
- **Machine Learning (ML):** A subset of AI where systems learn patterns from data instead of following hand-written rules.
- **Deep Learning (DL):** A subset of ML using neural networks with many layers.
- **Model:** The learned function that maps inputs (features) to outputs (predictions).
- **Feature:** A measurable input property used by a model.
- **Label:** The known correct answer for a training example.
- **Training:** Adjusting a model's parameters to fit example data.
- **Inference:** Using a trained model to make predictions on new data.
- **Overfitting / Underfitting:** Learning the training data too closely / too loosely to generalise.
- **Drift:** Gradual loss of model accuracy as real-world data changes over time.

---

## Summary

- **AI ⊃ ML ⊃ DL ⊃ Generative AI.** Each is a subset of the one before it.
- **AI** is defined by intelligent behaviour, not technique; rule-based systems count as AI.
- **ML** learns rules from **data and answers** instead of being given rules by a human. Its key ideas are features, labels, training, inference and evaluation.
- **Always evaluate on unseen data.** The train/test split protects you from being fooled by overfitting, the ML equivalent of a test that can never fail.
- **Deep learning** uses many-layered neural networks that learn features automatically, which makes it powerful for unstructured data like text and images, at the cost of more data, more compute and less interpretability.
- Testers bring exactly the mindset ML needs: questioning data quality, checking behaviour on unseen inputs and watching for drift.

---

## Additional Resources

- IBM, *AI vs. machine learning vs. deep learning vs. neural networks: What's the difference?*: https://www.ibm.com/think/topics/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks
- Google for Developers, *Machine Learning Crash Course* (free, interactive, beginner-friendly): https://developers.google.com/machine-learning/crash-course
- scikit-learn, *User Guide* (the library used in this lesson's code): https://scikit-learn.org/stable/user_guide.html
