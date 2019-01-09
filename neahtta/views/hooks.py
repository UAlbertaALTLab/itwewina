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

from . import blueprint
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
    _from = request.view_args.get('_from')
    _to = request.view_args.get('_to')

    if '_from' in request.view_args and '_to' in request.view_args:
        g._from = request.view_args.get('_from')
        g._to = request.view_args.get('_to')
    elif 'from_language' in request.view_args and 'to_language' in request.view_args:
        g._from = request.view_args.get('from_language')
        g._to = request.view_args.get('to_language')
    else:
        if request.url_rule == '/':
            g._from, g._to = current_app.config.default_language_pair
            _from, _to = current_app.config.default_language_pair

    if hasattr(g, '_to'):
        g.ui_lang = iso_filter(session.get('locale', g._to))
    else:
        g.ui_lang = iso_filter(session.get('locale'))

    current_pair_settings, orig_pair_opts = current_app.config.resolve_original_pair(_from, _to)
    g.current_pair_settings = current_pair_settings

    orig = orig_pair_opts.get('orig_pair')
    if orig != ():
        g.orig_from, g.orig_to = orig
    else:
        g.orig_from, g.orig_to = _from, _to
