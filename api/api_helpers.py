"""Модуль содержит методы с генерацией и удалением тестовых данных"""
import requests
from faker import Faker

from api.api_urls import Urls

fake = Faker('ru_RU')


# генерируем случайный email
def email_generate():
    email = fake.email()
    return email


# генерируем случайный пароль
def password_generate():
    password = fake.password(length = 10, special_chars = False, digits = False, upper_case = False, lower_case = True)
    return password


#  генерируем случайное имя пользователя
def first_name_generate():
    first_name = fake.first_name()
    return first_name


#  удаляем созданного пользователя
def delete_user(response_for_delete_json=None):
    payload_for_delete = {
        "refreshToken": response_for_delete_json['refreshToken']
    }
    headers_for_delete = {
        "Authorization": response_for_delete_json['accessToken']
    }
    delete_user_response = requests.delete(Urls.GET_USER_INFO_URL, data = payload_for_delete,
                                           headers = headers_for_delete)
    assert delete_user_response.status_code == 202
