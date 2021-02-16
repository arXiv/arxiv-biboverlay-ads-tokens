"""Functions to access ADS's OAuth API"""
import uuid

from flask import current_app, Flask

from .date_utils import future_datetime


def init(app: Flask) -> None:
    """Init the service on a Flask app"""
    # HTTP client is provided by requests module; it handles
    # connection pooling here we just set some headers we always want
    # to use while sending a request
    app.client.headers.update({"Authorization": f'Bearer {app.config["API_TOKEN"]}'})


def verify_token(access_token: str) -> bool:
    """Checks if access_token still works"""
    url = "{}/{}".format(
        current_app.config["API_URL"], current_app.config["PROTECTED_ENDPOINT"]
    )
    r = current_app.client.get(url, headers={"Authorization": f"Bearer {access_token}"})
    return r.status_code == 200  # TODO: handle refresh in the future


def create_client():
    """Registers new OAuths application with ADS API"""

    url = "{}/{}".format(
        current_app.config["API_URL"], current_app.config["BOOTSTRAP_ENDPOINT"]
    )

    id = str(uuid.uuid4())

    kwargs = {
        "name": "{}:{}".format(current_app.config["CLIENT_NAME_PREFIX"], id),
        "scopes": " ".join(current_app.config["CLIENT_SCOPES"]),
        "redirect_uri": current_app.config["CLIENT_REDIRECT_URI"],
        "create_new": True,
        "ratelimit": current_app.config["CLIENT_RATELIMIT"],
    }

    expires = future_datetime(current_app.config["CLIENT_TOKEN_LIFETIME"])
    kwargs.update({"expires": expires.isoformat()})

    r = current_app.client.get(url, params=kwargs)

    if r.status_code == 200:
        ads_resp = r.json()
        # Don't let the browser client get the client_secret
        return {
            "token": ads_resp["access_token"],
#            "expire_in": ads_resp["expire_in"], # often expire_in is just the current time
            "expire_in": expires.isoformat(),
            "scopes": ads_resp["scopes"],
            "ratelimit": ads_resp["ratelimit"],
        }

    else:
        current_app.logger.error(
            "Unexpected response for %s (%s): %s", url, kwargs, r.text
        )
