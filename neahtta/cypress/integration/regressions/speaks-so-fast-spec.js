/**
 * Test the scenario described in MD_validation_170602.pptx:
 *
 * https://drive.google.com/open?id=0B3eCGz24iHRmSGpLUHNUakxxWFE
 */

describe('Masckwacîs Dictionary validation', function () {
  it('should find "nistohtat"', function () {
    cy.visit('/crk/eng');

    // Type "nistohtat" and do the search.
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
      .wait(50) /* Wait a bit so that the autocomplete doesn't eat up the first keypress. */
      .type('nistohtat');
    cy.get('form#neahttasaanit')
      .contains('.hidden-phone *', 'Search') // Click the desktop visible link
      .click();

    // Should be on a results page.
    cy.contains('√nistohtâ')
      .should('be.visible');
  });

  it('should find "speak"', function () {
    cy.visit('/crk/eng');

    cy.get('#left_nav')
      .contains('English → Plains Cree') // translate from English to nêhiyawêwin
      .click();

    // Search for "speak".
    cy.neahttaSearch('speak');

    // check that we're on the results page.
    cy.contains("speak (verb");
  });

  it('should find "cacâstapiwêt"', function () {
    cy.visit('/eng/crk/');

    // search for "fast".
    cy.neahttaSearch('fast');

    // Find "talking fast" on the results page.
    cy.contains('cacâstapiwêw')
      .click();

    // The basic paradigm should have the 3s+Conjuct form.
    cy.contains('ê-cacâstapiwêt')
      .should('be.visible');
  });

  it('should find "nisitohtatwêw"', function () {
    // Now, search for 'understand' on the detail page.
    cy.visit('/eng/crk/');

    // Search for "understand".
    cy.neahttaSearch('understand');

    // Click on the correct search result.
    cy.contains('nisitohtawêw')
      .click();

    // 3s→4, independent exists...
    cy.contains('nisitohtawêw')
      .should('be.visible');

    cy.contains('ê-nisitohtawât')
      .should('be.visible');

    cy.get('.nav')
      .contains('full').click();

    // X→3g (unspecified actor to 3rd person) should be in the full paradigm
    cy.contains('kâ-nistohtâht')
      .should('be.visible');
  });

  it('should find "âyiman"', function () {
    cy.visit('/crk/eng/');

    cy.neahttaSearch('ayiman');
    // We should be on the results page now.
    cy.contains('√âyiman');

    // There should be at least two entries: one for a noun, and one for a
    // verb.
    cy.get('a').contains('âyiman (Noun');
    cy.get('a').contains('âyiman (Verb');
  });

  it('should find "iyikohk"', function () {
    cy.visit('/crk/eng/');

    cy.neahttaSearch('iyikohk');
    // We should be on the results page now.

    // There should be at least this entry:
    cy.get('a').contains('iyikohk (particle');
  });

  it('should find "wanihtawêw"', function () {
    cy.visit('/eng/crk/');
    cy.neahttaSearch('misunderstand');
    cy.get('a')
      .contains('wanihtawêw');
  });

  it('should find "wani-"', function () {
    cy.visit('/crk/eng/');
    cy.neahttaSearch('wani-');
    cy.get('a')
      .contains('indistinctly, blurred');
  });
});
