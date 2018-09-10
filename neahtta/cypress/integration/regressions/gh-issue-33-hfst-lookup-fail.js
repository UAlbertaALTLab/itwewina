describe('When HFST does not match a form', function () {
  it('should display as hyphens in the paradigm', function () {
    // TODO: This might need a better example of a word with out an analysis.
    cy. instantNeahttaSearch('crk', 'eng', 'wâpamêw');
    cy.contains('a', 'wâpamêw')
      .click();

    // View the full paradigm
    cy.get('.nav')
      .contains('full').click();

    // There might be this mess of tags here; it really should not be there.
    cy.get('#paradigm-tab-3 > .miniparadigm')
      .should('not.contain', 'Imp+Imm+2Sg+4Sg/PlO');
  });
});
