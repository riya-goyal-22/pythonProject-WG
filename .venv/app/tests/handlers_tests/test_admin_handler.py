from logging import raiseExceptions

import pytest
from unittest.mock import Mock, patch
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from flask import Flask, g
from app.handlers.admin_handler import AdminHandler
from app.models.new_ngo import NewNGO
from app.models.ngo import NGO
from app.utils.errors.custom_errors import DatabaseError, NotExistsError, NGOExistsError
from app.config.config import MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, VALIDATION_FAILURE, DB_ERROR, \
    INVALID_REQUEST_BODY_FORMAT, ID_NOT_EXIST
from app.utils.enums.role import Role


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def admin_service():
    return Mock()


@pytest.fixture
def admin_handler(admin_service):
    return AdminHandler(admin_service)


@pytest.fixture
def valid_ngo_data():
    return {
        "name": "Test NGO",
        "email": "test@ngo.com",
        "phone_no": "1234567890",
        "address": "123 Test St",
        "details": "Test Description"
    }


class TestAdminHandler:

    # Tests for create_ngo method
    def test_create_ngo_success(self, app, admin_handler, valid_ngo_data):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 201
                    assert response["status_code"] == 201
                    assert response["message"] == "Success"
                    admin_handler.user_service.add_ngo.assert_called_once()

    def test_create_ngo_missing_request_body(self, app, admin_handler):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=None):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 400
                    assert response["status_code"] == MISSING_REQUEST_BODY
                    assert response["message"] == "Missing Request body"
                    admin_handler.user_service.add_ngo.assert_not_called()

    def test_create_ngo_missing_fields(self, app, admin_handler):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value={"name": "Test NGO"}):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 422
                    assert response["status_code"] == MISSING_REQUIRED_FIELDS
                    assert response["message"] == "Missing required fields"

    def test_create_ngo_invalid_email(self, app, admin_handler, valid_ngo_data):
        invalid_data = valid_ngo_data.copy()
        invalid_data["email"] = "invalid-email"

        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=invalid_data):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 422
                    assert response["status_code"] == VALIDATION_FAILURE
                    assert response["message"] == "Invalid email id"

    def test_create_ngo_invalid_phone(self, app, admin_handler, valid_ngo_data):
        invalid_data = valid_ngo_data.copy()
        invalid_data["phone_no"] = "123"

        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=invalid_data):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 422
                    assert response["status_code"] == VALIDATION_FAILURE
                    assert response["message"] == "Invalid phone number"

    def test_create_ngo_database_error(self, app, admin_handler, valid_ngo_data):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    admin_handler.user_service.add_ngo.side_effect = DatabaseError("Internal server error")
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 500
                    assert response["status_code"] == DB_ERROR
                    assert response["message"] == "Internal server error"

    def test_create_ngo_already_exist(self, app, admin_handler, valid_ngo_data):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    admin_handler.user_service.add_ngo.side_effect = NGOExistsError("ngo already registered with this email id")
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 422
                    assert response["status_code"] == VALIDATION_FAILURE
                    assert response["message"] == "ngo already registered with this email id"

    def test_create_ngo_bad_request(self, app, admin_handler, valid_ngo_data):
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', side_effect= BadRequest):
                    response, status_code = admin_handler.create_ngo()

                    assert status_code == 400
                    assert response["status_code"] == INVALID_REQUEST_BODY_FORMAT
                    assert response["message"] == "Invalid request body format"

    def test_create_ngo_unsupported_media(self, app, admin_handler, valid_ngo_data):
        # Simulate a non-JSON request body with 'application/text' content type
        with app.test_request_context(content_type='application/text'):
            with app.app_context():
                g.role = Role.ADMIN.value
                response, status_code = admin_handler.create_ngo()

                # Assert that the response returns a 415 status code
                assert status_code == 415
                assert response["status_code"] == INVALID_REQUEST_BODY_FORMAT
                assert response["message"] == "Unsupported media type, Expected application/json"

    # Tests for update_ngo method
    def test_update_ngo_success(self, app, admin_handler, valid_ngo_data):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 200
                    assert response["status_code"] == 200
                    assert response["message"] == "Success"
                    admin_handler.user_service.update_ngo.assert_called_once()

    def test_update_ngo_missing_request_body(self, app, admin_handler):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=None):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 400
                    assert response["status_code"] == MISSING_REQUEST_BODY
                    assert response["message"] == "Missing Request body"
                    admin_handler.user_service.add_ngo.assert_not_called()

    def test_update_ngo_missing_fields(self, app, admin_handler):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value={"name": "Test NGO"}):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 422
                    assert response["status_code"] == MISSING_REQUIRED_FIELDS
                    assert response["message"] == "Missing required fields"

    def test_update_ngo_invalid_email(self, app, admin_handler, valid_ngo_data):
        invalid_data = valid_ngo_data.copy()
        invalid_data["email"] = "invalid-email"

        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=invalid_data):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 422
                    assert response["status_code"] == VALIDATION_FAILURE
                    assert response["message"] == "Invalid email id"

    def test_update_ngo_invalid_phone(self, app, admin_handler, valid_ngo_data):
        invalid_data = valid_ngo_data.copy()
        invalid_data["phone_no"] = "123"

        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=invalid_data):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 422
                    assert response["status_code"] == VALIDATION_FAILURE
                    assert response["message"] == "Invalid phone number"

    def test_update_ngo_database_error(self, app, admin_handler, valid_ngo_data):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    admin_handler.user_service.update_ngo.side_effect = DatabaseError("Internal server error")
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 500
                    assert response["status_code"] == DB_ERROR
                    assert response["message"] == "Internal server error"

    def test_update_ngo_unsupported_media(self, app, admin_handler, valid_ngo_data):
        # Simulate a non-JSON request body with 'application/text' content type
        ngo_id = "123"
        with app.test_request_context(content_type='application/text'):
            with app.app_context():
                g.role = Role.ADMIN.value
                response, status_code = admin_handler.update_ngo(ngo_id)

                # Assert that the response returns a 415 status code
                assert status_code == 415
                assert response["status_code"] == INVALID_REQUEST_BODY_FORMAT
                assert response["message"] == "Unsupported media type, Expected application/json"

    def test_update_ngo_not_exists(self, app, admin_handler, valid_ngo_data):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', return_value=valid_ngo_data):
                    admin_handler.user_service.update_ngo.side_effect = NotExistsError("NGO not found")
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 404
                    assert response["status_code"] == ID_NOT_EXIST
                    assert response["message"] == "NGO not found"

    def test_update_ngo_bad_request(self, app, admin_handler, valid_ngo_data):
        ngo_id = '123'
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                with patch('flask.request.get_json', side_effect= BadRequest):
                    response, status_code = admin_handler.update_ngo(ngo_id)

                    assert status_code == 400
                    assert response["status_code"] == INVALID_REQUEST_BODY_FORMAT
                    assert response["message"] == "Invalid request body format"

    # Tests for delete_ngo method
    def test_delete_ngo_success(self, app, admin_handler):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                response, status_code = admin_handler.delete_ngo(ngo_id)

                assert status_code == 200
                assert response["status_code"] == 200
                assert response["message"] == "Success"
                admin_handler.user_service.delete_ngo.assert_called_once_with(ngo_id)

    def test_delete_ngo_not_exists(self, app, admin_handler):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                admin_handler.user_service.delete_ngo.side_effect = NotExistsError("NGO not found")
                response, status_code = admin_handler.delete_ngo(ngo_id)

                assert status_code == 404
                assert response["status_code"] == ID_NOT_EXIST
                assert response["message"] == "NGO not found"

    def test_delete_ngo_database_error(self, app, admin_handler):
        ngo_id = "123"
        with app.test_request_context():
            with app.app_context():
                g.role = Role.ADMIN.value
                admin_handler.user_service.delete_ngo.side_effect = DatabaseError("Database error")
                response, status_code = admin_handler.delete_ngo(ngo_id)

                assert status_code == 500
                assert response["status_code"] == DB_ERROR
                assert response["message"] == "Database error"