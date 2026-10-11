Feature: Login
  As a registered customer
  I want to log in
  so that I can see the products

  # GIVEN: these two scenarios come from the demo. Keep them.
  # TODO (slot 3): add at least THREE more login scenarios that your Three Amigos workshop agreed on
  #   (for example: a locked-out user, a missing username, a missing password).

  Scenario: Successful login with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page

  Scenario: Login is rejected for a wrong password
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "wrong_password"
    Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed
