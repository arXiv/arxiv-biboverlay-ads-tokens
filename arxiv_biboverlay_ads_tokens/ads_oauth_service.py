from flask import current_app


def init(app):    
    # HTTP client is provided by requests module; it handles connection pooling
    # here we just set some headers we always want to use while sending a request
    app.client.headers.update({f'Authorization': 'Bearer {app.config["API_TOKEN"]}'})


def verify_token(access_token):
    """Checks if access_token still works"""
    url = "{}/{}".format(
        current_app.config["API_URL"],
        current_app.config["PROTECTED_ENDPOINT"]
    )
    r = current_app.client.get(url)
    return r.status_code == 200  # TODO: handle refresh in the future


def create_client():
    """Registers new OAuths application with ADS API"""

    url = "{}/{}".format(
        current_app.config["API_URL"],
        current_app.config["BOOTSTRAP_ENDPOINT"]
    )

    #TODO FIX THIS
    counter = 0
    # with self.session_scope() as session:
    #     counter = session.query(OAuthClient).count()  # or we could simply use UUID

    kwargs = {
        "name": "{}:{}".format(
            current_app.config["CLIENT_NAME_PREFIX"], counter + 1
        ),
        "scopes": " ".join(current_app.config["CLIENT_SCOPES"]),
        "redirect_uri": current_app.config["CLIENT_REDIRECT_URI"],
        "create_new": True,
        "ratelimit": current_app.config["CLIENT_RATELIMIT"],
    }

    #TODO fix expires
    # if current_app.config["CLIENT_TOKEN_LIFETIME"]:
    #     expires = future_datetime(current_app.config["CLIENT_TOKEN_LIFETIME"])
    #     kwargs.update({"expires": expires.isoformat()})

    r = current_app.client.get(url, params=kwargs)

    if r.status_code == 200:
        return r.json()
        # j = r.json()
        # with current_app.session_scope() as session:
        #     c = OAuthClient(
        #         client_id=j["client_id"],
        #         client_secret=j["client_secret"],
        #         token=j["access_token"],
        #         refresh_token=j["refresh_token"],
        #         expire_in=j["expire_in"],
        #         scopes=" ".join(j["scopes"] or []),
        #         username=j["username"],
        #         ratelimit=j["ratelimit"],
        #     )
        #     session.add(c)
        #     session.commit()
        #    return c.toJSON()
    else:
        current_app.logger.error("Unexpected response for %s (%s): %s", url, kwargs, r.text)
