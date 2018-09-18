/**
 * Some lemmas may have multiple valid analyses. NDS should display them all.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/25
 */
describe('Lemmas with ambiguous analyses', function () {
  it('should display all plausible wordforms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nipihk');

    // "water" + Locative
    cy.contains('.possible_analyses', 'nipîhk');

    // "leaf" + Locative
    cy.contains('.possible_analyses', 'nîpîhk');

    // it is summer -- better as ê-nîpihk
    cy.contains('.possible_analyses', 'nîpihk');

    // "dead" + imperative + immediate + 2p plural actor
    cy.contains('.possible_analyses', 'nipik');
    // "dead" + Conjunct + unspecified actor
    cy.contains('.possible_analyses', 'nipihk');
  });
});
