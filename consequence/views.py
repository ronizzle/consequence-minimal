from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'consequence/index.html')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Successfully registered for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'consequence/register.html', context)


def login(request):
    context = {}
    return render(request, 'consequence/login.html', context)
