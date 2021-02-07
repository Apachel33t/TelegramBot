from ..services import TelegramBot
from ..cases import *
from ..models import *
from ..messages_for_user import *
from ..keyboards.ru_keyboards import *
from ..keyboards.en_keyboards import *
from pprint import pprint


class ActionProfile(TelegramBot):

    @staticmethod
    def switch_profile(chat_object, position, client):
        if chat_object.msg_text in back_to and client.hexists(f"user:{chat_object.from_id}", "action") is False:
            TelegramBot.send_main_keyboard(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "position")
        elif chat_object.msg_text in edit_email:
            client.hset(f"user:{chat_object.from_id}", "action", "edit_my_email")
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                TelegramBot.send_edit_keyboard(chat_object, "Введите e-mail.")
            else:
                TelegramBot.send_edit_keyboard(chat_object, "Enter e-mail.")
        elif chat_object.msg_text in edit_name:
            client.hset(f"user:{chat_object.from_id}", "action", "edit_my_name")
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                TelegramBot.send_edit_keyboard(chat_object, "Введите имя.")
            else:
                TelegramBot.send_edit_keyboard(chat_object, "Enter name.")
        elif chat_object.msg_text in withdraw_funds:
            client.hset(f"user:{chat_object.from_id}", "action", "withdraw_cash")
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                TelegramBot.send_edit_keyboard(chat_object, "Введите сумму которую хотие вывести.")
            else:
                TelegramBot.send_edit_keyboard(chat_object, "Enter the amount you want to withdraw.")
        elif chat_object.msg_text in top_up_balance:
            client.hset(f"user:{chat_object.from_id}", "action", "top_up_balance")
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                ru_send_user_about_balance(chat_object)
                TelegramBot.send_edit_keyboard(chat_object, "Введите сумму.")
            else:
                en_send_user_about_balance(chat_object)
                TelegramBot.send_edit_keyboard(chat_object, "Enter sum.")
        elif client.hexists(f"user:{chat_object.from_id}", "action") is not False:
            if client.hget(f"user:{chat_object.from_id}", "action") == b"edit_my_email":
                ActionProfile.edit_my_email(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"edit_my_name":
                ActionProfile.edit_my_name(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"top_up_balance":
                ActionProfile.top_up_balance(chat_object, client)
            elif client.hget(f"user:{chat_object.from_id}", "action") == b"withdraw_cash":
                ActionProfile.withdraw_cash(chat_object, client)

    @staticmethod
    def withdraw_cash(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_his_profile(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
            client.hdel(f"user:{chat_object.from_id}", "sum")
            client.hdel(f"user:{chat_object.from_id}", "bank_name")
            client.hdel(f"user:{chat_object.from_id}", "phone_or_card")
        elif len(chat_object.msg_text) > 2 and client.hexists(f"user:{chat_object.from_id}", "sum") is False:
            client.hset(f"user:{chat_object.from_id}", "sum", chat_object.msg_text)
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                ru_send_please_bank_nam(chat_object)
            else:
                en_send_please_bank_nam(chat_object)
        elif len(chat_object.msg_text) > 2 and client.hexists(f"user:{chat_object.from_id}", "bank_name") is False:
            client.hset(f"user:{chat_object.from_id}", "bank_name", chat_object.msg_text)
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                ru_send_please_phone_or_chard_num(chat_object)
            else:
                en_send_please_phone_or_chard_num(chat_object)
        elif 10 < len(chat_object.msg_text) < 17 and client.hexists(f"user:{chat_object.from_id}", "phone_or_card") is False:
            client.hset(f"user:{chat_object.from_id}", "phone_or_card", chat_object.msg_text)
            if client.hget(f"user:{chat_object.from_id}", "phone_or_card") == 11:
                phone = client.hget(f"user:{chat_object.from_id}", "phone_or_card")
                card = False
            else:
                card = client.hget(f"user:{chat_object.from_id}", "phone_or_card")
                phone = False
            sum_with = client.hget(f"user:{chat_object.from_id}", "sum")
            bank_name = client.hget(f"user:{chat_object.from_id}", "bank_name")
            if User.objects.filter(external_id=chat_object.from_id, current_lang="RU"):
                send_keyboard(ru_accept_send_data_withdraw_keyboard, chat_object.from_id, ru_check_input_withdraw(sum_with, bank_name, phone, card))
            else:
                send_keyboard(en_accept_send_data_withdraw_keyboard, chat_object.from_id, en_check_input_withdraw(sum_with, bank_name, phone, card))
        elif client.hexists(f"user:{chat_object.from_id}", "phone_or_card") and chat_object.msg_text in accept:
            if client.hget(f"user:{chat_object.from_id}", "phone_or_card") == 11:
                phone = client.hget(f"user:{chat_object.from_id}", "phone_or_card")
                card = None
            else:
                card = client.hget(f"user:{chat_object.from_id}", "phone_or_card")
                phone = None
            UserRequestWithdrawCash.objects.create_request(chat_object.from_id,
                                                           client.hget(f"user:{chat_object.from_id}", "sum"),
                                                           client.hget(f"user:{chat_object.from_id}", "bank_name"),
                                                           card, phone)
            client.hdel(f"user:{chat_object.from_id}", "action")
            client.hdel(f"user:{chat_object.from_id}", "sum")
            client.hdel(f"user:{chat_object.from_id}", "bank_name")
            client.hdel(f"user:{chat_object.from_id}", "phone_or_card")
            TelegramBot.send_his_profile(chat_object)
        else:
            TelegramBot.send_input_error_message(chat_object)

    @staticmethod
    def top_up_balance(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_his_profile(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
        elif len(chat_object.msg_text) > 2:
            UserRequestTopOfBalance.objects.create_balance_request(chat_object.from_id, chat_object.msg_text)
            client.hdel(f"user:{chat_object.from_id}", "action")
            TelegramBot.send_his_profile(chat_object)
        else:
            TelegramBot.send_input_error_message(chat_object)

    @staticmethod
    def edit_my_name(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_his_profile(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
        elif len(chat_object.msg_text) > 3:
            user = User.objects.get(external_id=chat_object.from_id)
            user.fullname = chat_object.msg_text
            user.save()
            client.hdel(f"user:{chat_object.from_id}", "action")
            TelegramBot.send_his_profile(chat_object)
        else:
            TelegramBot.send_input_error_message(chat_object)

    @staticmethod
    def edit_my_email(chat_object, client):
        if chat_object.msg_text in back_to:
            TelegramBot.send_his_profile(chat_object)
            client.hdel(f"user:{chat_object.from_id}", "action")
        elif chat_object.msg_text.find("@") != -1:
            user = User.objects.get(external_id=chat_object.from_id)
            user.email = chat_object.msg_text
            user.save()
            client.hdel(f"user:{chat_object.from_id}", "action")
            TelegramBot.send_his_profile(chat_object)
        else:
            TelegramBot.send_input_error_message(chat_object)

