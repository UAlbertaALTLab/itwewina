/**
 * Non-PxX words crash itwêwina search.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/58
 */
describe('Searching for non-PxX words', function () {
  it('should display search results for words like "-okom"', function () {
    cy.visit('/');
    cy.neahttaSearch('nohkom');
    // Previously, the search would crash here, before getting to the results
    // page.

    cy.contains('a', 'nôhkom');
  });
});
