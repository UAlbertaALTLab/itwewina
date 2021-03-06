// For Firefox: reenable buttons when back button is pressed
$(window).bind("unload", function() {
    $('input').attr('readonly', false);
    $('button').attr('disabled', false);
});

$(document).ready( function() {
    var $searchForm = $('form#neahttasaanit');
    // Select everything when the document loads
    // $('input[name="lookup"]').select();

    // Doublecheck focus-- need to retrigger the event because sometimes it
    // isn't properly trigggered 
    //
    if($(document).width() > 801) {
        setTimeout(function() {
            $('input[name="lookup"]').focus().select();
        }, 120);
    }

    // Setup the autocomplete dropdown box with an old version of Bootstrap Typeahead:
    var item_count = parseInt($('input[name="lookup"]').attr('data-items')) || 5;
    $('input[name="lookup"]').typeahead({
        items: item_count,
        // Load the autocomplete results via an AJAX call.
        source: function (typeahead, query) {
            if (query.length > 1) {
                var _from = typeahead.$element.attr('data-language-from')
                    , _to = typeahead.$element.attr('data-language-to')
                    , default_autocomplete = '/autocomplete/' + _from + '/' + _to + '/'
                    ;
                var url = $('input[name="lookup"]').attr('data-autocomplete-path') || default_autocomplete;
                return $.get(url, { lookup: query }, function (data) {
                    return typeahead.process(data);
                });
            } else {
                return [] ;
            }
        },
        // Immediately perform search when selected or when <enter> is pressed.
        onselect: performSearch,
        onenter: performSearch,
    });
    $('input').focus(function(evt) {
        $('input').attr('readonly', false);
        $('button').attr('disabled', false);
    });

    $('form').submit(function(evt) {
        var inputs = $(evt.target).find('input[type="text"], input[name="lookup"]')
          , target = $(evt.target).find('button[type=submit][clicked=true]')
          , submit = $(evt.target).find('button[type="submit"]')
          ;

        // Discourage submission if there is nothing to submit
        for (_i = 0, _len = inputs.length; _i < _len; _i++) {
            i = inputs[_i];
            if ($(i).val().length === 0) {
                return false;
            } else {
                continue;
            }
        }

        // Okay! Looking up something!
        // While we wait, disable the current search box.
        inputs.prop("readonly", true);
        submit.prop("disabled", true);

        // Re-enable the form elements after a delay.
        setTimeout(function(){
            inputs.prop("readonly", false);
            submit.prop("disabled", false);
        }, 1000);

    });

    // Initiates the search with whatever's typed in the form.
    function performSearch() {
        $searchForm.submit();
    }
});

// vim: set ts=4 sw=4 tw=0 syntax=javascript :
