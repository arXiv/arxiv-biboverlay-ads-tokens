"""
Database models
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from abovl import utils

Base = declarative_base()

class OAuthClient(Base):
    __tablename__ = 'oauth_client'
    id = sa.Column(sa.Integer, primary_key=True)
    token = sa.Column(sa.String(40))
    client_id = sa.Column(sa.String(40))
    client_secret = sa.Column(sa.String(80))
    refresh_token = sa.Column(sa.String(40))
    expire_in = sa.Column(utils.UTCDateTime)
    created = sa.Column(utils.UTCDateTime, default=utils.now)
    scopes = sa.Column(sa.Text())
    username = sa.Column(sa.String(512))
    ratelimit = sa.Column(sa.Float())
    
    def toJSON(self):
        """Returns value formatted as python dict. Oftentimes
        very useful for simple operations"""
        
        return {
            'id': self.id,
            'token': self.token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'scopes': self.scopes,
            'username': self.username,
            'ratelimit': self.ratelimit,
            'created': self.created and self.created.isoformat() or None,
            'expire_in': self.expire_in and self.expire_in.isoformat() or None
        }
