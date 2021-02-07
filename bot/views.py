from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint

import redis
# File with messages in different languages for all user (super user, admins, common users, payment users)
from .messages_for_user import *
# File with buttons in different languages
from bot.keyboards.ru_keyboards import *
from bot.keyboards.en_keyboards import *
# File with all kinds of choices in different languages
from .cases import *
from .services import TelegramBot
# Actions
from .actions.action_profile import ActionProfile
from .actions.action_user_projects import UserProjects

# Redis usage in this project like something between "state" or "session"
client = redis.Redis(host='127.0.0.1', port=6379)


# Main class which processes webhook from api.telegram.org/bot
class TelegramBotController(HttpRequest):

    @csrf_exempt
    @require_http_methods(["GET", "POST"])
    def get_update(request):
        try:
            chat_object = ReturnTelegramChatObjects(request)
            TelegramBotController.switch(chat_object)
        except Exception:
            print(ERROR_WHEN_ENCAPSULATE_OBJECT)
        return HttpResponse(ok)

    @staticmethod
    def switch(chat_object):
        if chat_object.msg_text == '/start':
            send_keyboard(ru_switch_lang_keyboard, chat_object.from_id, select_language)
        elif chat_object.msg_text in switch_lang_case:
            try:
                client.hdel(f"user:{chat_object.from_id}", "position")
                client.hdel(f"user:{chat_object.from_id}", "action")
                TelegramBot.authenticate_user(chat_object)
                TelegramBot.send_main_keyboard(chat_object)
            except Exception:
                print(ERROR_WHEN_TRYING_CREATE_OR_AUTHENTICATE_USER)
        elif chat_object.msg_text in choose_project:
            pass
        elif chat_object.msg_text in my_profile:
            client.hset(f"user:{chat_object.from_id}", "position", "my_profile_user")
            TelegramBot.send_his_profile(chat_object)
        elif chat_object.msg_text in my_projects:
            client.hset(f"user:{chat_object.from_id}", "position", "common_user_projects")
            TelegramBot.let_users_choose_role(chat_object)
        elif chat_object.msg_text in help_to_user:
            TelegramBot.send_help_message(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "position") is not False:
            position = client.hget(f"user:{chat_object.from_id}", "position")
            TelegramBotController.switch_secondary(chat_object, position)

    @staticmethod
    def switch_secondary(chat_object, position):
        if position == b'my_profile_user':
            try:
                ActionProfile.switch_profile(chat_object, position, client)
            except Exception:
                print('Exception in switch_profile')
        elif position == b'common_user_projects':
            try:
                UserProjects.switch_user_projects(chat_object, position, client)
            except Exception:
                print('Exception in common_user_projects')
        else:
            pprint('ELSE')
