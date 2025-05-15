import requests
from requests import RequestException

from Coursework_6_DRF.settings import BOT_TOKEN, TG_URL

bot_token = BOT_TOKEN


def send_notification(text, chat_id):
    """ Отправляет сообщение через Telegram """
    params = {
        'text': text,
        'chat_id': chat_id
    }
    try:
        response = requests.get(f'{TG_URL}{bot_token}/sendMessage', params=params)
        response.raise_for_status()
    except RequestException as e:
        print(f'Ошибка при отправке  уведомления: {e}')
