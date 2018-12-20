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

  it('should separate translation groups with a semicolon', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ahkameyihtam');

    cy.get('.lexeme')
      .contains('.lexeme', 'âhkamêyihtam')
      .as('lexeme');

    let translation1 = /He keeps on thinking of what has to be done[.]?\s+MD/
    let translation2 = /s\/he continues to think of future deeds or tasks[.]?\s+CW/;
    let both = new RegExp(`${translation1.source};\\s+${translation2.source}|` +
                          `${translation2.source};\\s+${translation1.source}`);
    cy.get('@lexeme').get('.meanings')
      .invoke('text')
      .should('match', translation1)
      .should('match', translation2)
      .should('match', both); // together!
  });
});
