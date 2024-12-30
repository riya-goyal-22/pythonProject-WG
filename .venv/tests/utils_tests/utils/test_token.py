import unittest
from unittest.mock import MagicMock
import datetime
import jwt
from app.utils.utilities.token import generate_token, decode_token
from app.config.config import SECRET_KEY
from app.utils.errors.custom_errors import TokenExpiredError, TokenInvalidError


class TestAuth(unittest.TestCase):

    def test_generate_token(self):
        """Test token generation."""
        user_id = "123"
        email = "test@example.com"
        role = "admin"

        # Create a MagicMock for jwt.encode
        mock_encode = MagicMock()

        # Mock current time
        mock_current_time = datetime.datetime.utcnow()
        mock_exp_time = mock_current_time + datetime.timedelta(hours=1)

        # Simulate what the JWT.encode will return (mock token)
        mock_encoded_token = "mocked_jwt_token"
        mock_encode.return_value = mock_encoded_token

        # Replace jwt.encode with the mock object
        jwt.encode = mock_encode

        # Generate the token using the function
        token = generate_token(user_id, email, role)

        # Verify that jwt.encode was called with the expected arguments
        mock_encode.assert_called_once()
        args, kwargs = mock_encode.call_args

        # Compare the exp time with a small tolerance
        actual_exp_time = args[0]['exp']
        tolerance = datetime.timedelta(seconds=5)
        self.assertTrue(abs(actual_exp_time - mock_exp_time) < tolerance)

        # Ensure that the returned token is the mock value
        self.assertEqual(token, mock_encoded_token)

    def test_decode_token_valid(self):
        """Test decoding a valid token."""
        # Create a MagicMock for jwt.decode
        mock_decode = MagicMock()

        # Simulate the payload returned by the decoded token
        mock_decoded_payload = {
            'user_id': '123',
            'email': 'test@example.com',
            'role': 'admin'
        }
        mock_decode.return_value = mock_decoded_payload

        # Replace jwt.decode with the mock object
        jwt.decode = mock_decode

        token = "mocked_jwt_token"
        decoded_data = decode_token(token)

        # Ensure jwt.decode is called with the correct token and secret
        mock_decode.assert_called_once_with(token, SECRET_KEY, algorithms=['HS256'])

        # Verify the decoded data matches the expected payload
        self.assertEqual(decoded_data, mock_decoded_payload)

    def test_decode_token_expired(self):
        """Test decoding an expired token raises the TokenExpiredError."""
        # Create a MagicMock for jwt.decode
        mock_decode = MagicMock()

        # Simulate an ExpiredSignatureError exception
        mock_decode.side_effect = jwt.ExpiredSignatureError

        # Replace jwt.decode with the mock object
        jwt.decode = mock_decode

        token = "expired_token"

        with self.assertRaises(TokenExpiredError):
            decode_token(token)

    def test_decode_token_invalid(self):
        """Test decoding an invalid token raises the TokenInvalidError."""
        # Create a MagicMock for jwt.decode
        mock_decode = MagicMock()

        # Simulate an InvalidTokenError exception
        mock_decode.side_effect = jwt.InvalidTokenError

        # Replace jwt.decode with the mock object
        jwt.decode = mock_decode

        token = "invalid_token"

        with self.assertRaises(TokenInvalidError):
            decode_token(token)


if __name__ == "__main__":
    unittest.main()
