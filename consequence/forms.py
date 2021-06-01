from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Account, TrueLayerAccountTransaction


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'number_of_employees', 'nature_of_business']


