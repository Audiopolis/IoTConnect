from django.urls import reverse
from rest_framework import status

from iotconnect.utilities.test_classes import IotConnectTestCase


class ConnectViewTest(IotConnectTestCase):
    def setUp(self):
        self.url = reverse('connect')

    def test_patch__method_not_allowed(self):
        response = self.patch()
        self.assert_status_code(response, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete__method_not_allowed(self):
        response = self.delete()
        self.assert_status_code(response, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get__not_authenticated__redirected_to_dataporten(self):
        response = self.get()
        redirect_pattern = "^https://auth.dataporten.no/oauth/authorization"
        self.assert_redirect(response, redirect_pattern=redirect_pattern)

    def test_post__no_data__bad_request(self):
        response = self.post()
        self.assert_status_code(response, status_code=status.HTTP_400_BAD_REQUEST)

    def test_post__some_data_but_not_required_data__bad_request(self):
        data = {'some_data': 'test'}
        response = self.post(data)
        self.assert_status_code(response, status_code=status.HTTP_400_BAD_REQUEST)

    def test_post__authentication_data_but_not_generation_options__bad_request(self):
        authentication_data = {'session_key': 'some_key'}
        response = self.post({'authentication_data': authentication_data})
        self.assert_status_code(response, status_code=status.HTTP_400_BAD_REQUEST)

    def test_post__nonsensical_authentication_data__bad_request(self):
        data = {
            'authentication_data': {'some_key': 'some_data'},
            'generation_options': self._get_valid_generation_options()
        }
        response = self.post(data)
        self.assert_status_code(response, status_code=status.HTTP_400_BAD_REQUEST)

    def test_post__nonsensical_session_key_in_authentication_data__forbidden(self):
        data = {
            'authentication_data': {'session_key': 'some_data'},
            'generation_options': self._get_valid_generation_options()
        }
        response = self.post(data)
        self.assert_status_code(response, status_code=status.HTTP_403_FORBIDDEN)

    # Helper methods

    @staticmethod
    def _get_valid_generation_options():
        return {
            'deliver_by_email': True,
            'device_type': 'Refrigerator'
        }


class DataportenRedirectViewTest(IotConnectTestCase):
    def setUp(self):
        self.url = reverse('dataporten-redirect')

    def test_post__method_not_allowed(self):
        response = self.post()
        self.assert_status_code(response, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get__no_code__service_unavailable(self):
        response = self.get()
        self.assert_status_code(response, status.HTTP_503_SERVICE_UNAVAILABLE)
