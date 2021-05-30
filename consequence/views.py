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
            return redirect('login')

    context = {'form': form}
    return render(request, 'consequence/register.html', context)


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    context = {}
    return render(request, 'consequence/login.html', context)


def dashboard(request):
    return HttpResponse('Dashboard says hello')
