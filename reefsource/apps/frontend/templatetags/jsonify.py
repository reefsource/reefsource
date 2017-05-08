from __future__ import unicode_literals

import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    elif isinstance(object, set):
        object = list(object)
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify, is_safe=True)