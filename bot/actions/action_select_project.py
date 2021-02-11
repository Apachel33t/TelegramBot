from ..services import TelegramBot
from ..cases import *
from ..models import *
from ..messages_for_user import *
from ..keyboards.ru_keyboards import *
from ..keyboards.en_keyboards import *
from pprint import pprint
from datetime import datetime, date, timedelta


class SelectProject(TelegramBot):

    @staticmethod
    def switch_select_project(chat_object, position, client):
        if chat_object.msg_text in categories:
            client.hset(f"user:{chat_object.from_id}", "offset", 0)
            client.hset(f"user:{chat_object.from_id}", "current_category", chat_object.msg_text)
            count = SelectProject.return_count_of_items(chat_object.msg_text)
            client.hset(f"user:{chat_object.from_id}", "count", count)
            SelectProject.send_project_for_user(chat_object, client, 0)
        elif client.hget(f"user:{chat_object.from_id}", "enter_offer") is not None:
            SelectProject.input_offer(chat_object, client)
        elif client.hget(f"user:{chat_object.from_id}", "current_category") is not None:
            SelectProject.switch_projects(chat_object, client)
        elif chat_object.msg_text in back_to:
            SelectProject.del_all(chat_object, client)
            TelegramBot.send_main_keyboard(chat_object)

    @staticmethod
    def switch_projects(chat_object, client):
        if chat_object.msg_text in back_to:
            SelectProject.del_all(chat_object, client)
            TelegramBot.select_a_project_category(chat_object)
        elif chat_object.msg_text in respond:
            SelectProject.enter_offer(chat_object, client)
        elif chat_object.msg_text in next:
            offset = int(client.hget(f"user:{chat_object.from_id}", "offset"))
            offset = offset + 1
            if int(client.hget(f"user:{chat_object.from_id}", "count")) > offset:
                client.hset(f"user:{chat_object.from_id}", "offset", offset)
                SelectProject.send_project_for_user(chat_object, client, offset)
            else:
                TelegramBot.that_was_last_task(chat_object)
        elif chat_object.msg_text in prev:
            offset = int(client.hget(f"user:{chat_object.from_id}", "offset"))
            offset = offset - 1
            if offset >= 0:
                client.hset(f"user:{chat_object.from_id}", "offset", offset)
                SelectProject.send_project_for_user(chat_object, client, offset)
            else:
                TelegramBot.that_was_last_task(chat_object)


    @staticmethod
    def input_offer(chat_object, client):
        if len(chat_object.msg_text) < 1024:
            to = str(client.hget(f"user:{chat_object.from_id}", "customer_id"), "UTF-8")
            OffersToCustomer.objects.create_offer(chat_object.from_id, to, chat_object.msg_text)
            TelegramBot.send_notify_to_user(chat_object, to, client)
            print('Norm')
            offset = int(client.hget(f"user:{chat_object.from_id}", "offset"))
            client.hdel(f"user:{chat_object.from_id}", "enter_offer")
            SelectProject.send_project_for_user(chat_object, client, offset)
        else:
            TelegramBot.send_error_project_name_incorrect(chat_object)

    @staticmethod
    def enter_offer(chat_object, client):
        if chat_object.msg_text in back_to:
            offset = int(client.hget(f"user:{chat_object.from_id}", "offset"))
            SelectProject.send_project_for_user(chat_object, client, offset)
            client.hdel(f"user:{chat_object.from_id}", "enter_offer")
            client.hdel(f"user:{chat_object.from_id}", "project_name_customer")
        else:
            client.hset(f"user:{chat_object.from_id}", "enter_offer", chat_object.msg_text)
            TelegramBot.send_enter_offer(chat_object)

    @staticmethod
    def del_all(chat_object, client):
        client.hdel(f"user:{chat_object.from_id}", "offset")
        client.hdel(f"user:{chat_object.from_id}", "current_category")
        client.hdel(f"user:{chat_object.from_id}", "count")
        client.hdel(f"user:{chat_object.from_id}", "customer_id")
        client.hdel(f"user:{chat_object.from_id}", "project_name_customer")

    @staticmethod
    def send_project_for_user(chat_object, client, offset):
        category = str(client.hget(f"user:{chat_object.from_id}", "current_category"), 'UTF-8')
        projects = SelectProject.return_projects_list_by_deadline(category, offset)
        client.hset(f"user:{chat_object.from_id}", "customer_id", projects[0].get('external_id'))
        client.hset(f"user:{chat_object.from_id}", "project_name_customer", projects[0].get('title'))
        TelegramBot.prev_next_keyboard(chat_object, projects[0])

    @staticmethod
    def return_projects_list_by_deadline(category, offset):
        offset_more = offset + 1
        today = date.today().strftime("%Y-%m-%d")
        return list(ProjectsByTelegramUser.objects.filter(deadline__range=(today, "2100-04-09"), category=category, status='waiting').values()[offset:offset_more])

    @staticmethod
    def return_count_of_items(category):
        today = date.today().strftime("%Y-%m-%d")
        return len(list(ProjectsByTelegramUser.objects.filter(deadline__range=(today, "2100-04-09"), category=category, status='waiting').values()))
