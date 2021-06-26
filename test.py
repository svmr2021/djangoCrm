import requests
from pprint import pprint

URL = 'http://127.0.0.1:8000'


def get_token():
    url = f'{URL}/api/auth/'
    response = requests.post(url, data={
        'username': 'Saidamir2001',
        'password': 'Adg@2052'
    })

    return response.json()


def get_data():
    url = f'{URL}/api/list/'
    header = {"Authorization": f'Token {get_token()}'}

    response = requests.get(url, headers=header)
    pprint(response.text)


def create_data():
    url = f'{URL}/api/list/'
    header = {"Authorization": f'Token {get_token()}'}
    data = {
        "first_name": "Saidasror",
        "last_name": "Takhirkhodjaev",
        "age": 20,
        "description": "Saidasror is a first lead",
        "date_added": "2021-06-25T07:16:20.527098Z",
        "phone_number": "998900066077",
        "email": "saidamirhoja2015@mail.ru",
        "organization": 1,
        "agent": 1,
        "category": 1
    }

    response = requests.post(url, data=data, headers=header)
    pprint(response.json())


def edit_data(id):
    url = f'{URL}/api/list/{id}/'
    header = {"Authorization": f'Token {get_token()}'}
    data = {
        "first_name": "AMORA",
        "last_name": "Takhirkhodjaev",
        "age": 55,
        "description": "Saidasror is a first lead",
        "date_added": "2021-06-26T06:07:19.538769Z",
        "phone_number": "998900066077",
        "email": "saidamirhoja2015@mail.ru",
        "organization": 1,
        "agent": 1,
        "category": 1
    }
    response = requests.put(url, data=data, headers=header)
    print(response.text)


def delete_data(id):
    url = f'{URL}/api/list/{id}/'
    header = {"Authorization": f'Token {get_token()}'}
    response = requests.delete(url,headers=header)
    print(response.text)


delete_data(4)