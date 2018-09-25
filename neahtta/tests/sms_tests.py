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


# TODO: spellrelax examples, säämkiõll 

# sääʹmkiõll
# sääʹmkiõll  sääʹmǩiõll+N+Sg+Nom

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
    # ( ('sms', 'fin'), u'mijjieh'),
    # ( ('sms', 'fin'), u'mijjese'),

    # ( ('fin', 'sms'), u'drikke'),


    # # placenames returned
    # ( ('sms', 'fin'), u'Röörovse'),

    # # misc inflections
    # ( ('sms', 'fin'), u'jovkedh'),
    # ( ('sms', 'fin'), u'jovkem'),

]


definition_exists_tests = [
    #  lang    pair    search    definition lemmas
    #                            

    # test hid works: guvlieh is unambiguously høre, govloeh is
    # unambiguously hørest
    # ( ('sms', 'fin'), u'guvlieh', u'høre'),
    # ( ('sms', 'fin'), u'govloeh', u'høres'),
]

# TODO: testcase for null lookup-- is returning 500 but should not be,
# but also need to make sure this fix sticks around.

#   /lookup/sme/nob/?callback=jQuery3094203984029384&lookup=&lemmatize=true

# TODO: use api lookups to determine that rule overrides are formatting
# things correctly

# TODO: for sma
paradigm_generation_tests = [

###  - V + context="upers"
#     ('sms', 'fin', u'mutskedh',
#             "upers not generated",
#             form_contains(set([u'mutskie']))),


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
