/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/91
 */
describe('Concise representations of dictionary sources', function () {
  it('should list the sources in superscript on the search page', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'acâhkos');

    cy.get('.results  .lexeme:first').as('lexeme')
    cy.get('@lexeme')
      .contains('a', 'acâhkos');
    cy.get('@lexeme').find('.meanings').as('meanings');
    cy.get('@meanings')
      .contains('cite', 'MD');
    cy.get('@meanings')
      .contains('cite', 'CW');
  });
});
