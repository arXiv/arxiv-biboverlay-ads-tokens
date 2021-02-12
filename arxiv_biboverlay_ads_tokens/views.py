from flask import current_app, request, Blueprint, jsonify, session

# from abovl.models import OAuthClient

bp = Blueprint("adstokens", __name__)


def set_api_token(client, session):
    """Save the token to the browser cookies via a Flask Session"""
    session["token"] = client["token"]
    session["expire_in"] = client["expire_in"]
    session["scopes"] = client["scopes"]
    session["ratelimit"] = client["ratelimit"]


def get_api_token(session):
    """Get the token from the browser coookies"""
    try:
        return {
            "access_token": session["token"],
            "expire_in": session["expire_in"],
            "scopes": session["scopes"],
            "ratelimit": session["ratelimit"],
        }
    except KeyError:
        return None


@bp.route("/token", methods=["GET"])
def token():
    """Will either create a new OAuth token
            - subordinate to the API_TOKEN
       Or retrieve stored token
           - based on a cookie
    """
    client = get_api_token(session)

    # verify it is still working
    if client is not None:
        current_app.logger.debug("Loaded client from cookie: %s", client)

        if not current_app.verify_token(client["token"]):
            session.clear()
            current_app.logger.info(
                "Deleted client (token no longer valid): %s", client
            )
            client = None

    # if all else failed, create a new application
    if client is None:
        client = current_app.ads.create_client()
        current_app.logger.info("Created a new OAuth Client/Token: {}", client)

    if not client:
        return jsonify({"error": "Error creating new OAuth application."}), 500

    set_api_token(client, session)

    # only return some info (don't want to expose client_secret in particular)
    return (
        jsonify(
            {
                "token": client["token"],
                "expire_in": client["expire_in"],
                "scopes": client["scopes"],
                "ratelimit": client["ratelimit"],
            }
        ),
        200,
    )


@bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ready"})
