from dataclasses import dataclass
from pydantic import BaseModel, field_validator
from utils.errors.custom_errors import CustomHTTPException
from app.config.config import VALIDATION_FAILURE
from app.utils.validators.validators import Validator


class NewNGO(BaseModel):
    name: str
    address: str
    phone_no: str
    email: str
    details: str

    @field_validator('name')
    def validate_name(cls, v: str):
        if not Validator.is_valid_name(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a valid name")
        return v

    @field_validator('email')
    def validate_email(cls, v: str):
        if not Validator.is_valid_email(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a valid email")
        return v

    @field_validator('phone_no')
    def validate_phone_no(cls, v: str):
        if not Validator.validate_phone_no(v):
            raise CustomHTTPException(422, VALIDATION_FAILURE, "Not a valid phone number")
        return v

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jojn Doe",
                "address":"sector no 12",
                "email": "john@watchguard.com",
                "phone_no":"9999999999",
                "details":"any detail"
            }
        }
