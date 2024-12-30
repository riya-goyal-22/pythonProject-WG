import pytest
from unittest.mock import MagicMock
from app.handlers.donor_handler import DonorHandler
from app.models.signup import UserSignup
from app.models.user import User
from app.utils.errors.custom_errors import UserExistsError, DatabaseError
from app.config.config import DB_ERROR, VALIDATION_FAILURE, UNEXPECTED_ERROR


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def donor_handler(mock_service):
    return DonorHandler(mock_service)


@pytest.fixture
def sample_signup_data():
    return UserSignup(
        name="Test Donor",
        email="donor@test.com",
        password="Test@123",
        phone_no="9999999999",
        address="Test Address",
        role="donor"
    )


class TestDonorHandler:
    def test_create_donor_success(self, donor_handler, mock_service, sample_signup_data):
        mock_service.signup.return_value = None
        # Act
        response = donor_handler.create_donor(sample_signup_data)

        # Assert
        assert response.status_code == 200
        response_dict = response.__dict__
        import json
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == 201
        assert body_dict['message'] == "Successfully signed up"

        # Verify service call
        user_dict = sample_signup_data.dict()
        called_user = mock_service.signup.call_args[0][0]
        assert called_user.name == sample_signup_data.name
        assert called_user.email == sample_signup_data.email
        assert called_user.address == sample_signup_data.address
        assert called_user.phone_no == sample_signup_data.phone_no
        assert called_user.password == sample_signup_data.password

    def test_create_donor_user_exists(self, donor_handler, mock_service, sample_signup_data):
        # Arrange
        mock_service.signup.side_effect = UserExistsError(sample_signup_data.email)

        # Act
        response = donor_handler.create_donor(sample_signup_data)

        # Assert
        assert response.status_code == 422
        response_dict = response.__dict__
        import json
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == VALIDATION_FAILURE
        assert body_dict['message'] == f"User with email {sample_signup_data.email} already exists"

        # Verify service call
        user_dict = sample_signup_data.dict()
        called_user = mock_service.signup.call_args[0][0]
        assert called_user.name == sample_signup_data.name
        assert called_user.email == sample_signup_data.email
        assert called_user.address == sample_signup_data.address
        assert called_user.phone_no == sample_signup_data.phone_no
        assert called_user.password == sample_signup_data.password

    def test_create_donor_database_error(self, donor_handler, mock_service, sample_signup_data):
        # Arrange
        mock_service.signup.side_effect = DatabaseError("Database connection failed")

        # Act
        response = donor_handler.create_donor(sample_signup_data)

        # Assert
        assert response.status_code == 500
        response_dict = response.__dict__
        import json
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == DB_ERROR
        assert body_dict['message'] == "Internal server error"

        # Verify service call
        user_dict = sample_signup_data.dict()
        called_user = mock_service.signup.call_args[0][0]
        assert called_user.name == sample_signup_data.name
        assert called_user.email == sample_signup_data.email
        assert called_user.address == sample_signup_data.address
        assert called_user.phone_no == sample_signup_data.phone_no
        assert called_user.password == sample_signup_data.password
