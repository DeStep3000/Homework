from http import HTTPStatus
from typing import Optional, List, Dict

import requests

API_BASE_URL = 'https://jsonplaceholder.typicode.com'


def get_users(params: Optional[dict] = None) -> List[Dict[str, str]]:
    """
    Функция для получения списка пользователей из внешнего API.

    Параметры:
    - params (dict): Опциональные GET параметры запроса.

    Возвращает:
    - list: Список словарей с данными о пользователях (каждый словарь содержит 'name' и 'email').

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки, например 404 NOT FOUND.
    - Выводит сообщение об ошибке и возвращает None при любой другой HTTP ошибке или сетевой проблеме.
    """
    response = None
    try:
        response = requests.get(f"{API_BASE_URL}/users", params=params, raise_for_status=False)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []

    if response.status_code == HTTPStatus.NOT_FOUND:
        print("Ошибка: Пользователи не найдены (404)")
        return []

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при проверке статуса ответа: {e}")
        return []

    return response.json()


def create_user(data: dict) -> Dict[str, str]:
    """
    Функция для создания нового пользователя в внешнем API.

    Параметры:
    - data (dict): Данные нового пользователя в формате {'name': 'John Doe', 'email': 'johndoe@example.com', ...}.

    Возвращает:
    - dict: Словарь с данными созданного пользователя, включая присвоенный ID.

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки.
    - Выводит сообщение об ошибке при любой другой HTTP ошибке или сетевой проблеме.
    """
    response = None
    try:
        response = requests.post(f"{API_BASE_URL}/users", json=data, raise_for_status=False)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return {}

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при проверке статуса ответа: {e}")
        return {}

    return response.json()


def update_user(user_id: int, data: dict) -> Dict[str, str]:
    """
    Функция для обновления данных о пользователе в внешнем API.

    Параметры:
    - user_id (int): ID пользователя, чьи данные нужно обновить.
    - data (dict): Новые данные пользователя в формате {'name': 'Jane Doe', 'email': 'janedoe@example.com', ...}.

    Возвращает:
    - dict: Словарь с обновленными данными пользователя.

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки.
    - Выводит сообщение об ошибке при любой другой HTTP ошибке или сетевой проблеме.
    """
    response = None
    try:
        response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=data, raise_for_status=False)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return {}

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при проверке статуса ответа: {e}")
        return {}

    return response.json()


def delete_user(user_id: int) -> None:
    """
    Функция для удаления пользователя из внешнего API.

    Параметры:
    - user_id (int): ID пользователя, которого нужно удалить.

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки.
    - Выводит сообщение об успешном удалении пользователя или сообщение об ошибке при любой другой HTTP ошибке или сетевой проблеме.
    """
    response = None
    try:
        response = requests.delete(f"{API_BASE_URL}/users/{user_id}", raise_for_status=False)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return

    if response.status_code == HTTPStatus.NOT_FOUND:
        print("Ошибка: 404")
        return

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при проверке статуса ответа: {e}")
        return

    print("Пользователь успешно удален")
