"""Модуль содержит эндпоинты для отправки тестовых запросов"""


class Urls:
    # основной url
    BASE_URL = 'https://stellarburgers.nomoreparties.site'

    # ручка для создания заказа или получения заказов конретного пользователя
    CREATE_ORDER_URL = f'{BASE_URL}/api/orders'

    # ручка для создания или для регистрации пользователя
    CREATE_USER_URL = f'{BASE_URL}/api/auth/register'

    # ручка для авторизации пользователя
    LOGIN_USER_URL = f'{BASE_URL}/api/auth/login'

    # ручка для выхода пользователя
    LOGOUT_USER_URL = f'{BASE_URL}/api/auth/logout'

    # ручка для обновления токена
    REFRESH_TOKEN_URL = f'{BASE_URL}/api/auth/token'

    # ручка для действий с данными пользвателя: получение/обновление/удаление
    GET_USER_INFO_URL = f'{BASE_URL}/api/auth/user'

    # ручка для получения списка заказов
    GET_ORDER_LIST_URL = f'{BASE_URL}/api/orders/all'
