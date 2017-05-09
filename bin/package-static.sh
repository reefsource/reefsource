#!/usr/bin/env bash

python manage.py collectstatic --noinput

version=`python -c "import reefsource; print (reefsource.__version__)"`
static_root=`python -c "from django.conf import settings; print (settings.STATIC_ROOT)"`

aws s3 sync "${static_root}" "s3://static.coralreefsource.org/${version}/" --acl 'public-read' --cache-control 'public, max-age=31536000'