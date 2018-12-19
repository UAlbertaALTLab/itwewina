/** == <audio> tag stuff == **/
$(function () {
    // Get the base URI from the link header.
    var baseURI = $('link[rel="x-recording-search-endpoint"]').attr('href');

    /* Fetch recordings for each valid searchable word form on the page. */
    $('.lexeme[data-recording-word-forms]').each(function () {
        var $lexeme = $(this);
        var wordforms = $lexeme.data('recording-word-forms');
        fetchRecordings($lexeme, wordforms);
    });

    function fetchRecordings($lexeme, wordforms) {
        var $recordings = $lexeme.find('.recordings');
        $.getJSON(baseURI + wordforms)
            .done(function (data) {
                if (data.length === 0) {
                    return;
                }

                data.forEach(function (recording) {
                    $recordings.append(makeRecordingAudioLink(recording));
                });

                // Reveal the recordings pane once it finally loads.
                $recordings.hide().show('slow');
                $lexeme.append($recordings);
            })
            .fail(function (jqXHR) {
                var $message = $('<p class="loading-failed"></p>');
                $message.text('No recordings found.')
                $recordings.append($message);
            })
            .always(function () {
                $recordings.find('.loading-indicator').remove();
                // I expect the item to never change after this, so tell
                // assistive technologies this!
                $recordings.attr('aria-live', 'off');
            });
    }

    function makeRecordingAudioLink(recording) {
        // Create the <a> link, substituting required information.
        var $link = $(
            '<a href="#" class="play-audio">' +
            '<i class="icon-volume-up"></i> ' +
            ' <span class="word-form"></span>' +
            // XXX: hard-coded spoken variety: Maskwacîs
            ' (<span class="speaker-name"></span>, Maskwacîs)' +
            '</a>');
        $link.children('.word-form')
            .text(recording.wordform);
        $link.children('.speaker-name')
            .text(recording.speaker_name);

        var audio = new Audio(recording.recording_url);
        // Don't preload the audio! Otherwise, this will make LOTS of requests
        // on some pages, that will ultimately go unused.
        audio.preload = 'none';

        $link.click(function (event) {
            event.preventDefault(); // don't jump around on the page.
            audio.play();
        });

        return $link;
    }
});
