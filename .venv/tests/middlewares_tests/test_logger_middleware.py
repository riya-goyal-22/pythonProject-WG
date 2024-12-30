import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse
from unittest.mock import MagicMock
from app.middlewares.logger_middleware import LogMiddleware
from unittest.mock import ANY


class TestLogMiddleware(unittest.TestCase):

    def setUp(self):
        self.app = FastAPI()
        self.logger = MagicMock()  # Mocking the logger

        @self.app.get("/test")
        async def test_endpoint():
            return JSONResponse(content={"message": "Hello, World!"})

        # Add middleware with mocked logger
        self.app.add_middleware(LogMiddleware, logger=self.logger)

        self.client = TestClient(self.app)

    def test_request_logging(self):
        response = self.client.get("/test")

        # Check that request was logged
        self.logger.info.assert_any_call(ANY)

    def test_response_logging(self):
        response = self.client.get("/test")

        # Check that response was logged
        self.logger.info.assert_any_call(ANY)

    def test_exception_logging(self):
        @self.app.get("/error")
        async def error_endpoint():
            raise ValueError("An intentional error!")

        response = self.client.get("/error")

        # Check that exception was logged
        self.logger.error.assert_any_call(ANY)


if __name__ == '__main__':
    unittest.main()