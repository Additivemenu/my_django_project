I'll introduce you to the key concepts in pytest that are essential for understanding and writing effective tests.





# Key Concepts in pytest

## 1. Test Functions and Files
- Test files should start with `test_` or end with `_test.py`
- Test functions/methods should start with `test_`
- Test class names should start with `Test`

```python
# test_example.py
def test_simple_addition():
    assert 1 + 1 == 2

class TestCalculator:
    def test_multiplication(self):
        assert 2 * 3 == 6
```

## 2. Assertions
pytest uses Python's built-in `assert` statement for verifications:

```python
def test_assertions():
    # Simple assertion
    assert True

    # Equality
    assert 1 + 1 == 2

    # In/Not In
    assert "hello" in "hello world"

    # Compare types
    assert isinstance("hello", str)

    # Exceptions
    with pytest.raises(ValueError):
        int("not a number")
```

## 3. Fixtures
Fixtures are functions that provide test data or test dependencies. They are marked with the `@pytest.fixture` decorator.

```python
import pytest

@pytest.fixture
def sample_data():
    return {
        'name': 'John',
        'age': 30
    }

def test_name(sample_data):
    assert sample_data['name'] == 'John'
```

### Fixture Scopes
- `scope="function"`: Run once per test function (default)
- `scope="class"`: Run once per test class
- `scope="module"`: Run once per module
- `scope="session"`: Run once per test session

```python
@pytest.fixture(scope="module")
def database_connection():
    db = connect_to_db()
    yield db
    db.close()
```

## 4. Markers
Markers are used to label tests and customize their behavior:

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    # This test is marked as slow
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6)
])
def test_multiplication(input, expected):
    assert input * 2 == expected
```

Common built-in markers:
- `@pytest.mark.skip`: Skip a test
- `@pytest.mark.skipif`: Skip conditionally
- `@pytest.mark.parametrize`: Run a test multiple times with different inputs
- `@pytest.mark.xfail`: Mark test as expected to fail

## 5. Parameterization
Run the same test with different inputs:

```python
@pytest.mark.parametrize("test_input,expected", [
    ("hello", 5),
    ("world", 5),
    ("pytest", 6)
])
def test_string_length(test_input, expected):
    assert len(test_input) == expected
```

## 6. conftest.py
Shared fixtures can be placed in a `conftest.py` file to make them available to all tests:

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def app_config():
    return {
        'API_URL': 'http://api.example.com',
        'API_KEY': 'test_key'
    }
```

## 7. Command Line Options
Common pytest commands:
```bash
# Run all tests
pytest

# Run specific test file -> actually you need to provide path to that file as well
pytest test_file.py

# Run specific test
pytest test_file.py::test_function

# Run marked tests
pytest -m slow

# Show print statements
pytest -s

# Verbose output
pytest -v

# Stop after first failure
pytest -x
```

## 8. Django-specific Features
When using pytest with Django:

```python
# Mark test as needing database access
@pytest.mark.django_db
def test_database_operation():
    User.objects.create(username="test")
    assert User.objects.count() == 1

# Client fixture for testing views
def test_view(client):
    response = client.get("/")
    assert response.status_code == 200

# RF (RequestFactory) fixture
def test_view_unit(rf):
    request = rf.get("/")
    response = MyView.as_view()(request)
    assert response.status_code == 200
```

## Best Practices
1. Keep tests simple and focused
2. Use descriptive test names
3. Follow the Arrange-Act-Assert pattern
4. Use fixtures for setup and teardown
5. Group related tests in classes
6. Use meaningful assert messages
7. Don't test implementation details

Example of a well-structured test:
```python
class TestUserRegistration:
    @pytest.fixture
    def valid_user_data(self):
        return {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123"
        }

    @pytest.mark.django_db
    def test_user_registration_success(self, valid_user_data, client):
        # Arrange
        assert User.objects.count() == 0
        
        # Act
        response = client.post("/register/", valid_user_data)
        
        # Assert
        assert response.status_code == 201
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == valid_user_data["username"]
```


These are the fundamental concepts in pytest. Would you like me to elaborate on any particular concept or provide more examples for specific use cases? For instance, I could:

1. Show more examples of fixture usage
2. Demonstrate more complex test scenarios
3. Explain more about Django-specific testing features
4. Show how to handle async tests
5. Explain test organization strategies