from app.config.config import DB_ERROR, MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, INVALID_CREDENTIALS, \
    INVALID_REQUEST_BODY_FORMAT, ID_NOT_EXIST
from app.models.login import UserLogin
from app.services.admin_service import AdminService
from app.services.donor_service import DonorService
from app.services.user_service import UserService
from flask import request, jsonify, g
from app.models.response import CustomResponse
from app.utils.validators.validators import Validator
from app.models.user_dto import User_DTO
from app.utils.errors.custom_errors import DatabaseError, \
    InvalidCredentialsError, NotExistsError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dataclasses import fields


class UserHandler:
    def __init__(self, user_service: UserService | AdminService | DonorService):
        self.user_service = user_service

    def get_profile(self):
        try:
            user = self.user_service.get_profile(g.get('user_id'))
            data = User_DTO(
                id=user.id,
                name=user.name,
                address=user.address,
                email=user.email,
                role=user.role,
                phone_no=user.phone_no
            )
            return CustomResponse(200, "Successfully viewed user profile", data.to_dict()).to_dict(), 200

        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500

    def login(self):
        try:
            data = request.get_json()
            if not data:
                return CustomResponse(MISSING_REQUEST_BODY, "Missing Request body", None).to_dict(), 400
            required_fields = [field.name for field in fields(UserLogin)]
            if not Validator.validate_required_fields(data, required_fields):
                return CustomResponse(MISSING_REQUIRED_FIELDS, "Missing required fields", None).to_dict(), 422
            request_obj = UserLogin.from_dict(data)
            token = self.user_service.login(request_obj.email, request_obj.password)
            return CustomResponse(200, "Successful login", token).to_dict(), 200

        except InvalidCredentialsError as e:
            return CustomResponse(INVALID_CREDENTIALS, str(e), None).to_dict(), 401
        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500
        except BadRequest:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Invalid request body format", None).to_dict(), 400
        except UnsupportedMediaType:
            return CustomResponse(INVALID_REQUEST_BODY_FORMAT, "Unsupported media type, Expected application/json", None).to_dict(), 415

    def get_list_of_ngos(self):
        try:
            ngos = self.user_service.get_all_ngos()
            ngos_dto = [ngo.to_dict() for ngo in ngos]
            return CustomResponse(200, 'Successfully retreived list of NGOs', ngos_dto).to_dict(), 200

        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500

    def get_one_ngo(self, ngo_id):
        try:
            ngo = self.user_service.get_ngo_by_id(ngo_id)
            return CustomResponse(200, "Success", ngo.to_dict()).to_dict(), 200

        except NotExistsError as e:
            return CustomResponse(ID_NOT_EXIST, str(e), None).to_dict(), 404
        except DatabaseError:
            return CustomResponse(DB_ERROR, "Internal server error", None).to_dict(), 500
