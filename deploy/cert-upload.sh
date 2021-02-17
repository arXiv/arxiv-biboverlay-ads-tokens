#!/bin/bash
### upload SSL cert to GCP ###
set -veu

echo "Uploading $SSL_CERT for project $PROJ"

if [ ! -e "services.arxiv.org.key" ] 
then
  echo "The services.arxiv.org.key is required. Get it from lastpass."
  exit 1
fi
if [ ! -e "services.arxiv.org.cer" ] 
then
  echo "The services.arxiv.org.cer is required. Get it from lastpass."
  exit 1
fi

gcloud compute ssl-certificates create $SSL_CERT \
       --project=$PROJ \
       --certificate=services.arxiv.org.cer \
       --private-key=services.arxiv.org.key \
       --global
