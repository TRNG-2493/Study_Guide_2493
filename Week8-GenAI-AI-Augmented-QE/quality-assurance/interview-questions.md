# Interview Questions: Week 8 - Generative AI & AI-Augmented Quality Engineering

Self-quiz bank for technical interviews. Say your answer out loud first, check that you used the keywords, then click **Click to Reveal Answer**. Each day has 18 questions (13 beginner, 4 intermediate, 1 advanced) based strictly on that day's written lessons.

---

# Day 1 - Monday: AI & Generative AI Fundamentals

## Beginner (Foundational)

### Q1: How do Artificial Intelligence, Machine Learning, Deep Learning and Generative AI relate to each other?
**Keywords:** nested, subset, rule-based, neural networks, Generative AI
**Hint:** Picture circles inside circles.
<details>
<summary>Click to Reveal Answer</summary>

They are nested subsets: AI ⊃ ML ⊃ DL ⊃ Generative AI. **AI** is the broad field of making machines perform tasks associated with human intelligence; it is defined by intelligent behaviour, not technique, so rule-based (symbolic) systems count as AI. **Machine Learning** is the part of AI where systems learn patterns from data instead of following hand-written rules. **Deep Learning** is the part of ML that uses neural networks with many layers. **Generative AI** sits inside deep learning and creates new content (text, code, images) that resembles its training data.
</details>

---

### Q2: What is the key difference between traditional programming and machine learning?
**Keywords:** rules, data, answers, model, learns
<details>
<summary>Click to Reveal Answer</summary>

In traditional programming a human writes the rules, and the program applies them to data to produce answers. In machine learning you give the algorithm **data and the correct answers** (examples of inputs and outputs), and it learns the rules itself. The learned rules are the **model**, which is then used for inference on new data.
</details>

---

### Q3: Define feature, label, parameter and hyperparameter.
**Keywords:** input property, correct answer, learned, chosen before training, max_depth
<details>
<summary>Click to Reveal Answer</summary>

A **feature** is a measurable input property used by a model (for example, the number of lines changed in a commit). A **label** is the known correct answer for a training example (for example, "flaky" or "genuine failure"). **Parameters** are learned by the model during training, such as neural network weights. **Hyperparameters** are chosen by a human before training, such as a decision tree's `max_depth`.
</details>

---

### Q4: Why must the test set be kept separate from the training set? What are overfitting and underfitting?
**Keywords:** unseen data, honest estimate, overfitting, underfitting, generalise
**Hint:** Think of it as a final exam the model has never seen.
<details>
<summary>Click to Reveal Answer</summary>

The test set gives an **honest estimate of performance on unseen data**. If you evaluate on the data the model trained on, you hide overfitting; it is the ML equivalent of a test that can never fail. **Overfitting** means the model learned the training data too closely (including its noise) and does not generalise; **underfitting** means it learned too loosely and misses real patterns in both training and new data. Testers should also watch for **drift**, the gradual loss of accuracy as real-world data changes.
</details>

---

### Q5: What single question distinguishes supervised from unsupervised learning? Give a QE example of each.
**Keywords:** labels, classification, regression, clustering, anomaly detection
<details>
<summary>Click to Reveal Answer</summary>

"**Do we have labels** (known correct answers) for the training data?" Supervised learning learns from labelled examples to predict answers: **classification** predicts a category (flaky vs. genuine failure, risky build vs. safe) and **regression** predicts a number (suite duration in minutes). Unsupervised learning finds structure in unlabelled data: **clustering** groups similar failure messages, **dimensionality reduction** (PCA) compresses many metrics into fewer, and **anomaly detection** finds unusual response times. With unsupervised results, a human must interpret what each group means. LLMs are pre-trained with a third family, **self-supervised** learning, where the labels come from the data itself (the next word).
</details>

---

### Q6: Define precision, recall and F1. Why is accuracy a poor metric when only 2% of builds fail?
**Keywords:** confusion matrix, precision, recall, harmonic mean, imbalanced
<details>
<summary>Click to Reveal Answer</summary>

From the confusion matrix: **precision** is, of everything the model flagged as positive, the fraction that truly was positive (how trustworthy the alarms are). **Recall** is, of all real positives, the fraction the model found (how many problems it catches). **F1** is the harmonic mean of the two, high only when both are high. With 2% failing builds, a model that always predicts "pass" scores 98% accuracy while catching **no** failures. Precision and recall on the failure class reveal this; accuracy alone hides it on imbalanced data.
</details>

---

### Q7: What three steps does an artificial neuron perform, and why does a network need non-linear activation functions?
**Keywords:** weights, sum, bias, activation function, XOR
<details>
<summary>Click to Reveal Answer</summary>

A neuron (1) multiplies each input by its **weight**, (2) sums the results and adds a **bias**, then (3) applies an **activation function** such as ReLU or sigmoid. Activations must be non-linear because without them stacked layers collapse into a single linear function, so depth adds nothing and the network cannot model complex patterns. The classic example is **XOR**, which a single neuron cannot learn but a small network with a hidden layer and non-linear activation can.
</details>

---

### Q8: How does a neural network learn? Explain loss, gradient descent, learning rate and backpropagation.
**Keywords:** loss function, gradient descent, learning rate, backpropagation, epoch
<details>
<summary>Click to Reveal Answer</summary>

A **forward pass** produces a prediction, and a **loss function** measures how wrong it is. **Backpropagation** works backwards from the output error, using the chain rule, to calculate how much each weight contributed (its gradient). **Gradient descent** then adjusts every weight a small step in the direction that reduces the loss. The **learning rate** sets the step size: too small is slow, too large overshoots. This repeats over **batches** (subsets of examples per update) and **epochs** (full passes over the training data).
</details>

---

### Q9: Describe the classic NLP preprocessing steps. What is the difference between stemming and lemmatisation?
**Keywords:** tokenisation, normalisation, stop words, stemming, lemmatisation
<details>
<summary>Click to Reveal Answer</summary>

A classic pipeline **tokenises** text (splits it into units; not as simple as splitting on spaces because of contractions, punctuation, code, URLs and numbers), **normalises** it (for example lowercasing, replacing numbers or timestamps with placeholders), **removes stop words** (very common words), and reduces words to a base form. **Stemming** chops endings using crude rules and may produce non-words; **lemmatisation** uses vocabulary and grammar to find the true dictionary form ("ran" → "run"). After that, the text is converted to numbers.
</details>

---

### Q10: What do TF-IDF and cosine similarity do, and why can they miss a duplicate bug written in different words?
**Keywords:** TF-IDF, distinctive words, cosine similarity, synonyms, embeddings
<details>
<summary>Click to Reveal Answer</summary>

**TF-IDF** weights words that are frequent in one document but rare across the collection, so distinctive words stand out and common words are down-weighted. **Cosine similarity** compares the direction of two such vectors, which enables tools like duplicate bug detection. But TF-IDF matches **exact words, not meanings**: "Cannot sign in" and "Login fails" share no words, so they look unrelated. **Embeddings** represent meaning as dense vectors, and **contextual embeddings** even change with the surrounding sentence, so **semantic search** finds duplicates written with different words.
</details>

---

### Q11: In one sentence, how does an LLM generate text? What is a token, and how does a raw model become an assistant?
**Keywords:** next-token prediction, autoregressive, token, pre-training, RLHF
<details>
<summary>Click to Reveal Answer</summary>

An LLM repeatedly predicts a probability distribution over the **next token** given all previous tokens, samples one, appends it and repeats (**autoregressive** generation). A **token** is a chunk of text (a whole word, word piece or symbol); models read and write tokens, so context limits and costs are counted in tokens. A raw model becomes an assistant in three stages: **pre-training** (self-supervised next-token prediction on huge text), **fine-tuning / instruction tuning** on curated examples, and **alignment** such as RLHF (reinforcement learning from human feedback). Pre-training also explains the **knowledge cut-off**.
</details>

---

### Q12: What do temperature, top-p and max tokens control? Is temperature 0 fully deterministic?
**Keywords:** temperature, top-p, sharper distribution, max tokens, non-deterministic
<details>
<summary>Click to Reveal Answer</summary>

**Temperature** reshapes the probability distribution: lowering it makes the distribution sharper, so output is more focused and repeatable; raising it makes output more varied. **Top-p** cuts off the unlikely tail, sampling only from the smallest set of tokens whose probabilities add up to p. **Max tokens** limits the output length (and can truncate it). Temperature 0 makes output much more repeatable but is **not guaranteed** to be identical between runs, so each run is still a sample.
</details>

---

### Q13: Why do LLMs hallucinate, and what other limitations must a quality engineer keep in mind?
**Keywords:** plausible, hallucination, knowledge cut-off, context window, draft to verify
<details>
<summary>Click to Reveal Answer</summary>

LLMs generate **statistically plausible continuations** rather than retrieving verified facts, and nothing in the basic generation loop checks truth, so they can produce fluent, confident output that is wrong or invented (**hallucination**). Other limitations follow from the same mechanism: **non-determinism** (sampled output), the **knowledge cut-off**, **missing context** (the context window is the model's only view of your situation), **bias** and **security risks**. The core rule for QE: **AI output is a draft to verify, not a fact to trust.**
</details>

---

## Intermediate (Application)

### Q14: Your team built a classifier that predicts risky builds. It reports 98% accuracy, but only 2% of builds fail and it caught almost none of them. How do you evaluate and tune it?
**Keywords:** accuracy trap, confusion matrix, recall, threshold, cost of false alarms
**Hint:** What happens if you lower the threshold from 0.5 to 0.3?
<details>
<summary>Click to Reveal Answer</summary>

98% accuracy is the **accuracy trap**: always predicting "pass" would score the same. Build the **confusion matrix** for the failure class and calculate **precision, recall and F1**. If recall is low, the model misses real risky builds. Then tune the **decision threshold**: lowering it (for example from 0.5 to 0.3) raises more alarms, so recall usually rises and precision usually falls. Choose the threshold based on the **cost of a missed problem versus a false alarm**. Also check the tester's usual concerns: the quality of the labels, behaviour on rare cases, **data leakage** (training features that would not be available at prediction time) and evaluation on a held-out test set.
</details>

---

### Q15: Your manager wants to "use GenAI" to group 5,000 nightly failure messages and to draft bug reports. How do you decide which tool fits each job?
**Keywords:** no AI, classic ML/NLP, GenAI, verifiability, risk if wrong
<details>
<summary>Click to Reveal Answer</summary>

First choose deliberately between **no AI, classic ML/NLP and GenAI**: deterministic problems need deterministic solutions. Clustering thousands of failure messages suits **classic NLP** (for example TF-IDF + k-means): it is fast, cheap, repeatable and runs locally at scale. Drafting bug-report wording suits **GenAI**, with a human reviewing it. Evaluate each use case on **value, frequency, verifiability, risk if wrong, data sensitivity and effort**. Verifiability matters most in QE: AI output can be wrong while looking right, so if a human cannot check it efficiently, the risk is high and the time saved disappears. Also remember the distinction: this is **AI for testing** (using AI to do QE work), not **testing of AI** (verifying AI-powered products).
</details>

---

### Q16: An AI assistant drafted pytest tests for `apply_coupon` (SAVE10 gives 10% off orders of $50.00 or more). They look professional. What kinds of mistakes do you look for before accepting them?
**Keywords:** contradicts requirement, invented requirement, unknown code, boundary, human review
<details>
<summary>Click to Reveal Answer</summary>

AI-generated tests can be wrong in ways that look right, so review each one against the requirement. Typical mistakes from the lesson's example: an **expected result that contradicts the requirement** (a small order receiving the discount); **wrong behaviour for unknown codes** (expecting the total to be returned instead of an error being raised); an **invented requirement** (asserting codes are case-insensitive when the requirement is silent); and **missing boundary tests** (no $49.99 / $50.00 checks). Human review is not optional, and your test design skills are what make the review effective.
</details>

---

### Q17: Your duplicate-bug detector uses TF-IDF and cosine similarity. It misses that "Cannot sign in" and "Login fails" describe the same issue. How would you improve it, and what still needs a human?
**Keywords:** exact words, synonyms, embeddings, semantic search, human confirms
<details>
<summary>Click to Reveal Answer</summary>

TF-IDF compares exact words, and these titles share none, so their similarity is near zero. Switch to (or add) **embeddings**, dense vectors learned from how words are used, which place texts with similar meaning close together even when the words differ; **semantic search** over those vectors finds the duplicate. Keep classic TF-IDF where exact-term matching is enough, because it is cheap and deterministic. A human still **confirms** suggested duplicates before closing reports, because similarity scores are probabilistic suggestions, not facts.
</details>

---

## Advanced (Deep Dive)

### Q18: Explain what happens inside an LLM between receiving "The login button is broken; please fix it" and producing its next word. Use attention and sampling, and connect the mechanism to why AI output must be verified in QE.
**Keywords:** tokens, self-attention, query/key/value, softmax, sampling
<details>
<summary>Click to Reveal Answer</summary>

The text is split into **tokens** (sub-word pieces built by methods such as BPE) and each becomes a vector. In each **Transformer** layer, **self-attention** lets every token weigh every other token: each token has a **query** (what it looks for), a **key** (what it offers for matching) and a **value** (what it passes on). Query-key dot products give relevance scores, **softmax** turns them into attention weights, and the weighted mix of values gives a context-aware representation, which is how "it" can attend to "button". At the end the model outputs a **probability distribution** over the next token. Settings shape the choice: **temperature** sharpens or flattens the distribution and **top-p** keeps only the smallest set of tokens whose probabilities reach p (with probabilities 0.5, 0.25, 0.15, 0.10 and top-p 0.8, the first three can be sampled). One token is **sampled**, appended, and the loop repeats.

Consequences for QE: nothing in this loop checks truth, so plausible but wrong text (hallucination) is natural; sampling makes outputs vary between runs; the model only knows its training data and the context window, so missing business rules are filled with typical content. Neural network outputs are **probabilistic, data-dependent and opaque**, so they must be verified by behaviour against an oracle, not trusted on confidence.
</details>

---

# Day 2 - Tuesday: Prompt Engineering for QE

## Beginner (Foundational)

### Q19: What is the difference between a prompt and prompt engineering, and why does the context window matter when you prompt about your own application?
**Keywords:** input, designing, testing, refining, context window
<details>
<summary>Click to Reveal Answer</summary>

A **prompt** is the input given to a GenAI model. **Prompt engineering** is the disciplined practice of designing, testing and refining prompts so the output is useful, accurate, consistent and in the required format. The model only knows what is inside its **context window** (plus its general training). Your application's business rules are not in its training, so if they are not in the prompt or conversation, the model will guess.
</details>

---

### Q20: Name the seven building blocks of a prompt.
**Keywords:** role, task, context, input data, constraints, output format, examples
<details>
<summary>Click to Reveal Answer</summary>

**Role/persona** (the perspective or expertise to adopt), **task/instruction** (what to do), **context** (background facts the model cannot know on its own), **input data** (the material to work on), **constraints** (rules or limits on the answer), **output format** (the exact shape of the answer) and **examples** (worked samples of the desired output). They work as a checklist when writing or reviewing a prompt.
</details>

---

### Q21: What belongs in the system, user and assistant messages of a chat API call, and why is the history resent each time?
**Keywords:** system message, user message, assistant message, stateless, history
<details>
<summary>Click to Reveal Answer</summary>

The **system** message holds standing instructions for the whole conversation: role, rules, tone, boundaries. The **user** message holds the specific request for this turn and its input data. **Assistant** messages are the model's previous replies. The model is **stateless** between calls; it remembers nothing, so the application keeps a conversation going by resending the whole history, including earlier assistant replies, on every call.
</details>

---

### Q22: Why does a vague prompt produce a generic answer? Name four dimensions of specificity.
**Keywords:** next-token prediction, average answer, scope, quantity, done-criteria
<details>
<summary>Click to Reveal Answer</summary>

The model predicts the most probable continuation of what it is given. With little detail, the most probable continuation is a blend of the many similar examples in its training data, an "average" answer that fits any coupon feature rather than yours. Specificity dimensions include: **task verb** ("design" test ideas), **scope** ("apply_coupon only, not payment"), **quantity** ("8 to 10"), **techniques** ("boundary value analysis"), **audience**, **format**, depth, tone, length and **done-criteria** ("49.99, 50.00 and 50.01 all covered").
</details>

---

### Q23: Why wrap pasted material in delimiters such as `<requirement>` tags, and where should key instructions go in a long prompt?
**Keywords:** delimiters, instructions vs data, lost in the middle, start, end
<details>
<summary>Click to Reveal Answer</summary>

Delimiters separate instructions from material, let you refer to blocks by name, make inputs easy to swap in code, and make instructions inside pasted text less likely to be followed. The **Lost in the Middle** research found that models use information near the **beginning or end** of a long input better than information in the middle. So put long reference material in clearly delimited blocks and place key instructions at the start, repeated at the end, never buried mid-prompt. More context is not always better: aim for high signal, low noise.
</details>

---

### Q24: Explain zero-shot, one-shot and few-shot prompting. When the model follows the examples, have its weights changed?
**Keywords:** shot, worked example, in-context learning, weights unchanged, fine-tuning
<details>
<summary>Click to Reveal Answer</summary>

A "shot" is a worked example (input plus desired output) placed in the prompt. **Zero-shot** has none, **one-shot** has one and **few-shot** has several, typically 2 to 5. Few-shot works through **in-context learning**: the examples exist only in the context window for that request and the model's weights do **not** change, so the examples must be sent with every request. That differs from supervised training or **fine-tuning**, which update the weights permanently. Examples show format, style, granularity, label values and decision boundaries far more efficiently than instructions can tell them.
</details>

---

### Q25: What biases and risks come with few-shot examples?
**Keywords:** majority-label bias, recency bias, over-copying, example leakage, diverse
<details>
<summary>Click to Reveal Answer</summary>

**Majority-label bias**: if most examples are labelled Major, answers drift towards Major. **Recency bias**: the last example has extra influence. **Over-copying (anchoring)**: the model copies incidental details, for example mentioning SAVE10 in gift-card tests because every example used it. **Example leakage**: the model returns an example's content instead of a new answer. Also watch for **outdated examples**. Fix them with representative, diverse, correct, consistently formatted and **label-balanced** examples, vary their order, state that examples show style only, and version-control them like test code.
</details>

---

### Q26: What are the two halves of format locking, and why is JSON usually preferred over CSV when output feeds Python code?
**Keywords:** request, enforce, types, nesting, json.loads
<details>
<summary>Click to Reveal Answer</summary>

Format locking means **requesting** the format in the prompt (and API settings) and **enforcing** it in code after the response arrives. Requesting only makes the right format likely; without enforcement, one malformed reply crashes or silently corrupts the pipeline. **JSON** carries types (numbers, strings, booleans, lists) and supports nesting, and Python's `json` module parses it directly into native objects. CSV values are all text, need manual conversion, have no nesting and break on commas inside values.
</details>

---

### Q27: What is the difference between syntax drift and structure drift? Which is more dangerous?
**Keywords:** code fences, trailing commas, missing keys, wrong types, parses successfully
<details>
<summary>Click to Reveal Answer</summary>

**Syntax drift** makes output fail to parse: code fences, chatty preamble, single quotes, trailing commas, truncation. **Structure drift** parses successfully but has missing, extra or renamed keys, wrong types (`"50"` instead of `50`) or values outside the allowed list. Structure drift is more dangerous because the JSON parses, so the problem surfaces later or not at all and may silently produce wrong tests. Always check keys, types and allowed values, not only "did it parse?"
</details>

---

### Q28: What do a provider's JSON mode and structured outputs guarantee, and what does neither guarantee?
**Keywords:** valid JSON, schema, content correctness, review
<details>
<summary>Click to Reveal Answer</summary>

**JSON mode** guarantees syntactically valid JSON. **Structured outputs** additionally constrain the response to match a supplied schema. **Neither guarantees the content is correct**, for example the right expected value. A locked format makes AI output usable and reviewable, not correct; content review is still required.
</details>

---

### Q29: Define sycophancy and the pink-elephant effect, and give a prompt change that reduces each.
**Keywords:** sycophancy, leading question, neutral, pink-elephant, positive instruction
<details>
<summary>Click to Reveal Answer</summary>

**Sycophancy** is the model's tendency to agree with the user or follow a wrong premise. Reduce it by asking neutrally ("Review this test against the rule below and list any problems") instead of "Confirm this is correct", and include the rule to check against. The **pink-elephant effect** means mentioning something in a "don't" instruction makes it more likely: "Don't use `time.sleep`" puts those tokens in context and gives no alternative. State the positive instruction instead: "Wait for elements using WebDriverWait with expected_conditions."
</details>

---

### Q30: In AI-assisted test design, why must the tester own the expected results, and what does "mark unspecified behaviour as ASK PO" prevent?
**Keywords:** test oracle, plausible text, requirement, invented requirements, product owner
<details>
<summary>Click to Reveal Answer</summary>

An LLM predicts plausible text; it does not check facts against the requirement, so it is **not a test oracle**. Expected results must come from the requirement, specification or product owner, and the tester is accountable for them. Use AI as a thinking partner that widens the funnel with ideas while you narrow it with correct expected results. "Mark unspecified behaviour as ASK PO" stops the model from **inventing requirements** (silently filling gaps with plausible assumptions) and turns those gaps into visible questions for the product owner.
</details>

---

### Q31: What five things should a good AI debugging request contain, and why ask for "ranked hypotheses with a way to confirm each" rather than "fix it"?
**Keywords:** full error output, minimal code, expected vs actual, what you tried, ranked hypotheses
<details>
<summary>Click to Reveal Answer</summary>

Include: the **full error output** copied exactly; the **minimal relevant code**; **expected versus actual** behaviour tied to the requirement; **what you already tried**; and **what kind of answer** you want (causes and confirmations before a fix). "Fix it" invites any change that makes the test pass, often weakening the test and hiding the bug. Ranked hypotheses keep the focus on the root cause, and confirmation steps mean **evidence**, not the model's confidence, decides.
</details>

---

## Intermediate (Application)

### Q32: You ask an AI for boundary tests for "SAVE10 gives 10% off a subtotal of $50.00 or more" and for a decision table with four binary conditions. It returns 49, 50, 51 and a 12-rule table. What is wrong and how do you check AI test designs?
**Keywords:** precision, 49.99, 50.00, 50.01, 2ⁿ rules
**Hint:** Money is measured in cents.
<details>
<summary>Click to Reveal Answer</summary>

With cent precision, 3-value BVA needs **49.99, 50.00 and 50.01**. Whole-dollar values cannot distinguish `>= 50` from, say, `> 49.5`, and never test the closest values on either side. A decision table with four binary conditions has **2⁴ = 16 rules**, so 12 means rules were skipped. Use **technique-driven prompts**: name the technique, state the precision, ask for the analysis (partitions or boundaries) first, then the tests. Then check with small independent Python checks: compute BVA values yourself, generate every combination with `itertools.product` and compare, and verify that every pair appears in a pairwise set (balanced value counts do not guarantee pair coverage).
</details>

---

### Q33: An AI assistant "fixed" a failing build by changing `assert total == 45.00` to `assert total in (45.00, 50.00)`. The build is green. What happened and what do you do? How can you prove a test can still catch bugs?
**Keywords:** weakened assertion, reject, root cause, mutation testing, survived
<details>
<summary>Click to Reveal Answer</summary>

The test was **weakened**: it now accepts the buggy result, so it can no longer detect the bug it was written for. Reject the change, find and fix the real cause (in the code, or in your understanding of the requirement) and keep the strict assertion. Read the diff of every AI change. To prove a test can fail, run a quick **mutation check**: deliberately introduce a small bug (a mutant) and confirm a test fails. A mutant that **survives** reveals a gap. The lesson's script uses `try/finally` so the original source file is always restored.
</details>

---

### Q34: A prompt that generates expected totals for ten coupon test cases gave the right answer the one time you ran it. Why is that weak evidence, and how would you make the process trustworthy?
**Keywords:** sampled, run several times, refinement loop, let code calculate, deterministic check
<details>
<summary>Click to Reveal Answer</summary>

Output is sampled, so a wrong answer with, say, a 20% probability will often not appear in a single run. **Run important prompts several times** and compare. Debug prompts with the loop **symptom → root cause → fix → re-run**, changing one thing at a time and keeping old versions (the same draft → run → evaluate → refine loop as a test cycle). Models work on tokens and make plausible arithmetic and counting slips, so ask the AI for interesting **inputs** (boundaries, edge cases) and calculate expected values yourself in code. Code catches counts, arithmetic, existence of functions and format; human judgement catches vagueness, sycophancy and invented requirements.
</details>

---

### Q35: You are writing the parser for a format-locked prompt. What should it tolerate, what should it reject, and how should it handle a bad reply?
**Keywords:** strip fences, json.loads, try/except, check structure, re-ask once
<details>
<summary>Click to Reveal Answer</summary>

Parse **defensively**: strip harmless wrapping such as code fences, extract the JSON block, call `json.loads` inside `try/except` (a `json.JSONDecodeError` gives `msg`, `lineno` and `colno`), then check the structure (keys, types, allowed values). Do **not** "repair" content, for example by replacing single quotes with double quotes: that changes the values themselves (apostrophes inside strings) and hides that the model ignored instructions. On failure, **re-ask once** with the exact error, then fail loudly, to avoid wasted tokens, infinite loops and hidden persistent failures.
</details>

---

## Advanced (Deep Dive)

### Q36: Design a reusable, versioned prompt-library entry that generates parametrized pytest cases for a business rule. Walk through the prompt structure and the checks around it, and explain why each part exists.
**Keywords:** persona, delimiters, few-shot, format lock, independent checks
<details>
<summary>Click to Reveal Answer</summary>

**Prompt structure.** A system message with a QA persona and standing rules; a user message with the task verb, scope and quantity; the requirement in delimiters (`<requirement>`); the tech stack and versions ("pytest, Python 3.x; Playwright for Python, sync API" when relevant, because versions change what correct code looks like); a named technique (EP/BVA with precision) and "analysis before tests"; a **do-not-invent rule with a way out** ("write ASK PO for unspecified behaviour"); 2-5 diverse, label-balanced **few-shot** examples from a different feature with "copy format, not content"; and a **locked JSON format** with exact fields, types and allowed values. Key instructions go at the start and are repeated at the end.

**Around the prompt.** Enforce the format in code (defensive parse, structure check, re-ask once). Run independent deterministic checks: case counts, BVA values, decision-table completeness, pairwise coverage, and expected values recomputed by human-written code from the requirement. Check that suggested APIs exist, remembering that `hasattr` can be fooled (`pytest.mark.parameterize` "exists" because marks are created dynamically), so running the tests is the real check. Run a mutation check to prove the tests can fail. Run the prompt several times before trusting it.

**As an artifact.** Store it in Git as a versioned prompt with acceptance criteria, a changelog and tests; never paste secrets or real customer data into it. The result is usable and reviewable; correctness still comes from your review against the requirement.
</details>

---

# Day 3 - Wednesday: AI-Augmented QA Lifecycle

## Beginner (Foundational)

### Q37: Name the STLC phases used this week and explain the assist, augment and autonomous levels of AI involvement. Which levels do most QA teams use?
**Keywords:** STLC, assist, augment, autonomous, human-in-the-loop
<details>
<summary>Click to Reveal Answer</summary>

The eight phases are: requirements analysis; test planning; test design; environment and data preparation; test implementation and execution; defect reporting and triage; reporting and closure; maintenance. At the **assist** level the AI suggests and the human does the work; at **augment** the AI drafts real artifacts and a human reviews and approves each one; at **autonomous** the AI produces and uses artifacts without per-item review. Most teams use assist and augment, with a **human in the loop**, because an LLM is not a test oracle, it is confidently wrong in the same style as when it is right, and accountability stays with people.
</details>

---

### Q38: Four unreviewed AI steps are each 90% correct. Roughly what fraction of final outputs is correct, and what does that tell you?
**Keywords:** error propagation, 0.9⁴, 66%, checkpoint, hand-over
<details>
<summary>Click to Reveal Answer</summary>

0.9 × 0.9 × 0.9 × 0.9 ≈ 0.656, about **two-thirds**. Errors made early are carried into and multiplied by later steps (**error propagation**). A human checkpoint at each hand-over is much cheaper than finding problems at the end. A copy-paste pipeline with no checkpoints is a lifecycle anti-pattern.
</details>

---

### Q39: Why is requirements analysis called shift-left testing, and what five defect categories did we use when reviewing stories?
**Keywords:** static testing, cheaper, ambiguous, incomplete, contradiction
<details>
<summary>Click to Reveal Answer</summary>

Requirements analysis is **static testing** of the test basis at the earliest point. Fixing a requirement means changing a sentence and having a conversation; fixing the same problem after it is built means changing design, code, tests and data, and possibly handling customer impact. The categories: **AMBIGUOUS** ("user-friendly"), **UNMEASURABLE** ("fast"), **INCOMPLETE** (no message for an empty required field; no behaviour for a second coupon), **CONTRADICTION** (criteria that conflict when read together) and **UNTESTABLE** (no observable outcome). Weak words and the INVEST checklist help spot problems.
</details>

---

### Q40: What is the "golden rule" for AI-assisted requirements analysis, and what does a grounding check catch?
**Keywords:** find problems, ask questions, never invent answers, quoted text, proposal
<details>
<summary>Click to Reveal Answer</summary>

The AI may **find problems and ask questions, but never answer them**; any proposed value must be labelled as a proposal and confirmed by the product owner. Otherwise invented values become part of the test basis and tests end up enforcing rules nobody agreed to. A **grounding check** verifies that text the AI claims to quote actually appears in the story, catching findings that paraphrase or invent requirement text (such as "must load in under 2 seconds").
</details>

---

### Q41: What is the difference between a test condition and a test case, and why is "Verify it works correctly" an unacceptable expected result?
**Keywords:** what to test, how to test, preconditions, observable, exact
<details>
<summary>Click to Reveal Answer</summary>

A **test condition** is *what* to test, a testable aspect of a requirement ("the $50.00 boundary"). A **test case** is *how*: a documented, repeatable set of ID, traced AC, preconditions, test data, steps and an **observable expected result**. "Verify it works correctly" is not observable or specific, so it can never fail and a tester cannot decide pass or fail from it. Expected results should name an exact total, message, page or state from the requirement, quoting messages exactly to avoid **message drift**.
</details>

---

### Q42: What are forward and backward traceability, and what is an orphan test condition?
**Keywords:** coverage gap, invented requirement, orphan, traceability matrix, product owner
<details>
<summary>Click to Reveal Answer</summary>

**Forward traceability** links each requirement to its tests and catches **coverage gaps** (an AC with no test). **Backward traceability** links each test to its requirement and catches **invented requirements** (a test traced to a non-existent AC5). A **traceability matrix** shows both. An **orphan** is a test condition or case that traces to no valid requirement; deal with it honestly by deleting it, turning it into a question for the product owner, or (if the PO agrees) adding a new acceptance criterion so it has a real parent. Note that 100% AC coverage still does not prove quality: coverage counts links, not correctness.
</details>

---

### Q43: Which jobs in test-data creation suit AI, and which suit code? Explain "one change at a time".
**Keywords:** ideas and variety, labels, the AI designs, code generates, checks prove
<details>
<summary>Click to Reveal Answer</summary>

AI is good at **ideas and variety** (unusual edge values such as non-ASCII digits) and weak at **labels, counts, hidden rules** (Luhn, dates, relationships), true randomness and volume, and it may reproduce real-looking data. The rule is: **the AI designs, code generates, checks prove**. Use seeded generators (Faker, `random.Random`) for volume and independent checks written from the requirement for validation. **One change at a time** means starting from a known-valid base row and changing exactly one field per row, so if a row is rejected only that field can be the reason.
</details>

---

### Q44: Why do seeds matter for generated test data, why never use AI-invented card numbers, and what is wrong with a hard-coded `locked_until` date?
**Keywords:** seed, reproducible, official test card numbers, referential integrity, relative to now
<details>
<summary>Click to Reveal Answer</summary>

A **seed** is the starting value of a pseudo-random generator; the same seed gives the same sequence, so you can regenerate exactly the row that failed overnight on CI. AI-invented card numbers might belong to a real person even if they pass the Luhn check; use the payment provider's **official test card numbers**, which only work in test mode (and `example.com` emails, 555-01xx phone numbers). A hard-coded `locked_until` is only "locked" on the day it was written and silently changes meaning later; write it relative to now (`now + timedelta(minutes=15)`, with `now` passed in). Also check **referential integrity**: an order's `user_id` must point to a user that exists.
</details>

---

### Q45: Explain fluency vs. correctness, automation bias and anchoring. Why should you review a story yourself before reading the AI's review?
**Keywords:** fluency, automation bias, commission, omission, anchoring
<details>
<summary>Click to Reveal Answer</summary>

**Fluency** is how well text reads; **correctness** is whether it matches the requirement and real behaviour. LLMs are very fluent, and humans treat fluent text as trustworthy. **Automation bias** is the tendency to favour an automated system's output and under-check it: an error of **commission** is acting on a wrong suggestion (copying an expected total of 44.99 for a $49.99 order); an error of **omission** is missing what was not flagged (no test for AC4). **Anchoring** means relying on the first information seen; once you read the AI's findings you think only within them. Reviewing first gives you independent expectations and a reference to judge what the AI missed. The goal is **calibrated trust**.
</details>

---

### Q46: List the nine-point human review checklist for AI-generated QA artifacts.
**Keywords:** correct, complete, grounded, traceable, safe
<details>
<summary>Click to Reveal Answer</summary>

C1 **Correct** (expected results match the oracle), C2 **Complete** (every AC including error paths and boundaries), C3 **Grounded** (no invented rules, fields or messages), C4 **Relevant** (matters for this story and its risk), C5 **Consistent** (terms, IDs, messages), C6 **Executable** (another tester could run it as written), C7 **Traceable** (points to a real AC ID), C8 **Safe** (no real personal data or secrets), C9 **Non-duplicated** (no near-copies). The same nine questions apply to requirements findings, test cases, test data and automation code.
</details>

---

### Q47: Why must you not use the application's actual output as the oracle when checking AI expected results? Who is accountable for an AI-generated test that lets a defect through?
**Keywords:** oracle, requirement, agrees with defects, accountable, approver
<details>
<summary>Click to Reveal Answer</summary>

A test whose expected result came from the code will agree with any defect in that code, so it cannot detect that the code is wrong. The oracle must come from the **requirement or its owner**, and an oracle function used to check AI output must be written by a human, independent of the AI that wrote the tests, or a shared misunderstanding will "agree with itself". Accountability lies with **the person who approved it** (and the team whose process accepted it); the AI is never the accountable party. "I missed the boundary when reviewing the AI's tests" is the accountable statement.
</details>

---

### Q48: Why should every prompt be treated as a data transfer, and how does data classification apply to a bug report?
**Keywords:** data transfer, stored, approved tools, restricted, most sensitive item
<details>
<summary>Click to Reveal Answer</summary>

Text you send leaves your machine and may be stored, logged, reviewed by vendor staff, processed by sub-processors or, in some products and settings, used for training. Unless a contract says otherwise, you have no control over it. Classify data (public, internal, confidential, restricted) and use only **approved tools** for each class; using unapproved tools is **shadow AI**. Classification follows the **most sensitive item** in the text: an internal bug report with one customer card number pasted in becomes **restricted**, and restricted data never goes to any AI tool.
</details>

---

### Q49: In redaction, what are false negatives and false positives, which should you prefer, and what do you do if a secret was pasted into a public chatbot?
**Keywords:** false negative, leak, over-redaction, allow-list, rotate
<details>
<summary>Click to Reveal Answer</summary>

A **false negative** is sensitive data the redactor misses (a leak); a **false positive** is harmless data redacted unnecessarily (the AI loses a little detail). Prefer false positives: over-redaction is a safe failure. Regex catches structured values like emails, cards and keys but misses names and addresses, so read the result. A pre-flight check should use an **allow-list** ("deny unless explicitly allowed"), so unknown tools are blocked by default. If a staging API key was pasted into a public chatbot, report it and **rotate** the key the same day (issue a new one, revoke the old), because you cannot know who has it.
</details>

---

## Intermediate (Application)

### Q50: An AI-drafted Playwright test `test_login` passes, but you discover it never actually logged in. It used `page.click("text=Log in")` and asserted `page.locator("h1").is_visible()`. Diagnose it and describe how you would fix and prove the test.
**Keywords:** heading matched, assertion cannot fail, get_by_role, web-first assertion, sabotage check
<details>
<summary>Click to Reveal Answer</summary>

Two reasons it passed: `click("text=Log in")` matched the `<h1>Log in</h1>` heading first and clicked it, so the form was never submitted; and an `h1` is visible on the login page as well as on My Account, so the assertion **cannot fail** on a login defect. Fix: give the AI the reviewed test case, a trimmed **DOM snippet** and your **team conventions**; use a user-facing locator such as `page.get_by_role("button", name="Log in")`, which is **strict** (errors on multiple matches); assert the exact expected outcome with a **web-first** `expect(...).to_have_text(...)` assertion, which retries, instead of reading `inner_text()` once. Then run a **sabotage check**: break the feature or expectation and confirm the test fails. "The test passes" is not evidence that it tests anything.
</details>

---

### Q51: The story does not say whether coupon codes are case-sensitive, and the AI wrote TC-05 expecting `save10` to work. A review script flags it as a MISMATCH. What do you do?
**Keywords:** grounded, invented requirement, retire ID, open question, product owner
<details>
<summary>Click to Reveal Answer</summary>

Checklist item **C3 (Grounded)** fails: it is an invented requirement. The script's MISMATCH is only one interpretation, because the requirement is silent; a human must recognise it as an **open question, not a simple correction**. Do not flip the test to the opposite assumption. Remove (retire) the test, log it in the correction log as INVENTED_REQUIREMENT, and send a question to the product owner. Retire the ID rather than renumbering the suite, because IDs appear in bug reports, run histories and automation code. Until the PO answers, there is no oracle and no trustworthy expected result.
</details>

---

### Q52: An AI produced 200 test cases for Project 2. You cannot review every item at the same depth. How do you decide review effort, and how do you know your reviews are working?
**Keywords:** impact, likelihood, reach, sampling with escalation, correction log
<details>
<summary>Click to Reveal Answer</summary>

Use **risk-based review depth** (LIGHT, STANDARD, FULL) scored on **impact** (how bad if wrong), **likelihood** the AI is wrong, and **reach** (how far the artifact travels; a shared fixture or CI-gating test affects many people). At volume, use **seeded random sampling with escalation**: review all high-risk items plus a random sample of the rest, and review everything if the sample's correction rate exceeds a threshold. Use small **review aids** (oracle comparison, traceability, duplicates, coverage) to point you at problems. Record every decision in a **correction log** and track acceptance, edit and rejection rates. A high acceptance rate only means something if reviews are real (checklist records, second reviewers for high risk, few escaped defects); otherwise it measures rubber-stamping. Only APPROVED items enter the suite.
</details>

---

### Q53: You ask an AI to write the end-of-cycle test summary. It reports "6 of 8 passed (75%)" but your run had 5 passed. How should AI-assisted reporting and defect drafting be set up?
**Keywords:** let code count, let AI write, check the numbers, UNKNOWN, human judges
<details>
<summary>Click to Reveal Answer</summary>

Apply **let code count, let AI write**: compute counts, totals and percentages in code (5 of 8, 62%), give those numbers to the model only to write the wording, then check that the numbers in the text match. For defect reports the pattern is **AI drafts, code checks the facts, human judges**: instruct "If a fact is missing, write UNKNOWN" so the model does not fill gaps with invented details, and run a check that catches missing fields and numbers not present in the notes. Code cannot judge whether the title is clear, the severity is right or the issue is really a defect; that remains human.
</details>

---

## Advanced (Deep Dive)

### Q54: Design an AI-augmented requirements-to-tests flow for Project 2 that is fast but safe. Where are the human checkpoints, the automated checks and the responsible-use controls, and why?
**Keywords:** human checkpoint, independent oracle, traceability, redaction, audit trail
<details>
<summary>Click to Reveal Answer</summary>

**Before any prompt:** classify the story and data, redact, and pass a pre-flight allow-list check for the tool; never send restricted data. **Requirements analysis:** review the story yourself first (avoid anchoring), run a weak-word linter, then an AI review with a JSON format lock and the golden rule; validate findings with shape, category, AC-reference and **grounding** checks. Checkpoint: the PO answers questions, criteria are rewritten as Given/When/Then with `<TO CONFIRM>` placeholders. **Test cases:** one story per prompt, traceability to one AC, exact messages and totals, `open_questions`, a case limit and a locked format; then field checks, a forward/backward **traceability matrix**, duplicate checks (Jaccard), and expected results compared with a **human-written oracle**; decide keep, fix, retire or add, and fill gaps with critique-and-extend. **Test data:** AI designs, seeded code generates, independent checks prove, a human checks realism and fairness (names with accents, apostrophes, hyphens). **Automation:** DOM snippet plus conventions, web-first assertions, AST linter for smells, a sabotage check. **Reporting:** let code count, let AI write.

Why: errors compound across hand-overs, so each stage gets a checkpoint; the oracle must be independent of the AI; and the cheapest automated checks run first so humans spend time on meaning. Keep an **audit trail** (AI suggestions vs. human overrides), an AI usage log, disclosure and a named owner per artifact; frameworks such as the NIST AI RMF (Govern, Map, Measure, Manage) and the risk-based EU AI Act explain why such evidence may be requested.
</details>

---

# Day 4 - Thursday: Agent Anatomy

## Beginner (Foundational)

### Q55: What is the difference between a chatbot and an AI agent, and what parts make up an agent's anatomy?
**Keywords:** instructions, contracts, validation gate, orchestration runtime, logs
<details>
<summary>Click to Reveal Answer</summary>

A **chatbot** is a conversation interface driven by a human turn by turn, with free-text answers. An **agent** is ordinary software that wraps a model with fixed instructions, agreed input/output contracts, an automatic check step and logs, so it can do a defined job repeatably. Its anatomy: **instructions** (system prompt), **prompt templates**, **input and output contracts**, a **validation gate**, optional **tools**, **context/memory**, an **orchestration runtime** and **logs**. The model provides language skill; the structure provides repeatability and safety.
</details>

---

### Q56: Describe the agent loop and the autonomy scale. Why do QA agents usually start at workflow level?
**Keywords:** perceive, reason, act, check, workflow
<details>
<summary>Click to Reveal Answer</summary>

The loop is **perceive → reason → act → check**; the **check** step is the one most often forgotten, and in QA it is non-negotiable. On the autonomy scale, an **assistant** lets the human decide, a **workflow** lets code decide the steps, and an **autonomous agent** lets the model decide. QA agents start as narrow **workflow-level** components because fixed paths are predictable and testable, errors compound across unchecked steps (0.9⁵ ≈ 0.59), and QA work aims to reduce uncertainty. One job, structured checkable output and a human approver make validation possible.
</details>

---

### Q57: What is the single-responsibility quick test for an agent, and why does TestCaseDesigner v1.0.0 have no tools?
**Keywords:** one sentence, without "and", tools, failure points, narrow
<details>
<summary>Click to Reveal Answer</summary>

Describe the agent's job in **one sentence without the word "and"**. "TestCaseDesigner turns one user story into test cases" passes. Single responsibility keeps contracts small and easy to validate, and agents with clear contracts can later be combined. TestCaseDesigner has no tools because its job (turning a story that is handed to it into test-case JSON) does not need any; every tool adds a way for things to go wrong, so an agent should get only the tools its job requires.
</details>

---

### Q58: Distinguish agent instructions, a one-off prompt and a prompt template. Why do instructions go in the system message?
**Keywords:** standing orders, system message, placeholders, rules not data, cached
<details>
<summary>Click to Reveal Answer</summary>

**Agent instructions** are fixed standing orders sent on every run, usually as the system message. A **one-off prompt** mixes task, rules and data for a single task. A **prompt template** is the reusable shape of the per-run message, with placeholders filled with each run's data. Instructions go in the system message because it separates **rules from data**, models are trained to give the system message strong weight across the conversation, per-run data stays clearly delimited, and an unchanging system block can often be cached.
</details>

---

### Q59: What nine questions should a complete agent instruction set answer, and which three lines are critical for a QA agent?
**Keywords:** role and goal, scope, escalation, grounding rule, output rule
<details>
<summary>Click to Reveal Answer</summary>

**Role and Goal, Scope, Inputs, Process, Rules, Output, Uncertainty and Escalation, Boundaries, Style.** For a QA agent the critical lines are the **grounding rule** (use only facts in the input, here the acceptance criteria), the **output rule** (one JSON object following a named contract) and the **escalation rule** (ask, don't guess: add a question to `open_questions` naming the AC). Write rules like requirements: positive, with reasons, free of contradictions (add tie-break rules), and testable.
</details>

---

### Q60: How are agent instructions and contracts versioned, and which kinds of change are breaking?
**Keywords:** semantic versioning, MAJOR, changelog, renaming, loosening an enum
<details>
<summary>Click to Reveal Answer</summary>

Use **semantic versioning** (`MAJOR.MINOR.PATCH`) with a **changelog** recording what changed and why, and store files in Git. A **MAJOR** change signals a breaking change: renaming or removing a field, adding a required output field, tightening rules, **loosening an output enum**, or changing a field's meaning. When the output gains a required field, the instructions go from 1.0.0 to 2.0.0 together with the output contract version, the header line and every sample pair; instruction and contract versions must stay aligned.
</details>

---

### Q61: What is an input/output contract for an agent, and why does an LLM-based agent need one more than an ordinary Python function?
**Keywords:** accepts, returns, preconditions, postconditions, drift
<details>
<summary>Click to Reveal Answer</summary>

An **IO contract** is a precise, written, ideally machine-checkable agreement on what the agent **accepts**, what it **returns**, and what it returns when it **cannot** do the job. In design-by-contract terms, **preconditions** are the caller's duty, while **postconditions** and **invariants** are the agent's duty, which tells you whose fault a failure is. An LLM agent needs it more because its output is generated, not computed: the shape can **drift** between runs or model versions, and it always produces plausible text instead of crashing. Without a contract, problems surface far downstream in consumers (like a `KeyError`) instead of at the boundary.
</details>

---

### Q62: What problem does the `status` + `open_questions` pattern solve?
**Keywords:** ok, needs_clarification, honest way out, guessing, fixed fields
<details>
<summary>Click to Reveal Answer</summary>

It gives the agent an honest, structured way to say "I can't design trustworthy tests for this" instead of guessing or inventing requirements. `status` is `ok` or `needs_clarification`, and `open_questions` lists what must be answered. Every consumer can handle every reply with the same fixed fields. For example, US-205 AC4 ("Only one coupon per order") does not say whether a second coupon is rejected or replaces the first, so the agent asks rather than writing a test, and that is correct behaviour, not a defect.
</details>

---

### Q63: What is JSON Schema? Explain schema vs. instance, `required` and `additionalProperties: false`.
**Keywords:** schema, instance, required, closed object, typos
<details>
<summary>Click to Reveal Answer</summary>

**JSON Schema** is a JSON vocabulary for describing and validating the shape of JSON data (`json.loads` only checks that text is well-formed). The **schema** is the rules; the **instance** is the data checked against them. Build object schemas in four steps: `type`, `properties`, `required`, `additionalProperties: false`. `properties` only constrains fields **if present**, so without `required` every field is optional and `{}` is valid. `additionalProperties: false` makes a **closed object** that rejects typos (`expected_reslt`), invented fields and unrequested commentary. This course uses draft 2020-12, declared with `$schema`.
</details>

---

### Q64: Three JSON Schema surprises: what does `default` do during validation, is `format` checked, and why does `{"oneOf": [{"type": "integer"}, {"type": "number"}]}` reject `5`?
**Keywords:** annotation, default never fills, format not checked, oneOf exactly one, anyOf
<details>
<summary>Click to Reveal Answer</summary>

`default` is an **annotation**: validation never fills in missing values, so your code must apply the default itself. `format` is also an annotation and is not checked unless you enable it. `5` is both an integer and a number, so it matches **two** branches, and `oneOf` requires **exactly one**; prefer `anyOf` unless you really mean "exactly one". Other annotations include `title`, `description` and `examples`.
</details>

---

### Q65: What is the difference between `validate()` and `iter_errors()`, and can the output schema check that every `ac_ids` entry exists in the input story?
**Keywords:** ValidationError, every error, path, one document, cross-document
<details>
<summary>Click to Reveal Answer</summary>

`validate()` raises a single `ValidationError` (or returns `None`); `iter_errors()` yields **every** error, each with a `path` (such as `test_cases/0/id`) and a `message`, so you can report everything at once. Use `Draft202012Validator.check_schema` to check the schema itself. A schema checks **one document on its own**, so it cannot see the input story; whether `AC5` really exists (rule R2) is a cross-document rule that needs code.
</details>

---

### Q66: Name the five categories of validation rule and say where each lives. When is a rule a warning rather than an error?
**Keywords:** structural, field-level, cross-field, cross-document, business/quality
<details>
<summary>Click to Reveal Answer</summary>

**Structural** and **field-level** rules live in JSON Schema; **cross-field (conditional)** rules can too, using `if`/`then` or `dependentRequired`. **Cross-document (semantic)** rules (R1-R5, such as "output `story_id` equals input `story_id`") need code that sees the input. **Business/quality** rules (Q1-Q3) need code warnings and human review. A rule is a **warning** when its automated check is a heuristic with false positives, such as Q2 "expected_result is concrete"; making it an error would block good output and teach people to bypass the gate. Keep all rules in a **rule catalogue** with ID, layer, severity, example violation and message.
</details>

---

### Q67: What does a complete sample input/output pair contain, what jobs can it do, and why don't we compare the agent's output to it word for word?
**Keywords:** expectations, MUST / MUST NOT / MAY, golden example, specification by example, contract test data
<details>
<summary>Click to Reveal Answer</summary>

A pair contains an **input**, a **reference expected output** and **expectations** (MUST / MUST NOT / MAY). It can do four jobs: **specification by example** (for humans), a **few-shot example** (for the model), **regression/golden data** (for later checks) and **contract test data** (valid and deliberately invalid samples). LLM output varies, so exact match is reserved for IDs, versions, counts and quoted text; everything else is judged with **property-based expectations** ("contains a case at $49.99"). Cover five categories: happy path, edge, clarification, invalid input and out of scope.
</details>

---

## Intermediate (Application)

### Q68: A teammate's template rendered with `str.format` crashes with `KeyError: '"status"'`. Another wants to use an f-string stored in a file. How do you advise them on rendering prompt templates?
**Keywords:** doubled braces, string.Template, substitute, safe_substitute, $$
<details>
<summary>Click to Reveal Answer</summary>

`str.format` treats every brace pair as a placeholder, so the JSON shape `{"status": "ok"}` looks like a variable named `"status"`. Fix it by doubling the literal braces (`{{ }}`) or switching to **`string.Template`**, where braces are plain text and placeholders are `$name`. An f-string is evaluated immediately where it is written, the `f` prefix cannot be stored in a text file, and it can run expressions, which you never want for text loaded from a file. Render with **`substitute()`**, which raises `KeyError` for a missing value, not `safe_substitute()`, which would send a literal `$max_cases` to the model. A literal dollar in the fixed text must be written `$$` (`$$50.00`), but values such as "$50.00" inside a story are inserted as plain text and never re-parsed. Test templates with pytest: the expected placeholder set, nothing left unfilled, loud failure on missing values.
</details>

---

### Q69: Three TestCaseDesigner replies arrive: one has `"status": "done"`, one has `"ac_ids": ["AC5"]` for a story with AC1-AC4, and one says "Total is $44.00" for a $50.00 subtotal with SAVE10. Which layer catches each?
**Keywords:** output schema, enum, R2, cross-document, human reviewer
<details>
<summary>Click to Reveal Answer</summary>

`"status": "done"` is caught by the **output schema** at the validation gate, because `status` is an `enum` of `ok` or `needs_clarification`. `"AC5"` matches the pattern `^AC[0-9]+$`, so it passes the schema; it is caught by code rule **R2** (every `ac_ids` entry exists in the input), which can see the input story. "Total is $44.00" is a valid string longer than five characters, so neither the schema nor the code rules catch it; the **human reviewer** must derive the correct total ($45.00) from AC1 (rule Q3). Shape is not meaning.
</details>

---

### Q70: A developer wants to add `"critical"` to the output `priority` enum and calls it "just a minor tweak". Is it? How would consumer-driven contracts help?
**Keywords:** breaking change, loosening an enum, consumers, consumer-driven contract, MAJOR
<details>
<summary>Click to Reveal Answer</summary>

For consumers it is a **breaking** change: an old consumer that maps only high/medium/low now receives a value it does not understand. Loosening an output enum is a classic "looks harmless" breaking change; it is safe as a minor change only if every consumer is confirmed to cope. With **consumer-driven contracts**, each consumer states the fields and values it needs and the contract is built from those needs. That justifies every required field and tells you exactly which consumers are affected by a change. Keep a consumer list, version the contract with SemVer, and update schema, instructions, templates and sample pairs in the same change.
</details>

---

### Q71: A first-draft instruction set says "If something is unclear, make reasonable assumptions" and "Return at most 6 test cases". What is wrong, and how would you rewrite it?
**Keywords:** invent requirements, escalation rule, open_questions, template placeholder, tie-break
<details>
<summary>Click to Reveal Answer</summary>

"Make reasonable assumptions" is the most dangerous line for a QA agent: it instructs the model to invent requirements silently, turning guesses into hidden expected results. Replace it with an **escalation rule**: add a question to `open_questions` naming the AC, with a "Reason:" clause so the model generalises and future editors know what breaks. "Return at most 6" depends on the per-call `max_cases`, so it belongs in the **template** as `Return at most $max_cases test cases.`; only things true on every call ("reply with JSON only") belong in instructions. Add a **tie-break rule** for conflicts: if `max_cases` is smaller than the number of ACs, cover high-priority criteria first and add one open question per uncovered criterion. A section checker scoring 9/9 is only a review aid; a human still reviews every line.
</details>

---

## Advanced (Deep Dive)

### Q72: You must design a new single-responsibility QA agent for Project 2 (for example, one that reviews a user story for defects). Walk through its full anatomy and explain how you would make its contract trustworthy before writing any model code.
**Keywords:** job sentence, contract in plain English, JSON Schema with if/then, rule catalogue, coverage matrix
<details>
<summary>Click to Reveal Answer</summary>

**Job:** one sentence without "and", workflow-level autonomy, no tools unless required, human approver. **Contract first, in plain English, then JSON Schema:** for every field state name, type, required/optional, allowed values, format, range and meaning, plus the clarification shape (`status` + `open_questions`) and a version. Decide required fields with four questions: who consumes it, can they work without it, is there a safe default, and can the agent honestly produce it (requiring what it cannot know invites invented filler). Require fields whose absence would be ambiguous (`open_questions: []`), prefer empty lists over `null`, and close objects with `additionalProperties: false`. Express conditional rules with `if`/`then` (status `ok` requires findings) or `dependentRequired`. **Rule catalogue:** cross-document rules (quoted text appears in the story, AC IDs exist) in code; quality heuristics as warnings; meaning for a human. Order the layers: input first (cheap), output schema, code rules, warnings, human review; collect all errors within a layer, but do not run deeper layers on broken shapes. Write error messages with rule ID, where, what, expected, actual and how to fix. **Instructions and template:** nine sections with grounding, output and escalation rules; a `string.Template` user message with a delimited story block. **Sample pairs:** human-written from the requirement (never AI-generated and lightly edited, which creates circular tests), covering happy path, edge, clarification, invalid input (`expected_output: null`, rejected before the model) and out of scope; check a **coverage matrix** for gaps and thin columns. Version everything together with SemVer and a changelog in Git.
</details>

---

# Day 5 - Friday: Building a First QA Agent

## Beginner (Foundational)

### Q73: What does it mean to write agent instructions at the "right altitude", and what four questions turn a draft rule into a good rule?
**Keywords:** right altitude, general principles, concrete example, trigger, checkable
<details>
<summary>Click to Reveal Answer</summary>

Right-altitude instructions state **general principles made concrete** with an example or measurable test ("for every numeric threshold, test at the threshold and just below it, e.g. $50.00 and $49.99"). Too-low instructions hard-code case-by-case logic for specific stories, which breaks on the next kind of story and grows contradictory; too-high instructions are vague wishes. The four questions: Can the model **find the trigger** in the input? Does the rule name a **concrete action or source**? Does it say **why**? Could a script or reviewer tell whether it was **followed**? Start from a **job card** (one job, consumer, inputs, outputs, done-criteria, out of scope) before writing any instruction text.
</details>

---

### Q74: What are a rule-to-check map and a desk-check, and what does it mean to "pin" the instructions?
**Keywords:** rule-to-check map, smell, desk-check, version header, agent.json
<details>
<summary>Click to Reveal Answer</summary>

A **rule-to-check map** links each instruction rule to the schema rule, code rule, quality rule or human check that verifies it; a rule with no check is only a hope and is a smell to resolve (for example by assigning the data-safety rule to human review). A **desk-check** walks sample inputs (P01-P05) through the draft by hand, pointing at the line that decides each behaviour, to find gaps and conflicts without running a model. Expect accepted gaps, things that are not the instructions' job (P04 malformed input is handled by the input gate), and real conflicts that need a team decision, not a silent edit. Release the file with a version header under a versioned name and **pin** that exact file in `agent.json` instead of "the latest".
</details>

---

### Q75: What is template drift, and how does a template library with partials and a manifest prevent it?
**Keywords:** drift, partial, manifest, value builder, strict render
<details>
<summary>Click to Reveal Answer</summary>

**Drift** happens when copies of the same prompt wording are edited independently until they disagree. A **template library** writes shared wording once as **partials** (reusable blocks such as the story block or format reminder, only included inside other templates) and refers to them with `name@version` includes. A **manifest** catalogues every template: name, version, kind (prompt or partial), file, declared variables, includes and description. **Value builders** keep formatting in code and wording in files. The library checks everything at load time and is **strict at render time**: missing values, unexpected values and unknown templates all raise errors.
</details>

---

### Q76: Why should `render()` reject an unexpected value, why is a rebuild that renders identical text a PATCH, and what is wrong with fixing a typo in a released template file?
**Keywords:** wrong version, identical text, PATCH, never edit released file, pin
<details>
<summary>Click to Reveal Answer</summary>

An unexpected value usually means the caller has a different template version in mind (a placeholder was renamed or removed); ignoring it would silently drop information from the prompt. If `tcd_user@1.0.1` renders exactly the same text as 1.0.0, the model receives the same prompt and behaviour cannot change, so it is a **PATCH**; a permanent test protects that equality. Editing a released file means one name and version now refers to two different prompts, so logs and run records mislead. Create a new version, register it, test it, and update the **pin** deliberately. Also: deprecate before deleting, assign owners and keep secrets out.
</details>

---

### Q77: Name the four enforcement points where TestCaseDesigner implements its IO contract, and what each protects.
**Keywords:** input gate, strict parse, output schema gate, typed objects, ContractError
<details>
<summary>Click to Reveal Answer</summary>

**(A) Input gate**: protects the model call and makes input errors the caller's responsibility. **(B) Parsing**: turns reply text into data and rejects anything that is not one JSON object. **(C) Output schema gate**: protects everything downstream from missing, unknown or badly typed fields. **(D) Typed objects** (`DesignResult`, `TestCase` dataclasses built only from validated output): give consumers named attributes guaranteed to exist. Every failure raises a `ContractError` with a **stage** (`input`, `parse`, `output`) and a list of `path: message` errors: a rejection with a reason, never a silent fix. Both schemas are checked at start-up, and paths are anchored to `ROOT` so they work from any working directory.
</details>

---

### Q78: Tuesday's defensive parser stripped Markdown fences. Why is Friday's `parse_reply` strict about them, and where are input defaults applied?
**Keywords:** contract forbids fences, measure, retry strategies, defaults once, caller wins
<details>
<summary>Click to Reveal Answer</summary>

The contract and instructions forbid fences, so accepting them would enforce a different contract from the written one; strictness also lets you **measure** how often the model breaks the format; and repairing or re-asking is a separate design decision (retry strategies, Week 9). Defaults are applied **once**, in `check_input`, with `{**INPUT_DEFAULTS, **story}`; the later dictionary wins, so the caller's `max_cases: 4` overrides the default 10. Applying defaults once means the template, the model and the validator all see the same `techniques` and `max_cases`.
</details>

---

### Q79: Describe the layers of TestCaseDesigner's output validation and the possible verdicts.
**Keywords:** parse, schema S1, fail fast, collect all, PASS_WITH_WARNINGS
<details>
<summary>Click to Reveal Answer</summary>

`validate_reply` takes the reply as a **string**, because parsing is part of validation. It runs **parse → output schema (S1)** with **fail fast**, because code rules cannot trust broken shapes, and records `stopped_at`. Then it runs the code rules **R1-R6** (errors) and quality checks **Q1-Q2** (warnings) with **collect all**. Q3 (does the expected result agree with its AC) goes to a **human**. The verdict is derived from severities: **FAIL** (reject and log), **PASS_WITH_WARNINGS** (review with the warnings first), **PASS** (still goes to review). If `stopped_at` is `"output"` and there are no R findings, R1-R6 never ran; they did not pass.
</details>

---

### Q80: A reply gets PASS. Can its test cases go straight into the Project 2 pytest suite? Why validate every reply even when using structured outputs?
**Keywords:** validation is not approval, untrusted input, OWASP LLM05, encoding, schema-valid but wrong
<details>
<summary>Click to Reveal Answer</summary>

No: **validation is not approval**. PASS only means no automated rule found a problem; a "$40.00 total" can pass every rule and be wrong, so the output still goes to human review. Validate every reply because models are non-deterministic, model output is **untrusted input** (OWASP LLM05), and structured-output features do not check everything: some keywords (`minLength`, `minimum`) may be unsupported, refusals or a `max_tokens` cut-off can still break the schema, and no such feature checks rules that compare output with input (R1-R6) or meaning (Q3). Validation can flag dangerous text (B1 warns on HTML markup), but **encoding** in the consuming code (such as `html.escape`) is what neutralises it.
</details>

---

### Q81: Explain the exit-code contract of `validate_output.py` and why results and diagnostics use different streams.
**Keywords:** 0, 1, 2, silent pass, stdout/stderr
<details>
<summary>Click to Reveal Answer</summary>

**0** = all replies valid; **1** = every reply was checked and at least one is bad (look at the agent's output); **2** = the check could not run (bad arguments, missing or broken files, nothing found), so nothing was judged and the setup must be fixed. A pipeline that cannot tell 1 from 2 sends people to debug the wrong thing, or treats "nothing checked" as success (a **silent pass**). Reports go to **stdout** and diagnostics ("cannot validate: ...") to **stderr**, so a user can redirect the report to a file while still seeing problems, and tests can check an unusable run produced no report. A broken *story* file is exit 2 because the reply cannot be judged fairly without its reference; a broken *reply* is a FAIL (exit 1) because that is exactly what the validator exists to report.
</details>

---

### Q82: Why does `main()` take an `argv` parameter and return an int, and how do you test that the validator catches the right defects?
**Keywords:** main(argv) -> int, sys.exit(main()), false-positive guard, planted defects, exact rule set
<details>
<summary>Click to Reveal Answer</summary>

`main(argv=None) -> int` lets tests call `main([...])` directly with any arguments and inspect the returned exit code without a subprocess; when run as a script, `sys.exit(main())` turns the value into the process exit code. Test the CLI with `capsys`, `tmp_path` and `pytest.raises(SystemExit)`. Test the validator with a **false-positive guard** (good output gives zero findings) and a parametrized table of **planted defects (mutants)**, asserting `fired == {rule}` rather than `rule in fired`, so a defect that triggers the right rule plus an unexpected one is caught. Keep each mutant minimal. Sort file pairings so report order is deterministic across machines.
</details>

---

### Q83: What are the steps of executing an agent against QA requirements, and why does the input gate run before the model call?
**Keywords:** prepare, gate, validate, record, triage
<details>
<summary>Click to Reveal Answer</summary>

Nine steps: select and prepare requirements; input gate; build messages; call the model; validate the reply; record; triage; human review; hand over to Project 2. The gate, message building, model call and validation live inside `TestCaseDesigner.run`; preparing and recording are in the runner; triage, review and hand-over are people and process. The gate runs first for **cost** (a doomed call wastes money and time), **quality** (broken input makes the model invent requirements) and **blame** (input problems belong to the caller, output problems to the agent). In the lesson, 6 stories cost 5 calls. A readiness checklist (IDs, testability, no secrets or personal data, approved tool, batch size, agent version) comes before any run.
</details>

---

### Q84: With temperature 0, are two runs guaranteed identical? What is a prompt fingerprint, and what does the run log record?
**Keywords:** temperature 0, sample, SHA-256, versions, JSON Lines
<details>
<summary>Click to Reveal Answer</summary>

No. Temperature 0 makes replies much more repeatable, but many providers still show small differences and the model behind a name can be updated; treat each run as a **sample**. A **prompt fingerprint** is a short SHA-256 hash of the exact messages sent: identical prompts give identical fingerprints. If two runs have the same version fields but different fingerprints, something in the exact text changed (the backlog story, or a file edited without a version bump); versions record what was meant to be sent, the fingerprint records what was sent. The runner writes versions, settings, fingerprint, errors and warnings to a **JSON Lines** log, and saves the gated input and raw reply as evidence for independent re-checking. The agent talks to models through a small `ModelClient` protocol (duck typing), with secrets taken from environment variables.
</details>

---

### Q85: What are the three different testing jobs around an agent, and why does one run prove little?
**Keywords:** test the validator, validate one output, test the agent, 0.75³, repeated runs
<details>
<summary>Click to Reveal Answer</summary>

**Testing the validator** checks that the checking code catches each planted defect (and nothing else). **Validating one output** decides whether a single reply is acceptable. **Testing the agent** measures how often, and in which ways, it produces acceptable output across many inputs and repeated runs. One run proves little: if the agent fails 25% of the time, a single run looks fine 75% of the time, and three runs in a row all look fine 0.75³ ≈ 42% of the time. An **evaluation suite** combines sample pairs, the full validator, property checks, many seeded runs and a scorecard; Q3 stays with humans.
</details>

---

## Intermediate (Application)

### Q86: You plant a defect by replacing `AC1` with `AC9` in one test case, and the validator reports two errors. A teammate calls it a validator bug. Is it? How do you read validation reports?
**Keywords:** R2, R3, one defect two consequences, shared cause, stopped_at
<details>
<summary>Click to Reveal Answer</summary>

It is not a bug. One defect has two true consequences: `AC9` does not exist in the story (**R2**) and AC1 is no longer covered by any test case or open question (**R3**). Read reports looking for **shared causes** rather than counting findings. Also read `stopped_at`: if validation stopped at the output schema, the absence of R findings means they never ran. Note that R3 searches for AC IDs with `\b` word boundaries so `AC1` is not "mentioned" by a question about `AC10`. For a planted-defect test that should fire exactly one rule, make the mutant minimal (for example, add an open question naming every AC so an "ok but empty" mutant fires only R6, not R3).
</details>

---

### Q87: In an execution run, US-412's reply is valid JSON matching the schema but FAILs R2 because TC-412-04 traces to AC4 (an invented case-insensitive search rule), and US-310 returns PASS with `needs_clarification`. What actions do you take?
**Keywords:** reject, no hand-patching, product owner, needs_clarification success, traceability matrix
<details>
<summary>Click to Reveal Answer</summary>

For **US-412**, reject the output and log it; do **not** hand-patch the reply and do **not** add the invented rule to the requirement. If the idea seems valuable, raise it with the product owner as a question. For **US-310**, PASS with `needs_clarification` is a **success**: the agent tested the clear ACs and asked about the vague one ("fast") instead of inventing a number, so the questions go to the product owner. Every outcome gets an **action and an owner**; passing output goes to human review; an agent never quietly rewrites a requirement. Build a **traceability matrix** from passing outputs, and keep stable IDs so the link carries into Project 2.
</details>

---

### Q88: Before evaluating TestCaseDesigner, you validate the sample pairs' reference answers and find P03 and P05 break R3. Why check the pairs first, and how do seeds make comparing v1.0.0 with v1.1.0 fair?
**Keywords:** oracle, test the test data, seeded, paired comparison, common random numbers
<details>
<summary>Click to Reveal Answer</summary>

The pairs are the **oracle**. If a reference answer breaks your own rules, the suite measures the agent against the wrong target; the bug can be in the test data, not the system under test. P03 and P05 were revised (revision 2, contract still 1.0.0). Seeding the simulated model with `f"{seed}-{story_id}"` makes results repeatable and gives a **paired comparison** (common random numbers): both versions receive exactly the same random draws, so differences in the scorecard come from the instruction change, not luck. With a real model you cannot control the randomness, which is one more reason to use enough runs. P04 (invalid input) runs only once, because the gate is deterministic; it passes only if the outcome is `rejected_input` and the model was never called.
</details>

---

### Q89: Error analysis shows failures from fenced JSON (S1), too many cases (R5), dropped AC coverage (R3/R6), invented AC IDs (R2) and vague results (Q2). Which do you fix with new instruction text, and which not?
**Keywords:** error analysis, targeted rules, one change at a time, validation gate, Week 9 retries
<details>
<summary>Click to Reveal Answer</summary>

Group failures by rule and root cause, then fix what the instructions can actually influence: dropped coverage, invented AC IDs and vague expected results were addressed in v1.1.0 with three **targeted, testable rules** (plus a team decision on the status question). Fenced JSON and over-limit output were **not** fixed with new text: the instructions already state those rules clearly, and repeating them rarely helps. Those formatting habits are handled by the pipeline: the **validation gate** rejects them now, and retry strategies (Week 9) will handle them later. Change one thing at a time, keep the old instruction file untouched so you can compare and roll back, bump the MINOR version, record evidence in the changelog and re-run the same suite.
</details>

---

## Advanced (Deep Dive)

### Q90: Walk through the full build-measure-refine cycle that took TestCaseDesigner from v1.0.0 to v1.1.0. How do you decide whether v1.1.0 is good enough to ship, and what remains a human responsibility?
**Keywords:** baseline, acceptance criteria, regressions, versioned config, human review
<details>
<summary>Click to Reveal Answer</summary>

**Build:** instructions at the right altitude with a rule-to-check map and desk-check; a template library with pinned versions; an implemented contract (input gate, strict parse, schema gate, typed objects); a validator (S1, R1-R6, Q1-Q2) wrapped in a CLI with an exit-code contract and tested with planted defects. **Measure:** validate the pairs first (the oracle), then run every pair many times with seeded runs and record a **baseline** scorecard; v1.0.0 scored **58%**, with main causes dropped AC coverage (R3/R6), invented AC IDs (R2) and vague results (Q2). **Refine:** error analysis, then a new instruction file (v1.1.0, MINOR) with three targeted rules, a changelog with evidence and a new config (`agent_v1.1.0.json`), leaving v1.0.0 untouched for rollback. **Re-measure** with the same suite and seeds: **85%, with no regressions**.

**Ship decision:** compare results with **pre-agreed, measurable acceptance criteria** for the agent, check for regressions, spot-check outputs, and document known issues (fenced JSON in about 1 run in 16 and occasional over-limit output, both rejected by the gate and planned for Week 9 retries). A typical decision: ship for internal use, with every output still passing through the validation gate and human sign-off.

**Human responsibility:** Q3, whether each expected result agrees with its acceptance criterion, which no code can judge; answering open questions (product owner); approving artifacts before they enter Project 2. Make the loop a habit: same suite, one change at a time, keep old versions, and turn real failures into new sample pairs.
</details>
