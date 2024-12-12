from app.services.admin_service import AdminService
from app.services.donor_service import DonorService
from app.services.user_service import UserService
from flask import request, jsonify,g
from app.models.response import CustomResponse
from app.utils.validators.validators import Validator
from app.models.user import User
from app.models.user_dto import User_DTO
import app.utils.utilities.token as TokenClass
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError, UserExistsError, DatabaseError, \
    InvalidCredentialsError, NotExistsError


class UserHandler:
    def __init__(self, user_service: UserService|AdminService|DonorService):
        self.user_service = user_service

    # Protected by middleware which check token
    def get_profile(self):
        auth_header = request.headers.get('Authorization')
        token = auth_header[len('Bearer '):]
        try:
            #payload = TokenClass.decode_token(token)
            user = self.user_service.get_profile(g.get('user_id'))
            data = User_DTO(
                id=user.id,
                name=user.name,
                address=user.address,
                email=user.email,
                role=user.role,
                phone_no=user.phone_no
            )
            return jsonify(CustomResponse(200, "Success", data.to_dict()).to_dict()),200

        except TokenExpiredError as e:
            # Handle TokenExpiredError
            return jsonify(CustomResponse(401, f"Error: {str(e)} - Please renew your token.", None).to_dict()),401

        except TokenInvalidError as e:
            # Handle TokenInvalidError
            return jsonify(CustomResponse(401, f"Error: {str(e)} - The token provided is invalid.", None).to_dict()),401

        except DatabaseError as e:
            # Handle database error
            return jsonify(CustomResponse(500, str(e), None).to_dict()),500

        except Exception as e:
            # Handle any other unexpected exceptions
            return jsonify(CustomResponse(401, f"An unexpected error occurred: {str(e)}", None).to_dict()),401

    def login(self):
        data = request.get_json()
        if not data:
            return jsonify(CustomResponse(400, "Missing Request body", None).to_dict()),400
        required_fields = ['email', 'password']
        if not Validator.validate_required_fields(data, required_fields):
            return jsonify(CustomResponse(400, "Missing required fields", None).to_dict()),400
        try:
            token = self.user_service.login(data['email'], data['password'])
            return jsonify(CustomResponse(200, "Success", token).to_dict()),200
        except InvalidCredentialsError as e:
            return jsonify(CustomResponse(401, str(e), None).to_dict()),401
        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()),500

    # middleware
    def get_list_of_ngos(self):
        try:
            ngos = self.user_service.get_all_ngos()
            ngos_dto = [ngo.to_dict() for ngo in ngos]
            return jsonify(CustomResponse(200, 'Success', ngos_dto).to_dict()),200

        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()),500

    # middleware
    def get_one_ngo(self,ngo_id):
        try:
            ngo = self.user_service.get_ngo_by_id(ngo_id)
            return jsonify(CustomResponse(200, "Success", ngo.to_dict()).to_dict())

        except NotExistsError as e:
            return jsonify(CustomResponse(400, str(e), None).to_dict()),400
        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()),500








