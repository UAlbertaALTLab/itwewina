#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to GT-style XML lexica,
with preprocessing from morphological analysers implemented as FSTs.

This is the main file which handles initializing the app and providing
endpoint functionality.

"""
import os
import sys
from signal import SIGUSR1

from application import create_app

app = create_app()
config = app.config

if __name__ == "__main__":
    app.caching_enabled = True
    if 'development' or 'dev' in sys.argv:
        app.production = False
        print "!! Running in development mode"
    else:
        app.production = True
        print "!! Running in production mode"

    # Extra arguments to use the reloader, if specified.
    kwargs = {}
    kwargs.update(use_reloader='--reload' in sys.argv)
    if '--send-sigusr1' in sys.argv:
        os.kill(os.getppid(), SIGUSR1)

    app.run(debug=True, **kwargs)

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :
