Feature: Dashboard

  Background: 
    Given user is on the homepage
    
  Scenario: Jobs route
    When user clicks "/jobs" href button
    Then user should be on "/jobs" page

  Scenario: Analytics route
    When user clicks "/billing" href button
    Then user should be on "/billing" page