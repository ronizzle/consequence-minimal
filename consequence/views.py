from django.shortcuts import render
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

    context = {'form': form}
    return render(request, 'consequence/register.html', context)
