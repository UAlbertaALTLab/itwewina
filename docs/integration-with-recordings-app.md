Integration with recordings app
===============================

itwêwina dynamically links to recordings stored and managed by the
Maskwacîs Recordings Validation Interface ([website][validation],
[GitHub repository][recval-repo]). Henceforth, I'll refer to the
recordings app as "`recval`".


How does it work?
-----------------

In a nutshell, itwêwina comes up with a few [word forms][] to look up
for _exact matches_ in `recval`. itwêwina (with client-side JavaScript)
uses `recval`'s [search API][recval-api] to find matching recordings,
along with metadata, including the speaker's code and gender. This is
then turned into appropriate HTML elements that are embedded in the
entry detail page.

### Important files:

 - `neahtta/configs/itwewina.config.yaml` or `neahtta/configs/itwewina.config.yaml.in`
 - `neahtta/views/search.py`
 - `neahtta/configs/language_specific_rules/templates/itwewina/includes.template`
 - `neahtta/configs/language_specific_rules/templates/detail_entry.template`
 - `neahtta/static/js/audio_links.js`

### Server-side details

First of all, itwêwina needs to know the URI of `recval`'s API endpoint.
This is specified in the application's settings (e.g.,
`neahtta/configs/itwewina.config.yaml`). The URI is a simple string to
the *exact* endpoint, minus path/query arguments. Here's an example of
the YAML file:

```yaml
ApplicationSettings:
  # ... other settings ...
  recordings_endpoint:
    'http://sapir.artsrn.ualberta.ca/validation/recording/_search/'
```

Next, some candidate word forms must be generated. Since `recval` does
not incorporate any computational models, it cannot figure out all
recordings for a given lemma. Instead, you must ask for the _precise_
word form, including diacritics for long vowels.

itwêwina generates candidate word forms in `views/search.html`. In
`determine_recording_word_forms()`, itwêwina generates multiple
candidates for the various different kinds of verbs; for (independent)
nouns and non-inflecting parts-of-speech, the lemma is used.

The list of candidate word forms is passed to the `detail_entry`
template, under the `recording_word_forms` template variable. Each
`.lexeme` HTML element gets a `data-recording-word-forms` attribute for
the list of recordings word forms.

In the `includes` template, the `recordings_endpoint` configuration is
embedded within a link header:

```html
<link rel="x-recording-search-endpoint" href="//domain.tld/endpoint/api/">
```

`audio_links.js` is included here as well.


### Client-side details

At each page load, when `[data-recording-word-forms]` attribute is
found, the JavaScript on the page will use the [`recval`'s API
endpoint][recval-api] to request a list of recordings. Either the
endpoint 404s — no suitable recordings are found, or the endpoint will
return one or more recordings details with an URI to the `.m4a` audio.

The JavaScript then creates a series of links that, when clicked, will
play the corresponding audio.

[recval-api]: https://github.com/UAlbertaALTLab/recording-validation-interface#web-api
[recval-repo]: https://github.com/UAlbertaALTLab/recording-validation-interface
[validation]: http://sapir.artsrn.ualberta.ca/validation/
[word forms]: ./glossary.md#word-form
