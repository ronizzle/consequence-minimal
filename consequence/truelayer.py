
from dotenv import dotenv_values

config = dotenv_values()


def link_builder():
    base_url = config['TRUELAYER_AUTH_URL']
    code = config['TRUELAYER_CODE']
    scope = config['TRUELAYER_SCOPE']
    redirect_uri = config['TRUELAYER_REDIRECT_URI']
    providers = config['TRUELAYER_PROVIDERS']
    client_id = config['TRUELAYER_CLIENT_ID']

    url = base_url + '?response_type=' + code + '&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&providers=' + providers
    return url

