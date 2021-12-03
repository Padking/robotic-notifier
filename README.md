# Robotic notifier

Бот-уведомитель

## Описание

Чат с уведомлениями о проверке работ уроков от [Devman](https://dvmn.org/)

### Начало работы

* Необходимо и достаточно:
  - получить токен для бота у [BotFather](https://t.me/botfather),
  - получить `chat_id` у [бота](https://t.me/userinfobot),
  - зарегистрироваться на [сайте Devman](https://dvmn.org/),
  - получить токен аутентификации для работы с [API Devman](https://dvmn.org/api/docs/)

### Особенности

- представляет собой альтернативу веб-интерфейсу, доступному в профиле [сайта Devman](https://dvmn.org/), которая присылает уведомления, используя realtime-технологию _long polling_,
- присылает кастомизированные сообщения П-лю, которые позволяют чётко понять: какую работу проверили и каков результат проверки,
- взаимодействует с long polling-частью [API Devman](https://dvmn.org/api/docs/)

## Примеры работы

  **Ответ бота-уведомителя при положительном результате проверки:**

  ![success_status_of_lesson_check](https://github.com/Padking/where-to-go/blob/master/screenshots/success_status_of_lesson_check.jpg)


  **Ответ бота-уведомителя при отрицательном результате проверки:**

  ![not_success_status_of_lesson_check](https://github.com/Padking/where-to-go/blob/master/screenshots/not_success_status_of_lesson_check.jpg)


  **Ответ бота-уведомителя при отсутствии результатов проверки:**

  ![no_proven_lessons](https://github.com/Padking/where-to-go/blob/master/screenshots/no_proven_lessons.png)


## Структура проекта

### `bot.py`

_Реализует логику бота-уведомителя с long polling_

### `courier.py`

_Реализует long polling без бота-уведомителя_

### Используемые технологии

* [requests](https://requests.readthedocs.io/en/master/)
* [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/en/stable/)

## Требования к окружению

* Python 3.8 и выше,
* Linux/Windows,
* Переменные окружения (ПеО).

Проект настраивается через ПеО, достаточно указать их в файле `.env`.
Передача значений ПеО происходит с использованием [environs](https://pypi.org/project/environs/).

### Параметры проекта

|       Ключ        |     Назначение     |   По умолчанию   |
|-------------------|------------------|------------------|
|`TELEGRAM_BOT_API_TOKEN`| Токен для взаимодействия с [Bot API](https://core.telegram.org/bots/api) | — |
|`TELEGRAM_USER_CHAT_ID`| Идентификатор чата бота-уведомителя и П-ля | — |
|`DEVMAN_API_AUTHORIZATION_TOKEN`| Токен аутентификации для работы с [API Devman](https://dvmn.org/api/docs/) | — |

## Установка

- Клонировать проект:
```sh
git clone https://github.com/Padking/robotic-notifier.git
cd robotic-notifier
```
- Создать каталог виртуального окружения (ВО)*,
   связать каталоги ВО и проекта,
   установить зависимости:
```sh
mkvirtualenv -p <path to python> <name of virtualenv>
setvirtualenvproject <path to virtualenv> <path to project>
pip install -r requirements.txt
```

- запустить бота-уведомителя:
```sh
python bot.py
```



\* с использованием [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html)