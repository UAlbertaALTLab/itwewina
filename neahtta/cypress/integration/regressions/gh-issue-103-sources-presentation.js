/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/103
 */
describe('Source superscripts', function () {
  it('should be unique in eng->crk', function () {
    cy.instantNeahttaSearch('eng', 'crk', 'dog');
    cy.contains('.lexeme span[lang=crk]', 'a dog.')
      .as('entry');
    cy.get('@entry')
      .contains(/beast of burden\W*CW/)
      .contains(/a dog[.]\W*MD/);
  });

  it('should be unique in crk->eng', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'wîtaskîwin');
    cy.contains('.lexeme', /Wetaskiwin,\s+AB\W*CW/)
      .as('entry');
    cy.get('@entry')
      .should('not.contain', 'CWCW')
      .contains(/peace, truce, alliance\W*CW/);
  });
});
