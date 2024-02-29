Feature: Dashboard

  Background:
    Given user is on the homepage
    And user clicks "/login" href button
    Then user should be on "/login" page
    When user fills "Email" with "botimage@gmail.com"
    And user fills "Password" with "abcdefg"
    And user clicks "login" datatestid button
    Then user should see "Login successful. Redirecting..."
    When user waits
    Given user clicks "/dashboard" href button
    Then user should be on "/dashboard" page

  Scenario: Jobs route
    When user clicks "/studies" href button
    Then user should be on "/studies" page

  Scenario: Analytics route
    When user clicks "/analytics" href button
    Then user should be on "/analytics" page

  Scenario: API Keys Route
    When user clicks "/apikeys" href button
    Then user should be on "/apikeys" page
