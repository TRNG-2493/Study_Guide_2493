
## Exercise 1 

1. Rewrite this requirement so it is testable, and list two questions you'd ask the author:
   *"Users should be able to reset their password easily."*
2. Classify each requirement as **functional** or **non-functional**:
    - (a) "The user can download an invoice as PDF."
    - (b) "The app works on Chrome, Firefox and Safari."
    - (c) "The system sends an SMS when an order ships."
3. Label each as **QA** or **QC**:
    - (a) Running test cases on a build
    - (b) Introducing a code review checklist
    - (c) Training developers on secure coding
    - (d) Inspecting a release candidate for defects
4. Label each as **verification** or **validation**:
    - (a) Reviewing the design document
    - (b) A customer trying the app in user acceptance testing
    - (c) A peer reviewing code against the spec
5. Identify the **error**, **defect**, and **failure**:
   *A developer thought VAT was 5% instead of 15%. The code calculates `price * 1.05`. Customers' invoices show too little tax.*

---

## Exercise 2 

1. Match each scenario to a testing principle:
    - (a) "We ran the same 50 tests for a year and found nothing new."
    - (b) "Most bugs came from the payment module."
    - (c) "The app passed every test, but users found it useless."
2. Manual or automated?
    - (a) Checking a new logo looks right on mobile
    - (b) Running 400 regression tests every night
    - (c) Exploring a brand-new feature for the first time
3. Write **two positive** and **three negative** test cases for a "Sign up" form with Email and Password (password must be 8–16 characters).
4. A movie ticket site gives prices by age: **0–12 = child, 13–59 = adult, 60+ = senior**. Identify the equivalence partitions (valid and invalid) and one test value for each.

---

## Exercise 3 

1. **BVA:** A text field accepts a username of **6 to 20 characters**. List the boundary values to test (three-value BVA) and the expected result for each.
2. **Decision table:** A bank approves a loan if the applicant has a salary over $30,000 **and** a good credit score. Applicants with only one of these are sent for manual review. Applicants with neither are rejected. Build the decision table.
3. **State transition:** A document can go **Draft → Submitted → Approved**, or **Submitted → Rejected → Draft** (edited and resubmitted). List the valid transitions and one invalid transition to test.
4. **Use case:** For "User withdraws cash from an ATM", write the main flow (4–6 steps) and two exception flows.
5. **Error guessing:** List five error-guessing tests for a "Phone number" field.
