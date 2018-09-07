/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/39
 */

describe('The paradigm table', function () {
  it('should display only unique elements in each cell', function () {
    cy.visit('/crk/eng');
    // Search for a transitive-animate verb; the most complex verb!
    cy.neahttaSearch('wâpamêw');
    cy.contains('a', 'wâpamêw')
      .click();

    // View the full paradigm
    cy.get('.nav')
      .contains('full').click();

    cy.contains('td', 'kiwâpamitin').then($cell => {
      const wordforms = words($cell.text());
      const uniqueWordforms = new Set(wordforms);

      // If there are duplicates, wordforms.length would be greater than the
      // number of unique wordforms.
      expect(wordforms.length).to.equal(uniqueWordforms.size);
    });
  });
});

function words(text) {
  return text.trim().split();
}
