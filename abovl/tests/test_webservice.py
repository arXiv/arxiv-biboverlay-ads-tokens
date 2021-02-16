from flask.ext.testing import TestCase
from flask import url_for, request, session
import unittest
from abovl.models import Base
from abovl import app
import json
import os
from mock import mock

class TestServices(TestCase):
    '''Tests that each route is an http response'''

    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
               'SQLALCHEMY_DATABASE_URI': 'sqlite://',
               'SQLALCHEMY_ECHO': False,
               'TESTING': True,
               'PROPAGATE_EXCEPTIONS': True,
               'TRAP_BAD_REQUEST_ERRORS': True
            })
        Base.metadata.bind = a.db.session.get_bind()
        Base.metadata.create_all()
        return a


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        Base.metadata.drop_all()
        self.app.db = None
        
    def test_token(self):
        x = {u'access_token': u'FIt3VtPsPgCUt5cHGVFq8rCLgbT0R8ZCrgrfyZma',
                     u'anonymous': False,
                     u'client_id': u'XU9ZwJLCf34Ye7SlzKDyJLylDOIoi817Z7V3OgG3',
                     u'client_name': u'BB client',
                     u'client_secret': u'LqA08B1gK5yNG0EFcJqoJNNDFNwtLUYmvyFWQA37Dw6swnhlMKo5giTSw0oz',
                     u'expire_in': u'2500-01-01T00:00:00',
                     u'ratelimit': 0.1,
                     u'refresh_token': u'ElG2GALhdNGJSqsCXgebuRUfCn3aERzzciESIPO5',
                     u'scopes': [u'user'],
                     u'token_type': u'Bearer',
                     u'username': u'real_user@unittests'}
        response = mock.MagicMock()
        response.status_code = 200
        response.json = lambda: x
        with mock.patch.object(self.app.client, 'get', return_value=response) as getter:
            url = url_for('abovl.token')
            with self.client as c:
                assert 'token' not in session
                r = c.get(url)
                assert r.status_code == 200
                assert r.json['expire_in'] == u'2500-01-01T00:00:00+00:00'
                assert r.json['token'] == 'FIt3VtPsPgCUt5cHGVFq8rCLgbT0R8ZCrgrfyZma'
                assert session['token'] == r.json['token']
                
                t = r.json['token']
                
                # trying to access with the same cookie should give us the same client
                r = c.get(url)
                assert r.status_code == 200
                assert session['token'] == t
                r.json['token'] == t
                
                # now clear the cookies
                x['access_token'] = 'new value'
                c.cookie_jar.clear()
                r = c.get(url)
                assert r.status_code == 200
                assert r.json['expire_in'] == u'2500-01-01T00:00:00+00:00'
                assert r.json['token'] == 'new value'
                assert session['token'] == r.json['token']
    
        
        
if __name__ == '__main__':
  unittest.main()
