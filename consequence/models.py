from django.db import models
from django.contrib.auth.models import User


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
