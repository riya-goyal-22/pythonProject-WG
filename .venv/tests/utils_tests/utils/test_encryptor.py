import unittest
import bcrypt
from app.utils.utilities.encrypter import hash_password, check_password


class TestPasswordHashing(unittest.TestCase):

    def setUp(self):
        """Set up the test data."""
        self.password = "secure_password"
        self.hashed_password = hash_password(self.password)

    def test_hash_password(self):
        """Test that the password is hashed correctly."""
        # Ensure the hashed password is not equal to the plain password
        self.assertNotEqual(self.password, self.hashed_password)

        # Ensure the hashed password is a valid bcrypt hash (should start with $2b$, $2a$, or $2y$)
        self.assertTrue(self.hashed_password.startswith('$2b$') or
                        self.hashed_password.startswith('$2a$') or
                        self.hashed_password.startswith('$2y$'))

    def test_check_password_correct(self):
        """Test that check_password returns True for correct password."""
        is_correct = check_password(self.hashed_password, self.password)
        self.assertTrue(is_correct)

    def test_check_password_incorrect(self):
        """Test that check_password returns False for incorrect password."""
        incorrect_password = "wrong_password"
        is_correct = check_password(self.hashed_password, incorrect_password)
        self.assertFalse(is_correct)


if __name__ == "__main__":
    unittest.main()
