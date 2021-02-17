export PROJ=arxiv-production
export NAME=biboverlay-tokens

export MIG="$NAME-mig"
export PORT=5000
export ZONE=us-east1-d
export HOST=services.arxiv.org

export SSL_CERT="services-arxiv-org-ssl-cert"

# This should not be set to latest so the instance tempalte is deterministic
# Builds from CI can just set the image URI during the MIG template command.
export IMAGE_URL="gcr.io/arxiv-production/biboverlay-tokens@sha256:982c8f4e4c748f9af8957aa006058726047e47c725847f55e72b12dd327fc134"
