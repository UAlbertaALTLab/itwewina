/**
 * Clicking a search suggestion should execute the search immediately.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/5
 */

describe('Clicking a search suggestion', function () {
  it('should execute the search immediately', function () {
    /* GIVEN I see search suggestion dropdown */
    cy.visit('/crk/eng');
    cy.get('input')
   /* XXX: Wait a bit so that the autocomplete doesn't eat up the first
      * character. */
      .wait(50)
    /* ... Type in a prefix that will FOR SURE yield something. */
      .type('atim');

    /* WHEN I click a suggestion. */
    cy.get('.dropdown-menu')
      .contains('a', 'atim')
      .click();

    /* THEN The search should execute immediately. */
    /* ... A link that says "dog" means it's done the search. */
    cy.contains('.results a', /\bdog\b/i);
  });
});
