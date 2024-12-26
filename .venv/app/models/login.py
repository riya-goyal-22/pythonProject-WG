from dataclasses import dataclass
from pydantic import BaseModel, field_validator
from app.utils.validators.validators import Validator
from utils.errors.custom_errors import CustomHTTPException
from app.config.config import VALIDATION_FAILURE


class UserLogin(BaseModel):
    email: str
    password: str

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

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
                "email": "john@watchguard.com",
                "password": "Strongpass@123"
            }
        }