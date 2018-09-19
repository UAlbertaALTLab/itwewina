/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/59
 */

describe('Search with hyphens in syllabics', function () {
  const NNBSP = '\u202f';
  const NBSP = '\u00A0';
  const niwiNohteNipan = ['ᓂᐏ', 'ᓄᐦᑌ', 'ᓂᐸᐣ'];

  it('should allow for NNBSP as a replacement for hyphens', function () {
    cy.instantNeahttaSearch('crk', 'eng', niwiNohteNipan.join(NNBSP));
    cy.contains('a', 'nipâw');
  });

  it('should allow for spaces as a replacement for hyphens', function () {
    cy.instantNeahttaSearch('crk', 'eng', niwiNohteNipan.join(' '));
    cy.contains('a', 'nipâw');
  });

  it('should allow for NBSP as a replacement for hyphens', function () {
    cy.instantNeahttaSearch('crk', 'eng', niwiNohteNipan.join(NBSP));
    cy.contains('a', 'nipâw');
  });

  it('should allow for nothing at all as a replacement for hyphens', function () {
    cy.instantNeahttaSearch('crk', 'eng', niwiNohteNipan.join(''));
    cy.contains('a', 'nipâw');
  });
});
