from ..services import TelegramBot
from ..cases import *
from ..models import *
from ..messages_for_user import *
from ..keyboards.ru_keyboards import *
from ..keyboards.en_keyboards import *
from pprint import pprint
from datetime import datetime, date, timedelta


class UserProjects(TelegramBot):

    @staticmethod
    def switch_user_projects(chat_object, position, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_main_keyboard(chat_object)
            UserProjects.delAll(chat_object, client)
        if chat_object.msg_text in im_customer:
            TelegramBot.send_customer_keyboard(chat_object)
            client.hset(f"user:{chat_object.from_id}", "action", "im_customer")
        elif chat_object.msg_text in im_performer:
            client.hset(f"user:{chat_object.from_id}", "action", "im_performer")
        elif chat_object.msg_text in in_process:
            UserProjects.get_customer_project(chat_object, client)
            client.hset(f"user:{chat_object.from_id}", "action", "in_process")
        elif client.hexists(f"user:{chat_object.from_id}", "action") is not False:
            if client.hget(f"user:{chat_object.from_id}", "action") == b"im_customer":
                UserProjects.im_customer(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"im_performer":
                UserProjects.im_performer(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"create_task":
                UserProjects.create_task(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"in_process":
                UserProjects.in_process(chat_object, client)

    @staticmethod
    def delAll(chat_object, client):
        client.hdel(f"user:{chat_object.from_id}", "action")
        client.hdel(f"user:{chat_object.from_id}", "project_name")
        client.hdel(f"user:{chat_object.from_id}", "project_file")
        client.hdel(f"user:{chat_object.from_id}", "project_filename")
        client.hdel(f"user:{chat_object.from_id}", "project_cost")
        client.hdel(f"user:{chat_object.from_id}", "project_category")
        client.hdel(f"user:{chat_object.from_id}", "project_file_status")
        client.hdel(f"user:{chat_object.from_id}", "project_description")


    # Start Customer
    @staticmethod
    def im_customer(chat_object, client):
        if chat_object.msg_text in create_task:
            client.hset(f"user:{chat_object.from_id}", "action", "create_task")
            TelegramBot.send_create_task_keyboard(chat_object)

    @staticmethod
    def get_customer_project(chat_object, client):
        projects = []
        project = list(ProjectsByTelegramUser.objects.filter(external_id=chat_object.from_id).values())
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            projects.append(['🔙 Назад'])
        else:
            projects.append(['🔙 Back to'])
        for item in project:
            projects.append([f'{item.get("title")}@{item.get("id")}@{item.get("external_id")}'])
        empty_keyboard.update({"keyboard": projects})
        pprint(empty_keyboard)
        send_keyboard(empty_keyboard, chat_object.from_id, '.')
        client.hset(f"user:{chat_object.from_id}", "action", "in_process")

    @staticmethod
    def in_process(chat_object, client):
        if chat_object.msg_text.find("@") != -1:
            try:
                task_str = chat_object.msg_text.split("@")
                task = ProjectsByTelegramUser.objects.get(id=task_str[1])
                client.hset(f"user:{chat_object.from_id}", "task_id", task_str[1])
                TelegramBot.send_project(chat_object, task)
            except:
                print('Something went wrong')
        elif chat_object.msg_text in delete:
            try:
                project_id = str(client.hget(f"user:{chat_object.from_id}", "task_id"), "utf-8")
                project = ProjectsByTelegramUser.objects.filter(id=project_id)
                project.delete()
                TelegramBot.send_success_message(chat_object)
                TelegramBot.send_customer_keyboard(chat_object)
            except:
                TelegramBot.send_error_cannot_delete_project(chat_object)


    @staticmethod
    def create_task(chat_object, client):
        if client.hexists(f"user:{chat_object.from_id}", "project_name") is False:
            if len(chat_object.msg_text) < 256:
                client.hset(f"user:{chat_object.from_id}", "project_name", chat_object.msg_text)
                TelegramBot.select_a_project_category(chat_object)
            else:
                TelegramBot.send_error_project_name_incorrect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_name") is True \
                and client.hexists(f"user:{chat_object.from_id}", "project_category") is False:
            pprint(chat_object.msg_text)
            if chat_object.msg_text in categories:
                client.hset(f"user:{chat_object.from_id}", "project_category", chat_object.msg_text)
                TelegramBot.send_enter_description_keyboard(chat_object)
            else:
                TelegramBot.send_error_category_incorrect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_category") is True \
                and client.hexists(f"user:{chat_object.from_id}", "project_description") is False:
            if len(chat_object.msg_text) < 1024:
                client.hset(f"user:{chat_object.from_id}", "project_description", chat_object.msg_text)
                TelegramBot.send_enter_deadline_keyboard(chat_object)
            else:
                TelegramBot.send_error_project_description_inccorect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_description") is True \
                and client.hexists(f"user:{chat_object.from_id}", "project_deadline") is False:
            try:
                if date.today() < datetime.strptime(chat_object.msg_text, "%d.%m.%Y").date():
                    client.hset(f"user:{chat_object.from_id}", "project_deadline", chat_object.msg_text)
                    TelegramBot.send_attach_file_keyboard(chat_object)
            except:
                TelegramBot.send_error_project_deadline_incorrect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_deadline") is True \
                and client.hexists(f"user:{chat_object.from_id}", "project_file") is False:
            try:
                if chat_object.msg_text in dont_attach:
                    TelegramBot.send_enter_cost_keyboard(chat_object)
                    client.hset(f"user:{chat_object.from_id}", "project_file_status", 'empty')
                    client.hset(f"user:{chat_object.from_id}", "project_file", 'empty')
                    client.hset(f"user:{chat_object.from_id}", "project_filename", 'empty')
                elif len(chat_object.file_id) > 60:
                    client.hset(f"user:{chat_object.from_id}", "project_file_status", chat_object.file_id)
                    client.hset(f"user:{chat_object.from_id}", "project_file", chat_object.file_id)
                    client.hset(f"user:{chat_object.from_id}", "project_filename", chat_object.file_name)
                    TelegramBot.send_enter_cost_keyboard(chat_object)
            except:
                TelegramBot.send_error_project_attach_file_incorrect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_file_status") is True and \
                client.hexists(f"user:{chat_object.from_id}", "project_cost") is False:
            try:
                if len(chat_object.msg_text) > 2:
                    client.hset(f"user:{chat_object.from_id}", "project_cost", chat_object.msg_text)
                    TelegramBot.send_accept_create_project(chat_object, client)
            except:
                TelegramBot.send_error_cost_incorrect(chat_object)
        elif client.hexists(f"user:{chat_object.from_id}", "project_cost") is True and chat_object.msg_text in accept:
            UserProjects.creating_task(chat_object, client)

    @staticmethod
    def creating_task(chat_object, client):
        try:
            title = str(client.hget(f"user:{chat_object.from_id}", "project_name"), "utf-8")
            file = str(client.hget(f"user:{chat_object.from_id}", "project_file"), "utf-8")
            filename = str(client.hget(f"user:{chat_object.from_id}", "project_filename"), "utf-8")
            deadline = str(client.hget(f"user:{chat_object.from_id}", "project_deadline"), "utf-8")
            deadline = datetime.strptime(deadline, "%d.%m.%Y").date()
            print(deadline)
            cost = str(client.hget(f"user:{chat_object.from_id}", "project_cost"), "utf-8")
            category = str(client.hget(f"user:{chat_object.from_id}", "project_category"), "utf-8")
            description = str(client.hget(f"user:{chat_object.from_id}", "project_description"), "utf-8")
            ProjectsByTelegramUser.objects.create_project(chat_object.from_id, title, file, filename, cost, category, description, deadline)
            UserProjects.delAll(chat_object, client)
            TelegramBot.send_success_message(chat_object)
            TelegramBot.send_customer_keyboard(chat_object)
        except Exception:
            print('Cannot create project, error: creating_task')

    # End Customer

    # Start Performer
    @staticmethod
    def im_performer(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_main_keyboard(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
    # End Performer
