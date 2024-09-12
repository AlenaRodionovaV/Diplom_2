"""Модуль содержит автотесты, проверяющие позитивные и негативные сценарии создания заказа"""

import requests
import pytest
import allure
from api.api_helpers import email_generate, password_generate, first_name_generate, delete_user
from api.api_reponses import Responses
from api.api_urls import Urls


class TestCreateOrder:
    @allure.title('Проверка успешного создания заказа')
    @allure.description('Проверяем, что при отправке корректных ингредиентов хешем создается заказ')
    def test_create_order_with_ingredients_authorised(self):
        payload_for_create_user = {
            "email": email_generate(),
            "password": password_generate(),
            "name": first_name_generate()
        }
        payload_for_create_order = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6f", "61c0c5a71d1f82001bdaaa71"]
        }
        # отправляем запрос на создание пользователя
        create_user_response = requests.post(Urls.CREATE_USER_URL, data = payload_for_create_user)
        response_for_delete_json = create_user_response.json()
        headers_for_create_order = {
            "Authorization": response_for_delete_json['accessToken']
        }
        # отправляем запрос на логин пользователя
        requests.post(Urls.LOGIN_USER_URL, data = payload_for_create_user)
        # отправляем запрос на создание заказа
        create_order_response = requests.post(Urls.CREATE_ORDER_URL, data = payload_for_create_order,
                                              headers = headers_for_create_order)
        create_order_response_json = create_order_response.json()
        # проверяем статус и тело ответа
        assert (create_order_response.status_code == 200 and set(create_order_response_json.keys()) ==
                Responses.CREATE_ORDER_RESPONSE_KEYS)
        # постусловие: удаляем только что созданного пользователя
        delete_user(response_for_delete_json)

    @allure.title('Проверка, что заказ не создается при определенных условиях')
    @allure.description('Проверяем, что при отправке пустого хеша ингредиентов неавторизованным пользователем заказ '
                        'не создается')
    def test_create_order_without_ingredients_unauthorised(self):
        payload_for_create_order = {
            "ingredients": []
        }
        # отправляем запрос на создание заказа
        create_order_response = requests.post(Urls.CREATE_ORDER_URL, data = payload_for_create_order)
        # проверяем статус и тело ответа
        assert (create_order_response.status_code == 400 and create_order_response.json() ==
                Responses.CREATE_ORDER_WITHOUT_INGREDIENTS)

    @allure.title('Проверка, что заказ не создается при определенных условиях')
    @allure.description('Проверяем, что при отправке некорректных ингредиентов заказ не создается')
    def test_create_order_with_wrong_ingredients(self):
        payload_for_create_order = {
            "ingredients": ["61c0c5a71d1f82001bdaaa71", "121!"]
        }
        # отправляем запрос на создание заказа
        create_order_response = requests.post(Urls.CREATE_ORDER_URL, data = payload_for_create_order)
        # проверяем статус и тело ответа
        assert create_order_response.status_code == 500
