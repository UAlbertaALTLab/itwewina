Giellatekno
===========

> [Eddie] from the future here! These are my personal instructions on how
> to get things setup on a Mac. If you're not on a Mac or these
> instructions don't work for you, don't hesitate to contact me! We'll
> figure it out together, and I'll publish the process on this wiki!

The "official" instructions are on the [Giella(teckno) site](http://giellatekno.uit.no/doc/infra/GettingStartedOnTheMac.html), but they're old and out of date. Also, I don't use Macports, so I'll
tell you how to do things with [Homebrew].

Dependencies
------------

You'll need GNU autotools, as Giellateckno loves autotools:

    brew install autoconf automake libtool

There are many [FST] compilers out there: [xfst], [hfst], and [foma]. The
Cree [FSTs] use features that can only be compiled in hfst, so get that too:

    brew install hfst

You'll need some version of Python 3.5 or greater, to run [the YAML test
cases][YAML tests]. There are [many ways of installing Python 3][install-python3] 😩, so choose what
works best for you!

Antti writes a lot of GNU [awk] code (sometimes incompatible with macOS supplied awk), so you'll probably want that too:

    brew install gawk

I might be forgetting some essential dependencies. If so, please let me know!


Getting the source code and setting up environment variables
------------------------------------------------------------

Checkout the source code somewhere on your computer. "The Norwegians"
like to check it out in the home directory, and assume everybody else
will do the same, but I put it where I want! There are instructions for
only checking out the languages required
(<http://giellatekno.uit.no/doc/infra/infraremake/GettingStartedWithTheNewInfra.html>),
which I'm reproducing here:

```sh
mkdir giella
cd giella
echo "export GTHOME=$(pwd)" >> ~/GTENVVARS  # we'll get to this later
svn co https://gtsvn.uit.no/langtech/trunk/giella-core
svn co https://gtsvn.uit.no/langtech/trunk/giella-shared
cd giella-core
echo "export GTCORE=$(pwd)" >> ~/GTENVVARS
./autogen.sh
./configure
make
cd ../giella-shared
echo "export GTSHARED=$(pwd)" >> ~/GTENVVARS
./autogen.sh
./configure
make
cd ..
mkdir langs
cd langs
svn co https://gtsvn.uit.no/langtech/trunk/langs/crk
echo "export GTLANG_crk=$(pwd)" >> ~/GTENVVARS
```

Giella relies on a few environment variables, which we've dumped in
`~/GTENVVARS`. Add these to [your shell startup script][sh-startup]
(e.g., `~/.bash_profile`, `~/.bashrc`, `~/.zshrc`,  etc.). Either
copy-paste the contents of `~/GTENVVARS` into your shell start-up
script, or source the file like this:

```sh
. ~/GTENVVARS
```

Restart your shell, and try the following commands:

    printenv GTHOME
    printenv GTCORE
    printenv GTLANG_crk

You should see the full paths to the appropriate directories.

Now, you can go into the Cree directory, and setup the appropriate build infrastructure!

```sh
cd $GTLANG_crk/
./autogen.sh
./configure --disable-syntax
```

What's the deal with `--disable-syntax`? If you don't specify
`--disable-syntax`, you'll require some OTHER dependencies that
I haven't listed and have never gotten working on my Mac laptop; it's
only necessary for some dependency grammar stuff that the PhD students
are doing, and is not required for compiling the FSTs. Speaking of...

Compiling the FSTs
------------------

In `$GTLANG_crk/` there should now be a Makefile, so type:

    make

...and after a while the `src/` directory should contain many `*.hfst` and
`*.hfstol` files.

Using the FSTs
==============

The ones you'll care about are `analyzer-gt-desc.ominvorous.hfst` and
`generator-gt-norm.hfst` and their `*.hfstol` equivalents.

`analyzer-gt-desc.ominvorous.hfst` is:

  - an **analyzer**: its intended purpose is to analyze Cree text, and produce an analysis
  - **desc**riptive: rather than require people always type in
    perfectly-spelled SRO, the descriptive analyzer tries to account for
    missing accents, missing h's, missing i's, using "bdg" instead of
    "ptk", and other common misspellings.
  - **omnivorous**: it can eat up input in SRO/circumflex, SRO/macron, and syllabics! The lemmas it produces will always be in SRO/circumflex, however.

You can use it with `hfst-lookup`:

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
 
The 0.000000 are the [negative log probabilities][neglogprob]. This would matter if we had a weighted FST that would count how probable each interpretation is, but we don't have a weighted FST (requires a training corpus, and the one we have mentions dying a whole lot more than water or leaves!). For now, you can ignore the probabilities, for the exception of a probability of "inf", which means the FST couldn't make heads or tails of the query.

`generator-gt-norm.hfst` is:

 - a **generator**: its intended purpose is to take an analysis (e.g.,
   `nipiy+N+I+Loc`) and convert it into a wordform
 - **norm**ative: its output is in normative orthography -- that is, perfect spelling, with all the accents in the right places.

Using it with `hfst-lookup`:

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


[Eddie]: https://github.com/eddieantonio
[FST]: ./FST
[FSTs]: ./FST
[xfst]: ./Glossary#xfst
[hfst]: ./Glossary#hfst
[foma]: ./Glossary#foma
[YAML tests]: ./YAML_tests
[awk]: https://en.wikipedia.org/wiki/AWK
[Homebrew]: https://brew.sh/
[install-python3]: https://realpython.com/installing-python/
[sh-startup]: https://stackoverflow.com/questions/15101559/terminal-where-is-the-shell-start-up-file
[neglogprob]: https://en.wikipedia.org/wiki/Log_probability
