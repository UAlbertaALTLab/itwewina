/**
 * TODO: description.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/92
 */
describe('Maskwacîs recordings integration', function () {
  const recordingSearchPattern =
    /^https?:[/][/]localhost:8000[/]recording[/]_search[/][^/]+$/;
  const recordingAudioPattern =
    /^https?:[/][/]localhost:8000[/]recording[/][^.]+[.]mp4$/;

  beforeEach(function () {
    cy.server();
  });

  it('should produce recordings for +V+AI+Indep+Pret+1Sg', function () {
    // Mock the API endpoint; we want to provide it our own data.
    cy.route(recordingSearchPattern, 'fixture:recording/_search/nikiskisin.json')
      .as('searchRecordings');
    // Mock the audio as well.
    cy.route(recordingAudioPattern, 'fixture:recording/tone220.mp4')
      .as('audioRecording');

    // Find 'kiskisiw'
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    cy.contains('a', 'kiskisiw').click();

    // TODO: Make sure the different word forms are on the page.
    false && cy.get('.lexeme[data-recording-word-forms]')
      .should(($lexeme) => {
        var expected = ['nikiskisin', 'kiskisiw', 'ê-kiskisit'];
        var actual = $lexeme.data('recording-word-forms').split(',');
        debugger;
        expect(actual.sort()).to.deepEqual(expected.sort());
      });

    // The website SHOULD make a request to get a list of recordings.
    cy.wait('@searchRecordings');

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();

    cy.wait('@audioRecording');
  });

  it.skip('should produce recordings for PV/e+...+V+AI+Conj+Pret+3Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-sôhkêyimot');
  });

  it.skip('should produce recordings for PV/e+...+V+TA+Conj+Pret+X+1SgO', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-kiskisototâht');
  });

  it.skip('should produce recordings for +V+TI+Indep+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'nimihtâtên');
  });

  it.skip('should produce recordings for PV/e+...+V+TI+Conj+Pret+1Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'ê-mihtâtamân');
  });

  it.skip('should produce recordings for +V+II+Indep+Pret+3Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'pîtosinâkwan');
  });

  it.skip('should produce recordings for +N+I+Sg', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiskisiwin');
  });

  it.skip('should produce recordings for +IPJ', function () {
    cy.instantNeahttaSearch('crk', 'eng', 'kiyâm');
  });
});
