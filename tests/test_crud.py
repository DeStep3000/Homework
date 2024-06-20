import pytest
from pytest import raises
from unittest.mock import patch
import requests
from crud import get_users, create_user, update_user, delete_user


# Тесты для функции get_users
@patch('crud.requests.get')
def test_get_users_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [{'name': 'John Doe', 'email': 'john@example.com'}]

    result = get_users()
    assert result == [{'name': 'John Doe', 'email': 'john@example.com'}]


@patch('crud.requests.get')
def test_get_users_not_found(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 404

    result = get_users()
    assert result == []


@patch('crud.requests.get')
def test_get_users_request_exception(mock_get):
    mock_get.side_effect = requests.RequestException

    result = get_users()
    assert result == []


# Тесты для функции create_user
@patch('crud.requests.post')
def test_create_user_success(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 201
    mock_response.json.return_value = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}

    result = create_user({'name': 'John Doe', 'email': 'john@example.com'})
    assert result == {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}


@patch('crud.requests.post')
def test_create_user_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 400

    result = create_user({'name': 'John Doe', 'email': 'john@example.com'})
    assert result == {}


@patch('crud.requests.post')
def test_create_user_request_exception(mock_post):
    mock_post.side_effect = requests.RequestException

    result = create_user({'name': 'John Doe', 'email': 'john@example.com'})
    assert result == {}


# Тесты для функции update_user
@patch('crud.requests.put')
def test_update_user_success(mock_put):
    mock_response = mock_put.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': 1, 'name': 'Jane Doe', 'email': 'jane@example.com'}

    result = update_user(1, {'name': 'Jane Doe', 'email': 'jane@example.com'})
    assert result == {'id': 1, 'name': 'Jane Doe', 'email': 'jane@example.com'}


@patch('crud.requests.put')
def test_update_user_failure(mock_put):
    mock_response = mock_put.return_value
    mock_response.status_code = 400

    result = update_user(1, {'name': 'Jane Doe', 'email': 'jane@example.com'})
    assert result == {}


@patch('crud.requests.put')
def test_update_user_request_exception(mock_put):
    mock_put.side_effect = requests.RequestException

    result = update_user(1, {'name': 'Jane Doe', 'email': 'jane@example.com'})
    assert result == {}


# Тесты для функции delete_user
@patch('crud.requests.delete')
def test_delete_user_success(mock_delete):
    mock_response = mock_delete.return_value
    mock_response.status_code = 204

    result = delete_user(1)
    assert result is None  # У функции delete_user нет возвращаемого значения


@patch('crud.requests.delete')
def test_delete_user_failure(mock_delete):
    mock_response = mock_delete.return_value
    mock_response.status_code = 400

    result = delete_user(1)
    assert result is None  # У функции delete_user нет возвращаемого значения


@patch('crud.requests.delete')
def test_delete_user_request_exception(mock_delete):
    mock_delete.side_effect = requests.RequestException

    result = delete_user(1)
    assert result is None  # У функции delete_user нет возвращаемого значения
