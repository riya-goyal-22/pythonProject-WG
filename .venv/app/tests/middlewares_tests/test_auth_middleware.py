import unittest
from unittest.mock import MagicMock
from flask import Flask, g
from app.middlewares.auth_middleware import auth_middleware
from app.models.response import CustomResponse
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError
from app.config.config import TOKEN_MISSING, TOKEN_INVALID, TOKEN_EXPIRED
from app.utils.utilities.token import decode_token


class TestAuthMiddleware(unittest.TestCase):
    def setUp(self):
        # Create a basic Flask app for testing
        self.app = Flask(__name__)
        self.app.add_url_rule('/user/login', 'login', lambda: 'login')
        self.app.add_url_rule('/user/signup', 'signup', lambda: 'signup')
        self.app.add_url_rule('/protected', 'protected', lambda: 'protected')

    def test_auth_middleware_missing_token(self):
        # Test the case where no token is provided
        mock_request = MagicMock()
        mock_request.headers.get.return_value = None  # No 'Authorization' header

        with self.app.test_request_context('/protected', headers={'Authorization': None}):
            response = auth_middleware()
            self.assertEqual(response[1], 401)
            self.assertEqual(response[0], CustomResponse(TOKEN_MISSING, "Unauthorized-Missing Token", None).to_dict())

    def test_auth_middleware_invalid_token_format(self):
        # Test case where token is not in 'Bearer <token>' format
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "InvalidTokenFormat"  # Invalid token format

        with self.app.test_request_context('/protected', headers={'Authorization': "InvalidTokenFormat"}):
            response = auth_middleware()
            self.assertEqual(response[1], 401)
            self.assertEqual(response[0], CustomResponse(TOKEN_MISSING, "Unauthorized-Missing Token", None).to_dict())

    def test_auth_middleware_valid_token(self):
        # Test case where a valid token is provided
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "Bearer validtoken123"  # Valid 'Bearer <token>'

        # Create MagicMock for decode_token to simulate successful token decoding
        mock_decode_token = MagicMock(return_value={'user_id': '12345', 'role': 'admin'})

        with self.app.test_request_context('/protected', headers={'Authorization': "Bearer validtoken123"}):
            # Temporarily assign MagicMock to decode_token in the middlewares
            with unittest.mock.patch('app.middlewares.auth_middleware.decode_token', mock_decode_token):
                response = auth_middleware()
                self.assertIsNone(response)  # No response means the middleware allowed the request
                self.assertEqual(g.user_id, '12345')
                self.assertEqual(g.role, 'admin')

        # Ensure decode_token was called with the correct token
        mock_decode_token.assert_called_once_with('validtoken123')

    def test_auth_middleware_token_invalid_payload(self):
        # Test case where token payload is invalid (missing user_id or role)
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "Bearer validtoken123"

        # Create MagicMock for decode_token to return invalid payload
        mock_decode_token = MagicMock(return_value={'user_id': None, 'role': None})

        with self.app.test_request_context('/protected', headers={'Authorization': "Bearer validtoken123"}):
            # Temporarily assign MagicMock to decode_token
            with unittest.mock.patch('app.middlewares.auth_middleware.decode_token', mock_decode_token):
                response = auth_middleware()
                self.assertEqual(response[1], 401)
                self.assertEqual(response[0],
                                 CustomResponse(TOKEN_INVALID, "Unauthorized, invalid token payload", None).to_dict())

    def test_auth_middleware_token_expired(self):
        # Test case where the token is expired
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "Bearer expiredtoken123"

        # Simulate TokenExpiredError exception with MagicMock
        mock_decode_token = MagicMock(side_effect=TokenExpiredError())

        with self.app.test_request_context('/protected', headers={'Authorization': "Bearer expiredtoken123"}):
            # Temporarily assign MagicMock to decode_token
            with unittest.mock.patch('app.middlewares.auth_middleware.decode_token', mock_decode_token):
                response = auth_middleware()
                self.assertEqual(response[1], 401)
                self.assertEqual(response[0], CustomResponse(TOKEN_EXPIRED, "Token expired", None).to_dict())

    def test_auth_middleware_token_invalid(self):
        # Test case where the token is invalid
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "Bearer invalidtoken123"

        # Simulate TokenInvalidError exception with MagicMock
        mock_decode_token = MagicMock(side_effect=TokenInvalidError())

        with self.app.test_request_context('/protected', headers={'Authorization': "Bearer invalidtoken123"}):
            # Temporarily assign MagicMock to decode_token
            with unittest.mock.patch('app.middlewares.auth_middleware.decode_token', mock_decode_token):
                response = auth_middleware()
                self.assertEqual(response[1], 401)
                self.assertEqual(response[0], CustomResponse(TOKEN_INVALID, "Token Invalid", None).to_dict())


if __name__ == '__main__':
    unittest.main()
