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
            send_keyboard(ru_accept_send_data_withdraw_keyboard, chat_object.from_id, 'Введите название проекта')
        else:
            send_keyboard(en_accept_send_data_withdraw_keyboard, chat_object.from_id, 'Enter title of project')

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
