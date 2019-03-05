/**
 * See GitHub issue #123:
 * https://github.com/UAlbertaALTLab/itwewina/issues/123
 */
describe('GitHub issue 123', function () {
  it('should say "awiyak" for [unspecfied actor] in the nêhiyawêwin paradigm', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'wîcêwêw');
    cy.contains('.lexeme a', 'wîcêwêw').click();
    cy.contains('[data-toggle]', 'nêhiyawêwin').click();

    cy.get('.miniparadigm[data-type="nêhiyawêwin"]')
      .should('contain', 'awiyak')
      .and('not.contain', 'ayiwak');
  });
});
