import datetime
import json

import requests
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from connect.utils import attempt_json_loads
from iotconnect.classes import AdHocAdapter
from uninett_api.settings._secrets import HEADERS, OWNER_ID


class HiveManagerAdapter(AdHocAdapter):
    group_id = 339207927204382

    def validate_data(self, data, **kwargs):
        # TODO: Validate all data, possibly using serializers
        # Convert to JSON
        data = attempt_json_loads(data)

        # Validation
        if data.get('deliver_by_email', None) is None:
            raise ValidationError("deliver_by_email is required")
        if not data.get('device_type', None):
            raise ValidationError("deliver_by_email is required")

        # Formatting
        if isinstance(data['deliver_by_email'], str):
            data['deliver_by_email'] = data['deliver_by_email'].upper() == 'TRUE'

        return data

    def perform_generation(self, validated_data):
        url = "https://cloud-ie.aerohive.com/xapi/v1/identity/credentials"
        params = {'ownerId': OWNER_ID}
        session_key = attempt_json_loads(self.request.data['authentication_data'])['session_key']
        session = Session.objects.get(pk=session_key).get_decoded()

        kwargs = {
            'feide_username': session['user_data']['userid_sec'][0],
            'group_id': self.group_id,
            'full_name': session['user_data']['name'],
            'organization_name': 'Uninett',
            'policy': 'PERSONAL',
            'device_type': validated_data['device_type'],
            'deliver_by_email': validated_data['deliver_by_email'],
            'email': session['user_data']['email']
        }
        data = self._get_generation_data(**kwargs)

        response = requests.post(url=url, params=params, data=json.dumps(data), headers=HEADERS)
        data, status_code = self._get_response_data(response)

        return Response(data=data, status=status_code)

    def _get_response_data(self, response):
        if response.status_code == status.HTTP_403_FORBIDDEN:
            data = {'error': 'Could not generate PSK because the user has already created one this second'}
            return data, response.status_code
        try:
            psk = attempt_json_loads(response.content)['data']['password']
            data = {'psk': psk, 'username': self.hive_user_name}
            status_code = status.HTTP_201_CREATED
        except TypeError:
            data = {'error': 'Could not generate PSK due to an unknown error with the multi-PSK service'}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return data, status_code

    def _get_generation_data(self, feide_username: str, group_id: int, full_name: str, organization_name: str, policy: str,
                             device_type: str, deliver_by_email: bool, email: str):
        feide_username = feide_username.strip('feide:').split('@')[0]
        hive_user_name = f"{feide_username}: {datetime.datetime.now().replace(microsecond=0).strftime('%y%m%d%H%M%S')}"
        self.hive_user_name = hive_user_name

        return {
            "deliverMethod": "NO_DELIVERY" if not deliver_by_email else "EMAIL",
            "firstName": f"{full_name}",
            "groupId": group_id,
            "lastName": feide_username,
            "email": email,
            "organization": organization_name,
            "policy": policy,
            "userName": hive_user_name,
            "purpose": device_type
        }
