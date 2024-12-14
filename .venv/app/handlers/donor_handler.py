from app.config.config import MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, VALIDATION_FAILURE, DB_ERROR, \
    INVALID_REQUEST_BODY_FORMAT
from app.handlers.user_handler import UserHandler
from app.models.signup import UserSignup
from app.services.donor_service import DonorService
from flask import request, jsonify
from app.models.response import CustomResponse
from app.utils.validators.validators import Validator
from app.models.user import User
from app.utils.errors.custom_errors import UserExistsError, DatabaseError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dataclasses import fields


class DonorHandler(UserHandler):
    def __init__(self, donor_service: DonorService):
        super().__init__(donor_service)

    def create_donor(self):
        try:
            data = request.get_json()
            if not data:
                return CustomResponse(MISSING_REQUEST_BODY, "Missing Request body", None).to_dict(), 400
            required_fields = [field.name for field in fields(UserSignup)]
            if not Validator.validate_required_fields(data, required_fields):
                return CustomResponse(MISSING_REQUIRED_FIELDS, "Missing required fields", None).to_dict(), 422
            request_obj = UserSignup.from_dict(data)
            if not Validator.is_valid_email(request_obj.email):
                return CustomResponse(VALIDATION_FAILURE, "Invalid email id", None).to_dict(), 422
            if not Validator.validate_phone_no(request_obj.phone_no):
                return CustomResponse(VALIDATION_FAILURE, "Invalid phone number", None).to_dict(), 422
            if not Validator.is_valid_password(request_obj.password):
                return CustomResponse(VALIDATION_FAILURE, "Password not strong", None).to_dict(), 422
            self.user_service.signup(User.from_dict(request_obj.to_dict()))
            return CustomResponse(201, "Success", None).to_dict(), 201
        except UserExistsError as e:
            return CustomResponse(VALIDATION_FAILURE, str(e), None).to_dict(), 422

        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500

        except BadRequest:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Invalid request body format", None).to_dict(), 400

        except UnsupportedMediaType:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Unsupported media type, Expected application/json", None).to_dict(), 415
