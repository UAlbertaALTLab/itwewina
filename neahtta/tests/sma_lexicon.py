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
import neahtta
import unittest
import tempfile

from .lexicon import ( BasicTests
                     , WordLookupTests
                     , WordLookupDetailTests
                     , WordLookupAPITests
                     , WordLookupAPIDefinitionTests
                     , ParadigmGenerationTests
                     , form_contains
                     , form_doesnt_contain
                     )

wordforms_that_shouldnt_fail = [
    ( ('sma', 'nob'), u'mijjieh'),
    ( ('sma', 'nob'), u'mijjese'),

    ( ('nob', 'sma'), u'drikke'),
    ( ('nob', 'sma'), u'forbi'),
    ( ('nob', 'sma'), u'stige'),

    # test that nob->sma placenames work with nynorsk
    ( ('nob', 'sma'), u'Noreg'),
    ( ('nob', 'sma'), u'Norge'),
    ( ('nob', 'sma'), u'skilnad'),

    # placenames returned
    ( ('sma', 'nob'), u'Röörovse'),

    # misc inflections
    ( ('sma', 'nob'), u'jovkedh'),
    ( ('sma', 'nob'), u'jovkem'),


]


definition_exists_tests = [
    #  lang    pair    search    definition lemmas
    #                            

    # test hid works: guvlieh is unambiguously høre, govloeh is
    # unambiguously hørest
    ( ('sma', 'nob'), u'guvlieh', u'høre'),
    ( ('sma', 'nob'), u'govloeh', u'høres'),
]

# TODO: testcase for null lookup-- is returning 500 but should not be,
# but also need to make sure this fix sticks around.

#   /lookup/sme/nob/?callback=jQuery3094203984029384&lookup=&lemmatize=true

# TODO: use api lookups to determine that rule overrides are formatting
# things correctly

# TODO: for sma
paradigm_generation_tests = [
###  - A: 
###     - http://localhost:5000/detail/sme/nob/ruoksat.json
###     - test that context is found as well as paradigm
###     - test that +Use/NGminip forms are not generated


###  - V + context="upers"
    ('sma', 'nob', u'mutskedh',
            "upers not generated",
            form_contains(set([u'mutskie']))),

#     ('sma', 'nob', u'lïgkedh',
#             "Impersonal verbs generate personal forms",
#             form_doesnt_contain(set([u"lïgkem"]))),

###  - V + Homonymy: svijredh
    ('sma', 'nob', u'govledh',
            "hom1 generated wrong",
            form_contains(set([u'(daan biejjien manne) govlem']))),

###  - N Pl: - common noun tanta pluralia - aajkoehkadtjh
    ('sma', 'nob', u'aajkoehkadtjh',
            "Prop pl forms missing",
            form_contains(set([u'aajkoehkadtji', u'aajkoehkadjijste']))),


###  - N Prop: Nöörje
    ('sma', 'nob', u'Nöörje',
            "Prop does not generate",
            form_contains(set([u'Nöörjese', u'Nöörjesne', u'Nöörjeste']))),

###  - N Prop Pl: Bealjehkh
    ('sma', 'nob', u'Bealjehkh',
            "Prop pl forms missing",
            form_contains(set([u'Bealjahkidie', u'Bealjahkinie', u'Bealjahkijstie']))),

###  - N Prop: Nöörje
    ('sma', 'nob', u'Nöörje',
            "Prop forms context missing",
            form_contains(set([u'Nöörjen baaktoe', u'Nöörjese', u'Nöörjesne', u'Nöörjeste']))),

###  - N Prop Pl: Bealjehkh
    ('sma', 'nob', u'Bealjehkh',
            "Prop forms context missing",
            form_contains(set([u'Bealjehki baaktoe', u'Bealjahkidie', u'Bealjahkinie', u'Bealjahkijstie']))),

###  - N Prop + Sem/Org: Stoerredigkie
    ('sma', 'nob', u'Stoerredigkie',
            "Prop forms context missing",
            form_contains(set([u'Stoerredigkien', u'Stoerredægkan', u'Stoerredigkeste']))),

]

class BasicTests(BasicTests):

    wordforms_that_shouldnt_fail = wordforms_that_shouldnt_fail

    def test_single_word(self):
        """ Test that the basic idea of testing will work.
            If there's a problem here, this is a problem. ;)
        """
        lang_pair, form = wordforms_that_shouldnt_fail[0]

        base = '/%s/%s/' % lang_pair
        rv = self.app.post(base, data={
            'lookup': form,
        })

        assert 'mijjieh' in rv.data
        assert u'vi' in rv.data.decode('utf-8')
        self.assertEqual(rv.status_code, 200)


class WordLookupAPIDefinitionTests(WordLookupAPIDefinitionTests):
    definition_exists_tests = definition_exists_tests

class WordLookupDetailTests(WordLookupDetailTests):
    wordforms_that_shouldnt_fail = wordforms_that_shouldnt_fail

class WordLookupAPITests(WordLookupAPITests):
    wordforms_that_shouldnt_fail = wordforms_that_shouldnt_fail

class ParadigmGenerationTests(ParadigmGenerationTests):
    paradigm_generation_tests = paradigm_generation_tests
