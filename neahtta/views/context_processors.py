from flask import current_app, request, g, session, render_template
from . import blueprint

from i18n.utils import get_locale

@blueprint.context_processor
def project_css():
    if current_app.config.has_project_css:
        return {'project_css': current_app.config.has_project_css}
    return {}


@blueprint.context_processor
def sources_template():
    get_template = current_app.jinja_env.select_template

    sources_template_exists = False
    has_sources = False

    _from, _to = current_app.config.default_language_pair
    has_sources = current_app.lexicon_templates.has_local_override(
        _from,
        'sources.template',)

    try:
        sources_template_path = './templates/sources.%s.html' % current_app.config.short_name
        with open(sources_template_path, 'r') as F:
            sources_template_exists = True
    except Exception, e:
        sources_template_exists = False

    return {'sources_template_exists': sources_template_exists or has_sources}

@blueprint.context_processor
def text_tv():
    if session.get('text_tv', False):
        return {'text_tv': True}
    else:
        return {'text_tv': False}

@blueprint.context_processor
def check_notice():
    from jinja2 import TemplateNotFound

    _from, _to = current_app.config.default_language_pair
    project_notice = current_app.lexicon_templates.render_individual_template(
        _from,
        'notice.template',
        **{'current_locale': get_locale()}
    )

    return {'project_notice': project_notice}

@blueprint.context_processor
def add_current_locale_code():
    return {'current_locale': get_locale()}

@blueprint.context_processor
def add_current_pair():
    """ If the request is for a form or a lookup, we include
    """

    _from = False
    _to = False
    pair_settings = False

    if hasattr(g, '_from') and hasattr(g, '_to'):
        _from = g._from
        _to = g._to
    else:
        _from, _to = current_app.config.default_language_pair

    pair_settings, orig_pair_opts = current_app.config.resolve_original_pair(_from, _to)

    return dict(_from=_from, _to=_to, current_pair_settings=pair_settings)

@blueprint.context_processor
def add_languages():
    """ Add internationalization languages to global context for
    templates.
    """
    return dict(internationalizations=current_app.config.locales_available)

@blueprint.context_processor
def define_app_name():
    """ Add the custom current_app name from configs to global context for
    templates.
    """
    return dict(app_name=current_app.config.app_name)

@blueprint.context_processor
def nav_style():
    return dict(grouped_nav=current_app.config.grouped_nav, new_mobile_nav=current_app.config.new_mobile_nav)

@blueprint.context_processor
def define_app_meta():
    return dict(app_meta_desc=current_app.config.meta_description)

@blueprint.context_processor
def define_app_title():
    return dict(app_meta_title=current_app.config.app_meta_title)

@blueprint.context_processor
def define_app_short_name():
    return dict(app_short_name=current_app.config.short_name)

@blueprint.context_processor
def define_app_mobile_bookmark_name():
    return dict(app_mobile_bookmark_name=current_app.config.app_mobile_bookmark_name)

@blueprint.context_processor
def define_app_meta_keywords():
    return dict(app_meta_keywords=current_app.config.meta_keywords)

@blueprint.context_processor
def define_app_production_mode():
    return dict(production_mode=current_app.production)

@blueprint.context_processor
def define_global_language_pairs():
    return dict(language_pairs=current_app.config.pair_definitions)

@blueprint.context_processor
def language_pairs_grouped_by_source():
    return dict(language_pairs_grouped_by_source=current_app.config.pair_definitions_grouped_source_locale())

@blueprint.context_processor
def define_variant_dictionaries():
    return dict(variant_dictionaries=current_app.config.variant_dictionaries)

@blueprint.context_processor
def detect_mobile_variables():
    # mobile test for most common browsers
    mobile = False
    if request.user_agent.platform in ['iphone', 'android']:
        mobile = True

    iphone = False
    if request.user_agent.platform == 'iphone':
        iphone = True

    return dict(mobile=mobile, iphone=iphone)

@blueprint.context_processor
def footer_template():

    _from, _to = current_app.config.default_language_pair
    footer_template = current_app.lexicon_templates.render_individual_template(
        _from,
        'footer.template',
        **{'current_locale': get_locale()}
    )
    return {'footer_template': footer_template}
