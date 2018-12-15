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
        $.getJSON(baseURI + wordforms, function (data) {
            if (data.length === 0) {
                return;
            }

            var $recordings = $('<div class="recordings">');
            data.forEach(function (recording) {
                $recordings.append(makeRecordingAudioLink(recording));
            });

            // Reveal the rec;ordings pane once it finally loads.
            $recordings.hide().show('slow');
            $lexeme.append($recordings);
        });
    }

    function makeRecordingAudioLink(recording) {
        // Create the <a> link, substituting required information.
        var $link = $(
            '<a href="#" class="play-audio">' +
            '<i class="icon-volume-up"></i> Listen:' +
            ' <span class="word-form"></span>' +
            // XXX: hard-coded spoken variety: Maskwacîs
            ' (Maskwacîs, <span class="speaker-gender"></span>)' +
            '</a>');
        $link.children('.word-form')
            .text(recording.wordform);
        console.assert(recording.gender === 'M' || recording.gender === 'F');
        $link.children('.speaker-gender')
            .text(recording.gender === 'M' ? '♂' : '♀');

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
