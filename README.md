# Программа для обучения студентов навыкам работы с библиотекой requests и декораторами.

Этот проект демонстрирует выполнение CRUD операций с использованием библиотеки `requests` и декораторов в Python. 

## Установка

1. Клонируйте репозиторий.
2. Установите необходимые зависимости, выполнив команду:

    ```sh
    pip install -r requirements.txt
    ```

## Файловая структура

- `crud.py` - содержит функции для выполнения CRUD операций.
- `main.py` - пример использования функций из `crud.py`.
- `retry_decorator.py` - декоратор для повторных попыток выполнения запроса.
- `test_crud.py` - тесты для функций в `crud.py`.

## Использование

### CRUD операции

```python
from crud import get_users, create_user, update_user, delete_user

# Получить список пользователей
users = get_users()
print(users)

# Создать нового пользователя
new_user = create_user({"name": "John Doe", "email": "john.doe@example.com"})
print(new_user)

# Обновить существующего пользователя
updated_user = update_user(1, {"name": "Jane Doe"})
print(updated_user)

# Удалить пользователя
delete_user(1)
```

### Декоратор для повторных попыток
```python
from retry_decorator import retry

@retry(retry_count=3)
def make_request():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status()
    return response.json()

try:
    users = make_request()
    print(users)
except requests.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
```

## Тестирование
```shell
pytest test_crud.py
```
