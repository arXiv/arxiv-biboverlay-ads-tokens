#!/bin/bash

set -v

source config.sh

if [ ! $1 ]
then
    echo "Must pass image URL as first parm"
    exit 1
fi


gcloud container images describe $1

if [ ! %! ]
then
    echo "No image found for $1"
    gcloud container images list
    exit 1
fi

set -ef
NEW_IMAGE_URL=$1

#### UPDATE PROCESS ####

# create a new template with a new name
TEMPLATE="$NAME-template-$(date +%Y%m%d-%H%M%S)"
gcloud compute instance-templates create-with-container $TEMPLATE \
       --machine-type e2-medium \
       --tags=allow-$NAME-health-check \
       --container-env-file=../env.list \
       --container-image $NEW_IMAGE_URL

# change the template of the instance group
gcloud compute instance-groups managed set-instance-template $MIG \
       --template=$TEMPLATE \
       --zone=$ZONE

# start a rolling update of the instance group
gcloud compute instance-groups managed rolling-action start-update $MIG \
       --version template=$TEMPLATE \
       --max-surge 4 \
       --zone=$ZONE
