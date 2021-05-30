from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index(request):
    return render(request, 'consequence/index.html')


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'consequence/register.html', context)
