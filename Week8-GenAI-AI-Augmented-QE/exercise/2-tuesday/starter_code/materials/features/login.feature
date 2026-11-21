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
