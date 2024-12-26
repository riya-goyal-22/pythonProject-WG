from app.config.config import INVALID_ACCESS, TOKEN_INVALID, DB_ERROR
from app.utils.enums.role import Role
from app.models.response import CustomResponse
from functools import wraps
from fastapi import Request
from utils.utilities.context import get_user_from_context


def admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Get the Request object from args or kwargs
            request = next((arg for arg in args if isinstance(arg, Request)), kwargs.get('request'))

            if not request:
                return CustomResponse(
                    status_code=TOKEN_INVALID,
                    message="Request context not available"
                ).to_dict()

            user = get_user_from_context(request)
            if not user or user.get('role') != 'admin':
                return CustomResponse(
                    status_code=INVALID_ACCESS,
                    message="Admin access required"
                ).to_dict()

            return func(*args, **kwargs)

        except Exception as e:
            return CustomResponse(
                status_code=DB_ERROR,
                message="Error checking admin privileges"
            ).to_dict()

    return wrapper