
from flask import current_app, request, Blueprint, jsonify, session
#from abovl.models import OAuthClient

bp = Blueprint('abovl', __name__)



@bp.route('/token', methods=['GET'])
def token():
    """Will either create a new OAuth token
            - subordinate to the API_TOKEN
       Or retrieve stored token
           - based on a cookie
    """

    token = session.get('token', None)
    client = None
    
    if token:
        client = current_app.load_client(token)

    # verify it is still working
    if client is not None:
        current_app.logger.debug('Loaded client based on a cookie: %s', client)
        
        if not current_app.verify_token(client['token']):
            current_app.delete_client(client['id'])
            current_app.logger.info('Deleted client (token no longer valid): %s', client)
            client = None
        
    # if all else failed, create  a new application
    if client is None:
        client = current_app.create_client()
        current_app.logger.info('Created a new OAuth Client/Token: {}', client)

    if not client:
        return jsonify({'error': 'Error creating new OAuth application.'}), 500
    
    # set the coookie to be able to provide the same clients with the existing token
    session['token'] = client['token']
         
    # only return some info (don't want to expose client_secret in particular)
    return jsonify({'token': client['token'], 'expire_in': client['expire_in'], 
                    'scopes': client['scopes'], 'ratelimit': client['ratelimit']}), 200

@bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ready'})
