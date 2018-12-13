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

  it('should produce recordings for +V+AI+Indep+Pret+1Sg', function () {
    // Mock the API endpoint; we want to provide it our own data.
    cy.route(recordingSearchPattern, 'fixture:recording/_search/nikiskisin.json')
      .as('searchRecordings');

    // Find 'kiskisiw' and click on its entry.
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

    // The website SHOULD make an XHR request to get a list of recordings.
    cy.wait('@searchRecordings');

    // Eventually, it should place 6 (from fixture) audio recordings.
    cy.get('.lexeme .recordings a.play-audio')
      .should('have.lengthOf', 6);

    // Click an audio link.
    cy.contains('a.play-audio', 'Maskwacîs').click();
    // Note: Cypress cannot stub responses from an <audio> element.
    // As well, asserting an a <audio> played is not directly supported:
    // https://github.com/cypress-io/cypress/issues/1750#issuecomment-392132279
    // So we're just hoping the audio plays here... 🤞

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
