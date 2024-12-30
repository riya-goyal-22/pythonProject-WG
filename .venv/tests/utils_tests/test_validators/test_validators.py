import unittest
from app.utils.validators.validators import Validator


class TestValidator(unittest.TestCase):

    def test_validate_required_fields(self):
        # Test case where required fields are present
        data = {'name': 'John', 'email': 'john@example.com', 'phone': '1234567890'}
        required_fields = ['name', 'email', 'phone']
        self.assertTrue(Validator.validate_required_fields(data, required_fields))

        # Test case where a required field is missing
        data_missing_field = {'name': 'John', 'email': 'john@example.com'}
        required_fields_missing = ['name', 'email', 'phone']
        self.assertFalse(Validator.validate_required_fields(data_missing_field, required_fields_missing))

    def test_is_valid_email(self):
        # Valid email
        valid_email = 'test@gmail.com'
        self.assertTrue(Validator.is_valid_email(valid_email))

        # Invalid email (missing '@')
        invalid_email = 'testexample.com'
        self.assertFalse(Validator.is_valid_email(invalid_email))

        # Invalid email (missing domain)
        invalid_email_2 = 'test@.com'
        self.assertFalse(Validator.is_valid_email(invalid_email_2))

    def test_is_valid_password(self):
        # Valid password
        valid_password = 'Test@1234'
        self.assertTrue(Validator.is_valid_password(valid_password))

        # Invalid password (too short)
        invalid_password_short = 'TEST'
        self.assertFalse(Validator.is_valid_password(invalid_password_short))

        # Invalid password (no lowercase)
        invalid_password = 'TESTTEST@1'
        self.assertFalse(Validator.is_valid_password(invalid_password))

        # Invalid password (no special character)
        invalid_password = 'Test123456'
        self.assertFalse(Validator.is_valid_password(invalid_password))

        # Invalid password (no uppercase)
        invalid_password_no_upper = 'test@1234'
        self.assertFalse(Validator.is_valid_password(invalid_password_no_upper))

        # Invalid password (no digit)
        invalid_password_no_digit = 'Test@password'
        self.assertFalse(Validator.is_valid_password(invalid_password_no_digit))

        # Invalid password (common password)
        invalid_password_common = 'password'
        self.assertFalse(Validator.is_valid_password(invalid_password_common))

    def test_validate_phone_no(self):
        # Valid phone number
        valid_phone = '123-456-7890'
        self.assertTrue(Validator.validate_phone_no(valid_phone))

        # Invalid phone number (wrong length)
        invalid_phone_short = '123-45-6789'
        self.assertFalse(Validator.validate_phone_no(invalid_phone_short))

        # Invalid phone number (non-digit characters)
        invalid_phone_with_letters = '123-456-abc0'
        self.assertFalse(Validator.validate_phone_no(invalid_phone_with_letters))

    def test_is_valid_name(self):
        valid_name = 'test user'
        self.assertTrue(Validator.is_valid_name(valid_name))

        invalid_name = ''
        self.assertFalse(Validator.is_valid_name(invalid_name))

        invalid_name = 'w'
        self.assertFalse(Validator.is_valid_name(invalid_name))


if __name__ == '__main__':
    unittest.main()
