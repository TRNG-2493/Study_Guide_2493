@search
Feature: Product search
  Shoppers find products by keyword.

  Scenario Outline: Search ignores letter case
    Given the catalogue contains the product "Walnut Desk Lamp"
    When I search for "<term>"
    Then the results should include "Walnut Desk Lamp"

    Examples:
      | term      |
      | desk lamp |
      | DESK LAMP |

  Scenario: Show a message when nothing matches
    Given the catalogue contains the product "Walnut Desk Lamp"
    When I search for "zzzz"
    Then I should see the message "No products found"
