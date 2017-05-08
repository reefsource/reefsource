#!/usr/bin/env bash

cmd="gunicorn reefsource.wsgi:application --bind=0.0.0.0:8000 -w 3"

if command -v newrelic-admin >/dev/null 2>&1; then
    newrelic-admin run-program ${cmd}
else
    ${cmd}
fi