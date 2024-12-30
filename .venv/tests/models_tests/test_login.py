import unittest

from app.models.login import UserLogin


class TestUserLogin(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample UserLogin instance
        user = UserLogin(email="test@example.com", password="securepassword")

        # Expected dictionary representation of the UserLogin instance
        expected_dict = {
            'email': "test@example.com",
            'password': "securepassword"
        }

        # Assert that the to_dict method returns the correct dictionary
        self.assertEqual(user.to_dict(), expected_dict)

    def test_from_dict(self):
        # Sample dictionary to convert to a UserLogin instance
        data_dict = {
            'email': "test@example.com",
            'password': "securepassword"
        }

        # Convert the dictionary to a UserLogin instance
        user = UserLogin.from_dict(data_dict)

        # Assert that the created UserLogin instance matches the dictionary values
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "securepassword")

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'password')
        data_dict = {
            'email': "test@example.com"
        }

        # Assert that from_dict raises a TypeError because 'password' is missing
        with self.assertRaises(TypeError):
            UserLogin.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
