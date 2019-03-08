/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/86
 */
describe('GitHub issue 86: mobile paradigms', function () {
  beforeEach(function () {
    // Addressable resolution of many Samsung smartphones:
    // https://mediag.com/blog/popular-screen-resolutions-designing-for-all/
    cy.viewport(360, 760);
  });

  it('should be able to switch the visible paradigm', function () {
    // Get to the detail page of 'mitêh'
    cy.instantNeahttaSearch('crk', 'eng', 'miteh');
    cy.contains('.lexeme a', 'mitêh').click();
    cy.url().should('contain', 'detail');

    // Open the paradigm display, should display basic paradigm.
    cy.get('.miniparadigm').should('not.be.visible');
    cy.contains('button', 'Paradigm').click();
    cy.get('.miniparadigm[data-type="basic"]').should('be.visible');

    // Access the full paradigm.
    cy.contains('[data-toggle="tab"]', 'full').click();
  });
});
