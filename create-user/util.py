import sys
import os
import datetime
import random
import string
import requests
import jwt
import pprint
from colorama import Fore, Back, Style
sys.path.append('../')
import secret

QUESTION = Fore.GREEN
DEFAULT = Fore.YELLOW
INPUT = Fore.WHITE

def print_header():
    print(Fore.CYAN + """
 _______  _______  _______  _______ 
/ ___   )(  ___  )(  ___  )(       )
\/   )  || (   ) || (   ) || () () |
    /   )| |   | || |   | || || || |
   /   / | |   | || |   | || |(_)| |
  /   /  | |   | || |   | || |   | |
 /   (_/\| (___) || (___) || )   ( |
(_______/(_______)(_______)|/     \|
""")
print(Style.RESET_ALL)

def print_info(msg):
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')

def call_api(method, path, payload, username=None, fail_on_error=True):
    domain = 'https://api.zoom.us/v2'
    if not path.startswith('/'):
        path = '/' + path
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + str(get_api_token())
    }
    if fail_on_error:
        return api_error_handler(requests.request(
            method,
            domain + path, 
            json=payload, 
            headers=headers), username)
    else:
        return requests.request(
                    method,
                    domain + path, 
                    json=payload, 
                    headers=headers)

def api_error_handler(response, username):
    if not str(response.status_code).startswith('2'):
        print(f'{Fore.RED}An error occured while processing API call: {Fore.YELLOW} {response.request.method} {response.request.url}')
        print(f'{Fore.RED}The call returned code {Fore.YELLOW} {response.status_code} {Fore.RED} and message:')
        try:
            response_json = response.json()
        except Exception:
            print(Fore.YELLOW + response.text)
            delete_user_and_exit(username)
        if not 'message' in response_json:
            print(Fore.YELLOW + response_json)
        else:
            pp = pprint.PrettyPrinter(indent=2)
            print(Fore.YELLOW)
            pp.pprint(response_json)
        print(Style.RESET_ALL)
        delete_user_and_exit(username)
    return response

def delete_user_and_exit(username):
    if username:
        call_api('DELETE', f'/users/{username}?action=delete', {})
    exit(-1)

def get_api_token():
    payload = {
        'iss': secret.api_key,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }
    jwt_encoded = str(jwt.encode(payload, secret.api_sec))
    jwt_encoded = jwt_encoded[2:]
    jwt_encoded = jwt_encoded[:-1]
    return jwt_encoded

def random_string(length = 10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_input_with_random_default(msg):
    data = input(QUESTION + msg + DEFAULT + ' [random]: ' + INPUT)
    if not data:
        data = random_string()
    print(Style.RESET_ALL)
    return data

def get_input_with_default(msg, default):
    data = input(QUESTION + msg + DEFAULT + f' [{default}]: ' + INPUT)
    if not data:
        data = default
    print(Style.RESET_ALL)
    return data

def get_input_with_none_default(msg):
    data = input(QUESTION + msg + DEFAULT + ' [None]: ' + INPUT)
    if not data:
        data = None
    print(Style.RESET_ALL)
    return data

def get_comma_separated_input(msg):
    data = input(QUESTION + msg + INPUT).split(',')
    print(Style.RESET_ALL)
    if len(data) == 0:
        return None
    return data

def validate_input(json):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(json)
    ok = input(f'\n{Fore.YELLOW}Is this ok (yes/no) {Fore.GREEN}[yes]? ')
    if not ok or ok == "yes":
        return True
    return False
