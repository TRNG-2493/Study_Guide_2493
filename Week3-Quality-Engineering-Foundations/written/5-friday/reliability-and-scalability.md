# Reliability and Scalability

**Week 3, Friday: Advanced Testing Concepts | Quality Engineering Foundations**

---

## Learning Objectives

By the end of this lesson you will be able to:

1. Define reliability and explain the four ISO 25010 reliability sub-characteristics (maturity, availability, fault tolerance, recoverability).
2. Distinguish reliability, availability, durability, resilience, robustness and maintainability.
3. Calculate MTBF, MTTR, MTTF, failure rate and availability, and convert "the nines" into allowed downtime per year, month and day.
4. Explain SLI, SLO, SLA, error budgets, RTO and RPO in plain language.
5. Describe the main types of reliability testing: fault injection, recovery, failover, backup and restore, soak, and chaos experiments.
6. Name eight resilience patterns (timeouts, retries with backoff, circuit breaker, bulkhead, graceful degradation, idempotency, health checks, redundancy) and write a test idea for each.
7. Recognise common failure modes: single point of failure, cascading failure, thundering herd, partial failure, data corruption and resource exhaustion.
8. Design reliability test scenarios for Project 1 (User Registration and Login) with clear expected behaviours.
9. Define scalability and compare vertical and horizontal scaling, elasticity, statelessness, load balancers, caching, CDNs, database scaling and queues.
10. Design a scalability test, calculate scaling efficiency, explain Amdahl's law in simple terms, and do basic capacity planning.
11. Run and read a safe Python demonstration of availability maths, a retry plus circuit-breaker toy, and a toy scalability model.
12. Pull the week together into the Project 1 test-design document and regression and risk plan.

---

## Why This Matters

Imagine you build a beautiful registration and login page. Every test case you wrote this week passes. The password rule works, the boundary values are correct, the state transitions behave. You release it.

On Monday morning the database server restarts for a routine update. For six minutes nobody can log in. The page shows a blank screen and a raw error message. Worse, three people who were halfway through registering now have half-created accounts that block them from trying again. At 9 a.m. a marketing email goes out, ten times the usual number of visitors arrive, and the single server that runs your app slows to a crawl.

None of those problems are "the feature is wrong". The feature is right. The problems are about **what happens when things go wrong** (reliability) and **what happens when things grow** (scalability).

Earlier today you learned how to measure speed and load: load, stress, spike and soak tests, percentiles, throughput, and bottlenecks. That lesson asked "how fast, and how much can it take?" This lesson asks two related but different questions:

- **Reliability:** Does the system keep working, and recover quickly and safely, when parts of it fail?
- **Scalability:** When demand grows, can we add resources and get a proportional gain, and at what cost?

Real users and real businesses care about both. Industry experience shows that users abandon services that fail often, and that outages cost money, trust and sometimes safety. As a Quality Engineer you are the person who asks the uncomfortable questions early: "What if the database goes away? What if we get ten times the traffic? How will we know?" This lesson gives you the vocabulary, the formulas and the test ideas to ask them well. It also finishes the week, so at the end we connect everything to your Project 1 deliverable.

---

## The Concept

We will take this in two parts. **Part A** covers reliability. **Part B** covers scalability. Then we run a Python demonstration, look at AI's role, review common mistakes, and finish with a sample plan, exercises, a knowledge check and the week wrap-up.

A friendly analogy to keep in mind throughout:

> **The hospital and the restaurant.**
> A hospital has a **backup generator**. When mains power fails, the generator starts and the operating theatre keeps its lights on. That is **reliability and resilience**: the service keeps going when something breaks.
> A restaurant becomes popular. At first it adds a few more tables (bigger room: **vertical scaling**, up to the walls). Then it opens a second kitchen and a second dining room in a nearby street (**horizontal scaling**). That is **scalability**: handling growth by adding resources. But if both kitchens must share one tiny cashier till, the till becomes the **bottleneck**, and adding kitchens helps less and less. Hold on to that picture; it will come back.

---

# PART A: RELIABILITY

## A1. What is reliability?

**Reliability** is the probability that a system performs its required functions without failure, for a specified period of time, in a specified environment.

Let us unpack each phrase, because every part matters for testing:

- **Probability:** reliability is a likelihood, not a promise. "99% reliable over a day" means that out of many days, about 99 in 100 run without failure.
- **Required functions:** we must know what "working" means. For Project 1, "working" includes: a visitor can register, a registered user can log in, a wrong password is rejected correctly.
- **Failure-free operation:** the system does what it should, with no failure observed by users.
- **Specified time:** reliability is always tied to a period. A system reliable for one hour may not be reliable for one year.
- **Specified environment:** the same software behaves differently on a developer laptop, a test server and production under heavy load. We state the conditions.

Remember the words from Wednesday: an **error** (human mistake) can introduce a **defect** (fault in the code or configuration), which can cause a **failure** (visible wrong behaviour). Reliability is about how often failures happen and how the system copes. A reliable system is not one that never has defects; it is one that rarely lets defects or environmental problems become failures that users see, and that recovers quickly when they do.

## A2. ISO 25010 and the reliability sub-characteristics

**ISO/IEC 25010** is an international standard that describes a model of **software product quality**. You met it indirectly when we split functional from non-functional testing today. The model groups quality into a set of **characteristics** such as functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability and portability. (Newer editions refine some names and add safety, so always check the current edition on iso.org.)

**Reliability** is one of those characteristics, and it has four sub-characteristics:

| Sub-characteristic | Plain meaning | Project 1 example | Example test |
|---|---|---|---|
| **Maturity** | How well the system avoids failures during normal operation, as defects are found and fixed over time | The login runs 10,000 normal logins with no unexpected errors | Run the regression suite and a long normal-usage run; count failures per hour |
| **Availability** | The degree to which the system is operational and accessible when needed | Users can reach the login page 24/7 | Monitor uptime; measure successful requests vs total |
| **Fault tolerance** | The system keeps operating as intended despite hardware or software faults | If one app server dies, logins continue on another | Kill one server while a login test runs |
| **Recoverability** | After an interruption or failure, the system can recover affected data and return to the desired state, and how quickly | After a database crash, restarted service has all committed accounts | Crash the database, time the recovery, verify data |

Note for the curious: the 2023 edition of the standard renames "maturity" to "faultlessness". The idea is the same: the system avoids faults in normal operation. We will use the four classic names because they are widely used in industry material.

## A3. Related terms: do not mix them up

These words are used loosely in meetings, so learn the differences. A table is the clearest way:

| Term | Simple definition | Question it answers | Hospital analogy | Project 1 example |
|---|---|---|---|---|
| **Reliability** | Works correctly without failure over a given time in a given environment | "How often does it fail?" | The operating theatre equipment rarely breaks | Login works correctly day after day |
| **Availability** | The fraction of time the system is up and usable | "Is it there when I need it?" | The theatre is open and usable 99.9% of the time | Login page reachable 99.9% of the month |
| **Durability** | Once data is saved, it stays saved (not lost or corrupted), even after crashes | "Will my data survive?" | Patient records are never lost, even in a fire (copies elsewhere) | A newly registered account still exists after a restart |
| **Resilience** | Ability to absorb a disruption, adapt and return to normal | "How well does it bounce back?" | When power fails, the generator and procedures keep care going | When the email service is down, registration still succeeds and the email is sent later |
| **Robustness** | Ability to handle invalid input or stressful conditions without crashing | "Does it break on odd input or heavy use?" | A monitor does not shut down because a nurse pressed buttons in the wrong order | A 5,000-character email address is rejected cleanly, not crashing the server |
| **Maintainability** | How easy it is to find, fix, change and test the system | "How quickly can we repair or improve it?" | Equipment designed so a technician can swap a part in minutes | Clear logs and modular code let a developer fix a login bug in an hour |

A few important relationships:

- A system can be **available but unreliable**: it is "up" 99.9% of the time, but while up it gives wrong answers or fails a lot of requests.
- A system can be **reliable but unavailable**: it never makes mistakes, but it is down for planned maintenance every Sunday for six hours.
- **Maintainability** feeds **availability** because it shortens repair time (MTTR, which we meet next).
- **Durability** is about data; a service can be up (available) and still have lost data (not durable). Both matter for registration, because a lost account is a serious defect.

## A4. Key reliability metrics, with formulas and worked examples

Numbers turn "it seems stable" into evidence. Here are the core metrics.

### Definitions

- **MTBF (Mean Time Between Failures):** the average time a **repairable** system runs between one failure and the next. Formula:

  `MTBF = total operating (up) time / number of failures`

- **MTTR (Mean Time To Repair or Recover):** the average time it takes to restore service after a failure, from the moment it fails until it works again. Formula:

  `MTTR = total repair (down) time / number of failures`

  Some teams define the "R" as Recovery, Restore, Repair or Respond. Always check which definition your team uses, because they measure slightly different stretches of the incident.

- **MTTF (Mean Time To Failure):** the average lifetime of a **non-repairable** item, which is thrown away when it fails (for example a light bulb or a one-use token generator). Formula:

  `MTTF = total operating time of all items / number of items`

- **Failure rate (lambda, written λ):** how many failures per unit of time. When failures are random and the rate is constant, `λ = 1 / MTBF`.

- **Availability:** the fraction of time the system is operational.

  `Availability = uptime / (uptime + downtime)`

  and, equivalently, using averages:

  `Availability = MTBF / (MTBF + MTTR)`

  Multiply by 100 to get a percentage.

### Worked example 1: MTBF, MTTR and availability from a log

A test server ran for **1,000 hours**. It failed **4 times**. Total time spent down across those failures was **8 hours**.

- Uptime = 1,000 - 8 = **992 hours**
- MTBF = 992 / 4 = **248 hours**
- MTTR = 8 / 4 = **2 hours**
- Availability = 248 / (248 + 2) = 248 / 250 = **0.992 = 99.2%**
- Check with the first formula: 992 / 1,000 = 0.992 = 99.2%. The two formulas agree.
- Failure rate λ = 1 / 248 = about **0.00403 failures per hour** (about 0.4% per hour).

### Worked example 2: MTTF

Five identical single-use hardware tokens last 800, 1,000, 1,200, 900 and 1,100 hours before failing. The total is 5,000 hours. MTTF = 5,000 / 5 = **1,000 hours**.

### Worked example 3: probability of surviving a period

If failures are random with a constant rate (a common simplification), the probability of **no failure** in time *t* is:

`R(t) = e^(-λ × t)`

For the example 1 system with λ = 1/248 per hour and t = 24 hours: λ × t = 24 / 248 = 0.0968. `e^(-0.0968)` is about **0.908**. So there is roughly a **90.8% chance** of a failure-free day. That might sound fine until you realise it means about one day in eleven contains a failure. Reliability must always be read with its time window.

### Worked example 4: which improvement helps more, fewer failures or faster repair?

Start with MTBF = 500 hours and MTTR = 2 hours: availability = 500 / 502 = **99.602%** (our Python demo prints exactly this).

- Cut repair time to 0.5 hours (better monitoring, automated restart, a runbook): 500 / 500.5 = **99.900%**.
- Double MTBF to 1,000 hours but leave MTTR at 2: 1,000 / 1,002 = **99.800%**.

Making recovery four times faster beat making failures half as frequent. This is why modern teams invest so heavily in monitoring, automation and rehearsed recovery: failures will happen, so **fast recovery** is often the cheapest way to raise availability.

### Worked example 5: components in series and in parallel

If login needs **both** a web server (99.9% available) and a database (99.9% available) to work, they are **in series**. Both must be up, so (assuming independent failures):

`0.999 × 0.999 = 0.998001`, about **99.8%**.

Every extra required component lowers overall availability.

If instead you have **two redundant** servers, each 99% available, and either one is enough, they are **in parallel**. The system is down only when **both** are down: `0.01 × 0.01 = 0.0001`. Availability = 1 - 0.0001 = **99.99%**. Redundancy, in other words, is a powerful tool. (Real failures are not always independent: if both servers share one power supply or one bad configuration, they fail together, which is exactly why testers check for hidden shared dependencies.)

## A5. "The nines": translating availability into downtime

Teams talk about availability as "three nines" (99.9%), "four nines" (99.99%) and so on. Each extra nine cuts the allowed downtime by a factor of ten. The calculation is simple:

`allowed downtime = period × (1 - availability)`

We use a **365-day year** (525,600 minutes) and a **30-day month** (43,200 minutes). A day has 1,440 minutes or 86,400 seconds.

| Availability | Nickname | Per year | Per 30-day month | Per day |
|---|---|---|---|---|
| 99% | two nines | 3.65 days (87.6 hours) | 7.2 hours (432 minutes) | 14.4 minutes |
| 99.9% | three nines | 8.76 hours (525.6 minutes) | 43.2 minutes | 86.4 seconds |
| 99.99% | four nines | 52.56 minutes | 4.32 minutes (259.2 seconds) | 8.64 seconds |
| 99.999% | five nines | 5.256 minutes (315.36 seconds, about 5 min 15 s) | 25.92 seconds | 0.864 seconds |

Spot-check one row together. For 99.9% per year: 525,600 × 0.001 = 525.6 minutes; 525.6 / 60 = 8.76 hours. Correct. For 99.99% per month: 43,200 × 0.0001 = 4.32 minutes; 4.32 × 60 = 259.2 seconds. Correct.

Why testers care: at five nines a single slow deployment or one two-minute database failover can use up the whole year's allowance. And each nine costs much more to achieve than the last. Most business web apps sensibly aim for three or four nines, not five. "Maximum possible" is rarely the right target; "right for the business" is.

## A6. SLI, SLO, SLA, and error budgets

These three acronyms come from the Site Reliability Engineering (SRE) world, popularised by Google's SRE books (links at the end). At name level:

| Term | Stands for | Meaning | Example for Project 1 |
|---|---|---|---|
| **SLI** | Service Level Indicator | A **measurement** of how the service is behaving | "Percentage of login requests that succeed in under 500 ms" |
| **SLO** | Service Level Objective | An internal **target** for an SLI | "99.9% of login requests succeed within 500 ms over 30 days" |
| **SLA** | Service Level Agreement | A **contract** with customers, often with penalties (refunds) if missed | "We guarantee 99.5% monthly availability or you receive a service credit" |

A helpful way to remember it: the SLI is the **thermometer reading**, the SLO is the **temperature we aim for**, the SLA is the **written promise with consequences**. Teams usually set the SLO tighter than the SLA, so they have warning before they break the contract.

### Error budget

An **error budget** is the amount of unreliability the SLO allows. If the SLO is 99.9% over 30 days, the budget is the remaining 0.1%: **43.2 minutes** of bad time in that month.

Example: this month you already had a 30-minute outage. You have used 30 / 43.2 = about **69.4%** of the budget and have **13.2 minutes** left. The team might decide to postpone risky releases until next month. The budget turns an argument ("is it stable enough to release?") into a shared number. As a tester, the budget also helps prioritise: a defect that burns budget fast is more urgent than one that does not.

## A7. RTO and RPO: planning for disaster

Two terms from disaster recovery and business continuity:

- **RTO (Recovery Time Objective):** the **maximum acceptable time** the service can be down after a disaster. "We must be back within 30 minutes."
- **RPO (Recovery Point Objective):** the **maximum acceptable amount of data loss**, measured in time. "We can lose at most the last 5 minutes of data."

```
 Time ---->
 [last good backup]----[data you can lose = RPO]----[DISASTER]----[downtime = RTO]----[service restored]
        02:00                                           15:00                              15:30
```

Worked example: backups run nightly at 02:00. A crash happens at 15:00. Everything registered since 02:00 is lost: **13 hours** of data. If the business RPO is **1 hour**, nightly backups do not meet it. You would need hourly backups or continuous replication. If restoring takes **45 minutes** and the RTO is **30 minutes**, the restore process also fails the objective. Both are testable: **you do a restore drill and time it**, and you compare the data you recover against what you expected. That is a core reliability test, which we meet below.

## A8. Types of reliability testing

Reliability testing is a family of tests, not one test. Each answers a different question.

| Type | What it does | Question answered | Link to earlier lessons |
|---|---|---|---|
| **Feature and regression reliability** | Runs the functional and regression suites repeatedly and over time, tracking pass rates and flaky (sometimes-failing) tests | "Do the features work consistently, release after release?" | Today's regression lesson; Wednesday's principles (defect clustering) |
| **Load-based reliability** | Applies expected and peak load and watches for errors, timeouts and failures, not just speed | "Does it keep working correctly under normal and busy conditions?" | Load testing from the performance lesson |
| **Soak (endurance) testing** | Runs normal load for hours or days | "Does it degrade over time from leaks or growing queues?" | Soak tests in the performance lesson |
| **Fault injection / failure testing** | Deliberately introduces faults (kill a process, drop packets, return errors) | "How does it behave when parts fail?" | New here |
| **Recovery testing** | Forces a failure and checks the system recovers (data, state, time) | "Does it come back correctly, and how fast?" | Measures MTTR, RTO |
| **Failover testing** | Fails the primary component to check that a standby takes over | "Does the backup actually take over?" | Redundancy, availability |
| **Backup and restore testing** | Restores backups into a clean environment and verifies the data | "Can we really get our data back?" | Measures RPO, RTO |
| **Chaos engineering** | Runs controlled experiments on the system, often in production, to find weaknesses before they cause outages | "What unexpected failures will bite us?" | Mindset from Wednesday: "what could go wrong?" |

### Fault injection

**Fault injection** means deliberately causing a failure to see how the system reacts. The faults can be simple: stop a service, block a network port, return HTTP 500 from a stub, fill a disk, slow a dependency down. It is like a fire drill: you do not wait for a real fire to find out whether the exits are blocked. Always do it in a **safe, controlled environment** that you own, with a plan to undo the fault.

### Recovery and failover testing

**Recovery testing** checks the return to normal after a failure: Is data intact? Is the service up? How long did it take (that is your measured MTTR)? **Failover testing** is a special case where a redundant component takes over automatically. A hospital generator that has never been started in a drill is a risk, because the first time you discover it does not start is during a real blackout. Failover that has never been tested is similarly unproven.

### Backup and restore testing

There is an old saying in operations: "A backup that has never been restored is only a hope." Test that backups run, are complete and can be restored, that the restored data is consistent (for example, the number of users matches, passwords still verify) and that the time taken meets RTO and RPO.

### Chaos engineering

**Chaos engineering** is the discipline of experimenting on a system to build confidence that it can withstand turbulent conditions. The best-known example is **Netflix's Chaos Monkey**, a tool that randomly terminates virtual machine instances in their production environment during business hours. The point was not to cause harm, but to make sure engineers built services that survive the loss of any single instance, because it would happen routinely. Netflix later grew this into a wider set of tools and the community published the **Principles of Chaos Engineering** (see the links at the end). The idea in the principles, in brief:

1. Start by defining the **steady state**, a measurable output that shows the system is healthy (for example, successful logins per minute).
2. Form a **hypothesis**: "the steady state will continue when we kill one app server".
3. Introduce **real-world events**: server crashes, network problems, traffic surges.
4. Run the experiment, ideally where real traffic exists, but **minimise the blast radius** (the portion of users or systems that could be harmed).
5. **Automate** experiments to run continuously, and learn from results.

For you as a beginner: chaos engineering is the scientific cousin of the exploratory testing you studied earlier today. You do not run it on a real production system on day one. You begin in a test environment with a clear hypothesis and a rollback plan.

## A9. Resilience patterns testers should know

Developers build **resilience patterns**: standard designs that help a system cope with failure. Testers do not need to implement them, but you must know their names, understand what they promise, and verify they actually work. Each has a one-line meaning and a test idea.

| Pattern | One-line meaning | Test idea (Project 1) |
|---|---|---|
| **Timeout** | Stop waiting for a slow dependency after a fixed time, instead of waiting forever | Make the email service respond after 30 seconds. Expect the registration call to give up at the configured timeout (for example 3 seconds) and respond cleanly |
| **Retry with backoff** | Try a failed call again, waiting longer each time (for example 1 s, 2 s, 4 s), often with random "jitter" | Fail the dependency twice then succeed. Expect 3 attempts with increasing gaps and one final success. Also make it fail permanently and confirm retries stop after the maximum |
| **Circuit breaker** | After repeated failures, "open the circuit" and fail fast for a while rather than hammering a broken dependency, then test with a trial call | Break the dependency, send repeated requests, check that after N failures requests are rejected instantly; restore it and check the circuit closes again |
| **Bulkhead** | Isolate resources so a failure in one area cannot sink everything (like watertight compartments in a ship) | Slow down the "forgot password" feature and confirm login still responds, because they use separate thread or connection pools |
| **Graceful degradation** | When a non-essential part fails, the core function continues with reduced features | Disable the "recent activity" widget service. Login must still work, with the widget hidden or showing a friendly message |
| **Idempotency** | Doing the same operation twice has the same effect as once, so safe retries do not duplicate things | Submit the identical registration request twice (or double-click). Expect one account, not two, and a consistent response |
| **Health check** | An endpoint or probe that reports whether a service is healthy, so load balancers and orchestrators can route around unhealthy instances | Stop the database. Expect the health endpoint to report unhealthy (not "OK"), and traffic to stop going to that instance |
| **Redundancy** | Keep spare copies of components so one failing does not stop the service | Kill one of two app servers during a login test. Expect no failed logins beyond a brief blip, and alerts firing |

### A closer look at two patterns

**Retry with backoff.** Imagine knocking on a door. If nobody answers, you do not knock 100 times in one second. You wait a bit, knock again, wait longer, knock again. If every client retries immediately at the same moment, they can make a struggling service worse (see "thundering herd" below). Backoff spreads retries over time; **jitter** adds a small random offset so clients do not all retry on the same beat. Testers check: Is there a maximum number of attempts? Do the waits grow? Are only safe, idempotent operations retried?

**Circuit breaker.** The name comes from the electrical breaker in your home: when the current is dangerous the breaker "trips" and cuts the circuit instead of letting the wiring burn. In software it has three states:

```
          failures >= threshold
   +--------+ ------------------> +--------+
   | CLOSED |                     |  OPEN  |  (fail fast, no calls to dependency)
   | normal |                     +--------+
   +--------+                          |
        ^                              | after reset timeout
        |                              v
        |        trial call ok    +-----------+
        +------------------------ | HALF-OPEN |
          (trial call fails: ---> | one probe |
           go back to OPEN)       +-----------+
```

You will see this behaviour run in the Python demo later in this lesson.

## A10. Failure modes to look for

A **failure mode** is a way in which something can fail. Knowing the common ones helps you imagine test scenarios (this connects with the "what could go wrong" mindset from Wednesday).

| Failure mode | Meaning | Example | What to test |
|---|---|---|---|
| **Single point of failure (SPOF)** | One component whose failure stops the whole system | One database server, one load balancer, one DNS entry, one person who knows the password | Identify every component; ask "if this died, what happens?" and then actually test it |
| **Cascading failure** | One failure triggers others in a chain | Slow database makes app threads pile up, the app slows, retries multiply load, the database falls over completely | Slow a dependency and watch whether the failure spreads; check timeouts, bulkheads and breakers stop the chain |
| **Thundering herd** | Many clients act at the same moment, often after an outage ends or a cache expires, overwhelming a service | After a 5-minute outage, 50,000 users' apps all retry at the same second | Simulate a mass reconnect or a cache flush; check backoff and jitter, rate limiting |
| **Partial failure** | Some parts or some requests fail while others work | 1 of 5 servers is bad: one request in five fails | Look for intermittent errors; check the load balancer removes bad instances |
| **Data corruption** | Data becomes wrong or inconsistent | A crash mid-write leaves a half-created user; two systems disagree | Interrupt writes; verify integrity, constraints and transactions; check restore results |
| **Resource exhaustion** | Running out of memory, disk, file handles, connections or threads | A **memory leak** (memory is allocated and never released) slowly kills the server after three days | Soak tests; fill the disk; open many connections; monitor memory trends |

**Memory leak** in simple words: the program keeps borrowing memory and never giving it back. It works fine for hours, then slows and crashes. Only long-duration runs reveal it, which is why soak testing exists.

## A11. Designing reliability test scenarios for Project 1

Here is a set of **fault scenarios** for Project 1 (User Registration and Login). The good habit is to write each as: **Scenario, how to inject it, expected behaviour, and what to verify afterwards**. Do these only in a test environment you own and control.

| # | Scenario | How to inject (test environment) | Expected behaviour | Verify afterwards |
|---|---|---|---|---|
| 1 | **Kill a service** (authentication or app process) during login | Stop the process mid-test; then restart it | Users see a friendly "service temporarily unavailable, please try again" message, not a stack trace or blank page. After restart, logins work again, without manual repair | Time to recover (MTTR); no corrupted sessions; alert was raised |
| 2 | **Drop the network** to the email provider during registration | Block the outbound port or point to a black-hole address | Account creation either completes with the verification email queued for later, or fails with a clear message and no half-created account. The page does not hang | No duplicate or orphan accounts; queued emails sent when the network returns |
| 3 | **Fill the disk** where logs or uploads are stored | Create a large dummy file until the volume is nearly full | Core login keeps working or fails safely; alerts fire before 100%; no data corruption | Disk alert triggered; no truncated database files; recovery after space is freed |
| 4 | **Slow dependency** (database or password-hash service answering in 5+ seconds) | Add artificial latency with a proxy or a stub | Requests time out at the configured limit and return a clear error; threads do not pile up; other features stay responsive | Response times; thread or connection counts return to normal; no cascading slowdown |
| 5 | **Restart during a write** (kill the app while a registration is being saved) | Kill the process between "submit" and "confirmation" | No half-created user. The database transaction either committed fully or rolled back. The user can retry and succeed with the same email | Count of accounts, unique email constraint intact, retry is idempotent |
| 6 | **Expired TLS certificate** | Install an expired certificate in the test environment | The failure is detected quickly by monitoring; clients see a clear security warning; the team has a renewal runbook | Alert time; certificate renewal procedure tested |
| 7 | **Clock skew** (server clocks disagree by minutes) | Shift one server's clock in a test environment | Session and token expiry still behave sensibly; verification links are not wrongly rejected or accepted; logs still orderable | No premature logout; no accepted-expired tokens; log timestamps consistent |
| 8 | **Database failover** | Stop the primary database; a standby should be promoted | Brief interruption within the RTO; no committed data lost within the RPO | Account count before and after; time to restore service |
| 9 | **Backup and restore** | Restore last night's backup into a clean environment | All accounts present up to the backup time; users can log in with their passwords | Restore duration vs RTO; data age vs RPO |

Notice the pattern in the "expected behaviour" column: **no crashes with raw errors, no lost or duplicated data, clear messages, fast recovery, and visible alerts.** Those five ideas are a reusable template for any reliability test.

## A12. Reliability growth and defect trends (introduction)

**Reliability growth** is the idea that, as testing finds and developers fix defects, the software's failure rate falls and its MTBF rises. You can see it in data.

Track the number of failures found per week of testing:

| Week | Failures found | Cumulative |
|---|---|---|
| 1 | 24 | 24 |
| 2 | 17 | 41 |
| 3 | 11 | 52 |
| 4 | 6 | 58 |
| 5 | 3 | 61 |
| 6 | 2 | 63 |

The weekly count is dropping and the cumulative line is flattening. That is a sign of growing maturity, though it is not proof that no defects remain (remember the principle that testing shows the presence of defects, not their absence). If the trend suddenly **rises again**, something changed: a new feature, a risky refactor or an environment problem. Connect this to what you learned about defect metrics on Tuesday: defect density, discovery rate and defect age all help judge release readiness.

For hardware, engineers often describe the **bathtub curve**: failure rates are high early on ("infant mortality"), low during the useful life, then rise again as parts wear out. Software does not physically wear out, but it shows a similar early-life spike after each release (new defects exposed to real use), then a calmer period. Remember it as: "watch the first days after every release more closely".

## A13. Monitoring, logging, alerting and observability for testers

You cannot fix or even prove what you cannot see. **Observability** is how well you can understand what is happening inside a system from the outside, using the data it produces. The three classic kinds of data (often called the three pillars) are:

| Signal | What it is | Example | Best for |
|---|---|---|---|
| **Logs** | Time-stamped text records of events | `2026-10-08 09:14:03 ERROR login failed user_id=482 reason=db_timeout` | Finding exactly what happened and why |
| **Metrics** | Numbers measured over time | Logins per second, error rate, CPU %, p95 latency | Spotting trends and triggering alerts |
| **Traces** | The path of one request through many services, with timing at each step | A login request: web (5 ms), auth service (20 ms), database (480 ms) | Finding which service is slow |

**Monitoring** watches known metrics and shows dashboards. **Alerting** notifies a human (or a system) when a metric crosses a threshold or an SLO is at risk. Google's SRE book describes four **golden signals** worth watching for any service: **latency** (how long requests take), **traffic** (how much demand), **errors** (how many requests fail) and **saturation** (how full the resources are). You already know the first three from the performance lesson. Saturation is "how close to the limit" (CPU, memory, connections).

Why testers need this:

- During a fault-injection test, the logs, metrics and traces tell you **what the system actually did**, not just what the screen showed.
- You can test the monitoring itself: "When I killed the service, did an alert fire within 2 minutes? Did it go to the right people? Did the message help?" **Alerts are part of the product's reliability.** An outage nobody noticed for an hour has a huge MTTR.
- Good bug reports include log excerpts and trace IDs, which makes defects faster to fix (your Tuesday defect-report skills at work).

### Reading an incident timeline

An **incident** is an event that disrupts or degrades a service. A **timeline** lists what happened in order. Learning to read one is valuable. Here is an example for Project 1:

```
09:00  Marketing email sent. Traffic starts rising.
09:05  Metric: login requests 3x normal.
09:08  Metric: database connections 95% of the limit (saturation).
09:10  Log: "ERROR timeout waiting for database connection" appears.
09:11  Metric: login error rate 18%. SLO breached.
09:14  ALERT fires: login error rate > 5%. (3 minutes after errors began)
09:16  On-call engineer acknowledges; checks dashboard.
09:25  Engineer increases the database connection limit (mitigation).
09:28  Error rate falls under 1%.
09:35  Incident declared resolved.
```

How to read it:

- **Time to detect (TTD):** errors began at 09:11 and the alert fired at 09:14: 3 minutes.
- **Time to respond:** the engineer acknowledged at 09:16.
- **Time to mitigate/recover:** service healthy again at 09:28. From failure start (09:10) to recovery (09:28) is **18 minutes of impact** (this feeds MTTR).
- **Contributing factors:** a traffic surge (spike) combined with a connection limit that was too low and no auto-scaling. A tester could have predicted this with a spike test and a saturation alert at 80%.
- Notice the **leading indicator** (database connections at 95%) appeared three minutes **before** user-visible errors. An alert on saturation would have bought time.

## A14. Incident postmortems (blameless)

A **postmortem** (also called an incident review or retrospective) is a written analysis after an incident. A **blameless** postmortem focuses on **what failed in the system and process**, not on who made a mistake. The reasoning: people make mistakes, so a system that depends on perfect humans is fragile. If people fear punishment they hide information, and the organisation stops learning. A blameless culture asks "how did our process let this happen?" rather than "whose fault was it?". Google's SRE book has a chapter on this (link at the end).

A simple template you can use for your own practice:

```
POSTMORTEM: <short title>
Date / Duration / Severity:
Author(s) / Status:

1. SUMMARY (2-3 sentences, plain language)
2. IMPACT (who/what affected, how many users, how long, SLO/error budget used)
3. TIMELINE (time-stamped list: start, detection, response, mitigation, resolution)
4. ROOT CAUSE(S) AND CONTRIBUTING FACTORS (use "5 Whys": keep asking why)
5. WHAT WENT WELL
6. WHAT WENT POORLY / WHERE WE GOT LUCKY
7. DETECTION: how did we find out? could we have found out sooner?
8. ACTION ITEMS (specific, owner, due date, type: prevent / detect / mitigate)
   e.g. "Add saturation alert at 80% DB connections - owner: A - due: next sprint"
   e.g. "Add spike test to the release checklist - owner: QE - due: next sprint"
9. LESSONS LEARNED
```

For a QE, the most important sections are **detection** and **action items**: every incident should leave behind at least one new test, one new alert or one new check.

---

# PART B: SCALABILITY

## B1. What is scalability?

**Scalability** is the ability of a system to handle **growth** (more users, more data, more transactions) by **adding resources**, and **how efficiently** it does so. There are two halves to this definition and both matter:

1. **Can it grow?** If traffic doubles, can we add servers, memory or other resources so it copes?
2. **How well does it grow?** If we double the servers, do we get double the capacity (ideal), or only 1.5 times (sub-linear), and what does it cost?

Restaurant analogy: your restaurant seats 40 people. On Saturday 80 arrive. Adding tables helps until the room is full. Adding a second restaurant helps further, but then you must manage two kitchens, share the menu and stock, and keep the customers from being confused. If both share a single cashier, doubling restaurants does not double throughput. **Scalability is about how much extra capacity each extra unit of resource really gives you.**

## B2. Vertical vs horizontal scaling

- **Vertical scaling (scale up):** make one machine bigger: more CPU, more memory, faster disk.
- **Horizontal scaling (scale out):** add more machines and share the work among them.

```
 VERTICAL (scale up)                     HORIZONTAL (scale out)

   +--------+      +------------+           +--------------+
   | Server |      |   BIGGER   |           | Load Balancer|
   | 4 CPU  | ---> |   SERVER   |           +------+-------+
   | 8 GB   |      |  16 CPU    |            /     |      \
   +--------+      |  64 GB     |       +-----+ +-----+ +-----+
                   +------------+       |Srv 1| |Srv 2| |Srv 3|
   One machine, bigger.                 +-----+ +-----+ +-----+
   Limit: the biggest machine           Many machines, shared work.
   you can buy.                         Limit: coordination and shared parts.
```

| Aspect | Vertical (scale up) | Horizontal (scale out) |
|---|---|---|
| How | Bigger machine | More machines |
| Restaurant | A bigger dining room | A second restaurant down the road |
| Pros | Simple: usually no code change; no need to share data between machines; easy to start | Can grow far beyond one machine; failure of one machine is tolerable (redundancy); can add and remove capacity gradually |
| Cons | Has a hard ceiling; expensive at the top end; a single point of failure; upgrade often needs downtime | More complex: needs load balancing, shared data design, stateless or well-managed state; harder to test and debug |
| Typical use | Databases (at first), small apps, quick fixes | Web and API servers, large-scale systems |
| Tester focus | Does performance really improve with bigger specs? Any restart downtime? | Does throughput grow with each machine? Is state shared correctly? Does the load balancer behave? |

Most real systems use **both**: scale up until it becomes costly, then scale out.

## B3. Elasticity and auto-scaling

- **Elasticity** is the ability to **automatically add and remove** resources to match demand, so you pay only for what you use. Think of a restaurant that rolls out extra tables for the Friday rush and puts them away on Monday.
- **Auto-scaling** is the mechanism that does it: a rule such as "if average CPU stays above 70% for 5 minutes, add one server; if it stays below 30%, remove one".

Scalability and elasticity are related but different. A system can be **scalable** (you *can* add servers by hand) without being **elastic** (it does so automatically). Testers check that scaling rules trigger at the right time, that new instances become healthy before receiving traffic, that scale-in does not drop active users' requests, and that there is an upper limit so a bug or attack does not create a huge bill.

## B4. Stateless vs stateful services

**State** is information a service remembers between requests. For example, after you log in, the server needs to remember that you are logged in. That memory is a **session**.

- A **stateful** service keeps that memory inside its own server. The next request must reach the **same** server.
- A **stateless** service keeps no memory of earlier requests inside the server. Each request carries what is needed, or the server looks it up from a shared place.

Why this matters: if Server 1 holds your session and the load balancer sends your next click to Server 2, you appear logged out. There are three common solutions at concept level:

1. **Sticky sessions:** the load balancer always sends a given user to the same server. Easy, but if that server dies, those users lose their session, and load can become uneven.
2. **Shared session store:** all servers store sessions in a shared fast store (like a dedicated session database or cache). Any server can serve any user. This is the standard way to make web servers stateless.
3. **Tokens held by the client:** the client carries a signed token proving who they are, so servers need no session memory.

```
 STATEFUL (sessions inside servers)        STATELESS (shared session store)

 User A --> [LB] --> Srv1 {A's session}     User A --> [LB] --> Srv1 --+
 User A --> [LB] --> Srv2 {??? no session}  User A --> [LB] --> Srv2 --+--> [Session Store]
   => "Why am I logged out?"                   => any server can serve any user
```

Statelessness helps scaling because servers become **interchangeable**: you can add or remove them freely, and one failing does not lose user context. For Project 1, an important test: log in, then make requests that land on different servers (or kill the server that served you), and confirm you stay logged in (if that is the design).

## B5. Load balancers, caching, CDNs, database scaling, and queues

These are the standard building blocks. At this stage you only need the **name, purpose and what to test**.

**Load balancer.** A component that spreads incoming requests across several servers and stops sending traffic to unhealthy ones (using health checks). Like a restaurant host who seats guests at whichever dining room has space. Test: distribution is reasonable, failed servers are removed, sessions work, the load balancer itself is not a single point of failure.

**Caching.** Storing the result of an expensive operation so the next request is answered faster without repeating the work. Like keeping popular dishes pre-prepared. Test: cache hit and miss behaviour, stale data (does the user see an outdated profile?), expiry and invalidation, behaviour when the cache is empty (a **cold cache** at startup, or after a flush, can cause a thundering herd on the database).

**CDN (Content Delivery Network).** A network of servers around the world that store copies of static content (images, scripts, styles) close to users. Like having local bakeries instead of shipping bread from one city. Test: static assets load from the CDN, updated files actually refresh, the site still works if the CDN is slow.

**Database scaling.** The database is often the hardest part to scale, because it holds shared state. Common ideas:

- **Indexing:** a lookup structure (like a book's index) that makes searches faster. Test: queries on large data (for example login by email) stay fast as the table grows.
- **Read replicas:** copies of the database that handle read requests, while one primary handles writes. Test: **replication lag**, where a replica is slightly behind. A user registers and immediately logs in; if the login reads from a lagging replica, "user not found" might appear. This is a classic bug.
- **Sharding:** splitting data across several databases (for example by user ID range or region). Test: data lands in the right shard, queries across shards work, and some shards are not much busier than others (a **hot shard**).

```
 Writes ---> [ Primary DB ] ---replicates--> [ Replica 1 ] <--- Reads
                             \-replicates--> [ Replica 2 ] <--- Reads

 SHARDING:  users A-M --> [DB Shard 1]      users N-Z --> [DB Shard 2]
```

**Queues and asynchronous processing.** Instead of doing slow work while the user waits, the system puts a job on a **queue** (a waiting line of tasks), and background **workers** process it. For Project 1, sending the verification email can be queued: the user sees "Registration received" immediately and the email follows. Queues smooth out spikes, because work piles up in the queue rather than overloading servers. Test: messages are not lost if a worker crashes, jobs are not processed twice (idempotency), queue length is monitored, and what happens if the queue grows without limit.

```
 [Web app] --> [ QUEUE: job job job job ] --> [Worker 1]
                                          --> [Worker 2] --> sends emails
```

## B6. Scalability testing in depth

### Goals

Scalability testing answers: **how does the system's performance change as we change load and resources, and where does scaling stop paying off?** Concretely:

- Find how much throughput each additional unit (server, instance, CPU core) really adds.
- Find the **limit** and the **bottleneck** that causes it.
- Verify that **auto-scaling and scale-in** work correctly.
- Provide data for **capacity planning** and **cost** decisions.

### Approach

Think of it as a staircase with two controlled variables:

1. Start with a **baseline**: 1 unit of resources (for example 1 server), measure maximum throughput at acceptable latency (for example p95 under 500 ms and errors under 1%). Use the load-testing approach from the performance lesson.
2. **Add resources step by step**: 2, then 4, then 8 servers. At each step **increase load** until you again reach the limit with acceptable latency.
3. **Record** throughput, latency percentiles, error rate and resource usage at each step.
4. **Compute** speedup and efficiency (below) and look for where it flattens.
5. **Investigate the bottleneck** when efficiency drops: database, shared lock, network, load balancer or a serial part of the code.
6. Where possible, also test **scaling down** and **elastic behaviour** (traffic rises, instances are added; traffic falls, instances are removed).

### Scalability factor and efficiency

Two simple numbers describe how well scaling works:

- **Speedup** (or scalability factor) = throughput with *n* units / throughput with 1 unit
- **Efficiency** = speedup / *n* (as a percentage). 100% is perfect (linear) scaling.

### Worked example: linear vs sub-linear

Suppose one server handles **500 req/s** at acceptable latency. We add servers and measure:

| Servers (n) | Measured throughput (req/s) | Ideal linear (500 × n) | Speedup (T/500) | Efficiency (speedup / n) | Throughput per server |
|---|---|---|---|---|---|
| 1 | 500 | 500 | 1.0 | 100% | 500 |
| 2 | 950 | 1,000 | 1.9 | 95% | 475 |
| 4 | 1,700 | 2,000 | 3.4 | 85% | 425 |
| 8 | 2,800 | 4,000 | 5.6 | 70% | 350 |

Check each calculation: 950 / 500 = 1.9, and 1.9 / 2 = 0.95. 1,700 / 500 = 3.4, and 3.4 / 4 = 0.85. 2,800 / 500 = 5.6, and 5.6 / 8 = 0.70. Correct.

**Linear scaling** would give 4,000 req/s at 8 servers. We got 2,800, which is **sub-linear**: we paid for 8 servers and got the output of 5.6. The missing 1,200 req/s points at a shared bottleneck (maybe the database, a lock, or the load balancer). That is a finding to report, with graphs and the resource metrics that explain it. Also compare **marginal gain**: going from 4 to 8 servers added 1,100 req/s (2,800 - 1,700), or 275 per added server, versus 500 for the first server.

### Cost versus scale trade-off

Suppose each server costs $100 per month. Cost per 1,000 req/s of capacity:

| Servers | Monthly cost | Throughput | Cost per 1,000 req/s |
|---|---|---|---|
| 1 | $100 | 500 | $100 / 0.5 = $200.00 |
| 2 | $200 | 950 | $200 / 0.95 = $210.53 |
| 4 | $400 | 1,700 | $400 / 1.7 = $235.29 |
| 8 | $800 | 2,800 | $800 / 2.8 = $285.71 |

As efficiency falls, each unit of capacity gets more expensive. This may be perfectly acceptable if you need the capacity, but it shows why the right answer is sometimes to **fix the bottleneck** (cheaper) rather than **buy more servers** (costlier). Scaling is a business decision, informed by test data.

### Amdahl's law (introduction)

Why does efficiency fall even with no obvious mistake? One reason is that **some part of the work cannot be spread out**: it must run one step after another (the "serial" part), such as writing to a single shared counter or database row. **Amdahl's law** gives the maximum speedup when part of the work is serial.

If a fraction **s** of the work is serial (cannot be parallelised) and the rest (1 - s) can be shared perfectly among **n** workers, the speedup is:

`Speedup(n) = 1 / ( s + (1 - s) / n )`

And as *n* grows without limit, the speedup approaches **1 / s**. That is a hard ceiling.

Worked example with s = 0.05 (5% serial): the best possible speedup is 1 / 0.05 = **20x**, however many workers you add. With *n* = 8: 1 / (0.05 + 0.95/8) = 1 / (0.05 + 0.11875) = 1 / 0.16875 = **5.93**. Our demo prints this. Restaurant link: the single cashier is the serial part. Ten kitchens do not help if every customer queues at one till. The restaurant's output is limited by the till.

Treat this as a simple model, not a prediction of real systems (real systems also have coordination costs, which can reduce performance further). But it teaches an important lesson: **to scale better, find and shrink the serial part.**

### Identifying limits and bottlenecks

As in the performance lesson, watch for the "knee": the point at which latency rises sharply and throughput stops growing. Typical culprits when scaling:

- A single database (all servers wait on one writer)
- Locks and shared counters
- Shared file storage or a single message queue
- The load balancer or network bandwidth
- External services with rate limits (for example an email provider that allows 10 sends per second no matter how many servers you add)
- Connection limits (each new server opens more database connections, hitting the database limit)

### Capacity planning basics

**Capacity planning** is estimating how many resources you will need to meet future demand. Key ideas:

- **Headroom:** spare capacity above current peak, so surprises and failures do not cause an outage. If servers run at 95% at peak, there is nowhere to go. Teams often target something like 60 to 70% utilisation at peak (the number is a policy choice, not a law).
- **Forecasting growth:** use historic trends and business plans (marketing campaigns, seasons) to predict demand.
- **N+1 redundancy:** provision one more unit than the minimum, so one can fail or be updated without a capacity loss.

**Worked example.** One Project 1 server can handle at most 400 req/s. The team's policy is to keep utilisation at or below 70% at peak, so the **planned capacity** per server is 400 × 0.70 = **280 req/s**. Today's peak is **600 req/s**.

- Servers needed today = 600 / 280 = 2.14, round up to **3**. With N+1 redundancy: **4**.
- Traffic is forecast to grow **10% per month**. In 6 months the peak is 600 × 1.1^6 = 600 × 1.771561 = about **1,063 req/s**.
- Servers needed in 6 months = 1,063 / 280 = 3.80, round up to **4**. With N+1: **5**.
- Because scaling is usually sub-linear (see above), add a margin or confirm the numbers with a scalability test at the larger size.

### Scalability vs performance vs capacity

These three words are often mixed up.

| Concept | Question | Example statement | Measured by | Link |
|---|---|---|---|---|
| **Performance** | How fast does it respond right now, for a given load? | "Login p95 is 300 ms at 100 users" | Response time, throughput, resource use | Today's performance lesson |
| **Capacity** | How much load can the current setup handle at acceptable quality? | "This setup handles up to 400 req/s" | Maximum sustainable throughput | Load and stress testing |
| **Scalability** | How does capacity or performance change as we add resources or demand grows? | "Doubling servers gives 1.9x capacity" | Speedup, efficiency, cost per unit | This lesson |

A one-line memory aid: performance is **speed now**, capacity is **size of the container now**, scalability is **how the container grows**. A system can be fast but not scalable (a very quick single server with a hard ceiling), or scalable but slow (adds capacity easily but each request is sluggish).

### Cloud-native context (names only)

Modern systems often run in the cloud with these technologies, which you will meet later in the programme. For now, simply know the names:

- **Containers** (for example Docker): lightweight packages that bundle an app and its dependencies, so it runs the same everywhere.
- **Kubernetes:** a system that runs and manages many containers, restarts failed ones, and can add or remove copies automatically.
- **Auto-scaling groups:** a cloud feature that adds or removes virtual machines based on rules.

**A caution:** moving to the cloud does **not** make an application automatically scalable or reliable. These tools give you the *ability* to scale; the application still needs stateless design, sensible limits and good tests.

---

## Putting It Together: The Python Demonstration

Now let us run something real. The script below uses only Python's standard library, takes less than a second, makes **no network calls and creates no files**, and is safe to run on any computer. It has three parts and a small test suite:

1. **Availability maths:** helpers for availability, MTBF/MTTR, and a nines table.
2. **Retry with exponential backoff plus a circuit breaker** against a flaky simulated dependency (seeded random numbers, so results are repeatable). The backoff waits are *recorded, not slept*, so it runs instantly. Time is passed in as a number, so tests need no real clock.
3. **A toy scalability model** using Amdahl's law with a 5% serial fraction.

Save it as `reliability_demo.py` and run `python3 reliability_demo.py` (or `python reliability_demo.py`).

```python
"""Reliability and scalability toy demo (standard library only, safe to run)."""
import random
import unittest

# ---------------- Part 1: availability helpers ----------------
MIN_PER_YEAR = 365 * 24 * 60      # 525,600
MIN_PER_MONTH = 30 * 24 * 60      # 43,200

def availability_from_times(uptime, downtime):
    return uptime / (uptime + downtime)

def availability_from_mtbf_mttr(mtbf, mttr):
    return mtbf / (mtbf + mttr)

def allowed_downtime_minutes(avail_pct, period_minutes):
    return period_minutes * (1 - avail_pct / 100)

def fmt_minutes(m):
    if m >= 60 * 24:
        return f"{m / 1440:.2f} days"
    if m >= 60:
        return f"{m / 60:.2f} hours"
    if m >= 1:
        return f"{m:.2f} minutes"
    return f"{m * 60:.2f} seconds"

def part1():
    print("=== Part 1: availability, MTBF, MTTR ===")
    a = availability_from_times(uptime=719, downtime=1)
    print(f"Availability from 719 h up, 1 h down: {a * 100:.3f}%")
    b = availability_from_mtbf_mttr(mtbf=500, mttr=2)
    print(f"Availability from MTBF=500 h, MTTR=2 h: {b * 100:.3f}%")
    print()
    print(f"{'Target':<9}{'Per year':<16}{'Per 30-day month':<18}")
    for pct in (99.0, 99.9, 99.99, 99.999):
        y = fmt_minutes(allowed_downtime_minutes(pct, MIN_PER_YEAR))
        m = fmt_minutes(allowed_downtime_minutes(pct, MIN_PER_MONTH))
        print(f"{pct:<9}{y:<16}{m:<18}")
    print()

# ---------------- Part 2: retry + circuit breaker ----------------
class FlakyDependency:
    """Fails with probability fail_rate, using a seeded random generator."""
    def __init__(self, fail_rate, seed):
        self.fail_rate = fail_rate
        self.rng = random.Random(seed)
        self.calls = 0
    def call(self):
        self.calls += 1
        if self.rng.random() < self.fail_rate:
            raise ConnectionError("dependency failed")
        return "ok"

def retry_with_backoff(func, max_attempts=4, base_delay=0.1, factor=2.0, delays_log=None):
    """Retry func; the waits are recorded, not slept, so the demo is instant."""
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except ConnectionError:
            if attempt == max_attempts:
                raise
            wait = base_delay * (factor ** (attempt - 1))
            if delays_log is not None:
                delays_log.append(round(wait, 3))

class CircuitOpenError(Exception):
    pass

class CircuitBreaker:
    CLOSED, OPEN, HALF_OPEN = "CLOSED", "OPEN", "HALF_OPEN"
    def __init__(self, failure_threshold=3, reset_timeout=10.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = self.CLOSED
        self.failures = 0
        self.opened_at = None
    def call(self, func, now):
        if self.state == self.OPEN:
            if now - self.opened_at >= self.reset_timeout:
                self.state = self.HALF_OPEN
            else:
                raise CircuitOpenError("circuit is open, failing fast")
        try:
            result = func()
        except ConnectionError:
            self.failures += 1
            if self.state == self.HALF_OPEN or self.failures >= self.failure_threshold:
                self.state = self.OPEN
                self.opened_at = now
            raise
        self.failures = 0
        self.state = self.CLOSED
        return result

def part2():
    print("=== Part 2: retry with backoff and circuit breaker ===")
    dep = FlakyDependency(fail_rate=0.5, seed=42)
    delays = []
    ok = failed = 0
    for _ in range(20):
        try:
            retry_with_backoff(dep.call, delays_log=delays)
            ok += 1
        except ConnectionError:
            failed += 1
    print(f"20 requests with retries: {ok} succeeded, {failed} failed, "
          f"{dep.calls} dependency calls, {len(delays)} backoff waits")
    print(f"First backoff waits (seconds): {delays[:6]}")

    broken = FlakyDependency(fail_rate=1.0, seed=1)
    cb = CircuitBreaker(failure_threshold=3, reset_timeout=10.0)
    print("Circuit breaker against a dependency that is fully down:")
    for t in range(6):
        try:
            cb.call(broken.call, now=t)
        except CircuitOpenError:
            print(f"  t={t}s: rejected fast, state={cb.state}, real calls so far={broken.calls}")
        except ConnectionError:
            print(f"  t={t}s: real call failed, state={cb.state}, real calls so far={broken.calls}")
    broken.fail_rate = 0.0
    print("Dependency recovers; breaker probes after the 10 s timeout:")
    r = cb.call(broken.call, now=14)
    print(f"  t=14s: result={r}, state={cb.state}")
    print()

# ---------------- Part 3: toy scalability model ----------------
def amdahl_speedup(workers, serial_fraction):
    return 1 / (serial_fraction + (1 - serial_fraction) / workers)

def part3():
    print("=== Part 3: toy scalability model (serial fraction 5%) ===")
    base, s = 100.0, 0.05
    print(f"{'Workers':<9}{'Throughput':<13}{'Speedup':<10}{'Efficiency':<11}")
    for n in (1, 2, 4, 8, 16, 32):
        sp = amdahl_speedup(n, s)
        print(f"{n:<9}{base * sp:<13.1f}{sp:<10.2f}{sp / n * 100:<10.1f}%")
    print(f"Upper limit as workers grow: {base / s:.0f} req/s (base / serial fraction)")
    print()

# ---------------- Tests ----------------
class ReliabilityTests(unittest.TestCase):
    def test_availability_formulas_agree(self):
        self.assertAlmostEqual(availability_from_times(98, 2), availability_from_mtbf_mttr(98, 2))
    def test_nines_year(self):
        self.assertAlmostEqual(allowed_downtime_minutes(99.9, MIN_PER_YEAR), 525.6)
        self.assertAlmostEqual(allowed_downtime_minutes(99.999, MIN_PER_YEAR), 5.256)
    def test_retry_succeeds_after_failures(self):
        calls = {"n": 0}
        def f():
            calls["n"] += 1
            if calls["n"] < 3:
                raise ConnectionError()
            return "ok"
        log = []
        self.assertEqual(retry_with_backoff(f, delays_log=log), "ok")
        self.assertEqual(log, [0.1, 0.2])
    def test_retry_gives_up(self):
        dep = FlakyDependency(1.0, 0)
        with self.assertRaises(ConnectionError):
            retry_with_backoff(dep.call, max_attempts=3)
        self.assertEqual(dep.calls, 3)
    def test_breaker_opens_and_fails_fast(self):
        dep = FlakyDependency(1.0, 0)
        cb = CircuitBreaker(3, 10)
        for t in range(3):
            with self.assertRaises(ConnectionError):
                cb.call(dep.call, now=t)
        self.assertEqual(cb.state, CircuitBreaker.OPEN)
        with self.assertRaises(CircuitOpenError):
            cb.call(dep.call, now=4)
        self.assertEqual(dep.calls, 3)
    def test_breaker_recovers(self):
        dep = FlakyDependency(1.0, 0)
        cb = CircuitBreaker(2, 10)
        for t in range(2):
            with self.assertRaises(ConnectionError):
                cb.call(dep.call, now=t)
        dep.fail_rate = 0.0
        self.assertEqual(cb.call(dep.call, now=20), "ok")
        self.assertEqual(cb.state, CircuitBreaker.CLOSED)
    def test_seeded_dependency_is_repeatable(self):
        a, b = FlakyDependency(0.5, 7), FlakyDependency(0.5, 7)
        def outcomes(d):
            r = []
            for _ in range(10):
                try: d.call(); r.append(1)
                except ConnectionError: r.append(0)
            return r
        self.assertEqual(outcomes(a), outcomes(b))
    def test_speedup_bounds(self):
        self.assertAlmostEqual(amdahl_speedup(1, 0.05), 1.0)
        self.assertLess(amdahl_speedup(1000, 0.05), 20.0)
        self.assertAlmostEqual(amdahl_speedup(8, 0.0), 8.0)

def run_tests():
    print("=== Tests ===")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReliabilityTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    part1(); part2(); part3(); run_tests()
```

### The genuine output

This is the real output from running the script (nothing edited):

```
=== Part 1: availability, MTBF, MTTR ===
Availability from 719 h up, 1 h down: 99.861%
Availability from MTBF=500 h, MTTR=2 h: 99.602%

Target   Per year        Per 30-day month  
99.0     3.65 days       7.20 hours        
99.9     8.76 hours      43.20 minutes     
99.99    52.56 minutes   4.32 minutes      
99.999   5.26 minutes    25.92 seconds     

=== Part 2: retry with backoff and circuit breaker ===
20 requests with retries: 19 succeeded, 1 failed, 36 dependency calls, 16 backoff waits
First backoff waits (seconds): [0.1, 0.2, 0.4, 0.1, 0.2, 0.4]
Circuit breaker against a dependency that is fully down:
  t=0s: real call failed, state=CLOSED, real calls so far=1
  t=1s: real call failed, state=CLOSED, real calls so far=2
  t=2s: real call failed, state=OPEN, real calls so far=3
  t=3s: rejected fast, state=OPEN, real calls so far=3
  t=4s: rejected fast, state=OPEN, real calls so far=3
  t=5s: rejected fast, state=OPEN, real calls so far=3
Dependency recovers; breaker probes after the 10 s timeout:
  t=14s: result=ok, state=CLOSED

=== Part 3: toy scalability model (serial fraction 5%) ===
Workers  Throughput   Speedup   Efficiency 
1        100.0        1.00      100.0     %
2        190.5        1.90      95.2      %
4        347.8        3.48      87.0      %
8        592.6        5.93      74.1      %
16       914.3        9.14      57.1      %
32       1254.9       12.55     39.2      %
Upper limit as workers grow: 2000 req/s (base / serial fraction)

=== Tests ===
test_availability_formulas_agree (__main__.ReliabilityTests.test_availability_formulas_agree) ... ok
test_breaker_opens_and_fails_fast (__main__.ReliabilityTests.test_breaker_opens_and_fails_fast) ... ok
test_breaker_recovers (__main__.ReliabilityTests.test_breaker_recovers) ... ok
test_nines_year (__main__.ReliabilityTests.test_nines_year) ... ok
test_retry_gives_up (__main__.ReliabilityTests.test_retry_gives_up) ... ok
test_retry_succeeds_after_failures (__main__.ReliabilityTests.test_retry_succeeds_after_failures) ... ok
test_seeded_dependency_is_repeatable (__main__.ReliabilityTests.test_seeded_dependency_is_repeatable) ... ok
test_speedup_bounds (__main__.ReliabilityTests.test_speedup_bounds) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

### Explaining the output, line by line

**Part 1**

- `Availability from 719 h up, 1 h down: 99.861%`. Total time is 720 hours (a 30-day month). 719 / 720 = 0.99861. We format it with three decimals as a percentage. One hour of downtime in a month is already worse than "three nines" would allow? Check: 99.9% allows 43.2 minutes per month, and 1 hour is 60 minutes, so yes, this month **missed** a 99.9% SLO but met a 99.5% SLA.
- `Availability from MTBF=500 h, MTTR=2 h: 99.602%`. 500 / (500 + 2) = 500 / 502 = 0.99602. This matches worked example 4 earlier.
- The table header and rows show the nines table, computed by the function rather than typed by hand. 99.0: 525,600 × 0.01 = 5,256 minutes, which `fmt_minutes` converts to days (5,256 / 1,440 = 3.65). 99.9: 525.6 minutes becomes 8.76 hours. 99.99: 52.56 minutes. 99.999: 5.256 minutes, printed rounded to `5.26 minutes` (the exact value is 5.256). The monthly column uses 43,200 minutes: 432 minutes = 7.20 hours; 43.2 minutes; 4.32 minutes; and 0.432 minutes, which is shown as 25.92 seconds (0.432 × 60).

**Part 2**

- `20 requests with retries: 19 succeeded, 1 failed, 36 dependency calls, 16 backoff waits`. The dependency fails half the time (seeded with 42, so the same sequence every run). Each request may try up to 4 times. 19 requests eventually succeeded. One request failed all 4 attempts (probability 0.5^4 = 6.25% per request, so about 1 in 16, so seeing 1 in 20 is plausible). The **36 calls** are more than the 20 requests, which shows the cost of retries: extra load on the dependency. The 16 backoff waits are the waits recorded between failed attempts (3 for the request that failed completely, plus waits for the others).
- `First backoff waits (seconds): [0.1, 0.2, 0.4, 0.1, 0.2, 0.4]`. Each wait doubles: `base_delay × factor^(attempt-1)` gives 0.1, 0.2, 0.4. The sequence restarts for the next request that needs retries. (Real systems would add random jitter and would actually wait; here we only record.)
- The circuit breaker is set to open after **3** consecutive failures. At `t=0s` and `t=1s` the real call fails, and the state stays `CLOSED` (the failure count is 1, then 2). At `t=2s` the third failure reaches the threshold, so the state flips to `OPEN`. The real call counter reads 3.
- At `t=3s`, `4s`, `5s` the breaker is open, so the requests are **rejected fast** with `CircuitOpenError`, and the "real calls so far" stays at **3**. This is the main benefit: the broken dependency is not being hammered, and callers get an immediate answer instead of waiting.
- `Dependency recovers`: we set the failure rate to 0. At `t=14s`, more than 10 seconds after the breaker opened at `t=2s`, the breaker moves to `HALF_OPEN`, allows one trial call, which succeeds, so the result is `ok` and the state returns to `CLOSED`.

**Part 3**

- The header prints the columns. Base throughput is 100 req/s for one worker, and the serial fraction is 5%.
- For 1 worker: speedup 1.00, efficiency 100%.
- For 2 workers: `1 / (0.05 + 0.95/2)` = 1 / 0.525 = 1.905, so throughput is 190.5 and efficiency is 1.905 / 2 = 95.2%.
- For 4 workers: 1 / (0.05 + 0.2375) = 3.478, throughput 347.8, efficiency 87.0%.
- For 8 workers: 5.93, throughput 592.6, efficiency 74.1%.
- For 16 workers: 9.14, throughput 914.3, efficiency 57.1%.
- For 32 workers: 12.55, throughput 1,254.9, efficiency 39.2%.
- `Upper limit as workers grow: 2000 req/s`. 100 / 0.05 = 2,000. Even with unlimited workers the toy system cannot exceed this; at 32 workers we have reached only about 63% of the ceiling (1,254.9 / 2,000) while using 32 times the resources. The "%" is on its own because of the column padding in the print statement; it is a formatting quirk, not a bug.

**Tests**

- Each `... ok` line is one test passing. What each one proves:
  - `test_availability_formulas_agree`: the uptime-based formula and the MTBF/MTTR formula give the same answer, 98 up and 2 down (98 / 100 = 0.98).
  - `test_nines_year`: 99.9% gives 525.6 minutes per year and 99.999% gives 5.256, which are the values in the nines table.
  - `test_retry_succeeds_after_failures`: after two failures the third attempt succeeds, and the recorded waits are exactly `[0.1, 0.2]`.
  - `test_retry_gives_up`: a permanently failing dependency receives exactly 3 calls when `max_attempts=3`, then the error is raised. Retries are bounded.
  - `test_breaker_opens_and_fails_fast`: after 3 failures the state is `OPEN`, the next call raises `CircuitOpenError`, and the dependency was called only 3 times.
  - `test_breaker_recovers`: after the timeout and a successful trial, the state is `CLOSED` again.
  - `test_seeded_dependency_is_repeatable`: two dependencies with the same seed produce the same ten outcomes. This is why seeding matters in tests: **deterministic randomness** makes failures reproducible, which you need for defect reports.
  - `test_speedup_bounds`: speedup with 1 worker is 1; with 1,000 workers it is still below 20 (the ceiling for 5% serial); with 0% serial work, 8 workers give exactly 8x.
- `Ran 8 tests in 0.000s` and `OK` mean all eight passed and the whole suite took well under a millisecond.

Try changing one thing at a time (for example, `fail_rate=0.8`, `failure_threshold=2`, or `s = 0.10`) and predict the result before you run it. Predicting then checking is how you build intuition.

---

## AI in Reliability

AI is increasingly used around reliability work. Three common uses at beginner level:

- **Anomaly detection:** machine-learning models learn the normal pattern of a metric (such as logins per minute at 9 a.m. on a Monday) and flag unusual deviations, sometimes before a fixed threshold would fire. This is useful for catching subtle problems like a slow memory leak.
- **AIOps:** "AI for IT operations", the use of AI to correlate alerts, group related incidents, suggest probable causes and sometimes trigger automated fixes. It aims to reduce alert noise, since a single incident can create hundreds of alerts.
- **Log summarisation and analysis:** language models can read thousands of log lines and produce a plain-language summary ("starting at 09:10, database timeouts increased; the first error was in the auth service"), or help draft a postmortem timeline and test ideas.

Used well, AI can speed up detection and diagnosis. But keep these **cautions** in mind:

1. **Verify, do not trust blindly.** A summary can sound confident and be wrong, or miss the one line that matters. Check against the raw logs, metrics and traces.
2. **Privacy and security.** Logs often contain personal data, email addresses, tokens or secrets. Never paste sensitive production logs into an unapproved AI tool. Follow your organisation's data rules and mask personal data.
3. **False positives and false negatives.** Anomaly detectors can cry wolf (alert fatigue) or miss slow, steady changes. Tune and evaluate them like any other test tool.
4. **Explainability.** If a model flags something, the team still needs to understand why before acting.
5. **AI-generated tests and plans need review.** AI can suggest fault scenarios (try asking it for "ten ways Project 1 login could fail"), but a human must judge relevance, safety and the expected result.
6. **Do not let automation act unsupervised on production** until its behaviour is well understood and safe limits are in place.

---

## Common Mistakes

| Mistake | Why it hurts | Better practice |
|---|---|---|
| **Confusing availability with reliability** | A system can be "up" but returning errors, or reliable but down for maintenance | Track both: uptime and successful-request rate (SLIs for each) |
| **Only testing the "happy infrastructure"** | Tests run only when every server, network and disk is healthy; the first real failure is a surprise | Add fault-injection scenarios to the plan (see A11) |
| **No recovery drills** | Backups, failovers and runbooks that have never been exercised often fail on the day | Schedule restore and failover drills and time them against RTO and RPO |
| **Assuming cloud means automatically scalable** | Cloud gives tools, not design. A stateful app or single database still has hard limits | Test scaling; design for statelessness; check quotas and limits |
| **Ignoring state** | Sessions, caches, queues and databases decide whether scaling and recovery work | Map where state lives; test session behaviour across servers and restarts |
| **Testing scale on a tiny environment** | Results from a laptop-size setup rarely predict production; bottlenecks appear only at size | Use a production-like environment, scaled data, and extrapolate carefully with stated assumptions |
| **Treating a high nine count as the goal** | Five nines is expensive and rarely needed | Agree targets with the business based on impact and cost |
| **Retrying everything blindly** | Retries of non-idempotent actions create duplicates; retries without backoff amplify outages | Retry only safe operations, with limits, backoff and jitter |
| **Alerts nobody tests** | An outage unnoticed for an hour has a very high MTTR | Test that alerts fire, reach the right people, and contain useful information |
| **Blaming people in postmortems** | People hide information and learning stops | Keep reviews blameless and focused on system and process fixes |
| **Using a single average** | Averages hide the unlucky users | Use percentiles and error rates (as in the performance lesson) |

---

## Sample Reliability and Scalability Test Checklist for Project 1

Use this as a starting point for the reliability and risk portion of your Project 1 test-design document. Adapt priorities to your own risk analysis. Items marked (R) are reliability and (S) scalability.

**Objectives and targets (agree these first)**

- [ ] (R) Availability target for login, for example 99.9% per 30-day month (43.2 minutes of allowed downtime), recorded as an SLO
- [ ] (R) SLIs defined: login success rate, registration success rate, p95 login latency
- [ ] (R) RTO and RPO defined for the user database (for example RTO 30 minutes, RPO 1 hour)
- [ ] (S) Expected peak load (users and requests per second) and growth forecast agreed with the product owner

**Environment and observability**

- [ ] Test environment is production-like (same architecture, similar data volume)
- [ ] Logs, metrics and traces are available; dashboards exist for latency, traffic, errors, saturation
- [ ] Alerts configured and listed with thresholds and recipients

**Reliability tests**

- [ ] (R) Regression suite run repeatedly (for example nightly) with pass rate and flaky tests tracked
- [ ] (R) Load-based reliability: error rate stays within SLO at expected peak load (reuse the load test)
- [ ] (R) Soak: 8 to 24 hours at normal load; memory, connections and disk trends are flat; no leaks
- [ ] (R) Scenario 1: kill the app or auth service during login; verify a friendly message and recovery time
- [ ] (R) Scenario 2: drop the connection to the email provider; verify no orphan or duplicate accounts and that emails are sent later
- [ ] (R) Scenario 3: fill the log disk; verify alerts and safe behaviour
- [ ] (R) Scenario 4: slow database; verify timeouts and no cascading slowdown
- [ ] (R) Scenario 5: restart during registration write; verify transactional integrity and idempotent retry
- [ ] (R) Scenario 6: expired TLS certificate detected by monitoring; renewal runbook exists
- [ ] (R) Scenario 7: clock skew; sessions, tokens and verification links behave correctly
- [ ] (R) Database failover; measure downtime and data loss against RTO and RPO
- [ ] (R) Backup restore into a clean environment; verify accounts and password logins; time it
- [ ] (R) Resilience patterns verified: timeout, retry with backoff, circuit breaker, graceful degradation, health checks, idempotent registration
- [ ] (R) Alerts: each injected fault triggers an alert within the agreed time with a useful message

**Scalability tests**

- [ ] (S) Baseline: maximum throughput of 1 instance at p95 < 500 ms and error rate < 1%
- [ ] (S) Stepwise scale-out: 1, 2, 4, 8 instances; record throughput, latency, resource use; compute speedup and efficiency
- [ ] (S) Session test: log in and continue on a different instance (stateless or shared session store works)
- [ ] (S) Replication lag test: register then immediately log in against a read replica (if used)
- [ ] (S) Spike test and auto-scaling: rapid load rise; new instances join healthy; scale-in does not drop requests; upper limit enforced
- [ ] (S) Data growth: login speed with 1,000, 100,000 and 1,000,000 user records
- [ ] (S) Identify bottleneck and limit; document the "knee"
- [ ] (S) Capacity plan: headroom, 6-month forecast, N+1, cost per 1,000 req/s

**Reporting**

- [ ] Results compared against SLOs and RTO/RPO; deviations logged as defects in Jira with evidence (log excerpts, graphs)
- [ ] Risks and recommendations recorded in the regression and risk plan
- [ ] Postmortem-style lessons learned for any failed drill

---

## Examples

### Example 1: Turning a business statement into a testable target

The product owner says: "Login must almost never go down." That is not testable. You ask questions and agree on: "The login service will be available 99.9% of each 30-day month, measured as the percentage of one-minute checks where a synthetic login succeeds." Allowed downtime is 43.2 minutes. Now you can test, monitor and report.

### Example 2: Reading a failed restore

A restore drill finishes in 55 minutes and the restored database has 12,480 accounts, but the live system had 12,512 at the time of the backup. Two findings: (1) 55 minutes breaks a 30-minute RTO; (2) 32 accounts are missing: 12,512 - 12,480 = 32. Investigate: perhaps the backup started before they registered (within the RPO), or the backup missed a table (a defect). A defect report in Jira would include the numbers, the steps and the logs.

### Example 3: A scaling result with a surprise

A scaling test shows 1 server = 300 req/s, 2 servers = 560, 4 servers = 600. Efficiency at 2 servers: (560 / 300) / 2 = 1.867 / 2 = 93.3%. At 4 servers: (600 / 300) / 4 = 2 / 4 = 50%. The jump from 2 to 4 servers added only 40 req/s, which is suspicious. CPU on the app servers is low while the database CPU is 98%: the **database is the bottleneck**. Adding web servers was the wrong investment. The fix might be indexing, caching or read replicas, then retest.

### Example 4: Idempotency saves the day

A user on a slow connection double-clicks "Register". Two identical requests arrive. Without idempotency, the second might create a duplicate account or an error. With a unique constraint on email, plus logic that returns the same result for a repeated request, the user ends with one account and a sensible message. The test: send the same request twice in parallel and count accounts: it must be exactly 1.

---

## Practice Exercises

Try each one on your own first, then compare with the answer key.

### Exercise 1: Compute availability and allowed downtime

(a) In a 30-day month (43,200 minutes), Project 1 login was down for a total of 30 minutes. What was the availability? Did it meet a 99.9% SLO?
(b) What is the allowed downtime per year and per 30-day month for a 99.95% target?

### Exercise 2: MTBF, MTTR and availability

Over 90 days (2,160 hours) a service had 6 outages with a total downtime of 9 hours. Compute MTTR, MTBF and availability.

### Exercise 3: Classify the scaling approach

State whether each is vertical or horizontal, and whether it is also elastic:
(a) Upgrading the database server from 16 GB to 64 GB of RAM.
(b) Adding three more web servers behind a load balancer.
(c) Kubernetes automatically adds pods when CPU stays above 70%.
(d) Moving from a small virtual machine to the next larger size.
(e) Splitting the users table across two databases by region.

### Exercise 4: Design five failure scenarios

Design five failure scenarios for Project 1. For each give: scenario, how to inject, expected behaviour, what to verify. Do not reuse the A11 table wording; invent your own.

### Exercise 5: Interpret a scaling table

| Servers | Throughput (req/s) |
|---|---|
| 1 | 200 |
| 2 | 380 |
| 4 | 700 |
| 8 | 1,000 |

Compute speedup and efficiency for each row. Where does scaling begin to flatten? What would you investigate, and would you add more servers?

### Exercise 6: Resilience pattern matching

Match each situation to a pattern: (a) the "forgot password" feature is slow and you want login unaffected; (b) a dependency has failed five times in a row and you want to stop calling it for 30 seconds; (c) a request waits forever for a reply; (d) a user double-submits a form; (e) the load balancer must stop sending traffic to a broken server.

---

## Answer Keys

### Exercise 1

(a) Uptime = 43,200 - 30 = 43,170 minutes. Availability = 43,170 / 43,200 = 0.999306, which is **99.931%**. The 99.9% SLO allows 43.2 minutes of downtime, and 30 minutes is less, so **yes, the SLO was met**. Error budget used: 30 / 43.2 = about 69.4%.

(b) Unavailability is 0.05% = 0.0005. Per year: 525,600 × 0.0005 = **262.8 minutes** = 4.38 hours. Per 30-day month: 43,200 × 0.0005 = **21.6 minutes**.

### Exercise 2

Downtime = 9 hours, so uptime = 2,160 - 9 = 2,151 hours.
- MTTR = 9 / 6 = **1.5 hours**
- MTBF = 2,151 / 6 = **358.5 hours**
- Availability = 358.5 / (358.5 + 1.5) = 358.5 / 360 = **0.99583 = 99.583%**. Check: 2,151 / 2,160 = 0.99583. Same.

### Exercise 3

(a) **Vertical** (scale up). Not elastic by itself.
(b) **Horizontal** (scale out). Elastic only if the servers are added automatically; if done by hand it is scalable but not elastic.
(c) **Horizontal and elastic** (auto-scaling).
(d) **Vertical**.
(e) **Horizontal** (data is spread across more databases: sharding). Not elastic by itself.

### Exercise 4

Sample answers (yours may differ, and that is fine as long as each has all four parts):

1. **Password-hash service times out.** Inject: stub returns after 10 s. Expect: request times out at the configured limit (for example 3 s), user sees "Please try again", no thread pile-up. Verify: other pages remain responsive and threads recover.
2. **Network partition between app and database for 60 seconds.** Inject: block the database port. Expect: friendly errors, health check turns unhealthy, circuit breaker opens, no stack traces. Verify: after restore, logins work without restarting the app; no data loss.
3. **Duplicate registration requests in parallel.** Inject: send two identical requests at the same instant. Expect: exactly one account, a consistent response. Verify: database has one row; no 500 error.
4. **Database restore from backup.** Inject: restore last night's backup in a clean environment. Expect: accounts up to the backup time exist, users can log in. Verify: restore time versus RTO; data age versus RPO.
5. **One of two app servers is killed during a 200-user load.** Inject: kill process at minute 5. Expect: error rate blips briefly, then returns to normal; alert fires. Verify: sessions survive (if shared store); the load balancer removes the dead node.

### Exercise 5

| Servers | Throughput | Speedup | Efficiency |
|---|---|---|---|
| 1 | 200 | 1.0 | 100% |
| 2 | 380 | 380 / 200 = 1.9 | 1.9 / 2 = 95% |
| 4 | 700 | 700 / 200 = 3.5 | 3.5 / 4 = 87.5% |
| 8 | 1,000 | 1,000 / 200 = 5.0 | 5.0 / 8 = 62.5% |

Scaling is healthy up to 4 servers, and **flattens between 4 and 8**: doubling servers added only 300 req/s (1,000 - 700), a 43% increase for a 100% increase in cost, so the marginal gain per added server is 75 req/s, versus 200 for the first. Do not add more servers yet. First investigate the bottleneck: look at database CPU and connections, locks, load balancer limits, any shared service or external rate limit. Fix it and retest. (Using Amdahl's formula as a rough guide, 5.0 speedup at n = 8 corresponds to a serial fraction of roughly 8.6%: from 1 / (s + (1 - s)/8) = 5 we get s + (1 - s)/8 = 0.2, so 8s + 1 - s = 1.6, so 7s = 0.6 and s = 0.0857. Treat that as an order-of-magnitude indicator only.)

### Exercise 6

(a) **Bulkhead** (isolate resources), also graceful degradation. (b) **Circuit breaker**. (c) **Timeout**. (d) **Idempotency**. (e) **Health check** (plus redundancy so other servers carry the load).

---

## Knowledge Check

1. What are the four ISO 25010 reliability sub-characteristics?
2. Which is better for raising availability: halving the failure rate, or quartering MTTR? Why might the second be easier?
3. A service is 99.9% available. How many minutes can it be down in a 30-day month?
4. What is the difference between an SLO and an SLA?
5. What does RPO measure, and what does RTO measure?
6. Why should retries use backoff and jitter?
7. In your own words, what is a circuit breaker and what state does it enter after too many failures?
8. Why does a stateless web server help scaling?
9. Scaling from 1 to 4 servers raised throughput from 400 to 1,200 req/s. What is the efficiency?
10. In the restaurant analogy, what does the single cashier represent, and what does Amdahl's law say about it?
11. Why is "we run in the cloud" not proof that a system scales?
12. Name two things a good blameless postmortem should leave behind.

### Answers

1. Maturity, availability, fault tolerance, recoverability.
2. Compare: halving failures doubles MTBF; quartering MTTR divides repair time by four. With MTBF 500 and MTTR 2: doubling MTBF gives 99.800%, quartering MTTR gives 99.900%. Faster recovery is often easier and cheaper (automation, monitoring, runbooks) than eliminating all failures.
3. 43,200 × 0.001 = **43.2 minutes**.
4. An SLO is an **internal target** for a service level measurement; an SLA is a **contract** with customers that often carries penalties if missed. SLOs are usually stricter.
5. RPO is the maximum acceptable **data loss measured in time**; RTO is the maximum acceptable **time to restore service**.
6. Backoff spaces retries out so they do not overload a struggling service; jitter randomises timing so many clients do not retry at the same instant (thundering herd).
7. A circuit breaker stops calls to a failing dependency after a threshold of failures and fails fast. It enters the **OPEN** state, later moves to **HALF-OPEN** for a trial call, and closes if the trial succeeds.
8. Stateless servers keep no per-user memory, so any server can handle any request. You can add, remove or lose servers freely without losing sessions.
9. Speedup = 1,200 / 400 = 3.0. Efficiency = 3.0 / 4 = **75%**.
10. It represents a **serial part** that cannot be spread across more resources (for example a single shared database writer). Amdahl's law says the maximum speedup is limited to 1 / s, where s is the serial fraction, no matter how many workers you add.
11. The cloud provides tools (auto-scaling, containers) but the application must be designed for scaling (stateless, no single bottleneck) and tested; limits, quotas and shared components still apply.
12. Examples: new or improved tests, new or improved alerts and monitoring, runbook updates, and specific action items with owners and dates.

---

## Try It: Project 1 Reliability and Scalability Mini-Assessment

**Goal:** add a reliability and scalability section to your Project 1 test-design document and regression and risk plan. Allow about 60 to 90 minutes.

**Steps**

1. **Set targets.** For the login feature, write an SLI, an SLO (choose 99.9% unless your team says otherwise), the allowed downtime per 30-day month, and an RTO and RPO for the user database. Show the arithmetic.
2. **Map dependencies.** Draw a simple box diagram of Project 1: browser, web app, database, email service. Mark every **single point of failure** in your diagram.
3. **Write six fault scenarios.** Use the format: scenario, how to inject, expected behaviour, what to verify. Include at least one from each category: kill a service, network failure, slow dependency, restart during write, a data scenario (backup restore or duplicate submit), and one of your choice (disk, certificate or clock).
4. **Link to resilience patterns.** For each scenario, name the pattern you would expect to see (timeout, retry, circuit breaker, bulkhead, graceful degradation, idempotency, health check, redundancy).
5. **Plan a scalability test.** Specify the baseline, the step sequence (1, 2, 4, 8 instances), the pass criteria (latency percentile and error rate), and how you will compute efficiency. Create a blank results table with throughput, speedup and efficiency columns.
6. **Capacity plan.** Using the worked example format, assume one server handles at most 300 req/s, a 70% planning limit, a current peak of 420 req/s and growth of 8% per month for 6 months. Calculate the servers needed now and in 6 months, with N+1.
7. **Run the demo.** Run the Python script, then change the serial fraction to 0.10 and the failure threshold to 2. Predict the effect, run again, and write two sentences about what changed.
8. **Risk entries.** Add three entries to your risk plan (risk, likelihood, impact, mitigation test) based on your scenarios, for example "Single database is a SPOF: high impact, medium likelihood; mitigation: failover drill".

**Check your work for step 6** (so you can self-mark): planned capacity per server = 300 × 0.7 = 210 req/s. Now: 420 / 210 = 2.0 servers exactly, so **2**, and **3** with N+1. In 6 months: 420 × 1.08^6. Since 1.08^2 = 1.1664; 1.08^3 = 1.259712; 1.08^6 = 1.259712^2 = 1.586874. So 420 × 1.586874 = about **666.5 req/s**. Servers = 666.5 / 210 = 3.17, so **4**, and **5** with N+1.

---

## Key Takeaways

- **Reliability** is the probability of failure-free operation for a stated time in a stated environment. Its ISO 25010 parts are maturity, availability, fault tolerance and recoverability.
- Know the vocabulary: reliability, availability, durability, resilience, robustness and maintainability are related but different.
- **Availability = MTBF / (MTBF + MTTR) = uptime / (uptime + downtime).** Each added "nine" cuts allowed downtime tenfold: 99.9% is 8.76 hours per year; 99.99% is 52.56 minutes; 99.999% is about 5.3 minutes.
- Faster **recovery** (low MTTR) is often the most efficient way to improve availability.
- **SLI** measures, **SLO** targets, **SLA** promises. The **error budget** is what the SLO allows you to "spend". **RTO** is how long you can be down; **RPO** is how much data you can lose.
- Reliability testing includes fault injection, recovery, failover, backup and restore, soak, and chaos experiments. Always run them in controlled environments with a rollback plan.
- Learn the resilience patterns by name and test each: timeout, retry with backoff, circuit breaker, bulkhead, graceful degradation, idempotency, health check, redundancy.
- Watch for failure modes: single points of failure, cascading failures, thundering herds, partial failures, data corruption, and resource exhaustion.
- Use **logs, metrics and traces** to see what happened, test your **alerts**, and learn from incidents through **blameless postmortems**.
- **Scalability** is handling growth by adding resources, and how efficiently. Scale **up** (bigger machine) or **out** (more machines). **Elasticity** is automatic scaling to demand.
- **Stateless** services scale more easily; manage state with shared stores, and watch for sticky sessions and replication lag.
- Test scalability by **increasing load stepwise while increasing resources**, then compute **speedup** and **efficiency**. Look for bottlenecks. **Amdahl's law:** speedup = 1 / (s + (1 - s)/n), limited to 1/s.
- **Capacity planning** uses headroom, forecasting and N+1 redundancy, and every decision has a **cost**.
- Performance is speed now, capacity is size now, scalability is how size grows.
- AI can help with anomaly detection, correlation and log summaries, but verify results and protect sensitive data.

---

## Week 3 Wrap-Up and What Comes Next

This week you moved from knowing how software is built (Monday) to knowing how to question it. In five days you covered: the SDLC, STLC, Agile and Jira; requirements analysis, test planning, execution and the defect lifecycle; the testing mindset, QA versus QC, and positive and negative testing; black-box techniques (boundary value analysis, equivalence partitioning, decision tables, state transition); and today's advanced topics: white-box testing, functional versus non-functional testing, exploratory, data-driven and regression testing, performance and stress testing, and reliability and scalability. Together, these give you a **quality engineering mindset**: ask what the software should do, how it could fail, how you would know, and how it holds up when conditions change.

All of it feeds one deliverable: **Project 1 - QE Foundations**, a sample web app with User Registration and Login. Friday's exercise completes your **test-design document** and **regression and risk plan**. Use this checklist to confirm you have each piece:

**Project 1 Week 3 deliverables checklist**

- [ ] **Requirements analysis:** requirements for registration and login reviewed, ambiguities and gaps noted, testable acceptance criteria written
- [ ] **Test plan:** scope, approach, entry and exit criteria, environments, roles, risks, schedule
- [ ] **Defect reports in Jira:** clear, reproducible reports with severity, priority, steps, expected and actual results, evidence, and a tracked lifecycle
- [ ] **Positive and negative test cases:** valid and invalid registration and login scenarios
- [ ] **Test-design document:** cases designed with boundary value analysis, equivalence partitioning, a decision table and state-transition cases (for example the login lockout)
- [ ] **Regression and risk plan:** which tests form the regression suite and when they run; risk ranking; the performance, reliability and scalability checks from today (including the checklist in this lesson)

If all six boxes are ticked, you have built a professional-quality test foundation for a small application. In the next phase of the programme you will start turning these manual designs into automated tests, and the same thinking (risk, evidence, repeatability) will guide that work. For now, take a moment to review your document with fresh eyes, as if you were a colleague who has never seen the project. Congratulations on completing Week 3.

---

## Additional Resources

- **Site Reliability Engineering (Google SRE book), table of contents:** https://sre.google/sre-book/table-of-contents/ . Free to read online. Good chapters for this lesson include those on service level objectives, monitoring distributed systems and postmortem culture.
- **Principles of Chaos Engineering:** https://principlesofchaos.org/ . A short page that states the discipline's definition and its core principles (steady state, hypothesis, real-world events, production experiments, automation, minimising blast radius).
- **ISO/IEC 25010 on iso.org:** https://www.iso.org/standard/35733.html . The product quality model standard page (this link is to the 2011 edition; search iso.org for "ISO/IEC 25010" to find the current revision). The full text is paid, but the page summarises the scope.
