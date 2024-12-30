from app.config.config import TOKEN_MISSING, TOKEN_INVALID, TOKEN_EXPIRED
from app.models.response import CustomResponse
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, Security
from app.utils.utilities.token import decode_token
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from app.utils.errors.custom_errors import CustomHTTPException
from app.utils.utilities.context import set_user_to_context, get_user_from_context


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ['/login', '/signup', '/', '/docs', '/openapi.json']:
            return await call_next(request)

        try:
            # Get token
            token = request.headers.get("Authorization")
            if token:
                token = token.split("Bearer ")[-1]

            if not token:
                return CustomResponse(http_status_code=401, status_code=TOKEN_MISSING,
                                      message="Missing token").to_response()

            # Decode the token using the secret key
            decoded_token = decode_token(token)
            print(decoded_token)

            # Extract user_id and role from the decoded token
            user_id = decoded_token.get("user_id")
            role = decoded_token.get("role")

            if not user_id or not role:
                return CustomResponse(http_status_code=401, status_code=TOKEN_INVALID,
                                      message="Unauthorized, invalid token payload").to_response()

            # Set user_id and role in request context
            user_data = {
                "user_id": user_id,
                "role": role
            }
            set_user_to_context(request, user_data)

        except TokenExpiredError as e:
            # This specific exception should be caught first
            return CustomResponse(http_status_code=401, status_code=TOKEN_EXPIRED, message=str(e)).to_response()

        except TokenInvalidError as e:
            # Then catch invalid token errors
            return CustomResponse(http_status_code=401, status_code=TOKEN_INVALID, message=str(e)).to_response()

        except Exception as e:
            # Generic exception handler should be last
            return CustomResponse(http_status_code=401, status_code=TOKEN_INVALID, message=str(e)).to_response()

        response = await call_next(request)
        return response