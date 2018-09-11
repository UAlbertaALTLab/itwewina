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
    findRowInBasicParadigm('3s poss (sg)', 'oniskima');
  });

  it('should display all NI-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitâs');
    // There are both animate and inanimate pants.
    // Choose the inanimate pants.
    cy.contains('a', /mitâs\b.+NDI-1/)
      .click();

    findRowInBasicParadigm('1s poss (sg)', 'nitâs');
    findRowInBasicParadigm('2s poss (sg)', 'kitâs');
    findRowInBasicParadigm('3s poss (obv)', 'otâsa');
    findRowInBasicParadigm('X poss (sg)', 'mitâs');
    findRowInBasicParadigm('X poss (pl)', 'mitâsak');
    findRowInBasicParadigm('X poss (obv)', 'mitâsa');
  });

  it('should display all NA-D forms', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'mitêh');
    cy.contains('a', 'mitêh')
      .click();

    findRowInBasicParadigm('1s poss (sg)', 'nitêh');
    findRowInBasicParadigm('2s poss (sg)', 'kitêh');
    findRowInBasicParadigm('3s poss (obv)', 'otêh');
    findRowInBasicParadigm('X poss (sg)', 'mitêh');
    findRowInBasicParadigm('X poss (pl)', 'mitêha');
    // TODO: should this be obviative ("someone's heart")
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
