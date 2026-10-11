Feature: Login
  As a registered customer
  I want to log in
  so that I can see the products

  Scenario: Successful login with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page

  Scenario: Login is rejected for a wrong password
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "wrong_password"
    Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed

  Scenario: A locked-out customer cannot log in
    Given the customer is on the login page
    When the customer logs in with username "locked_out_user" and password "secret_sauce"
    Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed

  Scenario: Login requires a username
    Given the customer is on the login page
    When the customer logs in with username "" and password "secret_sauce"
    Then the error message "Epic sadface: Username is required" is displayed

  Scenario: Login requires a password
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password ""
    Then the error message "Epic sadface: Password is required" is displayed
