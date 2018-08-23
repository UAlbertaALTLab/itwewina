# -*- coding: UTF-8 -*-
"""
Tools for compiling dictionaries automatically.

Fabric will automatically execute sets of commands remotely, and will
log in via SSH automatically to do this, assuming you have the proper
credentials.

To install Fabric, follow the instructions on the website:

    http://fabfile.org/

Then run the following to check that it works.

    fab --list

## Basic commands

In order to perform a task for a specific instance, you must specify a
few things.

    fab LOCATION DICT TASKS

So, to compile the lexicon locally for baakoeh, you would run:

    $ fab local baakoeh compile_dictionary

To do the same remotely, and restart the service, you would run:

    $ fab gtweb sanat compile_dictionary restart_service

With the latter, Fabric will connect via SSH and run commands remotely.
You may be asked for your SSH password.

"""

#    TODO: fab local start_project PROJNAME
#      - create infrastructure for new project
#        - configs/sample.config.yaml.in -> configs/PROJNAME.config.yaml.in
#        - templates/about.blank.html -> configs/about.PROJNAME.html
#        - grey box search notice template
#        - mkdir:
#
#    TODO: fab local add_language PROJNAME LANGISO
#      - create basic files for languages
#        - mkdir:
#            configs/language_specific_rules/tagsets/

import os
import signal
import socket
import sys
from config import yaml
from contextlib import contextmanager
from signal import SIGTERM, SIGUSR1

from fabric.api import cd, env, local, prefix, prompt, run, settings, task
from fabric.api import local as lrun
from fabric.colors import cyan, green, red, yellow
from fabric.contrib.console import confirm
from fabric.decorators import roles
from fabric.operations import sudo
from fabric.utils import abort

# Hosts that have an nds- init.d script
running_service = [
    'gtweb.uit.no',
    'gtlab.uit.no',
    'gtoahpa.uit.no',
    'sapir.artsrn.ualberta.ca',
    # sapir
    'arrl-web003',
]

no_fst_install = [
    'gtoahpa.uit.no',
]

location_restriction_notice = {

    'gtoahpa.uit.no': ['sanit', 'baakoeh'],
    'gtweb.uit.no':  ['dikaneisdi', 'erey', 'guusaaw', 'itwewina', 'kyv',
                      'muter', 'saan', 'saanih', 'sanat', 'sonad', 'vada',
                      'valks'],
    # sapir
    'arrl-web003':   ['gunaha', 'kidwinan', 'guusaaw', 'itwewina']
}


def get_projects():
    """ Find all existing projects which can be included as an env
    argument """
    import os

    conf_suffix = ".config.yaml.in"

    avail_projects = []
    for d, ds, fs in os.walk('.'):
        for f in fs:
            if f.endswith(conf_suffix):
                avail_projects.append(
                    f.replace(conf_suffix, '')
                )

    return avail_projects


def get_project():
    avail_projects = get_projects()

    proj_arg = [a for a in sys.argv if a in avail_projects]

    if len(proj_arg) > 0:
        proj_arg = proj_arg[0]
    else:
        proj_arg = False

    return proj_arg


def run_or_die(cmd, *args, **kwargs):
    """
    The same thing as env.run(), but automatically aborts if a command fails.
    """
    import sys
    result = env.run(cmd, *args, **kwargs)
    if result.return_code != 0:
        print(red("%r exited with status %d" % (cmd, result.return_code)))
        sys.exit(1)
    return result


@task(aliases=get_projects())
def set_proj():
    """ Set the project. This is aliased to whatever existing project
    names there are. ... Assuming no project name will be 'local' or
    'compile' """
    proj = get_project()

    env.clean_first = False

    if proj:
        env.current_dict = proj
    else:
        print >> sys.stderr, "This is not a valid project name."
        sys.exit()

    host = socket.gethostname()

    if host in running_service:
        has_restriction = sum(location_restriction_notice.values(), [])
        if proj in has_restriction:
            host_rest = location_restriction_notice.get(host, False)
            if host_rest:
                if proj not in host_rest:
                    print >> sys.stderr, red(
                        "%s is not on the current host <%s>." % (proj, host))
                    cont = raw_input(red('Continue anyway? [Y/N] \n'))
                    if cont != 'Y':
                        sys.exit()


@task
def local(*args, **kwargs):
    """ Run a command using the local environment.
    """
    from fabric.operations import local as lrun
    import os

    env.run = lrun
    env.hosts = ['localhost']

    gthome = os.environ.get('GTHOME')

    if gthome is None:
        sys.exit("GTHOME environment variable is not set.")

    env.path_base = os.getcwd()

    env.svn_path = gthome
    env.dict_path = os.path.join(env.path_base, 'dicts')
    env.neahtta_path = env.path_base
    env.i18n_path = os.path.join(env.path_base, 'translations')

    # Make command needs to include explicit path to file, because of
    # fabric.
    env.make_cmd = "make -C %s -f %s" % (env.dict_path, os.path.join(env.dict_path, 'Makefile'))
    env.remote_no_fst = False

    return env


env.no_svn_up = False
env.use_ssh_config = True
# env.key_filename = '~/.ssh/neahtta'

# set up environments
# Assume local unless otherwise noted
if ['local', 'gtweb', 'gtoahpa', 'sapir'] not in sys.argv:
    env = local(env)


env.real_hostname = socket.gethostname()


@task
def ship_it(tests='run'):
    """
    Tests and ships itwêwina on to Sapir.
    """
    if tests == 'run':
        integration_tests()
    # Fast-forward production's branch to development, and push!
    lrun('git fetch . development:sapir')
    lrun('git push origin sapir:sapir')
    deploy()


@task
def deploy():
    """
    Deploys itwêwina on Sapir.
    """

    require_sapir()
    require_itwewina()

    # This will ONLY run on Sapir
    no_svn_up()

    # TODO: nice to have: have the dictionaries changed?
    # TODO: nice to have: have the FSTs changed?

    with cd(env.itwewina_path):
        if git_branch() != 'sapir':
            abort(('Expected to be on the `sapir` branch; actually on `%s`. '
                   'Please log into Sapir and git checkout development') %
                  git_branch())

        if git_has_uncommited_changes():
            abort('Refusing to pull with uncommited changes. '
                  'Please commit, stash, or reset the changes as needed')

        run('git pull')
        with prefix('source venv/bin/activate'):
            # TODO: Check if deps have changed before doing this:
            run('pip install -r requirements.txt')


@task
def provision():
    """
    Provisions (setup for the first time) itwêwina on Sapir.

    This means cloning the repository, setting up the virtualenv, and patching
    the Babel locales.
    """

    require_sapir()
    require_itwewina()

    # Clone the repo
    clone_url = lrun('git remote get-url origin', capture=True)
    with cd(env.clone_path):
        run('git clone %s itwewina' % clone_url)

    assert env.itwewina_path.startswith(env.clone_path),\
        'did not find itwewina within the clone path'

    # Setup the virtualenv
    with cd(env.itwewina_path):
        run('virtualenv %s' % env.virtualenv_path)
        with prefix('source %s/bin/activate' % env.virtualenv_path):
            run('pip install -r requirements.txt')

    # Create dummy locales for 'crk'. Python-Babel crashes if these files aren't
    # there, but it doesn't actually use them for anything important ¯\_(ツ)_/¯
    locale_dir = os.path.join(
        env.virtualenv_path, 'lib', 'python2.7', 'site-packages', 'babel', 'localedata'
    )
    with cd(locale_dir):
        for locale in ('crk', 'crk_Macr', 'crk_Syll'):
            run('cp en_CA.dat %s.dat' % locale)


def require_itwewina():
    """
    Check that we're using deploying itwewina; abort otherwise.
    """
    if env.get('current_dict') != 'itwewina':
        abort('please run as `fab [server] itwewina [commands ...]`')


def require_sapir():
    """
    Check that we're using deploying on sapir; abort otherwise.
    """
    if not all('sapir' in hostname for hostname in env.hosts):
        print(env.hosts)
        abort('please run as `fab sapir [app] [commands ...]`')


def git_branch():
    """
    Returns the remote git branch.
    """
    branches = run('git branch --no-color').split('\n')
    for branch_line in branches:
        # Get rid of trailing newline
        branch_line = branch_line.rstrip()
        if branch_line.startswith('* '):
            return branch_line[2:]
    abort('could not detect current git branch in %r' % branches)


def git_has_uncommited_changes():
    """
    Return whether the remote git repository has uncommited changes.

    Ignores untracked files.
    """
    output = run('git status --porcelain --untracked-files=no')
    # If there's any output at all, that means there's untracked changes.
    return len(output) > 0


@task
def no_svn_up():
    """ Do not SVN up """
    env.no_svn_up = True


@task
def sapir():
    """
    Runs commands on Sapir.
    """
    _ = os.path.join
    env.run = run
    env.hosts = ['sapir.artsrn.ualberta.ca']
    env.path_base = '/home/ARTSRN/easantos'
    env.clone_path = env.path_base
    env.itwewina_path = _(env.path_base, 'itwewina', 'neahtta')
    env.virtualenv_path = _(env.itwewina_path, '.venv')

    env.svn_path = env.path_base + '/gtsvn'
    env.dict_path = env.path_base + '/neahtta/dicts'
    env.neahtta_path = env.path_base + '/neahtta'
    env.i18n_path = env.path_base + '/neahtta/translations'

    env.make_cmd = "make -C %s -f %s" % (env.dict_path, os.path.join(env.dict_path, 'Makefile'))
    env.remote_no_fst = False


@task
def gtweb():
    """ Run a command remotely on gtweb
    """
    env.run = run
    env.hosts = ['neahtta@gtweb.uit.no']
    env.path_base = '/home/neahtta'

    env.svn_path = env.path_base + '/gtsvn'
    env.dict_path = env.path_base + '/neahtta/dicts'
    env.neahtta_path = env.path_base + '/neahtta'
    env.i18n_path = env.path_base + '/neahtta/translations'

    env.make_cmd = "make -C %s -f %s" % (env.dict_path, os.path.join(env.dict_path, 'Makefile'))
    env.remote_no_fst = False


@task
def gtoahpa():
    """ Run a command remotely on gtoahpa
    """
    env.run = run
    env.hosts = ['neahtta@gtoahpa.uit.no']
    env.path_base = '/home/neahtta'

    env.svn_path = env.path_base + '/gtsvn'
    env.dict_path = env.path_base + '/neahtta/dicts'
    env.neahtta_path = env.path_base + '/neahtta'
    env.i18n_path = env.path_base + '/neahtta/translations'

    env.make_cmd = "make -C %s -f %s" % (env.dict_path, os.path.join(env.dict_path, 'Makefile'))
    env.remote_no_fst = True


@task
def update_configs():
    """ SVN up the config files """
    if env.no_svn_up:
        print(yellow("** skipping svn up **"))
        return

    with cd(env.neahtta_path):
        paths = [
            'configs/',
            'translations/',
        ]
        print(cyan("** svn up **"))
    for p in paths:
        _p = os.path.join(env.neahtta_path, p)
        with cd(_p):
            env.run('svn up ' + _p)


def read_config(proj):

    import yaml

    def gettext_yaml_wrapper(loader, node):
        from flask.ext.babel import lazy_gettext as _
        return node.value

    yaml.add_constructor('!gettext', gettext_yaml_wrapper)

    _path = 'configs/%s.config.yaml' % proj

    try:
        open(_path, 'r').read()
    except IOError:
        if env.real_hostname not in running_service:
            _path = 'configs/%s.config.yaml.in' % proj
            print(yellow("** Production config not found, using development (*.in)"))
        else:
            print(
                red("** Production config not found, and on a production server. Exiting."))
            sys.exit()

    with open(_path, 'r') as F:
        config = yaml.load(F)

    return config


@task
def update_gtsvn():
    """ SVN up the various ~/gtsvn/ directories """

    if env.no_svn_up:
        print(yellow("** skipping svn up **"))
        return

    with cd(env.svn_path):
        config = read_config(env.current_dict)
        svn_langs = [l.get('iso') for l in config.get('Languages')
                     if not l.get('variant', False)]
        svn_lang_paths = ['langs/%s' % l for l in svn_langs]
        # TODO: replace langs with specific list of langs from config
        # file
        paths = [
            'giella-core/',
            'words/',
            'art/dicts/',
        ] + svn_lang_paths
        print(cyan("** svn up **"))
    for p in paths:
        _p = os.path.join(env.svn_path, p)
        with cd(_p):
            try:
                svn_up_cmd = env.run('svn up ' + _p)
            except:
                abort(
                    red("\n* svn up failed in <%s>. Prehaps the tree is locked?" % _p) + '\n' +
                    red("  Correct this (maybe with `svn cleanup`) and rerun the command, or run with `no_svn_up`.")
                )

    # TODO: necessary to run autogen just in case?
    print(cyan("** Compiling giella-core **"))
    giella_core = os.path.join(env.svn_path, 'giella-core')
    with cd(giella_core):
        make_file = env.svn_path + '/giella-core/Makefile'
        make_ = "make -C %s -f %s" % (giella_core, make_file
                                      )
        result = env.run(make_)


@task
def restart_service(dictionary=False):
    """ Restarts the service. """

    if not dictionary:
        dictionary = env.current_dict

    fail = False

    # Not a big issue, but figure this out for local development.
    # if env.real_hostname not in running_service:
    #     print env.real_hostname
    #     print(green("** No need to restart, nds-<%s> not available on this host. **" % dictionary))
    #     return

    with cd(env.neahtta_path):
        _path = '%s.wsgi' % env.current_dict
        try:
            os.utime(_path, None)
            touched = True
        except Exception, e:
            touched = False
        if touched:
            print(cyan("** Restarting service for <%s> **" % dictionary))
            sys.exit()

        print(cyan("** Restarting service for <%s> **" % dictionary))
        restart = env.run("sudo service nds-%s restart" % dictionary)
        if not restart.failed:
            print(green("** <%s> Service has restarted successfully **" % dictionary))
        else:
            fail = True

    if fail:
        print(red("** something went wrong while restarting <%s> **" % dictionary))


@task
def compile_dictionary(dictionary=False, restart=False):
    """ Compile a dictionary project on the server, and restart the
    corresponding service.

        $ fab compile_dictionary:DICT
    """

    failed = False

    if not dictionary:
        dictionary = env.current_dict

    update_gtsvn()

    with cd(env.dict_path):
        env.run("svn up Makefile")

        result = env.run(env.make_cmd + " %s-lexica" % dictionary)

        if result.failed:
            failed = True

    if restart:
        restart_service(dictionary)

    if failed:
        print(red("** Something went wrong while compiling <%s> **" % dictionary))


@task
def compile(dictionary=False, restart=False):
    """ Compile a dictionary, fsts and lexica, on the server.

        $ fab compile:DICT

        NB: if the hostname is gtoahpa.uit.no (set in no_fst_install
        list above), only the lexicon will be compiled, FSTs will not be
        compiled or installed.
    """

    hup = False
    failed = False

    print(cyan("Executing on <%s>" % env.real_hostname))

    if not dictionary:
        dictionary = env.current_dict

    update_configs()
    update_gtsvn()

    with cd(env.dict_path) and settings(warn_only=True):
        if env.no_svn_up:
            print(yellow("** Skipping svn up of Makefile"))
        else:
            env.run("svn up Makefile")

        if env.real_hostname in no_fst_install or env.remote_no_fst:
            print(yellow("** Skip FST compile for gtoahpa **"))
            print(cyan("** Compiling lexicon for <%s> **" % dictionary))
            result = env.run(env.make_cmd + " %s-lexica" % dictionary)
            skip_fst = True
        else:
            skip_fst = False

            print(cyan("** Compiling lexicon and FSTs for <%s> **" % dictionary))

            if env.clean_first in ['Y', 'y']:
                clean_result = env.run(env.make_cmd + " %s-clean" % dictionary)

            result = env.run(env.make_cmd + " %s" % dictionary)

        if not result.succeeded:
            print(red("** There was some problem building the FSTs for this dictionary."))
            print(red("** Remove and check out individual language directories first?"))
            print(red("** WARNING: this will run `rm -rf $GTHOME/langs/LANG for each"))
            print(red("**          language in the current project. If you have"))
            print(red("**          ocal changes, they will be lost."))
            prompt('[Y/n]', key='clean_first')
            failed = True
            if env.clean_first in ['Y', 'y']:
                compile(dictionary, restart)

        if not skip_fst:
            print(cyan("** Installing FSTs for <%s> **" % dictionary))
            result = env.run(env.make_cmd + " %s-install" % dictionary)
            if result.failed:
                failed = True

    if restart:
        restart_service(dictionary)

    if failed:
        print(red("** Something went wrong while compiling <%s> **" % dictionary))
    else:
        print(cyan(
            "** <%s> FSTs and Lexicon compiled okay, should be safe to restart. **" % dictionary))


@task
def compile_fst(iso='x'):
    """ Compile a dictionary project on the server.

        $ fab compile_dictionary:DICT
    """

    hup = False

    dictionary = env.current_dict

    update_gtsvn()

    # TODO: need a make path to clean existing dictionary
    with cd(env.dict_path):
        # env.run("svn up Makefile")
        print(cyan("** Compiling FST for <%s> **" % iso))

        clear_tmp = env.run(env.make_cmd + " rm-%s" % iso)

        make_fsts = env.run(env.make_cmd + " %s" % iso)
        make_fsts = env.run(env.make_cmd + " %s-%s-install" %
                            (dictionary, iso))

        if make_fsts.failed:
            print(red("** Something went wrong while compiling <%s> **" % iso))
        else:
            print(cyan("** FST <%s> compiled **" % iso))


@task
def test_configuration():
    """ Test the configuration and check language files for errors. """

    _path = 'configs/%s.config.yaml' % env.current_dict

    try:
        open(_path, 'r').read()
    except IOError:
        if env.real_hostname not in running_service:
            _path = 'configs/%s.config.yaml.in' % env.current_dict
            print(yellow("** Production config not found, using development (*.in)"))
        else:
            print(
                red("** Production config not found, and on a production server. Exiting."))
            sys.exit()

    # TODO: this assumes virtualenv is enabled, need to explicitly enable
    _dict = env.current_dict
    with cd(env.dict_path):
        print(cyan("** Checking paths and testing XML for <%s> **" % _dict))

        cmd = "NDS_CONFIG=%s python manage.py chk-fst-paths" % _path
        test_cmd = env.run(cmd)
        if test_cmd.failed:
            print(red("** Something went wrong while testing <%s> **" % _dict))
        else:
            print(cyan("** Everything seems to work **"))


@task
def extract_strings():
    """ Extract all the translation strings to the template and *.po files. """

    print(cyan("** Extracting strings"))
    cmd = "pybabel extract -F babel.cfg -k gettext -o translations/messages.pot ."
    extract_cmd = env.run(cmd)
    if extract_cmd.failed:
        print(red("** Extraction failed, aborting."))
    else:
        print(cyan("** Extraction worked, updating files."))
        cmd = "pybabel update -i translations/messages.pot -d translations"
        update_cmd = env.run(cmd)
        if update_cmd.failed:
            print(red("** Update failed."))
        else:
            print(green("** Update worked. You may now check in or translate."))


@task
def update_strings():
    if env.no_svn_up:
        print(yellow("** skipping svn up **"))
        compile_strings()
        return

    with cd(env.i18n_path):
        env.run("svn up")

    compile_strings()


@task
def find_babel():
    import babel
    print babel

# TODO: handle babel.core.UnknownLocaleError: unknown locale 'hdn', with
# cleaner error message


@task
def compile_strings():
    """ Compile .po strings to .mo strings for use in the live server. """

    if hasattr(env, 'current_dict'):
        config = 'configs/%s.config.yaml.in' % env.current_dict
        with open(config, 'r') as F:
            _y = yaml.load(F.read())
            langs = _y.get('ApplicationSettings', {}).get('locales_available')

        for lang in langs:
            # run for each language
            cmd = "pybabel compile -d translations -l %s" % lang
            compile_cmd = env.run(cmd)
            if compile_cmd.failed:
                print(red("** Compilation failed, aborting."))
            else:
                print(green("** Compilation successful."))
    else:
        cmd = "pybabel compile -d translations"
        with settings(warn_only=True):
            compile_cmd = env.run(cmd, capture=True)
        if compile_cmd.failed:
            if 'babel.core.UnknownLocaleError' in compile_cmd.stderr:
                error_line = [l for l in compile_cmd.stderr.splitlines(
                ) if 'babel.core.UnknownLocaleError' in l]
                print(red("** String compilation failed, aborting:  ") +
                      cyan(''.join(error_line)))
                print("")
                print(yellow("  Either: "))
                print(yellow(
                    "   * rerun the command with the project name, i.e., `fab PROJNAME compile_strings`."))
                print(
                    yellow("   * Troubleshoot missing locale. (see Troubleshooting doc)"))
            else:
                print(compile_cmd.stderr)
                print(red("** Compilation failed, aborting."))
        else:
            print(compile_cmd.stdout)
            print(green("** Compilation successful."))


def where(iso):
    """ Searches Config and Config.in files for languages defined in
    Languages. Returns list of tuples.

        (config_path, short_name, iso)

    """

    configs = []
    for d, path, fs in os.walk('configs/'):
        for f in fs:
            if f.endswith(('.config.yaml.in', '.config.yaml')):
                configs.append(os.path.join(d, f))

    def test_lang(i):
        if isinstance(iso, list):
            if i.get('iso') in iso:
                return True
        else:
            if i.get('iso') == iso:
                return True
        return False

    locations = []
    for config in configs:
        with open(config, 'r') as F:
            _y = yaml.load(F.read())
            short_name = _y.get('ApplicationSettings', {}).get('short_name')
            langs = filter(test_lang, _y.get('Languages'))

            for l in langs:
                locations.append((config, short_name, l.get('iso')))

    return locations


@task
def where_is(iso='x'):
    """ Search *.in files for language ISOs to return projects that the
    language is present in. """

    if '+' in iso:
        iso = iso.split('+')

    locations = where(iso)

    for config, shortname, l in locations:
        print '%s : %s\t\t%s' % (l, shortname, config)


def search_running():
    """ Find all running services, return tuple of shortname and pidfile path
    """
    pidfile_suffix = "-pidfile.pid"

    pids = []
    for d, ds, fs in os.walk('.'):
        for f in fs:
            if f.endswith(pidfile_suffix):
                pids.append(
                    (f.replace(pidfile_suffix, ''), os.path.join(d, f))
                )

    return pids


@task
def find_running():
    hostname = env.real_hostname
    for shortname, pidfile in search_running():
        print "%s running on %s (%s)" % (
            green(shortname), yellow(hostname), pidfile)


@task
def restart_running():
    hostname = env.real_hostname
    find_running()

    with cd(env.neahtta_path):
        running_services = search_running()
        failures = []

        for s, pid in running_services:
            print(cyan("** Restarting service for <%s> **" % s))
            stop = env.run("sudo service nds-%s stop" % s)
            if not stop.failed:
                start = env.run("sudo service nds-%s start" % s)
                if not start.failed:
                    print(green("** <%s> Service has restarted successfully **" % s))
                else:
                    failures.append((s, pid))
            else:
                failures.append((s, pid))

    if len(failures) > 0:
        print(red("** something went wrong while restarting the following **"))
        for f in failures:
            print (s, pid)


@task
def runserver(send_sigusr1=False):
    """ Run the development server."""

    cmd = "pybabel compile -d translations"

    _path = 'configs/%s.config.yaml' % env.current_dict

    try:
        open(_path, 'r').read()
    except IOError:
        if env.real_hostname not in running_service:
            _path = 'configs/%s.config.yaml.in' % env.current_dict
            print(yellow("** Production config not found, using development (*.in)"))
        else:
            print(
                red("** Production config not found, and on a production server. Exiting."))
            sys.exit(-1)

    # TODO: request a signal
    # TODO: option to turn on or off reloader.

    cmd = ['NDS_CONFIG=%s' % _path,
           'python neahtta.py dev']
    if send_sigusr1:
        cmd.append('--send-sigusr1')

    # when instructed to send SIGUSR1, the parent of this process must know
    # about it.
    def forward_sigusr1(signum, _frame):
        assert signum == SIGUSR1
        os.kill(os.getppid(), SIGUSR1)

    with temporary_signal_handler(SIGUSR1, forward_sigusr1):
        print(green("** Starting development server."))
        run_cmd = env.run(' '.join(cmd))

    if run_cmd.failed:
        print(red("** Starting failed for some reason."))
        sys.exit(-1)


@task
def doctest():
    """ Run unit tests embedded in code
    """

    doctests = [
        'morphology/utils.py',
    ]

    doctest_cmd = 'python -m doctest -v %s'

    for _file in doctests:
        test_cmd = run_or_die(doctest_cmd % _file)


@task
def test_project():
    """ Test the configuration and check language files for errors. """

    yaml_path = 'configs/%s.config.yaml.in' % env.current_dict

    _dict = env.current_dict
    with cd(env.dict_path):

        print(cyan("** Running tests for %s" % _dict))

        cmd = "NDS_CONFIG=%s python -m unittest tests.yaml_tests" % (yaml_path)
        run_or_die(cmd)

# TODO: this is going away in favor of the better new thing: `test_project`, `doctest`, and `test`


@task
def unittests():
    """
    DEPRECATED: Test the configuration and check language files for errors.
    """

    yaml_path = 'configs/%s.config.yaml' % env.current_dict

    try:
        with open(yaml_path, 'r') as F:
            _y = yaml.load(F)
    except IOError:
        if env.real_hostname not in running_service:
            yaml_path = 'configs/%s.config.yaml.in' % env.current_dict
            print(yellow("** Production config not found, using development (*.in)"))
            with open(yaml_path, 'r') as F:
                _y = yaml.load(F)
        else:
            print(
                red("** Production config not found, and on a production server. Exiting."))
            sys.exit(-1)

    # TODO: this assumes virtualenv is enabled, need to explicitly enable
    _dict = env.current_dict
    with cd(env.dict_path):

        unittest_modules = _y.get('UnitTests', False)
        if not unittest_modules:
            print(red("** `UnitTests` not found in %s. Example:" % yaml_path))
            print >> sys.stderr, ""
            print >> sys.stderr, "    UnitTests:"
            print >> sys.stderr, '     - "tests.LANG1_lexicon"'
            print >> sys.stderr, '     - "tests.LANG2_lexicon"'
            print >> sys.stderr, ""
            sys.exit(-1)

        for unittest in unittest_modules:

            # unittest_file = unittest.replace('/', '.') + '.py'
            # try:
            #     open(os.path.join(env.path_base, unittest_file.replace('/', '.') + '.py'), 'r').read()
            # except:
            #     print(yellow("** File does not exist for %s" % unittest_file))
            #     continue

            print(cyan("** Running tests for %s" % unittest))

            cmd = "NDS_CONFIG=%s python -m unittest %s" % (yaml_path, unittest)
            test_cmd = run_or_die(cmd)

            if test_cmd.failed:
                print(red("** Something went wrong while testing <%s> **" % _dict))
                sys.exit(-1)


@task
def test():
    test_configuration()
    doctest()
    unittests()
    test_project()


@task
def integration_tests():
    """
    Run Cypress integration tests. This starts a development server on
    http://localhost:5000, and shuts it down when the tests are done.

    Integrations can ONLY be run locally.
    """
    from fabric.operations import local as lrun

    if env.hosts != ['localhost']:
        abort(red("** can only run integration tests on localhost"))

    with development_server():
        lrun("npm run cypress:run")


@contextmanager
def development_server():
    """
    Starts the developer server in another process.

    with development_server():
        # run tests and things here
    # server will terminate here.

    """
    # Basically, fork(), wait for a signal before continuing.
    # Then politely request to quit.

    pid = os.fork()
    if pid == 0:
        # Child process.
        # Make this process the new session leader/process group leader.
        # This means that killpg(pid) will terminate the server and all its
        # children.
        os.setsid()
        runserver(send_sigusr1=True)
        sys.exit()

    # Parent process.

    # Python 2 work around. Since there is non nonlocal keyword, we need to
    # mutate a variable in the closure in order for that to be reflected
    # outside of the inner function. In other words, we can't just say
    # child_ready = True inside wait_for_sigusr1, because a new variable is
    # created only in the signal handler :/
    child_ready = []

    def wait_for_sigusr1(signum, _stack_frame):
        assert signum == SIGUSR1
        child_ready.append(True)

    try:
        # Wait for the SIGUSR1...
        with temporary_signal_handler(SIGUSR1, wait_for_sigusr1):
            while not child_ready:
                signal.pause()

        # The server is ready!
        print(green("** development server ready!"))
        yield
    finally:
        # No matter what happens, *always* kill the child process group, lest they
        # become orphaned zombies.
        assert os.getsid(
            pid) == pid, "Child PID must be session leader, but it's not!"
        os.killpg(pid, SIGTERM)


@contextmanager
def temporary_signal_handler(signalnum, handler):
    """
    Sets a signal handler temporarily within a context manager. Usage:

    with temporary_signal_handler(SIG, handler_function):
        # do things
    # signal handler reset.
    """
    original_handler = signal.getsignal(signalnum)
    signal.signal(signalnum, handler)
    try:
        yield
    finally:
        # *Always* reset the orignal handler
        signal.signal(signalnum, original_handler)


def commit_gtweb_tag():
    """

    svn rm nds-stable-gtweb
    svn commit nds-stable-gtweb -m "preparing for update"
    https://gtsvn.uit.no/langtech/tags/apps/dicts/nds
    svn copy https://gtsvn.uit.no/langtech/trunk/apps/dicts/nds nds-stable-gtweb
    """


def get_status_code(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    import httplib
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None


@task
def test_running():

    hosts = [
        "kyv.oahpa.no",
        "saanih.oahpa.no",
        "valks.oahpa.no",
        "itwewina.oahpa.no",
        "muter.oahpa.no",
        "saanih.oahpa.no",
        "saan.oahpa.no",
        "sonad.oahpa.no",
        "guusaaw.oahpa.no",
        "vada.oahpa.no",
    ]

    for h in hosts:
        code = get_status_code(h)
        if code != 200:
            col = red
            msg = 'ERROR? ' + str(code) + ' '
        else:
            col = green
            msg = ''
        print(col(msg + h))

# vim: set ts=4 sw=4 sts=4 et:
