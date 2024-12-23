import unittest
from unittest import mock
from app.repositories.ngo_repository import NGORepository
from app.models.ngo import NGO
from app.utils.errors.custom_errors import DatabaseError, NotExistsError


class TestNGORepository(unittest.TestCase):
    def setUp(self):
        # Mock the database connection
        self.mock_db = mock.MagicMock()
        # Create the repository with the mock db
        self.ngo_repository = NGORepository(self.mock_db)
        # Mock the query builder
        self.ngo_repository.query_builder = mock.MagicMock()

        # Common test data
        self.test_ngo_data = {
            'id': 1,
            'name': 'Test NGO',
            'phone_no': '1234567890',
            'email': 'test@ngo.com',
            'details': 'Test Details',
            'address': 'Test Address'
        }

    def test_get_all_ngos_success(self):
        # Arrange
        mock_data = [
            {'id': 1, 'name': 'NGO 1', 'phone_no': '123', 'email': 'ngo1@email.com', 'details': 'Details 1',
             'address': 'Address 1'},
            {'id': 2, 'name': 'NGO 2', 'phone_no': '456', 'email': 'ngo2@email.com', 'details': 'Details 2',
             'address': 'Address 2'}
        ]

        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchall.return_value = mock_data

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act
            ngos = self.ngo_repository.get_all_ngos()

            # Assert
            self.assertEqual(len(ngos), 2)
            self.assertEqual(ngos[0].name, 'NGO 1')
            self.assertEqual(ngos[1].name, 'NGO 2')

    def test_get_all_ngos_empty(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchall.return_value = []

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act
            ngos = self.ngo_repository.get_all_ngos()

            # Assert
            self.assertEqual(len(ngos), 0)
            self.assertIsInstance(ngos, list)

    def test_get_all_ngos_database_error(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.get_all_ngos()

    def test_get_ngo_by_id_success(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [1])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchone.return_value = self.test_ngo_data

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act
            ngo = self.ngo_repository.get_ngo_by_id('1')

            # Assert
            self.assertEqual(ngo.id, 1)
            self.assertEqual(ngo.name, 'Test NGO')
            self.assertEqual(ngo.email, 'test@ngo.com')

    def test_get_ngo_by_id_not_exists(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [1])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchone.return_value = None

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            with self.assertRaises(NotExistsError):
                self.ngo_repository.get_ngo_by_id('1')

    def test_get_ngo_by_id_database_error(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', [1])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.get_ngo_by_id('1')

    def test_get_ngo_by_email_success(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', ['test@ngo.com'])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchone.return_value = self.test_ngo_data

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act
            ngo = self.ngo_repository.get_ngo_by_email('test@ngo.com')

            # Assert
            self.assertIsNotNone(ngo)
            self.assertEqual(ngo.email, 'test@ngo.com')

    def test_get_ngo_by_email_not_exists(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', ['test@ngo.com'])
        mock_cursor = mock.MagicMock()
        mock_cursor.fetchone.return_value = None

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act
            ngo = self.ngo_repository.get_ngo_by_email('test@ngo.com')

            # Assert
            self.assertIsNone(ngo)

    def test_get_ngo_by_email_database_error(self):
        # Arrange
        self.ngo_repository.query_builder.select.return_value = ('SELECT query', ['test@ngo.com'])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.get_ngo_by_email('test@ngo.com')

    def test_create_ngo_success(self):
        # Arrange
        test_ngo = NGO(**self.test_ngo_data)
        self.ngo_repository.query_builder.insert.return_value = ('INSERT query', [])
        mock_cursor = mock.MagicMock()

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            try:
                self.ngo_repository.create_ngo(test_ngo)
            except Exception as e:
                self.fail(f"create_ngo raised an unexpected exception: {e}")

    def test_create_ngo_database_error(self):
        # Arrange
        test_ngo = NGO(**self.test_ngo_data)
        self.ngo_repository.query_builder.insert.return_value = ('INSERT query', [])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.create_ngo(test_ngo)

    def test_delete_ngo_by_id_success(self):
        # Arrange
        self.ngo_repository.query_builder.delete.return_value = ('DELETE query', [1])
        mock_cursor = mock.MagicMock()
        mock_cursor.rowcount = 1

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            try:
                self.ngo_repository.delete_ngo_by_id('1')
            except Exception as e:
                self.fail(f"delete_ngo_by_id raised an unexpected exception: {e}")

    def test_delete_ngo_by_id_not_exists(self):
        # Arrange
        self.ngo_repository.query_builder.delete.return_value = ('DELETE query', [1])
        mock_cursor = mock.MagicMock()
        mock_cursor.rowcount = 0

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            with self.assertRaises(NotExistsError):
                self.ngo_repository.delete_ngo_by_id('1')

    def test_delete_ngo_by_id_database_error(self):
        # Arrange
        self.ngo_repository.query_builder.delete.return_value = ('DELETE query', [1])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.delete_ngo_by_id('1')

    def test_update_ngo_by_id_success(self):
        # Arrange
        test_ngo = NGO(**self.test_ngo_data)
        self.ngo_repository.query_builder.update.return_value = ('UPDATE query', [])
        mock_cursor = mock.MagicMock()
        mock_cursor.rowcount = 1

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            try:
                self.ngo_repository.update_ngo_by_id(test_ngo)
            except Exception as e:
                self.fail(f"update_ngo_by_id raised an unexpected exception: {e}")

    def test_update_ngo_by_id_not_exists(self):
        # Arrange
        test_ngo = NGO(**self.test_ngo_data)
        self.ngo_repository.query_builder.update.return_value = ('UPDATE query', [])
        mock_cursor = mock.MagicMock()
        mock_cursor.rowcount = 0

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query', return_value=mock_cursor):
            # Act & Assert
            with self.assertRaises(NotExistsError):
                self.ngo_repository.update_ngo_by_id(test_ngo)

    def test_update_ngo_by_id_database_error(self):
        # Arrange
        test_ngo = NGO(**self.test_ngo_data)
        self.ngo_repository.query_builder.update.return_value = ('UPDATE query', [])

        with mock.patch('app.utils.queries.query_executor.SQLiteQueryExecutor.execute_query',
                        side_effect=Exception('Database error')):
            # Act & Assert
            with self.assertRaises(DatabaseError):
                self.ngo_repository.update_ngo_by_id(test_ngo)


if __name__ == '__main__':
    unittest.main()