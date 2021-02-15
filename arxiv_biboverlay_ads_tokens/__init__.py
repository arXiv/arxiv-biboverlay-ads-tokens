import flask
import requests
from datetime import timedelta

from arxiv_biboverlay_ads_tokens import config
import arxiv_biboverlay_ads_tokens.ads_oauth_service as ads
from .views import bp


def create_app(test_config=None):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """
    app = flask.Flask("biboverlay_ads_token_service")

    app.config.from_object(config)
    if test_config is not None:
        app.config.from_mapping(test_config)

    app.permanent_session_lifetime = timedelta(
        seconds=app.config["CLIENT_TOKEN_LIFETIME"] + 1
    )
    app.url_map.strict_slashes = False

    app.register_blueprint(bp)

    # HTTP connection pool from ADS microservice utils - The maximum
    # number of retries each connection should attempt: this applies
    # only to failed DNS lookups, socket connections and connection
    # timeouts, never to requests where data has made it to the
    # server. By default, requests does not retry failed connections.
    # http://docs.python-requests.org/en/latest/api/?highlight=max_retries#requests.adapters.HTTPAdapter
    app.client = requests.Session()
    http_adapter = requests.adapters.HTTPAdapter(
        pool_connections=app.config.get("REQUESTS_POOL_CONNECTIONS", 10),
        pool_maxsize=app.config.get("REQUESTS_POOL_MAXSIZE", 1000),
        max_retries=app.config.get("REQUESTS_POOL_RETRIES", 3),
        pool_block=False,
    )
    app.client.mount(u"http://", http_adapter)

    app.ads = ads
    ads.init(app)

    return app
