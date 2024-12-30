import unittest
from unittest.mock import MagicMock
from app.models.signup import UserSignup
from app.utils.errors.custom_errors import CustomHTTPException
from app.config.config import VALIDATION_FAILURE
from app.utils.validators.validators import Validator


class TestUserSignup(unittest.TestCase):

    def setUp(self):
        self.original_is_valid_name = Validator.is_valid_name
        self.original_validate_phone_no = Validator.validate_phone_no
        self.original_is_valid_email = Validator.is_valid_email
        self.original_is_valid_password = Validator.is_valid_password

        # Create a MagicMock instance for Validator
        self.mock_is_valid_name = MagicMock()
        self.mock_validate_phone_no = MagicMock()
        self.mock_is_valid_email = MagicMock()
        self.mock_is_valid_password = MagicMock()


        # Valid data setup
        self.valid_data = {
            "name": "John Doe",
            "address": "Ward no 12",
            "phone_no": "9999999999",
            "email": "john@gmail.com",
            "password": "Strongpass@123"
        }

        # Assign the mock to the Validator methods
        Validator.is_valid_name = self.mock_is_valid_name
        Validator.validate_phone_no = self.mock_validate_phone_no
        Validator.is_valid_email = self.mock_is_valid_email
        Validator.is_valid_password = self.mock_is_valid_password

    def test_valid_data(self):
        # Setup mock methods to return True for valid data
        self.mock_is_valid_name.return_value = True
        self.mock_validate_phone_no.return_value = True
        self.mock_is_valid_email.return_value = True
        self.mock_is_valid_password.return_value = True

        # Create the UserSignup instance using valid data
        user_signup = UserSignup.from_dict(self.valid_data)

        # Assert the instance is created correctly
        self.assertEqual(user_signup.name, "John Doe")
        self.assertEqual(user_signup.phone_no, "9999999999")
        self.assertEqual(user_signup.email, "john@gmail.com")
        self.assertEqual(user_signup.password, "Strongpass@123")

    def test_invalid_name(self):
        # Setup mock method to return False for invalid name
        self.mock_is_valid_name.return_value = False

        # Create invalid data with an invalid name
        invalid_data = {**self.valid_data, "name": "Invalid Name"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserSignup.from_dict(invalid_data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a valid name")

    def test_invalid_phone_no(self):
        # Setup mock method to return False for invalid phone number
        self.mock_validate_phone_no.return_value = False

        # Create invalid data with an invalid phone number
        invalid_data = {**self.valid_data, "phone_no": "invalid_phone"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserSignup.from_dict(invalid_data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a valid phone number")

    def test_invalid_email(self):
        # Setup mock method to return False for invalid email
        self.mock_is_valid_email.return_value = False

        # Create invalid data with an invalid email
        invalid_data = {**self.valid_data, "email": "invalid_email"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserSignup.from_dict(invalid_data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a valid email")

    def test_invalid_password(self):
        # Setup mock method to return False for invalid password
        self.mock_is_valid_password.return_value = False

        # Create invalid data with an invalid password
        invalid_data = {**self.valid_data, "password": "weakpass"}

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            UserSignup.from_dict(invalid_data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(context.exception.message, "Not a strong password")

    def tearDown(self):
        # Restore the original methods after each test to avoid side effects
        Validator.is_valid_name = self.original_is_valid_name
        Validator.validate_phone_no = self.original_validate_phone_no
        Validator.is_valid_email = self.original_is_valid_email
        Validator.is_valid_password = self.original_is_valid_password


if __name__ == "__main__":
    unittest.main()
