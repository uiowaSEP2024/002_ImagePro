Feature: API Keys

  Background:
    Given user is on the homepage
    And user clicks "/login" href button
    Then user should be on "/login" page
    When user fills "Email" with "admin1@admin.com"
    And user fills "Password" with "abcdefg"
    And user clicks "login" datatestid button
    Then user should see "Login successful. Redirecting..."
    When user waits
    Given user clicks "/apikeys" href button
    Then user should be on "/apikeys" page

  Scenario: Create API Key Happy Route
    Then user should see "Manage API Keys"
    When user fills "Note" with "My Key"
    And user clicks "submit" datatestid button
    Then user should see "Please copy this key for later. This is the only time you will see it."
