from .utils import *

# File with messages, statuses, error messages in different languages
# for all user (super user, admins, common users, payment users)


# For TelegramBot class
# Errors and Exceptions

ERROR_WHEN_ENCAPSULATE_OBJECT = 'Something went wrong when bot try encapsulate object.'

ERROR_WHEN_TRYING_CREATE_OR_AUTHENTICATE_USER = 'Cannot determine or create account for user'

# For TelegramBot class
# Responses Statuses

ok = 'success'

# For TelegramBot class
# Messages for users

select_language = 'Выберете язык\nSelect lang'


def ru_greeting_message(chat_object):
    send_message(f'Здравствуйте {chat_object.username}\n'
                 f'Добро пожаловать в команду топовых фрилансеров!\n\n'
                 f'Отлично!\n\n'
                 f'"✅ Выбрать проект" - нажмите на эту кнопку, чтобы посмотреть доступные проекты,\n'
                 f'"👤 Мой профиль" - нажмите на эту кнопку, чтобы посмотреть информаци о вашем профиле,\n'
                 f'"📝 Мои проекты" - нажмите на эту кнопку, чтобы посмотреть проекты, над которыми вы работаете,\n'
                 f'"❓ Помощь" - нажмите на эту кнопку, чтобы перейти в чат с онлайн-консультантом,\n',
                 chat_object.from_id)


def en_greeting_message(chat_object):
    send_message(f'Greeting {chat_object.username}\n\n'
                 f'Welcome to the top team freelancers!\n\n'
                 f'Excellent!\n\n'
                 f'"✅ Select project" - click on this button to see available projects,\n'
                 f'"👤 My profile" - click on this button to view your profile information,\n'
                 f'"📝 My projects" - click on this button to view the projects you are working on,\n'
                 f'"❓ Help" - click on this button to go to a chat with an online consultant,\n',
                 chat_object.from_id)


def ru_check_input_withdraw(sum_withdraw, name_bank, phone=False, card=False):
    if phone is not False:
        return f'Сумма {sum_withdraw}\nНаименование банка {name_bank}\nНомер телефона {phone}'
    elif card is not False:
        return f'Сумма {sum_withdraw}\nНаименование банка {name_bank}\nНомер карты {card}'


def en_check_input_withdraw(sum_withdraw, name_bank, phone=False, card=False):
    if phone is not False:
        return f'Sum {sum_withdraw}\nName of bank {name_bank}\nPhone number {phone}'
    elif card is not False:
        return f'Sum {sum_withdraw}\nName of bank {name_bank}\nCard number {card}'


def ru_send_user_about_balance(chat_object):
    send_message(f'Карта хуярта раз: {chat_object.from_id}\n'
                 f'Карта хуярта два: {chat_object.username}\n'
                 f'Мне впадлу думать за тебя думай что тут писать и продумывай', chat_object.from_id)


def en_send_user_about_balance(chat_object):
    send_message(f'Карта хуярта first: {chat_object.from_id}\n'
                 f'Карта хуярта second: {chat_object.username}\n'
                 f'Мне впадлу думать за тебя думай что тут писать и продумывай', chat_object.from_id)


def ru_send_user_profile(chat_object, user):
    send_message(f'Ваш telegram ID: {chat_object.from_id}\n'
                 f'Никнейм в telegram: {chat_object.username}\n'
                 f'Имя: {user.fullname}\n'
                 f'E-Mail: {user.email}\n'
                 f'Выполненные проекты: Projects::DoesNotExists\n'
                 f'Проекты в работе: UserProjects::DoesNotExists\n'
                 f'Уровень заказчика: func_payer::DoesNotExists\n'
                 f'Уровень исполнителя: func_worker::DoesNotExists\n'
                 f'Ваш баланс: 0 рублей', chat_object.from_id)


def en_send_user_profile(chat_object, user):
    send_message(f'Your telegram ID: {chat_object.from_id}\n'
                 f'Username в telegram: {chat_object.username}\n'
                 f'Name: {user.fullname}\n'
                 f'E-Mail: {user.email}\n'
                 f'Completed projects: Projects::DoesNotExists\n'
                 f'Projects in progress: UserProjects::DoesNotExists\n'
                 f'Executor Level: func_payer::DoesNotExists\n'
                 f'Customer Level: func_worker::DoesNotExists\n'
                 f'Your balance: 0 rub', chat_object.from_id)


def ru_send_please_phone_or_chard_num(chat_object):
    send_message('Введите номер телефона или банковской карты без пробелов', chat_object.from_id)


def en_send_please_phone_or_chard_num(chat_object):
    send_message('Enter your phone or bank card number without spaces', chat_object.from_id)


def ru_send_please_bank_nam(chat_object):
    send_message('Введите название банка на который хотете вывести деньги', chat_object.from_id)


def en_send_please_bank_nam(chat_object):
    send_message('Enter the name of the bank to which you want to withdraw money', chat_object.from_id)


def ru_send_help_message(chat_object):
    send_message("Обратитесь в техническую поддержу t.me/apacheL9 и изложите им свою проблему.\n"
                 "Ожидание может составлять от 5 минут до 1 часа.", chat_object.from_id)


def en_send_help_message(chat_object):
    send_message("Contact with technical support t.me/apacheL9 and tell them your problem.\n"
                 "The wait can range from 5 minutes to 1 hour.", chat_object.from_id)


def ru_success_message(chat_object):
    send_message("Успешно.", chat_object.from_id)


def en_success_message(chat_object):
    send_message("Success.", chat_object.from_id)


def ru_error_message(chat_object, msg):
    send_message(f"Ошибка, {msg}", chat_object.from_id)


def en_error_message(chat_object, msg):
    send_message(f"Error, {msg}", chat_object.from_id)
