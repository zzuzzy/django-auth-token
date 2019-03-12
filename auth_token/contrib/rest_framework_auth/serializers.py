from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.compat import authenticate


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(label=_('Username'))
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    permanent = serializers.BooleanField(label=_('Permanent'), required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class MobileAuthTokenSerializer(serializers.Serializer):

    uuid = serializers.UUIDField(label=_('device UUID'))
    login_device_token = serializers.CharField(
        label=_('Device Token'),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        uuid = attrs.get('uuid')
        token = attrs.get('login_device_token')

        if uuid and token:
            # DeviceBackend is called here
            user = authenticate(request=self.context.get('request'),
                                device_uuid=uuid, mobile_login_token=token)

            if not user:
                raise serializers.ValidationError(
                    _('Unable to log in with provided credentials.'),
                    code='authorization')
        else:
            raise serializers.ValidationError(
                _('Must include "uuid" and "token".'), code='authorization')

        attrs['user'] = user
        return attrs


class MobileAuthTokenRegisterSerializer(serializers.Serializer):

    uuid = serializers.UUIDField(label=_('device UUID'))
