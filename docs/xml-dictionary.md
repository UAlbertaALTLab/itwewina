The XML Dictionary format
-------------------------

The dictionaries are stored in an *ad hoc* dictionary format. There
appears to be many different variants of the format originally designed
in Giellatekno for Northern Saami.

The original documentation for this format is [here][original-docs], but
it's in Norwegian. There's also a tiny bit of documentation inline in
[the DTD file][gt_dictionary.dtd], but, as it claims:

> This document is not quite finished yet...

This is a description of the XML format, as it is used in itwêwina.
A single dictionary XML file is a collection of **dictionary entries**
(the _lexicon_) that have translations that are cited from one or more
**dictionary sources**.

The original XML dictionary format appears to support more use cases,
but we have opted to focus on a few key use cases pertinent to Plains
Cree.


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

```xml
<source id="CW">
  <title>Cree : Words / nehiýawewin : itwēwina</title>
</source>
```

`<t>` elements will cite this source using the id: `CW`.

```xml
<source id="MD">
  <title>Maskwacîs Dictionary</title>
</source>
```

`<t>` elements will cite this source using the id: `MD`.


## `<e>`: dictionary entry

Represents a single "word" in the dictionary. In _itwêwina_, each
[lemma][] is assumed to have exactly one `<e>` entry and each `<e>`
describes exactly one [lemma][].

An element may have more than one `<mg>` meaning, each with one or more
`<t>` translations.

### Required children

 - exactly one `<lg>` (lemma group) containing exactly one `<l>` lemma
   and `<lc>` lemma category.
 - one or more `<mg>` meaning groups.

## `<lg>`: lemma group

A **lemma group** describes a [lemma][]. A lemma group has two required
children, and one optional child.

### Required children

 - exactly one `<l>` lemma element with a required `pos=""` attribute
 - exactly one `<lc>` lemma comment element

### Optional children

 - one optional `<stem>` element

### Example

This describes "acâhkos", which is a noun.

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
part-of-speech is typically "V" or "N", and certain searches will match
on this value.


## `<lc>`: lemma category

The **lemma category** determines which layout will be be used when
rendering the paradigm.

In Plains Cree, the format of the **lemma category** is as follows:

### Nouns

`ND?(A|I)-(1|2|3|4|4w|5|[?]|x)`

**N**oun, **A**nimate or **I**nanimate, optionally dependent, followed
by its noun class.

### Verbs

`V{class}-(n|v|1|2|3|4|5)`

**V**erb, followed by its transitivity, and the animacy of its
dependents. Note, that abbreviations are historical Algonquian
linguistics terminology, and Plains Cree verbs can be viewed as
categorized by the quantity (0, 1, or 2) of its animate dependents (its
*valency*). After the hyphen, the verb class follows.

 - VII — verb inanimate    intransitive (0 animate dependents)
 - VAI – verb intransitive animate      (1 animate dependent)
 - VTI - verb transitive   inanimate    (1 animate dependent)
 - VTA — verb transitive   animate      (2 animate dependents)


### Other

`IPC` — any word that does not inflect.

## `<stem>`: linguistic stem

The stem is used in the FST to transduce into inflected word forms.
Note that the stem **MAY NOT** be a valid [word form][] by itself.


## `<mg>`: meaning group

A **meaning group** contains one or more different possible meanings of
the lemma.

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

### Optional attributes

 - `xml:lang=""` attribute. As of 2018-02-04, this attribute is ignored,
   but it signifies what language the translation is written in.

### Example

There is one meaning, but the `MD` source translates it as "an arrow",
while the `CW` source translates it as "arrow, little arrow".

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


## `<t>`: translation

A translation, as quoted from one or more of the `<source>` dictionary
sources. The translation text is the plain text translation of the
lemma, for *one* given meaning. The translation **MUST** indicate the
part-of-speech in the target language; it **MUST** also cite which
dictionary source(s) the plain-text translation is quoted from.

### Required attributes

 - `pos=""` the part-of-speech in the target language
 - `source=""` a space-separated list containing `<source>` IDs. This
   means that this particular translation came from the source(s)
   indicated. If at least one `<source>` element exists in `<r>`, each
   `<t>` **MUST** list at least one source ID. If no `<source>` element
   exists in `<r>`, the `sources=""` attribute **MAY** be absent.

### Example

The translation is "star" and it cited in two different dictionary
sources:

```xml
<t pos="N" sources="MD CW">star</t>
```


## Complete dictionary example

Here is a full lexicon with two sources, and three dictionary entries.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<r>
   <!-- The dictionary sources -->
   <source id="CW">
      <title>Cree : Words / nehiýawewin : itwēwina</title>
   </source>
   <source id="MD">
      <title>Maskwacîs Dictionary</title>
   </source>

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
         <stem>acâhkos-</stem>
      </lg>
      <mg>
          <tg xml:lang="eng">
              <t pos="N" sources="MD">an arrow</t>
          </tg>
          <tg>
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


## Other examples

```xml
<e src="the title of the source dictionary">
    <lg>
        <l pos="N">mitâs</l> <!-- Lemma with its part-of-speech as an attribute -->
        <lc>NDI-1</lc>   <!-- the "lemma comment" --
                              crk uses this to disambiguate forms within parts-of-speech. -->
    </lg>
</e>
```

[lemma]: ./glossary.md#lemma
[original-docs]: http://giellatekno.uit.no/doc/dicts/dictionarywork.html
[gt_dictionary.dtd]: https://victorio.uit.no/langtech/trunk/words/dicts/scripts/gt_dictionary.dtd
