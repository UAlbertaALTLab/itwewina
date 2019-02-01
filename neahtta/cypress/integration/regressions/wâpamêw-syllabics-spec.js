/**
 * Tests for previous app regressions that should continue working.
 */

describe('Display of syllabic codas', function () {
  it('should render wâpamêw+V+TA+Ind+Prs+3Sg+4Sg/PlO as ᐘᐸᒣᐤ', function () {
    cy.visit('/');

    cy.get('#left_nav')
      .contains('ᒐᐦᑲᓯᓇᐦᐃᑲᐣ') // Use syllabics written variant.
      .click();

    // Type "ᐘᐸᒣᐤ" in the search box, and do the search.
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
      .wait(50) /* Wait a bit so that typing won't eat keypresses! */
      .type('ᐘᐸᒣᐤ');
    cy.get('form#neahttasaanit')
      .contains('button:visible', /Search|nitona|ᓂᑐᓇ/) // Search!
      .click();

    // Should have gone to the search results page.
    // XXX: Navigating doesn't change the URL, so the best thing to do is to
    // check if a result appeared on the page.
    cy.contains(/√wâpam/);

    // Click the search result for "wâpamêw".
    cy.contains('ᐚᐸᒣᐤ')
      .click();

    var ᐘᐸᒣᐤ_percent_encoded = encodeURIComponent('ᐚᐸᒣᐤ');

    // We should navigate to a page.
    cy.url()
      .should('include', 'detail')
      .should('include', ᐘᐸᒣᐤ_percent_encoded);

    // Get the full paradigm.
    cy.contains('a', 'linguistic')
      .click();

    cy.get('.miniparadigm[data-type="linguistic"]')
      .as('paradigm')
      .should('be.visible', true);

    // Find the derivation in the full paradigm tab.
    cy.get('@paradigm')
      .contains('3s → 4')
      .parents('tr').first()
      .contains('ᐚᐸᒣᐤ')
      .should('be.visible', true);
  });
});
