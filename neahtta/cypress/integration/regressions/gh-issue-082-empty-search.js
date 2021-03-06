/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/82
 */

describe('Search an with an empty query', function () {

  it('should not crash', function () {
    // Regression: the server should NOT return a 500 error
    cy.instantNeahttaSearch('crk', 'eng', '');

    // If we've gotten to the page, the page should not return an exception
    // message.
    cy.get('body')
      .should('not.contain', 'Unknown lookup type');
  });

  it('should not be possible to submit a search', function () {
    cy.visit('/crk/eng');

    cy.get('form#neahttasaanit')
      .submit();

    cy.url()
      .should('not.contain', '?lookup');
  });
});
