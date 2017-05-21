import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


def get_file_location(path):
    return 's3://{bucket}/{path}'.format(bucket=settings.AWS_STORAGE_BUCKET_NAME, path=path)


@shared_task
def stage1(path):
    logger.info('starting stage1')

    import boto3
    client = boto3.client('ecs')
    cluster = 'reefsource'
    task_family = 'image_preprocessor'

    client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
        'containerOverrides': [{
            'name': 'image_preprocessor',
            'command': [
                get_file_location(path),
            ],
        }, ], }, )


@shared_task
def stage2(path):
    logger.info('starting stage2')

    import boto3
    client = boto3.client('ecs')
    cluster = 'reefsource'
    task_family = 'image_calibration'

    client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
        'containerOverrides': [{
            'name' : 'image_calibration',
            'command': [
                get_file_location(path),
            ],
        }, ], }, )
