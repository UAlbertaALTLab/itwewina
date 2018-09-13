/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/46
 */

describe('The "Search in texts" link', function () {
  it('should redirect to a lemma search in Korp', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nokom');

    cy.get('.entry_row:first')
      .contains('a', /\b(masinahikêwina|Texts)\b/)
      .then($a => {
        expect($a.attr('href')).to.match(/^https?:[/][/]altlab.ualberta.ca[/]korp[/]/);
      });
  });
});
