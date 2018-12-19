/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/5
 */

describe('The "itwêwina" logo', function () {
  it('should display with a circumflexed ê in crk', function () {
    cy.visit('/crk/eng');
    cy.logoContains('itwêwina');
  });

  it("should display with a macron'd ē in crkMacr", function () {
    cy.visit('/crkMacr/eng');
    cy.logoContains('itwēwina');
  });

  it('should display in syllabics in crkS', function () {
    cy.visit('/crkS/eng');
    cy.logoContains('ᐃᑘᐏᓇ');
  });

  it('should display with a circumflexed ê by default', function () {
    cy.visit('/');
    cy.logoContains('itwêwina');
  });
});
