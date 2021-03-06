The XML Dictionary format
-------------------------

The dictionaries are stored in an *ad hoc* dictionary format. There
appears to be many different variants of the format originally designed
in Giellatekno for Northern Saami.

The original documentation for this format is [here][original-docs], but
it's in Norwegian. There's also a tiny bit of documentation inline in
[the DTD file][gt_dictionary.dtd], but, as it claims:

> This document is not quite finished yet...

---

This is a description of the XML format as it is used in itwêwina.
A single dictionary XML file is a collection of **dictionary entries**
(the _lexicon_) that have translations that are cited from one or more
**dictionary sources**.

The original XML dictionary format appears to support more use cases,
but we have opted to focus on a few key use cases pertinent to Plains
Cree.

  - Plains Cree to English
  - English to Plains Cree

The two dictionary directions differ a bit in their required fields, and
intended usage.


## `<r>`: The root element

The root element is `<r>`. `<r>` contains:

 - zero or more `<source>` elements
 - zero or more `<e>` elements

By convention, all `<source>` elements go near the top of the file, then
the `<e>` elements follow alphabetically (according to their lemma).
There will be far fewer `<source>` elements than `<e>` elements.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<r>
    <!-- dictionary sources -->
    <source id="..."> ... </source>
    <source id="..."> ... </source>
    <source id="..."> ... </source>

    <!-- dictionary entries -->
    <e> ... </e>
    <e> ... </e>
    <e> ... </e>
</r>
```


## `<source>`: Dictionary source

A **dictionary source** is the metadata for a particular source of
definitions. Think of it like a bibliography entry.

`<source>` contains one required attribute, `id=""`, and exactly one
required child: `<title>`.

### Required attributes

 - `id=""` a machine-readable ID used by `<t>` elements to "cite" which
   source it comes from. This is similar to `id=""` attributes in HTML.
   The ID **SHOULD** be a short, ASCII-representable string, containing
   only alphanumerics (U+0030—U+0039, U+0041–U+005A, U+0061–U+007A) and
   the hyphen-minus character (U+002D). The ID **MUST NOT** contain any
   spacing or format characters.

### Required children

 - `<title>`: contains the title of the dictionary source in plain text.

### Example

`<t>` and `<trunc>` elements will cite the following source using the id `CW`:

```xml
<source id="CW">
  <title>Cree : Words / nehiýawewin : itwēwina</title>
</source>

```

`<t>` and `<trunc>` elements will cite the following source using the id `MD`:


```xml
<source id="MD">
  <title>Maskwacîs Cree Dictionary</title>
</source>
```


## `<e>`: dictionary entry

Represents a single lemma in the dictionary. In laymen's terms, this is
like a word in one particular part of speech e.g., "bank" (Noun). Since
the `<t>` and `<trunc>` elements indicate which dictionary source a particular
translation/definition comes from, a single `<e>` element may contain
content from multiple dictionary sources.

An element may have more than one `<mg>` meaning, each with one or more
`<t>` translations.

### Required children

 - exactly one `<lg>` (lemma group) containing exactly one `<l>` lemma
   and optionally one `<lc>` lemma category.
 - one or more `<mg>` meaning groups.

### Example

Consider the following English utterance: "bank".

It can be interpreted as a **noun**:

```
<e>
  <lg>
    <l pos="N">bank</l>
    <lc>Noun/regular-unvoiced</lc>
    <stem>bank</stem>
  </lg>
  <!-- continued in next example -->
```

This noun can have multiple **meanings**:

```xml
  <mg>
    <tg xml:lang="eng">
      <t sources="OED">the land alongside or sloping down to a river or lake</t>
    </tg>
  </mg>

  <mg>
    <tg xml:lang="eng">
      <t sources="OED">A financial establishment that uses money deposited customers for investment [...] </t>
    </tg>
  </mg>
</e>
```

> *Source*: [Oxford Living English Dictionary](https://en.oxforddictionaries.com/definition/bank#h47327854587960)

A different `<e>` interprets "bank" as a **verb**:

```xml
<e>
  <lg>
    <l pos="N">bank</l>
    <lc>Verb/regular</lc>
    <stem>bank</stem>
  </lg>
  <!-- continued in next example -->
```

This verb can have multiple different meanings as well.

```xml
  <mg>
    <tg xml:lang="eng">
      <t sources="OED">Heap a substance into a mass or mound</t>
    </tg>
  </mg>
  <mg>
    <tg xml:lang="eng">
      <!-- <re> is a restriction on the context of the definition -->
      <re>with reference to an aircraft or vehicle</re>
      <t sources="OED">tilt or cause to tilt sideways in making a turn</t>
    </tg>
  </mg>
</e>
```

> *Source*: [Oxford Living English Dictionary](https://en.oxforddictionaries.com/definition/bank#h47327854587960)

The reason that there would be *two* different lemmas (`<e>` elements)
of "bank" is because, being from different parts-of-speech, they
*inflect* differently.

For example, the first `<e>`, with `<l pos="N">bank</l>` would inflect
as:

|           | Singular | Plural |
|-----------|----------|--------|
| Plain     | bank     | banks  |
| Posessive | bank's   | banks' |

Where as the second lemma `<l pos="V">bank</l>` inflect as:

|     | Present | Past   | Present progressive | Future    |
|-----|---------|--------|---------------------|-----------|
| 1Sg | bank    | banked | am banking          | will bank |
| 2Sg | bank    | banked | are banking         | will bank |
| 3Sg | banks   | banked | is banking          | will bank |
| 1Pl | bank    | banked | are banking         | will bank |
| 2Pl | bank    | banked | are banking         | will bank |
| 3Pl | bank    | banked | are banking         | will bank |

If it has a different inflectional paradigm, that means it's a different
lemma!


## `<lg>`: lemma group

A **lemma group** describes a [lemma][]. A lemma group has two required
children, and one optional child.

### Required children

 - exactly one `<l>` lemma element with a required `pos=""` attribute
 - (Plains Cree to English direction only) exactly one `<lc>` lemma
   category element.

### Optional children

 - one optional `<stem>` element

### Example

This describes "acâhkos", which is an animate noun:

```xml
<lg>
  <l pos="N">acâhkos</l>
  <lc>NA-1</lc>
  <stem>acâhkos-</stem>
</lg>
```


## `<l>`: lemma

The text of this entry is the canonical [word form][] of the dictionary
entry. Look-ups in the dictionary will match for this [word form][]
exactly. In addition to the text of the entry, the `<l>` lemma element
has one required attribute: `pos=""`, or the **part-of-speech**. The
part-of-speech is typically "V" or "N". Certain searches will match
on the value of `pos=""` exactly.


## `<lc>`: lemma category

The **lemma category** determines which layout will be be used when
rendering the paradigm.

> See also: [the lemma categories for Plains Cree](./crk-lemma-categories.md)


## `<stem>`: linguistic stem

The stem is used in the FST to transduce into inflected word forms.
Note that the stem **MAY NOT** be a valid [word form][] by itself.


## `<mg>`: meaning group

A **meaning group** contains one or more different possible meanings of
the lemma. In the English to Plains Cree direction, this is
a translation of the English word to Cree. An entry would use more than
one meaning groups when the meanings are not obviously related.

## Required children

 - one or more `<tg>` translation groups.


### Example

There are two separate meanings of this entry. One is "s/he shakes s.t.", as
listed in the `MD` dictionary source. The other meaning is "s/he rubs s.t.",
as listed in the `CW` dictionary source.

```xml
<mg>
  <tg xml:lang="eng">
    <t pos="V" sources="MD">s/he shakes s.t.</t>
  </tg>
</mg>
<mg>
  <tg xml:lang="eng">
    <t pos="V" sources="CW">s/he rubs s.t.</t>
  </tg>
</mg>
```

## `<tg>`: translation group

A **translation group** lists all the different translations of
a particular meaning of a lemma.

### Required children

 - one or more `<t>` translations
 - (English to Plains Cree direction only) one or more `<trunc>`
   truncated gloss.

### Required attributes

 - `xml:lang=""` attribute. This must be a three-letter ISO 639-3
   language code. Neahttadigisánit supports multiple translation
   languages, and thus these codes serve to differentiate what language
   the translation is written in. Currently itwêwina only supports `crk`
   and `eng`. Thus, every `<tg>` in the `crkeng.xml` dictionary will have
   its `xml:lang="eng"`, as that is the only language it translates
   into; likewise, every `<tg>` in the `engcrk.xml` dictionary will have
   its `xml:lang="crk"`.

### Example

In the Plains Cree to English direction, there is one meaning, but the
`MD` source translates it as "an arrow", while the `CW` source
translates it as "arrow, little arrow".

```xml
<mg>
  <tg xml:lang="eng">
    <t pos="N" sources="MD">an arrow</t>
  </tg>
  <tg>
    <t pos="N" sources="CW">arrow, little arrow</t>
  </tg>
</mg>
```

In the English to Plains Cree direction, there is one meaning, but they
have similar but distinct glosses in the various sources:

```xml
<mg>
  <tg xml:lang="crk">
    <trunc sources="MD">pow-wow dancing.</trunc>
    <trunc sources="CW">the Grass Dance, pow-wow</trunc>
    <t rank="1.0" pos="N">pwâtisimowin</t>
  </tg>
</mg>
```


## `<t>`: translation

A translation, as quoted from one or more of the `<source>` dictionary
sources. The translation text is the plain text translation of the
lemma, for *one* given meaning. The translation **MUST** indicate the
part-of-speech in the target language; in the Plains Cree to English
direction, it **MUST** also cite which dictionary source(s) the
plain-text translation is quoted from.

### Required attributes

 - `pos=""` the part-of-speech in the target language
 - (Plains Cree to English direction only) `source=""` a space-separated list containing `<source>` IDs. This
   means that this particular translation came from the source(s)
   indicated. If at least one `<source>` element exists in `<r>`, each
   `<t>` **MUST** list at least one source ID. If no `<source>` element
   exists in `<r>`, the `sources=""` attribute **MAY** be absent.

### Optional attributes

 - `rank=''` a floating point number that conveys the absolute rank of
   the translation. A smaller value means the translation should be
   presented first in a list of ranked results.

### Example

The translation is "star" and it cites two different dictionary sources:

```xml
<t pos="N" sources="MD CW">star</t>
```


## `<trunc>`: truncated gloss

A truncated gloss, is an abbreviated translation, to describe the
sibling `<t>` translation. This element is used **exclusively** in the
English to Plains Cree direction (i.e., `engcrk.xml`). The `<trunc>`
element **MUST** provide an non-empty `source=""` attribute.

### Required attributes

 - `source=""` a space-separated list containing `<source>` IDs. This is
   identical in semantics to `source=""` attribute of `<t>` elements.

### Example

The English word "grandma" is `<t>` translated as "nôhkom" by both
dictionary sources. Besides the `<t>` element, there must be a `<trunc>`
element to list the truncated translation from the dictionary source(s).

```xml
<tg>
  <t pos="N">nôhkom</t>
  <trunc sources="CW">my grandmother</trunc>
  <trunc sources="MD">grandma</trunc>
</tg>
```


## Complete Plains Cree to English dictionary example

Here is a full lexicon with two sources, and three dictionary entries.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<r>
   <!-- The dictionary sources -->
   <source id="CW">
      <title>Cree : Words / nehiýawewin : itwēwina</title>
   </source>
   <source id="MD">
      <title>Maskwacîs Cree Dictionary</title>
   </source>
PP
   <!-- The dictionary entries -->
   <e>
      <lg>
         <l pos="N">acâhkos</l>
         <lc>NA-1</lc>
         <stem>acâhkos-</stem>
      </lg>
      <mg>
          <tg xml:lang="eng">
              <t pos="N" sources="MD CW">star</t>
          </tg>
      </mg>
   </e>

   <e>
      <lg>
         <l pos="N">acosis</l>
         <lc>NA-1</lc>
         <stem>acosis-</stem>
      </lg>
      <mg>
          <tg xml:lang="eng">
              <t pos="N" sources="MD">an arrow</t>
          </tg>
          <tg xml:lang="eng">
              <t pos="N" sources="CW">arrow, little arrow</t>
          </tg>
      </mg>
   </e>

   <e>
      <lg>
         <l pos="V">mimikopitam</l>
         <lc>VTI-1</lc>
         <stem>mimikopit-</stem>
      </lg>
      <mg>
          <tg xml:lang="eng">
              <t pos="V" sources="MD">He shakes it.</t>
          </tg>
      </mg>
      <mg>
          <tg xml:lang="eng">
              <t pos="V" sources="CW">s/he rubs s.t.</t>
          </tg>
      </mg>
   </e>
</r>
```


## Complete English to Plains Cree dictionary example

Here is a full lexicon with two sources, and four entries.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<r>
  <!-- The dictionary sources -->
  <source id="CW">
    <title>Cree : Words / nēhiyawēwin : itwēwina</title>
  </source>
  <source id="MD">
    <title>Maskwacîs Cree Dictionary</title>
  </source>

  <!-- The dictionary sources -->
  <e>
    <lg xml:lang="eng">
      <l pos="N">pow-wow</l>
    </lg>
    <mg>
      <tg xml:lang="crk">
        <!-- Entry in both, and broad gloss. -->
        <trunc sources="MD">pow-wow dancing.</trunc>
        <trunc sources="CW">the Grass Dance, pow-wow</trunc>
        <t rank="1.0" pos="N">pwâtisimowin</t>
      </tg>
    </mg>
  </e>

  <e>
    <lg xml:lang="eng">
      <l pos="N">Dipper</l>
    </lg>
    <mg>
      <tg xml:lang="crk">
        <!-- Entry in both, exactly the same transcription -->
        <trunc sources="MD CW">the Big Dipper, the Great Bear [constellation]</trunc>
        <t rank="1.0" pos="N">ocêkatâhk</t>
      </tg>
    </mg>
  </e>

  <e>
    <lg xml:lang="eng">
      <l pos="N">hive</l>
    </lg>
    <mg>
      <tg xml:lang="crk">
        <!-- Entry only in Maskwacîs Dictionary -->
        <trunc sources="MD">a bee's nest, [Bee hive].</trunc>
        <t rank="1.0" pos="N">amowaciston</t>
      </tg>
    </mg>
  </e>

  <e>
    <lg xml:lang="eng">
      <l pos="V">hobble</l>
    </lg>
    <mg>
      <tg xml:lang="crk">
        <!-- Entry only in Cree : Words -->
        <trunc sources="CW">hobble s.o. [e.g. a horse]</trunc>
        <t rank="1.0" pos="V">napwahpitêw</t>
      </tg>
    </mg>
  </e>
</r>
```

[lemma]: ./glossary.md#lemma
[word form]: ./glossary.md#word-form
[original-docs]: http://giellatekno.uit.no/doc/dicts/dictionarywork.html
[gt_dictionary.dtd]: https://victorio.uit.no/langtech/trunk/words/dicts/scripts/gt_dictionary.dtd
