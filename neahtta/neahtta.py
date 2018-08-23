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

if __name__ == "__main__":
    app.caching_enabled = True

    if 'development' or 'dev' in sys.argv:
        app.production = False
        print "!! Running in development mode"
    else:
        app.production = True
        print "!! Running in production mode"

    # Sometimes, the app that started the server will want to know when
    # it's ready to take requests. For example, when running the
    # integration tests, we'd like to start the server, wait for it to
    # be ready, then issue HTTP requests to test the service.
    #
    # SIGUSR1 is how we indicate that this process is ready to start
    # taking requests. If the parent process requests
    # (e.g., the fabfile), we'll send SIGUSR1 back to the parent to let
    # it know that initialization is pretty much over, and it can start
    # issuing HTTP requests.
    #
    # NOTE: There is a slight race condition here in that issuing the
    # signal could lead to a context switch back to the parent process,
    # that could then open a socket immediately and attempt to connect
    # to this server before app.run() starts listen()ing.  In practice,
    # this has never happened to me, because the integration testing
    # framework itself needs to initialize, and takes long enough that
    # app.run() has long started listen()ing before it makes its first
    # HTTP request.
    if '--send-sigusr1' in sys.argv:
        os.kill(os.getppid(), SIGUSR1)

    app.run(debug=True,
            use_reloader='--reload' in sys.argv)

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :
