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

import os
import neahtta
import unittest

# TODO: run a test against all sme stuff

class TemplateRenderTest(unittest.TestCase):
    """ Test basic template rendering.
    """

    def setUp(self):
        from entry_templates import TemplateConfig

        _app = neahtta.app
        # Turn on debug to disable SMTP logging
        _app.debug = True
        _app.logger.removeHandler(_app.logger.smtp_handler)

        # Disable caching
        _app.caching_enabled = False
        self.app = _app.test_client()
        self.current_app = _app
        self.template_renderer = TemplateConfig(self.current_app)

    def testRenderSme(self):

        with self.current_app.app_context():
            lookup = self.current_app.morpholexicon.lookup('mannat', source_lang='sme', target_lang='nob')
            # TODO: current_app missing new style template filter
            # extension
            for lexicon, analyses in lookup:
                rendered = self.template_renderer.render_template('sme', 'entry.template',
                                             lexicon_entry=lexicon,
                                             analyses=analyses, _from='sme',
                                             _to='nob')
                print rendered
