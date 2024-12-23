import unittest
from app.utils.queries.query_generator import SQLiteQueryBuilder


class TestSQLiteQueryBuilder(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of SQLiteQueryBuilder"""
        self.builder = SQLiteQueryBuilder('users')

    def test_insert(self):
        """Test the INSERT query generation"""
        data = {'name': 'Alice', 'age': 30}
        result = self.builder.insert(data)
        expected_query = "INSERT INTO users (name, age) VALUES (?, ?)"
        expected_values = ('Alice', 30)
        self.assertEqual(result.query, expected_query)
        self.assertEqual(result.values, expected_values)

    def test_select(self):
        """Test the SELECT query generation without WHERE"""
        result = self.builder.select(['name', 'age'])
        expected_query = "SELECT name, age FROM users"
        expected_values = tuple()
        self.assertEqual(result.query, expected_query)
        self.assertEqual(result.values, expected_values)

    def test_select_with_where(self):
        """Test the SELECT query generation with WHERE"""
        where = {'name': 'Alice', 'age': 30}
        result = self.builder.select(['name', 'age'], where)
        expected_query = "SELECT name, age FROM users WHERE name = ? AND age = ?"
        expected_values = ('Alice', 30)
        self.assertEqual(result.query, expected_query)
        self.assertEqual(result.values, expected_values)

    def test_update(self):
        """Test the UPDATE query generation"""
        data = {'name': 'Alice', 'age': 31}
        where = {'name': 'Alice'}
        result = self.builder.update(data, where)
        expected_query = "UPDATE users SET name = ?, age = ? WHERE name = ?"
        expected_values = ('Alice', 31, 'Alice')
        self.assertEqual(result.query, expected_query)
        self.assertEqual(result.values, expected_values)

    def test_delete(self):
        """Test the DELETE query generation"""
        where = {'name': 'Alice'}
        result = self.builder.delete(where)
        expected_query = "DELETE FROM users WHERE name = ?"
        expected_values = ('Alice',)
        self.assertEqual(result.query, expected_query)
        self.assertEqual(result.values, expected_values)


# Run the tests
if __name__ == '__main__':
    unittest.main()