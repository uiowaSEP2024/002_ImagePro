import { When, Then, Given } from "@badeball/cypress-cucumber-preprocessor";

Given("user is on the homepage", function () {
  cy.visit("http://localhost:3000").then(() => {
    cy.window().its("Cypress").should("be.an", "object");
  });
});

Given('user clicks {string} href button', function (string) {
  cy.wait(6000);
  cy.get(`[href="${string}"]`).click({multiple: true })
  cy.wait(6000);
});

Then("user should be on {string} page", function (string) {
  cy.location("pathname").should('match', new RegExp(`${string}`) );
});

When(
  "user fills {string} with {string}",
  function (string, text) {
    cy.get(`[id="${string}"]`).type(`${text}{enter}`);
  }
);

When("user clicks {string} datatestid button", function (string) {
  cy.get(`[data-testid="${string}"]`).click({force: true})
});

When("user waits", function (string) {
  cy.wait(2000);
});

Then("user should see {string}", function (string) {
  cy.on('window:alert', (text) => {
    expect(text).to.contains(`"${string}"`);
  });
});