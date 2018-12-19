/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/12
 */

describe('Orthographical normatization and presentations of word-form matching search string', function () {
  it('normatizes "e-wapamat"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('e-wapamat');
    cy.containsInterpretation('ê-wâpamât');
  });

  it('normatizes "ekakwenohtewawahwapamat"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('ekakwenohtewawahwapamat');
    /* XXX:  match either wa- or wâ-
     * NDS currently will only show *one* of these two forms, but which of the
     * two is unclear without FST weighting. Hence, expect either one of them.
     *
     * See discussion at:
     * https://github.com/UAlbertaALTLab/itwewina/issues/12#issuecomment-414729826
     */
    cy.containsInterpretation(/^ê-kakwê-nôhtê-w[aâ]-wâh-wâpamât$/);
  });

  it('normatizes "ma-mah-miyo-na-nah-nipaw"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('ma-mah-miyo-na-nah-nipaw');
    cy.containsInterpretation('ma-mâh-miyo-na-nâh-nipâw');
  });
});
