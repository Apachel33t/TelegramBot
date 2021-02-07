from .models import *
from pprint import pprint

# File with SDK telegram by https://github.com/Apachel33t
from .utils import *
# File with messages in different languages for all user (super user, admins, common users, payment users)
from .messages_for_user import *
# File with buttons in different languages
from bot.keyboards.ru_keyboards import *
from bot.keyboards.en_keyboards import *
# File with all kinds of choices in different languages


# Main class which processes webhook from api.telegram.org/bot
class TelegramBot:

    @staticmethod
    def send_input_error_message(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'данные введены не корректно.')
        else:
            en_error_message(chat_object, 'data entered incorrectly.')

    @staticmethod
    def send_success_message(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_success_message(chat_object)
        else:
            en_success_message(chat_object)

    @staticmethod
    def send_error_cannot_delete_project(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'Вы не можете удалить этот проект.')
        else:
            en_error_message(chat_object, "You cannot delete with project.")

    @staticmethod
    def send_edit_keyboard(chat_object, msg):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_decline_keyboard, chat_object.from_id, f'Чтобы отменить действие нажмите 🔙 Назад.\n{msg}')
        else:
            send_keyboard(en_decline_keyboard, chat_object.from_id, f'To decline this action press 🔙 Back to.\n{msg}')

    @staticmethod
    def let_users_choose_role(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_role_keyboard, chat_object.from_id, 'Выберете роль.')
        else:
            send_keyboard(en_role_keyboard, chat_object.from_id, 'Select role.')

    @staticmethod
    def send_his_profile(chat_object):
        user = User.objects.get(external_id=chat_object.from_id)
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_user_profile_keyboard, chat_object.from_id, 'Ваш профиль.')
            ru_send_user_profile(chat_object, user)
        else:
            send_keyboard(en_user_profile_keyboard, chat_object.from_id, 'Your profile.')
            en_send_user_profile(chat_object, user)

    @staticmethod
    def send_create_task_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_create_project_keyboard, chat_object.from_id, 'Введите название проекта')
        else:
            send_keyboard(en_create_project_keyboard, chat_object.from_id, 'Enter title of project')

    @staticmethod
    def send_enter_description_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_create_project_keyboard, chat_object.from_id, 'Введите описание проекта')
        else:
            send_keyboard(en_create_project_keyboard, chat_object.from_id, 'Enter description of project')

    @staticmethod
    def send_accept_create_project(chat_object, client):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_send_project_for_accept(chat_object, client)
            send_keyboard(ru_accept_send_data_withdraw_keyboard, chat_object.from_id, 'Выберете действие.')
        else:
            en_send_project_for_accept(chat_object, client)
            send_keyboard(en_accept_send_data_withdraw_keyboard, chat_object.from_id, 'Select.')

    @staticmethod
    def send_error_cost_incorrect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'цена за проект от 101 до 999 999 рублей.')
        else:
            en_error_message(chat_object, 'cost project range at 101 to 999 999 rub.')

    @staticmethod
    def send_attach_file_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_attach_file_keyboard, chat_object.from_id, 'Прикрепите изображение или файл как документ.')
        else:
            send_keyboard(en_attach_file_keyboard, chat_object.from_id, 'Attach any file or image like document.')

    @staticmethod
    def send_enter_cost_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_create_project_keyboard, chat_object.from_id, 'Введите цену, минимальная цена 101 рубль.')
        else:
            send_keyboard(en_create_project_keyboard, chat_object.from_id, 'Enter cost, at 101 rub.')

    @staticmethod
    def send_project(chat_object, task):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_send_his_project(chat_object, task, ru_edit_project_keyboard)
        else:
            en_send_his_project(chat_object, task, en_edit_project_keyboard)

    @staticmethod
    def send_error_project_attach_file_incorrect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'не зависимо от формата файла или картинки приложите его как документ.')
        else:
            en_error_message(chat_object, 'you must attach file or image like document.')

    @staticmethod
    def send_error_project_description_inccorect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'слишком длинное описание.')
        else:
            en_error_message(chat_object, 'to long description.')

    @staticmethod
    def send_enter_deadline_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_create_project_keyboard, chat_object.from_id, 'Введите сроки проекта в формате дд.мм.гггг')
        else:
            send_keyboard(en_create_project_keyboard, chat_object.from_id, 'Enter deadline of project in format '
                                                                           'dd.mm.yyyy')

    @staticmethod
    def select_a_project_category(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_categories_of_projects, chat_object.from_id, 'Выберете категорию проекта')
        else:
            send_keyboard(en_categories_of_projects, chat_object.from_id, 'Select a project category')

    @staticmethod
    def send_error_project_name_incorrect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'слишком длинное имя.')
        else:
            en_error_message(chat_object, 'to long name.')

    @staticmethod
    def send_error_project_deadline_incorrect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, f'вы ввели не корректную дату. Для ввода требуется дата в формате дд.мм.гггг.\nПример 21.01.2021')
        else:
            en_error_message(chat_object, f'incorrect date. Enter date in format dd.mm.yyyy.\nExample 21.01.2021')

    @staticmethod
    def send_error_category_incorrect(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_error_message(chat_object, 'нужно выбрать имя категории из списка кнопок.')
        else:
            en_error_message(chat_object, 'you must select category in buttons list.')

    @staticmethod
    def send_customer_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_customer_choose_keyboard, chat_object.from_id, 'Выбранный профиль: Заказчик.')
        else:
            send_keyboard(en_customer_choose_keyboard, chat_object.from_id, 'Current profile: Customer.')

    @staticmethod
    def send_main_keyboard(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            send_keyboard(ru_common_user_keyboard, chat_object.from_id, 'Главная панель.')
        else:
            send_keyboard(en_common_user_keyboard, chat_object.from_id, 'Main panel.')

    @staticmethod
    def send_help_message(chat_object):
        if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
            ru_send_help_message(chat_object)
        else:
            en_send_help_message(chat_object)

    @staticmethod
    def authenticate_user(chat_object):
        if chat_object.msg_text == '🇬🇧 English':
            if User.objects.filter(external_id=chat_object.from_id).exists():
                user = User.objects.get(external_id=chat_object.from_id)
                user.current_lang = 'EN'
                user.save()
            else:
                User.objects.create_user(chat_object.from_id, 'EN', chat_object.username, 'user')
            en_greeting_message(chat_object)
        elif chat_object.msg_text == '🇷🇺 Русский':
            if User.objects.filter(external_id=chat_object.from_id).exists():
                user = User.objects.get(external_id=chat_object.from_id)
                user.current_lang = 'RU'
                user.save()
            else:
                User.objects.create_user(chat_object.from_id, 'RU', chat_object.username, 'user')
            ru_greeting_message(chat_object)
