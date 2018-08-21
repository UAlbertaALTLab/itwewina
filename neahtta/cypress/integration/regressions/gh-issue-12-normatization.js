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
    cy.contains('ê-kakwê-nôhtê-wa-wâh-wâpamât');
  });

  it('normatizes "ma-mah-miyo-na-nah-nipaw"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('ma-mah-miyo-na-nah-nipaw');
    cy.contains('ma-mâh-miyo-na-nâh-nipâw');
  });


  it('finds multiple possibilities for "nipihk"', function () {
    cy.visit('/crk/eng');

    cy.neahttaSearch('nipihk');
    cy.contains('nipîhk');
    cy.contains('nîpîhk');
    cy.contains('nipihk');
    cy.contains('nîpihk');
    cy.contains('nipik');
  });
});
