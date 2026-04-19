import requests
import allure
import pytest
from helpers import cancel_order
from data import create_order_colors, create_order_data
from urls import base_url

class TestCreateOrder:
    tracks = []

    @allure.title('Проверка успешного создания заказа, когда передан цвет')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    @pytest.mark.parametrize('color', create_order_colors)
    def test_create_order_with_color(self, color):
        payload = create_order_data.copy()
        payload['color'] = color

        response = requests.post(f'{base_url}/orders', json=payload)
        response_body = response.json()

        self.tracks.append(response_body.get('track'))

        assert response.status_code == 201
        assert 'track' in response_body

    @allure.title('Проверка успешного создания заказа, когда не передан цвет')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    def test_create_order_without_color(self):
        payload = create_order_data.copy()

        response = requests.post(f'{base_url}/orders', json=payload)
        response_body = response.json()

        self.tracks.append(response_body.get('track'))

        assert response.status_code == 201
        assert 'track' in response_body
        
    @classmethod
    def teardown_class(cls):
        with allure.step('Отменяем созданные заказы'):
            cancel_order(cls.tracks)
