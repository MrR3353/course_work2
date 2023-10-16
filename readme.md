# Курсовая работа по теме "Планировщик задач"

## Стек:
* Django
* Celery
* Redis
* Aiogram
* MDBootstrap
* Chart.js

## Запуск:
Перед запуском необходимо добавить в корневую папку todoapp файл `.env` с переменными среды, например:

```
API_TOKEN=
CHROME_DRIVER=
```
В `API_TOKEN` указать токен от Telegram бота

В `CHROME_DRIVER` указать путь к chromedriver.exe


Запуск Redis
```sh
"Redis-x64-5.0.14.1/start_redis.bat"
``` 

Установка зависимостей:  
```sh
pip install -r requirements.txt  
```
Все команды выполняются из корневой директории `course_work2`

Запуск сервера:
```sh
cd todoapp && python manage.py runserver
```

Запуск бота:
```sh
cd todoapp && python tgbot.py
```

Запуск celery:
```sh
cd todoapp && celery -A todoapp.celery_task:celery worker --loglevel=INFO --pool=solo
```
```sh
cd todoapp && celery -A todoapp.celery_task:celery beat --loglevel=INFO
```

Запуск flower:
```sh
cd todoapp && celery -A todoapp.celery_task:celery flower
```

Запуск теста:
```sh
cd todoapp/tests && python test.py
```