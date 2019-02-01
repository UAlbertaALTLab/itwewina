describe("The basic noun paradigms", function () {
  it('should display all NI forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'astotin');
    cy.contains('a', 'astotin')
      .click();

    findRowInLinguisticParadigm('Singular', 'astotin');
    findRowInLinguisticParadigm('Plural', 'astotina');
    findRowInLinguisticParadigm('Locative', 'astotinihk');
    findRowInLinguisticParadigm('1s', 'nitastotin');
    findRowInLinguisticParadigm('2s', 'kitastotin');
    findRowInLinguisticParadigm('3s', 'otastotin');
  });

  it('should display all NA forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'niska');
    cy.contains('a', 'niska')
      .click();

    findRowInLinguisticParadigm('Singular', 'niska');
    findRowInLinguisticParadigm('Plural', 'niskak');
    findRowInLinguisticParadigm('Obviative', 'niska');
    findRowInLinguisticParadigm('Locative', 'niskihk');
    findRowInLinguisticParadigm('Distributive', 'niskinâhk');

    findRowInLinguisticParadigm('1s', 'niniskim');
    findRowInLinguisticParadigm('2s', 'kiniskim');
    findRowInLinguisticParadigm('3s', 'oniskima');
  });

  it('should display all NA-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'masakay');
    cy.contains('a', 'masakay')
      .click();

    findRowInLinguisticParadigm('1s', 'nasakay');
    findRowInLinguisticParadigm('2s', 'kasakay');
    findRowInLinguisticParadigm('3s', 'wasakaya');
    findRowInLinguisticParadigm('X', 'masakay');
    findRowInLinguisticParadigm('X', 'masakayak');
    findRowInLinguisticParadigm('X', 'masakaya');
  });

  it('should display all NI-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitêh');
    cy.contains('a', 'mitêh')
      .click();

    findRowInLinguisticParadigm('1s', 'nitêh');
    findRowInLinguisticParadigm('2s', 'kitêh');
    findRowInLinguisticParadigm('3s', 'otêh');
    findRowInLinguisticParadigm('Singular', 'mitêh');
    findRowInLinguisticParadigm('Plural', 'mitêha');
    findRowInLinguisticParadigm('Locative', 'mitêhihk');
  });


  function findRowInLinguisticParadigm(header, wordform) {
    // ensure this header is on the page.
    cy.contains('.nav a', 'linguistic')
      .click();

    cy.get('table[data-type="linguistic"]')
      .contains('th', header)
      .should('be.visible')
      .then($headerCell => {
        let $wordforms = $headerCell.siblings('td');
        expect($wordforms.text()).to.include(wordform);
      });
  };
});
