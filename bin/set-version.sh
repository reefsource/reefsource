#!/usr/bin/env bash

# create a version file
cat > reefsource/version.py << EOF
from __future__ import absolute_import, unicode_literals

build = $CIRCLE_BUILD_NUM
githash = '$CIRCLE_SHA1'
EOF