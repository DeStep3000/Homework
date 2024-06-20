import pytest
from unittest.mock import patch, Mock
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
def test_make_request_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200

    make_request()


@patch('main.requests.get')
def test_make_request_failure(mock_get):
    mock_get.side_effect = requests.RequestException

    with pytest.raises(requests.RequestException):
        make_request()
