import json
import traceback
from datetime import datetime, timedelta
import flask
from app.config.config import UNEXPECTED_ERROR
from app.models.response import CustomResponse
from flask import request, jsonify, g
from logging import Logger


def _sanitize_body(body):
    """
    This method sanitizes the request body to remove sensitive information.
    """
    if isinstance(body, dict):
        sanitized_body = body.copy()
        for key in sanitized_body:
            if key.lower() in ['password']:
                sanitized_body[key] = "****"
        return sanitized_body
    return body


def log_request_middleware(logger: Logger):
    request_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
    user_id = getattr(g, 'user_id', None)
    user_role = getattr(g, 'user_role', None)
    sanitized_body = _sanitize_body(request.get_json(silent=True) or {})
    log_data = {
        "timestamp": request_time,
        "method": request.method,
        "url": request.url,
        "remote_addr": request.remote_addr,
        "headers": dict(request.headers),
        "query_params": request.args.to_dict(),
        "body": sanitized_body,
        "user_agent": request.user_agent.string,
        "user_id": user_id,
        "user_role": user_role
    }
    logger.info(json.dumps(log_data, indent=4))


def log_response_middleware(logger: Logger, response: flask.Response) -> flask.Response:
    response_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
    user_id = getattr(g, 'user_id', None)
    user_role = getattr(g, 'user_role', None)
    response_data = response.get_json() if response.is_json else {}
    log_data = {
        "timestamp": response_time,
        "status_code": response.status_code,
        "method": request.method,
        "url": request.url,
        "response_data": response_data,
        "response_headers": dict(response.headers),
        "user_id": user_id,
        "user_role": user_role
    }
    logger.info(json.dumps(log_data, indent=4))
    return response


def log_exceptions(logger: Logger, e: Exception):
    exception_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
    user_id = getattr(g, 'user_id', None)
    user_role = getattr(g, 'user_role', None)
    sanitized_body = _sanitize_body(request.get_json(silent=True) or {})
    log_data = {
        "timestamp": exception_time,
        "error_message": str(e),
        "traceback": traceback.format_exc(),
        "request_method": request.method,
        "request_url": request.url,
        "request_remote_addr": request.remote_addr,
        "request_headers": dict(request.headers),
        "request_body": sanitized_body,
        "user_id": user_id,
        "user_role": user_role
    }
    logger.error(json.dumps(log_data, indent=4))
    return CustomResponse(UNEXPECTED_ERROR, "An unexpected error occurred", None), 500
