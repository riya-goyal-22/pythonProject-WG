import jwt
from app.models.response import CustomResponse
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError
from flask import request, jsonify, g

from app.utils.utilities.token import decode_token


def auth_middleware():
    if request.path in ['/user/login', '/user/signup','/']:
        return None

    auth_token = request.headers.get('Authorization')
    if not auth_token or not auth_token.startswith('Bearer '):
        return jsonify(CustomResponse(401,"Unauthorized-Missing Token",None).to_dict()), 401

    token = auth_token.split(' ')[1]
    try:
        # Decode the token using the secret key
        decoded_token = decode_token(token)

        # Extract user_id and role from the decoded token
        user_id = decoded_token.get("user_id")
        role = decoded_token.get("role")

        if not user_id or not role:
            return jsonify(CustomResponse(401,"Unauthorized, invalid token payload",None).to_dict()), 401

        # Set user_id and role in Flask's global context
        g.user_id = user_id
        g.role = role

    except TokenExpiredError as e:
        return jsonify(CustomResponse(401,str(e),None).to_dict()), 401
    except TokenInvalidError as e:
        return jsonify(CustomResponse(401,str(e),None).to_dict()), 401