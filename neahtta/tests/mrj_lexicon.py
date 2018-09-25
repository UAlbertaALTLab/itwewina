# -*- coding: UTF-8 -*-

# Neahttadigisánit — online, inflectional dictionary
# Copyright (C) 2013–2017 University of Tromsø
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

import os
import unittest
import tempfile

from .lexicon import ( WordLookupDetailTests
                     , WordLookupAPITests
                     , WordLookupAPIDefinitionTests
                     , ParadigmGenerationTests
                     , form_contains
                     , form_doesnt_contain
                     )

# These should not produce a 404.

wordforms_that_shouldnt_fail = [
    ( ('mrj', 'fin'), u'ловка'),
    ( ('mrj', 'fin'), u'ломбы'),
    ( ('mrj', 'fin'), u'ло'),
]


# These forms should have a matching definition, i.e., <väli> must be a
# possible definition of <ло>

# With these tests, there is not as big of a need to be extensive, as
# much as making sure that there are tests for a larger variety of types
# of words, to make sure that the FST lines up with the lexicon.

# NB: make sure word strings are unicode, marked with u.

definition_exists_tests = [
    #  lang    pair    search    definition lemmas
    #                            
    ( ('mrj', 'fin'), u'ло', u'väli'),
    ( ('mrj', 'fin'), u'ло', u'kalastaa'),

    ( ('mrj', 'fin'), u'ловка',  u'näppäryys'),
    ( ('mrj', 'fin'), u'ломбы',  u'tuomi'),

]

paradigm_generation_tests = [
    # source, target, lemma, error_msg, paradigm_test

###  - V: 
    ('mrj', 'fin', u'лӓктӓш',
            "mrj verbs not generating",
            form_contains(set([u"лӓктӓм", u"лӓктеш"]))),

###  - N + context="bivttas":  heittot
###     - http://localhost:5000/detail/sme/nob/heittot.html

    ('mrj', 'fin', u'книгӓ',
            "mrj nouns not generating",
            form_contains(set([u"книгӓн", u"книгӓге"]))),

]

class WordLookupAPIDefinitionTests(WordLookupAPIDefinitionTests):
	definition_exists_tests = definition_exists_tests

class WordLookupDetailTests(WordLookupDetailTests):
	wordforms_that_shouldnt_fail = wordforms_that_shouldnt_fail

class WordLookupAPITests(WordLookupAPITests):
	wordforms_that_shouldnt_fail = wordforms_that_shouldnt_fail

class ParadigmGenerationTests(ParadigmGenerationTests):
    paradigm_generation_tests = paradigm_generation_tests

