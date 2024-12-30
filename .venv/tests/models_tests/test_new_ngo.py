import unittest
from app.models.new_ngo import NewNGO


class TestNewNGO(unittest.TestCase):

    def test_to_dict(self):
        # Create a sample NewNGO instance
        ngo = NewNGO(
            name="Helping Hands",
            address="123 Charity Lane",
            phone_no="123-456-7890",
            email="contact@helpinghands.org",
            details="Non-profit organization focused on education and healthcare"
        )

        # Expected dictionary representation of the NewNGO instance
        expected_dict = {
            'name': "Helping Hands",
            'email': "contact@helpinghands.org",
            'details': "Non-profit organization focused on education and healthcare",
            'address': "123 Charity Lane",
            'phone_no': "123-456-7890"
        }

        # Assert that the to_dict method returns the correct dictionary
        self.assertEqual(ngo.to_dict(), expected_dict)

    def test_from_dict(self):
        # Sample dictionary to convert to a NewNGO instance
        data_dict = {
            'name': "Helping Hands",
            'email': "contact@helpinghands.org",
            'details': "Non-profit organization focused on education and healthcare",
            'address': "123 Charity Lane",
            'phone_no': "123-456-7890"
        }

        # Convert the dictionary to a NewNGO instance
        ngo = NewNGO.from_dict(data_dict)

        # Assert that the created NewNGO instance matches the dictionary values
        self.assertEqual(ngo.name, "Helping Hands")
        self.assertEqual(ngo.email, "contact@helpinghands.org")
        self.assertEqual(ngo.details, "Non-profit organization focused on education and healthcare")
        self.assertEqual(ngo.address, "123 Charity Lane")
        self.assertEqual(ngo.phone_no, "123-456-7890")

    def test_from_dict_missing_key(self):
        # Sample dictionary missing a key (e.g., 'phone_no')
        data_dict = {
            'name': "Helping Hands",
            'email': "contact@helpinghands.org",
            'details': "Non-profit organization focused on education and healthcare",
            'address': "123 Charity Lane"
        }

        # Assert that from_dict raises a TypeError because 'phone_no' is missing
        with self.assertRaises(TypeError):
            NewNGO.from_dict(data_dict)


if __name__ == '__main__':
    unittest.main()
