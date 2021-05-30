from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),
]