﻿
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

    // TODO: where will we get the word forms from?
    // TODO: generate these in itwewina and place in a data-wordforms="" in
    // the definition, I guess?
    // TODO: where will we get the base URI from?
    $.getJSON(baseURI + wordform, function (data) {
        console.assert(data.length >= 1);
        var recordingData = data[0];

        // Place links in the page:
        //
        // a.play-audio
        // <a class="play-audio">
        //  <i class="icon-volume-up></i>
        //    🔈 Listen (Maskwacîs, ♀)
        // </a>
        var audio = new Audio(recordingData.recording_url);

        var $link = $(
            '<a href="#" class="play-audio">' +
            'Listen <i class="icon-volume-up"></i>:' +
            ' <span class="word-form"></span>' +
            // XXX: hard-coded spoken variety: Maskwacîs
            ' (Maskwacîs, <span class="speaker-gender"></span>)' +
            '</a>');

        $link.children('.word-form')
            .text(recordingData.wordform);
        console.assert(recordingData.gender === 'M' || recordingData.gender === 'F');
        $link.children('.speaker-gender')
            .text(recordingData.gender === 'M' ? '♂' : '♀');
        $link.click(function () {
            audio.play();
        });
        $('.lexeme').append($link);


        // Produce HTML like this...:
        // within lexeme, produce links
        // TODO: not dialect, but **variety**
        // TODO: Male/Female signs (like gen 2 pokêmon)
        /*
        <div class="audio-container">
            <a class="audio-link" data-audio-player="" data-audio-target="/itwewina/static/aud/crk/asiniy.mp3" target="blank" href="#">
                <i class="icon-volume-up"></i>
                <span class="audio-meta">
                    <span data-type="dialect">Maskwacîs</span>,
                    <span data-type="speaker">?</span>
                </span>
            </a>
        </div>
        */
    });

});
