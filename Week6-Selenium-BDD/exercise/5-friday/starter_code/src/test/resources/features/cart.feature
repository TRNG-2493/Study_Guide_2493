Feature: Shopping cart
  As a shopper
  I want to add products to my cart
  so that I can buy several things in one order

  Scenario: Adding a product increases the cart count
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart count shows 1

  Scenario: An added product is listed in the cart
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    And the shopper opens the cart
    Then the cart lists "Sauce Labs Backpack"

  Scenario: Adding several products at once
    Given the shopper is logged in
    When the shopper adds the following products to the cart
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart count shows 3

  Scenario: Removing the only product empties the cart
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    And the shopper opens the cart
    And the shopper removes "Sauce Labs Backpack" from the cart
    Then the cart is empty

  Scenario: Removing one product keeps the other
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    And the shopper adds "Sauce Labs Bike Light" to the cart
    And the shopper opens the cart
    And the shopper removes "Sauce Labs Backpack" from the cart
    Then the cart lists "Sauce Labs Bike Light"
    But the cart does not list "Sauce Labs Backpack"
