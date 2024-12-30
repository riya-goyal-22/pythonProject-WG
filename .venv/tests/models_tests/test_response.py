import unittest
from starlette.responses import JSONResponse
from app.models.response import CustomResponse

class TestCustomResponse(unittest.TestCase):

    def setUp(self):
        # Initialize a CustomResponse object for testing
        self.response = CustomResponse(
            status_code=1001,
            message="Test Message",
            http_status_code=400,
            data={"key": "value"}
        )

    def test_to_dict_with_data(self):
        # Expected dictionary output
        expected_dict = {
            'status_code': 1001,
            'message': 'Test Message',
            'data': {'key': 'value'}
        }

        # Call to_dict method and compare with expected output
        result = self.response.to_dict()
        self.assertEqual(result, expected_dict)

    def test_to_dict_without_data(self):
        # Create a response without data
        response_without_data = CustomResponse(
            status_code=1001,
            message="Test Message",
            http_status_code=400
        )

        # Expected dictionary output
        expected_dict = {
            'status_code': 1001,
            'message': 'Test Message'
        }

        # Call to_dict method and compare with expected output
        result = response_without_data.to_dict()
        self.assertEqual(result, expected_dict)

    def test_to_response_with_data(self):
        # Create the expected JSONResponse object
        expected_response = JSONResponse(
            status_code=400,
            content={
                'status_code': 1001,
                'message': 'Test Message',
                'data': {'key': 'value'}
            }
        )

        # Call to_response method and compare status code and content
        result = self.response.to_response()
        self.assertEqual(result.status_code, expected_response.status_code)
        self.assertEqual(result.body.decode(), expected_response.body.decode())  # Comparing the body content

    def test_to_response_without_data(self):
        # Create a response without data
        response_without_data = CustomResponse(
            status_code=1001,
            message="Test Message",
            http_status_code=400
        )

        # Expected JSONResponse object without data
        expected_response = JSONResponse(
            status_code=400,
            content={
                'status_code': 1001,
                'message': 'Test Message'
            }
        )

        # Call to_response method and compare status code and content
        result = response_without_data.to_response()
        self.assertEqual(result.status_code, expected_response.status_code)
        self.assertEqual(result.body.decode(), expected_response.body.decode())  # Comparing the body content

    def tearDown(self):
        # Cleanup any resources (if needed)
        pass


if __name__ == "__main__":
    unittest.main()
