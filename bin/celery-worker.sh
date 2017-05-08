#!/usr/bin/env bash

DEFAULT_LOG_LEVEL="INFO"
LOGLEVEL=${LOGLEVEL:-$DEFAULT_LOG_LEVEL}

cmd="celery worker -A reefsource -l $LOGLEVEL -n worker1.%h $EXTRA_OPTIONS"

if command -v newrelic-admin >/dev/null 2>&1; then
    newrelic-admin run-program ${cmd}
else
    ${cmd}
fi
