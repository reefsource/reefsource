#!/usr/bin/env python

import argparse
import json
import boto3

class DeploymentManager():
    def __init__(self):
        self.client = boto3.client('ecs')
        self.cluster = 'reefsource'

    def get_env_variables_by_env_name(self, environment_name):
        '''
        :param task_family:
        :return:
        returns an array of env variables for given environment, example:
        [
            {
            "name": "MYSQL_ROOT_PASSWORD",
            "value": "password"
            }
        ]
        '''

        s3 = boto3.resource('s3')
        env_vars = s3.Object('secrets.coralreefsource.org', '{environment_name}_environment_vars'.format(environment_name=environment_name))
        json_str = env_vars.get()["Body"].read().decode('utf-8')

        return json.loads(json_str)

    def get_template(self, task_family, image_tag, env_vars):
        return {
            "family": task_family,
            "containerDefinitions": [{
                "image": "078097297037.dkr.ecr.us-east-1.amazonaws.com/{task_family}:{image_tag}".format(task_family=task_family, image_tag=image_tag),
                "cpu": 384,
                "memory": 512,
                "essential": True,
                "environment": env_vars,
            }]
        }

    def generate_django_template(self, image_tag, task_family, env_vars):
        template = self.get_template(task_family, image_tag, env_vars)
        template['containerDefinitions']['name'] = "django"
        template['containerDefinitions']['entryPoint'] = ["./bin/gunicorn.sh"]
        template['containerDefinitions']['portMappings'] = [{
            "containerPort": 8000,
            "protocol": "tcp"
        }]
        return template


    def generate_db_migrate_template(self, image_tag, task_family, env_vars):
        template = self.get_template(task_family, image_tag, env_vars)
        template['family'] = template['containerDefinitions']['name'] = "django_migrate"
        template['containerDefinitions']['entryPoint'] = ["./manage.py migrate"]

        return template

    def register_task_definition(self, template):
        response = self.client.client.register_task_definition(
            family=template['family_name'],
            containerDefinitions=template
        )
        return  response['taskDefinition']['revision']

    def getTaskDefinitionName(self, template, revision):
        return '{family_name}:{revision}'.format(family_name=template['family_name'], revision=revision)

    def update_service(self, service_name, template):
        django_task_template_revision = self.register_task_definition(template)
        
        # Update the service with the new task definition and desired count
        current_desired_count = self.client.describe_services(
            cluster=self.cluster,
            services=[service_name]
        )[0]['desiredCount']

        self.client.update_service(
            cluster=self.cluster,
            service='reefsource',
            desiredCount=current_desired_count,
            taskDefinition=self.getTaskDefinitionName(template, django_task_template_revision)
        )
    def run_task(self, template):
        db_migrate_task_template_revision = self.register_task_definition(template)
        self.client.run_task(cluster=self.cluster, taskDefinition=template)

    def deploy(self, image_tag):
        env_vars = self.get_env_variables_by_env_name('reefsource')
        
        django_task_template = self.generate_django_template(image_tag, task_family='reefsource', env_vars=env_vars)
        db_migrate_task_template = self.generate_db_migrate_template(image_tag, task_family='reefsource', env_vars=env_vars)

        self.update_service(service_name='reefsource', template=django_task_template)
        self.run_task(template=db_migrate_task_template)
             
def get_args():
    parser = argparse.ArgumentParser(description='deploys django app and applies migration using docker image tag')
    parser.add_argument('--image_tag', required=True, help='docker tag')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()

    deploy_manager = DeploymentManager()
    deploy_manager.deploy(args.image_tag)