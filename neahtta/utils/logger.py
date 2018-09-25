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

import datetime

def get_time():
    return datetime.datetime.now().replace(microsecond=0).isoformat()

def get_ip(request):
    return request.remote_addr or ''

def logIndexLookups(user_input, results, from_language, to_language):
    from logging import getLogger
    from flask import request

    # This is all just for logging
    success = False
    result_lemmas = set()
    tx_set = set()

    for result in results:
        result_lookups = result.get('lookups')
        if result_lookups:
            success = True
            for lookup in result_lookups:
                l_left = lookup.get('left')
                l_right = ', '.join([_l.get('tx') for _l in lookup.get('right')])
                tx_set.add(l_right)
                result_lemmas.add(lookup.get('left'))

    result_lemmas = ', '.join(list(result_lemmas))
    meanings = '; '.join(list(tx_set))

    user_ip = ''

    if request:
        user_ip = get_ip(request)

    user_log = getLogger("user_log")
    user_log.info('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        user_input,
        str(success),
        result_lemmas,
        meanings,
        from_language,
        to_language,
        get_time(),
        user_ip
    ))

def logSimpleLookups(user_input, results, from_language, to_language):
    from logging import getLogger
    from flask import request

    # This is all just for logging
    success = False
    result_lemmas = set()
    tx_set = set()

    for result in results:
        result_lookups = result.get('lookups')
        if result_lookups:
            success = True
            for lookup in result_lookups:
                l_left = lookup.get('left')
                l_right = ', '.join(lookup.get('right'))
                tx_set.add(l_right)
                result_lemmas.add(lookup.get('left'))

    result_lemmas = ', '.join(list(result_lemmas))
    meanings = '; '.join(list(tx_set))

    user_ip = ''
    if request:
        user_ip = get_ip(request)

    user_log = getLogger("user_log")
    user_log.info('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        user_input,
        str(success),
        result_lemmas,
        meanings,
        from_language,
        to_language,
        get_time(),
        user_ip
    ))

