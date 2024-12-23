import unittest

from app.models.response import CustomResponse


class TestCustomResponse(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample CustomResponse instance
        response = CustomResponse(
            status_code=200,
            message="Request was successful.",
            data={"key": "value"}
        )

        # Expected dictionary representation of the CustomResponse instance
        expected_dict = {
            'status_code': 200,
            'message': "Request was successful.",
            'data': {"key": "value"}
        }

        # Assert that the to_dict method returns the correct dictionary
        self.assertEqual(response.to_dict(), expected_dict)

    def test_from_dict(self):
        # Sample dictionary to convert to a CustomResponse instance
        data_dict = {
            'status_code': 200,
            'message': "Request was successful.",
            'data': {"key": "value"}
        }

        # Convert the dictionary to a CustomResponse instance
        response = CustomResponse.from_dict(data_dict)

        # Assert that the created CustomResponse instance matches the dictionary values
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.message, "Request was successful.")
        self.assertEqual(response.data, {"key": "value"})

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'data')
        data_dict = {
            'status_code': 200,
            'message': "Request was successful."
        }

        # Assert that from_dict raises a TypeError because 'data' is missing
        with self.assertRaises(TypeError):
            CustomResponse.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
