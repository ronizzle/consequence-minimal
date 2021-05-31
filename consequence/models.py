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
