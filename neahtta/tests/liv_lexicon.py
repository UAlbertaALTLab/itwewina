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


# um
# vȱlda+V+Ind+Prs+Sg3



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

paradigm_generation_tests = [
    # source, target, lemma, error_msg, paradigm_test

###  - V: 
    ('liv', 'fin', u'vȱlda',
            u" vȱlda  not generating",
            form_doesnt_contain(set([u"um"]))),


]

class ParadigmGenerationTests(ParadigmGenerationTests):
    paradigm_generation_tests = paradigm_generation_tests
