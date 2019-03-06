# variables which should be supplied by the environment (contain secrets)
SQLALCHEMY_DATABASE_URI = 'sqlite:///testdb.sqlite'
API_TOKEN = 'this is a secret api token!'
SECRET_KEY = 'change me'

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
CLIENT_TOKEN_LIFETIME = 60*5 #4*60*60


# on ADS side the OAuth application (when created)
# is given a name; which becomes unique identification
# (besides client id)
CLIENT_NAME_PREFIX = 'BibOverlay'


# Here you can override oauth scopes that should be
# granted to the newly created application (once created
# those cannot be edited); if None then ADS will assign
# some default API scopes
CLIENT_SCOPES = 'api'


# For OAuth dance (that is - to request permissions to
# access user's data, every OAuth application must provide
# an redirect URI) - clients will be redirected to that 
# address. Put in here the real name of the server
# where this microservice is deployed. Must be running
# under HTTPS scheme; e.g. https://foobar.elasticbeanstalk.com
CLIENT_REDIRECT_URI = None


# Sessions are used to store data on the server side; as 
# a more safe alternative to saving data (oauth token) in 
# a client cookie
SESSION_TYPE = 'sqlalchemy'

# perhaps if performance problems:
#SQLALCHEMY_TRACK_MODIFICATIONS = False
