/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/8
 */

describe('Navigating to a search results page', function () {
  it('should display the query text in the URL', function () {
    cy.visit('/');

    // Search for something.
    cy.neahttaSearch('miskinahk');

    // Wait for the results page.
    cy.contains('turtle');

    cy.url()
      .should('contain', 'lookup=miskinahk')
  });
});
