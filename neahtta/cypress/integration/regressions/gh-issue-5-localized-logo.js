/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/5
 */

describe('The "itwêwina" logo', function () {
  it('should display with a circumflexed ê by default', function () {
    cy.visit('/crk/eng');
    cy.get('a.brand')
      .contains('*', 'itwêwina', { timeout: 0 });
  });

  it("should display with a macron'd ē in crkMacr", function () {
    cy.visit('/crkMacr/eng');
    cy.get('a.brand')
      .contains('*', 'itwēwina', { timeout: 0 });
  });
});
