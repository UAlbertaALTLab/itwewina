Overview
========

Welcome to the [itwêwina]---a smart [Plains Cree] dictionary.

itwêwina uses [finite-state transducers][FST] to analyze the structure
of Cree words, as well as to conjugate Cree words.

There are many projects that tie into this effort: notably,
**[Giellatekno](#giellatekno)**---an infrastructure for creating language technology,
like the FSTs, and **[neahttadigisanít](#neahttadigisanít)**


Giellatekno
-----------


Neahttadigisanít
----------------


Minor projects
--------------

### [crk_orthography]

A bidirectional [SRO]/[syllabics] transliterator for Plains Cree.
[Try it here](https://crk-orthography-demo.herokuapp.com/)!
As of this writing, [crk_orthography] does NOT use FSTs to convert
between SRO and syllabics, however this may be possible in the future.
For more information on SRO/syllabics transliteration, see [its
documentation][crkdocs]. For more information on _why_ it was made, see
[this blog post][why-syllabics].

[SRO]: https://crk-orthography.readthedocs.io/en/stable/glossary.html#term-sro
[Syllabics]: https://crk-orthography.readthedocs.io/en/stable/glossary.html#term-syllabics
[crkdocs]: https://crk-orthography.readthedocs.io/en/stable/
[why-syllabics]: https://www.eddieantonio.ca/blog/2018/07/30/why-i-made-yet-another-cree-syllabics-converter/


### [nehiyawewin-syllabics]

A tab-separated CSV database of the Unicode characters used to write
Cree Y-dialect, a.k.a., Plains Cree. Useful for listing the subset of
characters from the [Unified Canadian Aboriginal Syllabics][ucas]
Unicode block, as well as listing the properties of each character.

[ucas]: https://en.wikipedia.org/wiki/Unified_Canadian_Aboriginal_Syllabics_(Unicode_block)


### [clean-wolvengrey]

The [ALTLab] team has a license to use the sources for [Dr. Arok
Wolvengrey][arok]'s [Cree: Words](https://uofrpress.ca/Books/C/Cree-Words)
Cree-English dictionary. [ALTLab] has the source to the dictionary in
a CSV file, but it has a few systematic issues. [clean-wolvengrey]
attempts to fix all of the issues.

---

Continue on to [Getting Started with Giellatekno!](./getting-started-giellatekno.md).


[ALTLab]: http://altlab.artsrn.ualberta.ca/
[arok]: http://fnuniv.ca/images/faculty/Wolvengrey_Aro.pdf
[clean-wolvengrey]: https://github.com/UAlbertaALTLab/clean-wolvengrey
[crk_orthography]: https://github.com/eddieantonio/crk_orthography
[FST]: ./finite-state-transducer.md
[itwewina]: http://altlab.ualberta.ca/itwewina/
[nehiyawewin-syllabics]: https://github.com/UAlbertaALTLab/nehiyawewin-syllabics
[Plains Cree]: https://en.wikipedia.org/wiki/Plains_Cree
