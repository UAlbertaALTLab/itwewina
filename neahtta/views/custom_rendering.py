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


class CustomRenderingOverrides(object):
    """ This object is for registering project- and language-specific
    functions to override various rendering features. """

    def __init__(self):
        self.sort_entry_list_display = {}

    def register_custom_sort(self, *langpairs):
        """ Register a custom sort function. This function will take one
        list object as its arguments, and the structure of that object is
        defined below...

        [search_result_obj, (lex, lemmas, paradigms, paradigm_layout), ...]

        search_result_obj (SearchResult) - search and results that generated this search

        tuple:
        lex (lxml Element) - the lexicon entry, xml node
        lemmas (list of [Lemma,...]) - morphological lookups from the analyzer
        paradigms (list) - generated paradigms, empty list if none
        paradigm_layout (layout or False) - layout file for paradigm, if any

        """

        def wrapper(override_function):
            for pair in langpairs:
                self.sort_entry_list_display[pair] = override_function

        return wrapper

template_rendering_overrides = CustomRenderingOverrides()
