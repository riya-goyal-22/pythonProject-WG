from app.config.config import INVALID_ACCESS
from flask import g, jsonify
from app.utils.enums.role import Role
from app.models.response import CustomResponse


def admin(f):
    def wrapped_func(*args, **kwargs):
        # Check if the user role in g is 'admin'
        if g.get("role") != Role.ADMIN.value:
            return CustomResponse(INVALID_ACCESS, "Admin access required", None).to_dict(), 403
        return f(*args, **kwargs)

    return wrapped_func
