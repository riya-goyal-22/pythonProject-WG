import unittest
from unittest.mock import MagicMock
from app.models.new_ngo import NewNGO
from app.utils.errors.custom_errors import CustomHTTPException
from app.config.config import VALIDATION_FAILURE
from app.utils.validators.validators import Validator


class TestNewNGO(unittest.TestCase):

    def setUp(self):
        self.original_is_valid_name = Validator.is_valid_name
        self.original_is_valid_email = Validator.is_valid_email
        self.original_is_valid_phone_no = Validator.validate_phone_no

        # Create MagicMock instances for each validation method
        self.mock_is_valid_name = MagicMock()
        self.mock_is_valid_email = MagicMock()
        self.mock_validate_phone_no = MagicMock()

        # Assign the MagicMock instances to the Validator methods
        Validator.is_valid_name = self.mock_is_valid_name
        Validator.is_valid_email = self.mock_is_valid_email
        Validator.validate_phone_no = self.mock_validate_phone_no

    def tearDown(self):
        Validator.is_valid_name = self.original_is_valid_name
        Validator.validate_phone_no = self.original_is_valid_phone_no
        Validator.is_valid_email = self.original_is_valid_email

    def test_valid_data(self):
        # Mock methods to return True for valid data
        self.mock_is_valid_name.return_value = True
        self.mock_is_valid_email.return_value = True
        self.mock_validate_phone_no.return_value = True

        # Create valid data dictionary
        data = {
            "name": "John Doe",
            "address": "Sector 12",
            "phone_no": "9999999999",
            "email": "john@watchguard.com",
            "details": "Any detail"
        }

        # Create NewNGO instance using from_dict method
        ngo = NewNGO.from_dict(data)

        # Check if the NewNGO object was correctly created
        self.assertEqual(ngo.name, "John Doe")
        self.assertEqual(ngo.address, "Sector 12")
        self.assertEqual(ngo.phone_no, "9999999999")
        self.assertEqual(ngo.email, "john@watchguard.com")
        self.assertEqual(ngo.details, "Any detail")

        # Ensure the validation methods were called
        self.mock_is_valid_name.assert_called_once_with("John Doe")
        self.mock_is_valid_email.assert_called_once_with("john@watchguard.com")
        self.mock_validate_phone_no.assert_called_once_with("9999999999")

    def test_invalid_name(self):
        # Mock methods to return False for invalid name
        self.mock_is_valid_name.return_value = False
        self.mock_is_valid_email.return_value = True
        self.mock_validate_phone_no.return_value = True

        # Create invalid data dictionary
        data = {
            "name": "John! Doe",  # Invalid name
            "address": "Sector 12",
            "phone_no": "9999999999",
            "email": "john@watchguard.com",
            "details": "Any detail"
        }

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            NewNGO.from_dict(data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(str(context.exception.message), "Not a valid name")

    def test_invalid_email(self):
        # Mock methods to return True for valid name and phone, False for invalid email
        self.mock_is_valid_name.return_value = True
        self.mock_is_valid_email.return_value = False
        self.mock_validate_phone_no.return_value = True

        # Create invalid data dictionary
        data = {
            "name": "John Doe",
            "address": "Sector 12",
            "phone_no": "9999999999",
            "email": "john@watchguard",  # Invalid email
            "details": "Any detail"
        }

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            NewNGO.from_dict(data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(str(context.exception.message), "Not a valid email")

    def test_invalid_phone_no(self):
        # Mock methods to return True for valid name and email, False for invalid phone number
        self.mock_is_valid_name.return_value = True
        self.mock_is_valid_email.return_value = True
        self.mock_validate_phone_no.return_value = False

        # Create invalid data dictionary
        data = {
            "name": "John Doe",
            "address": "Sector 12",
            "phone_no": "999",  # Invalid phone number
            "email": "john@watchguard.com",
            "details": "Any detail"
        }

        # Expect a CustomHTTPException to be raised
        with self.assertRaises(CustomHTTPException) as context:
            NewNGO.from_dict(data)

        # Assert the exception details
        self.assertEqual(context.exception.status_code, 422)
        self.assertEqual(context.exception.error_code, VALIDATION_FAILURE)
        self.assertEqual(str(context.exception.message), "Not a valid phone number")

    def test_valid_data_no_exceptions(self):
        # Mock methods to return True for valid data
        self.mock_is_valid_name.return_value = True
        self.mock_is_valid_email.return_value = True
        self.mock_validate_phone_no.return_value = True

        # Create valid data dictionary
        data = {
            "name": "John Doe",
            "address": "Sector 12",
            "phone_no": "9999999999",
            "email": "john@watchguard.com",
            "details": "Any detail"
        }

        # No exception should be raised here
        ngo = NewNGO.from_dict(data)
        self.assertIsInstance(ngo, NewNGO)


if __name__ == '__main__':
    unittest.main()
