
from helpers.requests import register_new_courier_and_return_login_password, delete_courier, login_courier
from helpers.utils import generate_random_string
import urls
import requests
import pytest
import allure


class TestLoginCourier:
    @allure.feature("Авторизация курьера")
    @allure.title("Успешная авторизация курьера")
    def test_courier_can_login(self, courier):
        courier_data, _ = courier

        login = courier_data[0]
        password = courier_data[1]
        with allure.step(f"Пробуем авторизоваться курьером {login}"):
            response = login_courier(login, password)
        with allure.step("Проверяем, что логин успешный"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.feature("Авторизация курьера")
    @allure.title("Попытка авторизации несуществующим пользователем")
    def test_nonexistent_user_cannot_login(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        with allure.step(f"Пробуем авторизоваться несуществующим пользователем {login}"):
            response = login_courier(login, password)
        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 404
            assert "message" in response.json()

    @allure.feature("Авторизация курьера")
    @pytest.mark.parametrize("field", ["login", "password"])
    @allure.title("Авторизация с неверными данными")
    def test_login_with_wrong_credentials_is_not_success(self, courier, field):
        courier_data, _ = courier

        login = courier_data[0]
        password = courier_data[1]

        if field == "login":
            login = generate_random_string(10)
        else:
            password = generate_random_string(10)
        with allure.step(f"Пробуем авторизоваться с неверным полем {field}"):
            response = login_courier(login, password)
        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 404
            assert "message" in response.json()

    @allure.feature("Авторизация курьера")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация с пропущенным обязательным полем")
    def test_login_missing_field_is_not_success(self, missing_field):

        payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10)
        }
        
        payload.pop(missing_field)
        with allure.step(f"Пробуем авторизоваться без поля {missing_field}"):
            response = requests.post(urls.LOGIN_COURIER, data=payload)
        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 400
            assert "message" in response.json()