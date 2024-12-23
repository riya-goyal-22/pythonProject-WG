import unittest
from unittest.mock import MagicMock
import sqlite3
from typing import Tuple
from app.utils.queries.query_executor import SQLiteQueryExecutor


class TestSQLiteQueryExecutor(unittest.TestCase):

    def setUp(self):
        """Set up mock connection and cursor for each test"""
        self.conn = MagicMock(spec=sqlite3.Connection)
        self.cursor = MagicMock(spec=sqlite3.Cursor)
        self.conn.cursor.return_value = self.cursor

    def test_execute_query(self):
        """Test the execute_query method"""

        # Define query and parameters
        query = "SELECT * FROM users WHERE id = ?"
        params = (1,)

        # Call execute_query method
        result_cursor = SQLiteQueryExecutor.execute_query(self.conn, query, params)

        # Check that the cursor's execute method was called correctly
        self.conn.cursor.assert_called_once()
        self.cursor.execute.assert_called_once_with(query, params)

        # Check if execute_query returns the cursor
        self.assertEqual(result_cursor, self.cursor)

    def test_execute_query_with_no_params(self):
        """Test the execute_query method with no parameters"""

        # Define query and no parameters
        query = "SELECT * FROM users"
        params = ()

        # Call execute_query method
        result_cursor = SQLiteQueryExecutor.execute_query(self.conn, query, params)

        # Check that the cursor's execute method was called correctly
        self.conn.cursor.assert_called_once()
        self.cursor.execute.assert_called_once_with(query, params)

        # Check if execute_query returns the cursor
        self.assertEqual(result_cursor, self.cursor)

    def test_execute_query_with_invalid_query(self):
        """Test the execute_query method with an invalid query"""

        # Define an invalid query
        query = "SELECT * FROM non_existent_table"
        params = ()

        # Simulate the exception raised by the SQLite cursor on failure
        self.cursor.execute.side_effect = sqlite3.OperationalError("no such table: non_existent_table")

        # Call execute_query and check for the exception
        with self.assertRaises(sqlite3.OperationalError):
            SQLiteQueryExecutor.execute_query(self.conn, query, params)

    def test_execute_query_with_multiple_params(self):
        """Test the execute_query method with multiple parameters"""

        # Define query and multiple parameters
        query = "UPDATE users SET name = ?, age = ? WHERE id = ?"
        params = ('Alice', 30, 1)

        # Call execute_query method
        result_cursor = SQLiteQueryExecutor.execute_query(self.conn, query, params)

        # Check that the cursor's execute method was called correctly
        self.conn.cursor.assert_called_once()
        self.cursor.execute.assert_called_once_with(query, params)

        # Check if execute_query returns the cursor
        self.assertEqual(result_cursor, self.cursor)


# Run the tests
if __name__ == '__main__':
    unittest.main()
