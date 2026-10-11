# Testing Principles: The Seven ISTQB Principles

## Learning Objectives

By the end of this lesson, you will be able to:

- State each of the seven ISTQB testing principles in your own plain words.
- Explain why each principle is true, using a reason and not just a slogan.
- Recognize each principle at work in a realistic project scenario.
- Calculate how quickly the number of possible input combinations grows, and explain why that makes exhaustive testing impossible.
- Use principles to make practical decisions about what to test first, how much to test, and when to stop.
- Apply all seven principles to the login and registration feature of Project 1 - QE Foundations.
- Separate the official ISTQB principles from other commonly cited testing heuristics (rules of thumb).
- Spot and correct common misunderstandings about each principle.

---

## Why This Matters

Earlier this week and earlier today you learned a lot of vocabulary and process: the SDLC (Software Development Life Cycle), the STLC (Software Testing Life Cycle), the defect lifecycle, QA versus QC, verification versus validation, and the difference between an error, a defect, and a failure. Those are the "what" of testing.

This lesson is about the "why" and the "how much." Testing principles are a short list of hard-won truths about testing that hold true across almost every project, technology, and company. They are the closest thing our profession has to laws of physics. You cannot ignore them, but once you understand them they make your decisions easier.

Here is why they matter to you as a future AI-enabled Test Automation Engineer:

1. **They protect you from impossible promises.** Someone will eventually ask you, "Can you guarantee there are no bugs?" The principles tell you the honest answer and give you the words to explain it.
2. **They help you decide where to spend limited time.** You will never have enough time to test everything. The principles tell you how to choose wisely.
3. **They shape automation.** Automation is powerful, but it can only repeat what you teach it. Several principles (exhaustive testing, pesticide paradox, context dependence) tell you what automation can and cannot do for you.
4. **They are examined.** The principles are a core part of the ISTQB Foundation Level syllabus, and interviewers love to ask about them.
5. **They are the foundation for what comes next.** Tomorrow you will learn test design techniques, which are the practical answer to the second principle. The next lesson covers positive and negative testing. Friday covers regression testing. All of these build on the ideas here.

Think of the principles as a compass. They do not give you turn-by-turn directions, but they keep you heading in the right direction when the map runs out.

---

## Where the Principles Come From

Software testing as a profession is decades old, and over that time practitioners noticed the same patterns again and again, regardless of the technology. Writers, researchers, and experienced testers began collecting these patterns into short lists of "principles." Different authors have published different lists over the years.

The version most widely used in training and certification is the list of **seven testing principles** formalized in the syllabus published by the **ISTQB** (International Software Testing Qualifications Board). ISTQB is an international, non-profit body that defines a common vocabulary and body of knowledge for testers and offers the Certified Tester certification family. Its Foundation Level syllabus lists the seven principles, and many countries' testing boards and training providers teach from it.

A few honest notes about this history:

- The principles are not a mathematical proof. They are consolidated professional experience.
- They are formalized in the ISTQB Foundation Level syllabus. Exact wording has been refined across syllabus versions. In some recent versions, a few principles are phrased slightly differently (for example, the "pesticide paradox" idea is also described as tests "wearing out," and the "absence-of-errors fallacy" is sometimes called the "absence-of-defects fallacy"). The ideas are the same.
- You should always check the current syllabus on the ISTQB website for the official wording if you plan to take the exam.

In this lesson we use the traditional names, because they are the ones you will hear most often in the industry.

---

## The Concept: The Seven Principles

For each principle below you will find: the plain statement, why it is true, a story, what it means in practice, how it applies to Project 1's login and registration feature, a common misunderstanding, and a quick check question.

A quick reminder about **Project 1 - QE Foundations**: it is the sample web application we use all week to practice quality-engineering habits. Today's exercise will have you write positive and negative test cases for its **login** and **registration** feature. Registration lets a new visitor create an account (typically with fields such as name, email, password, and password confirmation). Login lets an existing user sign in with their credentials. Keep that feature in mind as we go.

---

### Principle 1: Testing Shows the Presence of Defects, Not Their Absence

#### Plain statement

Testing can show that defects exist. It can never prove that there are none. Even if you run a thousand tests and they all pass, you cannot say "this software is bug-free." You can only say "we did not find any defects with the tests we ran."

#### Why it is true

Think about what a passing test actually proves. It proves that for one specific set of inputs, in one specific environment, under one specific set of conditions, the software behaved correctly. It says nothing about every input you did not try.

An analogy: imagine you want to prove "all swans are white." You can look at a thousand white swans and feel more confident, but you can never be certain. A single black swan, seen once, proves the statement false. Software testing works the same way. One failing test proves a defect exists. A thousand passing tests only increase your confidence.

The second reason is the next principle: because you cannot test everything, there will always be untested situations where a hidden defect could be waiting.

#### A story

A small team builds an online ticketing site. They run 600 tests before launch and all pass. The release manager announces, "Testing found nothing, so the product is clean." Two weeks after launch, a customer in a time zone far from the company's headquarters buys a ticket at 11:50 PM on the last day of the month, and the confirmation email shows the wrong event date. None of the 600 tests had tried that combination of time zone and date.

The 600 passing tests were real work and gave real confidence. The mistake was the claim "no bugs." The correct claim would have been: "We ran 600 tests, found and fixed the defects those tests revealed, and the remaining risk is low in the areas we tested."

#### What it means in practice

- **Report with honest language.** Say "no defects were found by the tests we executed" and "our confidence is high in the areas we covered," not "the software is perfect."
- **Describe your coverage.** Always be ready to say what you tested and what you did not. Coverage (how much of the requirements, features, or code your tests exercise) is how you communicate the limits of your testing.
- **Aim your tests at finding defects.** A test designed to confirm that things work will happily pass. A test designed to try to break things is more likely to reveal problems. This links to the testing mindset you studied earlier today.
- **Reduce risk, do not claim certainty.** Testing's job is to reduce the risk of defects remaining in the product to an acceptable level, and to give stakeholders (the people with an interest in the product) the information they need to decide.

#### Applied to Project 1: login and registration

Suppose you write 15 test cases for registration and all pass. You can say: "The registration scenarios we designed work correctly." You cannot say "registration is bug-free." Perhaps nobody tried a 300-character email address, an email with a plus sign, or two people registering with the same email at the same instant. Passing tests are evidence, not proof.

#### Common misunderstanding

"If all my tests pass, the software is ready and correct." Passing tests are good news, but "ready" is a business decision based on risk, coverage, and exit criteria (the agreed conditions for finishing a test phase, which you met on Tuesday), not just a green result.

#### Quick check

*Your teammate says: "We ran 200 tests and every single one passed, so there are zero bugs." What is wrong with this statement?*

(Answer: Passing tests show that the tested situations work. They cannot prove that no defects remain in situations that were not tested. The accurate statement is that no defects were found by those 200 tests.)

---

### Principle 2: Exhaustive Testing Is Impossible

#### Plain statement

It is not possible to test every combination of inputs, preconditions (the starting conditions), and paths through the software, except in trivial cases. Because of that, we must choose a smaller, smart set of tests.

**Exhaustive testing** means testing every possible input value in every possible combination under every possible condition.

#### Why it is true: the numbers

The number of combinations grows by multiplication, and multiplication grows very fast. Let us build a realistic example for a registration form. Suppose the form (and the environment around it) has these choices:

| Factor | Number of options |
|---|---|
| Country (a drop-down of 10 countries) | 10 |
| Browser (Chrome, Firefox, Safari, Edge) | 4 |
| Device (desktop, tablet, phone) | 3 |
| Newsletter checkbox (opted in or out) | 2 |
| Account type (Personal, Business, Student) | 3 |
| Payment plan (Free, Monthly, Yearly) | 3 |
| Language (5 languages) | 5 |

To find the total number of combinations, multiply the options:

10 x 4 x 3 x 2 x 3 x 3 x 5 = **10,800 combinations**

Notice that we have not even typed anything into a text field yet. This is only the "choose from a list" parts. If each test takes about 30 seconds to run by hand and you work without stopping, 10,800 tests take 324,000 seconds, which is about 3.75 days of non-stop testing. That is for a small form, and for one round of testing only.

Now consider the text fields. Suppose the password field accepts up to 20 characters, and each character could be any of roughly 95 printable keyboard characters. The number of possible 20-character passwords is 95 multiplied by itself 20 times, which is roughly 3.6 followed by 39 zeros (3.6 x 10^39). Even a computer checking a billion passwords per second would not finish in any useful lifetime. And we have not counted shorter passwords, or combined the password with the other fields.

You can verify the first calculation yourself with a tiny Python program. `itertools.product` produces every combination of several lists.

```python
from itertools import product

# Each factor lists its representative options
country = ["USA", "Canada", "UK", "India", "Germany",
           "Brazil", "Japan", "Australia", "France", "Mexico"]
browser = ["Chrome", "Firefox", "Safari", "Edge"]
device = ["Desktop", "Tablet", "Phone"]
newsletter = ["opted in", "opted out"]
account_type = ["Personal", "Business", "Student"]
payment_plan = ["Free", "Monthly", "Yearly"]
language = ["English", "Spanish", "French", "German", "Hindi"]

fields = [country, browser, device, newsletter,
          account_type, payment_plan, language]

combos = list(product(*fields))
print("Total combinations:", len(combos))
print("First one:", combos[0])

# At 30 seconds per test, running non-stop
seconds = len(combos) * 30
print("Days of non-stop testing:", round(seconds / 86400, 1))
```

When run, this prints:

```
Total combinations: 10800
First one: ('USA', 'Chrome', 'Desktop', 'opted in', 'Personal', 'Free', 'English')
Days of non-stop testing: 3.8
```

Try adding one more factor with 4 options and re-run it. The total jumps to 43,200. Every new factor multiplies the total, which is why the growth feels explosive.

There is also a second source of impossibility: **paths**. Software contains decisions ("if the password is too short, show an error; otherwise continue"). Every decision splits the flow in two. Twenty independent decisions in sequence create over a million possible paths. And a third: **timing and state**. Things like network speed, how many users are online, what was done earlier in the session, and the time of day all influence behavior.

#### A story

A test lead at a travel company once tried to schedule "complete" testing of the flight-search screen: every origin, every destination, every date, every passenger count, every cabin class. She calculated the total and found that, even with automation running around the clock, the answer was measured in centuries. She replaced the plan with a risk-based set of a few hundred carefully chosen tests, and the team shipped on time with no embarrassing surprises. The lesson: the right goal is not "test everything" but "test the right things."

#### What it means in practice

- **You must choose.** Selecting what to test is not laziness. It is the core skill of a tester.
- **Use techniques to select tests intelligently.** Tomorrow you will learn test design techniques such as equivalence partitioning and boundary value analysis. These are the practical answer to this principle: they let you pick a small number of tests that represent huge ranges of inputs. For today, just know that they exist and that they build directly on this principle.
- **Use risk and priority.** Test the areas where failure would hurt the most, and where failure is most likely, first. We introduce this later in this lesson.
- **Be transparent about what is not covered.** Because some areas will be tested lightly or not at all, make this visible to stakeholders.

#### Applied to Project 1: login and registration

Consider only the email field of registration. It accepts text of many lengths, with letters, digits, symbols, unicode characters, and spaces. You cannot try every possible email. Instead you will choose representatives: a normal valid email, an email missing the "@", one with two "@" symbols, an extremely long one, an empty one, and so on. Each representative stands in for a whole group of similar inputs. That choice is exactly what you will practice in today's exercise.

#### Common misunderstanding

"Automation will let us run everything, so exhaustive testing becomes possible." Automation makes tests faster and repeatable, but it does not change the arithmetic. Even at a million tests per second, the password example above is hopeless. Automation lets you run more tests, but you still have to choose which ones.

#### Quick check

*A form has 5 drop-downs with 6 options each. How many combinations of drop-down choices are there?*

(Answer: 6 x 6 x 6 x 6 x 6 = 6^5 = 7,776.)

---

### Principle 3: Early Testing Saves Time and Money

#### Plain statement

Testing activities should start as early as possible in the development life cycle, and be focused on defined objectives. Defects found early are cheaper to fix than defects found late. Moving testing earlier in the timeline is often called **shift-left** (because if you draw the SDLC as a line from left, requirements, to right, release, you are shifting testing activities towards the left).

#### Why it is true

A defect is cheapest to fix at the moment it is introduced and gets more expensive with every step it travels downstream. Here is the reasoning:

- A misunderstanding in a **requirement** costs almost nothing to fix if you spot it in a review: you change a sentence.
- If it survives into **design**, you must change diagrams and decisions.
- If it survives into **code**, you must change code and re-test it.
- If it survives into **testing**, you must find it, report it, triage it, fix it, rebuild, and re-test.
- If it survives into **production**, you must also deal with unhappy customers, emergency fixes, possible data corruption, support calls, and damage to reputation.

Each stage adds more people, more rework, and more things that were built on top of the faulty piece. Imagine finding a wrong measurement on a blueprint versus finding it after the walls are built. Moving a line on paper is trivial; moving a wall is not.

The size of the cost increase differs from project to project, and you will see exaggerated statistics quoted ("100 times more expensive!"). Treat any specific multiplier with caution. The direction of the trend is well accepted in the industry; the exact numbers depend on the project.

Early testing includes more than running software. It includes **static testing**, which means examining work products (requirements, designs, code) without executing the software, for example by reviewing a requirement document. You have already done this: Tuesday's requirements analysis was early testing.

#### A story

During a requirements review for an online store, a tester asks, "The requirement says discount codes are valid 'for one month.' Does that mean 30 days, one calendar month, or until the end of the month?" The product owner realizes that three people had three different assumptions. The sentence is rewritten in two minutes. If nobody had asked, three different developers might have coded three different behaviors, and the confusion would have surfaced months later as customer complaints about "expired" coupons.

#### What it means in practice

- **Review requirements and user stories.** Look for ambiguity, contradictions, missing details, and untestable statements ("the system should be fast" is not testable; "the login page loads in under 3 seconds" is).
- **Join planning and refinement meetings.** In Agile teams, testers attend backlog refinement and sprint planning (ceremonies you covered Monday) so they can ask questions before the code exists.
- **Prepare test cases while development happens.** You do not need to wait for the finished build to write tests.
- **Take part in design and code reviews** where appropriate.
- **Think about testability** early: can this feature be tested easily? Are there clear, observable results?

#### Applied to Project 1: login and registration

Before looking at the running application, read its requirements. Ask early questions such as:

- What are the password rules exactly (minimum length, required character types)?
- Is the email case-sensitive?
- What happens after five failed login attempts?
- Must the user verify their email before logging in?
- What message should appear if the email is already registered?

Every unanswered question is a potential defect that you caught for free.

#### Common misunderstanding

"Early testing means running tests on unfinished code." Not necessarily. Early testing often means thinking, questioning, and reviewing, before any code runs. Also, "early" does not mean "only early." You still test later too.

#### Quick check

*Name two early testing activities a tester can do before any code is written.*

(Answer examples: reviewing requirements or user stories for ambiguity, taking part in backlog refinement, drafting test cases from acceptance criteria, reviewing designs, thinking about testability.)

---

### Principle 4: Defects Cluster Together

#### Plain statement

A small number of modules or areas of the system usually contain most of the defects. Defects are not spread evenly; they are concentrated, or "clustered." This is also referred to as the principle of **defect clustering**.

#### Why it is true

Several natural forces cause clustering:

- **Complexity.** Complicated logic (payments, tax calculations, permissions) has more places to go wrong than a static "About us" page.
- **Change.** Code that is edited often accumulates mistakes. Each change is a chance to break something.
- **Dependencies.** Modules connected to many other modules are exposed to many sources of trouble.
- **People and pressure.** A module written in a hurry, by a newcomer, or by a team that has misunderstood the requirement tends to carry more defects.
- **Legacy code.** Old code that nobody fully understands is fragile.

The **Pareto principle** (also called the 80/20 rule) gives useful intuition. It is named after an economist who observed an uneven distribution in a different domain, and it states roughly that a large majority of effects (about 80 percent) come from a small minority of causes (about 20 percent). In testing, the intuition is "a small fraction of the modules will contain most of the defects." Treat 80/20 as a rule of thumb, not an exact law: in your project it might be 70/30 or 90/10.

#### An example: defects per module

Imagine an e-commerce application with 8 modules, and 100 defects logged during one release. The table below shows where they were found:

| Module | Defects found | Share of total | Cumulative share |
|---|---|---|---|
| Checkout | 41 | 41% | 41% |
| Registration | 22 | 22% | 63% |
| Payments | 18 | 18% | 81% |
| Search | 6 | 6% | 87% |
| Profile | 5 | 5% | 92% |
| Login | 4 | 4% | 96% |
| Help pages | 2 | 2% | 98% |
| Notifications | 2 | 2% | 100% |
| **Total** | **100** | **100%** | |

Look at the "Cumulative share" column. The top three modules (3 out of 8, which is 37.5 percent of the modules) hold 81 percent of the defects. A team that noticed this could put extra testing, extra code review, and extra developer attention on Checkout, Registration, and Payments. That is much smarter than giving all eight modules the same amount of effort.

#### A story

A team keeps a simple spreadsheet recording which module each bug belongs to. After three releases, they notice the "shopping cart" module appears at the top of the list every time. They schedule a design review of that module, discover that its logic had been patched repeatedly without a clear structure, and refactor it (reorganize the code without changing behavior). Defects from that module drop sharply in the next release. The data pointed to the problem before anyone's gut feeling did.

#### What it means in practice

- **Track defects by module or feature.** Use Jira fields such as component or label (from your Jira lessons) so you can count them.
- **Look at the data.** Periodically ask "where are our bugs coming from?"
- **Focus extra testing where clusters appear,** and look at neighboring areas, since related problems often hide nearby.
- **Use clusters for prediction.** A module that was buggy last release will likely be buggy next release.
- **Do not neglect the rest.** The other 20 percent of defects are scattered across the other 80 percent of the system. Low-defect areas still need baseline testing.

#### Applied to Project 1: login and registration

Registration is usually busier than login: it has more fields, more validation rules, email checks, duplicate-account checks, and often a confirmation step. Expect more defects there. When you find a validation defect on the email field (for example, it accepts an address with no "@"), it is wise to test other fields' validation (name, password, confirm password) more intensely, because the same developer and same approach may have caused similar problems.

#### Common misunderstanding

"Clustering means the module with the most bugs is badly written and its developer is at fault." Clusters are a signal about the system, its complexity, and its history, not a verdict about a person. Also, clusters can shift over time. Last release's hotspot may be quiet next time.

#### Quick check

*In a release, 3 of 10 modules contain 75 percent of the defects. Where should you place additional testing effort, and why?*

(Answer: On those 3 modules, because defects are concentrated there; but still keep baseline testing on the other 7, since defects can occur anywhere and clusters can move.)

---

### Principle 5: Beware of the Pesticide Paradox

#### Plain statement

If you run the same tests over and over, they eventually stop finding new defects. To keep finding defects, tests must be regularly reviewed and revised, and new tests written.

#### Why it is true (and why it has that name)

Farmers who spray the same pesticide on a field year after year find that, over time, the surviving insects are those that resist it. The pesticide stops working as well. Software tests behave like this pesticide: the defects that the tests could catch get found and fixed, and what is left is the set of defects those tests cannot see.

Software also changes. New features, new code paths, and new user behavior appear, but an old test suite (a collection of tests) only checks the old things. The suite keeps passing, which feels comforting, but the green result slowly means less and less.

Note that this does not mean old tests are useless. A repeated test is valuable for confirming that existing behavior still works (this is the purpose of regression testing, which we cover in depth on Friday). The paradox is about relying on the same tests as your only defense, and expecting them to keep finding new defects.

#### A story: the stale regression suite

A team has a regression suite of 200 automated tests for their account portal. It was written two years ago and runs every night. It has been green for months, and the dashboard looks wonderful. Meanwhile, the product has changed:

- A "Sign in with Google" button was added, and no test covers it.
- The password rules were tightened, but the tests still use a short password that is now rejected; the team "fixed" those failing tests by deleting the check instead of updating the data.
- The mobile layout was redesigned, but all tests run only at desktop screen size.
- Several tests assert only that "the page loads," which will pass even if the form is broken.

One day a release goes out in which Google sign-in fails for new users. All 200 tests are green. Customers find the defect within an hour. The suite did not fail; it simply no longer asked the right questions.

#### What it means in practice

- **Schedule test maintenance.** Review and update tests whenever requirements change and at regular intervals, just as you maintain code.
- **Add tests for new features and for every escaped defect.** When a defect reaches production, add a test that would have caught it.
- **Vary your inputs.** Use different data, different paths, and different environments from time to time.
- **Mix in exploratory testing.** In exploratory testing, you learn, design, and execute tests at the same time, using your curiosity instead of a script. It finds things that fixed scripts miss.
- **Watch for "always green" suites.** A suite that has never failed in a year might be extremely healthy, or it might be asleep. Investigate which.
- **Remove or fix weak tests.** Delete duplicate tests and tests that cannot fail.

#### Applied to Project 1: login and registration

Suppose you write a set of registration tests today. In two weeks the team adds a "Confirm password" field and a rule requiring one special character in the password. If you do not revise the tests, they might all keep passing while the new rules go completely unchecked. After every change to login or registration, ask: "Which of my tests are now outdated, and which new situations need new tests?"

#### Common misunderstanding

"Our regression suite always passes, so the quality is high." A passing suite tells you only that the specific things it checks still work. Whether those are the right things is a separate question, which only review answers.

#### Quick check

*An automated suite has passed every night for 18 months, although the product has had many new features. Give one reason you should not be completely reassured.*

(Answer: The suite may not cover the new features, may use outdated data, or may contain weak assertions; per the pesticide paradox, unchanged tests stop finding new defects, so the suite must be reviewed and updated.)

---

### Principle 6: Testing Is Context Dependent

#### Plain statement

Testing is done differently in different contexts. There is no single "right way" to test that fits every project. How you test depends on what the software does, who uses it, what could go wrong, the life cycle model, the regulations, and the risks.

#### Why it is true

Software ranges from a birthday-card website to the controller of an insulin pump. The consequences of failure differ enormously, and so do the expectations about rigor, documentation, and speed. A fixed recipe cannot suit all of them. Context includes:

- **Risk and consequence of failure** (annoyance, lost money, injury, loss of life).
- **Users** (children, doctors, the general public, internal staff).
- **Regulations and standards** (finance, healthcare, aviation, and others often have legal requirements).
- **Development model** (Agile with weekly releases versus a heavily planned model, which you saw Monday).
- **Technology** (web, mobile, embedded devices, APIs).
- **Time, budget, and team skills.**

#### A comparison of four contexts

| Aspect | Banking app | Video game | Medical device | Marketing website |
|---|---|---|---|---|
| Main risk if it fails | Financial loss, fraud, legal penalties | Player frustration, bad reviews, refunds | Patient harm or death | Lost leads, brand damage |
| Top quality focus | Security, accuracy of calculations, auditability | Performance, fun, graphics, balance, compatibility | Safety, reliability, correctness | Content accuracy, appearance, browser support, speed |
| Typical depth of documentation | High: detailed, traceable, audited | Moderate: often lighter, with lots of playtesting | Very high: formal and regulated | Light to moderate |
| Regulation | Heavy (financial rules, data protection) | Light, apart from age ratings and platform rules | Very heavy (medical regulations) | Light (privacy, accessibility) |
| Testing style | Rigorous, risk-based, security and transaction testing | Heavy playtesting, performance and device testing, exploratory | Formal verification and validation, extensive evidence | Visual checks, cross-browser, link and form tests |
| Acceptable release speed | Slower, careful | Fast patches common | Slow, controlled | Very fast |

A bug that makes a game character walk through a wall is a funny video on social media. The same kind of "small" miscalculation in a medical device's dosage or a bank's interest could be a disaster. Same type of mistake, completely different significance.

#### A story

Two testers meet at a conference. One works on flight-control software and one on a recipe-sharing website. The aviation tester describes formal reviews, evidence trails, and months of test preparation. The recipe tester describes shipping updates twice a day with quick exploratory checks. Each thinks the other is "doing it wrong," until they realize that each approach is right for their context. Applying aviation process to a recipe site would waste money; applying recipe-site process to aviation would be reckless.

#### What it means in practice

- **Ask about context before choosing an approach.** Who are the users? What is the worst thing that could happen? What are the rules?
- **Adapt your test strategy.** The depth, tools, and techniques should fit the risk.
- **Do not copy blindly.** A technique that worked at your last company may not suit this one.
- **Learn the domain.** Understanding banking, healthcare, or gaming helps you spot what matters.

#### Applied to Project 1: login and registration

Project 1 is a sample training app, so its risks are low in real-world terms. But imagine the same login feature in different contexts. In a hospital portal, it protects medical records, so security and access control testing become critical. In a bank, failed-login lockout and password strength get intense attention. In a casual hobby forum, a simpler check may be enough. As you write your test cases today, decide what level of rigor matches the sample app's purpose and say why.

#### Common misunderstanding

"Context dependent means anything goes, so there are no standards." Context dependence means the standards and depth are chosen deliberately based on risk, not that you may skip the thinking. The principles themselves still apply everywhere.

#### Quick check

*Why would you test a medical-device display differently from a marketing website?*

(Answer: Failure consequences, regulation, users, and risk differ greatly; a failure of the medical device could harm patients, so testing must be more rigorous and documented.)

---

### Principle 7: Absence-of-Errors Fallacy

#### Plain statement

It is a **fallacy** (a mistaken belief) to think that finding and fixing a large number of defects will ensure the success of a system. A system can be nearly or completely free of defects and still be useless if it does not meet the users' needs and expectations.

#### Why it is true

"Works as specified" and "is what people need" are two different things. A product can follow its specification perfectly, but if the specification described the wrong product, or the product is too confusing, slow, or irrelevant, then users will not adopt it.

This links straight to **verification versus validation**, which you learned earlier today:

- **Verification** asks, "Are we building the product right?" (Does it match the specification?)
- **Validation** asks, "Are we building the right product?" (Does it meet the users' real needs?)

A product can pass verification with flying colors and fail validation. The absence-of-errors fallacy is the warning that defect-hunting alone is not enough: we also need to validate that the product is the right one.

#### A story

A company builds a travel-booking app and tests it exhaustively. After months, the defect count is near zero. The app launches, and nobody uses it. User research later shows that travelers wanted to compare prices across airlines at a glance, but the app forced them through a ten-step booking wizard first. Every button worked perfectly. The product simply solved the wrong problem for the people it was meant to serve.

#### What it means in practice

- **Involve users and stakeholders early and often.** Demos, feedback sessions, and user acceptance testing (UAT) check whether the product fits real needs.
- **Test usability and fitness for purpose,** not just correctness.
- **Challenge requirements** (see Principle 3). If a requirement seems to solve a problem nobody has, say so.
- **Report beyond defects.** Useful feedback includes "this flow is confusing" and "this takes too many steps," even when nothing is technically broken.
- **Remember the product's goals.** Quality is not "zero defects." Quality is the degree to which the product satisfies stated and implied needs.

#### Applied to Project 1: login and registration

Imagine registration works flawlessly: all validations are correct and all your tests pass. But it asks for twelve fields including a phone number, a postal address, and a date of birth, and users abandon the form halfway. Or the error messages say "Error 4017" with no explanation. The feature is defect-free and yet it fails its purpose. As a tester, you should also ask: "Would a real new user find this easy and sensible?"

#### Common misunderstanding

"Our goal is zero defects, so if we hit it we have succeeded." Zero defects is not the goal; a product that is useful, valuable, and trusted is. Low defects are necessary but not sufficient.

#### Quick check

*The software matches its specification exactly, but customers say it does not help them do their job. Which principle is this, and which concept does it relate to?*

(Answer: The absence-of-errors fallacy; it relates to validation, building the right product.)

---

## Other Commonly Cited Principles (Additional Heuristics)

The seven principles above are the official list in the ISTQB Foundation Level syllabus. You will also hear other statements quoted in books, articles, and teams. They are **not part of the official ISTQB seven.** We call them **additional heuristics**: useful rules of thumb that many practitioners find sensible. Do not write them in an exam as official principles; do use them as practical guidance.

| Heuristic (not official ISTQB) | What it means | Link to the official principles |
|---|---|---|
| Testing must be traceable to requirements | Each test should connect back to a requirement or user story, so you can show what has been covered and what has not. This connection is called **traceability**. | Supports honest reporting under Principle 1 and checks for fit under Principle 7. |
| Test the riskiest parts first | Start with the areas where failure is most likely or most damaging. | Follows from Principles 2, 4, and 6. |
| Independent testing is valuable | People who did not write the code often find different defects, because they do not share the author's assumptions. **Independence** can range from a developer testing a colleague's work to a separate test team. | Related to the testing mindset from earlier today. |
| Test planning is never finished | Plans change as you learn more, so revise them. | Related to Principles 5 and 6. |
| Good testing is both a technical and a creative activity | It needs systematic technique and curious exploration. | Related to Principles 2 and 5. |

When you see "principles of testing" lists online with different numbers (some say 7, some 10, some 12), they are usually mixing the official seven with items like these. That is not a mistake; just be aware of which list is which.

---

## Summary Table: The Seven Principles at a Glance

| # | Principle | One-line meaning | Key action for testers | Project 1 example |
|---|---|---|---|---|
| 1 | Testing shows the presence of defects, not their absence | Passing tests never prove zero bugs | Report coverage and residual risk honestly | 15 passing registration tests do not mean registration is bug-free |
| 2 | Exhaustive testing is impossible | You cannot test every combination | Choose tests using risk and techniques | Pick representative emails instead of trying every possible email |
| 3 | Early testing saves time and money | The earlier a defect is found, the cheaper the fix | Review requirements, shift left | Ask about password rules before coding or testing |
| 4 | Defects cluster together | A few modules hold most defects | Track defects by module and focus there | Registration likely has more defects than login |
| 5 | Beware of the pesticide paradox | Repeated identical tests stop finding new bugs | Review and update tests regularly | Update tests when "confirm password" is added |
| 6 | Testing is context dependent | Different software needs different testing | Adapt strategy to risk, users, rules | Bank-style login needs far more rigor than a hobby forum |
| 7 | Absence-of-errors fallacy | Bug-free is not the same as useful | Validate against real user needs | A flawless 12-field form that users abandon |

---

## How the Principles Guide Real Decisions

The principles are not trivia. They shape three daily decisions: what to test first, how to organize effort, and when to stop.

### Prioritization

Because exhaustive testing is impossible (Principle 2), you must prioritize. **Prioritization** means ordering your testing so the most important things are tested first, and so that if time runs out, what remains untested is what matters least.

Practical questions to ask for each feature or test:

1. **How bad is it if this fails?** (Impact: money, safety, reputation, legal.)
2. **How likely is it to fail?** (Likelihood: new code, complex logic, past defect clusters, inexperienced authors.)
3. **How often is it used?** (A feature everyone uses every day deserves more attention than one used rarely.)

### A first look at risk-based testing

**Risk** is the chance that something undesirable happens, combined with how bad it would be. A rough way to think about it:

> Risk = Likelihood of failure x Impact of failure

**Risk-based testing** means using risk to decide what to test, how deeply, and in what order. High-risk items get more tests, earlier. Low-risk items get fewer. This approach combines several principles at once: Principle 2 (we must choose), Principle 4 (clusters raise likelihood), and Principle 6 (context defines impact). We will build on risk-based thinking in later weeks; for now, a simple table is enough.

For login and registration:

| Item | Likelihood of failure | Impact if it fails | Priority |
|---|---|---|---|
| Login with valid credentials | Low | Very high (nobody can use the app) | High |
| Registration with a duplicate email | Medium | High (duplicate or hijacked accounts) | High |
| Password strength validation | Medium | High (security) | High |
| Error message wording | Medium | Low | Low |
| Page footer links | Low | Low | Low |

### Stopping criteria: when do you stop testing?

If you can never prove there are no defects (Principle 1) and cannot test everything (Principle 2), how do you know when to stop? Testing stops when it is *sensible* to stop, which is defined by **exit criteria**: the agreed conditions that must be met to consider a test phase complete. On Tuesday, in test planning, you learned that exit criteria are written into the test plan. The principles explain why they are needed: without them, testing would never end.

Common exit criteria include:

- A target percentage of planned tests have been executed (for example, 100 percent of high-priority tests and 90 percent of the rest).
- A required level of coverage of requirements has been reached.
- No open critical or high-severity defects remain (or those remaining are accepted by stakeholders).
- The defect discovery rate has dropped: the number of new defects found per day has fallen to a low level.
- The agreed time or budget is used up, with the remaining risk understood and signed off by stakeholders.

Notice that "we found no more bugs" is not on the list as a proof of quality. By Principle 1, it only means no more were found. Stopping is a risk decision made together with stakeholders, based on evidence, rather than a claim of perfection. Also notice the pesticide paradox: a falling discovery rate may mean the product is stabilizing, or it may mean your tests have gone stale, so check that your tests are still fresh before trusting a low discovery rate.

---

## Examples

Here are three short worked examples in which several principles appear together.

**Example A: The launch decision.** A team has run all planned tests. Ninety-eight percent pass, and the remaining failures are cosmetic. A manager says, "Great, then it is bug-free." You respond with Principle 1: the tests show the absence of *known* failures only. You then suggest reviewing the coverage report and the exit criteria. Together you decide to release, with a monitoring plan for the first week.

**Example B: Where to look.** Your defect log shows that most new bugs this sprint come from the "reset password" feature. Principle 4 says to expect more there, and Principle 5 reminds you that your existing tests for it are probably not finding the new kinds of problems. You write fresh tests and try exploratory sessions. Principle 3 suggests asking the developer to walk you through the next change before they code it.

**Example C: The perfect product nobody wanted.** A feature passes every test, yet usage analytics show people avoid it. Principle 7 tells you to look beyond defects. You interview users, discover that the feature's name confuses them, and suggest a clearer label and flow.

---

## Scenario-Matching Exercise

Read each scenario and decide which of the seven principles it best illustrates. Some principles will be used more than once. Write down your answers, then check the answer key.

**The principles (for reference):**

1. Testing shows the presence of defects, not their absence
2. Exhaustive testing is impossible
3. Early testing saves time and money
4. Defects cluster together
5. Beware of the pesticide paradox
6. Testing is context dependent
7. Absence-of-errors fallacy

**Scenarios:**

**S1.** A tester runs 500 tests, all pass, and writes in the report: "No defects were found by the executed tests; areas not covered are listed in Appendix B."

**S2.** A team wants to verify a search box that accepts 50 characters from a 70-character alphabet and decides instead to test a handful of representative inputs.

**S3.** A tester reads a user story and asks, "What is the maximum length of the username?" before any code is written, and the product owner realizes the story was unclear.

**S4.** After three releases, a spreadsheet shows that the "invoicing" module accounts for most of the logged bugs, so the team assigns extra reviewers to it.

**S5.** An automated suite that has run unchanged for two years starts missing bugs in the newly added features.

**S6.** A game studio tests mostly through large playtesting sessions and device-compatibility checks, while a hospital software vendor produces formal, traceable evidence for every test.

**S7.** An app has almost no defects, but customers stop using it because its main workflow does not match how they actually work.

**S8.** A product owner insists, "Our testers found nothing last night, so we can promise customers it is flawless."

**S9.** A tester calculates that a form with 6 drop-downs of 8 options each has over 260,000 combinations and proposes a prioritized subset.

**S10.** A defect found during a requirements review costs a one-sentence edit, while the same defect found after release requires an emergency patch and customer apologies.

**S11.** A test lead schedules a quarterly review to retire duplicate tests, update outdated data, and add tests for features released since the last review.

**S12.** Two projects, a financial trading system and a personal blog, use very different amounts of test documentation and security testing, and both teams are right to.

**S13.** The same three screens in a mobile app keep producing most of the crashes, release after release, so the team adds more tests and code review to those screens.

**S14.** After a user-feedback session reveals that people find the new registration flow baffling, the team realizes that passing all tests was never enough.

### Answer Key

| Scenario | Principle | Reasoning |
|---|---|---|
| S1 | 1 | The wording shows awareness that passing tests do not prove absence of defects. |
| S2 | 2 | 70^50 combinations are too many; representative selection is needed. |
| S3 | 3 | Questioning a user story before coding is early (shift-left) testing. |
| S4 | 4 | A small number of modules hold most defects. |
| S5 | 5 | Unchanged tests stop finding new defects as the product evolves. |
| S6 | 6 | Different contexts require different testing approaches. |
| S7 | 7 | Defect-free but not meeting user needs. |
| S8 | 1 | Absence of findings is not proof of absence of defects. |
| S9 | 2 | 8^6 = 262,144 combinations, too many to test exhaustively; prioritize. |
| S10 | 3 | Cost of fixing grows the later a defect is found. |
| S11 | 5 | Regular review and update of tests counters the pesticide paradox. |
| S12 | 6 | Risk, regulation, and impact differ by context. |
| S13 | 4 | Persistent hot spots: defects cluster. |
| S14 | 7 | Passing tests (verification) does not guarantee that the product is right for users (validation). |

Score yourself: 13-14 correct means you have a firm grasp. 10-12 means review the principles you missed. Below 10, reread the relevant sections and try again tomorrow.

---

## Try It: Apply the Principles to Login and Registration

This activity prepares you for the positive and negative test case exercise that comes later today. You do not need to write full test cases yet. Positive and negative testing is the topic of the next lesson, so here you are thinking at the level of principles.

**Part A: Principle application worksheet.** In a notes document, create a table with seven rows (one per principle) and three columns: "What this principle says about login/registration," "One specific question or action it suggests," and "Risk if I ignore it." Fill it in for Project 1.

**Part B: The combination count.**
1. Open Project 1's registration page (or its requirements) and list every field and every drop-down or checkbox.
2. For each choice-based field, count the realistic options.
3. Multiply to get the number of combinations.
4. Use the Python snippet from Principle 2, modified for your own lists, to confirm your number. Save your script as a scratch file (not in the project).
5. Write two sentences on how you would reduce the number to a manageable set.

**Part C: A tiny risk table.** Choose five behaviors of login and registration. For each, rate likelihood and impact (low, medium, high) and assign priority. Decide which two you would test first and why.

**Part D: Questions for the requirements.** Write five questions you would ask the product owner about login and registration before testing. Link each to Principle 3.

**Stretch:** Explain, in three sentences, how you would decide when to stop testing registration, naming at least two exit criteria.

---

## Case-Study Analysis Task

Read the following case and answer the questions in writing. Aim for a short paragraph per question.

> **BrightCart Online** is a small online grocery store. Three months before launch, the team skipped requirements reviews to "save time." The testers started when the build was ready and wrote 300 test cases, which they ran unchanged every week for the next ten weeks. Pass rates rose steadily to 99 percent. The project manager announced, "Zero defects, we are ready for a perfect launch."
>
> After launch, the first week brought many complaints. The checkout page had repeated failures, with the "delivery slot" selector responsible for most support tickets. Customers using a new phone model could not complete orders, a case no test used. The registration form worked exactly as specified, but customers disliked having to create an account before they could even browse the products, and many abandoned it. The team later discovered that the requirement for "delivery slots" had been understood three different ways by three developers, and the fix required reworking the screens, the database, and the confirmation emails.

**Questions:**

1. Which principles were violated or illustrated? Name at least five and point to the evidence in the story.
2. What could the team have done during requirements to prevent the delivery slot problem? Estimate how the cost of fixing it then would have compared with the cost after launch (describe the direction; you do not need exact numbers).
3. What does the cluster of checkout and delivery-slot tickets suggest about where to focus additional testing in the next release?
4. How should the project manager's statement "Zero defects" have been phrased?
5. Suggest three changes to the test approach for the next release, each linked to a principle.
6. What additional information (not defects) would help the team learn whether the registration flow meets user needs?

**Suggested points for your answers (use to check your work afterwards):** Principle 3 (skipped reviews and the late-discovered misunderstanding); Principle 5 (the 300 unchanged tests); Principle 1 (the "zero defects" claim); Principle 4 (checkout clustering); Principle 2 (no test for the new phone model, because not everything can be covered, though device analytics could guide choices); Principle 7 (registration worked to specification but frustrated users); Principle 6 (a grocery store with a consumer audience has different priorities from a bank, so mobile and usability matter greatly). A better statement would be: "Testing found and fixed the defects our tests could reveal, and the remaining risks are understood and accepted."

---

## Common Misconceptions

| Misconception | Reality |
|---|---|
| "If testing finds no bugs, there are none." | Testing can only show that defects exist (Principle 1). |
| "With enough automation we can test everything." | Automation speeds up testing but does not change the arithmetic of combinations (Principle 2). |
| "Testers should wait until the build is ready." | Testing can and should begin with requirements (Principle 3). |
| "Every module deserves identical testing effort." | Effort should reflect risk and defect history (Principle 4). |
| "A green regression suite means we are safe." | Unreviewed suites go stale (Principle 5). |
| "There is one best way to test." | Good testing is chosen to fit the context (Principle 6). |
| "Our goal is zero defects." | A product must also be useful and fit users' needs (Principle 7). |
| "The 80/20 rule is exact." | It is an intuition; real splits vary. |
| "The principles are optional advice." | They are well-established guidance, though applying them still needs judgment. |
| "The ISTQB list contains ten or twelve principles." | The ISTQB Foundation Level lists seven; longer lists mix in additional heuristics. |
| "Early testing means no testing later." | It means starting early, not stopping early. |
| "Stopping testing means we are finished finding bugs." | Stopping means the remaining risk is acceptable under agreed exit criteria. |

---

## Knowledge Check

Answer these questions, then compare with the answers below.

1. State Principle 1 in your own words and give one sentence explaining why it holds.
2. A form has 4 drop-downs with 5, 3, 2, and 6 options. How many combinations of choices exist?
3. Why is "test everything" not a realistic strategy even when you have automation?
4. What does "shift-left" mean?
5. A requirement says "The page must load quickly." Why is this a problem for early testing, and how could you improve it?
6. What is the Pareto principle, and how does it relate to defect clustering?
7. Give two reasons defects tend to cluster in particular modules.
8. Explain the pesticide paradox using the pesticide analogy.
9. Name two actions that reduce the effect of the pesticide paradox.
10. Give one reason why a banking app and a mobile game require different testing.
11. Which principle warns that a defect-free product can still fail? Which concept from earlier today does it relate to?
12. Name two additional heuristics (not official ISTQB principles) from this lesson.
13. List three common exit criteria.
14. A manager asks you to confirm "100 percent bug-free." What do you say?
15. In Project 1, which is more likely to harbor more defects, login or registration, and why? Which principle does this reflect?

### Answers

1. Testing can reveal that defects exist but cannot prove none remain, because passing tests only cover the situations that were tried, and an untried situation may hide a defect.
2. 5 x 3 x 2 x 6 = 180 combinations.
3. The number of combinations grows by multiplication so quickly that even very fast automation cannot cover them (Principle 2). Automation lets you run more tests, but you still need to choose which ones.
4. Moving testing activities earlier in the life cycle (toward the "left" of a timeline that starts with requirements), for example reviewing requirements before code is written.
5. "Quickly" is vague and cannot be verified. Rewrite it with a measurable target, such as "The page loads in under 3 seconds on a standard broadband connection for 95 percent of requests."
6. The Pareto principle (80/20 rule) says most effects come from a minority of causes. Applied to defects, a minority of modules usually holds a majority of the defects.
7. Any two of: high complexity, frequent change, many dependencies, time pressure or inexperience of the authors, old and poorly understood code.
8. Insects that survive a pesticide become resistant, so repeated spraying stops working. Likewise, repeated identical tests stop finding new defects because the defects they could find were already fixed, and the remaining ones are outside their reach.
9. Any two of: review and update tests regularly, add tests for new features and escaped defects, vary test data, use exploratory testing, remove weak tests.
10. Risk, regulation, and impact of failure differ. A banking app handles money and must meet strict security and audit demands; a game emphasizes performance, playability, and device compatibility, and a bug is typically less harmful.
11. The absence-of-errors fallacy; it relates to validation (building the right product).
12. Any two of: traceability of tests to requirements, test the riskiest parts first, independent testing is valuable, test planning is never finished, testing is both technical and creative.
13. Any three of: planned tests executed to a target percentage, required coverage reached, no open critical defects, defect discovery rate has fallen, time or budget used up with remaining risk accepted.
14. "I cannot confirm that. Testing can show the presence of defects but not their absence. Here is what we tested, what we found, what we did not cover, and the remaining risks."
15. Registration, because it has more fields, validations, and checks (greater complexity). This reflects defect clustering (Principle 4), and the plan should remain open to evidence from actual defect data.

---

## Key Takeaways

- The seven ISTQB principles are consolidated professional experience, formalized in the ISTQB Foundation Level syllabus. They guide decisions in every kind of project.
- **Principle 1:** Tests reveal defects but cannot prove there are none. Report coverage and remaining risk honestly.
- **Principle 2:** Combinations multiply into astronomical numbers (the 7-factor form alone has 10,800), so we must choose tests wisely. Test design techniques, introduced tomorrow, are the practical answer.
- **Principle 3:** Start early. Reviewing requirements is testing, and the cost of fixing a defect generally rises the later it is found.
- **Principle 4:** Defects cluster. Track them by module and focus extra effort where they concentrate, but keep baseline testing everywhere.
- **Principle 5:** Tests wear out. Review, update, and diversify them, or they will stop finding new problems.
- **Principle 6:** Context decides approach. Always ask who the users are, what could go wrong, and what rules apply.
- **Principle 7:** A defect-free product can still fail if it is not what users need. Validation matters as much as verification.
- Principles drive prioritization, risk-based thinking, and stopping decisions based on exit criteria agreed in the test plan.
- Additional heuristics (traceability, riskiest first, independence) are useful but are not part of the official seven.
- Apply the principles to Project 1 today: ask early questions, count combinations, pick representative inputs, and expect registration to be the busier area.

---

## Additional Resources

- **ISTQB (International Software Testing Qualifications Board) - Foundation Level certification and syllabus:** https://www.istqb.org/ (navigate to the Certified Tester Foundation Level page to download the official syllabus, which contains the authoritative wording of the seven principles).
- **Guru99 - Seven Principles of Software Testing:** https://www.guru99.com/software-testing-seven-principles.html (a beginner-friendly summary with examples).
- **Atlassian - Software Testing (Continuous Delivery guides):** https://www.atlassian.com/continuous-delivery/software-testing (articles on testing in modern delivery pipelines, helpful for understanding early testing and automation in practice).

Next up: positive and negative testing, followed tomorrow by test design techniques, the practical tools for choosing good tests when you cannot test everything.
