/**
 * What info will we provide per each recording?
 * See: https://github.com/UAlbertaALTLab/itwewina/issues/100
 */

describe('Recordings meta information', function () {
  const recordingSearchPattern =
    /^https?:[/][/]localhost:8000[/]recording[/]_search[/][^/]+$/;

  beforeEach(function () {
    cy.server();
  });

  it("should display the word form, and the speaker's name", function () {
    // Provide our own data for the endpoint.
    cy.route(recordingSearchPattern, [
      // nikostên, as spoken by kîsikâw
      {
        "wordform": "nikostên",
        "speaker": "GOR",
        "speaker_name": "kîsikâw",
        "anonymous": false,
        "gender": "M",
        "recording_url": "http://sapir.artsrn.ualberta.ca/validation/recording/a7b75da2410ef401efd5249aa2932b6eb54c765a97fccb121388d3d72a93b4fe.m4a"
      },
      // ê-kostahk, as spoken by Rosie
      {
        "wordform": "êkostahk",
        "speaker": "ROS2",
        "speaker_name": "Rosie Rowan",
        "anonymous": false,
        "gender": "F",
        "recording_url": "http://sapir.artsrn.ualberta.ca/validation/recording/77719aa2329d8c54609d5c393a1e7fb5b771fc110434e3a9a9c92ebc817a38d6.m4a"
      },
      {
        "wordform": "kostam",
          "speaker": "ROS2",
          "speaker_name": "Rosie Rowan",
          "anonymous": false,
          "gender": "F",
          "recording_url": "http://sapir.artsrn.ualberta.ca/validation/recording/69d6e1f43cf793c89c93d5c05398743596da230abe0bd8f1dab9b58dbba271d2.m4a"
      },
    ])
      .as('searchRecordings');

    // Get to the details page, where the recordings are actually loaded.
    cy.instantNeahttaSearch('crk', 'eng', 'kostam');
    cy.contains('.lexeme:first a', 'kostam').click();
    cy.url()
      .should('match', /[/]detail[/].+[/]kostam\b/);

    // Wait for the results to come back.
    cy.wait('@searchRecordings');

    // Mini-regression test. Original results looked like this:
    //    Listen: lemma (Maskwacîs, Gender)
    // New format is:
    //    lemma (Speaker name, Maskwacîs)
    // Ensure the old format is GONE!
    cy.get('.recordings')
      .contains('.play-audio', 'kostam')
      .should('not.contain', 'Listen')
      .and('not.contain', '♀')
      .should('contain', 'kostam')
      .and('contain', 'Rosie Rowan')
      .and('contain', 'Maskwacîs)');

    // Find nikostên
    cy.get('.recordings')
      .contains('.play-audio', 'nikostên')
      .should('contain', 'kîsikâw')

    // Find ê-kostahk
    cy.get('.recordings')
      .contains('.play-audio', 'êkostahk')
      .should('contain', 'Rosie Rowan');
  });
});
