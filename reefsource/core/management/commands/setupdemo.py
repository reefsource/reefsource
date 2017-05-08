import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from reefsource.apps.accounts.models import AppAccount
from reefsource.apps.operations.models import Account, Category
from reefsource.apps.securities.models import Broker, Security
from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates superuser and demo account, and bootstraps the project'

    def handle(self, *args, **options):
        with transaction.atomic():
            user, created = User.objects.get_or_create(username='lkarolewski', defaults={
                'first_name': 'Lukasz',
                'last_name': 'Karolewski',
                'email': 'lkarolewski@gmail.com',
                'password': 'pbkdf2_sha256$20000$mhPZPWeblD8t$08bVuSLFw2QN6bPMPIEOddCHD2H2ySVJj90PWjVvx+c=',
                'is_superuser': True,
                'is_staff': True,
            })

            cash_acc, created = Account.objects.get_or_create(app_account=user.app_account, name='Vanguard Cash', currency=AppAccount.Currency.USD)
            holdings_acc, created = Account.objects.get_or_create(app_account=user.app_account, name='Vanguard Holdings', currency=AppAccount.Currency.USD)

            investments, created = Category.objects.get_or_create(app_account=user.app_account, name='Investments')
            gains, created = Category.objects.get_or_create(app_account=user.app_account, name='Gains', parent=investments)
            losses, created = Category.objects.get_or_create(app_account=user.app_account, name='Losses', parent=investments)
            commissions, created = Category.objects.get_or_create(app_account=user.app_account, name='Commissions', parent=investments)

            Security.objects.get_or_create(id='SYMC')

            Broker.objects.get_or_create(app_account=user.app_account,
                                         name='Vanguard',
                                         cash_account=cash_acc,
                                         holdings_account=holdings_acc,
                                         currency=AppAccount.Currency.USD,
                                         commission_category=commissions,
                                         gain_category=gains,
                                         loss_category=losses)
