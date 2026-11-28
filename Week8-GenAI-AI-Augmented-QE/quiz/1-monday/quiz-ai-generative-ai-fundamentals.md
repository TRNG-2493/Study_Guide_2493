# Weekly Knowledge Check: [Week8-GenAI-AI-Augmented-QE] — Monday: AI & Generative AI Fundamentals

**Covers:** AI, ML & DL · Supervised vs. unsupervised learning · Neural network fundamentals · NLP fundamentals · Generative AI concepts · Generative AI applications within QE
**Questions:** 50 · **Formats:** Multiple Choice, True/False, Code Prediction, Fill-in-the-Blank

---

## Part 1: Multiple Choice

### 1. Which ordering runs from the outermost circle to the innermost?
- [ ] A) Machine Learning → AI → Deep Learning → Generative AI
- [ ] B) AI → Machine Learning → Deep Learning → Generative AI
- [ ] C) AI → Deep Learning → Machine Learning → Generative AI
- [ ] D) Generative AI → Deep Learning → Machine Learning → AI

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) AI → Machine Learning → Deep Learning → Generative AI

**Explanation:** Each field sits inside the one before it: AI ⊃ ML ⊃ DL ⊃ GenAI.
- **Why others are wrong:**
  - A) ML is a part of AI, so it cannot sit outside it.
  - C) Deep learning is a part of machine learning, not the other way round.
  - D) This is the innermost-to-outermost order, reversed.
</details>

---

### 2. A script pages the on-call engineer when "ERROR" appears 5 times in one minute. How should it be classified?
- [ ] A) Machine learning, because it makes a decision automatically
- [ ] B) Deep learning, because it processes log text
- [ ] C) Rule-based AI, because a person wrote the rule and nothing was learned
- [ ] D) Generative AI, because it produces an alert

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Rule-based AI

**Explanation:** A hand-written rule is AI but not ML. Nothing in it was learned from labelled data.
- **Why others are wrong:**
  - A) Deciding automatically does not make something ML. ML means the rule was *learned* from data.
  - B) Deep learning needs multi-layer neural networks. This is a counter and a threshold.
  - D) Sending an alert is not creating new content in the GenAI sense.
</details>

---

### 3. What is the key difference between traditional programming and machine learning?
- [ ] A) Traditional programming uses data; ML does not
- [ ] B) In traditional programming a person writes the rules; in ML the computer produces the rules from data plus correct answers
- [ ] C) ML always gives the same answer; traditional programs are random
- [ ] D) There is no difference; ML is just a faster language

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Traditional code: rules + data → answers. ML: data + answers → rules (the model).
- **Why others are wrong:**
  - A) Both use data. ML also needs labelled examples to learn from.
  - C) Traditional code is the deterministic one. Some ML systems, such as LLMs, are not deterministic.
  - D) ML is a way of producing rules, not a programming language.
</details>

---

### 4. An AI assistant claims its rule "correctly classifies all 12 rows". What should you do first?
- [ ] A) Ask the same AI whether it is sure
- [ ] B) Apply the rule to every row yourself and count, then test it on new rows it has never seen
- [ ] C) Accept it, since 12 out of 12 is 100%
- [ ] D) Add more rows to the training data and retrain

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This week's habit is "ask the AI, then check its answer." You check the claim by hand or with a script, then check it on unseen data.
- **Why others are wrong:**
  - A) Asking the same AI is not an independent check.
  - C) The claim may simply be false, and even if it is true, 100% on training rows can hide overfitting.
  - D) Retraining does not tell you whether the original claim was true.
</details>

---

### 5. A model scores very well on its training data but poorly on new data. What is this called?
- [ ] A) Underfitting
- [ ] B) Drift
- [ ] C) Overfitting
- [ ] D) Hallucination

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Overfitting

**Explanation:** Overfitting means the model fits its training data too closely, for example by memorising it, so it fails to generalise.
- **Why others are wrong:**
  - A) Underfitting means the model fits too *loosely* and does poorly even on training data.
  - B) Drift is a slow loss of accuracy as real-world data changes over time.
  - D) Hallucination is confident but false output from a GenAI tool.
</details>

---

### 6. "Predict how many minutes the regression suite will take." Which kind of supervised learning is this?
- [ ] A) Classification
- [ ] B) Regression
- [ ] C) Clustering
- [ ] D) Anomaly detection

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Regression

**Explanation:** The answer is a number with units (minutes), and predicting a number is regression.
- **Why others are wrong:**
  - A) Classification predicts a category, such as pass or fail.
  - C) Clustering is unsupervised and groups examples. It does not predict a value.
  - D) Anomaly detection finds outliers. It does not predict durations.
</details>

---

### 7. Which single question decides whether a problem is supervised or unsupervised?
- [ ] A) "How much data do we have?"
- [ ] B) "Do we have labels?"
- [ ] C) "Is the data text or numbers?"
- [ ] D) "Do we need a neural network?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "Do we have labels?"

**Explanation:** Labelled examples (with correct answers) mean supervised learning. No labels means unsupervised learning.
- **Why others are wrong:**
  - A) Data size affects quality, not which approach you use.
  - C) Both approaches work with text or numbers once they are turned into features.
  - D) Either approach may or may not use a neural network.
</details>

---

### 8. A model warns on 10 builds and 6 of them really fail. Which metric is 6 ÷ 10?
- [ ] A) Recall
- [ ] B) Accuracy
- [ ] C) Precision
- [ ] D) Loss

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Precision

**Explanation:** Precision is the share of warnings that were right: 6 correct out of 10 warnings = 0.60.
- **Why others are wrong:**
  - A) Recall is the share of all real failures that were caught, so its denominator is the total number of failures, not the number of warnings.
  - B) Accuracy counts all predictions, including the quiet ones.
  - D) Loss measures how wrong a network's outputs are during training.
</details>

---

### 9. A clustering tool returns three groups of test failures. Who decides what each group *means*?
- [ ] A) The algorithm, because it found the groups
- [ ] B) A person, who names each group as a hypothesis and checks real examples
- [ ] C) Nobody; clusters do not need names
- [ ] D) The AI assistant, if you paste in the cluster IDs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The algorithm only knows that items are similar in the data. It cannot know the cause. A tester names the groups and confirms them against examples.
- **Why others are wrong:**
  - A) Finding similarity is not the same as understanding a cause.
  - C) Unnamed groups are not actionable for a team.
  - D) Cluster IDs alone carry no meaning, and the AI's guess would still need checking.
</details>

---

### 10. Why might a model that is 98% accurate be useless?
- [ ] A) 98% is below the industry standard of 99%
- [ ] B) If only 2% of cases are the class you care about, always predicting the common class gives 98% accuracy and catches none of them
- [ ] C) Accuracy can never be above 95% without overfitting
- [ ] D) Accuracy only applies to regression models

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** This is the accuracy paradox. With class imbalance, high accuracy can hide a recall of 0 on the rare class.
- **Why others are wrong:**
  - A) There is no universal 99% standard. The issue is what the number hides.
  - C) High accuracy is possible without overfitting. Overfitting is about failing on unseen data.
  - D) Accuracy is a classification metric.
</details>

---

### 11. What is data leakage?
- [ ] A) Training data being stolen from a server
- [ ] B) Training with information that will not be available at prediction time
- [ ] C) Losing rows when loading a CSV
- [ ] D) A model forgetting what it learned

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Leakage makes a model look great in testing and fail in real use. Ask of every feature: "Would we know this value at the moment we need the prediction?"
- **Why others are wrong:**
  - A) That is a security breach, not the ML term.
  - C) Lost rows are a data-quality problem, not leakage.
  - D) Losing accuracy over time is closer to drift.
</details>

---

### 12. What three steps does a single artificial neuron perform?
- [ ] A) Sort the inputs, average them, round the result
- [ ] B) Multiply inputs by weights, add them with a bias to get z, pass z through an activation function
- [ ] C) Tokenise the input, embed it, sample a token
- [ ] D) Compare with the label, compute the loss, update the weights

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A neuron is simple arithmetic: weighted sum plus bias gives z, and the activation turns z into an output.
- **Why others are wrong:**
  - A) Neurons do not sort or average their inputs.
  - C) These are LLM text-generation steps, not what a single neuron does.
  - D) These are training steps, not the neuron's forward computation.
</details>

---

### 13. Why does a neural network need non-linear activation functions such as ReLU?
- [ ] A) To make training faster
- [ ] B) Without them, stacked layers collapse into one weighted sum and are no more powerful than one neuron
- [ ] C) To keep all outputs between 0 and 1
- [ ] D) Because linear functions cannot be computed by GPUs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Non-linearity is what lets layers combine features to solve problems such as XOR, which one neuron cannot learn.
- **Why others are wrong:**
  - A) Speed is not the reason non-linearity is required.
  - C) ReLU outputs can be any non-negative number, so keeping outputs between 0 and 1 is not the purpose.
  - D) GPUs compute linear operations very well.
</details>

---

### 14. During training, the learning rate is set far too large. What is the likely result?
- [ ] A) Training is very slow but accurate
- [ ] B) Training overshoots the best weights and may never settle
- [ ] C) The network gains more parameters
- [ ] D) The model becomes deterministic

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The learning rate is the size of each adjustment step. Steps that are too big jump past the best weights.
- **Why others are wrong:**
  - A) That describes a learning rate that is too *small*.
  - C) The learning rate does not change the network's size.
  - D) The learning rate has nothing to do with determinism at inference time.
</details>

---

### 15. Retraining fixed one wrong output, but a different case changed its answer. What should a tester do?
- [ ] A) Ignore it, since the targeted fix worked
- [ ] B) Treat it as a regression risk: re-run a full labelled set, review changed answers, and get a label for the changed case
- [ ] C) Roll back to the very first model ever trained
- [ ] D) Increase the learning rate and retrain

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Fixing one case can change others, just as a code change can break other tests. Re-check the full set.
- **Why others are wrong:**
  - A) Ignoring side effects is exactly how regressions ship.
  - C) Rolling all the way back throws away valid improvements without any analysis.
  - D) Tuning blindly does not investigate the changed answer.
</details>

---

### 16. Which pairing of network design and data type is correct?
- [ ] A) CNN → long text; Transformer → images
- [ ] B) CNN → images; RNN → sequences; Transformer → long text and code
- [ ] C) RNN → images; CNN → sequences
- [ ] D) Transformer → images only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** CNNs suit images, RNNs suit sequences, and Transformers suit long text and code (they power today's LLMs).
- **Why others are wrong:**
  - A) This swaps the CNN and Transformer roles.
  - C) This swaps the RNN and CNN roles.
  - D) Transformers are best known for text and code.
</details>

---

### 17. Why can removing stop words be risky when comparing bug titles?
- [ ] A) Stop words are always the most important words
- [ ] B) Some stop-word lists include "not" or "no", so "Login does not work" and "Login does work" could look identical
- [ ] C) Removing stop words breaks the tokeniser
- [ ] D) Stop words carry the TF-IDF weight

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Negation words change meaning completely. Dropping them is one of the two cleaning traps.
- **Why others are wrong:**
  - A) Most stop words ("the", "is") really are low-value, which is why lists exist.
  - C) Tokenising happens separately and is not affected.
  - D) Common words get *low* IDF weight, not high.
</details>

---

### 18. What does TF-IDF add to simple word counts?
- [ ] A) It removes all stop words automatically
- [ ] B) It weights words that are frequent in one document but rare overall, so distinctive words count more
- [ ] C) It understands synonyms such as "voucher" and "coupon"
- [ ] D) It keeps word order

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** TF-IDF makes "coupon" count for more than a common word such as "page".
- **Why others are wrong:**
  - A) Stop-word removal is a separate cleaning step.
  - C) TF-IDF is still word-based and blind to meaning. Embeddings handle synonyms.
  - D) Like bag of words, it ignores word order.
</details>

---

### 19. The bug "discount voucher makes the basket price incorrect" scored 0.00 against the coupon bug it duplicates. Why?
- [ ] A) The threshold was set too high
- [ ] B) It shared no words with it; word matching compares spelling, not meaning
- [ ] C) Cosine similarity cannot handle short titles
- [ ] D) The stop-word list removed every word

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Word-based methods cannot tell that "voucher" means "coupon" or "basket" means "cart". Their blind spot is meaning.
- **Why others are wrong:**
  - A) A score of exactly 0.00 means there was no overlap at all, whatever the threshold.
  - C) Short titles work fine. The issue is that no words were shared.
  - D) Words like "voucher" and "basket" are not stop words.
</details>

---

### 20. What is an embedding?
- [ ] A) A hand-written list of synonyms
- [ ] B) A learned vector in which similar meanings get similar numbers
- [ ] C) A count of how often each word appears
- [ ] D) A compressed copy of the training data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** A neural network learns embeddings from large amounts of text, based on the idea that words in similar contexts have similar meanings.
- **Why others are wrong:**
  - A) Embeddings are learned, not written by hand.
  - C) That is bag of words.
  - D) An embedding represents meaning. It does not store the data.
</details>

---

### 21. In one sentence, what does an LLM do when it generates text?
- [ ] A) It searches a database for the best matching sentence
- [ ] B) It repeatedly predicts a probability for each possible next token, picks one, appends it, and repeats
- [ ] C) It looks up facts online and summarises them
- [ ] D) It translates a hidden rule set into English

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Generation is next-token prediction plus sampling. Nothing in that loop looks up or checks facts.
- **Why others are wrong:**
  - A) LLMs do not retrieve stored sentences. They generate token by token.
  - C) The core loop has no fact lookup, which is why hallucinations happen.
  - D) There is no hand-written rule set inside an LLM.
</details>

---

### 22. Roughly how many English words are 100 tokens?
- [ ] A) About 25
- [ ] B) About 75
- [ ] C) About 100
- [ ] D) About 400

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) About 75

**Explanation:** A token is about three-quarters of an English word on average.
- **Why others are wrong:**
  - A) That would mean 4 tokens per word, which is far too many.
  - C) Tokens are often parts of words, so it is not one to one.
  - D) That would mean each token holds several words.
</details>

---

### 23. A long chat starts ignoring a rule you gave in your first message. What is the likely cause?
- [ ] A) The model has been retrained mid-chat
- [ ] B) The early message has dropped out of the context window, or gets little attention among a lot of text
- [ ] C) The temperature has automatically increased
- [ ] D) The knowledge cut-off has passed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** The context window is short-term memory counted in tokens. Restate the rule or start a new chat.
- **Why others are wrong:**
  - A) Models are not retrained during your chat.
  - C) Temperature is a fixed setting. It does not drift over a conversation.
  - D) The knowledge cut-off concerns training data dates, not your messages.
</details>

---

### 24. An AI confidently explains a pytest function. What is the right way to check it exists?
- [ ] A) Ask the AI "Are you sure?"
- [ ] B) Look it up in the official docs (docs.pytest.org) or run code that uses it
- [ ] C) Trust it if the explanation is detailed
- [ ] D) Ask a different chat with the same AI

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Check every fact, function and package against official documentation or by running code.
- **Why others are wrong:**
  - A) The same model can confidently repeat its error.
  - C) Fluent does not mean correct. Detail is not evidence.
  - D) Another chat with the same model is still not an independent source.
</details>

---

### 25. Three of four AI-drafted tests fail against a `cart.py` that is known to be correct. What does that tell you?
- [ ] A) The code is wrong
- [ ] B) Only that the tests and the code disagree; the requirement decides which is wrong
- [ ] C) pytest is misconfigured
- [ ] D) The AI needs a higher temperature

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Failing tests do not prove the code is wrong. Here the code was correct and the tests were wrong.
- **Why others are wrong:**
  - A) That jumps to a conclusion without checking the requirement.
  - C) Nothing points to a configuration problem.
  - D) Higher temperature makes output more random, not more correct.
</details>

---

### 26. The AI draft includes `test_coupon_is_case_insensitive`, but the requirement says nothing about lowercase codes. What should you do?
- [ ] A) Keep it, because it is extra coverage
- [ ] B) Fix the code so lowercase works
- [ ] C) Remove it, note why, and ask the business analyst
- [ ] D) Mark it as skipped forever

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C)

**Explanation:** It is an invented requirement (a hallucination). Keeping it would quietly change the requirement.
- **Why others are wrong:**
  - A) Coverage of a rule nobody asked for is not coverage.
  - B) Changing the code to fit an invented test changes the product without approval.
  - D) Skipping it hides the question instead of resolving it.
</details>

---

### 27. When should you use ordinary code instead of GenAI for a testing task?
- [ ] A) Never; GenAI is always faster
- [ ] B) When the rule can be written down exactly, such as checking for HTTP 200
- [ ] C) Only when GenAI tools are unavailable
- [ ] D) When the input is messy natural language

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B)

**Explanation:** Code is exact, fast, free and gives the same answer every time. Use labelled history for classic ML, and messy language or drafting for GenAI.
- **Why others are wrong:**
  - A) GenAI is slower, costs more and is non-deterministic for exact rules.
  - C) Code is often the better choice even when GenAI is available.
  - D) Messy language is where GenAI fits best.
</details>

---

## Part 2: True / False

### 28. True or False: Hallucinations come from a different mechanism than an LLM's correct answers.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Both come from the same mechanism: producing likely text. That is why fluent output can still be false.
</details>

---

### 29. True or False: Setting a low temperature makes an LLM's output more predictable and less varied.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Low temperature sharpens the probabilities, so the most likely token is chosen almost every time.
</details>

---

### 30. True or False: Because of sampling, the same prompt can give different answers, so you should test AI output over several runs.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** LLMs are non-deterministic. One good run does not prove the next run will be good.
</details>

---

### 31. True or False: Passing tests prove that the code is correct.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A test using $100 passes with either `>` or `>=`, so the boundary bug ships. Every test must be able to fail.
</details>

---

### 32. True or False: Deep learning learns its own features from messy data, but at the cost of more data, more compute and rules people cannot read.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** That is the trade-off between deep learning and simpler models such as a readable decision tree.
</details>

---

### 33. True or False: Scaling the features before clustering has no effect on the groups k-means finds.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Scaling changes what the algorithm finds, because without it a feature with a large range dominates the distances.
</details>

---

### 34. True or False: If an AI gives a correct prediction, the reason it gives must also be correct.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A reason you cannot trace to the data is a guess, even when the prediction is right. Check every reason against the data.
</details>

---

### 35. True or False: Classic word matching can be preferable to an AI assistant because it is cheap, repeatable, explainable and runs locally.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The recommended pattern is to use both: cheap word matching to narrow the field, then meaning-based judgement from an AI or a person.
</details>

---

### 36. True or False: In this week's course, "testing of AI" (testing products that contain AI) is the main focus.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** This week covers **AI for testing**, which means using AI tools to help with testing work.
</details>

---

### 37. True or False: A single neuron can learn the XOR pattern ("exactly one of two is true").
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** XOR needs layers with non-linear activations. One neuron cannot learn it.
</details>

---

### 38. True or False: In GenAI use-case scoring, an idea that scores low can sometimes be redesigned, for example "AI drafts, a person decides", to raise its score.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Having the AI draft a release-readiness summary instead of deciding raises both the risk score (a person decides) and checkability (every line traces to the test report).
</details>

---

## Part 3: Code Prediction

### 39. What does this code print?
```python
import re
STOP_WORDS = {"a", "an", "the", "is", "on", "once", "does", "after", "when", "are", "two"}

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return [w for w in text.split() if w not in STOP_WORDS]

print(clean("Login does NOT work on Safari!"))
```
- [ ] A) `['login', 'work', 'safari']`
- [ ] B) `['login', 'not', 'work', 'safari']`
- [ ] C) `['Login', 'NOT', 'work', 'Safari']`
- [ ] D) `['login', 'does', 'not', 'work', 'on', 'safari']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['login', 'not', 'work', 'safari']`

**Explanation:** The text is lowercased, "!" becomes a space, and "does" and "on" are removed as stop words. "not" is not in this list, so it survives.
- **Why others are wrong:**
  - A) "not" would only disappear if it were in `STOP_WORDS`. It is not.
  - C) `text.lower()` runs first, so no capitals remain.
  - D) "does" and "on" are both in `STOP_WORDS`.
</details>

---

### 40. A neuron uses a step activation (output 1 if z > 0, else 0). What does this print?
```python
inputs = [1, 0, 1]
weights = [2.0, 0.5, 1.5]
bias = -3.0
z = sum(i * w for i, w in zip(inputs, weights)) + bias
print(z, 1 if z > 0 else 0)
```
- [ ] A) `-0.5 0`
- [ ] B) `0.5 1`
- [ ] C) `3.5 1`
- [ ] D) `0.0 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `0.5 1`

**Explanation:** 2.0×1 + 0.5×0 + 1.5×1 = 3.5, then 3.5 − 3.0 = 0.5. Since 0.5 > 0, the step outputs 1.
- **Why others are wrong:**
  - A) −0.5 is the result for inputs [1, 1, 0].
  - C) 3.5 is the weighted sum before the bias is added.
  - D) z is not zero, so the output is not 0.
</details>

---

### 41. What does this print?
```python
relu = lambda z: max(0, z)
print([relu(v) for v in [-2, 0, 3.5]])
```
- [ ] A) `[2, 0, 3.5]`
- [ ] B) `[0, 0, 3.5]`
- [ ] C) `[0, 1, 1]`
- [ ] D) `[-2, 0, 3.5]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[0, 0, 3.5]`

**Explanation:** ReLU outputs 0 for negative z and z otherwise.
- **Why others are wrong:**
  - A) ReLU does not take the absolute value.
  - C) That looks like a step function, not ReLU.
  - D) Negative values are clipped to 0.
</details>

---

### 42. What does this print?
```python
tp, fp, fn = 8, 2, 8
precision = tp / (tp + fp)
recall = tp / (tp + fn)
print(precision, recall)
```
- [ ] A) `0.5 0.8`
- [ ] B) `0.8 0.5`
- [ ] C) `0.8 0.8`
- [ ] D) `1.0 0.5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `0.8 0.5`

**Explanation:** Precision = 8 ÷ 10 = 0.8 (most warnings were right). Recall = 8 ÷ 16 = 0.5 (half of the real problems were missed).
- **Why others are wrong:**
  - A) This swaps the two metrics.
  - C) Recall uses false negatives, not false positives.
  - D) There were 2 false alarms, so precision cannot be 1.0.
</details>

---

### 43. This version of `apply_coupon` contains a bug. What does it print?
```python
def apply_coupon(total, code):
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon: {code}")
    if total > 50:
        return round(total * 0.9, 2)
    return total

print(apply_coupon(50, "SAVE10"), apply_coupon(100, "SAVE10"))
```
- [ ] A) `45.0 90.0`
- [ ] B) `50 90.0`
- [ ] C) `50 100`
- [ ] D) `ValueError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `50 90.0`

**Explanation:** With `>`, exactly $50 gets no discount, which breaks the "$50.00 or more" rule. $100 is still discounted. This is why a $100-only test misses the bug and a boundary test at $50.00 catches it.
- **Why others are wrong:**
  - A) 45.0 would be correct behaviour (`>=`), not this buggy code.
  - C) $100 is above 50, so it is discounted to 90.0.
  - D) "SAVE10" is a valid code.
</details>

---

### 44. Using the *correct* rule (`total >= 50`), what does this print?
```python
print(apply_coupon(49.99, "SAVE10"), apply_coupon(50, "SAVE10"))
```
- [ ] A) `44.99 45.0`
- [ ] B) `49.99 45.0`
- [ ] C) `49.99 50`
- [ ] D) `45.0 45.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `49.99 45.0`

**Explanation:** $49.99 is the last value without a discount, and $50.00 is the first value with one. These are the Boundary Value Analysis pair.
- **Why others are wrong:**
  - A) Orders under $50 are unchanged, not discounted.
  - C) $50 qualifies under `>=`.
  - D) $49.99 does not qualify.
</details>

---

### 45. What does this print?
```python
try:
    apply_coupon(80, "save10")
except ValueError as ex:
    print(ex)
```
- [ ] A) `72.0`
- [ ] B) `80`
- [ ] C) `Unknown coupon: save10`
- [ ] D) Nothing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Unknown coupon: save10`

**Explanation:** The comparison is case-sensitive, so "save10" is not "SAVE10" and a ValueError is raised. The requirement never says lowercase codes are accepted, which is why the AI's case-insensitive test was an invented requirement.
- **Why others are wrong:**
  - A) That would require a case-insensitive check, which the code does not have.
  - B) Unknown codes must raise an error, not return the total.
  - D) The `except` block prints the message.
</details>

---

### 46. A model always predicts "pass". What does this print?
```python
preds  = ["pass"] * 100
actual = ["pass"] * 98 + ["fail"] * 2
acc = sum(p == a for p, a in zip(preds, actual)) / 100
rec = sum(p == "fail" and a == "fail" for p, a in zip(preds, actual)) / 2
print(acc, rec)
```
- [ ] A) `0.98 1.0`
- [ ] B) `0.98 0.0`
- [ ] C) `0.02 0.0`
- [ ] D) `1.0 0.98`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `0.98 0.0`

**Explanation:** This is the accuracy paradox: 98% accuracy, yet it catches zero of the failures.
- **Why others are wrong:**
  - A) It never predicts "fail", so recall cannot be 1.0.
  - C) 98 of the 100 predictions match.
  - D) Two predictions are wrong, so accuracy is not 1.0.
</details>

---

## Part 4: Fill-in-the-Blank

### 47. A network has 4 inputs, one hidden layer of 3 neurons and 2 outputs. It has `_____` parameters (weights + biases).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 23

**Explanation:** Hidden layer: 3 × (4 + 1) = 15. Output layer: 2 × (3 + 1) = 8. Total: 15 + 8 = 23. Each neuron has one weight per input plus one bias.
</details>

---

### 48. The `_____` window is an LLM's short-term memory, measured in tokens.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** context

**Explanation:** Long chats or huge pastes can push earlier content out of the context window.
</details>

---

### 49. `_____` works backwards from the output error to find each weight's share of the blame, and `_____` adjusts the weights in the direction that reduces the loss fastest.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Backpropagation; gradient descent

**Explanation:** Gradient descent does the nudging, and backpropagation shares out the blame.
</details>

---

### 50. The three classic AI test mistakes are contradicting the requirement, `_____` a requirement, and missing cases such as `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** inventing; boundaries

**Explanation:** Review every AI test against the requirement: contradicting, inventing and missing, especially boundary values such as $50.00 and $49.99.
</details>
