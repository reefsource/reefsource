#!/bin/bash
set -x

psql -U postgres -c "drop database reefsource" &&
psql -U postgres -c "create database reefsource" &&
./bin/after-deploy.sh &&
python manage.py setupdemo &&
python manage.py backfill --all
