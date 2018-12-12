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
    cy.route(recordingSearchPattern, [
      {
        "gender": "F",
        "recording_url": "http://localhost:8000/recording/7353dda3d48799325ee62de0eceb4b50839382cfcf0ebf96c70d84fd37881201.m4a",
        "speaker": "ROS",
        "wordform": "nikiskisin"
      },
      {
        "gender": "F",
        "recording_url": "http://localhost:8000/recording/dac08c374354594b7a77195daa4fd2e12a88acc5acf4e4894dd612354c1e7a92.m4a",
        "speaker": "ROS",
        "wordform": "nikiskisin"
      },
      {
        "gender": "M",
        "recording_url": "http://localhost:8000/recording/1576034645a6b765ab40275a67390fa197ee3c7ed8cc949907d132df3c0f1c9e.m4a",
        "speaker": "GOR",
        "wordform": "nikiskisin"
      },
      {
        "gender": "M",
        "recording_url": "http://localhost:8000/recording/a86939d888ff908d091538b2c1a3dc4fb383167b781b5dddddd4253342b0dace.m4a",
        "speaker": "GOR",
        "wordform": "nikiskisin"
      },
      {
        "gender": "F",
        "recording_url": "http://localhost:8000/recording/2198ff134107ff474115cdb48ee36f88c17168e215fe424da4cc414bab0f4582.m4a",
        "speaker": "LOU",
        "wordform": "nikiskisin"
      },
      {
        "gender": "F",
        "recording_url": "http://localhost:8000/recording/e8dd10846601861c1e9c4edf944b1e4da7670ed669fe027bd0b27e0af954e031.m4a",
        "speaker": "LOU",
        "wordform": "nikiskisin"
      }
    ]).as('getRecordings');

    // Find 'kiskisiw'
    cy.instantNeahttaSearch('crk', 'eng', 'nikiskisin');
    cy.contains('a', 'kiskisiw').click();

    // The website SHOULD make a request to get a list of recordings.
    cy.wait('@getRecordings');

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
