import pytest
from unittest.mock import Mock, patch
from app.handlers.admin_handler import AdminHandler
from app.models.new_ngo import NewNGO
from app.models.ngo import NGO
from app.utils.errors.custom_errors import DatabaseError, NotExistsError, NGOExistsError
from app.models.response import CustomResponse
from fastapi import Request

@pytest.fixture
def admin_service():
    return Mock()

@pytest.fixture
def admin_handler(admin_service):
    return AdminHandler(admin_service)

@pytest.fixture
def mock_request():
    """Mock FastAPI request fixture with admin role"""
    # Create base mock request with receive channel
    mock_scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
        "query_string": b"",
        "client": ("127.0.0.1", 8000),
    }

    async def mock_receive():
        return {"type": "http.request", "body": b""}

    mock_request = Request(mock_scope, receive=mock_receive)

    # Set up admin user directly on state
    mock_request.state.user = {"role": "admin", "user_id": "test-user"}

    return mock_request

@pytest.fixture
def sample_ngo_data():
    return NewNGO(
        name="Test NGO",
        details="Test Description",
        email="test@ngo.com",
        phone_no="1234567890",
        address="Test Address"
    )

class TestAdminHandler:
    def test_create_ngo_success(self, admin_handler, mock_request, sample_ngo_data):
        # Arrange
        expected_response = CustomResponse(
            status_code=201,
            message="Successfully created",
            http_status_code=201
        ).to_dict()

        # Act
        result = admin_handler.create_ngo(mock_request, sample_ngo_data)

        # Assert
        result_dict = result.__dict__

        import json
        body_dict = json.loads(result_dict['body'])

        assert body_dict == expected_response
        admin_handler.user_service.add_ngo.assert_called_once()

    def test_create_ngo_exists_error(self, admin_handler, mock_request, sample_ngo_data):
        # Arrange
        error_message = "NGO already exists"
        admin_handler.user_service.add_ngo.side_effect = NGOExistsError(error_message)

        # Act
        result = admin_handler.create_ngo(mock_request, sample_ngo_data)

        # Assert
        assert result.status_code == 422
        assert "NGO already exists" in result.body.decode()

    def test_create_ngo_database_error(self, admin_handler, mock_request, sample_ngo_data):
        # Arrange
        admin_handler.user_service.add_ngo.side_effect = DatabaseError("Internal server error")

        # Act
        result = admin_handler.create_ngo(mock_request, sample_ngo_data)

        # Assert
        result_dict = result.__dict__

        import json
        body_dict = json.loads(result_dict['body'])

        assert result.status_code == 500
        assert "Internal server error" in body_dict['message']

    def test_update_ngo_success(self, admin_handler, mock_request, sample_ngo_data):
        # Arrange
        ngo_id = "123"
        expected_response = CustomResponse(
            status_code=200,
            message="Successfully updated"
        ).to_dict()

        # Act
        result = admin_handler.update_ngo(mock_request, ngo_id, sample_ngo_data)

        # Assert
        result_dict = result.__dict__

        import json
        body_dict = json.loads(result_dict['body'])

        assert body_dict == expected_response
        admin_handler.user_service.update_ngo.assert_called_once()

    def test_update_ngo_not_exists(self, admin_handler, mock_request, sample_ngo_data):
        # Arrange
        ngo_id = "123"
        error_message = "NGO not found"
        admin_handler.user_service.update_ngo.side_effect = NotExistsError(error_message)

        # Act
        result = admin_handler.update_ngo(mock_request, ngo_id, sample_ngo_data)

        # Assert
        assert result.status_code == 404
        assert error_message in result.body.decode()

    def test_delete_ngo_success(self, admin_handler, mock_request):
        # Arrange
        ngo_id = "123"
        expected_response = CustomResponse(
            status_code=200,
            message="Successfully deleted"
        ).to_dict()

        # Act
        result = admin_handler.delete_ngo(mock_request, ngo_id)

        # Assert
        result_dict = result.__dict__

        import json
        body_dict = json.loads(result_dict['body'])

        assert body_dict == expected_response
        admin_handler.user_service.delete_ngo.assert_called_once_with(ngo_id)

    def test_delete_ngo_not_exists(self, admin_handler, mock_request):
        # Arrange
        ngo_id = "123"
        error_message = "NGO not found"
        admin_handler.user_service.delete_ngo.side_effect = NotExistsError(error_message)

        # Act
        result = admin_handler.delete_ngo(mock_request, ngo_id)

        # Assert
        assert result.status_code == 404
        assert error_message in result.body.decode()

    def test_delete_ngo_database_error(self, admin_handler, mock_request):
        # Arrange
        ngo_id = "123"
        error_message = "Database error"
        admin_handler.user_service.delete_ngo.side_effect = DatabaseError(error_message)

        # Act
        result = admin_handler.delete_ngo(mock_request, ngo_id)

        # Assert
        assert result.status_code == 500
        assert error_message in result.body.decode()