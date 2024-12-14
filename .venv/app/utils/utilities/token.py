import jwt
import datetime
from app.config.config import SECRET_KEY
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError


def generate_token(id: str, email: str, role: str):
    payload = {
        'user_id': id,
        'email': email,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise TokenInvalidError()
