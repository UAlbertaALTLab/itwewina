/**
 * Nouns with OBLIGATORY POSSESSION and cannot have "unspecified
 * possessor" ("non-PxX nouns") should link to their lemma, which is in the
 * first-person possessor form ("Px1Sg").
 *
 * For example, "kôhkom" is *your* grandmother. There can't just be a 
 * "grandmother"; she has to be my grandmother, your grandmother, or their
 * grandmother! These are non-PxX nouns.
 *
 * Historically, we'd present non-PxX nouns as the stem, and link to the
 * Px1Sg form of the noun with a <lemma_ref> element in the dictionary, but
 * this turns out to be inelegant.
 * 
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/57
 */
describe('Non-PxX NDA nouns', function () {
  it('should have lemmas in the Px1Sg form', function () {
    // Search for "kokom", which should match the Px2Sg form of "nôhkom".
    cy.instantNeahttaSearch('crk', 'eng', 'kokom');

    // The lexical entry should be nôhkom! The Px1Sg form of the word.
    cy.get('.lexeme')
      .contains('a', /nôhkom\s+[(]Noun/);
  });

  it('should have a NDA paradigm, with missing unspecified actor entries', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kokom');

    // The lexical entry should be nôhkom! The Px1Sg form of the word.
    cy.contains('.lexeme a', /nôhkom\s+[(]Noun/)
      .click();

    cy.contains('td', 'nôhkom');
    cy.contains('td', 'kôhkom');
    cy.contains('td', 'ôhkom');
  });
});
