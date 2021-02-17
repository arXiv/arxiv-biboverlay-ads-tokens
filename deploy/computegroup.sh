#!/bin/bash
# makes the managed instance group #
set -u

gcloud compute instance-groups managed describe $MIG
LACKS_MIG=$?
if [ ! $LACKS_MIG ]
then
    echo "Skipping create instance gorup since one exists"
    exit
fi


set -uve
       
# # Need to open the firewall to perform health check on instances
gcloud compute firewall-rules create allow-$NAME-health-check \
       --allow tcp:$PORT \
       --source-ranges 130.211.0.0/22,35.191.0.0/16,209.85.204.0/22 \
       --network default 

       
# make template see https://cloud.google.com/compute/docs/instance-templates/create-instance-templates#with-container
TEMPLATE="$NAME-template-$(date +%Y%m%d-%H%M%S)"
gcloud compute instance-templates create-with-container $TEMPLATE \
       --machine-type e2-medium \
       --tags=allow-$NAME-health-check \
       --container-env-file=../env.list \
       --container-image $IMAGE_URL


# make instance group
gcloud compute instance-groups managed create $MIG \
       --base-instance-name $NAME \
       --size 1\
       --template $TEMPLATE \
       --zone $ZONE

# Set named port for the load balancer to pick up. By default, the load
# balancer is looking for http and it has been tricky to get it to use a different name.
gcloud compute instance-groups managed set-named-ports $MIG \
       --named-ports http:$PORT \
       --zone=$ZONE
