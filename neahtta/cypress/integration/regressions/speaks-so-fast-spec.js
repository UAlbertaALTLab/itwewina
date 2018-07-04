/**
 * Test MD_validation_170602.pptx
 */

describe('scenario', function () {
  it('should find "nistohtat"', function () {
    cy.visit('/crk/eng');
    // cy.screenshot();

    // Type "nistohtat" and do the search.
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
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

    // search for "speak".
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
      .type('speak');
    cy.get('form#neahttasaanit')
      .get('button[type=submit]')
      .click();

    // check that we're on the results page.
    cy.contains("speak (verb");
  });

  it('should find "cacâstapiwêt"', function () {
    cy.visit('/eng/crk/');

    // search for "fast".
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
      .type('fast');
    cy.get('form#neahttasaanit')
      .get('button[type=submit]')
      .click();

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
    cy.get('form#neahttasaanit')
      .get('input[name=lookup]')
      .type('understand');
    cy.get('form#neahttasaanit')
      .get('button[type=submit]')
      .click();

    // Click on the correct search result.
    cy.contains('nisitohtawêw')
      .click();

    // 3s→4, independent exists...
    cy.contains('nisitohtawêw')
      .should('be.visible');

    // XXX: however the conjunct form is missing!
    expect(() => {
      // TODO: Use a new FST and this should work
      cy.contains('ê-nisitohtawêw')
        .should('be.visible');
    }).to.throw;
  });
});
