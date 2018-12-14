/**
 * TODO: description.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/92
 */
describe('Maskwacîs recordings integration', function () {
  const recordingSearchPattern =
    /^https?:[/][/]localhost:8000[/]recording[/]_search[/][^/]+$/;

  beforeEach(function () {
    cy.server();
  });

  it.skip('should include the endpoint as a <link>', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    cy.contains('a', 'kiskisiw').click();
    cy.get('link[rel="x-recording-search-endpoint"]')
      .should(($link) => {
        expect($link.attr('href') + 'ê').to.match(recordingSearchPattern);
      });
  });

  function fetchRecordings({ fixture, lemma, searchFor, expectedWordForms }) {
    // Mock the API endpoint; we want to provide it our own data from the
    // suppied fixture filename.
    cy.route(recordingSearchPattern, `fixture:recording/_search/${fixture}`)
      .as('searchRecordings');

    // Find the term and click on its entry.
    cy.instantNeahttaSearch('crk', 'eng', searchFor || lemma);
    cy.contains('a', lemma).click();

    // Make sure the expected word forms are on the page.
    cy.get('.lexeme[data-recording-word-forms]')
      .should(($lexeme) => {
        var actual = $lexeme.data('recording-word-forms').split(',').sort();
        expect(actual).to.deep.equal(expectedWordForms.sort());
      });

    // The website SHOULD make an XHR request to get a list of recordings.
    cy.wait('@searchRecordings');
  }

  it('should produce recordings for +V+AI+Indep+Pret+1Sg', function () {
    fetchRecordings({
      fixture: 'nikiskisin.json',
      searchFor: 'nikiskisin',
      lemma: 'kiskisiw',
      expectedWordForms: ['nikiskisin', 'kiskisiw', 'ê-kiskisit'],
    });
    // Eventually, it should place 6 (see the fixture) audio recordings.
    cy.get('.lexeme .recordings a.play-audio')
      .should('have.lengthOf', 6);

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();
    // Note: Cypress cannot stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just hoping the audio plays here... 🤞
  });

  it('should produce recordings for PV/e+...+V+AI+Conj+Pret+3Sg', function () {
    fetchRecordings({
      fixture: 'esohkeyimot.json',
      searchFor: 'esohkeyimot',
      lemma: 'sôhkêyimow',
      expectedWordForms: ['nisôhkêyimon', 'sôhkêyimow', 'ê-sôhkêyimot'],
    });

    // Eventually, it should place 6 (see the fixture) audio recordings.
    cy.get('.lexeme .recordings a.play-audio')
      .should('have.lengthOf', 3);

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();
    // Note: Cypress cannot stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just hoping the audio plays here... 🤞
  });

  it.skip('should produce recordings for PV/e+...+V+TA+Conj+Pret+X+1SgO', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-kiskisototâht');
  });

  it('should produce recordings for +V+TI+Indep+Pret+1Sg', function () {
    fetchRecordings({
      fixture: 'nimihtaten.json',
      searchFor: 'nimihtaten',
      lemma: 'mihtâtam',
      expectedWordForms: ['nimihtâtên', 'mihtâtam', 'ê-mihtâtahk'],
    });

    // Eventually, it should place 6 (see the fixture) audio recordings.
    cy.get('.lexeme .recordings a.play-audio')
      .should('have.lengthOf', 6);

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();
    // Note: Cypress cannot stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just hoping the audio plays here... 🤞
  });

  it.skip('should produce recordings for PV/e+...+V+TI+Conj+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-mihtâtamân');
  });

  it('should produce recordings for +V+II+Indep+Prs+3Sg', function () {
    fetchRecordings({
      fixture: 'pitosinakwan.json',
      lemma: 'pîtosinâkwan',
      expectedWordForms: ['pîtosinâkwan', 'ê-pîtosinâkwak'],
    });

    // Eventually, it should place 6 (see the fixture) audio recordings.
    cy.get('.lexeme .recordings a.play-audio')
      .should('have.lengthOf', 6);

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();
    // Note: Cypress cannot stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just hoping the audio plays here... 🤞
  });

  it.skip('should produce recordings for +N+I+Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiskisiwin');
  });

  it.skip('should produce recordings for +IPJ', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiyâm');
  });
});
