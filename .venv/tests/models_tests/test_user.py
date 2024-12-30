import unittest
from app.utils.enums.role import Role
from uuid import UUID
from app.models.user import User
import uuid


class TestUser(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample User instance
        user = User(
            name="John Doe",
            email="johndoe@example.com",
            password="securepassword",
            phone_no="987-654-3210",
            address="123 Elm Street"
        )

        # Expected dictionary representation of the User instance
        expected_dict = {
            "id": user.id,  # id should be dynamically generated
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "securepassword",
            "phone_no": "987-654-3210",
            "address": "123 Elm Street",
            "role": Role.DONOR.value  # Default role
        }

        # Assert that the to_dict method returns the correct dictionary
        user_dict = user.to_dict()

        self.assertEqual(user_dict["name"], expected_dict["name"])
        self.assertEqual(user_dict["email"], expected_dict["email"])
        self.assertEqual(user_dict["password"], expected_dict["password"])
        self.assertEqual(user_dict["phone_no"], expected_dict["phone_no"])
        self.assertEqual(user_dict["address"], expected_dict["address"])
        self.assertEqual(user_dict["role"], expected_dict["role"])

        # Check if the 'id' in the dictionary is a valid UUID
        self.assertIsInstance(UUID(user_dict["id"]), UUID)

    def test_from_dict(self):
        # Sample dictionary to convert to a User instance
        data_dict = {
            "id": str(uuid.uuid4()),
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "securepassword",
            "phone_no": "987-654-3210",
            "address": "123 Elm Street",
            "role": Role.DONOR.value
        }

        # Convert the dictionary to a User instance
        user = User.from_dict(data_dict)

        # Assert that the created User instance matches the dictionary values
        self.assertEqual(user.name, data_dict["name"])
        self.assertEqual(user.email, data_dict["email"])
        self.assertEqual(user.password, data_dict["password"])
        self.assertEqual(user.phone_no, data_dict["phone_no"])
        self.assertEqual(user.address, data_dict["address"])
        self.assertEqual(user.role, data_dict["role"])
        self.assertEqual(user.id, data_dict["id"])

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'phone_no')
        data_dict = {
            "id": str(uuid.uuid4()),
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "securepassword",
            "address": "123 Elm Street",
            "role": Role.DONOR.value
        }

        # Assert that from_dict raises a TypeError because 'phone_no' is missing
        with self.assertRaises(TypeError):
            User.from_dict(data_dict)

    def test_default_role(self):
        # Create a User with the default role (Role.DONOR.value)
        user = User(
            name="Jane Doe",
            email="janedoe@example.com",
            password="anotherpassword",
            phone_no="123-456-7890",
            address="456 Oak Street"
        )

        # Assert that the role is set to the default value (Role.DONOR.value)
        self.assertEqual(user.role, Role.DONOR.value)


if __name__ == '__main__':
    unittest.main()
