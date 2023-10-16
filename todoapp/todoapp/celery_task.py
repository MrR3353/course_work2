import datetime
import os

import django
from pytz import utc

# settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")
django.setup()

from tgbot import send_notification
from todolist.models import Category, ToDo
from django.contrib.auth.models import User

from .settings import CELERY_ON

from celery import Celery


celery = Celery(
    'worker',
    # backend='redis://localhost:6379',
    # broker='amqp://localhost:5672'
    broker='redis://localhost:6379',
)

celery.conf.timezone = 'Europe/Moscow'


def send_message(tg_chat_id, todo):
    text = f'Привет! У тебя запланирована задача {todo.title}, она начнется в {(todo.starts + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")}'
    send_notification(tg_chat_id, text)


@celery.task
def task():
    print('TASK')
    users = User.objects.all()
    for user in users:
        if user.profile.is_notifications and user.profile.tg_chat_id:
            categories = Category.objects.filter(user=user)
            for category in categories:
                todos = ToDo.objects.filter(category=category)
                for todo in todos:
                    if todo.starts:
                        if todo.num_notifications == 0:
                            starts = todo.starts + datetime.timedelta(hours=3)
                            now = utc.localize(datetime.datetime.now())
                            if starts <= now + datetime.timedelta(minutes=user.profile.time_before_notification):
                                send_message(user.profile.tg_chat_id, todo)
                                todo.num_notifications += 1
                                todo.save()


if CELERY_ON:
    celery.add_periodic_task(10, task.s(), name='send notifications')


# celery -A todoapp.celery_task:celery worker --loglevel=INFO --pool=solo
# celery -A todoapp.celery_task:celery beat --loglevel=INFO
# celery -A todoapp.celery_task:celery flower
