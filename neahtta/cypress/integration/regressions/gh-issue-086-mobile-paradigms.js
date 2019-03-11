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

    // The page should display the basic paradigm.
    cy.get('.miniparadigm[data-type="basic"]')
      .should('be.visible');

    // Access the full paradigm.
    cy.contains('[data-toggle="tab"]', 'full').click();

    // We can see the labels of the full paradigm at least.
    cy.contains('.miniparadigm[data-type="full"] th', "someone's")
      .should('be.visible')

    // Now navigate back to the basic paradigm.
    cy.contains('[data-toggle="tab"]', 'basic').click();
    cy.get('.miniparadigm[data-type="basic"]')
      .should('be.visible');
  });
});
