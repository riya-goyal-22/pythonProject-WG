import unittest
from unittest.mock import MagicMock
from app.models.login import UserLogin
from app.utils.errors.custom_errors import CustomHTTPException
from app.config.config import VALIDATION_FAILURE
from app.utils.validators.validators import Validator


# Create a test case class
class TestUserLogin(unittest.TestCase):

    def setUp(self):
        self.original_is_valid_email = Validator.is_valid_email
        self.original_is_valid_password = Validator.is_valid_password

        # Create MagicMock instances for each validation method
        self.mock_is_valid_password = MagicMock()
        self.mock_is_valid_email = MagicMock()


        # Assign the MagicMock instances to the Validator methods
        Validator.is_valid_password = self.mock_is_valid_password
        Validator.is_valid_email = self.mock_is_valid_email

    def tearDown(self):
        # Restore the original methods after each test to avoid side effects
        Validator.is_valid_email = self.original_is_valid_email
        Validator.is_valid_password = self.original_is_valid_password

    def test_valid_email_and_password(self):
        # Setup mock methods to return True for valid email and password
        self.mock_is_valid_email.return_value = True
        self.mock_is_valid_password.return_value = True

        # Create valid data dictionary
        data = {"email": "valid@example.com", "password": "ValidPassword123"}

        # Create UserLogin instance using from_dict method
        user_login = UserLogin.from_dict(data)

        # Check if the UserLogin object was correctly created
        self.assertEqual(user_login.email, "valid@example.com")
        self.assertEqual(user_login.password, "ValidPassword123")

        # Ensure the validation methods were called
        self.mock_is_valid_email.assert_called_once_with("valid@example.com")
        self.mock_is_valid_password.assert_called_once_with("ValidPassword123")

    def test_invalid_email(self):
        # Setup mock methods to return False for invalid email
        self.mock_is_valid_email.return_value = False
        self.mock_is_valid_password.return_value = True

        # Create invalid data dictionary
        data = {"email": "invalid-email", "password": "ValidPassword123"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserLogin.from_dict(data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a valid email")

    def test_invalid_password(self):
        # Setup mock methods to return True for valid email and False for invalid password
        self.mock_is_valid_email.return_value = True
        self.mock_is_valid_password.return_value = False

        # Create invalid data dictionary
        data = {"email": "valid@example.com", "password": "weakpass"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserLogin.from_dict(data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a strong password")

    def test_valid_data_no_exceptions(self):
        # Setup mock methods to return True for both valid email and password
        self.mock_is_valid_email.return_value = True
        self.mock_is_valid_password.return_value = True

        # Create valid data dictionary
        data = {"email": "valid@example.com", "password": "ValidPassword123"}

        # No exception should be raised here
        user_login = UserLogin.from_dict(data)
        self.assertIsInstance(user_login, UserLogin)


if __name__ == '__main__':
    unittest.main()
