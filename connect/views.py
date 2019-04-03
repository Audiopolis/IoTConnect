from django.shortcuts import redirect
from rest_framework.views import APIView

from connect.classes.adapter import HiveManagerAdapter
from connect.classes.authenticator import FeideAuthenticator
from connect.utils import get_access_token, get_user_data, get_first_name
from iotconnect.classes import IotConnectView
from uninett_api.settings._test import FRONTEND_URL


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
            url = f"{FRONTEND_URL}?session_key={session._session_key}&name={get_first_name(user_data)}"
        else:
            url = "https://auth.dataporten.no/oauth/authorization?client_id=857348bd-71b3-443f-be5d-f7bd4421668f" \
                  "&response_type=code"

        return redirect(to=url)


class DataportenRedirectView(APIView):
    permission_classes = []

    def get(self, request, **_kwargs):
        code = request.query_params.get('code', None)
        if code:
            access_token = get_access_token(request.query_params['code'])
            user_data = get_user_data(access_token)
            request.session['access_token'] = access_token
            request.session['user_data'] = user_data
            if not request.session.session_key:
                request.session.save()
            session_key = request.session.session_key
            return redirect(f"{FRONTEND_URL}?session_key={session_key}&name={get_first_name(user_data)}")
        else:
            raise ValueError("code was not supplied")
