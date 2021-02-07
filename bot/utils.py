from django.conf import settings
#from pprint import pprint

import requests
import json


def send_message(msg, chat_id):
    requests.get(f'{settings.URL}sendMessage?chat_id={chat_id}&text={msg}')


def send_keyboard(buttons, chat_id, msg):
    buttons = json.dumps(buttons)
    requests.get(f'{settings.URL}sendMessage?chat_id={chat_id}&text={msg}&reply_markup={buttons}')


def get_file(file_id):
    response = requests.get(f'{settings.URL}getFile?file_id={file_id}')
    response = json.loads(response.content)
    return response["result"]["file_path"]


def send_file(file_id, chat_id, file_name):
    requests.get(f'{settings.URL}sendDocument?chat_id={chat_id}&document={file_id}')


def download_file(file_name, file_path):
    response = requests.get(f'{settings.URL_DOWNLOAD}{file_path}', allow_redirects=True)
    open(file_name, 'wb').write(response.content)


class ReturnTelegramChatObjects:

    def __init__(self, request):
        req = json.loads(request.body)
        if 'document' in req:
            self.file_id = req['message']['document']['file_id']
            self.file_name = req['message']['document']['file_name']
            self.msg_text = None
            get_file(self.file_id)
        elif 'text' in req['message']:
            self.msg_text = req['message']['text']
            self.file_id = None
            self.file_name = None
        self.from_id = req['message']['from']['id']
        self.username = req['message']['from']['username']
