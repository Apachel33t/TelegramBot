from django.core.management.base import BaseCommand

import requests

from settings.local_settings import *

class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        r = requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook')
        print(r.status_code)
        print(r.text)
