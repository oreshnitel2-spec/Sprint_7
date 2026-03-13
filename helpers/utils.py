import random
import string
import allure

def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

@allure.step("Собираем payload для курьера")
def build_courier_payload(login=None, password=None, first_name="TestName"):
    login = login or generate_random_string(10)
    password = password or generate_random_string(10)
    return {"login": login, "password": password, "firstName": first_name}


@allure.step("Собираем payload для заказа, цвета: {color}")
def build_order_payload(color=None):
   
    return {
        "firstName": "Leon",
        "lastName": "Kennedy",
        "address": "Racoon city, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-06-12",
        "comment": generate_random_string(20),
        "color": color or []
    }