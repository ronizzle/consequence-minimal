from django.db import models
from django.contrib.auth.models import User

CURRENCY = (
    ('GBP', 'GBP'),
    ('USD', 'USD'),
)


class BusinessNature(models.Model):
    name = models.CharField(max_length=200, null=True)
    impact_per_employees = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=200, null=True)
    number_of_employees = models.SmallIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nature_of_business = models.ForeignKey(BusinessNature, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class TrueLayerAccount(models.Model):

    display_name = models.CharField(max_length=200, null=True)
    tl_account_id = models.CharField(max_length=200, null=True)
    account_type = models.CharField(max_length=200, null=True)
    currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    account_number = models.CharField(max_length=200, null=True)
    account_number_swift_bic = models.CharField(max_length=200, null=True)
    account_number_sort_code = models.CharField(max_length=200, null=True)
    provider_display_name = models.CharField(max_length=200, null=True)
    provider_id = models.CharField(max_length=200, null=True)
    provider_logo_uri = models.CharField(max_length=200, null=True)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_name


class TrueLayerCard(models.Model):

    display_name = models.CharField(max_length=200, null=True)
    tl_account_id = models.CharField(max_length=200, null=True)
    card_type = models.CharField(max_length=200, null=True)
    name_on_card = models.CharField(max_length=200, null=True)
    card_network = models.CharField(max_length=200, null=True)
    partial_card_number = models.CharField(max_length=200, null=True)
    currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    provider_display_name = models.CharField(max_length=200, null=True)
    provider_id = models.CharField(max_length=200, null=True)
    provider_logo_uri = models.CharField(max_length=200, null=True)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_name


class TrueLayerAccountTransaction(models.Model):
    description = models.CharField(max_length=200, null=True)
    transaction_type = models.CharField(max_length=200, null=True)
    transaction_category = models.CharField(max_length=200, null=True)
    transaction_classification_primary = models.CharField(max_length=200, null=True)
    merchant_name = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True)
    currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    provider_transaction_category = models.CharField(max_length=200, null=True)
    running_balance_currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    running_balance_amount = models.FloatField(null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    tl_account = models.ForeignKey(TrueLayerAccount, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description


class TrueLayerCardTransaction(models.Model):

    description = models.CharField(max_length=200, null=True)
    transaction_type = models.CharField(max_length=200, null=True)
    transaction_category = models.CharField(max_length=200, null=True)
    transaction_classification_primary = models.CharField(max_length=200, null=True)
    merchant_name = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True)
    currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    transaction_id = models.CharField(max_length=200, null=True)
    provider_transaction_category = models.CharField(max_length=200, null=True)
    running_balance_currency = models.CharField(max_length=200, null=True, choices=CURRENCY)
    running_balance_amount = models.FloatField(null=True)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    tl_card = models.ForeignKey(TrueLayerCard, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description


class TrueLayerMerchant(models.Model):
    merchant_name = models.CharField(max_length=200, null=True)
    co2e_factor = models.FloatField(null=True)

    def __str__(self):
        return self.merchant_name


class TrueLayerClassification(models.Model):
    transaction_classification = models.CharField(max_length=200, null=True)
    co2e_factor = models.FloatField(null=True)

    def __str__(self):
        return self.transaction_classification

