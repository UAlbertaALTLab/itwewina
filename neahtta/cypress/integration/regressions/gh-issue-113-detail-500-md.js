/**
 * Clicking on details yields 500 error:
 * KeyError: u'maskwacis_dictionary in template </templates/itwewina/about.template>'
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/113
 */
describe('GitHub issue 113', function () {
  it('should not crash when clicking on a details page', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'maskosis');
    cy.contains('.lexeme:first a', 'maskosis')
      .click();

    cy.url()
      .should('contain', '/detail/');

    // We should not see the crash!
    cy.get('body')
      .should('not.contain', 'KeyError');
  });
});
