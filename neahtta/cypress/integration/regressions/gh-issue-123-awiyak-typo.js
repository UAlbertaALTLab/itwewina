/**
 * See GitHub issue #123:
 * https://github.com/UAlbertaALTLab/itwewina/issues/123
 */
describe('The nêhiyawêwin paradigm', function () {
  it('should say ayiwak for "somebody"', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'wîcêwêw');
    cy.contains('.lexeme a', 'wîcêwêw').click();
    cy.contains('[data-toggle]', 'nêhiyawêwin').click();

    cy.get('.miniparadigm[data-type="nêhiyawêwin"]')
      .should('contain', 'awiyak')
      .and('not.contain', 'ayiwak');
  });
});
