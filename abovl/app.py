#!/usr/bin/python
# -*- coding: utf-8 -*-

from uuid import uuid4
from adsmutils import ADSFlask
from abovl.views import bp
from abovl.models import OAuthClient
from abovl.utils import future_datetime
from flask_session import Session
from retry import retry
from dateutil import tz

from datetime import datetime, timedelta
from adsmutils import get_date
utc_zone = tz.tzutc()

def create_app(**config):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    
    app = AbovlADSFlask('arxiv_biboverlay', local_config=config)
    app.config.from_pyfile("./config.py")
    app.url_map.strict_slashes = False
    app.register_blueprint(bp)
    
    sess = Session()
    sess.init_app(app) 
    
    return app


class AbovlADSFlask(ADSFlask):
    
    def __init__(self, *args, **kwargs):
        ADSFlask.__init__(self, *args, **kwargs)

        api_token=self.config.get("API_TOKEN") # API_TOKEN is needed, should be in env vars 

        # To avoid AttributeError: 'Request' object has no attribute 'is_xhr'
        self.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        
        # HTTP client is provided by requests module; it handles connection pooling
        # here we just set some headers we always want to use while sending a request
        self.client.headers.update({'Authorization': 'Bearer {}'.format(api_token)})


    @retry(tries=3, delay=1)
    def load_client(self, token):
        """Loads client entry from the database."""
        with self.session_scope() as session:
            t = session.query(OAuthClient).filter_by(token=token).first()
            if t:
                return t.toJSON()

    @retry(tries=3, delay=1)
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
    
        id = uuid4()
        kwargs = {
            'name': '{}:{}'.format(self.config.get('CLIENT_NAME_PREFIX', 'OAuth application'), id),
            'scopes': ' '.join(self.config.get('CLIENT_SCOPES', []) or []),
            'redirect_uri': self.config.get('CLIENT_REDIRECT_URI', None),
            'create_new': True,
            'ratelimit': self.config.get('CLIENT_RATELIMIT', 1.0)
        }

        if self.config.get('CLIENT_TOKEN_LIFETIME'):
            expires = future_datetime(self.config.get('CLIENT_TOKEN_LIFETIME'))
            kwargs.update({'expires': expires.isoformat()})

        r = self.client.get(url, params=kwargs)
    
        if r.status_code == 200:
            j = r.json()
            kwargs = {
                "client_id": j['client_id'],
                "client_secret": j['client_secret'],
                "token": j['access_token'],
                "refresh_token": j['refresh_token'],
                "scopes": ' '.join(j['scopes'] or []),
                "username": j['username'],
                "ratelimit": j['ratelimit'],
                "expire_in": get_date(j['expire_in']).astimezone(utc_zone),
                "created": datetime.utcnow().replace(tzinfo=utc_zone),
            }
            c = OAuthClient(**kwargs)
            try:
                self._write_client(c)
            except Exception as exx:
                self.logger.error('Could not save client to DB %s', exx)
                # Unable to save to db, just return the data from ADS
                return kwargs

            return kwargs
        else:
            self.logger.error('Unexpected response from ADS for %s (%s): %s', url, kwargs, r.text)


    @retry(tries=3, delay=1)
    def _write_client(self, client):
        with self.session_scope() as session:
            client.toJSON()
            session.add(client)
            session.commit()
