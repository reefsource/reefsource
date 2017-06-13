from rest_framework import serializers


class NonBlankValidator():
    def __call__(self, value):
        if not value:
            message = 'This field must not be blank'
            raise serializers.ValidationError(message)