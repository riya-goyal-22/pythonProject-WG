from logging import raiseExceptions

import pytest
from unittest import mock
from app.models.user import User
from app.utils.errors.custom_errors import DatabaseError, NotExistsError
from app.repositories.user_repository import UserRepository


@pytest.fixture
def mock_db():
    # Fixture to create a mock database connection
    return mock.MagicMock()


@pytest.fixture
def user_data():
    # Fixture to provide sample user data
    return User(id="1", name="John Doe", email="johndoe@example.com", password="password123",
                phone_no="1234567890", address="123 Main St", role="user")


@pytest.fixture
def repository(mock_db):
    # Fixture to provide an instance of UserRepository with a mock database
    return UserRepository(mock_db)


@pytest.fixture
def mock_execute_query():
    # Fixture to mock the SQLiteQueryExecutor.execute_query method
    with mock.patch('app.repositories.user_repository.SQLiteQueryExecutor.execute_query') as mock_execute_query:
        yield mock_execute_query


@pytest.fixture
def mock_select():
    # Fixture to mock the SQLiteQueryBuilder.select method
    with mock.patch('app.repositories.user_repository.SQLiteQueryBuilder.select') as mockk:
        yield mockk


@pytest.fixture
def mock_insert():
    # Fixture to mock the SQLiteQueryBuilder.insert method
    with mock.patch('app.repositories.user_repository.SQLiteQueryBuilder.insert') as mockk:
        yield mockk


def test_create_user_success(repository, mock_db, mock_insert, mock_execute_query, user_data):
    # Mocking the insert query and execution
    mock_insert.return_value = ("INSERT INTO users", {'id': "1", 'name': "John Doe", 'email': "johndoe@example.com"})
    mock_execute_query.return_value = None

    # Run the test
    repository.create_user(user_data)

    # Assert if the query was executed using unittest assertions
    mock_insert.assert_called_once()
    mock_execute_query.assert_called_once()


def test_create_user_failure(repository, mock_db, mock_insert, mock_execute_query, user_data):
    # Simulating an exception during query execution
    mock_insert.return_value = ("INSERT INTO users", {'id': "1", 'name': "John Doe", 'email': "johndoe@example.com"})
    mock_execute_query.side_effect = Exception("Database error")

    # Run the test and assert exception using pytest's.raises
    with pytest.raises(DatabaseError):
        repository.create_user(user_data)


def test_get_user_by_id_success(repository, mock_db, mock_select, mock_execute_query, user_data):
    # Mock user data for the response
    user_data_dict = {'id': "1", 'name': "John Doe", 'email': "johndoe@example.com", 'password': "password123",
                      'phone_no': "1234567890", 'address': "123 Main St", 'role': "user"}

    mock_cursor = mock.MagicMock()
    mock_cursor.fetchone.return_value = user_data_dict
    mock_execute_query.return_value = mock_cursor

    # Mocking the select query
    mock_select.return_value = ("SELECT * FROM users", {'id': "1"})

    # Run the test
    user = repository.get_user_by_id("1")

    # Assert user is returned correctly using pytest's assert
    assert user.id == "1"
    assert user.name == "John Doe"
    mock_execute_query.assert_called_once()


def test_get_user_by_id_not_found(repository, mock_db, mock_select, mock_execute_query):
    # Simulate no user found
    mock_cursor = mock.MagicMock()
    mock_cursor.fetchone.return_value = None  # No user found
    mock_execute_query.return_value = mock_cursor

    # Mocking the select query
    mock_select.return_value = ("SELECT * FROM users", {'id': "2"})

    # Run the test
    with pytest.raises(NotExistsError):
        user = repository.get_user_by_id("2")

    # Assert that no user is returned
    mock_execute_query.assert_called_once()


def test_get_user_by_email_success(repository, mock_db, mock_select, mock_execute_query, user_data):
    # Mock user data for the response
    user_data_dict = {'id': "1", 'name': "John Doe", 'email': "johndoe@example.com", 'password': "password123",
                      'phone_no': "1234567890", 'address': "123 Main St", 'role': "user"}

    mock_cursor = mock.MagicMock()
    mock_cursor.fetchone.return_value = user_data_dict
    mock_execute_query.return_value = mock_cursor

    # Mocking the select query
    mock_select.return_value = ("SELECT * FROM users", {'email': "johndoe@example.com"})

    # Run the test
    user = repository.get_user_by_email("johndoe@example.com")

    # Assert user is returned correctly
    assert user.id == "1"
    assert user.email == "johndoe@example.com"
    mock_execute_query.assert_called_once()


def test_get_user_by_email_not_found(repository, mock_db, mock_select, mock_execute_query):
    # Simulate no user found
    mock_cursor = mock.MagicMock()
    mock_cursor.fetchone.return_value = None  # No user found
    mock_execute_query.return_value = mock_cursor

    # Mocking the select query
    mock_select.return_value = ("SELECT * FROM users", {'email': "notfound@example.com"})

    # Run the test
    user = repository.get_user_by_email("notfound@example.com")

    # Assert that no user is returned
    assert user is None
    mock_execute_query.assert_called_once()
