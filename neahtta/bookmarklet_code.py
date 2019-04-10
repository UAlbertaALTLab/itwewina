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

# This code works if you copy paste it into the browser's console,
# however in order for it to work as a bookmarklet, it must be URL
# encoded.

import re
import os
from urllib import quote



__all__ = [
    'bookmarklet_escaped',
    'bookmarklet_quote',
    'generate_bookmarklet_code',
    'prod_host'
]


def cwd(x):
    return os.path.join(os.path.dirname(__file__), x)


def minify(js_code):
    """
    Psuedo- JavaScript minification. Removes initial whitespace, double-slash comments, and all newlines.
    :param js_code:
    :return:
    """
    initial_whitespace = re.compile(r'^\s+', re.MULTILINE)
    double_slash_comments = re.compile(r'^//.*$', re.MULTILINE)
    newlines = re.compile(r'\n+')
    js_code = initial_whitespace.sub('', js_code)
    js_code = double_slash_comments.sub('', js_code)
    return newlines.sub('', js_code)


def bookmarklet_quote(x):
    return quote(x, safe="()")


def generate_bookmarklet_code(reader_settings, request_host):
    """
    Returns an escaped bookmarklet code, with the given reader settings.

    :param reader_settings:
    :param request_host:
    :return:
    """
    api_host = reader_settings.get('api_host', request_host)
    media_host = reader_settings.get('media_host', request_host)

    bmarklet = _bmark.replace('{{NDS_API_HOST}}', '//' + api_host)\
                     .replace('{{NDS_MEDIA_HOST}}', '//' + media_host)

    return bookmarklet_quote(bmarklet)


with open(cwd('static/js/bookmark.js'), 'r') as F:
    _bmark = minify(F.read())

bookmarklet_escaped = bookmarklet_quote(_bmark)

# TODO: is this actually used for anything?
prod_host = "sanit.oahpa.no"

