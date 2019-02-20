SQLALCHEMY_DATABASE_URI = 'sqlite:///testdb.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_TOKEN = 'this is a secret api token!'
API_URL = 'https://api.adsabs.harvard.edu'

# ratio of the normal ratelimit that should be available to the
# newly created clients (e.g. .1 will give the new client 10% of
# normal ratelimits available at ADS). This setting may be important
# because each user account only has limited capacity. For example,
# if your user account has global ratelimit of 100, you can create
# 100 / 0.1 = 1000 sub-clients
CLIENT_RATELIMIT = 0.1

# Flask key used to sign cookies and to salt db entries
SECRET_KEY = 'change me'

# on ADS side the OAuth application (when created)
# is given a name; which becomes unique identification
# (besides client id)
CLIENT_NAME_PREFIX = 'BibOverlay'


# Here you can override oauth scopes that should be
# granted to the newly created application (once created
# those cannot be edited); if None then ADS will assign
# some default API scopes
CLIENT_SCOPES = None


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
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = True

#SESSION_SQLALCHEMY_TABLE = 'sessions'
#app.config[SESSION_SQLALCHEMY] = db
