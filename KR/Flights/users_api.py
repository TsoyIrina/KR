import json

import requests
from ast import literal_eval

from requests.auth import HTTPBasicAuth

url_base = 'http://127.0.0.1:8000/api/v1/'


def login(login, password):
    url = f'{url_base}login/'
    payload = {'username': login, 'password': password}
    return requests.post(url, data=payload).json()


def take_profile(username):
    url = url_base + 'profile/'
    res = requests.get(url).json()
    for user in res:
        if user['user']['username'] == str(username):
            return user
    return 'None'


def del_tick(tick_pk):
    url = f'{url_base}ticket/{tick_pk}/'
    return requests.delete(url)


def create_tick(body):
    url = f'{url_base}ticket/'
    return requests.post(url, json=body)


def update_profile(user_pk, body):
    url = f'{url_base}profile/{user_pk}/'
    return requests.patch(url, json=body)


def update_tick(tick_pk):
    url = f'{url_base}ticket/{tick_pk}/'
    return requests.patch(url, json={
        "paid": 'true'
    })


def take_tickets(profile_pk):
    url = f'{url_base}ticket/'
    res = requests.get(url).json()
    tick_res = []
    for tick in res:
        if tick['profile'] == profile_pk:
            tick_res.append(tick)
    return tick_res


if __name__ == '__main__':
    obj = {
        "profile": 1,
        "flights": [
            {
                "from_airport": {
                    "code": "FNJ",
                    "name": "Pyongyang Sunan International Airport"
                },
                "to_airport": {
                    "code": "TRC",
                    "name": "Francisco Sarabia International Airport"
                },
                "airline": {
                    "code": "D7",
                    "name": "AirAsia X"
                },
                "price": "2293.97"
            }
        ],
        "date": "2023-12-29"
    }
    print(update_tick(64))
    # print(take_profile('root'))

# [{'user': {'username': 'root', 'email': 'eda@mail.ru', 'first_name': 'Ирина1', 'last_name': 'd'},
#   'location': 'MVF'},
#  {'user': {'username': 'inotadmin', 'email': 'i@not.admin', 'first_name': 'Not', 'last_name': 'Admin'},
#   'location': 'ENA'},
#  {'user': {'username': 'who', 'email': 'who@who.ho', 'first_name': '', 'last_name': ''},
#   'location': ''}]


# [{'profile':
#           {'user': {'username': 'root', 'email': 'eda@mail.ru', 'first_name': 'Ирина1', 'last_name': 'd'},
#  'location': 'MVF'},
#  'flights':
#       [   {'air_from': 'FNJ', 'air_to': 'TRC', 'air_line': 'D7', 'price': '2293.97'}],
#  'num_stops': 0,
#  'ad': 1,
#  'ch': 0,
#  'inf': 0,
#  'date': '4567-03-12',
#  'price': '2293.97',
#  'paid': True},
#  {'profile': {'user': {'username': 'root', 'email': 'eda@mail.ru', 'first_name': 'Ирина1', 'last_name': 'd'}, 'location': 'MVF'}, 'flights': [{'air_from': 'ENA', 'air_to': 'LKN', 'air_line': 'IN', 'price': '100.00'}, {'air_from': 'LKN', 'air_to': 'KLF', 'air_line': 'IN', 'price': '100.00'}], 'num_stops': 1, 'ad': 1, 'ch': 0, 'inf': 0, 'date': '0456-03-12', 'price': '200.00', 'paid': True}, {'profile': {'user': {'username': 'root', 'email': 'eda@mail.ru', 'first_name': 'Ирина1', 'last_name': 'd'}, 'location': 'MVF'}, 'flights': [{'air_from': 'ENA', 'air_to': 'LKN', 'air_line': 'IN', 'price': '100.00'}, {'air_from': 'LKN', 'air_to': 'KLF', 'air_line': 'IN', 'price': '100.00'}], 'num_stops': 1, 'ad': 1, 'ch': 1, 'inf': 3, 'date': '2023-12-22', 'price': '480.00', 'paid': True}, {'profile': {'user': {'username': 'inotadmin', 'email': 'i@not.admin', 'first_name': 'Not', 'last_name': 'Admin'}, 'location': 'ENA'}, 'flights': [{'air_from': 'ENA', 'air_to': 'LKN', 'air_line': 'IN', 'price': '100.00'}, {'air_from': 'LKN', 'air_to': 'KLF', 'air_line': 'IN', 'price': '100.00'}], 'num_stops': 1, 'ad': 1, 'ch': 0, 'inf': 0, 'date': '2023-12-14', 'price': '200.00', 'paid': True}, {'profile': {'user': {'username': 'inotadmin', 'email': 'i@not.admin', 'first_name': 'Not', 'last_name': 'Admin'}, 'location': 'ENA'}, 'flights': [{'air_from': 'ENA', 'air_to': 'LKN', 'air_line': 'IN', 'price': '100.00'}, {'air_from': 'LKN', 'air_to': 'KLF', 'air_line': 'IN', 'price': '100.00'}], 'num_stops': 1, 'ad': 1, 'ch': 0, 'inf': 0, 'date': '2023-12-30', 'price': '200.00', 'paid': False}, {'profile': {'user': {'username': 'who', 'email': 'who@who.ho', 'first_name': '', 'last_name': ''}, 'location': ''}, 'flights': [{'air_from': 'FNJ', 'air_to': 'TRC', 'air_line': 'D7', 'price': '2293.97'}], 'num_stops': 0, 'ad': 1, 'ch': 0, 'inf': 0, 'date': '2023-12-29', 'price': '2293.97', 'paid': False}]
