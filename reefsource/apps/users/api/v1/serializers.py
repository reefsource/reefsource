from django.contrib.auth import authenticate
from rest_framework import serializers

from reefsource.apps.users.models import User
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class LoginSerializer(serializers.Serializer):
    """
        Serializer class used to validate a username and password.
        'username' is identified by the custom UserModel.USERNAME_FIELD.
        Returns a user profile
        """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                return {'user': user}

            else:
                msg = 'Unable to login with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)


class UserSerializer(AppendIdModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id', 'last_login', 'date_joined',)
        exclude = ('password',)


class UserProfileSerializer(AppendIdModelSerializer):

    permissions = serializers.StringRelatedField(source='get_all_permissions', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'permissions')
        read_only_fields = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')
