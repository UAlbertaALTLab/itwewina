/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/108
 */
describe('The English to Plains Cree dictionary', function () {
  it('should contain translations from Cree : Words', function () {
    cy.instantNeahttaSearch('eng', 'crk', 'hobble');
    cy.contains('.lexeme', 'napwahpitêw')
      .as('entry');
    // It should have the truncated gloss:
    cy.get('@entry')
      .contains('hobble s.o');
    // It should have the source.
    cy.get('@entry')
      .contains('cite', 'CW');
  });

  it('should contain translations from the Maskwacîs Dictionary', function () {
    cy.instantNeahttaSearch('eng', 'crk', 'hive');
    cy.contains('.lexeme', 'amowaciston')
      .as('entry');
    // It should have the truncated gloss:
    cy.get('@entry')
      .contains("a bee's nest");
    // It should have the source.
    cy.get('@entry')
      .contains('cite', 'MD');
  });

  it('should contain translations from the both dictionaries (shared truncated definition)', function () {
    cy.instantNeahttaSearch('eng', 'crk', 'Dipper');
    cy.contains('.lexeme', 'ocêkatâhk')
      .as('entry');
    // It should have the truncated gloss:
    cy.get('@entry')
      .contains('the Big Dipper, the Great Bear');
    // It should have both sources:
    cy.get('@entry')
      .contains('cite', 'MD')
    cy.get('@entry')
      .contains('cite', 'CW');
  });

  it('should contain translations from the both dictionaries (separate truncated definitions)', function () {
    cy.instantNeahttaSearch('eng', 'crk', 'pow-wow');
    cy.contains('.lexeme', 'pwâtisimowin')
      .as('entry');
    // It should have the truncated gloss:
    cy.get('@entry')
      .contains('pow-wow dancing')
      .contains('cite', 'MD')
    // It should have both sources:
    cy.get('@entry')
      .contains('the Grass Dance')
      .contains('cite', 'CW');
  });
});
