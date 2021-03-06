###

A jQuery plugin for allowing users to click to look up words
from Neahttadigisánit dictionary services.

###

Templates = require './templates'
Selection = require './selection'
DictionaryAPI = require './dictionary'
DSt = require('./DSt').DSt
Semver = require '../lib/semver'
JQZIndex = require('lib/jquery.topZindex')

selectionizer = new Selection()
templates = new Templates()

SpinnerHex = """data:image/gif;base64,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"""

# Wrap jQuery and add plugin functionality
jQuery(document).ready ($) ->

  _ = module.fakeGetText

  getHostShortname = (url_path) ->
    url = document.createElement('a')
    url.href = url_path
    host = url.hostname
    if host
      return host.split('.')[0]
    return false

  first = (somearray) ->
    if somearray.length > 0
      return somearray[0]
    else
      return false

  # A shortcut

  # Global values set by the bookmarklet init script or manual inclusion
  API_HOST = window.NDS_API_HOST || window.API_HOST
  window.NDS_SHORT_NAME = getHostShortname(API_HOST)

  window.nds_exports = {}

  # Increment this whenever the bookmarklet code (_not this file_) has changed.
  # This way the plugin will notify users to update their bookmark.
  EXPECT_BOOKMARKLET_VERSION = '0.0.4'

  initSpinner = () ->
    ###
        spinner popup in right corner; `spinner = initSpinner()` to
        create or find, then usual `spinner.show()` or `.hide()` as
        needed.
    ###
    spinnerExists = $(document).find('.spinner')
    if spinnerExists.length == 0
      spinner = $("""<img src="#{SpinnerHex}" class="spinner" />""")
      $(document).find('body').append(spinner)
      return spinner
    return spinnerExists

  ## Some global ajax stuff
  ##
  ## 

  $.ajaxSetup
    timeout: 10 * 1000
    beforeSend: (args) ->
      spinner = initSpinner()
      spinner.show()
    complete: (args) ->
      spinner = initSpinner()
      spinner.hide()
    dataType: "json"
    cache: true
    error: () =>
      $(document).find('body').find('.errornav').remove()
      $(document).find('body').append templates.ErrorBar {
        host: API_HOST
      }

  ##
  ## NDS Functionality
  ## 

  dictionary = new DictionaryAPI {
    host: "/"
  }

  cleanTooltipResponse = (selection, response, opts) ->
    ###
        Clean response from tooltip $.post query, and display results
    ###

    string   = selection.string
    element  = selection.element
    range    = selection.range

    if opts.tooltip
      # TODO: expand wrapped range to include MWEs
      #
      _wrapElement = $("""
      <a style="font-style: italic; border: 1px solid #CEE; padding: 0 2px" 
         class="tooltip_target">#{string}</a>
      """)[0]
      selectionizer.surroundRange(range, _wrapElement)

    templates.renderPopup(response, selection)

  lookupSelectEvent = (evt, string, element, range, opts, full_text) ->

    result_elem = $(document).find(opts.formResults)

    # Remove punctuation, some browsers select it by default with double
    # click
    string = $.trim(string)
    # TODO: this doesn't seem to actually be adhering to \b, or is considering
    # - surroundings to be part of \b and thus stripping word-internal -. Need
    # to replace with beginning and ends, but evaluate first whether this is
    # actually necessary
    # .replace(/\b[-.,()&$#!\[\]{}"]+\B|\B[-.,()&$#!\[\]{}"]+\b/g, "")

    settings = NDS.$.fn.getCurrentDictOpts().settings
    if settings.multiword_lookups
      if (string.length > 120)
        console.log "DEBUG: string was too long."
        console.log string.length
        return false
    else
      if (string.length > 60) or (string.search(' ') > -1)
        console.log "DEBUG: string was too long or contained spaces."
        console.log string.length
        return false

    langpair = DSt.get(NDS_SHORT_NAME + '-' + 'digisanit-select-langpair')
    # "aaa-bbb"
    [source_lang, target_lang] = langpair.split('-')
    lookup_string = string

    # Now why am I doing it this way? provide default pair from menu?
    _cp = first NDS.options.dictionaries.filter (e) =>
      e.from.iso == source_lang and e.to.iso == target_lang
    
    if _cp?
      uri = _cp.uri
    else
      uri = false

    window.cp = _cp

    post_data =
      lookup: lookup_string
      lemmatize: true

    # TODO: results should be displayed clearly: currently if there's a match
    # in two things for the same result, it isn't clear which is for which
    #
    if settings.multiword_lookups
      post_data.multiword = true
      _min = settings.multiword_range[0]
      _max = settings.multiword_range[1]

      mws = selectionizer.getMultiwordPermutations(_min, _max)

      # TODO: filter only on permitted mwes from list? 
      # TODO: now that we're sending json, can drop the join
      post_data.lookup = mws

    url = "#{opts.api_host}#{uri}"

    response_func = (response, textStatus) =>
      selection = {
        string: string
        element: element
        range: range
      }
      cleanTooltipResponse(selection, response, opts)

    # TODO: this will need to use POST if we end up sending the whole text
    # string due to size limitations with HTTP parameters, however some
    # problems to overcome:
    #
    # * POST: server will need an OPTIONS request for this endpoint to tell the
    # client it is allowed to make the crossdomain request.
    #
    # * jsonp is GET only, thus will have a limitation
    #
    # $.post(url, post_data, response_func, "json")

    $.ajax({
      url: url,
      type: "POST",
      contentType: "application/json; charset=UTF-8",
      # dataType: "jsonp",
      data: JSON.stringify post_data
    }).done(response_func)

    return false

  ##
   # $(document).selectToLookup();
   #
   #
   ##

  $.fn.selectToLookup = (opts) ->
    opts = $.extend {}, $.fn.selectToLookup.options, opts
    NDS.options = opts
    spinner = initSpinner()

    if window.NDS_API_HOST || window.API_HOST
      window.API_HOST = window.NDS_API_HOST || window.API_HOST
      if /\/$/.test(window.API_HOST)
        window.API_HOST = window.API_HOST.slice(0, window.API_HOST.length - 1)
    if NDS.options.api_host
      if /\/$/.test(NDS.options.api_host)
        NDS.options.api_host = NDS.options.api_host.slice(0, NDS.options.api_host.length - 1)
      window.API_HOST = NDS.options.api_host

    if 'file:' == window.location.protocol
      window.API_HOST = 'http:' + '//' + window.API_HOST
      NDS.options.api_host = window.API_HOST
    if 'http:' not in window.API_HOST or 'https:' not in window.API_HOST
      window.API_HOST = window.location.protocol + '//' + window.API_HOST
      NDS.options.api_host = window.API_HOST

    window.NDS_SHORT_NAME = getHostShortname(NDS.options.api_host)

    # version notify
    newVersionNotify = () ->
      $.getJSON(
        NDS.options.api_host + '/read/update/json/' + '?callback=?'
        (response) ->
          $(document).find('body').append(
            templates.NotifyWindow(response)
          )
          $(document).find('#notifications').modal({
            backdrop: true
            keyboard: true
          })
          $('#close_modal').click () ->
            $('#notifications').modal('hide')
            DSt.set(NDS_SHORT_NAME + '-' + 'digisanit-select-langpair', null)
            DSt.set(NDS_SHORT_NAME + '-' + 'nds-languages', null)
            DSt.set(NDS_SHORT_NAME + '-' + 'nds-localization', null)
            DSt.set(NDS_SHORT_NAME + '-' + 'nds-stored-config', null)
            window.location.reload()
            return false
      )
      return false

    window.newVersionNotify = newVersionNotify

    ie8Notify = () ->
      $.getJSON(
        NDS.options.api_host + "/read/ie8_instructions/json/" + '?callback=?'
        (response) ->
          $(document).find('body').prepend(
            templates.NotifyWindow(response)
          )
          $(document).find('#notifications').modal({
            backdrop: true
            keyboard: true
          })
          $('#close_modal').click () ->
            $('#notifications').modal('hide')
            DSt.set(NDS_SHORT_NAME + '-' + 'nds-ie8-dismissed', true)
            return false
      )
      return true

    window.ie8Notify = ie8Notify

    # This runs after either we get the response from the server about
    # language pairs and internationalization, or recover it from local
    # storage.
    initializeWithSettings = () ->
      # Delete temporary thing.
      delete window.lookup_regex

      if NDS.options.displayOptions
          
        $(document).find('body').append templates.OptionsTab(NDS.options)
        window.optTab = $(document).find('#webdict_options')
        ### Over 9000?!! ###
        window.optTab.css('z-index', 9000)
        $(document).find('#webdict_options').topZIndex()
        # Demote common social stuff
        $(document).find('#lessbuttons_holder').css({
            'z-index': 5000,
        })

      # Recall stored language pair from session
      previous_langpair = DSt.get(
        NDS_SHORT_NAME + '-' + 'digisanit-select-langpair'
      )
      if previous_langpair
        _select = "select[name='language_pair']"
        _opt = window.optTab.find(_select).val(previous_langpair)
      else
        if NDS.options.default_language_pair
          [_from, _to] = NDS.options.default_language_pair
          _select = "select[name='language_pair'] option[value='#{_from}-#{_to}']"
          _opt = window.optTab.find(_select).val()
          previous_langpair = DSt.set(NDS_SHORT_NAME + '-' + 'digisanit-select-langpair', _opt)
        else
          _select = "select[name='language_pair']"
          _opt = window.optTab.find(_select).val()
          previous_langpair = DSt.set(NDS_SHORT_NAME + '-' + 'digisanit-select-langpair', _opt)
      
      holdingOption = (evt) =>
        clean(evt)

        if evt.altKey
          element = evt.target
          within_options = $(element).parents('#webdict_options')
          if within_options.length > 0
            $(within_options[0]).find('#debug').show()
            return false
          [range, full_text] = selectionizer.getFirstRange()
          string = selectionizer.cloneContents(range)
          if range and string
            lookupSelectEvent(evt, string, element, range, NDS.options, full_text)
          return false
        return true

      clean = (event) ->
        parents = []
        $(document).find('a.tooltip_target').each () ->
          parents.push $(this).parent()
          $(this).popover('destroy')
          $(this).replaceWith(this.childNodes)
        $(document).find('a.tooltip_target').contents().unwrap()
        selectionizer.cleanRange()

      window.cleanTooltips = clean
      $(document).bind('click', holdingOption)

    storeConfigs = (response) ->
      # store in local storage
      DSt.set(NDS_SHORT_NAME + '-' + 'nds-languages',    response.dictionaries)
      DSt.set(NDS_SHORT_NAME + '-' + 'nds-localization', response.localization)
      DSt.set(NDS_SHORT_NAME + '-' + 'nds-stored-config', "true")
      return true

    extendLanguageOpts = (response) =>
      window.r_test = response
      NDS.options.dictionaries = response.dictionaries
      NDS.options.localization = response.localization
      NDS.options.default_language_pair = response.default_language_pair
      storeConfigs(response)
      return

    fetchConfigs = () ->
      console.log "trying " + NDS.options.api_host
      url = "#{NDS.options.api_host}/read/config/"
      $.getJSON(
        url + '?callback=?'
        extendLanguageOpts
      )

    extendLanguageOptsAndInit = (response) =>
      extendLanguageOpts(response)
      initializeWithSettings()

    recallLanguageOpts = () =>
      # Sometimes this ends up not getting parsed from JSON
      # automatically from DSt.get, even though .set properly stores it.
      locales = DSt.get(NDS_SHORT_NAME + '-' + 'nds-localization')
      if typeof locales == "string"
        locales = JSON.parse locales
      NDS.options.localization = locales

      # dicts = DSt.get(NDS_SHORT_NAME + '-' + 'nds-languages')
      # if typeof dicts == "string"
      #   dicts = JSON.parse dicts
      # NDS.options.dictionaries = dicts

      initializeWithSettings()


    ##
    ## Check the version of the bookmark and compare with what the
    ## plugin desires, and also check for IE8. If either of these is
    ## true, then we display some notifications to the user that they
    ## need to change some settings or update.
    ##

    version_ok = false

    if window.NDS_BOOKMARK_VERSION?
      version_ok = Semver.gte( window.NDS_BOOKMARK_VERSION
                             , EXPECT_BOOKMARKLET_VERSION
                             )
    else
      version_ok = true

    uagent = navigator.userAgent
    [old_ie, dismissed] = [false, false]
    if "MSIE 8.0" in uagent
      old_ie = true
      dismissed = DSt.get(NDS_SHORT_NAME + '-' + 'nds-ie8-dismissed')

    if version_ok
      if old_ie
        console.log "ie8 detected"
        if not dismissed
          ie8Notify()
      # stored_config = DSt.get(NDS_SHORT_NAME + '-' + 'nds-stored-config')
      # if stored_config?
      #   recallLanguageOpts()
      url = "#{opts.api_host}/read/config/"
      $.getJSON(
        url + '?callback=?'
        extendLanguageOptsAndInit
      )
      return false
    else
      newVersionNotify()
      return false

    # TODO: one idea for how to handle lookups wtihout alt/option key
    #
    # else
    #   if string != ''
    #     window.optTab.find('.well').addClass('highlight')
    #     window.optTab.find('.well a.open').click (o) =>
    #       lookupSelectEvent(evt, string, element, index, opts)
    #       return false
    #   else
    #     window.optTab.find('.well').removeClass('highlight')

  $.fn.setDefaultPair = () ->
    # If nothing is returned, then the user probably switched projects or
    # somehow a default option wasn't set, so we pick the first in order for
    # the rest of the lookup to work, and 
    _default = NDS.options.dictionaries[0]
    _default_iso = "#{_default.from.iso}-#{_default.to.iso}"

    console.log "picking default: #{_default_iso}"
    $('select[name=language_pair]').val(_default_iso)
    optsp = NDS.$('div.option_panel')
    optsp.show()
    # optsp.find('a.close').toggle()
    return _default

  $.fn.getOptsForDict = (_from, _to) ->
    for dict in NDS.options.dictionaries
      if dict.from.iso == _from and dict.to.iso == _to
        return dict
    console.log "#{_from}-#{_to} pair doesn't exist in this project"
    return $.fn.setDefaultPair()

  # TODO: what to do when nothing is set
  $.fn.getCurrentDictOpts = () ->
    pair = DSt.get(NDS_SHORT_NAME + '-' + 'digisanit-select-langpair')
    console.log "checking #{NDS_SHORT_NAME}"
    console.log pair
    [_from, _to] = pair.split('-')
    NDS.$.fn.getOptsForDict _from, _to

  $.fn.selectToLookup.options =
    api_host: API_HOST
    formResults: "#results"
    sourceLanguage: "sme"
    langPairSelect: "#webdict_options *[name='language_pair']"
    tooltip: true
    # Provide a word regex to improve the selection system.
    languageWordOptions: false
    displayOptions: true
    dictionaries: [
      {
        from:
          iso: 'sme'
          name: 'nordsamisk'
        to:
          iso: 'nob'
          name: 'norsk'
        uri: '/lookup/sme/nob/'
      }
    ]

# End jQuery wrap
