import unittest

from app.models.user_dto import User_DTO


class TestUserDTO(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample User_DTO instance
        user_dto = User_DTO(
            id="12345",
            name="John Doe",
            address="123 Elm Street",
            email="johndoe@example.com",
            phone_no="987-654-3210",
            role="admin"
        )

        # Expected dictionary representation of the User_DTO instance
        expected_dict = {
            'id': "12345",
            'name': "John Doe",
            'address': "123 Elm Street",
            'email': "johndoe@example.com",
            'phone_no': "987-654-3210",
            'role': "admin"
        }

        # Assert that the to_dict method returns the correct dictionary
        self.assertEqual(user_dto.to_dict(), expected_dict)

    def test_from_dict(self):
        # Sample dictionary to convert to a User_DTO instance
        data_dict = {
            'id': "12345",
            'name': "John Doe",
            'address': "123 Elm Street",
            'email': "johndoe@example.com",
            'phone_no': "987-654-3210",
            'role': "admin"
        }

        # Convert the dictionary to a User_DTO instance
        user_dto = User_DTO.from_dict(data_dict)

        # Assert that the created User_DTO instance matches the dictionary values
        self.assertEqual(user_dto.id, data_dict['id'])
        self.assertEqual(user_dto.name, data_dict['name'])
        self.assertEqual(user_dto.address, data_dict['address'])
        self.assertEqual(user_dto.email, data_dict['email'])
        self.assertEqual(user_dto.phone_no, data_dict['phone_no'])
        self.assertEqual(user_dto.role, data_dict['role'])

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'phone_no')
        data_dict = {
            'id': "12345",
            'name': "John Doe",
            'address': "123 Elm Street",
            'email': "johndoe@example.com",
            'role': "admin"
        }

        # Assert that from_dict raises a TypeError because 'phone_no' is missing
        with self.assertRaises(TypeError):
            User_DTO.from_dict(data_dict)

    def test_default_role(self):
        # Create a User_DTO instance with all fields, but we add default value for role.
        data_dict = {
            'id': "12345",
            'name': "John Doe",
            'address': "123 Elm Street",
            'email': "johndoe@example.com",
            'phone_no': "987-654-3210"
        }

        # Assert that the role is correctly assigned from the dictionary (if provided)
        with self.assertRaises(TypeError):
            User_DTO.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
