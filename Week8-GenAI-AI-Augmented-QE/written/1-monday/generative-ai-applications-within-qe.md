# Generative AI Applications within QE

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish **AI for testing** (using AI to help test) from **testing of AI** (testing AI-powered products).
- Map Generative AI applications onto the stages of the **software testing life cycle (STLC)** you learned in Week 3.
- Describe the most common GenAI applications in QE (requirements review, test idea generation, test data, test code drafting, failure analysis, defect reporting, reporting and knowledge support) and the **value and risk** of each.
- Recognise the main **categories of AI tools** used by QE teams.
- Decide when a problem suits **Generative AI**, when it suits **classic ML or NLP** (from earlier today) and when it needs **no AI at all**.
- **Evaluate and prioritise** candidate GenAI use cases with a simple scoring framework, including a small Python helper.
- Explain, with a concrete example, why AI output in QE must always be **reviewed by a human**, and connect today's ideas to your **Project 2** work.

---

## Why This Matters

You now know what Generative AI is and how it works. The natural next question is: **where does it actually help a quality engineer, and where does it not?**

The industry has moved past asking *whether* to use GenAI in testing. Testing organisations now publish guidance on it; for example, ISTQB, the body behind many testing certifications, introduced a dedicated **Certified Tester: Testing with Generative AI (CT-GenAI)** specialist certification covering GenAI across the test process, its risks and its adoption. Employers increasingly expect test automation engineers to use AI tools productively **and** responsibly.

But hype is everywhere. Some claims ("AI writes all your tests", "no more test maintenance") are unrealistic, and teams that believe them end up with large volumes of low-value or incorrect tests. A skilled engineer can tell a strong use case from a weak one.

This lesson gives you a **map** of the landscape. It deliberately stays at the "what and why" level. The "how" is coming fast: prompt engineering and AI-assisted test design and debugging on **Tuesday**; AI across the QA life cycle, including requirements, test cases, test data, automation, human validation and responsible use, on **Wednesday**; and agents on **Thursday and Friday**. Today's exercise asks you to research and present three GenAI use cases for Project 2, and this lesson is your preparation for it.

---

## The Concept

### 1. Two Different Relationships Between AI and QE

| | AI **for** testing | Testing **of** AI |
|--|--------------------|-------------------|
| Meaning | Using AI tools to make QE work faster or better. | Verifying the quality of products that contain AI features (chatbots, recommendation engines, AI search). |
| Example | Using an assistant to draft test scenarios for a checkout page. | Testing that a support chatbot gives accurate, safe answers. |
| Where in this course | **This week** | Later weeks of the program |

This lesson, and this week, focus on **AI for testing**. Keep the distinction clear when you read articles or talk to colleagues, because the two need very different skills.

### 2. Where GenAI Fits in the Testing Life Cycle

Recall the main STLC activities from Week 3. Generative AI can contribute to almost every one of them, but not equally well:

| STLC activity | GenAI application | Typical value | Key risk | Covered in depth |
|---------------|-------------------|---------------|----------|------------------|
| **Test planning** | Drafting test strategy outlines, risk lists, checklists | Faster first drafts; fewer forgotten areas | Generic content not tailored to your product | Wednesday |
| **Requirements analysis** | Spotting ambiguity, gaps and contradictions; suggesting clarifying questions | Problems found before any code is written | Missing domain-specific gaps; inventing requirements | Wednesday |
| **Test design** | Suggesting test ideas, scenarios, edge cases, Gherkin drafts | Broader coverage ideas, quickly | Plausible but wrong expected results; duplicate or low-value tests | Tuesday and Wednesday |
| **Test data** | Generating realistic synthetic records, boundary values, varied inputs | Realistic data without using real customer data | Invalid or unrealistic data; accidental use of real personal data | Wednesday |
| **Test automation** | Drafting, explaining and refactoring test code (pytest, Playwright, Selenium) | Faster coding; help with unfamiliar APIs | Hallucinated methods; brittle locators; weak assertions | Tuesday and Wednesday |
| **Test execution and debugging** | Explaining errors, summarising logs, suggesting likely causes | Faster diagnosis | Confident but wrong explanations | Tuesday |
| **Defect management** | Drafting clear bug reports, summarising long threads, suggesting duplicates | Clearer, more consistent reports | Misstated reproduction steps or severity | Wednesday |
| **Reporting and closure** | Summarising results for different audiences | Faster communication | Over-optimistic or inaccurate summaries | Wednesday |

The final column matters for this course: today you learn **what is possible**; the following days teach you **how to do it well**.

### 3. A Closer Look at the Main Applications

#### 3.1 Requirements review

**What:** You give an AI assistant a user story or specification and ask it to look for ambiguity, missing details, conflicting statements and untestable wording.

**Why it helps:** Defects found in requirements are the cheapest to fix (you saw the cost-of-defects idea in Week 3). An assistant can quickly flag phrases like *"the page should load fast"* (how fast? under what load?) or *"users can apply a discount"* (which users? one discount or several?).

**Watch out for:** The model does not know your business rules. It may "fill in" missing details with invented assumptions that *sound* official.

*Illustration (simplified):*

```text
Requirement:  "Registered users can apply one coupon per order. Coupons expire."

Possible AI observations:
- "Expire" is undefined: after a fixed date? after N days? at what time zone?
- What happens if a guest user tries to apply a coupon?
- Can a coupon be removed and a different one applied?
- What message is shown for an expired coupon?
```

These are exactly the kinds of questions a good tester raises. AI helps you raise them faster, but **you** decide which are relevant.

#### 3.2 Test idea and scenario generation

**What:** Generating lists of test ideas, positive and negative scenarios, boundary cases and Gherkin drafts from a feature description.

**Why it helps:** Breadth. LLMs have seen a huge number of examples of software features and their typical failure points (empty inputs, very long strings, special characters, time zones, concurrency), so they are good at suggesting ideas you might not think of under time pressure.

**Watch out for:** Quantity is not quality. A list of 60 generated scenarios may contain duplicates, trivial cases and scenarios with **wrong expected results**. Test design techniques you already know (equivalence partitioning, boundary value analysis, decision tables) remain the yardstick for judging the list.

#### 3.3 Test data generation

**What:** Producing synthetic but realistic data: user profiles, addresses, product catalogues, invalid inputs, multilingual names, edge-case strings.

**Why it helps:** Realistic, varied data finds defects that `"test1"`, `"test2"` never will (names with apostrophes, addresses with unusual formats, emoji). Synthetic data also avoids copying **real customer data** into test environments, which is often prohibited by privacy rules.

**Watch out for:** Generated data may break your system's validation rules, be less varied than it looks, or accidentally resemble real people. Generated data still needs checking against the rules of your domain.

#### 3.4 Drafting and improving test code

**What:** Coding assistants suggest code as you type in your IDE, or produce code on request: a pytest fixture, a Playwright page object, an API test using `requests` (as in Week 7). They can also **explain** unfamiliar code and **refactor** repetitive tests.

**Why it helps:** Less time on boilerplate; faster learning of new libraries; help translating a manual test case into an automated skeleton.

**Watch out for:** Code that **looks** correct but calls methods that do not exist (hallucination), uses outdated APIs (knowledge cut-off), relies on fragile locators, or contains **weak assertions** that can never fail. Section 7 shows a concrete example.

#### 3.5 Debugging and failure analysis

**What:** Pasting an error, stack trace or log extract and asking for an explanation and likely causes; summarising a long CI log.

**Why it helps:** Faster orientation, especially with unfamiliar stacks or noisy logs.

**Watch out for:** The model only sees what you give it (the context window, from the previous lesson). It will often suggest a **plausible** cause rather than the **actual** one. Treat explanations as hypotheses to verify, never as conclusions. Also be careful what logs contain before sharing them (tokens, passwords, personal data).

#### 3.6 Defect reporting and triage

**What:** Turning rough notes into a structured bug report (title, steps, expected vs. actual, environment); summarising a long defect discussion; suggesting possible duplicates.

**Why it helps:** Clear, consistent bug reports save developer time. Duplicate detection reduces noise. Recall from the NLP lesson that duplicate detection can be done with TF-IDF and cosine similarity, or with embeddings for meaning-based matching; GenAI adds the ability to *explain* why two reports seem related.

**Watch out for:** AI rewriting can subtly change reproduction steps or overstate severity. The reporter must confirm the final version.

#### 3.7 Test reporting and communication

**What:** Summarising test results for different audiences, for example a technical summary for developers and a short risk-focused update for a product owner.

**Watch out for:** Summaries that sound reassuring while omitting a critical failure. Numbers in summaries must be checked against the real report (recall that LLMs are weak at exact counting).

#### 3.8 Knowledge support and onboarding

**What:** Asking questions about a test framework, a library, a codebase or a testing concept; generating explanations or study material.

**Why it helps:** Faster onboarding to new projects, such as joining a team with a large existing Playwright framework.

**Watch out for:** Out-of-date or invented answers about specific tools. Prefer official documentation for anything you will rely on, as you have throughout this course.

#### 3.9 AI features inside testing tools

Many commercial and open-source testing tools now include AI features, such as suggesting or repairing locators when the UI changes ("self-healing"), visual comparison that ignores insignificant differences, or natural-language test authoring. Capabilities vary widely between tools and change frequently, so evaluate any specific claim with a proof of concept on **your** application rather than trusting marketing material.

#### 3.10 Agents: the next step

So far, every application is a **single interaction**: you ask, the AI answers, you review. An **AI agent** goes further, using an LLM to work through multi-step tasks, sometimes using tools along the way. You will dissect agent anatomy on Thursday and build your **first QA agent** on Friday; agentic QE continues in Week 9. For now, just know that agents build on everything in this lesson, and they make reviewing and validating output even more important.

### 4. The Tool Landscape

You will meet four broad categories of tools. Specific products change quickly, so learn the categories:

| Category | What it is | Typical QE use |
|----------|-----------|----------------|
| **General chat assistants** | Web or desktop chat interfaces to an LLM. | Requirements review, test ideas, explanations, drafting reports. |
| **IDE coding assistants** | Assistants integrated into editors such as VS Code (for example GitHub Copilot and similar tools). | Code completion, generating and explaining test code, refactoring. |
| **AI features in test platforms** | AI built into test management, automation or visual testing tools. | Locator suggestions, test authoring, result analysis. |
| **LLM APIs** | Programmatic access to models from code. | Building your own tools and agents, such as Friday's QA agent. |

Your organisation may approve some tools and prohibit others, often because of where your data is sent and stored. Always use the tools approved for the data you are working with. Responsible use is covered in depth on Wednesday.

### 5. GenAI, Classic ML or No AI? Choosing the Right Tool

Today's earlier lessons give you a fuller toolbox than "just use an LLM". A good engineer chooses deliberately:

| Problem | Best fit | Why |
|---------|---------|-----|
| Check that a field accepts at most 50 characters | **No AI**: a normal parametrised pytest test | Deterministic rule; AI adds nothing but variability. |
| Group 20,000 nightly failure messages into kinds | **Classic ML/NLP** (TF-IDF + clustering) | Fast, cheap, repeatable, works offline. |
| Predict which tests are likely to fail for a change, from CI history | **Classic supervised ML** | Numeric, tabular, labelled history. |
| Find possible duplicates for a newly filed bug | **Classic NLP or embeddings**, optionally with GenAI to explain matches | Similarity search is a well-solved problem. |
| Draft test scenarios from a new user story | **GenAI** | Needs language understanding and broad knowledge of typical failure points. |
| Summarise a confusing 80-message defect thread for a manager | **GenAI** | Natural language generation for a specific audience. |
| Draft a Playwright page object for a new page | **GenAI** (IDE assistant), then human review | Accelerates boilerplate; human ensures correctness. |

Rules of thumb:

- If a **simple deterministic rule** solves it, do not use AI.
- If you have **lots of structured or labelled data** and need **repeatable** results at scale, consider **classic ML/NLP**.
- If the task needs **understanding or producing natural language or code** and a human can **check the result**, consider **GenAI**.

### 6. Evaluating and Prioritising Use Cases

Not every possible application is worth pursuing. Before adopting a GenAI use case, evaluate it against a few criteria:

| Criterion | Question to ask | Why it matters |
|-----------|----------------|----------------|
| **Value** | How much time or quality improvement would it bring? | Effort should go where the payoff is. |
| **Frequency** | How often does the team do this task? | A daily task benefits far more than a yearly one. |
| **Verifiability** | How easily and quickly can a human check the AI's output? | If checking takes as long as doing it, the benefit disappears; if it cannot be checked, the risk is high. |
| **Risk if wrong** | What happens if a wrong output slips through? | A bad test idea wastes minutes; a wrong "all clear" summary could ship a defect. |
| **Data sensitivity** | Does the task involve secrets, personal or confidential data? | May rule out tools or require approved environments. |
| **Effort to adopt** | How much setup, learning or integration is needed? | Quick wins build confidence. |

**Verifiability** is the criterion beginners most often overlook, and it is the most important for QE. A useful habit: *for every AI use case, name who checks the output and how.*

The following small Python helper turns these criteria into a ranked list. It is plain Python, no AI involved; it is a decision aid, not a decision maker.

```python
# rank_use_cases.py
from dataclasses import dataclass

@dataclass
class UseCase:
    name: str
    value: int            # 1 (low) to 5 (high)
    frequency: int        # 1 (rare) to 5 (daily)
    verifiability: int    # 1 (hard to check) to 5 (easy to check)
    risk_if_wrong: int    # 1 (harmless) to 5 (severe)
    data_sensitivity: int # 1 (public/synthetic) to 5 (highly sensitive)

WEIGHTS = {"value": 3, "frequency": 2, "verifiability": 3, "risk_if_wrong": -2, "data_sensitivity": -2}

def score(uc: UseCase) -> int:
    return sum(weight * getattr(uc, field) for field, weight in WEIGHTS.items())

candidates = [
    UseCase("Draft edge-case ideas for new user stories", 4, 4, 4, 2, 1),
    UseCase("Summarise nightly CI failure logs", 4, 5, 3, 3, 3),
    UseCase("Generate synthetic customer records", 3, 3, 4, 2, 2),
    UseCase("Auto-approve releases from test summaries", 5, 3, 1, 5, 2),
]

for uc in sorted(candidates, key=score, reverse=True):
    print(f"{score(uc):4d}  {uc.name}")
```

**Code walkthrough:**

- `@dataclass` (a Python feature you met in Week 2's advanced Python) generates the `__init__` method for us, so each `UseCase` is a tidy record with named fields.
- `WEIGHTS` encodes priorities: value and verifiability count strongly in favour; risk and sensitivity count **against** (negative weights).
- `getattr(uc, field)` reads a field by its name as a string, so one loop handles every criterion.
- `sorted(..., key=score, reverse=True)` ranks highest score first.
- Notice where *"Auto-approve releases from test summaries"* lands. High value on paper, but terrible verifiability and severe risk if wrong. That reflects a core principle: **GenAI in QE assists human judgement; it does not replace it.**

Change the scores and weights to reflect your own team's situation; the point is to make the reasoning **explicit and discussable**, not to produce a magic number.

### 7. Why Every AI Output Needs a Reviewer: A Concrete Example

Here is a small function from a generic e-commerce web app, with its requirement in the docstring:

```python
# cart.py
def apply_coupon(total: float, code: str) -> float:
    """SAVE10 gives 10% off orders of $50.00 or more.
    Orders under $50.00 are unchanged. Unknown codes raise ValueError."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total
```

Imagine an AI assistant drafted these tests. They look tidy and professional:

```python
# test_cart_ai_draft.py
from cart import apply_coupon

def test_save10_applies_discount():
    assert apply_coupon(100, "SAVE10") == 90

def test_save10_small_order_gets_discount():
    assert apply_coupon(20, "SAVE10") < 20          # (1)

def test_unknown_coupon_returns_original_total():
    assert apply_coupon(100, "BOGUS") == 100         # (2)

def test_coupon_is_case_insensitive():
    assert apply_coupon(100, "save10") == 90         # (3)
```

Run them with `pytest test_cart_ai_draft.py` and three of the four fail. But here **the code is correct and the tests are wrong**:

1. **Contradicts the requirement.** Orders under $50 should be unchanged, not discounted.
2. **Wrong expected behaviour.** The requirement says unknown codes raise `ValueError`; a correct test would use `pytest.raises(ValueError)`.
3. **Invents a requirement.** Nothing says coupons are case-insensitive. The AI filled a gap with a plausible assumption, which is a form of hallucination.

And something important is **missing**: no boundary tests at exactly **$50.00** and just below (**$49.99**), which is where defects most often hide (boundary value analysis, Week 3).

Now imagine the opposite situation: the code had a bug and the AI-generated tests were written to match the buggy behaviour. They would all **pass**, giving false confidence. Either way, the tests are only as good as the human review behind them. This is why **human validation of AI output** is a central skill of this week. You will learn a structured approach to it on Wednesday.

### 8. Setting Realistic Expectations

| Realistic benefits | Unrealistic expectations |
|--------------------|-------------------------|
| Faster first drafts of tests, data, reports and code | "AI writes the entire test suite for us" |
| Broader brainstorming of scenarios and edge cases | "AI-generated tests are correct by default" |
| Quicker understanding of unfamiliar code and errors | "AI knows our system and business rules" |
| More consistent documentation and bug reports | "We no longer need test design skills" |
| Lower barrier to learning new tools | "AI removes the need for maintenance" |

Your testing knowledge becomes **more** valuable with AI, not less. The engineer who knows boundary value analysis is the one who notices the missing $49.99 test. To know whether a use case is really working, teams measure things like time saved per task, the proportion of AI output accepted without major rework, and defects found, rather than relying on impressions.

### 9. Connecting to Project 2

Your Project 2 is a **test automation framework** for a web application. Assuming a generic web app with typical features (registration and login, product search, cart and checkout), here are examples of the **kinds** of candidates you might consider:

- Reviewing user stories for the checkout flow to surface ambiguities before automating them.
- Brainstorming negative and boundary scenarios for the registration form.
- Generating synthetic user and product data for data-driven tests.
- Drafting page-object skeletons for new pages, then reviewing and hardening them.
- Summarising failed CI runs of your Playwright suite for a daily stand-up.

In today's exercise you will research and present **three** GenAI use cases for Project 2. Use the criteria in section 6, and for each use case be ready to answer: **What is the value? How will a human verify the output? What could go wrong?** Do not worry yet about *how* to write the prompts; that is exactly what Tuesday is for.

---

## Practice Exercises

1. **Map the life cycle.** For each STLC activity in section 2, write one GenAI application specific to a login page of a generic web app.
2. **GenAI, classic ML or no AI?** Decide and justify in one sentence each: (a) verify that a password field masks input; (b) group 3,000 Selenium failure messages from last quarter; (c) turn a product owner's rough notes into Gherkin draft scenarios; (d) estimate the run time of a test suite from its size and worker count.
3. **Fix the AI draft.** Rewrite `test_cart_ai_draft.py` from section 7 so that it correctly reflects the requirement. Include boundary tests at 49.99 and 50.00 and use `pytest.raises` for the unknown-code case. Run your tests against `cart.py`.
4. **Rank your own use cases.** Add three Project 2 use cases to `rank_use_cases.py` with your own scores. Then change the verifiability weight from `3` to `0` and observe how the ranking changes. Write two sentences on why verifiability deserves a strong weight in QE.
5. **Spot the hype.** Find one article, product page or social media post that makes a claim about AI in testing. Classify the claim as realistic or unrealistic using section 8, and explain your reasoning.

---

## Knowledge Check

1. What is the difference between "AI for testing" and "testing of AI"?
2. Name four STLC activities where GenAI can help, with one application each.
3. Why is verifiability such an important criterion when choosing a GenAI use case in QE?
4. Give one QE problem better suited to classic ML/NLP than to GenAI, and explain why.
5. In the `apply_coupon` example, name two different kinds of mistake in the AI-drafted tests.

<details>
<summary>Suggested answers</summary>

1. AI for testing uses AI tools to help perform QE work; testing of AI verifies products that contain AI features.
2. For example: requirements analysis (ambiguity review), test design (scenario ideas), test data (synthetic records), automation (drafting test code), debugging (log summaries), defect management (bug report drafts).
3. Because AI output can be wrong while looking right; if a human cannot check it efficiently and reliably, the risk is high and the time saved disappears.
4. Clustering thousands of failure messages: classic NLP is fast, cheap, repeatable and runs locally at scale.
5. Any two of: an expected result that contradicts the requirement (small orders discounted), wrong behaviour for unknown codes (returns total instead of raising), an invented requirement (case-insensitivity), missing boundary tests.

</details>

---

## Glossary

- **AI for testing:** Using AI tools to support QE activities.
- **Testing of AI:** Verifying the quality of AI-powered products.
- **STLC:** Software Testing Life Cycle, the stages of testing activity from planning to closure.
- **Coding assistant:** An AI tool integrated into an editor that suggests or generates code.
- **Synthetic data:** Artificially generated data that mimics real data without being real records.
- **Verifiability:** How easily and reliably a human can check whether an AI output is correct.
- **Self-healing locator:** A tool feature that attempts to adapt a UI locator automatically when the page changes.
- **AI agent:** A system that uses an LLM to work through multi-step tasks, often using tools (covered Thursday and Friday).

---

## Summary

- Distinguish **AI for testing** (this week) from **testing of AI** (later weeks).
- GenAI can assist **every STLC activity**: requirements review, test design, test data, automation, debugging, defect reporting and communication. Each has real value and real risks.
- Tools fall into four categories: **chat assistants, IDE coding assistants, AI features in test platforms and LLM APIs**.
- Choose deliberately between **no AI, classic ML/NLP and GenAI**; deterministic problems need deterministic solutions.
- Evaluate use cases on **value, frequency, verifiability, risk if wrong, data sensitivity and effort**. Verifiability is crucial in QE.
- AI-generated tests can be wrong in ways that look right. **Human review is not optional**, and your test design skills are what make that review effective.
- Tomorrow you learn how to communicate with these tools effectively through prompt engineering.

---

## Additional Resources

- ISTQB, *Certified Tester: Testing with Generative AI (CT-GenAI)* (syllabus and overview of GenAI across the test process): https://istqb.org/certifications/gen-ai/
- GitHub Docs, *Quickstart for GitHub Copilot* (an example of an IDE coding assistant): https://docs.github.com/en/copilot/get-started/quickstart
- NIST, *Generative Artificial Intelligence Profile (NIST AI 600-1)* (risks to keep in mind when adopting GenAI): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
