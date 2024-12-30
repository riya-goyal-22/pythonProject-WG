import unittest
import uuid
from app.models.ngo import NGO

class TestNGO(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample NGO instance
        ngo = NGO(
            name="Global Health Initiative",
            email="contact@ghi.org",
            details="A non-profit organization focused on global healthcare.",
            phone_no="987-654-3210",
            address="456 Health Street"
        )

        # Expected dictionary representation of the NGO instance
        expected_dict = {
            "id": ngo.id,  # ID should be dynamically generated
            "name": "Global Health Initiative",
            "email": "contact@ghi.org",
            "phone_no": "987-654-3210",
            "address": "456 Health Street",
            "details": "A non-profit organization focused on global healthcare."
        }

        # Assert that the to_dict method returns the correct dictionary
        ngo_dict = ngo.to_dict()
        self.assertEqual(ngo_dict["name"], expected_dict["name"])
        self.assertEqual(ngo_dict["email"], expected_dict["email"])
        self.assertEqual(ngo_dict["phone_no"], expected_dict["phone_no"])
        self.assertEqual(ngo_dict["address"], expected_dict["address"])
        self.assertEqual(ngo_dict["details"], expected_dict["details"])
        # Check that the generated ID is a valid UUID
        self.assertTrue(uuid.UUID(ngo_dict["id"], version=4))

    def test_from_dict(self):
        # Sample dictionary to convert to a NGO instance
        data_dict = {
            "id": str(uuid.uuid4()),
            "name": "Global Health Initiative",
            "email": "contact@ghi.org",
            "details": "A non-profit organization focused on global healthcare.",
            "phone_no": "987-654-3210",
            "address": "456 Health Street"
        }

        # Convert the dictionary to a NGO instance
        ngo = NGO.from_dict(data_dict)

        # Assert that the created NGO instance matches the dictionary values
        self.assertEqual(ngo.name, data_dict["name"])
        self.assertEqual(ngo.email, data_dict["email"])
        self.assertEqual(ngo.phone_no, data_dict["phone_no"])
        self.assertEqual(ngo.address, data_dict["address"])
        self.assertEqual(ngo.details, data_dict["details"])
        # Assert that the ID in the dictionary is the same as the one in the instance
        self.assertEqual(ngo.id, data_dict["id"])

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'phone_no')
        data_dict = {
            "name": "Global Health Initiative",
            "email": "contact@ghi.org",
            "details": "A non-profit organization focused on global healthcare.",
            "address": "456 Health Street"
        }

        # Assert that from_dict raises a TypeError because 'phone_no' is missing
        with self.assertRaises(TypeError):
            NGO.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
