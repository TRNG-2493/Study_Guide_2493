# Generative AI Concepts

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what Generative AI and Large Language Models (LLMs) are, and how they differ from the predictive models earlier today.
- **Describe** how an LLM writes text: tokens, next-token prediction, probabilities and sampling.
- **Explain** what the context window and temperature are, and why the same question can give different answers.
- **Describe**, at a high level, how a raw model becomes a helpful assistant.
- **Check** an AI answer for hallucination, and name the limitations every tester must remember: hallucination, knowledge cut-off and non-determinism.

---

## Why This Matters

Today you have travelled from AI to machine learning, to neural networks, to NLP. This lesson is where those threads meet. **Generative AI is deep learning applied to language and other media, built on the NLP ideas you just met.**

It is also the technology behind the tools you will use all week: chat assistants, coding assistants in your editor, tools that draft test cases from requirements, and the QA agent you will build on Friday. To use these tools well, and to judge their output, you need to know what they are actually doing.

Most mistakes people make with GenAI come from a wrong picture of how it works. Two common wrong pictures:

- *"It looks things up in a database."* It does not. It predicts likely text.
- *"It knows when it is unsure."* It does not reliably. It sounds equally confident when right and wrong.

These mistakes have real costs in software. In a 2024 study, researchers generated 576,000 code samples with 16 popular code-generating LLMs and checked every software package the code referred to. They found that on average at least 5.2% of the packages suggested by commercial models, and 21.7% of those suggested by open-source models, **did not exist** ([Spracklen et al., *We Have a Package for You!*](https://arxiv.org/abs/2406.10279)).

A developer who installs a package by that name without checking could get nothing, or worse, a malicious package that someone published under the invented name. By the end of this lesson you will understand why this happens, and how a tester guards against it.

> **Using this with the handout:** this lesson goes deeper into **Handout 02, Topic 2**. It uses the same six Gherkin lines, the same `tiny_llm.py`, and the same two prompts: the randomness check and the hallucination probe.

---

## The Concept

### 1. What Is Generative AI?

**Generative AI (GenAI)** is AI that **creates new content**, such as text, code, test cases, images or audio, instead of only sorting things or predicting a label. It usually responds to an input written in plain language, called a **prompt**.

Compare the two families of models you have met today:

| | Predictive (discriminative) models | Generative models |
|---|---|---|
| Question they answer | "Which category?" / "What number?" | "What content fits this request?" |
| Output | A label, score or number | New content |
| Examples from today | The flaky-test tree, the build-risk classifier, the duplicate finder | An LLM drafting a test plan, or explaining a stack trace |
| How you check it | Compare with the correct label | Read it against the requirement; often no single right answer |

Generative models differ in **what** they produce, but they are built from the same ingredients: neural networks, trained on data, by reducing a loss.

### 2. Foundation Models and LLMs

A **foundation model** is a very large model trained on a broad, massive dataset, which can then be used for many different tasks. Instead of training one model for bug routing, another for summarising and another for translation, one foundation model handles all of them from instructions alone.

A **Large Language Model (LLM)** is a foundation model specialised in language, which very often includes code. "Large" refers to:

- **Parameters:** billions of weights, the same kind of weights you met in *Neural Network Fundamentals*.
- **Training data:** enormous collections of text and code.
- **Compute:** training needs large clusters of specialised hardware.

You will meet LLM families from several organisations, such as OpenAI's GPT models (behind ChatGPT), Anthropic's Claude, Google's Gemini and Meta's Llama. Some are only available as hosted services; others are **open-weight**, meaning the trained weights can be downloaded and run on your own machines. The specific models change quickly. The concepts in this lesson do not.

Many current models are **multimodal**: they can take in, or produce, more than one kind of content. A multimodal model can read a screenshot of a web page and describe what looks broken, for example.

### 3. How an LLM Writes Text

This is the most important section of the lesson. The core mechanism fits in one sentence:

> **An LLM repeatedly predicts the next token, given all the tokens so far.**

Let us unpack it.

#### 3.1 Tokens

LLMs do not read whole words or single letters. They read **tokens**: chunks of text that can be a whole common word, part of a longer word, a punctuation mark, or a word with its leading space. An illustrative split (real splits vary by model):

```text
"Playwright locator timed out"
  -> ["Play", "wright", " loc", "ator", " timed", " out"]
```

Common words usually become one token; rarer words split into pieces. This lets a fixed vocabulary of tokens represent **any** text, including code, typos and invented words. It is the **tokenisation** you met in *NLP Fundamentals*, at a finer grain.

Why tokens matter to you:

- **Limits are counted in tokens**, not words (see the context window, section 6).
- **Costs** of hosted models are usually charged per token, for both what you send and what comes back.
- As a rough guide for English, OpenAI says **1 token is about 4 characters, or about three-quarters of a word**, so 100 tokens is about 75 words ([OpenAI Help Center](https://help.openai.com/en/articles/4936856)). Code, other languages, and strings such as IDs and hashes often use more tokens per word.

Each token is turned into an **embedding**, exactly as in *NLP Fundamentals*, before it enters the network.

#### 3.2 Next-token prediction

Given the text so far, the model outputs a **probability for every token in its vocabulary**: how likely is each one to come next? For the input *"Given the user is on the login"*, the probabilities might look like this (illustrative numbers):

```text
" page"     0.62
" screen"   0.21
" form"     0.09
" button"   0.03
...         (tens of thousands of other tokens with tiny probabilities)
```

These probabilities come from the **softmax** step you worked by hand in *Neural Network Fundamentals*: the network gives each possible token a score, and softmax turns the scores into probabilities that add up to 1.

#### 3.3 The generation loop

The model then **chooses** one token from those probabilities, adds it to the text, and repeats:

1. Read all the text so far.
2. Predict a probability for every possible next token.
3. Pick one, usually at random, weighted by the probabilities. This is called **sampling**.
4. Add it to the text, and go back to step 1.
5. Stop at a special "end" token, or when a length limit is reached.

An answer of 300 words is roughly 400 of these loops. Notice what is **not** in the loop: no step looks anything up, and no step checks whether the text is true. The model only ever asks, "what probably comes next?"

#### 3.4 Be the language model, by hand

Pretend your entire training data is these six Gherkin lines from the handout:

```text
given the user is on the login page
when the user enters a valid password
then the user sees the dashboard
given the user is on the cart page
when the user applies a valid coupon
then the user sees the discounted total
```

Predict the next word, using **only** what you have seen:

- *when the user enters a valid ___* → "password". In the data, "enters a valid" is always followed by "password". You are certain.
- *then the user sees the ___* → "dashboard" or "discounted". Each appears once after "sees the". You have to **choose**.
- *given the user is on the ___* → "login" or "cart". Again, a choice.

That is exactly what an LLM does at every step: sometimes one option is overwhelming, and sometimes several options are close, and it picks one.

#### 3.5 A tiny language model in Python

The handout's `tiny_llm.py` builds the smallest possible language model from those six lines. It uses standard Python only:

```python
import math
import random
from collections import Counter, defaultdict

# Step 1: the "training data" - a few lines of Gherkin
text = """
given the user is on the login page
when the user enters a valid password
then the user sees the dashboard
given the user is on the cart page
when the user applies a valid coupon
then the user sees the discounted total
"""
words = text.split()

# Step 2: "training" - count which word follows which
follows = defaultdict(Counter)
for current, nxt in zip(words, words[1:]):
    follows[current][nxt] += 1
print("After 'the':", dict(follows["the"]))

# Step 3: "generation" - pick the next word again and again
def generate(start, length=6, seed=None):
    rng = random.Random(seed)
    out = [start]
    for _ in range(length):
        options = follows[out[-1]]
        if not options:
            break
        out.append(rng.choices(list(options), weights=list(options.values()))[0])
    return " ".join(out)

for seed in (3, 10, 2):
    print(generate("when", seed=seed))

# Step 4: temperature - low = safe and predictable, high = more random
scores = {"page": 3.0, "screen": 1.9, "form": 1.1, "button": -0.2}
for t in (0.2, 1.0, 2.0):
    exps = {w: math.exp(s / t) for w, s in scores.items()}
    total = sum(exps.values())
    print(f"temperature {t}:", {w: round(e / total, 2) for w, e in exps.items()})
```

Output:

```text
After 'the': {'user': 6, 'login': 1, 'dashboard': 1, 'cart': 1, 'discounted': 1}
when the user enters a valid password
when the user sees the cart page
when the discounted total
temperature 0.2: {'page': 1.0, 'screen': 0.0, 'form': 0.0, 'button': 0.0}
temperature 1.0: {'page': 0.66, 'screen': 0.22, 'form': 0.1, 'button': 0.03}
temperature 2.0: {'page': 0.46, 'screen': 0.27, 'form': 0.18, 'button': 0.09}
```

What to notice:

- **Training** (`follows[current][nxt] += 1`) just counts which word follows which. That count table is the model's entire "knowledge". After "the", it has seen "user" 6 times and four other words once each.
- **Generation** (`rng.choices(..., weights=...)`) picks the next word at random, weighted by those counts, again and again. A fixed `seed` makes the random choices repeatable, so you get the same three sentences every run.
- **Temperature** (Step 4) divides the scores before softmax. You will meet it properly in section 7.

#### 3.6 Read the output like a tester

| Generated sentence | What happened |
|---|---|
| `when the user enters a valid password` | Copied from the training data. Correct. |
| `when the user sees the cart page` | **Fluent and believable, but never in the training data.** The model joined pieces that each "fit". A tiny **hallucination**. |
| `when the discounted total` | Nonsense. After "the" it picked "discounted", which happens to follow "the" once. |

Look closely at the middle sentence. Every pair of words in it was seen in training ("the user", "user sees", "sees the", "the cart", "cart page"). The model never checked whether the **whole** sentence was true; it only checked that each next word was likely. That is the mechanism behind hallucination, from this 30-word toy all the way up to ChatGPT, Copilot and Claude.

Real LLMs are this idea scaled up enormously: instead of counting word pairs, a neural network with billions of weights scores every possible next token using everything in the text so far. They are vastly better, rarely produce nonsense like the third sentence, and are often correct. But they are still **predicting likely text**. **Fluent does not mean correct.**

### 4. The Transformer and Attention (Intuition Only)

Our toy only looks one word back. Real LLMs look at **everything** in the text so far, and decide which parts matter for the next token. The design that does this is the **Transformer**, introduced by Google researchers in 2017 in a paper titled *"Attention Is All You Need"*.

Its key idea is **attention**: for each token, the model works out how much every other token should influence it. Consider:

> *"The tester raised a bug against the checkout page because **it** crashed on Safari."*

What does "it" refer to: the tester, the bug, or the page? You know it is the page. Attention is how the model makes that link: when processing "it", it gives high attention to "checkout page" and "crashed", and low attention to "tester".

You do not need the maths. The practical points:

- Attention lets the model use context from far back in your prompt, such as a rule you stated at the start.
- But attention is spread across everything. Very long prompts can dilute it, so instructions buried in the middle of a long text are easier to miss. You will use this on Tuesday, when you write prompts.

### 5. How a Raw Model Becomes a Helpful Assistant

A chat assistant is built in stages:

1. **Pre-training.** The model reads an enormous amount of text and learns to predict the next token. This is the **self-supervised learning** you met in *Supervised vs. Unsupervised Learning*: the text supplies its own labels, because the "correct answer" is simply the next token. The result can continue any text, but it is not yet good at following requests.
2. **Instruction tuning (fine-tuning).** The model is trained further on examples of requests paired with good responses, so it learns to answer questions and follow instructions.
3. **Alignment.** People compare and rate the model's answers, and the model is trained to prefer the kinds of answers people rated as helpful, honest and harmless. A common method is **reinforcement learning from human feedback (RLHF)**, which uses the reinforcement learning idea of rewards.

Two consequences for testers:

- The assistant has been trained to **sound helpful**. That is useful, but it also means it tends to give an answer even when the honest answer is "I don't know".
- Everything it "knows" comes from training data up to a certain date, which brings us to its limits.

### 6. The Context Window

The **context window** is the maximum amount of text, counted in tokens, that the model can take into account at once. It includes **everything**: your instructions, the conversation so far, anything you pasted, and the reply it is writing.

Think of it as the model's **short-term memory**, or a desk of fixed size: anything that does not fit on the desk is not in view. Context windows differ between models and change as new models are released, so check your tool's documentation for the current size.

**Work it out by hand.** Using the rough guide from section 3.1 (100 tokens ≈ 75 words), a 3,000-word failure log is about 3,000 ÷ 75 × 100 = **4,000 tokens**. Add your question and the reply, and that one paste may use a large share of a small context window. Logs full of IDs, timestamps and stack traces usually need even more tokens than ordinary prose.

What this means in practice:

- **In a long chat, early messages can drop out of view.** If the model starts ignoring a rule you gave at the start, restate it, or start a new chat.
- **Pasting a huge log or a whole codebase may not fit.** Some tools quietly cut the text; others refuse. Paste only the part that matters.
- **The model has no memory between separate chats** unless the tool adds a memory feature. Each new chat starts from an empty desk.

### 7. Generation Settings: Temperature, Top-p and Max Tokens

When the model picks the next token, a few settings control how it picks. Chat apps set these for you; developers set them when they call a model from code.

#### 7.1 Temperature

**Temperature** controls how much randomness goes into the choice. It divides the scores before softmax:

- **Low temperature** sharpens the probabilities, so the top choice almost always wins. Output is predictable and repetitive.
- **High temperature** flattens them, so less likely tokens get picked more often. Output is more varied, and more likely to go wrong.

Look back at the `tiny_llm.py` output. At temperature **0.2**, "page" gets a probability of 1.0 (rounded): it will be chosen every time. At **1.0**, the probabilities are the plain softmax: page 0.66, screen 0.22. At **2.0**, they spread out to page 0.46, screen 0.27, form 0.18 and button 0.09, so roughly one time in eleven the model would write "button".

As a rule of thumb:

- For **test data or structured output that must be consistent**, you want low temperature.
- For **brainstorming test ideas**, a moderate temperature gives more variety.

#### 7.2 Top-p and max tokens

- **Top-p** (also called nucleus sampling) limits the choice to the smallest set of top tokens whose probabilities add up to *p*. With top-p 0.9, the model only samples from the tokens that together make up 90% of the probability, ignoring the long tail of unlikely ones.
- **Max tokens** caps the length of the reply. If an answer stops mid-sentence, it may have hit this limit.

#### 7.3 Same question, different answers

Because of sampling, **the same prompt can give different answers**. In the lecture you ask the same question in two new chats:

```text
Suggest 5 names for automated tests that check a coupon code on a checkout page.
```

You typically get similar **kinds** of names, with different wording and order. For a tester, this has two big consequences:

- You cannot test an AI feature by running it once. You need several runs, and checks that judge whether each answer is acceptable, rather than comparing with one exact expected string. You will build exactly this kind of check on Friday.
- Two testers with the same prompt can get different test cases. Review the output, not the prompt alone.

Even temperature 0 does not guarantee identical output every time with hosted models. Small differences in how the computation runs can still change a token, and one changed token changes everything after it. Treat "repeatable" as "mostly repeatable".

### 8. Limitations You Must Understand

| Limitation | What it means | Why it happens | Testing example |
|---|---|---|---|
| **Hallucination** | Confident, fluent, wrong content | It predicts likely text and never checks facts | Invents a pytest function or a package that does not exist |
| **Knowledge cut-off** | It only knows its training data, up to a date | Training stops at some point | Suggests an outdated Selenium method |
| **Non-determinism** | Different answers to the same prompt | Sampling | Two runs produce different test cases |
| **No reliable self-check** | It cannot tell you reliably when it is wrong | Confidence is a style of text, not a measurement | "This rule is 100% correct" when it is not |
| **Weak exact arithmetic** | Slips on long or tricky sums | It predicts digits as text rather than calculating | A wrong total in a test's expected result |
| **Security and privacy risks** | Leaking pasted secrets; obeying instructions hidden in input | It treats all text in its window as possible instructions | A log pasted into a prompt contains a password |

The last row is a topic of its own, covered on Wednesday in *Responsible Use of AI in QE*.

#### 8.1 Catching a hallucination

In the lecture you try this **hallucination probe**:

```text
Explain what the pytest function pytest.assert_coupon_valid() does and show an example.
```

The function **does not exist**. A good answer says so, and suggests a plain `assert` or a helper function you write yourself. A poor answer confidently explains its parameters and shows example code, all invented.

Why would a model invent it? Because the request is shaped like countless real questions about real pytest functions, and the most likely continuation of "Explain what pytest.X does" is an explanation. Nothing in the generation loop checks whether X is real.

How to check whether a function, method or package is real:

- **Search the official documentation**, for example docs.pytest.org or playwright.dev.
- **Run the code.** A made-up function fails immediately with an error such as `AttributeError`.
- **For packages, check the official registry**, such as pypi.org, before installing, and look at who publishes the package and how widely it is used.
- **Do not just ask the same AI "are you sure?"** It may simply produce a confident "yes".

### 9. Key Terms You Will Hear This Week (Recognition Only)

You will meet these properly later this week. For now, just recognise the names:

- **Prompt engineering:** writing prompts that get reliable results (Tuesday).
- **Zero-shot and few-shot prompting:** asking with no examples, or with a few examples (Tuesday).
- **Retrieval-augmented generation (RAG):** giving the model relevant documents to read before it answers.
- **Fine-tuning:** further training a model on your own examples.
- **AI agent:** a system that uses a model, instructions and checks to do a job step by step (Thursday and Friday).

---

## Practice Exercises

1. **Count like the model (paper, 10 min).** Using the six Gherkin lines, list every word that follows "user", and how many times. If the tiny model has just written "the user", what are the probabilities of each possible next word? Which generated sentences starting "given the user" are real, and which are invented?

   *Hint:* "user" is followed by four different words.

2. **Choose the temperature (paper, 5 min).** For each task, choose low or moderate temperature and give a one-line reason: (a) generating 20 test usernames that must be identical every run; (b) brainstorming unusual ways a user might break the checkout; (c) converting a test case into a fixed JSON format.

3. **Probe for hallucinations (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** in a new chat, ask: *"Which Python package should I install to compare two screenshots in a pytest test? Give the exact pip install command."*
   - **Review:** note each package name it suggests.
   - **Run:** look up each name on pypi.org. Does it exist? Who publishes it? When was it last updated? Then, in a separate new chat, ask: *"Explain what the Playwright method page.wait_for_coupon() does."*, and check playwright.dev.
   - **Record:** for each answer, write "real", "invented" or "real but not what it claimed", and one sentence on how you checked.

4. **Context window (paper, 5 min).** A tester pastes a 6,000-line log into a chat, then asks, "Why did the checkout test fail?" The answer ignores the error near the top of the log. Give two possible reasons, using sections 4 and 6, and two things the tester could do differently.

---

## Knowledge Check

1. In one sentence, what does an LLM do when it generates text?

<details><summary>Answer</summary>

It repeatedly predicts a probability for every possible next token, picks one, adds it to the text, and repeats.

</details>

2. What is a token, and roughly how many words is 100 tokens of English?

<details><summary>Answer</summary>

A chunk of text: a word, part of a word or a punctuation mark. As a rough guide, 100 tokens is about 75 English words.

</details>

3. Why did `tiny_llm.py` produce "when the user sees the cart page", a sentence that was never in its training data?

<details><summary>Answer</summary>

It only checks that each next word is likely after the previous one. Every word pair was seen in training, but the whole sentence was not. That is a tiny hallucination.

</details>

4. What does lowering the temperature do?

<details><summary>Answer</summary>

It sharpens the probabilities, so the most likely token is chosen almost every time. Output becomes more predictable and less varied.

</details>

5. A long chat starts ignoring a rule you gave in your first message. What is the likely cause?

<details><summary>Answer</summary>

The early message may have dropped out of the context window, or be getting little attention among a lot of text. Restate the rule, or start a new chat.

</details>

6. An AI explains a pytest function confidently. How do you check it is real?

<details><summary>Answer</summary>

Look it up in the official documentation (docs.pytest.org) or run code that uses it. Do not rely on asking the same AI whether it is sure.

</details>

---

## Glossary

- **Generative AI (GenAI):** AI that creates new content, such as text, code or images.
- **Prompt:** the input you give a generative model, in plain language.
- **Foundation model:** a very large model trained on broad data and usable for many tasks.
- **Large Language Model (LLM):** a foundation model specialised in language and code.
- **Open-weight model:** a model whose trained weights can be downloaded and run locally.
- **Multimodal:** able to take in or produce more than one kind of content, such as text and images.
- **Token:** a chunk of text an LLM reads and writes; about three-quarters of an English word on average.
- **Next-token prediction:** predicting the probability of each possible next token.
- **Sampling:** choosing the next token at random, weighted by the probabilities.
- **Transformer:** the network design behind today's LLMs (2017).
- **Attention:** how a Transformer decides which earlier tokens matter for the current one.
- **Pre-training:** the first stage of training, learning to predict the next token from huge amounts of text.
- **Instruction tuning:** further training on requests paired with good answers.
- **RLHF:** reinforcement learning from human feedback; training a model towards answers people rated well.
- **Context window:** the maximum number of tokens the model can take into account at once.
- **Temperature:** a setting that controls randomness; low is predictable, high is varied.
- **Top-p:** a setting that limits sampling to the most likely tokens that together reach probability *p*.
- **Max tokens:** a setting that caps the length of the reply.
- **Hallucination:** confident but false output.
- **Knowledge cut-off:** the date after which the model has no training data.
- **Non-determinism:** giving different outputs for the same input.

---

## Summary

- **GenAI creates content; predictive ML picks a label.** LLMs are huge neural networks trained on text and code.
- **An LLM repeatedly predicts the next token** and samples one. Nothing in that loop looks facts up or checks truth.
- **Fluent does not mean correct.** Hallucinations come from the same mechanism as correct answers: likely text.
- **The context window is short-term memory**, counted in tokens; long chats and huge pastes can push things out of view.
- **Temperature controls randomness**, and sampling means the same prompt can give different answers, so test AI output over several runs.
- **Check every fact, function and package** against official documentation or by running the code.

---

## Additional Resources

- OpenAI Help Center, *Understanding and counting tokens*: https://help.openai.com/en/articles/4936856
- Google for Developers, *Machine Learning Crash Course: Large language models*: https://developers.google.com/machine-learning/crash-course/llm
- Spracklen et al., *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs*: https://arxiv.org/abs/2406.10279
