from contextlib import suppress
from typing import Dict

import requests

from environs import Env
from telegram import Bot
from telegram.constants import PARSEMODE_HTML


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


def get_prepared_msg_text_for_sending(msg_template: str, ctx: Dict,
                                      additional_ctx: Dict) -> str:

    msg_text = 'Проверенных работ нет'
    if verified_lessons := ctx.get('new_attempts', None):
        verified_lesson = verified_lessons[0]
        lesson_check_status = verified_lesson['is_negative']

        resolved_lesson_msg_text = additional_ctx['resolved']
        not_resolved_lesson_msg_text = additional_ctx['not_resolved']
        lesson_check_result = (
            resolved_lesson_msg_text if lesson_check_status
            else not_resolved_lesson_msg_text
        )

        placeholders = {
            'lesson_title': verified_lesson['lesson_title'],
            'lesson_check_result': lesson_check_result,
            'lesson_url': verified_lesson['lesson_url'],
        }
        msg_text = msg_template.format(**placeholders)

    return msg_text


def main():
    env = Env()
    env.read_env()

    telegram_bot_api_token = env('TELEGRAM_BOT_API_TOKEN')
    telegram_user_chat_id = env('TELEGRAM_USER_CHAT_ID')

    url = 'https://dvmn.org/api/long_polling/'
    devman_authorization_api_token = env('DEVMAN_API_AUTHORIZATION_TOKEN')
    headers = {
        'Authorization': f'Token {devman_authorization_api_token}',
    }
    raw_response = {'status': 'poll_started'}

    lesson_check_status_to_msg_text = {
        'resolved': (
            'Преподавателю всё понравилось, '
            'можно приступать к следующему уроку!'
        ),
        'not_resolved': 'К сожалению, в работе нашлись ошибки.',
    }
    msg_template = (
        'У вас проверили работу &#171{lesson_title}&#187 \n\n'
        '{lesson_check_result} \n\n'
        '<a href="{lesson_url}">Ссылка на задачу</a>'
    )

    bot = Bot(token=telegram_bot_api_token)
    with suppress(requests.ConnectionError, requests.ReadTimeout):
        while True:
            params = {
                'timestamp': get_timestamp(raw_response),
            }
            raw_response = execute_communication_session(url, headers=headers,
                                                         params=params, timeout=None)
            msg_text = get_prepared_msg_text_for_sending(msg_template, raw_response,
                                                         lesson_check_status_to_msg_text)
            bot.send_message(text=msg_text, chat_id=telegram_user_chat_id,
                             parse_mode=PARSEMODE_HTML,
                             disable_web_page_preview=True,
                             disable_notification=True)


if __name__ == '__main__':
    main()
