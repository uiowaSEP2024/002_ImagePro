Feature: Dashboard

  Background: 
    Given user is on the homepage
    And user clicks "/login" href button
    Then user should be on "/login" page
    When user fills "Email" with "botimage@gmail.com"
    And user fills "Password" with "abd"
    And user clicks "login" datatestid button
    Then user should see "Login successful. Redirecting..."
    When user waits
    Given user clicks "/dashboard" href button
    Then user should be on "/dashboard" page

  Scenario: Jobs route
    When user clicks "/jobs" href button
    Then user should be on "/jobs" page

  Scenario: Analytics route
    When user clicks "/billing" href button
    Then user should be on "/billing" page

  Scenario: API Keys Route
    When user clicks "/apikeys" href button
    Then user should be on "/apikeys" page