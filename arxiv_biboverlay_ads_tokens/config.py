import os

# ##### Die if any of these are not configured from environment ##############
# Setting these from defaults could lead to configuration mistakes.

SECRET_KEY = os.environ['SECRET_KEY']  # must be set in environ
API_TOKEN = os.environ['API_TOKEN']  # must be set in environ

# ######## The following configs have resonable defaults #####################

# url to use for the oauth client
API_URL = os.environ.get('API_URL', 'https://api.adsabs.harvard.edu')

# ratio of the normal ratelimit that should be available to the
# newly created clients (e.g. .1 will give the new client 10% of
# normal ratelimits available at ADS). This setting may be important
# because each user account only has limited capacity. For example,
# if your user account has global ratelimit of 100, you can create
# 100 / 0.1 = 1000 sub-clients
CLIENT_RATELIMIT = float(os.environ.get('CLIENT_RATELIMIT', 0.02))


# it is easier if each token has a finite lifetime so that we can cycle unused
# tokens back to active users. here is the lifetime of each client token we
# lease, in seconds. If the base rate is 5k/day, we have a application rate of
# 40x, and there are 40k potential users per day with 30 abstracts allocated
# for viewing: on average, we need a token lifetime of
#   t_token = (5k * 40) / (40k * 30) * 24 hours = 4 hours
# If None, then the default will be accepted from the main app
CLIENT_TOKEN_LIFETIME = int(os.environ.get('CLIENT_TOKEN_LIFETIME', 4*60*60))


# on ADS side the OAuth application (when created)
# is given a name; which becomes unique identification
# (besides client id)
CLIENT_NAME_PREFIX = os.environ.get('CLIENT_NAME_PREFIX', 'BibOverlay')


# Here you can override oauth scopes that should be
# granted to the newly created application (once created
# those cannot be edited); if None then ADS will assign
# some default API scopes
CLIENT_SCOPES = os.environ.get('CLIENT_SCOPES', 'api')


# For OAuth dance (that is - to request permissions to access user's
# data, every OAuth application must provide an redirect URI) -
# clients will be redirected to that address. Put in here the real
# name of the server where this microservice is deployed. Must be
# running under HTTPS scheme; e.g. https://foobar.elasticbeanstalk.com
CLIENT_REDIRECT_URI = os.environ.get('CLIENT_REDIRECT_URI', None)


# ADS endopoint for veritying a token
PROTECTED_ENDPOINT = os.environ.get("PROTECTED_ENDPOINT",
                                    "v1/accounts/protected")

# ADS endpoint for getting a new application API token
BOOTSTRAP_ENDPOINT = os.environ.get("BOOTSTRAP_ENDPOINT",
                                    "v1/accounts/bootstrap")

# Domain name of server hosting bibex.js to use in Access-Control-Allow-Origin
CORS_DOMAIN = os.environ.get("CORS_DOMAIN", "https://arxiv.org")
