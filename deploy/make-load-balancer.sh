#!/bin/bash
### Setting up the load balancer ###
set -ev

# from https://cloud.google.com/load-balancing/docs/https/ext-https-lb-simple#load-balancer
# Modified slightly for wsgi port at $PORT

# reserve an IP address
# gcloud compute addresses create lb-ipv4-services-arxiv-org \
#        --project=$PROJ \
#        --ip-version=IPV4 \
#        --global
       
# Make health check for instance group

gcloud compute health-checks create http $NAME-health-check \
       --check-interval=20s \
       --timeout=10s \
       --unhealthy-threshold=3 \
       --request-path="/bibex/ads/status" \
       --port=$PORT
# Flask will 404 if SERVER_NAME is set and the request deosn't match SERVER_NAME
# But you can just not set SERVER_NAME and it will be fine.
#--host=something.arxiv.org \

# Create a backend service
gcloud compute backend-services create $NAME-backend-service \
       --project=$PROJ \
       --port-name=http \
       --health-checks=$NAME-health-check \
       --global

# Add backend as a link to biboverlay-token instance group
gcloud compute backend-services add-backend $NAME-backend-service \
       --project=$PROJ \
       --instance-group=$MIG \
       --instance-group-zone=$ZONE \
       --balancing-mode=RATE \
       --max-rate=200 \
       --global

# Create a URL map to route incoming requests to the backend service:
# This becomes the name of the load balancer in the GCP UI
gcloud compute url-maps create service-lb \
       --project=$PROJ \
       --default-service $NAME-backend-service

# Create a target HTTP(S) proxy to route requests to your URL map.
# The proxy is the portion of the load balancer that holds the SSL
# certificate.
gcloud compute target-https-proxies create $NAME-target-https-proxy \
       --project=$PROJ \
       --ssl-certificates=services-arxiv-org-ssl-cert \
       --url-map=service-lb

# Create a global forwarding rule to route incoming requests to the proxy.
gcloud compute forwarding-rules create $NAME-forwarding-rule \
       --project=$PROJ \
       --address=lb-ipv4-services-arxiv-org \
       --target-https-proxy=$NAME-target-https-proxy \
       --global \
       --ports=443



MAPPINGS="/bibex/ads/*=$NAME-backend-service"
gcloud compute url-maps add-path-matcher service-lb \
       --path-matcher-name=$NAME-paths \
       --delete-orphaned-path-matcher \
       --default-service=$NAME-backend-service \
       --new-hosts=$HOST \
       --path-rules=$MAPPINGS


# If the load balancer doesn't work after about 60 sec.
# to to the GCP UI, go to load balancer, go to the load balancer that
# this script creates, click edit, click finalize and then save (or update)

