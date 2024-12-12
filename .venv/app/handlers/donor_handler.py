from app.handlers.user_handler import UserHandler
from app.services.donor_service import DonorService
from flask import request, jsonify
from app.models.response import CustomResponse
from app.utils.validators.validators import Validator
from app.models.user import User
from app.models.user_dto import User_DTO
import app.utils.utilities.token as TokenClass
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError, UserExistsError, DatabaseError, \
    InvalidCredentialsError


class DonorHandler(UserHandler):
    def __init__(self,donor_service: DonorService):
        super().__init__(donor_service)

    def create_donor(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify(CustomResponse(400,"Missing Request body",None).to_dict()),400
            required_fields = ['name','address','phone_no','email','password']
            if not Validator.validate_required_fields(data,required_fields):
                return jsonify(CustomResponse(400,"Missing required fields",None).to_dict()),400
            if not Validator.is_valid_email(data['email']):
                return jsonify(CustomResponse(400,"Invalid email id",None).to_dict()),400
            if not Validator.validate_phone_no(data['phone_no']):
                return jsonify(CustomResponse(400,"Invalid phone number",None).to_dict()),400
            if not Validator.is_valid_password(data['password']):
                return jsonify(CustomResponse(400,"Password not strong",None).to_dict()),400
            user = User(
                name=data['name'],
                address=data['address'],
                phone_no=data['phone_no'],
                email=data['email'],
                password=data['password'],
            )
            self.user_service.signup(user)
            return jsonify(CustomResponse(201,"Success",None).to_dict()),201
        except UserExistsError as e:
            return jsonify(CustomResponse(400,str(e),None).to_dict()),400

        except DatabaseError as e:
            return jsonify(CustomResponse(400,str(e),None).to_dict()),400

        except Exception as e:
            return jsonify(CustomResponse(500,str(e),None).to_dict()),500










