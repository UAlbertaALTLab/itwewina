/**
 * There should be indication when the audio is loading.
 *
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/97
 */
describe('Loading audio', function () {
  const recordingSearchPattern =
    /^https?:[/][/]localhost:8000[/]recording[/]_search[/][^/]+$/;

  beforeEach(function () {
    cy.server();
  });

  it('should display a loading widget on page load', function () {
    // Provide our own data for the endpoint.
    cy.route({
      url: recordingSearchPattern,
      response: 'fixture:recording/_search/kostam.json',
      delay: 1000,
    })
      .as('searchRecordings');

    // Get to the details page, where the recordings are actually loaded.
    cy.instantNeahttaSearch('crk', 'eng', 'kostam');
    cy.contains('.lexeme:first a', 'kostam').click();
    cy.url()
      .should('match', /[/]detail[/].+[/]kostam\b/);

    cy.get('.lexeme:first .recordings').as('recordings');

    // At this point, there should be a loading indicator.
    cy.get('@recordings')
      .get('.loading-indicator')
      .should('be.visible');

    // Wait for the results to come back.
    cy.wait('@searchRecordings');

    // The loading indicator should disappear now!
    cy.get('@recordings')
      .should('not.have.descendants', '.loading-indicator');
  });
});
