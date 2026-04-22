import pytest
import allure
from helpers import register_new_courier_and_return_courier_data, get_courier_id, delete_couriers, generate_new_courier_data, send_create_courier_request
from data import wrong_payload_for_create

class TestCreateCourier:

    @classmethod
    def setup_class(cls):
        cls.courier_ids = []

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    def test_create_courier(self):
        payload = generate_new_courier_data()

        response = send_create_courier_request(payload)

        self.courier_ids.append(get_courier_id([payload['login'], payload['password']]))

        assert response.status_code == 201
        assert response.json()['ok'] == True

    @allure.title('Проверка НЕуспешного создания курьера, когда логин уже занят')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    def test_create_courier_with_exist_login_failed(self):
        courier_data = register_new_courier_and_return_courier_data()

        self.courier_ids.append(get_courier_id([courier_data[0], courier_data[1]]))

        payload = {
        "login": courier_data[0],
        "password": courier_data[1],
        "firstName": courier_data[2]
        }

        response = send_create_courier_request(payload)
        assert response.status_code == 409
        assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Проверка НЕуспешного создания курьера, когда не переданы обязательные параметры')
    @allure.description('Отправляем запрос и проверяем статус и содержимое ответа')
    @pytest.mark.parametrize('payload', wrong_payload_for_create)
    def test_create_courier_missing_parameters_failed(self, payload):
        response = send_create_courier_request(payload)
        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи"

    @classmethod
    def teardown_class(cls):
        with allure.step('Удаляем тестового курьера'):
            delete_couriers(cls.courier_ids)
