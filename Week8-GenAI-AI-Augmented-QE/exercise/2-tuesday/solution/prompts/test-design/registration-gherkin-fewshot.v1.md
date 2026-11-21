# Prompt: registration Gherkin, few-shot (v1)

Purpose: Turn registration acceptance criteria into a feature file in the ShopFront house style.
Version: 1
Tested with: <Claude model name shown in the interface>, 2 runs, <YYYY-MM-DD>
Technique: few-shot (two examples from other features), boundary value analysis
Acceptance criteria: house style (first person, tag, exact quoted messages, Scenario Outline for data, no prose); all four error messages and the welcome message; boundaries 3/4/16/17 characters and ages 15/16/99/100; no leakage from the examples
Check with: python tools/check_gherkin.py <reply>, then read every scenario against materials/registration-criteria.md
Changes from previous: first version
Evidence: evidence/registration-gherkin-fewshot.v1.run1.txt (passes), leak.txt (backup showing leakage)
Placeholders: none (parameterised templates are Thursday's topic)

## Prompt

```text
Convert the acceptance criteria into a Gherkin feature in our house style.
Rules:
- Use a Scenario Outline with Examples when criteria differ only by data.
- Write steps from the shopper's point of view ("I").
- Put exact values and exact messages in double quotes in the steps.
- Include the boundary values on both sides of every limit.
- Tag the feature with its requirement area.
- Output only the Gherkin, with no explanation.

<example>
Acceptance criteria:
- A registered shopper who logs in with the correct password sees "My account".
- A wrong or empty password shows "Invalid email or password".

Gherkin:
@login
Feature: Shopper login
  Registered shoppers sign in with their email address and password.

  Scenario: Log in with the correct password
    Given I am a registered shopper with email "mila.ortiz@example.org"
    When I log in with password "Tulip-Garden-42"
    Then I should see the "My account" page

  Scenario Outline: Reject a wrong or empty password
    Given I am a registered shopper with email "mila.ortiz@example.org"
    When I log in with password "<password>"
    Then I should see the message "Invalid email or password"

    Examples:
      | password      |
      | tulip-garden  |
      |               |
</example>

<example>
Acceptance criteria:
- When nothing matches the search term, the page shows "No products found".

Gherkin:
@search
Feature: Product search
  Shoppers find products by keyword.

  Scenario: Show a message when nothing matches
    Given the catalogue contains the product "Walnut Desk Lamp"
    When I search for "zzzz"
    Then I should see the message "No products found"
</example>

Acceptance criteria:
<paste the five bullet points from materials/registration-criteria.md here>

Gherkin:
```

## Review notes

Chose the search example WITHOUT the "ignores letter case" scenario: the backup reply leak.txt shows how that scenario can turn into a registration rule. Checked boundaries by reading: abc (3) and a 17-character name rejected; abcd (4) and a 16-character name accepted; ages 15 and 100 rejected, 16 and 99 accepted. The run1 reply did not test "must start with a letter" with a hyphen first; added as a review note for the next version.
