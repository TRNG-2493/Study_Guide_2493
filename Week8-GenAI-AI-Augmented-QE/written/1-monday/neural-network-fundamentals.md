# Neural Network Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- **Calculate** the output of a single artificial neuron by hand from its inputs, weights, bias and activation function.
- **Explain** what weights, a bias and an activation function each do, and why networks need non-linear activations.
- **Count** the parameters (weights and biases) in a small network, and explain what "billions of parameters" means.
- **Describe** how a network learns: compare its output with a label, measure the error, nudge the weights, repeat.
- **Check** an AI assistant's neuron arithmetic against your own, and explain why a tester should check numbers from an AI.

---

## Why This Matters

In *Artificial Intelligence, Machine Learning and Deep Learning*, you learned that deep learning uses "neural networks with many layers". This lesson opens that box.

You do not need to build neural networks to be a good quality engineer. But you will test systems that contain them, and use tools built on them every day this week. ChatGPT, Copilot and Claude are all neural networks. Knowing what is inside explains several things you will see:

- **Why you cannot read the rules.** A network's knowledge is spread across a huge number of numbers called **weights**. GPT-3, an earlier OpenAI language model, had **175 billion** of them ([Brown et al., 2020](https://arxiv.org/abs/2005.14165)). Nobody can read 175 billion numbers, so you test the behaviour instead.
- **Why training data matters so much.** A network only learns from the examples it was given. Gaps in the examples become gaps in its behaviour.
- **Why "it learned" does not mean "it is right".** Learning means getting closer to the labels it was trained on. If those labels or examples are poor, the network learns the wrong lesson very efficiently.

By the end of this lesson you will have worked one neuron by hand, fixed it with one "learning" step, and watched a few lines of Python do the same.

> **Using this with the handout:** this lesson goes deeper into **Handout 01, Topic 3**. It uses the same neuron (weights 2.0, 0.5 and 1.5; bias −3.0), the same failures A, B and C, and the same `neuron.py`.

---

## The Concept

### 1. The Inspiration: Biological Neurons (Loosely)

Your brain contains billions of nerve cells called **neurons**. Each one receives signals from other neurons, and if the combined signal is strong enough, it "fires" and sends a signal on.

Artificial neural networks borrow this idea **very loosely**. An artificial neuron is not a model of a brain cell; it is a small piece of arithmetic. The comparison is useful for one thing only: **many simple units, connected together, can do something none of them could do alone.**

### 2. The Artificial Neuron

An **artificial neuron** does three things:

1. **Multiplies** each input by a **weight**.
2. **Adds** the results together, plus a **bias**. The total is usually called **z**.
3. Passes z through an **activation function**, which decides the output.

```text
input 1 ──(× weight 1)──┐
input 2 ──(× weight 2)──┼──► sum + bias = z ──► activation ──► output
input 3 ──(× weight 3)──┘
```

What each part means:

- **Weights** say how much each input matters. A big weight means "this input counts a lot". A negative weight means "this input pushes the answer the other way".
- **Bias** is a starting nudge. A large negative bias makes the neuron harder to "switch on"; a positive bias makes it easier.
- **Activation function** turns z into the neuron's output. The simplest is a **step**: output 1 if z is above 0, otherwise 0.

**An everyday analogy: a weighted vote.** Imagine a release manager deciding whether to stop a release. Three people report in: the test lead, a developer and a product owner. The manager trusts the test lead most (a big weight), the developer a little less, and the product owner's view on this matter least. The manager is also cautious by default and needs a strong case before stopping anything; that caution is the bias. Add up the weighted opinions, subtract the caution, and if the total is positive, stop the release.

#### 2.1 Worked example: does this failure need attention now?

Here is the neuron from the handout. It decides whether a test failure needs **attention right now** (1) or **can wait** (0). Each failure has three inputs:

- `is_smoke_test`: 1 if it is a critical smoke test, 0 if not
- `times_failed_this_week`: how many times it failed this week
- `failed_in_production_env`: 1 if it failed in the production-like environment, 0 if not

The weights are **2.0** (smoke test), **0.5** (each failure this week) and **1.5** (production-like environment). The bias is **−3.0**.

The QA lead has already labelled the right answer for each failure, using the team's rule: *"A failing smoke test always needs attention now. A normal test that failed once in dev can wait."*

Now work each failure through the neuron:

| Failure | Inputs | Weighted sum | + bias | z | Step output | Label | Match? |
|---|---|---|---|---|---|---|---|
| A: smoke test, failed 3×, production-like env | [1, 3, 1] | 2.0 + 1.5 + 1.5 = 5.0 | −3.0 | **+2.0** | 1 | 1 | ✅ |
| B: normal test, failed once, dev | [0, 1, 0] | 0 + 0.5 + 0 = 0.5 | −3.0 | **−2.5** | 0 | 0 | ✅ |
| C: smoke test, failed once, dev | [1, 1, 0] | 2.0 + 0.5 + 0 = 2.5 | −3.0 | **−0.5** | 0 | 1 | ❌ |

Follow failure A slowly once: the smoke-test input is 1, times 2.0, gives 2.0. Three failures times 0.5 gives 1.5. The production-like input is 1, times 1.5, gives 1.5. The sum is 5.0. Add the bias (−3.0) and z = +2.0. That is above 0, so the step outputs 1.

Failure **C** is the interesting one. It is a smoke test, so the label says it needs attention. But it failed only once, in dev, so its weighted sum (2.5) does not beat the bias (−3.0). The neuron's output does not match the label: **the neuron is wrong about C**. Finding and fixing mismatches like this is exactly what training does, as you will see in section 5.

#### 2.2 The same neuron in Python

The handout's `neuron.py` does the same arithmetic. It needs no installs:

```python
def neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias   # weighted sum + bias
    return z, (1 if z > 0 else 0)                              # step activation

weights, bias = [2.0, 0.5, 1.5], -3.0
for failure in ([1, 3, 1], [0, 1, 0], [1, 1, 0]):
    z, output = neuron(failure, weights, bias)
    print(f"{failure} -> z = {z:+.1f} -> output {output}")
```

Run it with `python neuron.py`. Output:

```text
[1, 3, 1] -> z = +2.0 -> output 1
[0, 1, 0] -> z = -2.5 -> output 0
[1, 1, 0] -> z = -0.5 -> output 0
```

What to notice:

- `zip(inputs, weights)` pairs each input with its weight: (1, 2.0), (3, 0.5), (1, 1.5).
- `sum(x * w for ...)` multiplies each pair and adds the results: the weighted sum.
- `1 if z > 0 else 0` is the step activation.
- `{z:+.1f}` prints z with a sign and one decimal place, so the output lines up with your table.

The code and your hand calculation agree. That is the point: **the code is a check on your understanding, and your understanding is a check on the code.**

### 3. Activation Functions: Why Non-Linearity Matters

The step function is easy to work by hand, but real networks use smoother activation functions. Three you will hear about:

| Activation | Rule | Output range | Example values |
|---|---|---|---|
| **Step** | 1 if z > 0, else 0 | 0 or 1 | z = 2.0 → 1; z = −0.5 → 0 |
| **Sigmoid** | Squashes any z into a value between 0 and 1 | 0 to 1 | z = 2.0 → 0.88; z = 0 → 0.50; z = −2.5 → 0.08 |
| **ReLU** (rectified linear unit) | 0 if z is negative, otherwise z itself | 0 and above | z = 2.0 → 2.0; z = −0.5 → 0 |

**Sigmoid** is useful when you want something like a probability: z = 2.0 becomes 0.88, which you can read as "88% sure this needs attention". **ReLU** is the most common choice inside modern deep networks, because it is cheap to compute and trains well.

#### 3.1 Why we need non-linear activations at all

An activation that is **non-linear** is one whose graph is not a straight line. Why does that matter? Without it, stacking layers achieves nothing. If every neuron just added weighted inputs, a stack of ten layers would collapse into a single weighted sum, no more powerful than one neuron.

Here is a classic problem a single neuron **cannot** solve. A test should be flagged when **exactly one** of two conditions holds:

| Ran on Chrome? | Ran on Firefox? | Flag? |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 0 |

This pattern is called **XOR** ("exclusive or"). Try to find weights and a bias for one step neuron that gives all four answers. You cannot: to make rows 2 and 3 output 1, both weights must be large enough to beat the bias; but then row 4, with both inputs at 1, beats it by even more and outputs 1 too.

A network with a **hidden layer** of non-linear neurons solves XOR easily. One hidden neuron can learn "at least one is true", another "both are true", and the output neuron combines them as "the first, but not the second".

Here is one set of numbers that works. Both hidden neurons use ReLU (negative values become 0):

- **Hidden neuron h1** = ReLU(Chrome + Firefox): it counts how many are true.
- **Hidden neuron h2** = ReLU(Chrome + Firefox − 1): it is above 0 only when **both** are true.
- **Output** = step(h1 − 2 × h2): 1 if the result is above 0.

Work it through:

| Chrome | Firefox | h1 | h2 | h1 − 2 × h2 | Output | Correct? |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | ✅ |
| 1 | 0 | 1 | 0 | 1 | 1 | ✅ |
| 0 | 1 | 1 | 0 | 1 | 1 | ✅ |
| 1 | 1 | 2 | 1 | 0 | 0 | ✅ |

The hidden layer created two **new features** that were not in the input: "how many" and "both". The output neuron then solved an easy problem using them. This is what layers do in every deep network, at a much larger scale: each layer builds more useful features out of the previous layer's outputs. In a real network, training finds these weights; nobody types them in.

#### 3.2 Softmax: turning scores into probabilities

One more activation is worth knowing by name, because you will meet it again later today in *Generative AI Concepts*. **Softmax** takes a list of scores, one per possible answer, and turns them into probabilities that add up to 1.

Suppose a bug-routing network gives these raw scores for three teams: **Checkout 2.0, Search 1.0, Login 0.1**. Softmax works in two steps:

1. Raise *e* (about 2.718) to the power of each score: 7.39, 2.72 and 1.11. These always come out positive.
2. Divide each by their total (11.21): **0.66, 0.24 and 0.10**.

So the network is about 66% sure the bug belongs to Checkout. The highest score always gets the highest probability, but the others keep a share. Language models use the same step to decide how likely each possible next word is.

### 4. Layers: Organising Neurons into a Network

A **neural network** connects many neurons in **layers**:

- The **input layer** holds the input values: for us, the three numbers describing a failure.
- One or more **hidden layers** of neurons each take the previous layer's outputs as their inputs.
- The **output layer** produces the final answer.

```text
 inputs          hidden layer        output
 is_smoke ───┬──► neuron 1 ───┐
 failures ───┼──► neuron 2 ───┼──► neuron ──► needs attention?
 prod_env ───┼──► neuron 3 ───┤
             └──► neuron 4 ───┘
```

Every input connects to every hidden neuron, and every hidden neuron connects to the output. Passing the inputs through the layers, one after another, to get an answer is called the **forward pass**. "Deep" learning simply means a network with **many** hidden layers.

#### 4.1 Counting parameters by hand

The weights and biases are together called the network's **parameters**. They are the numbers training adjusts. Counting them is simple:

- **Hidden layer:** each of the 4 hidden neurons has 3 weights (one per input) and 1 bias: 4 × (3 + 1) = **16**.
- **Output layer:** the output neuron has 4 weights (one per hidden neuron) and 1 bias: 1 × (4 + 1) = **5**.
- **Total:** 16 + 5 = **21 parameters**.

Our single neuron from section 2 had 4 parameters. This small network has 21. Make the layers wider and add more of them, and the number grows very fast. That is how you get to GPT-3's 175 billion. Every one of those numbers was set by training, not by a person, which is why no one can point to "the rule" a large model followed.

### 5. How Neural Networks Learn

A network starts with weights that are usually small random numbers, so its first answers are poor. **Training** improves them using labelled examples. At heart, the loop is the one you already know from testing: **run, compare with the expected result, fix, run again.**

1. **Forward pass:** run an example through the network and get an output.
2. **Compare:** measure how wrong the output is against the label. That measure is called the **loss**. A loss of 0 means perfect.
3. **Adjust:** nudge each weight and bias a little, in the direction that makes the loss smaller.
4. **Repeat** for every example, many times over.

#### 5.1 One learning step, by hand

Go back to failure C, the one the neuron got wrong. The neuron said 0; the label says 1. Its z was −0.5, just below the line. Two simple nudges fix it:

- Change the **bias** from −3.0 to **−1.5**. C becomes 2.5 − 1.5 = **+1.0** → 1 ✅.
- Or change the **smoke-test weight** from 2.0 to **3.5**. C becomes 3.5 + 0.5 − 3.0 = **+1.0** → 1 ✅.

A fix is only good if it does not break anything else. With the bias at −1.5, recheck the others: A is 5.0 − 1.5 = +3.5 → 1 ✅, and B is 0.5 − 1.5 = −1.0 → 0 ✅. All three now match.

That is training in miniature: **see an error, adjust a weight or the bias, recheck the other examples.** A real network does this automatically, millions of times, over millions or billions of parameters.

#### 5.2 Letting the computer do the nudging

The script below uses one of the oldest learning rules, the **perceptron rule**. After each example, if the output was wrong, it moves every weight a little towards the right answer. The size of each nudge is set by the **learning rate**.

```python
# learn_neuron.py
def neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias
    return 1 if z > 0 else 0

examples = [([1, 3, 1], 1), ([0, 1, 0], 0), ([1, 1, 0], 1)]   # failures A, B, C with labels
weights, bias, learning_rate = [2.0, 0.5, 1.5], -3.0, 0.5

for rnd in range(1, 4):
    mistakes = 0
    for inputs, label in examples:
        error = label - neuron(inputs, weights, bias)     # +1, 0 or -1
        if error != 0:
            mistakes += 1
            weights = [w + learning_rate * error * x for w, x in zip(weights, inputs)]
            bias = bias + learning_rate * error
    print(f"Round {rnd}: {mistakes} mistake(s), weights {weights}, bias {bias}")

print("New failure E [0, 2, 1] ->", neuron([0, 2, 1], weights, bias))
```

Output:

```text
Round 1: 1 mistake(s), weights [2.5, 1.0, 1.5], bias -2.5
Round 2: 0 mistake(s), weights [2.5, 1.0, 1.5], bias -2.5
Round 3: 0 mistake(s), weights [2.5, 1.0, 1.5], bias -2.5
New failure E [0, 2, 1] -> 1
```

What to notice:

- `error = label - neuron(...)` is +1 when the neuron said 0 but should have said 1, −1 for the opposite mistake, and 0 when it was right.
- When there is an error, each weight moves by `learning_rate * error * x`. Inputs that were 0 do not change their weight, because they did not contribute to the mistake.
- In round 1 the only mistake is C. Its inputs were [1, 1, 0], so the first two weights rise by 0.5, the third stays, and the bias rises by 0.5. From round 2 on, there are no mistakes: training has **converged**.
- Each pass through all the examples is often called an **epoch**. Here, one epoch was enough.

Now look at the last line. **E** is a failure the neuron never trained on: a normal test that failed twice in the production-like environment. Before training, its z was 0 + 1.0 + 1.5 − 3.0 = −0.5, so it would wait. After training, z is 0 + 2.0 + 1.5 − 2.5 = +1.0, so it **needs attention now**. Fixing C changed the answer for E.

Is that right? Nobody has labelled E, so nobody knows. This is a real effect in every trained model: **fixing one behaviour changes others you did not test.** That is why testers re-run a full set of examples after any change to a model, the same way you run a regression suite after a code change.

#### 5.3 How real networks learn: gradient descent and backpropagation

The perceptron rule works for one step neuron. Real networks use smooth activations and a smarter version of the same idea, called **gradient descent**.

**An analogy: walking downhill in the fog.** You are on a hillside in thick fog, and you want to reach the bottom of the valley, where the loss is lowest. You cannot see the valley, but you can feel the slope under your feet. So you take a step in the steepest downhill direction, feel the slope again, and repeat. The **gradient** is that slope: for each weight, it says which way and how strongly changing it would reduce the loss.

The **learning rate** is your step size:

- **Too small**, and you take forever to reach the bottom.
- **Too large**, and you overshoot, jumping from one side of the valley to the other and never settling.

In a network with many layers, how does each weight know its share of the blame for a wrong answer? **Backpropagation** works it out. It starts at the output error and works backwards, layer by layer, calculating how much each weight contributed. You do not need the maths this week; just remember the idea: **backpropagation shares out the blame, and gradient descent uses it to adjust every weight.**

### 6. Families of Neural Networks

Different kinds of data suit different network designs. You will hear these names:

| Family | Good at | QE example |
|---|---|---|
| **Feedforward network** | Tables of numbers, like our example | Predicting which failures need attention |
| **Convolutional neural network (CNN)** | Images: it looks for local patterns such as edges and shapes | Visual testing: spotting a missing button in a screenshot |
| **Recurrent neural network (RNN)** | Sequences, read one step at a time | Older text and speech systems |
| **Transformer** | Long sequences of text and code, read all at once | The design inside today's large language models, covered later today in *Generative AI Concepts* |

### 7. What This Means for You as a Quality Engineer

Neural networks bring a few challenges that testers are well placed to catch:

- **They need lots of good data.** A network learns only from the examples it saw. Coverage of the training data matters as much as coverage of a test suite.
- **They can overfit.** With enough parameters, a network can memorise its training examples and fail on new ones, as you saw in *Artificial Intelligence, Machine Learning and Deep Learning*.
- **They are black boxes.** You cannot read the rule behind a decision, so you judge them by behaviour on well-chosen inputs: black-box testing.
- **Changes ripple.** As failure E showed, retraining to fix one case can change others.

**A coverage gap (illustrative scenario).** Imagine a team trains a CNN to flag broken page layouts in screenshots. Every training screenshot uses the app's light theme. When the dark theme ships, the network flags almost every dark-theme page as "broken", because dark pages look nothing like anything it learned as "normal". The network is not faulty; its training data never covered dark pages. A tester who asks "what did the training data include?" finds this before release.

---

## Practice Exercises

1. **Work a new failure by hand (paper, 10 min).** Using the original neuron (weights 2.0, 0.5, 1.5; bias −3.0), calculate z and the step output for:
   - (a) a smoke test that failed 2 times in the production-like environment: [1, 2, 1]
   - (b) a normal test that failed 6 times in dev: [0, 6, 0]

   Then recalculate both with the trained values from section 5.2 (weights 2.5, 1.0, 1.5; bias −2.5). Did training change either answer? Do you, as a tester, agree with the new answers?

2. **Count the parameters (paper, 5 min).** A network has 5 inputs, a hidden layer of 8 neurons, a second hidden layer of 4 neurons and 2 outputs. How many parameters does it have? Show the count for each layer.

   *Hint:* for each layer, (number of neurons) × (inputs per neuron + 1).

3. **Check the AI's arithmetic (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** ask your AI assistant: *"A neuron has weights [1.5, -0.75, 2.0] and bias -1.25, with a step activation (1 if z > 0, else 0). For each input, show the weighted sum, z and the output: [2, 4, 1], [0, 2, 1], [1, 0, 0]."*
   - **Review:** write down its z values and outputs.
   - **Run:** change the weights, bias and inputs in `neuron.py` and run it.
   - **Record:** did the AI's numbers match? If not, which step did it get wrong? Negative weights and decimals are where slips usually happen.

4. **See non-linearity (browser, 15 min).** Open the TensorFlow Playground (link in Additional Resources) and pick the **exclusive or** dataset (the one with four coloured squares). Set **0 hidden layers** and press play: what happens? Now add one hidden layer with **2 neurons**, set the activation to **ReLU**, and play again. Explain the difference using section 3.1.

---

## Knowledge Check

1. What three steps does a single artificial neuron perform?

<details><summary>Answer</summary>

It multiplies each input by its weight, adds them up with a bias to get z, and passes z through an activation function to get the output.

</details>

2. A neuron has weights [2.0, 0.5, 1.5] and bias −3.0. What is z for inputs [1, 1, 0], and what does a step activation output?

<details><summary>Answer</summary>

2.0 + 0.5 + 0 = 2.5, plus −3.0 gives z = −0.5. That is not above 0, so the step outputs 0.

</details>

3. Why does a network need non-linear activation functions?

<details><summary>Answer</summary>

Without them, stacked layers collapse into a single weighted sum, no more powerful than one neuron. Non-linear activations let layers combine features to solve problems like XOR.

</details>

4. How many parameters does a network with 3 inputs, one hidden layer of 4 neurons and 1 output have?

<details><summary>Answer</summary>

Hidden layer: 4 × (3 + 1) = 16. Output: 1 × (4 + 1) = 5. Total: 21.

</details>

5. What is the learning rate, and what goes wrong if it is too large?

<details><summary>Answer</summary>

The size of each adjustment step during training. Too large, and training overshoots the best weights and may never settle; too small, and it is very slow.

</details>

6. Retraining fixed one wrong output, and a different, unlabelled case changed its answer. What should a tester do?

<details><summary>Answer</summary>

Treat it like a regression risk: re-run a full set of labelled examples, review the changed answers, and get a label for the changed case before trusting it.

</details>

---

## Glossary

- **Artificial neuron:** a unit that multiplies inputs by weights, adds a bias and applies an activation function.
- **Weight:** a number saying how much an input matters to a neuron.
- **Bias:** a number added to the weighted sum; it makes a neuron easier or harder to switch on.
- **z:** the weighted sum plus the bias, before the activation.
- **Activation function:** the rule that turns z into a neuron's output.
- **Step / sigmoid / ReLU:** activations that output 0 or 1 / a value between 0 and 1 / 0 for negative z, otherwise z.
- **Non-linear:** not a straight-line relationship; needed for layers to add power.
- **XOR:** "exactly one of two is true"; a pattern one neuron cannot learn.
- **Softmax:** turns a list of scores into probabilities that add up to 1.
- **Neural network:** neurons connected in layers.
- **Input / hidden / output layer:** the input values / the layers in between / the layer that gives the answer.
- **Forward pass:** running inputs through the layers to get an output.
- **Parameters:** all the weights and biases in a network.
- **Training:** adjusting parameters so outputs match the labels.
- **Loss:** a number measuring how wrong the outputs are.
- **Learning rate:** the size of each adjustment step.
- **Perceptron rule:** a simple learning rule that nudges weights after each mistake.
- **Epoch:** one pass through all the training examples.
- **Converged:** training has stopped improving because there are no more errors to fix.
- **Gradient descent:** adjusting weights in the direction that reduces the loss fastest.
- **Backpropagation:** working backwards from the output error to find each weight's share of the blame.
- **CNN / RNN / Transformer:** network designs for images / sequences / long text and code.

---

## Summary

- **A neuron is simple arithmetic:** inputs × weights, plus a bias, through an activation. You can work one by hand.
- **Weights set importance and the bias sets the threshold.** Non-linear activations, such as ReLU, are what make extra layers worth having.
- **Networks stack neurons in layers**, and their parameters add up fast: 4 for one neuron, 21 for a tiny network, 175 billion for GPT-3.
- **Learning means: compare with the label, measure the error, nudge the weights, repeat.** Gradient descent does the nudging and backpropagation shares out the blame.
- **Fixing one case can change others.** Re-check a full set of examples after any change, exactly like a regression suite.
- **Networks are black boxes trained on data**, so test their behaviour, and ask what their training data covered.

---

## Additional Resources

- TensorFlow Playground (tinker with a real neural network in your browser): https://playground.tensorflow.org/
- Google for Developers, *Machine Learning Crash Course: Neural networks* (nodes, hidden layers, activation functions and backpropagation): https://developers.google.com/machine-learning/crash-course/neural-networks
- Brown et al., *Language Models are Few-Shot Learners* (the GPT-3 paper; read the abstract for the 175-billion-parameter figure): https://arxiv.org/abs/2005.14165
