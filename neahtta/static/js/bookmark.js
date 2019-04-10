// bookmark.js: the actual code in the bookmarklet!
//
// NOTE ABOUT MODIFYING THIS FILE:
// All lines beginning with optional whitespace followed by //
// are removed.
// All newlines are removed.
// There is no more minification than that!
// The string literals that look like {{VARIABLE}} are placeholders -- they are
// intentionally replaced with alternate Note that there cannot be a spaces in
// the placeholder.

(function() {
  var NDS_API_HOST = "{{NDS_API_HOST}}",
    NDS_MEDIA_HOST = "{{NDS_MEDIA_HOST}}",
    BOOKMARKLET_VERSION = "0.0.4",
    // TODO: support https://
    scheme = "file:" === window.location.protocol ? "http:" : "",
    link = document.createElement("link"),
    script = document.createElement("script");

  // Get the CSS styles for the reader
  link.href = scheme + NDS_MEDIA_HOST + "/static/css/jquery.neahttadigisanit.css";
  link.rel = "stylesheet";

  // Get the full source code of the reader.
  script.type = "text/javascript";
  script.src = scheme + NDS_MEDIA_HOST + "/static/js/bookmarklet.min.js";

  // Set some global variables; the scripts will need them
  window['NDS_API_HOST'] = NDS_API_HOST;
  window['NDS_BOOKMARK_VERSION'] = BOOKMARKLET_VERSION;
  document.getElementsByTagName("head")[0].appendChild(link);
  document.getElementsByTagName("body")[0].appendChild(script);
})();
