import json

from django.contrib.sessions.models import Session
from rest_framework.exceptions import ValidationError

from connect.utils import get_user_data, attempt_json_loads
from iotconnect.classes import Authenticator


class FeideAuthenticator(Authenticator):
    def validate_data(self, data, **kwargs):
        # Convert to JSON
        data = attempt_json_loads(data)

        if self.request.method.upper() != 'GET' and not data.get('session_key', None):
            # session_key is required when posting, because sessions will not work when posting using XmlHttpRequests.
            raise ValidationError({'session_key': 'session_key is required'})

        return data

    def is_authorized(self, validated_data):
        request = self.request

        # When the method is GET, we do not expect the authentication data to be sent. Handle this case.
        if request.method.upper() == 'GET':
            session = request.session
        else:
            # The method is not GET.
            session_key = validated_data['session_key']
            try:
                # Get the session using the authentication data (session_key). Required because CORS does not work.
                session = Session.objects.get(pk=session_key).get_decoded()
            except Session.DoesNotExist:
                # The session key is invalid. Require authentication.
                return False

        # Try to get the access token from the session.
        access_token = session.get('access_token', None)
        if access_token:
            # Try to get the user data from the session.
            session_data = session.get('user_data', None)
            # If an access token exists in the session, try to get user data from Feide.
            feide_data = get_user_data(access_token=access_token)
            # Validate
            return self._validate_user_data(session_data, feide_data)

        # access_token is not stored in session. Require authentication.
        return False

    @staticmethod
    def _validate_user_data(session_data, feide_data):
        # The user is authenticated.
        return session_data and feide_data and feide_data == session_data
