
from flask_session import Session
from flask import Flask

#from .views import bp
#from .models import OAuthClient
#from .utils import future_datetime


def create_app(test_config=None):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """
    app = Flask("biboverlay_ads_token_service")

    app.config.from_object('arxiv_biboverlay_ads_tokens.config')
    if test_config is not None:
        app.config.from_mapping(test_config)
        
    app.url_map.strict_slashes = False

    #app.register_blueprint(bp)
    @app.route('/token')
    def token():
        return f"Token!" + app.config.get("API_TOKEN") + " " + f"{app.config}" + "lskdjfskdj"
    
    sess = Session()
    sess.init_app(app)
    
    return app


# class ADSTokenFlask(flask):
    
#     def __init__(self, *args, **kwargs):
#         flask.__init__(self, *args, **kwargs)
        
#         # HTTP client is provided by requests module; it handles connection pooling
#         # here we just set some headers we always want to use while sending a request
#         self.client.headers.update({'Authorization': 'Bearer {}'.format(self.config.get("API_TOKEN", ''))})
        
    
#     def load_client(self, token):
#         """Loads client entry from the database."""
        
#         with self.session_scope() as session:
#             t = session.query(OAuthClient).filter_by(token=token).first()
#             if t:
#                 return t.toJSON()

#     def delete_client(self, cid):
#         with self.session_scope() as session:
#             session.query(OAuthClient).filter_by(id=cid).delete()
#             session.commit()
            
    
#     def verify_token(self, token):
#         url = '{}/{}'.format(self.config.get('API_URL'), self.config.get('PROTECTED_ENDPOINT', 'v1/accounts/protected'))
#         r = self.client.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
#         return r.status_code == 200 #TODO: we could also handle refresh in the future
    
    
#     def create_client(self):
#         """Calls ADS api and gets a new OAuth application
#             registered."""
        
#         url = '{}/{}'.format(self.config.get('API_URL'), self.config.get('BOOTSTRAP_ENDPOINT', 'v1/accounts/bootstrap'))
        
#         counter = 0
#         with self.session_scope() as session:
#             counter = session.query(OAuthClient).count() # or we could simply use UUID
            
#         kwargs = {
#             'name': '{}:{}'.format(self.config.get('CLIENT_NAME_PREFIX', 'OAuth application'), counter+1),
#             'scopes': ' '.join(self.config.get('CLIENT_SCOPES', []) or []),
#             'redirect_uri': self.config.get('CLIENT_REDIRECT_URI', None),
#             'create_new': True,
#             'ratelimit': self.config.get('CLIENT_RATELIMIT', 1.0)
#         }

#         if self.config.get('CLIENT_TOKEN_LIFETIME'):
#             expires = future_datetime(self.config.get('CLIENT_TOKEN_LIFETIME'))
#             kwargs.update({'expires': expires.isoformat()})

#         r = self.client.get(url, params=kwargs)
        
#         if r.status_code == 200:
#             j = r.json()
#             with self.session_scope() as session:
#                 c = OAuthClient(client_id=j['client_id'], client_secret=j['client_secret'],
#                                 token=j['access_token'], refresh_token=j['refresh_token'],
#                                 expire_in=j['expire_in'], scopes=' '.join(j['scopes'] or []),
#                                 username=j['username'], ratelimit=j['ratelimit'])
#                 session.add(c)
#                 session.commit()
#                 return c.toJSON()
#         else:
#             self.logger.error('Unexpected response for %s (%s): %s', url, kwargs, r.text)
