Feature: Signup

  Background: 
    Given user is on the homepage
    And user clicks "/signup" href button
    Then user should be on "/signup" page

  Scenario: Create a New User
    When user fills "First Name" with "John"
    And user fills "Last Name" with "Thomas"
    And user fills "Email" with "john@gmail.com"
    And user fills "Password" with "abd"
    And user fills "Confirm Password" with "abd"
    And user clicks "signup" datatestid button
    Then user should see "Sign up successful"
    And user should be on "/signup" page

  Scenario: User does not follow form validations
    When user fills "First Name" with "John"
    And user fills "Last Name" with "Thom"
    And user fills "Email" with "john1@gmail.com"
    And user fills "Password" with "abd"
    And user fills "Confirm Password" with "cat"
    Then user should see "Passwords Do Not Match"
    And user should be on "/signup" page