Feature: Product sorting
  As a shopper
  I want to sort the product list
  so that I can find what I want quickly

  Scenario: Sorting by price from low to high
    Given the shopper is logged in
    When the shopper sorts the products by "Price (low to high)"
    Then the products are listed from cheapest to most expensive

  Scenario: Sorting by price from high to low
    Given the shopper is logged in
    When the shopper sorts the products by "Price (high to low)"
    Then the products are listed from most expensive to cheapest

  Scenario: Sorting by name from Z to A
    Given the shopper is logged in
    When the shopper sorts the products by "Name (Z to A)"
    Then the products are listed in reverse alphabetical order

  Scenario: Sorting does not change the cart
    Given the shopper is logged in
    And the shopper adds "Sauce Labs Backpack" to the cart
    When the shopper sorts the products by "Name (Z to A)"
    Then the products are listed in reverse alphabetical order
    But the cart count shows 1
