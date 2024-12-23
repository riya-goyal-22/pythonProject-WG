import unittest
from unittest.mock import MagicMock
from app.utils.logger.logger import Logger


class TestLogger(unittest.TestCase):

    def setUp(self):
        """Set up the necessary mock objects before each test."""
        # Create a MagicMock for the logger instance
        self.mock_logger_instance = MagicMock()

        # Mock the getLogger method to return the mocked logger instance
        self.mock_get_logger = MagicMock(return_value=self.mock_logger_instance)

        # Mock the RotatingFileHandler and _initialize_logger to avoid actual file handling
        Logger._get_logger = self.mock_get_logger

        # Mock the _initialize_logger to set up the logger correctly
        Logger._initialize_logger = MagicMock(return_value=None)

        # Directly set the logger attribute here to avoid the error in tests
        self.logger = Logger()

        # Ensure self.logger has been set up correctly by checking the attribute
        self.logger.logger = self.mock_logger_instance

    def test_singleton_behavior(self):
        """Test that Logger follows the singleton pattern."""
        # Instantiate the Logger twice
        logger1 = Logger()
        logger2 = Logger()

        # Ensure both logger instances are the same (singleton behavior)
        self.assertIs(logger1, logger2)

    def test_info_logging(self):
        """Test that info logging works as expected."""
        # Call the info method
        message = "Test info message"
        self.logger.info(message)

        # Ensure the info method is called on the mock logger instance with the correct message
        self.mock_logger_instance.info.assert_called_once_with(message)

    def test_error_logging(self):
        """Test that error logging works as expected."""
        # Call the error method
        message = "Test error message"
        self.logger.error(message)

        # Ensure the error method is called on the mock logger instance with the correct message
        self.mock_logger_instance.error.assert_called_once_with(message)

    def test_warning_logging(self):
        """Test that warning logging works as expected."""
        # Call the warning method
        message = "Test warning message"
        self.logger.warning(message)

        # Ensure the warning method is called on the mock logger instance with the correct message
        self.mock_logger_instance.warning.assert_called_once_with(message)

    def test_debug_logging(self):
        """Test that debug logging works as expected."""
        # Call the debug method
        message = "Test debug message"
        self.logger.debug(message)

        # Ensure the debug method is called on the mock logger instance with the correct message
        self.mock_logger_instance.debug.assert_called_once_with(message)


if __name__ == "__main__":
    unittest.main()
