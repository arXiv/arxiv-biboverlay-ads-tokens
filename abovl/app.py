#!/usr/bin/python
# -*- coding: utf-8 -*-

from adsmutils import ADSFlask
from abovl.views import bp
from abovl.models import OAuthClient
from flask.ext.session import Session

def create_app(**config):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    app = AbovlADSFlask('arxiv_biboverlay', local_config=config)
    app.url_map.strict_slashes = False    
    app.register_blueprint(bp)
    
    sess = Session()
    sess.init_app(app) 
    
    return app


class AbovlADSFlask(ADSFlask):
    
    def __init__(self, *args, **kwargs):
        ADSFlask.__init__(self, *args, **kwargs)
        
        # HTTP client is provided by requests module; it handles connection pooling
        # here we just set some headers we always want to use while sending a request
        self.client.headers.update({'Authorization': 'Bearer {}'.format(self.config.get("API_TOKEN", ''))})
        
    
    def load_client(self, token):
        """Loads client entry from the database."""
        
        with self.session_scope() as session:
            t = session.query(OAuthClient).filter_by(token=token).first()
            if t:
                return t.toJSON()

    def delete_client(self, cid):
        with self.session_scope() as session:
            session.query(OAuthClient).filter_by(id=cid).delete()
            session.commit()
            
    
    def verify_token(self, token):
        url = '{}/{}'.format(self.config.get('API_URL'), self.config.get('PROTECTED_ENDPOINT', 'v1/accounts/protected'))
        r = self.client.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
        return r.status_code == 200 #TODO: we could also handle refresh in the future
    
    
    def create_client(self):
        """Calls ADS api and gets a new OAuth application
            registered."""
        
        url = '{}/{}'.format(self.config.get('API_URL'), self.config.get('BOOTSTRAP_ENDPOINT', 'v1/accounts/bootstrap'))
        
        counter = 0
        with self.session_scope() as session:
            counter = session.query(OAuthClient).count() # or we could simply use UUID
            
        kwargs = {
            'name': '{}:{}'.format(self.config.get('CLIENT_NAME_PREFIX', 'OAuth application'), counter+1),
            'scopes': ' '.join(self.config.get('CLIENT_SCOPES', []) or []),
            'redirect_uri': self.config.get('CLIENT_REDIRECT_URI', None),
            'create_new': True,
            'ratelimit': self.config.get('CLIENT_RATELIMIT', 1.0)
        }
        
        r = self.client.get(url, params=kwargs)
        
        if r.status_code == 200:
            j = r.json()
            with self.session_scope() as session:
                c = OAuthClient(client_id=j['client_id'], client_secret=j['client_secret'],
                                token=j['access_token'], refresh_token=j['refresh_token'],
                                expire_in=j['expire_in'], scopes=' '.join(j['scopes'] or []),
                                username=j['username'], ratelimit=j['ratelimit'])
                session.add(c)
                session.commit()
                return c.toJSON()
        else:
            self.logger.error('Unexpected response for %s (%s): %s', url, kwargs, r.text)
