/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/73
 */
describe('Particles', function () {
  it('should analyze +Ipc particles', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'êha');

    cy.get('.entry_row:first').as('lemma');
    // Ensure this is actually the entry with êha/"yes" particle
    cy.get('@lemma')
      .contains('a', /êha\s[(].+IP[CJ][)]/);

    // Check for an analysis ANYWHERE on the page.
    cy.contains('.possible_analyses', 'Independent particle');

    // Check for the analysis under the same entry.
    cy.get('@lemma')
      .contains('.possible_analyses', 'Independent particle');
  });
});
