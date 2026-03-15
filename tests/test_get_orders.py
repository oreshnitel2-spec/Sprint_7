import pytest
import requests
import urls
from helpers.requests import cancel_order
from helpers.utils import build_order_payload
import allure


class TestGetOrder:

    @allure.feature("Список заказов")
    @allure.title("Список заказов возвращается как словарь со списком orders")
    def test_get_orders_returns_list_with_one_order(self, test_order):
  
        track = test_order
        with allure.step("Отправляем GET запрос на получение списка заказов"):     
            response_list = requests.get(urls.GET_ORDERS)
            assert response_list.status_code == 200, "Запрос списка заказов не успешен"
        with allure.step("Проверяем, что ответ является словарём и содержит список orders"):
            data = response_list.json()
            assert isinstance(data, dict), "Ответ не является словарём"
            assert "orders" in data, "В ответе нет поля 'orders'"
            orders = data["orders"]
            assert isinstance(orders, list), "Поле 'orders' не является списком"
