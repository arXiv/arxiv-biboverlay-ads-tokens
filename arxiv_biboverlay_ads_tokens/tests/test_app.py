
import unittest
from abovl import app, models
import os, json
from mock import mock, PropertyMock

class TestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.app = app.AbovlADSFlask('test', local_config=\
            {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///',
            'SQLALCHEMY_ECHO': False
            })
        models.Base.metadata.bind = self.app.db.session.get_bind()
        models.Base.metadata.create_all()
    
    
    def tearDown(self):
        self.app.close_app()
        unittest.TestCase.tearDown(self)
        models.Base.metadata.drop_all()


    def test_load(self):
        app = self.app
        with app.session_scope() as session:
            session.add(models.OAuthClient(token='foo'))
            session.commit()
        
        t = app.load_client('foo')
        assert t['id'] == 1
        assert t['token'] == 'foo'
        
    def test_create_client(self):
        data = {
          "access_token": "foobarbaz", 
          "username": "foo.bar@gmail.com", 
          "token_type": "Bearer", 
          "expire_in": "2050-01-01T00:00:00", 
          "refresh_token": "refreshfoo",
          "scopes": ["api", "execute-query", "store-query"],
          "client_id": "abcd",
          "client_secret": "clientsecret",
          "ratelimit": 1.0
        }
        r = PropertyMock()
        r.text = str(data)
        r.json = lambda: data
        r.status_code = 200
        with mock.patch.object(self.app.client, 'get', return_value=r) as client:
            c = self.app.create_client()
            self.assertDictContainsSubset({'username': u'foo.bar@gmail.com', 
                                              'scopes': 'api execute-query store-query', 
                                              'token': u'foobarbaz', 
                                              'client_id': u'abcd',  
                                              'client_secret': u'clientsecret', 
                                              'expire_in': '2050-01-01T00:00:00+00:00', 
                                              'id': 1, 
                                              'refresh_token': u'refreshfoo'}, c)


if __name__ == '__main__':
    unittest.main()