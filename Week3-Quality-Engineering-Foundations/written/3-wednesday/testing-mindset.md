# Testing Mindset

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what a "mindset" is and why it matters as much as technique in testing.
2. Compare the developer mindset (build and construct) with the tester mindset (question, explore and challenge) as complementary, not competing, perspectives.
3. Describe eleven core traits of an effective tester and give a concrete example of each.
4. Look at a feature through the eyes of different users: a typical user, an attacker, a stressed user, a first-time user, a hurried user and a user relying on accessibility tools.
5. Use "what if" questioning, clarifying questions and assumption-challenging to uncover problems before and after code is written.
6. Recognise common cognitive biases in testing (confirmation bias, anchoring, familiarity and blind spots, optimism bias and "works on my machine") and apply specific counter-measures.
7. Describe levels of independence in testing and the trade-offs of each.
8. Report problems constructively: factual, evidence-based, and focused on the product rather than the person.
9. Explain how testers collaborate with developers and product owners, and why quality is a whole-team responsibility.
10. Introduce risk-based thinking to balance thoroughness against available time.
11. Describe the ethical and professional expectations of a tester, including honesty, confidentiality and integrity.
12. Explain how the testing mindset applies in Agile teams and when using AI tools, including the danger of automation bias.
13. Apply the mindset to the Project 1 login page by producing a list of 15 "what if" questions.

---

## Why This Matters

### In the industry

Imagine two testers given the same login page and the same two hours. The first follows the requirements line by line: valid username and valid password, check. Invalid password, check. Empty fields, check. They report that everything passed.

The second tester also checks those things, but then starts asking different questions. What if I paste a password with a trailing space? What if I press the Back button after logging out? What if I click "Login" five times very quickly? What if I am on a slow mobile connection? What if my screen reader cannot tell me why the login failed?

Both testers may know exactly the same tools and techniques. What separates them is a way of thinking. Employers consistently say this is what they look for. Tools change every few years, frameworks come and go, and AI assistants are rewriting how test cases are produced. The curious, careful, constructive way of thinking about software remains valuable through all of it.

This is why we say that **mindset matters as much as technique**. A technique is a method you can look up, such as how to write a test case. A mindset is the attitude that decides whether you reach for that technique at the right moment, and whether you notice the thing nobody asked you to check.

### In your Weekly Epic

This week you are building the quality-engineering mindset. On Monday you saw where testing fits in the SDLC and STLC, and how Agile teams work. On Tuesday you analysed requirements, planned and executed tests, and followed defects through their lifecycle in Jira. Today you learn the thinking underneath all of that. Later today, you will meet formal terminology (QA and QC, verification and validation, error, defect and failure) and the seven testing principles, and tomorrow you will learn test-design techniques. Those lessons give you the vocabulary and the methods. This lesson gives you the attitude that makes them work.

Throughout the week you are applying everything to **Project 1 - QE Foundations**, a sample web app you are planning quality for. Today's exercise has you write positive and negative test cases for its login and registration feature. A good negative test case begins with a good "what if" question, and this lesson teaches you how to ask them.

---

## The Concept

### 1. What is a mindset?

A **mindset** is a set of habits, beliefs and attitudes that shapes how you notice things, what you decide to do about them, and how you react when things go wrong. It is the lens through which you view a situation.

An analogy: two people walk into the same kitchen. A chef notices the sharpness of the knives, the freshness of the ingredients and the layout of the workstations. A health inspector walks into the same kitchen and notices the temperature of the fridge, the cleanliness of the cutting boards and the hand-washing sink. Same room, different lens, different findings. Neither is wrong. The kitchen needs both.

In testing, the lens is: "How could this fail, and who would be affected if it did?"

**Why mindset matters as much as technique:**

- Techniques tell you *how* to test. Mindset tells you *what to wonder about* and *when to dig deeper*.
- Most serious defects are not found in the cases someone wrote down in advance. They are found because a tester became curious about something unexpected.
- A tester with strong technique but a passive mindset only confirms what is already known. A tester with a strong mindset keeps learning about the product.
- Mindset is how you behave when there is no script: when a requirement is vague, the deadline is close, or the build looks fine and everyone wants to go home.

Good news for beginners: a mindset is not a talent you are born with. It is a set of habits, and habits can be practised. By the end of this lesson you will have exercises to do exactly that.

### 2. Developer mindset and tester mindset

Software is made by people with different focuses. Two of the most common are the developer's and the tester's.

| Aspect | Developer mindset | Tester mindset |
|---|---|---|
| Main question | "How do I make this work?" | "How could this fail, and does it work for everyone who needs it?" |
| Natural direction | Build, construct, solve | Question, explore, challenge |
| Focus | Designing a solution that meets the requirement | Examining the solution against requirements, expectations and risks |
| Typical view of input | The expected, valid cases the code is designed for | Unexpected, invalid, extreme and unusual inputs as well as valid ones |
| Success feels like | A feature that works as designed | Information that makes the product better and the team more confident |
| Strength | Deep knowledge of how the code works | Wide knowledge of how the product behaves from the outside, and for different users |

**This is not a rivalry.** It is easy to imagine developers as people who "make things" and testers as people who "break things". That picture is misleading and harmful. A tester does not break the product. The product already contains the weaknesses; the tester reveals them while it is still cheap to fix them. The tester's goal is not to make developers look bad. The goal is to help the whole team ship something good.

A useful analogy is a bridge. The structural engineer designs a bridge to carry load. An independent inspector examines the same bridge asking where it might crack, what happens in a storm, what happens if traffic is heavier than expected. Nobody thinks the inspector is the engineer's enemy. A bridge that passes both perspectives is one you would trust to drive over.

**Developers can and should think like testers**, too. Good developers write unit tests, review each other's code, and ask "what if" while building. Testers also need to think like builders: to understand how the system is put together, and what is feasible to fix. The best teams blur the line. The mindsets are complementary; each person simply leans toward one more than the other as their main role.

### 3. Core traits of an effective tester

Below are eleven traits. For each, you will see what it means and a concrete example. Notice how many of them are about people and communication, not only technology.

#### 3.1 Curiosity

**What it is:** A genuine desire to understand how something works and what happens when you try something different.

**Example:** While testing a search box, a curious tester wonders what happens if they search for a word with an accent, such as "café". They discover the search treats "cafe" and "café" as different words, so customers searching without accents miss half the products.

#### 3.2 Critical thinking

**What it is:** Evaluating information carefully and logically, asking whether claims are supported by evidence, rather than accepting them at face value.

**Example:** A requirement says "The system must respond quickly." A critical thinker asks: "What does quickly mean? Under one second? On what device? With how many users?" They help turn a vague phrase into something that can be checked.

#### 3.3 Skepticism

**What it is:** A healthy habit of not simply believing that something works because someone said so. Skepticism is not cynicism or distrust of people; it is a habit of asking for evidence.

**Example:** A developer says, "I fixed the password reset bug." A skeptical tester does not just trust the message. They re-run the exact steps from the original report, then also try a few nearby cases, because fixes sometimes work in one situation and quietly break another.

#### 3.4 Attention to detail

**What it is:** Noticing small things: a misspelled label, a number off by one, a button slightly misaligned, an error message that mentions the wrong field.

**Example:** On a registration page, the tester notices the heading says "Create Acount". It is a small error, but on the first page a new customer sees, it makes the brand look careless. They also notice the confirmation email says "Welcome, null", which points to a real data bug.

#### 3.5 Systems thinking

**What it is:** Seeing the product not as isolated screens but as a connected system: front end, back end, database, third-party services, networks, devices and people. A change in one place may ripple to others.

**Example:** A team changes the maximum username length from 20 to 30 characters on the registration form. A systems thinker asks: does the database column allow 30? Does the profile page layout break with a longer name? Does the welcome email template handle it? Does the mobile app truncate it?

#### 3.6 Empathy for the user

**What it is:** Understanding how real people experience the product, including their goals, frustrations, abilities and circumstances.

**Example:** A login error says "Authentication failure: code 0x4F". Technically correct, but a real user cannot understand it. An empathetic tester reports that the message should say what happened and what to do next, such as "That email or password does not look right. Try again or reset your password."

#### 3.7 Communication

**What it is:** Explaining findings clearly, listening to others, asking good questions, and adapting your message to the audience (a developer, a product owner or a manager).

**Example:** Instead of saying "Checkout is broken", a good communicator writes, "On the Payment page, clicking Pay with a saved card shows a blank screen. Steps, screenshot and browser console log attached. It happens on Chrome and Firefox but not Safari." We return to this skill in depth later.

#### 3.8 Tenacity

**What it is:** Persistence. Not giving up when a problem is hard to reproduce or when you are told "it works for me."

**Example:** A tester sees a crash once in twenty attempts. Rather than dismissing it, they note the time, the device, what they did just before, and keep trying until they find that it only happens when the session timeout expires while a form is open. That detail lets the developer fix it in an hour.

#### 3.9 Humility

**What it is:** Accepting that you can be wrong, that you cannot test everything, and that you can learn from anyone on the team.

**Example:** A tester logs a defect saying the discount code field is broken. A developer explains that codes are case-sensitive by design, and the requirement says so. A humble tester says thanks, closes the report, and suggests that the error message be clearer, since other users will make the same mistake.

#### 3.10 Risk awareness

**What it is:** Understanding that some failures matter far more than others, and focusing effort where the cost of failure is highest.

**Example:** A typo on the "About us" page and a wrong total on the payment page are both defects. A risk-aware tester knows which to test first when time is short. (More on this in section 11.)

#### 3.11 Continuous learning

**What it is:** Treating learning as a permanent part of the job: new domains, new tools, new kinds of failure.

**Example:** A tester joins a project involving online payments. They spend a few evenings reading how card payments work in general, so they can ask smarter questions about refunds, declined cards and timeouts.

**Reflection:** Which three traits come most naturally to you today? Which two would you like to strengthen? Write them down; you will revisit this in the Try it activity.

### 4. Thinking like different users

A feature is not used by "the user". It is used by many different people in many different situations. Strong testers deliberately switch perspectives. The following are six perspectives, using a login form as the running example.

| Perspective | Who they are | What they do or need | Login-form example questions |
|---|---|---|---|
| Typical user | Someone doing the main task as designed | Wants to complete the task simply | Can I log in with correct details? Is it easy? |
| Attacker | Someone trying to misuse the system | Tries to get in without permission, steal data or cause damage | What if I try thousands of passwords? What if I paste script text into the username? Does the error message reveal whether an email exists? |
| Stressed user | Someone under pressure or emotional strain | Makes mistakes, clicks repeatedly, loses patience | What if I mistype three times and panic? Is the error message calm and helpful? What if I double-click Login? |
| First-time user | Someone who has never seen the product | Does not know the terms, conventions or hidden steps | Is it obvious where to register? Does "Sign in" vs "Log in" confuse me? Do I know what the password rules are before I type? |
| Hurried user | Someone short on time, often on a phone | Skips instructions, uses shortcuts, works on small screens | Can I log in with one hand on a phone? Does autofill work? Does the page load fast enough on weak signal? |
| Accessibility user | Someone using a screen reader, keyboard only, magnification, or with colour blindness, hearing or motor differences | Needs the product to work with assistive technology | Can I reach every field with the Tab key? Does the screen reader announce the error? Is the error shown only in red colour? Is the contrast readable? |

**A note on the attacker perspective.** Thinking like an attacker does not mean behaving like one. You think about misuse in order to protect people, and you only do so on systems you are explicitly authorised to test. We return to this under ethics.

**A note on the accessibility perspective.** **Accessibility** means designing products so that people with a wide range of abilities and circumstances can use them. This includes people with permanent disabilities, temporary ones (a broken arm) and situational ones (bright sunlight on a screen). Accessibility is both an ethical matter and, in many countries, a legal requirement. Testers who think about it early save the team expensive rework.

**Practice tip:** Before testing any feature, pick two of these perspectives and write one sentence describing what that person would be trying to do. You will immediately see questions you would otherwise miss.

### 5. The art of questioning

Much of testing is asking good questions, of the product, of the requirements and of people. Three habits make this practical.

#### 5.1 "What if" questioning

"What if" is the simplest and most powerful testing tool. You take something that is assumed to be normal and change one thing.

Pattern: **What if [something unusual happens] at [this point]?**

Some useful categories of "what if":

- **What if the input is unusual?** Empty, very long, very short, special characters, emoji, spaces, different languages, negative numbers, zero.
- **What if the order is unusual?** Steps done in a different sequence, Back button, refresh in the middle, double-click.
- **What if the environment is unusual?** Slow network, no network, small screen, old browser, different time zone, low battery.
- **What if the user is unusual?** New, expert, impatient, distracted, assistive technology, a different language.
- **What if something external fails?** The email service is down, the database is slow, the payment provider times out.
- **What if the amount is unusual?** One record, no records, a million records.
- **What if time changes?** Session expires, the clock changes, a leap year, midnight.

#### 5.2 Asking questions

Testers are allowed, and expected, to ask questions. Some are best asked early, in refinement or planning meetings, where a cheap question can prevent an expensive defect (you saw on Tuesday how requirements analysis works).

Good questions have these qualities:

- They are **specific** ("What should happen when the password is 65 characters long?") rather than vague ("What about passwords?").
- They are **open** when exploring ("How is this feature expected to behave if the user has no internet?") and **closed** when confirming ("Is the maximum length 64 characters?").
- They are **respectful**. A question is not an accusation. "I want to make sure I understand the intent" is a friendlier start than "You forgot to say...".

Examples of useful clarifying questions for a registration feature:

- Are usernames case-sensitive?
- Is the email address verified before the account becomes active?
- What happens if someone registers with an email that already exists?
- What are the password rules, and where are they shown to the user?
- Who can see the error messages, and what level of detail is safe?

#### 5.3 Challenging assumptions

An **assumption** is something we take to be true without having checked. Assumptions are the hiding place for most defects. They exist in requirements ("Users will always have an email address"), in designs ("The server will always respond"), in code ("This list will never be empty") and in our own heads ("Nobody would do that").

To challenge an assumption:

1. **Notice** it. Phrases like "obviously", "of course", "always", "never", "everyone", "nobody" and "just" often signal one.
2. **Name** it, write it down in plain words.
3. **Ask** "What if this is not true?" and "How would we know?"
4. **Decide** what to do: check it, test it, or ask someone.

A tiny code example shows how an assumption can hide. A developer writes this simple input handler for a registration form:

```python
def register(username, age):
    # Assumes: username is never empty, age is always a whole number
    if len(username) < 3:
        return "Username too short"
    if age < 18:
        return "You must be 18 or older"
    create_account(username, age)
    return "Account created"
```

The code looks reasonable. A tester reading it, or exploring the form, will question the assumptions:

- What if `username` is `None` (nothing was sent)? `len(None)` would crash the program.
- What if the username is three spaces? `len("   ")` is 3, so it passes, but is that a valid username?
- What if `age` arrives as the text "twenty" or as "18.5"? The comparison `age < 18` would crash or behave strangely.
- What if `age` is negative or 500? The code only rejects values below 18, so 500 is accepted.
- What if the same username already exists? Nothing here checks.
- What if the username contains characters that could cause trouble later, such as quotes or angle brackets?

You do not need to be a programmer to ask these. You only need to ask, "What is this code or screen assuming, and what if that is wrong?"

### 6. Cognitive biases in testing

A **cognitive bias** is a systematic pattern in how human brains take shortcuts, which can lead to errors in judgement. They are not signs of laziness or stupidity; everyone has them. Testers need to know them because testing is largely a thinking activity, and biased thinking produces missed defects.

| Bias | What it means | How it shows up in testing | How to counter it |
|---|---|---|---|
| Confirmation bias | Tending to look for evidence that supports what we already believe | Running only tests expected to pass; reading "the login works" and then only trying cases that prove it | Deliberately design tests intended to **disprove** the claim; write negative tests first; ask a colleague to suggest cases you would not choose |
| Anchoring | Relying too heavily on the first piece of information received | Being told "this area is very stable" and testing it lightly; accepting the first estimate or first explanation of a bug without exploring alternatives | Ask "What evidence supports that?"; generate at least two other explanations; treat early information as a hypothesis, not a fact |
| Familiarity and blind spots | After seeing a product many times, you stop noticing its flaws; you see what you expect to see | Missing a typo you have read twenty times; following the same route through the app every time | Take breaks; change the order of your tests; use a different device or persona; pair with someone seeing it fresh; use checklists |
| Optimism bias | Believing things will go better than they probably will | "This is a tiny change, it will not break anything"; skipping regression checks because the release is small | Ask "What is the worst realistic outcome?"; base decisions on risk and evidence rather than on hope |
| "Works on my machine" | Assuming that because something works in your environment it works everywhere | A developer or tester confirms a fix locally and signs it off, while the real users have a different browser, data or settings | Record the exact environment (device, browser, version, data); test in an environment as close as possible to production; try the steps on a second configuration |

More notes on the bias list:

- **Confirmation bias** is the most common. A famous idea in reasoning is that we feel more comfortable proving ourselves right than looking for the one case that proves us wrong. Testing is, essentially, the discipline of looking for that case.
- **Anchoring** can also affect bug triage. If the first person to look at a defect calls it "minor", later reviewers tend to accept that without looking again.
- **Blind spots** also affect developers reviewing their own code, which is one reason independent review matters (next section).
- **"Works on my machine"** is so common it has become a joke in the industry. It is not an insult; it is a reminder that there are always differences between environments. The cure is not argument but evidence: exact steps, exact environment, and where possible a recording or a log.

**A simple personal habit:** at the end of a test session, ask yourself, "What did I assume? What did I not look at because I felt sure?"

### 7. Independence of testing

**Independence** in testing means how far the person testing is separated from the person who built the thing. The more separation, the more likely the tester is to have a different perspective, free from the author's assumptions and blind spots.

Why does this matter? Because of the biases above. Authors tend to test their own work in the way they designed it to be used. They also may feel pride or pressure that makes it harder to see problems.

Levels of independence, from least to most:

| Level | Description | Benefits | Trade-offs |
|---|---|---|---|
| 1. The author tests their own work | A developer tries out the code they just wrote (for example unit tests) | Fast, cheap, immediate feedback; developer knows the code well | Strongest blind spots; tends to confirm rather than challenge |
| 2. Another developer on the team tests | A colleague reviews or tests the work (peer review, pairing) | Fresh eyes with technical depth; still quick | Same team culture and assumptions; may not take a user's view |
| 3. A tester within the team | A dedicated tester or QA engineer embedded in the Agile team | Specialist skills, early involvement, good collaboration | Might start thinking like the team, and gradually share its blind spots |
| 4. A separate testing group within the organisation | A test team or centre of excellence in the same company | More objective; different reporting line; broad experience | Slower feedback; more handoffs; less shared context |
| 5. External or third-party testers | People from outside the organisation, such as a specialist firm or crowd-testing | Highest objectivity; specialist skills (e.g., security, accessibility); real-world variety | Cost; time needed to learn the product; confidentiality concerns need managing |

Important points:

- **More independence is not always "better".** It brings objectivity, but loses speed and context. The right level depends on the risk. A small internal tool may be fine with levels 1 to 3. A medical device or payment system will probably want more.
- **Most teams mix levels.** Developers write unit tests (level 1), peers review code (level 2), embedded testers explore the features (level 3) and occasionally a specialist firm runs a security assessment (level 5).
- **Independence is about mind as well as organisation.** Even inside one team, a tester who keeps a questioning attitude provides independence of thought. And a developer who deliberately tries to break their own feature, with a checklist and a fresh pair of eyes, narrows the gap.

(You will see in the testing principles lesson later today why testing is context-dependent. The independence you choose is an example of that.)

### 8. Reporting problems constructively

You can find the most important defect in the world, but if you report it badly, it may be ignored, misunderstood or take more time than it should to fix. Reporting is part of the mindset, because it reflects how you treat colleagues.

Three guiding principles:

1. **Be factual.** Describe what you observed, not what you feel or guess. Avoid exaggerated words ("terrible", "useless") and avoid claims about cause unless you have proof.
2. **Blame the product, not the person.** The report is about the behaviour of the software. Avoid language that points to a person ("you forgot", "your code").
3. **Give evidence.** Steps to reproduce, expected versus actual result, environment, screenshots, recordings, logs. Evidence turns an opinion into information.

Remember the defect report structure you used in Jira on Tuesday: summary, steps to reproduce, expected result, actual result, environment and attachments. Good mindset makes these fields useful.

#### Before and after examples

**Example 1: Vague and accusatory versus factual**

Before:
> Login is broken again. Whoever changed it clearly did not test it. Fix ASAP.

After:
> Summary: Login fails with a valid account after the password has been changed.
> Steps: 1) Change password to "NewPass#2024" on the Profile page. 2) Log out. 3) Log in with the new password.
> Expected: Login succeeds.
> Actual: Message "Invalid credentials" appears. Logging in with the old password succeeds.
> Environment: Chrome 120, Windows 11, test environment build 4.2.1.
> Attached: screen recording.

**Example 2: Opinion versus evidence**

Before:
> The registration page is too slow.

After:
> On the registration page, after clicking "Create account", the loading spinner shows for about 9 seconds before the confirmation appears (measured three times: 8.7, 9.1, 9.4 seconds) on a simulated slow 3G connection. On a normal connection it takes about 1 second. The requirement states a confirmation within 3 seconds.

**Example 3: Blaming a person versus describing behaviour**

Before:
> You did not handle empty passwords.

After:
> When the password field is left empty and Login is clicked, the page shows a blank error banner instead of a message. Expected: a message such as "Please enter your password."

**Example 4: Talking to someone face to face**

Before:
> "Your fix does not work."

After:
> "I tried the fix on my side and the original steps still fail at step 3. Could we look at it together? I have the recording ready, and maybe I have a different setting."

Tips for tone:

- Start with what you saw. Add what you expected. Offer help.
- Use neutral words such as "I observed", "the system shows", "the page displays".
- Acknowledge good work as well. If a feature is solid, say so. This builds trust, so that your next defect report is received with attention rather than defensiveness.
- If you are unsure it is a defect, say so: "I am not sure if this is intended. Could we check?"
- Choose the right channel. A quick conversation can be better than a long thread, and you should still record the outcome in the tracker.

### 9. Collaboration with developers and product owners

Quality is built in conversations. Testers work closely with several roles you met on Monday.

**With developers:**

- Treat them as partners in solving the same problem: delivering a working product.
- Share your testing ideas early, so they can think about those cases while building.
- Ask to sit with them when reproducing a tricky defect; two people looking at one screen can save hours.
- Learn their language: read pull requests, ask about the architecture, understand logs.
- Say thank you for quick fixes; ask politely when a report lacks detail on their side.
- Ask what they have already tested, to avoid duplication and to learn where they are less sure.

**With product owners:**

- The **product owner** is the person in a Scrum team responsible for the product's value and the backlog. They decide what is built and in what order.
- Ask them what matters most to users and the business; it helps you prioritise testing (risk).
- Clarify acceptance criteria before development starts. If a criterion is ambiguous, raise it in refinement.
- Help them understand the implications of defects in business terms, for example "Customers who register with a plus sign in their email cannot receive the welcome message" is more meaningful than "Email regex fails".
- Respect that decisions about releasing with known issues belong to the people accountable for the business, but make sure those decisions are informed by your honest information.

**A useful structure for a three-way conversation** (often called "Three Amigos" in Agile teams, between business, development and testing): before work starts on a story, the product owner explains the need, the developer explains how it might be built, and the tester asks what could go wrong and what examples would show it is right. Many defects are prevented in this 15-minute chat.

### 10. Ownership of quality: a whole-team responsibility

It is tempting to think that testers "own" quality: they are the ones who sign off, so they are the ones responsible. That is a trap.

- **Quality is built into the product at every step**: in understanding the need, in the design, in the code, in the build pipeline, in the test, in the release and in monitoring.
- **Everyone contributes.** Product owners write clear stories. Designers create usable interfaces. Developers write clean code and unit tests. Operations people keep environments stable. Testers bring specialist skills, coach others and look at the whole picture.
- **Testers are quality advocates and coaches** as much as checkers. They help the team to think about quality, rather than be a gate at the end that catches everything.

A simple analogy: in a restaurant, the head chef may have the best palate, but food safety and taste depend on the person buying the ingredients, the person cleaning the kitchen, the person cooking and the person serving. If only one person cares, the restaurant will have problems.

What ownership looks like in practice:

- Do not say "That is not my job." Say "How can I help us get this right?"
- When a defect escapes into production, the team asks "How can we change our process so this is caught earlier?", not "Whose fault was it?"
- Testers share their test ideas so developers can test earlier; developers share their changes so testers know where to focus.
- The team agrees on a shared definition of done that includes quality activities.

### 11. Thoroughness versus time: an introduction to risk-based thinking

There is a hard truth in testing: **you can never test everything**. Even a simple login form has an almost infinite number of possible inputs (every possible username and password, on every device and network, at every time). Time and budget are limited. So the question is not "Have we tested everything?" but "Have we tested the right things, well enough, given what we know?"

(The idea that exhaustive testing is impossible is one of the seven testing principles, which you will study in detail later today. Here we focus on the mindset it creates.)

**Risk-based thinking** is a way to decide where to focus. A **risk** is a possible problem that might happen in the future, combined with how bad it would be if it did. Two simple questions help you rank risk:

1. **Likelihood:** How likely is it to fail? (Complex, new or recently changed code is more likely to fail than simple, stable code.)
2. **Impact:** How bad would it be if it did? (Money lost, privacy exposed, safety, reputation, many users affected, no workaround.)

A quick way to use these is a small grid:

| | Low impact | High impact |
|---|---|---|
| **High likelihood** | Test, but briefly | Test first and in depth |
| **Low likelihood** | Test lightly or accept the risk | Test carefully; consider extra checks |

Applying it to Project 1:

- Login with valid credentials: high impact (nobody can use the app without it), moderate likelihood if recently changed, so test it first and often.
- Password reset: high impact (account recovery and security), so test it thoroughly.
- The colour of the footer link: low impact, low likelihood, so test lightly.
- Registration validation: high likelihood of mistakes (many rules and inputs), high impact (bad data, security), so test in depth.

Some rules of thumb:

- Test the most important things first, so that if time runs out, the biggest risks are covered.
- Be transparent. Tell stakeholders what was tested, what was not, and what risks remain. Silence is not an option.
- Re-evaluate as you learn. If you find many defects in one area, increase attention there (defects tend to cluster).
- Do not use risk as an excuse for laziness. "Low risk" must be a judgement based on information, not a feeling.

You will use this more formally when you study test planning and design techniques tomorrow.

### 12. Ethical and professional behaviour

Testers are trusted with access to systems, data and knowledge of weaknesses. This brings responsibility. Professional bodies such as ISTQB publish codes of ethics for testers. While wording varies, the key themes are consistent: acting in the public interest, acting in the interest of clients and employers, maintaining product integrity, using good judgement, supporting managers and leaders ethically, protecting the reputation of the profession, being supportive of colleagues, and committing to continuous learning. In everyday terms:

- **Honesty in reporting.** Report what you actually found. Do not hide failures to please someone, do not exaggerate to win an argument, and do not mark a test as passed when you did not run it. If you made a mistake, own it quickly; early honesty is always cheaper than late discovery. Test results are the basis for decisions, perhaps about safety or money; if they are false, the decisions will be wrong.
- **Confidentiality.** You may see customer data, unreleased products, security vulnerabilities and business secrets. Do not share them outside your authorised circle, do not copy real personal data into public tools or personal accounts, and follow your organisation's rules on test data. Where possible, use fake or masked data.
- **Authorisation.** Only test systems you have permission to test. "Thinking like an attacker" is a thinking tool, not a licence to probe systems that are not yours.
- **Integrity and independence of judgement.** Do not let pressure, friendship or reward change what you report. You can be kind in how you say a thing, but not change the fact.
- **Public interest.** If software could harm people (health, safety, privacy, finances), speak up through the proper channels, even when it is inconvenient.
- **Respect for colleagues.** Give credit, do not blame individuals, and be open to feedback.
- **Professional development.** Keep your skills current and help others to learn.

A sample ethical dilemma: it is Friday, the release is tomorrow, and you have found a defect where a user's saved address occasionally shows to another user. Your manager says, "Let's not put that in writing; we'll fix it next sprint." What do you do? The professional answer is to record the defect honestly, explain the risk clearly (privacy exposure), and escalate to the people who make release decisions. You do not need to be dramatic; you need to be honest and make sure the right people have the information.

### 13. Mindset in Agile teams

Agile teams deliver in small increments and welcome change. The testing mindset fits naturally here, and is in fact essential.

- **Test early and continuously.** Testers take part from backlog refinement onwards rather than waiting for a finished build. Asking "What if?" about a user story before it is coded is cheaper than finding the defect after.
- **Fast feedback.** Short cycles mean you provide information quickly and often. A tester who holds back findings until the end of the sprint wastes the benefit.
- **Embrace change.** Requirements will evolve. Keep your mind open, keep your tests adaptable, and avoid being attached to your first plan.
- **Collaboration over handoffs.** Testers, developers and the product owner work side by side, as you saw with Scrum ceremonies (planning, daily scrum, review, retrospective).
- **Whole-team quality.** The team agrees on acceptance criteria and a definition of done that include testing activities.
- **Retrospective thinking.** Use retrospectives to reflect honestly on what slipped through and why, always focusing on process rather than people.
- **Continuous improvement.** Every sprint is a chance to try a slightly better way of working.

### 14. Mindset in the age of AI tools

AI assistants are now part of many testers' daily work. They can suggest test ideas, draft test cases, turn requirements into scenarios, propose test data and help summarise logs. Used well, they are like a very fast, very well-read colleague who sometimes makes things up.

**How AI can support the mindset:**

- Generating "what if" ideas to spark your own thinking, especially across the perspectives from section 4 ("List ways a stressed user might misuse a login form").
- Drafting a first set of test cases that you then review and refine.
- Spotting ambiguity in a requirement ("Which parts of this story are unclear?").
- Helping to explain unfamiliar technology or code.

**What AI cannot replace:**

- Knowledge of your specific product, users and business context.
- Judgement about risk and priority.
- Actually running the test and observing the real behaviour.
- Accountability. If a defect escapes, "the AI said it was fine" is not an acceptable explanation.

**Always verify.** AI output can be confident and wrong. It may invent requirements, miss important cases, suggest outdated advice or produce tests that look plausible but check nothing. Treat every output as a draft written by a junior colleague whom you are mentoring: useful, but needing review.

**Automation bias** is the tendency to over-trust the output of automated systems, including AI tools and automated test results. Examples:

- A suite of automated tests is green, so the tester assumes the product is fine, without asking whether the tests check the right things.
- An AI generates 50 test cases; the tester accepts them all without noticing that none covers a stressed user, an accessibility user or a boundary value.
- A tool says "no accessibility issues found", so the tester stops checking, even though automated tools can only detect a portion of accessibility problems.

**Counter-measures:**

- Ask "What is this not checking?" of every tool result.
- Review AI-suggested test cases against the requirement and against your own list of perspectives.
- Run a few checks by hand to compare with what the tool reported.
- Never paste confidential data (customer records, credentials, unreleased designs) into an AI tool unless your organisation has approved it.
- Keep your own curiosity switched on: use AI to widen your thinking, not to replace it.

---

## Examples

### Mini-exercise 1: "Break the pencil" brainstorm

**Task:** You are given an ordinary wooden pencil. In five minutes, list as many ways as you can to test it or to make it fail. Do not worry about whether the ideas are sensible.

**Why this works:** It trains you to move beyond the obvious "does it write?" and to explore different conditions, users and uses.

**Sample answers (grouped):**

- *Basic function:* Does it write on paper? Is the line dark enough? Does it write on other surfaces (cardboard, wood, glass)?
- *Durability:* Drop it from desk height; from a greater height. Does the lead snap inside the wood? Bend it until it cracks. Squeeze it in a closed fist. Sharpen it many times: how long does it last?
- *Environment:* Leave it in a hot car; in a freezer; in water for a day. Does the paint peel? Does it write after drying?
- *Different users:* Can a left-handed person use it comfortably? A child? Someone with weak grip? Is the paint safe if a child chews it?
- *Usability:* Is the hardness grade (HB, 2B) clear? Does the eraser work well, or does it smudge? Does it roll off a sloped desk?
- *Quality and consistency:* Compare ten pencils from one pack. Are they the same length and hardness? Is the lead centred in the wood?
- *Misuse:* Use it as a hair pin, a lever, a stirrer. What happens when someone writes very hard or very fast?
- *Safety:* Is the paint non-toxic? Are there splinters? What happens when the tip breaks off?
- *Lifetime:* How many words can it write before it is too short to hold?

Notice how many ideas relate to users and conditions rather than to the pencil itself.

### Mini-exercise 2: "Vending machine" brainstorm

**Task:** A vending machine sells snacks and drinks. Customers choose an item by code (for example "B3"), pay with coins, notes or card, and the machine dispenses the item and any change. List as many test ideas as you can in five minutes.

**Sample answers:**

- *Normal use:* Insert exact amount, choose B3, receive item. Insert more than the price, receive correct change. Pay by card.
- *Payment:* Insert an invalid or foreign coin. A damaged or folded note. A card with insufficient funds. Cancel after paying: is the money returned? Put in many coins very fast. Pay with only small coins and receive change in large amounts. What if the machine has no change?
- *Selection:* Enter a code that does not exist ("Z9"). Press two codes at once. Change your mind after the first digit. Press the button for a sold-out item.
- *Dispensing:* The item gets stuck in the spiral. Two items drop at once. A bottle falls and breaks. The flap is jammed.
- *Interruptions:* Power cut during dispensing. Network failure during card payment: am I charged without getting an item?
- *Users:* A child who cannot reach the buttons. A wheelchair user. A person with low vision: are the codes readable? A person who does not read the language. A person in a hurry who presses buttons repeatedly. A person who shakes the machine.
- *Security and misuse:* Fake coins. Prying open the coin slot. Pulling the money-back lever repeatedly while inserting. Card cloning devices.
- *Environment:* Very hot or cold weather; direct sunlight on the display; heavy rain; a noisy location.
- *Maintenance and data:* Stock count wrong; prices changed by staff but display not updated; sales totals do not match cash.
- *Health and compliance:* Expiry dates; refrigerated items at the right temperature; allergen labels visible.

### Mini-exercise 3: "Login form" brainstorm

**Task:** A simple login form has an email field, a password field and a Login button. Brainstorm for five minutes.

**Sample answers:**

- *Valid input:* Correct email and password; email in different letter case; leading/trailing spaces around the email.
- *Invalid input:* Wrong password; unknown email; both empty; one empty; email without "@"; very long email; password of one character; password with emoji or non-English characters.
- *Behaviour:* Press Enter instead of clicking; double-click Login; click Login ten times quickly; use the Back button after logging in; refresh during login; open the login page in two tabs.
- *Security:* Many wrong attempts in a row (is there lockout or delay?); SQL-style or script-like text in the fields; does the error message reveal whether the email exists; is the password hidden; is there a "show password" option; is the connection encrypted; is the password visible in the URL or in browser history.
- *Session:* "Remember me" behaviour; session timeout; logging out and pressing Back; logging in on two devices.
- *Usability:* Is the cursor automatically in the first field? Does Tab move in a logical order? Is the "Forgot password" link visible? Does the browser or password manager autofill correctly?
- *Compatibility:* Phone, tablet, desktop; different browsers; small windows; zoomed text at 200%.
- *Accessibility:* Keyboard-only use; screen reader labels; errors not conveyed by colour alone; sufficient contrast.
- *Performance:* Slow connection; many people logging in at once.
- *Failure of dependencies:* Authentication server down; database slow; what message does the user see?

### Mini-exercise 4: Observation exercise

**Task:** Choose an everyday object or screen you can look at for two minutes, such as a door, a coffee machine, a bus-stop display or a mobile app's home screen. First, write down five things you notice. Then, write five things that you would not have noticed in a quick glance. Finally, write three questions about it.

**Why this works:** Testers need to see what is actually there rather than what they expect to be there. This directly counters familiarity and blind spots.

**Sample answers (a door):**

- *Five first things:* It is wooden; has a metal handle; is painted white; opens inward; has a lock.
- *Five things not noticed at first:* The handle is at a height a child could not reach; the paint is chipped near the bottom; the hinge squeaks; there is a gap under the door; the lock needs a key on both sides, which could be a problem in a fire.
- *Questions:* What happens in an emergency? Who uses this door most often? How would a person with a wheelchair open it? What happens in cold weather: does the door swell?

**Sample answers (a mobile app home screen):**

- *First things:* A logo, a search bar, three banners, a bottom menu.
- *Less obvious:* The second banner text is cut off; the icon for "Profile" looks like "Settings"; the search bar does not say what can be searched; no loading indicator appears for two seconds.
- *Questions:* What does the screen look like with no internet? What if the banner text is much longer? How does the page look on the smallest phone?

**Tip:** Do this exercise once a day for a week with different things. It builds the habit of noticing.

### Mini-exercise 5: Find-the-assumptions exercise

**Task:** Read this short requirement for the registration feature and list every assumption you can find (stated or hidden).

> "As a new customer, I want to register with my email address and a password so that I can place orders. After registering, I receive a confirmation email and I am logged in automatically."

**Sample answers:**

1. Every customer has an email address.
2. Each person has only one email address, and each email belongs to only one person.
3. The email address is typed correctly, and the system can tell if it is not.
4. The password rules are known to the user, but they are not stated here. Which rules apply?
5. The email system always works and always delivers. What if the email is delayed, goes to spam or fails?
6. "Logged in automatically" assumes the account is immediately active, even though the email has not yet been confirmed. Is that intended?
7. A customer will register only once. What if they register again with the same email?
8. The user registers from a device that can run the site.
9. The user can read and understand the language of the page.
10. "Customer" means a person; automated programs registering many accounts are not considered.
11. A "new customer" has no existing account under another name or email.
12. Registration should be fast enough; the requirement gives no number.
13. The user is allowed to register (age, country, legal restrictions are not mentioned).
14. Personal data will be handled appropriately; no mention of privacy consent.

For each assumption, a tester would ask: "How do we know? What happens if it is wrong?" These become questions for the product owner and test ideas for the team.

---

## Case Study: When a Small Assumption Costs a Lot

A well-known example is the loss of the **Mars Climate Orbiter**, a NASA space probe, in 1999. Described in general terms, the incident is widely reported as follows: two teams working on parts of the system used different units of measurement for a calculation involving the force produced by the spacecraft's thrusters. One part of the software produced numbers in one unit system, and another part consumed the numbers assuming a different unit system. The numbers were passed from one to the other without anything checking or converting them. Over many months, the small difference built up, the spacecraft's path was not what the planners believed, and the mission was lost when it approached the planet.

**What can testers learn from this?** (Notice that we focus on thinking, not on blaming anyone. Investigations of events like this usually point to several contributing factors in the process, not one careless person.)

- **Hidden assumptions.** Each team probably believed the other team's numbers were in the units it expected. Nobody asked "What if the other side is using something different?" A tester's habit of challenging assumptions at interfaces between components would help.
- **Systems thinking.** Each part may have worked correctly on its own. The failure appeared where the parts connected. Integration points are fertile ground for "what if" questions.
- **Weak signals.** Reports suggest that there were hints during the journey that the path was slightly off. Skepticism and tenacity mean following up on small anomalies rather than explaining them away (a form of anchoring: "it was fine so far").
- **Communication.** Information has to flow between teams in a form that is clear and checked. A good tester asks about interfaces: "What is the format, the unit, the range?"
- **The cost of late discovery.** The same question asked early, in a design or review meeting, costs almost nothing. Asked after launch, it is very expensive. This is why testers are involved early.

**A smaller, everyday version:** A web app lets users enter a price. The front end sends "10,50" (comma as the decimal separator, as in many European countries) but the server expects "10.50". Some users are charged 1050, some get an error, some get 10. Each component "works", but the assumption about format is unspoken. The tester's question, "What if the user's locale is different?", finds it.

**Discussion questions:**

1. Which of the traits from section 3 would have been most useful here?
2. At which point in the project could a question have been cheapest to ask?
3. What kind of independence (section 7) might have helped?

---

## Try It: Project 1 Login Page - 15 "What If" Questions

### Context

You are planning quality for Project 1 - QE Foundations. Its login page has an email field, a password field, a "Log in" button, a "Forgot password?" link and a "Create account" link. After a successful login, the user lands on their dashboard.

### Your task (about 30 to 40 minutes)

1. **Pick perspectives.** Choose at least four of the six perspectives from section 4 (typical, attacker, stressed, first-time, hurried, accessibility).
2. **Write 15 "what if" questions** about the login page. Rules:
   - Each question must start with "What if".
   - Cover at least five different categories from section 5.1 (input, order, environment, user, external failure, amount, time).
   - Include at least two questions that challenge an assumption you wrote down.
   - Include at least one that relates to accessibility and one that relates to security.
3. **Rate the risk.** Next to each question, write H, M or L for likelihood and for impact (section 11).
4. **Choose your top three.** Which three would you test first if you only had 30 minutes, and why?
5. **Reflect.** Which of the biases in section 6 might have shaped your list? What could you do to counter them?

### Template

| # | What if... | Perspective | Category | Likelihood (H/M/L) | Impact (H/M/L) |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |
| 15 | | | | | |

### Sample answer (use after you have tried your own)

| # | What if... | Perspective | Category | Likelihood | Impact |
|---|---|---|---|---|---|
| 1 | What if the user types their email with a capital letter, such as "Alex@Example.com", when they registered with "alex@example.com"? | Typical | Input | H | M |
| 2 | What if there are accidental spaces before or after the email (common when pasting)? | Hurried | Input | H | M |
| 3 | What if the password field is left empty and the user presses Enter? | Stressed | Input / order | H | L |
| 4 | What if the user enters a wrong password ten times in a row, quickly? Is the account locked, delayed or unprotected? | Attacker | Amount | M | H |
| 5 | What if the user types script-like or database-like text into the email field? | Attacker | Input | M | H |
| 6 | What if the error message says "No account found with this email" versus "Wrong password", revealing which emails are registered? | Attacker | External / information | M | H |
| 7 | What if the user clicks "Log in" five times in a row because nothing seems to happen? | Stressed | Order | H | M |
| 8 | What if the connection is very slow or drops while the login request is being sent? | Hurried | Environment | H | M |
| 9 | What if the user uses only the keyboard (Tab, Enter) and no mouse? Is the focus order logical and visible? | Accessibility | User | M | H |
| 10 | What if a screen reader user fails to log in? Is the error announced, and is it linked to the correct field? | Accessibility | User | M | H |
| 11 | What if the error is shown only in red colour, and the user is colour blind? | Accessibility | User | M | M |
| 12 | What if a first-time user does not know whether to use an email or a username, or what the password rules are? | First-time | User | H | M |
| 13 | What if the user logs out and presses the browser Back button? Can they still see their dashboard? | Typical / attacker | Order | M | H |
| 14 | What if the user's session expires while they are in the middle of a task, and they are sent to the login page? Do they return to where they were? | Typical | Time | M | M |
| 15 | What if the authentication service or database is unavailable? Does the user see a helpful message, or a technical error? | Stressed | External failure | L | H |

**Possible top three (30 minutes):** #4 (brute-force protection, high impact), #13 (access after logout, high impact), and #6 (information leak). They combine moderate likelihood with high impact on security and privacy.

**Reflection example:** "I noticed that I wrote many input questions and few time-related ones. That may be familiarity bias because I think about forms first. To counter it, I will pick a category I used least and add three questions from it."

### Stretch goal

Ask an AI assistant for 15 "what if" questions about the same login page. Compare its list with yours. Which ideas did it have that you missed? Which of its ideas are wrong, irrelevant or already covered by the requirements? What did you learn about verifying AI suggestions?

---

## Knowledge Check

Try to answer on your own before reading the answers.

**Q1. In your own words, what is a mindset, and why can it matter as much as technique in testing?**

**Q2. Which statement best describes the relationship between the developer mindset and the tester mindset?**
a) They are opposed; testers exist to catch developers' mistakes.
b) They are complementary perspectives aimed at the same goal: a good product.
c) Only testers need to think about quality.
d) Developers should never test their own work.

**Q3. A tester reads the requirement "The system should handle large files." Which trait is being used when they ask, "How large is large? What happens when the file is bigger than that?"**

**Q4. Match each user perspective with a login-page question:**
1. Attacker
2. Stressed user
3. First-time user
4. Accessibility user

a) Is it clear where to register and what the password rules are?
b) Can I use every control with the keyboard and a screen reader?
c) What if I send thousands of password guesses?
d) What if I click Login again and again, because I am in a hurry and panicking?

**Q5. A tester is told, "This module has always been very stable," and then tests it very lightly. Which bias is this, and how can it be countered?**

**Q6. A developer says: "I tested it and it works on my machine." Describe two things a tester can do in response, in a constructive way.**

**Q7. Order these from least to most independent: (a) a separate test team in the same company, (b) the developer who wrote the code, (c) an external specialist firm, (d) a tester embedded in the Agile team, (e) another developer on the team.**

**Q8. Rewrite this defect report in a constructive way: "Your search is garbage. It never finds anything."**

**Q9. Why is "quality is the tester's responsibility" an unhelpful statement? What is a better one?**

**Q10. You have two hours and many things to test. Describe how you would decide what to test first.**

**Q11. An AI assistant produces 40 test cases for the registration page. Your colleague suggests running them all and signing off. What risk is there, and what would you do?**

**Q12. You discover a defect that exposes one user's personal data to another. A manager asks you not to report it before the release. What do you do and why?**

### Answers

**A1.** A mindset is a set of habits, attitudes and beliefs that shapes how you notice and respond to things. In testing, techniques tell you how to test, while mindset decides what you wonder about, how deeply you dig, and how you behave when there is no script. Most important defects come from curiosity and questioning, not only from following instructions, so mindset matters as much as technique.

**A2.** b. The two mindsets complement each other. Developers lean toward building, testers lean toward questioning and exploring, and both aim for a good product. Developers also test (for example unit tests) and testers also need to understand construction.

**A3.** Critical thinking (also curiosity and attention to detail). The tester challenges a vague phrase and tries to turn it into something testable.

**A4.** 1-c, 2-d, 3-a, 4-b.

**A5.** Anchoring (the first information, "very stable", sets the level of effort), combined with optimism bias. Counter by asking for evidence of stability (past defects, recent changes), testing based on risk and recent change, and treating early information as a hypothesis.

**A6.** For example: (1) Ask for the exact environment details (browser, version, data, settings) and try the same steps in a second environment close to the real one; (2) share your own steps and a recording, and offer to reproduce it together. Avoid argument; use evidence and a collaborative tone.

**A7.** (b) developer who wrote the code; (e) another developer; (d) embedded tester; (a) separate test team; (c) external specialist firm.

**A8.** Example: "Searching for 'café' on the Products page returns 0 results, although three products with 'café' in the name exist. Searching for 'cafe' returns them. Expected: both searches return the same results. Environment: Chrome 120, test build 4.2.1. Screenshot attached." This is factual, specific, product-focused and has evidence.

**A9.** Quality is built in at every step by the whole team (product owner, designer, developers, testers, operations). If one person is seen as responsible, others will not take care, and problems are found late. A better statement: "Quality is everyone's responsibility; testers contribute specialist skills and help the team think about quality."

**A10.** Use risk-based thinking: for each area consider likelihood of failure (new, complex, changed, past defects) and impact (money, safety, privacy, number of users, reputation). Test high-likelihood/high-impact areas first, briefly cover low-risk areas, and tell stakeholders clearly what was and was not tested.

**A11.** Automation bias: over-trusting generated output. The cases may be incomplete, inaccurate or check the wrong things, and may miss perspectives (stressed user, accessibility) or product-specific rules. Review them against requirements and your own "what if" list, remove or fix poor ones, add missing ones, run a sample and observe real behaviour, and take responsibility for the result.

**A12.** Report it honestly and completely in the tracker with evidence, explain the privacy risk in business terms, and escalate to the people accountable for the release decision. Do not hide or downplay it. Honesty, public interest and integrity are core professional ethics, and the decision to release must be made with accurate information.

---

## Key Takeaways

- A **mindset** is a lens: habits and attitudes that shape what you notice and do. In testing it matters as much as technique.
- The **developer mindset** leans toward building; the **tester mindset** leans toward questioning, exploring and challenging. They are complementary partners, not rivals.
- Effective testers show **curiosity, critical thinking, skepticism, attention to detail, systems thinking, empathy for the user, communication, tenacity, humility, risk awareness and continuous learning**. All of them can be practised.
- Look at a feature through **many users' eyes**: typical, attacker, stressed, first-time, hurried and accessibility users.
- **"What if" questions, clarifying questions and challenging assumptions** are your main tools. Hidden assumptions are where defects hide.
- **Cognitive biases** (confirmation, anchoring, familiarity and blind spots, optimism, "works on my machine") are normal. Counter them deliberately with disproving tests, evidence, fresh eyes and variety.
- **Independence** brings objectivity but costs speed and context. Choose the level to suit the risk, and mix levels.
- Report **factually, blame the product not the person, and give evidence**.
- Work **collaboratively** with developers and product owners; **quality is a whole-team responsibility**.
- You cannot test everything. Use **risk-based thinking** (likelihood and impact) to focus on what matters most, and be transparent about what was not covered.
- Be **honest, confidential, authorised and professional**; follow the spirit of ISTQB-style ethics.
- In Agile, test early, give fast feedback and embrace change. With AI tools, use them to widen your ideas, **verify everything**, and beware of **automation bias**.

---

## Additional Resources

- **ISTQB (International Software Testing Qualifications Board):** https://www.istqb.org - the home of the Foundation Level syllabus and the code of ethics that many testing certifications follow. The ISTQB glossary is at https://glossary.istqb.org.
- **Ministry of Testing:** https://www.ministryoftesting.com - a large community with articles, talks, courses and discussion about testing skills and thinking.
- **Atlassian Agile Coach:** https://www.atlassian.com/agile - friendly guides on Agile, Scrum, and the way teams collaborate on quality, useful alongside your Jira practice.
