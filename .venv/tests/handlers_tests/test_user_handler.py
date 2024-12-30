import unittest
from unittest.mock import MagicMock
from app.handlers.user_handler import UserHandler
from app.models.login import UserLogin
from app.models.user_dto import User_DTO
from app.utils.errors.custom_errors import DatabaseError, InvalidCredentialsError, NotExistsError
from config.config import DB_ERROR, INVALID_CREDENTIALS, ID_NOT_EXIST
from flask import g, Flask
from models.new_ngo import NewNGO
from starlette.testclient import TestClient
from utils.utilities.context import get_user_from_context
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
import pytest
from app.handlers.main import create_app
import json
from app.models.ngo import NGO


@pytest.fixture
def mock_app():
    app = FastAPI()
    return app

@pytest.fixture
def mock_request():
    return MagicMock()

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def user_handler(mock_service):
    return UserHandler(mock_service)

@pytest.fixture
def sample_user():
    return User_DTO(
        '1','Test User','Sector no 1','test@gmail.com','9999999999','user'
    )

@pytest.fixture
def sample_login_request():
    return UserLogin(
        email='test@gmail.com',
        password='Strong@1234'
    )

@pytest.fixture
def sample_ngo_list():
    ngos: list[NGO] = [
        NGO('NGO 1','ngo@gmail.com','details','9999999999','address','1'),
        NGO('NGO 2','ngo2@gmail.com','details','9999999999','address','2')
    ]
    return ngos

@pytest.fixture
def sample_ngo():
    return NGO('NGO 1','ngo@gmail.com','details','9999999999','address','1')

class TestUserHandler():

    def setup_method(self):
        """Setup method that runs before each test"""
        # Patch the get_user_from_context function
        self.original_get_user = get_user_from_context
        get_user_from_context.__code__ = (lambda r: r.state.user).__code__

    def teardown_method(self):
        """Teardown method that runs after each test"""
        # Restore the original function
        get_user_from_context.__code__ = self.original_get_user.__code__

    def test_get_profile_success(self, user_handler, sample_user, mock_service, mock_request):
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.get_profile.return_value = sample_user

        # Act
        response = user_handler.get_profile(mock_request)

        # Assert
        assert response.status_code == 200
        response_dict = response.__dict__

        # Parse the JSON body
        import json
        body_dict = json.loads(response_dict['body'])

        # Assert on the parsed data
        assert body_dict['data']['id'] == "1"
        assert body_dict['data']['name'] == "Test User"
        mock_service.get_profile.assert_called_once_with('1')

    def test_get_profile_database_error(self, user_handler, mock_service, mock_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.get_profile.side_effect = DatabaseError("Database connection failed")

        # Act
        response = user_handler.get_profile(mock_request)

        # Assert
        assert response.status_code == 500

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == DB_ERROR  # This should be your defined DB_ERROR code
        assert body_dict['message'] == "Internal server error"

        # Verify service call
        mock_service.get_profile.assert_called_once_with('1')


    def test_login_success(self,user_handler,mock_service,mock_request,sample_login_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        token = 'token'
        mock_service.login.return_value = token

        # Act
        response = user_handler.login(sample_login_request)

        # Assert
        assert response.status_code == 200

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['data'] == token
        assert body_dict['status_code'] == 200
        assert body_dict['message'] == "Successful login"


    def test_login_database_error(self,user_handler,mock_service,mock_request,sample_login_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.login.side_effect = DatabaseError("Internal server error")

        # Act
        response = user_handler.login(sample_login_request)

        # Assert
        assert response.status_code == 500

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == DB_ERROR
        assert body_dict['message'] == "Internal server error"

    def test_login_invalid_credentials_error(self,user_handler,mock_service,mock_request,sample_login_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.login.side_effect = InvalidCredentialsError("Invalid credentials")

        # Act
        response = user_handler.login(sample_login_request)

        # Assert
        assert response.status_code == 401

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == INVALID_CREDENTIALS
        assert body_dict['message'] == "Invalid credentials"

    def test_get_ngos_success(self, user_handler, mock_service, mock_request, sample_ngo_list):
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.get_all_ngos.return_value = sample_ngo_list

        # Act
        response = user_handler.get_list_of_ngos()

        # Assert
        assert response.status_code == 200
        response_dict = response.__dict__

        # Parse the JSON body
        import json
        body_dict = json.loads(response_dict['body'])

        # Assert on the parsed data
        assert body_dict['data']== [ngo.to_dict() for ngo in sample_ngo_list]
        assert body_dict['message'] == "Successfully retreived list of NGOs"
        mock_service.get_all_ngos.assert_called_once()

    def test_get_ngos_database_error(self,user_handler,mock_service,mock_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        mock_service.get_all_ngos.side_effect = DatabaseError("Internal server error")

        # Act
        response = user_handler.get_list_of_ngos()

        # Assert
        assert response.status_code == 500

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == DB_ERROR
        assert body_dict['message'] == "Internal server error"

    def test_get_ngo_success(self, user_handler, mock_service, mock_request, sample_ngo):
        mock_request.state.user.__getitem__.return_value = '1'
        ngo_id = '1'
        mock_service.get_ngo_by_id.return_value = sample_ngo

        # Act
        response = user_handler.get_one_ngo(ngo_id)

        # Assert
        assert response.status_code == 200
        response_dict = response.__dict__

        # Parse the JSON body
        import json
        body_dict = json.loads(response_dict['body'])

        # Assert on the parsed data
        assert body_dict['data']== sample_ngo.to_dict()
        assert body_dict['message'] == "Successfully retreived ngo by id"
        mock_service.get_ngo_by_id.assert_called_once_with(ngo_id)

    def test_get_ngo_database_error(self,user_handler,mock_service,mock_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        ngo_id = '1'
        mock_service.get_ngo_by_id.side_effect = DatabaseError("Internal server error")

        # Act
        response = user_handler.get_one_ngo(ngo_id)

        # Assert
        assert response.status_code == 500

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == DB_ERROR
        assert body_dict['message'] == "Internal server error"

    def test_get_ngo_not_exist_error(self,user_handler,mock_service,mock_request):
        # Arrange
        mock_request.state.user.__getitem__.return_value = '1'
        ngo_id = '1'
        mock_service.get_ngo_by_id.side_effect = NotExistsError("Id does not exist")

        # Act
        response = user_handler.get_one_ngo(ngo_id)

        # Assert
        assert response.status_code == 404

        response_dict = response.__dict__
        body_dict = json.loads(response_dict['body'])

        assert body_dict['status_code'] == ID_NOT_EXIST
        assert body_dict['message'] == "Id does not exist"


if __name__ == '__main__':
    unittest.main()