/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/85
 */
describe('Non-linguistic paradigms', function () {
  it.only('should exist for na nouns', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'miskinahk');
    cy.contains('a', 'miskinâhk').click();

    // Will load a new page
    cy.contains('a', 'plain')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=plain]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'One')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'Many')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'my')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'your')
      .should('be.visible');
  });

  it('should exist for nad nouns', function () {
    // FAIL
    cy.get('body').should('be.falsy');
  });

});
