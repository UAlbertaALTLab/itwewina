﻿from lxml import etree
from lookups import SearchTypes

""" Our project-wide search_types repository. """
search_types = SearchTypes({})

##
##  Lexicon
##
##

import sys

DEFAULT_XPATHS = {
    'pos': 'lg/l/@pos',
}

def hash_node(node):
    return unicode(hash(etree.tostring(node)))

class LexiconOverrides(object):
    """ Class for collecting functions marked with decorators that
    provide special handling of tags. One class instantiated in
    morphology module: `generation_overrides`.

    Current practice is to store these in language-specific modules within
    :py:module:`configs.language_specific_rules`...
    """

    ##
    ### Here are the functions that apply all the rules
    ##

    def format_source(self, lang_iso, ui_lang, e, target_lang, default_str):
        """ Find the function decorated by
                @overrides.entry_source_formatter(iso)
            and run the function on an XML node.
        """
        if lang_iso in self.source_formatters:
            return self.source_formatters.get(lang_iso)(ui_lang, e, target_lang) \
                or default_str
        return default_str

    def format_target(self, src_iso, targ_iso, ui_lang, e, tg, default_str):
        """ Find the function decorated by
                @overrides.entry_source_formatter(iso)
            and run the function on an XML node.
        """
        if (src_iso, targ_iso) in self.target_formatters:
            return self.target_formatters.get((src_iso, targ_iso))(ui_lang, e, tg) \
                or default_str
        return default_str

    def process_prelookups(self, lexicon_language_pairs, function):
        """ This runs the generator function, and applies all of the
        function contexts to the output. Or in other words, this
        decorator works on the output of the decorated function, but
        also captures the input arguments, making them available to each
        function in the registry.
        """
        def decorate(*args, **kwargs):
            lang_pair = lexicon_language_pairs.get(args)
            _from = args[0]
            newargs = args
            newkwargs = kwargs
            for f in self.prelookup_processors[_from]:
                newargs, newkwargs = f(*newargs, **newkwargs)
            return function(*newargs, **newkwargs)
        return decorate

    def process_postlookups(self, lexicon_language_pairs, function):
        """ Lexicon lookups are passed through all of these functions
        """
        def decorate(*lang_pair_args, **kwargs):
            lang_pair = lexicon_language_pairs.get(lang_pair_args)
            result_nodes = function(*lang_pair_args, **kwargs)
            for f in self.postlookup_filters[lang_pair_args]:
                result_nodes = f(lang_pair, result_nodes, kwargs)
            return result_nodes
        return decorate

    ##
    ### Here are the decorators
    ##

    def entry_source_formatter(self, *language_isos):
        """ Register a function for a language ISO.

        Functions decorated by this registry decorator should take one
        argument, an entry node, and return either a string or None. If
        None is returned, then a default value will be returned instead.

        The default value is passed to the function format_source, which
        selects the registered function and executes it.

        """
        def wrapper(formatter_function):
            for language_iso in language_isos:
                if language_iso in self.source_formatters:
                    print ' * OBS! Source formatter already registered for %s.' % \
                        language_iso
                    print '   ignoring redefinition on <%s>.' % \
                        restrictor_function.__name__
                else:
                    self.source_formatters[language_iso] = formatter_function
                    print '%s formatter: entry formatter for source - %s' %\
                          ( language_iso
                          , formatter_function.__name__
                          )
        return wrapper

    def entry_target_formatter(self, *iso_pairs):
        """ Register a function for a language ISO
        """
        def wrapper(formatter_function):
            for (src_iso, targ_iso) in iso_pairs:
                if (src_iso, targ_iso) in self.target_formatters:
                    print ' * OBS! Target formatter already registered for %s.' % \
                        repr((src_iso, targ_iso))
                    print '   ignoring redefinition on <%s>.' % \
                        formatter_function.__name__
                else:
                    self.target_formatters[(src_iso, targ_iso)] = formatter_function
                    print '%s formatter: entry formatter for target - %s' %\
                          ( '%s - %s' % (src_iso, targ_iso)
                          , formatter_function.__name__
                          )
        return wrapper

    def pre_lookup_tag_rewrite_for_iso(self, *language_isos):
        """ Register a function for a language ISO to adjust tags used in
        FSTs for use in lexicon lookups.

        >>> @lexicon_overrides.pre_lookup_tag_rewrite_for_iso('sme')
        >>> def someFunction(*args, **kwargs):
        >>>     ... some processing on tags, may be conditional, etc.
        >>>     return args, kwargs

        A typical example usage would be:

        >>> @lexicon.pre_lookup_tag_rewrite_for_iso('sme')
        >>> def pos_to_fst(*args, **kwargs):
        >>>     if 'lemma' in kwargs and 'pos' in kwargs:
        >>>         _k = kwargs['pos'].replace('.', '').replace('+', '')
        >>>         new_pos = LEX_TO_FST.get(_k, False)
        >>>         if new_pos:
        >>>             kwargs['pos'] = new_pos
        >>>     return args, kwargs

        Thus replacing the FST output containing 'egen' as a POS to
        'Prop' so that it may be found in a lexical entry containing
        a 'Prop' attribute.
        """
        def wrapper(restrictor_function):
            for language_iso in language_isos:
                self.prelookup_processors[language_iso]\
                    .append(restrictor_function)
                print '%s overrides: lexicon pre-lookup arg rewriter - %s' %\
                      ( language_iso
                      , restrictor_function.__name__
                      )
        return wrapper

    def postlookup_filters_for_lexicon(self, *lexica):
        """ Register a function for a language ISO to adjust tags used
        in FSTs for use in lexicon lookups. The decorator function takes
        a tuple for every function that the decorator should be applied
        to

        >>> @lexicon_overrides.lookup_filters_for_lexicon(('sme', 'nob'))
        >>> def someFunction(nodelist):
        >>>     ... some processing on tags, may be conditional, etc.
        >>>     return nodelist

        """
        def wrapper(restrictor_function):
            for lexicon in lexica:
                self.postlookup_filters[lexicon]\
                    .append(restrictor_function)
                print '%s overrides: lexicon lookup filter - %s' %\
                      ( lexicon
                      , restrictor_function.__name__
                      )
        return wrapper

    def external_search(self, *lexica):
        """ Register a function for a language ISO to adjust tags used
        in FSTs for use in lexicon lookups. The decorator function takes
        a tuple for every function that the decorator should be applied
        to

        >>> @lexicon_overrides.lookup_filters_for_lexicon(('sme', 'nob'))
        >>> def someFunction(nodelist):
        >>>     ... some processing on tags, may be conditional, etc.
        >>>     return nodelist

        """
        def wrapper(search_function):
            for shortcut_name, source, target in lexica:
                self.external_search_redirect[(shortcut_name, source, target)] = \
                    search_function
                print '%s->%s overrides: lexicon lookup filter - %s' %\
                      ( source, target
                      , shortcut_name
                      )

        return wrapper

    def __init__(self):
        from collections import defaultdict

        self.prelookup_processors = defaultdict(list)
        self.target_formatters = defaultdict(bool)
        self.source_formatters = defaultdict(bool)
        self.postlookup_filters = defaultdict(list)

        self.external_search_redirect = defaultdict(bool)

lexicon_overrides = LexiconOverrides()

PARSED_TREES = {}

regexpNS = "http://exslt.org/regular-expressions"

# @search_types.add_custom_lookup_type('regular')
class XMLDict(object):
    """ XML dictionary class. Initiate with a file path or an already parsed
    tree, exposes methods for searching in XML.

    Entries should be formatted by creating an EntryNodeIterator object,
    which will clean them on iteration.

    """

    PARSED_TREES = PARSED_TREES


    def __init__(self, filename=False, tree=False, options={}):

        xpaths = DEFAULT_XPATHS.copy()
        xpaths.update(**options)

        if not tree:
            if filename not in PARSED_TREES:
                print "parsing %s" % filename
                try:
                    self.tree = etree.parse(filename)
                    PARSED_TREES[filename] = self.tree
                except Exception, e:
                    print
                    print " *** ** ** ** ** ** * ***"
                    print " *** ERROR parsing %s" % filename
                    print " *** ** ** ** ** ** * ***"
                    print
                    print " Check the compilation process... "
                    print " Is the file empty?"
                    print " Saxon errors?"
                    print
                    sys.exit(2)
            else:
                self.tree = PARSED_TREES[filename]
        else:
            self.tree = tree
        self.xpath_evaluator = etree.XPathDocumentEvaluator(self.tree)

        # Initialize XPath queries

        _re_pos_match = """re:match(%(pos)s, $pos, "i")""" % xpaths

        self.lemmaStartsWith = etree.XPath(
            ".//e[starts-with(%(pos)s, $lemma)]" % xpaths
        )

        self.lemma = etree.XPath('.//e[lg/l/text() = $lemma]')

        self.lemmaPOS = etree.XPath(
            './/e[lg/l/text() = $lemma and ' + _re_pos_match + ']',
            namespaces={'re': regexpNS})

        self.lemmaPOSAndType = etree.XPath(
            ' and '.join([ './/e[lg/l/text() = $lemma'
                         , _re_pos_match
                         , 'lg/l/@type = $_type]'
                         ])
            , namespaces={'re': regexpNS}
        )

    def XPath(self, xpathobj, *args, **kwargs):
        return xpathobj(self.tree, *args, **kwargs)

    def lookupLemmaStartsWith(self, lemma):
        return self.XPath( self.lemmaStartsWith
                         , lemma=lemma
                         )

    def lookupLemma(self, lemma):
        return self.XPath( self.lemma
                         , lemma=lemma
                         )

    def lookupLemmaPOS(self, lemma, pos):
        # Can't insert variables in EXSLT expressions within a compiled
        # xpath statement, so doing this.
        pos = "^%s$" % pos
        return self.XPath( self.lemmaPOS
                         , lemma=lemma
                         , pos=pos
                         )

    def lookupLemmaPOSAndType(self, lemma, pos, _type):
        pos = "^%s$" % pos
        return self.XPath( self.lemmaPOSAndType
                         , lemma=lemma
                         , pos=pos
                         , _type=_type
                         )

    def iterate_entries(self, start=0, end=20, words=False):

        if words:
            _xp = etree.XPath(".//e/lg/l/text()")
            ws = _xp(self.tree)

            if end:
                ws = ws[start:end]

            return ws
        else:
            if end:
                _xp = etree.XPath(".//e[position() >= %s and position() < %s]" % (start, end))
            else:
                _xp = etree.XPath(".//e")

        return _xp(self.tree)

    def iterate_letter_pages(self, page_size=20):
        # 1.) make list of tuples containing the first letter and the
        # iteration number, and then the page count

        # 2.) filter out only instances where the first letter is
        # different from the second

        _xp = etree.XPath(".//e/lg/l/text()")
        ws = _xp(self.tree)

        counts = []
        page = 0
        iteration = 0
        last_letter = ws[0][0]

        for i, w in enumerate(ws):
            current_letter = w[0].lower()
            if i % page_size == 0 and i > 0:
                page += 1
            if last_letter != current_letter:
                counts.append(
                    (current_letter, page)
                )
            last_letter = current_letter

        return counts

    def iterate_entries_count(self):
        _xp = etree.XPath(".//e")
        es = len(_xp(self.tree))

        return len(es)

    def lookupOtherLemmaAttr(self, **attrs):
        attr_conditions = []
        for k, v in attrs.iteritems():
            attr_conditions.append("lg/l/@%s = '%s'" % (k, v))
        attr_conditions = ' and '.join(attr_conditions)

        _xpath_expr = ".//e[%s]" % attr_conditions
        _xp = etree.XPath(_xpath_expr , namespaces={'re': regexpNS})
        return _xp(self.tree)


class AutocompleteFilters(object):

    def autocomplete_filter_for_lang(self, language_iso):
        def wrapper(filter_function):
            self._filters[language_iso].append(filter_function)
            print '%s filter: autocomplete entry filter for language - %s' % \
                  ( language_iso
                  , filter_function.__name__
                  )
        return wrapper

    def __init__(self, *args, **kwargs):
        from collections import defaultdict
        self._filters = defaultdict(list)

autocomplete_filters = AutocompleteFilters()

class AutocompleteTrie(XMLDict):

    @property
    def allLemmas(self):
        """ Returns iterator for all lemmas.
        """
        entries = self.tree.findall('e/lg/l')
        filters = autocomplete_filters._filters.get(self.language_pair, [])
        if len(filters) > 0:
            for f in filters:
                entries = f(entries)
        lemma_strings = (e.text for e in entries if e.text)
        return lemma_strings

    def autocomplete(self, query):
        if self.trie:
            if hasattr(self.trie, 'autocomplete'):
                return sorted(list(self.trie.autocomplete(query)))
        return []

    def __init__(self, *args, **kwargs):
        if 'language_pair' in kwargs:
            self.language_pair = kwargs.pop('language_pair')

        super(AutocompleteTrie, self).__init__(*args, **kwargs)

        from trie import Trie

        print "* Preparing autocomplete trie..."
        filename = kwargs.get('filename')

        parsed_key = 'auto-' + filename
        if parsed_key not in PARSED_TREES:
            self.trie = Trie()
            try:
                self.trie.update(self.allLemmas)
            except:
                print "Trie processing error"
                print list(self.allLemmas)
                self.trie = False
            PARSED_TREES[parsed_key] = self.trie

        else:
            self.trie = PARSED_TREES['auto-'+filename]


class ReverseLookups(XMLDict):
    """

    1. don't use entries with reverse="no" at entry level

    2. search by e/mg/tg/t/text() instead of /e/lg/l/text()

    """

    def cleanEntry(self, e):
        ts = e.findall('mg/tg/t')
        ts_text = [t.text for t in ts]
        ts_pos = [t.get('pos') for t in ts]

        l = e.find('lg/l')
        right_text = [l.text]

        return {'left': ts_text, 'pos': ts_pos, 'right': right_text}

    def lookupLemmaStartsWith(self, lemma):
        _xpath = './/e[mg/tg/t/starts-with(text(), "%s")]' % lemma
        return self.XPath(_xpath)

    def lookupLemma(self, lemma):
        _xpath = [ './/e[mg/tg/t/text() = "%s"' % lemma
                 , 'not(@reverse)]'
                 ]
        _xpath = ' and '.join(_xpath)
        nodes = self.XPath(_xpath)
        return self.modifyNodes(nodes)

    def lookupLemmaPOS(self, lemma, pos):
        _xpath = ' and '.join(
            [ './/e[mg/tg/t/text() = "%s"' % lemma
            , 'not(@reverse)'
            , 'mg/tg/t/@pos = "%s"]' % pos.lower()
            ]
        )
        return self.XPath(_xpath)


class DictionaryEntry(object):
    """
    An entry from the XML dictionary.


    """

    def __init__(self, lemma_ir, pos, source, lemma_content, stem,
                 translation, translation_language, translation_pos,
                 lemma_alt=None):
        """

        :param lemma_ir: :text()
        :param pos: .//l[@pos]
        :param source: .//[@src]
        :param lemma_content: .//lc:text()
        :param stem: .//stem:text()
        :param translation: .//t:text()
        :param translation_language: .//tg[@xml:lang]
        :param translation_pos: .//t[@pos]
        :param lemma_alt: Alternate orthography representation.
        """
        self.lemma_ir = lemma_ir
        self.pos = pos
        self.source = source
        self.lemma_content = lemma_content
        self.stem = stem
        self.translation = translation
        self.translation_language = translation_language
        self.translation_pos = translation_pos
        self.lemma_alt = lemma_alt

    @property
    def lemma(self):
        """
        :return: The lemma, in the preferred orthography. If not available, then
                 simply the lemma in the internal representation.
        """
        return self.lemma_alt or self.lemma_ir

    @classmethod
    def from_element(cls, element, lemma_alt=None):
        """
        Creates a DictionaryEntry (or subclass) from the etree.Element instance.
        :param element: etree.Element <e src="..."></e>
        :return: a DictionaryEntry
        """
        return cls(element.findtext('.//l'),
                   element.findtext('.//l[@pos]'),
                   element.attrib['src'],
                   element.findtext('.//lc'),
                   element.findtext('.//stem'),
                   element.findtext('.//t'),
                   NotImplemented, # This doesn't work: .findtext('.//tg[@xml:lang]'),
                   element.findtext('.//t[@pos]'),
                   lemma_alt=lemma_alt)


class DictionaryEntryXMLDictCompat(DictionaryEntry):
    """
    Same as DictionaryEntry, but provides special functions to be compatible with
    the deprecated, lxml.Element ways.
    """

    def findtext(self, query, default=None):
        # TODO: interpret queries as requests for data.
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError


class AlternateOrthographyDict(object):
    """
    A lexicon/Dict (not to be confused with Python's dict) that wraps an existing Dict,
    however, it produces results in an alternate orthography.
    """

    def __init__(self, language_pair, orthography, original_dict):
        """

        :param original_dict: XMLDict
        :param source_language_code: string
        """
        self._original_dict = original_dict
        self.language_pair = language_pair
        source, _, self.script = orthography.partition('-')
        if source != self.language_pair[0]:
            raise ValueError('Mismatched language pair and orthography: %r %r' %
                             (language_pair, orthography))
        assert self.script, 'empty script for orthography: ' + self.orthography
        # TODO: figure out orthography!

    @property
    def orthography(self):
        """
        :return: the language tag of the source language, with orthography.
        Something like 'crk-Cans'.
        """
        return '%s-%s' % (self.source, self.script)

    @property
    def source(self):
        """
        :return: the source language, without the orthography or script.
        """
        return self.language_pair[0]

    def lookupLemmaStartsWith(self, *args, **kwargs):
        return self._remap(self._original_dict.lookupLemmaStartsWith(*args, **kwargs))

    def lookupLemma(self, *args, **kwargs):
        return self._remap(self._original_dict.lookupLemma(*args, **kwargs))

    def lookupLemmaPOS(self, *args, **kwargs):
        return self._remap(self._original_dict.lookupLemmaPOS(*args, **kwargs))

    def lookupLemmaPOSAndType(self, *args, **kwargs):
        return self._remap(self._original_dict.lookupLemmaPOSAndType(*args, **kwargs))

    def lookupOtherLemmaAttr(self, *args, **kwargs):
        return self._remap(self._original_dict.lookupOtherLemmaAttr(*args, **kwargs))

    # TODO: implement iterate_entries(...)
    # TODO: implement iterate_letter_pages(...)
    # TODO: implement iterate_entries_count(...)
    # TODO: implement lookupOtherLemmaAttr(...)

    def _remap(self, elements):
        """
        Maps each element to a DictionaryEntry instance.
        :param elements: a list of etree.Element instances obtained from the XML dictionary.
        :return: a list of DictionaryEntry instances
        """
        return [DictionaryEntryXMLDictCompat.from_element(e) for e in elements]


class Lexicon(object):

    def __init__(self, settings):
        """ Create a lexicon based on the configuration.

        Each XML file will be loaded individually, and the file handle
        will be cached, so if multiple dictionaries (for example, one
        lexicon may have multiple input variants), these will not be
        loaded into memory separately.

        """

        from collections import OrderedDict

        # Initialize variant lookup types
        lookup_types = {
            'regular': XMLDict,
            'test_data': XMLDict,
        }

        lookup_types.update(search_types.search_types)

        reg_type = lookup_types.get('regular', XMLDict)

        language_pairs = dict(
            [ (k, reg_type(filename=v, options=settings.dictionary_options.get(k, {})))
              for k, v in settings.dictionaries.iteritems() ]
        )

        # TODO: Create "derivative" dictionaries that parse a "base" dictinonary once,
        # but act as spelling variant dictionaries.
        #
        # e.g.,
        #  - crkeng-Macron.xml derives from crkeng.xml
        #  - crkeng-Cans.xml derives from crkeng.xml
        alternate_dicts = {
            k: self.create_variant_dictionary(k, v, reg_type, settings, language_pairs)
            for k, v in settings.variant_dictionaries.iteritems()
        }

        # run through variant searches for overrides
        variant_searches = dict()

        for k, variants in settings.search_variants.iteritems():
            pair_variants = OrderedDict()
            for var in variants:
                variant_type = var.get('type', 'regular')
                cls = lookup_types.get(variant_type)
                variant_search = cls(filename=var.get('path'))
                pair_variants[variant_type] = variant_search
            variant_searches[k] = pair_variants

        self.variant_searches = variant_searches
        # language_pairs.update(alternate_dicts)
        langs_and_alternates = {}
        langs_and_alternates.update(language_pairs)
        langs_and_alternates.update(alternate_dicts)

        self.lookup = lexicon_overrides.process_postlookups(
            langs_and_alternates,
            lexicon_overrides.process_prelookups(
                langs_and_alternates,
                self.lookup
            )
        )

        self.variant_lookup = lexicon_overrides.process_postlookups(
            variant_searches,
            lexicon_overrides.process_prelookups(
                variant_searches,
                self.variant_lookup
            )
        )

        self.language_pairs = langs_and_alternates

        autocomplete_tries = {}
        for k, v in language_pairs.iteritems():
            if settings.pair_definitions.get(k).get('autocomplete'):
                has_root = language_pairs.get(k)
                if has_root:
                    fname = settings.dictionaries.get(k)
                    autocomplete_tries[k] = AutocompleteTrie( tree=has_root.tree
                                                            , filename=fname
                                                            , language_pair=k
                                                            )

        self.autocomplete_tries = autocomplete_tries

    @staticmethod
    def create_variant_dictionary(name, dictionary_info, reg_type, settings, language_pairs):
        if 'derivative_orthography' in dictionary_info:
            language_pair = dictionary_info['orig_pair']
            original_dict = language_pairs[language_pair]
            orthography = dictionary_info['derivative_orthography']
            return AlternateOrthographyDict(language_pair, orthography, original_dict)
        else:
            return reg_type(filename=dictionary_info.get('path'),
                            options=settings.dictionary_options.get(name, {}))

    def get_lookup_type(self, lexicon, lemma, pos, pos_type, lem_args):
        """ Determine what type of lookup to perform based on the
            available arguments, and return that lookup function.
        """

        args = ( bool(lemma)
               , bool(pos)
               , bool(pos_type)
               , bool(lem_args)
               )

        funcs = { (True, False, False, False): lexicon.lookupLemma
                , (True, True, False, False):  lexicon.lookupLemmaPOS
                , (True, True, True, False):   lexicon.lookupLemmaPOSAndType
                , (False, False, False, True): lexicon.lookupOtherLemmaAttr
                }

        largs = [lemma]

        if pos:
            largs.append(pos)
        if pos_type:
            largs.append(pos_type)

        return funcs.get(args, False), largs

    def browse(self, _from, _to, page=0, count=20, _format=None):

        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        start = count * page
        end = count * (page + 1)

        result = _dict.iterate_entries(start, end)

        if len(result) == 0:
            return False

        if _format:
            result = list(_format(result))

        return result

    def list_words(self, _from, _to, start=0, end=40, _format=None):

        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        result = _dict.iterate_entries(start, end, words=True)

        if len(result) == 0:
            return False

        if _format:
            result = list(_format(result))

        return result

    def get_letter_positions(self, _from, _to):

        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        result = _dict.iterate_letter_pages()

        if len(result) == 0:
            return False

        return result


    def lookup(self, _from, _to, lemma,
               pos=False, pos_type=False,
               _format=False, lemma_attrs=False, user_input=False):
        """ Perform a lexicon lookup. Depending on the keyword
        arguments, several types of lookups may be performed.

          * lemma lookup -
            `lexicon.lookup(source_lang, target_lang, lemma)`

          * lemma lookup + POS -
            `lexicon.lookup(source_lang, target_lang, lemma, pos=POS)`

             This lookup uses the lemma, and the `@pos` attribute on the <l /> node.

          * lemma lookup + POS + Type -
             `lexicon.lookup(source_lang, target_lang, lemma, pos=POS)`

             This lookup uses the lemma, the `@pos` attribute on the <l /> node,
             and the `@type` attribute.

          * lemma lookup + other attributes
            `lexicon.lookup(source_lang, target_lang, lemma, lemma_attrs={'attr_1': asdf, 'attr_2': asdf}`

            A dictionary of arguments may be supplied, matching attributes on the <l /> node.
        """

        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        _lookup_func, largs = self.get_lookup_type(_dict, lemma, pos, pos_type, lemma_attrs)

        if not _lookup_func and lemma is not None:
            raise Exception(
                "Unknown lookup type for <%s> (lemma: %s, pos: %s, pos_type: %s, lemma_attrs: %s)" %
                ( user_input
                , lemma
                , pos
                , pos_type
                , repr(lemma_attrs)
                )
            )

        if lemma_attrs:
            result = _lookup_func(**lemma_attrs)
        else:
            result = _lookup_func(*largs)

        if len(result) == 0:
            return False

        if _format:
            result = list(_format(result))

        return result

    def variant_lookup(self, _from, _to, search_type, lemma,
               pos=False, pos_type=False,
               _format=False, lemma_attrs=False, user_input=False):
        """ Perform a lexicon lookup. Depending on the keyword
        arguments, several types of lookups may be performed.

          * term lookup -
            `lexicon.lookup(source_lang, target_lang, type, term)`

          TODO: these

          * lemma lookup + POS -
            `lexicon.lookup(source_lang, target_lang, lemma, pos=POS)`

             This lookup uses the lemma, and the `@pos` attribute on the <l /> node.

          * lemma lookup + POS + Type -
             `lexicon.lookup(source_lang, target_lang, lemma, pos=POS)`

             This lookup uses the lemma, the `@pos` attribute on the <l /> node,
             and the `@type` attribute.

          * lemma lookup + other attributes
            `lexicon.lookup(source_lang, target_lang, lemma, lemma_attrs={'attr_1': asdf, 'attr_2': asdf}`

            A dictionary of arguments may be supplied, matching attributes on the <l /> node.
        """

        _dict = self.variant_searches.get((_from, _to), {}).get(search_type, False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        _lookup_func, largs = self.get_lookup_type(_dict, lemma, pos, pos_type, lemma_attrs)

        if not _lookup_func:
            raise Exception(
                "Unknown lookup type for <%s> (lemma: %s, pos: %s, pos_type: %s, lemma_attrs: %s)" %
                ( user_input
                , lemma
                , pos
                , pos_type
                , repr(lemma_attrs)
                )
            )

        if lemma_attrs:
            result = _lookup_func(**lemma_attrs)
        else:
            result = _lookup_func(*largs)

        if len(result) == 0:
            return False

        if _format:
            result = list(_format(result))

        return result

    def lookups(self, _from, _to, lookups, *args, **kwargs):
        from functools import partial

        _look = partial( self.lookup
                       , _from=_from
                       , _to=_to
                       , *args
                       , **kwargs
                       )

        results = zip( lookups
                     , map(lambda x: _look(lemma=x), lookups)
                     )

        success = any([res for l, res in results])

        return results, success
