from environs import Env

from telegram import Bot


def main():
    env = Env()
    env.read_env()

    telegram_bot_api_token = env('TELEGRAM_BOT_API_TOKEN')
    telegram_user_chat_id = env('TELEGRAM_USER_CHAT_ID')

    bot = Bot(token=telegram_bot_api_token)
    updates = bot.get_updates()

    greeting_msg_template = 'Hello, {}'
    name_to_greeting = updates[0].message.from_user.first_name
    msg_text = greeting_msg_template.format(name_to_greeting)

    bot.send_message(text=msg_text, chat_id=telegram_user_chat_id)


if __name__ == '__main__':
    main()
