import unittest
from unittest.mock import MagicMock
from app.models.user import User
from app.services.donor_service import DonorService
from app.utils.errors.custom_errors import UserExistsError
import app.utils.utilities.encrypter as encrypter


class TestDonorService(unittest.TestCase):

    def setUp(self):
        # Create mock repositories
        self.mock_user_repo = MagicMock()
        self.mock_ngo_repo = MagicMock()

        # Create an instance of DonorService with the mocked repositories
        self.donor_service = DonorService(user_repo=self.mock_user_repo, ngo_repo=self.mock_ngo_repo)

    def test_signup_when_user_exists(self):
        # Arrange: Create a user object and mock the user repository to return an existing user
        existing_user = User(
            name="John Doe",
            email="johndoe@example.com",
            password="password123",  # This will be hashed later
            phone_no="9876543210",
            address="123 Elm Street"
        )
        self.mock_user_repo.get_user_by_email.return_value = existing_user  # Simulating user already exists

        # Create a new user with the same email
        new_user = User(
            name="Jane Doe",
            email="johndoe@example.com",  # Same email as the existing user
            password="newpassword123",  # New password to be hashed
            phone_no="1234567890",
            address="456 Oak Avenue"
        )

        # Assert: Check that UserExistsError is raised when trying to sign up with an existing email
        with self.assertRaises(UserExistsError) as context:
            self.donor_service.signup(new_user)

        # Assert: Verify that the error message contains the email of the user
        self.assertEqual(str(context.exception), "User with email johndoe@example.com already exists")
        self.mock_user_repo.get_user_by_email.assert_called_once_with(new_user.email)

    def test_signup_when_user_does_not_exist(self):
        # Arrange: Mock the repository to return None, meaning the user does not exist
        self.mock_user_repo.get_user_by_email.return_value = None

        # Create a new user to sign up
        new_user = User(
            name="Jane Doe",
            email="janedoe@example.com",
            password="newpassword123",  # This password will be hashed
            phone_no="1234567890",
            address="456 Oak Avenue"
        )
        unhashed_password = new_user.password

        # Mock the create_user method to check if it's called during signup
        self.mock_user_repo.create_user.return_value = new_user

        # Act: Call the signup method to create a new user
        result = self.donor_service.signup(new_user)

        # Assert: Check if the returned result is the same as the user we tried to sign up
        self.assertEqual(result, new_user)

        # Assert: Verify that the create_user method was called once with the new user
        self.mock_user_repo.create_user.assert_called_once_with(new_user)

        # Assert: Verify that the password has been hashed
        self.assertNotEqual(result.password, unhashed_password)
        self.assertTrue(encrypter.check_password(result.password, "newpassword123"))

    def test_signup_password_hashing(self):
        # Arrange: Mock the repository to return None, meaning the user does not exist
        self.mock_user_repo.get_user_by_email.return_value = None

        # Create a new user to sign up
        new_user = User(
            name="Jane Doe",
            email="janedoe@example.com",
            password="plainpassword",  # Plain password to be hashed
            phone_no="1234567890",
            address="456 Oak Avenue"
        )

        # Mock the create_user method to simulate user creation
        self.mock_user_repo.create_user.return_value = new_user

        # Act: Call the signup method to create a new user
        result = self.donor_service.signup(new_user)

        # Assert: Check if the returned result is the same as the user we tried to sign up
        self.assertEqual(result, new_user)

        # Assert: Verify that the password is hashed and does not match the plain password
        self.assertNotEqual(result.password, "plainpassword")
        self.assertTrue(encrypter.check_password(result.password, "plainpassword"))


if __name__ == '__main__':
    unittest.main()
