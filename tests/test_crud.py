from http import HTTPStatus
from unittest.mock import patch, Mock

import requests

from crud import get_users, create_user, update_user, delete_user


# Тест для функции get_users
@patch('crud.requests.get')
def test_get_users_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = [{"id": 1, "name": "John Doe"}]
    mock_get.return_value = mock_response

    users = get_users()
    assert users == [{"id": 1, "name": "John Doe"}]


@patch('crud.requests.get')
def test_get_users_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.NOT_FOUND
    mock_get.return_value = mock_response

    users = get_users()
    assert users == []


@patch('crud.requests.get')
def test_get_users_request_exception(mock_get):
    mock_get.side_effect = requests.RequestException("Ошибка сети")

    users = get_users()
    assert users == []


# Тест для функции create_user
@patch('crud.requests.post')
def test_create_user_success(mock_post):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.CREATED
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_post.return_value = mock_response

    new_user = create_user({"name": "John Doe"})
    assert new_user == {"id": 1, "name": "John Doe"}


@patch('crud.requests.post')
def test_create_user_request_exception(mock_post):
    mock_post.side_effect = requests.RequestException("Ошибка сети")

    new_user = create_user({"name": "John Doe"})
    assert new_user == {}


# Тест для функции update_user
@patch('crud.requests.put')
def test_update_user_success(mock_put):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {"id": 1, "name": "Jane Doe"}
    mock_put.return_value = mock_response

    updated_user = update_user(1, {"name": "Jane Doe"})
    assert updated_user == {"id": 1, "name": "Jane Doe"}


@patch('crud.requests.put')
def test_update_user_request_exception(mock_put):
    mock_put.side_effect = requests.RequestException("Ошибка сети")

    updated_user = update_user(1, {"name": "Jane Doe"})
    assert updated_user == {}


# Тест для функции delete_user
@patch('crud.requests.delete')
def test_delete_user_success_no_content(mock_delete):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.NO_CONTENT
    mock_delete.return_value = mock_response

    with patch('builtins.print') as mock_print:
        delete_user(1)
        mock_print.assert_any_call("Пользователь успешно удален")


@patch('crud.requests.delete')
def test_delete_user_success_ok(mock_delete):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_delete.return_value = mock_response

    with patch('builtins.print') as mock_print:
        delete_user(1)
        mock_print.assert_any_call("Пользователь успешно удален")


@patch('crud.requests.delete')
def test_delete_user_failure(mock_delete):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.NOT_FOUND
    mock_delete.return_value = mock_response

    with patch('builtins.print') as mock_print:
        delete_user(1)
        mock_print.assert_any_call("Ошибка: 404")


@patch('crud.requests.delete')
def test_delete_user_request_exception(mock_delete):
    mock_delete.side_effect = requests.RequestException("Ошибка сети")

    with patch('builtins.print') as mock_print:
        delete_user(1)
        mock_print.assert_any_call("Ошибка запроса: Ошибка сети")
