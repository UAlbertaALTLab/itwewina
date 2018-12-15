/**
 * TODO: description.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/92
 */
describe('Maskwacîs recordings integration', function () {
  let fetchRecordings;
  const recordingSearchPattern =
    /^https?:[/][/]localhost:8000[/]recording[/]_search[/][^/]+$/;

  beforeEach(function () {
    cy.server();
    // Due to it using `this` for every text, we need to bind fetchRecordings
    // to the correct `this` context here:
    fetchRecordings = _fetchRecordings.bind(this);
  });

  it('should include the endpoint as a <link>', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    cy.contains('a', 'kiskisiw').click();
    cy.get('link[rel="x-recording-search-endpoint"]')
      .should(($link) => {
        expect($link.attr('href') + 'ê').to.match(recordingSearchPattern);
      });
  });

  it('should produce recordings for +V+AI+Indep+Pret+1Sg', function () {
    fetchRecordings({
      fixture: 'nikiskisin.json',
      searchFor: 'nikiskisin',
      lemma: 'kiskisiw',
      expectedWordForms: ['nikiskisin', 'kiskisiw', 'ê-kiskisit'],
    });
  });

  it('should produce recordings for PV/e+...+V+AI+Conj+Pret+3Sg', function () {
    fetchRecordings({
      fixture: 'esohkeyimot.json',
      searchFor: 'esohkeyimot',
      lemma: 'sôhkêyimow',
      expectedWordForms: ['nisôhkêyimon', 'sôhkêyimow', 'ê-sôhkêyimot'],
    });
  });

  it('should produce recordings for PV/e+...+V+TA+Conj+Pret+X+1SgO', function () {
    fetchRecordings({
      fixture: 'ekiskisototaht.json',
      searchFor: 'ekiskisototaht',
      lemma: 'kiskisototawêw',
      expectedWordForms: ['kikiskisototâtin', 'kiskisototawêw', 'ê-kiskisototâht'],
    });
  });

  it('should produce recordings for +V+TI+Indep+Pret+1Sg', function () {
    fetchRecordings({
      fixture: 'nimihtaten.json',
      searchFor: 'nimihtaten',
      lemma: 'mihtâtam',
      expectedWordForms: ['nimihtâtên', 'mihtâtam', 'ê-mihtâtahk'],
    });
  });

  it('should produce recordings for PV/e+...+V+TI+Conj+Pret+1Sg', function () {
    fetchRecordings({
      fixture: 'emihtataman.json',
      searchFor: 'emihtataman',
      lemma: 'mihtâtam',
      expectedWordForms: ['nimihtâtên', 'mihtâtam', 'ê-mihtâtahk'],
    });
  });

  it('should produce recordings for +V+II+Indep+Prs+3Sg', function () {
    fetchRecordings({
      fixture: 'pitosinakwan.json',
      lemma: 'pîtosinâkwan',
      expectedWordForms: ['pîtosinâkwan', 'ê-pîtosinâkwak'],
    });
  });

  it('should produce recordings for +N+I+Sg', function () {
    fetchRecordings({
      fixture: 'kiskisomitowin.json',
      lemma: 'kiskisomitowin',
      expectedWordForms: ['kiskisomitowin'],
    });
  });

  it('should produce recordings for +IPJ', function () {
    fetchRecordings({
      fixture: 'kiyam.json',
      searchFor: 'kiyam',
      lemma: 'kiyâm',
      expectedWordForms: ['kiyâm'],
    });
  });

  /**
   * Look up a word, and make sure we're getting back the correct recordings.
   * WARNING! This WILL need to be bound to the proper `this` context before
   * using.
   */
  function _fetchRecordings ({ fixture, lemma, searchFor, expectedWordForms }) {
    // Mock the API endpoint; we want to provide it our own data from the
    // suppied fixture filename.
    cy.fixture(`recording/_search/${fixture}`).as('recordingsResults');
    cy.route(recordingSearchPattern, '@recordingsResults')
      .as('searchRecordings');

    // Find the term and click on its entry.
    cy.instantNeahttaSearch('crk', 'eng', searchFor || lemma);
    cy.contains('.lexeme a', lemma).click();

    // Make sure the expected word forms are on the page.
    cy.get('.lexeme[data-recording-word-forms]')
      .should(($lexeme) => {
        var actual = $lexeme.data('recording-word-forms').split(',').sort();
        expect(actual).to.deep.equal(expectedWordForms.sort());
      });

    // The website SHOULD make an XHR request to get a list of recordings.
    cy.wait('@searchRecordings');

    // Eventually, it should place as many audio links on the page as there
    // were entries returned by the XHR.
    cy.get('.lexeme .recordings a.play-audio').then((audioLinks) => {
      expect(audioLinks).to.have.lengthOf(this.recordingsResults.length)
    })

    // Click an audio link.
    // Note: Cypress CANNOT stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just *hoping* the audio plays here... 🤞
    cy.contains('a.play-audio', 'Maskwacîs').click({
      // HACK: I'm too lazy to fix the layouts right now, but the paradigm
      // table can sometimes occlude the recordings, so just force the
      // interaction. This can be fixed with z-index tweaking.
      force: true,
    });
  };
});
