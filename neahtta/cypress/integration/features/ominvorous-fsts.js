/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/43
 */
describe('Ominvorous lookups', function () {
  const syllabicsSearch = 'ᓃᐱᕀ';
  const circumflexSearch = 'nîpiy';
  const macronSearch = 'nīpiy';

  it('should search in circumflexes at the homepage', function () {
    cy.visit('/');
    cy.neahttaSearch(circumflexSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nîpiy');
  });

  it('should search in macrons at the homepage', function () {
    cy.visit('/');
    cy.neahttaSearch(macronSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nîpiy');
  });

  it('should search in syllabics at the homepage', function () {
    cy.visit('/');
    cy.neahttaSearch(syllabicsSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nîpiy');
  });

  it('should search in syllabics in syllabics mode', function () {
    cy.visit('/crkS/eng');
    cy.neahttaSearch(syllabicsSearch);
    cy.contains('a', 'ᓂᐱᕀ');
    cy.contains('a', 'ᓃᐱᕀ');
  });

  it('should search in circumflexes in syllabics mode', function () {
    cy.visit('/crkS/eng');
    cy.neahttaSearch(circumflexSearch);
    cy.contains('a', 'ᓂᐱᕀ');
    cy.contains('a', 'ᓃᐱᕀ');
  });

  it('should search in macrons in syllabics mode', function () {
    cy.visit('/crkS/eng');
    cy.neahttaSearch(macronSearch);
    cy.contains('a', 'ᓂᐱᕀ');
    cy.contains('a', 'ᓃᐱᕀ');
  });

  it('should search in macrons in macron mode', function () {
    cy.visit('/crkMacr/eng');
    cy.neahttaSearch(macronSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nīpiy');
  });

  it('should search in circumflexes in macron mode', function () {
    cy.visit('/crkMacr/eng');
    cy.neahttaSearch(circumflexSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nīpiy');
  });

  it('should search in syllabics in macron mode', function () {
    cy.visit('/crkMacr/eng');
    cy.neahttaSearch(circumflexSearch);
    cy.contains('a', 'nipiy');
    cy.contains('a', 'nīpiy');
  });
});
