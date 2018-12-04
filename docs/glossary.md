analyzer
--------

[analyzer]: #analyzer
[analyzers]: #analyzer

An **analyzer** is an [FST] intended primarily to convert
[word forms] into a [morphological analysis][analysis]. For example,
if you apply the Cree analyzer to the word form `ê-wâpamit`, it will
return the analysis `PV/e+wâpamêw+V+TA+Cnj+Prs+3Sg+1SgO`, meaning
the [lemma] is "wâpamêw", it\'s a **Transitive** **Animate**
**Verb**, in the **Conjunct** form, in the **Present** tense with
a **3rd person singular** [actor] and a **first-person singular**
[object].

descriptive
-----------

[descriptive]: #descriptive

A **descriptive** [FST] operates on orthographically dubious text.
This means that the text may be written in a non-standard
orthography, make some common spelling mistakes, and may be lacking
accents or aspiration marks where they would be required in
"correct" text. Think [descriptive linguistics](https://en.wikipedia.org/wiki/Linguistic_description).
In practice, we use **descriptive [analyzers]** to accept input and
[word forms][] however people may type it---we allow for some wiggle-room
and forgive orthographic mistakes, in the hope that the FST will
find the most appropriate analysis.

FST
---

[FST]: #FST

A **finite-state transducer** is a computational formalism that is
useful for defining functions that convert an input string into an
output string. In practice, linguists can use this to convert
a [word form] into its [lexeme]+[tags] and back again. See main
article: [Finite-state transducer].

generator
---------

[generator]: #generator
[generators]: #generator

A **generator** is an [FST] that converts a
[morphological analysis][analysis] into one or more [word forms]. For
example, if you apply the Cree generator to the analysis
`miskinâhk+N+A+Distr`, it will output the word form `miskinâhkonâhk`.

lemma
--------

[lemma]: #lemma

A **lemma** is the "dictionary form" of a word. The lemma is usually
a possible word form of the word. In the case of Cree non-dependent
nouns, the lemma is the singular form of the noun. In the case of
dependent nouns, the lemma is the singular first-person possessor form.
In the case of VII/VAI/VTI verbs, it's the independent, present tense,
third person form of the verb. In the case of VTA verbs, it's the
independent, present tense, third person actor/obviative goal form of
the verb.

A lemma can be considered the "canonical" form of the word. This is the
form of the word produced by the FST, and written as the key in the
dictionary XML file.

normative
---------

[normative]: #normative

A **normative** [FST] operates on orthographically-correct text.
This means, no spelling errors, accents in all the right places, and
in the exactly correct letter case. In practice, we use **normative
[generators]** that, given an [analysis], output a [word forms] that
is perfectly written and spelled-out.

word form
---------

[word form]: #word-form
[word forms]: #word-form

A **word form** (also spelled **wordform**) is a specific grammatical
realization of a word. For example, the [lemma][] *eat* has several
different word forms including *eat*, *ate*, *eaten*, and *eats*.
Likewise, the Cree word *wâpamêw* has many possible word forms, including
*kiwâpamin*, *kiwâpamatin*, and *wâpmaêw*, among many others.

<!-- -->

[Finite-state transducer]: ./finite-state-transducer.md
