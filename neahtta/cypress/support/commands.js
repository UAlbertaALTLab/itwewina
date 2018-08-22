// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

/**
 * Executes a search. Should land on the search page.
 * 
 * NOTE: This skips waiting for autocompletion!
 * (Autocompletion makes these tests rather
 */
Cypress.Commands.add('neahttaSearch', (term) => {
  cy.get('form#neahttasaanit')
    .get('input[name=lookup]')
    // Force the textbox to have the text we want, without "typing" it in, one
    // character at a time, as .type() would do.
    .invoke('val', term);
  cy.get('form#neahttasaanit')
    .get('button[name=search]:visible')
    .click();
});

/**
 * Check the logo if it contains certain text.
 */
Cypress.Commands.add('logoContains', (content) => {
    cy.get('a.brand')
      .contains('*', content, { timeout: 0 });
});
