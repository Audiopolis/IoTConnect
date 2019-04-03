import json

import requests

from uninett_api.settings._secrets import DATAPORTEN_HEADERS, SOCIAL_AUTH_DATAPORTEN_SECRET, SOCIAL_AUTH_DATAPORTEN_KEY
from uninett_api.settings._test import BACKEND_URL


def get_access_token(code):
    url = 'https://auth.dataporten.no/oauth/token'
    payload = {'grant_type': 'authorization_code',
               'code': code,
               'client_id': SOCIAL_AUTH_DATAPORTEN_KEY,
               'client_secret': SOCIAL_AUTH_DATAPORTEN_SECRET,
               'redirect_uri': f"{BACKEND_URL}/connect/complete/dataporten/"}

    response = requests.post(url=url, data=payload, headers=DATAPORTEN_HEADERS)
    access_token = json.loads(response.content)['access_token']

    return access_token


def get_user_data(access_token):
    url = 'https://auth.dataporten.no/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url=url, headers=headers)
    content = json.loads(response.content)
    return content.get('user', None)


def get_first_name(user_data):
    name = user_data.get('name', 'bruker')
    return name.split(' ')[0]
