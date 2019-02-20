# -*- coding: utf-8 -*-
import os
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.debug import DebuggedApplication

import abovl.app
import bootstrap

def turn_on_debug(app):
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    app.debug = True


def application(environ, start_response):
    app = abovl.app.create_app()
    bootstrap.bootstrap(app)

    print("MATT: checking debug")
    if os.environ.get('DEBUG'):
        turn_on_debug(app)
        print("DEBUG")

    return app(environ, start_response)

