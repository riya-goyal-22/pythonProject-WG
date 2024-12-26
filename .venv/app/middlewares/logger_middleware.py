from app.config.config import UNEXPECTED_ERROR
from app.models.response import CustomResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from utils.utilities.context import get_user_from_context
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from app.utils.logger.logger import Logger
import json
import traceback
from fastapi.responses import StreamingResponse


# class LogRequestMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app, logger: Logger):
#         super().__init__(app)
#         self.logger = logger
#
#     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
#         request_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
#         user_data = get_user_from_context(request)
#         user_id = user_data["user_id"] if user_data else ""
#         user_role = user_data["role"] if user_data else ""
#         body = await request.json() if request.method in ['POST', 'PUT', 'PATCH'] else {}
#         sanitized_body = self.logger._sanitize_body(body)
#         log_data = {
#             "timestamp": request_time,
#             "method": request.method,
#             "url": str(request.url),
#             "remote_addr": request.client.host,
#             "headers": dict(request.headers),
#             "query_params": dict(request.query_params),
#             "body": sanitized_body,
#             "user_agent": request.headers.get('User-Agent'),
#             "user_id": user_id,
#             "user_role": user_role
#         }
#         self.logger.info(json.dumps(log_data, indent=4))
#
#         response = await call_next(request)
#         return response

#
# # class LogResponseMiddleware(BaseHTTPMiddleware):
# #     def __init__(self, app, logger: Logger):
# #         super().__init__(app)
# #         self.logger = logger
# #
# #     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
# #         response = await call_next(request)
# #
# #         response_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
# #         user_data = get_user_from_context(request)
# #         user_id = user_data['user_id'] if user_data else ""
# #         user_role = user_data['role'] if user_data else ""
# #         response_data =  response
# #
# #         log_data = {
# #             "timestamp": response_time,
# #             "status_code": response.status_code,
# #             "method": request.method,
# #             "url": str(request.url),
# #             "response_data": response_data,
# #             "response_headers": dict(response.headers),
# #             "user_id": user_id,
# #             "user_role": user_role
# #         }
# #
# #         self.logger.info(json.dumps(log_data, indent=4))
# #         return response
#
# class LogResponseMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app, logger: Logger):
#         super().__init__(app)
#         self.logger = logger
#
#     async def dispatch(self, request: Request, call_next) -> Response:
#         original_response = await call_next(request)
#
#         response_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
#         user_data = get_user_from_context(request)
#         user_id = user_data['user_id'] if user_data else ""
#         user_role = user_data['role'] if user_data else ""
#
#         try:
#             # Create a copy of the response for logging
#             response_copy = Response(
#                 content=await original_response.body() if not isinstance(original_response, StreamingResponse) else b"",
#                 status_code=original_response.status_code,
#                 headers=dict(original_response.headers),
#                 media_type=original_response.media_type
#             )
#
#             # Get response content based on type
#             if isinstance(original_response, StreamingResponse):
#                 response_body = {
#                     "content_type": original_response.media_type,
#                     "status": "Streaming response - content not logged"
#                 }
#             else:
#                 try:
#                     if response_copy.headers.get("content-type", "").startswith("application/json"):
#                         response_body = json.loads(response_copy.body.decode())
#                     else:
#                         response_body = response_copy.body.decode()
#                 except Exception as e:
#                     response_body = f"Failed to decode response body: {str(e)}"
#
#             log_data = {
#                 "timestamp": response_time,
#                 "status_code": original_response.status_code,
#                 "method": request.method,
#                 "url": str(request.url),
#                 "content_type": original_response.headers.get("content-type", ""),
#                 "response_body": response_body,
#                 "response_headers": dict(original_response.headers),
#                 "user_id": user_id,
#                 "user_role": user_role
#             }
#
#             self.logger.info(json.dumps(log_data, indent=4))
#
#         except Exception as e:
#             self.logger.error(f"Error logging response: {str(e)}")
#
#         return original_response


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: Logger):
        super().__init__(app)
        self.logger = logger

    async def get_request_body(self, request: Request) -> Dict:
        """
        Safely extracts and sanitizes request body
        """
        try:
            body = await request.json()
            return self.logger._sanitize_body(body)
        except:
            try:
                body = await request.form()
                return dict(body)
            except:
                return {}

    async def log_request(self, request: Request, user_id: Optional[str] = None, user_role: Optional[str] = None):
        """
        Logs incoming request details
        """
        request_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
        body = await self.get_request_body(request)

        log_data = {
            "timestamp": request_time,
            "method": request.method,
            "url": str(request.url),
            "remote_addr": request.client.host if request.client else None,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "body": body,
            "user_agent": request.headers.get("user-agent"),
            "user_id": user_id,
            "user_role": user_role
        }

        self.logger.info(f"Request: {json.dumps(log_data, indent=4)}")

    async def log_response(self, request: Request, response: Response, user_id: Optional[str] = None,
                           user_role: Optional[str] = None):
        """
        Logs outgoing response details
        """
        response_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

        # Handle different response types
        if isinstance(response, StreamingResponse):
            response_data = "Streaming response - content not logged"
        elif isinstance(response, JSONResponse):
            response_data = json.loads(response.body.decode())
        else:
            try:
                response_data = response.body.decode()
            except:
                response_data = "Unable to decode response body"

        log_data = {
            "timestamp": response_time,
            "status_code": response.status_code,
            "method": request.method,
            "url": str(request.url),
            "response_data": response_data,
            "response_headers": dict(response.headers),
            "user_id": user_id,
            "user_role": user_role
        }

        self.logger.info(f"Response: {json.dumps(log_data, indent=4)}")

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get user context - implement this based on your auth system
        user_id = None
        user_role = None
        try:
            # Log request
            await self.log_request(request, user_id, user_role)

            # Process request
            response = await call_next(request)

            # Log response
            await self.log_response(request, response, user_id, user_role)

            return response

        except Exception as e:
            # Log exception
            self.log_exception(request, e, user_id, user_role)
            print(e)
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "status_code": 500,
                    "message": "An unexpected error occurred",
                    "data": None
                }
            )

    def log_exception(self, request: Request, exc: Exception, user_id: Optional[str] = None,
                      user_role: Optional[str] = None):
        """
        Logs exception details
        """
        exception_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

        log_data = {
            "timestamp": exception_time,
            "error_message": str(exc),
            "traceback": traceback.format_exc(),
            "request_method": request.method,
            "request_url": str(request.url),
            "request_remote_addr": request.client.host if request.client else None,
            "request_headers": dict(request.headers),
            "user_id": user_id,
            "user_role": user_role
        }

        self.logger.error(f"Exception: {json.dumps(log_data, indent=4)}")