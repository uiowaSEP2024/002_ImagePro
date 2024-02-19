Feature: Login

  Background:
    Given user is on the homepage
    And user clicks "/login" href button
    Then user should be on "/login" page

  Scenario: Login Success
    When user fills "Email" with "johndoe@gmail.com"
    And user fills "Password" with "abd"
    And user clicks "login" datatestid button
    Then user should see "Login successful. Redirecting..."

  Scenario: Login Failure
    When user fills "Email" with "john.doe@gmail.com"
    And user fills "Password" with "cat"
    And user clicks "login" datatestid button
    Then user should see "Login failed. Please try again."
    And user should be on "/login" page
