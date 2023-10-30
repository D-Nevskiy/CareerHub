import os

import requests
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail

from careerhub.settings import DEFAULT_FROM_EMAIL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerhub.settings')

app = Celery('careerhub')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def send_activation_email(activation_link, recipient_list):
    """
    Отправляет письмо со ссылкой активации пользователю.

    :param activation_link: Ссылка для активации аккаунта.
    :param recipient_list: Список получателей письма.
    :return: None
    """
    subject = 'Активация аккаунта в сервисе Яндекс.Найм'
    message = ('Пожалуйста, активируйте свой аккаунт чтобы '
               'начать пользоваться сервисом.')
    message += (f'\nАктивируйте ваш аккаунт, перейдя по следующей '
                f'ссылке:\nhttps://tracker-hiring.ddns.net{activation_link}')
    from_email = DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list)


@app.task()
def activate_user(uid, token):
    """
    Активирует пользователя с заданным UID и токеном.

    :param uid: Уникальный идентификатор пользователя.
    :param token: Токен активации.
    :return: Ответ, указывающий на успешную активацию или ошибку.
    """
    payload = {'uid': uid, 'token': token}
    url = "http://backend:8000/api/users/activation/"
    response = requests.post(url, data=payload)
    return response
