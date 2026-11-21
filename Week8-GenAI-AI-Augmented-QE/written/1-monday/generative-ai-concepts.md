# Generative AI Concepts

## Learning Objectives

By the end of this lesson you will be able to:

- Define **Generative AI** and contrast **generative** models with the **discriminative** (predictive) models you met earlier today.
- Explain what **foundation models** and **large language models (LLMs)** are, and name the kinds of content GenAI can produce (text, code, images, audio, video) including **multimodal** models.
- Describe how an LLM produces text: **tokens**, **next-token prediction**, **probability distributions** and **sampling**.
- Explain the core idea of the **Transformer** and its **attention** mechanism at an intuitive level.
- Describe the stages that turn a raw model into a helpful assistant: **pre-training**, **fine-tuning / instruction tuning** and **alignment (e.g. RLHF)**.
- Explain the generation settings you will see in tools and APIs: **temperature**, **top-p**, **max tokens**, and the **context window**.
- Name the key limitations of GenAI, especially **hallucination**, **non-determinism** and **knowledge cut-offs**, and explain *why* each happens.
- Build a tiny next-word generator in Python to see the core mechanism with your own eyes.

---

## Why This Matters

Today you have travelled from AI to machine learning, to neural networks, to NLP. This lesson is where those threads meet. **Generative AI is deep learning (neural networks) applied to language and other media, trained largely by self-supervised learning, and built on decades of NLP.**

Generative AI is the technology behind the tools that are changing everyday QE work: chat assistants, coding assistants inside your IDE, tools that draft test cases from requirements, and the QA agent you will build this Friday. To use these tools well, and to judge their output critically, you need to know **what they are actually doing**. Most mistakes people make with GenAI come from a wrong mental model, such as "it looks things up in a database" or "it knows when it is unsure". Neither is true, and by the end of this lesson you will understand why.

This lesson is conceptual. How to *write* effective instructions for these models (prompt engineering) is the subject of Tuesday, and how to apply them across the QA lifecycle is Wednesday.

---

## The Concept

### 1. What Is Generative AI?

**Generative AI (GenAI)** refers to AI systems that **create new content** (text, code, images, audio, video, structured data) that resembles the data they were trained on, usually in response to an input called a **prompt**.

The key word is *create*. Compare the two families of models:

| | Discriminative (predictive) models | Generative models |
|--|------------------------------------|-------------------|
| Question they answer | "Which category does this belong to?" / "What number?" | "What content would plausibly come next / fit this request?" |
| Output | A label, score or number | New content |
| Examples from today | The flaky-test classifier, the build-risk model, the bug router | An LLM writing a test plan draft; an image model creating a UI mock-up |
| QE example | "Is this failure flaky?" -> `0.83` | "Summarise this failure log for a developer" -> a paragraph |

You already built discriminative models today. Generative models are different in *what* they output, but they are built from the same ingredients: neural networks, trained on data, by minimising a loss.

### 2. Foundation Models and LLMs

A **foundation model** is a very large model trained on a broad, massive dataset that can be adapted to many tasks. Instead of training a separate model for every task (one for bug routing, one for summarisation, one for translation), one foundation model can handle many tasks from instructions alone.

A **Large Language Model (LLM)** is a foundation model specialised in language (and, very often, code, which is also a language). "Large" refers to:

- **Parameters:** billions of weights (the same weights you met in the neural network lesson).
- **Training data:** enormous collections of text and code from many sources.
- **Compute:** training requires large clusters of specialised hardware.

You will encounter LLM families from several organisations, such as OpenAI's GPT models, Anthropic's Claude, Google's Gemini, Meta's Llama and Mistral's models. Some are available only through hosted services; others are **open-weight**, meaning the trained weights can be downloaded and run on your own infrastructure. The specific models change quickly; the concepts in this lesson do not.

#### 2.1 Beyond text: other kinds of generative models

| Modality | What it generates | QE-relevant example |
|----------|-------------------|---------------------|
| Text | Prose, summaries, explanations | Bug-report summaries, test plan drafts |
| Code | Source code in many languages | Draft pytest or Playwright code |
| Images | Pictures from descriptions | UI mock-ups; varied images for upload-feature testing |
| Audio / speech | Speech, sound | Voice inputs for testing voice features |
| Video | Short clips | Demo or training media |
| Structured data | Tables, records in specific formats | Synthetic test records |

A **multimodal** model can take in and/or produce more than one type, for example reading a **screenshot** of a web page and describing what looks broken. Many current LLMs are multimodal.

### 3. How an LLM Generates Text

This is the most important section of the lesson. The core mechanism of an LLM is surprisingly simple to state:

> **An LLM repeatedly predicts the next token, given all the tokens so far.**

Let us unpack every word.

#### 3.1 Tokens

LLMs do not read words or characters directly; they read **tokens**. A token is a chunk of text, often a whole common word, a piece of a longer word, a space plus a word, or a punctuation mark. Modern models use **sub-word tokenisation** (a common method is **byte-pair encoding, BPE**), which builds a vocabulary of frequent chunks from training data.

An illustrative (not exact) split:

```text
"Playwright locator timed out"
  -> ["Play", "wright", " loc", "ator", " timed", " out"]
```

Common words become a single token; rarer words split into several pieces. This lets a fixed vocabulary (often tens of thousands to a few hundred thousand tokens) represent **any** text, including made-up words, code and typos, which links straight back to the tokenisation you learned in the NLP lesson.

Why tokens matter to you in practice:

- **Limits are measured in tokens**, not words or characters (see the context window, section 6).
- **Costs** of hosted models are usually charged **per token** of input and output.
- As a rough rule of thumb for English, one token is about **three-quarters of a word**, so 1,000 tokens is roughly 750 words. Code, non-English text and unusual strings (IDs, hashes, base64) often use more tokens.

Each token is converted into an **embedding** (a vector of numbers), exactly the idea you met in the NLP lesson, before entering the neural network.

#### 3.2 Next-token prediction

Given the text so far, the model outputs a **probability for every token in its vocabulary**: how likely is each one to come next? For the input *"Given the user is on the login"*, the model might produce:

```text
" page"     0.62
" screen"   0.21
" form"     0.09
" button"   0.03
...         (tens of thousands of other tokens with tiny probabilities)
```

These probabilities come from the **softmax** function you met in the neural network lesson, applied to the network's final scores.

#### 3.3 Sampling and the generation loop

The model then **chooses** one token from that distribution, appends it to the text, and repeats:

```text
"Given the user is on the login"            -> picks " page"
"Given the user is on the login page"       -> picks ","
"Given the user is on the login page,"      -> picks " When"
... repeat until a special end token or a length limit is reached
```

This loop is called **autoregressive generation**: each new token depends on all previous ones, including the tokens the model itself just generated. Notice the consequence: **an early wrong token can steer everything that follows**, because later tokens are built on top of it.

#### 3.4 Build it: a tiny next-word generator

To make this concrete, let us build the simplest possible language model: a **bigram model** that learns which word tends to follow which, from a handful of Gherkin-style sentences (you wrote Gherkin in Week 6). Real LLMs are vastly more sophisticated, but the *generation loop* is the same.

```python
# tiny_language_model.py
import random
from collections import Counter, defaultdict

corpus = """
given the user is on the login page
when the user enters a valid password
then the user sees the dashboard
given the user is on the cart page
when the user applies a valid coupon
then the user sees the discounted total
given the user is on the search page
when the user enters a product name
then the user sees matching products
""".split()

# 1. "Training": count which word follows which
next_word_counts = defaultdict(Counter)
for current, nxt in zip(corpus, corpus[1:]):
    next_word_counts[current][nxt] += 1

def next_word_probabilities(word):
    counts = next_word_counts[word]
    total = sum(counts.values())
    return {w: c / total for w, c in counts.items()}

print("After 'the':", {w: round(p, 2) for w, p in next_word_probabilities("the").items()})

# 2. "Generation": repeatedly sample the next word
def generate(start: str, length: int = 8, seed: int | None = None) -> str:
    rng = random.Random(seed)
    words = [start]
    for _ in range(length):
        probs = next_word_probabilities(words[-1])
        if not probs:
            break
        choices, weights = zip(*probs.items())
        words.append(rng.choices(choices, weights=weights)[0])
    return " ".join(words)

for seed in (1, 2, 3):
    print(generate("given", seed=seed))
```

**Code walkthrough:**

- `corpus` is our tiny "training data", split into words (word-level tokens for simplicity).
- `defaultdict(Counter)` creates a dictionary where each word maps to a counter of the words that followed it. `zip(corpus, corpus[1:])` walks through pairs of neighbouring words. This counting is our whole "training".
- `next_word_probabilities` turns counts into probabilities, the equivalent of the LLM's probability distribution over its vocabulary.
- `rng.choices(choices, weights=weights)` **samples** a word according to those probabilities, so likely words are chosen more often but not always.
- Running with different seeds produces **different sentences**, some sensible and some odd mixtures. With seed 1 you should see *"given the cart page when the user sees matching"*: fluent-ish, built entirely from real training phrases, yet describing a scenario that never existed That is a toy version of two real LLM behaviours: **variability** between runs, and **fluent-sounding output that was never in the training data and is not necessarily correct**.

The gigantic difference between this toy and an LLM: our model looks back **one** word; an LLM considers **thousands of tokens of context at once** through attention, and its "knowledge" is stored in billions of learned weights rather than a small count table.

### 4. The Transformer and Attention (Intuition Only)

Earlier language models read text one word at a time and struggled to remember things from far back in a sentence. In 2017, the paper *"Attention Is All You Need"* introduced the **Transformer** architecture, which underlies essentially all modern LLMs.

Its key idea is **self-attention**: when processing each token, the model can **look at every other token in the context and decide how much each one matters** for understanding the current one.

Example:

```text
"The test failed because it could not find the button, so we updated it."
```

What does the final "**it**" refer to? The test? The button? The locator? Attention lets the model weigh all earlier tokens and, through learned patterns, connect "it" to the most plausible antecedent. This is also how **contextual embeddings** (from the NLP lesson) are produced: each token's vector is updated using information from the tokens it attends to.

Two more practical benefits:

- Transformers process all tokens of the input **in parallel** during training, which suits GPUs and made training on huge datasets feasible.
- Stacking many attention layers lets the model build up increasingly abstract understanding, just like deeper layers in the neural network lesson learned more complex features.

You do not need the full mathematics of attention for this course, but a small worked example makes the idea concrete. Remember: **attention = each token looks at all the others to decide what is relevant.**

#### 4.1 Attention in miniature

Attention works with three roles for every token, usually explained with a library analogy:

| Role | Library analogy | In the model |
|------|-----------------|--------------|
| **Query** | The question you bring to the library desk: "I need something about UI elements." | What the current token is looking for. |
| **Key** | The label on each book's spine. | What each token offers, used to judge relevance. |
| **Value** | The content inside the book. | The information a token passes on if it is found relevant. |

The steps for one token are:

1. Compare its **query** with every token's **key** using a **dot product** (multiply position by position and add, the same operation as a neuron's weighted sum). A bigger result means "more relevant".
2. Scale the scores down (divide by the square root of the vector length) to keep the numbers in a sensible range.
3. Apply **softmax** to turn the scores into **attention weights** that add up to 1.
4. Take a weighted mix of the tokens' **values** using those weights. That mix becomes the token's new, context-aware representation.

Here is steps 1 to 3 for the word "it" in *"the test clicked the button but it was hidden"*, using hand-made 3-number vectors. In a real model these vectors have hundreds or thousands of numbers and are **learned during training**, not written by hand:

```python
# attention_toy.py
import numpy as np

tokens = ["the", "test", "clicked", "the", "button", "but", "it", "was", "hidden"]

# Toy 3-number "meaning" vectors. Pretend dimensions: [is-a-UI-element, is-an-action, is-a-pronoun]
keys = np.array([
    [0.0, 0.0, 0.0],   # the
    [0.2, 0.1, 0.0],   # test
    [0.1, 1.0, 0.0],   # clicked
    [0.0, 0.0, 0.0],   # the
    [1.0, 0.1, 0.0],   # button
    [0.0, 0.0, 0.0],   # but
    [0.3, 0.0, 1.0],   # it
    [0.0, 0.2, 0.0],   # was
    [0.6, 0.3, 0.0],   # hidden
])

# The query for "it" asks: "which earlier word is a UI element I could be referring to?"
query_it = np.array([4.0, 0.0, 0.0])

scores = keys @ query_it / np.sqrt(len(query_it))      # one relevance score per token
weights = np.exp(scores) / np.exp(scores).sum()          # softmax -> attention weights sum to 1

for token, weight in sorted(zip(tokens, weights), key=lambda p: p[1], reverse=True)[:4]:
    print(f"{token:8s} {weight:.2f}")
```

Output:

```text
button   0.44
hidden   0.17
it       0.09
test     0.07
```

**Code walkthrough:**

- Each row of `keys` describes one token. We invented three meaning dimensions so you can read them: "button" scores high on *is-a-UI-element*; "clicked" scores high on *is-an-action*.
- `query_it` is what "it" is looking for: something that is a UI element (a pronoun usually refers back to a thing).
- `keys @ query_it` is a matrix-times-vector multiplication: one dot product per token, giving a relevance score for each. `np.sqrt(len(query_it))` is the scaling from step 2.
- The softmax line turns scores into weights between 0 and 1 that sum to 1, exactly like the softmax in the neural network lesson.
- The result: "it" pays the most attention (0.44) to **"button"**, so the model's updated representation of "it" will be built mostly from the meaning of "button". The ambiguity is resolved: the button was hidden, not the test.

Real Transformers run this calculation for **every token at once**, many times in parallel (called **multi-head attention**, where each "head" can focus on a different kind of relationship such as grammar, references or topic), and stack dozens of such layers. The principle stays the same: score relevance, softmax, mix.

### 5. How a Raw Model Becomes a Helpful Assistant

An assistant like the ones you will use this week typically goes through several training stages:

| Stage | What happens | Type of learning | Result |
|-------|-------------|------------------|--------|
| **1. Pre-training** | The model reads an enormous amount of text and code, learning to predict the next token. | **Self-supervised** (from the supervised vs. unsupervised lesson): the real next token is the label. | A **base model** that is very knowledgeable about language patterns but just continues text; it does not reliably follow instructions. |
| **2. Fine-tuning / instruction tuning** | Further training on curated examples of instructions paired with good responses. | Supervised | A model that follows requests ("Summarise this log") rather than just continuing text. |
| **3. Alignment, e.g. RLHF** | Humans compare or rate model responses; the model is trained to prefer responses people judge helpful, honest and safe. **RLHF** = Reinforcement Learning from Human Feedback. Other alignment methods also exist. | Reinforcement learning and related techniques | An assistant that is more helpful and more likely to decline harmful requests. |

Two important consequences for testers:

- **Knowledge cut-off.** Pre-training uses data up to a certain date. The model has no built-in knowledge of anything after that, such as a library version released last month, unless a tool supplies it (for example, web search or documents you provide).
- **"Helpful-sounding" is a trained behaviour.** Alignment teaches models to produce responses people like. That usually correlates with correctness, but not always. A confident, well-structured answer can still be wrong.

Organisations can also **fine-tune** a foundation model further on their own data for specialised tasks, though for many QE uses, giving the model the right context in the request is enough. How to provide that context well is a Tuesday topic.

### 6. The Context Window

The **context window** is the maximum number of tokens the model can consider at once: your input (instructions, pasted code, documents, conversation history) **plus** the output it generates. Current models range from thousands to hundreds of thousands of tokens, and some support even more.

Think of the context window as the model's **working memory** or a desk of fixed size:

- Everything the model "knows" about **your** situation must be on the desk: the requirement, the code, the error message.
- If the conversation or document is too long, the oldest or excess content must be **dropped or summarised**, and the model can no longer see it.
- LLMs have **no memory between separate requests** by default. Chat applications create the illusion of memory by re-sending the conversation history each time.
- Even within the window, very long inputs can make it harder for a model to use every detail reliably. More context is not automatically better context.

### 7. Generation Settings: Temperature, Top-p and Max Tokens

When you use an LLM through an API or some tools, you can control *how* it samples the next token.

#### 7.1 Temperature

**Temperature** reshapes the probability distribution before sampling:

- **Low temperature (e.g. 0 to 0.3):** sharpens the distribution; the most likely tokens dominate. Output is more focused, consistent and repetitive. Good for code, structured output and factual tasks.
- **High temperature (e.g. 0.8 to 1.0 or more):** flattens the distribution; less likely tokens get picked more often. Output is more varied and "creative", and also more likely to drift.

```python
# temperature_demo.py
import numpy as np

tokens = [" page", " screen", " form", " button"]
logits = np.array([3.0, 1.9, 1.1, -0.2])     # raw scores from the model's final layer

def softmax_with_temperature(scores, temperature):
    scaled = scores / temperature
    exps = np.exp(scaled - scaled.max())
    return exps / exps.sum()

for t in (0.2, 0.7, 1.0, 1.5):
    probs = softmax_with_temperature(logits, t)
    pretty = ", ".join(f"{tok.strip()}={p:.2f}" for tok, p in zip(tokens, probs))
    print(f"temperature {t}: {pretty}")
```

**Code walkthrough:**

- **Logits** are the raw scores the network produces before softmax.
- Dividing by the temperature before softmax is exactly how temperature works. A small temperature makes big scores even bigger relative to small ones, so `" page"` takes almost all the probability. A large temperature shrinks the differences, spreading probability out.
- Run it and watch `page` go from near-certain at 0.2 to much less dominant at 1.5.

#### 7.2 Top-p and max tokens

- **Top-p (nucleus sampling):** sample only from the smallest set of the most likely tokens whose probabilities add up to at least *p* (e.g. 0.9), cutting off the long tail of unlikely tokens. Providers commonly recommend adjusting either temperature or top-p, not both at once.

Here is top-p in a few lines of Python, using a next-token distribution like the one in section 3.2:

```python
# top_p_demo.py
tokens = [" page", " screen", " form", " button"]
probs  = [0.66, 0.22, 0.09, 0.03]        # already sorted from most to least likely

def nucleus(tokens, probs, p):
    kept, total = [], 0.0
    for tok, prob in zip(tokens, probs):
        kept.append((tok, prob))
        total += prob
        if total >= p:                    # stop once the kept tokens cover probability p
            break
    return [(tok, round(prob / total, 2)) for tok, prob in kept]   # re-normalise to sum to 1

for p in (0.5, 0.8, 0.9, 1.0):
    print(f"top_p={p}: {nucleus(tokens, probs, p)}")
```

Output:

```text
top_p=0.5: [(' page', 1.0)]
top_p=0.8: [(' page', 0.75), (' screen', 0.25)]
top_p=0.9: [(' page', 0.68), (' screen', 0.23), (' form', 0.09)]
top_p=1.0: [(' page', 0.66), (' screen', 0.22), (' form', 0.09), (' button', 0.03)]
```

**Code walkthrough:** the function walks down the tokens from most to least likely, keeping each one and adding its probability to a running `total`, and stops as soon as the total reaches *p*. The kept probabilities are then **re-normalised** (divided by `total`) so they add up to 1 again, and the model samples only from that "nucleus". With `top_p=0.5`, " page" alone already covers 66%, so it is the only candidate: output becomes very predictable. With `top_p=0.9`, the three most likely tokens survive and the unlikely " button" can never be chosen. With `top_p=1.0`, nothing is cut off.

**Temperature vs. top-p in one sentence:** temperature **reshapes** the whole probability distribution (sharper or flatter); top-p **cuts off** the unlikely tail and keeps the shape of what remains.

- **Max tokens (maximum output length):** a hard cap on how many tokens the model may generate. If the cap is hit, output stops mid-thought, which matters when you expect complete code or complete structured data.

#### 7.3 Is temperature 0 deterministic?

Setting temperature to (or near) 0 makes the model pick the most likely token almost every time, which makes output **much more repeatable**. But in practice, hosted models may still produce **occasional differences** between runs, because of factors such as how computations are batched and executed on hardware, and model updates by the provider. For QE this means: **design your checks to tolerate variation in AI output, rather than assuming identical output every time.** How to validate AI output reliably is covered in depth later this week, on Wednesday and Friday.

#### 7.4 What a request looks like

Most LLM APIs accept a request shaped roughly like the following. Field names vary by provider; this is an illustrative Python dictionary, not a specific vendor's API:

```python
# request_shape.py  (illustrative only: no network call is made)
request = {
    "model": "example-llm-model",
    "messages": [
        {"role": "user", "content": "Summarise this failure log in two sentences: ..."},
    ],
    "temperature": 0.2,     # focused, repeatable output
    "max_tokens": 300,      # cap on output length
}
print(sorted(request.keys()))
```

The model's response contains the generated text plus metadata such as **token usage** (input and output tokens), which is what you are billed for. You will see live calls in today's instructor demo. Writing effective instructions inside that `content` field is Tuesday's topic, and the extra roles and structure used to build agents are covered on Thursday.

### 8. Limitations You Must Understand

Every limitation below follows directly from the mechanics you just learned.

| Limitation | What it looks like | Why it happens |
|-----------|--------------------|----------------|
| **Hallucination** | Confident, fluent output that is false: an invented API method, a non-existent pytest flag, a fabricated citation. | The model generates **plausible** continuations, not verified facts. There is no built-in fact-checker, and the generation loop does not stop to check a source. |
| **Non-determinism** | Different answers to the same request. | Sampling from probabilities (section 3.3); infrastructure effects (section 7.3). |
| **Knowledge cut-off** | Unaware of recent library versions, new APIs or your company's latest changes. | Pre-training data stops at a date (section 5). |
| **No access to your context by default** | Generic answers that ignore your framework, naming conventions or environments. | The model only sees what is in its context window (section 6). |
| **Sensitivity to wording** | Small changes in how you ask produce noticeably different results. | Different input tokens shift every next-token probability. (Tuesday is about working *with* this.) |
| **Calculation and counting errors** | Mistakes in arithmetic, counting items or exact string manipulation. | Text is processed as tokens, not digits or characters, and the model predicts likely text rather than executing an algorithm (unless it is connected to a tool such as a code runner). |
| **Bias** | Outputs that reflect stereotypes or skews in training data. | Models learn patterns present in their data, including unwanted ones. |
| **Security and privacy risks** | Leaking sensitive data that was pasted in; being manipulated by malicious instructions hidden in input (**prompt injection**). | The model treats everything in its context as text to respond to. |

Two short notes on the last rows. First, never paste secrets (passwords, API keys, tokens, customer personal data) into an AI tool that is not approved for that data; you learned to protect secrets in Week 7's CI/CD lessons, and the same discipline applies here. Second, responsible use of AI in QE is a full lesson on Wednesday, and testing the security of AI-powered products comes in later weeks; for today, just recognise the names.

#### 8.1 Hallucination deserves special attention

For a quality engineer, hallucination is the single most important limitation, because hallucinated output often **looks exactly like correct output**. Examples you may genuinely encounter:

- A Playwright method that sounds right but does not exist in the library.
- A test that passes because it asserts something trivially true rather than the requirement.
- A confident explanation of a failure that ignores the actual stack trace.

Remember from the neural network lesson: **fluency and confidence are not evidence of correctness.** Treat GenAI output as a fast, often useful **first draft** from a capable but unreliable colleague, which must be reviewed. You will learn a structured approach to that review on Wednesday.

### 9. Key Terms You Will Hear This Week (Recognition Only)

| Term | One-line meaning | Covered in depth |
|------|------------------|------------------|
| **Prompt** | The input text you give a model. | Prompt engineering, Tuesday |
| **System instructions** | Standing instructions that shape a model's behaviour across a conversation or task. | Agent instructions, Thursday |
| **AI agent** | A system that uses an LLM to work towards a goal, often taking steps and using tools. | Thursday and Friday (and Week 9) |
| **Embeddings / semantic search** | Meaning-vectors used to find related content. | Introduced in today's NLP lesson |
| **Retrieval-augmented generation (RAG)** | Supplying a model with relevant documents retrieved at request time so its answers are grounded in them. | Later in the program |

---

## Practice Exercises

1. **Discriminative or generative?** Classify each: (a) a model that predicts whether a pull request will break the build; (b) a tool that drafts a bug report from a failing test's output; (c) a model that labels screenshots as "layout OK" or "layout broken"; (d) a tool that creates 50 realistic fake customer addresses.
2. **Run the toy LLM.** Run `tiny_language_model.py` with seeds 1 to 10. Find at least one generated sentence that is grammatical but **not** in the training data and would describe a wrong test (for example, mixing the coupon and login flows). Explain in two sentences how this relates to hallucination.
3. **Attention by hand.** In `attention_toy.py`, change `query_it` to `[0.0, 4.0, 0.0]` (a query looking for an *action*). Before running, predict which token will receive the most attention. Run it and explain the result. Then explain in one sentence why real models learn these vectors rather than having them written by hand.
4. **Top-p.** Run `top_p_demo.py` with `p` values of 0.7 and 0.95. Which tokens survive each time? Which setting would you prefer when generating a CSS selector, and which when brainstorming unusual test ideas?
5. **Temperature.** Run `temperature_demo.py` and add temperatures `0.05` and `3.0`. Describe in plain English what each would mean for generating (a) a Playwright locator and (b) brainstorming edge-case ideas.
6. **Token budgeting.** Using the rough rule of 1 token ≈ 0.75 English words, estimate the tokens needed for: a 600-word requirement, a 300-line Python test file (assume about 8 words per line) and a 1,200-word CI log. Would they fit together in a context window of 8,000 tokens with room for a 1,000-token answer?
7. **Spot the cause.** For each scenario, name the limitation from section 8 and its root cause: (a) the assistant recommends a configuration option introduced after its training; (b) two teammates ask the same question and get different test lists; (c) the assistant ignores your project's custom `BasePage` class.

---

## Knowledge Check

1. In one sentence, what is the core mechanism by which an LLM generates text?
2. What is a token, and why do context limits and costs use tokens rather than words?
3. What does self-attention allow a Transformer to do?
4. Name the three common training stages that turn a raw model into an assistant.
5. What does lowering the temperature do to the output?
6. Why do LLMs hallucinate?
7. With top-p set to 0.8, which tokens can be sampled if the next-token probabilities are 0.5, 0.25, 0.15 and 0.10?

<details>
<summary>Suggested answers</summary>

1. It repeatedly predicts a probability distribution over the next token given all previous tokens, samples one, appends it and repeats.
2. A chunk of text (whole word, word piece or symbol) that the model processes; models read and produce tokens, so limits and billing are naturally counted in them.
3. Let each token weigh the relevance of every other token in the context when building its representation.
4. Pre-training (self-supervised next-token prediction), fine-tuning/instruction tuning, and alignment such as RLHF.
5. It makes the probability distribution sharper, so output is more focused and repeatable and less varied.
6. They generate statistically plausible continuations rather than retrieving verified facts, and nothing in the basic generation loop checks truth.
7. The first three (0.5 + 0.25 = 0.75 is below 0.8, so the 0.15 token is also needed); the 0.10 token is cut off.

</details>

---

## Glossary

- **Generative AI:** AI that creates new content resembling its training data.
- **Discriminative model:** A model that predicts a label or value for an input.
- **Foundation model:** A large model trained broadly and adaptable to many tasks.
- **LLM (Large Language Model):** A foundation model for language (and usually code).
- **Multimodal:** Able to handle more than one type of data (text, images, audio, …).
- **Token:** The unit of text an LLM reads and writes.
- **Autoregressive generation:** Producing output one token at a time, each based on all previous tokens.
- **Transformer / self-attention:** The architecture behind LLMs / its mechanism for weighing the relevance of every token to every other.
- **Pre-training / fine-tuning / RLHF:** Learning from huge unlabelled text / adapting with curated examples / aligning with human preference feedback.
- **Context window:** The maximum number of tokens (input plus output) a model can handle at once.
- **Query / key / value:** The three roles each token plays in attention: what it looks for, what it offers for matching, and the information it passes on.
- **Attention weights:** Softmax-normalised relevance scores that decide how much each token contributes to another token's representation.
- **Temperature / top-p:** Settings controlling randomness in token sampling: temperature reshapes the distribution; top-p cuts off its unlikely tail.
- **Hallucination:** Fluent, confident output that is factually wrong or invented.
- **Knowledge cut-off:** The date after which a model's training data contains no information.

---

## Summary

- **Generative AI creates content**; discriminative models predict labels. Both are built from neural networks trained on data.
- **LLMs** are huge Transformer-based models that **repeatedly predict the next token**, sampling from a probability distribution. You built a toy version that shows the same loop and the same failure modes.
- **Attention** lets each token look at every other token: query-key dot products give relevance scores, softmax turns them into weights, and the weighted mix of values gives a context-aware representation. You traced this for the word "it".
- Assistants are made through **pre-training** (self-supervised), **instruction tuning** and **alignment** (e.g. RLHF), which also explains the **knowledge cut-off**.
- The **context window** is the model's only view of your situation; **temperature**, **top-p** and **max tokens** shape the output.
- Key limitations (**hallucination, non-determinism, knowledge cut-off, missing context, bias, security risks**) follow directly from how LLMs work. For a quality engineer, the core rule is: **AI output is a draft to verify, not a fact to trust.**

---

## Additional Resources

- Google for Developers, *Machine Learning Crash Course: Introduction to Large Language Models* (tokens, Transformers, self-attention, fine-tuning): https://developers.google.com/machine-learning/crash-course/llm
- Hugging Face, *LLM Course* (free course on Transformers and LLMs, starting from the basics): https://huggingface.co/learn/llm-course/chapter1/1
- NIST, *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)* (authoritative overview of GenAI risks, including confabulation/hallucination): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
