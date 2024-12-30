import unittest
from unittest.mock import MagicMock
from app.models.ngo import NGO
from app.utils.errors.custom_errors import NGOExistsError
from app.services.admin_service import AdminService
from app.repositories.ngo_repository import NGORepository


class TestAdminService(unittest.TestCase):

    def setUp(self):
        # Create mock repositories
        self.mock_user_repo = MagicMock()
        self.mock_ngo_repo = MagicMock()

        # Create instance of AdminService with the mocked repositories
        self.admin_service = AdminService(user_repo=self.mock_user_repo, ngo_repo=self.mock_ngo_repo)

    def test_add_ngo_when_ngo_exists(self):
        # Arrange: Set up the mock to return an NGO when searching by email
        existing_ngo = NGO(
            name="Existing NGO",
            email="existing@ngo.com",
            address="123 NGO Lane",
            phone_no="9876543210",
            details="Already exists"
        )
        self.mock_ngo_repo.get_ngo_by_email.return_value = existing_ngo

        # Create a new NGO instance to be added
        new_ngo = NGO(
            name="New NGO",
            email="existing@ngo.com",  # Same email as the existing one
            address="456 New NGO Road",
            phone_no="1234567890",
            details="A new organization"
        )

        # Assert: Check that NGOExistsError is raised when adding the NGO with an existing email
        with self.assertRaises(NGOExistsError) as context:
            self.admin_service.add_ngo(new_ngo)

        # Assert: Verify that the error message is correct
        self.assertEqual(str(context.exception), "ngo already registered with this email id")
        self.mock_ngo_repo.get_ngo_by_email.assert_called_once_with(new_ngo.email)

    def test_add_ngo_when_ngo_does_not_exist(self):
        # Arrange: Set up the mock to return None when searching for the NGO by email (i.e., email not already taken)
        self.mock_ngo_repo.get_ngo_by_email.return_value = None

        # Create a new NGO instance to be added
        new_ngo = NGO(
            name="New NGO",
            email="new@ngo.com",
            address="456 New NGO Road",
            phone_no="1234567890",
            details="A new organization"
        )

        # Act: Call the method to add the NGO
        self.admin_service.add_ngo(new_ngo)

        # Assert: Verify that create_ngo was called once with the correct NGO
        self.mock_ngo_repo.create_ngo.assert_called_once_with(new_ngo)

    def test_update_ngo_when_ngo_exists(self):
        # Arrange: Set up the mock to return an NGO when searching by email
        existing_ngo = NGO(
            name="Existing NGO",
            email="existing@ngo.com",
            address="123 NGO Lane",
            phone_no="9876543210",
            details="Already exists"
        )
        self.mock_ngo_repo.get_ngo_by_email.return_value = existing_ngo

        # Create a new NGO instance to be updated
        update_ngo = NGO(
            name="Updated NGO",
            email="existing@ngo.com",  # Same email as the existing one
            address="456 Updated NGO Road",
            phone_no="1234567890",
            details="Updated details"
        )

        # Assert: Check that NGOExistsError is raised when updating the NGO with an existing email
        with self.assertRaises(NGOExistsError) as context:
            self.admin_service.update_ngo(update_ngo)

        # Assert: Verify that the error message is correct
        self.assertEqual(str(context.exception), "ngo already registered with this email id")
        self.mock_ngo_repo.get_ngo_by_email.assert_called_once_with(update_ngo.email)

    def test_update_ngo_when_ngo_does_not_exist(self):
        # Arrange: Set up the mock to return None when searching for the NGO by email
        self.mock_ngo_repo.get_ngo_by_email.return_value = None

        # Create a new NGO instance to be updated
        update_ngo = NGO(
            name="Updated NGO",
            email="updated@ngo.com",
            address="456 Updated NGO Road",
            phone_no="1234567890",
            details="Updated details"
        )

        # Act: Call the method to update the NGO
        self.admin_service.update_ngo(update_ngo)

        # Assert: Verify that update_ngo_by_id was called once with the correct NGO
        self.mock_ngo_repo.update_ngo_by_id.assert_called_once_with(update_ngo)

    def test_delete_ngo(self):
        # Arrange: Set up the mock for deleting the NGO by id
        ngo_id = "ngo123"

        # Act: Call the method to delete the NGO
        self.admin_service.delete_ngo(ngo_id)

        # Assert: Verify that delete_ngo_by_id was called with the correct NGO id
        self.mock_ngo_repo.delete_ngo_by_id.assert_called_once_with(ngo_id)


if __name__ == '__main__':
    unittest.main()
