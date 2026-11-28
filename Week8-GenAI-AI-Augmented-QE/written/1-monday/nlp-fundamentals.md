# NLP Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what Natural Language Processing (NLP) is, and why human language is hard for computers.
- **Clean** a piece of text by hand the way an NLP system does: lowercase, remove punctuation, split into tokens, drop stop words.
- **Compare** two bug reports by shared words, and explain what TF-IDF and cosine similarity add.
- **Explain** what embeddings are, and why they catch duplicates that word matching misses.
- **Choose** between classic NLP and an AI assistant for a text task in testing, and say why.

---

## Why This Matters

So far today, the examples have been tables of numbers: retries, timing spreads, files changed. But much of what testers deal with is **text**: bug reports, user stories, acceptance criteria, log messages, test names, review comments.

Text is where a lot of QE time goes. Large projects receive a constant stream of reports. Mozilla, for example, receives hundreds of Firefox bug reports and feature requests every day ([Mozilla Hacks, 2019](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)). Someone has to read each one, decide where it goes, and spot when it repeats a bug already logged. A duplicate that slips through means two people investigate the same problem; a "duplicate" that is really a new bug means a defect gets closed without a fix.

**Natural Language Processing** is how computers work with this text. It is also the bridge between the machine learning you met earlier today and the AI assistants you will use all week. ChatGPT, Copilot and Claude are, at heart, very large NLP systems.

> **Using this with the handout:** this lesson goes deeper into **Handout 02, Topic 1**. It uses the same four bug reports (BUG-101 to BUG-104), the same new bug, the same "voucher" bug and the same `duplicate_finder.py`.

---

## The Concept

### 1. What Is NLP?

**Natural Language Processing (NLP)** is the part of AI that helps computers work with **human language**: reading it, sorting it, comparing it, and generating it. "Natural" language means the languages people speak and write, such as English or Hindi, as opposed to programming languages such as Python.

Computers only work with numbers. So every NLP system, from a 1990s spam filter to Claude, does two things before anything else:

1. **Cleans** the text, so that trivial differences do not get in the way.
2. **Turns the text into numbers**, so that the computer can compare and learn from it.

How well a system does step 2 decides almost everything about how clever it can be.

### 2. Why Language Is Hard for Computers

Language is easy for people and hard for machines. Here is why, with examples from bug reports:

| Problem | What it means | Testing example |
|---|---|---|
| **Same meaning, different words** | People describe one thing in many ways | "Checkout does nothing" / "Clicking CHECKOUT doesn't work!" / "Can't complete purchase" |
| **Same word, different meanings** | One word can mean several things | "The test *passed*" / "The user *passed* a null value" |
| **Context changes meaning** | The words around a word matter | "Fails on retry" vs "Passes on retry" differ by one word, but mean opposite things |
| **Messy writing** | Typos, abbreviations, missing words | "chkout btn brkn on saf" |
| **Domain jargon** | Teams have their own words | "P1", "flaky", "smoke", "e2e", "SIT" |

A good NLP system has to cope with all of these. The simple methods in this lesson cope with some, and you will see exactly where they break.

### 3. Step One: Cleaning the Text

Here are the bug reports from the handout. A tester is about to log the **new bug**, and wants to know whether it is a duplicate:

```text
BUG-101: Checkout button does nothing on Safari after applying a coupon
BUG-102: Login page shows a blank screen on slow 3G network
BUG-103: Product images fail to load on the search results page
BUG-104: Cart total is wrong when two coupons are applied

NEW BUG: Safari: clicking CHECKOUT does nothing once a coupon code is applied!
```

Before comparing anything, an NLP system cleans the text. The usual steps:

1. **Lowercase** everything, so "CHECKOUT" and "checkout" count as the same word.
2. **Remove punctuation**, so "Safari:" and "applied!" become "safari" and "applied".
3. **Tokenise**: split the text into units called **tokens**. Here, a token is one word.
4. **Remove stop words**: very common words such as "a", "the", "is" and "on" that appear everywhere and rarely help tell texts apart.

Do it by hand for the new bug and you get: `safari, clicking, checkout, nothing, coupon, code, applied`. Notice that the shouting in "CHECKOUT" and the "!" have gone. That is the whole point of cleaning: remove differences that do not change the meaning.

A few lines of Python do the same:

```python
# clean_text.py
import re

STOP_WORDS = {"a", "an", "the", "is", "on", "once", "does", "after", "when", "are", "two"}

def clean(text):
    text = text.lower()                       # CHECKOUT -> checkout
    text = re.sub(r"[^a-z0-9 ]", " ", text)   # punctuation -> spaces
    return [w for w in text.split() if w not in STOP_WORDS]

print(clean("Safari: clicking CHECKOUT does nothing once a coupon code is applied!"))
print(clean("Cart total is wrong when two coupons are applied"))
```

Output:

```text
['safari', 'clicking', 'checkout', 'nothing', 'coupon', 'code', 'applied']
['cart', 'total', 'wrong', 'coupons', 'applied']
```

What to notice:

- `text.lower()` makes the text lowercase.
- `re.sub(r"[^a-z0-9 ]", " ", text)` uses a regular expression (Week 1) to replace every character that is **not** a letter, digit or space with a space.
- `text.split()` is the tokeniser: it splits on spaces.
- The list comprehension keeps only the words that are not in `STOP_WORDS`. Real libraries have stop-word lists of a few hundred words.

#### 3.1 Two cleaning traps

**Word forms.** Look at the second output: it says `coupons`, while the new bug says `coupon`. To a simple word matcher, those are different words. Two techniques fix this:

- **Stemming** chops words down to a rough root: "coupons" → "coupon", "applying" and "applied" → "appli". It is fast but crude.
- **Lemmatisation** uses a dictionary to find the proper base form: "applied" → "apply", "was" → "be". It is slower but more accurate.

**Stop words that matter.** Removing stop words is usually safe, but not always. Many standard lists include "not" and "no". Now compare *"Login does not work"* with *"Login does work"*. Drop "does" and "not", and both become `login, work`: the cleaning has erased the difference between a bug and a non-bug. When the text is short and the meaning is fragile, as in bug titles and test results, check your stop-word list.

### 4. Step Two: Turning Text into Numbers

Once the text is clean, it must become numbers.

#### 4.1 Bag of words

The simplest method is a **bag of words**. List every distinct word in all the documents (the **vocabulary**), then describe each document by how many times each word appears. Word order is thrown away, as if you tipped the words into a bag.

Take three short bug titles: *"checkout fails on safari"*, *"login fails on safari"* and *"checkout slow"*. After cleaning (dropping "on"), the vocabulary is: checkout, fails, safari, login, slow.

| Title | checkout | fails | safari | login | slow |
|---|---|---|---|---|---|
| checkout fails safari | 1 | 1 | 1 | 0 | 0 |
| login fails safari | 0 | 1 | 1 | 1 | 0 |
| checkout slow | 1 | 0 | 0 | 0 | 1 |

Each row is now a list of numbers, called a **vector**. The computer can compare these rows, just as you compared rows of features in the flaky-test table.

#### 4.2 TF-IDF: some words matter more

Should every word count the same? Imagine 5,000 bug reports from one shop. The word "page" might appear in a third of them, so sharing "page" says little. The word "coupon" might appear in only a few dozen, so sharing "coupon" is a strong clue.

**TF-IDF** (term frequency × inverse document frequency) builds that idea into the numbers:

- **Term frequency (TF):** how often a word appears in **this** document.
- **Inverse document frequency (IDF):** how **rare** the word is across **all** documents. Rare words score high; common words score low.

Multiply the two, and each word's value is high when it is frequent in this document but rare overall. Distinctive words, such as "safari" or "coupon", count for more than common ones.

**Work it by hand** with the three titles from section 4.1. A common form of IDF is log(N ÷ df), where **N** is the number of documents (3) and **df** is how many documents contain the word. Using the natural log:

| Word | Appears in (df) | IDF = log(3 ÷ df) |
|---|---|---|
| checkout | 2 titles | log(1.5) ≈ **0.41** |
| fails | 2 titles | ≈ **0.41** |
| safari | 2 titles | ≈ **0.41** |
| login | 1 title | log(3) ≈ **1.10** |
| slow | 1 title | ≈ **1.10** |

Each word appears once per title, so TF is 1, and TF-IDF equals the IDF. In *"login fails safari"*, the word "login" now counts almost three times as much as "fails" or "safari", because only one title mentions it. In a real tracker with thousands of reports, the gap between common and rare words is far bigger. Libraries such as scikit-learn use a slightly adjusted ("smoothed") formula, so their exact numbers differ, but the idea is the same.

### 5. Measuring Similarity: Is It a Duplicate?

#### 5.1 By hand: count the shared words

Start simply. For each existing bug, count how many of the new bug's important words (`safari, clicking, checkout, nothing, coupon, code, applied`) it also contains, after lowercasing:

| Bug | Shared important words | Count |
|---|---|---|
| BUG-101 | safari, checkout, nothing, coupon | **4** |
| BUG-102 | none | **0** |
| BUG-103 | none | **0** |
| BUG-104 | applied | **1** |

BUG-101 wins clearly. Notice that BUG-104 shares "applied" but **not** "coupon", because it says "coupons". Exact word matching treats them as different words, as section 3.1 warned.

#### 5.2 Cosine similarity

Counting shared words is a good start, but it favours long reports, which share more words just by being long. **Cosine similarity** fixes this. Think of each document's vector as an arrow. Cosine similarity measures the **angle** between two arrows, not their length:

- Arrows pointing the same way score **1**: the documents use words in the same proportions.
- Arrows at right angles score **0**: no words in common.

For word counts, scores run from 0 (nothing in common) to 1 (the same mix of words).

**Work it by hand** with the bag-of-words rows from section 4.1. The recipe: multiply matching numbers and add them up (the **dot product**), then divide by the two arrows' lengths (the square root of the sum of each row's squared numbers).

- *checkout fails safari* [1, 1, 1, 0, 0] vs *login fails safari* [0, 1, 1, 1, 0]: dot product = 0 + 1 + 1 + 0 + 0 = 2. Both lengths are √3 ≈ 1.73. Cosine = 2 ÷ (1.73 × 1.73) ≈ **0.67**.
- *checkout fails safari* [1, 1, 1, 0, 0] vs *checkout slow* [1, 0, 0, 0, 1]: dot product = 1. Lengths are √3 ≈ 1.73 and √2 ≈ 1.41. Cosine = 1 ÷ (1.73 × 1.41) ≈ **0.41**.

The first pair shares two words out of three, so it scores higher. Notice that this says nothing about whether they are the **same bug**: one is about checkout and one is about login. Similar wording is a clue, not a verdict.

#### 5.3 The duplicate finder

The handout's script combines TF-IDF and cosine similarity. It needs scikit-learn (`python -m pip install scikit-learn`).

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

bugs = {
    "BUG-101": "Checkout button does nothing on Safari after applying a coupon",
    "BUG-102": "Login page shows a blank screen on slow 3G network",
    "BUG-103": "Product images fail to load on the search results page",
    "BUG-104": "Cart total is wrong when two coupons are applied",
}
new_bug = "Safari: clicking CHECKOUT does nothing once a coupon code is applied!"

vectors = TfidfVectorizer(stop_words="english").fit_transform(list(bugs.values()) + [new_bug])
scores = cosine_similarity(vectors[-1], vectors[:-1])[0]          # new bug vs each old one
for bug_id, score in sorted(zip(bugs, scores), key=lambda p: p[1], reverse=True):
    print(f"{score:.2f}  {bug_id}  {bugs[bug_id]}")
```

Output:

```text
0.53  BUG-101  Checkout button does nothing on Safari after applying a coupon
0.13  BUG-104  Cart total is wrong when two coupons are applied
0.00  BUG-102  Login page shows a blank screen on slow 3G network
0.00  BUG-103  Product images fail to load on the search results page
```

What to notice:

- `TfidfVectorizer(stop_words="english")` does the cleaning from section 3, using scikit-learn's built-in English stop-word list, then builds TF-IDF vectors.
- `fit_transform(...)` learns the vocabulary and the IDF values from all five texts, then turns each one into a vector.
- `vectors[-1]` is the new bug (the last item), and `vectors[:-1]` is the four old bugs.
- `cosine_similarity` scores the new bug against each old one, and the loop prints them from most to least similar.

The script agrees with your hand count: BUG-101 first, and BUG-104 a little. A team might set a rule such as "warn about a possible duplicate if the score is above 0.4". Choosing that threshold is the precision-and-recall trade-off from *Supervised vs. Unsupervised Learning*: too low gives false alarms, too high misses duplicates.

### 6. The Blind Spot: Meaning

A different tester writes the new bug like this:

```text
NEW BUG: Discount voucher makes the basket price incorrect
```

A person sees at once that this is the **same problem as BUG-104**: a wrong cart total when a coupon is used. Now count shared words with BUG-104 by hand: discount, voucher, basket, price, incorrect against cart, total, wrong, coupons, applied. **Zero.**

Put this wording into `new_bug` and run the script again. We did, and **every score is 0.00**. Word matching cannot know that "voucher" means "coupon", "basket" means "cart", "price" means "total" and "incorrect" means "wrong". It sees spelling, not meaning.

This is the most important limit of classic word-based NLP, and it is common in real bug trackers, where different people describe the same defect in their own words.

### 7. Embeddings: Numbers That Capture Meaning

Modern NLP solves the blind spot with **embeddings**. An embedding is a list of numbers for a word or a piece of text, chosen so that **things with similar meanings get similar numbers**.

#### 7.1 A toy example, by hand

Real embeddings have hundreds or thousands of numbers each. To see the idea, here are made-up embeddings with just three numbers. They are **illustrative**, invented for this lesson. Imagine the three numbers mean roughly "about discounts", "about shopping containers" and "about signing in":

| Word | Discount | Container | Sign-in |
|---|---|---|---|
| coupon | 0.9 | 0.2 | 0.0 |
| voucher | 0.8 | 0.3 | 0.1 |
| basket | 0.2 | 0.9 | 0.0 |
| login | 0.0 | 0.1 | 0.9 |

"Coupon" and "voucher" have similar numbers, even though they share no letters in the right places. Measure it with cosine similarity:

1. Multiply matching numbers and add: 0.9 × 0.8 + 0.2 × 0.3 + 0.0 × 0.1 = **0.78**.
2. Find each arrow's length: √(0.81 + 0.04 + 0) ≈ 0.922 for coupon, and √(0.64 + 0.09 + 0.01) ≈ 0.860 for voucher.
3. Divide: 0.78 ÷ (0.922 × 0.860) ≈ **0.98**.

Do the same for the other pairs, and coupon–basket scores 0.42, while coupon–login scores **0.02**. With embeddings, "voucher" lands right next to "coupon", so the voucher bug can be matched to BUG-104.

#### 7.2 Where do the numbers come from?

Nobody types embeddings in. They are **learned** by a neural network from huge amounts of text, using one simple idea: **words that appear in similar contexts have similar meanings.** "Coupon" and "voucher" both turn up near "apply", "discount", "code" and "checkout", so training gives them similar numbers. A famous early method, **word2vec** (2013), learned embeddings this way.

Learned embeddings do not have neat, nameable dimensions like our toy table. Each of the hundreds of numbers is a pattern the network found useful, and no single one usually means "discount". You cannot read them, but you can measure distances between them.

#### 7.3 Contextual embeddings

Early embeddings gave each word **one** set of numbers, whatever the sentence. But "passed" in *"the test passed"* and *"the user passed a null value"* means different things. **Contextual embeddings** fix this: the numbers for a word depend on the words around it. Modern language models, including the AI assistants you use, work with contextual embeddings.

Embeddings of whole sentences also power **semantic search**: searching by meaning instead of by keyword. Search a bug tracker for "voucher breaks the basket", and semantic search can return BUG-104.

#### 7.4 Asking an AI assistant

Your AI assistant works with meaning, so it can make the link word matching missed. In the lecture you paste the four bugs and the voucher bug and ask:

```text
Is the new bug a likely duplicate of any existing bug?
Answer with the bug ID (or "none") and a one-line reason.
```

A good reply, **illustrative** and written for this lesson, looks like:

```text
BUG-104: both describe an incorrect cart/basket total when a coupon/voucher discount is used.
```

Check two things: that it picked BUG-104, and that its reason links the **meanings** (voucher ≈ coupon, basket ≈ cart, price ≈ total). As always, a confident answer still needs a person to confirm it, by opening BUG-104 and reading it.

### 8. Common NLP Tasks in Testing

| Task | What it does | Testing example |
|---|---|---|
| **Text classification** | Puts text into a category | Route a bug report to the right team |
| **Similarity / duplicate detection** | Measures how alike two texts are | Warn before logging a duplicate bug |
| **Named entity recognition** | Finds names of things in text | Pull browser names, versions and error codes out of bug reports |
| **Sentiment analysis** | Judges whether text is positive or negative | Spot angry app-store reviews after a release |
| **Summarisation** | Shortens long text | Summarise a 2,000-line failure log |
| **Text generation** | Writes new text | Draft test cases from a user story (this week) |

### 9. How NLP Got Here

You do not need the history in detail, but the stages explain why today's tools behave as they do:

1. **Rules** (from the 1950s): people wrote grammar rules and word lists by hand. Precise, but brittle.
2. **Statistics** (from the 1990s): counting words, as in bag of words and TF-IDF. Robust and cheap, but blind to meaning.
3. **Embeddings** (2010s): neural networks learned numbers that capture meaning.
4. **Transformers and large language models** (2017 onwards): very large networks trained on enormous amounts of text, using contextual embeddings. You will study these later today in *Generative AI Concepts*.

### 10. Classic NLP or an AI Assistant?

Newer is not always better. Both approaches have a place:

| | Classic NLP (word matching, TF-IDF) | AI assistant (LLM) |
|---|---|---|
| Understands meaning? | No: spelling only | Yes, largely |
| Same answer every time? | Yes | No: it can vary between runs |
| Speed and cost | Very fast, almost free | Slower; usually paid per use |
| Explainable? | Yes: you can list the shared words | Only through the reason it writes, which needs checking |
| Privacy | Runs on your machine | Text may go to an outside service |

A practical pattern combines them. Run cheap word matching over all 50,000 old bugs to pick the top 10 candidates, then ask an AI assistant, or a person, to judge those 10 by meaning. You get the speed of one and the understanding of the other.

### 11. Testing an NLP Feature Like a Tester

Suppose your team adds a "possible duplicate" warning to the bug tracker. How would you test it? The same way as any classifier, using what you learned in *Supervised vs. Unsupervised Learning*:

1. **Build labelled pairs.** Collect, say, 100 pairs of bug reports, and have people label each pair "duplicate" or "not duplicate". Include hard cases on purpose: same meaning in different words (the voucher bug), and similar words with different meaning (Safari vs Firefox, checkout vs login).
2. **Run the feature on every pair** and record its score and whether it warned.
3. **Measure precision and recall** at the chosen threshold. Low precision means testers learn to ignore the warning. Low recall means duplicates still get logged.
4. **Try a few thresholds**, and pick one with the team, based on which mistake costs more.
5. **Keep the labelled pairs** as a regression set, and re-run them whenever the feature, the threshold or the underlying model changes.

Those hard cases matter most. A duplicate finder tested only on easy examples, where duplicates share most of their words, will look excellent and then fail in real use. Choosing inputs that probe the edges is exactly the skill testers bring.

---

## Practice Exercises

1. **Clean and compare (paper, 10 min).** Clean these two bug titles by hand, using the stop-word list from `clean_text.py`, then count their shared words:
   - *"Search results are empty when the query has an apostrophe"*
   - *"Searching for O'Brien returns no results"*

   Would exact word matching call them duplicates? What would stemming change? Are they really the same bug?

2. **The "not" trap (paper, 5 min).** Write two bug titles that differ only by "not" or "no", where one describes a bug and the other describes correct behaviour. Clean both with a stop-word list that includes "not". What happens, and how would you fix the cleaning?

3. **Same words, different bug? (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** paste the handout's duplicate-check prompt, but replace the new bug with: *"Checkout button does nothing on Firefox after applying a coupon"*.
   - **Review:** does the AI call it a duplicate of BUG-101? What reason does it give? Does it mention the browser?
   - **Run:** put the same text into `new_bug` in `duplicate_finder.py` and run it. How high does BUG-101 score?
   - **Record:** as a tester, is this a duplicate, or a separate browser-specific bug? Write two sentences on what high word overlap does and does not prove.

   *Hint:* the browser is part of the bug's environment, and a Safari fix may not fix Firefox.

4. **Pick the tool (paper, 10 min).** For each task, choose classic NLP, an AI assistant, or both, and give one reason: (a) flagging any log line containing "ERROR" or "FATAL"; (b) deciding whether a customer complaint is about delivery, payment or product quality; (c) checking 50,000 old bugs for possible duplicates of a new one.

---

## Knowledge Check

1. What two things does every NLP system do with text before anything else?

<details><summary>Answer</summary>

It cleans the text (for example lowercasing, removing punctuation, tokenising and removing stop words), then turns it into numbers.

</details>

2. Why can removing stop words be risky for bug titles?

<details><summary>Answer</summary>

Some stop-word lists include words like "not" and "no". Removing them can make "Login does not work" and "Login does work" look identical.

</details>

3. What does TF-IDF add to simple word counts?

<details><summary>Answer</summary>

It gives more weight to words that are frequent in one document but rare across all documents, so distinctive words such as "coupon" count more than common ones such as "page".

</details>

4. Why did the "voucher" bug score 0.00 against every existing bug in `duplicate_finder.py`?

<details><summary>Answer</summary>

It shared no words with any of them. Word matching compares spelling, not meaning, so it cannot tell that "voucher" means "coupon" or "basket" means "cart".

</details>

5. What is an embedding, and how are its numbers chosen?

<details><summary>Answer</summary>

A list of numbers for a word or text, where similar meanings get similar numbers. The numbers are learned by a neural network from large amounts of text, based on the idea that words in similar contexts have similar meanings.

</details>

6. Give one reason to use classic word matching instead of an AI assistant.

<details><summary>Answer</summary>

Any one of: it is fast and almost free, it gives the same answer every time, you can explain it by listing the shared words, or it runs locally so no text leaves your machine.

</details>

---

## Glossary

- **Natural Language Processing (NLP):** the part of AI that works with human language.
- **Token:** one unit of text after splitting, such as a word.
- **Tokenisation:** splitting text into tokens.
- **Stop words:** very common words, such as "the" and "is", often removed before comparing texts.
- **Stemming:** cutting words down to a rough root ("coupons" → "coupon").
- **Lemmatisation:** reducing words to their dictionary form ("applied" → "apply").
- **Vocabulary:** the list of distinct words across all the documents.
- **Bag of words:** describing a document by its word counts, ignoring word order.
- **Vector:** a list of numbers that describes something.
- **TF-IDF:** word weights that are high for words frequent in a document but rare overall.
- **Dot product:** multiply matching numbers in two vectors and add the results.
- **Cosine similarity:** a score from the angle between two vectors; 1 means the same direction, 0 means nothing in common.
- **IDF (inverse document frequency):** a weight that is high for words found in few documents and low for words found in many.
- **Threshold (for duplicates):** the similarity score above which a tool warns "possible duplicate"; set it with precision and recall in mind.
- **Embedding:** a learned vector in which similar meanings get similar numbers.
- **word2vec:** an early, well-known method for learning word embeddings.
- **Contextual embedding:** an embedding that changes with the surrounding words.
- **Semantic search:** searching by meaning rather than by keyword.
- **Named entity recognition:** finding names of things, such as browsers or error codes, in text.
- **Sentiment analysis:** judging whether text is positive or negative.

---

## Summary

- **NLP lets computers work with human language**, and it always starts by cleaning text and turning it into numbers.
- **Cleaning removes trivial differences**, but watch the traps: word forms ("coupon" vs "coupons") and meaningful stop words ("not").
- **Word-based methods**, such as bag of words, TF-IDF and cosine similarity, are fast, cheap and explainable, and good at finding reports that share distinctive words.
- **Their blind spot is meaning**: "discount voucher makes the basket price incorrect" scored 0.00 against the bug it duplicates.
- **Embeddings capture meaning** as learned numbers, which is what lets AI assistants link "voucher" to "coupon".
- **Use both:** cheap word matching to narrow the field, then meaning-based judgement, from an AI or a person, to decide.

---

## Additional Resources

- Google for Developers, *Machine Learning Crash Course: Embeddings*: https://developers.google.com/machine-learning/crash-course/embeddings
- scikit-learn, *TfidfVectorizer* (the tool used in `duplicate_finder.py`): https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
- Jurafsky and Martin, *Speech and Language Processing* (free online textbook; the chapter on vector semantics and embeddings goes further): https://web.stanford.edu/~jurafsky/slp3/
