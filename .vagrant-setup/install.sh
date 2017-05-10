#!/bin/bash

# Script to set up a Django project on Vagrant.

# Installation settings

USERNAME=ubuntu

PROJECT_NAME=$1
PROJECT_DIR=/home/$USERNAME/$PROJECT_NAME

PGSQL_VERSION=9.6
DB_NAME=$PROJECT_NAME
VIRTUALENV_NAME=$PROJECT_NAME
VIRTUALENV_DIR=/home/$USERNAME/.virtualenvs/$PROJECT_NAME
SSL_DOMAIN=$PROJECT_NAME.local

PROVISIONING_FLAG_DIR=/home/$USERNAME/provisioning/$PROJECT_NAME
mkdir -p $PROVISIONING_FLAG_DIR

set -x

if [ ! -f $PROVISIONING_FLAG_DIR/apt-get ]; then
    echo 'Configure apt-get'
    echo "deb http://nginx.org/packages/mainline/ubuntu/ `lsb_release -c | awk '{print $2}'` nginx" | sudo tee -a /etc/apt/sources.list
    echo "deb-src http://nginx.org/packages/mainline/ubuntu/ `lsb_release -c | awk '{print $2}'` nginx" | sudo tee -a /etc/apt/sources.list

    sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ `lsb_release -c | awk '{print $2}'`-pgdg main"
    wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

    echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
    wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

    echo 'Refresh apt-get repo'
    apt-get update -y

    echo 'Install packages from apt-get'

    apt-get install -y --force-yes git \
        build-essential \
        python \
        python-dev \
        python3-dev \
        python-setuptools \
        libxml2-dev \
        libxslt-dev \
        nginx \
        redis-server \
        rabbitmq-server \
        postgresql-$PGSQL_VERSION \
        libpq-dev \
        awscli

    # Python dev packages build-essential python python-dev python-setuptools
    # Required by ofxparse libxml2-dev libxslt-dev

    # Dependencies for image processing with Pillow (drop-in replacement for PIL)
    # supporting: jpeg, tiff, png, freetype, littlecms
    # (pip install pillow to get pillow itself, it is not in requirements.txt)
    # apt-get install -y libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev

    # Install project dependencies for audio transcoding (mpeg, aac)
    # apt-get install -y lame faad

    date > "$PROVISIONING_FLAG_DIR/apt-get"
fi

if [ ! -f $PROVISIONING_FLAG_DIR/nginx ]; then
    echo 'Setup nginx'

    sudo service nginx stop
    STATIC_PATH=$PROJECT_DIR/static

    sudo cat $PROJECT_DIR/.vagrant-setup/conf/nginx-default-site | sed "s#_SSL_DOMAIN_#$SSL_DOMAIN#g" | sed "s#_STATIC_PATH_#$STATIC_PATH#g" > /etc/nginx/conf.d/default.conf

    mkdir -p /etc/nginx/ssl/

    # Create the key for the Certificate Authority.  2048 is the bit encrypting, you can set it whatever you want
    openssl genrsa -out /etc/nginx/ssl/$SSL_DOMAIN.key 2048

    # Next create the certificate and self-sign it (what the -new and -x509 do).  Note, I'm explicitly telling it the main config path.  You have to.
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -key /etc/nginx/ssl/$SSL_DOMAIN.key -out /etc/nginx/ssl/$SSL_DOMAIN.cert -subj "/CN=*.$SSL_DOMAIN/C=CA/L=USA/O=reefsource/emailAddress=admin@reefsource.com"

    openssl dhparam -out /etc/nginx/dhparam.pem 1024
    sudo service nginx start

    date > "$PROVISIONING_FLAG_DIR/nginx"
fi


if [ ! -f $PROVISIONING_FLAG_DIR/rabbitmq ]; then
    echo 'Setup RabbitMQ'

    rabbitmq-plugins enable rabbitmq_management

    rabbitmqctl add_user reefsource reefsource
    rabbitmqctl add_vhost reefsourcecore
    rabbitmqctl set_user_tags reefsource administrator #required to see everything in flower
    rabbitmqctl set_permissions -p reefsourcecore reefsource ".*" ".*" ".*"

    service rabbitmq-server restart
    date > "$PROVISIONING_FLAG_DIR/rabbitmq"
fi


if [ ! -f $PROVISIONING_FLAG_DIR/postgres ]; then
    echo 'Setup Postgresql'

    cp $PROJECT_DIR/.vagrant-setup/conf/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
    /etc/init.d/postgresql reload

    sudo su - postgres -c "psql -c \"CREATE USER reefsource WITH PASSWORD 'reefsource';\""
    sudo su - postgres -c "psql -c \"CREATE EXTENSION tablefunc;\""

    createdb -Upostgres -O reefsource $DB_NAME

    date > "$PROVISIONING_FLAG_DIR/postgres"
fi

if [ ! -f $PROVISIONING_FLAG_DIR/virtualenv ]; then
    echo 'Setup virtualenv global '
    if ! command -v pip; then
        easy_install -U pip
    fi
    if [ ! -f /usr/local/bin/virtualenv ]; then
        pip install virtualenv virtualenvwrapper
    fi
    date > "$PROVISIONING_FLAG_DIR/virtualenv"
fi

if [ ! -f $PROVISIONING_FLAG_DIR/bashrc ]; then
    echo 'Setup bash environment global'
    cat $PROJECT_DIR/.vagrant-setup/conf/bashrc >> /home/$USERNAME/.bashrc

    date > "$PROVISIONING_FLAG_DIR/bashrc"
fi

if [ ! -f $PROVISIONING_FLAG_DIR/virtualenv_proj ]; then
    echo 'Setup virtualenv for project'
    sudo su - $USERNAME -c "virtualenv $VIRTUALENV_DIR -p `which python3` && echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"
    sudo su - $USERNAME -c "$VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements/local.txt"
    sudo su - $USERNAME -c "echo \"workon $VIRTUALENV_NAME\" >> ~/.bashrc"

    date > "$PROVISIONING_FLAG_DIR/virtualenv_proj"
fi

echo "installation of prerequisites done, running migrate and projectsetup"
sudo su - $USERNAME -c "$VIRTUALENV_DIR/bin/python $PROJECT_DIR/manage.py migrate --settings=reefsource.settings.local"
sudo su - $USERNAME -c "$VIRTUALENV_DIR/bin/python $PROJECT_DIR/manage.py setupdefaults --settings=reefsource.settings.local"

if [ ! -f $PROVISIONING_FLAG_DIR/demo ]; then
    sudo su - $USERNAME -c "$VIRTUALENV_DIR/bin/python $PROJECT_DIR/manage.py setupdemo --settings=reefsource.settings.local"
    sudo su - $USERNAME -c "$VIRTUALENV_DIR/bin/python $PROJECT_DIR/manage.py backfill --settings=reefsource.settings.local"
    date > "$PROVISIONING_FLAG_DIR/demo"
fi