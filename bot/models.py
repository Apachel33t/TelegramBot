from django.db import models
from .models_manager import *


class User(models.Model):
    """Object with all users (admins, common users, payment users)"""
    external_id = models.TextField(
        verbose_name="User id in telegrams"
    )
    current_lang = models.TextField(
        verbose_name="Telegram user selected language"
    )
    username = models.TextField(
        verbose_name="Username in telegrams"
    )
    fullname = models.TextField(
        verbose_name="fullname",
        null=True,
        default=None,
        blank=True,
        max_length=128,
    )
    rights = models.TextField(
        verbose_name="Telegram bot user rights"
    )
    date_of_creation = models.DateField(
        verbose_name='Date of creation user',
        auto_now_add=True
    )
    date_of_when_began_admin = models.DateField(
        verbose_name='Date of when began admin',
        auto_now=True
    )
    email = models.EmailField(
        verbose_name="User email",
        null=True,
        default=None,
        blank=True,
        max_length=64,
    )

    objects = UserManager()


class UserRequestTopOfBalance(models.Model):
    external_id = models.TextField(
        verbose_name="User id in telegrams"
    )
    sum = models.TextField(
        verbose_name="Top-up amount"
    )

    objects = UserRequestTopOfBalanceManager()


class UserRequestWithdrawCash(models.Model):
    external_id = models.TextField(
        verbose_name="User id in telegrams"
    )
    sum = models.TextField(
        verbose_name="Top-up amount",
        null=True,
        default=None,
        blank=True,
    )
    bank_name = models.TextField(
        verbose_name="User bank card",
        null=True,
        default=None,
        blank=True,
    )
    card_num = models.TextField(
        verbose_name="User bank card",
        null=True,
        default=None,
        blank=True,
    )
    phone_num = models.TextField(
        verbose_name="User phone",
        null=True,
        default=None,
        blank=True,
    )

    objects = UserRequestWithdrawCashManager()


class ProfileTelegramUser(models.Model):
    """Info about user projects and other data"""
    external_id = models.TextField(
        verbose_name="User id in telegrams"
    )
    current_count_of_completed_projects = models.TextField(
        verbose_name="Current number of user projects completed",
        null=True,
        default=None,
        blank=True
    )
    current_count_of_active_projects = models.TextField(
        verbose_name="Current number of user projects active",
        null=True,
        default=None,
        blank=True
    )


class ProjectsByTelegramUser(models.Model):
    """Проекты которые пользователь исполняет"""
    external_id = models.TextField(
        verbose_name="User id in telegrams"
    )
    title = models.TextField(
        verbose_name="Title of project"
    )
    img = models.TextField(
        verbose_name="Attached files"
    )
    data_of_create = models.DateField(
        verbose_name="Date of create project",
        auto_now_add=True
    )
    cost = models.TextField(
        verbose_name="Project cost"
    )
    category = models.TextField(
        verbose_name="Category name"
    )
    description = models.TextField(
        verbose_name="Project description"
    )
    status = models.TextField(
        verbose_name="Status of project"
    )
    """Use external_id in table user"""
    performer_ext_id = models.TextField(
        verbose_name="Id telegram user which perform task"
    )


class FilesByTelegramUser(models.Model):
    pass


class FeedbacksByTelegramUser(models.Model):
    pass
