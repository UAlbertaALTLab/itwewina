/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/2
 */
describe('The language selector', function () {
  it('should have a button for each language', function () {
    cy.visit('/');

    cy.get('nav [data-cy=language-selector').as('langs');
    cy.get('langs')
      .contains('a, button', 'nê')
      .contains('a, button', 'en')
      .contains('a, button', 'ᓀ');
  });
});
