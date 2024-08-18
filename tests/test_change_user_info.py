"""Модуль содержит автотесты, проверяющие позитивные и негативные сценарии обновления данных пользователя"""
import allure
import requests
import pytest
from api.api_helpers import email_generate, password_generate, first_name_generate, delete_user
from api.api_reponses import Responses
from api.api_urls import Urls


class TestChangeUserInfo:
    @allure.title('Проверка изменения данных пользователя')
    @allure.description('Проверяем, что авторизованный пользователь может менять свои данные')
    def test_change_user_info_authorised(self):
        payload_for_create = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        payload_for_update = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload_for_create)
        response_for_delete_json = create_user_response.json()
        #  достаем access токен для последующего обновления инфы о пользователе
        headers_for_update_info = {
            "Authorization": response_for_delete_json['accessToken']
        }
        # отправляем запрос на логин пользователя
        requests.post(Urls.LOGIN_USER_URL, data = payload_for_create)
        # отправляем запрос на изменение данных пользователя
        update_info_response = requests.patch(Urls.GET_USER_INFO_URL, data = payload_for_update,
                                              headers = headers_for_update_info)
        update_info_response_json = update_info_response.json()
        #  проверяем статус и тело ответа
        assert (update_info_response.status_code == 200 and set(update_info_response_json.keys()) ==
                Responses.CHANGE_USER_INFO_RESPONSE_KEYS)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    @allure.title('Проверка, что данные пользователя нельзя поменять при определенных условиях')
    @allure.description('Проверяем, что неавторизованный пользователь не может поменять свои данные')
    def test_change_user_info_unauthorised(self):
        payload_for_update = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на изменение данных пользователя без авторизации
        update_info_response = requests.patch(Urls.GET_USER_INFO_URL, data = payload_for_update)
        #  проверяем статус и тело ответа
        assert (update_info_response.status_code == 401 and update_info_response.json() ==
                Responses.USER_UNAUTHORISED_RESPONSE)
