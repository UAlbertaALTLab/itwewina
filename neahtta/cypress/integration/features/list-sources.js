/**
 * Tests the display (or omission of display) of the sources for a particular
 * entry's text/
 */

describe("List of an entry's sources", function () {
  it.only('should not be displayed on the search results page', function () {
    cy.visit('/crk/eng');
    cy.neahttaSearch('wanâpamow');

    // We should be on the results page.
    cy.contains('√wanâpamo-');

    // This word comes from Arok's dictionary.
    // We should not know that from the front page.
    cy.get('.lexeme')
      .should('not.contain', 'nêhiyawêwin : itwêwina / Cree : Word');
  });
});
