# Performance and Stress Testing

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what "performance" means from the point of view of a user and from the point of view of the business, and why it matters.
- Describe the performance testing umbrella and distinguish load, stress, spike, soak (endurance), volume, scalability, baseline (benchmark), capacity and smoke performance tests, including their goals, load shapes and pass criteria.
- Define and use the key vocabulary: virtual users, concurrent users, requests per second, throughput, response time, latency, think time, ramp-up, steady state, percentiles, error rate, saturation, bottleneck, resource utilization, connection pools, queueing, caching, SLA, SLO, SLI, Little's Law and Apdex.
- Explain why averages mislead and compute average, median, p90, p95 and p99 from a list of response times.
- Follow the performance test process step by step, from goals and non-functional requirements to reporting, and build a workload model for Project 1 with real numbers.
- Read a result table and a response-time-versus-load graph, and recognise the "knee" where a system saturates.
- Name common bottlenecks and describe where they hide.
- Describe front-end performance basics (page load, Core Web Vitals, Lighthouse) and recognise the main performance tools by name.
- Run a safe, local-only mini load test in Python and interpret its output.
- Explain how performance checks fit into CI/CD, how AI can assist (and where it must not be trusted blindly), and which mistakes to avoid.
- Write a complete performance test plan and scenario table with measurable acceptance criteria for Project 1 (User Registration and Login).

## Why This Matters

Imagine you have spent two weeks building a flawless registration and login feature for Project 1. Every functional test passes. Every boundary value behaves. Every negative test is rejected correctly. On launch day, 2,000 people try to log in within the same ten minutes, and the login page takes 25 seconds to respond. Then it starts returning errors. Then it stops responding at all.

Was the feature "correct"? In the functional sense, yes: given enough time, it would have logged people in. In every sense that matters to a real person, no. The product failed.

This is the gap that performance testing fills. In your Wednesday lesson you learned that quality is more than "does it do what the requirement says". Earlier today you met non-functional testing and saw that performance is one of its most important types. This lesson takes that preview and turns it into a skill.

Here is why employers care:

- **Users leave when things are slow.** People are impatient, and there is always another site or app a tap away. A slow login or a sluggish checkout page quietly sends users to a competitor. They rarely file a defect; they simply do not come back.
- **Slowness costs money.** For businesses that sell things, every abandoned session is lost revenue. For businesses that serve customers, every failed login becomes a support call. For internal tools, slow software wastes paid staff time every single day.
- **Contracts and promises depend on it.** Many organisations promise customers specific response times and availability in a Service Level Agreement (SLA). Missing those promises can lead to penalties, refunds and damaged trust.
- **Performance problems are cheap to find early and very expensive to find late.** A slow database query discovered in a test environment is a small ticket. The same query discovered during a live outage at peak time is an incident, an apology email and a long night for several people.
- **Performance is a skill gap.** Many testers are comfortable with functional testing but nervous about performance. Understanding the concepts in this lesson makes you noticeably more valuable, and it prepares you for the tool-based performance courses that come later in this programme.

You do not need to be a performance specialist to benefit from this lesson. You need to understand the ideas well enough to ask the right questions, design sensible tests, and read results without being fooled by them. That is exactly what we will build.

---

## The Concept

### 1. What Is "Performance"?

When people say "the app is slow" they usually mean one thing, but performance is actually a family of related qualities. It helps to look at it from two angles.

#### The user's view

A user does not think about servers. A user experiences:

- **Speed:** how long it takes before they see what they asked for. "I clicked Log In and the dashboard appeared in one second."
- **Responsiveness:** whether the application reacts quickly to their actions and feels smooth. "I typed in the password box and nothing lagged."
- **Reliability under pressure:** whether it keeps working when it is busy. "It was fast at 3 a.m. but fell over at lunchtime."

#### The business's view

The business and the engineering team care about the same experience, but they also care about what is happening behind the scenes and what it costs:

- **Speed and responsiveness** (response time) for real users, usually described with targets.
- **Capacity:** how many users or how much work the system can handle at once before quality drops below an acceptable level.
- **Resource use:** how much CPU (processor), memory (RAM), disk activity and network bandwidth the system consumes to do its work. Using more resources means paying more for servers and cloud bills.
- **Stability under load:** whether the system stays steady during sustained or heavy use, with no creeping slowdowns, crashes or errors.

A useful way to hold all of this together is the **restaurant at lunch rush** analogy, which we will return to throughout this lesson.

> Think of a restaurant. A customer's experience is how long they wait for a table, how long the food takes, and whether the order is right. The owner cares about those things too, but also about how many customers the kitchen can serve per hour (capacity), how many cooks and how much gas and electricity it takes (resource use), and whether the kitchen stays calm and consistent during a long, busy Saturday (stability). A restaurant that produces great food in a quiet room at 3 p.m. but collapses at 12:30 p.m. is a restaurant with a performance problem, not a food problem.

Software is exactly the same. Functional testing asks, "Is the food correct?" Performance testing asks, "Is it still correct, fast and consistent when the room is full?"

#### Why performance matters (in general terms)

We will avoid quoting specific statistics here, because numbers in articles vary and go out of date. The general, widely accepted points are enough:

1. **User abandonment.** The longer people wait, the more likely they are to give up, refresh repeatedly, or leave. Slow pages and slow actions frustrate people, and frustrated people stop using a product.
2. **Revenue and conversion.** When registration, login or payment flows are slow or fail under load, fewer people complete them. For a business this directly reduces sign-ups, sales and renewals.
3. **Reputation and trust.** Outages and slowdowns during high-profile moments (a sale, a ticket release, a public announcement) become public stories.
4. **SLAs and obligations.** Customers, partners and regulators may expect specific response times and uptime. Breaking them has consequences.
5. **Cost.** An inefficient system needs more servers to do the same work. Finding and fixing inefficiency is often cheaper than buying more hardware.
6. **Competitive advantage.** A fast, smooth product feels more professional and trustworthy.

---

### 2. The Performance Testing Umbrella

**Performance testing** is the general term for testing how a system behaves in terms of speed, capacity, resource use and stability under a given workload. It is a non-functional testing activity: we are not checking whether login validates passwords correctly (that is functional), we are checking whether login stays fast and stable when many people use it.

Under this umbrella sit several distinct types of tests. They differ in the shape of the load we apply, how long we apply it, and the question we want to answer. Mixing them up is one of the most common beginner errors, so we will go through each carefully.

A quick reference first:

| Type | Core question | Load shape | Typical duration |
|---|---|---|---|
| Smoke performance | "Does the performance test even work, and is the system sane under tiny load?" | Very small, flat | Minutes |
| Baseline / benchmark | "What is normal right now, so we can compare later?" | Light to moderate, flat | Minutes to an hour |
| Load | "Does it meet targets under the expected load?" | Ramp up, then flat plateau | 30 to 60 minutes (often) |
| Stress | "Where does it break, and how does it recover?" | Staircase beyond the limit, then drop | 30 to 90 minutes |
| Spike | "Can it survive a sudden surge?" | Sharp jump, brief hold, drop | Minutes |
| Soak / endurance | "Does it stay healthy over a long time?" | Moderate flat for a long time | Hours (4, 8, 24 or more) |
| Volume | "Does it cope with a large amount of data?" | Normal load, huge data | Varies |
| Capacity | "What is the maximum load we can carry within targets?" | Staircase, find the limit within targets | Varies |
| Scalability | "If we add resources, does capacity grow proportionally?" | Repeat tests at different sizes | Covered in the next lesson |

We will now take each in turn.

#### 2.1 Load testing

**Definition.** Load testing applies the *expected* amount of load, the volume of users and activity that the system is meant to handle on a busy but normal day, and measures whether it meets its performance targets.

**Goal.** To answer: "Under the load we realistically expect, are response times acceptable, are errors rare, and are resources comfortable?"

**Analogy.** A bridge is designed for a certain traffic: say, rush hour with cars and lorries bumper to bumper. A load test is driving that expected rush-hour traffic across and checking that the bridge holds without strain.

**Load shape.** Users are added gradually (ramp-up), held at the target level for a meaningful period (steady state), and then removed gradually (ramp-down).

```
Virtual
Users
  |
  |            ___________________________
  |           /                           \
  |          /      steady state           \
  |         /      (measure here)            \
  |        /                                  \
  |_______/                                    \______
  +--------------------------------------------------> Time
      ramp-up                               ramp-down
```

**Typical Project 1 scenario.** Simulate the expected peak: for instance, the login journey running at 5 journeys per second with a realistic mix of registration, invalid login and password reset activity (we will calculate this properly later), held steady for 30 minutes.

**Pass criteria (examples).**
- 95th percentile (p95) login response time at most 800 ms during steady state.
- Error rate below 1 percent.
- CPU on the application server below 70 percent on average; memory stable.
- No requests failing with server errors (HTTP 5xx) beyond the allowed error rate.

#### 2.2 Stress testing

**Definition.** Stress testing deliberately pushes a system *beyond* its expected, even its designed, limits to find the **breaking point**, to see *how* it fails, and to observe whether and how it recovers when the pressure is removed.

**Goal.** To answer three questions:
1. At what load does the system stop meeting its targets, and at what load does it actually break?
2. When it breaks, does it fail gracefully (clear error messages, no data loss) or catastrophically (crashes, corrupted data, hangs)?
3. After the load drops, does it return to normal on its own (recovery)?

**Analogy.** Engineers load a test bridge with more and more weight, well past anything it will ever carry in real life, to learn exactly where it bends and cracks. The point is not to destroy it for fun but to know the margin of safety and the failure behaviour.

**Load shape.** A staircase that keeps climbing until the system fails, followed by a drop back to a low level to observe recovery.

```
Virtual
Users
  |                                      _______
  |                                _____|       |
  |                          _____|             |
  |                    _____|                   |   <- breaking point
  |              _____|                          |
  |        _____|                                |
  |  _____|                                      |_______  <- drop: watch recovery
  |_|                                                    
  +--------------------------------------------------------> Time
     step 1  step 2  step 3  step 4  step 5   cool-down
```

**Typical Project 1 scenario.** Increase login traffic in steps of 25 percent above the expected peak (125 percent, 150 percent, 200 percent, 300 percent) holding each step for five minutes, until errors exceed a threshold or response times become unusable. Then reduce to normal load and watch how long recovery takes.

**Pass criteria (examples).** Stress tests are different from load tests: there is no "everything must be fast" target at extreme load. Instead, typical criteria are:
- The system does not crash or corrupt data (for example, no half-created user accounts).
- Failures are controlled: the system returns clear, quick errors such as "please try again shortly" rather than hanging indefinitely.
- After the load returns to normal, response times and error rates return to baseline within an agreed time (for example, within five minutes) without manual restart.
- The breaking point is documented and exceeds the expected peak by an agreed safety margin (for example, at least twice the expected peak).

**Important.** Stress testing is not "load testing but bigger". Its purpose and its judgement criteria are different. A load test passes or fails against targets. A stress test *discovers* limits and failure behaviour.

#### 2.3 Spike testing

**Definition.** Spike testing applies a sudden, sharp increase in load, held briefly, then a sharp decrease, to see whether the system can absorb abrupt surges and recover.

**Goal.** To answer: "What happens when traffic goes from quiet to enormous almost instantly?" Real traffic is often not smooth. A marketing email lands, a link goes viral, a ticket sale opens at exactly 9:00 a.m., or the whole office logs in at the start of the working day.

**Analogy.** A football match ends and 40,000 people walk to the station at once. A station that is fine with a steady flow of passengers may be overwhelmed by the sudden wave.

**Load shape.**

```
Virtual
Users
  |             __
  |            |  |            <- sudden spike
  |            |  |
  |            |  |
  |            |  |
  |____________|  |____________  <- return to normal: does it recover?
  +------------------------------> Time
     normal      spike  normal
```

**Typical Project 1 scenario.** Normal load of 10 logins per second suddenly jumps to 10 times that for two minutes, as if a marketing email announcing a new feature has just been sent, then drops back to normal.

**Pass criteria (examples).**
- No crash or permanent failure during the spike.
- Errors during the spike stay within an agreed limit (for example, below 5 percent) or the system sheds load in a controlled way (clear "busy" messages).
- Within a defined period after the spike (for example, two minutes), response times and error rate return to baseline levels.

#### 2.4 Soak (endurance) testing

**Definition.** Soak testing, also called endurance testing, applies a moderate, realistic load over a *long* period (many hours or even days) to expose problems that only appear with time.

**Goal.** To find issues such as:
- **Memory leaks:** a program keeps grabbing memory and never gives it back, so usage creeps up until the system slows or crashes.
- **Resource exhaustion:** running out of database connections, file handles or disk space because something is not released or cleaned up.
- **Gradual slowdowns:** log files growing, caches filling or fragmentation making things slower over hours.
- **Scheduled-job interference:** nightly cleanups or backups colliding with user traffic.

**Analogy.** A bridge may carry a heavy lorry once without trouble but suffer metal fatigue after a million crossings. A soak test is the million crossings.

**Load shape.** Flat and moderate for a long time. What matters is not the load level but the *trend* of the measurements over time.

```
Virtual
Users
  |   ____________________________________________
  |  /                                            \
  | /               long, steady load              \
  |/                  (hours)                       \
  +---------------------------------------------------> Time

Server memory used, over the same time (a leak looks like this):
  |                                         .  '
  |                                  .  '
  |                           .  '
  |                    .  '
  |             .  '
  |      .  '
  +---------------------------------------------------> Time
  (healthy memory would wander but stay roughly flat)
```

**Typical Project 1 scenario.** Run login and registration at 60 percent of expected peak for eight hours, watching memory, connection counts, response time and error rate.

**Pass criteria (examples).**
- Response time at hour 8 within 10 percent of response time at hour 1.
- Memory use shows no sustained upward trend (the line is flat, after any initial warm-up).
- Error rate stays below the agreed limit for the whole duration.
- Database connection counts return to normal levels and do not creep up.

#### 2.5 Volume testing

**Definition.** Volume testing checks how a system behaves when it has to handle a *large amount of data*, as opposed to a large number of users.

**Goal.** To discover problems that only appear when tables, files and indexes become big. A login that is fast with 50 sample users in a test database may be painfully slow with 5 million real accounts.

**Analogy.** A library catalogue search is quick in a small village library and much slower in a national library unless the catalogue is well organised.

**Typical Project 1 scenario.** Pre-load the database with 2 million user accounts, then measure login lookup time, registration duplicate-email checks, and any "list users" admin screens. Also check importing a large file of new users or generating a big report.

**Pass criteria (examples).**
- Login p95 with 2 million accounts is within 10 percent of login p95 with 1,000 accounts (the lookup should be indexed and scale well).
- Admin export of all users completes within an agreed time and does not crash the server.
- Disk and memory use stay within planned limits.

Volume testing links closely to the test data pitfalls we discuss later.

#### 2.6 Scalability testing (a pointer)

**Definition.** Scalability testing checks whether a system can grow its capacity when you give it more resources (for example, more servers), and how efficiently it does so.

We will not go deeper here, because **the next lesson, "Reliability and scalability", covers scalability in detail**, along with reliability, availability, failover and capacity planning. For today, hold on to just this idea: load testing asks "can it handle what we expect?", while scalability testing asks "if we need to handle more, can we simply add resources and have it work?"

#### 2.7 Baseline (benchmark) testing

**Definition.** A baseline test measures performance under a known, controlled, usually moderate load to establish a reference point: "this is what normal looks like for this version, on this environment."

**Goal.** Later results mean nothing without something to compare against. A baseline allows statements such as "the new release made login 30 percent slower", which is far more useful than "login takes 600 ms".

**Typical Project 1 scenario.** Run the standard login scenario at 10 percent of expected load every time the team releases, and record p50, p95, error rate and CPU. Store results to compare releases.

**Pass criteria (examples).** A baseline itself usually has no pass or fail; it records numbers. Once a baseline exists, comparisons become the criteria: for example, "p95 must not worsen by more than 10 percent versus the previous release baseline".

The word **benchmark** is sometimes used for comparing against an external standard or competitor, or comparing two technologies, for example "which database setting performs best". In day-to-day team conversation baseline and benchmark are often used interchangeably, so check what a colleague means.

#### 2.8 Capacity testing

**Definition.** Capacity testing determines the *maximum* load a system can carry while still meeting its performance targets.

**Goal.** To answer: "How many users or transactions per second can we support before response times or errors exceed our limits?" That number is the system's capacity.

**How it differs from stress testing.** Stress testing keeps going beyond the limit to see how the system *breaks*. Capacity testing is interested in the highest load at which the system is *still acceptable*. Both use rising load, but they report different findings: "we exceed targets above 85 requests per second" (capacity) versus "the service crashes at 140 requests per second and recovers in four minutes" (stress).

**Typical Project 1 scenario.** Step up login load until p95 passes 800 ms or errors exceed 1 percent; the last acceptable step is the capacity (for example, 85 requests per second). Compare with the planned peak of about 44 requests per second (which we will compute shortly) to see the safety margin.

Capacity *planning* (forecasting future needs and deciding what to buy or provision) is a bigger topic that belongs to the next lesson.

#### 2.9 Smoke performance testing

**Definition.** A smoke performance test is a very small, very quick run, a handful of users for a minute or two, to confirm that the test scripts work, the environment is up, and nothing is obviously, badly slow.

**Goal.** To avoid wasting a two-hour load test on a broken script or a misconfigured environment. It is the performance equivalent of a smoke test in functional testing: a fast check that it is worth continuing.

**Typical Project 1 scenario.** Five virtual users run login and registration for two minutes. Pass if every request returns the expected status code, the error rate is 0 percent, and p95 is within a generous limit (for example, below 1.5 seconds).

Smoke performance tests are ideal for automated pipelines because they are fast; more on that in the CI/CD section.

#### 2.10 How the types relate

A helpful way to remember the types is by the question each answers:

- **Smoke:** is it worth running the real tests?
- **Baseline:** what is normal?
- **Load:** is it good enough at the expected load?
- **Capacity:** how much can it carry while staying good enough?
- **Stress:** what happens when it is pushed beyond that, and does it recover?
- **Spike:** what about sudden surges?
- **Soak:** does it stay healthy for a long time?
- **Volume:** does it cope with a lot of data?
- **Scalability:** will adding resources help? (next lesson)

---

### 3. Key Concepts and Vocabulary

Performance testing has a lot of jargon. None of it is difficult, but terms are easy to mix up. We will define each one plainly.

#### 3.1 Virtual users, concurrent users, requests per second

**Virtual user (VU).** A simulated user created by the test tool. A virtual user executes a scripted journey: for example, open the login page, submit credentials, view the dashboard, pause, log out. Real tools create hundreds or thousands of VUs without needing real people.

**Concurrent users.** The number of users who are *active in the system at the same time*, in the middle of a session. This is a statement about how many people are "in the building".

**Requests per second (RPS) or throughput.** The number of requests the system handles each second. Throughput is more generally the amount of work done per unit time; it might be measured in requests per second, transactions per second or megabytes per second. This is a statement about how fast work arrives and gets done.

**Transactions per second (TPS).** A *transaction* in performance testing is a meaningful business step made of one or more requests, such as "Login" (which may involve loading a page, posting credentials, and loading a dashboard). TPS counts how many of these complete per second. One login transaction might contain five requests, so 10 TPS of login might equal 50 RPS.

**Why concurrent users and RPS are not the same.** This is the most important vocabulary distinction in the lesson. Picture the restaurant: 100 diners seated (concurrent users) does not tell you how many orders the kitchen receives per minute. If every diner is chatting and reading the menu, the kitchen may receive only a few orders. If everyone orders at the same moment, the kitchen is flooded. Likewise, 1,000 concurrent users who each click once every minute produce about 17 requests per second; 100 concurrent users who click every second produce 100 requests per second. The second group is the heavier load, despite being only a tenth of the number of people.

#### 3.2 Response time, latency and processing time

These three terms are often used loosely, and different tools use slightly different definitions, so always check what a particular tool or document means. A common, useful way to understand them:

- **Response time:** the total time from the moment the client sends a request until it has received the complete response. This is what the user (or the test tool) experiences.
- **Latency:** the delay in getting the *first part* of the answer back, strongly influenced by network travel time and waiting. Some people use "latency" as a simple synonym for network delay (the time for a message to travel there and back); some tools use it to mean time to first byte. Be aware of this inconsistency.
- **Processing time (server time):** the time the server actually spends working on the request (running code, querying the database), excluding network travel.

A rough picture:

```
Client                                         Server
  | --- request travels over network --->        |
  |        (network latency, outbound)            |
  |                                         [ processing time:
  |                                           run code, query DB ]
  | <--- response travels back over network ---  |
  |        (network latency, inbound,             |
  |         plus time to download the body)       |
  
  Response time = outbound travel + queueing + processing + inbound travel + download
```

Analogy: ordering from a restaurant by phone. Processing time is how long the kitchen takes to cook. Latency is the time for your call to connect and your order to arrive. Response time is the whole wait from the moment you place the order until the food is on your table.

#### 3.3 Think time

**Think time** is the pause a real user takes between actions: reading a page, typing a password, deciding what to click. In a test script we add deliberate pauses to model this.

Without think time, each virtual user hammers the system as fast as it can, producing far more load than a real person would. Imagine each diner placing a new order the instant their previous one arrives. The kitchen would be overwhelmed by a fraction of the customers. A script with no think time is one of the most common ways to produce unrealistic results (see "Common Mistakes").

Think time is usually randomised within a range (for example, 2 to 6 seconds) to avoid all virtual users acting in lock-step.

A related idea is **pacing**, controlling how often a user starts a new complete iteration of a journey, used to hold a target rate of journeys per second.

#### 3.4 Ramp-up, steady state and ramp-down

- **Ramp-up:** gradually increasing the number of virtual users from zero to the target. Starting everyone at once is unrealistic for most scenarios (except a deliberate spike test) and can overwhelm a system that has not warmed up.
- **Steady state:** the period in which load is held constant. Measurements for pass/fail are normally taken here, because ramp-up and ramp-down numbers are distorted by the changing load.
- **Ramp-down:** gradually reducing load at the end, which also helps check recovery and clean shutdown.

Warm-up matters too. Systems often run slower initially because caches are empty, code is not yet optimised by the runtime, and connection pools are still opening connections. This is why we discard the first part of a test from the analysis.

#### 3.5 Percentiles: average, median, p90, p95, p99

This is the single most important analysis idea in performance testing.

- **Average (mean):** add up all response times and divide by how many there are.
- **Median (p50):** the middle value. Half of responses were faster, half slower.
- **Percentile (pN):** the response time that N percent of requests were at or below. If p95 is 800 ms, then 95 percent of requests completed in 800 ms or less, and 5 percent took longer.
- **p90, p95, p99:** the 90th, 95th and 99th percentiles, commonly used to describe the "slow tail".

**Why averages mislead: a worked example.**

Suppose we measure 100 login requests. 95 of them took 200 ms. 5 of them took 8,000 ms (8 seconds), perhaps because they hit a database that was briefly locked.

- **Average** = (95 x 200 + 5 x 8,000) / 100 = (19,000 + 40,000) / 100 = **590 ms**.
- **Median (p50)** = the 50th value in sorted order = **200 ms**.
- **p90** = the 90th value = **200 ms**.
- **p95** = the 95th value (using the nearest-rank method, rank = 0.95 x 100 = 95) = **200 ms**.
- **p99** = the 99th value = **8,000 ms**.
- **Maximum** = **8,000 ms**.

Look at what the average says: "login takes about 590 ms". But *nobody* experienced 590 ms. 95 people had a fast 200 ms experience, and 5 people waited a full 8 seconds. The average describes no real user and hides both the good news (most people are fast) and the bad news (a few people have a terrible time). The percentiles tell the truth: typical experience is 200 ms, but one in a hundred requests is painfully slow.

Now imagine the data is flipped as the load increases and 20 percent of requests become slow. The average might only move a little while p90 and p95 jump dramatically. Percentiles reveal the pain much sooner than averages do.

**How percentiles are calculated (nearest-rank method).**

1. Sort the values from smallest to largest.
2. Compute the rank = ceiling(P / 100 x N), where N is the number of values.
3. The percentile is the value at that rank (counting from 1).

Different tools use slightly different methods (some interpolate between values), so tiny differences between tools are normal. What matters is using the same method consistently when comparing runs.

**A caution about averaging percentiles.** Never calculate the "average of the p95 values" from several test runs or several servers and call it the overall p95. Percentiles cannot be combined that way. Instead, compute the percentile from the combined raw measurements, or use a monitoring system that merges distributions properly.

**Which percentile should we use?**
- **p50** describes the typical experience.
- **p90 and p95** are common targets in requirements ("95 percent of logins complete within 800 ms").
- **p99** matters for high-volume systems and for systems where a slow tail causes timeouts. When one page load makes dozens of requests, the chance that *at least one* hits the slow tail is much higher than the per-request tail suggests.

#### 3.6 Error rate

**Error rate** is the percentage of requests (or transactions) that fail, expressed as failed divided by total. Failures include server errors (HTTP 5xx), timeouts, connection refusals, and also wrong responses (a 200 status with an error message in the body, if the script checks for it).

Always report error rate alongside response time. A system that responds in 50 ms because it immediately returns an error is "fast" but useless. You will see an example of this in our hands-on run later: when the server starts rejecting requests, throughput appears to *increase*, because failures are cheap and quick.

#### 3.7 Saturation and bottleneck

**Resource saturation** means a resource is so busy that extra demand has to wait. When CPU is at 100 percent, new work queues for processor time. When all database connections are in use, new requests queue for a connection.

A **bottleneck** is the single resource or component that limits the performance of the whole system, the narrowest point in the pipe. Improving anything *other* than the bottleneck makes little difference to overall performance. If the database can only handle 200 queries per second, then buying a faster web server will not raise the system's total capacity above that.

**Motorway analogy.** A four-lane motorway narrows to one lane for roadworks. It does not matter how smooth the other sections are or how fast the cars are; the one-lane stretch limits throughput for everyone, and a queue builds behind it. Performance testing is largely about finding that stretch of road.

#### 3.8 Resource utilization

Resource utilization is how much of a resource is being used. We watch the four classic resources on every server involved:

- **CPU:** the processor's busy time. Consistently very high CPU means the server is working hard; saturation means requests wait.
- **Memory (RAM):** how much is in use. A steady climb that never levels off suggests a leak. Running out causes slowdowns (swapping to disk) or crashes.
- **Disk I/O:** how much reading and writing to storage is happening. Databases and logging can make disks the bottleneck.
- **Network:** bandwidth and packets moving in and out. Large files and chatty services can saturate the network.

Healthy systems usually leave headroom (spare capacity) so that surges do not push them over the edge. A common rule of thumb in team discussions is to keep CPU well below saturation at expected peak, but your project's NFRs should state the actual target rather than relying on folk numbers.

#### 3.9 Connection pools, queueing and caching

**Connection pool.** Opening a connection to a database is slow and expensive, so applications open a fixed number of connections in advance (a "pool") and lend them out to requests, taking them back when finished. A pool of 20 connections means at most 20 database operations run simultaneously. If a 21st request arrives, it waits in line. If the pool is too small, it becomes a bottleneck; if it is too large, it can overwhelm the database.

**Queueing.** Whenever demand for a resource exceeds what is available right now, requests wait in a queue. Queues are the hidden engine behind most performance behaviour. When a system is lightly loaded, queues are nearly empty and response time is basically processing time. As utilisation approaches 100 percent, queue lengths and waiting times grow explosively, and response time shoots up. This is why graphs have that famous "knee" shape, which we examine in the section on reading results.

**Caching.** A cache stores the results of expensive work so it can be reused rather than recomputed. For example, remembering a user's profile in fast memory instead of querying the database each time. Caching can dramatically improve performance, but it also affects testing in important ways:
- A "cold" cache (empty) behaves very differently from a "warm" cache (filled). Tests should account for both.
- If your test data causes every request to hit the same cached item, the results are unrealistically good. Realistic variety in test data matters.
- Caches can hide problems that reappear when the cache is cleared or expires.

#### 3.10 SLA, SLO, SLI

These three terms describe how performance promises are expressed and measured. At name level:

- **SLI (Service Level Indicator):** a *measurement* of some aspect of service quality. Example: "the percentage of login requests completing in under 800 ms".
- **SLO (Service Level Objective):** an internal *target* for an SLI. Example: "99 percent of logins complete under 800 ms, measured over 30 days".
- **SLA (Service Level Agreement):** a formal *agreement*, often a contract with a customer, that includes consequences if targets are missed. Example: "Login availability of at least 99.9 percent per month, or the customer receives a service credit".

An easy way to remember: the SLI is the thermometer reading, the SLO is the temperature we aim for, and the SLA is the promise with penalties we make to the customer. Performance tests verify that the system can meet its SLOs and SLAs and should use the same measurements (SLIs).

(Availability, the "99.9 percent" style of target, is explored in the next lesson.)

#### 3.11 Little's Law (introductory)

**Little's Law** is a simple, powerful relationship from queueing theory:

> **L = lambda x W**

Where:
- **L** = the average number of items in the system (for example, users or requests in progress).
- **lambda** (the Greek letter, written here as "lambda" or the arrival rate) = the average rate at which items arrive (per second or per minute).
- **W** = the average time each item spends in the system.

The beauty of the law is that it holds for a very wide range of systems without needing to know the details inside, as long as the system is stable (the average arrival rate roughly equals the average departure rate) and you use consistent time units.

**Simple example: a coffee shop.** Customers arrive at 2 per minute (lambda = 2). Each customer stays an average of 5 minutes (W = 5). The average number of customers in the shop is L = 2 x 5 = **10**. If you counted heads in the shop at random moments, you would find about 10 people.

**Applied to a website.** If 5 users start a session each second (lambda = 5 per second) and each session lasts on average 192 seconds (W = 192), then the average number of concurrent users is 5 x 192 = **960**. We use exactly this calculation in the workload modelling example below.

**Applied to a server.** If a server receives 40 requests per second and each takes 0.25 seconds from arrival to completion, then on average 40 x 0.25 = **10 requests** are in progress inside the server at any moment. If the server can only process 8 at a time, a queue forms and times lengthen.

This is an introduction only. We use the law as a sanity check for numbers, not as a tool for precise prediction.

#### 3.12 Apdex (name level)

**Apdex (Application Performance Index)** is a standard way to turn response times into a single satisfaction score between 0 and 1. You pick a target time T. Responses faster than T count as "satisfied", those between T and about 4T count as "tolerating" (counted as half), and anything slower is "frustrated". The score is roughly (satisfied + half of tolerating) divided by total samples. Many monitoring products show an Apdex number. It is handy as a headline but hides detail, so use it alongside percentiles, not instead of them.

#### 3.13 Vocabulary quick reference

| Term | One-line meaning |
|---|---|
| Virtual user (VU) | A simulated user running a scripted journey |
| Concurrent users | Users active in the system at the same time |
| RPS / throughput | Requests (or work units) completed per second |
| TPS | Business transactions completed per second |
| Response time | Total time from sending a request to receiving the full response |
| Latency | Delay before a response starts to arrive (often network-related); check each tool's definition |
| Processing time | Time the server spends doing the work |
| Think time | Deliberate pause that models a real user's reading and typing |
| Ramp-up / steady state / ramp-down | Increase load, hold load, decrease load |
| Percentile (p95) | Value that 95 percent of measurements are at or below |
| Error rate | Percentage of failed requests |
| Saturation | A resource is fully busy and extra work must wait |
| Bottleneck | The single component that limits overall performance |
| Connection pool | A fixed set of reusable connections, for example to a database |
| Queueing | Waiting in line for a busy resource |
| Cache | Stored results reused to avoid repeating expensive work |
| SLI / SLO / SLA | Measurement / internal target / contractual promise |
| Little's Law | L = lambda x W: items in system = arrival rate x time in system |
| Apdex | A 0-to-1 satisfaction score derived from response times |

---

### 4. The Performance Test Process, Step by Step

Performance testing is not "point a tool at the website and press go". Done properly it follows a structured process, much like the test planning and execution cycle you learned on Tuesday.

```
 +---------------+   +--------------+   +--------------+   +-----------+
 | 1. Define     |-->| 2. Identify  |-->| 3. Prepare   |-->| 4. Script |
 | goals / NFRs  |   | scenarios &  |   | environment  |   | the       |
 |               |   | workload     |   | and data     |   | scenarios |
 +---------------+   +--------------+   +--------------+   +-----------+
                                                                  |
 +---------------+   +--------------+   +--------------+   +------v----+
 | 9. Report     |<--| 8. Tune and  |<--| 7. Analyse   |<--| 5. Execute|
 |               |   |    retest    |   |    results   |   | 6. Monitor|
 +---------------+   +--------------+   +--------------+   +-----------+
```

#### Step 1: Define goals and non-functional requirements (NFRs)

Ask: "What does 'good enough' mean?" Performance targets must be measurable. Compare:

- Poor: "Login should be fast."
- Good: "Under 1,000 concurrent users, 95 percent of login requests must complete within 800 ms, with an error rate below 1 percent."

Where do targets come from? Business stakeholders, SLAs, competitor expectations, previous release measurements and user research. If none exist, propose targets and get them agreed. This links directly to the requirements lessons from Tuesday: performance requirements need to be testable just like functional ones.

#### Step 2: Identify critical scenarios and build a workload model

You cannot (and should not) test every page. Choose the journeys that are most frequent, most business-critical, or most resource-hungry. For Project 1 those are login, registration, and probably password reset.

A **workload model** describes *what* load to apply: which journeys, in what proportions, at what rates, with what think times and for how long. Real usage data (from analytics or logs) is the best input. For new systems without data, you use estimates from the business and refine them later. A workload model section with numbers appears below.

#### Step 3: Prepare the test environment and data

- **Environment:** as close to production as practical, in hardware size, software versions, configuration, database size and network setup. Results from a tiny test server cannot be scaled up reliably to predict production.
- **Data:** enough realistic, varied test accounts and records; the right volumes; data that resets cleanly between runs.
- **Isolation:** no other teams running tests or deployments on the environment during your run, or results become unreliable.
- **Load generators:** the machines that run the virtual users must themselves be powerful enough and well connected, or they become the bottleneck.

#### Step 4: Script the scenarios

Create automated scripts that replay the journeys realistically: correct requests, parameterised data (different users, not the same one), correlated dynamic values (such as session tokens), think times, and checks that responses are correct. A script that "passes" because it received a fast error page is worse than useless.

#### Step 5: Execute, in the right order

Run tests in a sensible sequence, from cheap and safe to expensive and aggressive:

1. **Smoke:** verify the scripts and environment work at tiny load.
2. **Baseline:** record normal behaviour at light load.
3. **Load:** apply expected peak load and compare against targets.
4. **Stress** (and spike, soak, volume as planned): explore the limits and long-term behaviour.

Running a long stress test before confirming that a smoke test passes risks wasting hours.

#### Step 6: Monitor while running

A load test without server-side monitoring tells you *that* something is slow but not *why*. Collect, alongside the test tool's results:

- CPU, memory, disk and network on each server.
- Application metrics: thread counts, queue lengths, garbage collection (memory cleanup) activity.
- Database metrics: active connections, slow queries, locks.
- Error logs.

#### Step 7: Analyse results

Look at percentiles, throughput, error rates and resource use together, over time. Find where response times start to climb, what resource saturated first, which transactions were slowest and which errors appeared. Compare with the targets and with the baseline.

#### Step 8: Tune and retest

Fix the identified bottleneck (add an index, enlarge a pool, optimise a query, add caching, compress assets). **Change one thing at a time** and rerun the *same* test so you can tell what helped. After fixing one bottleneck, another will usually become the new limit. The cycle repeats until targets are met.

#### Step 9: Report

Tell the story to a mixed audience: a short summary for managers (pass or fail against targets, key risks, recommendations), and detailed data for engineers (graphs, tables, bottlenecks, environment details, versions, test configuration so the run can be repeated).

#### Performance test plan template

Use this outline as a starting point; adapt it to your team.

| Section | What to write |
|---|---|
| 1. Purpose and scope | Which system, release and features; what is in and out of scope |
| 2. Objectives | The questions the testing must answer |
| 3. Non-functional requirements | Measurable targets (response times, throughput, error rate, resource limits), with sources |
| 4. Test types planned | Smoke, baseline, load, stress, spike, soak, volume, and why each is included or excluded |
| 5. Workload model | Journeys, mix percentages, arrival rates, think times, durations |
| 6. Test environment | Servers, sizes, versions, configuration, differences from production |
| 7. Test data | Volumes, how created, how reset, privacy handling |
| 8. Tools | Load tool, monitoring tools, where load generators run |
| 9. Monitoring plan | Which metrics from which servers, sampling interval |
| 10. Entry and exit criteria | When testing may start; when it is complete |
| 11. Schedule and roles | Who does what and when; windows for shared environments |
| 12. Risks and assumptions | For example, environment smaller than production |
| 13. Reporting | Format, audience, frequency |

---

### 5. Workload Modelling: A Worked Example for Project 1

Let us build a workload model with real arithmetic. All the numbers are *assumptions chosen for teaching*; in a real project you would take them from analytics, logs or business forecasts.

**Business assumption.** During the busiest minute of the busiest hour (for example, Monday 9:00 a.m. when staff start work), Project 1 expects **300 user journeys per minute**. Note that a "journey" is one visit with a purpose.

#### Step A: Divide the journeys into a mix

| Journey | Share of traffic | Journeys per minute (peak) | Journeys per second |
|---|---|---|---|
| Successful login and browse | 70% | 210 | 3.5 |
| New user registration | 15% | 45 | 0.75 |
| Invalid login attempt (wrong password) | 10% | 30 | 0.5 |
| Password reset request | 5% | 15 | 0.25 |
| **Total** | **100%** | **300** | **5.0** |

Check: 210 + 45 + 30 + 15 = 300. And 300 divided by 60 = 5 journeys per second. Percentages: 70 + 15 + 10 + 5 = 100.

#### Step B: Requests per journey and the target RPS

Suppose measurement of the application (for example with the browser's network tab, which we mention later) shows the number of HTTP requests each journey makes. These include the page itself, scripts, API calls and so on:

| Journey | Requests per journey |
|---|---|
| Successful login and browse | 10 |
| New user registration | 8 |
| Invalid login attempt | 3 |
| Password reset request | 4 |

Weighted average requests per journey = (0.70 x 10) + (0.15 x 8) + (0.10 x 3) + (0.05 x 4) = 7.0 + 1.2 + 0.3 + 0.2 = **8.7 requests per journey**.

Peak requests per second = 5 journeys per second x 8.7 = **43.5 RPS**.

Alternatively, journey by journey: login 3.5 x 10 = 35, registration 0.75 x 8 = 6, invalid 0.5 x 3 = 1.5, reset 0.25 x 4 = 1. Total = 35 + 6 + 1.5 + 1 = **43.5 RPS**. The two methods agree.

#### Step C: Add headroom

We never design only for the expected peak, because real traffic is uneven and forecasts are wrong. Suppose the business wants the system to handle **50 percent above expected peak** without breaching targets. Target load = 43.5 x 1.5 = **65.25 RPS**, which we round to **about 65 RPS**.

So: the *load test* runs at the expected 43.5 RPS (and perhaps also at 65 RPS to confirm headroom), and the *stress test* goes well beyond.

#### Step D: Concurrent users (using Little's Law)

How many users are in the system at once? We need how long each journey lasts, including the time the user spends reading and typing:

| Journey | Typical duration | Share | Weighted contribution |
|---|---|---|---|
| Successful login and browse | 240 seconds (4 minutes) | 0.70 | 168 |
| New user registration | 120 seconds (2 minutes) | 0.15 | 18 |
| Invalid login attempt | 30 seconds | 0.10 | 3 |
| Password reset request | 60 seconds | 0.05 | 3 |
| **Average duration W** | | | **192 seconds** |

Using L = lambda x W: L = 5 journeys per second x 192 seconds = **960 concurrent users**.

#### Step E: Reality check on concurrency versus RPS

960 concurrent users produce only 43.5 RPS. That is about 0.045 requests per second per user, roughly one request every 22 seconds each, which makes sense for people who spend most of their time reading and typing. This reinforces why you cannot simply say "960 users" and stop: the test must be told *how fast* users act (think time), not just how many exist.

#### Step F: Convert to test settings

There are two common ways to drive a test:

1. **Closed model (user-driven):** set a number of virtual users who each loop through journeys with think times. Total load emerges from VUs and think times. To hold about 960 concurrent journeys you would configure about 960 VUs, each running a journey of average length 192 seconds including think times, then starting another. (Note that if the system slows down, a closed model automatically slows the arrival rate, because users wait for responses.)
2. **Open model (arrival-rate-driven):** set arrivals at 5 journeys per second regardless of how slow the system gets. This better represents real public traffic, where new people keep arriving even if the site is struggling. Many modern tools support this style (for example, "constant arrival rate" scenarios).

Knowing both and choosing consciously is a sign of a mature tester. For public sign-up and login traffic, the open model is usually the more honest model of reality.

#### Step G: Plan the test shape

- Ramp-up: 5 minutes from 0 to target.
- Steady state: 30 minutes at target.
- Ramp-down: 5 minutes.
- Measure pass/fail only on the 30-minute steady state.

---

### 6. Reading Results

Collecting numbers is easy; understanding them is the craft.

#### 6.1 A sample load test result table

Below is a *sample* (invented for teaching) summary of a 30-minute steady-state load test on Project 1 at expected peak.

| Transaction | Samples | Avg (ms) | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Max (ms) | Error rate | Target p95 | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| Open login page | 9,100 | 120 | 100 | 190 | 240 | 520 | 1,900 | 0.0% | 500 | Pass |
| Submit login | 6,300 | 410 | 330 | 650 | 790 | 1,450 | 4,800 | 0.3% | 800 | Pass (narrowly) |
| Submit registration | 1,350 | 780 | 640 | 1,250 | 1,520 | 2,600 | 7,200 | 0.8% | 1,500 | Fail (narrowly) |
| Password reset request | 450 | 300 | 250 | 480 | 560 | 900 | 2,100 | 0.0% | 1,000 | Pass |

How a professional reads this:

- "Submit login" passes its p95 target by only 10 ms. That is a *warning*, not a comfort. There is little headroom, and the p99 is close to double the p95. We should look at what happens at 150 percent load.
- "Submit registration" misses its p95 target by 20 ms. Registration is the heaviest transaction (the system checks for duplicate emails, hashes a password and writes to the database). Hashing passwords is deliberately slow for security reasons, so the investigation might look at CPU usage and the duplicate-email lookup.
- Averages are all comfortably lower than the p95 values. If we had judged only on averages, registration (780 ms average) would have looked "fine".
- Max values are single outliers; they matter if they repeat or point to timeouts, but we do not usually set targets on the maximum.

#### 6.2 A sample stress test result table

Here is a *sample* staircase stress test of the login transaction, each step held for five minutes:

| Step | Load (as % of expected peak) | Throughput (RPS) | p95 (ms) | Error rate | Server CPU | DB connections in use |
|---|---|---|---|---|---|---|
| 1 | 100% | 43 | 790 | 0.3% | 45% | 8 of 20 |
| 2 | 125% | 54 | 850 | 0.4% | 56% | 10 of 20 |
| 3 | 150% | 65 | 1,100 | 0.9% | 69% | 14 of 20 |
| 4 | 200% | 85 | 2,900 | 3.5% | 88% | 20 of 20 (full) |
| 5 | 250% | 88 | 9,400 | 18% | 97% | 20 of 20 (full), requests waiting |
| 6 | 300% | 70 | timeouts | 55% | 99% | 20 of 20, many timeouts |
| Recovery (back to 100%) | 100% | 43 | 800 after 4 minutes | 0.3% after 4 minutes | 46% | 8 of 20 |

Reading it:

- Up to 150 percent, behaviour is orderly: response time and CPU rise slowly.
- Between 150 and 200 percent something changes: p95 nearly triples, the database connection pool fills up. This is the **knee** (explained next).
- At 250 and 300 percent throughput *stops growing and then falls*; the system is doing less useful work while receiving more demand. This is typical of overload.
- Recovery took about four minutes to return to baseline, which may or may not meet the agreed recovery target.
- The capacity within targets (p95 below 800 ms, errors below 1 percent) is somewhere around the first step or just above it; the margin is thin, which is an important finding.

#### 6.3 The response-time-versus-load graph

If you plot response time against load (users or RPS), healthy systems show a characteristic shape. We will draw one in ASCII.

```
Response
time
(ms)
  |
  |                                                  *
  |                                               *
  |                                           *     <- 4. Collapse:
  |                                       *            errors, timeouts,
  |                                    *               throughput falls
  |                                 *   <- 3. Saturation: queues build,
  |                              *         response time rises steeply
  |                          *
  |                     *  <- THE KNEE (about here)
  |     *   *   *   *
  |_*______________________  <- 1. Flat region: system is comfortable
  +------------------------------------------------------> Load (users or RPS)
       |                |                   |
    comfortable     approaching          overloaded
                    the limit
```

And throughput against the same load axis:

```
Throughput
(RPS)
  |                          ___________
  |                       __/           \___
  |                    __/                   \___   <- throughput falls in overload
  |                 __/
  |              __/       <- rises linearly while there is spare capacity
  |           __/
  |        __/
  |     __/
  |  __/
  +----------------------------------------------> Load (users or RPS)
                         ^
                    peak capacity
```

**The knee.** In the flat region, adding load barely changes response time because resources are free. Past a certain point, some resource saturates, requests start queueing, and each extra unit of load adds a disproportionate amount of waiting time. The point where the curve bends upward is the knee, and it is one of the most useful things a performance test can find. Operating comfortably *below* the knee is the goal; the safety margin is the distance between expected peak load and the knee.

The restaurant explains it perfectly. With four tables occupied in a ten-table room the waiter attends immediately. With nine tables occupied there is occasionally a wait. Once the room is full and a queue forms at the door, every additional party multiplies everyone's waiting. The kitchen did not become half as skilled; it simply ran out of free capacity.

#### 6.4 Identifying the bottleneck from the evidence

When you see the knee, ask: "What saturated first?" Check each resource at that moment:

- CPU near 100 percent on the application server suggests compute-bound code (or an inefficient algorithm).
- CPU low on the application server but response time climbing suggests that requests are waiting for something else: a database, a downstream service, a thread pool or a connection pool.
- Database connections all in use plus slow query log entries suggests a database bottleneck.
- Memory climbing steadily and garbage collection or swapping rising suggests memory pressure or a leak.
- Network at its bandwidth limit points to large payloads or insufficient bandwidth.

A very useful clue: **if response time grows but nothing looks busy, something is waiting**, usually on a lock, a pool, or a slow external call.

---

### 7. Common Bottlenecks and Where They Hide

This is a conceptual tour. You will not need to fix these today, but you should be able to recognise the vocabulary and symptoms when developers and performance engineers discuss them.

| Bottleneck | What it is | Typical symptom | Where it hides |
|---|---|---|---|
| Slow database queries | A query that scans a lot of data or does needless work | Response time rises with data size; database CPU or I/O high | Database; slow query log |
| N+1 query problem | Code fetches a list (1 query) and then runs one extra query for each item (N queries) instead of fetching everything in one go | Fine with 5 items, painful with 500; huge numbers of tiny queries | Application code that uses an ORM (object-relational mapper) |
| Missing index | The database has no "table of contents" for a column, so it reads every row to find a match | Lookups slow down as the table grows; volume tests expose it | Database schema (for example, searching by email without an index) |
| Thread pool exhaustion | The server has a fixed number of worker threads; all are busy or blocked, so new requests wait | Low CPU, high response time, requests timing out | Application server configuration |
| Connection pool exhaustion | All database connections are borrowed, so requests queue for one | Plateau in throughput; waiting rather than working | Application to database link |
| Memory leak | Memory is allocated and never released | Memory climbs during soak tests; eventual slowdown or crash | Application code or libraries |
| Third-party calls | Calls to an external service (email sender, identity provider, payment gateway) are slow or rate-limited | Specific transactions slow, others fine; delay does not scale with your CPU | Integrations |
| Network | Bandwidth limits, high round-trip delay, chatty communication | Large pages slow; many small calls add up | Between client, servers and services |
| Front-end assets | Large images, unminified scripts, too many requests, blocking scripts | Slow page load even when the server responds quickly | Browser; page design |
| Locks and contention | Many requests need to update the same row or resource, so they take turns | Throughput flat despite free CPU; rising waits | Database transactions; shared resources |
| Inefficient or expensive algorithms | Work grows much faster than the size of the input | CPU-bound slowdowns at larger data sizes | Application code |
| Garbage collection pauses | The runtime periodically pauses to clean up memory | Periodic latency spikes in the tail (p99) | Runtime memory settings |

**The N+1 problem, explained simply.** Imagine you are asked to list 100 users along with each user's country. A sensible approach asks the database once for "users joined with countries". An N+1 approach asks once for the 100 users and then 100 separate times for each user's country: 101 round trips. With a pool of limited connections and a network hop for each call, those 101 trips add up painfully. The code "works" in functional testing, because with five test users it is still fast; only load or volume reveals the problem.

**Missing index, explained simply.** A phone book is sorted by surname, so finding "Singh" is quick. If instead it were in random order, you would have to read every entry. Without an index, the database does the equivalent of reading every entry. For login, "find the account with this email" must be indexed or the cost grows with every new user registered.

**Important testing mindset.** As a tester you often do not fix the bottleneck. Your job is to find it, show evidence (graphs, resource data, which transaction), and describe it clearly enough that a developer can act. Saying "login is slow at 500 users; p95 climbs from 300 ms to 4 seconds while database connections hit the pool limit of 20" is a defect report developers love. Saying "the app is slow" is not.

---

### 8. Client-Side (Front-End) Performance, Briefly

So far we have focused on the *server*, handling many users. But there is another side: how fast a *single* page feels in one user's browser. A server can respond in 100 ms and the page may still take six seconds to appear if it downloads huge images and slow scripts. Front-end performance is mostly about what the browser has to download, process and draw.

Key ideas:

- **Page load time:** how long until the page is usable. It is affected by the size and number of resources (images, scripts, stylesheets), how they are compressed and cached, and whether scripts block the page from displaying.
- **Core Web Vitals:** a set of user-centred metrics published by Google as a standard way to describe real-world page experience. Know their names and one-line meanings:
  - **LCP (Largest Contentful Paint):** how long it takes for the largest main piece of content (a hero image or headline block) to appear. It measures *perceived loading speed*.
  - **INP (Interaction to Next Paint):** how quickly the page visually responds after the user interacts (taps, clicks, types). It measures *responsiveness*. (INP replaced an older metric called FID.)
  - **CLS (Cumulative Layout Shift):** how much the page jumps around unexpectedly while loading, such as a button moving just as you try to click it. It measures *visual stability*.
- **Lighthouse:** a free tool built into Chrome's developer tools (and available as a command-line tool) that audits a page and reports scores and suggestions for performance, accessibility, best practices and SEO. It is an excellent first look at front-end performance with no setup.
- **Browser DevTools Network tab:** shows every request a page makes, how large each is and how long each took, in a waterfall chart. It is the best way to see why a page is slow, and the best way to count requests for your workload model (as we did earlier).

Server-side load tests simulate *requests*, not browsers, so they do not measure rendering. Front-end checks and server load tests complement each other: one asks "is the page well built?", the other asks "does the back end hold up under many users?" A complete performance strategy considers both.

---

### 9. Tools Overview (and Honest Guidance)

You do not need to learn any of these today. Detailed tool setup, scripting and analysis come in later courses within this programme. For now, it is enough to recognise the names and understand what each is for.

**Load generation tools**

| Tool | One-line description | Notes |
|---|---|---|
| Apache JMeter | A long-established, free, open-source tool with a graphical interface for building load tests; widely used and widely asked about in interviews | Heavier on resources; tests stored as XML files |
| Gatling | Open-source load tool where scenarios are written as code, known for efficient resource use and good reports | Code-centric |
| k6 | Open-source tool where tests are written in JavaScript, designed for developers and pipelines, with built-in thresholds | Friendly to CI/CD |
| Locust | Open-source tool where user behaviour is written in plain Python | Easy for Python learners |
| Artillery | Open-source tool configured with YAML and JavaScript, popular for API and web socket testing | Quick to start |
| BlazeMeter | A commercial cloud platform that runs JMeter, Gatling, k6 and other tests at large scale, with reporting | Hosted service |
| LoadRunner | A long-established commercial enterprise tool, still found in large organisations | Licensed product |

**Front-end analysis tools**

| Tool | One-line description |
|---|---|
| Lighthouse | Audits page performance and gives scored recommendations |
| Browser DevTools Network tab | Shows each request, size and timing in a waterfall |

**Monitoring and observability tools (names only)**

| Tool | One-line description |
|---|---|
| Prometheus | Collects and stores time-series metrics from servers and applications |
| Grafana | Draws dashboards and graphs from metrics sources such as Prometheus |
| APM (Application Performance Monitoring) tools | Products that trace requests through an application and show where time is spent; examples include Datadog, New Relic and Dynatrace |

**Honest guidance.**

- The tool matters less than the thinking. Workload models, realistic data, percentiles and monitoring are the same whichever tool you use.
- Pick based on your team's skills and ecosystem: Python teams may like Locust, JavaScript teams k6, Java teams Gatling or JMeter, and large enterprises may already own LoadRunner or BlazeMeter.
- Learn one properly and the others become easy.
- Tools are changing quickly; always check current official documentation rather than relying on old tutorials.

---

### 10. Hands-On: A Safe, Local Mini Load Test in Python

This section lets you *see* load, latency, percentiles and saturation with your own eyes, using only the Python standard library. You do not install anything.

#### 10.1 Ethics and legal safety: read before running

> **WARNING. Only run load or stress tests against systems you own or have explicit, written permission to test.**
>
> The script in this lesson only talks to `127.0.0.1`, which is *your own computer*, and it starts its own tiny server inside the same program. **Never point a load testing script, even a small one, at a third-party website, a public API, a school or employer system, or any server you do not own, without written permission from the owner.**
>
> Generating heavy traffic against systems without authorisation can be treated as an attack (a denial-of-service or DoS attack). It can breach terms of service and computer misuse laws, get your network address blocked, and have serious professional and legal consequences. "I was only testing" is not a defence. Even with permission, agree timing, limits and a contact person in advance, and test against a test environment wherever possible, not live production.

Professional performance testers always have a written scope, sign-off and a rollback plan for exactly this reason.

#### 10.2 What the program does

1. Starts a tiny web server in a background thread inside the same script. Port 0 asks the operating system to pick any free port, so there is no clash with other programs.
2. The server pretends to have a **database with only 4 connections** (a semaphore, a counter that allows only 4 holders at once). Each request needs 20 ms of "database time". So at most 4 requests can be processed at once, and the maximum capacity is about 4 / 0.020 = 200 requests per second. Extra requests wait in a queue, exactly like real connection pool exhaustion.
3. Runs a **load test** with a ramp of 5, 20 and 50 virtual users on the `/login` endpoint and prints average, p50, p95, p99, throughput and error rate.
4. Runs a **stress test** on the `/limited` endpoint. This endpoint gives up and returns HTTP 503 (Service Unavailable) if it has to wait more than 150 ms for a database connection. We increase to 100 users to push past capacity.

#### 10.3 The code

Save this as `mini_load_test.py` somewhere *outside* your project's test folders (for example, a scratch or practice folder) and run it with `python mini_load_test.py` (or `python3` on some systems). It needs Python 3.8 or later.

```python
"""Mini load test against our OWN local server only (127.0.0.1)."""
import threading, time, urllib.request, urllib.error, statistics
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_POOL = threading.BoundedSemaphore(4)   # pretend database: 4 connections
WORK_TIME = 0.02                          # each request needs 20 ms of "database" time

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):         # keep the console quiet
        pass
    def do_GET(self):
        if self.path == "/login":
            with DB_POOL:                 # wait here if all 4 connections are busy
                time.sleep(WORK_TIME)
            self.send_response(200)
        elif self.path == "/limited":
            got = DB_POOL.acquire(timeout=0.15)   # give up waiting after 150 ms
            if not got:
                self.send_response(503)           # "Service Unavailable"
                self.end_headers()
                return
            try:
                time.sleep(WORK_TIME)
            finally:
                DB_POOL.release()
            self.send_response(200)
        else:
            self.send_response(404)
        self.end_headers()
        self.wfile.write(b"ok")

def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]

def one_request(url):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            ok = resp.status == 200
    except (urllib.error.URLError, OSError):
        ok = False
    return time.perf_counter() - start, ok

def virtual_user(url, n, think):
    results = []
    for _ in range(n):
        results.append(one_request(url))
        time.sleep(think)
    return results

def percentile(sorted_vals, p):
    k = max(0, min(len(sorted_vals) - 1, int(round(p / 100 * len(sorted_vals) + 0.5)) - 1))
    return sorted_vals[k]

def run_step(url, users, n=15, think=0.05):
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=users) as pool:
        futures = [pool.submit(virtual_user, url, n, think) for _ in range(users)]
        samples = [s for f in futures for s in f.result()]
    elapsed = time.perf_counter() - t0
    times = sorted(t * 1000 for t, _ in samples)
    errors = sum(1 for _, ok in samples if not ok)
    print(f"{users:>5} {len(samples):>6} {statistics.mean(times):>8.1f} "
          f"{percentile(times,50):>7.1f} {percentile(times,95):>7.1f} "
          f"{percentile(times,99):>7.1f} {len(samples)/elapsed:>9.1f} "
          f"{100*errors/len(samples):>7.1f}%")

HEADER = "Users Reqs  Avg(ms) p50(ms) p95(ms) p99(ms)  Req/sec  Errors"
if __name__ == "__main__":
    server, port = start_server()
    base = f"http://127.0.0.1:{port}"
    print("LOAD TEST: /login (requests queue politely)")
    print(HEADER)
    for users in (5, 20, 50):
        run_step(base + "/login", users)
    print("\nSTRESS TEST: /limited (server gives up after 150 ms of waiting)")
    print(HEADER)
    for users in (5, 20, 50, 100):
        run_step(base + "/limited", users, n=15)
    server.shutdown()
```

#### 10.4 Line-by-line explanation

**The imports**
- `threading` lets us run code in the background and provides the semaphore.
- `time` provides `sleep` (pause) and `perf_counter` (a high-resolution stopwatch ideal for measuring short durations).
- `urllib.request` and `urllib.error` let Python make HTTP requests without installing anything.
- `statistics` provides `mean`.
- `ThreadPoolExecutor` runs many functions at the same time using a pool of threads; each thread plays one virtual user.
- `BaseHTTPRequestHandler` and `ThreadingHTTPServer` build a simple web server; "Threading" means each incoming request is handled in its own thread so several can be in progress at once.

**The fake database**
- `DB_POOL = threading.BoundedSemaphore(4)` creates a counter that starts at 4. Each time code "acquires" it, the counter goes down; when the counter is 0, anyone else trying to acquire it must wait. "Releasing" adds one back. This models a connection pool with four connections.
- `WORK_TIME = 0.02` is how long each request holds a connection: 20 milliseconds.

**The request handler**
- `class Handler(BaseHTTPRequestHandler)` defines how our server reacts to requests.
- `log_message` is overridden to do nothing, because by default the server prints a line for every request, which would flood the screen.
- `do_GET` is called automatically for every HTTP GET request. `self.path` holds the address requested.
- For `/login`: `with DB_POOL:` acquires a connection (waiting as long as necessary), runs the indented block, and automatically releases afterwards. Inside it, `time.sleep(WORK_TIME)` pretends to do 20 ms of database work. Then the server sends status 200 (OK).
- For `/limited`: `DB_POOL.acquire(timeout=0.15)` tries to get a connection but only waits up to 0.15 seconds (150 ms). It returns `True` if it got one and `False` if it gave up. If it gave up, the server sends status 503 and returns early. If it got one, it does the work inside `try`, and `finally` guarantees the connection is released even if something goes wrong.
- For any other path, the server sends 404 (Not Found).
- Finally `end_headers()` finishes the response headers and `wfile.write(b"ok")` sends a tiny body.

**Starting the server**
- `ThreadingHTTPServer(("127.0.0.1", 0), Handler)` creates a server bound to the local machine only (127.0.0.1 is never reachable from outside your computer) on port 0 (any free port).
- `daemon_threads = True` makes sure leftover request threads do not stop the program from exiting.
- `threading.Thread(target=server.serve_forever, daemon=True).start()` runs the server loop in the background so the rest of the script can continue.
- We return the server object and the chosen port number.

**One request, timed**
- `time.perf_counter()` is called before and after the request to compute the elapsed seconds.
- `urlopen(url, timeout=2)` sends the request, waiting at most two seconds.
- If the server responds, `ok` is whether the status was 200. If the connection fails or times out, we catch the exception and mark `ok = False`.
- It returns a pair: how long it took and whether it succeeded.

**A virtual user**
- `virtual_user` makes `n` requests in a loop, sleeping `think` seconds (50 ms) between them. That sleep is our **think time**. It collects and returns all results.

**Percentile function**
- `percentile` implements the nearest-rank idea on an already sorted list. It converts `p` percent to a position in the list, rounds it, and guards against going outside the list bounds. (Real tools may use slightly different formulas; this one is good enough to teach the concept.)

**Running one step of the ramp**
- `run_step` starts a stopwatch, creates a thread pool with `users` workers, and submits one `virtual_user` job per user. Each job runs concurrently.
- `f.result()` waits for each job to finish and gets its list of results; the list comprehension flattens everyone's results into one list called `samples`.
- `elapsed` is the total wall-clock time, used to calculate throughput (samples divided by seconds).
- `times` converts seconds to milliseconds and sorts them (percentiles need sorted data).
- `errors` counts failed samples.
- The `print` line formats a row: users, number of requests, average, p50, p95, p99, requests per second and error percentage.

**Main program**
- Start the server and build the base address.
- The load test loops over 5, 20 and 50 users against `/login`.
- The stress test loops over 5, 20, 50 and 100 users against `/limited`.
- `server.shutdown()` stops the server cleanly.

#### 10.5 Genuine output

This is real output from running the script on the machine used to prepare this lesson:

```
LOAD TEST: /login (requests queue politely)
Users Reqs  Avg(ms) p50(ms) p95(ms) p99(ms)  Req/sec  Errors
    5     75     27.6    21.7    99.4   120.2      63.2     0.0%
   20    300     59.3    21.7    53.8  1241.9     129.3     0.0%
   50    750    184.6   199.4   206.6  1203.5     188.7     0.0%

STRESS TEST: /limited (server gives up after 150 ms of waiting)
Users Reqs  Avg(ms) p50(ms) p95(ms) p99(ms)  Req/sec  Errors
    5     75     21.9    21.5    23.2    39.1      68.2     0.0%
   20    300     51.7    51.2    55.3    93.7     190.0     0.0%
   50    750    150.8   151.1   171.5  1176.8     210.1     9.2%
  100   1500    174.8   152.4   172.0  1191.9     344.8    46.1%
```

**Your numbers will differ.** They depend on your processor, operating system, how busy your machine is and the Python version. That is normal and is itself a lesson: performance numbers are specific to an environment, which is exactly why baselines and production-like test environments matter. The *patterns* should be similar: latency rising with users, throughput flattening near 200 requests per second, and errors appearing in the stress run.

#### 10.6 How to read this output

**The load test (`/login`).**

- With 5 users, almost every request takes about 21 to 22 ms (p50 = 21.7 ms), which is the 20 ms of "database" work plus tiny overhead. The pool has four connections and only five users with think time, so there is almost no waiting.
- With 20 users, the median is still about 21.7 ms but the average has risen to 59.3 ms. The throughput roughly doubled (129 requests per second), showing the system still has spare capacity, but the *tail* is starting to show.
- With 50 users, the median jumps to 199 ms, about ten times higher. Throughput is 188.7 requests per second, close to the theoretical ceiling of 200 (4 connections / 0.020 seconds). We have reached **saturation**: more users no longer produce more throughput; they only produce longer queues. That is the knee in action, and the connection pool is our bottleneck, exactly what a performance engineer would identify.
- Notice the **averages versus percentiles** story. In the 20-user row, the p95 is 53.8 ms (comfortable) but the p99 is 1,241.9 ms. A tiny percentage of requests took over a second, which the average of 59.3 ms did not reveal. In both the 20-user and 50-user rows, p99 is more than 1,200 ms, even though p50 and p95 look acceptable at 20 users. A p99 near 1.2 seconds on a quiet local machine suggests something other than our simulated database. A plausible explanation (we did not prove it here) is that when many threads open new connections at the same instant, a few connection attempts are delayed by the operating system's connection handling, which is a typical cause of "mysterious" slow tails. This is a good real-world reminder: **investigate outliers rather than ignoring them, and be careful about claiming causes you have not verified.** In real projects you would repeat the run, then check server logs and network statistics before concluding.
- The 5-user row has a surprisingly high p95 (99.4 ms) compared with its median (21.7 ms). With few samples (75), a handful of slow first-time requests, such as establishing the very first connections and starting threads, lifts the tail. This is a **warm-up effect**. It is why we discard the early part of a test and why small sample sizes make percentiles noisy.

**The stress test (`/limited`).**

- With 5 and 20 users, no errors; latency grows modestly.
- With 50 users, 9.2 percent of requests fail. The server is giving up after waiting 150 ms for a connection, so those failures complete at about 150 ms. Notice the median is 151 ms, right at the give-up limit: a large portion of requests are now either waiting nearly 150 ms and succeeding or waiting 150 ms and being rejected.
- With 100 users, 46.1 percent fail. The system is overloaded and sheds load by rejecting requests.
- **Look at the throughput column:** it *rises* to 344.8 requests per second at 100 users, even though the real capacity is about 200. Why? Because failed requests are cheap: the server rejects them quickly. The counter counts all requests including failures, so raw throughput looks impressive while the service is actually failing nearly half its users. **Always look at throughput together with the error rate, and count successful requests for useful throughput.** In this run, successful throughput at 100 users is about 344.8 x (1 - 0.461) = approximately 186 successful requests per second, in line with the real ceiling.
- This is a small model of what a stress test reveals: how the system behaves *past* its limits. Here it fails in a fairly graceful way, returning clear 503 responses quickly instead of hanging. (Contrast with the `/login` endpoint, which just queues politely and gets slower and slower.)

**Experiments to try (still local only).**

1. Change `DB_POOL = threading.BoundedSemaphore(4)` to 8. Predict what happens to the knee, then run again. (Capacity should roughly double, since 8 / 0.020 = 400 per second.)
2. Change `WORK_TIME` to `0.05`. Predict the new ceiling (4 / 0.05 = 80 per second) and check.
3. Set `think` to `0` and observe what happens to load without think time.
4. Increase the 150 ms wait in `/limited` to 1 second and see how failures turn into long waits instead.

For each, write your prediction *before* running. Predicting then checking is how intuition about performance is built.

#### 10.7 For later weeks: the same idea in Locust (not run here)

The following is a tiny **Locust** file, shown only so you can recognise what a real tool script looks like. Do not run it today; Locust is not installed in this course yet, and it must only ever be pointed at systems you own or have written permission to test. Tool setup comes in later courses.

```python
# locustfile.py  -- FOR LATER WEEKS (not run in this lesson)
from locust import HttpUser, task, between

class LoginUser(HttpUser):
    wait_time = between(1, 3)          # think time: pause 1 to 3 seconds between tasks
    host = "http://localhost:8000"     # your OWN test system only

    @task(7)                           # weight 7: runs seven times as often as weight 1
    def login(self):
        self.client.post("/api/login",
                         json={"email": "user1@example.com", "password": "Passw0rd!"})

    @task(1)                           # weight 1
    def view_profile(self):
        self.client.get("/api/profile")
```

What it expresses:
- `HttpUser` is a virtual user that makes HTTP requests; each simulated user is an instance of this class.
- `wait_time = between(1, 3)` is randomised think time.
- `@task(7)` and `@task(1)` express a workload mix: roughly 7 out of every 8 actions are logins and 1 in 8 is a profile view, which is the same idea as the percentages in our workload model.
- `self.client` is a tracked HTTP session that records response times and failures for the report.

You would start it with a command such as `locust` and choose the number of users and the spawn (ramp-up) rate in its web page. For now, simply notice how much of the *thinking* (think time, mix, ramp) matches what you already know.

---

### 11. Performance Testing in CI/CD and Shift-Left

In Monday's lessons you met the SDLC, agile delivery and the idea of testing early. This applies to performance too.

**Shift-left for performance.** Waiting until the end of a project for performance testing is risky: if a fundamental design problem (a chatty design, a missing index, an inefficient approach) is discovered one week before launch, fixing it is costly and stressful. **Shifting left** means thinking about performance from the start:

- Write performance requirements alongside functional ones during requirements analysis.
- Review designs for obvious risks (for example, "this screen loads every user record").
- Developers run quick checks on their own machines and measure query times.
- Run small performance tests on early builds, not just at the end.

**In the CI/CD pipeline.** A continuous integration and delivery pipeline builds, tests and deploys software automatically on every change. Performance checks fit into that rhythm in tiers:

| Pipeline stage | Performance activity | Why |
|---|---|---|
| Every commit or build | Smoke performance test: a few virtual users for one to two minutes against a test deployment, with a few strict checks | Fast early warning that something is badly slower |
| Every build (cheap checks) | Unit-level timing checks or "performance budgets" | Catches regressions in key functions or page weight early |
| Nightly or scheduled | Fuller load test at expected peak, results compared with the previous baseline | Detects gradual slowdowns without delaying developers |
| Weekly or before major releases | Stress, spike, soak and volume tests on a production-like environment | These take hours and need a dedicated environment |
| After deployment | Monitoring dashboards and alerts in production | Real users are the ultimate load test; alerts catch what tests missed |

**Performance budgets.** A *budget* is a limit on a performance measure that the build must not exceed, for example "login p95 at most 800 ms in the smoke test", "home page transfers at most 1.5 MB", or "Lighthouse performance score at least 80". If the budget is exceeded, the pipeline fails or warns, just like a failing functional test. Budgets stop performance from eroding one small change at a time.

Here is a small illustration of a budget, expressed as a k6 script with **thresholds**. It is shown for recognition only; k6 setup is a later topic, and as always it targets only your own test system.

```javascript
// smoke-performance.js  -- FOR LATER WEEKS (not run in this lesson)
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,                 // five virtual users
  duration: '1m',         // for one minute
  thresholds: {
    http_req_failed: ['rate<0.01'],      // fewer than 1% of requests may fail
    http_req_duration: ['p(95)<800'],    // 95% of requests must finish within 800 ms
  },
};

export default function () {
  const res = http.get('http://localhost:8000/login');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);               // think time
}
```

If either threshold is breached, k6 reports the test as failed and returns a non-zero exit code, so a pipeline can automatically fail the build.

**Cautions for CI/CD performance tests.**
- Shared pipeline machines are noisy; use generous margins or relative comparisons against a recent baseline to avoid flaky failures.
- Keep the fast checks fast; push the heavy tests to nightly or scheduled runs.
- Version your test scripts with the code, just like functional automation.
- Keep results history so trends are visible.

---

### 12. AI-Assisted Performance Analysis: Realistic Expectations

AI tools can help a performance tester, but they are assistants, not oracles. Here is a realistic view.

**Where AI can genuinely help**

- **Drafting:** producing first drafts of test plans, scenario tables, workload model calculations and script skeletons (for example a Locust or k6 file) that you then review and correct.
- **Explaining:** summarising what a metric means, or explaining an unfamiliar error message or configuration option.
- **Analysis support:** reading exported result tables, spotting patterns (such as p99 climbing while p50 stays flat), proposing hypotheses about bottlenecks and suggesting what to check next.
- **Log and trace summarisation:** condensing large volumes of logs or slow-query output into themes.
- **Anomaly detection:** many monitoring products use machine learning to flag unusual metric patterns or compare a run to historical runs.
- **Generating test data:** creating varied, realistic-looking fake users and inputs.

**Cautions**

1. **Hypotheses are not findings.** An AI may confidently suggest "the bottleneck is the database index". That is a *lead* to verify with evidence, not a conclusion. Always confirm using monitoring data and a controlled retest.
2. **AI can invent details.** Generated scripts may use options that do not exist, wrong syntax, or statistics that sound plausible but are made up. Run and review everything; check against official documentation.
3. **Garbage in, garbage out.** If the workload model or data you feed it is unrealistic, the analysis will be too.
4. **Privacy and confidentiality.** Do not paste real customer data, secrets, internal URLs or confidential results into external AI tools unless your organisation's policy allows it. Use sanitised or synthetic data.
5. **No substitute for understanding.** If you do not understand percentiles, saturation and queueing, you cannot judge whether the AI's explanation is right. This lesson's vocabulary is what lets you ask better questions and catch mistakes.
6. **Safety.** Never let an AI tool (or an AI-generated script) run load against any system without your explicit check of the target. A wrong target address in a generated script is an easy and serious mistake.

A good prompt to an AI assistant is specific: give the context (the application, the load model, the result table), ask for hypotheses ranked by likelihood together with the evidence that would confirm or rule out each, and then go and gather that evidence yourself.

---

### 13. Test Environment and Test Data Pitfalls

Many performance testing efforts fail not because of the tool but because of the environment and data.

**Environment pitfalls**

- **Non-representative size.** Testing on a single small server when production has several large ones, then trying to extrapolate. Performance does not scale linearly, so extrapolation is unreliable. If the environment is smaller, say so in the report and treat results as relative, not absolute.
- **Different configuration.** Different database settings, pool sizes, software versions, or missing a load balancer, can change behaviour completely.
- **Shared environment noise.** Other teams' deployments or tests running at the same time distort your results. Book exclusive time.
- **Stubbed or missing dependencies.** If a third-party service is replaced with an instant fake, results may be too optimistic; if it is real, you may be generating load on someone else's system. Agree how to handle each integration (use a realistic simulator with realistic delays, or a vendor-provided test sandbox with permission).
- **Cold versus warm state.** Make sure that caches and connection pools are in a known state, and document it.
- **Load generators as the limit.** If the machine producing the load is overloaded or on a weak connection, you measure *its* limit, not the system's.

**Data pitfalls**

- **Too little data.** A database with 100 rows hides missing-index and volume problems.
- **Unrealistic distribution.** If every virtual user logs in as the same account, caching makes things look unrealistically fast, and locking on a single row makes things look unrealistically slow. Use a pool of many distinct, realistic accounts.
- **Data that is used up.** Registration tests need *new, unique* emails every time. Duplicate emails cause validation errors that look like failures. Generate unique data per virtual user and iteration.
- **Data that is not reset.** After a run, leftover records affect the next run. Plan clean-up or restore from a snapshot to keep tests repeatable.
- **Privacy.** Do not copy real personal data into test environments without anonymising it. Prefer synthetic data, in line with privacy law and company policy.
- **Wrong password policies or locked accounts.** Repeated failed logins may lock test accounts; account for lockout rules in your scenarios.

---

### 14. Common Mistakes

| Mistake | Why it hurts | Better practice |
|---|---|---|
| Testing on a non-representative environment | Results do not predict production behaviour | Make it production-like, or clearly label the differences |
| Judging by averages only | Hides the slow tail that real users feel | Report p50, p90, p95, p99 and error rate |
| No think time | Creates far more load per user than reality; results are meaningless | Model realistic, randomised think times |
| Unrealistic scripts | Same user, same data, no variety, no dynamic values handled | Parameterise data, handle sessions, mix journeys |
| Testing only the happy path | Real traffic includes failed logins, validation errors, password resets | Include negative and edge journeys in the mix (your Wednesday lesson applies here too) |
| Not monitoring the server | You know it is slow but not why | Monitor CPU, memory, disk, network, database, application metrics |
| Running load from a laptop on Wi-Fi | The laptop or the wireless network becomes the bottleneck and adds noise | Use dedicated load generators on a stable network close to the target, and monitor the generators too |
| Measuring during ramp-up | Numbers are distorted by changing load and warm-up | Measure the steady state only |
| Changing many things between runs | You cannot tell what caused a change | Change one thing at a time and keep a log |
| Running a single test and trusting it | Results vary run to run | Repeat key runs and look for consistency |
| Ignoring errors | Fast errors look like good performance | Always check error rate and response correctness |
| Starting too late | Fundamental design problems are costly to fix | Shift left; test early and often |
| Testing against systems you do not own | Legal and ethical violations; can look like an attack | Own or have written permission, agree limits |
| Treating the result as eternal | Code, data and infrastructure change | Re-baseline regularly and monitor in production |

---

## Examples

### Example 1: A complete performance test plan and scenario table for Project 1 (Login and Registration)

This example gives you a complete model of what a performance test plan fragment looks like for Project 1. The numbers connect to the workload model above. You can use it as a template for your own test design document and regression/risk plan.

**Performance requirements (NFRs) for Project 1**

| ID | Requirement | Measure | Target |
|---|---|---|---|
| NFR-P-01 | Login responsiveness | p95 response time of the "Submit login" transaction at expected peak load | Less than or equal to 800 ms |
| NFR-P-02 | Registration responsiveness | p95 response time of "Submit registration" at expected peak load | Less than or equal to 1,500 ms |
| NFR-P-03 | Login page load | p95 response time of "Open login page" at expected peak | Less than or equal to 500 ms |
| NFR-P-04 | Error rate | Failed requests across all scenarios during steady state | Less than 1% |
| NFR-P-05 | Capacity headroom | System sustains 150% of expected peak while meeting NFR-P-01 and NFR-P-04 | Yes |
| NFR-P-06 | Resource usage | Application server CPU at expected peak | Less than or equal to 70% average |
| NFR-P-07 | Stability | Memory trend over an 8-hour soak | No sustained upward trend; end within 10% of the hour-1 level |
| NFR-P-08 | Recovery | Time to return to baseline response time and error rate after overload ends | Within 5 minutes without manual restart |
| NFR-P-09 | Data volume | Login p95 with 2 million accounts compared with 1,000 accounts | Within 10% |
| NFR-P-10 | Front-end | Lighthouse performance score of login page on a standard desktop profile; LCP | Score at least 80; LCP at most 2.5 seconds (as an agreed project target) |

(The LCP figure follows the commonly published "good" threshold; confirm the current value on the web.dev page listed in the Additional Resources section before adopting it.)

**Scenario table**

| Scenario ID | Test type | Journey and workload | Load shape | Duration | Environment and data | Acceptance criteria | Monitoring |
|---|---|---|---|---|---|---|---|
| PT-01 | Smoke performance | Login and registration, 5 VUs, realistic think time | Flat, 5 VUs | 2 min | Test environment; 50 prepared accounts | 0% errors; p95 of all transactions below 1.5 s; scripts verified | Test tool output; app logs |
| PT-02 | Baseline | Standard mix (70/15/10/5) at 10% of expected peak (0.5 journeys/s) | Ramp 2 min, steady 15 min | 20 min | Production-like env; 10,000 accounts | Record p50, p90, p95, p99, RPS, CPU, memory; stored as the release baseline | CPU, memory, DB connections |
| PT-03 | Load | Standard mix at expected peak: 5 journeys/s (about 43.5 RPS) | Ramp 5 min, steady 30 min, ramp-down 5 min | 40 min | Production-like env; 200,000 accounts; unique emails for registration | NFR-P-01 to P-04 and P-06 met in steady state; no single transaction exceeds its target | App server and DB metrics; error logs |
| PT-04 | Load (headroom) | Standard mix at 150% of expected peak: 7.5 journeys/s (about 65 RPS) | Ramp 5 min, steady 20 min | 30 min | As PT-03 | NFR-P-01 and P-04 met (NFR-P-05) | As PT-03 |
| PT-05 | Capacity | Standard mix, step up 10% per step from 100% until p95 login exceeds 800 ms or errors exceed 1% | Staircase, 5 min per step | Up to 60 min | As PT-03 | Report highest compliant load (capacity) and the resource that saturated first; capacity at least 150% of expected peak | Full monitoring |
| PT-06 | Stress | Login-heavy mix, step to 200%, 300%, 400% of expected peak, then back to 100% | Staircase to failure, then drop | 60 min | As PT-03 | No data corruption (no partial accounts); errors are fast and clear (503 or friendly message), no hangs beyond the timeout; breaking point at least 2x expected peak; recovery within 5 min (NFR-P-08) | Full monitoring; DB integrity check afterwards |
| PT-07 | Spike | Normal 2 journeys/s jumping to 20 journeys/s for 2 minutes, then back | Sharp spike | 15 min | As PT-03 | No crash; errors below 5% during spike; return to baseline within 2 min | Full monitoring |
| PT-08 | Soak | Standard mix at 60% of expected peak | Flat | 8 hours | As PT-03 | NFR-P-07 met; error rate below 1% throughout; DB connections stable | Memory, connections, response time trend |
| PT-09 | Volume | Standard mix at 50% of expected peak after loading 2 million accounts; plus admin export of all users | Flat | 30 min plus export | Production-like env; 2 million accounts | NFR-P-09 met; export completes within 15 minutes without errors | DB metrics (slow queries, disk I/O) |
| PT-10 | Front-end check | Lighthouse audit and DevTools network review of login and registration pages | Single user | 10 min | Test environment | NFR-P-10 met; page weight and request count recorded | Lighthouse report |
| PT-11 | Regression (performance) in CI | PT-01 style smoke on every build; PT-03 nightly | Per above | Per above | Test environment | Smoke: p95 login at most 800 ms and 0% errors; nightly: p95 worse than previous baseline by no more than 10% | Pipeline reports; trend dashboard |

Several things to notice as a reviewer of this plan:

- Every row has a *measurable* acceptance criterion; none says "should be fast".
- It combines several types because each answers a different question.
- It follows the recommended order: smoke, baseline, load, then capacity and stress, with soak and volume as longer special runs.
- The data requirements are explicit (unique emails, volumes).
- Recovery and data integrity are checked in the stress test, not just speed.

### Example 2: Why the average hid the problem

A team reports "average login time is 450 ms, target is 800 ms, we pass." The raw data for a 10-request sample is, in milliseconds: 180, 190, 200, 210, 220, 230, 240, 250, 260, 2,720.

- Sum = 180 + 190 + 200 + 210 + 220 + 230 + 240 + 250 + 260 + 2,720 = 4,700. Average = 470 ms.
- Median = (220 + 230) / 2 = 225 ms.
- p90 (rank = 0.90 x 10 = 9, ninth value) = 260 ms.
- Maximum = 2,720 ms.

The average is below 800 ms, but one in ten users waited nearly three seconds. For a real system with thousands of users, that is hundreds of people having a poor experience every minute. An agreed target stated as "p95 at most 800 ms" would have caught this when the sample grows large enough.

### Example 3: Classifying a described test

A test engineer describes: "We start with 10 virtual users, add 10 more every 5 minutes until the login page begins returning errors at 130 users. Then we cut back to 10 users and check how long it takes for error messages to stop."

Classification: **stress test** (staircase beyond limits, finds breaking point, observes recovery). It is not a load test because the load goes beyond expected levels and the purpose is to find a limit. It is not a spike test because the load increases in steps rather than suddenly.

---

## Try It: Project 1 Performance Activity

This activity ties the lesson to your Project 1 test-design document and regression and risk plan. You will work in your own files and (optionally) in a local scratch folder. No external system is touched.

**Part A: Measure what you can see (about 15 minutes)**

1. Open the Project 1 login page in your browser. Open Developer Tools and select the **Network** tab. Reload the page.
2. Record: how many requests the page made, the total size transferred, and the total load time shown.
3. Pick the slowest three requests and note what they are (script, image, API call).
4. If your browser has Lighthouse in DevTools, run a performance audit and record the score, LCP and any top suggestion.

Write three or four sentences interpreting what you found. Would this be a front-end or back-end concern?

**Part B: Build your workload model (about 25 minutes)**

1. Choose your own peak journeys per minute for Project 1 (use 300 if you wish to match the lesson, or pick your own assumption and justify it).
2. Create a journey mix table with percentages that add to 100 for at least four journeys.
3. Using your measurements from Part A (or assumptions), assign requests per journey and compute the weighted average requests per journey, then the peak RPS.
4. Add a headroom factor and compute the target RPS.
5. Estimate journey durations and use Little's Law to compute the concurrent users.
6. Write down the ramp-up, steady-state and ramp-down you would use.

**Part C: Complete the performance section of your design document (about 30 minutes)**

1. Write at least five measurable performance NFRs for Project 1 (response time percentile, error rate, capacity headroom, stability, recovery).
2. Create a scenario table with at least six scenarios covering smoke, baseline, load, stress, spike and soak, including acceptance criteria, data needs and monitoring for each.
3. In your risk plan, add at least three performance risks (for example, "login p95 exceeds target at peak", "registration duplicate-email check slow with large data", "password hashing saturates CPU") with likelihood, impact and the test that mitigates each.
4. In your regression plan, state which performance checks run on every build, nightly and before release.

**Part D: Run the local mini load test (about 20 minutes, optional but recommended)**

1. Save and run the Python script from this lesson on your own machine (local only).
2. Capture your output table.
3. Do experiment 1 or 2 from the experiments list, writing your prediction first.
4. In two or three sentences, describe where the knee was and which resource (in the simulation: the connection pool) was the bottleneck.

**Reflection questions**

- Which of your journeys is the heaviest for the server? Why?
- If you could only run one performance test before launch, which would it be and why?
- What could make your test results misleading?

---

## Practice Exercises

### Exercise 1: Compute percentiles

Here are 20 login response times in milliseconds, in the order they were recorded:

`120, 135, 110, 150, 125, 140, 130, 145, 115, 160, 155, 170, 128, 132, 138, 900, 142, 148, 135, 2500`

Calculate: (a) the average, (b) the median, (c) p90, (d) p95, (e) p99. Use the nearest-rank method for the percentiles. Then explain which number you would put in a report and why.

### Exercise 2: Design a workload model

Project 2 (a different sample app) expects 600 journeys per minute at peak: 60 percent "browse and log in", 25 percent "register", 10 percent "invalid login" and 5 percent "password reset". Requests per journey are 12, 9, 3 and 4 respectively. Average journey durations are 300, 150, 30 and 60 seconds respectively.

Compute: (a) journeys per second for each journey type; (b) the weighted average requests per journey; (c) peak RPS; (d) target RPS with 40 percent headroom; (e) the weighted average duration and the concurrent users using Little's Law.

### Exercise 3: Classify the test

Classify each description as load, stress, spike, soak, volume or smoke performance test, and justify:

1. "Fifty users log in steadily for 12 hours; we watch memory use."
2. "At exactly 09:00 the number of users jumps from 20 to 2,000 for three minutes."
3. "Three users run through login for 90 seconds to confirm the new script and environment are working."
4. "We load 10 million customer records and time the search and the nightly export."
5. "Users ramp to the expected 800 concurrent users and hold for 30 minutes, with a p95 target of 800 ms."
6. "We keep adding 100 users every 10 minutes until errors exceed 20 percent, then stop and watch recovery."

### Exercise 4: Identify the bottleneck from a described graph

A load test of the Project 1 login produces these observations as load increases:

| Users | p95 (ms) | Throughput (RPS) | App server CPU | DB connections in use (pool size 30) | DB CPU |
|---|---|---|---|---|---|
| 100 | 300 | 40 | 25% | 8 | 20% |
| 200 | 320 | 80 | 40% | 15 | 35% |
| 300 | 400 | 118 | 55% | 24 | 50% |
| 400 | 1,500 | 125 | 60% | 30 (full) | 55% |
| 500 | 4,800 | 124 | 62% | 30 (full) | 56% |
| 600 | 9,500 (with timeouts) | 110 | 63% | 30 (full) | 55% |

(a) Where is the knee? (b) What is the most likely bottleneck, and what evidence supports it? (c) What would you try first, and how would you confirm it worked? (d) Why would buying a bigger application server probably not help?

### Exercise 5: Spot the flaws

A colleague describes their test: "I ran the login test from my laptop over Wi-Fi against the shared dev server while other teams were deploying. I used 1 test user, no think time, 500 threads, and the average came out at 200 ms, so we pass." List at least six problems.

---

## Answer Keys

### Answer to Exercise 1

**Sorted list (20 values):** 110, 115, 120, 125, 128, 130, 132, 135, 135, 138, 140, 142, 145, 148, 150, 155, 160, 170, 900, 2500

**Sum:** 110 + 115 + 120 + 125 + 128 + 130 + 132 + 135 + 135 + 138 + 140 + 142 + 145 + 148 + 150 + 155 + 160 + 170 + 900 + 2500 = 5,878.

(a) **Average** = 5,878 / 20 = **293.9 ms**.

(b) **Median.** With 20 values, the median is the average of the 10th and 11th values: (138 + 140) / 2 = **139 ms**. (Using nearest-rank, rank = ceiling(0.5 x 20) = 10, giving 138 ms. Both are acceptable; state which method you used.)

(c) **p90.** Rank = ceiling(0.90 x 20) = 18. The 18th value is **170 ms**.

(d) **p95.** Rank = ceiling(0.95 x 20) = 19. The 19th value is **900 ms**.

(e) **p99.** Rank = ceiling(0.99 x 20) = ceiling(19.8) = 20. The 20th value is **2,500 ms**.

**What to report.** The average (about 294 ms) is more than twice the median (about 139 ms) because two large outliers (900 and 2,500) pull it up; neither number describes what most users felt. A good report states: median about 139 ms, p90 170 ms, p95 900 ms, p99 2,500 ms, and flags that 10 percent of requests (two of twenty) were far slower than the rest and need investigation. Note also that with only 20 samples, p95 and p99 are each determined by single values, so the estimates are very noisy; real tests collect thousands of samples.

### Answer to Exercise 2

(a) Journeys per second: 600 per minute / 60 = 10 per second in total.
- Browse and log in: 60% of 10 = **6.0 per second**
- Register: 25% = **2.5 per second**
- Invalid login: 10% = **1.0 per second**
- Password reset: 5% = **0.5 per second**
(Check: 6 + 2.5 + 1 + 0.5 = 10.)

(b) Weighted average requests per journey = (0.60 x 12) + (0.25 x 9) + (0.10 x 3) + (0.05 x 4) = 7.2 + 2.25 + 0.3 + 0.2 = **9.95 requests per journey**.

(c) Peak RPS = 10 x 9.95 = **99.5 RPS**.
(Check by journey: 6 x 12 = 72; 2.5 x 9 = 22.5; 1 x 3 = 3; 0.5 x 4 = 2. Total = 99.5.)

(d) With 40 percent headroom: 99.5 x 1.4 = **139.3 RPS** (about 139).

(e) Weighted average duration = (0.60 x 300) + (0.25 x 150) + (0.10 x 30) + (0.05 x 60) = 180 + 37.5 + 3 + 3 = **223.5 seconds**.
Concurrent users L = lambda x W = 10 x 223.5 = **2,235 concurrent users**.

Notice again: about 2,235 concurrent users generate only about 99.5 requests per second.

### Answer to Exercise 3

1. **Soak (endurance) test.** Moderate steady load for a long duration; watching memory.
2. **Spike test.** Sudden, sharp jump for a short time.
3. **Smoke performance test.** Tiny load, short duration, checking scripts and environment.
4. **Volume test.** The emphasis is on a large amount of data, not on a large number of users.
5. **Load test.** Expected load, held steady, measured against a target.
6. **Stress test.** Load increases in steps beyond limits until failure, then recovery is observed.

### Answer to Exercise 4

(a) **The knee is between 300 and 400 users.** At 300 users p95 is 400 ms and throughput is still rising almost linearly (about 0.39 RPS per user). At 400 users p95 jumps to 1,500 ms and throughput barely increases (118 to 125).

(b) **Most likely bottleneck: the database connection pool (pool size 30).** Evidence: at 400 users and above, all 30 connections are in use, while CPU on both the application server (60 to 63 percent) and the database (about 55 percent) is far from saturated. Response time climbs and throughput flattens (and later falls) without any CPU limit being hit, which is the signature of requests waiting in a queue for a pooled resource. Before 400 users, the pool had spare connections and everything scaled smoothly.

(c) **First steps.** (1) Confirm: check pool wait metrics and how long each request holds a connection; look for slow queries or transactions held open for too long, since shortening connection hold time is usually better than just enlarging the pool. (2) Try one change at a time: for example, tune the slowest queries or add a missing index, and/or carefully increase the pool size while watching database CPU (a larger pool can overload the database). (3) Rerun the identical test and confirm the knee moves to a higher load, with p95 and throughput improving, and monitor for the next bottleneck.

(d) **A bigger application server would probably not help** because its CPU is only about 60 percent and it is not the resource that is saturated. The limiting factor is the fixed number of database connections (and what each holds). More application server power cannot create more database connections, so throughput would remain capped at about 125 RPS.

### Answer to Exercise 5

Problems include:

1. **Load generated from a laptop over Wi-Fi**: the laptop or wireless network may be the limit and adds noise.
2. **Shared dev server with concurrent deployments**: results are distorted by other activity; the environment is not production-like or isolated.
3. **Only one test user**: unrealistic data; caching and locking effects on a single account.
4. **No think time**: each virtual user generates far more load than a human would.
5. **500 threads**: not derived from a workload model; arbitrary and likely unrealistic (or the laptop itself may fail).
6. **Judging by the average only**: no percentiles, so tail latency is hidden.
7. **No error rate reported**: fast failures may be inflating the apparent performance.
8. **No server monitoring**: no evidence of why times are what they are or whether resources saturated.
9. **No stated target or SLA**: "pass" is undefined (200 ms against what requirement?).
10. **Only the login path, presumably the happy path**: no registration, invalid logins or other journeys, and no warm-up or steady-state measurement mentioned.
11. **Possibly testing without permission**: against a shared server; agreement and timing should be arranged.

---

## Knowledge Check

Try to answer each question before reading the answer beneath it.

**1. In one sentence each, what is the difference between a load test and a stress test?**

A load test applies the *expected* load to check that the system meets its performance targets. A stress test pushes *beyond* expected limits to find the breaking point, see how the system fails, and observe how it recovers.

**2. Why can 1,000 concurrent users produce less load than 100 concurrent users?**

Concurrent users counts people in the system, not how often they act. If the 1,000 users each act once a minute they generate about 17 requests per second, whereas 100 users each acting once a second generate 100 requests per second. Load depends on the request rate, which is shaped by think time.

**3. A report says "average response time 400 ms" and p99 is 6 seconds. Which better describes the experience of the slowest users, and why do we care?**

The p99 does. The average hides rare but severe slowness. One in a hundred requests taking six seconds means many real people suffer waits at scale, and in pages that make many requests, it is likely that at least one request per page hits the slow tail.

**4. What is think time and what happens if you leave it out?**

Think time is the deliberate pause that models a real user's reading and typing between actions. Leaving it out makes each virtual user generate far more load than a real person, so the system appears to fail at user counts it could easily handle in reality, and results are misleading.

**5. Using Little's Law: 8 new sessions start every second and each lasts on average 90 seconds. How many concurrent users on average?**

L = lambda x W = 8 x 90 = **720 concurrent users**.

**6. A system's response time stays flat until 300 users, then rises sharply while CPU is still at 40 percent and database connections are all in use. What is the likely bottleneck?**

The database connection pool (requests are queueing for connections). CPU is not saturated, so the system is waiting rather than working.

**7. Which kind of test would you use to find a memory leak, and why?**

A soak (endurance) test, because leaks accumulate gradually and only become visible over many hours of steady load. You watch memory over time for a continuing upward trend.

**8. Why do we report error rate next to response time?**

Because failed requests are often returned very quickly, which can make response time and throughput look good while many users are actually failing. Without the error rate you could declare a failing system "fast".

**9. Name the three Core Web Vitals and give a one-line meaning of each.**

LCP (Largest Contentful Paint): how quickly the main content appears. INP (Interaction to Next Paint): how quickly the page responds visually to user interaction. CLS (Cumulative Layout Shift): how much the layout jumps around unexpectedly while loading.

**10. What is the difference between an SLI, an SLO and an SLA?**

An SLI is a measurement (for example, percent of logins under 800 ms). An SLO is an internal target for that measurement. An SLA is a formal agreement, often contractual, with consequences for missing the target.

**11. Why must you only run load tests against systems you own or have written permission to test?**

Because heavy traffic against a system you are not authorised to test can be treated as a denial-of-service attack, may break the law and terms of service, can disrupt other people's services and can have serious professional consequences. Even with permission, agree timings and limits in advance and prefer test environments.

**12. Why do we run a smoke performance test before a long load test?**

To confirm that scripts, data, environment and monitoring work at tiny load, so that we do not waste hours on a long run that was broken from the start.

**13. In the hands-on run, why did throughput rise to about 345 requests per second at 100 users in the stress test even though capacity was about 200?**

Because failed requests are rejected quickly and still counted. About 46 percent of the requests failed, so successful throughput was only roughly 186 per second, close to the real ceiling. Useful throughput must be judged together with the error rate.

**14. Give two ways AI tools can help a performance tester and two cautions.**

Help: drafting plans and script skeletons; summarising results and suggesting hypotheses about bottlenecks. Cautions: suggestions are hypotheses that must be verified with monitoring data and retests; AI can invent details or wrong syntax; do not share confidential data or let generated scripts run against unverified targets.

**15. Where in a CI/CD pipeline do different performance tests belong?**

Fast smoke performance checks and performance budgets run on every build; fuller load tests run nightly or on a schedule and are compared with the baseline; heavy stress, spike, soak and volume tests run weekly or before major releases on a production-like environment; production monitoring and alerts continue after release.

---

## Key Takeaways

- Performance is more than "fast": it includes speed, responsiveness, capacity, resource use and stability under load, seen from both the user's and the business's viewpoint.
- Performance testing is an umbrella. Load testing checks expected load; stress testing finds the breaking point and checks recovery; spike testing checks sudden surges; soak testing finds problems that appear over time, such as memory leaks; volume testing checks large data; baseline tests establish what normal is; capacity testing finds the highest acceptable load; smoke performance tests check that it is worth continuing; scalability testing is explored in the next lesson.
- Concurrent users and requests per second are different things. Think time and pacing link them, and Little's Law (L = lambda x W) provides a simple sanity check.
- Averages mislead. Use percentiles (p50, p90, p95, p99), report the error rate beside them, and never average percentiles.
- Good tests start with measurable NFRs and a workload model built from realistic journey mixes, not a guess at "how many users".
- Systems have a knee: beyond a certain load, queues form and response time climbs steeply. Find the bottleneck by asking which resource saturated first, and remember that low CPU with rising response time means something is waiting.
- Common bottlenecks include slow or missing-index queries, the N+1 pattern, thread and connection pools, memory leaks, third-party calls, network and front-end assets.
- Front-end performance (page load, LCP, INP, CLS, Lighthouse, the DevTools Network tab) complements server-side load testing.
- Tools (JMeter, Gatling, k6, Locust, Artillery, BlazeMeter, LoadRunner and monitoring stacks like Prometheus and Grafana) matter less than the thinking; detailed setups come in later courses.
- Make performance continuous: shift left, use budgets and smoke checks on builds, nightly load runs and production monitoring.
- AI can draft, summarise and suggest hypotheses, but every claim needs evidence from real measurements.
- Avoid the common mistakes: non-representative environments, averages only, no think time, unrealistic scripts, happy-path-only tests, no server monitoring and load generated from a weak laptop on Wi-Fi.
- Only test systems you own or have written permission to test. Unauthorised load testing can be treated as an attack.
- Reliability, availability, scalability, failover and capacity planning are the subject of the next lesson.

---

## Additional Resources

- Apache JMeter (official site, user manual and getting-started guides): https://jmeter.apache.org/
- Grafana k6 documentation (load testing concepts, test types such as load, stress, spike and soak, and thresholds): https://grafana.com/docs/k6/latest/
- web.dev, Core Web Vitals (definitions of LCP, INP and CLS, with guidance on measuring and improving them): https://web.dev/articles/vitals
- Locust documentation (for the Python-based tool previewed in this lesson, for later weeks): https://docs.locust.io/

Next lesson: **Reliability and scalability**, where we build on what you learned here about capacity and saturation and explore how systems stay available, recover from failure and grow.
