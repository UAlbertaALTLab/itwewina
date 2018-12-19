/**
 * Tests the display (or omission of display) of the sources for a particular
 * entry's text.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/7
 */

describe("List of an entry's sources", function () {
  it('should not be displayed on the search results page', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'wanâpamow');

    // We should be on the results page.
    cy.contains('√wanâpamo-');

    // This word comes from Arok's dictionary.
    // We should not know that from the front page.
    cy.get('.lexeme')
      .should('not.contain', 'nêhiyawêwin : itwêwina / Cree : Word');
  });

  it('should be displayed on the details page', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'wanâpamow');
    cy.contains('a', 'wanâpamow')
      .click();

    // We should be on the details page.
    cy.url()
      .should('contain', 'detail');

    // We should see the source on the page.
    cy.get('.lexeme .entry_source')
      .should('contain', 'CW');
    // Behaviour changed! See https://github.com/UAlbertaALTLab/itwewina/issues/91
  });
});
