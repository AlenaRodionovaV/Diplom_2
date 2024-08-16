"""Модуль содержит автотесты, проверяющие позитивные и негативные сценарии авторизации пользователя"""

import requests
import pytest
from api.api_helpers import email_generate, password_generate, first_name_generate, delete_user
from api.api_reponses import Responses
from api.api_urls import Urls


class TestLoginUser:
    def test_login_user(self):
        payload = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        response_for_delete_json = create_user_response.json()
        # отправляем запрос на логин пользователя
        login_user_response = requests.post(Urls.LOGIN_USER_URL, data = payload)
        login_user_response_json = login_user_response.json()
        # проверяем статус и тело ответа
        assert (login_user_response.status_code == 200 and set(login_user_response_json.keys()) ==
                Responses.CREATE_OR_LOGIN_USER_RESPONSE_KEYS)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    def test_login_user_with_incorrect_login_and_password(self):
        payload_for_create = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        payload_for_login = {
            "email": "12345677654321@mail.ru",
            "password": "12121212121212121211212",
            "name": payload_for_create["name"]
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload_for_create)
        response_for_delete_json = create_user_response.json()
        # отправляем запрос на логин пользователя
        login_user_response = requests.post(Urls.LOGIN_USER_URL, data = payload_for_login)
        # проверяем статус и тело ответа
        assert (login_user_response.status_code == 401 and login_user_response.json() ==
                Responses.INCORRECT_EMAIL_OR_PASSWORD_RESPONSE)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)
