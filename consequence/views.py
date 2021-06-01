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
    if 'access_token' in request.session:
        del request.session['access_token']

    if 'refresh_token' in request.session:
        del request.session['refresh_token']

    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def dashboard_index(request):
    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    context = {
        'user': user,
        'link': '',
        'account': account
    }

    if 'access_token' not in request.session:
        context['link'] = truelayer_link_builder()

    return render(request, 'consequence/dashboard/pages/index.html', context)


@login_required(login_url='login_page')
def update_profile(request):
    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()

    if request.method == 'POST':
        business_nature = BusinessNature.objects.get(id=request.POST.get('nature_of_business'))
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            if account is None:
                account = Account()

            account.name = request.POST.get('name')
            account.number_of_employees = request.POST.get('number_of_employees')
            account.nature_of_business = business_nature
            account.user = user
            account.save()
            return redirect('/profile')

    form = CreateAccountForm()
    if account is not None:
        form = CreateAccountForm(instance=account)

    context = {
        'form': form,
    }
    return render(request, 'consequence/dashboard/pages/profile.html', context)





@login_required(login_url='login_page')
def truelayer_callback(request):
    token_auth_response = truelayer_connect_token(request.GET.get('code'))
    context = {}
    if 'error' in token_auth_response:
        return render(request, 'consequence/truelayer/login-error.html', context)

    if 'access_token' in token_auth_response:
        request.session['refresh_token'] = token_auth_response['refresh_token']
        request.session['access_token'] = token_auth_response['access_token']
        return render(request, 'consequence/truelayer/login-success.html', context)

    return redirect('/dashboard_index')



@login_required(login_url='login_page')
def truelayer_accounts_index(request):
    if 'access_token' not in request.session:
        return redirect('/dashboard_index')

    url_suffix = 'data/v1/accounts'
    accounts = truelayer_rest_call(url_suffix, request.session['access_token'])
    context = {'accounts': accounts['results']}
    return render(request, 'consequence/dashboard/truelayer/accounts.html', context)


@login_required(login_url='login_page')
def truelayer_cards_index(request):
    if 'access_token' not in request.session:
        return redirect('/dashboard_index')

    url_suffix = 'data/v1/cards'
    cards = truelayer_rest_call(url_suffix, request.session['access_token'])
    context = {'cards': cards['results']}
    return render(request, 'consequence/dashboard/truelayer/cards.html', context)



@login_required(login_url='login_page')
def truelayer_link_account(request, pk):

    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    tl_accounts = TrueLayerAccount.objects.filter(tl_account_id=pk)
    if tl_accounts.count() > 0:
        messages.error(request, 'Error encountered: Account ' + tl_accounts.first().display_name + ' is already linked for another user!')
        return redirect('truelayer_accounts_index')

    url_suffix = 'data/v1/accounts/' + pk
    account = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]
    tl_account = TrueLayerAccount()
    tl_account.display_name = account['display_name']
    tl_account.tl_account_id = account['account_id']
    tl_account.account_type = account['account_type']
    tl_account.currency = account['currency']
    tl_account.account_number = account['account_number']['number']
    tl_account.account_number_swift_bic = account['account_number']['swift_bic']
    tl_account.account_number_sort_code = account['account_number']['sort_code']
    tl_account.provider_display_name = account['provider']['display_name']
    tl_account.provider_id = account['provider']['provider_id']
    tl_account.provider_logo_uri = account['provider']['logo_uri']
    tl_account = account
    tl_account.save()

    messages.error(request, 'Account ' + tl_account.display_name + ' successfully linked!')
    return redirect('truelayer_accounts_index')



@login_required(login_url='login_page')
def truelayer_link_card(request, pk):

    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    tl_cards = TrueLayerCard.objects.filter(tl_account_id=pk)
    if tl_cards.count() > 0:
        messages.error(request, 'Error encountered: Card ' + tl_cards.first().display_name + ' is already linked for another user!')
        return redirect('truelayer_cards_index')

    url_suffix = 'data/v1/cards/' + pk
    card = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]
    tl_card = TrueLayerCard()
    tl_card.tl_account_id = card['account_id']
    tl_card.display_name = card['display_name']
    tl_card.card_type = card['card_type']
    tl_card.name_on_card = card['name_on_card']
    tl_card.card_network = card['card_network']
    tl_card.partial_card_number = card['partial_card_number']
    tl_card.currency = card['currency']
    tl_card.provider_display_name = card['provider']['display_name']
    tl_card.provider_id = card['provider']['provider_id']
    tl_card.provider_logo_uri = card['provider']['logo_uri']
    tl_card.account = account
    tl_card.save()

    messages.error(request, 'Card ' + tl_card.display_name + ' successfully linked!')
    return redirect('truelayer_cards_index')



@login_required(login_url='login_page')
def truelayer_card_record(request, pk):
    url_suffix = 'data/v1/cards/' + pk
    card = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]

    transactions_url_suffix = 'data/v1/cards/' + pk + '/transactions'
    card_transactions = truelayer_rest_call(transactions_url_suffix, request.session['access_token'])['results']
    context = {'card': card, 'card_transactions': card_transactions}
    return render(request, 'consequence/dashboard/truelayer/card.html', context)



@login_required(login_url='login_page')
def truelayer_account_record(request, pk):
    url_suffix = 'data/v1/accounts/' + pk
    account = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]

    transactions_url_suffix = 'data/v1/accounts/' + pk + '/transactions'
    account_transactions = truelayer_rest_call(transactions_url_suffix, request.session['access_token'])['results']
    context = {'account': account, 'account_transactions': account_transactions}
    print(account_transactions[0])
    return render(request, 'consequence/dashboard/truelayer/account.html', context)



@login_required(login_url='login_page')
def truelayer_link_account_transaction(request, accoount_id, transaction_id):

    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    tl_account_transactions = TrueLayerAccountTransaction.objects.filter(transaction_id=accoount_id)
    if tl_account_transactions.count() > 0:
        messages.error(request, 'Error encountered: Account ' + tl_account_transactions.first().description + ' is already linked for another user!')
        return redirect('truelayer_accounts_index')

    url_suffix = 'data/v1/accounts/' + transaction_id + '/transactions'
    account_transaction = truelayer_rest_call(url_suffix, request.session['access_token'])

    print(account_transaction)
    return HttpResponse(account_transaction)
