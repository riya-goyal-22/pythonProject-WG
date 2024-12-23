import unittest
from unittest import mock
from datetime import datetime, timedelta
import json
import flask
from flask import Flask, g
from app.config.config import UNEXPECTED_ERROR
from app.middlewares.logger_middleware import (
    _sanitize_body,
    log_request_middleware,
    log_response_middleware,
    log_exceptions
)


class TestLoggingMiddleware(unittest.TestCase):
    def setUp(self):
        # Create Flask app for testing
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create test client
        self.client = self.app.test_client()

        # Mock logger
        self.mock_logger = mock.Mock()

        # Mock datetime
        self.mock_datetime = datetime(2024, 1, 1, 12, 0)
        self.mock_ist_time = (self.mock_datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

    def tearDown(self):
        self.app_context.pop()

    def test_sanitize_body_with_password(self):
        # Arrange
        test_body = {
            "username": "testuser",
            "password": "secretpassword",
            "email": "test@example.com"
        }

        # Act
        result = _sanitize_body(test_body)

        # Assert
        self.assertEqual(result["password"], "****")
        self.assertEqual(result["username"], "testuser")
        self.assertEqual(result["email"], "test@example.com")

    def test_sanitize_body_without_password(self):
        # Arrange
        test_body = {
            "username": "testuser",
            "email": "test@example.com"
        }

        # Act
        result = _sanitize_body(test_body)

        # Assert
        self.assertEqual(result, test_body)

    def test_sanitize_body_non_dict(self):
        # Arrange
        test_body = "plain text body"

        # Act
        result = _sanitize_body(test_body)

        # Assert
        self.assertEqual(result, test_body)

    @mock.patch('datetime.datetime')
    def test_log_request_middleware(self, mock_dt):
        # Arrange
        mock_dt.utcnow.return_value = self.mock_datetime

        with self.app.test_request_context(
                '/api',
                method='POST',
                json={'key': 'value'},
                headers={'Content-Type': 'application/json'}
        ):
            # Set g context
            g.user_id = '123'
            g.user_role = 'admin'

            # Act
            log_request_middleware(self.mock_logger)

            # Assert
            self.mock_logger.info.assert_called_once()
            log_call = self.mock_logger.info.call_args[0][0]
            log_data = json.loads(log_call)

            self.assertEqual(log_data['timestamp'], self.mock_ist_time)
            self.assertEqual(log_data['method'], 'POST')
            self.assertEqual(log_data['url'], 'http://localhost/api')
            self.assertEqual(log_data['user_id'], '123')
            self.assertEqual(log_data['user_role'], 'admin')

    @mock.patch('datetime.datetime')
    def test_log_response_middleware(self, mock_dt):
        # Arrange
        mock_dt.utcnow.return_value = self.mock_datetime

        with self.app.test_request_context('/api', method='GET'):
            # Set g context
            g.user_id = '123'
            g.user_role = 'admin'

            # Create mock response
            mock_response = flask.Response(
                response=json.dumps({'data': 'test'}),
                status=200,
                mimetype='application/json'
            )

            # Act
            result = log_response_middleware(self.mock_logger, mock_response)

            # Assert
            self.mock_logger.info.assert_called_once()
            log_call = self.mock_logger.info.call_args[0][0]
            log_data = json.loads(log_call)

            self.assertEqual(log_data['timestamp'], self.mock_ist_time)
            self.assertEqual(log_data['status_code'], 200)
            self.assertEqual(log_data['method'], 'GET')
            self.assertEqual(log_data['url'], 'http://localhost/api')
            self.assertEqual(result, mock_response)

    @mock.patch('datetime.datetime')
    def test_log_exceptions(self, mock_dt):
        # Arrange
        mock_dt.utcnow.return_value = self.mock_datetime

        with self.app.test_request_context(
                '/api',
                method='POST',
                json={'key': 'value'},
                headers={'Content-Type': 'application/json'}
        ):
            # Set g context
            g.user_id = '123'
            g.user_role = 'admin'

            # Create test exception
            test_exception = ValueError("Test error")

            # Act
            response, status_code = log_exceptions(self.mock_logger, test_exception)

            # Assert
            self.mock_logger.error.assert_called_once()
            log_call = self.mock_logger.error.call_args[0][0]
            log_data = json.loads(log_call)

            self.assertEqual(log_data['timestamp'], self.mock_ist_time)
            self.assertEqual(log_data['error_message'], "Test error")
            self.assertEqual(log_data['request_method'], 'POST')
            self.assertEqual(log_data['user_id'], '123')
            self.assertEqual(log_data['user_role'], 'admin')

            self.assertEqual(status_code, 500)
            self.assertEqual(response.message, "An unexpected error occurred")
            self.assertEqual(response.status_code, UNEXPECTED_ERROR)
            self.assertIsNone(response.data)

    @mock.patch('datetime.datetime')
    def test_log_exceptions_with_password_in_body(self, mock_dt):
        # Arrange
        mock_dt.utcnow.return_value = self.mock_datetime

        with self.app.test_request_context(
                '/api',
                method='POST',
                json={
                    'username': 'testuser',
                    'password': 'secret123',
                    'email': 'test@example.com'
                },
                headers={'Content-Type': 'application/json'}
        ):
            # Set g context
            g.user_id = '123'
            g.user_role = 'admin'

            # Act
            response, status_code = log_exceptions(self.mock_logger, ValueError("Test error"))

            # Assert
            log_call = self.mock_logger.error.call_args[0][0]
            log_data = json.loads(log_call)

            # Check that password is sanitized in the logged request body
            self.assertEqual(log_data['request_body']['password'], '****')
            self.assertEqual(log_data['request_body']['username'], 'testuser')


if __name__ == '__main__':
    unittest.main()