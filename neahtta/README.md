Neahttadigisánit
================

This is programmer-directed information, for development. If curious about
linguist-oriented and maintainer documentation, see
[neahttadigisanit][nds_doc].

  [nds_doc]: http://giellatekno.uit.no/doc/dicts/neahttadigisanit.html

Neahttadigisánit maintainer tasks
---------------------------------

Updating dictionaries & FSTs

    $ fab PROJECT compile

Updating just the lexicon

    $ fab PROJECT compile_dictionary

Updating translation strings

    $ fab PROJECT compile_strings

Testing configuration (run before restart, always)

    $ fab PROJECT test_configuration

Restarting services

    $ fab PROJECT restart_service

Find a language

    $ fab where_is:ISO


Overview
--------

A service using the [Flask][1] framework to serve up dictionary entries
using XML lexica and morphological analyzer services. Returns data in
JSON, and some HTML.

 [1]: http://flask.pocoo.org/

For more information on package dependencies, see `requirements.txt`.

## Installing

You need:

  - Python 2.7.12, with Python virtualenv
  - [Node.JS][]
  - [HFST](https://github.com/hfst/hfst/wiki/Download-And-Install)


### Python

**Make sure you're in `neahtta/`!**

Use [virtualenv][venv] to create a **Python 2.7** environment with requirements.txt.
The virtualenv could really go anywhere, but a common convention is to save it
in the local directory so that you always know where it is.

    virtualenv --python=$(which python2.7) .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Additional dependencies that you may need while developing NDS/itwêwina are in
`requirements_dev.txt`:

    pip install -r requirements_dev.txt

If more requirements become necessary, be sure to update the file and check it
in.

    pip freeze > requirements.txt

Update [Babel][]'s locale data. Babel probably will not have locales
created for 'crk' or its written variants. On Sapir, existing locales are
located here:

    /srv/apps/nds/babel_locales/crk.dat
    /srv/apps/nds/babel_locales/crk_Macr.dat
    /srv/apps/nds/babel_locales/crk_Syll.dat

As a sloppy workaround or if you don't have access to these, you can copy the
locales for `en_CA.bin`, located in your virtualenv:

    .venv/lib/python2.7/site-packages/babel/locale-data/en_CA.dat

Copy `en_CA.bin` like so:

    cp .venv/lib/python2.7/site-packages/babel/locale-data/{en_CA,crk}.dat
    cp .venv/lib/python2.7/site-packages/babel/locale-data/{en_CA,crk_Macr}.dat
    cp .venv/lib/python2.7/site-packages/babel/locale-data/{en_CA,crk_Syll}.dat

[Babel]: http://babel.pocoo.org/en/latest/index.html
[venv]: http://www.virtualenv.org/

### Node.JS

Install [Node.JS], however is most convenient for your system.

Now, install neahtta's additional dependencies:

    npm install

[Node.JS]: https://nodejs.org


### HFST

[Download HFST](https://github.com/hfst/hfst/wiki/Download-And-Install)
for your platform and install it.

#### How I installed it on macOS

I happen to have [Homebrew][brew] installed, so my `/usr/local` directory is
available for me to install things.

I downloaded [HFST 3.15.0](hfst-3.15.0+g3693~1b601689.tar.bz2), and
extracted it. I created the following directory:

Homebrew operates by installing entire software distributions in
`/usr/local/Cellar` in the format of `<software package>/<version>`.
So I created the directory cooresponding to HFST 3.15.0:

    mkdir -p /usr/local/Cellar/hfst/3.15.0

I then moved the directories `bin/`, `include/`, `lib/`, and `share/`
to said directory:

    mv bin include lib share /usr/local/Cellar/hfst/3.15.0

Now brew can manage symbolic links for us! Tell brew to link the latest
version of hfst:

    brew link hfst

[brew]: https://brew.sh/

Now you can test HFST:

    hash hfst-optimized-lookup
    echo "wapamew" | hfst-optimized-lookup -q analyser-gt-desc.omnivorous.hfstol


### Generating the secret key/token

The secret key is required for session storage in Flask.

To generate `secret_key.do.not.check.in`, use a cryptographically secure random
number generator. You can use the included script that will do this for you:

    python generate_key.py > secret_key.do.not.check.in


## The FSTs and the dictionaries

Make sure you copy the latest FSTs and dictionaries to the appropriate places.

What I do is copy all the dictionaries (XML files) from the server's copy of
itwêwina to my local copy:

    scp sapir.artsrn.ualberta.ca:/data/exps/itwewina/neahtta/dicts/*.xml dicts/

As for the FSTs, ask Antti (or me, Eddie) where the latest FSTs are, and copy
them somewhere accessible. On **Sapir**, this is

    /opt/smi/crk/bin/

You will need configure this directory in `configs/itwewina.config.yml`.

## Configuration

Copy `configs/itwewina.config.yaml.in` to `configs/itwewina.config.yaml`:

    cp configs/itwewina.config.yaml.in configs/itwewina.config.yaml

Edit settings in `configs/itwewina.config.yaml` as necessary. You will
probably want to change the FST paths (under `Morphology`), as well as
`recordings_endpoint`.

## Running the development server

Activate the virtualenv, then:

    fab itwewina runserver

Replace "itwewina" with the specific instance you need.


After waiting to see ` * Running on http://127.0.0.1:5000/`, you should
be able to access itwêwina at <http://localhost:5000/itwewina/>.


## Testing

This project uses [cypress.io][] for in-browser (integration) tests.

If you just want to run the tests, do the following:

    fab itwewina integration_tests

If you are developing new tests or features, do the following:

First, start the development server (see above). It should be accessible at
<http://localhost:5000/itwewina/>.

Assuming you already ran `npm install`, you should be able to run the UI tests
with the following command:

    npm test

**Note**: You probably need an up-to-date browser for this to work. On my
machine, this starts up a new Google Chrome 67 window and does all its testing
in there.

If you want to write tests interactively, use Cypress's dashboard:

    npm run cypress:open

For help with writing new tests, follow the [Cypress test writing
guide][cypress-guide].

[cypress.io]: https://www.cypress.io/
[cypress-guide]: https://docs.cypress.io/guides/getting-started/writing-your-first-test.html


## Deployment

Always merge code you want to deploy into the `development` branch.
Then use the following command:

    fab sapir itwewina ship_it

This runs the integration tests (see [Testing]). Once the test pass,
this updates the `sapir` branch to be up-to-date with development, and the
pushes the newly updated branch to GitHub. Then it pulls the changes on Sapir,
including installing any new requirements and restarts the `mod_wsgi` server.

If you just want to pull the latest changes from the `sapir` branch, you can use
this instead:

    fab sapir itwewina deploy

The code runs within [mod_wsgi].

[mod_wsgi]: http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/

Copy `itwewina.wsgi.template` to `itwewina.wsgi` and customize it as required,
following the documentation for both Flask and [mod_wsgi].


## Loose documentation

I wrote this documentation as I was setting up the new deployment of itwêwina on
Sapir. It is not very well edited :/

> Okay so you need to have the FSTs in a readable place.
>
> Probably set them to 444 permissions (all read permissions).
> The directory is 774 (list directory and write new files) -- gotta let that webserver process create temp
> files if it wants to.
>
> Then you need to have the dictionaries in the right place. I am doing
> this.
>
> OH, and you need to generate the translations :/
>
>     fab itwewina compile_strings
>
> You need node.js...
>
>     npm install
>
> GENERATE A SECRET KEY:
>
>     python ./generate_key.py > secret_key.do.not.check.in
>
> Setup the WSGI config:
>
> In general, follow:
>
> http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/
>
> But here's the config we have:
>
> Part of /etc/apache2/sites-available/000-default.conf:
>
>     WSGIDaemonProcess itwewina user=neahtta group=www-data threads=3
>     WSGIScriptAlias /itwewina /data/exps/itwewina/neahtta/itwewina.wsgi/itwewina
>     WSGIScriptReloading On
>
>     <Directory /data/exps/itwewina/neahtta>
>         WSGIProcessGroup itwewina
>         WSGIApplicationGroup %{GLOBAL}
>         Require all granted
>     </Directory>
>
> ---
>
> Finally, you're able to
>
>    fab itwewina runserver



### Lexical and linguistic dependencies to check

You should have the dictionaries in `/dict` and models in `/opt/smi/{lang}/src`
(where `{lang}` is a language ISO code).

 * svn up main/words/dicts/
 * svn up main/gt/
 * svn up main/langs

#### Makefile

The Makefile in `neahtta/dicts/` can be used to generate dictionary XML files,
and also to compile and manage the installation of FSTs and other morphologies.

See `make help` for more information.

## Developing

> 👇 this stuff was written a long time ago, and I don't know how much is
> relevant anymore :/

### Module-specific documentation.

For Python-module specific documentation, see the docstrings available in the
individual Python files. A short overview follows:

 * `neahtta.py` - initialization of Flask app, endpoints.
 * `config.py` and `configs/` - app configuration, yaml parsing, and yaml files
 * `configs/language_specific_rules` - directory for storing language-specific
   display, morphology and lexicon overrides.
 * `configs/language_names.py` - ISO names and 2-char -> 3-char definitions
 * `translations/` - i18n/i10n/localization details and .po files.
 * `lexicon/` - XML parsing
 * `morphology/` - FST parsing, lemmatization modules
 * `morpholex/` - Thing that ties these two together
 * `static/` - js, css, img, etc.
 * `templates/` - jinja2 templates for endpoints.
 * `dicts/` - path where XML files are typically stored

### XML format

See <https://github.com/UAlbertaALTLab/itwewina/blob/development/docs/xml-dictionary.md>
