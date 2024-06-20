import time
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
    url = f"{API_BASE_URL}/users"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f'Ошибка 404: Пользователи не найдены ({err})')
        else:
            print(f'HTTP ошибка: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Сетевая ошибка: {err}')


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
    url = f'{API_BASE_URL}/users'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f'HTTP ошибка при создании пользователя: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Сетевая ошибка при создании пользователя: {err}')


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
    url = f'{API_BASE_URL}/users/{user_id}'
    try:
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f'HTTP ошибка при обновлении пользователя: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Сетевая ошибка при обновлении пользователя: {err}')


def delete_user(user_id: int) -> None:
    """
    Функция для удаления пользователя из внешнего API.

    Параметры:
    - user_id (int): ID пользователя, которого нужно удалить.

    Поведение при ошибке:
    - Обрабатывает HTTP ошибки.
    - Выводит сообщение об успешном удалении пользователя или сообщение об ошибке при любой другой HTTP ошибке или сетевой проблеме.
    """
    url = f'{API_BASE_URL}/users/{user_id}'
    try:
        response = requests.delete(url)
        response.raise_for_status()
        if response.status_code == 200:
            print(f'Пользователь с id = {user_id} успешно удалён.')
    except requests.exceptions.HTTPError as err:
        print(f'HTTP ошибка при удалении пользователя: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Сетевая ошибка при удалении пользователя: {err}')


# Декоратор для повторных попыток при сетевой ошибке

def retry(retry_count: int) -> callable:
    """
    Декоратор для повторной попытки выполнения функции при сетевой ошибке.

    Параметры:
    - retry_count (int): Количество попыток повтора.

    Возвращает:
    - Результат выполнения декорированной функции или возбуждает исключение при неудаче всех попыток.

    Поведение при ошибке:
    - Повторяет выполнение декорированной функции указанное количество раз при сетевых ошибках.
    - При неудаче всех попыток выводит сообщение об ошибке и возбуждает исключение.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retry_count):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt < retry_count - 1:
                        print(f'Попытка {attempt + 1} не удалась. Повторная попытка через 3 секунды...')
                        time.sleep(3)
                    else:
                        print(f'Все {retry_count} попыток завершились ошибкой: {e}')
                        raise

        return wrapper

    return decorator


@retry(retry_count=3)
def make_request() -> None:
    """
    Пример функции для демонстрации работы декоратора retry.
    Эта функция будет декорирована декоратором retry и будет повторяться при сетевых ошибках.

    Поведение при ошибке:
    - Если не удается выполнить запрос после всех попыток, возбуждается исключение.
    """
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    response.raise_for_status()
    return response.json()


def main() -> None:
    """
    Основная функция программы.
    """

    print('Получение списка пользователей:')
    users = get_users(params={'_limit': 5})
    if users:
        for user in users:
            print(f'Имя: {user['name']}, Email: {user['email']}')

    print('\nСоздание нового пользователя:')
    new_user_data = {
        'name': 'John Doe',
        'username': 'johndoe',
        'email': 'johndoe@tinkoff.com',
    }
    created_user = create_user(new_user_data)
    if created_user:
        print(f'Новый пользователь создан: {created_user}')

    print('\nОбновление информации о пользователе:')
    user_id_to_update = 1
    updated_user_data = {
        'name': 'Jane Doe',
        'username': 'janedoe',
        'email': 'janedoe@yandex.com',
    }
    updated_user = update_user(user_id_to_update, updated_user_data)
    if updated_user:
        print(f'Информация о пользователе с id = {user_id_to_update} обновлена: {updated_user}')

    print("\nУдаление пользователя:")
    user_id_to_delete = 1
    delete_user(user_id_to_delete)

    print("\nПример использования декоратора для повторных попыток:")
    try:
        make_request()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при выполнении запроса: {e}')


if __name__ == "__main__":
    main()
