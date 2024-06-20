import unittest
from unittest.mock import patch, Mock

from requests.exceptions import HTTPError, RequestException

import main


class TestAPIFunctions(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_users_success(self, mock_get):
        # Устанавливаем поведение мока
        mock_response = Mock()
        mock_response.json.return_value = [
            {'name': 'Leanne Graham', 'email': 'Sincere@april.biz'},
            {'name': 'Ervin Howell', 'email': 'Shanna@melissa.tv'}
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Вызываем функцию, которую тестируем
        result = main.get_users(params={'_limit': 2})

        # Проверяем, что функция вернула ожидаемый результат
        self.assertEqual(result, [
            {'name': 'Leanne Graham', 'email': 'Sincere@april.biz'},
            {'name': 'Ervin Howell', 'email': 'Shanna@melissa.tv'}
        ])

    @patch('main.requests.get')
    def test_get_users_http_error(self, mock_get):
        # Устанавливаем поведение мока для HTTPError
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # Вызываем функцию, которую тестируем
        result = main.get_users(params={'_limit': 2})

        # Проверяем что функция обработала ошибку корректно
        self.assertIsNone(result)

    @patch('main.requests.get')
    def test_get_users_request_exception(self, mock_get):
        # Устанавливаем поведение мока для RequestException
        mock_get.side_effect = RequestException("Connection error")

        # Вызываем функцию, которую тестируем
        result = main.get_users(params={'_limit': 2})

        # Проверяем что функция обработала ошибку корректно
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
