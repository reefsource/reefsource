#!/usr/bin/env bash

python manage.py collectstatic --noinput

version=`python -c "import reefsource; print (reefsource.__version__)"`
static_root=`python -c "from django.conf import settings; print (settings.STATIC_ROOT)"`

aws s3 sync "${static_root}" "s3://static.coralreefsource.org/${version}/" --acl 'public-read' --cache-control 'public, max-age=31536000'

# clean up previous version
aws s3 mv "s3://static.coralreefsource.org/current" current
aws s3 rm "s3://static.coralreefsource.org/`cat current`/" --recursive --only-show-errors
echo ${version} > current
aws s3 mv current "s3://static.coralreefsource.org/current"