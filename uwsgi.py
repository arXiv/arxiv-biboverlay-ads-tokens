import abovl


def application(environ, start_response):
    app = abovl.create_app()
    return app(environ, start_response)

