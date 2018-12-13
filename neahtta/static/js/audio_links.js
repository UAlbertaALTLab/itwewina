
// https://github.com/scottschiller/SoundManager2/
//
// http://www.schillmania.com/projects/soundmanager2/doc/getstarted/#basic-inclusion


// TODO: add loading and playing icons
$(document).ready(function(){
    soundManager.setup({
      url: '../vendor/SoundManager2/swf/',
      flashVersion: 9, // optional: shiny features (default = 8)
      // optional: ignore Flash where possible, use 100% HTML5 mode
      // preferFlash: false,
      onready: function() {
        // Ready to use; soundManager.createSound() etc. can now be called.
        console.log("soundmanager ready");
      }
    });

    $('[data-audio-player]').click( function(btn){

       btn.preventDefault();

       audio = $(btn.target).attr('data-audio-target')
             || $(btn.target).parents('a.audio-link').attr('data-audio-target');

       function finished_event() {
         soundManager.destroySound('dictionary-player');
         return true;
       }

       function get_player() {
         sound_obj = soundManager.createSound({
           id: "dictionary-player",
           url: '',
           onfinish: finished_event
           // onerror: error_event
           // onplay: begin_event
           // whileloading: whileload_event
         });
         // sound_obj._a.playbackRate = opts.rate;
         return sound_obj;

       }

       sound_obj = get_player();
       sound_obj.url = audio;

       sound_obj.play({position:0});

    });
});

/** == <audio> tag stuff == **/
$(function () {
    // TODO: derive this from configuration.
    var baseURI = 'http://localhost:8000/recording/_search/';

    // TODO: Look for the wordforms in the .lexeme[data-recording-wordforms]
    var wordform = 'nikiskisin';

    $.getJSON(baseURI + wordform, function (data) {
        if (data.length === 0) {
            return;
        }

        var $recordings = $('<div class="recordings">');
        data.forEach(function (recording) {
            $recordings.append(makeRecordingAudioLink(recording));
        });
        $('.lexeme').append($recordings);
    });

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
        $link.click(function () {
            audio.play();
        });

        return $link;
    }
});
