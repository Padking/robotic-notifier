from pprint import pprint

import requests

from environs import Env


def main():
    env = Env()
    env.read_env()

    url = 'https://dvmn.org/api/user_reviews/'
    devman_authorization_api_token = env('DEVMAN_API_AUTHORIZATION_TOKEN')
    headers = {
        'Authorization': f'Token {devman_authorization_api_token}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    pprint(response.json())


if __name__ == '__main__':
    main()
