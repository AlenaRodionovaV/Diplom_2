"""Модуль содержит автотесты, проверяющие сценарии получения заказов конкретного пользователя"""
import allure
import requests
import pytest
from api.api_helpers import email_generate, password_generate, first_name_generate, delete_user
from api.api_reponses import Responses
from api.api_urls import Urls


class TestGetOrderList:
    @allure.title('Проверка успешного получения списка заказов')
    @allure.description('Проверяем, что авторизованному пользоветлю можно получить список заказов')
    def test_get_user_order_list_authorised(self):
        payload = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload)
        response_for_delete_json = create_user_response.json()
        headers_for_order_list = {
            "Authorization": response_for_delete_json['accessToken']
        }
        #  отправляем запрос на получение списка заказов пользователя
        get_order_list_response = requests.get(Urls.CREATE_ORDER_URL, headers = headers_for_order_list)
        get_order_list_response_json = get_order_list_response.json()
        #  проверяем статус и тело ответа
        assert (get_order_list_response.status_code == 200 and set(get_order_list_response_json.keys()) ==
                Responses.GET_ORDER_LIST_RESPONSE_KEYS)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    @allure.title('Проверка невозможности получения списка заказов при определенных условиях')
    @allure.description('Проверяем, что неавторизованному пользоветлю нельзя получить список заказов')
    def test_get_user_order_list_unauthorised(self):
        get_order_list_response = requests.get(Urls.CREATE_ORDER_URL)
        assert (get_order_list_response.status_code == 401 and get_order_list_response.json() ==
                Responses.USER_UNAUTHORISED_RESPONSE)
