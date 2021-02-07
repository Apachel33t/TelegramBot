from django.core.management.base import BaseCommand

from bot.models import *

import secrets


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        key = secrets.token_urlsafe(16)
        #Secret.keys.create(key=key)
        #print(key)
