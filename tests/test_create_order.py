from urllib import response

import pytest
import requests
import urls
from helpers.requests import cancel_order
from helpers.utils import build_order_payload
import allure


class TestCreateOrder:
    
    @allure.feature("Создание заказа")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Проверка успешного создания заказа с цветами {color}")
    def test_create_order_with_different_colors(self, color):

        payload = build_order_payload(color=color)
        with allure.step("Отправляем POST-запрос на создание заказа"):
            response = requests.post(urls.CREATE_ORDER, json=payload)
            assert response.status_code == 201
        with allure.step("Проверяем, что в ответе есть трек заказа"):
            assert "track" in response.json()
            track = response.json()["track"]
        cancel_order(track)