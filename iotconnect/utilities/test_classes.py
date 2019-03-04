import json

from rest_framework.test import APITestCase


class IotConnectTestCase(APITestCase):
    url = ''

    def get(self, url=None, query_params=None):
        url = url or self.url
        query_params = query_params if query_params else {}
        response = self.client.get(url, data=query_params, **self._get_extra_headers())
        return response

    def post(self, data=None, url=None, **kwargs):
        url = url or self.url
        data = json.dumps(data)
        response = self.client.post(url, data, content_type='application/json', **self._get_extra_headers(), **kwargs)
        return response

    @staticmethod
    def _get_extra_headers():
        return {'HTTP_ACCEPT': f'application/json'}
