"""Модуль содержит вспомогательную тестовую информацию"""
from api.api_helpers import password_generate, first_name_generate, email_generate


class Data:
    #  тело запроса без поля email
    payload_without_email = {
        "email": "",
        "password": password_generate(),
        "name": first_name_generate()
    }
    #  тело запроса без поля password
    payload_without_password = {
        "email": email_generate(),
        "password": "",
        "name": first_name_generate()
    }

    #  тело запроса без поля name
    payload_without_name = {
        "email": email_generate(),
        "password": password_generate(),
        "name": ""
    }
