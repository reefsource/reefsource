# reefsource 

## Technologies

* Python >= 3.5.x
* Django >= 1.10.x
* Celery
* Postgres 9.6
* Redis
* RabbitMQ

## Setup
Install 

* VirtualBox 
* Vagrant 
* node 
* jspm (npm install jspm -g)

Setup local environment...

	vagrant up

Build javascript bundles

	npm install
	gulp

### Settings

Create `reefsource/settings/local.py` file and put copy paste following:

	import os

	os.environ.setdefault('DJANGO_DEBUG', 'True')

	os.environ.setdefault('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
	os.environ.setdefault('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

	# pick one env:
	from reefsource.settings.vagrant import *
	#from reefsource.settings.docker import *

## Running

In order to run the project in Vagrant you will need to configure a Pycharm remote interpreter (recommended) or a `vagrant ssh`

**Note:** All commands below should be run the inside of a VM.

Start the project's development server with using the django development server...

	python manage.py runserver 0.0.0.0:8000
	
A celery worker can be started using either the full command

	celery -A reefsource -L <INFO|DEBUG|ERROR|WARNING> worker -B
	
when working with javascript run following to automatically rebuild js bundles run following on HOST machine

	gulp watch

#monitoring

`flower --port=5555 --broker=amqp://reefsource:reefsource@127.0.0.1:5672/reefsourcecore --broker_api=http://guest:guest@localhost:15672/api/`

rabbitmq admin 

`guest:guest` @ `http://localhost:15672/#/`

# Docker

## connect to running container
`docker exec -it <container name> /bin/bash`

# PSQL
```
psql -U reefsource reefsource
\l - list databases
\connect DBNAME - change database
\dt - list tables
\q - to quit
\d+ TABLENAME - show ddl of a table
```

## restore from backup
```
psql -U postgres
DROP database reefsource;
CREATE database reefsource;
\q
cat filename.gz | gunzip | psql -U reefsource reefsource 
```

# django
to list current django settings 

`python manage.py diffsettings --all`