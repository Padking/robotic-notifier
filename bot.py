#!bin/python

import logging
import time

from textwrap import dedent
from typing import Dict

import requests

from environs import Env
from telegram import Bot
from telegram.constants import PARSEMODE_HTML


logger = logging.getLogger(__file__)


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


def long_polling(bot, telegram_user_chat_id, url, headers: Dict):

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

    get_starting_msg_text = 'Бот запущен'
    restart_msg_text = 'Бот перезапустится через время'

    connection_error_msg_text = 'Соединение с Сетью разорвано'
    readtimeout_msg_text = (
        'Devman-сервер не предоставил ответ за время, равное тайм-ауту'
    )
    error_msg_text = 'Возникло непреднамеренное завершение работы.'

    timestamp = get_timestamp()
    logger.info(get_starting_msg_text)
    while True:
        try:
            params = {
                'timestamp': timestamp,
            }
            payload = get_response_payload(url, headers=headers,
                                           params=params)
            timestamp = get_timestamp(payload)

            msg_text = get_message_text(msg_template, payload,
                                        lesson_check_status_to_msg_text)
            bot.send_message(text=msg_text, chat_id=telegram_user_chat_id,
                             parse_mode=PARSEMODE_HTML,
                             disable_web_page_preview=True,
                             disable_notification=True)
        except requests.ConnectionError:
            logger.warning(connection_error_msg_text)
            logger.info(restart_msg_text)
            time.sleep(60)
            continue
        except requests.ReadTimeout:
            logger.warning(readtimeout_msg_text)
            continue
        except Exception:
            logger.exception(error_msg_text)
            logger.info(restart_msg_text)
            time.sleep(120)
            continue


if __name__ == '__main__':
    env = Env()
    env.read_env()

    telegram_bot_api_token = env('TELEGRAM_BOT_API_TOKEN')
    telegram_user_chat_id = env('TELEGRAM_USER_CHAT_ID')

    url = 'https://dvmn.org/api/long_polling/'
    devman_authorization_api_token = env('DEVMAN_API_AUTHORIZATION_TOKEN')
    headers = {
        'Authorization': f'Token {devman_authorization_api_token}',
    }

    bot = Bot(token=telegram_bot_api_token)

    LOG_FILENAME = 'bot.log'
    logging.basicConfig(filename=LOG_FILENAME,
                        format='%(levelname)s %(asctime)s %(message)s')

    class BotLogHandler(logging.Handler):
        def emit(self, record: logging.LogRecord):
            log_entry_msg = self.format(record)
            bot.send_message(text=log_entry_msg, chat_id=telegram_user_chat_id,
                             parse_mode=PARSEMODE_HTML,
                             disable_notification=True)

    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogHandler())

    long_polling(bot, telegram_user_chat_id, url, headers)
