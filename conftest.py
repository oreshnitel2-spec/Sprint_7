import allure
import pytest
import requests
from helpers.requests import cancel_order, register_new_courier_and_return_login_password, delete_courier, login_courier
from helpers.utils import build_order_payload
import urls
 



@pytest.fixture
def courier():
    with allure.step("Создаём тестового курьера"):
        courier_data = register_new_courier_and_return_login_password()
        login = courier_data[0]
        password = courier_data[1]
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
    yield courier_data, courier_id
    with allure.step(f"Удаляем курьера с ID {courier_id}"):
        delete_courier(courier_id)

@pytest.fixture
def test_order():
    with allure.step("Создаём тестовый заказ"):
        payload = build_order_payload(color=["BLACK"])
        response = requests.post(urls.CREATE_ORDER, json=payload)
        assert response.status_code == 201
        track = response.json()["track"]
    yield track
    with allure.step(f"Отменяем тестовый заказ с track {track}"):
        cancel_order(track)