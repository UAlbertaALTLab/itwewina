The XML Dictionary format
-------------------------

The dictionaries are stored in an *ad hoc* dictionary format. There
appears to be many different variants of the format originally designed
in Giellatekno for Northern Saami.


The original documentation for this format is [here][original-docs], but
it's in Norwegian. There's also a tiny bit of documentation inline in
[the DTD file][gt_dictionary.dtd], but, as it claims:

> This document is not quite finished yet...

Here's an informal description of the XML format.


```xml
<e src="the title of the source dictionary">
    <lg>
        <l pos="N">mitâs</l> <!-- Lemma with its part-of-speech as an attribute -->
        <lc>NDI-1</lc>   <!-- the "lemma comment" --
                              crk uses this to disambiguate forms within parts-of-speech. -->
    </lg>
    <mg><!-- the definitions, but I don't care about this here --></mg>
</e>
```

Hey, guess what! I also didn't document all of this yet. Pester me in the GitHub issues to finish this: <https://github.com/UAlbertaALTLab/itwewina/issues/63>

[original-docs]: http://giellatekno.uit.no/doc/dicts/dictionarywork.html
[gt_dictionary.dtd]: https://victorio.uit.no/langtech/trunk/words/dicts/scripts/gt_dictionary.dtd
