import os

# variables which should be supplied by the environment (contain secrets)
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:///testdb.sqlite')

# The API_TOKEN from the people at ADS.
# Fail if this isn't set in the environ
API_TOKEN = os.environ.get("API_TOKEN")

SECRET_KEY = os.environ.get("SECRET_KEY")

# url to use for the oauth client
API_URL = 'https://api.adsabs.harvard.edu'

# ratio of the normal ratelimit that should be available to the
# newly created clients (e.g. .1 will give the new client 10% of
# normal ratelimits available at ADS). This setting may be important
# because each user account only has limited capacity. For example,
# if your user account has global ratelimit of 100, you can create
# 100 / 0.1 = 1000 sub-clients
CLIENT_RATELIMIT = 0.02


# it is easier if each token has a finite lifetime so that we can cycle unused
# tokens back to active users. here is the lifetime of each client token we
# lease, in seconds. If the base rate is 5k/day, we have a application rate of
# 40x, and there are 40k potential users per day with 30 abstracts allocated
# for viewing: on average, we need a token lifetime of
#   t_token = (5k * 40) / (40k * 30) * 24 hours = 4 hours
# If None, then the default will be accepted from the main app
CLIENT_TOKEN_LIFETIME = 4*60*60


# on ADS side the OAuth application (when created)
# is given a name; which becomes unique identification
# (besides client id)
CLIENT_NAME_PREFIX = 'BibOverlay'


# Here you can override oauth scopes that should be
# granted to the newly created application (once created
# those cannot be edited); if None then ADS will assign
# some default API scopes
CLIENT_SCOPES = 'api'


# For OAuth dance (that is - to request permissions to access user's
# data, every OAuth application must provide an redirect URI) -
# clients will be redirected to that address. Put in here the real
# name of the server where this microservice is deployed. Must be
# running under HTTPS scheme; e.g. https://foobar.elasticbeanstalk.com
CLIENT_REDIRECT_URI = None


# Sessions are used to store data on the server side; as a more safe
# alternative to saving data (oauth token) in a client cookie
SESSION_TYPE = 'sqlalchemy'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLAlchemy does not seem to respect pool or max_overflow in a
# resonable manner. Ex with 4 processes and pool=1 overflow=8 I'm
# seeing 80 connections to mysql when I'd expect 36.  uWsgi restart of
# workers will close all connections held by that worker so setting
# uwsgi max-worker-lifetime to a low value (around 10 or 15 sec) is a
# way to work around this problem. Hopefully it is fixed in newer
# versions.
#SQLALCHEMY_POOL_SIZE = 1
#SQLALCHEMY_MAX_OVERFLOW = 1

# By default SQLAlchemy keeps connections around forever
# Invalidate them after a time. This barely seems to work.
#SQLALCHEMY_POOL_RECYCLE = 1
