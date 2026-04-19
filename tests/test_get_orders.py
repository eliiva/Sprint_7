import requests
import allure
from helpers import create_order_and_return_track, cancel_order
from urls import base_url

class TestGetOrders:
    track = ''

    @classmethod
    def setup_class(cls):
        with allure.step('Создаём тестовый заказ'):
            cls.track = create_order_and_return_track()

    @allure.title('Проверка успешного получения списка заказов')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    def test_get_orders(self):
        response = requests.get(f'{base_url}/orders')

        assert response.status_code == 200
        assert 'orders' in response.json()

    @classmethod
    def teardown_class(cls):
        with allure.step('Удаляем тестовый заказ'):
            cancel_order([cls.track])
