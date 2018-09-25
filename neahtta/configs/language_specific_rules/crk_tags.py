# -*- coding: UTF-8 -*-

# Neahttadigisánit — online, inflectional dictionary
# Copyright (C) 2013–2017 University of Tromsø
# Copyright (C) 2018 University of Alberta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

pre_lemma_tags = [
    'RdplW',
    'RdplS',
]

# TODO: replace PV/ with user-defined regex or something
def process_crk_analysis(analysis_line):
    r""" Take an analysis line, and return a tuple of the lemma,
    followed by a reformatted tag where tags before the lemma are
    combined with tags after the lemma. Strings without any preverb
    material are not changed.

        >>> process_crk_analysis("wordform\tPV/asdf+PV/bbq+lemma+POS+Type+Sg1")
        ('wordform', 'lemma+PV/asdf+PV/bbq+POS+Type+Sg1')
        >>> process_crk_analysis("wordform\tlemma+POS+Type+Sg1")
        ('wordform', 'lemma+POS+Type+Sg1')
        >>> process_crk_analysis("wordform\tPV/asdf+PV/bbq+lemma")
        ('wordform', 'lemma+PV/asdf+PV/bbq')
        >>> process_crk_analysis("ninahnipan\tRdplS+nipâw+V+AI+Ind+Prs+1Sg")
        ('ninahnipan', 'nipâw+RdplS+V+AI+Ind+Prs+1Sg')
        >>> process_crk_analysis("ninanahnipan\tRdplW+RdplS+nipâw+V+AI+Ind+Prs+1Sg")
        ('ninanahnipan', 'nipâw+RdplW+RdplS+V+AI+Ind+Prs+1Sg')

    NB: For the purposes of redisplaying the stem in NDS, we add
    +Tpl/Lemma in between any preceding tags and following tags.

        >>> process_crk_analysis("ninanahnipan\tRdplW+RdplS+nipâw+V+AI+Ind+Prs+1Sg")
        ('ninanahnipan', 'nipâw+RdplW+RdplS+Tpl/Lemma+V+AI+Ind+Prs+1Sg')

    hfst-lookup produces weights, even for unweighted FSTs. This can partition
    those too.

        >>> process_crk_analysis("wordform\tPV/asdf+PV/bbq+lemma+POS+Type+Sg1\t0.0000")
        ('wordform', 'lemma+PV/asdf+PV/bbq+POS+Type+Sg1')
        >>> process_crk_analysis("wordform\tlemma+POS+Type+Sg1\t0.0000")
        ('wordform', 'lemma+POS+Type+Sg1')
        >>> process_crk_analysis("wordform\tPV/asdf+PV/bbq+lemma\t0.0000")
        ('wordform', 'lemma+PV/asdf+PV/bbq')
        >>> process_crk_analysis("ninahnipan\tRdplS+nipâw+V+AI+Ind+Prs+1Sg\tinf")
        ('ninahnipan', 'nipâw+RdplS+V+AI+Ind+Prs+1Sg')
        >>> process_crk_analysis("ninanahnipan\tRdplW+RdplS+nipâw+V+AI+Ind+Prs+1Sg\t3.1415")
        ('ninanahnipan', 'nipâw+RdplW+RdplS+V+AI+Ind+Prs+1Sg')


    """

    # The output of the lookup tools is two or three tab-separated columns:
    #  column 1: the input
    #  column 2: the raw analysis
    #  column 3: (optional) the weight of this analysis
    # For our purposes, we can chuck out the weight.
    columns = analysis_line.split("\t")
    assert len(columns) in (2, 3)
    wordform, analysis_string = columns[:2]

    lemma = False

    tag_sep = '+'

    parts = analysis_string.split(tag_sep)
    has_preverbs = False

    for p in parts:
        if p.startswith('PV/') or p in pre_lemma_tags:
            has_preverbs = True
        else:
            lemma = p
            break

    preverbs, _, tag = analysis_string.partition(tag_sep + lemma + tag_sep)

    # When there is no `tag` from the partition ...
    if len(tag) == 0:
        # ... because there are preverbs and nothing else
        if has_preverbs:
            # remove the lemma from the tag
            preverbs = preverbs.replace(tag_sep + lemma, '')
        # ... because there are no preverbs
        else:
            _lem, _, tag = analysis_string.partition(lemma + tag_sep)
            preverbs = None

    reformatted_tag_parts = [lemma]

    if preverbs:
        reformatted_tag_parts.append(preverbs)
    if tag:
        reformatted_tag_parts.append('Tpl/Lemma')
        reformatted_tag_parts.append(tag)

    reformatted_tag = tag_sep.join(reformatted_tag_parts)

    return (wordform, reformatted_tag)

def main():
    print '--'
    print process_crk_analysis("PV/asdf+PV/bbq+lemma+POS+Type+Sg1")
    # ('lemma', 'PV/asdf+PV/bbq+POS+Type+Sg1')
    print process_crk_analysis("lemma+POS+Type+Sg1")
    # ('lemma', 'lemma+POS+Type+Sg1')
    print process_crk_analysis("PV/asdf+PV/bbq+lemma")

    print process_crk_analysis("ninahnipan\tRdplS+nipâw+V+AI+Ind+Prs+1Sg")
    # ('ninahnipan', 'nipâw+RdplS+V+AI+Ind+Prs+1Sg')
    print process_crk_analysis("ninanahnipan\tRdplW+RdplS+nipâw+V+AI+Ind+Prs+1Sg")
    # ('ninanahnipan', 'nipâw+RdplW+RdplS+V+AI+Ind+Prs+1Sg')

if __name__ == "__main__":
    import sys
    sys.exit(main())

