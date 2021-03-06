/**
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/85
 */
describe('Non-linguistic paradigms', function () {
  it('should exist for NA nouns', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'miskinahk');
    cy.contains('a', 'miskinâhk').click();

    // Will load a new page
    cy.contains('a', 'basic')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=basic]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'One')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'Many')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'my')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'your')
      .should('be.visible');
  });

  it('should exist for NI nouns', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'osi');
    cy.contains('a', 'ôsi').click();

    // Will load a new page
    cy.contains('a', 'basic')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=basic]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'One')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'Many')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'my')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'your')
      .should('be.visible');
  });

  it('should exist for NAD nouns', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nimosom');
    cy.contains('a', 'nimosôm').click();

    // Will load a new page
    cy.contains('a', 'basic')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=basic]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'my')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'your')
      .should('be.visible');
  });

  it('should exist for NID nouns', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'miteh');
    cy.contains('a', 'mitêh').click();

    // Will load a new page
    cy.contains('a', 'basic')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=basic]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'my')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'your')
      .should('be.visible');
  });

  it('should exist for VTA verbs', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'miyew');
    cy.contains('a', 'miyêw').click();

    // Will load a new page
    cy.contains('a', 'basic')
      .click();
    // Try out a few of the simplified header names.
    cy.get('.miniparadigm[data-type=basic]').as('paradigm')
    cy.get('@paradigm')
      .contains('th', 'you (one) → me')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 'I → you (one)')
      .should('be.visible');
    cy.get('@paradigm')
      .contains('th', 's/he → him/her/them (further)')
      .should('be.visible');
  });
});
