import json
import re

from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.test import APITestCase


class IotConnectTestCase(APITestCase):
    url = ''

    def get(self, query_params=None):
        query_params = query_params if query_params else {}
        response = self.client.get(self.url, query_params, **self._get_extra_headers())
        return response

    def post(self, data=None, **kwargs):
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json', **self._get_extra_headers(),
                                    **kwargs)
        return response

    def patch(self, data=None, **kwargs):
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json', **self._get_extra_headers(),
                                     **kwargs)
        return response

    def delete(self, query_params=None):
        query_params = query_params if query_params else {}
        response = self.client.delete(self.url, query_params, **self._get_extra_headers())
        return response

    def assert_status_code(self, response, status_code: status):
        self.assertEqual(status_code, response.status_code)

    def assert_redirect(self, response, redirect_pattern: str = None):
        self.assertTrue(isinstance(response, HttpResponseRedirect))

        if redirect_pattern:
            self.assertIsNotNone(re.match(redirect_pattern, response.url))

    @staticmethod
    def _get_extra_headers():
        return {'HTTP_ACCEPT': f'application/json'}
