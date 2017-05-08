#!/bin/bash
set -x
if [ -z "$1" ]
  then
    echo "restore-db name_of_backup.gzip"
fi

psql -U postgres -c "drop database reefsource" &&
psql -U postgres -c "create database reefsource" &&
cat $1 | gunzip | psql -U reefsource reefsource