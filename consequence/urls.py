from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_user, name='logout_user'),
    path('dashboard', views.dashboard_index, name='dashboard_index'),
]