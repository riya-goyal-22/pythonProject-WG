import pytest
import datetime
import jwt
from config.config import SECRET_KEY
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.config.config import TOKEN_MISSING, TOKEN_INVALID, TOKEN_EXPIRED
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError
from app.utils.utilities.token import decode_token
from app.utils.utilities.context import set_user_to_context
from app.middlewares.auth_middleware import AuthMiddleware
from app.utils.enums.role import Role


# Create a simple FastAPI app for testing
app = FastAPI()
# Add middleware after routes
app.add_middleware(AuthMiddleware)

@app.get("/protected")
async def protected_route():
    return {"message": "success"}


@app.get("/login")
async def login_route():
    return {"message": "login"}


@app.get("/signup")
async def signup_route():
    return {"message": "signup"}


@app.get("/")
async def root_route():
    return {"message": "root"}

client = TestClient(app)

def create_token(user_id="test-user", role=Role.DONOR.value, expired=False):
    """Helper function to create JWT tokens for testing"""
    payload = {
        "user_id": user_id,
        "role": role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1), # Token expires in 1 hour
        "iat": datetime.datetime.utcnow(),  # Issued at
        "nbf": datetime.datetime.utcnow(),  # Not before
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


class TestAuthMiddleware:
    def setup_method(self):
        # Setup mock token data
        self.client = client

    def test_valid_token(self):
        # Arrange
        token = create_token()

        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    def test_excluded_path(self):
        # Test all excluded paths
        excluded_paths = ['/login', '/signup', '/', '/docs', '/openapi.json']

        for path in excluded_paths:
            if path in ['/login', '/signup', '/']:  # Only test paths we've defined
                response = client.get(path)
                assert response.status_code == 200

    def test_missing_token(self):
        # Act
        response = client.get("/protected")

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_MISSING
        assert "Missing token" in response.json()["message"]

    def test_invalid_token_format(self):
        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": "Invalid-Format"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_INVALID

    def test_expired_token(self):
        token = create_token(expired=True)

        # Act
        response = self.client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_EXPIRED

    def test_invalid_token(self):
        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer invalid.token.here"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_INVALID

    def test_invalid_token_payload(self):
        # Arrange
        payload = {
            "user_id": "test-user",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_INVALID
        assert "invalid token" in response.json()["message"]

    @patch('app.utils.utilities.token.decode_token')
    def test_unexpected_error(self,mock_decode_token):
        # Arrange
        mock_decode_token.side_effect = Exception("Unexpected error")

        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {self.valid_token}"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["status_code"] == TOKEN_INVALID

    @patch('app.utils.utilities.context.set_user_to_context')
    def test_context_setting(self, mock_set_context):
        # Arrange
        token = create_token()
        # Act
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        mock_set_context.assert_called_once()
        context_call = mock_set_context.call_args
        assert context_call[1]['user_data']['user_id'] == "test-user"
        assert context_call[1]['user_data']['role'] == Role.DONOR.value
        assert response.status_code == 200

