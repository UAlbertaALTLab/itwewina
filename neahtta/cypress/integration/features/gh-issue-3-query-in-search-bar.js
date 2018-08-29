/**
 * Does the query text end up in the search results' search box?
 *
 * See https://github.com/UAlbertaALTLab/itwewina/issues/3
 */

describe('Navigating to the results page', function () {
  it('should display the query text in the search bar', function () {
    cy.visit('/crk/eng');
    cy.get('input[name=lookup]').as('searchBox');

    cy.get('@searchBox')
      .wait(50) // As always, delay a bit so that the first few characters
                // don't get eaten up.
      .type('atim{enter}');

    // We should now navigate to the results page, displaying "dog" among its
    // results:
    cy.contains('dog');

    // We should see «atim» in the search box.
    cy.get('@searchBox')
      .should('have.value', 'atim');
  });
});
