# Reefsource

[![CircleCI](https://circleci.com/gh/reefsource/reefsource.svg?style=svg)](https://circleci.com/gh/reefsource/reefsource)

## Technologies

* Python >= 3.5.x
* Django >= 1.10.x
* Celery
* Postgres 9.6
* Redis
* RabbitMQ

## local setup
1. Install 
    * [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
    * [Vagrant](https://www.vagrantup.com/downloads.html)
    * [node](https://nodejs.org/en/download/)
    * angular cli (`npm install -g @angular/cli`)


2. Create `reefsource/settings/local.py` file and put copy paste following:

	```
	import os

	os.environ.setdefault('DJANGO_DEBUG', 'True')

	os.environ.setdefault('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
	os.environ.setdefault('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

	from reefsource.settings.vagrant import *
	```

3. Build javascript bundles

	`npm install`

4. Setup local environment...

	`vagrant up`


## Running

There are two parts of the application:
 - django api server and (`/reefsource` directory)
 - angular 2 single page application (`/client` directory)
 
### Django api server:
In order to run the project in Vagrant you will need to configure a Pycharm remote interpreter (recommended) or a `vagrant ssh`

**Note:** All commands below should be run the inside of a VM.

Start the project's development server with using the django development server...

	python manage.py runserver 0.0.0.0:8000

A celery worker can be started using either the full command

	celery -A reefsource -L <INFO|DEBUG|ERROR|WARNING> worker -B

### single page application 
On the host machine run 

	npm start

This will start another server on http://localhost:4200