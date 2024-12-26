from dataclasses import dataclass
from app.config.config import VALIDATION_FAILURE
from app.utils.validators.validators import Validator
from pydantic import BaseModel, field_validator
from utils.errors.custom_errors import CustomHTTPException


class UserSignup(BaseModel):
    name: str
    address: str
    phone_no: str
    email: str
    password: str

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

    @field_validator('name')
    def validate_name(cls, v: str):
        if not Validator.is_valid_name(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,"Not a valid name")
        return v

    @field_validator('phone_no')
    def validate_phone_no(cls, v: str):
        if not Validator.validate_phone_no(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a valid phone number")
        return v

    @field_validator('email')
    def validate_email(cls, v: str):
        if not Validator.is_valid_email(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a valid email")
        return v

    @field_validator('password')
    def validate_password(cls, v: str):
        if not Validator.is_valid_password(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a strong password")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@gmail.com",
                "password": "Strongpass@123",
                "phone_no": "9999999999",
                "address": "Ward no 12"
            }
        }