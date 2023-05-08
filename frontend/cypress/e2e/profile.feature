Feature: Profile

  Background: 
    Given user is on the homepage
    And user clicks "/login" href button
    Then user should be on "/login" page
    When user fills "Email" with "johndoe@gmail.com"
    And user fills "Password" with "abd"
    And user clicks "login" datatestid button
    Then user should see "Login successful. Redirecting..."
    When user waits
    And user clicks "/profile" href button
    Then user should be on "/profile" page

  Scenario: User profile
    Then user should see "John Doe"
    And user should see "johndoe@gmail.com"
    And user should see "customer"
    