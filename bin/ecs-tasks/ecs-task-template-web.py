import argparse
import json
import boto3

def get_env_variables(task_family):
    '''  
    :param task_family: 
    :return: 
    returns an array of env variables, example:
    [
        {
          "name": "MYSQL_ROOT_PASSWORD",
          "value": "password"
        }
    ] 
    '''

    s3 = boto3.resource('s3')
    env_vars = s3.Object('secrets.coralreefsource.org', '{task_family}_environment_vars'.format(task_family=task_family))
    json_str = env_vars.get()["Body"].read().decode('utf-8')

    return json.loads(json_str)


def generate_template(image_tag, task_family):
    env_vars = get_env_variables(task_family)

    template = {
        "family": task_family,
        "containerDefinitions": [{
            "image": "078097297037.dkr.ecr.us-east-1.amazonaws.com/reefsource:{image_tag}".format(image_tag=image_tag),
            "name": "reefsource_web",
            "cpu": 384,
            "memory": 512,
            "essential": True,
            "entryPoint": ["./bin/gunicorn.sh"],
            "portMappings": [{
                "containerPort": 8000,
                "protocol": "tcp"
            }],
            "environment": env_vars,
        }]
    }

    return template

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate ecs task definition.')
    parser.add_argument('--image_tag', required=True, help='docker tag')
    parser.add_argument('--task_family', required=True, help='ecs task family name')

    args = parser.parse_args()

    print(json.dumps(generate_template(args.image_tag, args.task_family), indent=2))
