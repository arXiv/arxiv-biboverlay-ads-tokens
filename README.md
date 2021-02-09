[![Build Status](https://travis-ci.org/romanchyla/arxiv_biboverlay.svg)](https://travis-ci.org/romanchyla/arxiv_biboverlay)
[![Coverage Status](https://coveralls.io/repos/romanchyla/arxiv_biboverlay/badge.svg)](https://coveralls.io/r/romanchyla/arxiv_biboverlay)

# arxiv_biboverlay
Tiny microservice to help arxiv. It provides a bootstrap service to obtain 
OAuth token that are subordinate to the main Arxiv OAuth client.

## deployment:

    Run development server with:
    
    `API_KEY=1234_GET_ME_FROM_ADS  uwsgi --ini uwsgi.ini`

    or 
    
    `API_TOKEN=1234_GET_ME_FROM_ADS  python cors.py`
    
    To create tables in new database run flask with BOOTSTRAP_UWSGI=1.

## Usage:

    `curl somewhere.com/token`
    
    The output will contain a new OAuth token and a cookie will be set. 
    
    If the browser/client sends the same cookie with the next request, 
    the system will return the same token (after having verified it still
    works; if verification fails a new token will be created).
    
    Without the cookie, a new token will be created every time.
