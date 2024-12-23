import unittest
from unittest.mock import MagicMock
from app.handlers.user_handler import UserHandler
from app.models.login import UserLogin
from app.models.user_dto import User_DTO
from app.utils.errors.custom_errors import DatabaseError, InvalidCredentialsError, NotExistsError
from flask import g, Flask
from werkzeug.exceptions import BadRequest, UnsupportedMediaType


class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Mock the service
        self.mock_service = MagicMock()
        self.handler = UserHandler(self.mock_service)

        # Mock request context for endpoints that need it
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_get_profile_success(self):
        with self.app.test_request_context():
            # Arrange
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.name = "Test User"
            mock_user.address = "Test Address"
            mock_user.email = "test@gmail.com"
            mock_user.role = "user"
            mock_user.phone_no = "1234567890"

            self.mock_service.get_profile.return_value = mock_user
            g.user_id = 1

            # Act
            response, status_code = self.handler.get_profile()

            # Assert
            self.assertEqual(status_code, 200)
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['message'], "Successfully viewed user profile")
            self.assertEqual(response['data']['id'], 1)
            self.assertEqual(response['data']['email'], "test@gmail.com")

    def test_get_profile_database_error(self):
        with self.app.test_request_context():
            # Arrange
            self.mock_service.get_profile.side_effect = DatabaseError("Internal server error")
            g.user_id = 1

            # Act
            response, status_code = self.handler.get_profile()

            # Assert
            self.assertEqual(status_code, 500)
            self.assertEqual(response['message'], "Internal server error")

    def test_login_success(self):
        with self.app.test_request_context(json={
            "email": "test@example.com",
            "password": "password123"
        }):
            # Arrange
            mock_token = {"token": "test_token"}
            self.mock_service.login.return_value = mock_token

            # Act
            response, status_code = self.handler.login()

            # Assert
            self.assertEqual(status_code, 200)
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['message'], "Successful login")
            self.assertEqual(response['data'], mock_token)

    def test_login_missing_body(self):
        with self.app.test_request_context(json={}):
            # Act
            response, status_code = self.handler.login()

            # Assert
            self.assertEqual(status_code, 400)
            self.assertEqual(response['message'], "Missing Request body")

    def test_login_invalid_credentials(self):
        with self.app.test_request_context(json={
            "email": "test@example.com",
            "password": "wrong_password"
        }):
            # Arrange
            self.mock_service.login.side_effect = InvalidCredentialsError("Invalid credentials")

            # Act
            response, status_code = self.handler.login()

            # Assert
            self.assertEqual(status_code, 401)
            self.assertEqual(response['message'], "Invalid credentials")

    def test_get_list_of_ngos_success(self):
        with self.app.test_request_context():
            # Arrange
            mock_ngo1 = MagicMock()
            mock_ngo1.to_dict.return_value = {"id": 1, "name": "NGO1"}
            mock_ngo2 = MagicMock()
            mock_ngo2.to_dict.return_value = {"id": 2, "name": "NGO2"}
            self.mock_service.get_all_ngos.return_value = [mock_ngo1, mock_ngo2]

            # Act
            response, status_code = self.handler.get_list_of_ngos()

            # Assert
            self.assertEqual(status_code, 200)
            self.assertEqual(len(response['data']), 2)
            self.assertEqual(response['message'], "Successfully retreived list of NGOs")

    def test_get_one_ngo_success(self):
        with self.app.test_request_context():
            # Arrange
            mock_ngo = MagicMock()
            mock_ngo.to_dict.return_value = {"id": 1, "name": "NGO1"}
            self.mock_service.get_ngo_by_id.return_value = mock_ngo

            # Act
            response, status_code = self.handler.get_one_ngo(1)

            # Assert
            self.assertEqual(status_code, 200)
            self.assertEqual(response['data']['id'], 1)
            self.assertEqual(response['message'], "Success")

    def test_get_one_ngo_not_found(self):
        with self.app.test_request_context():
            # Arrange
            self.mock_service.get_ngo_by_id.side_effect = NotExistsError("NGO not found")

            # Act
            response, status_code = self.handler.get_one_ngo(999)

            # Assert
            self.assertEqual(status_code, 404)
            self.assertEqual(response['message'], "NGO not found")

    def test_login_missing_required_fields(self):
        with self.app.test_request_context(json={
            "email": "test@example.com"
            # Missing password field
        }):
            # Act
            response, status_code = self.handler.login()

            # Assert
            self.assertEqual(status_code, 422)
            self.assertEqual(response['message'], "Missing required fields")

    def test_login_invalid_json_format(self):
        with self.app.test_request_context(data="string", content_type="application/json"):
            # Act
            response, status_code = self.handler.login()

            # Assert
            self.assertEqual(status_code, 400)
            self.assertEqual(response['message'], "Invalid request body format")


if __name__ == '__main__':
    unittest.main()