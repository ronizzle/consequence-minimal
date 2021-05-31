from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .truelayer import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard_index')

    return redirect('login_page')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_index')

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
    if request.user.is_authenticated:
        return redirect('dashboard_index')

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


@login_required(login_url='login_page')
def logout_user(request):
    context = {}
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def dashboard_index(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user,
        'link': '',
        'account': user.account
    }

    if 'access_token' not in request.session:
        context.link = link_builder()

    return render(request, 'consequence/dashboard/pages/index.html', context)
