import allure
import requests
from utils import generate_random_string
from urls import base_url
from data import create_order_data

@allure.step('Генерируем набор данных для тестового курьера')
def generate_new_courier_data():
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    return payload

@allure.step('Отправляем запрос на создание курьера и возвращаем ответ')
def send_create_courier_request(payload):
    response = requests.post(f'{base_url}/courier', json=payload)

    return response

@allure.step('Отправляем запрос на создание заказа и возвращаем ответ')
def send_create_order_request(payload):
    response = requests.post(f'{base_url}/orders', json=payload)

    return response

@allure.step('Отправляем запрос на получение списка заказов и возвращаем ответ')
def send_get_orders_list_request():
    response = requests.get(f'{base_url}/orders')

    return response

@allure.step('Отправляем запрос на логин курьера и возвращаем ответ')
def send_login_request(payload):
    response = requests.post(f'{base_url}/courier/login', json=payload)

    return response

@allure.step('Создаём тестового курьера и возвращаем его данные')
def register_new_courier_and_return_courier_data():
    courier_data = []
    payload = generate_new_courier_data()

    response = send_create_courier_request(payload)

    if response.status_code == 201:
        courier_data.append(payload['login'])
        courier_data.append(payload['password'])
        courier_data.append(payload['firstName'])

    return courier_data

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
