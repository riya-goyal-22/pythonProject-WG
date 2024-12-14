import logging
from logging.handlers import RotatingFileHandler
from threading import Lock
from app.config.config import LOG_FILE


class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialize_logger()
            return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger("ThreadSafeLogger")
        self.logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all logs

        # Rotating File Handler (Thread-Safe)
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)

        # Custom Formatter with extra fields
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s "
        )
        file_handler.setFormatter(formatter)

        # Adding Handler
        self.logger.addHandler(file_handler)

    # Convenience methods for logging
    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)
