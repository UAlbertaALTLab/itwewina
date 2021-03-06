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

# -*- coding: UTF-8 -*-

# Neahttadigisánit — online, inflectional dictionary
# Copyright (C) 2013–2017 University of Tromsø
# Copyright (C) 2018 University of Alberta
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


__all__ = [
    'create_app'
]

ADMINS = [
    'ryan.txanson+nds@gmail.com',
]

import sys, os
import logging

import yaml

from   flask                          import ( Flask
                                             , request
                                             , session
                                             )

# from   werkzeug.contrib.cache         import SimpleCache
from   config                         import Config
from   logging                        import getLogger

from   flask.ext.babel                 import Babel
from   flask.ext.limiter               import Limiter

from cache                            import cache

# Configure user_log
user_log = getLogger("user_log")
useLogFile = logging.FileHandler('user_log.txt')
user_log.addHandler(useLogFile)
user_log.setLevel("INFO")

cwd = lambda x: os.path.join(os.path.dirname(__file__), x)

def jinja_options_and_filters(app):

    from filters import register_filters

    app = register_filters(app)
    app.jinja_env.line_statement_prefix = '#'
    app.jinja_env.add_extension('jinja2.ext.i18n')
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    return app

def register_babel(app):

    babel = Babel(app)
    babel.init_app(app)

    app.babel = babel

    locales = app.config.locales_available
    ensure_translations_exist(locales)

    @app.before_request
    def append_session_globals():
        """ Add two-character and three-char session locale to global
        template contexts: session_locale, session_locale_long_iso.
        """

        from i18n.utils import iso_filter
        from itertools import izip_longest

        loc = get_locale()

        app.jinja_env.globals['session_locale'] = loc
        app.jinja_env.globals['zip'] = zip
        app.jinja_env.globals['izip_longest'] = izip_longest
        app.jinja_env.globals['session_locale_long_iso'] = iso_filter(loc)

    @app.babel.localeselector
    def get_locale():
        """ This function defines the behavior involved in selecting a
        locale. """

        # TODO: redo this method such that it receives the language from:
        #   1. language requested in the query string
        #   2. language associated with the session
        #   3. guess from Accept-Language header:
        # >>> request.accept_languages.best_match(['crk-Macr', 'crk-Cans', 'crk', 'en'])

        # Does the locale exist already?
        ses_lang = session.get('locale', None)
        forced_ses_lang = session.get('force_locale', None)

        if forced_ses_lang is not None:
            return forced_ses_lang
        elif ses_lang is not None:
            return ses_lang
        else:
            # Is there a default locale specified in config file?
            ses_lang = app.config.default_locale
            if not app.config.default_locale:
                # Guess the locale based on some magic that babel performs
                # on request headers.
                ses_lang = request.accept_languages.best_match(locales)
            # Append to session
            session.locale = ses_lang
            app.jinja_env.globals['session'] = session

        return ses_lang

    return app

def prepare_assets(app):
    """ Prepare asset registries, collect and combine them into several lists.

        Prepare template tags for collecting additional assets along the way.

    """

    # TODO: how to collect additional assets called in templates?

    import socket

    real_hostname = socket.gethostname()

    prod_hosts = [
        'gtweb.uit.no',
        'gtlab.uit.no',
        'gtoahpa.uit.no'
    ]

    if real_hostname in prod_hosts:
        dev = False
    else:
        dev = True

    js_dev_assets = []
    css_dev_assets = []

    if dev:
        print 'Including dev assets...'
        js_dev_assets = [
            'js/test_palette.js',
        ]
        css_dev_assets = [
            'css/test_palette.css',
        ]

    from flask.ext.assets import Environment, Bundle

    assets = Environment(app)
    app.assets = assets

    # assumes you've npm install uglify
    if not os.path.exists('./node_modules/uglify-js/bin/uglifyjs'):
        print >> sys.stderr, "Couldn't find uglify js: `npm install uglify-js`"
        sys.exit(1)

    app.assets.config['UGLIFYJS_BIN'] = './node_modules/uglify-js/bin/uglifyjs'
    app.assets.init_app(app)

    proj_css = []
    if app.config.has_project_css:
        proj_css.append(app.config.has_project_css.replace('static/', ''))

    # assets
    app.assets.main_js_assets = [
        'js/DSt.js',
        'js/bootstrap-collapse.js',
        'js/bootstrap-dropdown.js',
        'js/bootstrap-tooltip.js',
        'js/standalone-app.js',
        'js/bootstrap-typeahead-fork.js',
        'js/base.js',
        'js/index.js',
        'js/detail.js',
        'js/audio_links.js',
        # TODO: underscore? angular? async_paradigms? 
    ] + js_dev_assets

    app.assets.main_css_assets = [
        'css/bootstrap.css',
        'css/bootstrap-responsive.css',
        'css/base.css',
        'css/detail.css',
        'css/about.css',
    ] + proj_css + css_dev_assets

    app.assets.t_css_assets = [
        "bootstra.386/css/bootstrap.css",
        "bootstra.386/css/bootstrap-responsive.css",
        "css/text-tv-base.css",
    ] + proj_css

    app.assets.t_js_assets = [
        "bootstra.386/js/jquery.js",
        "bootstra.386/js/bootstrap-386.js",
    ]

    # mobile nav
    app.assets.nav_menu_css = [
        'navmenu/css/normalize.css',
        'navmenu/css/icons.css',
        'navmenu/css/component.css',
    ]

    # for footer
    app.assets.nav_menu_js = [
        'navmenu/js/modernizr.custom.js',
        'navmenu/js/classie.js',
        'navmenu/js/mlpushmenu.js',
        'navmenu/js/mobile_nav_init.js',
    ]

    app.assets.prepared = False

    # TODO: register separate asset path for inclusion of navmenu stuff
    # TODO: register separate asset path for texttv

    # TODO: this requires preprocessing templates once so the function
    # runs.

    return app


def register_assets(app):
    """ After all assets have been collected from parsed templates...

      * js/app-compiled-PROJNAME.js
      * js/app-t-compiled-PROJNAME.js
      * js/nav-menu-compiled-PROJNAME.js

      * css/app-compiled-PROJNAME.css
      * css/app-t-compiled-PROJNAME.css
      * css/nav-menu-compiled-PROJNAME.css

    """
    from flask.ext.assets import Environment, Bundle

    # TODO: register output including proj name

    # app.config['ASSETS_DEBUG'] = True

    js_filters = "uglifyjs"
    css_filters = "cssmin"

    PROJ = app.config.short_name

    main_js = Bundle(*app.assets.main_js_assets, filters=js_filters, output="js/app-compiled-%s.js" % PROJ)
    main_css = Bundle(*app.assets.main_css_assets, filters=css_filters, output="css/app-compiled-%s.css" % PROJ)
    app.assets.register('main_js', main_js)
    app.assets.register('main_css', main_css)

    main_t_js = Bundle(*app.assets.t_js_assets, filters=js_filters, output="js/app-t-compiled-%s.js" % PROJ)
    main_t_css = Bundle(*app.assets.t_css_assets, filters=css_filters, output="css/app-t-compiled-%s.css" % PROJ)
    app.assets.register('main_t_js', main_t_js)
    app.assets.register('main_t_css', main_t_css)

    nav_menu_js = Bundle(*app.assets.nav_menu_js, filters=js_filters, output="js/nav-menu-compiled-%s.js" % PROJ)
    nav_menu_css = Bundle(*app.assets.nav_menu_css, filters=css_filters, output="css/nav-menu-compiled-%s.css" % PROJ)
    app.assets.register('nav_menu_js', nav_menu_js)
    app.assets.register('nav_menu_css', nav_menu_css)

    # Trigger this to prevent stuff from being reregistered on each
    # view
    app.assets.prepared = True

    return app


def ensure_translations_exist(locales):
    """
    Ensures that the messages.mo file exists before running.

    The messages.mo files are created using:

        fab itwewina compile_strings

    :param locales: list of locales to check
    """
    # translations / <locale> / LC_MESSAGES / messages.{po,mo}
    j = os.path.join

    ensure_file_exists('translations', directory=True)

    for locale in locales:
        locale_dir = j('translations', locale)
        ensure_file_exists(locale_dir, directory=True)
        translation = j(locale_dir, 'LC_MESSAGES', 'messages.po')

        try:
            ensure_file_exists(translation)
        except EnvironmentError as e:
            print >> sys.stderr, "Could not find translation. Please see: fab itwewina extract_strings"
            raise e

        compiled_translation = j(locale_dir, 'LC_MESSAGES', 'messages.mo')

        try:
            ensure_file_exists(compiled_translation)
        except EnvironmentError as e:
            print >> sys.stderr, "Could not find compiled translation. Please run: fab itwewina compile_strings"
            raise e


def ensure_file_exists(path, directory=False):
    if not os.path.exists(path):
        raise EnvironmentError('Could not find file: %s' % path)

    if directory and not os.path.isdir(path):
        raise EnvironmentError('Not a directory: %s' % path)


def create_app():
    """ Set up the Flask app, cache, read app configuration file, and
    other things.
    """
    import conf as configs

    from morpholex import MorphoLexicon

    # TODO: this is called twice sometimes, slowdowns have been reduced,
    # but don't know why yet. Need to check. It only happens on the
    # first POST lookup, however...

    with open(os.environ['NDS_CONFIG'], 'r') as F:
        static_prefix = yaml.load(F).get('ApplicationSettings').get('fcgi_script_path', '')

    os.environ['PATH'] += os.pathsep + os.path.join(os.path.dirname(__file__), 'node_modules/.bin')

    app = Flask(__name__,
                static_url_path=static_prefix+'/static',
                template_folder=cwd('templates'))

    app = jinja_options_and_filters(app)
    app.production = False

    DEFAULT_CONF = os.path.join(os.path.dirname(__file__),
                                'configs')

    app.config['cache'] = cache
    # TODO: make sure this isn't being specified by an env variable
    app.config['NDS_CONFDIR'] = os.environ.get('NDS_CONFDIR', DEFAULT_CONF)
    app.config['jinja_env'] = app.jinja_env

    app.config = Config('.', defaults=app.config)
    app.config.from_envvar('NDS_CONFIG')
    app.config.overrides = configs.blueprint.load_language_overrides(app)
    app.config.prepare_lexica()
    app.config.add_optional_routes()

    os.environ['NDS_PATH_PREFIX'] = app.config.fcgi_script_path
    app.static_url_path = app.config.fcgi_script_path + app.static_url_path

    # Prepare assets before custom templates are read
    app = prepare_assets(app)

    # Register rate limiter
    limiter = Limiter(app, global_limits=["120/minute"])
    app.limiter = limiter
    app.config['APPLICATION_ROOT'] = app.config.fcgi_script_path

    # Register language specific config information
    import views
    app.register_blueprint(views.blueprint, url_prefix=app.config['APPLICATION_ROOT'])
    app.register_blueprint(configs.blueprint, url_prefix=app.config['APPLICATION_ROOT'])

    # Prepare cache
    cache_path = os.path.join(os.path.dirname(__file__), 'tmp/generator_cache/%s/' % app.config.short_name)
    cache.init_app(app, {'CACHE_TYPE': 'filesystem', 'CACHE_DIR': cache_path})

    app.cache = cache

    with app.app_context():
        app.cache.clear()

    app.config['cache'] = cache

    app.morpholexicon = MorphoLexicon(app.config)

    from paradigms import ParadigmConfig

    pc = ParadigmConfig(app)
    app.morpholexicon.paradigms = pc

    ## Read and prepare the templates

    from entry_template_filters import register_template_filters
    from entry_templates import TemplateConfig

    app = register_template_filters(app)
    app.lexicon_templates = TemplateConfig(app, debug=True)

    try:
        with open('secret_key.do.not.check.in', 'r') as F:
            key = F.readlines()[0].strip()
        app.config['SECRET_KEY'] = key
    except IOError:
        print >> sys.stderr, """
        You need to generate a secret key, and store it in a file with the
        following name: secret_key.do.not.check.in """
        sys.exit()

    app = register_babel(app)
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@gtweb.uit.no',
                                   ADMINS, 'NDS error')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    from logging import FileHandler
    from logging.handlers import SMTPHandler
    from socket import gethostname

    if app.debug:
        mail_handler = FileHandler('debug_email_log.txt')
    else:
        _admins = ADMINS + app.config.admins
        mail_handler = SMTPHandler('127.0.0.1',
                                   "server-error@%s" % gethostname(),
                                   ADMINS, "NDS-%s Failed" %  app.config.short_name)
        app.logger.smtp_handler = mail_handler

    # Templates are read, register the assets
    register_assets(app)

    mail_handler.setLevel(logging.ERROR)

    app.logger.addHandler(mail_handler)

    return app
