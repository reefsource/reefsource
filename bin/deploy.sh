#!/usr/bin/env bash

CLUSTER_NAME=reefsource
SERVICE_NAME=reefsource
TASK_FAMILY=reefsource

BUILD_NUMBER=${CIRCLE_BUILD_NUM}

# Create a new task definition for this build
./ecs-tasks/ecs-task-tempalte-web.py ${IMAGE_TAG} ${TASK_FAMILY} > tmp-${BUILD_NUMBER}.json
aws ecs register-task-definition --family ${TASK_FAMILY} --cli-input-json file://tmp-${BUILD_NUMBER}.json

# Update the service with the new task definition and desired count
TASK_REVISION=`aws ecs describe-task-definition --task-definition ${TASK_FAMILY} | egrep "revision" | tr "/" " " | awk '{print $2}' | sed 's/"$//'`
DESIRED_COUNT=`aws ecs describe-services --cluster ${CLUSTER_NAME} --services ${SERVICE_NAME} | egrep "desiredCount" | head -1 | tr "/" " " | awk '{print $2}' | sed 's/,$//'`
if [ ${DESIRED_COUNT} = "0" ]; then
    DESIRED_COUNT="1"
fi

aws ecs update-service --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME} --task-definition ${TASK_FAMILY}:${TASK_REVISION} --desired-count ${DESIRED_COUNT}
