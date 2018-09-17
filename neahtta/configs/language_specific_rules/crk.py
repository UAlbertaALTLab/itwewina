# -*- coding: UTF-8 -*-
import re

from morphology import generation_overrides as morphology
from morpholex import morpholex_overrides as morpholex
from lexicon import lexicon_overrides

from lexicon import search_types, CustomLookupType
from lxml import etree

from morphology.morphology import TagPart
from views.custom_rendering import template_rendering_overrides

from flask import current_app, g


@lexicon_overrides.pre_lookup_tag_rewrite_for_iso('eng')
def casefold_english_search(source, target, search_term, **kwargs):
    """
    Support for casefolding (case-insensitive) search from eng -> crk.

    This assumes all the lemmas in engcrk.xml are lower case (which may be
    false).
    """

    # XXX: This function knows WAAAAAAAY too much about how
    # lexicon.Lexicon.lookup() is implemented.
    # After all, this function's purpose is to modify the arguments
    # to .lookup() before it's called  ¯\_(ツ)_/¯

    if kwargs.get('tried_case_folding', False):
        # We've already tried case-folding the arguments,
        # and that didn't work so search with the user input verbatim.
        new_kwargs = kwargs.copy()
        new_kwargs.update(redo_search_with_user_input=False)
        del new_kwargs['tried_case_folding']
        args = (source, target, search_term or kwargs.get('user_input'))
    else:
        # Let's try case-folding!
        args = (source, target, search_term.lower())
        new_kwargs = kwargs.copy()
        # If case-folding didn't work, we'll ask Lexicon.lookup() to
        # redo the search using the original term. This will search for an
        # EXACT match in the XML dictionary, including letter case
        # (and hit the True case of this if/else in the process).
        new_kwargs.update(redo_search_with_user_input=True)

    return args, new_kwargs


@lexicon_overrides.pre_lookup_tag_rewrite_for_iso('crkS')
def remove_spaces_before_lemma(source, target, lemma, **kwargs):
    """
    Syllabics lemmas may have spaces before them. These will not match in
    the XML dictionary, so get rid of the leading spaces.

    :param source: 'crkS'
    :param target: probably 'eng'
    :param lemma: (unicode) a lemma in syllabics, maybe with a leading space.
    :return: altered arguments with "fixed" lemma
    """
    assert source in ('crkS', u'crkS')
    args = (source, target, lemma.lstrip())
    return args, kwargs


@template_rendering_overrides.register_custom_sort(('crk', 'eng'), ('crkMacr', 'eng'), ('crkS', 'eng'))
def sort_by_analyses(search_result_obj, unsorted_entries_and_tags_and_paradigms):
    """ This is where we sort analyses first, and then everything else.

    Copying the original sorting to modify that. Original sort is:
     * entries where lemma matches (==) the user input first
     * otherwise alphabetical sort by lemma.

    TODO:
     * show analyses first, perhaps with absolute match first of these;
     * then show sorted non-morphological matches below

    """

    def sort_key((lex, morph, p, l)):
        _str_norm = 'string(normalize-space(%s))'
        lemma = lex.xpath(_str_norm % './lg/l/text()')
        return (lemma, morph)

    def sort_with_user_input_first((a_lemma, a_morph), (b_lemma, b_morph)):
        a_has_morph = len(a_morph) > 0
        b_has_morph = len(b_morph) > 0

        a_lemma_matches_input = a_lemma == search_result_obj.user_input
        b_lemma_matches_input = b_lemma == search_result_obj.user_input

        move_up = -1
        move_down = 1
        no_diff = 0

        def sort_lemma_alpha():
            if a_lemma < b_lemma:
                return move_up
            elif a_lemma > b_lemma:
                return move_down
            else:
                return no_diff

        # sort alphabetically within main groups split by presence of
        # lemmas
        if (a_has_morph and b_has_morph) or (not a_has_morph and not b_has_morph):
            return sort_lemma_alpha()

        # otherwise sort by presence of morphology
        if a_has_morph and not b_has_morph:
            return move_up

        if not a_has_morph and b_has_morph:
            return move_down

        return no_diff

    return sorted( unsorted_entries_and_tags_and_paradigms
                 , key=sort_key
                 , cmp=sort_with_user_input_first
                 )

# @lexicon_overrides.postlookup_filters_for_lexicon(('eng', 'crk'))
# def sort_by_rank(lex, nodelist, *args, **kwargs):
# 
#     _str_norm = 'string(normalize-space(%s))'
# 
#     def get_rank(n):
#         try:
#             rank = int( n.xpath(_str_norm % './/rank/@rank') )
#         except:
#             rank = False
#         if rank:
#             return rank
#         else:
#             return n.xpath(_str_norm % './/l/text()')
# 
#     return sorted(nodelist, key=get_rank)

# NB: general search type, so crk->eng, and everything else that isn't
# eng->crk substring type
class CustomCrkSearch(CustomLookupType):
    """ This is the custom lookup type class from which all custom
    lookup types should be subclassed.
    """

    lemma_match_query = './/e[re:test(lg/l/text(), $lemma_fuzz, \'i\')]'

    # we will use this to match things less than 3 chars.
    lemma_strict_match = './/e[lg/l/text() = $lemma]'

    def lookupLemma(self, lemma):

        if len(lemma) <= 3 or g._from == 'eng':
            match_fx = self.prepare_xpath(self.lemma_strict_match)
        else:
            match_fx = self.lemma

        # Can only have one character on the left side, because
        # iterating through input string one character by one character
        # to make sure replacements don't overlap.

        # TODO: can we use a generalized spell relax function for this?
        fuzzings = {
            u'a': u'[aâā]',
            u'â': u'[aâā]',
            u'i': u'[iîī]',
            u'î': u'[iîī]',
            u'e': u'[eêē]',
            u'ê': u'[eêē]',
            u'u': u'[uûū]',
            u'û': u'[uûū]',
        }

        lemma_fuzz = ''
        for c in lemma:
            lemma_fuzz += fuzzings.get(c, c)

        return self.XPath( match_fx
                         , lemma=lemma
                         , lemma_fuzz=lemma_fuzz
                         )

search_types.add_custom_lookup_type('regular')(CustomCrkSearch)

# NB: eng->crk only 
class EngToCrkSubstringLookups(CustomLookupType):
    """
    NB: for the moment this is eng-crk specific, this is defined in itwewina.config.yaml.in

    # TODO: document this

    """

    lemma = etree.XPath('.//e[contains(mg/tg/key/text(), $lemma)]')

    def filterNodes(self, nodes, lemma):
        """ This is our own custom modification within this search type
        will pop off definition nodes that do not match, by operating on
        clones and returning the clones.

        Here we select the children of the <e /> and run a test on them,
        if they succeed, then don't pop the node. Then return the
        trimmed elements.

        This is probably the best option for compatibility with the rest
        of NDS, but need to have a way of generalizing this, because at
        the moment, this is lexicon-specific.
        """
        import copy

        def duplicate_node(node):
            return copy.deepcopy(node)

        def test_node(node):
            tg_node_expr = " and ".join([
                '(key/text() = "%s")' % l_part
                for l_part in lemma.split(',')
            ])
            _xp = 'tg[%s]' % tg_node_expr
            return len(node.xpath(_xp)) == 0

        def process_node(node):
            mgs = node.findall('mg')
            c = len(node.findall('mg'))

            # Remove nodes not passing the test, these shall diminish
            # and go into the west, and remain <mg />.
            for mg in mgs:
                if test_node(mg):
                    c -= 1
                    node.remove(mg)

            # If trimming <mg /> results in no actual translations, we
            # don't display the node.
            if c == 0:
                return None
            else:
                return node

        new_nodes = []
        for node in map(duplicate_node, nodes):
            new_nodes.append(process_node(node))

        return [n for n in new_nodes if n != None]

    def lookupLemma(self, lemma):

        keys = ' and '.join([
            '(mg/tg/key/text() = "%s")' % l
            for l in lemma.split(',')
        ])

        key_expr = './/e[%s]' % keys

        xp = etree.XPath(key_expr)

        nodes = self.XPath( xp, lemma=lemma)
        return self.filterNodes(nodes, lemma=lemma)

search_types.add_custom_lookup_type('substring_match')(EngToCrkSubstringLookups)

# NB: this search type has not been registered, just copying here so it
# will not get lost.
# 
# search_types.add_custom_lookup_type('keyword')(SubstringLookups)
class KeywordLookups(CustomLookupType):
    """
    NB: for the moment this is eng-crk specific.

    1. search by //e/mg/tg/t/text() instead of //e/lg/l/text()
    2. after the search, we duplicate and re-test the matched <e />
       nodes to remove any <mg /> that do not apply to the query.
    3. Duplicated nodes are returned to the rest of the query, and no
       one knows the difference

    TODO: how to provide an entry hash for these? Linkability to search
      results would be great.

    TODO: think about how to generalize this. Since this is code beyond
    a sort of 'base functionality', it may need to stand somewhere other
    than in `lexicon.lexicon`. Providing an easy API for extending
    search types would be great, because down the line there will be
    more search types.

    """

    def __init__(self, filename=False, tree=False):
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
        self.lemma = etree.XPath('.//e[mg/tg/key/text() = $lemma]')

    def cleanEntry(self, e):
        ts = e.findall('mg/tg/t')
        ts_text = [t.text for t in ts]
        ts_pos = [t.get('pos') for t in ts]

        l = e.find('lg/l')
        right_text = [l.text]

        return {'left': ts_text, 'pos': ts_pos, 'right': right_text}

    def filterNodes(self, nodes, lemma):
        """ 
        # TODO: update this so it's not operating on keywords, instead
        # definitions

        Modify the nodes in some way, but by duplicating them first.

        Here we select the children of the <e /> and run a test on them,
        if they succeed, then don't pop the node. Then return the
        trimmed elements.

        This is probably the best option for compatibility with the rest
        of NDS, but need to have a way of generalizing this, because at
        the moment, this is lexicon-specific.
        """
        import copy

        def duplicate_node(node):
            # previously: etree.XML(etree.tostring(node))
            return copy.deepcopy(node) 

        def test_node(node):
            tg_node_expr = " and ".join([
                '(key/text() = "%s")' % l_part
                for l_part in lemma.split(',')
            ])
            _xp = 'tg[%s]' % tg_node_expr
            return len(node.xpath(_xp)) == 0

        def process_node(node):
            mgs = node.findall('mg')
            c = len(node.findall('mg'))
            # Remove nodes not passing the test, these shall diminish
            # and go into the west, and remain <mg />.
            for mg in mgs:
                if test_node(mg):
                    c -= 1
                    node.remove(mg)
            # If trimming <mg /> results in no actual translations, we
            # don't display the node.
            if c == 0:
                return None
            else:
                return node

        new_nodes = []
        for node in map(duplicate_node, nodes):
            new_nodes.append(process_node(node))

        return [n for n in new_nodes if n != None]

    def lookupLemma(self, lemma):

        keys = ' and '.join([
            '(mg/tg/key/text() = "%s")' % l
            for l in lemma.split(',')
        ])

        key_expr = './/e[%s]' % keys

        xp = etree.XPath(key_expr)

        nodes = self.XPath( xp, lemma=lemma)
        return self.filterNodes(nodes, lemma=lemma)


@morphology.postgeneration_filter_for_iso('crk', 'crkMacr', 'crkS')
def force_hyphen(generated_forms, *input_args, **input_kwargs):
    """ For any +Cnj forms that are generated, filter out those
    without ê- """

    def matches_hyphen(f):
        return u'ê-' in f or u'ē-' in f

    def form_fx((tag, forms)):
        if forms:
            _hyph = [f for f in forms if '-' in f]
            if len(_hyph) > 0:
                unhyphs = [h.replace('-', '') for h in _hyph]
                # throw out all forms that have a hyphenated equivalent
                _filt = lambda x: x not in unhyphs and '%' not in x
                fs = filter(_filt, forms)
                return (tag, fs)

        return (tag, forms)

    return map(form_fx, generated_forms)

@morphology.tag_filter_for_iso('crk', 'crkMacr', 'crkS')
def adjust_tags_for_gen(lemma, tags, node=None, **kwargs):
    """ **tag filter**: Lexicon -> FST changes.

    Change POS to be compatible with FST for when they are not.
    """

    if 'template_tag' not in kwargs:
        return lemma, tags, node

    # get tagset for pre-lemma stuff
    morph = current_app.config.morphologies.get(g._from, False)
    tagsets = morph.tagsets.sets

    prelemmas = tagsets.get('prelemma_tags')

    prelemma_pattern = create_prelemma_matcher(prelemmas.members)

    cleaned_tags = []
    for t in tags:
        # Figure out which tags goes BEFORE the lemma.
        prefixes = []
        suffixes = []

        for tag in t:
            if prelemma_pattern.match(tag):
                prefixes.append(tag)
            else:
                suffixes.append(tag)

        cleaned_tag = prefixes + [lemma] + suffixes
        cleaned_tags.append(cleaned_tag)

    if len(cleaned_tags) == 0 and len(tags) > 0:
        tags = cleaned_tags

    return lemma, cleaned_tags, node


def create_prelemma_matcher(prelemmas):
    """
    Given a sequence of prelemma tags, spits out a compiled regular expression that will match a tag.
    This pattern is helpful for filtering prelemma tagparts in a taglist.

    >>> rdplw = TagPart('RdplW')
    >>> rdpls = TagPart('RdplS')
    >>> pv = TagPart({'match': '^PV', 'regex': True})
    >>> prelemmas = [rdplw, rdpls, pv]
    >>> p = create_prelemma_matcher(prelemmas)
    >>> p.pattern
    u'(?:^RdplW$)|(?:^RdplS$)|(?:^PV)'
    >>> bool(p.match(u'RdplW'))
    True
    >>> bool(p.match(u'PV/e'))
    True
    >>> bool(p.match(u'pve'))
    False
    >>> bool(p.match(u'lemmaRdplW'))
    False

    :param prelemmas: Sequence of prelemma tags
    :return: a compiled regular expression
    """

    alternatives = []

    for tagpart in prelemmas:
        assert isinstance(tagpart, TagPart)
        if tagpart.regex:
            alternatives.append(unicode(tagpart.val))
        else:
            alternatives.append(u'^' + unicode(tagpart) + u'$')

    return re.compile(u'|'.join(u'(?:' + regex + u')' for regex in alternatives))
