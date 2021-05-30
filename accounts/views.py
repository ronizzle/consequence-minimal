from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return HttpResponse('home page')


def products(request):
    return HttpResponse('products page')


def customer(request):
    return HttpResponse('customer page')
