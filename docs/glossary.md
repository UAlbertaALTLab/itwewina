analyzer
--------

[analyzer]: #analyzer
[analyzers]: #analyzer

An **analyzer** is an [FST] intended primarily to convert
[wordforms] into a [morphological analysis][analysis]. For example,
if you apply the Cree analyzer to the wordform `ê-wâpamit`, it will
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
wordforms however people may type it---we allow for some wiggle-room
and forgive orthographic mistakes, in the hope that the FST will
find the most appropriate analysis.

FST
---

[FST]: #FST

A **finite-state transducer** is a computational formalism that is
useful for defining functions that convert an input string into an
output string. In practice, linguists can use this to convert
a [wordform] into its [lexeme]+[tags] and back again. See main
article: [Finite-state transducer].

generator
---------

[generator]: #generator
[generators]: #generator

A **generator** is an [FST] that converts a
[morphological analysis][analysis] into one or more [wordforms]. For
example, if you apply the Cree generator to the analysis
`miskinâhk+N+A+Distr`, it will output the wordform `miskinâhkonâhk`.

normative
---------

[normative]: #normative

A **normative** [FST] operates on orthographically-correct text.
This means, no spelling errors, accents in all the right places, and
in the exactly correct letter case. In practice, we use **normative
[generators]** that, given an [analysis], output a [wordforms] that
is perfectly written and spelled-out.

<!-- -->

[Finite-state transducer]: ./Finite-state_Transducer.md
