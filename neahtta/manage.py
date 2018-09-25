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

from flask import Flask
from flask.ext.actions import Manager
from neahtta import app

from fabric.colors import red, green

manager = Manager(app, default_server_actions=True)

@manager.register('compilemessages')
def compilemessages(app):
    """ TODO: pybabel compile -d translations
    """
    def action():
        print """ You might be looking for this ...
            - pybabel compile -d translations
        """
        return False
    return action

@manager.register('makemessages')
def hello(app):
    def action():
        """ You might be looking for this ...
            - pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
            - pybabel update -i translations/messages.pot -d translations
        """
        return False
    return action

@manager.register('chk-fst-paths')
def chk_fst_paths(app):

    def get_dates(_file):
        import os.path, time
        return time.ctime(os.path.getctime(_file))

    def action():
        fsts = app.config.yaml.get('Morphology').iteritems()
        print ''
        print 'Checking config files and whether they exist...'
        missing_fst = False
        for k, v in fsts:
            file_path = ''.join(v.get('file'))
            i_file_path = ''.join(v.get('inverse_file'))
            file_exists   = red('MISSING: ')
            i_file_exists = red('MISSING: ')
            dates = 'UPDATED: ?'
            i_dates = 'UPDATED: ?'
            try:
                with open(file_path):
                    file_exists = green('FOUND:   ')
                    dates       = 'UPDATED: %s' % get_dates(file_path)
            except IOError:
                missing_fst = True
            try:
                with open(i_file_path):
                    i_file_exists = green('FOUND:   ')
                    i_dates       = 'UPDATED: %s' % get_dates(i_file_path)
            except IOError:
                missing_fst = True

            print "%s:" % k
            print "  " + file_exists + file_path
            print "  " + dates
            print ''
            print "  " + i_file_exists + i_file_path
            print "  " + i_dates
            print ''
            print ''

        if missing_fst:
            print red("Some FSTs were not found. See above.")
        return False
    return action

if __name__ == "__main__":
    app.caching_enabled = True
    manager.run()

