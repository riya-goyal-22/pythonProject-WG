from app.config.config import DB_ERROR, MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, INVALID_CREDENTIALS, \
    INVALID_REQUEST_BODY_FORMAT, ID_NOT_EXIST
from app.models.login import UserLogin
from app.services.admin_service import AdminService
from app.services.donor_service import DonorService
from app.services.user_service import UserService
from fastapi import Request
from app.models.response import CustomResponse
from app.utils.validators.validators import Validator
from app.models.user_dto import User_DTO
from app.utils.errors.custom_errors import DatabaseError, \
    InvalidCredentialsError, NotExistsError
from app.utils.utilities.context import get_user_from_context
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dataclasses import fields


class UserHandler:
    def __init__(self, user_service: UserService | AdminService | DonorService):
        self.user_service = user_service

    def get_profile(self,request: Request):
        try:
            user_id = get_user_from_context(request)['user_id']
            user = self.user_service.get_profile(user_id)
            data = User_DTO(
                id=user.id,
                name=user.name,
                address=user.address,
                email=user.email,
                role=user.role,
                phone_no=user.phone_no
            )
            return CustomResponse(status_code=200, message="Successfully viewed user profile", data=data.to_dict()).to_response()

        except DatabaseError:
            return CustomResponse(status_code=DB_ERROR, message="Internal server error", http_status_code=500).to_response()


    def login(self, data: UserLogin):
        try:
            token = self.user_service.login(data.email, data.password)
            return CustomResponse(status_code=200, message="Successful login", data=token).to_response()

        except InvalidCredentialsError as e:
            return CustomResponse(status_code=INVALID_CREDENTIALS, message=str(e), http_status_code=401).to_response()

        except DatabaseError:
            return CustomResponse(status_code=DB_ERROR, message="Internal server error", http_status_code=500).to_response()


    def get_list_of_ngos(self):
        try:
            ngos = self.user_service.get_all_ngos()
            ngos_dto = [ngo.to_dict() for ngo in ngos]
            return CustomResponse(status_code=200, message='Successfully retreived list of NGOs', data=ngos_dto).to_response()

        except DatabaseError:
            return CustomResponse(status_code=DB_ERROR, message="Internal server error", http_status_code=500).to_response()


    def get_one_ngo(self, ngo_id):
        try:
            ngo = self.user_service.get_ngo_by_id(ngo_id)
            return CustomResponse(status_code=200, message="Successfully retreived ngo by id", data=ngo.to_dict()).to_response()

        except NotExistsError as e:
            return CustomResponse(status_code=ID_NOT_EXIST, message=str(e), http_status_code=404).to_response()

        except DatabaseError:
            return CustomResponse(status_code=DB_ERROR, message="Internal server error", http_status_code=500).to_response()
