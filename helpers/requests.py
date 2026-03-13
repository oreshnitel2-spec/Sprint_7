import requests
import random
import string
from helpers.utils import generate_random_string
import urls 
import allure

@allure.step("Регистрируем нового курьера")
def register_new_courier_and_return_login_password():
    
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

 
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(urls.CREATE_COURIER, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass 

@allure.step("Удаляем курьера с ID {courier_id}")
def delete_courier(courier_id):
    response = requests.delete(
        f"{urls.CREATE_COURIER}/{courier_id}")
    return response

@allure.step("Авторизация курьера")
def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }

    response = requests.post(urls.LOGIN_COURIER,data=payload)
    return response

@allure.step("Отмена заказа с треком {track}")
def cancel_order(track):
    response = requests.put(urls.CANCEL_ORDER, params={"track": track})
    return response