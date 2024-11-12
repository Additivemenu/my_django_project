# test_user_service.py
import pytest
from unittest.mock import Mock, patch
from .database import DatabaseConnection
from .user_service import UserService

@pytest.fixture
def mock_db():
    """
    !Fixture that provides a mock database connection instance, since we want to perform test for user_service, we need to mock its dependencies
    !see a more complex example in my_aws_app where we use magic mock to mock boto3 client
    
    This fixture does 3 main things:
    1. `@pytest.fixture` tells pytest "this is a fixture function that will run before any test that requests it
    
    2. `mock = Mock(spec=DatabaseConnection)` creates a fake (mock) version of the DatabaseConnection class:
        !It's like creating a placeholder that has all the same methods as DatabaseConnection
        By using spec=DatabaseConnection, it ensures this mock only allows methods that exist in the real DatabaseConnection class
        If you try to call a method that doesn't exist in DatabaseConnection, it will raise an error

    3. `mock.is_connected = True` sets a default property on the mock:

    This makes the mock pretend it's already connected to the database
    Any test using this mock will see is_connected as True unless they change it
    """
    mock = Mock(spec=DatabaseConnection)
    mock.is_connected = True
    return mock

@pytest.fixture
def user_service(mock_db):
    """Fixture that provides a UserService instance with a mock database"""
    return UserService(mock_db)

@pytest.fixture
def mock_db_with_user(mock_db):
    """Fixture that provides a mock database pre-configured with a test user"""
    mock_db.execute_query.return_value = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"}
    ]
    return mock_db

@pytest.fixture
def mock_db_empty(mock_db):
    """Fixture that provides a mock database configured to return no results"""
    mock_db.execute_query.return_value = []
    return mock_db

@pytest.fixture
def mock_db_disconnected(mock_db):
    """Fixture that provides a mock database in disconnected state"""
    mock_db.is_connected = False
    mock_db.execute_query.side_effect = ConnectionError("Not connected to database")
    return mock_db

def test_get_user_email(user_service, mock_db_with_user):
    # Test the get_user_email method
    email = user_service.get_user_email(1)
    
    # Assertions
    assert email == "john@example.com"
    mock_db_with_user.execute_query.assert_called_once_with(
        "SELECT * FROM users WHERE id = %s", 
        [1]
    )

def test_get_user_email_not_found(mock_db_empty):
    # Create service with empty database mock
    user_service = UserService(mock_db_empty)
    
    # Test that ValueError is raised when user is not found
    with pytest.raises(ValueError) as exc_info:
        user_service.get_user_email(999)
    
    assert str(exc_info.value) == "User with id 999 not found"
    mock_db_empty.execute_query.assert_called_once_with(
        "SELECT * FROM users WHERE id = %s",
        [999]
    )

def test_database_not_connected(mock_db_disconnected):
    # Create service with disconnected database mock
    user_service = UserService(mock_db_disconnected)
    
    # Test that ConnectionError is raised when database is not connected
    with pytest.raises(ConnectionError) as exc_info:
        user_service.get_user_email(1)
    
    assert str(exc_info.value) == "Not connected to database"





# Example of fixture composition and parameterization
@pytest.fixture
def mock_db_with_custom_user(mock_db):
    """Fixture factory that creates a mock DB with custom user data"""
    def _mock_db_with_custom_user(user_data):
        mock_db.execute_query.return_value = [user_data]
        return mock_db
    return _mock_db_with_custom_user

@pytest.mark.parametrize("user_data", [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
])
def test_get_user_email_parameterized(mock_db_with_custom_user, user_data):
    # Create mock DB with specific user data
    mock_db = mock_db_with_custom_user(user_data)
    user_service = UserService(mock_db)
    
    # Test the get_user_email method
    email = user_service.get_user_email(user_data["id"])
    
    # Assertions
    assert email == user_data["email"]
    mock_db.execute_query.assert_called_once_with(
        "SELECT * FROM users WHERE id = %s", 
        [user_data["id"]]
    )