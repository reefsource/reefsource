import os

# this file gets overwritten by ./bin/set-version.sh executed by CI

build = os.getenv('CIRCLE_BUILD_NUM', 'x')
githash = os.getenv('CIRCLE_SHA1', 'x')