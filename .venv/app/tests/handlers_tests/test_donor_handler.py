import unittest
from unittest.mock import MagicMock
from flask import Flask
from app.handlers.donor_handler import DonorHandler
from app.models.signup import UserSignup
from app.models.user import User
from app.utils.errors.custom_errors import UserExistsError, DatabaseError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType


class TestDonorHandler(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()

        self.mock_donor_service = MagicMock()
        self.donor_handler = DonorHandler(self.mock_donor_service)
        self.valid_request_data = {
            "email": "test@gmail.com",
            "password": "StrongP@ss123",
            "phone_no": "1234567890",
            "name": "Test User",
            "address": "123 Test St"
        }

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_create_donor_success(self):
        with self.app.test_request_context(json=self.valid_request_data):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 201)
            self.assertEqual(response["status_code"], 201)
            self.assertEqual(response["message"], "Success")
            self.mock_donor_service.signup.assert_called_once()

    def test_create_donor_missing_request_body(self):
        with self.app.test_request_context(json={}):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 400)
            self.assertEqual(response["message"], "Missing Request body")
            self.mock_donor_service.signup.assert_not_called()

    def test_create_donor_missing_required_fields(self):
        invalid_data = self.valid_request_data.copy()
        del invalid_data["email"]
        with self.app.test_request_context(json=invalid_data):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], "Missing required fields")
            self.mock_donor_service.signup.assert_not_called()

    def test_create_donor_invalid_email(self):
        invalid_data = self.valid_request_data.copy()
        invalid_data["email"] = "invalid-email"
        with self.app.test_request_context(json=invalid_data):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], "Invalid email id")
            self.mock_donor_service.signup.assert_not_called()

    def test_create_donor_invalid_phone(self):
        invalid_data = self.valid_request_data.copy()
        invalid_data["phone_no"] = "123"  # Invalid phone number
        with self.app.test_request_context(json=invalid_data):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], "Invalid phone number")
            self.mock_donor_service.signup.assert_not_called()

    def test_create_donor_weak_password(self):
        invalid_data = self.valid_request_data.copy()
        invalid_data["password"] = "weak"
        with self.app.test_request_context(json=invalid_data):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], "Password not strong")
            self.mock_donor_service.signup.assert_not_called()

    def test_create_donor_user_exists(self):
        with self.app.test_request_context(json=self.valid_request_data):
            # Arrange
            self.mock_donor_service.signup.side_effect = UserExistsError(f'{self.valid_request_data['email']}')

            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], f'User with email {self.valid_request_data['email']} already exists')

    def test_create_donor_database_error(self):
        with self.app.test_request_context(json=self.valid_request_data):
            # Arrange
            self.mock_donor_service.signup.side_effect = DatabaseError("Database connection failed")

            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 500)
            self.assertEqual(response["message"], "Internal server error")

    def test_create_donor_bad_request(self):
        with self.app.test_request_context('/',content_type="application/json"):
            # Arrange - force BadRequest exception
            self.app.test_client().post('/', data='invalid json')

            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 400)
            self.assertEqual(response["message"], "Invalid request body format")

    def test_create_donor_unsupported_media_type(self):
        with self.app.test_request_context('/', content_type='text/plain'):
            # Act
            response, status_code = self.donor_handler.create_donor()

            # Assert
            self.assertEqual(status_code, 415)
            self.assertEqual(response["message"], "Unsupported media type, Expected application/json")


if __name__ == '__main__':
    unittest.main()