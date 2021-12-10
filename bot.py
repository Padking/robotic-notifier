#!bin/python

import time

from textwrap import dedent
from typing import Dict

import requests

from environs import Env
from telegram import Bot
from telegram.constants import PARSEMODE_HTML


def get_response_payload(url, headers=None,
                         params=None, timeout=90):

    response = requests.get(url, params=params,
                            headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    return payload


def get_timestamp(ctx: Dict = None):

    ctx = ctx or {}
    status = ctx.get('status', '')

    timestamp = ''
    if status == 'timeout':
        timestamp = ctx['timestamp_to_request']
    elif status == 'found':
        timestamp = ctx['last_attempt_timestamp']

    return timestamp


def get_message_text(msg_template: str,
                     ctx: Dict,
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

    resolved_text_undedented = '''
        Преподавателю всё понравилось,
        можно приступать к следующему уроку!
    '''
    lesson_check_status_to_msg_text = {
        'resolved': dedent(resolved_text_undedented),
        'not_resolved': 'К сожалению, в работе нашлись ошибки.',
    }
    msg_template_undedented = '''
        У вас проверили работу &#171{lesson_title}&#187
        {lesson_check_result}
        <a href="{lesson_url}">Ссылка на задачу</a>
    '''
    msg_template = dedent(msg_template_undedented)

    bot = Bot(token=telegram_bot_api_token)
    timestamp = get_timestamp()

    while True:
        try:
            params = {
                'timestamp': timestamp,
            }
            payload = get_response_payload(url, headers=headers,
                                           params=params, timeout=None)
            timestamp = get_timestamp(payload)

            msg_text = get_message_text(msg_template, payload,
                                        lesson_check_status_to_msg_text)
            bot.send_message(text=msg_text, chat_id=telegram_user_chat_id,
                             parse_mode=PARSEMODE_HTML,
                             disable_web_page_preview=True,
                             disable_notification=True)
        except requests.ConnectionError:
            time.sleep(60)
            continue
        except requests.ReadTimeout:
            continue


if __name__ == '__main__':
    main()
