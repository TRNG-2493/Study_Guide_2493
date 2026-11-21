# Neural Network Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **artificial neuron** is and compute its output by hand from **inputs, weights and a bias**.
- Describe the role of **activation functions** (step, sigmoid, ReLU, softmax) and explain why networks need **non-linearity**.
- Describe how neurons are organised into **input, hidden and output layers**, and trace a **forward pass** through a small network.
- Explain, at an intuitive level, how networks **learn**: **loss functions, gradient descent, learning rate, backpropagation, epochs and batches**.
- Implement a tiny neural network **from scratch in Python with NumPy** and watch it learn a problem a single neuron cannot solve.
- Recognise the main network families (**feed-forward, convolutional, recurrent, Transformer**) and what each is good at.
- Explain why neural networks behave as they do from a tester's point of view: probabilistic outputs, confidence that is not correctness, and sensitivity to data.

---

## Why This Matters

Earlier today you learned that **deep learning** is machine learning with many-layered neural networks, and that it powers modern AI, including the Generative AI tools you will use all week. Large language models such as the ones behind ChatGPT, Claude, Gemini and GitHub Copilot are, at their core, **very large neural networks**.

You do not need to become a data scientist to work well with these tools. But you do need an accurate mental model of what is happening inside, because it explains behaviour you will see as a quality engineer:

- Why the same question can produce **different answers**.
- Why an AI can sound **completely confident and still be wrong**.
- Why a model trained on one kind of data struggles with **unfamiliar inputs**.
- Why "it worked on my three examples" is **not** evidence that it works in general.

This lesson demystifies neural networks by building one from scratch, line by line, using the Python skills you developed in Weeks 1 and 2.

---

## The Concept

### 1. The Inspiration: Biological Neurons (Loosely)

Your brain contains billions of nerve cells called **neurons**. Very roughly, a neuron receives signals from other neurons, and if the combined signal is strong enough, it "fires" and sends a signal onward. Connections that are used together tend to strengthen, which is part of how we learn.

Artificial neural networks borrow this **idea** (many simple units, connected, with adjustable connection strengths) but they are **mathematical functions**, not models of real brains. The analogy is useful for intuition; do not take it further than that.

### 2. The Artificial Neuron

An artificial neuron (also called a **node** or **unit**) does three simple things:

1. Takes several **inputs** (numbers): x₁, x₂, x₃, …
2. Multiplies each input by a **weight** (w₁, w₂, w₃, …), adds them up, and adds a **bias** (b).
3. Passes that total through an **activation function** to produce its **output**.

```text
   x1 ---- w1 ----\
                   \
   x2 ---- w2 ------ ( Σ  +  b ) ---> activation f( ) ---> output
                   /
   x3 ---- w3 ----/

   z      = w1*x1 + w2*x2 + w3*x3 + b        (weighted sum)
   output = f(z)                              (activation)
```

- **Weights** say how *important* each input is. A large positive weight means "this input pushes the output up strongly"; a negative weight pushes it down; near zero means "mostly ignore this input".
- The **bias** shifts the threshold, making the neuron easier or harder to activate regardless of inputs. Think of it as the neuron's baseline mood.
- **Weights and biases are the parameters** that training adjusts. This is exactly the "parameters" idea from the first lesson today.

#### 2.1 A worked example by hand

Imagine a neuron that decides whether a test failure deserves **immediate attention**. Inputs:

- x₁ = test is in the **smoke suite** (1 = yes, 0 = no)
- x₂ = **number of consecutive failures** (e.g. 3)
- x₃ = failure seen in **production-like environment** (1 = yes)

Suppose the weights are w₁ = 2.0, w₂ = 0.5, w₃ = 1.5 and the bias b = -3.0.

For a smoke test (x₁ = 1) that failed 3 times (x₂ = 3) in staging (x₃ = 1):

```text
z = (2.0 * 1) + (0.5 * 3) + (1.5 * 1) + (-3.0)
  = 2.0 + 1.5 + 1.5 - 3.0
  = 2.0
```

With a simple **step** activation ("output 1 if z > 0, else 0"), the output is **1: needs attention**.

For a non-smoke test that failed once in a dev environment: z = 0 + 0.5 + 0 - 3.0 = -2.5, output **0**.

Here we chose the weights by hand. The whole point of a neural network is that **training finds good weights automatically** from examples.

#### 2.2 The same neuron in Python

```python
# single_neuron.py
def step(z: float) -> int:
    return 1 if z > 0 else 0

def neuron(inputs, weights, bias, activation=step):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias
    return activation(z)

weights = [2.0, 0.5, 1.5]
bias = -3.0

print(neuron([1, 3, 1], weights, bias))   # 1 -> needs attention
print(neuron([0, 1, 0], weights, bias))   # 0 -> can wait
```

`zip(inputs, weights)` pairs each input with its weight; the generator expression multiplies each pair, and `sum` adds them. This single neuron is called a **perceptron**, one of the earliest neural network ideas (from the late 1950s).

### 3. Activation Functions: Why Non-Linearity Matters

The **activation function** decides how a neuron turns its weighted sum `z` into an output. Common choices:

| Function | Formula (informal) | Output range | Typical use |
|----------|--------------------|--------------|-------------|
| **Step** | 1 if z > 0, else 0 | 0 or 1 | Historical perceptron; not used for training modern networks because it has no useful slope. |
| **Sigmoid** | 1 / (1 + e^(-z)) | 0 to 1 | Output layer for yes/no probability. You met it in the previous lesson. |
| **Tanh** | (e^z - e^(-z)) / (e^z + e^(-z)) | -1 to 1 | Older hidden layers; recurrent networks. |
| **ReLU** (Rectified Linear Unit) | max(0, z) | 0 to ∞ | The default for hidden layers in most modern networks: simple and fast. |
| **Softmax** | Turns a list of scores into probabilities that add up to 1 | 0 to 1 each, sum = 1 | Output layer for multi-class problems ("Critical / Major / Minor"). Also used by LLMs to choose the next word, as you will see later today. |

```python
# activations.py
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)

def softmax(scores):
    exps = np.exp(scores - np.max(scores))   # subtract max for numerical stability
    return exps / exps.sum()

z = np.array([-2.0, 0.0, 3.0])
print("sigmoid:", sigmoid(z).round(3))       # [0.119 0.5   0.953]
print("relu:   ", relu(z))                   # [0. 0. 3.]
print("softmax:", softmax(z).round(3))       # [0.006 0.047 0.946]  -> sums to 1
```

#### 3.1 Why do we need non-linear activations at all?

If every neuron just output its weighted sum (a straight-line, **linear** function), then stacking layers would be pointless: a linear function of a linear function is still a linear function. A hundred-layer network would be no more powerful than a single layer.

**Non-linear** activations like ReLU and sigmoid "bend" the output. Stacking many bends lets the network represent very complicated shapes and decision boundaries. That is the source of a neural network's power.

The classic demonstration is the **XOR** problem ("exclusive OR": output 1 when exactly one input is 1):

| Input A | Input B | XOR |
|---------|---------|-----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

A QE version: *"Raise an alert when exactly one of the two redundant health checks fails."* (Both failing is a known maintenance window; neither failing is normal.)

If you plot the four points, **no single straight line** can separate the 1s from the 0s. A single neuron draws one straight line, so it **cannot** learn XOR. A network with one hidden layer can. You will prove this in code in section 6.

### 4. Layers: Organising Neurons into a Network

A neural network arranges neurons in **layers**:

```text
 INPUT LAYER          HIDDEN LAYER(S)           OUTPUT LAYER
 (features)           (learned features)        (prediction)

   x1  o ---------\    o  -----\
                   >---o        >----  o  -->  P(flaky)
   x2  o ---------/    o  -----/
                       o
   x3  o -------------/

 Every arrow has its own weight. Every hidden/output neuron has its own bias.
```

- **Input layer:** not really neurons; it just holds the feature values (e.g. retries, duration, network calls).
- **Hidden layers:** the layers in between. They are called *hidden* because you never see their values directly in the data; the network invents them. Each hidden neuron learns to detect some useful combination of inputs.
- **Output layer:** produces the final answer. One sigmoid neuron for a yes/no probability; several softmax neurons for multi-class; a plain linear neuron for regression.

When every neuron in one layer connects to every neuron in the next, the layer is called **fully connected** or **dense**. A network made of dense layers is a **multi-layer perceptron (MLP)**: the same `MLPClassifier` you used in the first lesson today.

**"Deep"** simply means many hidden layers. There is no strict cut-off, but modern deep networks can have dozens to hundreds of layers.

#### 4.1 A quick primer: vectors, matrices and shapes

Neural network code is written with **vectors** and **matrices** rather than loops over individual neurons. If you have not met them before, this is all you need for this lesson.

- A **scalar** is a single number: `3.5`.
- A **vector** is an ordered list of numbers: `[2.0, 3.5, 9.0]`. One example's features form a vector.
- A **matrix** is a table of numbers with rows and columns. A whole dataset is a matrix (one row per example, one column per feature), and so is a layer's set of weights.
- The **shape** of an array describes its size: a vector of 3 numbers has shape `(3,)`; a matrix with 2 rows and 3 columns has shape `(2, 3)`. Shapes are written **(rows, columns)**.

In NumPy, every array has a `.shape` attribute, and checking shapes is the single most useful debugging habit in ML code. A huge share of beginner errors are "shape mismatch" errors.

**The dot product.** Multiply two equal-length vectors position by position, then add up the results:

```text
[1, 2, 3] · [10, 20, 30]  =  1*10 + 2*20 + 3*30  =  10 + 40 + 90  =  140
```

Look closely: that is exactly a neuron's **weighted sum** from section 2 (inputs times weights, added up), just without the bias.

**Matrix multiplication** (written `@` in Python) is many dot products at once. Each **row** of the left matrix is dotted with each **column** of the right matrix:

```python
# shapes_primer.py
import numpy as np

v = np.array([10, 20, 30])          # a vector
A = np.array([[1, 2, 3],
              [4, 5, 6]])            # a matrix with 2 rows and 3 columns

print("v.shape:", v.shape)          # (3,)
print("A.shape:", A.shape)          # (2, 3)
print("A @ v =", A @ v)             # [140 320]
# Row 1: 1*10 + 2*20 + 3*30 = 140
# Row 2: 4*10 + 5*20 + 6*30 = 320

# The shape rule: (rows_a, n) @ (n, cols_b) -> (rows_a, cols_b)
X = np.ones((4, 3))                 # 4 examples, 3 features each
W = np.ones((3, 5))                 # weights: 3 inputs -> 5 neurons
print("(X @ W).shape:", (X @ W).shape)   # (4, 5): 4 examples, 5 neuron outputs each

try:
    np.ones((4, 3)) @ np.ones((4, 5))    # inner sizes 3 and 4 do not match
except ValueError as error:
    print("Shape mismatch:", type(error).__name__)
```

**The shape rule** is the one thing to memorise: for `A @ B`, the **number of columns of A must equal the number of rows of B**, and the result has the rows of A and the columns of B. In a neural network layer:

```text
inputs (examples, features) @ weights (features, neurons) -> outputs (examples, neurons)
```

So one line of NumPy computes the weighted sum of **every neuron for every example** at once. That is why the forward-pass code below has no loops.

**Transpose.** `M.T` flips a matrix so rows become columns: shape `(4, 1)` becomes `(1, 4)`. You will see `.T` in the training code in section 6, where it is used purely to make shapes line up for a multiplication.

#### 4.2 The forward pass

Running inputs through the network to get an output is called a **forward pass** (or **inference**). Each layer takes the previous layer's outputs as its inputs. Using NumPy, a whole layer can be computed in one line with **matrix multiplication**:

```python
# forward_pass.py
import numpy as np

def relu(z):
    return np.maximum(0, z)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

x = np.array([2.0, 3.5, 9.0])                 # one example: 3 input features

# Layer 1: 3 inputs -> 4 hidden neurons
W1 = np.array([[ 0.2, -0.5,  0.1,  0.4],
               [ 0.3,  0.2, -0.3,  0.1],
               [-0.1,  0.05, 0.2, -0.2]])     # shape (3, 4)
b1 = np.array([0.1, 0.0, -0.2, 0.05])         # shape (4,)

# Layer 2: 4 hidden -> 1 output
W2 = np.array([[0.6], [-0.4], [0.3], [0.2]])  # shape (4, 1)
b2 = np.array([-0.3])

hidden = relu(x @ W1 + b1)                    # @ is matrix multiplication
output = sigmoid(hidden @ W2 + b2)

print("Hidden layer values:", hidden.round(3))
print("Output probability: ", output.round(3))
```

**Code walkthrough:**

- `x @ W1` multiplies the 3 inputs (shape `(3,)`) by a 3×4 weight matrix (shape `(3, 4)`), producing 4 weighted sums at once (shape `(4,)`), one per hidden neuron. Column *j* of `W1` holds the three weights of hidden neuron *j*. This is exactly the hand calculation from section 2.1, done for four neurons simultaneously.
- Adding `b1` adds each neuron's bias; `relu` applies the activation.
- The second layer repeats the pattern, and `sigmoid` turns the final number into a probability.
- Matrix multiplication is why **GPUs** matter: they perform huge numbers of these multiplications in parallel.

#### 4.3 Counting parameters

Every weight and bias is a parameter. For a dense layer: **parameters = (inputs × outputs) + outputs**.

In the example above: layer 1 has 3×4 + 4 = 16, layer 2 has 4×1 + 1 = 5, so **21 parameters** in total.

A small image classifier might have millions of parameters. Large language models have **billions** (and the largest are reported to have far more). Same building blocks, enormously more of them. This scale is why LLMs are expensive to train and why their individual decisions are very hard to explain.

### 5. How Neural Networks Learn

Random weights produce random answers. **Training** is the process of nudging every weight and bias, step by step, so the network's predictions get closer to the labels. It has four ingredients.

#### 5.1 The loss function: measuring "how wrong"

A **loss function** turns the gap between prediction and truth into a single number. Lower is better.

- For regression, a common loss is **mean squared error (MSE)**: the average of (prediction - truth)².
- For classification, a common loss is **cross-entropy (log loss)**: it punishes confident wrong answers very heavily. Predicting 0.99 for "flaky" when the truth is "defect" costs far more than predicting 0.6.

Training has one goal: **make the loss as small as possible** on the training data, while still generalising to unseen data.

#### 5.2 Gradient descent: walking downhill in the fog

Imagine standing on a hillside in thick fog, trying to reach the lowest point of the valley. You cannot see the valley, but you can feel the slope under your feet. A sensible strategy: **take a small step in the steepest downhill direction, then repeat.**

That is **gradient descent**:

- The "landscape" is the loss, plotted against all the weights.
- The **gradient** is the slope: for each weight, it says "if you increase this weight slightly, the loss goes up (or down) by this much".
- Each step updates every weight a little in the direction that reduces loss:

```text
new_weight = old_weight - learning_rate * gradient
```

The **learning rate** is the step size, a hyperparameter:

| Learning rate | What happens |
|---------------|-------------|
| Too small | Training is painfully slow; may stop before reaching a good point. |
| Too large | Steps overshoot the valley; loss jumps around or explodes. |
| About right | Loss falls steadily, then levels off. |

#### 5.3 One training step, worked by hand

Analogies only go so far. Let us perform **one complete training step** with real numbers on the smallest possible network: **one neuron, one input, sigmoid activation, squared-error loss**.

Setup:

- Input `x = 2.0`, correct label `y = 1` (say, "this failure is flaky").
- Starting weight `w = 0.5`, starting bias `b = 0.0`.
- Learning rate = `1.0`.

**Step 1: forward pass.**

```text
z = w * x + b = 0.5 * 2.0 + 0.0 = 1.0
a = sigmoid(1.0)              = 0.7311      (the prediction)
```

**Step 2: loss.**

```text
loss = (a - y)²  = (0.7311 - 1)²  = 0.0723
```

The prediction (0.73) is too low; the truth is 1. We want to push it up.

**Step 3: gradients (how does the loss change if we nudge w or b?).** The weight affects the loss through a **chain** of steps: `w` changes `z`, `z` changes `a`, `a` changes the loss. To find the total effect, we find the effect of each link and **multiply them together**. That is the **chain rule**, and it is the whole idea behind backpropagation.

| Link in the chain | Meaning | Formula | Value |
|-------------------|---------|---------|-------|
| loss ← a | How the loss changes as the prediction changes | 2 × (a − y) | 2 × (0.7311 − 1) = **−0.5379** |
| a ← z | Slope of the sigmoid at z | a × (1 − a) | 0.7311 × 0.2689 = **0.1966** |
| z ← w | How z changes as w changes | x | **2.0** |
| z ← b | How z changes as b changes | 1 | **1.0** |

Multiply along each chain:

```text
gradient for w = (-0.5379) * 0.1966 * 2.0 = -0.2115
gradient for b = (-0.5379) * 0.1966 * 1.0 = -0.1058
```

A **negative** gradient means "increasing this parameter would **decrease** the loss", which is what we want.

**Step 4: update with gradient descent.**

```text
new w = 0.5 - 1.0 * (-0.2115) = 0.7115
new b = 0.0 - 1.0 * (-0.1058) = 0.1058
```

**Step 5: check that it helped.**

```text
new z = 0.7115 * 2.0 + 0.1058 = 1.5288
new a = sigmoid(1.5288)       = 0.8218
new loss = (0.8218 - 1)²      = 0.0317     (down from 0.0723)
```

The prediction moved from 0.73 towards 1, and the loss more than halved. **Training is nothing more than repeating this step thousands of times, for every weight, on many examples.** Here is the same step in Python, so you can verify every number:

```python
# one_training_step.py
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

x, y = 2.0, 1.0          # input and correct label
w, b = 0.5, 0.0          # starting parameters
learning_rate = 1.0

# Forward pass and loss
z = w * x + b
a = sigmoid(z)
loss = (a - y) ** 2
print(f"before: prediction={a:.4f}  loss={loss:.4f}")

# Backward pass: chain rule, one link at a time
dloss_da = 2 * (a - y)        # loss <- a
da_dz = a * (1 - a)           # a <- z (sigmoid slope)
grad_w = dloss_da * da_dz * x # z <- w is x
grad_b = dloss_da * da_dz * 1 # z <- b is 1
print(f"gradients: w={grad_w:.4f}  b={grad_b:.4f}")

# Gradient descent update
w -= learning_rate * grad_w
b -= learning_rate * grad_b

a_new = sigmoid(w * x + b)
print(f"after:  prediction={a_new:.4f}  loss={(a_new - y) ** 2:.4f}  (w={w:.4f}, b={b:.4f})")
```

#### 5.4 Backpropagation: sharing the blame

In section 5.3 the chain had three links. In a network with many layers, the chain is longer: an early-layer weight affects a hidden neuron, which affects the next layer, which affects the output, which affects the loss. **Backpropagation** is the systematic way of applying the chain rule through all those layers. It starts from the error at the output and works **backwards**, layer by layer, reusing each layer's result to calculate the previous layer's gradients efficiently. Gradient descent then uses those gradients to update every weight.

A useful analogy is a relay team reviewing a lost race: they start with the final time, then work backwards leg by leg to work out how much each runner's performance contributed, so each runner knows exactly what to improve.

You will almost never implement backpropagation by hand in industry; frameworks such as PyTorch and TensorFlow compute gradients automatically. But knowing how it works explains how a network with billions of parameters can learn at all, and section 6 shows it for a real two-layer network.

#### 5.5 Epochs and batches

- An **epoch** is one complete pass through the entire training dataset.
- Data is usually processed in **batches** (for example, 32 examples at a time). The network updates its weights after each batch. This is more efficient than one example at a time and more practical than the whole dataset at once.
- Training typically runs for many epochs, while you watch the loss on training data **and** on held-back validation data.

The full loop:

```text
repeat for each epoch:
    for each batch of training examples:
        1. Forward pass:   compute predictions
        2. Loss:           measure how wrong they are
        3. Backward pass:  backpropagation computes gradients
        4. Update:         gradient descent adjusts weights
    check loss on validation data (stop early if it starts getting worse)
```

### 6. Build It: A Network That Learns XOR From Scratch

Now let us put every idea together. We will train a tiny network with **2 inputs, 4 hidden neurons and 1 output** to learn XOR using only NumPy, so nothing is hidden inside a library.

```python
# xor_from_scratch.py
import numpy as np

rng = np.random.default_rng(0)

# Training data: the four XOR cases
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 1. Initialise weights randomly (small values) and biases at zero
W1 = rng.normal(0, 1, (2, 4))    # 2 inputs  -> 4 hidden neurons
b1 = np.zeros(4)
W2 = rng.normal(0, 1, (4, 1))    # 4 hidden -> 1 output
b2 = np.zeros(1)

learning_rate = 1.0

for epoch in range(5001):
    # 2. Forward pass
    hidden = sigmoid(X @ W1 + b1)          # shape (4 examples, 4 hidden values)
    output = sigmoid(hidden @ W2 + b2)     # shape (4, 1)

    # 3. Loss: mean squared error
    loss = np.mean((output - y) ** 2)

    # 4. Backward pass (backpropagation): gradients via the chain rule
    d_output = 2 * (output - y) / len(X) * output * (1 - output)
    d_W2 = hidden.T @ d_output
    d_b2 = d_output.sum(axis=0)
    d_hidden = (d_output @ W2.T) * hidden * (1 - hidden)
    d_W1 = X.T @ d_hidden
    d_b1 = d_hidden.sum(axis=0)

    # 5. Gradient descent update
    W2 -= learning_rate * d_W2
    b2 -= learning_rate * d_b2
    W1 -= learning_rate * d_W1
    b1 -= learning_rate * d_b1

    if epoch % 1000 == 0:
        print(f"epoch {epoch:4d}  loss {loss:.4f}")

print("\nPredictions after training:")
for inputs, prob in zip(X, output):
    print(f"  {inputs.astype(int)} -> {prob[0]:.3f}  (rounded: {int(prob[0] > 0.5)})")
```

**Code walkthrough:**

- **Initialisation:** weights start as small random numbers. If they all started equal, every hidden neuron would learn the same thing; randomness lets them specialise.
- **Forward pass:** identical to section 4.2, but for all four examples at once (each row of `X` is one example). Shapes: `X` is `(4, 2)`, `W1` is `(2, 4)`, so `hidden` is `(4, 4)`: four examples, four hidden values each.
- **Loss:** mean squared error between predictions and labels.
- **Backward pass:** explained line by line in the table below.
- **Update:** `W -= learning_rate * gradient` is the gradient-descent rule from section 5.2. `-=` means "subtract and store back into the same variable".
- **Printing every 1,000 epochs** lets you watch the loss fall, which is the most basic health check of any training run.

**The backward pass, line by line.** Each line is the hand calculation from section 5.3, done for whole matrices at once:

| Line | Plain-English meaning | Link to section 5.3 |
|------|----------------------|---------------------|
| `d_output = 2 * (output - y) / len(X) * output * (1 - output)` | How much the loss changes as each output neuron's `z` changes. `/ len(X)` appears because the loss is an **average** over 4 examples. | `dloss_da * da_dz` |
| `d_W2 = hidden.T @ d_output` | Gradient for each output-layer weight: the error signal times the input that weight received (here, the hidden values). `.T` lines the shapes up: `(4, 4)` @ `(4, 1)` → `(4, 1)`, the same shape as `W2`. | `... * x` |
| `d_b2 = d_output.sum(axis=0)` | Gradient for the output bias: add up the error signal over all examples. | `... * 1` |
| `d_hidden = (d_output @ W2.T) * hidden * (1 - hidden)` | **The backwards step.** Send the output error back through the weights `W2` to find each hidden neuron's share of the blame, then multiply by the sigmoid slope of each hidden neuron. | The chain gets one layer longer |
| `d_W1 = X.T @ d_hidden` | Gradient for each first-layer weight: hidden error signal times the input it received (the original features). | `... * x` |
| `d_b1 = d_hidden.sum(axis=0)` | Gradient for the hidden biases. | `... * 1` |

A useful self-check: **every gradient has exactly the same shape as the parameter it updates** (`d_W1` matches `W1`, `d_b2` matches `b2`, and so on). If you ever write training code and the shapes do not match, you have found your bug.

When you run it, the loss should drop from roughly 0.3 at the start (no better than guessing) to close to 0, and the rounded predictions should match the XOR table: `0, 1, 1, 0`. A single neuron could never do this. The hidden neurons learned intermediate features (typically combinations similar to "A or B" and "A and B") that together make XOR solvable.

> **Try it:** shrink the hidden layer to **2 neurons** (change `(2, 4)` to `(2, 2)`, `np.zeros(4)` to `np.zeros(2)` and `(4, 1)` to `(2, 1)`), then try random seeds 0 to 19 in `default_rng(...)`. Most seeds learn XOR, but some (for example 5, 6 and 13) get stuck with a loss around 0.13-0.17 and wrong predictions. Same code, same data, different random start, different result. Keep that in mind: **neural network training is not perfectly deterministic**, and that is one root of the variable behaviour you will see from AI tools.

### 7. Families of Neural Networks

Different problems use different network shapes, called **architectures**:

| Architecture | Designed for | Key idea | QE connection |
|--------------|-------------|----------|---------------|
| **Feed-forward / MLP** | Tabular data | Dense layers; data flows one way. | Predicting flaky tests or build risk from metrics. |
| **Convolutional Neural Network (CNN)** | Images | Small filters slide over the image, detecting local patterns (edges, shapes) wherever they appear. | Visual regression tools that recognise UI elements in screenshots. |
| **Recurrent Neural Network (RNN, LSTM)** | Sequences (text, time series) | Processes items one at a time, carrying a "memory" forward. | Older text and log models; largely replaced for language by Transformers. |
| **Transformer** | Sequences, especially language | **Attention**: every word can directly look at every other word to decide what matters. | The architecture behind today's LLMs. You will learn its core idea in the Generative AI concepts lesson later today. |

### 8. Training Challenges in Brief

- **Overfitting:** big networks can memorise training data. Common remedies are more data, **early stopping** (stop when validation loss starts to rise), and **dropout** (randomly switching off neurons during training so the network cannot rely on any single one).
- **Vanishing gradients:** in very deep networks, gradients can shrink to almost nothing as they travel backwards, so early layers stop learning. ReLU activations and other architectural tricks largely solved this.
- **Data and compute hunger:** deep networks often need large datasets and GPU time.
- **Opacity:** with millions of weights, explaining *why* a particular prediction was made is hard. This is an active research area called **interpretability** or **explainability**.

### 9. What This Means for You as a Quality Engineer

| Neural network fact | What you will observe | Healthy tester response |
|---------------------|----------------------|-------------------------|
| Outputs are **probabilities**, not facts. | AI tools give plausible-sounding answers that can be wrong. | Treat output as a draft to verify, not a verdict. |
| A high probability is **not proof** of correctness. | A model can be 99% "confident" and wrong, especially on unusual inputs. | Do not equate confidence or fluency with accuracy. |
| Behaviour comes from **training data**. | Tools work best on common patterns and worse on your organisation's unusual ones. | Expect weaker results on niche frameworks or internal conventions. |
| Training and generation involve **randomness**. | The same request can give different results on different runs. | Do not assume one good run proves reliability. |
| Knowledge is spread across **millions or billions of weights**. | You cannot "read the code" to find a bug. | Judge by behaviour: test with varied inputs, which is classic black-box testing. |

How to verify AI output systematically is a big topic in its own right. We will cover it in depth on Wednesday.

---

## Practice Exercises

1. **By hand.** Using the neuron in section 2.1 (weights 2.0, 0.5, 1.5; bias -3.0; step activation), compute the output for: (a) smoke test, 1 failure, staging; (b) non-smoke test, 6 failures, not staging. Show the weighted sum each time.
2. **Count parameters.** A network has 10 inputs, a hidden layer of 32 neurons, a second hidden layer of 16 neurons and 3 outputs. How many parameters does it have? Show the calculation per layer.
3. **Learning rate experiment.** In `xor_from_scratch.py`, try learning rates of `0.01`, `1.0` and `100.0`. Record the final loss for each. Explain what you see using the "walking downhill in the fog" analogy.
4. **Remove the hidden layer's non-linearity.** Replace `sigmoid` in the **hidden** layer with an identity function (`lambda z: z`) and adjust the backward pass by replacing `hidden * (1 - hidden)` with `1`. Does the network still learn XOR? Explain why, using section 3.1.
5. **Play visually.** Open the TensorFlow Neural Network Playground (link below). Choose the circular "ring" dataset. Find the smallest network (fewest neurons and layers) that separates the classes. Then remove all hidden layers and observe what happens.

---

## Knowledge Check

1. What three steps does a single artificial neuron perform?
2. Why does a network need non-linear activation functions?
3. What is the role of the learning rate in gradient descent?
4. In one sentence, what does backpropagation do?
5. Which neural network architecture underlies today's large language models?

<details>
<summary>Suggested answers</summary>

1. Multiply each input by its weight, sum them and add a bias, then apply an activation function.
2. Without non-linearity, stacked layers collapse into a single linear function and cannot model complex patterns such as XOR.
3. It sets the size of each weight-update step: too small is slow, too large overshoots.
4. It works backwards from the output error to calculate how much each weight contributed (its gradient), so gradient descent can update it.
5. The Transformer.

</details>

---

## Glossary

- **Neuron (node, unit):** Computes a weighted sum of inputs plus a bias, then applies an activation function.
- **Weight:** A learned number expressing how strongly an input influences a neuron.
- **Bias:** A learned number that shifts a neuron's activation threshold.
- **Activation function:** A function (e.g. ReLU, sigmoid, softmax) applied to a neuron's weighted sum, usually non-linear.
- **Hidden layer:** A layer between input and output whose values are learned internal features.
- **Forward pass:** Computing the output from the input, layer by layer.
- **Loss function:** A measure of how wrong the predictions are.
- **Gradient descent:** Repeatedly adjusting weights in the direction that reduces loss.
- **Learning rate:** The step size used in gradient descent.
- **Backpropagation:** The algorithm that computes each weight's gradient by working backwards from the output error.
- **Epoch / Batch:** One full pass over the training data / a subset of examples processed before one weight update.

---

## Summary

- An artificial neuron computes **weighted sum + bias**, then applies an **activation function**.
- **Non-linear activations** (ReLU, sigmoid) let stacked layers learn complex patterns; without them, depth adds nothing.
- Networks are organised into **input, hidden and output layers**; a **forward pass** produces a prediction using matrix multiplication.
- Training minimises a **loss** using **gradient descent**, with **backpropagation** computing every weight's gradient, over many **epochs** and **batches**.
- You built a network from scratch that learns **XOR**, something a single neuron cannot.
- Different **architectures** suit different data; the **Transformer** powers modern LLMs.
- For QE: neural network outputs are **probabilistic, data-dependent and opaque**, so they must be verified by behaviour, not trusted on confidence.

---

## Additional Resources

- 3Blue1Brown, *Neural Networks* lesson series (outstanding visual explanations of neurons, gradient descent and backpropagation): https://3blue1brown.com/lessons/neural-networks
- Google for Developers, *Machine Learning Crash Course: Neural networks*: https://developers.google.com/machine-learning/crash-course/neural-networks
- TensorFlow, *A Neural Network Playground* (train small networks visually in your browser): https://playground.tensorflow.org
