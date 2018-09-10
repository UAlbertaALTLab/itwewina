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
