/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/30
 */

describe('Display of SRO macrons and circumflexes ', function () {
  it('should produce at least four search results for "nipihk" in macron SRO', function () {
    cy.visit('/crkMacr/eng');

    cy.neahttaSearch('nipihk');

    cy.containsInterpretation('nipīhk');
    cy.containsInterpretation('nīpīhk');
    cy.containsInterpretation('nīpihk');

    /* XXX: see above; also, there seems to be a Giella error in the macron
     * FSTs. */
    // cy.containsInterpretation(/\bnipih?k\b/);
  });

  it('should produce at least four search results for "nipihk" in circumflex SRO', function () {
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
