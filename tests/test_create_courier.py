import requests
from helpers.requests import register_new_courier_and_return_login_password, delete_courier, login_courier
from helpers.utils import generate_random_string, build_courier_payload
import urls
import pytest
import allure


class TestCreateCourier:

    @allure.feature("Cоздание курьера")
    @allure.title("Курьер успешно создаётся")
    def test_create_courier_is_success(self, courier):
        courier_data, _ = courier
        with allure.step("Проверяем, что данные курьера не пустые"):
            assert len(courier_data) > 0, "Курьер не был создан"

    @allure.feature("Cоздание курьера")  
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_is_not_success(self, courier):
        courier_data, _ = courier
        with allure.step("Проверяем, что данные курьера не пустые"):
            assert len(courier_data) > 0, "Курьер не был создан"
        
        login = courier_data[0]
        password = courier_data[1]
        first_name = courier_data[2]

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        with allure.step(f"Пробуем создать курьера с уже существующими данными: {payload}"):
            response = requests.post(urls.CREATE_COURIER, data=payload)
        with allure.step("Проверяем, что ответ содержит ошибку 409 и сообщение"):    
            assert response.status_code == 409, "Повторный курьер был создан"
            assert "message" in response.json(), "В ответе нет поля message"

    @allure.feature("Cоздание курьера")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Создание курьера с пропущенным обязательным полем {missing_field}")
    def test_create_courier_missing_field(self, missing_field):

        payload = build_courier_payload()
        with allure.step(f"Удаляем обязательное поле '{missing_field}' из payload"):
            payload.pop(missing_field)
        with allure.step(f"Пробуем создать курьера с payload: {payload}"):       
            response = requests.post(urls.CREATE_COURIER, data=payload)
        with allure.step("Проверяем, что ответ содержит ошибку 400 и сообщение"):
            assert response.status_code == 400, f"Отсутствие поля {missing_field} не дало ошибку"
            assert "message" in response.json()

    @allure.feature("Cоздание курьера")
    @allure.title("Проверка корректного ответа при успешном создании курьера")
    def test_create_courier_returns_correct_response(self):
        payload = build_courier_payload()
        with allure.step(f"Создаём курьера с payload: {payload}"):
            response = requests.post(urls.CREATE_COURIER, data=payload)
        with allure.step("Проверяем, что ответ успешный и содержит {'ok': True}"):
            assert response.status_code == 201, "Курьер не был создан"
            assert response.json() == {"ok": True}, f"Ожидался ответ {{'ok': True}}, но вернулось {response.json()}"
        with allure.step("Удаляем созданного курьера"):
            login_response = login_courier(payload["login"], payload["password"])
            courier_id = login_response.json()["id"]
            delete_courier(courier_id)