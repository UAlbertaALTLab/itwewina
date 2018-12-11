/**
 * TODO: description.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/92
 */
describe('Maskwacîs recordings integration', function () {
  it('should produce recordings for +V+AI+Indep+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    // TODO: The actual test part of this!
  });

  it('should produce recordings for PV/e+...+V+AI+Conj+Pret+3Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-sôhkêyimot');
  });
  
  it('should produce recordings for PV/e+...+V+TA+Conj+Pret+X+1SgO', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-kiskisototâht');
  });

  it('should produce recordings for +V+TI+Indep+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nimihtâtên');
  });

  it('should produce recordings for PV/e+...+V+TI+Conj+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-mihtâtamân');
  });

  it('should produce recordings for +V+II+Indep+Pret+3Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'pîtosinâkwan');
  });

  it('should produce recordings for +N+I+Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiskisiwin');
  });

  it('should produce recordings for +IPJ', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiyâm');
  });
});
