/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/12
 */

describe('Orthographical normatization and presentations of word-form matching search string', function () {
  it('normatizes "e-wapamat"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('e-wapamat');
    cy.contains('ê-wâpamât');
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
    cy.contains(/ê-kakwê-nôhtê-w[aâ]-wâh-wâpamât/);
  });

  it('normatizes "ma-mah-miyo-na-nah-nipaw"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('ma-mah-miyo-na-nah-nipaw');
    cy.contains('ma-mâh-miyo-na-nâh-nipâw');
  });


  it('finds multiple possibilities for "nipihk"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('nipihk');
    cy.contains('.possible_analyses *', /\bnipîhk\b/);
    cy.contains('.possible_analyses *', /\bnîpîhk\b/);
    cy.contains('.possible_analyses *', /\bnipihk\b/);
    cy.contains('.possible_analyses *', /\bnîpihk\b/);
    cy.contains('.possible_analyses *', /\bnipik\b/);
  });
});
