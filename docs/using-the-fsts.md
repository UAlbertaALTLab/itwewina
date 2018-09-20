Using the FSTs
==============

Many FSTs are created when typing `make` within `$GTLANG_crk/src`,
however, the FSTs that matter the most are are
`analyzer-gt-desc.ominvorous.hfst` and `generator-gt-norm.hfst` and
their `*.hfstol` equivalents.


analyzer-gt-desc.ominvorous.hfst
--------------------------------

`analyzer-gt-desc.ominvorous.hfst` is:

  - an **analyzer**: its intended purpose is to analyze Cree text, and produce an analysis
  - **desc**riptive: rather than require people always type in
    perfectly-spelled SRO, the descriptive analyzer tries to account for
    missing accents, missing h's, missing i's, using "bdg" instead of
    "ptk", and other common misspellings.
  - **omnivorous**: it can eat up input in SRO/circumflex, SRO/macron, and syllabics! The lemmas it produces will always be in SRO/circumflex, however.

You can use it with [hfst-lookup]:

```sh
echo "nipihk" | hfst-lookup -q analyzer-gt-desc.omnivorous.hfstol
```

```
nipihk	nipiy+N+I+Loc	0.000000
nipihk	nîpiy+N+I+Loc	0.000000
nipihk	nipiw+V+AI+Cnj+Prs+X	0.000000
nipihk	nîpin+V+II+Cnj+Prs+3Sg	0.000000
nipihk	nipiw+V+AI+Imp+Imm+2Pl	0.000000
```

(The "ol" in `*.hfstol` stands for "optimized lookup". These FSTs are faster to perform lookups. Sometimes.)

What this is telling you is that "nipihk" can be interpreted in five different ways:

 - nipiy + Noun + Inanimate + Locative ("at the water");
 - nîpiy + Noun + Inanimate + Locative ("at the leaf");
 - nipiw + Verb + Animate/Intransitive + Conjunct + Present + Unspecified actor/subject ("SOMEBODY IS DEAD")
 - nîpin + Verb + Inanimate/Intransitive + Conjunct + Present + third person singular actor/subject ("it is summer")
 - nipiw + Verb + Animate/Intransitive + Imperative + Immediate + second person plural actor ("ya'll go ahead and die" -- ask a Cree speaker for a better translation)

The `0.000000` are the [negative log probabilities][neglogprob]. This would matter if we had a weighted FST that would count how probable each interpretation is, but we don't have a weighted FST (requires a training corpus, and the one we have mentions dying a whole lot more than water or leaves!). For now, you can ignore the probabilities, for the exception of a probability of "inf", which means the FST couldn't make heads or tails of the query.

generator-gt-norm.hfst
----------------------

`generator-gt-norm.hfst` is:

 - a **generator**: its intended purpose is to take an analysis (e.g.,
   `nipiy+N+I+Loc`) and convert it into a wordform
 - **norm**ative: its output is in normative orthography -- that is, perfect spelling, with all the accents in the right places.

Using it with [hfst-lookup]:

```sh
echo "nipiy+N+I+Loc" | hfst-lookup -q generator-gt-norm.hfstol
```
```
nipiy+N+I+Loc	nipîhk	0.000000
```

So "nipîhk" is how you spell the inanimate noun "nipiy" in locative case, with 100% probability. Some words will have multiple ways of spelling them:

```sh
echo "atim+N+A+Der/Dim+N+A+Sg" | hfst-lookup -q generator-gt-norm.hfstol
```
```
atim+N+A+Der/Dim+N+A+Sg	acimosis	0.000000
atim+N+A+Der/Dim+N+A+Sg	acimos	0.000000
```

("Der/Dim" is "derived diminutive" when the diminutive of a word can be considered a dictionary entry in-and-of-itself).


[hfst-lookup]: https://github.com/hfst/hfst/wiki/HfstLookUp
[neglogprob]: https://en.wikipedia.org/wiki/Log_probability
