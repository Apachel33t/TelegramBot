from django.db import models


class UserManager(models.Manager):
    def create_user(self, external_id,
                    current_lang, username,
                    rights):
        user = self.create(
            external_id=external_id,
            current_lang=current_lang,
            username=username,
            rights=rights
        )


class UserRequestTopOfBalanceManager(models.Manager):
    def create_balance_request(self, external_id, payment_sum):
        user_request = self.create(
            external_id=external_id,
            sum=payment_sum,
        )


class UserRequestWithdrawCashManager(models.Manager):
    def create_request(self, external_id,
                       withdraw_sum, bank_name, card_num,
                       phone_num):
        user_request = self.create(
            external_id=external_id,
            sum=withdraw_sum,
            bank_name=bank_name,
            card_num=card_num,
            phone_num=phone_num
        )


class ProjectsByTelegramUserManager(models.Manager):
    def create_project(self, external_id, title, file, filename, cost, category, description, deadline):
        project = self.create(
            external_id=external_id,
            title=title,
            file=file,
            filename=filename,
            cost=cost,
            category=category,
            description=description,
            deadline=deadline,
            status='waiting'
        )


class OffersToCustomerManager(models.Manager):
    def create_offer(self, external_from_id, external_to_id, offer):
        project = self.create(
            external_from_id=external_from_id,
            external_to_id=external_to_id,
            offer=offer
        )
