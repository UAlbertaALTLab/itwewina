/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/30
 */

describe('Display of SRO macrons and circumflexes ', function () {
  it('should produce five search results for "nipihk" in circumflex SRO', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('nipihk');
    cy.containsInterpretation('nipîhk');
    cy.containsInterpretation('nîpîhk');
    cy.containsInterpretation('nîpihk');
    /**
     * XXX: The lemma for 'nipihk' and 'nipik' is 'nipiw',
     * however currently NDS will only show one analysis. It should show both
     * analyses, however, this is tracked by issue #25.
     *
     * See: https://github.com/UAlbertaALTLab/itwewina/issues/25
     */
    cy.containsInterpretation(/\bnipih?k\b/);
  });
});