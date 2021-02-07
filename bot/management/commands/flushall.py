from django.core.management.base import BaseCommand

import redis

# COMMAND flushall for clear all key-value in redis
# Redis usage in this project like something between "state" or "session"
client = redis.Redis(host='127.0.0.1', port=6379)


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **options):
        try:
            client.flushall()
            print('Success')
        except Exception:
            print("Something went wrong.")
