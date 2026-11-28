# Interview Questions: Week 8 - Generative AI & AI-Augmented Quality Engineering

Self-quiz bank: 100 questions, 20 per day, split 14 beginner (70%), 5 intermediate (25%) and 1 advanced (5%). Cover the answer, say yours out loud, then reveal it and check the **Keywords**. Every answer is based on this week's written lessons in `content/Week8-GenAI-AI-Augmented-QE/written/`.

---

## Day 1 (Monday): AI & Generative AI Fundamentals

### Beginner (Foundational)

#### Q1: [AI, ML & DL] How are AI, Machine Learning, Deep Learning and Generative AI related?
**Keywords:** AI ⊃ ML ⊃ DL ⊃ GenAI, rule-based, learns from data, neural networks, creates content
<details>
<summary>Click to Reveal Answer</summary>

They are nested: **AI ⊃ ML ⊃ DL ⊃ GenAI**.
- **AI** is making a computer do things we would call intelligent, such as deciding or predicting. A rule-based script (an expert system) is AI but not ML, because people wrote all the rules.
- **ML** is the part of AI where the computer learns rules from labelled examples.
- **Deep Learning** is the part of ML that uses neural networks with many layers.
- **Generative AI** is the part of DL that creates new content. LLMs are the engine inside GenAI chat tools.
</details>

---

#### Q2: [AI, ML & DL] Define feature, label, model and prediction.
**Keywords:** feature, label, correct answer, learned rule, new data
<details>
<summary>Click to Reveal Answer</summary>

- **Feature:** one piece of information about an example.
- **Label:** the correct answer for an example.
- **Model:** the rule that was learned from the training data.
- **Prediction:** using the model on new data.

Training data is the labelled examples used to learn the model; test data is kept back to check it.
</details>

---

#### Q3: [AI, ML & DL] What are overfitting and underfitting, and why must a model be tested on data it has never seen?
**Keywords:** too closely, too loosely, generalise, test data, "accuracy measured on what data?"
<details>
<summary>Click to Reveal Answer</summary>

**Overfitting** is fitting the training data too closely; **underfitting** is fitting it too loosely. Either way, the model does not work well on new data. A score on the training data only shows that the model memorised what it saw, so you always test on held-back data and ask: "accuracy measured on what data?"
</details>

---

#### Q4: [AI, ML & DL] What is model drift?
**Keywords:** slow loss of accuracy, real-world data changes, monitoring
<details>
<summary>Click to Reveal Answer</summary>

Drift is a model's slow loss of accuracy as real-world data changes away from the data it was trained on. A model that was good at release can quietly get worse, so its results need checking over time, not just once.
</details>

---

#### Q5: [Supervised vs Unsupervised] What is the difference between supervised and unsupervised learning?
**Keywords:** labels, predicts, discovers, clustering, "do we have labels?"
<details>
<summary>Click to Reveal Answer</summary>

The deciding question is **"Do we have labels?"**
- **Supervised learning** learns from examples that come with the correct answers (labels), and it **predicts**.
- **Unsupervised learning** finds structure in examples with no labels, and it **discovers** groups (clustering) and outliers (anomaly detection).
</details>

---

#### Q6: [Supervised vs Unsupervised] What is the difference between classification and regression?
**Keywords:** category, number, supervised
<details>
<summary>Click to Reveal Answer</summary>

Both are supervised learning. **Classification** predicts a category (such as "Critical" or "Low" severity). **Regression** predicts a number (such as how many hours a fix will take).
</details>

---

#### Q7: [Supervised vs Unsupervised] Explain precision and recall.
**Keywords:** of all warnings, of all real problems, false alarm, missed problem, cost
<details>
<summary>Click to Reveal Answer</summary>

- **Precision:** of all the warnings, the share that were right. Low precision means many false alarms (false positives).
- **Recall:** of all the real problems, the share that were caught. Low recall means many misses (false negatives).

Which matters more depends on the cost of a false alarm compared with the cost of a miss.
</details>

---

#### Q8: [Supervised vs Unsupervised] In clustering, who names the clusters, and why does scaling matter?
**Keywords:** algorithm finds groups, person names them, k-means, scaling, feature dominates
<details>
<summary>Click to Reveal Answer</summary>

The algorithm (such as k-means) finds the groups; **a person names them** and decides what they mean. **Scaling** puts features on comparable ranges so no single feature dominates. Without it, a feature with large numbers decides the groups, so scaling changes what the algorithm finds.
</details>

---

#### Q9: [Neural Networks] What does one artificial neuron compute, and what are its weights and bias for?
**Keywords:** inputs × weights, bias, z, activation function, importance, threshold
<details>
<summary>Click to Reveal Answer</summary>

A neuron multiplies each input by a weight, adds them up, adds a bias (this total is **z**) and passes z through an **activation function** (such as step, sigmoid or ReLU) to get its output. **Weights** set how much each input matters; the **bias** sets the threshold, making the neuron easier or harder to switch on. It is simple arithmetic you can work by hand.
</details>

---

#### Q10: [Neural Networks] How does a neural network learn?
**Keywords:** forward pass, loss, gradient descent, backpropagation, learning rate, epoch
<details>
<summary>Click to Reveal Answer</summary>

Compare with the label, measure the error, nudge the weights, repeat:
1. A **forward pass** runs inputs through the layers to get an output.
2. The **loss** measures how wrong the outputs are.
3. **Backpropagation** works backwards from the output error to find each weight's share of the blame.
4. **Gradient descent** adjusts the weights in the direction that reduces the loss fastest, in steps sized by the **learning rate**.

One pass through all the training examples is an **epoch**.
</details>

---

#### Q11: [NLP] What are tokenisation, stop words, stemming and lemmatisation?
**Keywords:** split into tokens, common words, rough root, dictionary form, "not"
<details>
<summary>Click to Reveal Answer</summary>

- **Tokenisation:** splitting text into tokens, such as words.
- **Stop words:** very common words ("the", "is") often removed before comparing texts.
- **Stemming:** cutting a word to a rough root ("coupons" → "coupon").
- **Lemmatisation:** reducing a word to its dictionary form ("applied" → "apply").

Cleaning removes trivial differences, but watch the traps: some stop words carry meaning, such as "not".
</details>

---

#### Q12: [NLP] What is the difference between word-based methods (bag of words, TF-IDF) and embeddings?
**Keywords:** word counts, word order ignored, rare words weighted, meaning, similar numbers
<details>
<summary>Click to Reveal Answer</summary>

**Bag of words** describes a document by its word counts and ignores word order. **TF-IDF** weights words that are frequent in one document but rare overall. Both are fast, cheap and explainable, but they cannot see meaning: different words with the same meaning score as unrelated. **Embeddings** are learned vectors in which similar meanings get similar numbers, which is what lets an AI link "voucher" to "coupon".
</details>

---

#### Q13: [GenAI Concepts] How does an LLM produce text, and why does that cause hallucinations?
**Keywords:** token, next-token prediction, sampling, likely text, nothing checks truth
<details>
<summary>Click to Reveal Answer</summary>

An LLM repeatedly predicts the probability of each possible next **token** (about three-quarters of an English word on average), **samples** one, adds it and repeats. Nothing in that loop looks facts up or checks truth. A **hallucination** (confident but false output) comes from the same mechanism as a correct answer: likely text. Fluent does not mean correct.
</details>

---

#### Q14: [GenAI Concepts] What are the context window and temperature?
**Keywords:** short-term memory, tokens, pushed out of view, randomness, low predictable, high varied
<details>
<summary>Click to Reveal Answer</summary>

The **context window** is the maximum number of tokens the model can take into account at once: its short-term memory. Long chats and huge pastes can push things out of view. **Temperature** controls randomness: low is predictable, high is varied. Related settings are **top-p** (sample only from the most likely tokens) and **max tokens** (cap the reply length).
</details>

---

### Intermediate (Application)

#### Q15: [Supervised vs Unsupervised] A bug-severity classifier scores 98% accuracy. Only 2% of bugs are Critical. Should you trust it?
**Hint:** What would a model that always says "not Critical" score?
**Keywords:** accuracy paradox, class imbalance, recall, precision, rare class
<details>
<summary>Click to Reveal Answer</summary>

Not yet. This is the **accuracy paradox**: with **class imbalance**, a model that never predicts Critical would also score 98% while missing every critical bug. I would ask for **precision and recall on the Critical class**. A missed critical bug is expensive, so recall matters most here. I would also ask what data the accuracy was measured on, and check for bad labels and data leakage.
</details>

---

#### Q16: [NLP] Your duplicate-bug detector uses TF-IDF. A report saying "discount voucher makes the basket price incorrect" scored 0.00 against the coupon bug it duplicates. How would you improve the process?
**Hint:** Different words, same meaning.
**Keywords:** blind spot is meaning, embeddings, narrow the field, threshold, precision and recall
<details>
<summary>Click to Reveal Answer</summary>

Word-based methods only match shared words, so "voucher" and "coupon" look unrelated; meaning is their blind spot. **Use both:** cheap word matching to narrow the field, then meaning-based judgement (embeddings, an AI or a person) to decide. The **threshold** for "possible duplicate" should be set with precision and recall in mind: too high misses duplicates, too low floods people with false alarms.
</details>

---

#### Q17: [GenAI in QE] An AI generated pytest tests for a free-shipping rule. Some fail. Does that prove the code is wrong?
**Hint:** Who wrote the expected values?
**Keywords:** contradicting, inventing, missing, boundaries, review against requirement, can fail
<details>
<summary>Click to Reveal Answer</summary>

No. **Failing tests do not prove the code is wrong, and passing tests do not prove it is right.** The AI may have made one of the three classic mistakes: **contradicting** the requirement, **inventing** a rule nobody asked for, or **missing** a case, especially a boundary such as $50.00 and $49.99. I would review every test against the requirement, check that it can fail, and only then decide whether the code or the test is wrong.
</details>

---

#### Q18: [GenAI in QE] When would you choose ordinary code, classic ML or GenAI for a QE task, and how do you pick a first use case?
**Hint:** Value, risk, checkability.
**Keywords:** exact rules, labelled history, messy language, use-case scoring, checkability, "AI drafts, a person decides"
<details>
<summary>Click to Reveal Answer</summary>

- **Exact rules** → ordinary code.
- **Labelled history** (such as past bugs with severities) → classic ML.
- **Messy language or drafting** → GenAI.

For a first GenAI use case, score ideas by **value, risk and checkability**, and start with ones that are valuable and easy to check. For risky ones, redesign as **"AI drafts, a person decides"**, so a person makes the final call and can trace the draft to its source.
</details>

---

#### Q19: [GenAI Concepts] You ran the same prompt twice and got different test cases. Is the tool broken?
**Hint:** Sampling.
**Keywords:** non-determinism, sampling, temperature, several runs, check facts
<details>
<summary>Click to Reveal Answer</summary>

No. LLMs **sample** the next token, so the same prompt can give different answers (**non-determinism**), more so at higher temperature. It means one run proves little: test AI output over several runs, and check every fact, function and package against official documentation or by running the code.
</details>

---

### Advanced (Deep Dive)

#### Q20: [Neural Networks] Why can a single neuron not learn XOR, and what does training a network teach a tester about regression?
**Hint:** Straight lines, and fixing one case.
**Keywords:** XOR, non-linear, hidden layer, ReLU, fixing one case changes others, regression suite
<details>
<summary>Click to Reveal Answer</summary>

XOR ("exactly one of two is true") is not a straight-line pattern, and a single neuron can only separate cases with a straight line, so it cannot learn it. Stacking neurons in layers with **non-linear** activations (such as ReLU) is what gives extra layers their power; without non-linearity, extra layers add nothing.

For testers: when training nudges weights to fix one example, **other examples can change too**. So after any change you re-check the full set of examples, exactly like a regression suite. And because networks are black boxes trained on data, you test their **behaviour** and ask what their training data covered.
</details>

---

## Day 2 (Tuesday): Prompt Engineering for QE

### Beginner (Foundational)

#### Q21: [Prompt Principles] What are the five parts of a strong prompt?
**Keywords:** role, task, context, constraints, output format
<details>
<summary>Click to Reveal Answer</summary>

**Role** (who the AI acts as), **task** (the job), **context** (the background material it must work from), **constraints** (rules for the answer, ideally checkable) and **output format** (the shape of the answer). Context usually helps most, because the model fills any missing context with invented content.
</details>

---

#### Q22: [Prompt Principles] What are system, user and assistant messages?
**Keywords:** standing instructions, particular request, earlier reply
<details>
<summary>Click to Reveal Answer</summary>

- **System message:** standing instructions for the whole conversation.
- **User message:** a particular request from the user.
- **Assistant message:** an earlier reply from the model.
</details>

---

#### Q23: [Prompt Principles] What makes a good constraint, and what is a "way out"?
**Keywords:** checkable, say what to do, "not specified", missing information, guessing
<details>
<summary>Click to Reveal Answer</summary>

A good constraint is **checkable**: you can confirm from the answer whether it was followed. Say what to do, not only what not to do. A **way out** tells the AI what to do when information is missing (ask a question, label an assumption, or write "NOT SPECIFIED") instead of guessing.
</details>

---

#### Q24: [Specificity & Context] What does "vague in, generic out" mean?
**Keywords:** gap filled with likely content, invented rules, scope, criteria, quantity, format
<details>
<summary>Click to Reveal Answer</summary>

Every gap in a prompt is filled with the most likely content, so a vague prompt gets a **generic answer** and invented rules. Be specific on every dimension: scope, task, criteria, quantity, format, audience and unknowns. Vague words like "good", "properly" or "some" are warning signs.
</details>

---

#### Q25: [Specificity & Context] How should you include requirements, code or error output in a prompt, and what must you never paste?
**Keywords:** paste the real thing, delimiters, `###`, placeholders, secrets, personal data
<details>
<summary>Click to Reveal Answer</summary>

Paste the **real** requirement, code or error, not a summary, and fence each item with **delimiters** such as `###` or `"""`. Paste what the task depends on and nothing else: too little means guessing, too much buries the key detail. **Never paste secrets or real personal data**; replace them with **placeholders** such as `<API_KEY>` that keep the shape of the evidence.
</details>

---

#### Q26: [Format Locking] What is format locking, and how do you lock a format?
**Keywords:** code will read it, container, fields and types, one example, exact count, forbid extra text
<details>
<summary>Click to Reveal Answer</summary>

Format locking fixes the exact shape of the AI's answer so code can read it. Use it whenever code will read the answer (a table for people, JSON for code, a fixed line for quick verdicts). Lock it by naming the container and every field with its type, showing one example, giving an exact count, and forbidding extra text.
</details>

---

#### Q27: [Format Locking] What is format drift, and what is defensive parsing?
**Keywords:** chatty wrapper, markdown fences, renamed fields, wrong counts, fail loudly
<details>
<summary>Click to Reveal Answer</summary>

**Format drift** is a reply moving away from the requested format: chatty wrappers, Markdown fences, renamed fields, wrong counts, wrong types. It is normal. **Defensive parsing** means reading a reply without assuming it is clean: extract what you need, parse it, check it, and **fail loudly** with a clear message when it is wrong.
</details>

---

#### Q28: [Format Locking] What is the difference between a shape check and a meaning check?
**Keywords:** types, counts, keys, values against the rule, perfect structure wrong value
<details>
<summary>Click to Reveal Answer</summary>

A **shape check** checks structure: types, counts and keys. A **meaning check** checks values against the rule. A reply can have perfect structure and a wrong value, so you need both.
</details>

---

#### Q29: [Few-Shot] What are zero-shot, one-shot and few-shot prompting, and what is in-context learning?
**Keywords:** no examples, one example, a few examples, follows the pattern, no retraining
<details>
<summary>Click to Reveal Answer</summary>

Zero-shot gives instructions only; one-shot gives one worked example (an input and its exact output); few-shot gives a few. **In-context learning** is the model following the pattern shown in the prompt **for that conversation only**, without retraining. Few-shot is best when format, labels or style are hard to put into words: it shows the answer instead of describing it.
</details>

---

#### Q30: [Few-Shot] What are majority-label bias and recency bias?
**Keywords:** most common label, last examples, balance, mix order
<details>
<summary>Click to Reveal Answer</summary>

**Majority-label bias** is leaning towards the label that appears most often in the examples. **Recency bias** is leaning towards the label of the last examples. To reduce both, balance the labels, mix the order, and test the prompt.
</details>

---

#### Q31: [Prompt Failure Modes] Name the common prompt failure modes and their shared root cause.
**Keywords:** hallucination, ignored instruction, wrong maths, outdated knowledge, inconsistency, predicts likely text
<details>
<summary>Click to Reveal Answer</summary>

**Hallucination**, **ignored instructions**, **wrong maths**, **outdated knowledge** (from the training cut-off) and **inconsistency** (different answers to the same prompt). They share one root: the model predicts likely text and does not check facts, count or calculate.
</details>

---

#### Q32: [Prompt Failure Modes] What is "lost in the middle", and how do you reduce it?
**Keywords:** long inputs, middle used less reliably, key rules last, paste only what matters
<details>
<summary>Click to Reveal Answer</summary>

It is the finding that models use information in the **middle** of long inputs less reliably. Reduce it by giving only the context the task needs, using exact numbers, and **putting the key rules last**.
</details>

---

#### Q33: [AI-Assisted Test Design] What are Equivalence Partitioning and Boundary Value Analysis, and why does "precision" matter?
**Keywords:** partitions, one value per group, edges, $0.01, 49.99
<details>
<summary>Click to Reveal Answer</summary>

**EP** divides inputs into groups the system should treat the same way and tests one value per group. **BVA** tests at and just around the edges of those partitions. **Precision** is the smallest step between values, such as $0.01 for money in cents; it decides what "just around" means (49.99 and 50.01 for a $50.00 rule, not 49 and 51).
</details>

---

#### Q34: [AI-Assisted Coding] What is the weakened-test trap?
**Keywords:** test changed, no longer checks requirement, green build, requirement decides
<details>
<summary>Click to Reveal Answer</summary>

An AI "fixes" a failing test by changing the test so it no longer checks what the requirement demands. The build goes green, but the bug is still there. A green build after changing a test is only correct if the **requirement** says the test was wrong.
</details>

---

### Intermediate (Application)

#### Q35: [AI-Assisted Coding] A test expects free shipping (0.00) at exactly $50.00, but the code returns 4.99. Write the outline of the debugging prompt you would send.
**Hint:** Six parts, plus one more thing.
**Keywords:** code, failing test, full error, expected vs actual, what you tried, what you want back, requirement
<details>
<summary>Click to Reveal Answer</summary>

The six parts: the **code** (`shipping.py`), the **failing test**, the **full error output**, **expected vs actual** ("Expected 0.00 at exactly $50.00. Actual: 4.99"), **what I already tried**, and **what I want back** (for example, the cause and a minimal fix with an explanation). Plus **the requirement**: without it, the AI cannot tell whether the code or the test is wrong. Before accepting a fix, I understand it, check it against the requirement, check what changed, prove the test can fail, and check every API exists.
</details>

---

#### Q36: [AI-Assisted Test Design] You asked an AI for boundary tests on "free shipping at $50 or more" and it gave 49, 50 and 51. What went wrong, and how do you prevent it?
**Hint:** Precision, and who works the technique first.
**Keywords:** technique-driven prompt, precision, 49.99, 50.01, work it yourself first, "not covered" list
<details>
<summary>Click to Reveal Answer</summary>

The AI stepped in whole dollars and missed **49.99 and 50.01**. Use a **technique-driven prompt**: name the technique (BVA), give the exact rule and its precision ($0.01), and ask for the working first and the gaps last. **Work the technique yourself before reading the AI's answer**, then compare. Treat its "not covered" list as questions for the requirement, and put only reviewed values into `pytest.mark.parametrize`.
</details>

---

#### Q37: [Format Locking] Your script calls `json.loads` on an AI reply and gets `JSONDecodeError`. The reply starts "Here are your tests:" and is wrapped in a ```json fence. What do you do?
**Hint:** Extract, parse, check, re-ask.
**Keywords:** format drift, extract the JSON, defensive parsing, re-ask once with the exact error, look yourself
<details>
<summary>Click to Reveal Answer</summary>

This is normal format drift. Parse **defensively**: extract just the JSON part (from the first `[` or `{` to the last), parse it, then run shape checks (types, counts, keys) and meaning checks. If it still fails, **re-ask once with the exact error**; if that fails, look at the reply yourself. Longer term, tighten the prompt: forbid extra text, or use a provider feature such as Structured Outputs.
</details>

---

#### Q38: [AI-Assisted Coding] An AI says it refactored your function "with no behaviour change". How do you verify that?
**Hint:** Refactor does not guarantee same behaviour.
**Keywords:** list of changes, diff, characterization tests, behaviour change, magic numbers
<details>
<summary>Click to Reveal Answer</summary>

"Refactor" does not guarantee "same behaviour". Ask the AI for a **list of changes**, read the **diff** line by line, and before the change pin important behaviour with **characterization tests** (tests that record what the code does today). Run them after the refactor; any difference is a behaviour change to investigate.
</details>

---

#### Q39: [Prompt Failure Modes] A severity-labelling prompt gives "High" on one run and "Medium" on the next for the same bug. How do you debug it?
**Hint:** Treat it like a flaky test.
**Keywords:** reproduce, new chat, consistency check, change one thing, prompt failure report
<details>
<summary>Click to Reveal Answer</summary>

Debug prompts like tests. **Reproduce** it by running the same prompt several times in new chats, and run a **consistency check** comparing the answers to find unstable values. Then **change one thing at a time** (for example, add the exact severity rules or balanced few-shot examples), re-run and compare. Record it in a **prompt failure report** with the failure mode and suggested fix.
</details>

---

### Advanced (Deep Dive)

#### Q40: [Few-Shot] Your few-shot prompt still invents a rule that is not in the requirement. Adding more examples does not help. Why, and how would you make the prompt reliable and reusable?
**Hint:** What do examples teach?
**Keywords:** examples teach patterns not facts, add context, way out, balanced varied examples, check with the same rule, prompt library, version
<details>
<summary>Click to Reveal Answer</summary>

**Examples teach patterns, not facts.** If the requirement is missing, the model fills the gap with likely content, and more examples cannot supply the missing fact. The fix is **context**: paste the real requirement between delimiters and give the AI a **way out** ("NOT SPECIFIED", or labelled assumptions).

To make it reliable: keep examples varied, correct, short, consistent and realistic; balance labels and mix the order to avoid majority-label and recency bias; check both the examples and the replies with the **same rule** (for example, a regular expression for each allowed answer line); and judge it over several runs. Then save it in a **prompt library** with a version and a "Use" line, so others reuse the working version.
</details>

---

## Day 3 (Wednesday): AI-Augmented QA Lifecycle

### Beginner (Foundational)

#### Q41: [AI in the QA Lifecycle] What are the three levels of AI involvement, and how do you choose one?
**Keywords:** assist, draft, automate, cost of a mistake, checkability, undone
<details>
<summary>Click to Reveal Answer</summary>

**Assist** (suggest ideas), **draft** (produce a first version a person reviews) and **automate** (run on its own). Choose deliberately, based on the **cost of a mistake**, how easily the output can be **checked**, and whether it can be **undone**.
</details>

---

#### Q42: [AI in the QA Lifecycle] What is error propagation in the STLC, and where is the cheapest place to catch it?
**Keywords:** hand-over, invented sentence, false bug, human check, "Is this statement actually in the story?"
<details>
<summary>Click to Reveal Answer</summary>

Each phase trusts the one before it, so an early AI mistake spreads. In the lesson, one invented sentence became a wrong test case, wrong data, a failing test and a **false bug**. Put a human check at every **hand-over**. The cheapest is the first: "Is this statement actually in the story?"
</details>

---

#### Q43: [Requirements Analysis] What makes a requirement testable, and what are the common defects?
**Keywords:** clear pass/fail, vague words, missing values, missing behaviour, weak obligations
<details>
<summary>Click to Reveal Answer</summary>

A requirement is **testable** when you can write a clear pass/fail test for it. Common defects: **vague words** ("fast", "several"), **missing values**, **missing behaviour** (what the user sees or the system does in a situation) and **weak obligations** ("may").
</details>

---

#### Q44: [Requirements Analysis] Why run a deterministic word check before an AI review of requirements?
**Keywords:** deterministic, same output, weak words, meaning, AI can be wrong
<details>
<summary>Click to Reveal Answer</summary>

The **word check** is deterministic and cheap: it always flags the same weak words. But it can't see meaning: it missed US-205 AC4, which has no weak words but no stated behaviour for a second coupon. The **AI review** then looks for meaning problems like that, though the AI can also be wrong. So use both, in that order, and turn every problem into an open question for the BA.
</details>

---

#### Q45: [AI-Generated Test Cases] What fields does a good test case have, and what is traceability?
**Keywords:** ID, requirement, title, steps, exact expected result, link to requirement, traceability matrix
<details>
<summary>Click to Reveal Answer</summary>

An **ID, the requirement it covers, a title, steps (and test data) and an exact expected result**. The requirement field is what makes review possible. **Traceability** is the link from each test case back to its requirement; a **traceability matrix** shows which cases cover each requirement.
</details>

---

#### Q46: [AI-Generated Test Cases] What should code check in AI test cases, and what should a human check?
**Keywords:** structure, fields, coverage, exact messages, meaning, invented rules, missing boundaries
<details>
<summary>Click to Reveal Answer</summary>

**Code checks structure** (fields, coverage, exact messages) in milliseconds. **Humans check meaning** (invented rules, missing boundaries, whether a case makes sense). An empty check output means the structure is right, not that the suite is complete.
</details>

---

#### Q47: [AI-Generated Test Data] What are positive, negative and boundary test data?
**Keywords:** accepted, rejected, one rule broken per row, on or next to a limit, 17, 18, 120, 121
<details>
<summary>Click to Reveal Answer</summary>

**Positive** data should be accepted; **negative** data should be rejected, with one rule broken per row so you know which rule caused it; **boundary** data sits on or next to a limit (such as ages 17, 18, 120 and 121). Work out what you need by purpose before asking the AI.
</details>

---

#### Q48: [AI-Generated Test Data] What is a hidden rule in test data, and how do you check AI data against it?
**Keywords:** ISO 3166-1 alpha-2, "UK" vs GB, independent check, script, not the same AI
<details>
<summary>Click to Reveal Answer</summary>

A **hidden rule** is one that is easy to break without noticing, such as ISO 3166-1 alpha-2 country codes: "UK" looks right but the code is **GB**. AI data looks realistic but often breaks such rules (also formats, ranges, duplicates, wrong types). Check every row with an **independent check**, such as a script, not by asking the same AI that produced it.
</details>

---

#### Q49: [AI-Generated Test Data] How do you make test data repeatable?
**Keywords:** save it, fixed seed, pseudo-random, same every run
<details>
<summary>Click to Reveal Answer</summary>

Save the data, or generate it with a **fixed seed**. Pseudo-random numbers are produced by a fixed process from the seed, so the same seed gives the same data on every run. Add boundary rows deliberately rather than hoping the generator hits them.
</details>

---

#### Q50: [AI-Assisted Automation] What is a weak assert, and where should expected values come from?
**Keywords:** `assert result`, `is not None`, exact assert, `==`, source of truth, never the code under test
<details>
<summary>Click to Reveal Answer</summary>

A **weak assert**, such as `assert result` or `assert x is not None`, passes for many wrong results and gives false confidence. Write **exact asserts** with `==` against an exact expected value. That value must come from the **source of truth** (the requirement or a reviewed test case), never from the code under test.
</details>

---

#### Q51: [AI-Assisted Automation] Why prefer user-facing locators in AI-generated Playwright code?
**Keywords:** `get_by_role`, `get_by_label`, `get_by_text`, fragile CSS/XPath, IDs, positions
<details>
<summary>Click to Reveal Answer</summary>

User-facing locators (`get_by_role`, `get_by_label`, `get_by_text`) find elements by what a user sees, so they survive changes to internal details. **Fragile locators** depend on IDs, classes or element positions and break easily. AI tools often generate fragile CSS and XPath, so review and replace them, and give the AI your team's conventions.
</details>

---

#### Q52: [Human Validation] Describe the human validation process and its four checklist questions.
**Keywords:** checklist, accept/edit/reject, record why, accountable, trace to AC, exact expected result, nothing invented, could it fail
<details>
<summary>Click to Reveal Answer</summary>

Checklist → **accept, edit or reject** → **record why**, with a named person staying **accountable**. The four questions: Does it **trace to an AC**? Is the **expected result exact**? Is **nothing invented**? **Could it fail**?
</details>

---

#### Q53: [Human Validation] What are the fluency trap, the volume trap and automation bias?
**Keywords:** well written, looks thorough, trusting a tool too much, method protects you
<details>
<summary>Click to Reveal Answer</summary>

- **Fluency trap:** trusting text because it is well written.
- **Volume trap:** trusting a large amount of output because it looks thorough.
- **Automation bias:** trusting a tool's output more than you should.

When attention fails, a review **method** (the checklist) protects you.
</details>

---

#### Q54: [Responsible Use] What does "redact before you prompt" mean?
**Keywords:** placeholders, `<EMAIL>`, keep structure, pre-flight check, "if in doubt, don't paste"
<details>
<summary>Click to Reveal Answer</summary>

Replace sensitive values (personal data and secrets) with **placeholders** such as `<EMAIL>` while keeping the structure, before sending anything to an AI tool. A redaction script with a **pre-flight check** refuses to send text that still contains sensitive data, but it only catches the patterns it knows, so read the output before pasting. **If in doubt, don't paste.**
</details>

---

### Intermediate (Application)

#### Q55: [AI-Assisted Automation] The AI's tests report `2 passed`. How do you know they actually test anything?
**Hint:** Break it on purpose.
**Keywords:** "break it" check, mutation testing, mutant, killed, survived, false confidence
<details>
<summary>Click to Reveal Answer</summary>

**Break the code on purpose** and re-run. In the lesson, the AI's tests still passed on broken code (`2 passed`), while the reviewed tests caught it (`3 failed, 1 passed`). **Mutation testing** formalises this: run the tests against copies of the code with one small change (**mutants**). A mutant the tests detect is **killed**; one they miss **survived** and shows a weak test. Prove each test can fail before you trust it.
</details>

---

#### Q56: [AI-Generated Test Data] An AI gave you five "valid" users and labelled one row "invalid: age 120". Your checker says only one user is valid and age 120 is allowed. What do you conclude?
**Hint:** Compare each row's claim with the checker's finding.
**Keywords:** labelled data, purpose column, independent check, mislabelled boundary, 1 of 5
<details>
<summary>Click to Reveal Answer</summary>

Trust the **independent checker**, then confirm against the rules. This matches the lesson: only **1 of 5** "valid" users was valid, and the AI **mislabelled the boundary age 120**. Labelled data (a **purpose column**) is what makes this visible: compare each row's claim with the checker's finding. Fix the data, add deliberate boundary rows, and save it so it is repeatable.
</details>

---

#### Q57: [AI in the QA Lifecycle] Your team wants AI to automatically file bug reports from failing tests. What level of AI involvement would you recommend?
**Hint:** Cost of a mistake, checkability, reversibility.
**Keywords:** draft not automate, false bug, over-generalisation, human check at hand-over, code points humans decide
<details>
<summary>Click to Reveal Answer</summary>

**Draft**, not automate. A failing test may be a wrong test (from an invented rule upstream), so auto-filed reports risk **false bugs** and **over-generalisation** from one failing case. Bug reports go to other people and cost time, so the cost of a mistake is real. Let the AI draft; a person checks the report against the requirement at the hand-over. Code points; humans decide.
</details>

---

#### Q58: [Responsible Use] You realise you pasted a production API key into an AI chat. What do you do?
**Hint:** Five steps.
**Keywords:** stop, delete, tell, rotate, learn, accountability
<details>
<summary>Click to Reveal Answer</summary>

**Stop, delete, tell, rotate, learn.** Stop pasting, delete the message where possible, tell the people responsible (as the AI usage policy says), **rotate** the key so the old value no longer works, and learn from it, for example by adding the pattern to the redaction script's pre-flight check.
</details>

---

#### Q59: [Human Validation] Your correction log shows a 50% accepted-as-is rate, with one wrong expected result and one invented rule. How do you use that?
**Hint:** Reviews as evidence.
**Keywords:** correction log, reason category, prompt fix, review depth, risk, sample finds problems
<details>
<summary>Click to Reveal Answer</summary>

The **correction log** turns reviews into evidence. Each **reason category** points to a prompt fix: the wrong expected result to stating exact values; the invented rule to forbidding anything not in the story. Match **review depth to risk**: money and security get a full review, and if a sample review finds problems, review everything.
</details>

---

### Advanced (Deep Dive)

#### Q60: [AI in the QA Lifecycle] Design an AI-assisted "requirements → test cases → test data" flow for a coupon story. Where do the human checks go, and who is accountable?
**Hint:** One check per hand-over.
**Keywords:** word check, AI review, question log, "(to confirm with the BA)", traceability matrix, structure script, independent data check, second reviewer, accountable, disclosure
<details>
<summary>Click to Reveal Answer</summary>

1. **Requirements:** run the deterministic word check, then an AI review that is banned from answering its own questions. Check for invented answers. Send every problem to the BA as an open question in a **question log**; mark temporary values "(to confirm with the BA)".
2. **Test cases:** give the AI the reviewed requirement. A **structure script** checks fields, coverage and exact messages; a **traceability matrix** questions coverage; a person reviews meaning with the four-question checklist (in two passes for large sets), calculating expected values by hand.
3. **Test data:** work out needed data by purpose first, then check every AI row with an **independent script**, labelled with a purpose column and saved or seeded.
4. **Automation:** exact asserts from the reviewed cases, and a "break it" check.

At every hand-over, ask "Is this in the story?" An AI can act as a **second reviewer**, but the story decides disagreements. A named person is **accountable** and **discloses** AI help; sensitive data is redacted before any prompt.
</details>

---

## Day 4 (Thursday): Agent Anatomy

### Beginner (Foundational)

#### Q61: [Agent Architecture] What is an AI agent in this course, and what are its parts?
**Keywords:** one job, same way every time, instructions, input template, output format, examples, checks
<details>
<summary>Click to Reveal Answer</summary>

An AI model set up to do **one job the same way every time**: a reusable package of **instructions, input template, output format, examples and checks**. This week's agent, TestCaseDesigner, turns one user story into test cases in a fixed JSON format. Its main benefit is checkable answers: the same shape every time.
</details>

---

#### Q62: [Agent Architecture] What is the difference between a workflow and an agent in Anthropic's sense?
**Keywords:** predefined code paths, model directs its own steps, tool use
<details>
<summary>Click to Reveal Answer</summary>

In a **workflow**, models and tools follow **predefined code paths**. In an **agent**, the **model directs its own steps** and tool use.
</details>

---

#### Q63: [Agent Architecture] Does an agent improve itself over time?
**Keywords:** does not learn by itself, change its files, which part allowed it
<details>
<summary>Click to Reveal Answer</summary>

No. An agent **does not learn by itself**; you improve it by changing its files (instructions, template, examples, checks). When a reply is wrong, ask **which part allowed it**, and fix that part.
</details>

---

#### Q64: [Agent Instructions] What are the five sections of agent instructions?
**Keywords:** role and goal, scope, rules, output, when something is unclear
<details>
<summary>Click to Reveal Answer</summary>

**Role and goal**, **scope** (what to do and not do), **rules**, **output**, and **when something is unclear**. They are the agent's standing orders, sent with every story, so their strengths and weaknesses repeat on every run.
</details>

---

#### Q65: [Agent Instructions] What is `needs_clarification`, and why does an agent need a way out?
**Keywords:** status, cannot test without more information, forbid guessing, questions
<details>
<summary>Click to Reveal Answer</summary>

`needs_clarification` is the status the agent uses when it cannot test a story without more information. It is the agent's **way out**: name the situation, forbid guessing, and say exactly where the question goes. Without it, the agent fills the gap with invented values.
</details>

---

#### Q66: [Prompt Templates] What is a prompt template, and how is the full agent prompt assembled?
**Keywords:** fixed text, placeholders, `$story_id`, fences, instructions, examples, story last
<details>
<summary>Click to Reveal Answer</summary>

A **prompt template** is fixed text with **placeholders** (such as `$story_id`, `$title`, `$max_cases`, `$acceptance_criteria`), filled with one story's data per run, in a copy of the template. The **full agent prompt** is instructions, then examples, then the filled template, with **fences** (`### Story` / `### End of story`) around the story, which goes **last**.
</details>

---

#### Q67: [Prompt Templates] What is a leftover placeholder, and why must placeholder names never change?
**Keywords:** not replaced, reaches the AI as `$name`, story files, program that fills it
<details>
<summary>Click to Reveal Answer</summary>

A **leftover placeholder** wasn't replaced, so it reaches the AI as `$name`. Any template change must be matched in every story file and in the program that fills it; code fills the templates, so names must be exact and stay the same.
</details>

---

#### Q68: [IO Contracts] What is an input/output contract, and what must it state for every field?
**Keywords:** valid input, valid output, name, kind, required, rule
<details>
<summary>Click to Reveal Answer</summary>

A written agreement on what goes into the agent (a story file) and what must come out (a reply). It is the definition of "a valid answer" every check is built from. For every field state its **name, kind** (text, number, list, object), whether it is **required**, and its **rule** (what a valid value looks like).
</details>

---

#### Q69: [IO Contracts] What do contract-first and source of truth mean?
**Keywords:** write contract before building, one document treated as correct, contract version
<details>
<summary>Click to Reveal Answer</summary>

**Contract-first** means writing the contract before building the parts that produce and check the data. The contract is the **source of truth**: when files disagree, it is the one everyone treats as correct. It has a **version** (such as v1) that changes whenever the agreement changes.
</details>

---

#### Q70: [JSON Schema] Name the main JSON Schema keywords and what each does.
**Keywords:** type, required, properties, enum, pattern, items, additionalProperties, minItems
<details>
<summary>Click to Reveal Answer</summary>

- `type`: what kind of value is allowed (`integer` rejects "3").
- `required`: fields that must be present.
- `properties`: rules for each named field.
- `enum`: the only allowed values.
- `pattern`: a regular expression text must match.
- `items`: rules for every item in a list.
- `additionalProperties`: whether unlisted fields are allowed.
- `minItems` / `minimum`: the smallest list length / number.
</details>

---

#### Q71: [JSON Schema] If a reply passes JSON Schema validation, is it correct?
**Keywords:** shape not meaning, well-formed, wrong amount, invented AC, deterministic
<details>
<summary>Click to Reveal Answer</summary>

No. A schema checks **shape, not meaning**. In the lesson, a wrong amount, an invented AC and an extra field all passed. Passing means **well-formed**. The validator is deterministic, so on shape its verdict beats an AI's, but rules that need the story come next.
</details>

---

#### Q72: [Required Fields] What is the difference between a missing field and an empty one?
**Keywords:** not there at all, there with nothing in it, "none", broken reply, `KeyError`
<details>
<summary>Click to Reveal Answer</summary>

**Missing** means not there at all; **empty** means there with nothing in it. An empty list means "none"; a missing field means a broken reply (and Python raises `KeyError` when code asks for it). This contract makes every field required, so an absence always means broken.
</details>

---

#### Q73: [Required Fields] What are the three layers of checking an agent reply?
**Keywords:** schema (shape), rules (reply against story), person (meaning), human checklist
<details>
<summary>Click to Reveal Answer</summary>

1. **Schema**: shape.
2. **Rules** (R1 to R4, Q1): the reply against the story.
3. **Person**: meaning, using the human checklist (invented values, boundaries, exact messages).

Invented values and missing boundaries pass both automatic layers, so the human layer stays essential.
</details>

---

#### Q74: [Sample Pairs] What is a sample input/output pair, and what is example leakage?
**Keywords:** story with correct reply, documents, teaches, show don't tell, copying details
<details>
<summary>Click to Reveal Answer</summary>

A **sample pair** is an example story with a correct reply. It **documents** a good answer and, in the prompt, **teaches** the AI the pattern: show, don't tell. **Example leakage** is the AI copying details of an example, such as its ID or values, into an unrelated reply. Use different stories from the real ones to reduce it.
</details>

---

### Intermediate (Application)

#### Q75: [JSON Schema] A reply has a test case with `"priority": "Urgent"`, a test case missing `id`, and an extra field `"notes"`. Which schema keywords catch each problem, and how does the validator report them?
**Hint:** Look for the path.
**Keywords:** enum, required, additionalProperties, path, `test_cases/0/id`, every mismatch
<details>
<summary>Click to Reveal Answer</summary>

- "Urgent" not in the allowed list → `enum`.
- Missing `id` → the test case's `required` list (inside `items`).
- Extra `notes` → `additionalProperties: false`.

The validator reports **every mismatch** with a **path** to its location, such as `test_cases/0/id`. Missing fields are what people and AIs most often miss, so walk the `required` lists field by field.
</details>

---

#### Q76: [Required Fields] Reply A passed the schema but broke R2, R3, R4 and Q1. Explain those rules and why a schema cannot check them.
**Hint:** What does the schema not see?
**Keywords:** R1 right story, R2 no invented ACs, R3 within limit, R4 coverage, Q1 vague expected results, needs the story
<details>
<summary>Click to Reveal Answer</summary>

- **R1:** the reply is for the right story (no wrong or mistyped ID).
- **R2:** no invented ACs (such as AC9 for US-205).
- **R3:** within the case limit.
- **R4:** coverage: every AC has a test case or an open question.
- **Q1:** no vague expected results ("Discount is applied correctly").

A schema sees **only the reply**. These rules compare the reply with the **story**, so they need code that reads both.
</details>

---

#### Q77: [Sample Pairs] For US-311, the agent's reply had a perfect format but invented "2 seconds". Adding a second example fixed it. Why, and what should you watch for?
**Hint:** What kind of story was Example 2?
**Keywords:** vague story, honest question, `needs_clarification`, leakage, test a clear story, every example passes every rule
<details>
<summary>Click to Reveal Answer</summary>

Example 2 showed a **vague story** answered with an **honest question** and `needs_clarification`, so the AI copied that pattern instead of inventing a value. Cover different situations (a clear story and a vague one). Watch for **leakage**, and re-test a **clear** story to make sure the agent doesn't now ask questions about everything. **Every example must pass every rule**, because the AI copies mistakes too.
</details>

---

#### Q78: [Agent Instructions] An agent sometimes returns too many test cases. How would you investigate and fix the instructions?
**Hint:** Test plan, smells, controlled change.
**Keywords:** test plan for instructions, instruction smell, contradiction, checkable rule, controlled change, versioning
<details>
<summary>Click to Reveal Answer</summary>

Write a **test plan for instructions** first: what a correct reply should contain for each story. Look for **instruction smells**, such as a **contradiction** between two rules. Make the limit a **checkable rule** (written from the observed mistake), fix **the section that allowed it**, not just the reply, and make a **controlled change** (one thing only) in a new **version**, so any difference in results is caused by that change.
</details>

---

#### Q79: [IO Contracts] A story file fails to load, and you see the AC text contains `"SAVE10"` in quotes. Separately, your code crashes with `KeyError: 'questions'` on a reply. What is going on in each case?
**Hint:** Escaping; missing vs empty.
**Keywords:** escaping, `\"`, JSON data file, missing field, required, broken reply
<details>
<summary>Click to Reveal Answer</summary>

1. Stories are **JSON data files**, so a quote inside a string must be **escaped** as `\"`. Otherwise it ends the string and the JSON is invalid.
2. `KeyError` means the field is **missing**, not empty. The contract makes every field required, so it's a broken reply: the agent should have returned an empty list if there were no questions. Code should report this as a contract failure, not crash.
</details>

---

### Advanced (Deep Dive)

#### Q80: [Agent Anatomy] In a pair-programming session, you design a requirements agent from scratch. Walk through its anatomy and how each part is checked.
**Hint:** Contract first, one job, three layers.
**Keywords:** one agent one job, contract-first, schema, enum status, pattern IDs, additionalProperties, rules needing the story, sample pairs, human checklist, version
<details>
<summary>Click to Reveal Answer</summary>

1. **One job**, stated in the role and goal, with a clear scope.
2. **Contract first:** for each input and output field, give name, kind, required and rule, including an honest "I can't" path (`needs_clarification`, empty test-case list, AC-prefixed questions). Version it, and treat it as the source of truth.
3. **JSON Schema** from the contract: `required` everywhere, `enum` for status, `pattern` for IDs, `additionalProperties: false`, limits like `minItems`. Make sure the schema still allows the honest empty-list reply.
4. **Instructions** in five sections, each rule checkable, with a way out.
5. **Template** with exact `$placeholders`, story fenced and last.
6. **Sample pairs** for a clear and a vague story, each passing every rule.
7. **Checks** in three layers: schema (shape), story rules like R1–R4 and Q1 (code), and the human checklist (meaning).

When a reply is wrong, find the part that allowed it and fix it in a new version.
</details>

---

## Day 5 (Friday): Building a First QA Agent

### Beginner (Foundational)

#### Q81: [Building Instructions] What changes when draft instructions become the official v1?
**Keywords:** same words, rule IDs, version, rule map, check
<details>
<summary>Click to Reveal Answer</summary>

v1 keeps the same words as the draft, plus **rule IDs** (such as G1 or F2) and a **version**. Every rule gets an ID and a check. A **rule map** links each rule to the check that tests it: code for structure (R3, R4, fields), people for meaning (G1, B1, M1). If a rule cannot be checked, ask how you would ever know it was broken.
</details>

---

#### Q82: [Building Instructions] Why must you never edit a version of the instructions after it has run?
**Keywords:** new version, comparable results, traceability, changelog
<details>
<summary>Click to Reveal Answer</summary>

Results must stay **comparable** and **traceable**: you must always be able to say which version produced each reply. Editing a version that already ran breaks that link. Create a new version (such as v1.1) instead.
</details>

---

#### Q83: [Building Instructions] What is grounding?
**Keywords:** stick to the facts given, nothing invented, G1
<details>
<summary>Click to Reveal Answer</summary>

**Grounding** means sticking to the facts given, without inventing anything. In the agent it is rule **G1**, checked by the human checklist question H1: is every rule or value in the test cases actually in the story?
</details>

---

#### Q84: [Reusable Templates] What does `build_prompts.py` do, and why does it use `substitute` instead of `safe_substitute`?
**Keywords:** `string.Template`, one prompt per story, stops on missing placeholder, `KeyError`, loud failure
<details>
<summary>Click to Reveal Answer</summary>

It uses Python's `string.Template` to fill the template for every story and saves one full prompt per story in `prompts/v1/`. `substitute` **stops** (with `KeyError`) on a missing placeholder; `safe_substitute` would leave it in the text. A loud failure is better than a quiet broken prompt.
</details>

---

#### Q85: [Reusable Templates] How are prompts and replies kept organised across versions, and what is the manual step this week?
**Keywords:** version in path, `replies/v1/<story id>.txt`, new chat, whole reply unedited
<details>
<summary>Click to Reveal Answer</summary>

The **version is part of the path** (`prompts/v1/`, `replies/v1/`), so versions never mix. The manual step: **you** paste each prompt into a **new chat** and save the **whole reply, unedited**, as `replies/v1/<story id>.txt`.
</details>

---

#### Q86: [Reusable Templates] What does "data in files, logic in code" mean for the agent?
**Keywords:** new stories, new versions, no code changes, JSON file
<details>
<summary>Click to Reveal Answer</summary>

Stories and instructions live in data files; the scripts hold the logic. So **new stories and new versions need no code changes**: add a JSON story file or a new instructions version and run the same command.
</details>

---

#### Q87: [Implementing IO Contracts] What does `check_reply.py` check, and in what order?
**Keywords:** find the JSON, required fields, R1 to R4, Q1, list of problems, early stop
<details>
<summary>Click to Reveal Answer</summary>

It finds the JSON in the reply, checks the required fields, then rules **R1 to R4 and Q1**, and returns a **list of problems**. If a reply is too broken for later checks (for example, no valid JSON), it **stops early**.
</details>

---

#### Q88: [Implementing IO Contracts] What does "defensive parsing" mean in `check_reply.py`?
**Keywords:** generous about wrapping, strict about content, chat text, fences, `find`/`rfind`, broken JSON
<details>
<summary>Click to Reveal Answer</summary>

It keeps only the JSON part of a reply (using `find` for the first and `rfind` for the last occurrence of the brackets) and handles broken JSON safely. It is **generous about wrapping** (chat text, fences) and **strict about content** (broken JSON is a failure).
</details>

---

#### Q89: [Implementing IO Contracts] How do sets make R2 and R4 easy to check?
**Keywords:** three sets, set difference, `a - b`, invented ACs, forgotten ACs
<details>
<summary>Click to Reveal Answer</summary>

Build three sets: the story's AC IDs, the ACs covered by test cases, and the ACs with open questions. **R2 (invented ACs)** is reply ACs minus story ACs; **R4 (forgotten ACs)** is story ACs minus covered and questioned ACs. Each is one subtraction (`a - b`).
</details>

---

#### Q90: [Validation Scripts] What does `run_agent.py` do, and what do WAITING, PASS and FAIL mean?
**Keywords:** whole backlog, one command, reuse, DRY, results table, no reply yet, broke a rule
<details>
<summary>Click to Reveal Answer</summary>

It runs the whole backlog with one command: build prompts, (you run the AI), check, record and compare. **WAITING** = no reply yet; **PASS** = passed the checker; **FAIL** = broke at least one rule. Results go to `results_<version>.md`, which doubles as a to-do list. It **reuses** `build_prompts` and `check_reply` and has **no rules of its own** (DRY), so a rule changed once is used by every run.
</details>

---

#### Q91: [Output Validation] What does a PASS from the checker script mean?
**Keywords:** well-formed, not correct, passed these checks, two layers
<details>
<summary>Click to Reveal Answer</summary>

**Well-formed, not correct.** It means "passed these checks" only. Validation has **two layers**: the script checks the contract; a person checks the meaning with the human checklist.
</details>

---

#### Q92: [Output Validation] What are the human checklist questions H1 to H4?
**Keywords:** invented, boundaries at limit and just below, exact messages, right status, G1, B1, M1, U1
<details>
<summary>Click to Reveal Answer</summary>

- **H1 (G1):** Is every rule or value in the test cases actually in the story?
- **H2 (B1):** Is every numeric limit tested at the limit **and** just below it ($50.00 and $49.99)?
- **H3 (M1):** Is every message copied **exactly**?
- **H4 (U1):** Is the status right? A story with no measurable value should be `needs_clarification`.
</details>

---

#### Q93: [Output Validation] What decisions can be made about a reply, and why must you never hand-edit one?
**Keywords:** accept, fix the instructions, questions to the BA, record why, `review_v1.md`
<details>
<summary>Click to Reveal Answer</summary>

**Accept**, **fix the instructions**, or **send questions to the BA**. Hand-editing a reply hides the agent's real behaviour, so the problem comes back next run; the fix belongs in the agent's files. Record why, with rule IDs and evidence, in `review_v1.md`; those notes drive the refinement.
</details>

---

#### Q94: [Executing Agents] What is triage of agent results, and does "accepted" mean finished?
**Keywords:** action, owner, tester, BA, agent maintainer, accepted is not finished
<details>
<summary>Click to Reveal Answer</summary>

**Triage** gives every result an **action and an owner**: the tester, the BA or the agent maintainer (one story can need two). **Accepted is not finished**: a tester still reviews the cases, adds real test data and confirms assumptions.
</details>

---

### Intermediate (Application)

#### Q95: [Output Validation] US-311 passed the script but was wrong. Explain what happened and what decision you would make.
**Hint:** H1 and H4.
**Keywords:** passed the script, invented "2 seconds", should be `needs_clarification`, fix the instructions, code points a person decides
<details>
<summary>Click to Reveal Answer</summary>

The reply was well-formed, so the script passed it, but the human review found **H1 ✗**: "2 seconds" is invented, and **H4 ✗**: the story has no measurable value, so the status should have been `needs_clarification` with a question. Decision: **fix the instructions** (for example, strengthen G1 and add a vague-story example), not the reply. Code can point; a person decides.
</details>

---

#### Q96: [Agent Refinement] The script reported 2 passes for v1, but the human review found only 1. How do you decide what to change for v1.1?
**Hint:** Count failures by rule from both layers.
**Keywords:** error analysis, both layers, H1 most common, targeted change, changelog, same stories
<details>
<summary>Click to Reveal Answer</summary>

Do **error analysis**: count failures by rule from **both** layers. In the lesson the most common problem was **H1 (invented content)**, found only by the human review; a script-only analysis would have missed it. Make **targeted changes** for failures actually seen (for example, name "time limits" and "case-sensitive" in G1; add "Count them before you reply" to F2), save v1.1 with a **changelog**, and rerun the **same** stories. With v1.1, all four passed both layers.
</details>

---

#### Q97: [Agent Refinement] You changed three rules at once in v1.1 and results improved. What can and can't you conclude?
**Hint:** Fair comparison.
**Keywords:** bundled changes, which one helped, one run proves little, variation, regression, removing rules
<details>
<summary>Click to Reveal Answer</summary>

**Bundling** is efficient but hides which change helped. Results vary **run to run**, so one run proves little. Always check for **regressions** (something that used to work and no longer does), and for **over-applying** rules, such as asking questions about a clear limit. A fair comparison changes only the instructions and reruns the same stories. Every rule costs length, so good refinement sometimes **removes** rules too.
</details>

---

#### Q98: [Implementing IO Contracts] How do you test the checker itself?
**Hint:** False alarms and gaps.
**Keywords:** compare with hand checks, false alarm, strict check, checker coverage, gaps
<details>
<summary>Click to Reveal Answer</summary>

Compare its results with your **hand checks**. In the lesson it matched every hand check but had **false alarms** ("networks", trailing braces) and **gaps** (status values, test case fields were not checked). Know your **checker coverage**: which parts of the contract it actually tests, so you know what the human layer must cover.
</details>

---

#### Q99: [Executing Agents] US-314's reply passed the script but assumed "day 30 is included" when the story doesn't say so. What do you do, and how do you avoid missing this?
**Hint:** Assumption stated as fact; prediction before review.
**Keywords:** assumption stated as fact, question to the BA, question log, full boundary analysis, prediction, anchoring
<details>
<summary>Click to Reveal Answer</summary>

It is an **assumption stated as fact**. Send a question to the **BA**, log it in the **question log**, and once answered, make sure the tests cover the boundary fully (just below, on and just above as needed). To avoid missing it, write a **prediction** of what a good reply should contain **before** reading the agent's reply, so the review isn't **anchored** by it.
</details>

---

### Advanced (Deep Dive)

#### Q100: [Agent Testing] Next week you'll automate the agent through an API. A colleague says, "The script passes everything now, so let's drop the human review." How do you respond, and what actually changes?
**Hint:** Which block changes, and what PASS means.
**Keywords:** API, step 2 only, human review stays, PASS means well-formed, checker gaps, triage, accountability, regression
<details>
<summary>Click to Reveal Answer</summary>

Only the **step 2 block** of `run_agent.py` (pasting each prompt and saving the reply) changes when the agent runs through an **API**; building, checking and recording stay the same. **The human review stays.** A script PASS means well-formed, not correct: US-311 passed with an invented value and the wrong status, and US-314 passed with an assumption stated as fact. The checker has known **gaps**, and invented content was the most common v1 failure, found **only** by people.

Automation makes runs faster and more frequent, which makes the evidence loop more important: keep two-layer validation, triage with owners, versioned instructions with changelogs, and regression checks on the same stories. A person stays accountable for what the agent produces.
</details>
