# NLP Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- Define **Natural Language Processing (NLP)** and explain why human language is hard for computers.
- Identify where NLP shows up in quality engineering: **requirements, user stories, Gherkin scenarios, bug reports, test logs and chat-based products**.
- Describe the classic **text preprocessing** steps: **tokenisation, normalisation, stop-word removal, stemming and lemmatisation**.
- Explain how **sub-word tokenisation (BPE)** builds a vocabulary, and run real stemming, lemmatisation, **named entity recognition** and **part-of-speech tagging** with NLTK and spaCy.
- Explain how text is turned into numbers using **bag-of-words** and **TF-IDF**, and know their limitations.
- Measure how similar two pieces of text are with **cosine similarity**, and apply it to **duplicate bug detection**.
- Build a simple **text classifier** that routes bug reports to the right component.
- Explain how **word embeddings** are learned, what **contextual embeddings** add, and how **semantic search** finds duplicates that word matching misses.
- Outline the evolution of NLP from rules to statistics to neural networks to **Transformers and LLMs**, setting up the Generative AI lessons that follow.

---

## Why This Matters

Look at the artefacts a quality engineer works with every day:

- **Requirements and user stories:** *"As a shopper, I want to save my cart so that I can check out later."*
- **Acceptance criteria and Gherkin** (you wrote these in Week 6): *"Given I am logged in, When I add an item, Then the cart count increases."*
- **Bug reports:** *"Checkout button unresponsive on Safari after applying coupon."*
- **Test logs and failure messages:** *"TimeoutError: locator.click: Timeout 30000ms exceeded."*
- **Product features** such as chatbots, search boxes and support assistants.

Almost all of this is **natural language**: text written by people, for people. Computers cannot natively understand any of it. **NLP is the branch of AI that makes text usable by machines**, and it is the direct ancestor of the large language models you will use for the rest of the week.

Understanding NLP fundamentals helps you in two ways. First, you can build simple, reliable tools yourself (duplicate-bug finders, log classifiers) with a few lines of Python. Second, you will understand *why* modern AI tools handle language the way they do, including their weak spots, which makes you a sharper tester of AI output.

---

## The Concept

### 1. What Is NLP?

**Natural Language Processing (NLP)** is a field at the intersection of computer science, AI and linguistics that enables computers to **read, interpret, classify and generate human language**.

It is often divided into two broad directions:

| Direction | Meaning | Examples |
|-----------|---------|----------|
| **Natural Language Understanding (NLU)** | Extracting meaning from text. | Classifying a bug report's component, detecting the intent of a chatbot message, finding the dates and names in a requirement. |
| **Natural Language Generation (NLG)** | Producing text. | Summarising a failure log, drafting release notes, writing test descriptions. |

Generative AI (later today) is essentially extremely capable NLG combined with strong NLU.

### 2. Why Language Is Hard for Computers

Humans resolve language effortlessly using context and world knowledge. Computers see only characters. Consider these challenges:

| Challenge | Example | Why it is hard |
|-----------|---------|----------------|
| **Ambiguity** | "The test **failed** to **fail**." / "Run the **suite**." | Words have multiple meanings; sentence structure can be read several ways. |
| **Synonyms** | "Login button", "sign-in CTA", "auth button" | Different words, same meaning. A keyword search finds only one. |
| **Context** | "It crashed **again**." | What crashed? Requires earlier context. |
| **Negation** | "The page does **not** fail to load." | A single word flips the meaning; simple word counting misses it. |
| **Typos and informal text** | "chekout brokn on mobil pls fix asap!!" | Real bug reports are messy. |
| **Domain jargon** | "Flaky", "smoke", "regression", "locator" | Everyday meanings differ from QE meanings. |
| **Sarcasm and tone** | "Great, the build is green... for once." | Meaning is opposite to the literal words. |

Keep this table in mind; every technique below is an attempt to handle some of these problems, and none handles all of them perfectly.

### 3. Text Preprocessing: Cleaning Up Before Analysis

Raw text must be broken down and cleaned before classic NLP techniques can use it. The standard steps:

#### 3.1 Tokenisation

**Tokenisation** splits text into smaller units called **tokens**, usually words and punctuation.

```text
"Checkout button unresponsive on Safari!"
  -> ["Checkout", "button", "unresponsive", "on", "Safari", "!"]
```

Tokenisation sounds trivial but is not: what about `"can't"`, `"e-mail"`, `"locator.click()"`, `"30000ms"` or URLs? Different tasks choose different rules. Modern LLMs use **sub-word tokenisation**, where common words stay whole and uncommon words are split into pieces. Section 3.6 shows how such a vocabulary is built, and the Generative AI concepts lesson later today explains why LLMs depend on it.

#### 3.2 Normalisation

**Normalisation** makes text consistent: converting to lowercase, removing or standardising punctuation, expanding contractions, and sometimes replacing volatile values like numbers, IDs or timestamps with placeholders. For logs, this is powerful:

```text
"Order 48213 failed at 2026-10-12 09:14:03"
"Order 99102 failed at 2026-10-13 22:40:51"
  both -> "order <NUM> failed at <TIMESTAMP>"
```

Now two "different" messages are recognised as the same kind of failure.

#### 3.3 Stop-word removal

**Stop words** are very common words that carry little meaning on their own: *the, a, is, on, at, and*. Removing them shrinks the data and focuses on meaningful words. But be careful: words like **"not"** are often on stop-word lists, and removing them destroys negation.

#### 3.4 Stemming and lemmatisation

Both reduce words to a base form so that variants are counted together:

| Technique | How it works | Example |
|-----------|-------------|---------|
| **Stemming** | Chops off word endings with crude rules. Fast; results may not be real words. | "failing", "failed", "fails" -> "fail"; "studies" -> "studi" |
| **Lemmatisation** | Uses vocabulary and grammar to find the dictionary form (the **lemma**). Slower, more accurate. | "failing", "failed" -> "fail"; "better" (adjective) -> "good"; "ran" -> "run" |

Here is a real comparison using two popular Python NLP libraries: **NLTK** (its Porter stemmer) and **spaCy** (its lemmatiser). Install them once with:

```bash
pip install nltk spacy
python -m spacy download en_core_web_sm
```

The second command downloads `en_core_web_sm`, spaCy's small English model (a trained pipeline that knows English vocabulary and grammar).

```python
# stem_vs_lemma.py
import spacy
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
nlp = spacy.load("en_core_web_sm")

sentence = "The retried tests were failing because studies showed better locators ran faster"
doc = nlp(sentence)

print(f"{'word':10s} {'stem (NLTK)':12s} {'lemma (spaCy)':12s}")
for token in doc:
    print(f"{token.text:10s} {stemmer.stem(token.text):12s} {token.lemma_:12s}")
```

Output (spaCy 3.8 with `en_core_web_sm` 3.8; other versions may differ slightly):

```text
word       stem (NLTK)  lemma (spaCy)
The        the          the
retried    retri        retry
tests      test         test
were       were         be
failing    fail         fail
because    becaus       because
studies    studi        study
showed     show         show
better     better       well
locators   locat        locator
ran        ran          run
faster     faster       fast
```

**Code walkthrough and observations:**

- `nlp(sentence)` runs spaCy's whole pipeline (tokenisation, grammar analysis, lemmatisation) and returns a `Doc`; looping over it gives `Token` objects. `token.lemma_` is the lemma (spaCy's text attributes end in an underscore).
- `stemmer.stem(word)` applies crude suffix rules: it produces non-words such as `retri`, `becaus`, `studi` and `locat`, and it cannot handle irregular forms like "were" or "ran".
- spaCy uses grammar: "were" becomes "be", "ran" becomes "run", "studies" becomes "study".
- Look at "better": spaCy decided it was an **adverb** here (as in "works better") and returned "well". Used as an adjective ("a better locator") it would return "good". The lemma depends on how the word is used, which is exactly why lemmatisation needs grammar.

**Which to use?** Stemming is fast and good enough when you only need to group variants for search or counting. Lemmatisation is better when the output must be real, readable words or when precision matters.

#### 3.5 A preprocessing function in Python

```python
# preprocess.py
import re

STOP_WORDS = {"the", "a", "an", "is", "on", "at", "in", "of", "to", "and", "after", "when", "for", "with"}

def normalise_log_line(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\d{4}-\d{2}-\d{2}[ t]\d{2}:\d{2}:\d{2}", "<timestamp>", text)
    text = re.sub(r"\b\d+\b", "<num>", text)
    return text

def tokenise(text: str) -> list[str]:
    # \w+ matches runs of letters, digits or underscores; <...> keeps our placeholders whole
    return re.findall(r"<\w+>|\w+", text)

def crude_stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            return token[: -len(suffix)]
    return token

def preprocess(text: str) -> list[str]:
    tokens = tokenise(normalise_log_line(text))
    return [crude_stem(t) for t in tokens if t not in STOP_WORDS]

print(preprocess("Order 48213 FAILED at 2026-10-12 09:14:03 when applying coupons"))
# ['order', '<num>', 'fail', '<timestamp>', 'apply', 'coupon']
```

**Code walkthrough:**

- `re.sub(pattern, replacement, text)` replaces every match of a regular expression (you used regex in Week 1). The timestamp pattern runs **before** the number pattern; otherwise the digits in the date would be replaced first and the timestamp would be lost. Order of preprocessing steps matters.
- `\b\d+\b` matches whole numbers (`\b` is a word boundary).
- `re.findall(r"<\w+>|\w+", text)` returns a list of tokens. The `|` means "or": match either a placeholder like `<num>` or a normal word.
- `crude_stem` is a toy stemmer to show the idea. Real projects use libraries such as **NLTK** or **spaCy**, which provide proper tokenisers, stop-word lists, stemmers and lemmatisers.

#### 3.6 Sub-word tokenisation: how BPE builds a vocabulary

Word-level tokenisation has a big problem: any word not seen during training (a new library name, a typo, a product code) is simply **unknown**. Character-level tokenisation never has unknown tokens but produces very long sequences that carry little meaning per token. **Sub-word tokenisation** sits in between, and the most widely known method is **Byte-Pair Encoding (BPE)**.

The idea is simple:

1. Start with every word split into single characters.
2. Count every pair of neighbouring symbols across the training text (weighted by how often each word appears).
3. **Merge the most frequent pair** into a new, longer symbol and add it to the vocabulary.
4. Repeat for a chosen number of merges.

Frequent words end up as single tokens; rare words stay split into reusable pieces. Here is a complete, runnable toy version:

```python
# toy_bpe.py
from collections import Counter

# Word frequencies from a tiny "training corpus" of test-automation text
word_counts = {"test": 10, "tests": 6, "tester": 3, "testing": 5, "locate": 2, "locator": 4, "locators": 3}

# Start: every word is a sequence of single characters
vocab = {tuple(word): count for word, count in word_counts.items()}

def most_frequent_pair(vocab):
    pairs = Counter()
    for symbols, count in vocab.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += count
    return pairs.most_common(1)[0][0]

def merge(vocab, pair):
    merged = {}
    for symbols, count in vocab.items():
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
                out.append(symbols[i] + symbols[i + 1])   # glue the pair into one symbol
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        merged[tuple(out)] = count
    return merged

merges = []
for step in range(1, 11):
    pair = most_frequent_pair(vocab)
    merges.append(pair)
    vocab = merge(vocab, pair)
    print(f"merge {step}: {pair[0]!r} + {pair[1]!r} -> {pair[0] + pair[1]!r}")

print("\nWords after 10 merges:")
for symbols in vocab:
    print("  ", " | ".join(symbols))

def tokenise(word):
    symbols = tuple(word)
    for pair in merges:                      # apply the learned merges in order
        symbols = next(iter(merge({symbols: 1}, pair)))
    return list(symbols)

print("\nNew word 'retesting' ->", tokenise("retesting"))
```

Output:

```text
merge 1: 't' + 'e' -> 'te'
merge 2: 'te' + 's' -> 'tes'
merge 3: 'tes' + 't' -> 'test'
merge 4: 'l' + 'o' -> 'lo'
merge 5: 'lo' + 'c' -> 'loc'
merge 6: 'loc' + 'a' -> 'loca'
merge 7: 'loca' + 't' -> 'locat'
merge 8: 'locat' + 'o' -> 'locato'
merge 9: 'locato' + 'r' -> 'locator'
merge 10: 'test' + 's' -> 'tests'

Words after 10 merges:
   test
   tests
   tes | te | r
   test | i | n | g
   loca | te
   locator
   locator | s

New word 'retesting' -> ['r', 'e', 'test', 'i', 'n', 'g']
```

**Code walkthrough:**

- `tuple(word)` splits a word into characters: `"test"` becomes `('t', 'e', 's', 't')`. Tuples are used because they can be dictionary keys.
- `most_frequent_pair` counts every neighbouring pair (`zip(symbols, symbols[1:])` pairs each symbol with the next one), **weighted by word frequency**: the pair `t e` inside "test" counts 10 times because "test" appeared 10 times.
- `merge` rebuilds each word, gluing the chosen pair into one symbol wherever it appears.
- `tokenise` applies the learned merges, in the order they were learned, to any new word.

**What the output teaches:**

- The most frequent words ("test", "tests", "locator") became **single tokens**.
- The unseen word **"retesting"** is not "unknown": it is split into known pieces, `re` and `test` plus characters. With more merges (real tokenisers perform tens of thousands), pieces like `ing` and `re` would become tokens too.
- "tester" became the odd split `tes | te | r`. Merges follow **frequency, not meaning**, so token boundaries do not always match how a human would split a word. This is one reason LLMs sometimes struggle with spelling, counting letters or exact string manipulation, which you will meet again in the Generative AI concepts lesson.

### 4. Turning Text into Numbers

As you learned earlier today, ML models only understand **numbers**. So the central question of classic NLP is: *how do we represent text as a list of numbers (a **vector**)?*

#### 4.1 Bag-of-words

The **bag-of-words** model builds a **vocabulary** of all words in a collection of documents, then represents each document by **counting** how often each word appears. Word order is thrown away, as if you tipped the words into a bag and shook it.

```python
# bag_of_words.py
from sklearn.feature_extraction.text import CountVectorizer

reports = [
    "checkout button not working on safari",
    "checkout page crashes after coupon",
    "login button not working on firefox",
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(reports)

print(vectorizer.get_feature_names_out())
print(X.toarray())
```

Output (columns are the vocabulary, in alphabetical order):

```text
['after' 'button' 'checkout' 'coupon' 'crashes' 'firefox' 'login' 'not' 'on' 'page' 'safari' 'working']
[[0 1 1 0 0 0 0 1 1 0 1 1]
 [1 0 1 1 1 0 0 0 0 1 0 0]
 [0 1 0 0 0 1 1 1 1 0 0 1]]
```

Each row is now a vector of numbers a model can use. **Limitations:** word order is lost ("dog bites man" = "man bites dog"), every word is equally important, and synonyms are completely unrelated ("crash" and "freeze" share nothing).

#### 4.2 TF-IDF: weighting words by importance

**TF-IDF** (Term Frequency × Inverse Document Frequency) improves on raw counts:

- **Term Frequency (TF):** how often a word appears in **this** document. More often = more relevant to this document.
- **Inverse Document Frequency (IDF):** how **rare** the word is across **all** documents. A word that appears everywhere (like "test" in a test log collection) tells you little, so it gets a low weight. A word that appears in few documents (like "coupon") is distinctive, so it gets a high weight.

The result: words that are frequent in one document but rare overall get the highest scores. TF-IDF has powered search engines and document classification for decades and is still a strong, cheap baseline.

```python
# tfidf_example.py
from sklearn.feature_extraction.text import TfidfVectorizer

reports = [
    "checkout button not working on safari",
    "checkout page crashes after coupon",
    "login button not working on firefox",
]
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(reports)

# Show the most distinctive words of the second report
row = X[1].toarray()[0]
words = tfidf.get_feature_names_out()
top = sorted(zip(words, row), key=lambda pair: pair[1], reverse=True)[:3]
print([(word, round(float(score), 2)) for word, score in top])
# [('after', 0.47), ('coupon', 0.47), ('crashes', 0.47)]  ('page' ties with these;
# 'checkout' scores lower because it also appears in another report)
```

### 5. Measuring Text Similarity: Duplicate Bug Detection

Once texts are vectors, we can measure how similar they are. The standard measure is **cosine similarity**: it compares the **direction** of two vectors, giving a score from 0 (nothing in common) to 1 (identical direction) for word-count vectors.

Why direction rather than distance? A long bug report and a short one about the same issue point in a similar direction even though their counts differ in size.

A very practical QE application: when someone files a new bug, **suggest likely duplicates**.

```python
# duplicate_bugs.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

existing_bugs = [
    "BUG-101 Checkout button does nothing on Safari after applying a coupon",
    "BUG-102 Login page shows blank screen on slow 3G network",
    "BUG-103 Product images fail to load on the search results page",
    "BUG-104 Cart total is wrong when two coupons are applied",
]
new_bug = "Safari: clicking checkout does nothing once a coupon code is applied"

vectorizer = TfidfVectorizer(stop_words="english")
vectors = vectorizer.fit_transform(existing_bugs + [new_bug])

scores = cosine_similarity(vectors[-1], vectors[:-1])[0]
for bug, score in sorted(zip(existing_bugs, scores), key=lambda p: p[1], reverse=True):
    print(f"{score:.2f}  {bug}")
```

**Code walkthrough:**

- `stop_words="english"` uses scikit-learn's built-in English stop-word list.
- We fit the vectoriser on all bugs **plus** the new one so they share a vocabulary.
- `cosine_similarity(vectors[-1], vectors[:-1])` compares the last vector (the new bug) with every existing bug.
- BUG-101 should score highest, even though the wording is different ("does nothing" / "clicking checkout does nothing", "applying a coupon" / "coupon code is applied"), because they share distinctive words: *safari, checkout, coupon*.

**Where it breaks:** if the new bug said *"Apple browser: purchase CTA unresponsive after promo code"*, TF-IDF would find almost no overlap, because it matches **words, not meanings**. Embeddings (section 7) solve that.

### 6. Text Classification: Routing Bug Reports

**Text classification** assigns a category to a piece of text. It is supervised learning (from the earlier lesson), with text turned into features. Let us route bug reports to the right team.

```python
# bug_router.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

training_reports = [
    "payment declined with valid card", "refund not processed", "coupon discount not applied at checkout",
    "card number field rejects spaces", "order total wrong after tax",
    "login fails with correct password", "password reset email never arrives", "session expires too quickly",
    "two factor code not accepted", "account locked after one attempt",
    "search returns no results for shoes", "filter by price ignored", "product images missing in search",
    "sorting by rating shows random order", "search suggestions are slow",
]
labels = (["payments"] * 5) + (["auth"] * 5) + (["search"] * 5)

classifier = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
classifier.fit(training_reports, labels)

new_reports = [
    "discount code ignored on checkout page",
    "cannot sign in, password rejected",
    "price filter does not work in search",
]
for report, team in zip(new_reports, classifier.predict(new_reports)):
    print(f"{team:9s} <- {report}")
```

**Code walkthrough:**

- The **pipeline** first converts text into TF-IDF vectors, then feeds them to a logistic-regression classifier. Because the pipeline is one object, `fit` and `predict` accept raw strings.
- With only 15 training examples this is a toy, but the structure is exactly what real teams use as a first baseline. Real systems train on thousands of historical, already-routed tickets.
- Test it like a tester: what happens with *"cannot sign in"* when the training data only says *"login"*? Synonyms are a weak spot for word-based features. Try it in the practice exercises.

### 7. Word Embeddings: Representing Meaning

Bag-of-words treats every word as unrelated to every other word. **Word embeddings** fixed this. An embedding represents each word as a **dense vector of numbers** (typically hundreds of dimensions), learned from huge amounts of text, such that **words used in similar contexts get similar vectors**.

The underlying idea is a famous linguistics principle: *"You shall know a word by the company it keeps"* (J. R. Firth, 1957). "Login" and "sign-in" appear in similar sentences, so their vectors end up close together.

Well-known early embedding methods include **Word2Vec** (2013) and **GloVe** (2014). They showed surprising properties, such as vector arithmetic capturing relationships, with the textbook example *king - man + woman ≈ queen*.

**How are embeddings learned?** With the self-supervised idea you met in the supervised vs. unsupervised lesson: the text provides its own labels. Word2Vec's "skip-gram" variant, for example, slides a small window over huge amounts of text and trains a simple neural network on one task: *given a word, predict the words around it*. The network's weights for each word, after training, **are** that word's embedding. Words that keep appearing next to the same neighbours must produce similar predictions, so they end up with similar vectors.

This short script shows the training pairs such a model would learn from:

```python
# skipgram_pairs.py
sentences = [
    "click the login button",
    "click the sign-in button",
    "apply the coupon code",
]
window = 1     # how many neighbours on each side count as "context"

pairs = []
for sentence in sentences:
    words = sentence.split()
    for i, centre in enumerate(words):
        for j in range(max(0, i - window), min(len(words), i + window + 1)):
            if j != i:
                pairs.append((centre, words[j]))

for centre in ("login", "sign-in", "coupon"):
    print(f"{centre:8s} appears next to: {[ctx for c, ctx in pairs if c == centre]}")
```

Output:

```text
login    appears next to: ['the', 'button']
sign-in  appears next to: ['the', 'button']
coupon   appears next to: ['the', 'code']
```

"login" and "sign-in" share exactly the same neighbours, so a model trained on these pairs is pushed towards giving them similar vectors, while "coupon" is pushed elsewhere. Nobody told the model that the words are synonyms; it inferred it from **the company they keep**. With billions of words of text, this produces vectors that capture surprisingly rich relationships.

Here is a toy illustration of what the finished vectors look like, with hand-made 3-dimensional vectors. Real embeddings are learned, not hand-made, and have many more dimensions:

```python
# toy_embeddings.py
import numpy as np

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Pretend dimensions: [authentication-ness, payment-ness, UI-element-ness]
emb = {
    "login":    np.array([0.90, 0.05, 0.30]),
    "sign-in":  np.array([0.88, 0.04, 0.35]),
    "password": np.array([0.80, 0.10, 0.10]),
    "coupon":   np.array([0.05, 0.90, 0.20]),
    "button":   np.array([0.20, 0.15, 0.95]),
}
print("login vs sign-in:", round(cosine(emb["login"], emb["sign-in"]), 3))   # very close
print("login vs coupon: ", round(cosine(emb["login"], emb["coupon"]), 3))    # far apart
```

**Code walkthrough:** `np.dot` multiplies matching positions and adds them up; `np.linalg.norm` gives each vector's length. Dividing gives the cosine similarity you used in section 5. With embeddings, "login" and "sign-in" are recognised as nearly the same, something bag-of-words could never do.

#### 7.1 Contextual embeddings

Classic word embeddings give each word **one** vector, regardless of context. But consider:

- "The test **suite** passed."
- "Book a **suite** at the hotel."
- "Click **run** to start." / "We had a good **run** of green builds."

**Contextual embeddings**, produced by Transformer models, give a word a **different vector depending on the surrounding sentence**. This was a major leap and is a core reason modern language models handle ambiguity far better. **Sentence embeddings** extend the idea to represent a whole sentence or paragraph as one vector, enabling meaning-based search ("semantic search"), such as finding the duplicate bug in section 5 even when it uses completely different words.

#### 7.2 Semantic search: how embeddings fix duplicate detection

Recall the failure from section 5: the new report *"Apple browser: purchase CTA unresponsive after promo code"* scored **0.00** against every existing bug with TF-IDF, because it shares no words with BUG-101, even though it describes the same problem. A **semantic search** pipeline replaces word counts with sentence embeddings:

```text
1. Embed every existing bug report once, using a pre-trained sentence-embedding model,
   and store the vectors.
2. When a new report arrives, embed it with the same model.
3. Compute cosine similarity between the new vector and every stored vector
   (exactly the calculation from section 5 and the toy example above).
4. Show the top few matches to the person filing the bug.
```

Because the embedding model learned from huge amounts of text that "Apple browser" relates to "Safari", "purchase" to "checkout", "CTA" to "button" and "promo code" to "coupon", BUG-101's vector ends up close to the new report's vector, and the duplicate is found.

| | TF-IDF similarity | Embedding similarity |
|--|-------------------|----------------------|
| Matches | Shared **words** | Shared **meaning** |
| Synonyms and paraphrases | Missed | Usually found |
| Setup | A few lines of scikit-learn, no download | Needs a pre-trained embedding model (a download or a hosted service) |
| Speed and cost | Very fast, runs anywhere | Slower; more compute |
| Explainability | Easy: you can see which words overlapped | Harder: similarity comes from learned vectors |

Libraries such as `sentence-transformers` provide ready-made sentence-embedding models in Python, and many AI providers offer embeddings through an API. Embedding models can also be wrong: two sentences can be close in meaning-space yet differ in a detail that matters for testing (for example, *"coupon applied twice"* vs. *"coupon not applied"*). As always, a human confirms that a suggested duplicate really is one.

### 8. The Classic NLP Task Catalogue

| Task | What it does | QE application |
|------|-------------|----------------|
| **Text classification** | Assigns a category to text. | Route bugs to teams; label failures as infra/product/test issue. |
| **Sentiment analysis** | Detects positive/negative/neutral tone. | Analyse app-store reviews after a release for quality signals. |
| **Named Entity Recognition (NER)** | Finds names of things: people, dates, products, amounts. | Extract amounts, dates and roles from requirements to build test data. |
| **Part-of-speech tagging** | Labels nouns, verbs, adjectives, … | Find the *actions* (verbs) and *objects* (nouns) in user stories to suggest test steps. |
| **Information retrieval / search** | Finds relevant documents for a query. | Search past incidents or test cases related to a change. |
| **Summarisation** | Produces a shorter version of a text. | Summarise a 5,000-line CI log or a long defect thread. |
| **Machine translation** | Converts between languages. | Localisation testing support. |
| **Question answering** | Answers questions from a text. | "Which acceptance criteria mention refunds?" |
| **Text generation** | Produces new text. | Drafting test ideas, release notes, bug summaries (Generative AI, later today). |

#### 8.1 Named entities and parts of speech in a requirement

Two tasks from the table are especially handy for testers working with requirements: **Named Entity Recognition (NER)**, which finds things like places, money, dates and times, and **part-of-speech (POS) tagging**, which labels each word as a noun, verb, adjective and so on. spaCy does both in a few lines:

```python
# requirement_analysis.py
import spacy

nlp = spacy.load("en_core_web_sm")
requirement = ("Registered users in Canada can apply a coupon worth $20 to orders placed "
               "before December 31, 2026, and the system must email a receipt within 5 minutes.")
doc = nlp(requirement)

print("Named entities:")
for ent in doc.ents:
    print(f"  {ent.text:22s} -> {ent.label_:8s} ({spacy.explain(ent.label_)})")

print("\nVerbs (possible test actions):", [t.lemma_ for t in doc if t.pos_ == "VERB"])
print("Nouns (possible test objects): ", [t.lemma_ for t in doc if t.pos_ == "NOUN"])
```

Output (spaCy 3.8 with `en_core_web_sm` 3.8):

```text
Named entities:
  Canada                 -> GPE      (Countries, cities, states)
  20                     -> MONEY    (Monetary values, including unit)
  December 31, 2026      -> DATE     (Absolute or relative dates or periods)
  5 minutes              -> TIME     (Times smaller than a day)

Verbs (possible test actions): ['register', 'apply', 'place', 'email']
Nouns (possible test objects):  ['user', 'coupon', 'order', 'system', 'receipt', 'minute']
```

**Code walkthrough:**

- `doc.ents` holds the named entities spaCy found; each has the matched `text` and a `label_`. `spacy.explain(label)` turns a short code such as `GPE` (geopolitical entity) into a readable description.
- `t.pos_` is each token's part of speech (`"VERB"`, `"NOUN"`, and so on). The list comprehensions keep only verbs or nouns, and use `t.lemma_` so "Registered" appears as "register".

**Why a tester cares:** every entity is a **test-data and boundary hint**. *Canada* suggests testing a user outside Canada; *$20* suggests checking orders below $20; *December 31, 2026* invites boundary tests just before and just after midnight (and the question "in which time zone?"); *5 minutes* is a timing requirement that needs a measurable check. The verbs sketch the **actions** a test will perform, and the nouns the **objects** involved.

**Notice the imperfections**, because spotting them is a tester's job: the money entity is `20` without the `$` sign, and "Registered" was tagged as a verb although here it describes the users. Small pre-trained models are useful assistants, not authorities, and their output should be checked before you build on it.

### 9. How NLP Evolved: From Rules to LLMs

```text
1950s-1980s   RULE-BASED NLP
              Hand-written grammars and dictionaries. Precise but brittle.
                    |
1990s-2000s   STATISTICAL NLP
              Counting words and word sequences (bag-of-words, n-grams, TF-IDF);
              classic ML classifiers. Robust, but no real notion of meaning.
                    |
2013-2017     NEURAL NLP
              Word embeddings (Word2Vec, GloVe); recurrent networks (RNN/LSTM)
              read text in sequence. Meaning captured as vectors.
                    |
2017-today    TRANSFORMERS AND LARGE LANGUAGE MODELS
              Attention mechanism; contextual embeddings; models pre-trained on
              enormous text collections that can both understand and generate text.
```

An **n-gram** is a sequence of *n* consecutive tokens ("checkout button" is a 2-gram, or **bigram**). Statistical language models predicted the next word using n-gram counts; for example, after "checkout", which word most often follows? Hold that idea: predicting the next token is exactly what large language models do, at a vastly greater scale and sophistication. You will see this in the next lesson.

### 10. Classic NLP or an LLM? A Practical Note

Today's LLMs can perform most of the tasks in section 8 from a simple instruction. So why learn TF-IDF?

| Classic NLP (TF-IDF, small classifiers) | LLM-based |
|------------------------------------------|-----------|
| Fast, cheap, runs locally on a laptop | Usually calls a hosted model; costs per use |
| Deterministic: same input, same output | Can vary between runs |
| Easy to test and explain | Harder to explain individual decisions |
| Needs labelled training data | Often works with little or no task-specific data |
| Weak on meaning, synonyms, context | Strong on meaning and context |

Good engineers choose the simplest tool that meets the need. Deduplicating 50,000 log lines every night is a perfect TF-IDF or clustering job. Summarising a confusing defect thread for a stakeholder is a job for an LLM. Many real solutions combine both.

---

## Practice Exercises

1. **Preprocessing.** Extend `preprocess.py` so that UUIDs (for example `3f2b8c1e-9a4d-4c2e-b8f1-2d7e6a9c0b11`) are replaced with `<uuid>` and URLs with `<url>`. Write three pytest tests for your function (you know how from Week 4).
2. **Negation trap.** Add `"not"` to `STOP_WORDS` and preprocess `"login does not fail"` and `"login does fail"`. What goes wrong? Write one sentence explaining the risk for a bug-triage tool.
3. **Duplicate detection.** Run `duplicate_bugs.py`. Then replace `new_bug` with `"Apple browser: purchase CTA unresponsive after promo code"`. What happens to the scores and why?
4. **Break the router.** Run `bug_router.py` with these new reports: `"unable to authenticate"`, `"promo code rejected"`, `"cannot find any items"`. Which are misrouted? Add two training examples that fix one misrouting and rerun.
5. **BPE experiment.** In `toy_bpe.py`, add `"testcase": 4` and `"testcases": 2` to `word_counts` and increase the merges to 15. Which new tokens appear? How is `"retesting"` tokenised now? Explain why the vocabulary changed.
6. **Requirement mining.** Run `requirement_analysis.py` on one acceptance criterion from your own Project 2 user stories (or invent one for a generic web app). List the entities found, then write three boundary or negative test ideas suggested by them. Note one thing spaCy got wrong or missed.
7. **Project 2 thinking.** List three kinds of text produced by your Project 2 test framework (for example, pytest failure messages, Playwright trace logs, CI job output). For each, name one NLP task from section 8 that could add value.

---

## Knowledge Check

1. What is tokenisation, and why is it not as simple as "split on spaces"?
2. What is the difference between stemming and lemmatisation?
3. What problem does TF-IDF solve compared with raw word counts?
4. Why can cosine similarity on TF-IDF vectors miss a duplicate bug written with different words?
5. What is the key difference between classic word embeddings and contextual embeddings?
6. In BPE, what decides which two symbols are merged next?
7. Name two kinds of named entity that could suggest boundary tests in a requirement, with an example of each.

<details>
<summary>Suggested answers</summary>

1. Splitting text into units (tokens). Contractions, punctuation, code, URLs, numbers and hyphenated words all need deliberate rules.
2. Stemming chops word endings by crude rules (may produce non-words); lemmatisation uses vocabulary and grammar to find the true dictionary form.
3. It down-weights words that appear in almost every document and highlights words distinctive to a particular document.
4. TF-IDF matches exact words, not meanings, so synonyms ("sign-in" vs "login") share no overlap.
5. Classic embeddings give one fixed vector per word; contextual embeddings give a word a different vector depending on its surrounding sentence.
6. Frequency: the pair of neighbouring symbols that appears most often in the training text (weighted by word counts).
7. For example: MONEY ("$20" -> test $19.99 and $20.00) and DATE ("December 31, 2026" -> test just before and after midnight, and the time zone). TIME and place entities also work.

</details>

---

## Glossary

- **NLP:** The field enabling computers to process, understand and generate human language.
- **Token / Tokenisation:** A unit of text / splitting text into those units.
- **Stop words:** Very common words often removed during preprocessing.
- **Stemming / Lemmatisation:** Reducing words to a base form by crude rules / by dictionary and grammar.
- **Bag-of-words:** Representing a document by word counts, ignoring order.
- **TF-IDF:** A word weighting that favours words frequent in a document but rare across the collection.
- **Cosine similarity:** A measure of how similar two vectors' directions are.
- **N-gram:** A sequence of n consecutive tokens.
- **Byte-Pair Encoding (BPE):** A sub-word tokenisation method that repeatedly merges the most frequent pair of symbols to build a vocabulary.
- **Lemma:** The dictionary form of a word ("ran" -> "run").
- **Named Entity Recognition (NER):** Finding and labelling names of things such as places, money, dates and times.
- **Part-of-speech (POS) tagging:** Labelling each word as a noun, verb, adjective and so on.
- **Embedding:** A dense numeric vector representing the meaning of a word, sentence or document.
- **Semantic search:** Finding text by similarity of meaning, using embeddings, rather than by shared words.
- **Contextual embedding:** An embedding that changes depending on surrounding text.

---

## Summary

- **NLP** lets computers work with human language, which is ambiguous, contextual, messy and full of synonyms and jargon.
- Classic pipelines **tokenise, normalise, remove stop words and stem or lemmatise** text, then convert it to numbers.
- **Bag-of-words** and **TF-IDF** turn text into vectors; **cosine similarity** compares them, enabling practical tools like **duplicate bug detection**, and classifiers can **route bug reports**.
- **Sub-word tokenisation (BPE)** builds a vocabulary of frequent pieces, so unseen words never become "unknown"; token boundaries follow frequency, not meaning.
- Libraries such as **NLTK** and **spaCy** provide real stemming, lemmatisation, **named entity recognition** and **part-of-speech tagging**; entities in requirements are natural test-data and boundary hints.
- Word-based methods match **words, not meanings**. **Embeddings**, learned self-supervised from the company words keep, represent meaning as vectors; **contextual embeddings** handle ambiguity, and **semantic search** finds duplicates written in different words.
- NLP evolved from **rules → statistics → neural networks → Transformers and LLMs**. Predicting the next token, which started with n-gram counts, is the core of the Generative AI you will study next.
- Choose the simplest tool that works: classic NLP is fast, cheap and deterministic; LLMs are powerful but variable.

---

## Additional Resources

- Hugging Face, *LLM Course* (chapter 1 introduces NLP, Transformers and what they can do): https://huggingface.co/learn/llm-course/chapter1/1
- spaCy, *spaCy 101: Everything you need to know* (tokenisation, lemmatisation, named entities and more, in Python): https://spacy.io/usage/spacy-101
- Google for Developers, *Machine Learning Crash Course: Introduction to Large Language Models* (tokens, n-grams and the path to Transformers): https://developers.google.com/machine-learning/crash-course/llm
