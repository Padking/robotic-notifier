from contextlib import suppress
from typing import Dict

import requests

from environs import Env


def execute_communication_session(url, headers=None,
                                  params=None, timeout=90):

    response = requests.get(url, params=params,
                            headers=headers, timeout=timeout)
    response.raise_for_status()

    raw_response = response.json()

    return raw_response


def get_timestamp(ctx: Dict):
    if ctx['status'] == 'timeout':
        timestamp = ctx['timestamp_to_request']
    elif ctx['status'] == 'found':
        timestamp = ctx['last_attempt_timestamp']
    elif ctx['status'] == 'poll_started':
        timestamp = ''

    return timestamp


if __name__ == '__main__':
    env = Env()
    env.read_env()

    url = 'https://dvmn.org/api/long_polling/'
    devman_authorization_api_token = env('DEVMAN_API_AUTHORIZATION_TOKEN')
    headers = {
        'Authorization': f'Token {devman_authorization_api_token}',
    }
    raw_response = {'status': 'poll_started'}

    with suppress(requests.ConnectionError, requests.ReadTimeout):
        while True:
            params = {
                'timestamp': get_timestamp(raw_response),
            }
            raw_response = execute_communication_session(url, headers=headers,
                                                         params=params, timeout=None)
