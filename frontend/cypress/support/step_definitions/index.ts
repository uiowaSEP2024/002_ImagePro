import { When, Then, Given } from "@badeball/cypress-cucumber-preprocessor";

Given("user is on the homepage", function () {
  cy.visit("http://localhost:3000").then(() => {
    cy.window().its("Cypress").should("be.an", "object");
  });
});

Given("user clicks sign up", function () {
  cy.get('[href="/signup"]').click({multiple: true })
});

Then("user should be on sign up page", function () {
  cy.location("pathname").should('match', new RegExp("/signup") );
});

When(
  "user fills First Name with John and Last Name with Thomas and Email with john@gmail.com",
  function () {
    cy.get('[id="First Name"]').type(`John{enter}`);
    cy.get('[id="Last Name"]').type(`Thomas{enter}`);
    cy.get('[id="Email"]').type(`john@gmail.com{enter}`);
  }
);

When("user fills Password with abd", function () {
  cy.get('[id="Password"]').type(`abd{enter}`);
});

When("user fills Confirm Password with abd", function () {
  cy.get('[id="Confirm Password"]').type(`abd{enter}`);
});

When("user clicks create account button", function () {
  cy.get('[data-testid="signup"]').click()
});

Then("user should see Sign up successful", function () {
  cy.on('window:alert', (text) => {
    expect(text).to.contains('Sign up successful');
  });
});

Then("user should still be on signup page", function () {
  cy.location("pathname").should('match', new RegExp("/signup") );
});

When("user puts Confirm Password as cat", function () {
  cy.get('[id="Confirm Password"]').type(`cat{enter}`);
});

Then("error message should display with Passwords Do Not Match", function () {
  cy.on('window:alert', (text) => {
    expect(text).to.contains('Sign up successful');
  });
});
