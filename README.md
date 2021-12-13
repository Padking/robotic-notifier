# Robotic notifier

Бот-уведомитель

  - [Описание](#описание)
    - [Начало работы](#начало-работы)
    - [Особенности](#особенности)
  - [Примеры работы](#примеры-работы)
    - [Используемые технологии](#используемые-технологии)
  - [Требования к окружению](#требования-к-окружению)
    - [Параметры проекта](#параметры-проекта)
    - [Организация dev-среды](#организация-dev-среды)
    - [Организация prod-среды](#организация-prod-среды)
  - [Установка](#установка)
    - [Для dev-среды](#для-dev-среды)
    - [Для prod-среды](#для-prod-среды)
      - [Пример запуска](#пример-запуска)

## Описание

Чат-бот с уведомлениями о проверке работ уроков от [Devman](https://dvmn.org/)

### Начало работы

* Необходимо и достаточно:
  - получить токен для чат-бота (далее по тексту, бот) у [BotFather](https://t.me/botfather),
  - получить `chat_id` у [бота](https://t.me/userinfobot),
  - зарегистрироваться на [сайте Devman](https://dvmn.org/),
  - получить токен аутентификации для работы с [API Devman](https://dvmn.org/api/docs/).

### Особенности

- представляет собой альтернативу веб-интерфейсу в виде бота, доступному в профиле [сайта Devman](https://dvmn.org/), который присылает уведомления, используя realtime-технологию _long polling_,
- присылает кастомизированные сообщения П-лю, которые позволяют чётко понять: какую работу проверили и каков результат проверки,
- взаимодействует с long polling-частью [API Devman](https://dvmn.org/api/docs/),
- осуществляет запись событий, отражающих ход работы бота, в журнал.

## Примеры работы

  **Ответ бота при положительном результате проверки:**

  ![success_status_of_lesson_check](https://github.com/Padking/robotic-notifier/blob/master/screenshots/success_status_of_lesson_check.png)


  **Ответ бота при отсутствии результатов проверки:**

  ![no_proven_lessons](https://github.com/Padking/robotic-notifier/blob/master/screenshots/no_proven_lessons.png)


### Используемые технологии

* [requests](https://requests.readthedocs.io/en/master/)
* [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/en/stable/)

## Требования к окружению

* Python 3.8 и выше,
* Linux/Windows,
* Переменные окружения (ПеО),
* Файл службы подсистемы инициализации _systemd_.

Проект настраивается через ПеО, достаточно указать их в файле `.env`.

Передача значений ПеО происходит с использованием [environs](https://pypi.org/project/environs/).

Prod-среда использует файл `bot.service`.

### Параметры проекта

|       Ключ        |     Назначение     |   По умолчанию   |
|-------------------|------------------|------------------|
|`TELEGRAM_BOT_API_TOKEN`| Токен для взаимодействия с [Bot API](https://core.telegram.org/bots/api) | — |
|`TELEGRAM_USER_CHAT_ID`| Идентификатор чата для бота и П-ля | — |
|`DEVMAN_API_AUTHORIZATION_TOKEN`| Токен аутентификации для работы с [API Devman](https://dvmn.org/api/docs/) | — |

### Организация dev-среды

- создать на основе `.env.override` файл `.env`,
- заполнить ключи значениями.

### Организация prod-среды

- выполнить пункты из раздела ["Организация dev-среды"](https://github.com/Padking/robotic-notifier#организация-dev-среды),
- отредактировать [файл](https://github.com/Padking/robotic-notifier/blob/master/bot.service).

## Установка

### Для dev-среды

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

- запустить бота:
```sh
python bot.py
```



\* с использованием [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html)


### Для prod-среды

- клонировать проект удобным способом, например, утилитой [scp](https://wiki.debian.org/SSH#scp), с помощью Git и проч.,
- [установить](https://devguide.python.org/setup/#compile-and-build) необходимую версию интерпретатора Python,
- установить менеджер пакетов (pip) для Python:
```sh
apt-get install python3-pip
```
- создать и активировать легковесное ВО:
```sh
cd <project directory>
python -m venv <path to virtual environment directory>
source <virt. environment directory name>/bin/activate
```
- установить зависимости:
```sh
pip install -r requirements.txt
```
- убедиться в работоспособности бота:
```sh
python bot.py
```
- отключить бота после подтверждения работоспособности:
```sh
Ctrl-c
```
- деактивировать ВО:
```sh
deactivate
```
- скорректировать [shebang](https://github.com/Padking/robotic-notifier/blob/master/bot.py#L1) (с учётом особенностей настройки ВО),
- сделать файл исполняемым:
```sh
chmod +x bot.py
```
- копировать файл службы:
```sh
cp ./bot.service /etc/systemd/system
```

#### Пример запуска

```sh
systemctl daemon-reload
systemctl enable bot.service
systemctl start bot.service
systemctl status bot.service
● bot.service - robotic-notifier
   Loaded: loaded (/etc/systemd/system/bot.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2021-12-10 20:08:37 MSK; 4s ago
 Main PID: 9545 (bot.py)
    Tasks: 1 (limit: 2356)
   Memory: 18.1M
   CGroup: /system.slice/bot.service
           └─9545 ... ...

Dec 10 20:08:37 59840 systemd[1]: Started robotic-notifier.
```
