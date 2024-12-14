from app.handlers.user_handler import UserHandler
from app.models.new_ngo import NewNGO
from app.services.admin_service import AdminService
from app.utils.errors.custom_errors import DatabaseError, NotExistsError, NGOExistsError
from app.utils.validators.validators import Validator
from app.models.response import CustomResponse
from app.utils.custom_decorators.admin_decorator import admin
from app.models.ngo import NGO
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dataclasses import fields
from app.config.config import MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, VALIDATION_FAILURE, DB_ERROR, \
    INVALID_REQUEST_BODY_FORMAT, ID_NOT_EXIST


class AdminHandler(UserHandler):
    def __init__(self, admin_service: AdminService):
        super().__init__(admin_service)

    @admin
    def create_ngo(self):
        try:
            data = request.get_json()
            if not data:
                return CustomResponse(MISSING_REQUEST_BODY, "Missing Request body", None).to_dict(), 400
            required_fields = [field.name for field in fields(NewNGO)]
            if not Validator.validate_required_fields(data, required_fields):
                return CustomResponse(MISSING_REQUIRED_FIELDS, "Missing required fields", None).to_dict(), 422
            request_obj = NewNGO.from_dict(data)
            if not Validator.is_valid_email(request_obj.email):
                return CustomResponse(VALIDATION_FAILURE, "Invalid email id", None).to_dict(), 422
            if not Validator.validate_phone_no(request_obj.phone_no):
                return CustomResponse(VALIDATION_FAILURE, "Invalid phone number", None).to_dict(), 422
            request_obj_dict = request_obj.to_dict()
            ngo = NGO.from_dict(request_obj_dict)
            self.user_service.add_ngo(ngo)
            return CustomResponse(201, "Success", None).to_dict(), 201

        except NGOExistsError as e:
            return CustomResponse(VALIDATION_FAILURE, str(e), None).to_dict(), 422

        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500

        except BadRequest:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Invalid request body format", None).to_dict(), 400

        except UnsupportedMediaType:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Unsupported media type, Expected application/json", None).to_dict(), 415

    @admin
    def update_ngo(self, ngo_id):
        try:
            data = request.get_json()
            if not data:
                return CustomResponse(MISSING_REQUEST_BODY, "Missing Request body", None).to_dict(), 400
            required_fields = [field.name for field in fields(NewNGO)]
            if not Validator.validate_required_fields(data, required_fields):
                return CustomResponse(MISSING_REQUIRED_FIELDS, "Missing required fields", None).to_dict(), 422
            request_obj = NewNGO.from_dict(data)
            if not Validator.is_valid_email(request_obj.email):
                return CustomResponse(VALIDATION_FAILURE, "Invalid email id", None).to_dict(), 422
            if not Validator.validate_phone_no(request_obj.phone_no):
                return CustomResponse(VALIDATION_FAILURE, "Invalid phone number", None).to_dict(), 422
            ngo = NGO.from_dict(request_obj.to_dict())
            ngo.id = ngo_id
            self.user_service.update_ngo(ngo)
            return CustomResponse(200, "Success", None).to_dict(), 200

        except NotExistsError as e:
            return CustomResponse(ID_NOT_EXIST, str(e), None).to_dict(), 404

        except DatabaseError as e:
            return CustomResponse(DB_ERROR, str(e), None).to_dict(), 500

        except BadRequestKeyError:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Invalid request body format", None).to_dict(), 400

        except UnsupportedMediaType:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Unsupported media type, Expected application/json", None).to_dict(), 415

    @admin
    def delete_ngo(self, ngo_id):
        try:
            self.user_service.delete_ngo(ngo_id)
            return CustomResponse(200, "Success", None).to_dict(), 200

        except NotExistsError as e:
            return CustomResponse(ID_NOT_EXIST, str(e), None).to_dict(), 404

        except DatabaseError as e:
            return CustomResponse(DB_ERROR, str(e), None).to_dict(), 500
