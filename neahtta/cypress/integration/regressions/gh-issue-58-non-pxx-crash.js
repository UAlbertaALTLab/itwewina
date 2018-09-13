/**
 * Non-PxX words crash itêwina search.
 */
describe('Searching for non-PxX words', function () {
  it('should display search results for words like "-okom"', function () {
    cy.visit('/');
    cy.neahttaSearch('nohkom');

    cy.contains('a', 'nôhkom');
  });
});
