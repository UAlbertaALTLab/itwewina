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
 * Executes a search via a URL. Should land on the search page.
 */
Cypress.Commands.add('instantNeahttaSearch', (source, target, term) => {
  cy.visit(`/${source}/${target}/?lookup=${encodeURIComponent(term)}`);
});

/**
 * Check the logo if it contains certain text.
 */
Cypress.Commands.add('logoContains', (content) => {
    cy.get('a.brand')
      .contains('*', content, { timeout: 0 });
});

/**
 * On the search results page, this command asserts that the given normatized
 * wordform interpretation is present.
 *
 * e.g., when you search for "miskinak", you would use this assertion to
 * ensure that "miskinâhk" is a search result.
 *
 * @param String|RegExp wordform
 *        When a String, searches for that EXACT wordform (i.e., it cannot be
 *        part of another word). You may also provide a RegExp which will be
 *        searched verbatim.
 */
Cypress.Commands.add('containsInterpretation', (wordform) => {
  var content = wordform instanceof RegExp ?
    /* NOTE: JavaScript's "\b" doesn't work with non-ASCII characters (boo!)
     * so we may have to be creative with how we define word boundaries. */
    wordform : new RegExp(`\\b${wordform}\\b|^${wordform}$`);

  cy.contains('.possible_analyses *', content);
});
