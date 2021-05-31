from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_user, name='logout_user'),
    path('dashboard', views.dashboard_index, name='dashboard_index'),
    path('profile', views.update_profile, name='update_profile'),

    #TrueLayer URLS
    path('truelayer/callback', views.truelayer_callback, name='truelayer_callback'),
    path('truelayer/accounts', views.truelayer_accounts_index, name='truelayer_accounts_index'),
    path('truelayer/cards', views.truelayer_cards_index, name='truelayer_cards_index'),
    path('truelayer/account/link/<str:pk>', views.truelayer_link_account, name='truelayer_link_account'),
    path('truelayer/card/link/<str:pk>', views.truelayer_link_card, name='truelayer_link_card'),
    path('truelayer/account/<str:pk>', views.truelayer_account_record, name='truelayer_account_record'),
    path('truelayer/card/<str:pk>', views.truelayer_card_record, name='truelayer_card_record'),
]