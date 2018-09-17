/**
 * Tests that dictionary entries with ambiguous animacy have the correct
 * analysis.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/55
 */

describe('Nouns of ambiguous animacy', function () {
  /*
   * "mitâs" is both an animate and an inanimate noun.
   *
   * mitâs (NDA-1) -- legging/gaiter
   * mitâs (NDI-1) -- pair of pants
   */
  it('should provide the "inanimate" tag for the inanimate form', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitâs');
    cy.contains('a', /mitâs.+NDI/)
      .click();

    cy.url()
      .should('contain', 'detail');
    cy.contains(/mitâs.+NDI-1/);
    // We're on the detail page now for the INANIMATE noun.
    
    cy.get('.possible_analyses').as('analyses');

    cy.get('@analyses')
      .contains('Inanimate');
  });

  it('should provide the "animate" tag for the animate form', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitâs');
    cy.contains('a', /mitâs.+NDA/)
      .click();

    cy.url()
      .should('contain', 'detail');
    cy.contains(/mitâs.+NDA-1/);
    // We're on the detail page now for the ANIMATE noun.
    
    cy.get('.possible_analyses').as('analyses');

    cy.get('@analyses')
      .contains('Animate');
  });

  it.only('should match PxX nouns in syllabics', function () {
    // Searching for syllabics should work.
    cy.instantNeahttaSearch('crkS', 'eng', 'nohkom');

    // It should contain the stem in SRO.
    cy.contains(/[ᑯᑰ]ᐦᑯᒼ/);
    // cy.contains('-ohkom');
  });
});
