/**
 * Tests the display (or omission of display) of the sources for a particular
 * entry's text/
 */

describe("List of an entry's sources", function () {
  it('should not be displayed on the search results page', function () {
    cy.visit('/crk/eng');
    cy.neahttaSearch('wanâpamow');

    // We should be on the results page.
    cy.contains('√wanâpamo-');

    // This word comes from Arok's dictionary.
    // We should not know that from the front page.
    cy.get('.lexeme')
      .should('not.contain', 'nêhiyawêwin : itwêwina / Cree : Word');
  });

  it('should be displayed on the details page', function () {
    var detailURL = '/detail/crk/eng/wan%C3%A2pamow.html?no_compounds=true&lemma_match=true&e_node=5556836001097474918';
    cy.visit(detailURL);

    // We should be on the details page.
    cy.contains('wanâpamow');

    // We should see the source on the page.
    cy.get('.lexeme')
      .should('contain', 'nêhiyawêwin : itwêwina / Cree : Word');
  });
});
