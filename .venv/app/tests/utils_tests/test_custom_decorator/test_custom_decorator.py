import unittest
from unittest.mock import MagicMock
from flask import Flask, g
from app.utils.enums.role import Role
from app.models.response import CustomResponse
from app.utils.custom_decorators.admin_decorator import admin
from app.config.config import INVALID_ACCESS

class TestAdminDecorator(unittest.TestCase):

    def setUp(self):
        # Set up a basic Flask app for testing
        self.app = Flask(__name__)

        # Create a simple route with the admin decorator
        @self.app.route('/admin-protected')
        @admin
        def protected():
            return "Welcome, admin!"

        # Initialize g mock
        self.g_mock = MagicMock()

    def test_admin_access_granted(self):
        with self.app.test_client() as client:
            with self.app.app_context():
                # Mock the 'g.get' method to return Role.ADMIN.value
                g.get = MagicMock(return_value=Role.ADMIN.value)
                response = client.get('/admin-protected')

            # Ensure the response status is 200 and the content matches
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Welcome, admin!")

    def test_admin_access_denied(self):
        # Simulate a non-admin role (e.g., user) using MagicMock
        self.g_mock.get.return_value = Role.DONOR.value

        with self.app.test_client() as client:
            # Mock the 'g' object within the context of the test request
            with self.app.app_context():
                g = self.g_mock
                response = client.get('/admin-protected')

            # Ensure the response status is 403 and the message is correct
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json, {
                "status_code": INVALID_ACCESS,
                "message": "Admin access required",
                "data": None
            })

if __name__ == '__main__':
    unittest.main()
