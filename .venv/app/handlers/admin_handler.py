from app.handlers.user_handler import UserHandler
from app.models.new_ngo import NewNGO
from app.services.admin_service import AdminService
from app.utils.errors.custom_errors import DatabaseError, NotExistsError, NGOExistsError
from app.utils.validators.validators import Validator
from app.models.response import CustomResponse
from app.utils.custom_decorators.admin_decorator import admin
from app.models.ngo import NGO
from fastapi import Request
from utils.errors.custom_errors import CustomHTTPException
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dataclasses import fields
from app.config.config import MISSING_REQUEST_BODY, MISSING_REQUIRED_FIELDS, VALIDATION_FAILURE, DB_ERROR, \
    INVALID_REQUEST_BODY_FORMAT, ID_NOT_EXIST


class AdminHandler(UserHandler):
    def __init__(self, admin_service: AdminService):
        super().__init__(admin_service)

    @admin
    def create_ngo(self,request: Request,data: NewNGO):
        try:
            ngo = NGO.from_dict(data.dict())
            self.user_service.add_ngo(ngo)
            return CustomResponse(status_code=201, message="Successfully created",http_status_code=201).to_response()

        except NGOExistsError as e:
            return CustomResponse(status_code=VALIDATION_FAILURE, message=str(e),http_status_code=422).to_response()

        except DatabaseError:
            return CustomResponse(http_status_code=500,status_code=DB_ERROR, message="Internal server error").to_response()

        except Exception:
            return CustomResponse(status_code=UNEXPECTED_ERROR, message="Unexpected error",http_status_code=500).to_response()


    @admin
    def update_ngo(self, request: Request, ngo_id, data: NewNGO):
        try:
            ngo = NGO.from_dict(data.dict())
            ngo.id = ngo_id
            self.user_service.update_ngo(ngo)
            return CustomResponse(status_code=200, message="Successfully updated").to_response()

        except NotExistsError as e:
            return CustomResponse(status_code=ID_NOT_EXIST, message=str(e), http_status_code=404).to_response()

        except DatabaseError as e:
            return CustomResponse(status_code=DB_ERROR, message=str(e), http_status_code=500).to_response()

        except Exception:
            return CustomResponse(status_code=UNEXPECTED_ERROR, message="Unexpected error",http_status_code=500).to_response()


    @admin
    def delete_ngo(self, request: Request, ngo_id):
        try:
            self.user_service.delete_ngo(ngo_id)
            return CustomResponse(status_code=200, message="Successfully deleted").to_response()

        except NotExistsError as e:
            return CustomResponse(status_code=ID_NOT_EXIST, message=str(e), http_status_code=404).to_response()

        except DatabaseError as e:
            return CustomResponse(status_code=DB_ERROR, message=str(e), http_status_code=500).to_response()

        except Exception:
            return CustomResponse(status_code=UNEXPECTED_ERROR, message="Unexpected error",http_status_code=500).to_response()
