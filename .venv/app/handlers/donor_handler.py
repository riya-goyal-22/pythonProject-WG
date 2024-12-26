from app.config.config import MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, VALIDATION_FAILURE, DB_ERROR, \
    INVALID_REQUEST_BODY_FORMAT
from app.handlers.user_handler import UserHandler
from app.models.signup import UserSignup
from app.services.donor_service import DonorService
from config.config import UNEXPECTED_ERROR
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

    def create_donor(self,data: UserSignup):
        try:
            self.user_service.signup(User.from_dict(data.dict()))
            return CustomResponse(status_code=201, message="Successfully signed up").to_response()

        except UserExistsError as e:
            return CustomResponse(status_code=VALIDATION_FAILURE, message=str(e), http_status_code=422).to_response()

        except DatabaseError:
            return CustomResponse(status_code=DB_ERROR, message="Internal server error", http_status_code=500).to_response()

        except Exception:
            return CustomResponse(status_code=UNEXPECTED_ERROR, message="Unexpected error",http_status_code=500).to_response()

