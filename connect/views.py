import urllib.parse

from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView

from connect.classes.adapter import HiveManagerAdapter
from connect.classes.authenticator import FeideAuthenticator
from connect.exceptions import NoDataportenCodeError
from connect.models import FeideIdentity, DeviceRegistration
from connect.utils import get_access_token, get_user_data, get_first_name
from iotconnect.classes import IotConnectView
from uninett_api.settings._locals import FRONTEND_URL
from uninett_api.settings._secrets import DATAPORTEN_KEY


class ConnectView(IotConnectView):
    authenticator = FeideAuthenticator()
    ad_hoc_adapter = HiveManagerAdapter()
    # Default is True. Added for clarity.
    requires_authentication = True
    permission_classes = []

    def get(self, request, **_kwargs):
        session = request.session
        access_token = session.get('access_token', None)
        authenticated = False
        if access_token:
            authenticated = self.authenticator.is_authorized({'access_token': access_token})

        if authenticated:
            user_data = session.get('user_data', [])
            query_strings = {'session_key': session._session_key, 'name': get_first_name(user_data)}
            encoded = urllib.parse.urlencode(query_strings)
            url = f"{FRONTEND_URL}?{encoded}"
        else:
            query_strings = {'client_id': DATAPORTEN_KEY, 'response_type': 'code'}
            encoded = urllib.parse.urlencode(query_strings)
            url = f"https://auth.dataporten.no/oauth/authorization?{encoded}"

        return redirect(to=url)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_201_CREATED:
            hive_manager_id = response.data['username']
            response.data = response.data['psk']
            session = Session.objects.get(pk=self.authentication_data['session_key']).get_decoded()
            user_data = get_user_data(access_token=session['access_token'])
            name = user_data['name']
            email = user_data['email']
            feide_username = user_data['userid_sec'][0]

            feide_identity, _created = FeideIdentity.objects.get_or_create(feide_user_id=feide_username)
            if feide_identity.name != name or feide_identity.email != email:
                feide_identity.name = name
                feide_identity.email = email
                feide_identity.save()

            device_description = self.generation_options['device_type']
            psk = response.data

            DeviceRegistration.objects.create(feide_id=feide_identity, device_description=device_description, psk=psk,
                                              hive_manager_id=hive_manager_id)

        return super().finalize_response(request, response, *args, **kwargs)


class DataportenRedirectView(APIView):
    permission_classes = []

    def get(self, request, **_kwargs):
        code = request.query_params.get('code', None)

        if not code:
            raise NoDataportenCodeError("code was not supplied")

        access_token = get_access_token(code)
        user_data = get_user_data(access_token)
        request.session['access_token'] = access_token
        request.session['user_data'] = user_data
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        query_strings = {'session_key': session_key, 'name': get_first_name(user_data)}
        encoded = urllib.parse.urlencode(query_strings)
        return redirect(f"{FRONTEND_URL}?{encoded}")
