from unittest.mock import patch

import pytest
import requests

from main import retry, make_request


# Тесты для декоратора retry
def test_retry_success():
    @retry(retry_count=3)
    def successful_function():
        return "success"

    assert successful_function() == "success"


def test_retry_failure():
    @retry(retry_count=3)
    def failing_function():
        raise requests.RequestException("Ошибка сети")

    with pytest.raises(requests.RequestException):
        failing_function()


@patch('main.requests.get')
@patch('main.time.sleep', return_value=None)  # Мокаем time.sleep для ускорения тестов
def test_make_request_success(mock_sleep, mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200

    with patch('builtins.print') as mock_print:
        make_request()
        mock_print.assert_any_call("Попытка 1...")
        mock_print.assert_any_call("Запрос успешно выполнен")


@patch('main.requests.get')
@patch('main.time.sleep', return_value=None)  # Мокаем time.sleep для ускорения тестов
def test_make_request_failure(mock_sleep, mock_get):
    mock_get.side_effect = requests.RequestException("Ошибка сети")

    with patch('builtins.print') as mock_print, pytest.raises(requests.RequestException):
        make_request()
        mock_print.assert_any_call("Попытка 1...")
        mock_print.assert_any_call("Ошибка запроса: Ошибка сети. Повторная попытка через 1 секунд...")
        mock_print.assert_any_call("Попытка 2...")
        mock_print.assert_any_call("Попытка 3...")
        mock_print.assert_any_call("Все попытки исчерпаны")
