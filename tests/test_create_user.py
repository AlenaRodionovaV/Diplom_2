"""Модуль содержит автотесты, проверяющие позитивные и негативные сценарии создания пользователя"""
import allure
import requests
import pytest
from api.api_helpers import email_generate, password_generate, first_name_generate, delete_user
from api.api_reponses import Responses
from api.api_urls import Urls
from api.api_data import Data


class TestCreateUser:
    @allure.title('Проверка успешного создания пользователя')
    @allure.description('Проверяем, что при отправке корректно заполненных полей email, password, name создается '
                        'пользователь')
    def test_create_user_success(self):
        payload = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        response_for_delete_json = create_user_response.json()
        # проверяем статус и тело ответа
        assert (create_user_response.status_code == 200 and set(response_for_delete_json.keys()) ==
                Responses.CREATE_OR_LOGIN_USER_RESPONSE_KEYS)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    @allure.title('Проверка, что пользователь не создается при определенных условиях')
    @allure.description('Проверяем, что при попытке создать пользователя с уже существующими email, password, '
                        'name пользователь не создается')
    def test_create_user_already_exist(self):
        payload = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        response_for_delete_json = create_user_response.json()
        # отправляем запрос на создание точно такого же пользователя
        user_already_exist_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        # проверяем статус и тело ответа
        assert (user_already_exist_response.status_code == 403 and user_already_exist_response.json() ==
                Responses.DELETE_USER_RESPONSE)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    @allure.title('Проверка, что пользователь не создается при определенных условиях')
    @allure.description('Проверяем, что при попытке создать пользователя без указания email/password/name '
                        'пользователь не создается, т.к. это обязательные поля')
    @pytest.mark.parametrize('payload', [Data.payload_without_email, Data.payload_without_password, Data.payload_without_name])
    def test_create_user_without_required_field(self, payload):
        # отправляем запрос на создание пользователя без указания email
        no_required_field_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        # проверяем статус и тело ответа
        assert (no_required_field_response.status_code == 403 and no_required_field_response.json() ==
                Responses.NO_REQUIRED_FIELD_RESPONSE)
