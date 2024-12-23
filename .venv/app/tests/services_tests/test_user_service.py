import unittest
from unittest.mock import MagicMock
from app.models.user import User
from app.models.ngo import NGO
from app.services.user_service import UserService
from app.utils.errors.custom_errors import InvalidCredentialsError
import app.utils.utilities.encrypter as encrypter
import app.utils.utilities.token as token


class TestUserService(unittest.TestCase):

    def setUp(self):
        # Create mock repositories
        self.mock_user_repo = MagicMock()
        self.mock_ngo_repo = MagicMock()

        # Create an instance of UserService with the mocked repositories
        self.user_service = UserService(user_repo=self.mock_user_repo, ngo_repo=self.mock_ngo_repo)

    def test_login_invalid_email(self):
        # Arrange: Mock the user_repo to return None (email not found)
        self.mock_user_repo.get_user_by_email.return_value = None

        # Act & Assert: Check if InvalidCredentialsError is raised for invalid email
        with self.assertRaises(InvalidCredentialsError) as context:
            self.user_service.login("invalidemail@example.com", "password123")

        self.assertEqual(str(context.exception), "Invalid Email Id")
        self.mock_user_repo.get_user_by_email.assert_called_once_with("invalidemail@example.com")

    def test_login_invalid_password(self):
        # Arrange: Mock a user object and user_repo to return the user with a mismatched password
        user = User(
            id="12345",
            name="John Doe",
            email="johndoe@example.com",
            password="hashedpassword",  # This is the hashed password in the database
            phone_no="9876543210",
            address="123 Elm Street",
            role="donor"
        )
        self.mock_user_repo.get_user_by_email.return_value = user

        # Mock the password check to return False (incorrect password)
        mock_check_password = MagicMock(return_value=False)
        encrypter.check_password = mock_check_password

        with self.assertRaises(InvalidCredentialsError) as context:
            self.user_service.login("johndoe@example.com", "wrongpassword123")

        self.assertEqual(str(context.exception), "Invalid password")
        self.mock_user_repo.get_user_by_email.assert_called_once_with("johndoe@example.com")
        mock_check_password.assert_called_once_with("hashedpassword", "wrongpassword123")

    def test_login_successful(self):
        # Arrange: Mock a user object and user_repo to return the user with the correct password
        user = User(
            id="12345",
            name="John Doe",
            email="johndoe@example.com",
            password="hashedpassword",  # Correct hashed password
            phone_no="9876543210",
            address="123 Elm Street",
            role="donor"
        )
        self.mock_user_repo.get_user_by_email.return_value = user

        # Mock the password check to return True (correct password)
        mock_check_password = MagicMock(return_value=True)
        encrypter.check_password = mock_check_password

        # Mock the token generation
        mock_generate_token = MagicMock(return_value="mocked_token")
        token.generate_token = mock_generate_token

        # Act: Call login with correct credentials
        token_result = self.user_service.login("johndoe@example.com", "password123")

        # Assert: Verify the token is generated and returned
        self.assertEqual(token_result, "mocked_token")
        mock_generate_token.assert_called_once_with(user.id, user.email, user.role)
        self.mock_user_repo.get_user_by_email.assert_called_once_with("johndoe@example.com")
        mock_check_password.assert_called_once_with("hashedpassword", "password123")

    def test_get_all_ngos(self):
        # Arrange: Create a list of mock NGO objects
        ngo_list = [
            NGO(id="1", name="NGO 1", email="ngo1@example.com", phone_no="9876543210", address="Address 1",
                details="Details 1"),
            NGO(id="2", name="NGO 2", email="ngo2@example.com", phone_no="1234567890", address="Address 2",
                details="Details 2")
        ]
        self.mock_ngo_repo.get_all_ngos.return_value = ngo_list

        # Act: Call the method to get all NGOs
        ngos = self.user_service.get_all_ngos()

        # Assert: Verify that the correct NGOs are returned
        self.assertEqual(ngos, ngo_list)
        self.mock_ngo_repo.get_all_ngos.assert_called_once()

    def test_get_ngo_by_id(self):
        # Arrange: Create a mock NGO object
        ngo = NGO(id="1", name="NGO 1", email="ngo1@example.com", phone_no="9876543210", address="Address 1",
                  details="Details 1")
        self.mock_ngo_repo.get_ngo_by_id.return_value = ngo

        # Act: Call the method to get NGO by ID
        result = self.user_service.get_ngo_by_id("1")

        # Assert: Verify that the correct NGO is returned
        self.assertEqual(result, ngo)
        self.mock_ngo_repo.get_ngo_by_id.assert_called_once_with("1")

    def test_get_profile(self):
        # Arrange: Create a mock user object
        user = User(
            id="12345",
            name="John Doe",
            email="johndoe@example.com",
            password="hashedpassword",
            phone_no="9876543210",
            address="123 Elm Street",
            role="donor"
        )
        self.mock_user_repo.get_user_by_id.return_value = user

        # Act: Call the method to get user profile by ID
        result = self.user_service.get_profile("12345")

        # Assert: Verify that the correct user is returned
        self.assertEqual(result, user)
        self.mock_user_repo.get_user_by_id.assert_called_once_with("12345")


if __name__ == '__main__':
    unittest.main()
