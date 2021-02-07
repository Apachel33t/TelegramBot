from ..services import TelegramBot
from ..cases import *
from ..models import *
from ..messages_for_user import *
from ..keyboards.ru_keyboards import *
from ..keyboards.en_keyboards import *
from pprint import pprint


class UserProjects(TelegramBot):

    @staticmethod
    def switch_user_projects(chat_object, position, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_main_keyboard(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
        if chat_object.msg_text in im_customer:
            TelegramBot.send_customer_keyboard(chat_object)
            client.hset(f"user:{chat_object.from_id}", "action", "im_customer")
        elif chat_object.msg_text in im_performer:
            client.hset(f"user:{chat_object.from_id}", "action", "im_performer")
        elif client.hexists(f"user:{chat_object.from_id}", "action") is not False:
            if client.hget(f"user:{chat_object.from_id}", "action") == b"im_customer":
                UserProjects.im_customer(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"im_performer":
                UserProjects.im_performer(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"create_task":
                UserProjects.create_task(chat_object, client)

    # Start Customer
    @staticmethod
    def im_customer(chat_object, client):
        if chat_object.msg_text in create_task:
            client.hset(f"user:{chat_object.from_id}", "action", "create_task")
            TelegramBot.send_create_task_keyboard(chat_object)


    @staticmethod
    def create_task(chat_object, client):
        pass

    # End Customer


    # Start Performer
    @staticmethod
    def im_performer(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_main_keyboard(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
    # End Performer
