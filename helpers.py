import allure
import requests
from utils import generate_random_string
from urls import base_url
from data import create_order_data

@allure.step('Создаём тестового курьера и возвращаем его данные')
def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{base_url}/courier', json=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

@allure.step('Получаем id курьера по логину и паролю')
def get_courier_id(courier_data):
    courier_id = ''

    payload = {
        "login": courier_data[0],
        "password": courier_data[1]
        }

    response = requests.post(f'{base_url}/courier/login', json=payload)
    if response.status_code == 200:
        courier_id = response.json()['id']

    return courier_id

@allure.step('Удаляем тестового курьера')
def delete_couriers(ids):
    if ids:
        for id in ids:
            requests.delete(f'{base_url}/courier{id}')

@allure.step('Создаём тестовый заказ и возвращаем его номер')
def create_order_and_return_track():
    track = ''
    payload = create_order_data.copy()

    response = requests.post(f'{base_url}/orders', json=payload)
    response_body = response.json()

    track = response_body.get('track')
    return track

@allure.step('Отменяем тестовые заказы')
def cancel_order(tracks):
    if tracks:
        for track in tracks:
            payload = {'track': track}
            requests.put(f'{base_url}/orders/cancel', json=payload)
