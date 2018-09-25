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

def remove_blank(generated_result, *generation_input_args, **kwargs):
    """ **Remove empty analyses**

    This is a language specific filter, more or less to aid in discovery
    of analyser errors with new language sets.
    """
    def _strip((lemma, tag_list, analyses)):
        if not analyses:
            return False
        return True

    return filter(_strip, generated_result)

def match_homonymy_entries(entries_and_tags):
    """ **Post morpho-lexicon override**

    This is performed after lookup has occurred, in order to filter out
    entries and analyses, when these depend on eachother.

    Here: we only want to return entries where the analysis homonymy tag
    matches the entry homonymy attribute. If entries do not have a
    homonymy attribute, then always return the entry.
    """

    filtered_results = []

    for entry, analyses in entries_and_tags:
        if entry is not None:
            entry_hid = entry.find('lg/l').attrib.get('hid', False)
            if entry_hid:
                # Sometimes tags don't have hid, but entry does. Thus:
                tag_hids = [x for x in [a.tag['homonyms'] for a in analyses]
                            if x is not None]
                if len(tag_hids) > 0:
                    # if they do, we do this
                    if entry_hid in tag_hids:
                        filtered_results.append((entry, analyses))
                else:
                    filtered_results.append((entry, analyses))
            else:
                filtered_results.append((entry, analyses))
        else:
            filtered_results.append((entry, analyses))

    return filtered_results
