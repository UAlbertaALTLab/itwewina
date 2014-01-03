# -*- encoding: utf-8 -*-
"""
sma-specific overrides, and pregenerated paradigm selection.

A set of lexicon-related language specific rules, provided by
`lexicon.LexiconOverrides`. There is probably a better location
for this documentation, but for now ...

Example source formatting function:

    @lexicon.entry_source_formatter('sme')
    def format_source_sme(ui_lang, entry_node):
        # do some processing on the entry node ...
        if successful:
            return some_formatted_string
        return None

Example target string formatting function:

    @lexicon.entry_target_formatter('sme', 'nob')
    def format_target_sme(ui_lang, entry_node, tg_node):
        # do some processing on the entry and tg node ...
        if successful:
            return some_formatted_string
        return None

"""

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

from morphology import generation_overrides as morphology
from lexicon import lexicon_overrides as lexicon
from flask import current_app
from morpholex import morpholex_overrides as morpholex

# TODO: for sma
context_for_tags = {
    # EX: guokte
    (u"gápmagat", "Num+Pl+Nom"): u"%(word_form)s (gápmagat)",
    (u"gápmagat", "Num+Pl+Gen"): u"%(word_form)s (gápmagiid)",

    (u"NONE", "N+Prop+Sem/Plc+Sg+Gen"): u"%(word_form)s baaktoe",
    (u"NONE", "N+Prop+Sem/Plc+Pl+Gen"): u"%(word_form)s baaktoe",

    # TODO: generic available if no context="mun" equivalent
    # EX: båetedh
    # ("NONE", "V+Ind+Prs+Sg1"):        u"(daan biejjien manne) %(word_form)s",
    # ("NONE", "V+Ind+Prs+Sg3"):        u"(daan biejjien dïhte) %(word_form)s",
    # ("NONE", "V+Ind+Prs+Pl3"):        u"(daan biejjien dat) %(word_form)s",
    # ("NONE", "V+Ind+Prt+Sg1"):        u"(jååktan manne) %(word_form)s",
    # ("NONE", "V+ConNeg"):             u"(ij) %(word_form)s",
    # ("NONE", "V+PrfPrc"):             u"(lea) %(word_form)s",
    # ("NONE", "V+Ger"):                u"(lea) %(word_form)s",

}

# TODO: for sma
@morphology.postgeneration_filter_for_iso('sma')
def word_generation_context(generated_result, *generation_input_args):
    """ **Post-generation filter***

    Include context for verbs in the text displayed in paradigm
    generation. The rule in this case is rather complex, and looks at
    the tag used in generation.

    Possible contexts:
      * (mun) dieđán
    """
    node  = generation_input_args[2]

    # TODO: for some reason not running...
    print generated_result
    print generation_input_args

    if len(node) == 0:
        return generated_result

    context = node.xpath('.//l/@context')

    if len(context) > 0:
        context = context[0]
    else:
        context = 'NONE'
        # return generated_result

    def apply_context(form):
        lemma, tag, forms = form
        tag = '+'.join(tag)

        context_formatter = context_for_tags.get(
            (context, tag), False
        )
        if context_formatter:
            formatted = []
            if forms:
                for f in forms:
                    f = context_formatter % {'word_form': f, 'context': context}
                    formatted.append(f)
            formatted_forms = formatted
        else:
            formatted_forms = forms

        tag = tag.split('+')

        return (lemma, tag, formatted_forms)

    print generated_result
    return map(apply_context, generated_result)

@lexicon.entry_source_formatter('sma')
def format_source_sma(ui_lang, e, target_lang):
    from morphology.utils import tagfilter_conf

    paren_args = []

    _str_norm = 'string(normalize-space(%s))'
    _lemma = e.xpath(_str_norm % 'lg/l/text()')
    _class = e.xpath(_str_norm % 'lg/l/@class')
    _pos = e.xpath(_str_norm % 'lg/l/@pos')

    _lemma_ref = e.xpath(_str_norm % 'lg/lemma_ref/text()')
    if _lemma_ref:
        _link_targ = u'/detail/%s/%s/%s.html' % ('sma', target_lang, _lemma_ref)
        _lemma_ref_link = u'<a href="%s"/>%s</a>' % (_link_targ, _lemma_ref)
        _lemma_ref_link = u'<span class="see_also"> → '  + _lemma_ref_link
        _lemma_ref_link += u'</span>'

    else:
        _lemma_ref_link = ''

    if _pos:
        filters = current_app.config.tag_filters.get(('sma', 'nob'))
        paren_args.append(tagfilter_conf(filters, _pos))

    if _class:
        paren_args.append(_class)

    if len(paren_args) > 0:
        entry_string = '%s (%s)' % (_lemma, ', '.join(paren_args))
        return entry_string + _lemma_ref_link
    else:
        return _lemma

    return None

# LEX_TO_FST = {
#     'a': 'A',
#     'adv': 'Adv',
#     'n': 'N',
#     'npl': 'N',
#     'num': 'Num',
#     'prop': 'Prop',
#     'v': 'V',
# }

@morphology.pregenerated_form_selector('sma')
def pregenerate_sma(form, tags, node):
    _has_mini_paradigm = node.xpath('.//mini_paradigm[1]')

    _has_lemma_ref     = node.xpath('.//lemma_ref')
    if len(_has_lemma_ref) > 0:
        return form, [], node, []
    if len(_has_mini_paradigm) == 0:
        return form, tags, node
    else:
        mp = _has_mini_paradigm[0]

    def analysis_node(node):
        """ Node ->
            ("lemma", ["Pron", "Sg", "Tag"], ["wordform", "wordform"])
        """
        tag = node.xpath('.//@ms')
        if len(tag) > 0:
            tag = tag[0].split('_')
        else:
            tag = []

        wfs = node.xpath('.//wordform/text()')

        return (form, tag, wfs)

    analyses = map(analysis_node, mp.xpath('.//analysis'))

    return form, tags, node, analyses

from common import remove_blank, match_homonymy_entries

morphology.postgeneration_filter_for_iso(
    'sma',
)(remove_blank)

morpholex.post_morpho_lexicon_override(
    'sma'
)(match_homonymy_entries)

