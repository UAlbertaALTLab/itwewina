/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/2
 */
describe('The language selector', function () {
  it('should have a button for each language', function () {
    cy.visit('/');

    cy.get('[data-cy=language-select]').as('langs');
    cy.get('@langs')
      .contains('a, button', 'nêhiyawêwin')
      .contains('a, button', 'English')
      .contains('a, button', 'ᓀᐦᐃᔭᐍᐏᐣ');
  });
});
