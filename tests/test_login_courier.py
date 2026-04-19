import requests
import allure
import pytest
from helpers import delete_couriers, register_new_courier_and_return_login_password, get_courier_id
from urls import base_url

class TestLoginCourier:
    courier_data = []
    courier_id = ''

    @classmethod
    def setup_class(cls):
        with allure.step('Создаём тестового курьера'):
            cls.courier_data = register_new_courier_and_return_login_password()
            cls.courier_id = get_courier_id(cls.courier_data)

    @allure.title('Проверка успешного логина курьера')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    def test_login_courier(self):
        payload = {
        "login": self.courier_data[0],
        "password": self.courier_data[1]
        }

        response = requests.post(f'{base_url}/courier/login', json=payload)
        assert response.status_code == 200
        assert 'id' in response.json()

    #тест с отсутствующим паролем падает из-за 504 ошибки
    @allure.title('Проверка НЕуспешного логина курьера, когда отсутствуют обязательные параметры')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    @pytest.mark.parametrize('missing_param', ['login', 'password'])
    def test_login_courier_missing_parameters_failed(self, missing_param):
        payload = {
            "login": self.courier_data[0],
            "password": self.courier_data[1]
        }
        payload.pop(missing_param)
        
        response = requests.post(f'{base_url}/courier/login', json=payload)
        
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Проверка НЕуспешного логина курьера, когда логин или пароль неверные')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    @pytest.mark.parametrize('wrong_param', ['login', 'password'])
    def test_login_courier_wrong_parameters_failed(self, wrong_param):
        payload = {
            "login": self.courier_data[0],
            "password": self.courier_data[1]
        }
        payload[wrong_param] = "wrong_value"
        
        response = requests.post(f'{base_url}/courier/login', json=payload)
        
        assert response.status_code == 404
        assert response.json()['message'] == 'Учетная запись не найдена'

    @classmethod
    def teardown_class(cls):
        with allure.step('Удаляем тестового курьера'):
            delete_couriers([cls.courier_id])
