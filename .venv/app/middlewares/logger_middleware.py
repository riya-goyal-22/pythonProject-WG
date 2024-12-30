from app.config.config import UNEXPECTED_ERROR
from app.models.response import CustomResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.utils.utilities.context import get_user_from_context
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from app.utils.logger.logger import Logger
import json
import traceback
from fastapi.responses import StreamingResponse


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
        user_data = get_user_from_context(request)
        user_id = user_data["user_id"] if user_data else ""
        user_role = user_data["role"] if user_data else ""

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
        user_data = get_user_from_context(request)
        user_id = user_data["user_id"] if user_data else ""
        user_role = user_data["role"] if user_data else ""

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