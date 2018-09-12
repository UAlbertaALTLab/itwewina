describe("The basic noun paradigms", function () {

  it('should display all NI forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'astotin');
    cy.contains('a', 'astotin')
      .click();

    findRowInBasicParadigm('Singular', 'astotin');
    findRowInBasicParadigm('Plural', 'astotina');
    findRowInBasicParadigm('Locative', 'astotinihk');
    findRowInBasicParadigm('1s poss (sg)', 'nitastotin');
    findRowInBasicParadigm('2s poss (sg)', 'kitastotin');
    findRowInBasicParadigm('3s poss (sg)', 'otastotin');
  });

  it('should display all NA forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'niska');
    cy.contains('a', 'niska')
      .click();

    findRowInBasicParadigm('Singular', 'niska');
    findRowInBasicParadigm('Plural', 'niskak');
    findRowInBasicParadigm('Obviative', 'niska');
    findRowInBasicParadigm('Locative', 'niskihk');
    findRowInBasicParadigm('Distributive', 'niskinâhk');

    findRowInBasicParadigm('1s poss (sg)', 'niniskim');
    findRowInBasicParadigm('2s poss (sg)', 'kiniskim');
    findRowInBasicParadigm('3s poss (obv)', 'oniskima');
  });

  it('should display all NA-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'masakay');
    cy.contains('a', 'masakay')
      .click();

    findRowInBasicParadigm('1s poss (sg)', 'nasakay');
    findRowInBasicParadigm('2s poss (sg)', 'kasakay');
    findRowInBasicParadigm('3s poss (obv)', 'wasakaya');
    findRowInBasicParadigm('X poss (sg)', 'masakay');
    findRowInBasicParadigm('X poss (pl)', 'masakayak');
    findRowInBasicParadigm('X poss (obv)', 'masakaya');
  });

  it('should display all NI-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitêh');
    cy.contains('a', 'mitêh')
      .click();

    findRowInBasicParadigm('1s poss (sg)', 'nitêh');
    findRowInBasicParadigm('2s poss (sg)', 'kitêh');
    findRowInBasicParadigm('3s poss (sg)', 'otêh');
    findRowInBasicParadigm('X poss (sg)', 'mitêh');
    findRowInBasicParadigm('X poss (pl)', 'mitêha');
    findRowInBasicParadigm('X poss (loc)', 'mitêhihk');
  });


  function findRowInBasicParadigm(header, wordform) {
    // ensure this header is on the page.
    cy.get('table[data-type="basic"]')
      .contains('th', header)
      .should('be.visible')
      .then($headerCell => {
        let $wordforms = $headerCell.siblings('td');
        expect($wordforms.text()).to.include(wordform);
      });
  };
});
