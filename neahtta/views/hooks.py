﻿from . import blueprint
from flask import current_app
from i18n.utils import iso_filter

from flask import ( request
                  , session
                  , g
                  )

@blueprint.before_request
def set_pair_request_globals():
    """ Set global language pair infos.
    """

    if '_from' in request.view_args and '_to' in request.view_args:
        g._from = request.view_args.get('_from')
        g._to = request.view_args.get('_to')
    else:
        if request.url_rule == '/':
            g._from, g._to = current_app.config.default_language_pair

    if hasattr(g, '_to'):
        g.ui_lang = iso_filter(session.get('locale', g._to))
    else:
        g.ui_lang = iso_filter(session.get('locale'))