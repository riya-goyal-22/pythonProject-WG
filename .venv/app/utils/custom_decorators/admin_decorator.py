from flask import g, jsonify
from app.enums.role import Role
from app.models.response import CustomResponse

def admin(f):
    def wrapped_func(*args, **kwargs):
        # Check if the user role in g is 'admin'
        if g.get("role") != Role.ADMIN.value:
            return jsonify(CustomResponse(403,"Admin access required",None)), 403
        return f(*args, **kwargs)

    return wrapped_func

# Riya Goyal


