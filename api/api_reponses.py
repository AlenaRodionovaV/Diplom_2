"""Модуль содержит ключи и значения, которые приходят в ответах на определенные запросы"""


class Responses:
    #  ключи ответа на запрос создания или авторизации пользователя
    CREATE_OR_LOGIN_USER_RESPONSE_KEYS = {"success", "user", "accessToken", "refreshToken"}

    #  ключи ответа на запрос изменения данных пользователя
    CHANGE_USER_INFO_RESPONSE_KEYS = {"success", "user"}

    #  ключи ответа на запрос о создании заказа
    CREATE_ORDER_RESPONSE_KEYS = {"success", "name", "order"}

    #  ключи ответа на запрос получения списка заказов конкретного пользователя
    GET_ORDER_LIST_RESPONSE_KEYS = {"success", "orders", "total", "totalToday"}

    #  тело ответа на запрос удаления пользователя
    DELETE_USER_RESPONSE = {
        "success": False,
        "message": "User already exists"
    }

    #  тело ответа на запрос создания пользователя без указания обязательных полей email/имени/пароля
    NO_REQUIRED_FIELD_RESPONSE = {
        "success": False,
        "message": "Email, password and name are required fields"
    }

    #  тело ответа на запрос авторизации пользователя с указанием некорректного email или пароля
    INCORRECT_EMAIL_OR_PASSWORD_RESPONSE = {
        "success": False,
        "message": "email or password are incorrect"
    }

    #  тело ответа на запрос об изменении данных неавторизованного пользователя
    USER_UNAUTHORISED_RESPONSE = {
        "success": False,
        "message": "You should be authorised"
    }

    #  тело ответа на запрос создания заказа без указания ингредиентов
    CREATE_ORDER_WITHOUT_INGREDIENTS = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }
