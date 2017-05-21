#!/usr/bin/env bash
set -x

python manage.py migrate --no-input && \
python manage.py setupdefaults