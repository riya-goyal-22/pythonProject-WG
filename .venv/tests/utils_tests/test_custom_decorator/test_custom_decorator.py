import unittest
from unittest.mock import MagicMock

from config.config import TOKEN_INVALID
from fastapi import Request
from app.utils.enums.role import Role
from app.models.response import CustomResponse
from app.utils.custom_decorators.admin_decorator import admin
from app.config.config import INVALID_ACCESS

class TestAdminDecorator(unittest.TestCase):

    def test_admin_decorator_authorized(self):
        """
        Test admin decorator with authorized access
        """
        # Create a mock request with admin user
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "admin"}

        # Mock function to be decorated
        @admin
        def test_function(request: Request):
            return "Authorized"

        # Run the function directly (no async needed for test)
        result = test_function(mock_request)
        self.assertEqual(result, "Authorized")

    def test_admin_decorator_unauthorized(self):
        """
        Test admin decorator with unauthorized access
        """
        # Create a mock request with non-admin user
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "user"}

        # Mock function to be decorated
        @admin
        def test_function(request: Request):
            return "Authorized"

        # Run the function directly
        result = test_function(mock_request)

        # Check for unauthorized response
        self.assertEqual(result["status_code"],INVALID_ACCESS)
        self.assertEqual(result["message"], "Admin access required")

    def test_admin_decorator_no_request(self):
        """
        Test admin decorator when request context is not available
        """
        # Mock function to be decorated
        @admin
        def test_function():
            return "Authorized"

        # Run the function directly (no async needed)
        result = test_function()

        # Check for invalid token payload error
        self.assertEqual(result["status_code"], TOKEN_INVALID)
        self.assertEqual(result["message"], "Request context not available")

if __name__ == '__main__':
    unittest.main()
