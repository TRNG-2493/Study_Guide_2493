# Defect vs. Error vs. Failure

## Learning Objectives

By the end of this lesson, you will be able to:

- Define **error**, **defect**, and **failure** in your own words and explain how they are connected in a cause-and-effect chain.
- Explain how the related terms (fault, bug, issue, incident, anomaly, mistake) fit around those three core words, and which ones are synonyms in everyday work.
- Describe, with a worked Python example, why a defect only produces a failure when specific inputs or conditions execute it.
- Recognize defects that never cause failures, and failures that are not caused by defects in the code at all.
- Explain why one error can create many defects and why one defect can cause many failures.
- Name the common places where errors originate and use simple root-cause categories.
- Show where defects are injected and detected across the SDLC and why finding them earlier is cheaper.
- Map the chain onto the Tuesday bug report and defect lifecycle.
- Calculate defect density and defect removal efficiency from simple numbers.
- Classify short real-world scenarios as error, defect, or failure, and trace a full chain from a root cause to a visible symptom.
- Run, diagnose, and fix a small buggy Python function, writing the failing check as a plain `assert`.

## Why This Matters

On Tuesday you learned to write a bug report and follow a defect through its lifecycle. You may have noticed that we used the words "defect" and "bug" as if they meant the same thing, and that we said a tester "found a defect." That was a simplification on purpose. Today we sharpen it.

In reality, a tester almost never sees a defect directly. A defect is a flaw sitting quietly inside a piece of work, such as a line of code, a sentence in a requirement, or a setting in a configuration file. A tester sees what happens when that flaw gets triggered: a wrong total on the screen, a button that does nothing, a page that crashes. The thing the tester sees is a **failure**. The developer then works backwards from the failure to find the defect, and a good team goes one step further and asks what **error** led to that defect in the first place, so it does not happen again.

Why does this matter for you as a Quality Engineer?

1. **Precision builds trust.** When you say "I observed a failure; the likely defect is in the discount calculation," developers take you seriously. When everything is just "a bug," conversations get vague.
2. **Better bug reports.** A bug report describes the failure (what you observed and how to reproduce it). Knowing that makes your reports about symptoms and evidence, not guesses about code you have not seen.
3. **Better testing.** If you understand that defects hide until specific inputs trigger them, you will understand why testing with only one "happy" example is not enough. That idea drives everything you will learn on Thursday about test design.
4. **Prevention, not just detection.** If you understand where errors come from, you can help the team stop them earlier, which is the heart of the quality-engineering mindset you started building this morning.

This vocabulary also appears on the ISTQB Foundation Level exam, and Wednesday's demo asks you to classify exploratory-session findings as error, defect, or failure and as positive or negative. Today's lesson gives you the tools to do that confidently.

---

## The Concept

### 1. A Simple Analogy: The Wrong Road Sign

Imagine a city worker is updating road signs. The worker misreads a map and believes that the airport is to the **left** at a particular junction, when it is actually to the **right**. The worker installs a sign pointing left.

- The worker's misunderstanding of the map is the **error** (a human mistake).
- The wrong sign standing at the junction is the **defect** (a flaw in a work product, the sign).
- A driver who follows the sign and ends up lost in the suburbs is the **failure** (an observable wrong result when the flaw is "executed" by someone using it).

Now notice some important things:

- The wrong sign sits there all day, every day. But it only causes a failure when a driver actually arrives at that junction heading to the airport. A driver who never uses that road is not affected. The defect exists, yet no failure happens.
- The driver, who is like a tester, does not see the worker's error or even the sign's flaw as such. The driver sees being lost. The road authority later investigates, finds the wrong sign, and eventually discovers the misread map.
- If the same worker misread the map for several junctions, several wrong signs would exist (one error, many defects). And one wrong sign could mislead hundreds of drivers (one defect, many failures).

Keep this picture in mind. Everything else in this lesson is a more detailed version of it.

### 2. The Core Chain

Here is the chain in software terms. Read the definitions carefully, because they are paraphrased from the ISTQB glossary and are the "official" meanings used in the industry.

| Term | Plain-language definition | Where it lives | Who "sees" it |
|---|---|---|---|
| **Error** (also called a **mistake**) | A human action that produces an incorrect result. Misunderstanding, forgetting, mistyping, wrongly assuming. | In a person's head or actions | Usually nobody, until later analysis |
| **Defect** (also called a **fault** or **bug**) | An imperfection or flaw in a work product, so that it does not meet its requirements or specification. | In a document, code, data, or configuration | Found by reviewing, static analysis, or by investigating a failure |
| **Failure** | An event in which a component or system does not perform a required function within specified limits, observed as a deviation from expected behavior. | In the running system's behavior | Testers, users, monitoring tools |

The chain looks like this:

```
  HUMAN                 WORK PRODUCT                 RUNNING SYSTEM
 +---------+   leads    +-----------+   executed     +-----------+
 |  ERROR  | ---------> |  DEFECT   | ------------>  |  FAILURE  |
 | (mistake)|  to       | (fault/bug)|  under the     | (observable|
 +---------+            +-----------+   right         |  wrong     |
      ^                       |         conditions    |  behavior) |
      |                       |                       +-----------+
   root cause           exists silently                     |
   (why did the         until triggered                     v
    person err?)                                   Tester or user notices,
                                                   reports an "incident"
```

Three important details hide in this diagram:

1. **The arrows are "can lead to," not "always leads to."** An error may or may not result in a defect (maybe a reviewer catches it first). A defect may or may not result in a failure (maybe the code is never run, or never run with the triggering input).
2. **A failure needs execution.** A defect in a document or in code is just text until somebody follows the document or the computer runs the code. Failure appears at runtime.
3. **Root cause sits one step before the error.** If you keep asking "why?", you end up at a root cause, such as unclear requirements or time pressure. We cover this in section 7.

### 3. The Related Terms: Synonyms and Distinct Words

People use many words around these three. Some are real synonyms in practice. Others are formally different. Here is the honest picture.

| Term | Meaning | Relationship to the core chain |
|---|---|---|
| **Mistake** | A human action that produces an incorrect result | Formal synonym of **error** |
| **Fault** | A flaw in a work product | Formal synonym of **defect** |
| **Bug** | Everyday slang for a flaw in software | Informal synonym of **defect** (and often used loosely for failure) |
| **Defect** | The official ISTQB term for the flaw | The standard word used in test documentation |
| **Failure** | Observable deviation when running the system | Formally distinct from defect |
| **Incident** | An event that needs attention or investigation, typically a failure that someone has noticed and reported | Related to failure: the "report" side of it |
| **Anomaly** | Any condition that deviates from expectation, seen during testing, review, or use. Might turn out to be a defect or a false alarm | Broader and more neutral: "something looks off" |
| **Issue** | A very broad everyday word. In Jira, an "issue" is any work item (story, task, bug, epic) | Not a formal testing term. Be careful: a Jira "issue" is not necessarily a defect |

A simple way to remember it:

- **Error = mistake** (the human part).
- **Defect = fault = bug** (the flaw in the work product).
- **Failure** (the visible misbehavior). This is the one that is formally different from the others.
- **Anomaly / incident** are neutral words for "we noticed something odd" before we know what caused it.
- **Issue** is a wide umbrella; Jira uses it for every type of ticket.

Why is "anomaly" useful? Because when you first see odd behavior, you do not yet know whether it is a defect, a misunderstanding of the requirement, a bad test environment, or a mistake in your own test. Calling it an anomaly or an incident keeps you honest. You observed something; the investigation decides what it is.

**What about Tuesday?** On Tuesday, "defect" and "bug" were used interchangeably. That remains fine in daily conversation, since in practice teams say "bug" for both the flaw and the symptom. The formal distinction, which you now know, is useful when you need precision: in a bug report you describe the **failure**; in the fix and root-cause analysis the team talks about the **defect** and the **error**.

> **A note on language in real workplaces.** Many teams file everything in a ticket type called "Bug" and never say "failure." That is normal. Do not correct your teammates in meetings. Instead, use the precise words in your own writing and let your clarity speak for itself.

### 4. The Extended Story: A Discount Code in Python

Let us make the chain concrete with a small story you can run.

**The requirement.** An online shop's requirement document says:

> *"Orders of $100 or more receive a 10% discount."*

**The error.** The developer, working quickly, reads this as "orders over $100." The words "or more" are skipped or mentally rounded off. This misunderstanding is the **error**. It is a human mistake and it happened in the developer's head. You cannot find it in the code itself, because a mistaken understanding is not a line of code.

**The defect.** The developer writes this function:

```python
def apply_discount(order_total):
    """Requirement: orders of $100 or more get 10% off."""
    if order_total > 100:          # defect: should be >=
        return round(order_total * 0.90, 2)
    return order_total
```

The operator `>` is the **defect**. It is a flaw in the work product (the source code). It is a very common kind of defect called an **off-by-one** or **boundary** defect, because it mishandles the value exactly at the edge (100). Notice that the defect is a direct consequence of the error: the developer understood "over 100," so the developer wrote "greater than 100."

**Does a failure happen?** Not necessarily. Let us run the function with several order totals:

```python
for amount in [50, 99.99, 100, 100.01, 250]:
    print(f"Order {amount:>7} -> pays {apply_discount(amount)}")
```

Output:

```
Order      50 -> pays 50
Order   99.99 -> pays 99.99
Order     100 -> pays 100
Order  100.01 -> pays 90.01
Order     250 -> pays 225.0
```

Let us check each row against the requirement:

| Order total | Expected (per requirement) | Actual | Verdict |
|---|---|---|---|
| 50 | 50 (no discount) | 50 | Correct |
| 99.99 | 99.99 (no discount) | 99.99 | Correct |
| **100** | **90.0 (10% off, "or more")** | **100** | **FAILURE** |
| 100.01 | 90.01 | 90.01 | Correct |
| 250 | 225.0 | 225.0 | Correct |

Look at what this tells us:

- The defect has been present in all five runs. It is always there.
- It only **caused a failure** for one input: exactly 100. For four out of five inputs, the function gave the right answer even though the code is wrong. The defect was "executed" every time, because the `if` line runs on every call, but it only produced an observable wrong result when the input sat on the boundary.
- A tester who tried only 50 and 250 (two "typical" examples) would conclude the function is fine. This is exactly why testers care about **boundaries**: Thursday's lesson on test design techniques will give you tools such as boundary value analysis to catch this systematically.

The customer's view: a customer with exactly $100.00 in the cart sees no discount, even though the website advertised one. They complain. That complaint is an **incident** report about a **failure**. The developer investigates, finds the `>` **defect**, and a root-cause discussion identifies the **error**: a misread requirement. The fix is a single character:

```python
if order_total >= 100:
```

Recap of the entire chain in this story:

```
 Developer reads "$100 or more" as "over $100"      -> ERROR
 Code contains `if order_total > 100`               -> DEFECT
 Customer with exactly $100 gets no discount        -> FAILURE
 Customer emails support; ticket is created         -> INCIDENT / bug report
```

### 5. Defects That Never Cause Failures

Not every defect results in a failure. Here are the common reasons:

**Dead code.** Code that can never be reached. Example:

```python
def get_label(status):
    if status == "active":
        return "Active"
    else:
        return "Inactive"
    print("Label returned")     # never runs: after return
```

If the `print` line had a flaw (say it referenced an undefined variable), nobody would ever notice, because it never executes.

**Rarely executed paths.** Code that runs only in unusual situations, such as the leap-year handling in a calendar, an error-recovery routine, or a rarely used admin feature. The defect may exist for years and cause a failure only on 29 February, or only when a disk is full.

**Unused features.** A function nobody calls, a feature behind a switch that is turned off, or an old module left in the code base.

**Defects in documents that no one follows.** A wrong figure in a design document that no developer happens to read has no effect.

**Defects masked by other behavior.** Two flaws can cancel each other out. A wrong sign (plus instead of minus) in one place and another wrong sign downstream can produce the correct end result. When one is fixed, the other suddenly causes a failure. Experienced testers call this fault masking.

Do these still count as defects? **Yes.** They are flaws. They deserve fixing eventually, because code changes over time: a "never-executed" path may become executed after a later change and then fail suddenly, with no obvious connection to the change that exposed it. But in terms of priority, a defect that cannot currently cause a failure is usually low priority. (Recall priority vs. severity from Tuesday. We recap it below.)

### 6. Failures Not Caused by Defects in the Code

The reverse also happens: a failure occurs even though the code is perfect. The ISTQB syllabus stresses that failures can be caused by environmental conditions too. Examples:

| Cause | Example | Is there a code defect? |
|---|---|---|
| **Hardware / radiation** | A stray cosmic ray or electromagnetic burst flips a bit in memory, producing a wrong number | No (rare, but real, especially in space and avionics) |
| **Environment configuration** | The test server runs a different time zone, so a report cut-off lands on the wrong day | Possibly a configuration defect, not a code defect |
| **Bad or missing test data** | The test database has no customer record for the test user, so login "fails" | No. The data is wrong |
| **Misuse** | A user pastes a 10,000-character string into a field the documentation says holds 50, and the app rejects it | Usually no. This is the system working as designed |
| **Outdated browser or device** | A site designed for modern browsers renders poorly on a ten-year-old browser the product states it does not support | Depends on the supported-platform requirement |
| **Network / third-party outage** | A payment provider is down, so the checkout shows an error | No defect in your code |
| **Expired certificate, full disk, revoked key** | Operations problems | No code defect; an operations or process defect |

This matters for you in practice. Before you report a failure, ask: *Is my environment correct? Is my data correct? Am I using the system as intended? Is this browser supported?* A report that turns out to be caused by a mistake in your test setup wastes everyone's time and slowly damages your credibility.

#### False positives and false negatives

Testing itself can be wrong in two ways. Learn these two words; they are used constantly.

| Term | Meaning | Example | Consequence |
|---|---|---|---|
| **False positive** (false alarm) | The test reports a failure, but there is actually **no defect** | Test fails because the test environment was down, or the expected result in the test was wrong | Wasted time; loss of trust in tests |
| **False negative** (missed defect) | The test passes, or reports no failure, but there **is** a defect | The tester checks only the value 250 and misses the boundary defect at 100 | Defect escapes to users; false confidence |

A way to remember: in testing, "positive" means "the test found a problem." So a *false* positive is a **false alarm**, and a *false* negative is a **missed problem**. (This is the opposite of the medical intuition that "positive is good." In testing, positive results in this sense mean "a defect was indicated.")

> **Careful, the word "positive" appears in a second meaning.** In this week you also meet "positive test case" and "negative test case." A positive test case checks valid input and expected behavior ("log in with correct credentials"). A negative test case checks invalid input and how the system copes ("log in with a wrong password"). That is a separate idea from false positives/negatives. We use it in the exercise below.

### 7. One Error, Many Defects; One Defect, Many Failures

The chain is not always a single line. It branches.

**One error, many defects.** Suppose a developer misunderstands the discount rule as "strictly over $100." They might apply the same misunderstanding in:

- the shopping-cart page (`>` instead of `>=`),
- the order summary email template,
- the invoice generator,
- the mobile app's own copy of the logic.

Four defects, one error. A different example: a team misunderstands the date format required (day/month vs. month/day). That one error might produce defects in the date picker, the report filter, the export file, and the database import.

**One defect, many failures.** The single `>` in `apply_discount` fails every time any customer spends exactly $100.00, so it can cause thousands of failures across many days, for many customers, through the website, the mobile app, and the phone-order system that reuse the function.

Here is the picture:

```
            ONE ERROR                         ONE DEFECT
               |                                  |
        +------+------+                    +------+------+
        |      |      |                    |      |      |
     defect  defect  defect             failure failure failure
     (cart)  (email) (invoice)          (web)   (app)   (phone)
```

This has two practical consequences:

1. **When you fix a defect, ask whether the same error produced siblings.** Search for similar code. A good developer or reviewer asks, "Where else did we make this same assumption?"
2. **Do not count failures as defects.** If 500 customers hit the same flaw, you have 500 failure reports but **one** defect. If your team's defect count is "number of tickets," duplicates can distort your numbers. Duplicate tickets are linked and closed, which you saw in the Tuesday defect workflow.

Here is a tiny code illustration of the "many defects" idea, using a password-length rule. Suppose the requirement is "a password must be 8 to 20 characters long, including both 8 and 20."

```python
def is_valid_password(pw):
    """Requirement: password must be 8 to 20 characters."""
    return 8 < len(pw) <= 20   # defect: should be 8 <= len(pw)

for pw in ["abc", "abcdefgh", "abcdefghi", "a" * 20, "a" * 21]:
    print(len(pw), is_valid_password(pw))
```

Output:

```
3 False
8 False
9 True
20 True
21 False
```

The 8-character password returns `False`, but it should be `True`. That is a failure caused by a defect on the lower boundary. The `<=` on the upper boundary is correct, so a person who tested only the upper boundary would miss it. If the same developer wrote the same style of check in the username validator, the phone validator, and the search-box limit, one error would have produced many defects.

### 8. Where Do Errors Come From?

Errors are human, so they appear wherever humans work. Understanding the common origins helps you find the **root cause**, which is the earliest fundamental reason that led to the error. Fixing only the defect is like mopping a floor while the tap is still running. Fixing the root cause turns off the tap.

| Origin | What happens | Example | Typical root-cause category |
|---|---|---|---|
| **Requirements** | Requirement is ambiguous, incomplete, contradictory, or missing | "The system should be fast" (how fast?) | Requirements / specification |
| **Design** | Design does not match the requirement, or the design is flawed | Architect assumes all users are in one time zone | Design / architecture |
| **Code** | Developer writes incorrect logic, wrong operator, typo, missed null check | `>` instead of `>=` | Implementation / coding |
| **Data** | Wrong, missing, or corrupt data; wrong data model | A column too short for real names | Data / database |
| **Process** | Steps skipped or not defined; no code review; no definition of done | Release built from an unreviewed branch | Process / methodology |
| **Communication** | Information lost between people or teams | The BA told the developer one thing, the designer another | Communication / collaboration |
| **Tooling** | Faulty or misconfigured tools | A build tool silently uses an old library version | Tools / environment |
| **Assumptions** | A belief that was never checked | "Every user has a phone number" | Assumption / domain knowledge |
| **Time pressure** | Rushing leads to skipped checks and shortcuts | Release in two days, code review skipped | Schedule / management |
| **Lack of skill or knowledge** | New team member unfamiliar with the domain or language | Misusing an API function that rounds differently | Training / onboarding |

A technique you can use to find root causes is the **"5 Whys."** Ask "why" repeatedly:

1. Why did customers with exactly $100 not get the discount? *Because the code uses `>`.*
2. Why does the code use `>`? *Because the developer thought the rule was "over $100."*
3. Why did the developer think that? *Because the ticket said "orders over $100" in its summary, while the requirements document said "or more."*
4. Why did the two differ? *Because the product owner edited the document but not the ticket.*
5. Why was the ticket not updated? *Because there is no step in the process that checks tickets against the requirements after a change.*

The last answer is a process gap, a root cause that could be addressed (for example, with a short "refinement check" after any requirement change). Notice how the story moved from a code detail to a team habit. That is the quality-engineering mindset at work: you are not blaming a person; you are improving the system the person works in.

> **Blameless culture.** Errors are human, and good teams talk about errors without blaming individuals. If a developer is blamed for a mistake, people hide mistakes, and hidden mistakes cost more in the long run.

### 9. Defect Injection and Defect Detection Across the SDLC

Remember the SDLC phases from Monday. Defects are **injected** (introduced) at some phase and **detected** (found) at some, possibly later, phase. The longer a defect lives before detection, the more work gets built on top of it, and the more expensive it is to repair.

| SDLC phase | What defects can be injected here | Typical ways they are detected | Relative cost to fix when found here (qualitative) |
|---|---|---|---|
| **Requirements** | Ambiguous, missing, or contradictory requirements | Requirement reviews, walkthroughs, asking questions | Very low: edit a sentence |
| **Design** | Flawed architecture, wrong interface, wrong data model | Design reviews, prototypes | Low: redraw a diagram, discuss |
| **Coding** | Logic errors, wrong operators, missing checks | Peer review, static analysis, unit tests | Low to moderate: change code, re-run unit tests |
| **System / integration testing** | Defects between components, environment issues | Test execution, failures observed by testers | Moderate: needs diagnosis, fix, rebuild, retest |
| **Acceptance testing** | Mismatch between product and real needs | Business users trying the product | Moderate to high: rework across several areas |
| **Production / after release** | Everything that slipped through | Customer complaints, monitoring | High: customers affected, emergency fixes, reputation damage, data repair |

We deliberately describe cost qualitatively. You will sometimes see charts claiming that fixing a defect in production is exactly ten, thirty, or a hundred times more expensive than in requirements. Those exact multipliers vary widely between organizations, projects, and studies, and should not be quoted as fact. The **direction** of the trend (later means costlier) is widely accepted, and the reasons are easy to see:

- More people and more documents depend on the flawed item as time passes.
- Fixing late means rework in design, code, tests, and documentation.
- Customers may suffer losses, and trust is hard to win back.
- Data created by the wrong behavior may need repair.

This idea is called **shift-left**: move quality activities earlier (to the left on a timeline). Reviewing requirements is testing, in a broad sense, because it detects defects before any code exists.

```
 TIME ------------------------------------------------------------>
 Requirements -> Design -> Code -> Test -> Release -> Production
   inject ^        inject ^  inject ^
   detect <-- ideally here    detect (testing)       detect (users: worst case)
   cost:  low ----------------------------------------------> high
```

A helpful companion measure is a **phase containment** goal: try to detect each defect in the same phase where it was injected. A defect injected in requirements and found in a requirement review has been contained.

### 10. How This Maps to the Tuesday Bug Report and Defect Lifecycle

Think back to Tuesday's bug report. A good bug report has a title, steps to reproduce, expected result, actual result, environment, severity, and attachments. Look at what those fields describe:

- **Steps to reproduce, actual result, environment:** these describe the **failure**. They record what you did and what you observed.
- **Expected result:** this is derived from the requirement or from reasonable expectations.
- The report does **not** usually include the exact line of code. That is the **defect**, and finding it is the developer's job during **diagnosis** (often called debugging).
- The **error** often shows up later in the **root cause** field of a resolved ticket, if your team records one.

Mapping onto the lifecycle states you learned (New, Assigned/Open, In Progress, Fixed, Ready for Retest, Retested/Verified, Closed, Reopened, Rejected, Deferred, Duplicate):

| Lifecycle moment | What is happening in terms of our chain |
|---|---|
| **New** | A tester or user reports a **failure** (an incident) |
| **Rejected / Not a defect** | Investigation shows no defect: it was a **false positive**, a misuse, a test-environment issue, or expected behavior |
| **Duplicate** | Another failure report that traces to the **same defect** |
| **Assigned / In Progress** | A developer diagnoses the failure to locate the **defect** and understand the **error** behind it |
| **Fixed** | The defect has been removed from the work product (code, config, data, or document) |
| **Ready for Retest / Retested** | The tester re-runs the steps that produced the **failure** to confirm it no longer happens, and runs related checks to be sure nothing else broke |
| **Reopened** | The failure still occurs: the fix did not remove the defect, or only removed part of it |
| **Deferred** | The defect is known, but the team decides to fix it later (often because its severity or priority is low) |
| **Closed** | The failure no longer occurs, and the matter is complete |

So the one-line summary: **a failure is what the tester observes and reports; the defect is what the developer finds and fixes; the error is what the team learns from.**

#### Severity vs. priority: a quick recap

- **Severity** is how serious the **impact** of the failure is on the system or users (technical and business impact). Example: a crash on checkout is high severity.
- **Priority** is how **urgently** the team should fix it (a business scheduling decision). Example: a typo in the company name on the home page may be low severity but high priority before a big launch.

The two are separate dials. Examples:

| Scenario | Severity | Priority |
|---|---|---|
| Checkout crashes for every customer | High | High |
| Crash in an admin report used once a year | High | Low |
| Company logo misspelled on the landing page the day before a launch | Low | High |
| Slightly misaligned icon on a rarely visited settings page | Low | Low |

Severity belongs mostly to the failure (what damage does it do?). Priority is a decision about the fix.

### 11. Defect Density and Defect Removal Efficiency: A Recap with Calculations

Quality teams like simple numbers, as long as they are understood and not abused. Two common measures:

**Defect density** = number of defects found / size of the work product.

Size is often measured in lines of code (usually per thousand lines, written KLOC), function points, or number of requirements/stories. It tells you how "dense" the defects are in a component.

**Defect removal efficiency (DRE)** = defects found before release / (defects found before release + defects found after release), usually shown as a percentage.

It measures how good your detection activities (reviews, testing) were at catching defects before customers did.

**Worked example.** A team releases a module of 20,000 lines of code (20 KLOC). During reviews and testing they found and confirmed **45** defects. In the first three months after release, customers reported failures that traced to **5** more defects.

- Total defects known: 45 + 5 = 50
- Defect density: 50 / 20 KLOC = **2.5 defects per KLOC**
- DRE: 45 / (45 + 5) = 45 / 50 = **90%**

Interpretation: the team caught nine out of every ten known defects before release. They still let some slip through, so they would ask which kinds of defects escaped and why.

Cautions:

- These numbers count only defects **found so far**. Undiscovered defects are not in the count. A low defect density might mean great code or might mean poor testing.
- Defect counts are not a measure of a person's worth. Never use them to rank individual developers or testers; people will adapt their behavior to the metric.
- Comparing across modules of very different complexity can mislead.

You can express DRE and density as code if you want a quick calculator:

```python
def defect_density(defects, kloc):
    return defects / kloc

def dre(found_before_release, found_after_release):
    return found_before_release / (found_before_release + found_after_release) * 100

print(defect_density(50, 20))   # 2.5
print(dre(45, 5))               # 90.0
```

### 12. Defect Prevention vs. Defect Detection

| | **Defect prevention** | **Defect detection** |
|---|---|---|
| Goal | Stop errors from becoming defects | Find defects that already exist |
| Focus | People, process, requirements, tools | Work products and running software |
| Typical activities | Clear requirements, training, coding standards, pair programming, checklists, definition of done, root-cause analysis, good tooling | Reviews, static analysis, unit/integration/system tests, exploratory testing, monitoring |
| Quality approach | Closer to **quality assurance** (process focus) | Closer to **quality control** (product focus) |
| When it acts | Before the defect is injected | After the defect is injected |

You met QA vs. QC earlier today: prevention is a QA-style activity (improve the way work is done), and detection is a QC-style activity (check the product). A mature team does both. Prevention reduces how many defects get created; detection catches the ones that still get through. Prevention alone is never perfect, because humans still make errors, and detection alone is expensive, because it finds problems only after they exist.

(Why defects tend to gather in certain places, and why re-running the same tests eventually stops finding new defects, are covered in the upcoming lesson on testing principles. For now, simply know those ideas exist.)

### 13. Putting It All Together in Project 1: The Login Feature

Time to apply this to our sample web app. Consider the login feature of Project 1.

**The requirement (from the requirements document):**

> *"A user logs in with their registered email address and password. Passwords are case-sensitive. A login with an incorrect password must be rejected with the message 'Invalid email or password'."*

**The error.** A developer implementing the check thinks "users often mistype the capitalization, so let's be friendly and ignore case." They either skim past "case-sensitive" or decide it would be an improvement. The developer's wrong understanding (or well-meant but unauthorized change) is the **error**.

**The defect.** In the code:

```python
def check_login(stored_password, entered_password):
    # defect: comparison ignores letter case, requirement says case-sensitive
    return stored_password.lower() == entered_password.lower()

print(check_login("Secret99", "Secret99"))   # True  - correct
print(check_login("Secret99", "secret99"))   # True  - WRONG, should be False
print(check_login("Secret99", "Other123"))   # False - correct
```

Output:

```
True
True
False
```

(Real login code would never store passwords in plain text and would compare hashes. The simplified function here is only to illustrate the logic.)

**The failure.** A tester runs a **negative test case**: log in with the right email and the password in the wrong case. Expected: rejection. Actual: login succeeds. The failure is only visible to a tester who chose that particular input. A tester who tried only "correct password" (a positive test) and "completely wrong password" would see nothing wrong.

Notice how this connects to your Wednesday exercise: writing both positive and negative test cases for login and registration is exactly how you reveal defects that remain invisible to happy-path checks.

**Sample bug report (what the tester writes, describing the failure):**

```
Title:        Login accepts password with different letter case
Project:      Project 1 - QE Foundations
Type:         Bug
Component:    Login
Environment:  Test (QA), Chrome 126 on Windows 11, build 0.4.2
Severity:     High (security-related: weakens credential check)
Priority:     High
Reporter:     <your name>

Preconditions:
  Registered user exists: email "demo.user@example.com", password "Secret99"

Steps to reproduce:
  1. Open the Login page.
  2. Enter email "demo.user@example.com".
  3. Enter password "secret99" (all lowercase).
  4. Click "Log in".

Expected result:
  Login is rejected with the message "Invalid email or password"
  (requirement REQ-LOGIN-03: passwords are case-sensitive).

Actual result:
  The user is logged in and redirected to the dashboard.

Attachments:  screenshot of dashboard after login, browser console log
Notes:        Reproduced 3 out of 3 times. Correct password "Secret99"
              also works. A completely different password is rejected correctly.
```

What the report contains and what it does not:

- It describes the **failure** (what was observed) and how to reproduce it.
- It references the requirement so the expected result is justified.
- It does not claim "the developer used `.lower()`." The tester did not see the code. The tester may mention a suspicion, but states it as such. Diagnosing the **defect** is the developer's job.

**What happens next.** The developer investigates and finds the `.lower()` calls (defect). During review, the team realizes the error: the requirement was skimmed. They also check the registration page, the password-reset page, and the mobile login for the same pattern (one error, possibly many defects). They fix the code and record root cause as "requirement misread," with an action to add a "key rules" checklist to code review. The tester retests the exact steps, plus the correct and wrong password cases (including a different-case wrong password), and closes the ticket.

---

## Examples

### Example A: Defect that stays hidden

```python
def calculate_tax(amount, region):
    if region == "EU":
        return amount * 0.20
    elif region == "US":
        return amount * 0.08
    elif region == "MARS":          # nobody can select this region
        return amount * 0.80 + "5"  # defect: adding a number and a string
    return 0.0

print(calculate_tax(100, "EU"))
print(calculate_tax(100, "US"))
```

Output:

```
20.0
8.0
```

The `"MARS"` branch contains a defect (it would raise a `TypeError`), but no input in normal use reaches it. The defect exists; a failure does not. If a later release adds "MARS" to the region list, the failure suddenly appears.

### Example B: Failure with no code defect

A tester runs a checkout test on Monday morning, and it fails because the payment provider's sandbox is offline for maintenance. Nothing in the code is wrong. The correct action is to check the environment, wait or retry later, and not file a code defect. Had the tester filed a bug, it would be rejected as "not a defect" (a false positive).

### Example C: One error, many defects, many failures

A team misunderstands "inclusive date range" (start and end dates both included) as exclusive. Defects appear in the booking search, the invoice night-count, and the cancellation-policy calculation. Each defect fails in multiple ways: wrong prices, wrong dates on emails, wrong refund amounts. A single misunderstanding led to three defects and, via those, to countless failures.

---

## Try It: Classification Practice

### Part 1: Classify 20 scenarios

For each scenario, decide: **Error** (a human mistake), **Defect** (a flaw sitting in a work product such as code, a document, data, or configuration), or **Failure** (an observable deviation when the system runs or is used). Try before looking at the answer key.

1. A developer reads "at least 18 years old" and understands it as "over 18."
2. The code contains `if age > 18` where the requirement says an applicant must be 18 or older.
3. An 18-year-old applicant is rejected on the registration page.
4. The requirements document says "minimum password length is 8" in one section and "minimum password length is 6" in another.
5. A business analyst assumes that every user has a mobile phone number and writes the requirement accordingly.
6. The app shows a blank white screen when the user taps "Pay."
7. A test case's expected result was copied from an older version of the product and no longer matches the current requirement.
8. A tired tester writes down the wrong expected result for a test case.
9. A tax function that is never called anywhere in the program uses the wrong formula.
10. The login page shows the label "Pasword" to every user.
11. A developer copies a validation block, pastes it for a second field, and forgets to change the field name.
12. The configuration file points the production application at the test database.
13. A monthly report shows totals that do not match the invoices, but only when run on the last day of the month.
14. A database column is defined to hold 20 characters, while customer names can be up to 50 characters.
15. A software architect designs the system assuming all users are in a single time zone.
16. Searching for "cafe" with an accent ("café") returns zero results, although matching products exist.
17. During a code review, a colleague notices a variable that is used before it is assigned (before the program has ever been run).
18. A developer misunderstands the rounding rule for prices.
19. After a user requests a password reset, the email never arrives.
20. The requirements do not mention what happens after five failed login attempts, although the business wants accounts locked.

### Answer key (Part 1)

| # | Answer | Reasoning |
|---|---|---|
| 1 | **Error** | A human misunderstanding of the requirement |
| 2 | **Defect** | Flaw in code (boundary operator) |
| 3 | **Failure** | Observable wrong behavior of the running system |
| 4 | **Defect** | Contradiction is a flaw in a work product (the requirements document) |
| 5 | **Error** | A human's wrong assumption. The resulting wrong requirement would be the defect |
| 6 | **Failure** | Observable misbehavior |
| 7 | **Defect** | Flaw in a work product (the test case). Defects are not only in code |
| 8 | **Error** | Human slip while writing the test case |
| 9 | **Defect** | A flaw exists, but it never causes a failure because the code is never executed |
| 10 | **Failure** | The user observes the wrong label. The defect is the misspelled text in the source or resource file |
| 11 | **Error** | Human mistake (copy-paste oversight). The wrong field name in code would be the defect |
| 12 | **Defect** | Flaw in a work product (configuration). A failure may follow once it is used |
| 13 | **Failure** | Observable wrong result, visible only under specific conditions (last day of month) |
| 14 | **Defect** | Flaw in the data design that does not meet the requirement |
| 15 | **Error** | A human design assumption. The resulting design flaw would be the defect |
| 16 | **Failure** | Observable deviation in behavior |
| 17 | **Defect** | Found by review (static testing) without executing the code, so no failure was ever seen |
| 18 | **Error** | A human misunderstanding of a rule |
| 19 | **Failure** | Observable: the expected email does not arrive. Cause is unknown: code defect, mail server, configuration, or spam filter |
| 20 | **Defect** | An omission (missing requirement) is a flaw in the requirements work product |

Count how many you got right: 18 to 20 is excellent; 14 to 17 is solid; fewer than 14, re-read sections 2 and 3 and try again. Note that some items (5, 10, 11, 15, 19) contain a second layer. Those are good discussion points for tomorrow's session.

### Part 2: Trace five scenarios through the full chain

For each scenario, name the **error**, the **defect**, and the **failure**. Then check the sample answer.

**Scenario A.** A product owner writes "Users get free shipping on orders of 50 dollars or more," but the developer implements `if total > 50: shipping = 0`. A customer with a 50.00 order is charged shipping.

**Scenario B.** A developer on a tight deadline skips input validation for the "quantity" field. A user types -5 and the app creates an order with a negative total, refunding money.

**Scenario C.** A requirements document does not state that usernames must be unique. The developer builds the registration form without a uniqueness check. Two users register with the same username, and later one sees the other's messages.

**Scenario D.** A team member sets the release build to use the test payment gateway key because the instructions were passed on verbally and misunderstood. Real customers' payments appear to succeed but no money is ever collected.

**Scenario E.** A developer believes a library function `round()` always rounds halves up. Python's `round()` rounds halves to the nearest even number, so `round(2.5)` gives 2. A price display shows 2 instead of 3 for a value of 2.5.

#### Sample answers (Part 2)

| Scenario | Error | Defect | Failure |
|---|---|---|---|
| **A** | Developer misreads "50 or more" as "over 50" | `>` instead of `>=` in the shipping check | Customer with exactly 50.00 is charged shipping |
| **B** | Under time pressure the developer decides to skip the validation (a deliberate shortcut, still a human mistake in judgment) | Missing check on the quantity field | Negative total creates a refund |
| **C** | Requirement author omits the uniqueness rule (an incomplete-requirement error), and the developer does not question it | Requirement omission, then missing uniqueness check in code and database constraint | Two users share a username; one sees another's messages |
| **D** | Miscommunication of verbal instructions | Wrong gateway key in the release configuration | Real payments appear to succeed but money is never collected |
| **E** | Wrong assumption about how `round()` behaves | Use of `round()` where explicit half-up rounding is required (for example with Python's `decimal` module) | A displayed price of 2.5 appears as 2 |

Let us verify scenario E, since it is a real surprise to many beginners:

```python
print(round(2.5))   # 2
print(round(3.5))   # 4
print(round(0.5))   # 0
```

Output:

```
2
4
0
```

That is "banker's rounding": halves round to the nearest even number. It is documented behavior, not a bug in Python. The **error** is the developer's assumption; the **defect** is using that function where the requirement needs "round half up."

---

## Hands-On Python Mini-Lab: Find, Prove, and Fix a Defect

In this lab you will play the roles of tester and developer. You will observe a failure, write the failing check as a plain `assert`, locate the defect, and fix it.

You need Python 3 installed (3.8 or newer is fine). No extra libraries are required.

**The requirement for the lab:**

> *Orders of 50.00 or more ship free. Orders below 50.00 pay a flat shipping fee of 4.99.*

### Step 1: Create the buggy program

Create a file named `lab.py` and paste this code:

```python
"""Mini-lab: Shipping fee calculator.
Requirement: Orders of 50.00 or more ship free.
Orders below 50.00 pay a flat fee of 4.99.
"""

def shipping_fee(order_total):
    if order_total > 50:
        return 0.0
    return 4.99


def run_checks():
    cases = [
        (20.00, 4.99),
        (49.99, 4.99),
        (50.00, 0.0),
        (50.01, 0.0),
        (120.00, 0.0),
    ]
    failures = 0
    for total, expected in cases:
        actual = shipping_fee(total)
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{status}: shipping_fee({total}) expected {expected}, got {actual}")
    print(f"{len(cases) - failures} passed, {failures} failed")


if __name__ == "__main__":
    run_checks()
```

### Step 2: Run it and observe

Run:

```
python lab.py
```

Expected output:

```
PASS: shipping_fee(20.0) expected 4.99, got 4.99
PASS: shipping_fee(49.99) expected 4.99, got 4.99
FAIL: shipping_fee(50.0) expected 0.0, got 4.99
PASS: shipping_fee(50.01) expected 0.0, got 0.0
PASS: shipping_fee(120.0) expected 0.0, got 0.0
4 passed, 1 failed
```

Four inputs pass and one fails. What you just saw is a **failure**: the observable deviation for the input 50.00. Notice that the defect sat in the code for all five runs; only one input exposed it.

Pause and write down, in your own words, three things:

1. What input triggered the failure?
2. What did the requirement say should happen?
3. What did the program do instead?

### Step 3: Write the failing test as a plain assert

An `assert` statement checks that a condition is true. If it is false, Python stops and raises an `AssertionError`, optionally showing your message. It is the simplest possible automated check, and you do not need any testing framework.

Create a second file named `test_lab.py` **in the same folder**:

```python
from lab import shipping_fee

assert shipping_fee(50.00) == 0.0, "Orders of exactly 50.00 should ship free"
print("ok")
```

Run it:

```
python test_lab.py
```

Expected output (the file path and line number may differ on your computer):

```
Traceback (most recent call last):
  File "test_lab.py", line 3, in <module>
    assert shipping_fee(50.00) == 0.0, "Orders of exactly 50.00 should ship free"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Orders of exactly 50.00 should ship free
```

This failing check is a **reproducible test** for the failure. It is the code version of the "steps to reproduce" in a bug report. Keep it: after the fix it becomes your **retest** and a **regression check** for the future. (Automation frameworks such as the ones you will meet in later weeks make this much more convenient, but the idea is exactly this.)

### Step 4: Find the defect

Look at `shipping_fee`. Compare the requirement ("50.00 **or more** ships free") with the code (`order_total > 50`):

- The requirement says 50.00 itself ships free.
- The code only gives free shipping for values strictly greater than 50.

So the **defect** is the operator `>` on the comparison line. A likely **error** behind it: the developer read "over 50" instead of "50 or more," exactly like the discount story earlier.

### Step 5: Fix the defect

Change this line in `lab.py`:

```python
    if order_total > 50:
```

to:

```python
    if order_total >= 50:
```

### Step 6: Retest

Run the assert again:

```
python test_lab.py
```

Expected output:

```
ok
```

Then run the full set of checks again:

```
python lab.py
```

Expected output:

```
PASS: shipping_fee(20.0) expected 4.99, got 4.99
PASS: shipping_fee(49.99) expected 4.99, got 4.99
PASS: shipping_fee(50.0) expected 0.0, got 0.0
PASS: shipping_fee(50.01) expected 0.0, got 0.0
PASS: shipping_fee(120.0) expected 0.0, got 0.0
5 passed, 0 failed
```

All five now pass. You followed the full cycle: observe failure, reproduce with a check, locate the defect, fix it, retest.

### Step 7: Reflect and extend

Answer these in your notes:

1. Which input exposed the failure, and why did the other four not?
2. If the tester had only tried 20.00 and 120.00, what kind of testing mistake (false negative) would have happened?
3. Write a bug report for the failure (use the template from the Project 1 login example). Which fields describe the failure and which would the developer add after finding the defect?
4. What could the team do to **prevent** this type of error? (Hint: think about requirement wording such as "at least," a team checklist, or a review habit.)
5. **Stretch:** add two more assert checks for the lower side of the boundary, `shipping_fee(49.99) == 4.99` and `shipping_fee(0) == 4.99`, and confirm they pass. Why is it valuable to test on both sides of a boundary?

---

## Common Misconceptions

| Misconception | Reality |
|---|---|
| "A defect and a failure are the same thing." | A defect is a flaw in a work product. A failure is the observed misbehavior when it runs. One causes the other, but they are different. |
| "If the code has a defect, the software will fail." | Only if the defect is executed under conditions that expose it. Many defects stay hidden for years. |
| "If all my tests pass, there are no defects." | Passing tests show only that those checks did not find a failure. Defects can still exist (a false negative situation). |
| "Every failure means there is a defect in the code." | Failures can come from environment, data, hardware, misuse, or an unsupported platform. |
| "Defects only exist in code." | Defects can exist in requirements, designs, test cases, documents, configuration, and data. |
| "Testers find defects." | Testers observe failures (dynamic testing) and also find defects directly through reviews and static analysis. Developers diagnose the failure to locate the defect. |
| "An error and a bug are the same." | The error is the human mistake; the bug (defect) is its result in the work product. |
| "One bug report equals one defect." | Several reports can come from one defect (duplicates), and one report can reveal several defects. |
| "Calling something an error or defect decides who is to blame." | These terms describe what happened, not who is at fault. Good teams fix the process, not blame people. |
| "'Issue' in Jira always means a defect." | In Jira, an issue is any work item: story, task, epic, or bug. |
| "A false positive is a good result." | In testing, a false positive is a false alarm: the test reported a problem that does not exist. |
| "Low severity means we can ignore it." | Severity is impact. Priority decides timing. A low-severity problem can still be high priority. |

---

## Knowledge Check

Answer the questions, then compare with the answers below.

1. In one sentence each, define error, defect, and failure.
2. Which two terms are formal synonyms of "defect," and which term is a formal synonym of "error"?
3. A developer misreads a requirement and writes `if score > 60` instead of `if score >= 60` for a pass mark. Identify the error, the defect, and the failure (and describe the input that triggers it).
4. Why might a defect never cause a failure? Give two reasons.
5. Give two examples of failures that are not caused by defects in the application code.
6. What is the difference between a false positive and a false negative in testing? Give an example of each.
7. Explain how one error can result in many defects, and how one defect can result in many failures.
8. Name five places where errors can originate and give one example for each.
9. In which SDLC phase is it generally cheapest to fix a defect, and why does cost tend to rise as time passes?
10. Which parts of a bug report describe the failure, and which part does the developer typically work out afterwards?
11. A module has 30 KLOC. Reviews and testing found 54 defects. After release, 6 more defects were found. Calculate defect density and DRE.
12. Is "defect prevention" more closely related to QA or QC? Explain.
13. A tester reports that login fails, but it turns out the test database was empty. Which lifecycle outcome is likely, and is this a false positive or a false negative?
14. Classify: (a) A requirement is missing a rule about refunds. (b) A customer is charged twice. (c) The architect forgets about mobile screens when designing the layout.
15. Severity vs. priority: give an example of a defect with low severity but high priority.

### Answers

1. **Error:** a human action or mistake that produces an incorrect result. **Defect:** a flaw in a work product (code, document, data, configuration) that means it does not meet its requirements. **Failure:** an observable deviation of the running system from required or expected behavior.
2. **Fault** and **bug** are synonyms of defect (bug being informal). **Mistake** is a synonym of error.
3. **Error:** the developer misunderstood "60 or above" as "above 60." **Defect:** the `>` operator in the code. **Failure:** a student with exactly 60 is shown as failing. The triggering input is exactly 60.
4. Any two of: the defect is in dead code that can never run; it is in a rarely executed path that is not triggered yet; it is in an unused feature or document; it is masked by another defect that cancels its effect.
5. Any two of: hardware or radiation effects; wrong environment configuration; bad or missing test data; user misuse; outdated or unsupported browser; third-party service outage.
6. A **false positive** is a reported failure when there is no defect (for example, a test fails because the test server was down). A **false negative** is a missed defect: the test shows no problem although a defect exists (for example, only testing 250 and not the boundary of 100).
7. One misunderstanding can be repeated in several places (cart, invoice, email), producing several defects. One defect in shared code can be triggered by many users, pages, or channels, producing many failures.
8. Any five of: requirements (ambiguous statement), design (single time zone assumption), code (wrong operator), data (column too short), process (skipped code review), communication (lost information between teams), tooling (misconfigured build tool), assumptions (everyone has a phone), time pressure (skipped checks), lack of skill or knowledge.
9. Requirements, because only text needs changing and little else depends on it. Later, more design, code, tests, documents, and users depend on the flaw, so rework is bigger and customer harm may occur.
10. The title, steps to reproduce, environment, expected and actual results, and attachments describe the failure. The developer works out the defect (location of the flaw) and, through root-cause analysis, the error.
11. Total defects = 54 + 6 = 60. Defect density = 60 / 30 = **2 defects per KLOC**. DRE = 54 / 60 = **90%**.
12. Mostly **QA**, because it improves how work is done (process) to stop errors from becoming defects. Detection is closer to QC.
13. Likely **Rejected / Not a defect** (or closed as an environment issue). It is a **false positive**.
14. (a) **Defect** (omission in a requirements document). (b) **Failure** (observable behavior). (c) **Error** (a human design assumption or oversight); the missing mobile layout in the design would be the resulting defect.
15. A misspelled company name on the home page the day before a launch: low impact on function, but must be fixed urgently.

---

## Key Takeaways

- **Error -> Defect -> Failure** is a chain of cause and effect: a human mistake leads to a flaw in a work product, which, when executed under the right conditions, leads to an observable wrong behavior.
- **Mistake = error. Fault = bug = defect.** Failure is formally distinct. **Anomaly** and **incident** are neutral words for "something looks wrong," and a Jira **issue** is simply any work item.
- A defect becomes a failure only when specific inputs or conditions execute it. That is why boundary values and varied inputs matter, and why one passing example proves very little.
- Some defects never cause failures, and some failures have no code defect (environment, data, hardware, misuse, unsupported platforms). Check your environment and data before you report.
- **False positives** are false alarms; **false negatives** are missed defects.
- One error can create many defects, and one defect can cause many failures, so count defects and failures separately and look for siblings when you fix something.
- Errors come from requirements, design, code, data, process, communication, tooling, assumptions, time pressure, and skills gaps. Use "5 Whys" to find root causes and improve the system, not to blame people.
- Defects are injected at every phase, and the later they are found, the costlier they are to fix. Shift quality activities left.
- In the lifecycle: the tester observes and reports the **failure**; the developer finds and fixes the **defect**; the team learns from the **error**.
- **Defect density** and **DRE** are useful but limited measures. Use them to understand and improve, not to judge individuals.
- Prevention (QA-style) and detection (QC-style) work together.
- Be ready for tomorrow: test design techniques will give you systematic ways to choose the inputs that reveal hidden defects, and the next-but-one lesson covers testing principles, which explain why defects cluster and why repeating the same tests loses power.

---

## Additional Resources

- **ISTQB Glossary** (official definitions of error, defect, failure, anomaly, incident, and more): https://glossary.istqb.org/
- **Guru99, "Difference Between Bug, Defect, Error, Fault & Failure"** (a beginner-friendly article on the same vocabulary): https://www.guru99.com/
 (search for "bug vs defect vs error vs failure" on the site)
- **Atlassian, "Bug tracking" guides** (practical advice on writing and managing bugs in Jira): https://www.atlassian.com/software/jira/guides
