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
    for account_result in accounts['results']:
        tl_account = TrueLayerAccount.objects.filter(tl_account_id=account_result['account_id']).first()
        if tl_account is not None:
            account_result['linked'] = True
        else:
            account_result['linked'] = False

    context = {'accounts': accounts['results']}
    return render(request, 'consequence/dashboard/truelayer/accounts.html', context)


@login_required(login_url='login_page')
def truelayer_cards_index(request):
    if 'access_token' not in request.session:
        return redirect('/dashboard_index')

    url_suffix = 'data/v1/cards'
    cards = truelayer_rest_call(url_suffix, request.session['access_token'])

    for card_result in cards['results']:
        tl_card = TrueLayerCard.objects.filter(tl_account_id=card_result['account_id']).first()
        if tl_card is not None:
            card_result['linked'] = True
        else:
            card_result['linked'] = False

    context = {'cards': cards['results']}
    return render(request, 'consequence/dashboard/truelayer/cards.html', context)


@login_required(login_url='login_page')
def truelayer_link_account(request, pk):
    user = User.objects.get(id=request.user.id)
    fetched_account = Account.objects.filter(user__id=user.id).first()
    tl_accounts = TrueLayerAccount.objects.filter(tl_account_id=pk)
    if tl_accounts.count() > 0:
        messages.error(request,
                       'Error encountered: Account ' + tl_accounts.first().display_name + ' is already linked for another user!')
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
    tl_account.account = fetched_account
    tl_account.save()

    messages.error(request, 'Account ' + tl_account.display_name + ' successfully linked!')
    return redirect('truelayer_accounts_index')


@login_required(login_url='login_page')
def truelayer_link_card(request, pk):
    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    tl_cards = TrueLayerCard.objects.filter(tl_account_id=pk)
    if tl_cards.count() > 0:
        messages.error(request,
                       'Error encountered: Card ' + tl_cards.first().display_name + ' is already linked for another user!')
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

    tl_card = TrueLayerCard.objects.filter(tl_account_id=pk).first()

    transactions_url_suffix = 'data/v1/cards/' + pk + '/transactions'
    card_transactions = truelayer_rest_call(transactions_url_suffix, request.session['access_token'])['results']

    for card_transaction in card_transactions:
        card_transaction['transaction_classification_primary'] = 'Uncategorized'

        if len(card_transaction['transaction_classification']) > 0:
            card_transaction['transaction_classification_primary'] = card_transaction['transaction_classification'][0]

        tl_card_transaction = TrueLayerCardTransaction.objects.filter(
            transaction_id=card_transaction['transaction_id']).first()

        if tl_card_transaction is not None:
            card_transaction['linked'] = True
        else:
            card_transaction['linked'] = False

    context = {'card': card, 'card_transactions': card_transactions, 'tl_card': tl_card}
    return render(request, 'consequence/dashboard/truelayer/card.html', context)


@login_required(login_url='login_page')
def truelayer_account_record(request, pk):
    url_suffix = 'data/v1/accounts/' + pk
    account = truelayer_rest_call(url_suffix, request.session['access_token'])['results'][0]
    tl_account = TrueLayerAccount.objects.filter(tl_account_id=pk).first()
    transactions_url_suffix = 'data/v1/accounts/' + pk + '/transactions'
    account_transactions = truelayer_rest_call(transactions_url_suffix, request.session['access_token'])['results']

    for account_transaction in account_transactions:
        account_transaction['transaction_classification_primary'] = 'Uncategorized'

        if len(account_transaction['transaction_classification']) > 0:
            account_transaction['transaction_classification_primary'] = \
            account_transaction['transaction_classification'][0]

        tl_account_transaction = TrueLayerAccountTransaction.objects.filter(
            transaction_id=account_transaction['transaction_id']).first()
        if tl_account_transaction is not None:
            account_transaction['linked'] = True
        else:
            account_transaction['linked'] = False

    context = {'account': account, 'account_transactions': account_transactions, 'tl_account': tl_account}
    return render(request, 'consequence/dashboard/truelayer/account.html', context)


@login_required(login_url='login_page')
def truelayer_link_account_transaction(request, account_id, transaction_id):
    if request.method == 'POST':
        tl_account_transaction = TrueLayerAccountTransaction.objects.filter(transaction_id=transaction_id).first()
        tl_account = TrueLayerAccount.objects.filter(tl_account_id=account_id).first()

        if tl_account_transaction is not None:
            messages.error(request,
                           'Error encountered: Transaction ID ' + transaction_id + ' already linked in the system.')
            return redirect('truelayer_accounts_index')

        tl_account_transaction = TrueLayerAccountTransaction()
        tl_account_transaction.description = request.POST.get('description')
        tl_account_transaction.transaction_type = request.POST.get('transaction_type')
        tl_account_transaction.transaction_category = request.POST.get('transaction_category')
        tl_account_transaction.merchant_name = request.POST.get('merchant_name')
        tl_account_transaction.amount = request.POST.get('amount')
        tl_account_transaction.currency = request.POST.get('currency')
        tl_account_transaction.provider_transaction_category = request.POST.get('provider_transaction_category')
        tl_account_transaction.running_balance_amount = request.POST.get('running_balance_amount')
        tl_account_transaction.running_balance_currency = request.POST.get('running_balance_currency')
        tl_account_transaction.transaction_id = request.POST.get('transaction_id')
        tl_account_transaction.transaction_classification_primary = request.POST.get(
            'transaction_classification_primary')
        tl_account_transaction.account = tl_account.account
        tl_account_transaction.tl_account = tl_account
        tl_account_transaction.save()
        messages.success(request, 'Successfully linked Account Transaction ID:' + transaction_id)
        return redirect('truelayer_accounts_index')

    return redirect('truelayer_accounts_index')


@login_required(login_url='login_page')
def truelayer_link_card_transaction(request, card_id, transaction_id):
    if request.method == 'POST':
        tl_card_transaction = TrueLayerCardTransaction.objects.filter(transaction_id=transaction_id).first()
        tl_card = TrueLayerCard.objects.filter(tl_account_id=card_id).first()
        print(tl_card)
        print(card_id)

        if tl_card_transaction is not None:
            messages.error(request,
                           'Error encountered: Transaction ID ' + transaction_id + ' already linked in the system.')
            return redirect('truelayer_cards_index')

        tl_card_transaction = TrueLayerCardTransaction()
        tl_card_transaction.description = request.POST.get('description')
        tl_card_transaction.transaction_type = request.POST.get('transaction_type')
        tl_card_transaction.transaction_category = request.POST.get('transaction_category')
        tl_card_transaction.merchant_name = request.POST.get('merchant_name')
        tl_card_transaction.amount = request.POST.get('amount')
        tl_card_transaction.currency = request.POST.get('currency')
        tl_card_transaction.provider_transaction_category = request.POST.get('provider_transaction_category')
        tl_card_transaction.running_balance_amount = request.POST.get('running_balance_amount')
        tl_card_transaction.running_balance_currency = request.POST.get('running_balance_currency')
        tl_card_transaction.transaction_classification_primary = request.POST.get('transaction_classification_primary')
        tl_card_transaction.transaction_id = request.POST.get('transaction_id')
        tl_card_transaction.account = tl_card.account
        tl_card_transaction.tl_card = tl_card
        tl_card_transaction.save()
        messages.success(request, 'Successfully linked Card Transaction ID:' + transaction_id)
        return redirect('truelayer_cards_index')

    return redirect('truelayer_accounts_index')


@login_required(login_url='login_page')
def dashboard_index(request):
    user = User.objects.get(id=request.user.id)
    account = Account.objects.filter(user__id=user.id).first()
    impact = calculate_impact(account)

    # {'records': records, 'impact_uncategorized': impact_uncategorized,
    # 'average_impact_categorized': average_impact_categorized, 'impact_categorized': impact_categorized}

    context = {
        'user': user,
        'link': '',
        'account': account,
        'total_impact': impact['total_impact'],
        'records': impact['records'],
        'impact_uncategorized': impact['impact_uncategorized'],
        'average_impact_categorized': impact['average_co2e_factor'],
        'impact_categorized': impact['impact_categorized'],
    }

    if 'access_token' not in request.session:
        context['link'] = truelayer_link_builder()

    return render(request, 'consequence/dashboard/pages/index.html', context)


def calculate_impact(account):
    tl_card_transactions = TrueLayerCardTransaction.objects.filter(account=account)
    tl_account_transactions = TrueLayerAccountTransaction.objects.filter(account=account)
    total_impact = 0
    total_co2e_factor = 0
    total_amount_uncategorized = 0
    classified_ctr = 0
    records = []

    for tl_card_transaction in tl_card_transactions:

        tl_merchant = TrueLayerMerchant.objects.filter(merchant_name=tl_card_transaction.merchant_name).first()

        if tl_merchant is not None:
            impact = (tl_card_transaction.amount * tl_merchant.co2e_factor)
            total_impact = total_impact + (tl_card_transaction.amount * tl_merchant.co2e_factor)
            total_co2e_factor = total_co2e_factor + tl_merchant.co2e_factor
            records.append({
                'transaction': {
                    'id': tl_card_transaction.transaction_id,
                    'type': 'Card',
                },
                'amount': tl_card_transaction.amount,
                'co2e_factor': tl_merchant.co2e_factor,
                'impact': impact,
                'source': {
                    'type': 'Merchant',
                    'label': tl_merchant.merchant_name,
                }
            })
            classified_ctr += 1

        elif tl_merchant is None:
            tl_classification = TrueLayerClassification.objects.filter(
                transaction_classification=tl_card_transaction.transaction_classification_primary).first()
            if tl_classification is not None:
                impact = (tl_card_transaction.amount * tl_classification.co2e_factor)
                total_impact = total_impact + impact
                records.append({
                    'transaction': {
                        'id': tl_card_transaction.transaction_id,
                        'type': 'Card',
                    },
                    'amount': tl_card_transaction.amount,
                    'co2e_factor': tl_classification.co2e_factor,
                    'impact': impact,
                    'source': {
                        'type': 'Classification',
                        'label': tl_classification.transaction_classification
                    }})
                classified_ctr += 1
            elif tl_classification is None:
                total_amount_uncategorized = total_amount_uncategorized + tl_card_transaction.amount
                records.append({
                    'transaction': {
                        'id': tl_card_transaction.transaction_id,
                        'type': 'Card',
                    },
                    'amount': tl_card_transaction.amount,
                    'co2e_factor': 'NA',
                    'impact': 'NA',
                })

    for tl_account_transaction in tl_account_transactions:

        tl_merchant = TrueLayerMerchant.objects.filter(merchant_name=tl_account_transaction.merchant_name).first()

        if tl_merchant is not None:
            impact = (tl_account_transaction.amount * tl_merchant.co2e_factor)
            total_impact = total_impact + (tl_account_transaction.amount * tl_merchant.co2e_factor)
            total_co2e_factor = total_co2e_factor + tl_merchant.co2e_factor
            records.append({
                'transaction': {
                    'id': tl_account_transaction.transaction_id,
                    'type': 'Account',
                },
                'amount': tl_account_transaction.amount,
                'co2e_factor': tl_merchant.co2e_factor,
                'impact': impact,
                'source': {
                    'type': 'Merchant',
                    'label': tl_merchant.merchant_name,
                }
            })
            classified_ctr += 1

        elif tl_merchant is None:
            tl_classification = TrueLayerClassification.objects.filter(
                transaction_classification=tl_account_transaction.transaction_classification_primary).first()
            if tl_classification is not None:
                impact = (tl_account_transaction.amount * tl_classification.co2e_factor)
                total_impact = total_impact + impact
                records.append({
                    'transaction': {
                        'id': tl_account_transaction.transaction_id,
                        'type': 'Account',
                    },
                    'amount': tl_account_transaction.amount,
                    'co2e_factor': tl_classification.co2e_factor,
                    'impact': impact,
                    'source': {
                        'type': 'Classification',
                        'label': tl_classification.transaction_classification
                    }})
                classified_ctr += 1
            elif tl_classification is None:
                total_amount_uncategorized = total_amount_uncategorized + tl_account_transaction.amount
                records.append({
                    'transaction': {
                        'id': tl_account_transaction.transaction_id,
                        'type': 'Account',
                    },
                    'amount': tl_account_transaction.amount,
                    'co2e_factor': 'NA',
                    'impact': 'NA',
                })

    average_co2e_factor = total_co2e_factor / classified_ctr
    impact_uncategorized = average_co2e_factor * total_amount_uncategorized
    impact_categorized = total_impact

    total_impact = impact_categorized + impact_uncategorized

    data = {'total_impact': total_impact,
            'total_co2e_factor': total_co2e_factor,
            'average_co2e_factor': average_co2e_factor,
            'classified_count': classified_ctr,
            'records': records,
            'impact_uncategorized': impact_uncategorized,
            'impact_categorized': impact_categorized}

    print(data)
    return data
