import requests
import json

from dotenv import dotenv_values

config = dotenv_values()




def truelayer_link_builder():
    base_url = config['TRUELAYER_AUTH_URL']
    code = config['TRUELAYER_CODE']
    scope = config['TRUELAYER_SCOPE']
    redirect_uri = config['TRUELAYER_REDIRECT_URI']
    providers = config['TRUELAYER_PROVIDERS']
    client_id = config['TRUELAYER_CLIENT_ID']

    url = base_url + '?response_type=' + code + '&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&providers=' + providers
    return url


def truelayer_connect_token(code):
    base_url = config['TRUELAYER_AUTH_URL']
    url = base_url + 'connect/token'
    client_id = config['TRUELAYER_CLIENT_ID']
    client_secret = config['TRUELAYER_CLIENT_SECRET']
    redirect_uri = config['TRUELAYER_REDIRECT_URI']
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }

    r = requests.post(url, data=post_data, auth=(client_id, client_secret))
    json_response = r.content.decode('utf-8')
    return json.loads(json_response)


