from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


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
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'consequence/authentication/register.html', context)


def login_page(request):

    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_index')
        else:
            messages.info(request, 'Invalid credentials.')
            return render(request, 'consequence/authentication/login.html', context)

    return render(request, 'consequence/authentication/login.html', context)


def logout_user(request):
    context = {}
    logout(request)
    return redirect('login_page')


def dashboard_index(request):
    context = {}
    return render(request, 'consequence/dashboard/pages/index.html', context)
