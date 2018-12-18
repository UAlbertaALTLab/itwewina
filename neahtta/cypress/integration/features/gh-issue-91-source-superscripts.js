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
      .and('have.css', 'vertical-align', 'super');
    // NOTE: bootstrap-tooltip rewrites the [title] attribute, so don't go
    // checking it!
    cy.get('@meanings')
      .contains('cite', 'CW')
      .and('have.css', 'vertical-align', 'super');
  });

  it('should display the full title of the source on hover', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'acâhkos');

    cy.get('.results .lexeme:first .meanings')
      .contains('cite', 'MD')
      .as('citation');

    cy.get('@citation')
      .trigger('mouseover');

    cy.get('.tooltip')
      .should('be.visible')
      .and('contain', 'Maskwacîs Cree Dictionary');
  });

  // XXX: blocked by https://github.com/UAlbertaALTLab/itwewina/issues/102
  it.skip('should separate translation groups with a semicolon', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'acosis');

    cy.get('.lexeme')
      .contains('.lexeme', 'acosis')
      .as('lexeme');

    cy.get('@lexeme').get('.meanings')
      .invoke('text')
      .should('match', /An arrow[.]?\s+MD/)  // translation 1
      .should('match', /arrow, little arrow\s+CW/)  // translation 2
      .should('match', /An arrow[.]?\s+MD;\s+arrow, little arrow\s+CW/); // together!
  });
});
