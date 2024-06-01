import requests
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Сообщение успешно отправлено в Telegram')
    else:
        print('Ошибка', response.text)

