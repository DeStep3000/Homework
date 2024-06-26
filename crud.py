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
    try:
        response = requests.get(f"{API_BASE_URL}/users", params=params, raise_for_status=False)
        if response.status_code == HTTPStatus.NOT_FOUND:
            print("Ошибка: Пользователи не найдены (404)")
            return []
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return []


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
    try:
        response = requests.post(f"{API_BASE_URL}/users", json=data, raise_for_status=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return {}


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
    try:
        response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=data, raise_for_status=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return {}


def delete_user(user_id: int) -> None:
    """
    Функция для удаления пользователя из внешнего API.

    Параметры:
    - user_id (int): ID пользователя, которого нужно удалить.

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки.
    - Выводит сообщение об успешном удалении пользователя или сообщение об ошибке при любой другой HTTP ошибке или сетевой проблеме.
    """
    try:
        response = requests.delete(f"{API_BASE_URL}/users/{user_id}", raise_for_status=False)
        if response.status_code == HTTPStatus.NOT_FOUND:
            print('Ошибка: 404')
        elif response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.OK):
            print('Пользователь успешно удален')
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        print(f'Ошибка запроса: {e}')
