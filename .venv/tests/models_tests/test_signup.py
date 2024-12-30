import unittest

from app.models.signup import UserSignup


class TestUserSignup(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample UserSignup instance
        user = UserSignup(
            name="John Doe",
            address="123 Elm Street",
            phone_no="987-654-3210",
            email="johndoe@example.com",
            password="securepassword"
        )

        # Expected dictionary representation of the UserSignup instance
        expected_dict = {
            'name': "John Doe",
            'email': "johndoe@example.com",
            'password': "securepassword",
            'address': "123 Elm Street",
            'phone_no': "987-654-3210"
        }

        # Assert that the to_dict method returns the correct dictionary
        self.assertEqual(user.to_dict(), expected_dict)

    def test_from_dict(self):
        # Sample dictionary to convert to a UserSignup instance
        data_dict = {
            'name': "John Doe",
            'email': "johndoe@example.com",
            'password': "securepassword",
            'address': "123 Elm Street",
            'phone_no': "987-654-3210"
        }

        # Convert the dictionary to a UserSignup instance
        user = UserSignup.from_dict(data_dict)

        # Assert that the created UserSignup instance matches the dictionary values
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.password, "securepassword")
        self.assertEqual(user.address, "123 Elm Street")
        self.assertEqual(user.phone_no, "987-654-3210")

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'phone_no')
        data_dict = {
            'name': "John Doe",
            'email': "johndoe@example.com",
            'password': "securepassword",
            'address': "123 Elm Street"
        }

        # Assert that from_dict raises a TypeError because 'phone_no' is missing
        with self.assertRaises(TypeError):
            UserSignup.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
