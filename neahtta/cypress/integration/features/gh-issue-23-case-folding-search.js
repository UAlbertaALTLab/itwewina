/**
 * Case-folding in search.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/23
 */

describe('Case folding when searching', function () {
  it('should find the same results as with all lowercase', function () {
    cy.visit('/eng/crk');
    cy.neahttaSearch(funkUpTheCase('Car'));
    cy.contains('a', 'sêhkê-pimipayîs');
  });

  function funkUpTheCase(string) {
    if (!string.match(/\w{3,}/)) {
      throw new Error(`"${string}" is too small to funk up`);
    }

    let result = '';
    for (let c of string) {
      result += (Math.random() > .5) ? c.toUpperCase() : c.toLowerCase();
    }

    // Try funking up the case again. Will infinitely loop. 
    if (result === string) {
      return funkUpTheCase(string);
    }

    return result;
  }
});
