# The source analyser and generator FSTs are done entirely in Standard Roman
# Orthography (Latn).  However, we require Canadian Aboriginal syllabics
# versions of both. This Makefile converts SRO FSTs in the equivillent
# syllabics FSTs.
#
# analyser-gt-desc.Cans-to-Cans.hfstol
# : An analyzer that accepts input in Canadian Aboriginal syllabics
#   and produces a morphological analysis with its lemma also written in syllabics.
#   "Descriptive" means it is able to understand non-standard orthography.
# 
# generator-gt-desc.Cans-to-Cans.hfstol
# : A generator that accepts a morphological analysis in Canadian Aboriginal syllabics,
#   and produces an orthographically correct surface form, also in syllabics.

FSTs = analyser-gt-desc.Cans-to-Cans.hfstol generator-gt-norm.Cans-to-Cans.hfstol

all: $(FSTs)


test: test-analyze test-generate

test-analyze: analyser-gt-desc.Cans-to-Cans.hfstol
	@echo "#" $@
	echo ᐚᐸᒣᐤ | hfst-lookup -q $<

test-generate: generator-gt-norm.Cans-to-Cans.hfstol
	@echo "#" $@
	echo wâpamêw+V+TA+Ind+Prs+3Sg+4Sg/PlO | hfst-lookup -q $<

clean:
	$(RM) $(FSTs) $(FSTs:.hfst=.hfstol) $(INTERMEDIATE_FSTs)

.PHONY: all clean test test-analyze test-generate

INTERMEDIATE_FSTs := generator-gt-norm.Cans-to-Latn.hfst analyser-gt-desc.Cans-to-Latn.hfst


HFSTCOMPOSE.RULE = hfst-compose -F -o $@ -1 $(word 1,$^) -2 $(word 2,$^)

%.Cans-to-Latn.hfst: Cans-to-Latn.compose.hfst %.hfst 
	$(HFSTCOMPOSE.RULE)

%.Cans-to-Cans.hfst: %.Cans-to-Latn.hfst Latn-to-Cans.compose.hfst 
	$(HFSTCOMPOSE.RULE)

%.hfstol: %.hfst
	hfst-fst2fst -O -o $@ -i $<
