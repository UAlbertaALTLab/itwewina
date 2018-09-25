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

from urllib import quote, quote_plus
import os

cwd = lambda x: os.path.join(os.path.dirname(__file__), x)

with open(cwd('static/js/bookmark.min.js'), 'r') as F:
    bmark = F.read().replace('\n', '')

bookmarklet_quote = lambda x: quote(x, safe="()")
bookmarklet_escaped = bookmarklet_quote(bmark)

prod_host = "sanit.oahpa.no"

def generate_bookmarklet_code(reader_settings, request_host):
    api_host = reader_settings.get('api_host', request_host)
    media_host = reader_settings.get('media_host', request_host)

    bmarklet = bmark
    bmarklet = bmarklet.replace('OMGNDS_API_HOSTBBQ', '//' + quote_plus(api_host))\
                       .replace('OMGNDS_MEDIA_HOSTBBQ', '//' + quote_plus(media_host))

    return bmarklet
