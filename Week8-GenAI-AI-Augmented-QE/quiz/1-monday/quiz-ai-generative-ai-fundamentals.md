# Daily Knowledge Check: Week 8 Monday - AI & Generative AI Fundamentals

This check covers AI, machine learning and deep learning; supervised vs. unsupervised learning; neural network fundamentals; NLP fundamentals; Generative AI concepts; and Generative AI applications within QE. Try each question on your own first, then open the solution to check your reasoning.

---

## Part 1: Multiple Choice

### 1. Which statement correctly describes the nesting of AI, ML, DL and Generative AI?

- [ ] A) Machine Learning contains AI, which contains Deep Learning
- [ ] B) AI contains Machine Learning, which contains Deep Learning, which contains Generative AI
- [ ] C) Deep Learning contains Machine Learning, which contains AI
- [ ] D) Generative AI and Deep Learning are separate fields that do not overlap

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) AI contains Machine Learning, which contains Deep Learning, which contains Generative AI

**Explanation:** The lesson's "nested circles" picture reads from the outside in: AI ⊃ ML ⊃ DL ⊃ Generative AI. All DL is ML and all ML is AI, but not the other way round.
- **Why others are wrong:**
  - A) AI is the outermost circle; ML sits inside it, not around it.
  - C) This reverses the nesting completely.
  - D) Today's Generative AI is built almost entirely with deep learning, so it sits inside DL.

</details>

### 2. A 1990s chess program that follows rules hand-written by experts is best described as:

- [ ] A) Machine learning, because it plays a game
- [ ] B) Deep learning, because it is complex
- [ ] C) AI, but not machine learning
- [ ] D) Not AI at all, because nothing is learned

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) AI, but not machine learning

**Explanation:** AI is defined by intelligent *behaviour*, not by technique. Rule-based (symbolic) systems count as AI even though they learn nothing from data.
- **Why others are wrong:**
  - A) Machine learning means learning patterns from data; this program's rules were written by humans.
  - B) Deep learning means many-layered neural networks; complexity alone does not make something DL.
  - D) Rule-based expert systems are a classic form of AI.

</details>

### 3. What is the key difference between traditional programming and machine learning?

- [ ] A) Traditional programming uses Python; ML uses special languages
- [ ] B) In traditional programming humans write the rules; in ML the algorithm learns the rules from examples of inputs and correct outputs
- [ ] C) ML never needs data; traditional programming always does
- [ ] D) Traditional programs can be tested; ML models cannot

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) In traditional programming humans write the rules; in ML the algorithm learns the rules from examples of inputs and correct outputs

**Explanation:** Traditional programming is "rules + data → answers"; ML training is "data + answers → rules (a model)".
- **Why others are wrong:**
  - A) Both are commonly written in Python (the lesson uses scikit-learn).
  - C) It is the reverse: ML is defined by learning from data.
  - D) ML models can be tested by their behaviour on inputs, which is black-box testing.

</details>

### 4. Which of these is a *hyperparameter* rather than a parameter?

- [ ] A) A neural network weight adjusted during training
- [ ] B) A neuron's bias value learned by gradient descent
- [ ] C) The `max_depth` of a decision tree chosen before training
- [ ] D) The thresholds a decision tree discovers inside `fit()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The `max_depth` of a decision tree chosen before training

**Explanation:** Hyperparameters are set by a human *before* training; parameters are learned *during* training.
- **Why others are wrong:**
  - A) Weights are learned parameters.
  - B) Biases are learned parameters too.
  - D) Split thresholds are learned from the data during `fit()`.

</details>

### 5. A teammate reports "training accuracy 99.8%, test accuracy 71%". What is most likely happening?

- [ ] A) Underfitting
- [ ] B) Overfitting
- [ ] C) Data drift in production
- [ ] D) The model is working perfectly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Overfitting

**Explanation:** A very high training score with a much lower test score means the model memorised the training data (including its noise) and does not generalise.
- **Why others are wrong:**
  - A) Underfitting shows low scores on *both* training and test data.
  - C) Drift happens after deployment as the real world changes; this gap appears at evaluation time.
  - D) A 29-point gap is a clear warning sign.

</details>

### 6. Why do we keep a test set separate from the training set?

- [ ] A) To make training faster
- [ ] B) To get an honest estimate of performance on unseen data
- [ ] C) Because scikit-learn refuses to train on all the data
- [ ] D) To increase the number of features

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) To get an honest estimate of performance on unseen data

**Explanation:** Evaluating on training data lets a model "score 100%" by memorising, like students who saw the exam as homework. The held-back test set exposes overfitting.
- **Why others are wrong:**
  - A) Speed is not the reason; holding data back is about honest evaluation.
  - C) The library will happily train on everything; the split is a methodology choice.
  - D) Splitting divides rows (examples), not columns (features).

</details>

### 7. Which three factors are given as the reason deep learning took off in the 2010s?

- [ ] A) Cheaper keyboards, faster internet and cloud storage
- [ ] B) Large datasets, GPU compute and better training techniques
- [ ] C) The invention of Python, NumPy and pytest
- [ ] D) Symbolic AI, expert systems and decision trees

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Large datasets, GPU compute and better training techniques

**Explanation:** Data (e.g. ImageNet), GPUs built for gaming, and improved training methods arrived together; AlexNet's 2012 ImageNet win was a turning point.
- **Why others are wrong:**
  - A) These are not the factors the lesson identifies.
  - C) Python tools help practitioners but did not cause the breakthrough.
  - D) These are older, non-deep approaches.

</details>

### 8. Compared with classic ML, deep learning typically:

- [ ] A) Needs less data and is easier to explain
- [ ] B) Learns features automatically from raw data but needs more data and compute
- [ ] C) Works only on tabular data
- [ ] D) Always beats a decision tree on small problems

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Learns features automatically from raw data but needs more data and compute

**Explanation:** DL's big advantage is feature learning on unstructured data (images, text, audio), at the cost of more data, more compute and less interpretability.
- **Why others are wrong:**
  - A) DL usually needs *more* data and is *harder* to explain.
  - C) Classic ML is the one most associated with tabular data; DL shines on unstructured data.
  - D) The lesson says a neural network is not guaranteed to beat a decision tree on a tiny tabular problem.

</details>

### 9. Which single question best decides between supervised and unsupervised learning?

- [ ] A) "Is the dataset bigger than 1,000 rows?"
- [ ] B) "Do we have labels (known correct answers) for the training data?"
- [ ] C) "Are we using a neural network?"
- [ ] D) "Will the model run on a GPU?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "Do we have labels (known correct answers) for the training data?"

**Explanation:** Supervised learning learns from inputs paired with labels; unsupervised learning has inputs only and discovers structure.
- **Why others are wrong:**
  - A) Dataset size does not define the family.
  - C) Neural networks can be used in both settings.
  - D) Hardware is irrelevant to the distinction.

</details>

### 10. "Predict how many minutes a Playwright suite will take on a new branch" is an example of:

- [ ] A) Binary classification
- [ ] B) Regression
- [ ] C) Clustering
- [ ] D) Anomaly detection

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Regression

**Explanation:** The label is a number with units (minutes). The lesson's rule of thumb: units → regression; a category → classification.
- **Why others are wrong:**
  - A) Classification predicts a category, not a quantity.
  - C) Clustering is unsupervised grouping without labels.
  - D) Anomaly detection flags unusual items; it does not predict a duration.

</details>

### 11. A bug tagged both "UI" and "accessibility" at the same time is an example of which task?

- [ ] A) Binary classification
- [ ] B) Multi-class classification
- [ ] C) Multi-label classification
- [ ] D) Regression

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Multi-label classification

**Explanation:** Multi-label means an example can have several labels at once.
- **Why others are wrong:**
  - A) Binary has exactly two classes and one label per example.
  - B) Multi-class has more than two classes but exactly *one* per example.
  - D) Regression predicts a number.

</details>

### 12. When does **precision** matter most?

- [ ] A) When missing a real problem is very expensive
- [ ] B) When false alarms are very expensive, such as paging an on-call engineer at 3 a.m.
- [ ] C) Only when classes are perfectly balanced
- [ ] D) When the model predicts numbers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) When false alarms are very expensive, such as paging an on-call engineer at 3 a.m.

**Explanation:** Precision = TP / (TP + FP): "when it raises an alarm, how often is it real?" It drops with every false positive.
- **Why others are wrong:**
  - A) That describes recall, which counts missed problems (FN).
  - C) That condition relates to when *accuracy* is meaningful.
  - D) Number prediction is regression, which uses error metrics such as MAE.

</details>

### 13. Only 2% of builds fail. A model that always predicts "passed" is 98% accurate. What is this called?

- [ ] A) The accuracy paradox
- [ ] B) Data leakage
- [ ] C) Gradient vanishing
- [ ] D) The elbow method

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The accuracy paradox

**Explanation:** High accuracy hides zero recall on the rare class you care about. Always ask for precision and recall on that class.
- **Why others are wrong:**
  - B) Leakage is when a feature secretly contains the answer.
  - C) Vanishing gradients is a deep-network training problem.
  - D) The elbow method helps choose k for k-means.

</details>

### 14. Why does F1 use the harmonic mean instead of an ordinary average?

- [ ] A) It is faster to calculate
- [ ] B) It is pulled towards the smaller value, so F1 is only high when both precision and recall are high
- [ ] C) It always equals accuracy
- [ ] D) It ignores false negatives

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is pulled towards the smaller value, so F1 is only high when both precision and recall are high

**Explanation:** The "only alarms when certain" model (precision 1.00, recall 0.10) has an ordinary average of 0.55 but F1 of only 0.18, exposing the weakness.
- **Why others are wrong:**
  - A) Speed is not the reason.
  - C) F1 and accuracy are different metrics.
  - D) F1 uses recall, which depends on false negatives.

</details>

### 15. You lower a classifier's decision threshold from 0.5 to 0.3. What usually happens?

- [ ] A) Fewer alarms; precision rises and recall falls
- [ ] B) More alarms; recall rises and precision falls
- [ ] C) Both precision and recall rise
- [ ] D) Nothing changes because the model is not retrained

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) More alarms; recall rises and precision falls

**Explanation:** In the lesson's output, threshold 0.3 raised 166 alarms (precision 0.56, recall 0.82) versus 116 at 0.5 (precision 0.64, recall 0.65).
- **Why others are wrong:**
  - A) That is what happens when you *raise* the threshold.
  - C) You cannot maximise both with the same model; the threshold trades one for the other.
  - D) The threshold changes predictions without retraining.

</details>

### 16. Which team decision should favour a **low** threshold (high recall)?

- [ ] A) Block the merge and page a senior engineer
- [ ] B) Automatically run the full regression suite when risk is high
- [ ] C) Post a public incident report
- [ ] D) Delete flaky tests automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Automatically run the full regression suite when risk is high

**Explanation:** Missing a failure is costly and running extra tests is cheap, so you want to catch as many risky builds as possible.
- **Why others are wrong:**
  - A) False alarms annoy people and erode trust, so this favours a high threshold (precision).
  - C) and D) These are costly or destructive actions where false alarms are harmful, so they would not favour a low threshold.

</details>

### 17. In k-means clustering, what does the algorithm output, and what must a human still do?

- [ ] A) Named categories such as "timeout"; nothing more is needed
- [ ] B) A cluster number for each example (and centres); a human must interpret what each cluster means
- [ ] C) A probability of failure for each test
- [ ] D) A list of labels that were in the training data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A cluster number for each example (and centres); a human must interpret what each cluster means

**Explanation:** k-means returns 0, 1, 2… with no meaning attached. A person looks at the averages and says "this cluster = memory leaks".
- **Why others are wrong:**
  - A) The algorithm never names clusters.
  - C) That is a supervised classifier output.
  - D) Clustering uses no labels at all.

</details>

### 18. Why is `StandardScaler` essential before k-means in the failure-clustering example?

- [ ] A) k-means only accepts integers
- [ ] B) k-means measures distance, so a large-valued feature (memory in MB) would dominate a small one (duration in seconds)
- [ ] C) It removes outliers automatically
- [ ] D) It adds labels to the data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) k-means measures distance, so a large-valued feature (memory in MB) would dominate a small one (duration in seconds)

**Explanation:** Scaling puts features on comparable ranges so each contributes fairly to distance.
- **Why others are wrong:**
  - A) k-means works with real numbers.
  - C) Scaling rescales values; it does not remove anything.
  - D) Scaling never creates labels.

</details>

### 19. A model predicting whether a release fails uses the feature `was_rolled_back`. Test scores look amazing. What is the problem?

- [ ] A) Class imbalance
- [ ] B) Data leakage: the feature would not be known at prediction time
- [ ] C) Underfitting
- [ ] D) Unscaled features

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Data leakage: the feature would not be known at prediction time

**Explanation:** A rollback happens *because* a release failed, so the feature secretly contains the answer. Ask of every feature: "Would I really know this value at prediction time?"
- **Why others are wrong:**
  - A) Imbalance is about rare classes, not leaked answers.
  - C) Underfitting produces poor scores, not amazing ones.
  - D) Scaling does not explain suspiciously perfect scores.

</details>

### 20. How are large language models **pre-trained**?

- [ ] A) Supervised learning on hand-labelled bug reports
- [ ] B) Self-supervised learning: predict the hidden next token, using the real next token as the label
- [ ] C) Unsupervised k-means clustering of documents
- [ ] D) Rule-based expert systems

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Self-supervised learning: predict the hidden next token, using the real next token as the label

**Explanation:** In self-supervised learning the data creates its own labels; this lets LLMs learn from enormous unlabelled text collections.
- **Why others are wrong:**
  - A) Hand-labelling at that scale is impossible; supervised fine-tuning comes later.
  - C) Clustering is not how LLMs learn to predict text.
  - D) LLMs are deep learning models, not hand-written rule systems.

</details>

### 21. What three things does a single artificial neuron do?

- [ ] A) Sort inputs, delete the smallest, return the largest
- [ ] B) Multiply each input by a weight, sum them and add a bias, then apply an activation function
- [ ] C) Store a training example, compare it with new input, return a label
- [ ] D) Split the data, train a tree, return accuracy

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Multiply each input by a weight, sum them and add a bias, then apply an activation function

**Explanation:** `z = w1*x1 + w2*x2 + … + b`, then `output = f(z)`.
- **Why others are wrong:**
  - A) Neurons do not sort or discard inputs.
  - C) That resembles k-nearest neighbours, not a neuron.
  - D) That describes an ML workflow, not a neuron.

</details>

### 22. Why do neural networks need **non-linear** activation functions?

- [ ] A) To make training deterministic
- [ ] B) Without them, stacked layers collapse into a single linear function and cannot model patterns like XOR
- [ ] C) To reduce the number of parameters
- [ ] D) Because GPUs cannot multiply matrices without them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Without them, stacked layers collapse into a single linear function and cannot model patterns like XOR

**Explanation:** A linear function of a linear function is still linear, so depth adds nothing. Non-linear "bends" let the network represent complex decision boundaries.
- **Why others are wrong:**
  - A) Activations do not remove randomness from training.
  - C) Activations add no parameters and do not remove any.
  - D) Matrix multiplication works regardless of activation.

</details>

### 23. Which activation function is the usual default for hidden layers in modern networks?

- [ ] A) Step
- [ ] B) Softmax
- [ ] C) ReLU
- [ ] D) Identity

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) ReLU

**Explanation:** ReLU, `max(0, z)`, is simple and fast and is the default for hidden layers in most modern networks.
- **Why others are wrong:**
  - A) Step has no useful slope, so it is not used to train modern networks.
  - B) Softmax is used in output layers for multi-class probabilities.
  - D) An identity (linear) activation would make stacked layers collapse into one.

</details>

### 24. If the learning rate is far too large, what typically happens during training?

- [ ] A) Training is slow but steady
- [ ] B) Steps overshoot the valley; the loss jumps around or explodes
- [ ] C) The network becomes deterministic
- [ ] D) The number of parameters grows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Steps overshoot the valley; the loss jumps around or explodes

**Explanation:** The learning rate is the step size in gradient descent; too large and you leap past the minimum.
- **Why others are wrong:**
  - A) Slow, steady progress is the symptom of a learning rate that is too *small*.
  - C) The learning rate does not control randomness.
  - D) Parameter count is fixed by the architecture.

</details>

### 25. In one sentence, what does **backpropagation** do?

- [ ] A) Runs inputs forward to produce a prediction
- [ ] B) Works backwards from the output error, using the chain rule, to compute how much each weight contributed (its gradient)
- [ ] C) Randomly switches off neurons during training
- [ ] D) Splits data into training and test sets

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Works backwards from the output error, using the chain rule, to compute how much each weight contributed (its gradient)

**Explanation:** Backpropagation computes gradients efficiently layer by layer; gradient descent then uses them to update the weights.
- **Why others are wrong:**
  - A) That is the forward pass.
  - C) That is dropout, a remedy for overfitting.
  - D) That is the train/test split.

</details>

### 26. Which neural network architecture underlies today's large language models?

- [ ] A) Convolutional Neural Network (CNN)
- [ ] B) Recurrent Neural Network (RNN/LSTM)
- [ ] C) Transformer
- [ ] D) Single perceptron

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Transformer

**Explanation:** Introduced in 2017 ("Attention Is All You Need"), the Transformer's self-attention lets every token look at every other token.
- **Why others are wrong:**
  - A) CNNs are designed for images.
  - B) RNNs read one item at a time and were largely replaced by Transformers for language.
  - D) A single perceptron cannot even learn XOR.

</details>

### 27. What is the key difference between **stemming** and **lemmatisation**?

- [ ] A) Stemming uses grammar; lemmatisation chops endings
- [ ] B) Stemming chops endings with crude rules (may produce non-words); lemmatisation uses vocabulary and grammar to find the dictionary form
- [ ] C) They are identical
- [ ] D) Lemmatisation only works on numbers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Stemming chops endings with crude rules (may produce non-words); lemmatisation uses vocabulary and grammar to find the dictionary form

**Explanation:** NLTK's Porter stemmer turned "studies" into "studi"; spaCy's lemmatiser returned "study" and turned "ran" into "run".
- **Why others are wrong:**
  - A) This reverses the two techniques.
  - C) They produced clearly different output in the lesson's table.
  - D) Lemmatisation works on words.

</details>

### 28. Why is removing **"not"** as a stop word risky?

- [ ] A) It makes the vocabulary too large
- [ ] B) It destroys negation, so "login does not fail" and "login does fail" look the same
- [ ] C) It breaks tokenisation of URLs
- [ ] D) Stop words are required by TF-IDF

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It destroys negation, so "login does not fail" and "login does fail" look the same

**Explanation:** A single word can flip the meaning; dropping it can make a bug-triage tool misread reports.
- **Why others are wrong:**
  - A) Removing words makes the vocabulary smaller, not larger.
  - C) "not" has nothing to do with URLs.
  - D) TF-IDF works with or without stop-word removal.

</details>

### 29. What problem does **TF-IDF** solve compared with raw word counts?

- [ ] A) It preserves word order
- [ ] B) It down-weights words that appear in almost every document and highlights distinctive ones
- [ ] C) It understands synonyms
- [ ] D) It produces contextual embeddings

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It down-weights words that appear in almost every document and highlights distinctive ones

**Explanation:** Inverse Document Frequency gives common words (like "test" in a test log collection) low weight and rare, distinctive words (like "coupon") high weight.
- **Why others are wrong:**
  - A) Like bag-of-words, TF-IDF ignores word order.
  - C) TF-IDF matches words, not meanings; synonyms share nothing.
  - D) Contextual embeddings come from Transformer models.

</details>

### 30. A new report says "Apple browser: purchase CTA unresponsive after promo code". TF-IDF similarity to BUG-101 ("Checkout button does nothing on Safari after applying a coupon") is near zero. What fixes this?

- [ ] A) Removing more stop words
- [ ] B) Semantic search with sentence embeddings, which match meaning rather than words
- [ ] C) Lowering the classifier threshold
- [ ] D) Using a stemmer

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Semantic search with sentence embeddings, which match meaning rather than words

**Explanation:** Embeddings learned from huge amounts of text place "Safari"/"Apple browser" and "coupon"/"promo code" close together, so the duplicate is found.
- **Why others are wrong:**
  - A) More stop-word removal leaves even fewer shared words.
  - C) Thresholds apply to classifiers, not to missing word overlap.
  - D) Stemming reduces word endings but cannot connect different words.

</details>

### 31. In Byte-Pair Encoding (BPE), what decides which two symbols are merged next?

- [ ] A) Their meaning
- [ ] B) Alphabetical order
- [ ] C) Frequency: the most common neighbouring pair (weighted by word counts)
- [ ] D) A random choice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Frequency: the most common neighbouring pair (weighted by word counts)

**Explanation:** Merges follow frequency, not meaning, which is why "tester" ended up split as `tes | te | r`.
- **Why others are wrong:**
  - A) BPE has no notion of meaning.
  - B) Order of the alphabet plays no role.
  - D) The process is deterministic counting, not random.

</details>

### 32. What is the core mechanism by which an LLM generates text?

- [ ] A) It looks up the answer in a database of facts
- [ ] B) It repeatedly predicts a probability distribution over the next token, samples one, appends it and repeats
- [ ] C) It searches the web for each sentence
- [ ] D) It copies the closest document from its training data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It repeatedly predicts a probability distribution over the next token, samples one, appends it and repeats

**Explanation:** This is autoregressive generation; each new token depends on all previous ones, including ones the model just produced.
- **Why others are wrong:**
  - A) The lesson calls "it looks things up in a database" a wrong mental model.
  - C) A base LLM has no built-in web access; tools must supply it.
  - D) LLMs generate new token sequences rather than copying documents.

</details>

### 33. Which training stage turns a base model that "just continues text" into one that follows requests like "Summarise this log"?

- [ ] A) Pre-training
- [ ] B) Fine-tuning / instruction tuning
- [ ] C) Tokenisation
- [ ] D) Inference

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Fine-tuning / instruction tuning

**Explanation:** Supervised training on curated instruction/response examples teaches the model to follow requests. Alignment (e.g. RLHF) then makes it more helpful and safe.
- **Why others are wrong:**
  - A) Pre-training produces the base model that only continues text.
  - C) Tokenisation splits text; it is not a training stage.
  - D) Inference is using a trained model, not training it.

</details>

### 34. Which statement about the **context window** is correct?

- [ ] A) It counts only the output tokens
- [ ] B) It is the maximum number of tokens (input plus output) the model can consider at once, and LLMs have no memory between separate requests by default
- [ ] C) More context always produces better answers
- [ ] D) It is measured in characters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is the maximum number of tokens (input plus output) the model can consider at once, and LLMs have no memory between separate requests by default

**Explanation:** Chat apps create the illusion of memory by re-sending the history each time.
- **Why others are wrong:**
  - A) It includes instructions, pasted content, history *and* the generated output.
  - C) The lesson says more context is not automatically better context.
  - D) Limits are measured in tokens.

</details>

### 35. Why do LLMs **hallucinate**?

- [ ] A) Because the temperature is always too high
- [ ] B) They generate statistically plausible continuations rather than verified facts, and nothing in the basic generation loop checks truth
- [ ] C) Because their training data contains no facts
- [ ] D) Because they are deliberately programmed to lie

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) They generate statistically plausible continuations rather than verified facts, and nothing in the basic generation loop checks truth

**Explanation:** Fluency and confidence are not evidence of correctness; hallucinated output often looks exactly like correct output.
- **Why others are wrong:**
  - A) Low temperature reduces variety but does not add fact-checking.
  - C) Training data contains plenty of facts; the problem is the lack of a verification step.
  - D) There is no intent involved.

</details>

### 36. Which pairing of task and best-fit approach matches the lesson?

- [ ] A) Check a field accepts at most 50 characters → GenAI
- [ ] B) Group 20,000 nightly failure messages → classic ML/NLP (TF-IDF + clustering)
- [ ] C) Summarise an 80-message defect thread for a manager → no AI
- [ ] D) Predict likely failing tests from labelled CI history → GenAI only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Group 20,000 nightly failure messages → classic ML/NLP (TF-IDF + clustering)

**Explanation:** Classic NLP is fast, cheap, repeatable and runs offline at scale.
- **Why others are wrong:**
  - A) A deterministic rule needs a normal parametrised pytest test; AI only adds variability.
  - C) Summarising for a specific audience is a natural GenAI task.
  - D) Numeric, tabular, labelled history is a classic supervised ML problem.

</details>

### 37. When evaluating a GenAI use case, which criterion does the lesson say beginners most often overlook, yet is the most important for QE?

- [ ] A) Effort to adopt
- [ ] B) Frequency
- [ ] C) Verifiability
- [ ] D) Value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Verifiability

**Explanation:** If checking AI output takes as long as doing the work, the benefit disappears; if it cannot be checked, the risk is high. Habit: name who checks the output and how.
- **Why others are wrong:**
  - A), B), D) These all matter, but the lesson singles out verifiability as the most overlooked and most important.

</details>

---

## Part 2: True/False

### 38. True or False: Every AI product you use today, including large language models, is considered narrow AI.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The lesson states every AI product in use today is narrow AI, even LLMs that cover a wide range of language tasks. AGI remains hypothetical and debated.

</details>

### 39. True or False: Adding more data always fixes a model.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** More *bad* or *biased* data makes a model worse. Data quality beats quantity ("garbage in, garbage out").

</details>

### 40. True or False: Once trained and deployed, an ML model stays correct indefinitely.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The world changes (new browsers, features, user behaviour), so models **drift** and need monitoring and retraining.

</details>

### 41. True or False: Every clustering run produces clusters, even on random noise.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is the "over-reading clusters" pitfall. Check whether clusters are stable across runs and meaningful to domain experts.

</details>

### 42. True or False: PCA's principal components are always identical to some of the original metrics.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Principal components are new, combined directions along which the data varies most. A human must interpret what they mean.

</details>

### 43. True or False: In the anomaly-detection example, a suspiciously fast 40 ms API response was flagged, and that matters because an instant answer might be an error page or empty cached data.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Not every anomaly is "too slow". `IsolationForest` flagged the 40 ms response alongside the slow spikes.

</details>

### 44. True or False: A single neuron (perceptron) can learn the XOR problem.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A single neuron draws one straight line, and no single straight line separates XOR's 1s from its 0s. A network with a hidden layer is needed.

</details>

### 45. True or False: A model reporting 99% confidence on an unusual input is very likely to be correct.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A high probability is not proof of correctness; models can be confidently wrong, especially on unfamiliar inputs. Do not equate confidence with accuracy.

</details>

### 46. True or False: Setting temperature to 0 guarantees identical output from a hosted model on every run.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It makes output much more repeatable, but hosted models can still differ occasionally due to hardware batching and provider updates. Design checks to tolerate variation.

</details>

### 47. True or False: In BPE, an unseen word such as "retesting" becomes an unknown token.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Sub-word tokenisation splits it into known pieces (in the toy example `['r', 'e', 'test', 'i', 'n', 'g']`), so nothing is ever "unknown".

</details>

### 48. True or False: In the `apply_coupon` example, the AI-drafted tests failed because the code under test was buggy.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The code was correct and the *tests* were wrong: one contradicted the requirement, one expected the wrong behaviour for unknown codes, and one invented case-insensitivity.

</details>

### 49. True or False: "AI for testing" and "testing of AI" mean the same thing.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** AI for testing uses AI tools to help QE work (this week). Testing of AI verifies products that contain AI features (later weeks). They need very different skills.

</details>

### 50. True or False: Classic NLP methods like TF-IDF are deterministic: the same input gives the same output.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The comparison table lists classic NLP as fast, cheap, local and deterministic, while LLM-based approaches can vary between runs.

</details>

---

## Part 3: Code Prediction

### 51. What does this code print?

```python
def step(z):
    return 1 if z > 0 else 0

def neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias
    return step(z)

print(neuron([0, 1, 0], [2.0, 0.5, 1.5], -3.0))
```

- [ ] A) 1
- [ ] B) 0
- [ ] C) -2.5
- [ ] D) An error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 0

**Explanation:** z = 0×2.0 + 1×0.5 + 0×1.5 − 3.0 = −2.5. The step function returns 0 because z is not greater than 0.
- **Why others are wrong:**
  - A) That would need z > 0 (as for input `[1, 3, 1]`, where z = 2.0).
  - C) −2.5 is z, but the function returns `step(z)`.
  - D) The code is valid.

</details>

### 52. What does this code print?

```python
import numpy as np

def relu(z):
    return np.maximum(0, z)

print(relu(np.array([-2.0, 0.0, 3.0])))
```

- [ ] A) `[-2. 0. 3.]`
- [ ] B) `[0. 0. 3.]`
- [ ] C) `[0.119 0.5 0.953]`
- [ ] D) `[2. 0. 3.]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[0. 0. 3.]`

**Explanation:** ReLU is `max(0, z)`: negatives become 0, positives pass through.
- **Why others are wrong:**
  - A) That is the unchanged input (an identity function).
  - C) Those are sigmoid outputs.
  - D) ReLU does not take absolute values.

</details>

### 53. What does this code print?

```python
import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6]])
v = np.array([10, 20, 30])
print(A @ v)
```

- [ ] A) `[140 320]`
- [ ] B) `[60 150]`
- [ ] C) `[[10 40 90] [40 100 180]]`
- [ ] D) ValueError: shape mismatch

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `[140 320]`

**Explanation:** Each row is dotted with `v`: 1×10 + 2×20 + 3×30 = 140; 4×10 + 5×20 + 6×30 = 320.
- **Why others are wrong:**
  - B) Those are just the row sums of A times 10, not dot products.
  - C) That is element-wise multiplication (`*`), not `@`.
  - D) A has 3 columns and v has 3 elements, so the shapes match.

</details>

### 54. What is printed?

```python
import numpy as np
X = np.ones((4, 3))
W = np.ones((3, 5))
print((X @ W).shape)
```

- [ ] A) `(3, 3)`
- [ ] B) `(4, 5)`
- [ ] C) `(5, 4)`
- [ ] D) ValueError

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `(4, 5)`

**Explanation:** Shape rule: `(rows_a, n) @ (n, cols_b) → (rows_a, cols_b)`. Four examples, five neuron outputs each.
- **Why others are wrong:**
  - A) The shared inner dimension (3) disappears in the result.
  - C) The result keeps A's rows then B's columns, not the reverse.
  - D) The inner sizes (3 and 3) match.

</details>

### 55. A dense network has 3 inputs → 4 hidden neurons → 1 output. How many parameters (weights + biases) does it have?

- [ ] A) 12
- [ ] B) 16
- [ ] C) 21
- [ ] D) 8

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 21

**Explanation:** Parameters per dense layer = inputs × outputs + outputs. Layer 1: 3×4 + 4 = 16. Layer 2: 4×1 + 1 = 5. Total 21.
- **Why others are wrong:**
  - A) 12 counts only layer 1's weights.
  - B) 16 is layer 1 alone.
  - D) 8 is just the neuron count (4 + 1) plus inputs, not parameters.

</details>

### 56. One neuron has input `x = 2.0`, weight `w = 0.5`, bias `b = 0.0`, label `y = 1`, sigmoid activation and learning rate 1.0. The gradient for `w` is −0.2115. What is the new weight after one gradient-descent step?

- [ ] A) 0.2885
- [ ] B) 0.7115
- [ ] C) 0.5
- [ ] D) −0.2115

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 0.7115

**Explanation:** `new_weight = old_weight − learning_rate × gradient = 0.5 − 1.0 × (−0.2115) = 0.7115`. A negative gradient means increasing the weight reduces the loss.
- **Why others are wrong:**
  - A) That adds the gradient instead of subtracting it.
  - C) The weight does change after an update.
  - D) That is the gradient, not the new weight.

</details>

### 57. What does this preprocessing call print (using the lesson's `preprocess` function, which lowercases, replaces timestamps with `<timestamp>` and numbers with `<num>`, removes stop words and crude-stems)?

```python
print(preprocess("Order 48213 FAILED at 2026-10-12 09:14:03 when applying coupons"))
```

- [ ] A) `['order', '48213', 'failed', 'at', '2026-10-12', 'applying', 'coupons']`
- [ ] B) `['order', '<num>', 'fail', '<timestamp>', 'apply', 'coupon']`
- [ ] C) `['order', '<num>', 'fail', '<num>', '<num>', 'apply', 'coupon']`
- [ ] D) `['Order', '<num>', 'FAILED', '<timestamp>', 'applying', 'coupons']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['order', '<num>', 'fail', '<timestamp>', 'apply', 'coupon']`

**Explanation:** Lowercasing, timestamp replacement (before numbers), number replacement, stop-word removal ("at", "when") and crude stemming ("failed" → "fail", "applying" → "apply", "coupons" → "coupon").
- **Why others are wrong:**
  - A) No normalisation, stop-word removal or stemming was applied.
  - C) This is what you would get if numbers were replaced *before* timestamps; the lesson stresses that order of steps matters.
  - D) Lowercasing and stemming are missing.

</details>

### 58. What does this code print for the word "login"?

```python
sentences = ["click the login button", "click the sign-in button", "apply the coupon code"]
window = 1
pairs = []
for s in sentences:
    words = s.split()
    for i, centre in enumerate(words):
        for j in range(max(0, i - window), min(len(words), i + window + 1)):
            if j != i:
                pairs.append((centre, words[j]))
print([ctx for c, ctx in pairs if c == "login"])
```

- [ ] A) `['click', 'the']`
- [ ] B) `['the', 'button']`
- [ ] C) `['button']`
- [ ] D) `['sign-in']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['the', 'button']`

**Explanation:** With a window of 1, the neighbours of "login" are the word before ("the") and after ("button"). "sign-in" has the same neighbours, which is why skip-gram training pushes them towards similar embeddings.
- **Why others are wrong:**
  - A) "click" is two positions away, outside the window.
  - C) The word before is included too.
  - D) "login" and "sign-in" are in different sentences and are never neighbours.

</details>

### 59. In the tiny bigram language model trained on the lesson's nine Gherkin-style sentences, "the" is followed by "user" 9 times out of 14. What probability does `next_word_probabilities("the")` give "user" (rounded to 2 dp)?

- [ ] A) 0.09
- [ ] B) 0.50
- [ ] C) 0.64
- [ ] D) 1.00

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 0.64

**Explanation:** The function divides each count by the total: 9 / 14 ≈ 0.64. The other five followers ("login", "dashboard", "cart", "discounted", "search") get 1/14 each.
- **Why others are wrong:**
  - A) That treats 9 as a percentage.
  - B) Probabilities come from counts, not an equal split between two options.
  - D) Other words also follow "the", so "user" is not certain.

</details>

### 60. Logits are `[3.0, 1.9, 1.1, -0.2]` for `[" page", " screen", " form", " button"]`. Which temperature makes " page" take almost all of the probability?

- [ ] A) 0.2
- [ ] B) 1.0
- [ ] C) 1.5
- [ ] D) Temperature has no effect on the distribution

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 0.2

**Explanation:** Dividing logits by a small temperature exaggerates the gaps, so the top token dominates (≈1.00 at 0.2, versus about 0.66 at 1.0).
- **Why others are wrong:**
  - B) At 1.0 the original softmax distribution applies (" page" ≈ 0.66).
  - C) Higher temperatures *flatten* the distribution.
  - D) Temperature reshapes the distribution before sampling.

</details>

### 61. With `top_p = 0.8` and sorted next-token probabilities `0.5, 0.25, 0.15, 0.10`, which tokens can be sampled?

- [ ] A) Only the first
- [ ] B) The first two
- [ ] C) The first three
- [ ] D) All four

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The first three

**Explanation:** 0.5 + 0.25 = 0.75 is still below 0.8, so the 0.15 token is also needed (total 0.90). The 0.10 token is cut off.
- **Why others are wrong:**
  - A) 0.5 does not reach 0.8.
  - B) 0.75 does not reach 0.8.
  - D) Top-p stops as soon as the running total reaches p.

</details>

### 62. What number does this scikit-learn snippet print (the size of the learned vocabulary)?

```python
from sklearn.feature_extraction.text import CountVectorizer
reports = ["checkout button not working on safari",
           "checkout page crashes after coupon",
           "login button not working on firefox"]
v = CountVectorizer()
v.fit_transform(reports)
print(len(v.get_feature_names_out()))
```

- [ ] A) 3
- [ ] B) 12
- [ ] C) 17
- [ ] D) 6

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 12

**Explanation:** The unique words are: after, button, checkout, coupon, crashes, firefox, login, not, on, page, safari, working (12, in alphabetical order).
- **Why others are wrong:**
  - A) 3 is the number of documents (rows).
  - C) 17 is the total word count including repeats.
  - D) 6 is the length of one document.

</details>

---

## Part 4: Fill-in-the-Blank

### 63. Recall = TP / (TP + ___).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** FN (false negatives)

**Explanation:** Recall asks "of all the real problems, how many did it catch?" Misses (false negatives) reduce it.

</details>

### 64. A flaky-test detector is evaluated with TP = 30, FP = 10, FN = 20, TN = 140. Its precision is ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 0.75 (75%)

**Explanation:** Precision = TP / (TP + FP) = 30 / 40 = 0.75. (For comparison, recall = 30 / 50 = 0.60 and accuracy = 170 / 200 = 0.85.)

</details>

### 65. In gradient descent, `new_weight = old_weight - ___ * gradient`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `learning_rate`

**Explanation:** The learning rate is the step size, a hyperparameter: too small is slow, too large overshoots.

</details>

### 66. One complete pass through the entire training dataset is called an ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** epoch

**Explanation:** Data is processed in batches within each epoch, and weights are updated after each batch.

</details>

### 67. The famous linguistics principle behind word embeddings says: "You shall know a word by the ___ it keeps."

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** company

**Explanation:** J. R. Firth (1957). Words used in similar contexts get similar vectors.

</details>

### 68. As a rough rule for English, one token is about ___ of a word, so 1,000 tokens is roughly 750 words.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** three-quarters (0.75)

**Explanation:** Code, non-English text and unusual strings such as IDs or base64 often use more tokens.

</details>

### 69. RLHF stands for Reinforcement Learning from Human ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Feedback

**Explanation:** Humans compare or rate responses and the model is trained to prefer responses judged helpful, honest and safe.

</details>

### 70. The ISTQB specialist certification covering GenAI across the test process is called Certified Tester: Testing with Generative AI, abbreviated ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** CT-GenAI

**Explanation:** The lesson cites it as evidence that the industry now publishes guidance on GenAI in testing.

</details>

---

## Part 5: Matching

### 71. Match each term (1-5) to its meaning (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Feature | | A | Using a trained model on new, unseen data |
| 2 | Label | | B | A number measuring how wrong predictions are |
| 3 | Inference | | C | A measurable input property of an example |
| 4 | Loss | | D | Gradual loss of accuracy as real-world data changes |
| 5 | Drift | | E | The known correct answer for an example |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-A, 4-B, 5-D

**Explanation:** Features are inputs (e.g. test duration); labels are answers (e.g. "flaky"); inference uses the model on new data; loss measures wrongness and training minimises it; drift is decay over time that needs monitoring.

</details>

### 72. Match each unsupervised technique or tool (1-4) to its purpose (A-D).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | k-means | | A | Compress many correlated features into fewer while keeping most variation |
| 2 | PCA | | B | Find points that are easy to isolate with random splits (outliers) |
| 3 | IsolationForest | | C | Group examples around k centres |
| 4 | Silhouette score | | D | A -1 to 1 number measuring how well separated clusters are |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-A, 3-B, 4-D

**Explanation:** k-means clusters; PCA reduces dimensions; IsolationForest detects anomalies; silhouette score (with the elbow method) helps choose k, but domain knowledge decides.

</details>

### 73. Match each network architecture (1-4) to what it is designed for (A-D).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | MLP / feed-forward | | A | Images, using small sliding filters |
| 2 | CNN | | B | Sequences, especially language, using attention |
| 3 | RNN / LSTM | | C | Tabular data with dense layers |
| 4 | Transformer | | D | Sequences processed one item at a time with a carried "memory" |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-A, 3-D, 4-B

**Explanation:** MLPs suit flaky-test prediction from metrics; CNNs suit visual regression; RNNs were largely replaced for language by Transformers, which power today's LLMs.

</details>

### 74. Match each attention role (1-3) to its library analogy (A-C).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Query | | A | The content inside the book |
| 2 | Key | | B | The question you bring to the library desk |
| 3 | Value | | C | The label on each book's spine |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-C, 3-A

**Explanation:** The query (what this token is looking for) is compared with each key (what each token offers) by dot product; softmax turns scores into weights; the weighted mix of values becomes the new representation.

</details>

### 75. Match each GenAI limitation (1-5) to its root cause (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | Hallucination | | A | Pre-training data stops at a date |
| 2 | Non-determinism | | B | The model only sees what is in its context window |
| 3 | Knowledge cut-off | | C | It generates plausible continuations with no built-in fact-checker |
| 4 | Ignores your custom `BasePage` class | | D | Text is processed as tokens and the model predicts likely text rather than running an algorithm |
| 5 | Counting and arithmetic errors | | E | Sampling from probabilities plus infrastructure effects |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-A, 4-B, 5-D

**Explanation:** Every limitation follows from LLM mechanics: plausibility without verification, sampling, a training cut-off date, a limited context window and token-based processing.

</details>
