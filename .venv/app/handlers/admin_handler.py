from app.handlers.user_handler import UserHandler
from app.services.admin_service import AdminService
from app.utils.errors.custom_errors import DatabaseError, NotExistsError, NGOExistsError
from app.utils.validators.validators import Validator
from app.models.response import CustomResponse
from app.utils.custom_decorators.admin_decorator import admin
from app.models.ngo import NGO
from flask import request, jsonify


class AdminHandler(UserHandler):
    def __init__(self,admin_service:AdminService):
        super().__init__(admin_service)

    #middleware
    @admin
    def create_ngo(self):
        data = request.get_json()
        if not data:
            return jsonify(CustomResponse(400, "Missing Request body", None).to_dict()), 400
        required_fields = ['name', 'address', 'phone_no', 'email', 'details']
        if not Validator.validate_required_fields(data, required_fields):
            return jsonify(CustomResponse(400, "Missing required fields", None).to_dict()), 400
        if not Validator.is_valid_email(data['email']):
            return jsonify(CustomResponse(400, "Invalid email id", None).to_dict()), 400
        if not Validator.validate_phone_no(data['phone_no']):
            return jsonify(CustomResponse(400, "Invalid phone number", None).to_dict()), 400
        try:
            ngo = NGO(
                name=data['name'],
                email=data['email'],
                address=data['address'],
                details=data['details'],
                phone_no=data['phone_no']
            )
            self.user_service.add_ngo(ngo)
            return jsonify(CustomResponse(201,"Success",None).to_dict()),201

        except NGOExistsError as e:
            return jsonify(CustomResponse(400, str(e), None).to_dict()), 400

        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

        except Exception as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

    @admin
    def update_ngo(self,ngo_id):
        data = request.get_json()
        if not data:
            return jsonify(CustomResponse(400, "Missing Request body", None).to_dict()), 400
        required_fields = ['name', 'address', 'phone_no', 'email', 'details']
        if not Validator.validate_required_fields(data, required_fields):
            return jsonify(CustomResponse(400, "Missing required fields", None).to_dict()), 400
        if not Validator.is_valid_email(data['email']):
            return jsonify(CustomResponse(400, "Invalid email id", None).to_dict()), 400
        if not Validator.validate_phone_no(data['phone_no']):
            return jsonify(CustomResponse(400, "Invalid phone number", None).to_dict()), 400
        try:
            ngo = NGO(
                id=ngo_id,
                name=data['name'],
                email=data['email'],
                address=data['address'],
                details=data['details'],
                phone_no=data['phone_no']
            )
            self.user_service.update_ngo(ngo)
            return jsonify(CustomResponse(200, "Success", None).to_dict()), 200

        except NotExistsError as e:
            return jsonify(CustomResponse(400, str(e), None).to_dict()),400

        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

        except Exception as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

    @admin
    def delete_ngo(self,ngo_id):
        try:
            self.user_service.delete_ngo(ngo_id)
            return jsonify(CustomResponse(200, "Success", None).to_dict()), 200

        except NotExistsError as e:
            return jsonify(CustomResponse(400, str(e), None).to_dict()),400

        except DatabaseError as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

        except Exception as e:
            return jsonify(CustomResponse(500, str(e), None).to_dict()), 500

