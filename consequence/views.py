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
    print(accounts)
    return render(request, 'consequence/dashboard/truelayer/accounts.html', context)


@login_required(login_url='login_page')
def truelayer_cards_index(request):
    if 'access_token' not in request.session:
        return redirect('/dashboard_index')

    url_suffix = 'data/v1/cards'
    cards = truelayer_rest_call(url_suffix, request.session['access_token'])
    context = {'cards': cards['results']}
    print(cards)
    return render(request, 'consequence/dashboard/truelayer/cards.html', context)



@login_required(login_url='login_page')
def truelayer_link_account(request, pk):

    tlAccounts = TrueLayerAccount.objects.filter(tl_account_id=pk)
    if tlAccounts.count() > 0:
        messages.error(request, 'Error encountered: Account ' + tlAccounts.first().display_name + ' is already linked for another user!')
        return redirect('/accounts')

    url_suffix = 'data/v1/accounts/' + pk
    account = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]
    tlAccount = TrueLayerAccount()
    tlAccount.display_name = account['display_name']
    tlAccount.tl_account_id = account['account_id']
    tlAccount.account_type = account['account_type']
    tlAccount.currency = account['currency']
    tlAccount.account_number = account['account_number']['number']
    tlAccount.account_number_swift_bic = account['account_number']['swift_bic']
    tlAccount.account_number_sort_code = account['account_number']['sort_code']
    tlAccount.provider_display_name = account['provider']['display_name']
    tlAccount.provider_id = account['provider']['provider_id']
    tlAccount.provider_logo_uri = account['provider']['logo_uri']
    tlAccount.save()

    messages.error(request, 'Account ' + tlAccount.display_name + ' successfully linked!')
    return redirect('/accounts')

