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

from .lexicon import XMLDict, regexpNS
from lxml import etree

_NAMESPACES = {
    're': regexpNS
}

class CustomLookupType(XMLDict):
    """ This is the custom lookup type class from which all custom
    lookup types should be subclassed.

    TODO: document lookup type functions,
        self.lemma
        self.lemmaPOS
        self.lemmaPOSAndType

        self.lookupLemma
        self.lookupLemmaPOS
        self.lookupLemmaPOSAndType

    """

    "Default namespaces, includes `re`, regexp"
    namespaces = _NAMESPACES

    """ This is an xpath string that will be used to match against
    lemmas. The xpath variable `$lemma` is accessible within the string.
    """
    lemma_match_query = './/e[lg/l/text() = $lemma]'

    """ Convenience function for preparing an xpath statement, including namespaces """
    prepare_xpath = lambda self, xp: etree.XPath(xp, namespaces=self.namespaces)

    def __init__(self, *args, **kwargs):
        """ Initialize the trees in the parent class and then provide
        some overrides. """

        super(CustomLookupType, self).__init__(*args, **kwargs)

        self.xpath_evaluator = etree.XPathDocumentEvaluator(self.tree)
        self.lemma = self.prepare_xpath(self.lemma_match_query)

    def cleanEntry(self, e):
        """ This function provides some basic parsing of each `<e />`
        node, returning a dictionary:

            Ex.) {'left': 'kissa', 'pos': 'N', 'right': 'cat'}

        """
        ts = e.findall('mg/tg/t')
        ts_text = [t.text for t in ts]
        ts_pos = [t.get('pos') for t in ts]

        l = e.find('lg/l')
        right_text = [l.text]

        return {'left': ts_text, 'pos': ts_pos, 'right': right_text}

    def lookupLemma(self, lemma):
        """ When the morpholexicon does not analyze anything and only
        passes a lemma to the lexicon, this function will be called to
        resolve entries. """
        return self.XPath( self.lemma
                         , lemma=lemma
                         )


