import time

import requests

from crud import get_users, create_user, update_user, delete_user
from typing import Callable


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

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retry_count):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    last_exception = e
                    print(f"Ошибка запроса: {e}. Повторная попытка...")
                    time.sleep(1)
            raise last_exception

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
    print(response.status_code)


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
