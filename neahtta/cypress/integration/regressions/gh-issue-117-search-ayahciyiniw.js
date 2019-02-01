/**
 * Searching for 'ayahciyiniw' yields 500 error:
 * KeyError: u'maskwacis_dictionary in template </templates/itwewina/about.template>'
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/113
 */
describe('GitHub issue 117', function () {
  it('should not crash when searching for "ayahciyiniw"', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ayahciyiniw');
    cy.contains('.lexeme:first a', 'ayahciyiniw');
  });
});
