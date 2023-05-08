Feature: Signup

  Background:
    Given user is on the homepage
    And user clicks sign up

  Scenario: Create a New User
    When user fills First Name with John and Last Name with Thomas and Email with john@gmail.com
    And user fills Password with abd
    And user fills Confirm Password with abd
    And user clicks create account button
    Then user should see Sign up successful
    And user should still be on signup page

  Scenario: User does not follow form validations
    When user fills First Name with John and Last Name with Thomas and Email with john@gmail.com
    And user fills Password with abd
    And user puts Confirm Password as cat
    Then error message should display with Passwords Do Not Match
    And user should still be on signup page