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
      .contains('cite', 'MD')
      .should('have.attr', 'title', 'Maskwacîs Cree Dictionary')
      .and('have.css', 'vertical-align', 'super');
    cy.get('@meanings')
      .contains('cite', 'CW')
      .and('have.css', 'vertical-align', 'super');
  });

  it('should display the full title of the source on hover', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'acâhkos');

    cy.get('.results .lexeme:first .meanings cite:first').as('citation')
      .contains('MD');

    cy.get('@citation')
      .trigger('mouseover');

    cy.get('.tooltip')
      .should('be.visible')
      .and('contain', 'Maskwacîs Cree Dictionary');
  });
});
