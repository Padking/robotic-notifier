from contextlib import suppress
from pprint import pprint

import requests

from environs import Env


def execute_communication_session(url, headers=None,
                                  params=None, timeout=90):

    response = requests.get(url, params=params,
                            headers=headers, timeout=timeout)
    response.raise_for_status()

    raw_response = response.json()

    return raw_response


def main():
    env = Env()
    env.read_env()

    url = 'https://dvmn.org/api/long_polling/'
    devman_authorization_api_token = env('DEVMAN_API_AUTHORIZATION_TOKEN')
    headers = {
        'Authorization': f'Token {devman_authorization_api_token}',
    }
    params = {
        'timestamp': 1637421213.336591,
    }

    raw_response = execute_communication_session(url, headers=headers,
                                                 params=None, timeout=120)
    pprint(raw_response)


if __name__ == '__main__':
    with suppress(requests.ConnectionError, requests.ReadTimeout):
        while True:
            main()
