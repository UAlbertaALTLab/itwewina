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
    // Mock the endpoint
    cy.route(recordingSearchPattern, 'fixture:recording/_search/nikiskisin.json')
      .as('getRecordings');

    // Find 'kiskisiw'
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    cy.contains('a', 'kiskisiw').click();

    // The website SHOULD make a request to get a list of recordings.
    cy.wait('@getRecordings');

    return;

    // TODO: mock the audio
    // TODO: fixture for the file

    // There should be 6 audio clips
    cy.get('audio')
      .should('have.lengthOf', 6)
      .invoke('play');

    // TODO: ensure the audio got requested/played
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
