/**
 * Pressing 'enter' once should initiate search when autocomplete box is open
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/27
 */

describe('The search autocompletion drop-down', function () {
  it('should execute the search upon pressing enter', function () {
    /* GIVEN I see search suggestion dropdown */
    cy.visit('/crk/eng');
    cy.get('input')
   /* XXX: Wait a bit so that the autocomplete doesn't eat up the first
      * character. */
      .wait(50)
    /* ... Type in a prefix that will FOR SURE yield something. */
      .type('atim');

    /* WHEN I press enter. */
    cy.get('input')
      .type('{enter}')

    /* THEN The search should execute immediately. */
    /* ... A link that says "dog" means it's done the search. */
    cy.contains('.results a', /\bdog\b/i);
  });
});
